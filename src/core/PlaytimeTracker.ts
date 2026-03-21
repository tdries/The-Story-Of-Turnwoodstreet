import { supabase } from '@core/SupabaseClient';

/**
 * PlaytimeTracker — counts seconds the player sprite is moving and syncs
 * to Supabase every 60 s.  Only counts real movement, not idle browser time.
 */
class PlaytimeTracker {
  private sessionMs   = 0;   // ms of movement accumulated this session
  private baseSeconds = 0;   // seconds already stored in DB from prior sessions
  private frameAccum  = 0;   // leftover ms < 1000
  private syncing     = false;

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

  /** Called on login: load prior playtime and immediately write profile. */
  async loadFromDB(): Promise<void> {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    // Load existing playtime so session adds on top
    const { data } = await supabase
      .from('players')
      .select('playtime_seconds')
      .eq('user_id', user.id)
      .single();
    if (data) this.baseSeconds = data.playtime_seconds ?? 0;

    // Immediately write profile info (name, email, avatar)
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

  /** Upsert current playtime + profile to DB. */
  async sync(): Promise<void> {
    if (this.syncing) return;
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

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
        playtime_seconds: this.totalSeconds,
        updated_at:       new Date().toISOString(),
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

  /** Fetch top-10 scoreboard rows. */
  static async getScoreboard(): Promise<Array<{
    display_name: string;
    avatar_url:   string | null;
    playtime_seconds: number;
    user_id:      string;
  }>> {
    const { data } = await supabase
      .from('players')
      .select('user_id, display_name, avatar_url, playtime_seconds')
      .order('playtime_seconds', { ascending: false })
      .limit(10);
    return data ?? [];
  }
}

export { PlaytimeTracker };
export const playtimeTracker = new PlaytimeTracker();
