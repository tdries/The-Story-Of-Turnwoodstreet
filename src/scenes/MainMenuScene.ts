import Phaser from 'phaser';
import { SCENE } from '@core/GameConfig';
import { stateManager }  from '@core/StateManager';
import { localeManager, LOCALES, LOCALE_LABELS } from '@i18n/LocaleManager';

/**
 * MainMenuScene — title screen with interactive cursor menu.
 * Shows DOORGAAN (if save exists) and NIEUW SPEL.
 * Arrow keys / W-S navigate; Z / Space / Enter selects.
 */
export class MainMenuScene extends Phaser.Scene {
  private cursor = 0;
  private menuItems: Array<{ label: string; action: () => void }> = [];
  private menuTexts: Phaser.GameObjects.Text[] = [];
  private blinkTimer = 0;
  private arrowText!: Phaser.GameObjects.Text;
  private _touchSeen = { up: false, down: false, action: false, enter: false };

  constructor() {
    super({ key: SCENE.MAIN_MENU });
  }

  create(): void {
    const { width, height } = this.scale;
    const cx = width / 2;

    // Build menu items based on whether a save exists
    if (stateManager.hasSave()) {
      this.menuItems = [
        { label: localeManager.t('continue_game'), action: () => this.continueGame() },
        { label: localeManager.t('new_game'),      action: () => this.newGame() },
      ];
    } else {
      this.menuItems = [
        { label: localeManager.t('new_game'), action: () => this.newGame() },
      ];
    }

    // ── Background ──────────────────────────────────────────────────────────
    this.add.image(cx, height / 2, 'menu_bg')
      .setDisplaySize(width, height)
      .setDepth(0);

    const overlay = this.add.graphics().setDepth(1);
    overlay.fillStyle(0x000000, 0.52);
    overlay.fillRect(0, 0, width, height);
    overlay.fillGradientStyle(0x000000, 0x000000, 0x000000, 0x000000, 0.3, 0.3, 0.0, 0.0);
    overlay.fillRect(0, 0, width, height / 2);
    overlay.fillGradientStyle(0x000000, 0x000000, 0x000000, 0x000000, 0.0, 0.0, 0.35, 0.35);
    overlay.fillRect(0, height / 2, width, height / 2);

    const D = 2;

    // ── Title ───────────────────────────────────────────────────────────────
    this.add.text(cx, 55, 'TURNHOUTSEBAAN', {
      fontFamily: '"Press Start 2P"',
      fontSize: '12px',
      color: '#FFD700',
      stroke: '#000000',
      strokeThickness: 5,
      shadow: { offsetX: 2, offsetY: 2, color: '#8B3103', fill: true },
    }).setOrigin(0.5).setDepth(D);

    this.add.text(cx, 76, 'RPG', {
      fontFamily: '"Press Start 2P"',
      fontSize: '18px',
      color: '#F0EAD6',
      stroke: '#000000',
      strokeThickness: 5,
    }).setOrigin(0.5).setDepth(D);

    this.add.text(cx, 103, 'Borgerhout · Antwerpen', {
      fontFamily: '"Press Start 2P"',
      fontSize: '5px',
      color: '#FF6633',
      stroke: '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5).setDepth(D);

    // Divider
    const divider = this.add.graphics().setDepth(D);
    divider.lineStyle(1, 0xFFD700, 0.5);
    divider.lineBetween(cx - 80, 116, cx + 80, 116);

    // ── Interactive menu ─────────────────────────────────────────────────────
    const menuStartY = this.menuItems.length === 1 ? 156 : 144;
    const menuSpacing = 18;

    this.menuTexts = this.menuItems.map(({ label }, i) => {
      return this.add.text(cx + 8, menuStartY + i * menuSpacing, label, {
        fontFamily: '"Press Start 2P"',
        fontSize: '7px',
        color: '#F0EAD6',
        stroke: '#000000',
        strokeThickness: 3,
      }).setOrigin(0.5).setDepth(D);
    });

    // Cursor arrow (blinking)
    this.arrowText = this.add.text(cx - 40, menuStartY, '▶', {
      fontFamily: '"Press Start 2P"',
      fontSize: '7px',
      color: '#FFD700',
      stroke: '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5).setDepth(D);

    this.updateCursor();

    // ── Version / credits ────────────────────────────────────────────────────
    this.add.text(width - 4, height - 4, 'v0.1.0', {
      fontFamily: '"Press Start 2P"',
      fontSize: '4px',
      color: '#888888',
    }).setOrigin(1, 1).setDepth(D);

    this.add.text(cx, height - 4, localeManager.t('game_footer'), {
      fontFamily: localeManager.gameFont,
      fontSize: '4px',
      color: '#888888',
    }).setOrigin(0.5, 1).setDepth(D);

    // ── Language selector (bottom-left) ──────────────────────────────────────
    const localeY = height - 4;
    const localeX = 6;
    LOCALES.forEach((loc, i) => {
      const active = loc === localeManager.locale;
      const btn = this.add.text(localeX + i * 22, localeY, LOCALE_LABELS[loc], {
        fontFamily: '"Press Start 2P"',
        fontSize: '4px',
        color: active ? '#FFD700' : '#555555',
      }).setOrigin(0, 1).setDepth(D).setInteractive({ useHandCursor: true });

      btn.on('pointerover',  () => { if (!active) btn.setColor('#AAAAAA'); });
      btn.on('pointerout',   () => { if (!active) btn.setColor('#555555'); });
      btn.on('pointerdown',  () => {
        if (loc === localeManager.locale) return;
        localeManager.setLocale(loc);
        // Reload page so all Phaser scenes and HTML are rebuilt with the new locale
        window.location.reload();
      });
    });

    // ── Input ────────────────────────────────────────────────────────────────
    const kb = this.input.keyboard!;

    kb.on('keydown-UP',    () => this.moveCursor(-1));
    kb.on('keydown-DOWN',  () => this.moveCursor(1));
    kb.on('keydown-W',     () => this.moveCursor(-1));
    kb.on('keydown-S',     () => this.moveCursor(1));
    kb.on('keydown-Z',     () => this.select());
    kb.on('keydown-SPACE', () => this.select());
    kb.on('keydown-ENTER', () => this.select());
  }

  update(_time: number, delta: number): void {
    this.blinkTimer += delta;
    if (this.blinkTimer > 500) {
      this.arrowText.setVisible(!this.arrowText.visible);
      this.blinkTimer = 0;
    }

    // Touch rising-edge detection
    const touch = (window as any).__touch;
    if (touch) {
      if (touch.up    && !this._touchSeen.up)     this.moveCursor(-1);
      if (touch.down  && !this._touchSeen.down)   this.moveCursor(1);
      if ((touch.action && !this._touchSeen.action) ||
          (touch.enter  && !this._touchSeen.enter))  this.select();
      this._touchSeen.up     = touch.up;
      this._touchSeen.down   = touch.down;
      this._touchSeen.action = touch.action;
      this._touchSeen.enter  = touch.enter;
    }
  }

  // ── private ─────────────────────────────────────────────────────────────

  private moveCursor(dir: -1 | 1): void {
    if (this.menuItems.length <= 1) return;
    this.cursor = (this.cursor + dir + this.menuItems.length) % this.menuItems.length;
    this.updateCursor();
    // Reset blink so arrow is visible immediately after move
    this.arrowText.setVisible(true);
    this.blinkTimer = 0;
  }

  private updateCursor(): void {
    const menuStartY = this.menuItems.length === 1 ? 156 : 144;
    const menuSpacing = 18;

    this.menuTexts.forEach((t, i) => {
      t.setColor(i === this.cursor ? '#FFD700' : '#F0EAD6');
    });

    this.arrowText.setY(menuStartY + this.cursor * menuSpacing);
  }

  private select(): void {
    this.menuItems[this.cursor].action();
  }

  private continueGame(): void {
    // State was already loaded from localStorage in the StateManager constructor
    this.cameras.main.fadeOut(400, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.start(SCENE.OVERWORLD);
    });
  }

  private newGame(): void {
    stateManager.reset();
    this.cameras.main.fadeOut(400, 0, 0, 0);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.start(SCENE.OVERWORLD);
    });
  }
}
