import Phaser from 'phaser';
import { GAME_CONFIG } from '@core/GameConfig';
import { BootScene }      from '@scenes/BootScene';
import { MainMenuScene }  from '@scenes/MainMenuScene';
import { OverworldScene } from '@scenes/OverworldScene';
import { BattleScene }    from '@scenes/BattleScene';
import { stateManager }   from '@core/StateManager';

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
    scene.sound.getAll().forEach((s: Phaser.Sound.BaseSound) => {
      (s as any).setVolume(enabled ? 0.35 : 0);
    });
  });
};
