import Phaser from 'phaser';
import { SCENE, GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';
import { InputHandler }   from '@core/InputHandler';
import { stateManager }   from '@core/StateManager';
import { Player }         from '@entities/Player';
import { NPC }            from '@entities/NPC';
import { HUD }            from '@ui/HUD';
import { ItemBar }        from '@ui/ItemBar';
import { DialogueBox }    from '@ui/DialogueBox';
import { DialogueSystem, DIALOGUES, DialogueConditions } from '@systems/DialogueSystem';
import { GateSystem, ZONE_STARTS } from '@systems/GateSystem';
import { getNavTarget }            from '@systems/GameMachine';
import { QuestSystem }    from '@systems/QuestSystem';
import { playtimeTracker } from '@core/PlaytimeTracker';
import { TimeManager }    from '@core/TimeManager';

/**
 * OverworldScene — the main exploration scene.
 *
 * World: Top-down oblique view of the Turnhoutsebaan, Borgerhout.
 * 5 zones gated by capabilities (see _AI_CONTEXT_/05_Gated_Progression.md).
 * Painter's algorithm: sky → buildings → props → Y-sorted entities → HUD.
 */
export class OverworldScene extends Phaser.Scene {
  private controls!:       InputHandler;
  private player!:         Player;
  private npcs:            NPC[]    = [];
  private crowdNPCs:       Phaser.Physics.Arcade.Sprite[] = [];
  private hud!:            HUD;
  private itemBar!:        ItemBar;
  private dialogueBox!:    DialogueBox;
  private dialogueSystem!: DialogueSystem;
  private navArrow!:       Phaser.GameObjects.Text;
  private _navBlink = 0;

  // Gate trigger zones (invisible physics zones)
  private gateTriggers: Array<{
    zone:  number;
    rect:  Phaser.GameObjects.Zone;
  }> = [];

  private lastPlayerX = 0;
  private locationTriggers: Array<
    | { type: 'dialogue'; x: number; width: number; dialogueId: string; onceFlag: string; requiredFlags?: Record<string, boolean> }
    | { type: 'battle';   x: number; width: number; enemyId: string;    onceFlag: string; requiredFlags?: Record<string, boolean> }
  > = [];
  private playtimeSyncTimer = 0;

  // ── Day/Night cycle ───────────────────────────────────────────────────────
  private _clock!:          TimeManager;
  private skyRect!:         Phaser.GameObjects.Rectangle;
  private sunGfx!:          Phaser.GameObjects.Graphics;
  private moonGfx!:         Phaser.GameObjects.Graphics;
  private starsGfx!:        Phaser.GameObjects.Graphics;
  private clouds:           Array<{ gfx: Phaser.GameObjects.Graphics; x: number; y: number; width: number; speed: number }> = [];
  private clockText!:       Phaser.GameObjects.Text;
  private crowdThresholds:  number[] = [];
  private vehicleThresholds: number[] = [];
  private nightProps:       Phaser.GameObjects.Text[] = [];
  private densityTimer = 0;

  private static readonly SKY_STOPS: Array<[number, number]> = [
    [ 0, 0x0D0D2B], [ 5, 0x0D0D2B], [ 6, 0x3D1A4A], [ 7, 0xE8936C],
    [ 8, 0xB8D0E8], [10, 0x78AFE1], [16, 0x78AFE1], [17, 0xF0C060],
    [18, 0xE87040], [19, 0x8A3060], [20, 0x3A1A50], [21, 0x120E2A],
    [24, 0x0D0D2B],
  ];

  // World dimensions (pixels)
  static readonly WORLD_W = GAME_WIDTH * 12;  // 5760 px (full Borgerhout→Wijnegem street)
  static readonly WORLD_H = GAME_HEIGHT;      // 270 px

  constructor() {
    super({ key: SCENE.OVERWORLD });
  }

  create(): void {
    this.controls = new InputHandler(this);

    this.buildWorld();
    this.spawnNamedNPCs();
    this.spawnCrowd();
    this.spawnVehicles();
    this.spawnTram();
    this.spawnBikers();
    this.spawnStepRiders();
    this.spawnPigeons();
    this.spawnCats();
    this.createPlayer();
    this.setupCamera();
    this.setupCollisions();
    this.setupZoneTriggers();
    this.setupLocationTriggers();
    this.createUI();
    this.initDayCycle();

    this.cameras.main.fadeIn(600, 0, 0, 0);
    this.syncMusic();

    // Auto-start Radio Minerva — user has already clicked Play so the browser
    // autoplay gesture requirement is satisfied.
    this.time.delayedCall(800, () => {
      (window as any).__startRadioMinerva?.();
    });
  }

  update(_time: number, delta: number): void {

    this.updateDayCycle(delta);

    // Block movement while dialogue is open
    if (this.dialogueSystem.isOpen) {
      this.dialogueSystem.update(this.controls);
      return;
    }

    this.player.update(this.controls, delta);

    // Track active playtime (only counts frames where player is moving)
    const isMoving = this.controls.left || this.controls.right
                  || this.controls.up   || this.controls.down;
    playtimeTracker.tick(delta, isMoving);
    this.playtimeSyncTimer += delta;
    if (this.playtimeSyncTimer >= 10_000) {
      this.playtimeSyncTimer = 0;
      playtimeTracker.sync();
    }

    this.npcs.forEach(npc => npc.update(delta));
    this.updateCrowd(delta);
    this.updateTram(delta);
    this.updateVehicles(delta);
    this.updateBikers(delta);
    this.updateStepRiders(delta);
    this.updatePigeons(delta);
    this.updateCats(delta);

    // ── Zone gate check ────────────────────────────────────────────────────
    const px = this.player.sprite.x;
    if (px > this.lastPlayerX) {
      const block = GateSystem.checkTransition(this.lastPlayerX, px);
      if (block) {
        this.player.sprite.setX(this.lastPlayerX);   // push back silently
      }
    }
    this.lastPlayerX = this.player.sprite.x;

    // ── Location triggers (one-shot walk-in events) ────────────────────────
    if (!this.dialogueSystem.isOpen) {
      const flags = stateManager.get().questFlags;
      for (const trigger of this.locationTriggers) {
        if (flags[trigger.onceFlag]) continue;
        if (trigger.requiredFlags) {
          const allMet = Object.entries(trigger.requiredFlags).every(([k, v]) => (flags[k] ?? false) === v);
          if (!allMet) continue;
        }
        if (px >= trigger.x && px <= trigger.x + trigger.width) {
          if (trigger.type === 'battle') {
            this.scene.pause(SCENE.OVERWORLD);
            this.scene.launch(SCENE.BATTLE, { enemyId: trigger.enemyId });
          } else {
            this.dialogueSystem.open(trigger.dialogueId);
          }
          break;
        }
      }
    }

    // ── Interaction ────────────────────────────────────────────────────────
    if (this.controls.actionJustPressed) {
      const target = this.getNearbyNPC();
      if (target) {
        const dlgId = this.resolveDialogueId(target);
        this.dialogueSystem.open(dlgId);
      }
    }

    // ── Quest auto-check ───────────────────────────────────────────────────
    const newDone = QuestSystem.checkAll();
    if (newDone.length > 0) {
      // TODO: show quest-complete toast via HUD
    }

    this.hud.update(stateManager.get().player);
    this.itemBar.update();
    this.updateNavArrow(delta);
  }

  // ── World ─────────────────────────────────────────────────────────────────

  private buildWorld(): void {
    const W = OverworldScene.WORLD_W;
    const H = OverworldScene.WORLD_H;

    const g = this.add.graphics();

    // Sky: handled by initDayCycle's skyRect (dynamic day/night cycle)

    // Asphalt road
    g.fillStyle(0x484440);
    g.fillRect(0, Math.floor(H * 0.55), W, Math.ceil(H * 0.45));

    // Front sidewalk
    g.fillStyle(0xB4AE9E);
    g.fillRect(0, Math.floor(H * 0.52), W, Math.ceil(H * 0.04));

    // Back sidewalk
    g.fillStyle(0xB4AE9E);
    g.fillRect(0, Math.floor(H * 0.77), W, Math.ceil(H * 0.04));

    // Red bike lanes (fietstraten) — between sidewalks and tram/car zone
    g.fillStyle(0xBB3030);
    g.fillRect(0, Math.floor(H * 0.558), W, Math.ceil(H * 0.040));  // front lane
    g.fillRect(0, Math.floor(H * 0.730), W, Math.ceil(H * 0.040));  // rear  lane

    // Bike-lane white bicycle stencils (every 160px, centred in lane)
    g.fillStyle(0xFFFFFF, 0.35);
    const frontLaneY = Math.floor(H * 0.578);
    const rearLaneY  = Math.floor(H * 0.750);
    for (let x = 80; x < W; x += 160) {
      // simple diamond stencil approximation
      g.fillRect(x - 2, frontLaneY - 1, 4, 2);
      g.fillRect(x - 1, frontLaneY + 1, 2, 2);
      g.fillRect(x - 2, rearLaneY  - 1, 4, 2);
      g.fillRect(x - 1, rearLaneY  + 1, 2, 2);
    }

    // Tram tracks — detailed: cross-ties + raised steel rails + highlights
    const r1 = Math.floor(H * 0.615);   // north rail centre
    const r2 = Math.floor(H * 0.685);   // south rail centre
    // Cross-ties (traverse / wooden sleepers)
    g.fillStyle(0x3A2A18);
    for (let x = 0; x < W; x += 10) {
      g.fillRect(x, r1 - 2, 7, 5);
      g.fillRect(x, r2 - 2, 7, 5);
    }
    // Rail base (dark shadow)
    g.fillStyle(0x606070);
    g.fillRect(0, r1 - 1, W, 4);
    g.fillRect(0, r2 - 1, W, 4);
    // Rail top (steel highlight)
    g.fillStyle(0xC8C8D8);
    g.fillRect(0, r1 - 1, W, 2);
    g.fillRect(0, r2 - 1, W, 2);
    // Rail inner groove (recess for flanged wheels)
    g.fillStyle(0x282830);
    g.fillRect(0, r1,     W, 1);
    g.fillRect(0, r2,     W, 1);

    // White dashed dividers at bike-lane edges
    g.fillStyle(0xFFFFFF, 0.50);
    for (let x = 0; x < W; x += 28) {
      g.fillRect(x, Math.floor(H * 0.556), 14, 1);
      g.fillRect(x, Math.floor(H * 0.600), 14, 1);
      g.fillRect(x, Math.floor(H * 0.728), 14, 1);
      g.fillRect(x, Math.floor(H * 0.772), 14, 1);
    }

    // Building facade strip
    this.placeBuildingFacades(W, H);

    // Street trees — placed after road so they render on top of asphalt
    this.placeStreetTrees(W, H);

    // Zone boundary visual hints (subtle colour shift at gates)
    this.drawZoneBoundaryMarkers(H);
  }

  /**
   * Building tiles (generated from Streetdata.md, house-number order):
   * Tile index map — Borgerhout (2140):
   *  0=Indian Boutique#137   1=Patisserie Aladdin#170  2=Brasserie 't Center#180
   *  3=Bakkerij Charif#189   4=Frituur de Tram#200     5=Theehuys Amal#215
   *  6=Mimoun#239            7=Nacht Winkel#240         8=Hammam Borgerhout#260
   *  9=Borger Hub#284        10=Apotheek Praats#317    11=Budget Market#326
   *  12=Costermans#332       13=Basic-Fit#360          14=New Star Kebab#370
   *  15=Carrefour Market     16=brick_a  17=brick_b   18=brick_c  19=vacant
   *  20=Ornipa Parket#257    21=Eéntje Meer#343        22=Heiremans#381
   *  23=Audifoon#410
   * Deurne (2100):
   *  24=Pluym#1-3            25=Svelta#30              26=Optiek VDB#31-33
   *  27=Inverko#62-64        28=Schaeps#92-94          29=Cobra Keukens#108
   *  30=Miss Sera#115        31=De Mont#212            32=Ter Rivierenhof#247
   * Wijnegem (2110):
   *  33=Wijnegem SEC#5       34=Nada#5u208             35=Beeckman#90
   *  36=Hillaert#276-278     37=Optiek Ann Brands#339  38=Apotheek Meeussen#351
   *  39=TattooCharis#372     40=Frituur De Brug#471
   */
  private placeBuildingFacades(W: number, H: number): void {
    const TW = 96;   // tile display width in Phaser game-units (2× the 48 game-px tile)
    const buildingBottom = Math.floor(H * 0.52);

    // Real house-number sequence (west → east), all shops from streetdata.md
    // Borgerhout → Deurne → Wijnegem
    const streetLayout = [
      16, 17,                          // brick (west edge)
      // ── Borgerhout (2140) ──────────────────────────────
      0,                               // Indian Boutique #137
      16,
      1,                               // Patisserie Aladdin #170
      2,                               // Brasserie 't Center #180
      3,                               // Bakkerij Charif #189
      16,
      4,                               // Frituur de Tram #200
      5,                               // Theehuys Amal #215
      18,
      6,                               // Mimoun #239
      7,                               // Nacht Winkel #240
      20,                              // Ornipa Parket #257
      17,
      8,                               // Hammam Borgerhout #260
      16,
      9,                               // Borger Hub #284
      18,
      10,                              // Apotheek Praats #317
      11,                              // Budget Market #326
      12,                              // Costermans Wielersport #332
      21,                              // Eéntje Meer #343
      19,                              // Vacant
      13,                              // Basic-Fit #360
      14,                              // New Star Kebab #370
      22,                              // Hendrik Heiremans #381
      16,
      23,                              // Audifoon #410
      15,                              // Carrefour Market
      17, 18,                          // brick filler
      // ── Deurne (2100) ─────────────────────────────────
      24,                              // Pluym #1-3
      16,
      25,                              // Svelta #30
      26,                              // Optiek Frits Van Den Bosh #31-33
      16,
      27,                              // Inverko Parfumerie #62-64
      16,
      28,                              // Schaeps Medische Hulpmiddelen #92-94
      29,                              // Cobra Keukens #108
      30,                              // Miss Sera #115
      16,
      31,                              // De Mont #212
      16,
      32,                              // Ter Rivierenhof #247
      17,
      // ── Wijnegem (2110) ───────────────────────────────
      33,                              // Wijnegem Shop Eat Enjoy #5
      34,                              // Nada #5 unit 208
      16,
      35,                              // Beeckman & Co #90
      17,
      36,                              // Hillaert #276-278
      17,
      37,                              // Optiek Ann Brands #339-341
      38,                              // Apotheek Meeussen #351
      39,                              // TattooCharis #372
      16,
      40,                              // Frituur De Brug #471
      17, 18,                          // brick (east edge)
    ];

    // Height variation per tile frame — buildings differ in stories/prominence.
    // Default display height: 130 Phaser units. All share dH_src=108 game-px crop.
    const TILE_HEIGHTS: Record<number, number> = {
      4:  114,  // Frituur de Tram         — low 1-storey shed
      7:  116,  // Nacht Winkel            — compact night shop
      8:  148,  // Hammam Borgerhout       — ornate 3-storey landmark
      9:  144,  // Borger Hub              — renovated 3-storey community hub
      11: 154,  // Budget Market           — 4-storey corner block
      13: 150,  // Basic-Fit               — large industrial gym volume
      15: 146,  // Carrefour               — wide supermarket
      16: 140,  // brick_a rowhouse        — standard 3-storey residence
      18: 142,  // brick_c (bay window)    — slightly taller gable
      20: 118,  // Ornipa Parket           — small 2-storey shop
      21: 112,  // Eéntje Meer             — tiny service office
      22: 138,  // Heiremans               — dignified 3-storey funeral home
      23: 124,  // Audifoon                — modern 2-storey clinic
      // Deurne
      24: 136,  // Pluym                   — large 3-storey furniture showroom
      25: 118,  // Svelta                  — small boutique
      26: 126,  // Optiek VDB              — mid-size optician
      27: 128,  // Inverko Parfumerie      — elegant 2-storey
      28: 122,  // Schaeps                 — small medical shop
      29: 132,  // Cobra Keukens           — medium showroom
      30: 120,  // Miss Sera               — boutique
      31: 124,  // De Mont                 — small gifts shop
      32: 136,  // Ter Rivierenhof         — brasserie, tall ceilings
      // Wijnegem
      33: 148,  // Wijnegem SEC            — large shopping centre
      34: 116,  // Nada                    — small shoe shop
      35: 130,  // Beeckman                — garden centre
      36: 120,  // Hillaert                — small specialist shop
      37: 126,  // Optiek Ann Brands       — optician
      38: 122,  // Apotheek Meeussen       — pharmacy
      39: 114,  // TattooCharis            — small tattoo studio
      40: 116,  // Frituur De Brug         — frituur
    };

    // All tiles: SCALE=8, plinth at game-y=104, show top 108 game-px of tile.
    // Displayed at TW=96 (2× wide); height varies per tile for skyline interest.
    const PNG_W  = 384;   // PNG frame width  (SCALE=8, TW=48 → 384 px)
    const dH_src = 108;   // source game-px to show (108 × 8 = 864 PNG px)

    let tileX = 0;
    let idx   = 0;
    while (tileX < W) {
      const frame      = streetLayout[idx % streetLayout.length];
      const dH_display = TILE_HEIGHTS[frame] ?? 130;
      this.add.image(tileX, buildingBottom, 'buildings', frame)
        .setOrigin(0, 1)
        .setCrop(0, 0, PNG_W, dH_src * 8)      // show top 108 game-px (864 PNG px)
        .setDisplaySize(TW, dH_display)
        .setDepth(1);
      tileX += TW;
      idx++;
    }
  }

  /**
   * Pixel-art city trees along both sides of the bike lanes.
   * Placed every ~180 px with slight random offset, alternating front/rear.
   * Each tree: trunk + round canopy, drawn with graphics (no texture needed).
   */
  private placeStreetTrees(W: number, H: number): void {
    // Y positions: just outside each bike lane (between sidewalk and bike lane edge)
    const frontTreeY = Math.floor(H * 0.552);   // just above front bike lane
    const rearTreeY  = Math.floor(H * 0.776);   // just below rear  bike lane

    const SPACING  = 180;   // px between trees on the same side
    const TRUNK_W  = 4;
    const TRUNK_H  = 10;
    const CANOPY_W = 10;    // ellipse half-width  (game units)
    const CANOPY_H = 30;    // ellipse half-height (3× taller)

    // Two shades of green for natural variety
    const canopyColors  = [0x2D7A2D, 0x3A9A3A, 0x256025, 0x4AAF4A];
    const shadowColor   = 0x1A5C1A;
    const trunkColor    = 0x6B4226;
    const trunkDark     = 0x4A2C10;

    // Draw one tree at (x, baseY) where baseY is the ground level of the trunk
    const drawTree = (g: Phaser.GameObjects.Graphics, x: number, baseY: number, colorIdx: number) => {
      const cy = baseY - TRUNK_H - CANOPY_H;  // canopy centre Y (bottom of ellipse at trunk top)

      // Trunk
      g.fillStyle(trunkColor);
      g.fillRect(x - TRUNK_W / 2, baseY - TRUNK_H, TRUNK_W, TRUNK_H);
      g.fillStyle(trunkDark);
      g.fillRect(x - TRUNK_W / 2, baseY - TRUNK_H, 1, TRUNK_H);

      // Canopy shadow (slightly offset down-right)
      g.fillStyle(shadowColor);
      g.fillEllipse(x + 2, cy + 2, CANOPY_W * 2, CANOPY_H * 2);

      // Canopy main
      g.fillStyle(canopyColors[colorIdx % canopyColors.length]);
      g.fillEllipse(x, cy, CANOPY_W * 2, CANOPY_H * 2);

      // Canopy highlight (top-left, smaller inner ellipse)
      g.fillStyle(0x5FCC5F);
      g.fillEllipse(x - 3, cy - Math.floor(CANOPY_H * 0.35), CANOPY_W * 0.9, CANOPY_H * 0.6);
    };

    const g = this.add.graphics().setDepth(2);

    let seedOffset = 0;
    for (let x = 60; x < W; x += SPACING) {
      // Randomise position and side using a deterministic offset
      const jitter     = ((seedOffset * 137) % 60) - 30;   // –30 to +30
      const colorIdx   = seedOffset % canopyColors.length;
      const frontOrRear = seedOffset % 3;   // 0,1 = front; 2 = rear

      if (frontOrRear < 2) {
        drawTree(g, x + jitter, frontTreeY, colorIdx);
      } else {
        drawTree(g, x + jitter, rearTreeY, colorIdx + 1);
      }
      seedOffset++;

      // Occasionally place one on the opposite side too
      if (seedOffset % 5 === 0) {
        const jitter2  = ((seedOffset * 97) % 40) - 20;
        drawTree(g, x + jitter2 + 90, rearTreeY, colorIdx + 2);
      }
    }
  }

  private drawZoneBoundaryMarkers(H: number): void {
    const g = this.add.graphics().setDepth(2);
    // Subtle vertical marker lines at each gate
    for (const zone of [2, 3, 4, 5]) {
      const x = ZONE_STARTS[zone];
      g.fillStyle(0x888888, 0.3);
      g.fillRect(x - 1, 0, 2, Math.floor(H * 0.52));
    }
  }

  // ── Named NPCs ────────────────────────────────────────────────────────────

  private spawnNamedNPCs(): void {
    const H = OverworldScene.WORLD_H;
    const sw = Math.floor(H * 0.54);   // front sidewalk y

    // Named NPCs — each uses individual spritesheet from BootScene
    // NPC x-positions aligned with their associated buildings (tile width = 96):
    //   #137 Indian Boutique  → x≈210   #170 Patisserie Aladdin → x≈400
    //   #189 Bakkerij Charif  → x≈590   #215 Theehuys Amal      → x≈880
    //   #239 Mimoun           → x≈1060  #260 Hammam Borgerhout  → x≈1360
    //   #284 Borger Hub       → x≈1550  #326 Budget Market      → x≈1840
    //   #332 Costermans       → x≈1940
    const seed: Array<{ id: string; texture: string; x: number; y: number; dialogue: string }> = [
      { id: 'baert',    texture: 'npc_baert',   x:  210, y: sw,     dialogue: 'stunt_baert'       }, // Indian Boutique #137
      { id: 'fatima',   texture: 'npc_fatima',  x:  400, y: sw,     dialogue: 'fatima_intro'      }, // Patisserie Aladdin #170
      { id: 'hamza',    texture: 'npc_hamza',   x:  500, y: sw + 2, dialogue: 'hamza_marbles'     }, // between #170 and #189
      { id: 'omar',     texture: 'npc_omar',    x:  590, y: sw - 2, dialogue: 'omar_bakker'       }, // Bakkerij Charif #189
      { id: 'reza',     texture: 'npc_reza',    x:  880, y: sw - 1, dialogue: 'reza_music'        }, // Theehuys Amal #215
      { id: 'aziz',     texture: 'npc_aziz',    x: 1060, y: sw - 1, dialogue: 'aziz_signature'   }, // Mimoun #239
      { id: 'tine',     texture: 'npc_tine',    x: 1160, y: sw + 1, dialogue: 'tine_faction'      }, // Nacht Winkel #240
      { id: 'el_osri',  texture: 'npc_el_osri', x: 1664, y: sw,     dialogue: 'district_mayor'    }, // Borger Hub #284 (tile 17, x=1632)
      // De Roma #286 handled by location trigger at x=1728 → de_roma_keeper dialogue
      { id: 'yusuf',    texture: 'npc_yusuf',   x:  300, y: sw,     dialogue: 'yusuf_delivery'    }, // near start of street — courier with flat tyre
    ];

    this.npcs = seed.map(d =>
      new NPC(this, d.x, d.y, d.texture, 0, d.id, d.dialogue),
    );
  }

  // ── Crowd NPCs (anonymous pedestrians + vehicles) ─────────────────────────

  private crowdTimers:      number[] = [];
  private crowdDirs:        number[] = [];
  private crowdFrameBases:  number[] = [];  // first frame index for each crowd NPC's variant
  private crowdStepTimers:  number[] = [];  // ms since last walk-frame toggle
  private crowdStepFrames:  number[] = [];  // 0 or 1 → pose 1 or 2 within variant

  // Vehicles: arcade static images so the player can collide with them individually
  private vehicles: Array<{ sprite: Phaser.Physics.Arcade.Image; vx: number; baseVx: number }> = [];

  // Tram: single eastbound De Lijn tram that cars must yield to
  private tram: { sprite: Phaser.Physics.Arcade.Image; state: 'moving' | 'stopped'; stateTimer: number } | null = null;
  private static readonly TRAM_SPEED = 44;   // px/s when moving

  private spawnVehicles(): void {
    const H  = OverworldScene.WORLD_H;
    const W  = OverworldScene.WORLD_W;
    const VW = 96;
    const VH = 26;  // keep cars short so they stay within their lane

    // North tram rail: H*0.615 = 166px  — cars must stay ABOVE this
    // South tram rail: H*0.685 = 185px  — buses must stay BELOW this
    // Front bike lane centre: H*0.578 = 156px
    // Rear  bike lane centre: H*0.750 = 202px
    const laneE = Math.floor(H * 0.608);  // eastbound — between front bike lane and north rail
    const laneW = Math.floor(H * 0.705);  // westbound — between south rail and rear bike lane

    // [frame, speed px/s, display_w, display_h]
    const eastTypes: [number, number, number, number][] = [
      [5, 46, VW + 14, VH],  // De Lijn bus — slowest, leads the queue
      [2, 62, VW + 6,  VH],  // kangoo
      [3, 70, VW,      VH],  // suv
      [4, 72, VW,      VH],  // taxi
    ];
    const westTypes: [number, number, number, number][] = [
      [0, 68, VW,      VH],      // clio_blue
      [1, 74, VW,      VH],      // clio_red
      [6, 86, VW - 14, VH - 4],  // scooter (smaller)
      [3, 65, VW,      VH],      // suv
    ];

    const N = 4;  // cars per lane — 4 cars spread across 2880px ≈ 720px each

    for (let i = 0; i < N; i++) {
      const spacing = W / N;

      const eConf = eastTypes[i];
      const ex = Math.floor(spacing * i + spacing * 0.3);
      const eImg = this.physics.add.staticImage(ex, laneE, 'vehicles', eConf[0])
        .setDisplaySize(eConf[2], eConf[3]).setOrigin(0.5, 0.5).setDepth(laneE);
      eImg.setBodySize(eConf[2] * 0.85, eConf[3] * 0.7);
      eImg.refreshBody();
      this.vehicles.push({ sprite: eImg, vx: eConf[1], baseVx: eConf[1] });

      const wConf = westTypes[i];
      const wx = Math.floor(spacing * i + spacing * 0.7);
      const wImg = this.physics.add.staticImage(wx, laneW, 'vehicles', wConf[0])
        .setDisplaySize(wConf[2], wConf[3]).setOrigin(0.5, 0.5).setFlipX(true).setDepth(laneW);
      wImg.setBodySize(wConf[2] * 0.85, wConf[3] * 0.7);
      wImg.refreshBody();
      this.vehicles.push({ sprite: wImg, vx: -wConf[1], baseVx: -wConf[1] });
    }
  }

  private updateVehicles(delta: number): void {
    const W          = OverworldScene.WORLD_W;
    const dt         = delta / 1000;
    const tramX      = this.tram?.sprite.x ?? null;
    const tramHalfW  = 168;
    const tramMoving = this.tram?.state === 'moving';
    const SAFE_GAP   = 110;  // minimum px between front bumpers before slowing

    const eastbound = this.vehicles.filter(v => v.baseVx > 0);
    const westbound = this.vehicles.filter(v => v.baseVx < 0);

    for (const v of this.vehicles) {
      if (!v.sprite.active) continue;
      const isEast  = v.baseVx > 0;
      const sameLane = isEast ? eastbound : westbound;

      // ── Find gap to nearest car ahead in same lane ─────────────────────
      let gapAhead = Infinity;
      for (const other of sameLane) {
        if (other === v) continue;
        const rawGap = isEast
          ? other.sprite.x - v.sprite.x   // positive = other is ahead for eastbound
          : v.sprite.x - other.sprite.x;  // positive = other is ahead for westbound
        if (rawGap > 0 && rawGap < gapAhead) gapAhead = rawGap;
      }

      // ── Target speed: yield to car ahead and/or tram ───────────────────
      let targetVx = Math.abs(v.baseVx);

      if (gapAhead < SAFE_GAP) {
        // Slow proportionally — stop completely when gap < 20px
        targetVx *= Math.max(0, (gapAhead - 20) / (SAFE_GAP - 20));
      }

      if (isEast && tramX !== null) {
        const tramGap = tramX - tramHalfW - v.sprite.x;
        if (tramGap > 0 && tramGap < 120) {
          targetVx = Math.min(targetVx, tramMoving ? OverworldScene.TRAM_SPEED * 0.9 : 0);
        }
      }

      // ── Smoothly adjust speed ──────────────────────────────────────────
      const absVx    = Math.abs(v.vx);
      const accel    = Math.abs(v.baseVx) * 2 * dt;
      const newAbsVx = absVx < targetVx
        ? Math.min(targetVx, absVx + accel)   // accelerate
        : Math.max(targetVx, absVx - accel * 3); // brake faster than accelerate
      v.vx = isEast ? newAbsVx : -newAbsVx;

      v.sprite.x += v.vx * dt;
      if (isEast  && v.sprite.x > W + 80) v.sprite.x = -80;
      if (!isEast && v.sprite.x < -80)    v.sprite.x = W + 80;
      (v.sprite.body as Phaser.Physics.Arcade.StaticBody).reset(v.sprite.x, v.sprite.y);
    }
  }

  private spawnTram(): void {
    const H  = OverworldScene.WORLD_H;
    const tramY = Math.floor(H * 0.650);   // centre between the two tram rails
    const img = this.physics.add.staticImage(-150, tramY, 'tram')
      .setDisplaySize(336, 66)
      .setOrigin(0.5, 0.5)
      .setDepth(tramY);   // Y-sort depth
    img.setBodySize(320, 50);
    img.refreshBody();
    this.tram = { sprite: img, state: 'moving', stateTimer: Phaser.Math.Between(10000, 16000) };
  }

  private updateTram(delta: number): void {
    if (!this.tram) return;
    const t = this.tram;
    const W = OverworldScene.WORLD_W;
    t.stateTimer -= delta;

    if (t.state === 'moving') {
      t.sprite.x += OverworldScene.TRAM_SPEED * (delta / 1000);
      if (t.sprite.x > W + 200) t.sprite.x = -200;
      (t.sprite.body as Phaser.Physics.Arcade.StaticBody).reset(t.sprite.x, t.sprite.y);
      if (t.stateTimer <= 0) {
        t.state = 'stopped';
        t.stateTimer = Phaser.Math.Between(2500, 4500);  // halt at stop 2.5–4.5s
      }
    } else {
      if (t.stateTimer <= 0) {
        t.state = 'moving';
        t.stateTimer = Phaser.Math.Between(8000, 15000); // drive 8–15s between stops
      }
    }
  }

  // Bikers: 16 types, two red bike lanes (front=eastbound, rear=westbound)
  private bikers: Array<{ sprite: Phaser.GameObjects.Image; vx: number }> = [];

  private spawnBikers(): void {
    const H  = OverworldScene.WORLD_H;
    const W  = OverworldScene.WORLD_W;
    // Bikes are player-sized: FW=36, FH=30 game-px (SCALE=6)
    const BW = 36;
    const BH = 30;

    const laneF = Math.floor(H * 0.578);   // front bike lane centre
    const laneR = Math.floor(H * 0.750);   // rear  bike lane centre

    // Per-frame speeds (px/s) reflecting each bike type's realistic pace
    const bikerSpeeds: Record<number, number> = {
      0:  95,  // racing_red    — very fast
      1:  90,  // racing_blue   — very fast
      2:  62,  // city_blue     — medium
      3:  58,  // city_red      — medium
      4:  74,  // ebike_gray    — medium-fast (electric assist)
      5:  50,  // mountain_green — medium-slow (upright position)
      6:  52,  // mountain_orange — medium-slow
      7:  36,  // cargo_yellow  — slow (heavy load)
      8:  30,  // cargo_child   — slow (child on back)
      9:  34,  // delivery_green — slow (laden delivery)
      10: 24,  // grandma_blue  — very slow
      11: 55,  // hijab_teal    — medium
      12: 53,  // hijab_purple  — medium
      13: 84,  // fixie_black   — fast (no brakes, no mercy)
      14: 28,  // dutch_beige   — slow (upright Dutch style)
      15: 66,  // bmx_red       — medium-fast
    };

    // 20 bikers: 11 eastbound on front lane, 9 westbound on rear lane
    for (let i = 0; i < 20; i++) {
      const eastbound = i < 11;
      const laneY     = eastbound ? laneF : laneR;
      const frame     = i % 16;                  // one of 16 biker types
      const speed     = bikerSpeeds[frame] ?? 50;
      const x         = Math.floor((W / 20) * i + Phaser.Math.Between(10, 50));

      const img = this.add.image(x, laneY, 'bikes', frame)
        .setDisplaySize(BW, BH)
        .setOrigin(0.5, 0.5)
        .setFlipX(!eastbound)   // westbound riders face left
        .setDepth(laneY);       // Y-sort depth matches lane position

      this.bikers.push({ sprite: img, vx: eastbound ? speed : -speed });
    }
  }

  private updateBikers(delta: number): void {
    const W  = OverworldScene.WORLD_W;
    const dt = delta / 1000;
    for (const b of this.bikers) {
      b.sprite.x += b.vx * dt;
      if (b.vx > 0 && b.sprite.x > W + 30)  b.sprite.x = -30;
      if (b.vx < 0 && b.sprite.x < -30)     b.sprite.x = W + 30;
    }
  }

  // Electric step riders: 4 types sharing the bike lanes
  private stepRiders: Array<{ sprite: Phaser.GameObjects.Image; vx: number }> = [];

  private spawnStepRiders(): void {
    const H  = OverworldScene.WORLD_H;
    const W  = OverworldScene.WORLD_W;
    // Same display size as bikers
    const SW = 36;
    const SH = 30;

    const laneF = Math.floor(H * 0.578);   // front bike lane centre
    const laneR = Math.floor(H * 0.750);   // rear  bike lane centre

    // Electric steps are faster than bikes (typical ~20–25 km/h)
    const stepSpeeds: Record<number, number> = {
      0: 110,  // kids         — fast (kids go brrrr)
      1:  95,  // moroccan_girl — medium-fast
      2: 125,  // fitness_boy  — fast (show off)
      3:  80,  // lovers       — relaxed pace
    };

    // 8 step riders spread across both lanes
    for (let i = 0; i < 8; i++) {
      const eastbound = i < 5;   // 5 eastbound, 3 westbound
      const laneY     = eastbound ? laneF : laneR;
      const frame     = i % 4;
      const speed     = stepSpeeds[frame] ?? 100;
      const x         = Math.floor((W / 8) * i + Phaser.Math.Between(20, 80));

      const img = this.add.image(x, laneY, 'steps', frame)
        .setDisplaySize(SW, SH)
        .setOrigin(0.5, 0.5)
        .setFlipX(!eastbound)
        .setDepth(laneY + 1);   // slightly above bikers to layer nicely

      this.stepRiders.push({ sprite: img, vx: eastbound ? speed : -speed });
    }
  }

  private updateStepRiders(delta: number): void {
    const W  = OverworldScene.WORLD_W;
    const dt = delta / 1000;
    for (const r of this.stepRiders) {
      r.sprite.x += r.vx * dt;
      if (r.vx > 0 && r.sprite.x > W + 30)  r.sprite.x = -30;
      if (r.vx < 0 && r.sprite.x < -30)     r.sprite.x = W + 30;
    }
  }

  private spawnCrowd(): void {
    const H  = OverworldScene.WORLD_H;
    const W  = OverworldScene.WORLD_W;
    const sy = Math.floor(H * 0.54);   // front sidewalk y
    const by = Math.floor(H * 0.79);   // back sidewalk y

    // 90 crowd pedestrians (3× original) spread across the world on both sidewalks.
    // Each of the 20 crowd variants has 3 frames: variantIdx*3+0 = idle,
    // variantIdx*3+1 = walkA, variantIdx*3+2 = walkB.
    for (let i = 0; i < 90; i++) {
      const x       = Phaser.Math.Between(40, W - 40);
      const y       = (i % 3 === 0) ? by : sy + Phaser.Math.Between(-2, 2);
      const variant = i % 20;
      const base    = variant * 3;    // first frame of this variant

      const s = this.physics.add.sprite(x, y, 'crowd', base);  // start on idle frame
      s.setOrigin(0.5, 1);
      s.setDisplaySize(12, 28);
      s.setDepth(y);
      s.setImmovable(false);

      this.crowdNPCs.push(s);
      this.crowdTimers.push(Phaser.Math.Between(1000, 4000));
      this.crowdDirs.push(Phaser.Math.Between(0, 1) === 0 ? -1 : 1);
      this.crowdFrameBases.push(base);
      this.crowdStepTimers.push(Phaser.Math.Between(0, 300));   // stagger phase
      this.crowdStepFrames.push(0);
    }
  }

  private updateCrowd(delta: number): void {
    const SPEED    = 18;
    const STEP_MS  = 240;   // ms per walk frame
    const W        = OverworldScene.WORLD_W;

    for (let i = 0; i < this.crowdNPCs.length; i++) {
      const s   = this.crowdNPCs[i];
      if (!s.active) continue;
      const dir = this.crowdDirs[i];

      // ── Direction timer ──────────────────────────────────────────────────
      this.crowdTimers[i] -= delta;
      if (this.crowdTimers[i] <= 0) {
        const prevDir = this.crowdDirs[i];
        const r = Phaser.Math.Between(0, 3);
        this.crowdDirs[i]   = r === 0 ? 0 : (r === 1 ? -1 : 1);
        this.crowdTimers[i] = Phaser.Math.Between(800, 3500);
        // On direction change, reset step to forward-foot-landing frame
        if (this.crowdDirs[i] !== prevDir && this.crowdDirs[i] !== 0) {
          this.crowdStepTimers[i] = 0;
          this.crowdStepFrames[i] = 1;   // frame base+2 = forward foot landing
        }
      }

      // ── Movement & animation ─────────────────────────────────────────────
      if (dir !== 0) {
        s.setVelocityX(dir * SPEED);
        s.setFlipX(dir < 0);
        if (s.x < 10)     s.setX(W - 10);
        if (s.x > W - 10) s.setX(10);

        // Cycle walk frames: base+1 and base+2
        this.crowdStepTimers[i] += delta;
        if (this.crowdStepTimers[i] >= STEP_MS) {
          this.crowdStepTimers[i] = 0;
          this.crowdStepFrames[i] = 1 - this.crowdStepFrames[i];   // 0 ↔ 1
        }
        const crowdWalkFrame = dir > 0
          ? 1 + this.crowdStepFrames[i]    // right: frames +1, +2
          : 2 - this.crowdStepFrames[i];   // left:  frames +2, +1 (phase-corrected)
        s.setFrame(this.crowdFrameBases[i] + crowdWalkFrame);
      } else {
        s.setVelocityX(0);
        s.setFrame(this.crowdFrameBases[i]);   // idle pose
        this.crowdStepTimers[i] = 0;
      }

      s.setDepth(s.y);
    }
  }

  // ── Pigeons ───────────────────────────────────────────────────────────────
  // 3 types × 4 frames: type*4+0=sit, +1=wings-up, +2=wings-level, +3=wings-down
  // Rooftop Y ≈ 10–15px (buildingBottom=140 - displayHeight=130 = 10px from top)

  private pigeons: Array<{
    sprite:     Phaser.GameObjects.Image;
    type:       number;  // 0=grey, 1=white dove, 2=fat brown
    state:      'sitting' | 'flying';
    stateTimer: number;
    fromX:      number;
    toX:        number;
    rooftopY:   number;
    animTimer:  number;
    animFrame:  number;  // 0-3 within type
  }> = [];

  private spawnPigeons(): void {
    const W = OverworldScene.WORLD_W;
    const H = OverworldScene.WORLD_H;
    const rooftopY = Math.floor(H * 0.52) - 125;  // near top of buildings

    for (let i = 0; i < 6; i++) {
      const x    = Math.floor((W / 6) * i + Phaser.Math.Between(20, 80));
      const type = i % 3;
      const sprite = this.add.image(x, rooftopY, 'pigeons', type * 4)
        .setDisplaySize(14, 14)
        .setOrigin(0.5, 0.5)
        .setDepth(rooftopY);

      this.pigeons.push({
        sprite,
        type,
        state:      'sitting',
        stateTimer: Phaser.Math.Between(2000, 6000),
        fromX:      x,
        toX:        x,
        rooftopY,
        animTimer:  Phaser.Math.Between(0, 400),
        animFrame:  0,
      });
    }
  }

  private updatePigeons(delta: number): void {
    const W = OverworldScene.WORLD_W;
    for (const p of this.pigeons) {
      p.stateTimer -= delta;

      if (p.state === 'sitting') {
        // Occasional idle head-bob using sit frame (frame 0 of type)
        p.animTimer += delta;
        if (p.animTimer > 800) {
          p.animTimer = 0;
          p.sprite.setFrame(p.type * 4 + 0);
        }
        if (p.stateTimer <= 0) {
          // Pick a new rooftop to fly to
          p.fromX = p.sprite.x;
          p.toX   = Phaser.Math.Clamp(
            p.sprite.x + Phaser.Math.Between(-320, 320),
            60, W - 60,
          );
          p.state      = 'flying';
          p.stateTimer = Math.abs(p.toX - p.fromX) / 80 * 1000;  // ~80px/s flight
          p.animTimer  = 0;
          p.animFrame  = 1;
        }
      } else {
        // Flying: animate wing frames 1→2→3→2→1 cycling
        p.animTimer += delta;
        if (p.animTimer >= 120) {
          p.animTimer = 0;
          p.animFrame = (p.animFrame < 3) ? p.animFrame + 1 : 1;
          p.sprite.setFrame(p.type * 4 + p.animFrame);
        }

        // Move towards target
        const progress = 1 - Math.max(0, p.stateTimer) / (Math.abs(p.toX - p.fromX) / 80 * 1000);
        p.sprite.x = p.fromX + (p.toX - p.fromX) * Math.min(progress, 1);
        p.sprite.setFlipX(p.toX < p.fromX);

        // Slight arc: rise in first half, descend in second half
        const arc = Math.sin(Math.PI * Math.min(progress, 1)) * 8;
        p.sprite.y = p.rooftopY - arc;

        if (p.stateTimer <= 0) {
          p.sprite.x = p.toX;
          p.sprite.y = p.rooftopY;
          p.sprite.setFrame(p.type * 4 + 0);
          p.state      = 'sitting';
          p.stateTimer = Phaser.Math.Between(3000, 8000);
          p.animTimer  = 0;
        }
      }
    }
  }

  // ── Street cats ───────────────────────────────────────────────────────────
  // 3 types × 5 walk frames: type*5+0..4 (elegant walk cycle)
  // Cats roam rooftops, occasionally sit or jump between levels

  private cats: Array<{
    sprite:     Phaser.GameObjects.Image;
    type:       number;   // 0=orange tabby, 1=black, 2=grey
    state:      'walking' | 'sitting';
    originX:    number;   // home position — cat wanders within ±80px of this
    vx:         number;
    stateTimer: number;
    rooftopY:   number;
    animTimer:  number;
    animFrame:  number;
  }> = [];

  private spawnCats(): void {
    const W = OverworldScene.WORLD_W;
    const H = OverworldScene.WORLD_H;
    const rooftopY = Math.floor(H * 0.52) - 118;

    for (let i = 0; i < 5; i++) {
      const x    = Math.floor((W / 5) * i + Phaser.Math.Between(60, 140));
      const type = i % 3;
      const sprite = this.add.image(x, rooftopY, 'cats', type * 5)
        .setDisplaySize(18, 12)
        .setOrigin(0.5, 1)
        .setDepth(rooftopY);

      this.cats.push({
        sprite,
        type,
        state:      'sitting',
        originX:    x,
        vx:         0,
        stateTimer: Phaser.Math.Between(2000, 6000),
        rooftopY,
        animTimer:  0,
        animFrame:  0,
      });
    }
  }

  private updateCats(delta: number): void {
    const dt = delta / 1000;

    for (const c of this.cats) {
      c.stateTimer -= delta;

      if (c.state === 'walking') {
        c.sprite.x += c.vx * dt;
        c.sprite.setFlipX(c.vx < 0);

        // Turn around when straying too far from home
        if (c.sprite.x > c.originX + 80 && c.vx > 0) c.vx *= -1;
        if (c.sprite.x < c.originX - 80 && c.vx < 0) c.vx *= -1;

        // Walk animation: cycle all 5 frames
        c.animTimer += delta;
        if (c.animTimer >= 160) {
          c.animTimer = 0;
          c.animFrame = (c.animFrame + 1) % 5;
          c.sprite.setFrame(c.type * 5 + c.animFrame);
        }

        if (c.stateTimer <= 0) {
          // Sit — cats rest longer than they walk
          c.state      = 'sitting';
          c.stateTimer = Phaser.Math.Between(4000, 10000);
          c.animFrame  = 0;
          c.sprite.setFrame(c.type * 5);
        }
      } else {
        // Sitting idle
        if (c.stateTimer <= 0) {
          // Pick a new direction and walk
          c.vx         = Phaser.Math.Between(10, 18) * (Phaser.Math.Between(0, 1) === 0 ? 1 : -1);
          c.state      = 'walking';
          c.stateTimer = Phaser.Math.Between(2000, 4500);
          c.animTimer  = 0;
        }
      }
    }
  }

  // ── Camera & physics ──────────────────────────────────────────────────────

  private createPlayer(): void {
    const spawn = stateManager.get().spawnPoint;
    this.player   = new Player(this, spawn.x, spawn.y);
    this.lastPlayerX = spawn.x;
  }

  private setupCamera(): void {
    this.cameras.main.setBounds(0, 0, OverworldScene.WORLD_W, OverworldScene.WORLD_H);
    this.cameras.main.startFollow(this.player.sprite, true, 0.08, 0.08);
    this.cameras.main.setDeadzone(GAME_WIDTH * 0.25, GAME_HEIGHT * 0.3);
  }

  private setupCollisions(): void {
    const W = OverworldScene.WORLD_W;
    const H = GAME_HEIGHT;

    // Allow the player to roam the full sidewalk + road band (H*0.50 – H*0.82).
    // Individual vehicles now act as physical obstacles via their static bodies.
    this.physics.world.setBounds(0, H * 0.50, W, H * 0.32);
    this.player.sprite.setCollideWorldBounds(true);

    // Per-vehicle colliders — player is pushed aside by each car/tram individually
    for (const v of this.vehicles) {
      this.physics.add.collider(this.player.sprite, v.sprite);
    }
    if (this.tram) {
      this.physics.add.collider(this.player.sprite, this.tram.sprite);
    }
  }

  // ── Location triggers (one-shot walk-in events) ───────────────────────────

  private setupLocationTriggers(): void {
    this.locationTriggers = [
      // ── Delivery quest — player must physically visit each address ─────────
      { type: 'dialogue', x: 192, width: 96, dialogueId: 'delivery_indian',
        onceFlag: 'delivered_137', requiredFlags: { delivery_packages_received: true } },
      { type: 'dialogue', x: 384, width: 96, dialogueId: 'delivery_aladdin',
        onceFlag: 'delivered_170', requiredFlags: { delivery_packages_received: true } },
      { type: 'dialogue', x: 1632, width: 96, dialogueId: 'delivery_borgerhub',
        onceFlag: 'delivered_284', requiredFlags: { delivery_packages_received: true } },
      // ── Budget Market flour pickup (bug 5 fix — not an NPC, location trigger) ─
      { type: 'dialogue', x: 1920, width: 96, dialogueId: 'budget_market_flour',
        onceFlag: 'has_flour', requiredFlags: { flour_quest_accepted: true } },
      // ── De Roma concert hall #286 — brick_c tile at x=1728 ────────────────
      { type: 'dialogue', x: 1728, width: 60, dialogueId: 'de_roma_keeper', onceFlag: 'visited_de_roma' },
      // ── Bureau-Bulldozer fight — guards zone 4 gate ───────────────────────
      { type: 'battle', x: 1810, width: 50, enemyId: 'bulldozer_bureau', onceFlag: 'has_permit_doc',
        requiredFlags: { visited_de_roma: true, speculator_threatened: true } },
    ];
  }

  // ── Zone gate triggers ────────────────────────────────────────────────────

  private setupZoneTriggers(): void {
    const H = OverworldScene.WORLD_H;
    for (const zone of [2, 3, 4, 5]) {
      const x = ZONE_STARTS[zone];
      const rect = this.add.zone(x, 0, 4, H).setOrigin(0, 0);
      this.physics.world.enable(rect);
      this.gateTriggers.push({ zone, rect });
    }
  }

  // ── UI ────────────────────────────────────────────────────────────────────

  private createUI(): void {
    this.hud            = new HUD(this);
    this.itemBar        = new ItemBar(this);
    this.dialogueBox    = new DialogueBox(this);
    this.dialogueSystem = new DialogueSystem(this.dialogueBox);
    this.dialogueSystem.onClose = () => this.syncMusic();

    // Navigation arrow — bottom-centre, fixed to camera
    this.navArrow = this.add.text(GAME_WIDTH / 2, GAME_HEIGHT - 6, '', {
      fontSize:        '11px',
      fontFamily:      'monospace',
      color:           '#ffffff',
      backgroundColor: '#00000088',
      padding:         { x: 5, y: 2 },
    }).setScrollFactor(0).setDepth(500).setOrigin(0.5, 1).setAlpha(0);
  }

  // ── Navigation arrow ──────────────────────────────────────────────────────

  /** Returns the world-x of the next quest objective, driven by XState machine state. */
  private getNextTarget(): { x: number; label: string } | null {
    return getNavTarget(stateManager.getSnapshot());
  }

  private updateNavArrow(delta: number): void {
    const target = this.getNextTarget();
    if (!target) { this.navArrow.setAlpha(0); return; }

    const px = this.player.sprite.x;
    const dx = target.x - px;
    if (Math.abs(dx) < 40) { this.navArrow.setAlpha(0); return; }  // close enough

    const goRight = dx > 0;
    this.navArrow.setText(goRight ? `${target.label}  ▶` : `◀  ${target.label}`);

    // Gentle pulse so it draws the eye without being distracting
    this._navBlink = (_navBlink => (_navBlink + delta * 0.003) % (Math.PI * 2))(this._navBlink);
    this.navArrow.setAlpha(0.55 + Math.sin(this._navBlink) * 0.3);
  }

  // ── Music ─────────────────────────────────────────────────────────────────

  private syncMusic(): void {
    const deliveryActive =
      stateManager.getFlag('met_yusuf') === true &&
      stateManager.getFlag('q_starter_delivery_done') !== true;

    const wantKey  = deliveryActive ? 'bgm_delivery' : 'bgm_lofi';
    const stopKey  = deliveryActive ? 'bgm_lofi'     : 'bgm_delivery';

    const current = this.sound.get(wantKey);
    if (current?.isPlaying) return;   // already on the right track

    // Fade out the current track, fade in the new one
    const outSound = this.sound.get(stopKey) as Phaser.Sound.WebAudioSound | null;
    if (outSound?.isPlaying) {
      this.tweens.add({
        targets: outSound,
        volume:  0,
        duration: 800,
        onComplete: () => outSound.stop(),
      });
    }

    this.time.delayedCall(outSound?.isPlaying ? 600 : 0, () => {
      if (!this.sound.get(wantKey)?.isPlaying) {
        this.sound.play(wantKey, { loop: true, volume: 0, });
        const inSound = this.sound.get(wantKey) as Phaser.Sound.WebAudioSound;
        this.tweens.add({ targets: inSound, volume: 0.35, duration: 800 });
      }
    });
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  private getNearbyNPC(): NPC | undefined {
    return this.npcs.find(npc =>
      Phaser.Math.Distance.Between(
        this.player.sprite.x, this.player.sprite.y,
        npc.sprite.x, npc.sprite.y,
      ) < 22,
    );
  }

  /**
   * Resolve the correct dialogue node for an NPC by evaluating all nodes that
   * declare `npc === npc.id` against current quest state, sorted by priority.
   * The highest-priority node whose conditions all pass wins.
   * Conditions and routing live in dialogue.json — no hardcoding here.
   */
  private resolveDialogueId(npc: NPC): string {
    const flags = stateManager.get().questFlags;
    const candidates = Object.entries(DIALOGUES)
      .filter(([_, node]) => node.npc === npc.id && this.conditionsMet(node.conditions, flags))
      .sort((a, b) => b[1].priority - a[1].priority);
    return candidates[0]?.[0] ?? npc.dialogueId;
  }

  /**
   * Returns true when ALL conditions in `cond` pass against current state.
   * Undefined flags are treated as false (matches switch/case !flags['x'] behaviour).
   */
  private conditionsMet(
    cond: DialogueConditions,
    flags: Record<string, boolean | string | number>,
  ): boolean {
    if (cond.flags) {
      for (const [key, val] of Object.entries(cond.flags)) {
        if ((flags[key] ?? false) !== val) return false;
      }
    }
    if (cond.items) {
      for (const id of cond.items)    { if (!stateManager.hasItem(id)) return false; }
    }
    if (cond.notItems) {
      for (const id of cond.notItems) { if (stateManager.hasItem(id))  return false; }
    }
    return true;
  }


  // ── Day/Night cycle ───────────────────────────────────────────────────────

  private initDayCycle(): void {
    const H    = GAME_HEIGHT;
    const skyH = Math.floor(H * 0.52);

    const savedMin = stateManager.get().gameTimeMinutes ?? 9 * 60;
    this._clock = new TimeManager(savedMin / 60);

    // Sky rectangle — screen-space, covers the sky strip
    this.skyRect = this.add.rectangle(0, 0, GAME_WIDTH, skyH, 0x78AFE1)
      .setOrigin(0, 0).setScrollFactor(0).setDepth(-2);

    // Stars — drawn once, toggled visible at night
    this.starsGfx = this.add.graphics().setScrollFactor(0).setDepth(-1);
    this.starsGfx.fillStyle(0xFFFFFF, 0.85);
    for (let i = 0; i < 80; i++) {
      this.starsGfx.fillPoint(
        Math.floor(Math.random() * GAME_WIDTH),
        Math.floor(Math.random() * (skyH - 8) + 4),
        1,
      );
    }
    this.starsGfx.setVisible(false);

    // Sun + moon: Graphics redrawn each frame
    this.sunGfx  = this.add.graphics().setScrollFactor(0).setDepth(-1);
    this.moonGfx = this.add.graphics().setScrollFactor(0).setDepth(-1);

    // Clouds: 4 drifting cloud shapes (screen-space)
    const cloudDefs = [
      { x:  40, y: 22, width: 64, speed: 2.2 },
      { x: 180, y: 34, width: 80, speed: 1.8 },
      { x: 310, y: 14, width: 52, speed: 3.0 },
      { x: 400, y: 28, width: 68, speed: 2.5 },
    ];
    for (const def of cloudDefs) {
      const gfx = this.add.graphics().setScrollFactor(0).setDepth(-1);
      this.drawCloud(gfx, def.width);
      gfx.x = def.x;
      gfx.y = def.y;
      this.clouds.push({ gfx, ...def });
    }

    // Clock — top-centre, screen-space
    this.clockText = this.add.text(GAME_WIDTH / 2, 4, '09:00 AM', {
      fontFamily:      '"Press Start 2P"',
      fontSize:        '6px',
      color:           '#FFFFFF',
      stroke:          '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5, 0).setScrollFactor(0).setDepth(201);

    // Night props — world-space emoji near bars/cafés, visible during isNightlife
    const sw = Math.floor(H * 0.54);
    const propDefs: Array<{ x: number; emoji: string }> = [
      { x:  748, emoji: '🍺' },  // Theehuys Amal #215
      { x:  775, emoji: '🚬' },
      { x: 1065, emoji: '🍺' },  // Mimoun #239
      { x: 1090, emoji: '🚬' },
      { x: 1265, emoji: '🚬' },  // Hammam #260
      { x: 1300, emoji: '🍺' },
      { x: 1455, emoji: '🍺' },  // Borger Hub #284
      { x:  592, emoji: '🚬' },  // Bakkerij Charif #189
      { x:  242, emoji: '🍺' },  // Indian Boutique #137
      { x:  265, emoji: '🚬' },
    ];
    for (const def of propDefs) {
      const t = this.add.text(def.x, sw - 14, def.emoji, { fontSize: '8px' })
        .setOrigin(0.5, 1).setDepth(200).setVisible(false);
      this.nightProps.push(t);
    }

    // Crowd thresholds: first 60 → random 0-1; last 30 (night crowd) → 0-0.4
    for (let i = 0; i < this.crowdNPCs.length; i++) {
      this.crowdThresholds.push(i < 60 ? Math.random() : Math.random() * 0.4);
    }

    // Vehicle thresholds: spread so low-index vehicles stay active even at low density
    for (let i = 0; i < this.vehicles.length; i++) {
      this.vehicleThresholds.push((i % 4 + 1) / 8);  // 0.125, 0.25, 0.375, 0.5
    }

    this.applyDayCycleState();
    this.updateDayCycle(0);
  }

  private updateDayCycle(delta: number): void {
    this._clock.update(delta);
    const fh   = this._clock.fractionalHour;
    const H    = GAME_HEIGHT;
    const skyH = Math.floor(H * 0.52);
    const dt   = delta / 1000;

    // Sky colour
    this.skyRect.setFillStyle(this.getSkyColor(fh));

    // Stars
    this.starsGfx.setVisible(this._clock.isNight);

    // Sun (6:30–19:30)
    this.sunGfx.clear();
    if (fh >= 6.5 && fh <= 19.5) {
      const t  = (fh - 6.5) / 13;
      const sx = t * GAME_WIDTH;
      const sy = skyH * 0.55 - Math.sin(Math.PI * t) * skyH * 0.38;
      const noon  = 1 - Math.abs(t - 0.5) * 2;
      const sg    = Math.round(160 + noon * 95);
      const sb    = Math.round(noon * 20);
      const sunCol = (0xFF << 16) | (sg << 8) | sb;
      this.sunGfx.fillStyle(sunCol, 0.28);
      this.sunGfx.fillCircle(sx, sy, 14);   // soft glow
      this.sunGfx.fillStyle(sunCol, 1);
      this.sunGfx.fillCircle(sx, sy, 9);
    }

    // Moon (20:00–06:00) with crescent shadow
    this.moonGfx.clear();
    if (fh >= 20 || fh < 6) {
      const moonFh = fh >= 20 ? fh : fh + 24;
      const t  = (moonFh - 20) / 10;
      const mx = t * GAME_WIDTH;
      const my = skyH * 0.45 - Math.sin(Math.PI * t) * skyH * 0.32;
      this.moonGfx.fillStyle(0xF8F8D0, 1);
      this.moonGfx.fillCircle(mx, my, 8);
      this.moonGfx.fillStyle(this.getSkyColor(fh), 1);
      this.moonGfx.fillCircle(mx + 3, my - 2, 8);  // crescent mask
    }

    // Clouds drift westward, wrap to right edge
    for (const cloud of this.clouds) {
      cloud.x -= cloud.speed * dt;
      if (cloud.x + cloud.width < 0) cloud.x = GAME_WIDTH;
      cloud.gfx.x = cloud.x;
    }

    // Clock
    this.clockText.setText(this._clock.timeStringAMPM);

    // Night props (bars/smokers visible 20:00–04:00)
    const showProps = this._clock.isNightlife;
    for (const p of this.nightProps) p.setVisible(showProps);

    // Recompute crowd/traffic density + sync game time to save state every 5 s
    this.densityTimer += delta;
    if (this.densityTimer >= 5000) {
      this.densityTimer = 0;
      this.applyDayCycleState();
      stateManager.setGameTime(this._clock.totalMinutes);
    }
  }

  private applyDayCycleState(): void {
    const crowd   = this._clock.crowdDensity;
    const traffic = this._clock.trafficDensity;

    for (let i = 0; i < this.crowdNPCs.length; i++) {
      const show = crowd >= this.crowdThresholds[i];
      if (!show) this.crowdNPCs[i].setVelocityX(0);
      this.crowdNPCs[i].setActive(show).setVisible(show);
    }

    for (let i = 0; i < this.vehicles.length; i++) {
      const show = traffic >= this.vehicleThresholds[i];
      this.vehicles[i].sprite.setActive(show).setVisible(show);
    }
  }

  /** Linearly interpolate between the sky colour stops at a given fractional hour. */
  private getSkyColor(fh: number): number {
    const stops = OverworldScene.SKY_STOPS;
    for (let i = 0; i < stops.length - 1; i++) {
      const [h0, c0] = stops[i];
      const [h1, c1] = stops[i + 1];
      if (fh >= h0 && fh < h1) {
        const t  = (fh - h0) / (h1 - h0);
        const r  = Math.round(((c0 >> 16) & 0xFF) + (((c1 >> 16) & 0xFF) - ((c0 >> 16) & 0xFF)) * t);
        const g  = Math.round(((c0 >>  8) & 0xFF) + (((c1 >>  8) & 0xFF) - ((c0 >>  8) & 0xFF)) * t);
        const b  = Math.round(( c0        & 0xFF) + (( c1        & 0xFF) - ( c0        & 0xFF)) * t);
        return (r << 16) | (g << 8) | b;
      }
    }
    return 0x0D0D2B;
  }

  /** Draw a fluffy cloud shape into a Graphics object (origin = left edge, centre-y). */
  private drawCloud(gfx: Phaser.GameObjects.Graphics, width: number): void {
    const h  = Math.floor(width * 0.38);
    const cx = width * 0.5;
    gfx.fillStyle(0xFFFFFF, 0.82);
    gfx.fillEllipse(cx,                0,          width,        h);
    gfx.fillEllipse(cx - width * 0.22, h * 0.15,  width * 0.55, h * 0.80);
    gfx.fillEllipse(cx + width * 0.18, h * 0.15,  width * 0.50, h * 0.72);
  }
}
