import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';

// Mirror of ItemBar constants — kept local so this scene has no external deps.
const ITEM_NAME_NL: Record<string, string> = {
  fabric_bolt:      'Stof',
  delivery_package: 'Pakjes',
  flour:            'Bloem',
  oud_string:       'Snaar',
  tram_ticket:      'Tram-ticket',
  harira:           'Harira',
  baklava:          'Baklava',
  samen_flyer:      'Flyer',
  permit_doc:       'Vergunning',
  friet:            'Friet',
  reuzenpoort_key:  'Sleutel',
  mint_tea:         'Muntthee',
  smoske:           'Smoske',
};

const ITEM_FRAME: Record<string, number> = {
  fabric_bolt:       0,
  delivery_package:  1,
  flour:             2,
  oud_string:        3,
  tram_ticket:       4,
  harira:            5,
  baklava:           6,
  samen_flyer:       7,
  permit_doc:        8,
  friet:             9,
  reuzenpoort_key:  10,
  mint_tea:         11,
  smoske:           12,
};

/**
 * ItemReceiveScene — Zelda-style item-get overlay.
 *
 * Launched on top of OverworldScene via scene.launch().
 * Shows the player holding the item above their head, then calls onDone()
 * which actually adds the item to inventory and resumes the dialogue.
 */
export class ItemReceiveScene extends Phaser.Scene {
  private onDone!:      () => void;
  private itemId!:      string;
  private speakerName!: string;
  private ready = false;

  constructor() { super({ key: 'ItemReceiveScene' }); }

  init(data: { itemId: string; speakerName: string; onDone: () => void }): void {
    this.itemId      = data.itemId;
    this.speakerName = data.speakerName;
    this.onDone      = data.onDone;
    this.ready       = false;
  }

  create(): void {
    const W  = GAME_WIDTH;
    const H  = GAME_HEIGHT;
    const cx = W / 2;
    const cy = H / 2;
    const gf = '"Press Start 2P"';

    // ── Dim overlay ───────────────────────────────────────────────────────────
    this.add.rectangle(0, 0, W, H, 0x000000, 0.72)
      .setOrigin(0, 0).setScrollFactor(0);

    // ── Panel ─────────────────────────────────────────────────────────────────
    const panH = 130;
    const panW = 170;
    this.add.rectangle(cx, cy, panW, panH, 0x0A0A12)
      .setStrokeStyle(2, 0xFFD700);

    // ── Headline ──────────────────────────────────────────────────────────────
    this.add.text(cx, cy - 57, 'JE HEBT ONTVANGEN!', {
      fontFamily: gf, fontSize: '4px', color: '#FFD700',
    }).setOrigin(0.5);

    const itemLabel = ITEM_NAME_NL[this.itemId] ?? this.itemId;
    this.add.text(cx, cy - 47, itemLabel.toUpperCase(), {
      fontFamily: gf, fontSize: '7px', color: '#F0EAD6',
    }).setOrigin(0.5);

    if (this.speakerName) {
      this.add.text(cx, cy + 57, `van ${this.speakerName}`, {
        fontFamily: gf, fontSize: '4px', color: 'rgba(240,234,214,0.5)',
      }).setOrigin(0.5);
    }

    // ── Player (battle sprite frame 0 = player standing, front-facing) ────────
    // battle_sprites frames are 384×512 px; displayed at 48×64 game-px
    const player = this.add.image(cx, cy + 62, 'battle_sprites', 0)
      .setDisplaySize(48, 64)
      .setOrigin(0.5, 1);
    player.y += 40; // start below panel; tween up

    // ── Item (items_sheet, 16×16 px per frame; display at 28×28) ─────────────
    const frame = ITEM_FRAME[this.itemId] ?? 0;
    const item = this.add.image(cx, cy - 10, 'items_sheet', frame)
      .setDisplaySize(28, 28)
      .setAlpha(0)
      .setScale(0);

    // ── Continue prompt ───────────────────────────────────────────────────────
    const prompt = this.add.text(cx, cy + 58, '▶ VERDER', {
      fontFamily: gf, fontSize: '4px', color: '#FFD700',
    }).setOrigin(0.5).setAlpha(0);

    // ── Tweens ────────────────────────────────────────────────────────────────
    // Player slides up
    this.tweens.add({
      targets: player, y: cy + 32, duration: 280, ease: 'Back.Out',
    });

    // Item pops in from above, bounces to rest above player's head
    this.tweens.add({
      targets: item,
      y:     { from: cy - 50, to: cy - 16 },
      scale: { from: 0, to: 1.5 },
      alpha: 1,
      delay:    180,
      duration: 380,
      ease: 'Back.Out',
      onComplete: () => {
        // Float loop
        this.tweens.add({
          targets: item, y: cy - 19, duration: 700,
          ease: 'Sine.easeInOut', yoyo: true, repeat: -1,
        });
        // Fade in prompt
        this.tweens.add({ targets: prompt, alpha: 1, duration: 300 });
        this.time.delayedCall(50, () => { this.ready = true; });
      },
    });

    // Gold sparkles burst around item
    this.time.delayedCall(300, () => this._sparkles(cx, cy - 16));

    // ── Input ─────────────────────────────────────────────────────────────────
    this.input.keyboard?.on('keydown', () => { if (this.ready) this._finish(); });
    this.input.on('pointerdown',        () => { if (this.ready) this._finish(); });
  }

  private _sparkles(cx: number, cy: number): void {
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2;
      const r = 18;
      const dot = this.add.circle(
        cx + Math.cos(angle) * r,
        cy + Math.sin(angle) * r,
        1.5, 0xFFD700,
      );
      this.tweens.add({
        targets: dot,
        x: dot.x + Math.cos(angle) * 12,
        y: dot.y + Math.sin(angle) * 12,
        alpha: 0, scale: 0,
        duration: 450, delay: i * 25, ease: 'Quad.Out',
        onComplete: () => dot.destroy(),
      });
    }
  }

  private _finish(): void {
    this.ready = false;
    this.cameras.main.flash(180, 255, 215, 0);
    this.time.delayedCall(180, () => {
      this.onDone();
      this.scene.stop();
    });
  }
}
