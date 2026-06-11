import { createActor }            from 'xstate';
import type { SnapshotFrom }      from 'xstate';
import { supabase }               from '@core/SupabaseClient';
import { StreetLoader }           from '@core/StreetLoader';
import {
  buildMachine,
  buildFlagToEvent,
  buildFlagBridge,
  buildGetNavTarget,
  buildGetHintText,
} from '@systems/StreetMachine';
import type { GameContext }       from '@systems/StreetMachine';
import { gameEventLogger }        from '@core/GameEventLogger';

// ── Build machine + helpers from active street's quests.json ─────────────────

const _questsDef    = StreetLoader.quests;
const _machine      = buildMachine(_questsDef);
const _flagBridge   = buildFlagBridge(_questsDef);
const _getNavTarget = buildGetNavTarget(_questsDef);
const _getHintText  = buildGetHintText(_questsDef);
const _flagToEvent  = buildFlagToEvent(_questsDef);

/** Flags owned by the machine (event-mapped or bridge-derived). Persisted
 *  extraFlags must never contain these — a stale copy would permanently
 *  shadow the machine-derived value in getFlags(). */
const _machineOwnedFlags = new Set<string>([
  ...Object.keys(_questsDef.flagToEvent),
  ..._questsDef.flagBridge.map(r => r.flag),
]);

function sanitizeExtraFlags(flags: QuestFlags | undefined): QuestFlags {
  if (!flags) return {};
  const clean: QuestFlags = {};
  for (const [k, v] of Object.entries(flags)) {
    if (!_machineOwnedFlags.has(k)) clean[k] = v;
  }
  return clean;
}

/** GameEvent union — keep generic so any event string works via cast. */
type GameEvent = { type: string; [key: string]: unknown };

/** The persisted snapshot type for the generated machine. */
type GameSnapshot = SnapshotFrom<typeof _machine>;

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

// FLAG_TO_EVENT is now built from quests.json via StreetMachine — see _flagToEvent above.

// ── Persisted snapshot shape ──────────────────────────────────────────────────

interface SaveData {
  machineSnapshot: GameSnapshot | null | undefined;
  currentMap:      string;
  spawnPoint:      { x: number; y: number };
  playtimeMs:      number;
  gameTimeMinutes: number;
  // Legacy questFlags kept so cloud saves don't break on transition
  questFlags?:     QuestFlags;
  /** ISO timestamp of this save — used for newer-wins merge with cloud saves. */
  savedAt?:        string;
}

// ── StateManager ──────────────────────────────────────────────────────────────

class StateManager {
  private actor: ReturnType<typeof createActor<typeof _machine>>;
  private currentMap:       string = 'borgerhout_main';
  private spawnPoint:       { x: number; y: number } = { x: 64, y: 146 };
  private playtimeMs:       number = 0;
  private gameTimeMinutes:  number = 9 * 60;
  /** Legacy flag store — still written for dialogue conditions not yet in bridge. */
  private extraFlags:       QuestFlags = {};
  private _autoSaveTimer:   ReturnType<typeof setTimeout> | null = null;

  constructor() {
    const persisted = this._loadPersistedSnapshot();
    if (persisted) {
      this.actor = persisted.snapshot
        ? createActor(_machine, { snapshot: persisted.snapshot })
        : createActor(_machine);
      this.currentMap      = persisted.currentMap;
      this.spawnPoint      = persisted.spawnPoint;
      this.playtimeMs      = persisted.playtimeMs;
      this.gameTimeMinutes = persisted.gameTimeMinutes;
      this.extraFlags      = sanitizeExtraFlags(persisted.questFlags);
    } else {
      this.actor = createActor(_machine);
    }
    this.actor.start();
    this._attachDebugLogger();
    this._attachAutoSave();
    gameEventLogger.attachSnapshotGetter(
      () => this.actor.getSnapshot() as { value: unknown; context: GameContext },
    );
  }

  /**
   * Debounced auto-save on every XState transition.
   * Batches rapid events (e.g. dialogue flag bursts) into one save after 1.5 s.
   * This closes the gap between the explicit dialogue/battle save calls.
   */
  private _attachAutoSave(): void {
    this.actor.subscribe(() => {
      if (this._autoSaveTimer) clearTimeout(this._autoSaveTimer);
      this._autoSaveTimer = setTimeout(() => {
        this._autoSaveTimer = null;
        this.save();
      }, 1500);
    });
  }

  private _attachDebugLogger(): void {
    if (!import.meta.env.DEV) return;

    this.actor.subscribe(snapshot => {
      const ctx = snapshot.context as typeof snapshot.context;
      const flags = _flagBridge(snapshot as { value: unknown; context: GameContext });
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
    const machineFlags = _flagBridge(this.actor.getSnapshot() as {
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
    if (value === true && key in _flagToEvent) {
      const event = _flagToEvent[key];
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

  // ── Skills ──────────────────────────────────────────────────────────────────

  hasSkill(skillId: string): boolean {
    return this._ctx().skills.includes(skillId);
  }

  addSkill(skillId: string): void {
    this.actor.send({ type: 'ADD_SKILL', skillId });
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
        savedAt:         new Date().toISOString(),
      };
      localStorage.setItem('tbaan_save_v2', JSON.stringify(data));
    } catch { /* storage full */ }
    void this.saveToCloud();
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
        savedAt:         new Date().toISOString(),
      };
      // supabase-js returns errors instead of throwing — check explicitly,
      // a silently failing upsert means stale cloud saves and rollbacks.
      const { error } = await supabase.from('save_states').upsert(
        { user_id: user.id, state: payload, saved_at: new Date().toISOString() },
        { onConflict: 'user_id' },
      );
      if (error) console.error('[StateManager] cloud save FAILED:', error.message);
    } catch (e) {
      console.error('[StateManager] cloud save unreachable:', (e as Error)?.message ?? e);
    }
  }

  /** Timestamp of the local save, 0 when absent/legacy (no savedAt field). */
  private _localSavedAt(): number {
    try {
      const raw = localStorage.getItem('tbaan_save_v2');
      if (!raw) return 0;
      const t = Date.parse((JSON.parse(raw) as SaveData).savedAt ?? '');
      return Number.isFinite(t) ? t : 0;
    } catch {
      return 0;
    }
  }

  /**
   * Pull the cloud save — but never roll back local progress: the cloud copy
   * is only applied when it is strictly newer than the local save.
   */
  async loadFromCloud(): Promise<void> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;
      const { data, error } = await supabase
        .from('save_states')
        .select('state, saved_at')
        .eq('user_id', user.id)
        .single();
      if (error) {
        if (error.code !== 'PGRST116') {   // PGRST116 = no row yet, expected for new players
          console.error('[StateManager] cloud load failed:', error.message);
        }
        return;
      }
      if (!data?.state) return;

      const cloudAt = Date.parse(data.saved_at ?? '');
      const localAt = this._localSavedAt();
      if (!Number.isFinite(cloudAt) || cloudAt <= localAt) {
        console.log('[StateManager] cloud save older than local — keeping local progress');
        return;
      }

      const s = data.state as SaveData;
      s.savedAt = data.saved_at;
      this._applyLoaded(s);
      try { localStorage.setItem('tbaan_save_v2', JSON.stringify(s)); } catch { /* ok */ }
      console.log('[StateManager] loaded newer save from cloud');
    } catch (e) {
      console.error('[StateManager] cloud load unreachable:', (e as Error)?.message ?? e);
    }
  }

  private _applyLoaded(s: SaveData): void {
    this.actor.stop();
    this.actor = s.machineSnapshot
      ? createActor(_machine, { snapshot: s.machineSnapshot })
      : createActor(_machine);
    this.actor.start();
    this.currentMap      = s.currentMap      ?? 'borgerhout_main';
    this.spawnPoint      = s.spawnPoint      ?? { x: 64, y: 146 };
    this.playtimeMs      = s.playtimeMs      ?? 0;
    this.gameTimeMinutes = s.gameTimeMinutes ?? 9 * 60;
    this.extraFlags      = sanitizeExtraFlags(s.questFlags);
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
    this.actor = createActor(_machine);
    this.actor.start();
    this.currentMap      = 'borgerhout_main';
    this.spawnPoint      = { x: 64, y: 146 };
    this.playtimeMs      = 0;
    this.gameTimeMinutes = 9 * 60;
    this.extraFlags      = {};
    localStorage.removeItem('tbaan_save_v2');
    localStorage.removeItem('tbaan_save');
    // Also clear the cloud slot — otherwise the next login would "restore"
    // the abandoned run over the new game.
    void this._deleteCloudSave();
  }

  private async _deleteCloudSave(): Promise<void> {
    try {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return;
      const { error } = await supabase.from('save_states').delete().eq('user_id', user.id);
      if (error) console.error('[StateManager] cloud save delete failed:', error.message);
    } catch { /* offline — stale cloud row will be overwritten by the next save */ }
  }

  // ── Navigation / hints ──────────────────────────────────────────────────────

  getNavTarget(): { x: number; label: string } | null {
    return _getNavTarget(this.actor.getSnapshot() as { value: unknown; context: GameContext });
  }

  getHintText(): string {
    return _getHintText(this.actor.getSnapshot() as { value: unknown; context: GameContext });
  }

  // ── Internals ───────────────────────────────────────────────────────────────

  private _ctx(): GameContext {
    return this.actor.getSnapshot().context;
  }
}

/** Singleton — import and use anywhere. */
export const stateManager = new StateManager();
