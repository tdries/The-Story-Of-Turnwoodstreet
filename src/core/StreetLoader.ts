/**
 * StreetLoader — typed access to all per-street JSON data files.
 *
 * To add a new street:
 *   1. Create src/data/streets/{streetId}/street.json
 *   2. Create src/data/streets/{streetId}/npcs.json
 *   3. Create src/data/streets/{streetId}/quests.json
 *   4. Create src/data/streets/{streetId}/enemies.json
 *   5. Register the imports below under the streetId key.
 *
 * The engine (OverworldScene, StreetMachine, StateManager) reads from
 * the active StreetDef — no street-specific code anywhere else.
 */

// ── Turnhoutsebaan imports ────────────────────────────────────────────────────
import tbStreet  from '@data/streets/turnhoutsebaan/street.json';
import tbNpcs    from '@data/streets/turnhoutsebaan/npcs.json';
import tbQuests  from '@data/streets/turnhoutsebaan/quests.json';
import tbEnemies from '@data/streets/turnhoutsebaan/enemies.json';

// ── Types ─────────────────────────────────────────────────────────────────────

export interface NpcDef {
  id:         string;
  texture:    string;
  x:          number;
  yOffset:    number;
  dialogueId: string;
  name?:      string;
  showFlag?:  string;
}

export interface BuildingEntry {
  number:      number;
  tile:        number;
  name:        string;
  type:        string;
  note?:       string;
  spanNumbers?: number[];
}

export interface StreetSection {
  id:         string;
  label:      string;
  postcode:   string;
  numberMin:  number;
  numberMax:  number;
  buildings:  BuildingEntry[];
}

export interface StreetDef {
  id:               string;
  name:             string;
  oddSide:          'north' | 'south';
  evenSide:         'north' | 'south';
  tileWidthUnits:   number;
  residentialTiles: number[];
  vacantTile:       number;
  sections:         StreetSection[];
}

export interface LocationTrigger {
  type:           'dialogue' | 'battle';
  x:              number;
  width:          number;
  dialogueId?:    string;
  enemyId?:       string;
  onceFlag:       string;
  requiredFlags?: Record<string, boolean>;
}

export interface QuestsDef {
  machineId:        string;
  context:          Record<string, unknown>;
  regions:          QuestRegionDef[];
  flagToEvent:      Record<string, string>;
  flagBridge:       FlagBridgeRule[];
  locationTriggers: LocationTrigger[];
  navTargets:       NavTargetDef[];
  hintTexts:        HintTextDef[];
}

export interface QuestRegionDef {
  id:          string;
  initial?:    string;
  type?:       'parallel';
  states?:     Record<string, QuestStateDef>;
  subRegions?: SubRegionDef[];
}

export interface QuestStateDef {
  on?:         Record<string, string>;
  type?:       'final' | 'parallel';
  subRegions?: SubRegionDef[];
  onDone?:     string;
}

export interface SubRegionDef {
  id:    string;
  event: string;
}

export interface FlagBridgeRule {
  flag:       string;
  region?:    string;
  faction?:   string;
  state?:     string;
  notState?:  string;
  anyState?:  string[];
  orSubState?: string[];
}

export interface NavTargetDef {
  condition?:  Record<string, string>;
  faction?:    string;
  done?:       boolean;
  x:           number;
  label:       string;
  subState?:   string[];   // additional stateIs() path that must also be true
}

export interface HintTextDef {
  condition?:         Record<string, string>;
  allFactionsComplete?: boolean;
  text:               string;
}

export interface EnemyDef {
  id:               string;
  name:             string;
  hp:               number;
  atk:              number;
  def:              number;
  spd:              number;
  xp:               number;
  coins:            number;
  loot:             string[];
  post_battle_flag?: string;
  taunt:            string[];
}

export interface StreetBundle {
  street:   StreetDef;
  npcs:     NpcDef[];
  quests:   QuestsDef;
  enemies:  Record<string, EnemyDef>;
}

// ── Registry ──────────────────────────────────────────────────────────────────

const REGISTRY: Record<string, StreetBundle> = {
  turnhoutsebaan: {
    street:  tbStreet  as unknown as StreetDef,
    npcs:    (tbNpcs as { npcs: NpcDef[] }).npcs,
    quests:  tbQuests  as unknown as QuestsDef,
    enemies: tbEnemies as unknown as Record<string, EnemyDef>,
  },
};

// ── Loader ────────────────────────────────────────────────────────────────────

export class StreetLoader {
  private static _active: StreetBundle = REGISTRY['turnhoutsebaan'];

  /** Set the active street. Call before creating OverworldScene. */
  static load(streetId: string): void {
    const bundle = REGISTRY[streetId];
    if (!bundle) throw new Error(`[StreetLoader] Unknown street: "${streetId}"`);
    StreetLoader._active = bundle;
    console.log(`[StreetLoader] Loaded street: ${bundle.street.name}`);
  }

  static get street():  StreetDef               { return StreetLoader._active.street;  }
  static get npcs():    NpcDef[]                 { return StreetLoader._active.npcs;    }
  static get quests():  QuestsDef                { return StreetLoader._active.quests;  }
  static get enemies(): Record<string, EnemyDef> { return StreetLoader._active.enemies; }
}
