import { stateManager } from '@core/StateManager';
import itemData from '@data/items.json';

export interface ItemDefinition {
  id:          string;
  name:        string;
  description: string;
  type:        'consumable' | 'key' | 'weapon' | 'misc';
  effect?:     { stat: string; amount: number };
  value:       number; // coin value
  stackable:   boolean;
}

const ITEMS = itemData as Record<string, ItemDefinition>;

export class InventorySystem {
  /**
   * Use an item from the player's inventory.
   * Returns the message to display, or null if item not found.
   */
  static use(itemId: string): string | null {
    const def = ITEMS[itemId];
    if (!def || !def.effect) return null;

    const removed = stateManager.removeItem(itemId);
    if (!removed) return null;

    const { stat, amount } = def.effect;
    if (stat === 'hp') {
      const player = stateManager.get().player;
      const newHp  = Math.min(player.maxHp, player.hp + amount);
      stateManager.setHP(newHp);
      return `${def.name} geeft +${newHp - player.hp} HP terug.`;
    }

    return `${def.name} gebruikt.`;
  }

  static getDefinition(itemId: string): ItemDefinition | undefined {
    return ITEMS[itemId];
  }

  static playerItems(): ItemDefinition[] {
    return stateManager.get().player.inventory
      .map(id => ITEMS[id])
      .filter(Boolean);
  }
}
