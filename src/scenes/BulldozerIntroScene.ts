import Phaser from 'phaser';
import { SCENE, GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';

/**
 * BulldozerIntroScene — cinematic cutscene before the Bureau-Buldozer battle.
 *
 * Sequence:
 *   1. Dusty-orange Borgerhout street fades in
 *   2. Giant bulldozer rolls in from the right with rumble + smoke
 *   3. Bureaucrat hops out with a speech bubble
 *   4. Player presses any key / tap → fades to BattleScene
 */
export class BulldozerIntroScene extends Phaser.Scene {
  private smokeTimer: Phaser.Time.TimerEvent | null = null;
  private fightStarted = false;

  constructor() {
    super({ key: SCENE.BULLDOZER_INTRO });
  }

  create(): void {
    this.fightStarted = false;
    this.cameras.main.fadeIn(500, 0, 0, 0);
    this.buildBackground();
    this.runSequence();
  }

  shutdown(): void {
    this.smokeTimer?.destroy();
  }

  // ── Background ────────────────────────────────────────────────────────────

  private buildBackground(): void {
    const W  = GAME_WIDTH;
    const H  = GAME_HEIGHT;
    const gY = Math.floor(H * 0.55);  // ground line
    const g  = this.add.graphics();

    // Dusty construction sky — gradient orange
    g.fillStyle(0xE8935A);
    g.fillRect(0, 0, W, gY);
    g.fillStyle(0xC96020, 0.5);
    g.fillRect(0, gY - 40, W, 40);

    // Building silhouettes
    g.fillStyle(0x1A0E06);
    const buildings = [
      [0,   40, 80], [45,  55, 65], [105, 35, 90],
      [145, 60, 70], [210, 45, 85], [260, 70, 60],
      [335, 50, 75], [390, 55, 80], [448, 32, 65],
    ] as [number, number, number][];
    for (const [bx, bw, bh] of buildings) {
      g.fillRect(bx, gY - bh, bw, bh);
      // Lit windows
      for (let wy = gY - bh + 6; wy < gY - 6; wy += 12) {
        for (let wx = bx + 4; wx < bx + bw - 4; wx += 9) {
          if (Math.random() > 0.45) {
            g.fillStyle(0xFFD060, 0.65);
            g.fillRect(wx, wy, 4, 4);
            g.fillStyle(0x1A0E06);
          }
        }
      }
    }

    // Asphalt
    g.fillStyle(0x484440);
    g.fillRect(0, gY, W, H - gY);

    // Sidewalk
    g.fillStyle(0xB4AE9E);
    g.fillRect(0, gY - 6, W, 8);

    // Road dashes
    g.fillStyle(0xF0EAD6, 0.25);
    for (let rx = 0; rx < W; rx += 38) {
      g.fillRect(rx, Math.floor(H * 0.72), 22, 2);
    }

    // Striped construction barriers along sidewalk
    const bTop = gY - 4;
    for (let bi = 0; bi < 7; bi++) {
      const sx = 10 + bi * 28;
      for (let s = 0; s < 4; s++) {
        g.fillStyle(s % 2 === 0 ? 0xE63946 : 0xF0EAD6);
        g.fillRect(sx + s * 6, bTop, 6, 9);
      }
      g.fillStyle(0x888888);
      g.fillRect(sx + 11, bTop + 9, 2, 7);
    }

    // Dust clouds in sky (semi-transparent circles)
    g.fillStyle(0xC07030, 0.3);
    for (const [cx, cy, cr] of [[80, 30, 20], [200, 18, 28], [350, 25, 18]] as [number, number, number][]) {
      g.fillCircle(cx, cy, cr);
    }
  }

  // ── Bulldozer (drawn as pixel-art geometry in a Container) ────────────────

  private buildBulldozer(): Phaser.GameObjects.Container {
    const H  = GAME_HEIGHT;
    const gY = Math.floor(H * 0.55);
    const g  = this.add.graphics();

    // All coords relative to container origin (0, 0) = bottom-right of body
    // Machine extends left (negative x) and upward (negative y)

    // ── Tracks ────────────────────────────────────────────────────────────
    g.fillStyle(0x222222);
    g.fillRoundedRect(-138, -18, 138, 18, 3);
    g.fillStyle(0x3A3A3A);
    g.fillRoundedRect(-134, -15, 130, 12, 2);
    // Tread links
    g.fillStyle(0x555555);
    for (let tx = -130; tx < -4; tx += 12) {
      g.fillRect(tx, -15, 2, 12);
    }
    // Sprocket wheels
    for (const wx of [-128, -88, -48, -10]) {
      g.fillStyle(0x4A4A4A);
      g.fillRect(wx - 7, -18, 14, 12);
      g.fillStyle(0x2A2A2A);
      g.fillRect(wx - 4, -16, 8, 8);
    }

    // ── Hull / main body ──────────────────────────────────────────────────
    // Shadow
    g.fillStyle(0x9A7010);
    g.fillRect(-136, -66, 136, 48);
    // Main yellow
    g.fillStyle(0xFFB800);
    g.fillRect(-134, -68, 132, 50);
    // Ribbing panels
    g.fillStyle(0xE0A000);
    for (let rx = -120; rx < -4; rx += 16) {
      g.fillRect(rx, -68, 3, 50);
    }
    // Scrape / wear mark
    g.fillStyle(0xCC9000);
    g.fillRect(-134, -44, 132, 3);
    g.fillStyle(0xFFCC40);
    g.fillRect(-134, -68, 132, 4); // top highlight

    // ── Cab ───────────────────────────────────────────────────────────────
    // Outer shell
    g.fillStyle(0xAA7800);
    g.fillRect(-44, -104, 44, 38);
    // Yellow body
    g.fillStyle(0xFFB800);
    g.fillRect(-42, -102, 40, 36);
    // Windshield (faces left)
    g.fillStyle(0x5AACE0);
    g.fillRect(-40, -100, 20, 26);
    // Window frame
    g.fillStyle(0x886600);
    g.fillRect(-40, -100, 20, 2);   // top
    g.fillRect(-40, -76, 20, 2);    // bottom
    g.fillRect(-40, -100, 2, 28);   // left
    g.fillRect(-22, -100, 2, 28);   // right
    g.fillRect(-31, -100, 2, 28);   // center divider
    // Rear vent slats
    g.fillStyle(0xAA8800);
    for (let vy = -96; vy > -76; vy -= 7) {
      g.fillRect(-18, vy, 14, 4);
    }
    // Cab top lip
    g.fillStyle(0xCC9A00);
    g.fillRect(-44, -106, 44, 4);

    // ── Exhaust pipe ──────────────────────────────────────────────────────
    g.fillStyle(0x555555);
    g.fillRect(-10, -122, 7, 20);
    // Pipe cap
    g.fillStyle(0x333333);
    g.fillRect(-12, -124, 11, 4);
    g.fillStyle(0x666666);
    g.fillRect(-11, -123, 9, 2);

    // ── Hydraulic arms (connecting blade to hull) ──────────────────────────
    g.fillStyle(0xAAAAAA);
    g.fillRect(-148, -82, 16, 7);   // upper arm
    g.fillRect(-148, -56, 16, 7);   // lower arm
    g.fillStyle(0x888888);
    g.fillRect(-146, -82, 5, 36);   // vertical strut

    // ── Blade ─────────────────────────────────────────────────────────────
    // Blade back
    g.fillStyle(0x666666);
    g.fillRect(-164, -90, 18, 80);
    // Blade face
    g.fillStyle(0x888888);
    g.fillRect(-168, -88, 10, 76);
    // Cutting edge highlight
    g.fillStyle(0xBBBBBB);
    g.fillRect(-170, -86, 4, 72);
    // Blade shadow side
    g.fillStyle(0x444444);
    g.fillRect(-150, -88, 4, 76);
    // Blade bottom curl
    g.fillStyle(0x999999);
    g.fillRect(-170, -14, 22, 5);
    // Dirt pile at blade
    g.fillStyle(0x7A5030);
    g.fillRect(-170, -8, 20, 8);
    g.fillStyle(0x5A3818);
    g.fillRect(-166, -4, 14, 4);

    // ── Headlight ─────────────────────────────────────────────────────────
    g.fillStyle(0xFFFF88);
    g.fillRect(-148, -82, 10, 6);
    // Light beam (faint, left-pointing)
    for (let li = 1; li <= 14; li++) {
      g.fillStyle(0xFFFF44, Math.max(0, 0.08 - li * 0.005));
      g.fillRect(-148 - li * 3, -82 + li, 6, 5 - Math.min(4, li));
    }

    // Container starts off-screen right; x=0 is at right edge of body
    const container = this.add.container(GAME_WIDTH + 180, gY, [g]);
    return container;
  }

  // ── Exhaust smoke ─────────────────────────────────────────────────────────

  private startSmoke(container: Phaser.GameObjects.Container): void {
    // Exhaust pipe is at local offset (-8, -118) from container origin
    this.smokeTimer = this.time.addEvent({
      delay: 200,
      repeat: -1,
      callback: () => {
        const wx = container.x - 8  + Phaser.Math.Between(-2, 2);
        const wy = container.y - 118;
        const r  = Phaser.Math.Between(4, 9);
        const p  = this.add.graphics();
        p.fillStyle(0x888888, 0.55);
        p.fillCircle(0, 0, r);
        p.x = wx;
        p.y = wy;
        this.tweens.add({
          targets:  p,
          x:        wx + Phaser.Math.Between(-10, 10),
          y:        wy - Phaser.Math.Between(18, 34),
          alpha:    0,
          scaleX:   2.2,
          scaleY:   2.2,
          duration: 750,
          onComplete: () => p.destroy(),
        });
      },
    });
  }

  // ── Cutscene sequence ─────────────────────────────────────────────────────

  private runSequence(): void {
    const W  = GAME_WIDTH;
    const H  = GAME_HEIGHT;
    const gY = Math.floor(H * 0.55);

    const bDozer = this.buildBulldozer();
    this.startSmoke(bDozer);

    // Engine rumble text (top of screen)
    const rumble = this.add.text(W / 2, 10,
      'RRRRRMMMMM...', {
        fontFamily: '"Press Start 2P"',
        fontSize: '4px',
        color: '#888888',
      }).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: rumble, alpha: 0.6, duration: 400,
      delay: 300, yoyo: true, repeat: 2,
    });

    // Slide bulldozer in from right
    this.time.delayedCall(350, () => {
      this.tweens.add({
        targets:  bDozer,
        x:        Math.floor(W * 0.61),
        duration: 1600,
        ease:     'Power2.easeOut',
        onUpdate: () => {
          // Subtle camera nudge while driving in
          this.cameras.main.setRotation(Math.sin(this.time.now * 0.08) * 0.002);
        },
        onComplete: () => {
          this.cameras.main.setRotation(0);
          // Heavy impact shake
          this.cameras.main.shake(700, 0.009);

          // "VASTGOED NV" logo stamped onto bulldozer body
          this.add.text(
            bDozer.x - 110, gY - 60,
            'VASTGOED\n    NV',
            { fontFamily: '"Press Start 2P"', fontSize: '4px', color: '#FFB800', lineSpacing: 3 },
          );

          // Bring in bureaucrat after shake settles
          this.time.delayedCall(550, () => this.showBureaucrat(bDozer, gY));
        },
      });
    });
  }

  private showBureaucrat(bDozer: Phaser.GameObjects.Container, gY: number): void {

    // Bureau-Buldozer sprite (frame 3 of battle_sprites)
    const b = this.add.image(bDozer.x - 98, gY + 2, 'battle_sprites', 3)
      .setDisplaySize(34, 46)
      .setAlpha(0)
      .setFlipX(false);

    // Hop down from bulldozer
    b.y = gY - 38;
    this.tweens.add({
      targets: b,
      y:       gY - 20,
      alpha:   1,
      duration: 280,
      ease:    'Bounce.easeOut',
    });

    // Speech bubble (appears 300ms after bureaucrat)
    this.time.delayedCall(320, () => {
      const bx = 8;
      const by = 10;
      const bw = 220;
      const bh = 60;

      const bubble = this.add.graphics();
      // Outer border
      bubble.fillStyle(0x333333);
      bubble.fillRoundedRect(bx, by, bw, bh, 5);
      // White fill
      bubble.fillStyle(0xF0EAD6);
      bubble.fillRoundedRect(bx + 2, by + 2, bw - 4, bh - 4, 4);
      // Pointer to bureaucrat (triangle bottom-right)
      bubble.fillStyle(0xF0EAD6);
      bubble.fillTriangle(
        bx + bw - 50, by + bh,
        bx + bw - 30, by + bh,
        bx + bw - 20, by + bh + 10,
      );
      bubble.fillStyle(0x333333);
      bubble.fillTriangle(
        bx + bw - 52, by + bh - 1,
        bx + bw - 28, by + bh - 1,
        bx + bw - 18, by + bh + 12,
      );
      bubble.fillStyle(0xF0EAD6);
      bubble.fillTriangle(
        bx + bw - 50, by + bh,
        bx + bw - 30, by + bh,
        bx + bw - 20, by + bh + 10,
      );

      bubble.setAlpha(0);
      this.tweens.add({ targets: bubble, alpha: 1, duration: 180 });

      const txt = this.add.text(bx + 8, by + 8,
        ['HALT!', 'ONTEIGENING IN UITVOERING.', 'ARTIKEL 4.2.9 BOUWBESLUIT.', 'U STAAT IN DE WEG.'],
        {
          fontFamily: '"Press Start 2P"',
          fontSize: '5px',
          color: '#1A0E06',
          lineSpacing: 4,
        }).setAlpha(0);
      this.tweens.add({ targets: txt, alpha: 1, duration: 180, delay: 100 });

      this.time.delayedCall(1400, () => this.showFightPrompt());
    });
  }

  private showFightPrompt(): void {
    const W = GAME_WIDTH;
    const H = GAME_HEIGHT;

    const prompt = this.add.text(W / 2, H * 0.88,
      '▶  VECHT  —  SPATIEBALK / KLIK',
      { fontFamily: '"Press Start 2P"', fontSize: '5px', color: '#FFD700' },
    ).setOrigin(0.5).setAlpha(0);

    this.tweens.add({
      targets: prompt,
      alpha:   1,
      duration: 350,
      yoyo:    true,
      repeat:  -1,
      repeatDelay: 300,
    });

    const startBattle = () => {
      if (this.fightStarted) return;
      this.fightStarted = true;
      this.smokeTimer?.destroy();
      this.cameras.main.fadeOut(400, 0, 0, 0);
      this.cameras.main.once('camerafadeoutcomplete', () => {
        this.scene.stop(SCENE.BULLDOZER_INTRO);
        this.scene.launch(SCENE.BATTLE, { enemyId: 'bulldozer_bureau' });
      });
    };

    this.input.keyboard?.once('keydown', startBattle);
    this.input.once('pointerdown', startBattle);
  }
}
