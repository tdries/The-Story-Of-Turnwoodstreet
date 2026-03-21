import Phaser from 'phaser';
import { InputHandler } from '@core/InputHandler';

/**
 * Player — young Moroccan boy on a city bicycle.
 *
 * Spritesheet: 'player' (player_sheet.png, 32×32 frames)
 *   Frame 0 — Idle (right-facing, neutral pedal)
 *   Frame 1 — Pedal A (right foot down)
 *   Frame 2 — Pedal B (left foot down)
 *   Frame 3 — Back view  (used when riding up the screen)
 *   Frame 4 — Front view (used when riding down the screen)
 *
 * Left-facing: frames 0–2 with flipX = true (no extra frames needed).
 */

const BIKE_SPEED = 120;   // pixels/s — faster than walking NPCs

export class Player {
  readonly sprite: Phaser.Physics.Arcade.Sprite;
  private facing: 'left' | 'right' | 'up' | 'down' = 'right';

  constructor(scene: Phaser.Scene, x: number, y: number) {
    this.sprite = scene.physics.add.sprite(x, y, 'player', 0);
    this.sprite.setOrigin(0.5, 1);
    this.sprite.setDepth(10);
    // PNG frames are 320×320 px; display at 32×32 Phaser units (out_scale=10)
    this.sprite.setDisplaySize(32, 32);

    // Collision body: narrow rectangle at wheel level (bottom third of frame)
    this.sprite.setBodySize(14, 8);
    this.sprite.setOffset(9, 22);

    this.registerAnims(scene);
    this.sprite.play('player_idle_right');
  }

  update(input: InputHandler, _delta: number): void {
    const { x, y } = input.dir;
    this.sprite.setVelocity(x * BIKE_SPEED, y * BIKE_SPEED);

    if (x > 0) {
      this.facing = 'right';
      this.sprite.setFlipX(false);
      this.sprite.play('player_ride', true);
    } else if (x < 0) {
      this.facing = 'left';
      this.sprite.setFlipX(true);
      this.sprite.play('player_ride', true);
    } else if (y < 0) {
      this.facing = 'up';
      this.sprite.setFlipX(false);
      this.sprite.play('player_back', true);
    } else if (y > 0) {
      this.facing = 'down';
      this.sprite.setFlipX(false);
      this.sprite.play('player_front', true);
    } else {
      // Idle — preserve last facing direction
      if (this.facing === 'left') {
        this.sprite.setFlipX(true);
      } else {
        this.sprite.setFlipX(false);
      }
      this.sprite.play('player_idle_right', true);
    }

    // Y-sort depth (painter's algorithm)
    this.sprite.setDepth(this.sprite.y);
  }

  private registerAnims(scene: Phaser.Scene): void {
    if (scene.anims.exists('player_idle_right')) return;

    // Riding (left/right) — alternates pedal frames
    scene.anims.create({
      key:       'player_ride',
      frames:    scene.anims.generateFrameNumbers('player', { frames: [1, 2] }),
      frameRate: 8,
      repeat:    -1,
    });

    // Idle (stopped)
    scene.anims.create({
      key:       'player_idle_right',
      frames:    scene.anims.generateFrameNumbers('player', { frames: [0] }),
      frameRate: 1,
      repeat:    0,
    });

    // Moving up the screen (back view)
    scene.anims.create({
      key:       'player_back',
      frames:    scene.anims.generateFrameNumbers('player', { frames: [3] }),
      frameRate: 1,
      repeat:    0,
    });

    // Moving down the screen (front view)
    scene.anims.create({
      key:       'player_front',
      frames:    scene.anims.generateFrameNumbers('player', { frames: [4] }),
      frameRate: 1,
      repeat:    0,
    });
  }
}
