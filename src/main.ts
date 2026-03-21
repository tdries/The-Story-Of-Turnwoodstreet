import Phaser from 'phaser';
import { GAME_CONFIG } from '@core/GameConfig';
import { BootScene }      from '@scenes/BootScene';
import { MainMenuScene }  from '@scenes/MainMenuScene';
import { OverworldScene } from '@scenes/OverworldScene';
import { BattleScene }    from '@scenes/BattleScene';

const config: Phaser.Types.Core.GameConfig = {
  ...GAME_CONFIG,
  scene: [BootScene, MainMenuScene, OverworldScene, BattleScene],
};

new Phaser.Game(config);
