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

new Phaser.Game(config);

// Expose save for the mobile save button
(window as any).__saveGame = () => stateManager.save();
