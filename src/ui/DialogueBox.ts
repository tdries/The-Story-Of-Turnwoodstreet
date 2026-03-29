import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';

/**
 * DialogueBox — camera-fixed dialogue panel at the bottom of the screen.
 *
 * Two modes:
 *   1. Text mode  — speaker name + body text with typewriter effect
 *   2. Choice mode — up to 4 labelled options, navigated with up/down, confirmed with action
 *
 * Portrait: when the active speaker has a matching portrait texture loaded, a
 * 64×64 inlay is shown in the top-right corner of the screen.  Frame 0 = neutral,
 * frame 1 = talking (mouth open).  The frame animates with the typewriter.
 */

// ── Speaker → portrait texture key ──────────────────────────────────────────
const SPEAKER_PORTRAIT: Record<string, string> = {
  'Fatima':            'portrait_fatima',
  'Omar':              'portrait_omar',
  'Mevrouw Baert':     'portrait_baert',
  'Reza':              'portrait_reza',
  'El Osri':           'portrait_el_osri',
  'Districtsvoorzitter': 'portrait_el_osri',
  'Yusuf':             'portrait_yusuf',
  'Aziz':              'portrait_aziz',
  'Sofia':             'portrait_sofia',
  'Hamza':             'portrait_hamza',
  'Tine':              'portrait_tine',
  // NPCs that share a base texture
  'Kevin':             'portrait_hamza',
  'Lotte':             'portrait_sofia',
  'Bram':              'portrait_omar',
  'Nathalie':          'portrait_tine',
  'Van den Berg':      'portrait_baert',
};

export class DialogueBox {
  private scene:        Phaser.Scene;
  private panel!:       Phaser.GameObjects.Rectangle;
  private border!:      Phaser.GameObjects.Rectangle;
  private speakerText!: Phaser.GameObjects.Text;
  private bodyText!:    Phaser.GameObjects.Text;
  private promptText!:  Phaser.GameObjects.Text;

  // Choice UI
  private choiceTexts:  Phaser.GameObjects.Text[] = [];
  private choiceCursor = 0;
  private _inChoiceMode = false;

  // Portrait UI (top-right corner)
  private portraitBorder!: Phaser.GameObjects.Rectangle;
  private portraitBg!:     Phaser.GameObjects.Rectangle;
  private portrait!:       Phaser.GameObjects.Sprite;

  private _visible    = false;
  private typeTimer:  Phaser.Time.TimerEvent | null = null;
  private _typeDone   = false;
  private _fullText   = '';

  private readonly BOX_H   = 90;
  private readonly PAD     = 6;
  private readonly BOX_Y   = GAME_HEIGHT - this.BOX_H - 2;
  private readonly MAX_CHOICES = 4;

  // Portrait constants
  private readonly PORT_SIZE = 32;   // display px in game coords (2× smaller)
  private readonly PORT_X    = GAME_WIDTH  - 4 - 32;   // left edge
  private readonly PORT_Y    = 4;                       // top edge

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.build();
  }

  // ── Build ──────────────────────────────────────────────────────────────────

  private build(): void {
    const y = this.BOX_Y;
    const w = GAME_WIDTH;

    this.border = this.scene.add.rectangle(1, y - 1, w - 2, this.BOX_H + 2, 0xFFD700)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(1000);

    this.panel = this.scene.add.rectangle(2, y, w - 4, this.BOX_H, 0x0A0A12)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(1001);

    this.speakerText = this.scene.add.text(this.PAD + 2, y + this.PAD, '', {
      fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#FFD700',
    }).setScrollFactor(0).setDepth(1002).setResolution(2);

    this.bodyText = this.scene.add.text(this.PAD + 2, y + this.PAD + 18, '', {
      fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#F0EAD6',
      wordWrap:   { width: w - this.PAD * 4 },
    }).setScrollFactor(0).setDepth(1002).setResolution(2);

    this.promptText = this.scene.add.text(w - this.PAD - 2, y + this.BOX_H - this.PAD - 2, '▼', {
      fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#FFD700',
    }).setOrigin(1, 1).setScrollFactor(0).setDepth(1002).setResolution(2);

    // Pre-build choice text objects (hidden until needed)
    for (let i = 0; i < this.MAX_CHOICES; i++) {
      const ct = this.scene.add.text(
        this.PAD + 8, y + this.PAD + 18 + i * 20, '',
        { fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#F0EAD6' },
      ).setScrollFactor(0).setDepth(1002).setResolution(2).setVisible(false);
      this.choiceTexts.push(ct);
    }

    // ── Portrait overlay (top-right) ───────────────────────────────────────
    const px = this.PORT_X;
    const py = this.PORT_Y;
    const ps = this.PORT_SIZE;

    // Gold border — 1px inset each side, matching the dialogue box border style
    this.portraitBorder = this.scene.add.rectangle(px - 1, py - 1, ps + 2, ps + 2, 0xFFD700)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(1003);

    // Dark background
    this.portraitBg = this.scene.add.rectangle(px, py, ps, ps, 0x0A0A12)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(1004);

    // Portrait sprite — start on a safe texture until a real one is set
    this.portrait = this.scene.add.sprite(px + ps / 2, py + ps / 2, '__DEFAULT')
      .setDisplaySize(ps, ps)
      .setScrollFactor(0)
      .setDepth(1005);

    this.setVisible(false);
  }

  // ── Text mode ──────────────────────────────────────────────────────────────

  show(speaker: string, text: string): void {
    this._inChoiceMode = false;
    this._typeDone     = false;
    this._fullText     = text;
    this.setVisible(true);
    this.choiceTexts.forEach(c => c.setVisible(false));
    this.speakerText.setText(speaker.toUpperCase());
    this.bodyText.setText('');
    this.promptText.setVisible(false);

    // Portrait: switch texture for current speaker
    this._showPortrait(speaker);

    if (this.typeTimer) { this.typeTimer.remove(); }
    let i = 0;
    this.typeTimer = this.scene.time.addEvent({
      delay: 28,
      repeat: text.length - 1,
      callback: () => {
        this.bodyText.setText(text.slice(0, ++i));
        if (i >= text.length) {
          this._typeDone = true;
          this.promptText.setVisible(true);
          this.portrait.setFrame(0);   // back to neutral when done typing
        }
      },
    });
  }

  /** Skip typewriter animation — reveal full text immediately. */
  skipType(): void {
    if (this.typeTimer && !this._typeDone) {
      this.typeTimer.remove();
      this.typeTimer = null;
      this.bodyText.setText(this._fullText);
      this._typeDone = true;
      this.promptText.setVisible(true);
      this.portrait.setFrame(0);
    }
  }

  get isTyping(): boolean { return !this._typeDone; }

  // ── Choice mode ────────────────────────────────────────────────────────────

  showChoices(labels: string[]): void {
    if (this.typeTimer) { this.typeTimer.remove(); this.typeTimer = null; }
    this._inChoiceMode = true;
    this._typeDone     = true;
    this.promptText.setVisible(false);
    this.bodyText.setVisible(false);
    this.portrait.setFrame(0);   // neutral while player picks

    const y   = this.BOX_Y;
    const cnt = Math.min(labels.length, this.MAX_CHOICES);
    this.choiceCursor = 0;

    for (let i = 0; i < this.MAX_CHOICES; i++) {
      const ct = this.choiceTexts[i];
      ct.setY(y + this.PAD + 18 + i * 20);
      if (i < cnt) {
        ct.setText((i === 0 ? '▶ ' : '  ') + labels[i]);
        ct.setColor('#F0EAD6');
        ct.setVisible(true);
      } else {
        ct.setVisible(false);
      }
    }
    this._refreshCursor();
  }

  moveCursor(delta: -1 | 1): void {
    if (!this._inChoiceMode) return;
    const visible = this.choiceTexts.filter(c => c.visible);
    this.choiceCursor = (this.choiceCursor + delta + visible.length) % visible.length;
    this._refreshCursor();
  }

  get selectedChoice(): number { return this.choiceCursor; }
  get inChoiceMode(): boolean  { return this._inChoiceMode; }

  private _refreshCursor(): void {
    const visible = this.choiceTexts.filter(c => c.visible);
    visible.forEach((ct, i) => {
      const raw = ct.text.replace(/^[▶\s]{2}/, '');
      ct.setText((i === this.choiceCursor ? '▶ ' : '  ') + raw);
      ct.setColor(i === this.choiceCursor ? '#FFD700' : '#F0EAD6');
    });
  }

  // ── Portrait helpers ───────────────────────────────────────────────────────

  private _showPortrait(speaker: string): void {
    const key = SPEAKER_PORTRAIT[speaker];
    if (key && this.scene.textures.exists(key)) {
      this.portrait.setTexture(key, 1).setDisplaySize(this.PORT_SIZE, this.PORT_SIZE);
      this.portraitBorder.setVisible(true);
      this.portraitBg.setVisible(true);
      this.portrait.setVisible(true);
    } else {
      this.portraitBorder.setVisible(false);
      this.portraitBg.setVisible(false);
      this.portrait.setVisible(false);
    }
  }

  // ── Lifecycle ──────────────────────────────────────────────────────────────

  hide(): void {
    if (this.typeTimer) { this.typeTimer.remove(); this.typeTimer = null; }
    this._inChoiceMode = false;
    this.bodyText.setVisible(true);
    this.setVisible(false);
  }

  private setVisible(v: boolean): void {
    this._visible = v;
    [this.border, this.panel, this.speakerText, this.bodyText, this.promptText]
      .forEach(o => o.setVisible(v));
    if (!v) {
      this.choiceTexts.forEach(c => c.setVisible(false));
      this.portraitBorder.setVisible(false);
      this.portraitBg.setVisible(false);
      this.portrait.setVisible(false);
    }
  }

  get visible(): boolean { return this._visible; }
}
