/**
 * StreetMachine.ts
 *
 * Builds an XState v5 parallel machine dynamically from a street's quests.json.
 * Also exports:
 *   - buildFlagToEvent()   → FLAG_TO_EVENT map for StateManager
 *   - buildFlagBridge()    → flagBridge() function for StateManager
 *   - buildGetNavTarget()  → getNavTarget() for OverworldScene
 *   - buildGetHintText()   → getHintText() for hint modal + nav
 *
 * Adding a new street = add quests.json. No TypeScript changes required.
 */

import { createMachine, assign } from 'xstate';
import type { QuestsDef, QuestRegionDef, QuestStateDef, FlagBridgeRule } from '@core/StreetLoader';

// ── Context (same shape for all streets) ─────────────────────────────────────

export interface GameContext {
  coins:     number;
  xp:        number;
  hp:        number;
  maxHp:     number;
  level:     number;
  xpNext:    number;
  inventory: string[];
  skills:    string[];
  name:      string;
}

// ── Snapshot type helper ──────────────────────────────────────────────────────

export type AnySnapshot = { value: unknown; context: GameContext };

// ── State helpers (same logic as GameMachine.ts) ──────────────────────────────

function stateIs(value: unknown, ...path: string[]): boolean {
  if (path.length === 0) return true;
  const [head, ...rest] = path;
  if (typeof value === 'string') return rest.length === 0 && value === head;
  if (typeof value !== 'object' || value === null) return false;
  const map = value as Record<string, unknown>;
  if (!(head in map)) return false;
  if (rest.length === 0) return true;
  return stateIs(map[head], ...rest);
}

function regionIs(value: unknown, region: string, state: string): boolean {
  if (typeof value !== 'object' || value === null) return false;
  const map = value as Record<string, unknown>;
  const rv  = map[region];
  if (typeof rv === 'string') return rv === state;
  if (typeof rv === 'object' && rv !== null) return state in (rv as Record<string, unknown>);
  return false;
}

function regionNotState(value: unknown, region: string, state: string): boolean {
  return !regionIs(value, region, state);
}

function regionAnyState(value: unknown, region: string, states: string[]): boolean {
  return states.some(s => regionIs(value, region, s));
}

function factionIs(value: unknown, faction: string): boolean {
  if (typeof value !== 'object' || value === null) return false;
  const factionsVal = (value as Record<string, unknown>)['factions'];
  return regionIs(factionsVal ?? value, faction, 'completed');
}

// ── XState config builder ────────────────────────────────────────────────────

/** Build a simple parallel sub-region (pending → done) */
function buildSubRegionState(event: string): object {
  return {
    initial: 'pending',
    states: {
      pending: { on: { [event]: 'done' } },
      done:    { type: 'final' },
    },
  };
}

/** Build a top-level faction-style parallel (all sub-regions idle → completed) */
function buildTopParallelRegion(subRegions: Array<{ id: string; event: string }>): object {
  const states: Record<string, object> = {};
  for (const sr of subRegions) {
    states[sr.id] = {
      initial: 'idle',
      states: {
        idle:      { on: { [sr.event]: 'completed' } },
        completed: { type: 'final' },
      },
    };
  }
  return { type: 'parallel', states };
}

function buildStateConfig(stateDef: QuestStateDef): object {
  if (stateDef.type === 'parallel' && stateDef.subRegions) {
    const subStates: Record<string, object> = {};
    for (const sr of stateDef.subRegions) {
      subStates[sr.id] = buildSubRegionState(sr.event);
    }
    return {
      type:   'parallel',
      states: subStates,
      ...(stateDef.onDone ? { onDone: stateDef.onDone } : {}),
    };
  }
  return {
    ...(stateDef.type ? { type: stateDef.type } : {}),
    ...(stateDef.on   ? { on: stateDef.on }      : {}),
  };
}

function buildRegionConfig(region: QuestRegionDef): object {
  // Top-level parallel (factions-style): has subRegions but no states map
  if (region.type === 'parallel' && region.subRegions && !region.states) {
    return buildTopParallelRegion(region.subRegions);
  }

  // Normal linear/compound region
  const states: Record<string, object> = {};
  for (const [stateName, stateDef] of Object.entries(region.states ?? {})) {
    states[stateName] = buildStateConfig(stateDef);
  }
  return {
    initial: region.initial,
    states,
  };
}

// ── Global inventory/stat event handlers (same for all streets) ──────────────

const GLOBAL_EVENTS = {
  ADD_ITEM: {
    actions: assign({
      inventory: ({ context, event }: { context: GameContext; event: { type: string; itemId?: string } }) =>
        [...context.inventory, event.itemId ?? ''],
    }),
  },
  REMOVE_ITEM: {
    actions: assign({
      inventory: ({ context, event }: { context: GameContext; event: { type: string; itemId?: string } }) => {
        const id  = event.itemId ?? '';
        const idx = context.inventory.indexOf(id);
        if (idx === -1) return context.inventory;
        const next = [...context.inventory];
        next.splice(idx, 1);
        return next;
      },
    }),
  },
  ADD_COINS: {
    actions: assign({
      coins: ({ context, event }: { context: GameContext; event: { type: string; amount?: number } }) =>
        Math.max(0, context.coins + (event.amount ?? 0)),
    }),
  },
  REMOVE_COINS: {
    actions: assign({
      coins: ({ context, event }: { context: GameContext; event: { type: string; amount?: number } }) =>
        Math.max(0, context.coins - (event.amount ?? 0)),
    }),
  },
  SET_HP: {
    actions: assign({
      hp: ({ context, event }: { context: GameContext; event: { type: string; hp?: number } }) =>
        Math.min(context.maxHp, Math.max(0, event.hp ?? 0)),
    }),
  },
  GAIN_XP: {
    actions: assign(({ context, event }: { context: GameContext; event: { type: string; amount?: number } }) => {
      const gain  = event.amount ?? 0;
      let xp      = context.xp + gain;
      let level   = context.level;
      let xpNext  = context.xpNext;
      let maxHp   = context.maxHp;
      while (xp >= xpNext) {
        xp    -= xpNext;
        level += 1;
        xpNext = Math.floor(xpNext * 1.5);
        maxHp += 5;
      }
      return { xp, level, xpNext, maxHp, hp: maxHp };
    }),
  },
  SET_NAME: {
    actions: assign({
      name: ({ event }: { event: { type: string; name?: string } }) => event.name ?? 'Speler',
    }),
  },
};

// ── Main machine builder ──────────────────────────────────────────────────────

export function buildMachine(def: QuestsDef) {
  const regionStates: Record<string, object> = {};
  for (const region of def.regions) {
    regionStates[region.id] = buildRegionConfig(region);
  }

  const ctx = def.context as unknown as GameContext;

  return createMachine(
    {
      id:      def.machineId,
      type:    'parallel',
      context: {
        coins:     ctx.coins     ?? 5,
        xp:        ctx.xp        ?? 0,
        hp:        ctx.hp        ?? 20,
        maxHp:     ctx.maxHp     ?? 20,
        level:     ctx.level     ?? 1,
        xpNext:    ctx.xpNext    ?? 100,
        inventory: (ctx.inventory ?? []) as string[],
        skills:    (ctx.skills    ?? []) as string[],
        name:      ctx.name      ?? 'Speler',
      } satisfies GameContext,
      on:     GLOBAL_EVENTS as unknown as never,
      states: regionStates,
    },
  );
}

// ── FLAG_TO_EVENT builder ─────────────────────────────────────────────────────

export function buildFlagToEvent(def: QuestsDef): Record<string, { type: string } | null> {
  const map: Record<string, { type: string } | null> = {};
  for (const [flag, event] of Object.entries(def.flagToEvent)) {
    map[flag] = { type: event };
  }
  return map;
}

// ── flagBridge builder ────────────────────────────────────────────────────────

export function buildFlagBridge(def: QuestsDef): (snapshot: AnySnapshot) => Record<string, boolean> {
  const rules: FlagBridgeRule[] = def.flagBridge;

  return function flagBridge(snapshot: AnySnapshot): Record<string, boolean> {
    const v      = snapshot.value;
    const result: Record<string, boolean> = {};

    for (const rule of rules) {
      let val = false;

      if (rule.faction !== undefined) {
        val = factionIs(v, rule.faction);
      } else if (rule.region) {
        const r = rule.region;

        if (rule.state) {
          val = regionIs(v, r, rule.state);
        } else if (rule.notState) {
          val = regionNotState(v, r, rule.notState);
        } else if (rule.anyState) {
          val = regionAnyState(v, r, rule.anyState);
        }

        // orSubState: also true if a sub-path matches
        if (!val && rule.orSubState) {
          val = stateIs(v, ...rule.orSubState);
        }
      }

      result[rule.flag] = val;
    }

    return result;
  };
}

// ── getNavTarget builder ──────────────────────────────────────────────────────

export function buildGetNavTarget(def: QuestsDef): (snapshot: AnySnapshot) => { x: number; label: string } | null {
  const targets = def.navTargets;

  // Count factions done
  function factionCount(v: unknown): number {
    const factionRegion = (typeof v === 'object' && v !== null)
      ? (v as Record<string, unknown>)['factions']
      : undefined;
    if (!factionRegion || typeof factionRegion !== 'object') return 0;
    return Object.keys(factionRegion as object).filter(f =>
      regionIs(factionRegion, f, 'completed'),
    ).length;
  }

  return function getNavTarget(snapshot: AnySnapshot): { x: number; label: string } | null {
    const v = snapshot.value;

    for (const t of targets) {
      if (t.faction !== undefined) {
        const isDone = factionIs(v, t.faction);
        if (t.done === false && !isDone) return { x: t.x, label: t.label };
        if (t.done === true  &&  isDone) return { x: t.x, label: t.label };
        continue;
      }

      if (t.condition) {
        const allMatch = Object.entries(t.condition).every(([region, state]) =>
          regionIs(v, region, state),
        );
        if (allMatch && factionCount(v) < 7) return { x: t.x, label: t.label };
      }
    }
    return null;
  };
}

// ── getHintText builder ───────────────────────────────────────────────────────

export function buildGetHintText(def: QuestsDef): (snapshot: AnySnapshot) => string {
  const hints = def.hintTexts;

  function factionCount(v: unknown): number {
    const fr = (typeof v === 'object' && v !== null)
      ? (v as Record<string, unknown>)['factions']
      : undefined;
    if (!fr || typeof fr !== 'object') return 0;
    return Object.keys(fr as object).filter(f => regionIs(fr, f, 'completed')).length;
  }

  return function getHintText(snapshot: AnySnapshot): string {
    const v = snapshot.value;

    for (const h of hints) {
      if (h.allFactionsComplete) {
        if (factionCount(v) >= 7) return h.text;
        continue;
      }
      if (h.condition) {
        const allMatch = Object.entries(h.condition).every(([region, state]) =>
          regionIs(v, region, state),
        );
        if (allMatch) return h.text;
      }
    }
    return 'Verken de Turnhoutsebaan en spreek met de bewoners.';
  };
}
