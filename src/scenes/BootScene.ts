import Phaser from 'phaser';
import { SCENE } from '@core/GameConfig';

/**
 * BootScene — loads all assets then transitions to MainMenu.
 * Renders a simple progress bar styled in the game palette.
 */
export class BootScene extends Phaser.Scene {
  constructor() {
    super({ key: SCENE.BOOT });
  }

  preload(): void {
    this.createProgressBar();
    this.loadAssets();
  }

  create(): void {
    this.scene.start(SCENE.MAIN_MENU);
  }

  // ── private ─────────────────────────────────────────────────────────────

  private createProgressBar(): void {
    const { width, height } = this.scale;
    const cx = width / 2;
    const cy = height / 2;

    // Background
    this.add.rectangle(cx, cy - 20, 200, 4, 0x2a2a2a);
    const bar = this.add.rectangle(cx - 100, cy - 20, 0, 4, 0xFFD700).setOrigin(0, 0.5);

    const label = this.add.text(cx, cy - 8, 'LADEN…', {
      fontFamily: '"Press Start 2P"',
      fontSize: '6px',
      color: '#F0EAD6',
    }).setOrigin(0.5);

    this.load.on('progress', (v: number) => {
      bar.width = 200 * v;
    });

    this.load.on('complete', () => {
      label.setText('KLAAR');
    });
  }

  private loadAssets(): void {
    // ── Player (5 frames: idle, pedalA, pedalB, back, front) ──────────────
    // PNG: 1600×320 px  (32 game-px × out_scale=10 = 320 px per frame)
    this.load.spritesheet('player',
      'assets/Sprites/characters/player/player_sheet.png',
      { frameWidth: 320, frameHeight: 320 });

    // ── NPCs — one spritesheet per character (3 frames each) ───────────────
    // PNG per NPC: 960×480 px  (32×48 game-px × out_scale=10)
    const npcNames = [
      'fatima', 'omar', 'baert', 'reza', 'el_osri',
      'yusuf',  'aziz', 'sofia', 'hamza', 'tine',
    ] as const;
    for (const name of npcNames) {
      this.load.spritesheet(
        `npc_${name}`,
        `assets/Sprites/characters/npcs/${name}/${name}_sheet.png`,
        { frameWidth: 640, frameHeight: 960 },
      );
    }

    // ── Buildings tileset (20 tiles, in house-number order) ────────────────
    // Tile: 48×112 game-px  →  384×896 PNG px  (scale=8)
    // Displayed in-game at 96×130 Phaser units (2× wide, 20% taller than game-px).
    // Order: indian_boutique(0) … aladdin(1) … charif(3) … hammam(8) …
    //        budgetmkt(11) … basic_fit(13) … newstar(14) … brick(16-18) … vacant(19)
    this.load.spritesheet('buildings',
      'assets/Sprites/buildings/building_tiles.png',
      { frameWidth: 384, frameHeight: 896 });

    // ── Bikes — 16 biker types, player-sized (facing right) ──────────────
    // Frame: 36×30 game-px × SCALE=6  →  216×180 px per frame
    // Sheet: 3456×180 px  (flip horizontally in-game for westbound)
    this.load.spritesheet('bikes',
      'assets/Sprites/bikes/bikes_sheet.png',
      { frameWidth: 216, frameHeight: 180 });

    // ── Tram — single Antwerp De Lijn tram (facing right) ─────────────────
    // PNG: 112×24 game-px × SCALE=4  →  448×96 px
    this.load.image('tram', 'assets/Sprites/tram/tram.png');

    // ── Electric step riders (4 variants: kids, moroccan_girl, fitness_boy, lovers) ──
    // Frame: 36×30 game-px × SCALE=6  →  216×180 px per frame
    // Sheet: 864×180 px  (flip horizontally for westbound)
    this.load.spritesheet('steps',
      'assets/Sprites/steps/steps_sheet.png',
      { frameWidth: 216, frameHeight: 180 });

    // ── Crowd pedestrians (20 variants × 3 frames, horizontal sheet) ───────
    // Frame: 12×28 game-px × SCALE=6  →  72×168 px per frame
    // Sheet: 4320×168 px  (60 frames total)
    this.load.spritesheet('crowd',
      'assets/Sprites/characters/crowd/crowd_sheet.png',
      { frameWidth: 72, frameHeight: 168 });

    // ── Vehicles (7 types, static, horizontal sheet) ───────────────────────
    // Frame: 64×28 game-px × SCALE=5  →  320×140 px per vehicle
    // Sheet: 2240×140 px  (7 frames: clio_blue…scooter)
    this.load.spritesheet('vehicles',
      'assets/Sprites/vehicles/vehicles_sheet.png',
      { frameWidth: 320, frameHeight: 140 });

    // ── Pigeons — 3 types × 4 animation frames (sit, wings-up, wings-level, wings-down)
    // Sheet: 384×32 px  (12 frames, frameWidth=32, frameHeight=32)
    this.load.spritesheet('pigeons',
      'assets/Sprites/birds/pigeons_sheet.png',
      { frameWidth: 32, frameHeight: 32 });

    // ── Street cats — 3 types × 5 walk frames
    // Sheet: 480×32 px  (15 frames, frameWidth=32, frameHeight=32)
    this.load.spritesheet('cats',
      'assets/Sprites/cats/cats_sheet.png',
      { frameWidth: 32, frameHeight: 32 });

    // ── Battle sprites (7 frames: player + 6 enemies, 48×64 game-px each) ──
    // Sheet: 336×64 game-px × out_scale=8 → 2688×512 px
    // Frames: 0=player, 1=straatvechter, 2=pickpocket, 3=bulldozer_bureau,
    //         4=speculant, 5=tram_geest, 6=vlok_geest
    this.load.spritesheet('battle_sprites',
      'assets/Sprites/battle/battle_sprites.png',
      { frameWidth: 384, frameHeight: 512 });

    // ── Item icons (13 icons × 16×16 px, horizontal strip) ───────────────
    // Order: fabric_bolt(0) delivery_package(1) flour(2) oud_string(3)
    //        tram_ticket(4) harira(5) baklava(6) samen_flyer(7) permit_doc(8)
    //        friet(9) reuzenpoort_key(10) mint_tea(11) smoske(12)
    this.load.spritesheet('items_sheet',
      'assets/Sprites/items/items_sheet.png',
      { frameWidth: 16, frameHeight: 16 });

    // ── NPC Portraits (2-frame: 0=neutral, 1=talking) ─────────────────
    // PNG per NPC: 256×128 px (2 × 64×64 game-px at scale=2)
    const portraitNames = [
      'fatima', 'omar', 'baert', 'reza', 'el_osri',
      'yusuf',  'aziz', 'sofia', 'hamza', 'tine',
    ] as const;
    for (const name of portraitNames) {
      this.load.spritesheet(
        `portrait_${name}`,
        `assets/Sprites/characters/npcs/portraits/${name}_portrait.png`,
        { frameWidth: 512, frameHeight: 512 },
      );
    }

    // ── Main menu background (AI-generated street art) ────────────────────
    this.load.image('menu_bg',
      'assets/Sprites/raw_assets/Gemini_Generated_Image_bwblrpbwblrpbwbl.png');

    // ── Tilemaps ──────────────────────────────────────────────────────────
    // this.load.tilemapTiledJSON('borgerhout_main', 'assets/maps/borgerhout_main.json');

    // ── Audio ─────────────────────────────────────────────────────────────
    this.load.audio('bgm_lofi',   'assets/audio/bgm/nastelbom-arabic-490152.mp3');
    this.load.audio('bgm_delivery', 'assets/audio/bgm/kissan4-pixel-paradise-358340.mp3');
    // this.load.audio('sfx_coin', ['assets/audio/sfx/coin_pickup.ogg']);
  }
}
