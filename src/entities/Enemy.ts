/**
 * Enemy — data container for battle enemies.
 * Overworld enemies are NPCs that trigger BattleScene on interaction.
 * This class holds the stat block used by CombatSystem.
 */
export interface EnemyStat {
  id:     string;
  name:   string;
  hp:     number;
  maxHp:  number;
  atk:    number;
  def:    number;
  spd:    number;
  xp:     number;
  coins:  number;
  loot?:  string[];   // item IDs
  taunt?: string[];   // combat taunts
}

export class Enemy {
  readonly stats: EnemyStat;
  currentHp: number;

  constructor(stats: EnemyStat) {
    this.stats     = stats;
    this.currentHp = stats.hp;
  }

  get isAlive(): boolean {
    return this.currentHp > 0;
  }

  takeDamage(amount: number): number {
    const effective = Math.max(1, amount - this.stats.def);
    this.currentHp  = Math.max(0, this.currentHp - effective);
    return effective;
  }

  get randomTaunt(): string {
    const taunts = this.stats.taunt ?? ['…'];
    return taunts[Math.floor(Math.random() * taunts.length)];
  }
}
