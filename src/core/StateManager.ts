import { createActor }            from 'xstate';
import type { SnapshotFrom }      from 'xstate';
import { supabase }               from '@core/SupabaseClient';
import { GameMachine, flagBridge } from '@systems/GameMachine';
import type { GameEvent, GameContext } from '@systems/GameMachine';
import { gameEventLogger }        from '@core/GameEventLogger';

/** The persisted snapshot type for GameMachine. */
type GameSnapshot = SnapshotFrom<typeof GameMachine>;

/**
 * Global game state — now powered by XState.
 * Lives outside Phaser scenes so it survives scene transitions.
 */
export interface PlayerState {
  name:   string;
  hp:     number;
  maxHp:  number;
  coins:  number;
  level:  number;
  xp:     number;
  xpNext: number;
  skills: string[];
  inventory: string[];
}

export interface QuestFlags {
  [key: string]: boolean | number | string;
}

export interface GameState {
  player:          PlayerState;
  questFlags:      QuestFlags;         // kept for serialisation compat
  currentMap:      string;
  spawnPoint:      { x: number; y: number };
  playtimeMs:      number;
  gameTimeMinutes: number;
}

// ── Flag → Event bridge map ───────────────────────────────────────────────────
// Maps known flag keys (set by dialogue.json) to machine events.
// If a flag key is listed here the bridge fires the corresponding event
// instead of (or in addition to) storing it in legacy questFlags.

const FLAG_TO_EVENT: Record<string, GameEvent | null> = {
  met_yusuf:                   { type: 'MET_YUSUF' },
  delivery_accepted:           { type: 'DELIVERY_ACCEPTED' },
  delivery_packages_received:  { type: 'DELIVERY_ACCEPTED' },   // alias
  delivered_137:               { type: 'DELIVERED_137' },
  delivered_170:               { type: 'DELIVERED_170' },
  delivered_284:               { type: 'DELIVERED_284' },
  delivery_done:               { type: 'DELIVERY_REWARDED' },

  met_fatima:                  { type: 'MET_FATIMA' },
  fabric_quest_accepted:       { type: 'FABRIC_ACCEPTED' },
  knows_stunt_location:        null,                             // informational only
  stunt_quest_active:          { type: 'FABRIC_PICKED_UP' },
  stunt_quest_done:            { type: 'FABRIC_DELIVERED' },

  omar_flour_asked:            { type: 'FLOUR_ACCEPTED' },
  flour_quest_accepted:        { type: 'FLOUR_ACCEPTED' },
  has_flour:                   { type: 'FLOUR_PICKED_UP' },
  omar_flour_done:             { type: 'FLOUR_DELIVERED' },

  oud_quest_accepted:          { type: 'OUD_ACCEPTED' },
  has_oud_string_item:         { type: 'OUD_FOUND' },
  reza_quest_done:             { type: 'OUD_DELIVERED' },

  sig_fatima:                  { type: 'SIG_FATIMA' },
  sig_omar:                    { type: 'SIG_OMAR' },
  sig_reza:                    { type: 'SIG_REZA' },
  sig_baert:                   { type: 'SIG_BAERT' },
  sig_aziz:                    { type: 'SIG_AZIZ' },
  speculator_threatened:       { type: 'SIGNATURES_DONE' },

  visited_de_roma:             { type: 'VISITED_DE_ROMA' },
  has_permit_doc:              { type: 'BULLDOZER_DEFEATED' },

  geest_encountered:           { type: 'GEEST_ENCOUNTERED' },
  kracht_van_gemeenschap:      { type: 'GEEST_DEFEATED' },

  met_mayor:                   { type: 'MET_MAYOR' },
  act4_briefed:                null,
  act4_started:                { type: 'MAYOR_BRIEFED' },

  fatima_convinced:            { type: 'FACTION_MOROCCAN' },
  tine_faction_convinced:      { type: 'FACTION_TURKISH' },
  baert_faction_convinced:     { type: 'FACTION_FLEMISH' },
  art_faction_convinced:       { type: 'FACTION_ART' },
  school_faction_convinced:    { type: 'FACTION_SCHOOL' },
  mosque_faction_convinced:    { type: 'FACTION_MOSQUE' },
  frituur_faction_convinced:   { type: 'FACTION_FRITUUR' },
};

// ── Persisted snapshot shape ──────────────────────────────────────────────────

interface SaveData {
  machineSnapshot: GameSnapshot | null | undefined;
  currentMap:      string;
  spawnPoint:      { x: number; y: number };
  playtimeMs:      number;
  gameTimeMinutes: number;
  // Legacy questFlags kept so cloud saves don't break on transition
  questFlags?:     QuestFlags;
}

// ── StateManager ──────────────────────────────────────────────────────────────

class StateManager {
  private actor: ReturnType<typeof createActor<typeof GameMachine>>;
  private currentMap:       string = 'borgerhout_main';
  private spawnPoint:       { x: number; y: number } = { x: 64, y: 146 };
  private playtimeMs:       number = 0;
  private gameTimeMinutes:  number = 9 * 60;
  /** Legacy flag store — still written for dialogue conditions not yet in bridge. */
  private extraFlags:       QuestFlags = {};

  constructor() {
    const persisted = this._loadPersistedSnapshot();
    if (persisted) {
      this.actor = persisted.snapshot
        ? createActor(GameMachine, { snapshot: persisted.snapshot })
        : createActor(GameMachine);
      this.currentMap      = persisted.currentMap;
      this.spawnPoint      = persisted.spawnPoint;
      this.playtimeMs      = persisted.playtimeMs;
      this.gameTimeMinutes = persisted.gameTimeMinutes;
      this.extraFlags      = persisted.questFlags ?? {};
    } else {
      this.actor = createActor(GameMachine);
    }
    this.actor.start();
    this._attachDebugLogger();
    gameEventLogger.attachSnapshotGetter(
      () => this.actor.getSnapshot() as { value: unknown; context: GameContext },
    );
  }

  private _attachDebugLogger(): void {
    if (!import.meta.env.DEV) return;

    this.actor.subscribe(snapshot => {
      const ctx = snapshot.context as typeof snapshot.context;
      const flags = flagBridge(snapshot as { value: unknown; context: GameContext });
      console.groupCollapsed(
        `%c[XState] transition`,
        'color: #FFD700; font-weight: bold',
      );
      console.log('state   :', snapshot.value);
      console.log('context :', { coins: ctx.coins, xp: ctx.xp, hp: ctx.hp, level: ctx.level, skills: ctx.skills, inventory: ctx.inventory });
      console.log('flags   :', flags);
      console.groupEnd();
    });
  }

  // ── Actor access ────────────────────────────────────────────────────────────

  /** Start the actor (idempotent — constructor already calls start()). */
  start(): void {
    // Actor started in constructor; exposed here for explicit callers.
  }

  /** Send a typed event directly to the machine (and log it). */
  send(event: GameEvent): void {
    this.actor.send(event);
    gameEventLogger.logXStateEvent(event.type);
  }

  /** Raw machine snapshot — used by getNavTarget and the debug logger. */
  getSnapshot(): { value: unknown; context: GameContext } {
    return this.actor.getSnapshot() as { value: unknown; context: GameContext };
  }

  // ── PlayerState facade ──────────────────────────────────────────────────────

  /** Returns current player stats derived from actor context. */
  getPlayer(): PlayerState {
    const ctx = this._ctx();
    return {
      name:      ctx.name,
      hp:        ctx.hp,
      maxHp:     ctx.maxHp,
      coins:     ctx.coins,
      level:     ctx.level,
      xp:        ctx.xp,
      xpNext:    ctx.xpNext,
      skills:    [...ctx.skills],
      inventory: [...ctx.inventory],
    };
  }

  /**
   * Legacy `.get()` — returns a GameState-shaped object for backwards compat.
   * Quest flags come from the machine bridge + any extra flags.
   */
  get(): GameState {
    return {
      player:          this.getPlayer(),
      questFlags:      this.getFlags(),
      currentMap:      this.currentMap,
      spawnPoint:      this.spawnPoint,
      playtimeMs:      this.playtimeMs,
      gameTimeMinutes: this.gameTimeMinutes,
    };
  }

  // ── Flag bridge ─────────────────────────────────────────────────────────────

  /**
   * Returns all boolean quest flags derived from machine state + extraFlags.
   * This is what DialogueSystem conditions read via getFlag().
   */
  getFlags(): QuestFlags {
    const machineFlags = flagBridge(this.actor.getSnapshot() as {
      value: unknown;
      context: GameContext;
    });
    // extraFlags override / supplement machine-derived flags
    return { ...machineFlags, ...this.extraFlags };
  }

  getFlag(key: string): boolean | number | string | undefined {
    return this.getFlags()[key];
  }

  /**
   * setFlag — bridge method called by DialogueSystem / QuestSystem.
   * Translates known flag keys into machine events; stores unknown flags
   * in extraFlags for dialogue conditions not yet migrated.
   */
  setFlag(key: string, value: boolean | number | string): void {
    // Only translate true-ish boolean flags to machine events
    if (value === true && key in FLAG_TO_EVENT) {
      const event = FLAG_TO_EVENT[key];
      if (event !== null) {
        this.actor.send(event);
        gameEventLogger.logXStateEvent(event.type);
      }
      // Don't store in extraFlags — machine state is the source of truth
      return;
    }
    // Numeric/string flags or flags not in the bridge go to extraFlags
    this.extraFlags[key] = value;
  }

  // ── Inventory helpers ───────────────────────────────────────────────────────

  hasItem(itemId: string): boolean {
    return this._ctx().inventory.includes(itemId);
  }

  addItem(itemId: string): void {
    this.actor.send({ type: 'ADD_ITEM', itemId });
    gameEventLogger.logItemAdd(itemId);
  }

  removeItem(itemId: string): boolean {
    if (!this.hasItem(itemId)) return false;
    this.actor.send({ type: 'REMOVE_ITEM', itemId });
    gameEventLogger.logItemRemove(itemId);
    return true;
  }

  // ── Coins / XP ─────────────────────────────────────────────────────────────

  setHP(hp: number): void {
    this.actor.send({ type: 'SET_HP', hp });
  }

  addCoins(amount: number): void {
    if (amount >= 0) {
      this.actor.send({ type: 'ADD_COINS', amount });
    } else {
      this.actor.send({ type: 'REMOVE_COINS', amount: -amount });
    }
  }

  /**
   * gainXP — handled in machine (GAIN_XP event does the levelling math).
   * Returns true if a level-up occurred.
   */
  gainXP(amount: number): boolean {
    const before = this._ctx().level;
    this.actor.send({ type: 'GAIN_XP', amount });
    return this._ctx().level > before;
  }

  // ── Map / time ──────────────────────────────────────────────────────────────

  setGameTime(totalMinutes: number): void {
    this.gameTimeMinutes = Math.round(totalMinutes) % 1440;
  }

  // ── Persistence ─────────────────────────────────────────────────────────────

  save(): void {
    try {
      const data: SaveData = {
        machineSnapshot: this.actor.getPersistedSnapshot() as GameSnapshot,
        currentMap:      this.currentMap,
        spawnPoint:      this.spawnPoint,
        playtimeMs:      this.playtimeMs,
        gameTimeMinutes: this.gameTimeMinutes,
        questFlags:      this.extraFlags,
      };
      localStorage.setItem('tbaan_save_v2', JSON.stringify(data));
    } catch { /* storage full */ }
    this.saveToCloud();
  }

  private async saveToCloud(): Promise<void> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;
      const payload = {
        machineSnapshot: this.actor.getPersistedSnapshot(),
        currentMap:      this.currentMap,
        spawnPoint:      this.spawnPoint,
        playtimeMs:      this.playtimeMs,
        gameTimeMinutes: this.gameTimeMinutes,
        questFlags:      this.extraFlags,
      };
      await supabase.from('save_states').upsert(
        { user_id: user.id, state: payload, saved_at: new Date().toISOString() },
        { onConflict: 'user_id' },
      );
    } catch { /* network unavailable */ }
  }

  async loadFromCloud(): Promise<void> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;
      const { data } = await supabase
        .from('save_states')
        .select('state')
        .eq('user_id', user.id)
        .single();
      if (data?.state) {
        const s = data.state as SaveData;
        this._applyLoaded(s);
        try { localStorage.setItem('tbaan_save_v2', JSON.stringify(s)); } catch { /* ok */ }
        console.log('[StateManager] loaded from cloud');
      }
    } catch { /* keep local state */ }
  }

  private _applyLoaded(s: SaveData): void {
    this.actor.stop();
    this.actor = s.machineSnapshot
      ? createActor(GameMachine, { snapshot: s.machineSnapshot })
      : createActor(GameMachine);
    this.actor.start();
    this.currentMap      = s.currentMap      ?? 'borgerhout_main';
    this.spawnPoint      = s.spawnPoint      ?? { x: 64, y: 146 };
    this.playtimeMs      = s.playtimeMs      ?? 0;
    this.gameTimeMinutes = s.gameTimeMinutes ?? 9 * 60;
    this.extraFlags      = s.questFlags      ?? {};
  }

  private _loadPersistedSnapshot(): {
    snapshot: GameSnapshot | null;
    currentMap: string;
    spawnPoint: { x: number; y: number };
    playtimeMs: number;
    gameTimeMinutes: number;
    questFlags: QuestFlags;
  } | null {
    try {
      // Try new v2 save first
      const raw = localStorage.getItem('tbaan_save_v2');
      if (raw) {
        const s = JSON.parse(raw) as SaveData;
        return {
          snapshot:        s.machineSnapshot ?? null,
          currentMap:      s.currentMap      ?? 'borgerhout_main',
          spawnPoint:      s.spawnPoint      ?? { x: 64, y: 146 },
          playtimeMs:      s.playtimeMs      ?? 0,
          gameTimeMinutes: s.gameTimeMinutes ?? 9 * 60,
          questFlags:      s.questFlags      ?? {},
        };
      }
      // Fall back to old v1 save — migrate flags into extraFlags
      const rawV1 = localStorage.getItem('tbaan_save');
      if (rawV1) {
        const oldState = JSON.parse(rawV1) as {
          player?: Partial<GameContext>;
          questFlags?: QuestFlags;
          currentMap?: string;
          spawnPoint?: { x: number; y: number };
          playtimeMs?: number;
          gameTimeMinutes?: number;
        };
        // Return null snapshot so machine starts fresh; flags go into extraFlags
        return {
          snapshot:        null,
          currentMap:      oldState.currentMap      ?? 'borgerhout_main',
          spawnPoint:      oldState.spawnPoint      ?? { x: 64, y: 146 },
          playtimeMs:      oldState.playtimeMs      ?? 0,
          gameTimeMinutes: oldState.gameTimeMinutes ?? 9 * 60,
          questFlags:      oldState.questFlags      ?? {},
        };
      }
      return null;
    } catch {
      return null;
    }
  }

  hasSave(): boolean {
    try {
      return (
        localStorage.getItem('tbaan_save_v2') !== null ||
        localStorage.getItem('tbaan_save') !== null
      );
    } catch {
      return false;
    }
  }

  reset(): void {
    this.actor.stop();
    this.actor = createActor(GameMachine);
    this.actor.start();
    this.currentMap      = 'borgerhout_main';
    this.spawnPoint      = { x: 64, y: 146 };
    this.playtimeMs      = 0;
    this.gameTimeMinutes = 9 * 60;
    this.extraFlags      = {};
    localStorage.removeItem('tbaan_save_v2');
    localStorage.removeItem('tbaan_save');
  }

  // ── Internals ───────────────────────────────────────────────────────────────

  private _ctx(): GameContext {
    return this.actor.getSnapshot().context;
  }
}

/** Singleton — import and use anywhere. */
export const stateManager = new StateManager();
