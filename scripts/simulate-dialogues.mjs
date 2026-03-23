#!/usr/bin/env node
/**
 * simulate-dialogues.mjs
 * Simulates every game phase and checks which dialogue fires for each NPC.
 * Run with: node scripts/simulate-dialogues.mjs
 *
 * Issues are printed as ❌. A clean run prints only ✓ rows.
 */

import { readFileSync } from 'fs';
const dialogue = JSON.parse(readFileSync('src/data/dialogue.json', 'utf8'));

// ── Dialogue resolution (mirrors DialogueSystem.resolveDialogueId) ────────────
function resolve(npc, flags) {
  const entries = Object.entries(dialogue)
    .filter(([, v]) => v.npc === npc)
    .sort((a, b) => (b[1].priority ?? 0) - (a[1].priority ?? 0));

  for (const [id, node] of entries) {
    const conds = node.conditions?.flags ?? {};
    const matches = Object.entries(conds).every(([k, expected]) => {
      const actual = flags[k] ?? false;
      return actual === expected;
    });
    if (matches) return id;
  }
  return null;
}

// ── Game phases (flags accumulate monotonically) ──────────────────────────────
// Each phase is the COMPLETE set of flags that are true at that point.
// Built cumulatively so it mirrors flagBridge output at each moment.

const P = (...objs) => Object.assign({}, ...objs);

const F = {
  // Delivery
  met_yusuf: { met_yusuf: true },
  delivery_accepted: { delivery_accepted: true, delivery_packages_received: true },
  pkg137: { delivered_137: true },
  pkg170: { delivered_170: true, met_fatima: true },   // delivering to Fatima triggers met_fatima
  pkg284: { delivered_284: true },
  delivery_done: { delivery_done: true },
  // Fabric
  fabric_accepted: { fabric_quest_accepted: true, knows_stunt_location: true },
  fabric_active: { stunt_quest_active: true },
  fabric_done: { stunt_quest_done: true, has_community_trust: true },
  // Flour — accumulative: done implies asked+accepted too (matches flagBridge)
  flour_asked: { omar_flour_asked: true, flour_quest_accepted: true },
  has_flour:   { has_flour: true },
  flour_done:  { omar_flour_done: true, knows_samen_tafel: true,
                 omar_flour_asked: true, flour_quest_accepted: true },
  // Oud
  oud_accepted: { oud_quest_accepted: true },
  oud_found: { has_oud_string_item: true },
  oud_done: { reza_quest_done: true },
  // Signatures
  sig_fatima: { sig_fatima: true },
  sig_omar: { sig_omar: true },
  sig_reza: { sig_reza: true },
  sig_baert: { sig_baert: true },
  sig_aziz: { sig_aziz: true, met_aziz: true },
  sigs_done: { speculator_threatened: true },
  // Bulldozer / De Roma / Geest / Mayor
  de_roma: { visited_de_roma: true },
  bulldozer: { has_permit_doc: true },
  geest_enc: { geest_encountered: true },
  geest_done: { kracht_van_gemeenschap: true },
  met_mayor: { met_mayor: true, act4_briefed: true },
  mayor_brief: { act4_started: true },
  // Factions
  fac_moroccan: { fatima_convinced: true },
  fac_turkish:  { tine_faction_convinced: true },
  fac_flemish:  { baert_faction_convinced: true },
};

// Phases: [name, flags, {npc: expectedDialogueId}]
const phases = [

  // ─── Act 0: Fresh start ──────────────────────────────────────────────────
  { name: 'NEW_GAME',
    flags: {},
    expect: {
      yusuf:    'yusuf_delivery',
      fatima:   'fatima_intro',         // should get intro, NOT fabric dialogue
      omar:     'omar_bakker',
      reza:     'reza_music',
      aziz:     'reuzenpoort_legend',
      baert:    'stunt_baert',
    }
  },

  // ─── Act 1: Yusuf introduces himself ────────────────────────────────────
  { name: 'MET_YUSUF',
    flags: P(F.met_yusuf),
    expect: {
      yusuf:  'yusuf_delivery',
    }
  },

  // ─── Act 1: Delivery accepted, no packages done ──────────────────────────
  { name: 'DELIVERY_ACCEPTED',
    flags: P(F.met_yusuf, F.delivery_accepted),
    expect: {
      yusuf:  'yusuf_delivery',        // fallback — "go deliver"
      fatima: 'fatima_intro',          // shouldn't know her yet
    }
  },

  // ─── Act 1: pkg137 done (Baert boutique) ────────────────────────────────
  { name: 'PKG137_DONE',
    flags: P(F.met_yusuf, F.delivery_accepted, F.pkg137),
    expect: {
      yusuf:  'yusuf_delivery',
      baert:  'stunt_baert',           // no quest from Baert yet
    }
  },

  // ─── Act 1: pkg170 done (met Fatima at the patisserie) ──────────────────
  { name: 'PKG170_DONE',
    flags: P(F.met_yusuf, F.delivery_accepted, F.pkg137, F.pkg170),
    expect: {
      yusuf:  'yusuf_delivery',
      fatima: 'fatima_intro',          // met her, but no fabric quest yet
      baert:  'stunt_baert',
    }
  },

  // ─── Act 1: All packages done, back to Yusuf ────────────────────────────
  { name: 'ALL_PKGS_DONE',
    flags: P(F.met_yusuf, F.delivery_accepted, F.pkg137, F.pkg170, F.pkg284),
    expect: {
      yusuf:  'yusuf_delivery_done',   // "all done, come get reward"
      fatima: 'fatima_intro',
    }
  },

  // ─── Act 1: Delivery rewarded ───────────────────────────────────────────
  { name: 'DELIVERY_DONE',
    flags: P(F.met_yusuf, F.delivery_accepted, F.pkg137, F.pkg170, F.pkg284, F.delivery_done, F.met_fatima ? {} : {}),
    expect: {
      yusuf:  'yusuf_done',
      fatima: 'fatima_intro',          // delivery done, fabric quest not accepted yet
    }
  },

  // ─── Act 1→2: Fatima's fabric quest accepted ────────────────────────────
  { name: 'FABRIC_QUEST_ACCEPTED',
    flags: P(F.met_yusuf, F.delivery_accepted, F.pkg137, F.pkg170, F.pkg284, F.delivery_done,
             { met_fatima: true }, F.fabric_accepted),
    expect: {
      fatima: 'fatima_fabric_accept',  // "go get fabric from Baert at #137"
      baert:  'stunt_baert_fabric',    // "of course, I set some aside"
      yusuf:  'yusuf_done',
    }
  },

  // ─── Act 1→2: Carrying the fabric (picked up from Baert) ────────────────
  { name: 'FABRIC_PICKED_UP',
    flags: P(F.met_yusuf, F.delivery_accepted, F.pkg137, F.pkg170, F.pkg284, F.delivery_done,
             { met_fatima: true }, F.fabric_accepted, F.fabric_active),
    expect: {
      fatima: 'fatima_after_fabric',   // wait for fabric delivery
      baert:  'stunt_baert',           // gave the fabric, fallback
    }
  },

  // ─── Act 2: Fabric delivered → trust unlocked ───────────────────────────
  { name: 'FABRIC_DELIVERED',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done),
    expect: {
      fatima:   'fatima_signature',     // "sign the petition!"
      baert:    'stunt_baert_signature',
      omar:     'omar_flour_request',   // hasn't asked for flour yet → asks now
      reza:     'reza_music',           // oud quest not accepted yet → reza offers it here
    }
  },

  // ─── Act 2: Flour quest accepted (Omar asked) ───────────────────────────
  { name: 'FLOUR_ACCEPTED',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done, F.flour_asked),
    expect: {
      omar:   'omar_flour_thanks',     // "Budget Market, go get it"
      fatima: 'fatima_signature',
    }
  },

  // ─── Act 2: Has flour, back to Omar ─────────────────────────────────────
  { name: 'HAS_FLOUR',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done, F.flour_asked, F.has_flour),
    expect: {
      omar:   'omar_flour_done',       // player delivers flour
      fatima: 'fatima_signature',
    }
  },

  // ─── Act 2: Flour delivered ──────────────────────────────────────────────
  { name: 'FLOUR_DONE',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done, F.flour_asked, F.flour_done),
    expect: {
      omar:   'omar_signature',        // now sign the petition
      fatima: 'fatima_signature',
    }
  },

  // ─── Act 2: Oud quest accepted (Reza asked), flour also done ────────────
  { name: 'OUD_ACCEPTED',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done, F.flour_done, F.oud_accepted),
    expect: {
      reza:   'reza_oud_accept',       // "go to Aziz for string"
      aziz:   'aziz_oud_string',       // "I have a string!"
      omar:   'omar_signature',        // flour done → ready to sign
      fatima: 'fatima_signature',
    }
  },

  // ─── Act 2: Found oud string at Aziz, flour also done ───────────────────
  { name: 'OUD_FOUND',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done, F.flour_done, F.oud_accepted, F.oud_found),
    expect: {
      reza:   'reza_oud_found',        // "the string! perfect."
      aziz:   'aziz_signature',        // string given → Aziz offers signature
      omar:   'omar_signature',
      fatima: 'fatima_signature',
    }
  },

  // ─── Act 2: Oud delivered to Reza, flour also done ──────────────────────
  { name: 'OUD_DONE',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_accepted, F.fabric_done, F.flour_done, F.oud_accepted, F.oud_done),
    expect: {
      reza:   'reza_signature',        // now sign the petition
      aziz:   'aziz_signature',        // string delivered → Aziz signs
      omar:   'omar_signature',
      fatima: 'fatima_signature',
    }
  },

  // ─── Act 2: All pre-sig quests done, collecting signatures ──────────────
  { name: 'COLLECTING_SIGS_0',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_done, F.flour_done, F.oud_done),
    expect: {
      fatima: 'fatima_signature',
      baert:  'stunt_baert_signature',
      omar:   'omar_signature',        // flour_done accumulates omar_flour_asked=true
      reza:   'reza_signature',
      aziz:   'aziz_signature',
    }
  },

  // ─── Act 2: Fatima signed ───────────────────────────────────────────────
  { name: 'SIG_FATIMA_DONE',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_done, F.flour_done, F.oud_done, F.sig_fatima),
    expect: {
      fatima: 'fatima_nora_wedding',   // now can talk about wedding memory
      baert:  'stunt_baert_signature',
      omar:   'omar_signature',
      reza:   'reza_signature',
      aziz:   'aziz_signature',
    }
  },

  // ─── Act 2: All signatures done → speculator threatened (no mayor yet) ──
  { name: 'ALL_SIGS_DONE',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_done, F.flour_done, F.oud_done,
             F.sig_fatima, F.sig_omar, F.sig_reza, F.sig_baert, F.sig_aziz, F.sigs_done),
    expect: {
      fatima: 'fatima_nora_wedding',   // sig done, no mayor yet → wedding memory
      baert:  'stunt_baert',           // sig done, mayor not met → fallback
      omar:   'omar_bakker',            // sig_omar=true → signature node fails → falls to bakker intro
      reza:   'reza_done',
      aziz:   'reuzenpoort_legend',    // sig done, all oud done → fallback (prio 0)
    }
  },

  // ─── Act 3: De Roma visited → fight speculator ───────────────────────────
  { name: 'DE_ROMA_VISITED',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_done, F.flour_done, F.oud_done,
             F.sig_fatima, F.sig_omar, F.sig_reza, F.sig_baert, F.sig_aziz, F.sigs_done,
             F.de_roma),
    expect: {}
  },

  // ─── Act 3: Bulldozer defeated (permit obtained) ─────────────────────────
  { name: 'BULLDOZER_DONE',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_done, F.flour_done, F.oud_done,
             F.sig_fatima, F.sig_omar, F.sig_reza, F.sig_baert, F.sig_aziz, F.sigs_done,
             F.de_roma, F.bulldozer),
    expect: {}
  },

  // ─── Act 3→4: Met mayor ─────────────────────────────────────────────────
  { name: 'MET_MAYOR',
    flags: P(F.met_yusuf, F.delivery_done, { met_fatima: true },
             F.fabric_done, F.flour_done, F.oud_done,
             F.sig_fatima, F.sig_omar, F.sig_reza, F.sig_baert, F.sig_aziz, F.sigs_done,
             F.de_roma, F.bulldozer, F.geest_done, F.met_mayor),
    expect: {
      baert:  'stunt_baert_faction',
      tine:   'tine_faction',
      fatima: 'fatima_faction',
      omar:   'omar_samen_tafel_prep',
    }
  },
];

// ── Run simulation ─────────────────────────────────────────────────────────────

let issues = 0;

for (const phase of phases) {
  const expected = phase.expect ?? {};
  const npcs = Object.keys(expected);
  if (npcs.length === 0) continue;

  console.log(`\n── ${phase.name} ${'─'.repeat(Math.max(0, 50 - phase.name.length))}`);

  // Also check all NPCs that have dialogue
  const allNpcs = [...new Set([...npcs,
    'yusuf','fatima','omar','reza','aziz','baert','tine','hamza','lotte','bram','el_osri'
  ])];

  for (const npc of allNpcs) {
    const actual = resolve(npc, phase.flags);
    const exp    = expected[npc];

    if (exp !== undefined && actual !== exp) {
      console.log(`  ❌ ${npc.padEnd(8)} got=${actual}  want=${exp}`);
      issues++;
    } else if (exp !== undefined) {
      console.log(`  ✓  ${npc.padEnd(8)} ${actual}`);
    } else {
      // Just informational — no expected value set, show what fires
      console.log(`     ${npc.padEnd(8)} ${actual}`);
    }
  }
}

console.log(`\n${'═'.repeat(60)}`);
if (issues === 0) {
  console.log('✅ All checked phases pass!');
} else {
  console.log(`❌ ${issues} issue(s) found — fix dialogue.json priority guards.`);
}
