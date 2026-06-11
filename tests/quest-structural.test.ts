/**
 * Quest structural & story-layer tests — Turnhoutsebaan
 *
 * Validates the STORY DATA layer (dialogue.json + street quests.json +
 * quests.json) that the machine-level simulation cannot see:
 *   - every referenced dialogue node / enemy exists
 *   - every dialogue condition flag has a producer somewhere
 *   - every faction is actually completable in-game
 *   - location-trigger dialogues set their own onceFlag (no re-fire loops)
 *   - quest objectives are simultaneously satisfiable (no mutually
 *     exclusive machine states — the bug that silently disabled all rewards)
 *   - nav/hints cover the endgame (factions + finale)
 *
 * Run with:  npm run test:quest
 */

import { describe, it, expect } from 'vitest';
import { createActor } from 'xstate';
import dialogueRaw from '../src/data/dialogue.json';
import questDefsRaw from '../src/data/quests.json';
import enemiesRaw from '../src/data/enemies.json';
import streetQuestsRaw from '../src/data/streets/turnhoutsebaan/quests.json';
import npcsRaw from '../src/data/streets/turnhoutsebaan/npcs.json';
import {
  buildMachine,
  buildFlagBridge,
  buildGetNavTarget,
  buildGetHintText,
  buildFlagToEvent,
  type AnySnapshot,
} from '../src/systems/StreetMachine';
import type { QuestsDef } from '../src/core/StreetLoader';

// ── Data ──────────────────────────────────────────────────────────────────────

interface Line {
  flag?: string; flagVal?: unknown;
  flag2?: string; flagVal2?: unknown;
  item?: string; removeItem?: string;
  choice?: Array<{ label: string; next?: string; flag?: string; flagVal?: unknown; item?: string }>;
}
interface Node {
  npc?: string;
  priority: number;
  conditions: { flags?: Record<string, unknown>; items?: string[]; notItems?: string[] };
  lines: Line[];
}

const DIALOGUES = dialogueRaw as unknown as Record<string, Node>;
const QUEST_DEFS = questDefsRaw as Record<string, {
  id: string;
  requiredFlags: string[];
  objectives: Array<{ id: string; checkFlag: string; checkValue: unknown }>;
  reward: { flags: Record<string, unknown>; items: string[]; skills: string[] };
  completionFlag: string;
}>;
const ENEMIES = enemiesRaw as Record<string, { post_battle_flag?: string; loot?: string[] }>;
const STREET  = streetQuestsRaw as unknown as QuestsDef;
const NPCS    = (npcsRaw as { npcs: Array<{ id: string; dialogueId: string }> }).npcs;

const machine = buildMachine(STREET);
const bridge  = buildFlagBridge(STREET);
const nav     = buildGetNavTarget(STREET);
const hint    = buildGetHintText(STREET);
const f2e     = buildFlagToEvent(STREET);

// Mirrors BattleScene.LOOT_FLAGS
const LOOT_FLAGS: Record<string, string> = {
  permit_doc:      'has_permit_doc',
  oud_string:      'has_oud_string_item',
  reuzenpoort_key: 'has_reuzenpoort_key',
};

// ── Helpers ───────────────────────────────────────────────────────────────────

/** All node ids reachable in-game: NPC-routable nodes, trigger dialogues,
 *  and the closure over choice.next jumps. */
function openableNodeIds(): Set<string> {
  const open = new Set<string>();
  for (const [id, node] of Object.entries(DIALOGUES)) {
    if (node.npc) open.add(id);
  }
  for (const t of STREET.locationTriggers) {
    if (t.type === 'dialogue' && t.dialogueId) open.add(t.dialogueId);
  }
  let grew = true;
  while (grew) {
    grew = false;
    for (const id of [...open]) {
      const node = DIALOGUES[id];
      if (!node) continue;
      for (const line of node.lines) {
        for (const c of line.choice ?? []) {
          if (c.next && !open.has(c.next)) { open.add(c.next); grew = true; }
        }
      }
    }
  }
  return open;
}

/** All flags a node (and its choice-jump closure) can set. */
function flagsSetByNode(id: string, seen = new Set<string>()): Set<string> {
  const out = new Set<string>();
  if (seen.has(id)) return out;
  seen.add(id);
  const node = DIALOGUES[id];
  if (!node) return out;
  for (const line of node.lines) {
    if (line.flag)  out.add(line.flag);
    if (line.flag2) out.add(line.flag2);
    for (const c of line.choice ?? []) {
      if (c.flag) out.add(c.flag);
      if (c.next) for (const f of flagsSetByNode(c.next, seen)) out.add(f);
    }
  }
  return out;
}

function freshActor() {
  const actor = createActor(machine);
  actor.start();
  return actor;
}

function send(actor: ReturnType<typeof freshActor>, flagKey: string): void {
  const event = f2e[flagKey];
  if (!event) throw new Error(`No flagToEvent mapping for "${flagKey}"`);
  actor.send(event);
}

function snap(actor: ReturnType<typeof freshActor>): AnySnapshot {
  return actor.getSnapshot() as AnySnapshot;
}

const GOLDEN_PATH = [
  'met_yusuf', 'delivery_accepted', 'delivered_137', 'delivered_170',
  'delivered_284', 'delivery_done',
  'met_fatima', 'fabric_quest_accepted', 'stunt_quest_active', 'stunt_quest_done',
  'oud_quest_accepted', 'has_oud_string_item', 'reza_quest_done',
  'flour_quest_accepted', 'has_flour', 'omar_flour_done',
  'sig_fatima', 'sig_omar', 'sig_reza', 'sig_baert', 'sig_aziz',
  'speculator_threatened',
  'visited_de_roma', 'has_permit_doc',
  'met_mayor', 'act4_started',
  'geest_encountered', 'kracht_van_gemeenschap',
  'fatima_convinced', 'tine_faction_convinced', 'baert_faction_convinced',
  'art_faction_convinced', 'school_faction_convinced', 'mosque_faction_convinced',
  'frituur_faction_convinced',
];

// ── Referential integrity ─────────────────────────────────────────────────────

describe('Referential integrity', () => {
  it('every choice.next jump targets an existing dialogue node', () => {
    for (const [id, node] of Object.entries(DIALOGUES)) {
      for (const line of node.lines) {
        for (const c of line.choice ?? []) {
          if (c.next) {
            expect(DIALOGUES[c.next], `choice.next "${c.next}" in node "${id}"`).toBeDefined();
          }
        }
      }
    }
  });

  it('every NPC dialogueId exists in dialogue.json', () => {
    for (const npc of NPCS) {
      expect(DIALOGUES[npc.dialogueId], `npc "${npc.id}" dialogueId "${npc.dialogueId}"`).toBeDefined();
    }
  });

  it('every location trigger references an existing dialogue or enemy', () => {
    for (const t of STREET.locationTriggers) {
      if (t.type === 'dialogue') {
        expect(DIALOGUES[t.dialogueId ?? ''], `trigger dialogue "${t.dialogueId}"`).toBeDefined();
      } else {
        expect(ENEMIES[t.enemyId ?? ''], `trigger enemy "${t.enemyId}"`).toBeDefined();
      }
    }
  });
});

// ── Flag producers ────────────────────────────────────────────────────────────

describe('Every consumed flag has a producer', () => {
  function producerFlags(): Set<string> {
    const out = new Set<string>();
    for (const rule of STREET.flagBridge) out.add(rule.flag);
    for (const key of Object.keys(STREET.flagToEvent)) out.add(key);
    for (const id of Object.keys(DIALOGUES)) for (const f of flagsSetByNode(id)) out.add(f);
    for (const t of STREET.locationTriggers) out.add(t.onceFlag);
    for (const e of Object.values(ENEMIES)) {
      if (e.post_battle_flag) out.add(e.post_battle_flag);
      for (const itemId of e.loot ?? []) {
        if (LOOT_FLAGS[itemId]) out.add(LOOT_FLAGS[itemId]);
      }
    }
    for (const q of Object.values(QUEST_DEFS)) {
      for (const f of Object.keys(q.reward.flags)) out.add(f);
      out.add(q.completionFlag);
      out.add(`q_rewarded_${q.id}`);
      for (const s of q.reward.skills) out.add(`skill_unlocked_${s}`);
    }
    out.add('samen_tafel_faction_N');
    return out;
  }

  const producers = producerFlags();

  it('dialogue node conditions only reference producible flags', () => {
    for (const [id, node] of Object.entries(DIALOGUES)) {
      for (const flag of Object.keys(node.conditions.flags ?? {})) {
        expect(producers.has(flag), `condition flag "${flag}" in node "${id}" has no producer`).toBe(true);
      }
    }
  });

  it('trigger requiredFlags only reference producible flags', () => {
    for (const t of STREET.locationTriggers) {
      for (const flag of Object.keys(t.requiredFlags ?? {})) {
        expect(producers.has(flag), `requiredFlag "${flag}" on trigger "${t.onceFlag}" has no producer`).toBe(true);
      }
    }
  });

  it('quest requiredFlags and objectives only reference producible flags', () => {
    for (const q of Object.values(QUEST_DEFS)) {
      for (const flag of q.requiredFlags) {
        expect(producers.has(flag), `quest ${q.id} requiredFlag "${flag}"`).toBe(true);
      }
      for (const obj of q.objectives) {
        expect(producers.has(obj.checkFlag), `quest ${q.id} objective "${obj.checkFlag}"`).toBe(true);
      }
    }
  });
});

// ── Faction completability (regression: 3 of 7 used to be unreachable) ───────

describe('All 7 factions are completable in-game', () => {
  const FACTION_FLAGS = [
    'fatima_convinced', 'tine_faction_convinced', 'baert_faction_convinced',
    'art_faction_convinced', 'school_faction_convinced',
    'mosque_faction_convinced', 'frituur_faction_convinced',
  ];

  it('every faction flag is set by a node reachable via an NPC or location trigger', () => {
    const open = openableNodeIds();
    for (const flag of FACTION_FLAGS) {
      const setters = [...open].filter(id => flagsSetByNode(id).has(flag));
      expect(setters.length, `faction flag "${flag}" has no reachable setter`).toBeGreaterThan(0);
    }
  });

  it('faction triggers exist for the NPC-less factions (mosque, art, frituur)', () => {
    const triggerDialogues = STREET.locationTriggers
      .filter(t => t.type === 'dialogue')
      .map(t => t.dialogueId);
    expect(triggerDialogues).toContain('imam_mosque');
    expect(triggerDialogues).toContain('borgerhub_faction');
    expect(triggerDialogues).toContain('frituur_faction');
  });
});

// ── Trigger once-handshake (regression: re-fire loops) ───────────────────────

describe('Location trigger once-semantics handshake', () => {
  it('every dialogue trigger sets its own onceFlag within the opened node (or its jumps)', () => {
    for (const t of STREET.locationTriggers) {
      if (t.type !== 'dialogue') continue;
      const set = flagsSetByNode(t.dialogueId ?? '');
      expect(set.has(t.onceFlag),
        `trigger dialogue "${t.dialogueId}" never sets its onceFlag "${t.onceFlag}"`).toBe(true);
    }
  });

  it('every battle trigger onceFlag is produced by loot or post_battle_flag', () => {
    for (const t of STREET.locationTriggers) {
      if (t.type !== 'battle') continue;
      const enemy = ENEMIES[t.enemyId ?? ''];
      const produced = new Set<string>([
        ...(enemy?.post_battle_flag ? [enemy.post_battle_flag] : []),
        ...(enemy?.loot ?? []).map(i => LOOT_FLAGS[i]).filter(Boolean),
      ]);
      expect(produced.has(t.onceFlag),
        `battle trigger "${t.enemyId}" never produces its onceFlag "${t.onceFlag}"`).toBe(true);
    }
  });
});

// ── Quest objective satisfiability (regression: rewards never granted) ───────

describe('Quest objectives are simultaneously satisfiable', () => {
  it('after a full golden-path run every quest has all requiredFlags + objectives true', () => {
    const actor = freshActor();
    for (const flag of GOLDEN_PATH) send(actor, flag);
    const flags = bridge(snap(actor));

    for (const q of Object.values(QUEST_DEFS)) {
      for (const f of q.requiredFlags) {
        expect(flags[f], `quest ${q.id}: requiredFlag "${f}" not true at end of golden path`).toBe(true);
      }
      for (const obj of q.objectives) {
        expect(flags[obj.checkFlag],
          `quest ${q.id}: objective "${obj.id}" flag "${obj.checkFlag}" not true at end of golden path — objectives may be mutually exclusive machine states`).toBe(obj.checkValue);
      }
    }
  });

  it('fabric pickup objective stays true after delivery (no mutually exclusive states)', () => {
    const actor = freshActor();
    ['met_fatima', 'fabric_quest_accepted', 'stunt_quest_active', 'stunt_quest_done']
      .forEach(f => send(actor, f));
    const flags = bridge(snap(actor));
    expect(flags.fabric_obtained).toBe(true);
    expect(flags.stunt_quest_done).toBe(true);
  });

  it('flour pickup objective stays true after delivery', () => {
    const actor = freshActor();
    ['flour_quest_accepted', 'has_flour', 'omar_flour_done'].forEach(f => send(actor, f));
    const flags = bridge(snap(actor));
    expect(flags.flour_obtained).toBe(true);
    expect(flags.omar_flour_done).toBe(true);
  });

  it('oud find objective stays true after delivery', () => {
    const actor = freshActor();
    ['oud_quest_accepted', 'has_oud_string_item', 'reza_quest_done'].forEach(f => send(actor, f));
    const flags = bridge(snap(actor));
    expect(flags.oud_string_found).toBe(true);
    expect(flags.reza_quest_done).toBe(true);
  });
});

// ── Fabric hint-path regression (the "Fatima loop") ───────────────────────────

describe('Regression — fabric hint path cannot drop FABRIC_PICKED_UP', () => {
  it('fatima_fabric_hint also accepts the quest (sets fabric_quest_accepted)', () => {
    expect(flagsSetByNode('fatima_fabric_hint').has('fabric_quest_accepted')).toBe(true);
  });

  it('stunt_baert_fabric sends FABRIC_ACCEPTED before FABRIC_PICKED_UP (flag before flag2)', () => {
    const node = DIALOGUES['stunt_baert_fabric'];
    const line = node.lines[0];
    expect(line.flag).toBe('fabric_quest_accepted');
    expect(line.flag2).toBe('stunt_quest_active');
  });

  it('machine accepts the hint-path sequence end-to-end', () => {
    const actor = freshActor();
    // hint path: MET_FATIMA, then the hint node fires FABRIC_ACCEPTED,
    // then Baert fires FABRIC_ACCEPTED (dropped, harmless) + FABRIC_PICKED_UP
    send(actor, 'met_fatima');
    send(actor, 'fabric_quest_accepted');
    send(actor, 'fabric_quest_accepted');
    send(actor, 'stunt_quest_active');
    const flags = bridge(snap(actor));
    expect(flags.stunt_quest_active).toBe(true);
  });
});

// ── Endgame guidance (factions + finale) ──────────────────────────────────────

describe('Endgame nav & hints', () => {
  function runGolden(upTo?: string) {
    const actor = freshActor();
    for (const flag of GOLDEN_PATH) {
      send(actor, flag);
      if (flag === upTo) break;
    }
    return actor;
  }

  it('after mayor briefing, hint guides toward the first open faction', () => {
    const actor = runGolden('kracht_van_gemeenschap');
    expect(hint(snap(actor))).toContain('Fatima');
  });

  it('mosque hint appears once geest is defeated and mosque is the only faction left', () => {
    const actor = freshActor();
    for (const flag of GOLDEN_PATH.filter(f => f !== 'mosque_faction_convinced')) send(actor, flag);
    expect(hint(snap(actor))).toContain('Moskee');
  });

  it('with all 7 factions done, nav points to the Grote 2km Tafel', () => {
    const actor = freshActor();
    for (const flag of GOLDEN_PATH) send(actor, flag);
    const target = nav(snap(actor));
    expect(target?.label).toBe('Grote 2km Tafel');
    expect(target?.x).toBe(4700);
    expect(hint(snap(actor))).toContain('Grote 2km Tafel');
  });

  it('finale trigger exists in zone 5 and its dialogue sets finale_seen', () => {
    const finale = STREET.locationTriggers.find(t => t.dialogueId === 'finale_tafel');
    expect(finale).toBeDefined();
    expect(finale!.x).toBeGreaterThanOrEqual(4608); // zone 5 starts at 4608
    expect(flagsSetByNode('finale_tafel').has('finale_seen')).toBe(true);
  });

  it('signature collection has per-NPC nav guidance', () => {
    const actor = runGolden('omar_flour_done');
    // signatures collecting, nothing signed → first pending sig is Fatima
    expect(nav(snap(actor))?.label).toBe('Handtekening: Fatima');
    send(actor, 'sig_fatima');
    expect(nav(snap(actor))?.label).toBe('Handtekening: Omar');
  });
});

// ── ADD_SKILL machine event ───────────────────────────────────────────────────

describe('ADD_SKILL event', () => {
  it('adds a skill to context.skills exactly once', () => {
    const actor = freshActor();
    actor.send({ type: 'ADD_SKILL', skillId: 'samen_aan_tafel' });
    actor.send({ type: 'ADD_SKILL', skillId: 'samen_aan_tafel' });
    expect(snap(actor).context.skills).toEqual(['samen_aan_tafel']);
  });
});
