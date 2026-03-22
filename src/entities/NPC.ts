import Phaser from 'phaser';

/**
 * NPC — a named character on the overworld.
 *
 * Movement: idles for 1.5–4.5 s, then walks to a nearby X position at a
 * gentle pace, then idles again.  Walk frames (1 & 2) are toggled at a
 * fixed step interval so the character visibly strides; direction is
 * communicated via setFlipX so both left and right look natural.
 */
export class NPC {
  readonly sprite:     Phaser.Physics.Arcade.Sprite;
  readonly id:         string;
  readonly dialogueId: string;

  private originX:   number;
  private targetX:   number;
  private isMoving   = false;
  private idleTimer  = 0;

  // Walk-animation state
  private stepFrame  = 0;          // toggles 0 / 1  → sprite frame 1 / 2
  private frameTimer = 0;
  private readonly STEP_MS  = 210; // ms per walk frame
  private readonly WALK_SPD = 18;  // px / s

  // Visibility helpers (name tag + arrow stored so setVisible() can toggle them)
  private nameTag!: Phaser.GameObjects.Text;
  private arrow!:   Phaser.GameObjects.Text;

  constructor(
    scene:      Phaser.Scene,
    x:          number,
    y:          number,
    texture:    string,
    _frame:     number,            // ignored — always starts idle (frame 0)
    id:         string,
    dialogueId: string,
    startVisible = true,
  ) {
    this.id         = id;
    this.dialogueId = dialogueId;
    this.originX    = x;
    this.targetX    = x;

    this.sprite = scene.physics.add.sprite(x, y, texture, 0);
    this.sprite.setOrigin(0.5, 1);
    this.sprite.setDepth(y);
    this.sprite.setImmovable(true);
    this.sprite.setDisplaySize(20, 30);
    this.sprite.setBodySize(10, 10);
    this.sprite.setOffset(5, 20);

    // Name tag (fixed at spawn position — fine for short wanders)
    this.nameTag = scene.add.text(x, y - 40, id.charAt(0).toUpperCase() + id.slice(1), {
      fontFamily: '"Press Start 2P"',
      fontSize:   '8px',
      color:      '#FFD700',
      stroke:     '#0A0A12',
      strokeThickness: 4,
    }).setOrigin(0.5).setDepth(y + 1);

    // Bouncing interaction arrow above name tag
    this.arrow = scene.add.text(x, y - 54, '▼', {
      fontFamily: '"Press Start 2P"',
      fontSize:   '5px',
      color:      '#FFD700',
      stroke:     '#0A0A12',
      strokeThickness: 2,
    }).setOrigin(0.5).setDepth(y + 2);
    scene.tweens.add({
      targets:  this.arrow,
      y:        y - 49,
      duration: 600,
      ease:     'Sine.easeInOut',
      yoyo:     true,
      repeat:   -1,
    });

    this.idleTimer = Phaser.Math.Between(500, 2500);

    if (!startVisible) this.setVisible(false);
  }

  /** Show or hide the NPC and disable/enable its physics body. */
  setVisible(visible: boolean): void {
    this.sprite.setVisible(visible);
    this.nameTag.setVisible(visible);
    this.arrow.setVisible(visible);
    const body = this.sprite.body as Phaser.Physics.Arcade.Body;
    if (body) body.enable = visible;
  }

  update(delta: number): void {
    const dt = delta / 1000;

    if (this.isMoving) {
      const dx = this.targetX - this.sprite.x;

      if (Math.abs(dx) < 0.8) {
        // Arrived — snap, idle
        this.sprite.setX(this.targetX);
        this.sprite.setFrame(0);
        this.isMoving  = false;
        this.idleTimer = Phaser.Math.Between(1500, 4500);
      } else {
        const dir = Math.sign(dx);
        this.sprite.x += dir * this.WALK_SPD * dt;
        this.sprite.setFlipX(dir < 0);

        // Cycle walk frames 1 ↔ 2.
        // When moving LEFT the frame order is reversed (2→1 instead of 1→2)
        // so the leading foot phases correctly after the sprite is flipped.
        this.frameTimer += delta;
        if (this.frameTimer >= this.STEP_MS) {
          this.frameTimer = 0;
          this.stepFrame  = 1 - this.stepFrame;
        }
        const walkFrame = dir > 0
          ? 1 + this.stepFrame    // right: 0→frame1, 1→frame2
          : 2 - this.stepFrame;   // left:  0→frame2, 1→frame1
        this.sprite.setFrame(walkFrame);
      }
    } else {
      // Idle — count down then pick a nearby target
      this.idleTimer -= delta;
      if (this.idleTimer <= 0) {
        const nudge    = Phaser.Math.Between(-22, 22);
        this.targetX   = Phaser.Math.Clamp(
          this.originX + nudge,
          this.originX - 22,
          this.originX + 22,
        );
        this.isMoving   = true;
        this.frameTimer = 0;
        // Start on the "forward foot landing" frame so the leading foot is
        // visually planted first — looks correct for both left and right dirs.
        this.stepFrame  = 1;
      }
    }

    this.sprite.setDepth(this.sprite.y);
  }
}
