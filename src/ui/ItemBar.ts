import Phaser from 'phaser';
import { stateManager } from '@core/StateManager';

/**
 * ItemBar — camera-fixed vertical panel on the left side of the screen.
 *
 * Shows every item currently in the player's inventory as a 16×16 pixel icon.
 * When an item is picked up it flashes gold; when removed it fades out.
 * Stackable items show a quantity badge in the top-right corner of the slot.
 *
 * Frame index map (matches Sprites/generate_items.py order):
 *   0  fabric_bolt        1  delivery_package   2  flour
 *   3  oud_string         4  tram_ticket        5  harira
 *   6  baklava            7  samen_flyer        8  permit_doc
 *   9  friet             10  reuzenpoort_key   11  mint_tea
 *  12  smoske
 */

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

const ITEM_NAME: Record<string, string> = {
  fabric_bolt:      'Stof',
  delivery_package: 'Pakjes',
  flour:            'Bloem',
  oud_string:       'Snaar',
  tram_ticket:      'Ticket',
  harira:           'Harira',
  baklava:          'Baklava',
  samen_flyer:      'Flyer',
  permit_doc:       'Vergunning',
  friet:            'Friet',
  reuzenpoort_key:  'Sleutel',
  mint_tea:         'Thee',
  smoske:           'Smoske',
};

// Layout constants (all in Phaser/game units)
const PANEL_X    =  1;
const PANEL_Y    = 38;   // just below the HUD panel (4+28+6)
const PANEL_W    = 22;
const ICON_SIZE  = 14;   // icon display size (14×14 game-px)
const SLOT_H     = 18;   // height per slot (icon + 4px gap)
const MAX_SLOTS  = 8;
const DEPTH_BASE = 110;

interface Slot {
  bg:    Phaser.GameObjects.Rectangle;
  icon:  Phaser.GameObjects.Image;
  badge: Phaser.GameObjects.Text;
  label: Phaser.GameObjects.Text;
  itemId: string;
}

export class ItemBar {
  private scene:   Phaser.Scene;
  private panel!:  Phaser.GameObjects.Rectangle;
  private header!: Phaser.GameObjects.Text;
  private slots:   Slot[] = [];
  private prevIds: string = '';   // serialised snapshot for change detection

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.buildPool();
  }

  // ── Build ──────────────────────────────────────────────────────────────────

  private buildPool(): void {
    // Backing panel — height grows dynamically, starts hidden
    this.panel = this.scene.add.rectangle(
      PANEL_X, PANEL_Y,
      PANEL_W, 4,
      0x0A0A12, 0.80,
    ).setOrigin(0, 0).setScrollFactor(0).setDepth(DEPTH_BASE).setVisible(false);

    // "ITEMS" header label
    this.header = this.scene.add.text(
      PANEL_X + 3, PANEL_Y + 2, 'ITEMS',
      { fontFamily: '"Press Start 2P"', fontSize: '3px', color: '#FFD700' },
    ).setScrollFactor(0).setDepth(DEPTH_BASE + 1).setVisible(false);

    // Pre-build MAX_SLOTS slots (hidden until needed)
    for (let i = 0; i < MAX_SLOTS; i++) {
      const y = PANEL_Y + 8 + i * SLOT_H;

      const bg = this.scene.add.rectangle(
        PANEL_X + 2, y, ICON_SIZE + 2, ICON_SIZE + 2, 0x1A1A2E,
      ).setOrigin(0, 0).setScrollFactor(0).setDepth(DEPTH_BASE + 1).setVisible(false);

      const icon = this.scene.add.image(
        PANEL_X + 3, y + 1, 'items_sheet', 0,
      ).setOrigin(0, 0).setScrollFactor(0).setDepth(DEPTH_BASE + 2)
        .setDisplaySize(ICON_SIZE, ICON_SIZE).setVisible(false);

      const badge = this.scene.add.text(
        PANEL_X + 2 + ICON_SIZE - 2, y, '1',
        { fontFamily: '"Press Start 2P"', fontSize: '3px', color: '#0A0A12',
          backgroundColor: '#FFD700', padding: { x: 1, y: 0 } },
      ).setOrigin(1, 0).setScrollFactor(0).setDepth(DEPTH_BASE + 3).setVisible(false);

      const label = this.scene.add.text(
        PANEL_X + 3, y + ICON_SIZE + 1, '',
        { fontFamily: '"Press Start 2P"', fontSize: '3px', color: '#888888' },
      ).setScrollFactor(0).setDepth(DEPTH_BASE + 2).setVisible(false);

      this.slots.push({ bg, icon, badge, label, itemId: '' });
    }
  }

  // ── Public ─────────────────────────────────────────────────────────────────

  /**
   * Call every frame from OverworldScene.update().
   * Only redraws when inventory actually changed.
   */
  update(): void {
    const inv   = stateManager.get().player.inventory;
    const idKey = inv.join(',');
    if (idKey === this.prevIds) return;

    const wasEmpty = this.prevIds === '';
    const oldIds   = this.prevIds ? this.prevIds.split(',') : [];
    this.prevIds   = idKey;

    // Count occurrences per item ID
    const counts: Record<string, number> = {};
    for (const id of inv) counts[id] = (counts[id] ?? 0) + 1;

    // Unique ordered list (preserve first-seen order)
    const unique: string[] = [];
    for (const id of inv) {
      if (!unique.includes(id)) unique.push(id);
    }

    const n = Math.min(unique.length, MAX_SLOTS);

    // Detect newly added items (for flash)
    const newlyAdded = unique.filter(id => !oldIds.includes(id));

    // Resize panel
    const panelH = n > 0 ? 8 + n * SLOT_H + 2 : 0;
    this.panel.setSize(PANEL_W, panelH).setVisible(n > 0);
    this.header.setVisible(n > 0);

    // Update slots
    for (let i = 0; i < MAX_SLOTS; i++) {
      const slot = this.slots[i];
      if (i < n) {
        const id    = unique[i];
        const count = counts[id];
        const frame = ITEM_FRAME[id] ?? 0;
        const name  = ITEM_NAME[id] ?? id;

        slot.itemId = id;
        slot.icon.setFrame(frame).setVisible(true);
        slot.bg.setVisible(true);

        // Count badge — only show when qty > 1
        if (count > 1) {
          slot.badge.setText(String(count)).setVisible(true);
        } else {
          slot.badge.setVisible(false);
        }

        // Short name label below icon
        slot.label.setText(name).setVisible(true);

        // Flash animation for newly received items
        if (!wasEmpty && newlyAdded.includes(id)) {
          this.flashSlot(slot);
        }
      } else {
        slot.icon.setVisible(false);
        slot.bg.setVisible(false);
        slot.badge.setVisible(false);
        slot.label.setVisible(false);
        slot.itemId = '';
      }
    }
  }

  // ── Private ────────────────────────────────────────────────────────────────

  private flashSlot(slot: Slot): void {
    // Gold border flash, then fade back
    slot.bg.setStrokeStyle(1, 0xFFD700, 1);
    this.scene.tweens.add({
      targets:  slot.bg,
      alpha:    { from: 0.3, to: 1 },
      duration: 120,
      yoyo:     true,
      repeat:   3,
      onComplete: () => {
        slot.bg.setStrokeStyle(0);
        slot.bg.setAlpha(1);
      },
    });

    // Icon bounce up
    const origY = slot.icon.y;
    this.scene.tweens.add({
      targets:  slot.icon,
      y:        origY - 3,
      duration: 80,
      yoyo:     true,
      repeat:   2,
      onComplete: () => slot.icon.setY(origY),
    });
  }
}
