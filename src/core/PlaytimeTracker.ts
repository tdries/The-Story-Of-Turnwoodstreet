import { supabase }     from '@core/SupabaseClient';
import { stateManager } from '@core/StateManager';

/**
 * PlaytimeTracker — counts seconds the player sprite is moving and syncs
 * to Supabase every 60 s.  Only counts real movement, not idle browser time.
 *
 * Also maintains `itemsCollected`: the cumulative set of every item the player
 * has EVER picked up (never shrinks, even after items are handed over).
 * Stored in the `items_collected` column of the `players` table.
 *
 * DB column needed:  ALTER TABLE players ADD COLUMN items_collected text[] DEFAULT '{}';
 */
class PlaytimeTracker {
  private sessionMs      = 0;   // ms of movement accumulated this session
  private baseSeconds    = 0;   // seconds already stored in DB from prior sessions
  private frameAccum     = 0;   // leftover ms < 1000
  private syncing        = false;
  private itemsCollected = new Set<string>();

  /** Called from OverworldScene.update() every frame. */
  tick(delta: number, isMoving: boolean): void {
    if (!isMoving) return;
    this.frameAccum += delta;
    if (this.frameAccum >= 1000) {
      const secs = Math.floor(this.frameAccum / 1000);
      this.sessionMs += secs * 1000;
      this.frameAccum -= secs * 1000;
    }
  }

  get totalSeconds(): number {
    return this.baseSeconds + Math.floor(this.sessionMs / 1000);
  }

  /** Called on login: load prior playtime + items_collected and write profile. */
  async loadFromDB(): Promise<void> {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    const { data } = await supabase
      .from('players')
      .select('playtime_seconds, items_collected')
      .eq('user_id', user.id)
      .single();
    if (data) {
      this.baseSeconds = data.playtime_seconds ?? 0;
      for (const id of (data.items_collected ?? [])) this.itemsCollected.add(id);
    }

    await supabase.from('players').upsert({
      user_id:          user.id,
      display_name:     user.user_metadata?.full_name
                     ?? user.user_metadata?.name
                     ?? user.user_metadata?.user_name
                     ?? 'Anon',
      email:            user.email ?? null,
      avatar_url:       user.user_metadata?.avatar_url
                     ?? user.user_metadata?.picture
                     ?? null,
      playtime_seconds: this.baseSeconds,
      updated_at:       new Date().toISOString(),
    }, { onConflict: 'user_id' });
  }

  /** Upsert current playtime + cumulative items to DB. */
  async sync(): Promise<void> {
    if (this.syncing) return;
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    // Merge current inventory into the cumulative set
    for (const id of stateManager.get().player.inventory) this.itemsCollected.add(id);

    this.syncing = true;
    try {
      const { error } = await supabase.from('players').upsert({
        user_id:          user.id,
        display_name:     user.user_metadata?.full_name
                       ?? user.user_metadata?.name
                       ?? user.user_metadata?.user_name
                       ?? 'Anon',
        email:            user.email ?? null,
        avatar_url:       user.user_metadata?.avatar_url
                       ?? user.user_metadata?.picture
                       ?? null,
        playtime_seconds:  this.totalSeconds,
        items_collected:   [...this.itemsCollected],
        updated_at:        new Date().toISOString(),
      }, { onConflict: 'user_id' });
      if (error) console.error('[PlaytimeTracker] sync error:', error);
      else console.log('[PlaytimeTracker] synced', this.totalSeconds, 's');
    } finally {
      this.syncing = false;
    }
  }

  debug(): void {
    console.log('[PlaytimeTracker] base:', this.baseSeconds, 's | session:', Math.floor(this.sessionMs / 1000), 's | total:', this.totalSeconds, 's');
  }

  /** Fetch top-50 scoreboard rows with feedback, guestbook and item history. */
  static async getScoreboard(): Promise<Array<{
    display_name:     string;
    avatar_url:       string | null;
    playtime_seconds: number;
    user_id:          string;
    feedback_count:   number;
    guestbook_count:  number;
    items_collected:  string[] | null;
  }>> {
    const { data: players } = await supabase
      .from('players')
      .select('user_id, display_name, avatar_url, playtime_seconds, items_collected')
      .order('playtime_seconds', { ascending: false })
      .limit(50);

    if (!players || players.length === 0) return [];

    const userIds = players.map(p => p.user_id).filter(Boolean);

    const [{ data: feedbacks }, { data: guestbooks }] = await Promise.all([
      supabase.from('feedback_submissions').select('user_id').in('user_id', userIds),
      supabase.from('guestbook').select('user_id').in('user_id', userIds),
    ]);

    const fbCount: Record<string, number> = {};
    const gbCount: Record<string, number> = {};
    for (const f of feedbacks  ?? []) if (f.user_id) fbCount[f.user_id] = (fbCount[f.user_id] ?? 0) + 1;
    for (const g of guestbooks ?? []) if (g.user_id) gbCount[g.user_id] = (gbCount[g.user_id] ?? 0) + 1;

    return players.map(p => ({
      ...p,
      items_collected:  (p.items_collected as string[] | null) ?? null,
      feedback_count:   fbCount[p.user_id] ?? 0,
      guestbook_count:  gbCount[p.user_id] ?? 0,
    }));
  }
}

export { PlaytimeTracker };
export const playtimeTracker = new PlaytimeTracker();
