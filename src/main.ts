import Phaser from 'phaser';
import { GAME_CONFIG } from '@core/GameConfig';
import { BootScene }      from '@scenes/BootScene';
import { MainMenuScene }  from '@scenes/MainMenuScene';
import { OverworldScene } from '@scenes/OverworldScene';
import { BattleScene }    from '@scenes/BattleScene';
import { stateManager }   from '@core/StateManager';
import { supabase, supabaseConfigured } from '@core/SupabaseClient';
import { playtimeTracker } from '@core/PlaytimeTracker';
import { PlaytimeTracker } from '@core/PlaytimeTracker';

const config: Phaser.Types.Core.GameConfig = {
  ...GAME_CONFIG,
  scene: [BootScene, MainMenuScene, OverworldScene, BattleScene],
};

const game = new Phaser.Game(config);

// Expose save for the mobile save button
(window as any).__saveGame = () => stateManager.save();

// Expose keyboard toggle so the feedback modal can silence Phaser input
(window as any).__setGameKeyboard = (enabled: boolean) => {
  game.scene.getScenes(true).forEach(scene => {
    if (scene.input?.keyboard) scene.input.keyboard.enabled = enabled;
  });
};

// Expose music mute/unmute for the radio button
(window as any).__setGameMusic = (enabled: boolean) => {
  game.scene.getScenes(true).forEach(scene => {
    (scene.sound as any).getAll().forEach((s: any) => {
      (s as any).setVolume(enabled ? 0.35 : 0);
    });
  });
};

// ── Auth / Scoreboard (Supabase) ────────────────────────────────────────────
(window as any).__loginWith = async (provider: 'google') => {
  if (!supabaseConfigured) {
    (window as any).__onLoginError?.('Supabase nog niet geconfigureerd (env vars ontbreken).');
    return;
  }
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: { redirectTo: window.location.origin },
    });
    if (error) (window as any).__onLoginError?.(error.message);
  } catch (e: any) {
    (window as any).__onLoginError?.(e?.message ?? 'Login mislukt.');
  }
};

(window as any).__logout = async () => {
  await playtimeTracker.sync();
  await supabase.auth.signOut();
  (window as any).__onAuthChange?.(null);
};

(window as any).__getScoreboard = () => PlaytimeTracker.getScoreboard();
(window as any).__debugPlaytime = () => playtimeTracker.debug();

(window as any).__logFeedback = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return;
  await supabase.rpc('increment_feedback_count', { uid: user.id });
};

/** Returns current email_optin value for the logged-in player, or undefined if not logged in. */
(window as any).__getSubscriptionStatus = async (): Promise<boolean | null | undefined> => {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return undefined;
  const { data } = await supabase
    .from('players')
    .select('email_optin')
    .eq('user_id', user.id)
    .single();
  return data?.email_optin ?? null; // null = not yet asked
};

// ── Guestbook ────────────────────────────────────────────────────────────────
(window as any).__fetchGuestbook = async (): Promise<Array<{ display_name: string; message: string }>> => {
  const { data, error } = await supabase
    .from('guestbook')
    .select('display_name, message')
    .order('created_at', { ascending: false })
    .limit(20);
  if (error) { console.warn('[guestbook] fetch error', error.message); return []; }
  return data ?? [];
};

(window as any).__postGuestbook = async (message: string): Promise<{ error?: string }> => {
  const { data: { user } } = await supabase.auth.getUser();
  const display_name = user?.user_metadata?.full_name ?? user?.email?.split('@')[0] ?? 'Anoniem';
  const { error } = await supabase.from('guestbook').insert({ message, display_name });
  if (error) return { error: error.message };
  return {};
};

/** Save the player's subscription opt-in choice (true = subscribed, false = declined). */
(window as any).__saveSubscription = async (optin: boolean): Promise<void> => {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return;
  await supabase.from('players').upsert(
    { user_id: user.id, email_optin: optin, updated_at: new Date().toISOString() },
    { onConflict: 'user_id' },
  );
};

// On page load: restore session and notify UI
supabase.auth.getSession().then(async ({ data: { session } }) => {
  if (session) {
    await playtimeTracker.loadFromDB();
    (window as any).__onAuthChange?.(session.user);
  }
});

// Keep UI in sync with auth state changes
supabase.auth.onAuthStateChange(async (_event, session) => {
  if (session) {
    await playtimeTracker.loadFromDB();
  }
  (window as any).__onAuthChange?.(session?.user ?? null);
});

// Sync playtime when tab closes so no movement time is lost
window.addEventListener('beforeunload', () => {
  playtimeTracker.sync();
});
