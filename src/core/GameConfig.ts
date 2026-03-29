import Phaser from 'phaser';

/** Logical game resolution — all coordinates work in these units. */
export const GAME_WIDTH  = 480;
export const GAME_HEIGHT = 270;

/** Pixel scale factor — each logical pixel renders at this size. */
export const PIXEL_SCALE = 3;

export const GAME_CONFIG: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width:  GAME_WIDTH,
  height: GAME_HEIGHT,
  zoom:   PIXEL_SCALE,
  parent: 'game-container',
  backgroundColor: '#0A0A12',
  pixelArt: true,
  antialias: false,
  roundPixels: true,
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 0 },
      debug:   false,
    },
  },
  scale: {
    mode:            Phaser.Scale.FIT,
    autoCenter:      Phaser.Scale.CENTER_BOTH,
    width:           GAME_WIDTH,
    height:          GAME_HEIGHT,
  },
};

/** Shared palette constants (mirrors palette.json colours). */
export const PALETTE = {
  SKY_DAWN:   0xF4A261,
  SKY_DAY:    0xA8D8EA,
  SKY_DUSK:   0xE76F51,
  SKY_NIGHT:  0x0A0A12,
  BRICK_LIT:  0xC1440E,
  BRICK_MID:  0x8B3103,
  BRICK_SHD:  0x5A1E00,
  BRICK_ACC:  0xE8896A,
  UI_BLACK:   0x0A0A12,
  UI_WHITE:   0xF0EAD6,
  UI_GOLD:    0xFFD700,
  UI_RED:     0xE63946,
} as const;

/** Scene keys — centralised to avoid string typos. */
export const SCENE = {
  BOOT:            'BootScene',
  MAIN_MENU:       'MainMenuScene',
  OVERWORLD:       'OverworldScene',
  BATTLE:          'BattleScene',
  ITEM_RECEIVE:    'ItemReceiveScene',
  BULLDOZER_INTRO: 'BulldozerIntroScene',
} as const;
