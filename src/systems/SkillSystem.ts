import { stateManager } from '@core/StateManager';
import skillData from '@data/skills.json';

export interface SkillDefinition {
  id:          string;
  name:        string;
  description: string;
  cost:        number;         // XP cost to learn
  mpCost:      number;         // MP cost to use (future)
  effect:      string;         // 'damage_2x' | 'heal_self' | 'stun' | etc.
  unlockFlag?: string;         // quest flag that must be set to unlock
}

const SKILLS = skillData as Record<string, SkillDefinition>;

/**
 * SkillSystem — manages which skills the player can learn and use.
 */
export class SkillSystem {
  /** Returns all skills the player has unlocked. */
  static playerSkills(): SkillDefinition[] {
    return stateManager.get().player.skills
      .map(id => SKILLS[id])
      .filter(Boolean);
  }

  /** Try to learn a skill. Returns success message or reason for failure. */
  static learn(skillId: string): string {
    const def = SKILLS[skillId];
    if (!def) return 'Onbekende skill.';

    const state = stateManager.get();
    if (state.player.skills.includes(skillId)) return `${def.name} al geleerd.`;
    if (def.unlockFlag && !stateManager.getFlag(def.unlockFlag)) return 'Nog niet ontgrendeld.';
    if (state.player.xp < def.cost) return `Niet genoeg XP. Nodig: ${def.cost}.`;

    state.player.xp -= def.cost;
    state.player.skills.push(skillId);
    return `${def.name} geleerd!`;
  }

  static getDefinition(skillId: string): SkillDefinition | undefined {
    return SKILLS[skillId];
  }

  /** Check if the player has a skill. */
  static has(skillId: string): boolean {
    return stateManager.get().player.skills.includes(skillId);
  }
}
