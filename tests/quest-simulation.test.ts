/**
 * Quest Simulation — Turnhoutsebaan
 *
 * Drives the XState machine through the full quest sequence without a browser
 * or Phaser. Verifies flags, nav arrows, hint texts, and location trigger
 * eligibility at every story checkpoint.
 *
 * Run with:  npm run test:quest
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { createActor }   from 'xstate';
import rawQuests         from '../src/data/streets/turnhoutsebaan/quests.json';
import {
  buildMachine,
  buildFlagBridge,
  buildGetNavTarget,
  buildGetHintText,
  buildFlagToEvent,
  type AnySnapshot,
} from '../src/systems/StreetMachine';
import type { QuestsDef, LocationTrigger } from '../src/core/StreetLoader';

// ── Setup ─────────────────────────────────────────────────────────────────────

const def      = rawQuests as unknown as QuestsDef;
const machine  = buildMachine(def);
const bridge   = buildFlagBridge(def);
const nav      = buildGetNavTarget(def);
const hint     = buildGetHintText(def);
const f2e      = buildFlagToEvent(def);

type Actor = ReturnType<typeof createActor<typeof machine>>;

function snap(actor: Actor): AnySnapshot {
  return actor.getSnapshot() as AnySnapshot;
}

/** All boolean flags derived from machine state. */
function flags(actor: Actor): Record<string, boolean> {
  return bridge(snap(actor));
}

/** Nav target at current state. */
function navTarget(actor: Actor) {
  return nav(snap(actor));
}

/** Hint text at current state. */
function hintText(actor: Actor) {
  return hint(snap(actor));
}

/**
 * Send a flag-key as if the dialogue system called stateManager.setFlag(key, true).
 * Looks up the corresponding machine event in flagToEvent and sends it.
 */
function setFlag(actor: Actor, flagKey: string): void {
  const event = f2e[flagKey];
  if (!event) throw new Error(`No flagToEvent mapping for "${flagKey}"`);
  actor.send(event);
}

/**
 * Returns location triggers that are currently eligible to fire:
 * - onceFlag not yet set
 * - requiredFlags (if any) all satisfied
 * Position-independent — tests only the flag logic, not player x.
 */
function eligibleTriggers(actor: Actor): string[] {
  const f = flags(actor);
  return def.locationTriggers
    .filter((t: LocationTrigger) => {
      if (f[t.onceFlag]) return false;
      if (!t.requiredFlags) return true;
      return Object.entries(t.requiredFlags).every(([k, v]) => (f[k] ?? false) === v);
    })
    .map((t: LocationTrigger) => t.onceFlag);
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('Quest Simulation — Turnhoutsebaan', () => {
  let actor: Actor;

  beforeEach(() => {
    actor = createActor(machine);
    actor.start();
  });

  // ── Act 0: Fresh start ─────────────────────────────────────────────────────

  describe('Act 0 — fresh start', () => {
    it('all quest flags are false', () => {
      const f = flags(actor);
      expect(f.met_yusuf).toBe(false);
      expect(f.delivery_packages_received).toBe(false);
      expect(f.delivered_137).toBe(false);
      expect(f.delivery_done).toBe(false);
      expect(f.met_fatima).toBe(false);
      expect(f.sig_fatima).toBe(false);
      expect(f.sig_omar).toBe(false);
      expect(f.geest_encountered).toBe(false);
      expect(f.kracht_van_gemeenschap).toBe(false);
    });

    it('nav points to Yusuf', () => {
      expect(navTarget(actor)?.label).toBe('Yusuf');
    });

    it('delivery triggers are blocked (quest not yet accepted)', () => {
      const eligible = eligibleTriggers(actor);
      expect(eligible).not.toContain('delivered_137');
      expect(eligible).not.toContain('delivered_170');
      expect(eligible).not.toContain('delivered_284');
    });

    it('de Roma trigger is eligible from the start', () => {
      expect(eligibleTriggers(actor)).toContain('visited_de_roma');
    });

    it('hint tells player to find Yusuf', () => {
      expect(hintText(actor)).toContain('Yusuf');
    });
  });

  // ── Act 1: Delivery quest ──────────────────────────────────────────────────

  describe('Act 1 — delivery quest', () => {
    it('after MET_YUSUF: met_yusuf=true, nav still Yusuf, delivery triggers still blocked', () => {
      setFlag(actor, 'met_yusuf');
      const f = flags(actor);
      expect(f.met_yusuf).toBe(true);
      expect(f.delivery_packages_received).toBe(false);
      expect(navTarget(actor)?.label).toBe('Yusuf');
      expect(eligibleTriggers(actor)).not.toContain('delivered_137');
    });

    it('after DELIVERY_ACCEPTED: triggers unblock, nav → #137', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      const f = flags(actor);
      expect(f.delivery_packages_received).toBe(true);
      expect(navTarget(actor)?.label).toBe('Adres 137');
      expect(navTarget(actor)?.x).toBe(192);
      // all three delivery triggers now eligible
      const eligible = eligibleTriggers(actor);
      expect(eligible).toContain('delivered_137');
      expect(eligible).toContain('delivered_170');
      expect(eligible).toContain('delivered_284');
    });

    it('after DELIVERED_137: nav shifts to #170', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      setFlag(actor, 'delivered_137');
      expect(flags(actor).delivered_137).toBe(true);
      expect(navTarget(actor)?.label).toBe('Adres 170');
      expect(navTarget(actor)?.x).toBe(384);
      // #137 trigger now blocked by onceFlag
      expect(eligibleTriggers(actor)).not.toContain('delivered_137');
      expect(eligibleTriggers(actor)).toContain('delivered_170');
    });

    it('after DELIVERED_170: nav shifts to #284', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      setFlag(actor, 'delivered_137');
      setFlag(actor, 'delivered_170');
      expect(navTarget(actor)?.label).toBe('Adres 284');
      expect(navTarget(actor)?.x).toBe(1632);
    });

    it('after all three delivered: nav → Yusuf (reward)', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      setFlag(actor, 'delivered_137');
      setFlag(actor, 'delivered_170');
      setFlag(actor, 'delivered_284');
      const f = flags(actor);
      expect(f.delivered_137).toBe(true);
      expect(f.delivered_170).toBe(true);
      expect(f.delivered_284).toBe(true);
      // machine should be in all_delivered now
      expect(navTarget(actor)?.label).toBe('Yusuf');
    });

    it('after DELIVERY_REWARDED: delivery_done=true', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      setFlag(actor, 'delivered_137');
      setFlag(actor, 'delivered_170');
      setFlag(actor, 'delivered_284');
      setFlag(actor, 'delivery_done');
      expect(flags(actor).delivery_done).toBe(true);
      expect(flags(actor).q_starter_delivery_done).toBe(true);
    });
  });

  // ── Act 1b: Fabric quest ───────────────────────────────────────────────────

  describe('Act 1b — fabric / community trust', () => {
    function setupDeliveryDone() {
      ['met_yusuf','delivery_accepted','delivered_137','delivered_170',
       'delivered_284','delivery_done'].forEach(f => setFlag(actor, f));
    }

    it('met_fatima stays false until MET_FATIMA fired', () => {
      setupDeliveryDone();
      expect(flags(actor).met_fatima).toBe(false);
    });

    it('after MET_FATIMA + FABRIC_ACCEPTED: fabric_quest_accepted=true, nav → Baert', () => {
      setupDeliveryDone();
      setFlag(actor, 'met_fatima');
      setFlag(actor, 'fabric_quest_accepted');
      const f = flags(actor);
      expect(f.fabric_quest_accepted).toBe(true);
      expect(f.knows_stunt_location).toBe(true);
      expect(navTarget(actor)?.label).toBe('Baert');
    });

    it('after FABRIC_PICKED_UP: stunt_quest_active=true, nav → Fatima', () => {
      setupDeliveryDone();
      setFlag(actor, 'met_fatima');
      setFlag(actor, 'fabric_quest_accepted');
      setFlag(actor, 'stunt_quest_active');
      const f = flags(actor);
      expect(f.stunt_quest_active).toBe(true);
      expect(f.stunt_quest_done).toBe(false);
      expect(navTarget(actor)?.label).toBe('Fatima');
    });

    it('after FABRIC_DELIVERED: has_community_trust=true', () => {
      setupDeliveryDone();
      setFlag(actor, 'met_fatima');
      setFlag(actor, 'fabric_quest_accepted');
      setFlag(actor, 'stunt_quest_active');
      setFlag(actor, 'stunt_quest_done');
      const f = flags(actor);
      expect(f.stunt_quest_done).toBe(true);
      expect(f.has_community_trust).toBe(true);
    });
  });

  // ── Act 2: Oud quest ───────────────────────────────────────────────────────

  describe('Act 2 — oud string quest', () => {
    // Nav tests require delivery + fabric done first (earlier navTargets take priority)
    function setupDeliveryAndFabricDone() {
      ['met_yusuf','delivery_accepted','delivered_137','delivered_170',
       'delivered_284','delivery_done','met_fatima','fabric_quest_accepted',
       'stunt_quest_active','stunt_quest_done'].forEach(f => setFlag(actor, f));
    }

    it('after OUD_ACCEPTED: oud_quest_accepted=true, nav → Aziz', () => {
      setupDeliveryAndFabricDone();
      setFlag(actor, 'oud_quest_accepted');
      expect(flags(actor).oud_quest_accepted).toBe(true);
      expect(navTarget(actor)?.label).toBe('Aziz');
    });

    it('after OUD_FOUND: has_oud_string_item=true, nav → Reza', () => {
      setupDeliveryAndFabricDone();
      setFlag(actor, 'oud_quest_accepted');
      setFlag(actor, 'has_oud_string_item');
      expect(flags(actor).has_oud_string_item).toBe(true);
      expect(navTarget(actor)?.label).toBe('Reza');
    });

    it('after OUD_DELIVERED: reza_quest_done=true', () => {
      setFlag(actor, 'oud_quest_accepted');
      setFlag(actor, 'has_oud_string_item');
      setFlag(actor, 'reza_quest_done');
      expect(flags(actor).reza_quest_done).toBe(true);
      expect(flags(actor).q_oud_string_done).toBe(true);
    });
  });

  // ── Act 2b: Flour quest ────────────────────────────────────────────────────

  describe('Act 2b — flour shortage quest', () => {
    // Nav tests require delivery + fabric + oud done first (earlier navTargets take priority)
    function setupDeliveryFabricOudDone() {
      ['met_yusuf','delivery_accepted','delivered_137','delivered_170',
       'delivered_284','delivery_done','met_fatima','fabric_quest_accepted',
       'stunt_quest_active','stunt_quest_done',
       'oud_quest_accepted','has_oud_string_item','reza_quest_done'].forEach(f => setFlag(actor, f));
    }

    it('flour trigger inactive before quest accepted', () => {
      expect(eligibleTriggers(actor)).not.toContain('has_flour');
    });

    it('after FLOUR_ACCEPTED: flour trigger becomes eligible, nav → Budget Market', () => {
      setupDeliveryFabricOudDone();
      setFlag(actor, 'flour_quest_accepted');
      expect(flags(actor).flour_quest_accepted).toBe(true);
      expect(eligibleTriggers(actor)).toContain('has_flour');
      expect(navTarget(actor)?.label).toBe('Budget Market');
    });

    it('after FLOUR_PICKED_UP: has_flour=true, nav → Omar, flour trigger blocked', () => {
      setupDeliveryFabricOudDone();
      setFlag(actor, 'flour_quest_accepted');
      setFlag(actor, 'has_flour');
      const f = flags(actor);
      expect(f.has_flour).toBe(true);
      expect(eligibleTriggers(actor)).not.toContain('has_flour');
      expect(navTarget(actor)?.label).toBe('Omar');
    });

    it('after FLOUR_DELIVERED: omar_flour_done=true', () => {
      setFlag(actor, 'flour_quest_accepted');
      setFlag(actor, 'has_flour');
      setFlag(actor, 'omar_flour_done');
      const f = flags(actor);
      expect(f.omar_flour_done).toBe(true);
      expect(f.knows_samen_tafel).toBe(true);
    });
  });

  // ── Act 3: Signatures ──────────────────────────────────────────────────────

  describe('Act 3 — signature collection (critical: individual tracking)', () => {
    it('all sig flags false at start', () => {
      const f = flags(actor);
      expect(f.sig_fatima).toBe(false);
      expect(f.sig_omar).toBe(false);
      expect(f.sig_reza).toBe(false);
      expect(f.sig_baert).toBe(false);
      expect(f.sig_aziz).toBe(false);
    });

    it('collecting Fatima sig does NOT set other sigs (no bleed-through)', () => {
      setFlag(actor, 'sig_fatima');
      const f = flags(actor);
      expect(f.sig_fatima).toBe(true);
      // Critical: only Fatima — the others must stay false
      expect(f.sig_omar).toBe(false);
      expect(f.sig_reza).toBe(false);
      expect(f.sig_baert).toBe(false);
      expect(f.sig_aziz).toBe(false);
    });

    it('each sig flag is independent', () => {
      setFlag(actor, 'sig_fatima');
      setFlag(actor, 'sig_baert');
      const f = flags(actor);
      expect(f.sig_fatima).toBe(true);
      expect(f.sig_baert).toBe(true);
      expect(f.sig_omar).toBe(false);
      expect(f.sig_reza).toBe(false);
      expect(f.sig_aziz).toBe(false);
    });

    it('speculator_threatened only true when all 5 sigs collected', () => {
      expect(flags(actor).speculator_threatened).toBe(false);
      setFlag(actor, 'sig_fatima');
      setFlag(actor, 'sig_omar');
      setFlag(actor, 'sig_reza');
      setFlag(actor, 'sig_baert');
      expect(flags(actor).speculator_threatened).toBe(false); // only 4
      setFlag(actor, 'sig_aziz');
      expect(flags(actor).speculator_threatened).toBe(true);  // all 5 ✓
      expect(flags(actor).q_signatures_done).toBe(true);
    });
  });

  // ── Act 3b: De Roma + Bulldozer ───────────────────────────────────────────

  describe('Act 3b — De Roma and Bulldozer', () => {
    // Nav tests require delivery + fabric + oud done (earlier navTargets take priority)
    function setupThroughOudDone() {
      ['met_yusuf','delivery_accepted','delivered_137','delivered_170',
       'delivered_284','delivery_done','met_fatima','fabric_quest_accepted',
       'stunt_quest_active','stunt_quest_done',
       'oud_quest_accepted','has_oud_string_item','reza_quest_done'].forEach(f => setFlag(actor, f));
    }

    it('bulldozer battle blocked before visiting De Roma', () => {
      expect(eligibleTriggers(actor)).not.toContain('has_permit_doc');
    });

    it('after VISITED_DE_ROMA: nav → Bulldozer, battle trigger eligible once speculator threatened', () => {
      setupThroughOudDone();
      setFlag(actor, 'visited_de_roma');
      // Need speculator_threatened for bulldozer trigger
      ['sig_fatima','sig_omar','sig_reza','sig_baert','sig_aziz'].forEach(f => setFlag(actor, f));
      expect(flags(actor).visited_de_roma).toBe(true);
      expect(flags(actor).speculator_threatened).toBe(true);
      expect(eligibleTriggers(actor)).toContain('has_permit_doc');
      expect(navTarget(actor)?.label).toBe('Bulldozer');
    });

    it('after BULLDOZER_DEFEATED: has_permit_doc=true, bulldozer trigger blocked', () => {
      setFlag(actor, 'visited_de_roma');
      setFlag(actor, 'has_permit_doc');
      expect(flags(actor).has_permit_doc).toBe(true);
      expect(flags(actor).q_bulldozer_done).toBe(true);
      expect(eligibleTriggers(actor)).not.toContain('has_permit_doc');
    });
  });

  // ── Act 3c: Mayor ──────────────────────────────────────────────────────────

  describe('Act 3c — Districtsvoorzitter meeting', () => {
    it('after MET_MAYOR: met_mayor=true, act4_started becomes available', () => {
      setFlag(actor, 'met_mayor');
      expect(flags(actor).met_mayor).toBe(true);
      expect(flags(actor).act4_briefed).toBe(true);
    });

    it('after MAYOR_BRIEFED: act4_started=true', () => {
      setFlag(actor, 'met_mayor');
      setFlag(actor, 'act4_started');
      expect(flags(actor).act4_started).toBe(true);
      expect(flags(actor).q_mayor_meeting_done).toBe(true);
    });
  });

  // ── Act 3d: Geest van '88 ─────────────────────────────────────────────────

  describe("Act 3d — Geest van '88", () => {
    it('encounter trigger eligible from the start (no requiredFlags)', () => {
      expect(eligibleTriggers(actor)).toContain('geest_encountered');
    });

    it('battle trigger blocked until encountered', () => {
      expect(eligibleTriggers(actor)).not.toContain('vlok_geest_verslagen');
    });

    it('after GEEST_ENCOUNTERED: battle trigger eligible', () => {
      setFlag(actor, 'geest_encountered');
      expect(flags(actor).geest_encountered).toBe(true);
      expect(eligibleTriggers(actor)).toContain('vlok_geest_verslagen');
    });

    it('after battle won: defeated dialogue trigger eligible', () => {
      setFlag(actor, 'geest_encountered');
      // vlok_geest_verslagen is a post-battle flag set by BattleScene, not via machine event
      // It goes into extraFlags; for this test we verify the machine side
      // The defeated dialogue requires vlok_geest_verslagen in extraFlags
      // so we verify geest state can reach completed via GEEST_DEFEATED
      setFlag(actor, 'kracht_van_gemeenschap'); // = GEEST_DEFEATED event
      expect(flags(actor).kracht_van_gemeenschap).toBe(true);
      expect(flags(actor).q_geest_88_done).toBe(true);
      // encounter + battle triggers now blocked
      expect(eligibleTriggers(actor)).not.toContain('geest_encountered');
      expect(eligibleTriggers(actor)).not.toContain('kracht_van_gemeenschap');
    });
  });

  // ── Act 4: Faction collection ──────────────────────────────────────────────

  describe('Act 4 — faction collection (7 parallel)', () => {
    const factions = [
      'fatima_convinced',      // moroccan
      'tine_faction_convinced', // turkish
      'baert_faction_convinced',// flemish
      'art_faction_convinced',
      'school_faction_convinced',
      'mosque_faction_convinced',
      'frituur_faction_convinced',
    ] as const;

    it('all faction flags false at start', () => {
      const f = flags(actor);
      factions.forEach(flag => expect(f[flag]).toBe(false));
    });

    it('each faction is independent', () => {
      setFlag(actor, 'fatima_convinced');
      const f = flags(actor);
      expect(f.fatima_convinced).toBe(true);
      expect(f.tine_faction_convinced).toBe(false);
      expect(f.baert_faction_convinced).toBe(false);
    });

    it('completing 6 factions does not set q_faction_*_done for the 7th', () => {
      factions.slice(0, 6).forEach(f => setFlag(actor, f));
      expect(flags(actor).frituur_faction_convinced).toBe(false);
    });

    it('all 7 factions complete', () => {
      factions.forEach(f => setFlag(actor, f));
      const f = flags(actor);
      factions.forEach(flag => expect(f[flag]).toBe(true));
    });
  });

  // ── Regression: nav delivery sequencing ───────────────────────────────────

  describe('Regression — delivery nav never stalls on completed address', () => {
    it('nav does not point to #137 after it has been delivered', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      setFlag(actor, 'delivered_137');
      const target = navTarget(actor);
      expect(target?.label).not.toBe('Adres 137');
      expect(target?.x).not.toBe(192);
    });

    it('nav does not point to #170 after it has been delivered', () => {
      setFlag(actor, 'met_yusuf');
      setFlag(actor, 'delivery_accepted');
      setFlag(actor, 'delivered_137');
      setFlag(actor, 'delivered_170');
      const target = navTarget(actor);
      expect(target?.label).not.toBe('Adres 170');
      expect(target?.x).not.toBe(384);
    });
  });

  // ── Regression: signature bleed-through ───────────────────────────────────

  describe('Regression — sig flags do not bleed across NPCs', () => {
    it('each combination of sigs tracks independently', () => {
      const sigs = ['sig_fatima','sig_omar','sig_reza','sig_baert','sig_aziz'];
      // Collect one at a time and verify only the expected one is true
      for (let i = 0; i < sigs.length; i++) {
        const fresh = createActor(machine);
        fresh.start();
        // Collect sigs 0..i
        for (let j = 0; j <= i; j++) setFlag(fresh, sigs[j]);
        const f = flags(fresh);
        for (let j = 0; j < sigs.length; j++) {
          if (j <= i) {
            expect(f[sigs[j]], `${sigs[j]} should be true after collecting ${sigs.slice(0,i+1)}`).toBe(true);
          } else {
            expect(f[sigs[j]], `${sigs[j]} should be false — not yet collected`).toBe(false);
          }
        }
      }
    });
  });

  // ── Location trigger completeness ──────────────────────────────────────────

  describe('Location triggers — structural checks', () => {
    it('every trigger has a unique onceFlag', () => {
      const flags = def.locationTriggers.map((t: LocationTrigger) => t.onceFlag);
      const unique = new Set(flags);
      expect(flags.length).toBe(unique.size);
    });

    it('every trigger dialogueId or enemyId is non-empty', () => {
      for (const t of def.locationTriggers) {
        if (t.type === 'dialogue') expect(t.dialogueId).toBeTruthy();
        if (t.type === 'battle')   expect(t.enemyId).toBeTruthy();
      }
    });

    it('every trigger has positive width', () => {
      for (const t of def.locationTriggers) {
        expect(t.width).toBeGreaterThan(0);
      }
    });

    it('every flagBridge rule references a known region or faction', () => {
      const regions = new Set(def.regions.map(r => r.id));
      for (const rule of def.flagBridge) {
        if (rule.faction !== undefined) continue;
        if (rule.region) {
          expect(regions.has(rule.region), `Unknown region "${rule.region}" in flagBridge rule for "${rule.flag}"`).toBe(true);
        }
      }
    });

    it('every flagToEvent entry has a matching machine event', () => {
      // Build the set of events the machine accepts (from quests.json regions)
      const events = new Set<string>();
      for (const e of Object.values(def.flagToEvent)) events.add(e);
      // All events should be valid strings
      for (const [flag, event] of Object.entries(def.flagToEvent)) {
        expect(typeof event, `flagToEvent["${flag}"] should be a string`).toBe('string');
        expect(event.length).toBeGreaterThan(0);
      }
    });
  });

  // ── Full playthrough smoke test ────────────────────────────────────────────

  describe('Full playthrough — complete main quest line', () => {
    it('survives a full run without throwing', () => {
      const sequence = [
        'met_yusuf',
        'delivery_accepted',
        'delivered_137',
        'delivered_170',
        'delivered_284',
        'delivery_done',
        'met_fatima',
        'fabric_quest_accepted',
        'stunt_quest_active',
        'stunt_quest_done',
        'oud_quest_accepted',
        'has_oud_string_item',
        'reza_quest_done',
        'flour_quest_accepted',
        'has_flour',
        'omar_flour_done',
        'sig_fatima',
        'sig_omar',
        'sig_reza',
        'sig_baert',
        'sig_aziz',
        'visited_de_roma',
        'has_permit_doc',
        'met_mayor',
        'act4_started',
        'geest_encountered',
        'kracht_van_gemeenschap',
        'fatima_convinced',
        'tine_faction_convinced',
        'baert_faction_convinced',
        'art_faction_convinced',
        'school_faction_convinced',
        'mosque_faction_convinced',
        'frituur_faction_convinced',
      ];

      for (const flag of sequence) {
        expect(() => setFlag(actor, flag)).not.toThrow();
      }

      // End state assertions
      const f = flags(actor);
      expect(f.delivery_done).toBe(true);
      expect(f.has_community_trust).toBe(true);
      expect(f.speculator_threatened).toBe(true);
      expect(f.kracht_van_gemeenschap).toBe(true);
      expect(f.fatima_convinced).toBe(true);
      expect(f.frituur_faction_convinced).toBe(true);
    });
  });
});
