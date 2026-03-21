import Phaser from 'phaser';
import { GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';

/**
 * DialogueBox — camera-fixed dialogue panel at the bottom of the screen.
 *
 * Two modes:
 *   1. Text mode  — speaker name + body text with typewriter effect
 *   2. Choice mode — up to 4 labelled options, navigated with up/down, confirmed with action
 */
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

  private _visible    = false;
  private typeTimer:  Phaser.Time.TimerEvent | null = null;
  private _typeDone   = false;
  private _fullText   = '';

  private readonly BOX_H   = 90;
  private readonly PAD     = 6;
  private readonly BOX_Y   = GAME_HEIGHT - this.BOX_H - 2;
  private readonly MAX_CHOICES = 4;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.build();
  }

  // ── Build ──────────────────────────────────────────────────────────────────

  private build(): void {
    const y = this.BOX_Y;
    const w = GAME_WIDTH;

    this.border = this.scene.add.rectangle(1, y - 1, w - 2, this.BOX_H + 2, 0xFFD700)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(200);

    this.panel = this.scene.add.rectangle(2, y, w - 4, this.BOX_H, 0x0A0A12)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(201);

    this.speakerText = this.scene.add.text(this.PAD + 2, y + this.PAD, '', {
      fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#FFD700',
    }).setScrollFactor(0).setDepth(202).setResolution(2);

    this.bodyText = this.scene.add.text(this.PAD + 2, y + this.PAD + 18, '', {
      fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#F0EAD6',
      wordWrap:   { width: w - this.PAD * 4 },
    }).setScrollFactor(0).setDepth(202).setResolution(2);

    this.promptText = this.scene.add.text(w - this.PAD - 2, y + this.BOX_H - this.PAD - 2, '▼', {
      fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#FFD700',
    }).setOrigin(1, 1).setScrollFactor(0).setDepth(202).setResolution(2);

    // Pre-build choice text objects (hidden until needed)
    for (let i = 0; i < this.MAX_CHOICES; i++) {
      const ct = this.scene.add.text(
        this.PAD + 8, y + this.PAD + 18 + i * 20, '',
        { fontFamily: '"Press Start 2P"', fontSize: '12px', color: '#F0EAD6' },
      ).setScrollFactor(0).setDepth(202).setResolution(2).setVisible(false);
      this.choiceTexts.push(ct);
    }

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
    if (!v) this.choiceTexts.forEach(c => c.setVisible(false));
  }

  get visible(): boolean { return this._visible; }
}
