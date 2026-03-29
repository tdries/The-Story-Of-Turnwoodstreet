/**
 * GameEventLogger — streams play-session events to Supabase for debugging.
 *
 * Notation format (one compact string per event):
 *   E»MET_YUSUF           XState machine event fired
 *   D»stunt_baert_fabric  Dialogue node opened
 *   I+fabric_bolt         Item added to inventory
 *   I-fabric_bolt         Item removed from inventory
 *   B»straatvechter:win+20xp+5c  Battle result
 *   M»borgerhout_east     Map / zone transition
 *
 * Every entry is suffixed with @[STATE] — a compact encoding of the
 * full XState machine value + player stats at that moment:
 *   [D:acc{137,170}·FA:pku·FL:idl·O:idl·S:col{fat,oma}·B:idl·G:idl·M:idl·FC:2·hp:18/25·lv:2·c:45]
 *
 * State segment abbreviations:
 *   D   delivery   (idl/met/acc{pkgs}/all/rwd)
 *   FA  fabric     (idl/met/acc/pku/cmp)
 *   FL  flour      (idl/acc/pku/cmp)
 *   O   oud        (idl/acc/fnd/cmp)
 *   S   signatures (idl/col{sigs}/cmp/rwd)
 *   B   bulldozer  (idl/vis/cmp)
 *   G   geest      (idl/enc/cmp)
 *   M   mayor      (idl/met/brf)
 *   FC  factions   (0–7)
 *   hp  current/max
 *   lv  level
 *   c   coins
 */

import { supabase } from '@core/SupabaseClient';
import type { GameContext } from '@systems/GameMachine';
import { getNavTarget, getHintText } from '@systems/GameMachine';

type AnySnapshot = { value: unknown; context: GameContext };

// ── State encoder ─────────────────────────────────────────────────────────────

function regionStr(v: unknown, region: string): string {
  if (typeof v !== 'object' || v === null) return 'idl';
  const r = (v as Record<string, unknown>)[region];
  if (typeof r === 'string') return abbr(r);
  if (typeof r === 'object' && r !== null) {
    return Object.keys(r as object)[0] ? abbr(Object.keys(r as object)[0]) : '?';
  }
  return 'idl';
}

/** Abbreviate common state names to 3 chars. */
function abbr(s: string): string {
  return (
    s === 'idle'          ? 'idl' :
    s === 'accepted'      ? 'acc' :
    s === 'completed'     ? 'cmp' :
    s === 'rewarded'      ? 'rwd' :
    s === 'picked_up'     ? 'pku' :
    s === 'encountered'   ? 'enc' :
    s === 'all_delivered' ? 'all' :
    s === 'collecting'    ? 'col' :
    s === 'de_roma_visited' ? 'vis' :
    s === 'briefed'       ? 'brf' :
    s === 'found'         ? 'fnd' :
    s.slice(0, 3)
  );
}

function deliveryEnc(v: unknown): string {
  if (typeof v !== 'object' || v === null) return 'D:idl';
  const d = (v as Record<string, unknown>)['delivery'];
  if (typeof d === 'string') return `D:${abbr(d)}`;
  if (typeof d === 'object' && d !== null) {
    const inner = (d as Record<string, unknown>)['accepted'];
    if (typeof inner === 'object' && inner !== null) {
      const done = Object.entries(inner as Record<string, unknown>)
        .filter(([, s]) => s === 'done' || (typeof s === 'object' && s !== null))
        .map(([k]) => k.replace('pkg', ''));
      return done.length > 0 ? `D:acc{${done.join(',')}}` : 'D:acc';
    }
  }
  return 'D:?';
}

function sigsEnc(v: unknown): string {
  if (typeof v !== 'object' || v === null) return 'S:idl';
  const s = (v as Record<string, unknown>)['signatures'];
  if (typeof s === 'string') return `S:${abbr(s)}`;
  if (typeof s === 'object' && s !== null) {
    const col = (s as Record<string, unknown>)['collecting'];
    if (typeof col === 'object' && col !== null) {
      const done = Object.entries(col as Record<string, unknown>)
        .filter(([, sv]) => sv === 'done')
        .map(([k]) => k.replace('_sig', '').slice(0, 3));
      return done.length > 0 ? `S:col{${done.join(',')}}` : 'S:col';
    }
    if ('completed' in (s as object)) return 'S:cmp';
    if ('rewarded'  in (s as object)) return 'S:rwd';
  }
  return 'S:?';
}

function factionsEnc(v: unknown): number {
  if (typeof v !== 'object' || v === null) return 0;
  const f = (v as Record<string, unknown>)['factions'];
  if (typeof f !== 'object' || f === null) return 0;
  return Object.values(f as Record<string, unknown>)
    .filter(fv => fv === 'completed' || (typeof fv === 'object' && fv !== null && 'completed' in (fv as object)))
    .length;
}

export function encodeState(snapshot: AnySnapshot): string {
  const v   = snapshot.value;
  const ctx = snapshot.context;
  const nav = getNavTarget(snapshot);
  const seg = [
    deliveryEnc(v),
    `FA:${regionStr(v, 'fabric')}`,
    `FL:${regionStr(v, 'flour')}`,
    `O:${regionStr(v, 'oud')}`,
    sigsEnc(v),
    `B:${regionStr(v, 'bulldozer')}`,
    `G:${regionStr(v, 'geest')}`,
    `M:${regionStr(v, 'mayor')}`,
    `FC:${factionsEnc(v)}`,
    `hp:${ctx.hp}/${ctx.maxHp}`,
    `lv:${ctx.level}`,
    `c:${ctx.coins}`,
    `N:${nav ? nav.label.replace(/\s+/g, '_') : 'nil'}`,
  ];
  return `[${seg.join('·')}]`;
}

// ── Logger ────────────────────────────────────────────────────────────────────

/** One row in the game_events table. */
interface EventRow {
  user_id:    string | null;
  session_id: string;
  seq:        number;
  notation:   string;         // the compact string
  raw_type:   string;         // 'xstate' | 'dialogue' | 'item' | 'battle' | 'map'
  raw_data:   Record<string, unknown>;
}

/** Set of XState event types that are stats/inventory, not quest events. */
const STAT_EVENTS = new Set([
  'ADD_ITEM', 'REMOVE_ITEM', 'ADD_COINS', 'REMOVE_COINS',
  'SET_HP', 'GAIN_XP', 'SET_NAME',
]);

class GameEventLogger {
  private sessionId   = crypto.randomUUID();
  private seq         = 0;
  private queue:      EventRow[] = [];
  private flushTimer: ReturnType<typeof setTimeout> | null = null;
  private userId:     string | null = null;

  /** Injected by StateManager to avoid circular imports. */
  private snapshotGetter: (() => AnySnapshot) | null = null;

  constructor() {
    // Resolve auth user; events are buffered until this resolves.
    supabase.auth.getUser().then(({ data }) => {
      const uid = data.user?.id ?? null;
      if (uid) this.activateUser(uid);
      // If not logged in, keep buffering — onAuthStateChange will activate later
    });

    // Activate logging the moment user logs in, even mid-session
    supabase.auth.onAuthStateChange((_event, session) => {
      const uid = session?.user?.id ?? null;
      if (uid && !this.userId) {
        this.activateUser(uid);
      } else if (!uid && this.userId) {
        this.userId = null;
        this.queue  = [];
      }
    });
  }

  private activateUser(uid: string): void {
    this.userId = uid;
    for (const row of this.queue) row.user_id = uid;
    void this.flush();
  }

  /** Called once by StateManager after actor is started. */
  attachSnapshotGetter(fn: () => AnySnapshot): void {
    this.snapshotGetter = fn;
  }

  // ── Public log methods ─────────────────────────────────────────────────────

  /** XState machine event fired (quest/dialogue events only, not stats). */
  logXStateEvent(eventType: string): void {
    if (STAT_EVENTS.has(eventType)) return;
    this.push('xstate', `E»${eventType}@${this.state()}`, { event: eventType });
  }

  /** Dialogue node opened by the player. */
  logDialogue(dialogueId: string): void {
    this.push('dialogue', `D»${dialogueId}@${this.state()}`, { dialogueId });
  }

  /** Item added to inventory. */
  logItemAdd(itemId: string): void {
    this.push('item', `I+${itemId}@${this.state()}`, { action: 'add', itemId });
  }

  /** Item removed from inventory. */
  logItemRemove(itemId: string): void {
    this.push('item', `I-${itemId}@${this.state()}`, { action: 'remove', itemId });
  }

  /** Battle outcome. */
  logBattle(enemyId: string, result: string, xpGain = 0, coinGain = 0): void {
    const suffix =
      result === 'victory' ? `win${xpGain  ? `+${xpGain}xp`   : ''}${coinGain ? `+${coinGain}c` : ''}` :
      result === 'escaped' ? 'esc' : 'def';
    this.push('battle', `B»${enemyId}:${suffix}@${this.state()}`,
      { enemyId, result, xpGain, coinGain });
  }

  /** Map / zone transition. */
  logMap(mapId: string): void {
    this.push('map', `M»${mapId}@${this.state()}`, { mapId });
  }

  // ── Internals ──────────────────────────────────────────────────────────────

  private state(): string {
    return this.snapshotGetter ? encodeState(this.snapshotGetter()) : '[?]';
  }

  private push(rawType: string, notation: string, rawData: Record<string, unknown>): void {
    const snap = this.snapshotGetter?.();
    const nav  = snap ? getNavTarget(snap) : null;
    const hint = snap ? getHintText(snap)  : null;

    this.queue.push({
      user_id:    this.userId,   // may be null if auth not yet resolved; stamped later
      session_id: this.sessionId,
      seq:        this.seq++,
      notation,
      raw_type:   rawType,
      raw_data:   { ...rawData, nav: nav?.label ?? null, hint },
    });
    // Only schedule a flush once we know the user (otherwise auth resolution flushes)
    if (this.userId) this.scheduleFlush();
  }

  private scheduleFlush(): void {
    if (this.flushTimer) return;
    this.flushTimer = setTimeout(() => {
      this.flushTimer = null;
      void this.flush();
    }, 2000); // batch writes every 2 s — non-blocking
  }

  private async flush(): Promise<void> {
    if (this.queue.length === 0) return;
    const batch = this.queue.splice(0, 100);
    try {
      const { error } = await supabase.from('game_events').insert(batch);
      if (error) console.error('[GameEventLogger] insert error:', error);
    } catch (err) {
      // Network unavailable — drop batch (debug telemetry, not save data)
      console.error('[GameEventLogger] network error:', err);
    }
  }
}

export const gameEventLogger = new GameEventLogger();
