export type BattleResult = 'victory' | 'defeat' | 'ongoing';

export interface Combatant {
  id:    string;
  name:  string;
  hp:    number;
  maxHp: number;
  atk:   number;
  def:   number;
  spd:   number;
}

interface TurnResult {
  message: string;
  damage:  number;
}

/**
 * CombatSystem — pure turn-based logic, no Phaser dependency.
 * BattleScene owns the UI; this class owns the numbers.
 */
export class CombatSystem {
  private player: Combatant;
  private enemy:  Combatant;
  private _isOver  = false;
  private _outcome: BattleResult = 'ongoing';

  constructor(player: Combatant, enemy: Combatant) {
    this.player = { ...player };
    this.enemy  = { ...enemy  };
  }

  playerTurn(action: 'attack' | 'skill'): TurnResult {
    if (this._isOver) return { message: '', damage: 0 };

    let dmg: number;
    if (action === 'skill') {
      dmg = Math.max(1, this.player.atk * 2 - this.enemy.def);
    } else {
      dmg = Math.max(1, this.player.atk - this.enemy.def + between(-2, 2));
    }

    this.enemy.hp = Math.max(0, this.enemy.hp - dmg);
    const msg = action === 'skill'
      ? `${this.player.name} gebruikt een skill! ${dmg} schade!`
      : `${this.player.name} valt aan voor ${dmg} schade.`;

    if (this.enemy.hp <= 0) {
      this._isOver  = true;
      this._outcome = 'victory';
    }

    return { message: msg, damage: dmg };
  }

  enemyTurn(): TurnResult {
    if (this._isOver) return { message: '', damage: 0 };

    const dmg = Math.max(1, this.enemy.atk - this.player.def + between(-1, 1));
    this.player.hp = Math.max(0, this.player.hp - dmg);
    const msg = `${this.enemy.name} slaat terug voor ${dmg}!`;

    if (this.player.hp <= 0) {
      this._isOver  = true;
      this._outcome = 'defeat';
    }

    return { message: msg, damage: dmg };
  }

  get isOver():    boolean       { return this._isOver;  }
  get outcome():   BattleResult  { return this._outcome; }

  getState(): { player: Combatant; enemy: Combatant } {
    return { player: { ...this.player }, enemy: { ...this.enemy } };
  }
}

function between(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
