import Phaser from 'phaser';

/** Unified input abstraction — keyboard + gamepad. */
export class InputHandler {
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private wasd!: {
    up:    Phaser.Input.Keyboard.Key;
    down:  Phaser.Input.Keyboard.Key;
    left:  Phaser.Input.Keyboard.Key;
    right: Phaser.Input.Keyboard.Key;
  };
  private actionKey!:  Phaser.Input.Keyboard.Key;   // Z
  private enterKey!:   Phaser.Input.Keyboard.Key;   // Enter
  private cancelKey!: Phaser.Input.Keyboard.Key;   // X / Escape
  private menuKey!:   Phaser.Input.Keyboard.Key;   // Tab / I

  constructor(scene: Phaser.Scene) {
    if (!scene.input.keyboard) throw new Error('Keyboard plugin not available');
    const kb = scene.input.keyboard;

    this.cursors = kb.createCursorKeys();
    this.wasd = {
      up:    kb.addKey(Phaser.Input.Keyboard.KeyCodes.W),
      down:  kb.addKey(Phaser.Input.Keyboard.KeyCodes.S),
      left:  kb.addKey(Phaser.Input.Keyboard.KeyCodes.A),
      right: kb.addKey(Phaser.Input.Keyboard.KeyCodes.D),
    };
    this.actionKey = kb.addKey(Phaser.Input.Keyboard.KeyCodes.Z);
    this.enterKey  = kb.addKey(Phaser.Input.Keyboard.KeyCodes.ENTER);
    this.cancelKey = kb.addKey(Phaser.Input.Keyboard.KeyCodes.X);
    this.menuKey   = kb.addKey(Phaser.Input.Keyboard.KeyCodes.TAB);
  }

  get up(): boolean {
    return this.cursors.up.isDown || this.wasd.up.isDown;
  }
  get down(): boolean {
    return this.cursors.down.isDown || this.wasd.down.isDown;
  }
  get left(): boolean {
    return this.cursors.left.isDown || this.wasd.left.isDown;
  }
  get right(): boolean {
    return this.cursors.right.isDown || this.wasd.right.isDown;
  }

  /** Direction vector, normalised. */
  get dir(): { x: number; y: number } {
    let x = 0;
    let y = 0;
    if (this.left)  x -= 1;
    if (this.right) x += 1;
    if (this.up)    y -= 1;
    if (this.down)  y += 1;
    if (x !== 0 && y !== 0) {
      const inv = 1 / Math.SQRT2;
      x *= inv;
      y *= inv;
    }
    return { x, y };
  }

  /** True only on the frame the key was pressed. */
  get actionJustPressed(): boolean {
    return Phaser.Input.Keyboard.JustDown(this.actionKey) ||
           Phaser.Input.Keyboard.JustDown(this.cursors.space) ||
           Phaser.Input.Keyboard.JustDown(this.enterKey);
  }
  get cancelJustPressed(): boolean {
    return Phaser.Input.Keyboard.JustDown(this.cancelKey) ||
           Phaser.Input.Keyboard.JustDown(this.cursors.shift);
  }
  get menuJustPressed(): boolean {
    return Phaser.Input.Keyboard.JustDown(this.menuKey);
  }
  get upJustPressed(): boolean {
    return Phaser.Input.Keyboard.JustDown(this.cursors.up) ||
           Phaser.Input.Keyboard.JustDown(this.wasd.up);
  }
  get downJustPressed(): boolean {
    return Phaser.Input.Keyboard.JustDown(this.cursors.down) ||
           Phaser.Input.Keyboard.JustDown(this.wasd.down);
  }
}
