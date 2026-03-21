/**
 * Global game state — quest flags, inventory, player stats.
 * Lives outside Phaser scenes so it survives scene transitions.
 */
export interface PlayerState {
  name:   string;
  hp:     number;
  maxHp:  number;
  coins:  number;
  level:  number;
  xp:     number;
  xpNext: number;
  skills: string[];       // skill IDs unlocked
  inventory: string[];    // item IDs
}

export interface QuestFlags {
  [key: string]: boolean | number | string;
}

export interface GameState {
  player:      PlayerState;
  questFlags:  QuestFlags;
  currentMap:  string;
  spawnPoint:  { x: number; y: number };
  playtimeMs:  number;
}

const DEFAULT_STATE: GameState = {
  player: {
    name:      'Speler',
    hp:        20,
    maxHp:     20,
    coins:     5,
    level:     1,
    xp:        0,
    xpNext:    100,
    skills:    [],
    inventory: [],
  },
  questFlags:  {},
  currentMap:  'borgerhout_main',
  spawnPoint:  { x: 64, y: 146 },   // front sidewalk band (H*0.52 ≈ 141, walkable to ~156)
  playtimeMs:  0,
};

class StateManager {
  private state: GameState;

  constructor() {
    this.state = this.load() ?? structuredClone(DEFAULT_STATE);
  }

  get(): GameState {
    return this.state;
  }

  setFlag(key: string, value: boolean | number | string): void {
    this.state.questFlags[key] = value;
  }

  getFlag(key: string): boolean | number | string | undefined {
    return this.state.questFlags[key];
  }

  addCoins(amount: number): void {
    this.state.player.coins = Math.max(0, this.state.player.coins + amount);
  }

  addItem(itemId: string): void {
    this.state.player.inventory.push(itemId);
  }

  removeItem(itemId: string): boolean {
    const idx = this.state.player.inventory.indexOf(itemId);
    if (idx === -1) return false;
    this.state.player.inventory.splice(idx, 1);
    return true;
  }

  hasItem(itemId: string): boolean {
    return this.state.player.inventory.includes(itemId);
  }

  gainXP(amount: number): boolean {
    this.state.player.xp += amount;
    if (this.state.player.xp >= this.state.player.xpNext) {
      this.levelUp();
      return true;
    }
    return false;
  }

  private levelUp(): void {
    const p = this.state.player;
    p.level  += 1;
    p.xp      = p.xp - p.xpNext;
    p.xpNext  = Math.floor(p.xpNext * 1.5);
    p.maxHp  += 5;
    p.hp      = p.maxHp;
  }

  save(): void {
    try {
      localStorage.setItem('tbaan_save', JSON.stringify(this.state));
    } catch { /* storage full or unavailable */ }
  }

  private load(): GameState | null {
    try {
      const raw = localStorage.getItem('tbaan_save');
      return raw ? (JSON.parse(raw) as GameState) : null;
    } catch {
      return null;
    }
  }

  hasSave(): boolean {
    try {
      return localStorage.getItem('tbaan_save') !== null;
    } catch {
      return false;
    }
  }

  reset(): void {
    this.state = structuredClone(DEFAULT_STATE);
    localStorage.removeItem('tbaan_save');
  }
}

/** Singleton — import and use anywhere. */
export const stateManager = new StateManager();
