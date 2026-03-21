import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';
import { InputHandler }    from '@core/InputHandler';
import { InventorySystem } from '@systems/InventorySystem';
import { stateManager }    from '@core/StateManager';
import { localeManager }   from '@i18n/LocaleManager';

/**
 * InventoryMenu — full-screen overlay that pauses the overworld.
 * Shown when the player presses TAB. Items are used with Z, closed with X/TAB.
 */
export class InventoryMenu {
  private scene:    Phaser.Scene;
  private panel!:   Phaser.GameObjects.Rectangle;
  private title!:   Phaser.GameObjects.Text;
  private rows:     Phaser.GameObjects.Text[] = [];
  private cursor    = 0;
  private _visible  = false;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.build();
    this.setVisible(false);
  }

  private build(): void {
    const W = GAME_WIDTH;
    const H = GAME_HEIGHT;
    const p = 8;

    this.panel = this.scene.add.rectangle(W / 2, H / 2, W - p * 2, H - p * 2, 0x0A0A12, 0.95)
      .setStrokeStyle(1, 0xFFD700)
      .setScrollFactor(0)
      .setDepth(300);

    this.title = this.scene.add.text(W / 2, p + 6, localeManager.t('backpack'), {
      fontFamily: localeManager.gameFont,
      fontSize:   '7px',
      color:      '#FFD700',
    }).setOrigin(0.5, 0).setScrollFactor(0).setDepth(301);
  }

  open(): void {
    this.cursor  = 0;
    this._visible = true;
    this.setVisible(true);
    this.refresh();
  }

  close(): void {
    this._visible = false;
    this.setVisible(false);
    this.rows.forEach(r => r.destroy());
    this.rows = [];
  }

  update(input: InputHandler): void {
    if (!this._visible) return;

    const items = InventorySystem.playerItems();
    if (input.upJustPressed)   this.cursor = Phaser.Math.Wrap(this.cursor - 1, 0, Math.max(1, items.length));
    if (input.downJustPressed) this.cursor = Phaser.Math.Wrap(this.cursor + 1, 0, Math.max(1, items.length));

    if (input.actionJustPressed && items[this.cursor]) {
      const msg = InventorySystem.use(items[this.cursor].id);
      if (msg) this.showFeedback(msg);
      this.refresh();
    }

    if (input.cancelJustPressed || input.menuJustPressed) this.close();
  }

  get isOpen(): boolean { return this._visible; }

  private refresh(): void {
    this.rows.forEach(r => r.destroy());
    this.rows = [];

    const items = InventorySystem.playerItems();
    const p     = stateManager.get().player;
    const W     = GAME_WIDTH;

    // Coins
    this.scene.add.text(W - 14, 10, `¢${p.coins}`, {
      fontFamily: '"Press Start 2P"', fontSize: '5px', color: '#FFD700',
    }).setOrigin(1, 0).setScrollFactor(0).setDepth(301);

    if (items.length === 0) {
      const t = this.scene.add.text(W / 2, GAME_HEIGHT / 2, localeManager.t('empty'), {
        fontFamily: localeManager.gameFont, fontSize: '5px', color: '#555555',
      }).setOrigin(0.5).setScrollFactor(0).setDepth(301);
      this.rows.push(t);
      return;
    }

    items.forEach((item, i) => {
      const y    = 28 + i * 14;
      const col  = i === this.cursor ? '#FFD700' : '#F0EAD6';
      const prefix = i === this.cursor ? '▶ ' : '  ';
      const displayName = localeManager.itemName(item.id) ?? item.name;
      const t = this.scene.add.text(12, y, `${prefix}${displayName}`, {
        fontFamily: localeManager.gameFont, fontSize: '5px', color: col,
      }).setScrollFactor(0).setDepth(301);
      this.rows.push(t);
    });

    if (items[this.cursor]) {
      const displayDesc = localeManager.itemDescription(items[this.cursor].id) ?? items[this.cursor].description;
      const desc = this.scene.add.text(12, GAME_HEIGHT - 22, displayDesc, {
        fontFamily: localeManager.gameFont, fontSize: '4px', color: '#888888',
        wordWrap: { width: W - 24 },
      }).setScrollFactor(0).setDepth(301);
      this.rows.push(desc);
    }
  }

  private showFeedback(msg: string): void {
    const t = this.scene.add.text(GAME_WIDTH / 2, GAME_HEIGHT - 30, msg, {
      fontFamily: '"Press Start 2P"', fontSize: '5px', color: '#52C41A',
      stroke: '#0A0A12', strokeThickness: 2,
    }).setOrigin(0.5).setScrollFactor(0).setDepth(305);
    this.scene.time.delayedCall(1200, () => t.destroy());
  }

  private setVisible(v: boolean): void {
    this.panel.setVisible(v);
    this.title.setVisible(v);
  }
}
