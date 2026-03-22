import { stateManager } from '@core/StateManager';

/**
 * ItemBar — delegates inventory rendering to the HTML layer via window.__setInventory.
 *
 * The HTML panel in index.html renders item icons using the items_sheet.png
 * sprite, giving sharper rendering than the Phaser canvas.
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

export interface InventoryItem {
  id:    string;
  name:  string;
  frame: number;
  count: number;
}

export class ItemBar {
  private prevIds = '';

  // Exposed for the HTML layer's flash animation trigger
  private newlyAdded: string[] = [];

  /**
   * Call every frame from OverworldScene.update().
   * Only updates when inventory actually changed.
   */
  update(): void {
    const inv   = stateManager.get().player.inventory;
    const idKey = inv.join(',');
    if (idKey === this.prevIds) return;

    const oldIds    = this.prevIds ? this.prevIds.split(',') : [];
    this.prevIds    = idKey;
    this.newlyAdded = [];

    const counts: Record<string, number> = {};
    for (const id of inv) counts[id] = (counts[id] ?? 0) + 1;

    const unique: string[] = [];
    for (const id of inv) {
      if (!unique.includes(id)) unique.push(id);
    }

    const items: InventoryItem[] = unique.map(id => ({
      id,
      name:  ITEM_NAME[id] ?? id,
      frame: ITEM_FRAME[id] ?? 0,
      count: counts[id],
    }));

    // Track newly added for flash
    this.newlyAdded = unique.filter(id => !oldIds.includes(id));

    // Push to HTML layer
    const setInv = (window as unknown as Record<string, unknown>).__setInventory as ((items: InventoryItem[], flash: string[]) => void) | undefined;
    setInv?.(items, this.newlyAdded);
  }
}
