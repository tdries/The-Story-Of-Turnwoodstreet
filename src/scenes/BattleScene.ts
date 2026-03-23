import Phaser from 'phaser';
import { SCENE, GAME_WIDTH, GAME_HEIGHT } from '@core/GameConfig';
import { stateManager }  from '@core/StateManager';
import { InputHandler }  from '@core/InputHandler';
import { CombatSystem, BattleResult } from '@systems/CombatSystem';
import { localeManager } from '@i18n/LocaleManager';
import { gameEventLogger } from '@core/GameEventLogger';
import enemyData from '@data/enemies.json';

export interface BattleSceneData {
  enemyId: string;
}

/**
 * BattleScene — turn-based combat.
 *
 * Layout (top-down letterbox within the game canvas):
 *   ┌─────────────────────────────────────────┐
 *   │  [Enemy sprite]   vs   [Player sprite]  │
 *   │─────────────────────────────────────────│
 *   │  HP bars + name labels                  │
 *   │─────────────────────────────────────────│
 *   │  [Attack] [Skill] [Item] [Run]          │
 *   └─────────────────────────────────────────┘
 */
export class BattleScene extends Phaser.Scene {
  private controls!: InputHandler;
  private combat!: CombatSystem;
  private enemyId!: string;
  private menuIndex = 0;
  private menuLocked = false;

  private menuTexts: Phaser.GameObjects.Text[] = [];
  private messageText!: Phaser.GameObjects.Text;
  private playerHpBar!: Phaser.GameObjects.Rectangle;
  private enemyHpBar!:  Phaser.GameObjects.Rectangle;
  // Maps enemyId → frame index in battle_sprites sheet
  private static readonly ENEMY_FRAMES: Record<string, number> = {
    straatvechter:    1,
    pickpocket:       2,
    bulldozer_bureau: 3,
    speculant:        4,
    tram_geest:       5,
    vlok_geest:       6,
  };

  // Menu labels resolved at create() time; indices: 0=attack 1=skill 2=item 3=run
  private readonly MENU_ACTIONS = ['attack', 'skill', 'item', 'run'] as const;
  private menuLabels: string[] = [];

  constructor() {
    super({ key: SCENE.BATTLE });
  }

  init(data: BattleSceneData): void {
    this.enemyId = data.enemyId ?? 'straatvechter';
  }

  create(): void {
    this.controls = new InputHandler(this);

    // Build locale-aware menu labels
    this.menuLabels = [
      localeManager.t('attack'),
      localeManager.t('skill'),
      localeManager.t('item'),
      localeManager.t('run'),
    ];

    const enemy = (enemyData as Record<string, typeof enemyData[keyof typeof enemyData]>)[this.enemyId];
    const player = stateManager.get().player;
    this.combat = new CombatSystem(
      { id: 'player', name: player.name, hp: player.hp, maxHp: player.maxHp, atk: 5, def: 2, spd: 4 },
      { id: this.enemyId, name: enemy?.name ?? localeManager.t('enemy_default'),
        hp: enemy?.hp ?? 10, maxHp: enemy?.hp ?? 10,
        atk: enemy?.atk ?? 3, def: enemy?.def ?? 1, spd: enemy?.spd ?? 3 },
    );

    const enemyName = enemy?.name ?? localeManager.t('enemy_default');
    this.buildUI(enemyName);
    this.cameras.main.fadeIn(300, 0, 0, 0);
    this.showMessage(localeManager.t('enemy_appears').replace('{name}', enemyName));
  }

  update(): void {
    if (this.menuLocked) return;

    if (this.controls.upJustPressed)   this.moveMenu(-1);
    if (this.controls.downJustPressed) this.moveMenu(1);

    if (this.controls.actionJustPressed) this.selectMenu();
    if (this.controls.cancelJustPressed) this.endBattle('escaped');
  }

  // ── UI ───────────────────────────────────────────────────────────────────

  private buildUI(enemyName: string): void {
    const W = GAME_WIDTH;
    const H = GAME_HEIGHT;

    // Background
    this.add.rectangle(W / 2, H / 2, W, H, 0x1a0a0a);

    // Battle sprites — enemy faces right (flipX), player faces left (flipX)
    const enemyFrame = BattleScene.ENEMY_FRAMES[this.enemyId] ?? 1;
    this.add.image(W * 0.32, H * 0.33, 'battle_sprites', enemyFrame)
      .setDisplaySize(44, 56).setFlipX(true);
    this.add.image(W * 0.68, H * 0.42, 'battle_sprites', 0)
      .setDisplaySize(36, 48).setFlipX(true);

    // HP bars
    const p = stateManager.get().player;
    this.add.text(8, H * 0.62, enemyName, { fontFamily: '"Press Start 2P"', fontSize: '5px', color: '#F0EAD6' });
    this.add.rectangle(8, H * 0.68, 80, 4, 0x333333).setOrigin(0, 0.5);
    this.enemyHpBar = this.add.rectangle(8, H * 0.68, 80, 4, 0xE63946).setOrigin(0, 0.5);

    this.add.text(W - 8, H * 0.62, p.name, { fontFamily: '"Press Start 2P"', fontSize: '5px', color: '#F0EAD6' }).setOrigin(1, 0);
    this.add.rectangle(W - 88, H * 0.68, 80, 4, 0x333333).setOrigin(0, 0.5);
    this.playerHpBar = this.add.rectangle(W - 88, H * 0.68, 80, 4, 0x52C41A).setOrigin(0, 0.5);

    // Message box
    this.add.rectangle(W / 2, H * 0.79, W - 4, 28, 0x111111).setStrokeStyle(1, 0x444444);
    this.messageText = this.add.text(6, H * 0.79 - 10, '', {
      fontFamily: '"Press Start 2P"',
      fontSize: '5px',
      color: '#F0EAD6',
      wordWrap: { width: W - 12 },
    });

    // Menu
    const menuX = W - 90;
    const menuY = H * 0.84;
    this.add.rectangle(menuX + 40, menuY + 12, 90, 36, 0x0A0A12).setStrokeStyle(1, 0xFFD700);
    this.menuTexts = this.menuLabels.map((label, i) => {
      return this.add.text(menuX + 4, menuY + 4 + i * 9, label, {
        fontFamily: localeManager.gameFont,
        fontSize: '5px',
        color: '#F0EAD6',
      });
    });

    this.highlightMenu();
  }

  private moveMenu(dir: number): void {
    this.menuIndex = Phaser.Math.Wrap(this.menuIndex + dir, 0, this.menuLabels.length);
    this.highlightMenu();
  }

  private highlightMenu(): void {
    this.menuTexts.forEach((t, i) => {
      t.setColor(i === this.menuIndex ? '#FFD700' : '#F0EAD6');
    });
  }

  private selectMenu(): void {
    const action = this.MENU_ACTIONS[this.menuIndex];
    if (action === 'run') { this.endBattle('escaped'); return; }

    this.menuLocked = true;
    const result = this.combat.playerTurn(action === 'attack' ? 'attack' : 'skill');
    this.showMessage(result.message);
    this.refreshBars();

    this.time.delayedCall(900, () => {
      if (this.combat.isOver) {
        this.endBattle(this.combat.outcome as BattleResult);
        return;
      }
      const enemyResult = this.combat.enemyTurn();
      this.showMessage(enemyResult.message);
      this.refreshBars();
      this.time.delayedCall(900, () => {
        if (this.combat.isOver) this.endBattle(this.combat.outcome as BattleResult);
        else this.menuLocked = false;
      });
    });
  }

  private refreshBars(): void {
    const { player, enemy } = this.combat.getState();
    this.playerHpBar.width = 80 * (player.hp / player.maxHp);
    this.enemyHpBar.width  = 80 * (enemy.hp  / enemy.maxHp);
  }

  private showMessage(msg: string): void {
    this.messageText.setText(msg);
  }

  // Items that grant a companion quest flag when received as loot
  private static readonly LOOT_FLAGS: Record<string, string> = {
    permit_doc:       'has_permit_doc',
    oud_string:       'has_oud_string_item',
    reuzenpoort_key:  'has_reuzenpoort_key',
  };

  private endBattle(result: BattleResult | 'escaped'): void {
    const enemyDef = (enemyData as Record<string, typeof enemyData[keyof typeof enemyData]>)[this.enemyId];

    if (result === 'victory') {
      const xpGain   = enemyDef?.xp    ?? 20;
      const coinGain  = enemyDef?.coins ?? 0;
      const loot      = (enemyDef as any)?.loot as string[] ?? [];

      gameEventLogger.logBattle(this.enemyId, result, xpGain, coinGain);

      const levelled = stateManager.gainXP(xpGain);
      if (coinGain > 0) stateManager.addCoins(coinGain);

      for (const itemId of loot) {
        stateManager.addItem(itemId);
        const flagKey = BattleScene.LOOT_FLAGS[itemId];
        if (flagKey) stateManager.setFlag(flagKey, true);
      }

      const msg = levelled ? localeManager.t('level_up') : `+${xpGain} XP`;
      this.showMessage(`${localeManager.t('victory')} ${msg}`);
    } else if (result === 'defeat') {
      gameEventLogger.logBattle(this.enemyId, result);
      stateManager.setHP(1);
      this.showMessage(localeManager.t('defeat'));
    } else if (result === 'escaped') {
      gameEventLogger.logBattle(this.enemyId, result);
    }

    stateManager.setHP(this.combat.getState().player.hp);
    stateManager.save();

    this.time.delayedCall(1200, () => {
      this.cameras.main.fadeOut(400, 0, 0, 0);
      this.cameras.main.once('camerafadeoutcomplete', () => {
        this.scene.stop(SCENE.BATTLE);
        this.scene.resume(SCENE.OVERWORLD);
      });
    });
  }
}
