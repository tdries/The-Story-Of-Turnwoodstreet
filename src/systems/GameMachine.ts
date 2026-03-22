/**
 * GameMachine.ts — Top-level parallel XState v5 machine for all quest arcs.
 *
 * Architecture:
 *   - One parallel region per quest arc (delivery, fabric, flour, oud,
 *     signatures, bulldozer, geest, mayor, factions)
 *   - Mutable player data (coins, xp, hp, maxHp, inventory) lives in context
 *   - Quest state is encoded in hierarchical states, NOT context flags
 *   - flagBridge(snapshot) maps current state → Record<string, boolean> so
 *     existing dialogue.json conditions work without modification
 */

import { createMachine, assign } from 'xstate';

// ── Context ─────────────────────────────────────────────────────────────────

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

// ── Events ───────────────────────────────────────────────────────────────────

export type GameEvent =
  // Delivery arc
  | { type: 'MET_YUSUF' }
  | { type: 'DELIVERY_ACCEPTED' }
  | { type: 'DELIVERED_137' }
  | { type: 'DELIVERED_170' }
  | { type: 'DELIVERED_284' }
  | { type: 'DELIVERY_REWARDED' }
  // Fabric arc
  | { type: 'MET_FATIMA' }
  | { type: 'FABRIC_ACCEPTED' }
  | { type: 'FABRIC_PICKED_UP' }
  | { type: 'FABRIC_DELIVERED' }
  // Flour arc
  | { type: 'FLOUR_ACCEPTED' }
  | { type: 'FLOUR_PICKED_UP' }
  | { type: 'FLOUR_DELIVERED' }
  // Oud arc
  | { type: 'OUD_ACCEPTED' }
  | { type: 'OUD_FOUND' }
  | { type: 'OUD_DELIVERED' }
  // Signatures arc
  | { type: 'SIG_FATIMA' }
  | { type: 'SIG_OMAR' }
  | { type: 'SIG_REZA' }
  | { type: 'SIG_BAERT' }
  | { type: 'SIG_AZIZ' }
  | { type: 'SIGNATURES_DONE' }
  // Bulldozer arc
  | { type: 'VISITED_DE_ROMA' }
  | { type: 'BULLDOZER_DEFEATED' }
  // Geest arc
  | { type: 'GEEST_ENCOUNTERED' }
  | { type: 'GEEST_DEFEATED' }
  // Mayor arc
  | { type: 'MET_MAYOR' }
  | { type: 'MAYOR_BRIEFED' }
  // Factions
  | { type: 'FACTION_MOROCCAN' }
  | { type: 'FACTION_TURKISH' }
  | { type: 'FACTION_FLEMISH' }
  | { type: 'FACTION_ART' }
  | { type: 'FACTION_SCHOOL' }
  | { type: 'FACTION_MOSQUE' }
  | { type: 'FACTION_FRITUUR' }
  // Inventory / stats
  | { type: 'ADD_ITEM';    itemId: string }
  | { type: 'REMOVE_ITEM'; itemId: string }
  | { type: 'ADD_COINS';   amount: number }
  | { type: 'REMOVE_COINS'; amount: number }
  | { type: 'SET_HP';      hp: number }
  | { type: 'GAIN_XP';     amount: number }
  | { type: 'SET_NAME';    name: string };

// ── Machine ──────────────────────────────────────────────────────────────────

export const GameMachine = createMachine(
  {
    id: 'game',
    type: 'parallel',

    context: {
      coins:     5,
      xp:        0,
      hp:        20,
      maxHp:     20,
      level:     1,
      xpNext:    100,
      inventory: [] as string[],
      skills:    [] as string[],
      name:      'Speler',
    } satisfies GameContext,

    // ── Global inventory / stat transitions (handled on root) ────────────────
    on: {
      ADD_ITEM: {
        actions: assign({
          inventory: ({ context, event }) =>
            [...context.inventory, (event as { type: 'ADD_ITEM'; itemId: string }).itemId],
        }),
      },
      REMOVE_ITEM: {
        actions: assign({
          inventory: ({ context, event }) => {
            const id  = (event as { type: 'REMOVE_ITEM'; itemId: string }).itemId;
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
          coins: ({ context, event }) =>
            Math.max(0, context.coins + (event as { type: 'ADD_COINS'; amount: number }).amount),
        }),
      },
      REMOVE_COINS: {
        actions: assign({
          coins: ({ context, event }) =>
            Math.max(0, context.coins - (event as { type: 'REMOVE_COINS'; amount: number }).amount),
        }),
      },
      SET_HP: {
        actions: assign({
          hp: ({ context, event }) =>
            Math.min(context.maxHp, Math.max(0, (event as { type: 'SET_HP'; hp: number }).hp)),
        }),
      },
      GAIN_XP: {
        actions: assign(({ context, event }) => {
          const gain   = (event as { type: 'GAIN_XP'; amount: number }).amount;
          let xp       = context.xp + gain;
          let level    = context.level;
          let xpNext   = context.xpNext;
          let maxHp    = context.maxHp;
          // Level-up loop
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
          name: ({ event }) => (event as { type: 'SET_NAME'; name: string }).name,
        }),
      },
    },

    states: {

      // ── Delivery arc ──────────────────────────────────────────────────────
      delivery: {
        initial: 'idle',
        states: {
          idle: {
            on: { MET_YUSUF: 'met' },
          },
          met: {
            on: { DELIVERY_ACCEPTED: 'accepted' },
          },
          accepted: {
            type: 'parallel',
            states: {
              pkg137: {
                initial: 'pending',
                states: {
                  pending: { on: { DELIVERED_137: 'done' } },
                  done:    { type: 'final' },
                },
              },
              pkg170: {
                initial: 'pending',
                states: {
                  pending: { on: { DELIVERED_170: 'done' } },
                  done:    { type: 'final' },
                },
              },
              pkg284: {
                initial: 'pending',
                states: {
                  pending: { on: { DELIVERED_284: 'done' } },
                  done:    { type: 'final' },
                },
              },
            },
            onDone: 'all_delivered',
          },
          all_delivered: {
            on: { DELIVERY_REWARDED: 'rewarded' },
          },
          rewarded: {
            type: 'final',
          },
        },
      },

      // ── Fabric arc ───────────────────────────────────────────────────────
      fabric: {
        initial: 'idle',
        states: {
          idle: {
            on: { MET_FATIMA: 'met' },
          },
          met: {
            on: { FABRIC_ACCEPTED: 'accepted' },
          },
          accepted: {
            on: { FABRIC_PICKED_UP: 'picked_up' },
          },
          picked_up: {
            on: { FABRIC_DELIVERED: 'completed' },
          },
          completed: {
            type: 'final',
          },
        },
      },

      // ── Flour arc ────────────────────────────────────────────────────────
      flour: {
        initial: 'idle',
        states: {
          idle: {
            on: { FLOUR_ACCEPTED: 'accepted' },
          },
          accepted: {
            on: { FLOUR_PICKED_UP: 'picked_up' },
          },
          picked_up: {
            on: { FLOUR_DELIVERED: 'completed' },
          },
          completed: {
            type: 'final',
          },
        },
      },

      // ── Oud arc ──────────────────────────────────────────────────────────
      oud: {
        initial: 'idle',
        states: {
          idle: {
            on: { OUD_ACCEPTED: 'accepted' },
          },
          accepted: {
            on: { OUD_FOUND: 'found' },
          },
          found: {
            on: { OUD_DELIVERED: 'completed' },
          },
          completed: {
            type: 'final',
          },
        },
      },

      // ── Signatures arc ───────────────────────────────────────────────────
      signatures: {
        initial: 'idle',
        states: {
          idle: {
            // Unlocked once player has community trust (fabric done)
            on: {
              SIG_FATIMA: 'collecting',
              SIG_OMAR:   'collecting',
              SIG_REZA:   'collecting',
              SIG_BAERT:  'collecting',
              SIG_AZIZ:   'collecting',
            },
          },
          collecting: {
            type: 'parallel',
            states: {
              fatima_sig: {
                initial: 'pending',
                states: {
                  pending: { on: { SIG_FATIMA: 'done' } },
                  done:    { type: 'final' },
                },
              },
              omar_sig: {
                initial: 'pending',
                states: {
                  pending: { on: { SIG_OMAR: 'done' } },
                  done:    { type: 'final' },
                },
              },
              reza_sig: {
                initial: 'pending',
                states: {
                  pending: { on: { SIG_REZA: 'done' } },
                  done:    { type: 'final' },
                },
              },
              baert_sig: {
                initial: 'pending',
                states: {
                  pending: { on: { SIG_BAERT: 'done' } },
                  done:    { type: 'final' },
                },
              },
              aziz_sig: {
                initial: 'pending',
                states: {
                  pending: { on: { SIG_AZIZ: 'done' } },
                  done:    { type: 'final' },
                },
              },
            },
            onDone: 'completed',
          },
          completed: {
            on: { SIGNATURES_DONE: 'rewarded' },
          },
          rewarded: {
            type: 'final',
          },
        },
      },

      // ── Bulldozer arc ────────────────────────────────────────────────────
      bulldozer: {
        initial: 'idle',
        states: {
          idle: {
            on: { VISITED_DE_ROMA: 'de_roma_visited' },
          },
          de_roma_visited: {
            on: { BULLDOZER_DEFEATED: 'completed' },
          },
          completed: {
            type: 'final',
          },
        },
      },

      // ── Geest arc ────────────────────────────────────────────────────────
      geest: {
        initial: 'idle',
        states: {
          idle: {
            on: { GEEST_ENCOUNTERED: 'encountered' },
          },
          encountered: {
            on: { GEEST_DEFEATED: 'completed' },
          },
          completed: {
            type: 'final',
          },
        },
      },

      // ── Mayor arc ────────────────────────────────────────────────────────
      mayor: {
        initial: 'idle',
        states: {
          idle: {
            on: { MET_MAYOR: 'met' },
          },
          met: {
            on: { MAYOR_BRIEFED: 'briefed' },
          },
          briefed: {
            type: 'final',
          },
        },
      },

      // ── Factions — parallel sub-regions ──────────────────────────────────
      factions: {
        type: 'parallel',
        states: {
          moroccan: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_MOROCCAN: 'completed' } },
              completed: { type: 'final' },
            },
          },
          turkish: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_TURKISH: 'completed' } },
              completed: { type: 'final' },
            },
          },
          flemish: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_FLEMISH: 'completed' } },
              completed: { type: 'final' },
            },
          },
          art: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_ART: 'completed' } },
              completed: { type: 'final' },
            },
          },
          school: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_SCHOOL: 'completed' } },
              completed: { type: 'final' },
            },
          },
          mosque: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_MOSQUE: 'completed' } },
              completed: { type: 'final' },
            },
          },
          frituur: {
            initial: 'idle',
            states: {
              idle:      { on: { FACTION_FRITUUR: 'completed' } },
              completed: { type: 'final' },
            },
          },
        },
      },
    },
  },
);

// ── Snapshot type helper ─────────────────────────────────────────────────────

// We infer the snapshot type generically to avoid deep TypeScript coupling.
type AnySnapshot = { value: unknown; context: GameContext };

/**
 * Read a nested XState v5 machine state value safely.
 *
 * XState v5 encodes state as:
 *   - A string when the current state has no active children:
 *       { delivery: "idle" }
 *   - A nested object when the current state is compound/parallel:
 *       { delivery: { accepted: { pkg137: "pending", pkg170: "done" } } }
 *
 * This function descends the path, handling both string-leaves and object-nodes.
 */
function stateIs(value: unknown, ...path: string[]): boolean {
  if (path.length === 0) return true;
  const [head, ...rest] = path;

  // String leaf: the current node encodes the active child state as a string
  if (typeof value === 'string') {
    // If we've consumed all path segments except the last, check equality
    return rest.length === 0 && value === head;
  }

  if (typeof value !== 'object' || value === null) return false;
  const map = value as Record<string, unknown>;
  if (!(head in map)) return false;
  if (rest.length === 0) return true;
  return stateIs(map[head], ...rest);
}

/**
 * Check whether a top-level parallel region is in the given state.
 * Handles both string values ({ delivery: "idle" }) and object values.
 */
function regionIs(value: unknown, region: string, state: string): boolean {
  if (typeof value !== 'object' || value === null) return false;
  const map = value as Record<string, unknown>;
  const regionVal = map[region];
  // Simple string case: { delivery: "met" }
  if (typeof regionVal === 'string') return regionVal === state;
  // Compound case: { delivery: { accepted: { ... } } }
  if (typeof regionVal === 'object' && regionVal !== null) {
    return state in (regionVal as Record<string, unknown>);
  }
  return false;
}

/**
 * Check a sub-state inside signatures.collecting.<sig>.<state>.
 * The XState value for the signatures collecting region looks like:
 *   { signatures: { collecting: { fatima_sig: "done", omar_sig: "pending", ... } } }
 */
function sigRegionIs(value: unknown, sig: string, state: string): boolean {
  return stateIs(value, 'signatures', 'collecting', sig, state);
}

function factionIs(value: unknown, faction: string): boolean {
  return regionIs(
    (typeof value === 'object' && value !== null)
      ? (value as Record<string, unknown>)['factions']
      : value,
    faction,
    'completed',
  );
}

/**
 * flagBridge — maps the current machine snapshot state to the flat
 * `Record<string, boolean>` format that dialogue.json conditions expect.
 *
 * This is the backwards-compatibility layer: you do NOT need to rewrite
 * any dialogue.json entries while the migration is in progress.
 */
export function flagBridge(snapshot: AnySnapshot): Record<string, boolean> {
  const v = snapshot.value;

  // Delivery region helpers
  const deliveryMet      = regionIs(v, 'delivery', 'met')
                         || regionIs(v, 'delivery', 'accepted')
                         || regionIs(v, 'delivery', 'all_delivered')
                         || regionIs(v, 'delivery', 'rewarded');
  const deliveryAccepted = regionIs(v, 'delivery', 'accepted')
                         || regionIs(v, 'delivery', 'all_delivered')
                         || regionIs(v, 'delivery', 'rewarded');

  // For parallel sub-states inside 'accepted' we check deeper
  const delivered137 = deliveryAccepted && stateIs(v, 'delivery', 'accepted', 'pkg137', 'done')
                     || regionIs(v, 'delivery', 'all_delivered')
                     || regionIs(v, 'delivery', 'rewarded');
  const delivered170 = deliveryAccepted && stateIs(v, 'delivery', 'accepted', 'pkg170', 'done')
                     || regionIs(v, 'delivery', 'all_delivered')
                     || regionIs(v, 'delivery', 'rewarded');
  const delivered284 = deliveryAccepted && stateIs(v, 'delivery', 'accepted', 'pkg284', 'done')
                     || regionIs(v, 'delivery', 'all_delivered')
                     || regionIs(v, 'delivery', 'rewarded');
  const deliveryDone = regionIs(v, 'delivery', 'rewarded');

  // Fabric
  const metFatima      = !regionIs(v, 'fabric', 'idle');
  const fabricAccepted = regionIs(v, 'fabric', 'accepted')
                       || regionIs(v, 'fabric', 'picked_up')
                       || regionIs(v, 'fabric', 'completed');
  const fabricActive   = regionIs(v, 'fabric', 'picked_up'); // stunt_quest_active
  const fabricDone     = regionIs(v, 'fabric', 'completed');  // stunt_quest_done
  const hasCommunityTrust = fabricDone;

  // Flour
  const flourAccepted = regionIs(v, 'flour', 'accepted')
                      || regionIs(v, 'flour', 'picked_up')
                      || regionIs(v, 'flour', 'completed');
  const hasFlour      = regionIs(v, 'flour', 'picked_up');
  const flourDone     = regionIs(v, 'flour', 'completed');    // omar_flour_done

  // Oud
  const oudAccepted = regionIs(v, 'oud', 'accepted')
                    || regionIs(v, 'oud', 'found')
                    || regionIs(v, 'oud', 'completed');
  const hasOudItem  = regionIs(v, 'oud', 'found');
  const oudDone     = regionIs(v, 'oud', 'completed');        // reza_quest_done

  // Signatures
  const sigsStarted  = !regionIs(v, 'signatures', 'idle');
  const sigFatima    = sigsStarted && (
                         sigRegionIs(v, 'fatima_sig', 'done')
                         || regionIs(v, 'signatures', 'completed')
                         || regionIs(v, 'signatures', 'rewarded')
                       );
  const sigOmar      = sigsStarted && (
                         sigRegionIs(v, 'omar_sig', 'done')
                         || regionIs(v, 'signatures', 'completed')
                         || regionIs(v, 'signatures', 'rewarded')
                       );
  const sigReza      = sigsStarted && (
                         sigRegionIs(v, 'reza_sig', 'done')
                         || regionIs(v, 'signatures', 'completed')
                         || regionIs(v, 'signatures', 'rewarded')
                       );
  const sigBaert     = sigsStarted && (
                         sigRegionIs(v, 'baert_sig', 'done')
                         || regionIs(v, 'signatures', 'completed')
                         || regionIs(v, 'signatures', 'rewarded')
                       );
  const sigAziz      = sigsStarted && (
                         sigRegionIs(v, 'aziz_sig', 'done')
                         || regionIs(v, 'signatures', 'completed')
                         || regionIs(v, 'signatures', 'rewarded')
                       );
  const sigsDone     = regionIs(v, 'signatures', 'completed')
                     || regionIs(v, 'signatures', 'rewarded'); // speculator_threatened

  // Bulldozer
  const visitedDeRoma    = !regionIs(v, 'bulldozer', 'idle');
  const bulldozerDefeated = regionIs(v, 'bulldozer', 'completed'); // has_permit_doc

  // Geest
  const geestEncountered = !regionIs(v, 'geest', 'idle');
  const geestDefeated    = regionIs(v, 'geest', 'completed');  // kracht_van_gemeenschap

  // Mayor
  const metMayor    = !regionIs(v, 'mayor', 'idle');
  const mayorBriefed = regionIs(v, 'mayor', 'briefed');        // act4_started

  // Factions
  const moroccanDone = factionIs(v, 'moroccan');
  const turkishDone  = factionIs(v, 'turkish');
  const flemishDone  = factionIs(v, 'flemish');
  const artDone      = factionIs(v, 'art');
  const schoolDone   = factionIs(v, 'school');
  const mosqueDone   = factionIs(v, 'mosque');
  const frituurDone  = factionIs(v, 'frituur');

  const factionCount = [
    moroccanDone, turkishDone, flemishDone, artDone,
    schoolDone, mosqueDone, frituurDone,
  ].filter(Boolean).length;

  return {
    // Delivery
    met_yusuf:                   deliveryMet,
    delivery_accepted:           deliveryAccepted,
    delivery_packages_received:  deliveryAccepted,
    delivered_137:               delivered137,
    delivered_170:               delivered170,
    delivered_284:               delivered284,
    delivery_done:               deliveryDone,
    q_starter_delivery_done:     deliveryDone,

    // Fabric / Fatima
    met_fatima:           metFatima,
    fabric_quest_accepted: fabricAccepted,
    knows_stunt_location:  fabricAccepted,
    stunt_quest_active:    fabricActive,
    stunt_quest_done:      fabricDone,
    has_community_trust:   hasCommunityTrust,
    q_fabric_quest_done:   fabricDone,

    // Flour
    omar_flour_asked:   flourAccepted,
    flour_quest_accepted: flourAccepted,
    has_flour:          hasFlour,
    omar_flour_done:    flourDone,
    knows_samen_tafel:  flourDone,
    q_flour_shortage_done: flourDone,

    // Oud
    oud_quest_accepted:  oudAccepted,
    has_oud_string_item: hasOudItem,
    reza_quest_done:     oudDone,
    q_oud_string_done:   oudDone,

    // Signatures
    sig_fatima:          sigFatima,
    sig_omar:            sigOmar,
    sig_reza:            sigReza,
    sig_baert:           sigBaert,
    sig_aziz:            sigAziz,
    met_aziz:            sigAziz,
    speculator_threatened: sigsDone,
    q_signatures_done:   sigsDone,

    // Bulldozer / De Roma
    visited_de_roma:    visitedDeRoma,
    has_permit_doc:     bulldozerDefeated,
    q_bulldozer_done:   bulldozerDefeated,

    // Geest
    geest_encountered:      geestEncountered,
    kracht_van_gemeenschap: geestDefeated,
    q_geest_88_done:        geestDefeated,

    // Mayor
    met_mayor:         metMayor,
    act4_briefed:      metMayor,
    act4_started:      mayorBriefed,
    q_mayor_meeting_done: metMayor,

    // Factions
    fatima_convinced:         moroccanDone,
    samen_tafel_faction_1:    moroccanDone,
    q_faction_moroccan_done:  moroccanDone,

    tine_faction_convinced:   turkishDone,
    samen_tafel_faction_2:    turkishDone,
    q_faction_turkish_done:   turkishDone,

    baert_faction_convinced:  flemishDone,
    samen_tafel_faction_3:    flemishDone,
    q_faction_flemish_done:   flemishDone,

    art_faction_convinced:    artDone,
    samen_tafel_faction_4:    artDone,
    q_faction_art_done:       artDone,

    school_faction_convinced: schoolDone,
    samen_tafel_faction_5:    schoolDone,
    q_faction_school_done:    schoolDone,

    mosque_faction_convinced: mosqueDone,
    samen_tafel_faction_6:    mosqueDone,
    q_faction_mosque_done:    mosqueDone,

    frituur_faction_convinced: frituurDone,
    samen_tafel_faction_7:    frituurDone,
    q_faction_frituur_done:   frituurDone,

    // Composite helpers used by dialogue conditions
    met_imam:             mosqueDone,
    samen_tafel_faction_N_eq_7: factionCount === 7,
  };
}

/** Convenience: get the numeric faction count from a snapshot. */
export function getFactionCount(snapshot: AnySnapshot): number {
  const flags = flagBridge(snapshot);
  return [
    flags['q_faction_moroccan_done'],
    flags['q_faction_turkish_done'],
    flags['q_faction_flemish_done'],
    flags['q_faction_art_done'],
    flags['q_faction_school_done'],
    flags['q_faction_mosque_done'],
    flags['q_faction_frituur_done'],
  ].filter(Boolean).length;
}

/** Get player stats from snapshot context (convenience wrapper). */
export function getSnapshot(actor: { getSnapshot(): { value: unknown; context: GameContext } }) {
  return actor.getSnapshot();
}
