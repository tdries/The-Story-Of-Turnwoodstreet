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

(window as any).__logFeedback = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return;
  await supabase.rpc('increment_feedback_count', { uid: user.id });
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
