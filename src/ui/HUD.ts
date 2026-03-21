import Phaser from 'phaser';
import { PlayerState, stateManager } from '@core/StateManager';
import { GAME_WIDTH, GAME_HEIGHT }   from '@core/GameConfig';

/**
 * HUD — top-left overlay showing HP bar, coins, and level.
 * Fixed to the camera (setScrollFactor(0)).
 */
export class HUD {
  private scene:     Phaser.Scene;
  private hpBar!:    Phaser.GameObjects.Rectangle;
  private coinsText!:Phaser.GameObjects.Text;
  private levelText!:Phaser.GameObjects.Text;

  private readonly BAR_W = 52;
  private readonly BAR_H = 4;
  private readonly PAD   = 4;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.build();
  }

  private build(): void {
    const p   = this.PAD;
    const bw  = this.BAR_W;
    const bh  = this.BAR_H;

    // Semi-transparent panel
    this.scene.add.rectangle(p, p, bw + p * 2, 28, 0x0A0A12, 0.75)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(100);

    // HP label
    this.scene.add.text(p + 2, p + 2, 'HP', {
      fontFamily: '"Press Start 2P"',
      fontSize:   '4px',
      color:      '#E63946',
    }).setScrollFactor(0).setDepth(101);

    // HP bar background
    this.scene.add.rectangle(p + 12, p + 4, bw, bh, 0x333333)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(101);

    // HP bar fill
    this.hpBar = this.scene.add.rectangle(p + 12, p + 4, bw, bh, 0x52C41A)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(102);

    // Coins
    this.coinsText = this.scene.add.text(p + 2, p + 12, '¢0', {
      fontFamily: '"Press Start 2P"',
      fontSize:   '4px',
      color:      '#FFD700',
    }).setScrollFactor(0).setDepth(101);

    // Level
    this.levelText = this.scene.add.text(p + 2, p + 20, 'Lv.1', {
      fontFamily: '"Press Start 2P"',
      fontSize:   '4px',
      color:      '#A8D8EA',
    }).setScrollFactor(0).setDepth(101);

    // Minimap stub (top-right)
    this.scene.add.rectangle(GAME_WIDTH - p - 32, p, 32, 24, 0x0A0A12, 0.6)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(100);

    this.scene.add.text(GAME_WIDTH - p - 30, p + 8, 'KAART', {
      fontFamily: '"Press Start 2P"',
      fontSize:   '3px',
      color:      '#555555',
    }).setScrollFactor(0).setDepth(101);

    // Save button — bottom-right corner
    const bx = GAME_WIDTH - p - 28;
    const by = GAME_HEIGHT - p - 14;
    const saveBg = this.scene.add.rectangle(bx, by, 30, 12, 0x1A3A1A, 0.85)
      .setOrigin(0, 0)
      .setScrollFactor(0)
      .setDepth(100)
      .setInteractive({ useHandCursor: true });
    const saveLabel = this.scene.add.text(bx + 15, by + 6, 'OPSLAAN', {
      fontFamily: '"Press Start 2P"',
      fontSize:   '3px',
      color:      '#7FDD7F',
    }).setOrigin(0.5, 0.5).setScrollFactor(0).setDepth(101);

    saveBg.on('pointerover',  () => { saveBg.setFillStyle(0x2A5A2A, 0.95); });
    saveBg.on('pointerout',   () => { saveBg.setFillStyle(0x1A3A1A, 0.85); });
    saveBg.on('pointerdown',  () => {
      stateManager.save();
      saveLabel.setText('OPGESLAGEN!');
      this.scene.time.delayedCall(1200, () => saveLabel.setText('OPSLAAN'));
    });

    // Black border frame around the entire game viewport
    const border = this.scene.add.graphics();
    border.lineStyle(16, 0x000000, 1);
    border.strokeRect(0, 0, GAME_WIDTH, GAME_HEIGHT);
    border.setScrollFactor(0).setDepth(300);

  }

  update(player: PlayerState): void {
    this.hpBar.width   = this.BAR_W * (player.hp / player.maxHp);
    this.coinsText.setText(`¢${player.coins}`);
    this.levelText.setText(`Lv.${player.level}`);

    // Bar colour: green → yellow → red
    const pct = player.hp / player.maxHp;
    if (pct > 0.5)      this.hpBar.setFillStyle(0x52C41A);
    else if (pct > 0.2) this.hpBar.setFillStyle(0xFFD700);
    else                this.hpBar.setFillStyle(0xE63946);
  }
}
