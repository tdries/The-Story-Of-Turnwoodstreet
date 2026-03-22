import { stateManager } from '@core/StateManager';
import questData from '@data/quests.json';

/**
 * QuestSystem — tracks quest state, checks objectives, fires rewards.
 *
 * Pure TypeScript — no Phaser imports.
 *
 * State is read via stateManager.getFlag(), which now queries the XState
 * GameMachine snapshot via the flagBridge. setFlag() translates known keys
 * into machine events automatically.
 *
 * Usage:
 *   QuestSystem.checkAll()          — call after every dialogue end / battle end
 *   QuestSystem.getActive()         — returns quests the player can work on
 *   QuestSystem.isComplete(id)      — check a single quest
 */

export interface QuestObjective {
  id:          string;
  description: string;
  checkFlag:   string;
  checkValue:  boolean | string | number;
  optional?:   boolean;
}

export interface QuestReward {
  flags:  Record<string, boolean | string | number>;
  items:  string[];
  coins:  number;
  xp:     number;
  skills: string[];
}

export interface QuestDef {
  id:             string;
  title:          string;
  description:    string;
  zone:           number;
  requiredFlags:  string[];
  objectives:     QuestObjective[];
  reward:         QuestReward;
  completionFlag: string;
}

const QUESTS = questData as Record<string, QuestDef>;

export class QuestSystem {

  // ── Queries ────────────────────────────────────────────────────────────────

  /**
   * Returns true if the quest's completion flag is set.
   * Reads from the XState machine via flagBridge.
   */
  static isComplete(questId: string): boolean {
    const q = QUESTS[questId];
    if (!q) return false;
    return stateManager.getFlag(q.completionFlag) === true;
  }

  /** Returns true if all required flags are set and the quest is not yet done. */
  static isActive(questId: string): boolean {
    if (QuestSystem.isComplete(questId)) return false;
    const q = QUESTS[questId];
    if (!q) return false;
    return q.requiredFlags.every(f => stateManager.getFlag(f) === true);
  }

  /** All quests currently accessible (requirements met, not yet complete). */
  static getActive(): QuestDef[] {
    return Object.values(QUESTS).filter(q => QuestSystem.isActive(q.id));
  }

  /** All quests that are complete. */
  static getCompleted(): QuestDef[] {
    return Object.values(QUESTS).filter(q => QuestSystem.isComplete(q.id));
  }

  /** Objectives completed so far for a quest. */
  static getProgress(questId: string): { done: number; total: number } {
    const q = QUESTS[questId];
    if (!q) return { done: 0, total: 0 };
    const done = q.objectives.filter(
      obj => stateManager.getFlag(obj.checkFlag) === obj.checkValue
    ).length;
    return { done, total: q.objectives.length };
  }

  /**
   * How many faction quests are complete (0–7).
   * Reads machine state via flagBridge for accuracy.
   */
  static getFactionCount(): number {
    return [
      'q_faction_moroccan_done',
      'q_faction_turkish_done',
      'q_faction_flemish_done',
      'q_faction_art_done',
      'q_faction_school_done',
      'q_faction_mosque_done',
      'q_faction_frituur_done',
    ].filter(f => stateManager.getFlag(f) === true).length;
  }

  // ── Core tick ──────────────────────────────────────────────────────────────

  /**
   * Check every active quest for completion.
   * Should be called after:
   *   - Any dialogue end (new flags may have been set / events sent to machine)
   *   - Any battle end
   *   - Any item pickup
   *
   * Returns list of newly completed quest IDs.
   */
  static checkAll(): string[] {
    const newlyDone: string[] = [];

    for (const q of Object.values(QUESTS)) {
      if (QuestSystem.isComplete(q.id)) continue;
      if (!QuestSystem.isActive(q.id)) continue;

      const allObjectivesMet = q.objectives.every(
        obj => stateManager.getFlag(obj.checkFlag) === obj.checkValue
      );

      if (allObjectivesMet) {
        QuestSystem._complete(q);
        newlyDone.push(q.id);
      }
    }

    // Keep samen_tafel_faction_N in sync (numeric flag for UI display)
    stateManager.setFlag('samen_tafel_faction_N', QuestSystem.getFactionCount());

    return newlyDone;
  }

  // ── Internals ──────────────────────────────────────────────────────────────

  private static _complete(q: QuestDef): void {
    // Apply flag rewards — setFlag() translates machine-known keys to events
    for (const [key, val] of Object.entries(q.reward.flags)) {
      stateManager.setFlag(key, val);
    }

    // Apply item rewards
    for (const itemId of q.reward.items) {
      stateManager.addItem(itemId);
    }

    // Apply coin reward
    if (q.reward.coins > 0) {
      stateManager.addCoins(q.reward.coins);
    }

    // Apply XP reward
    if (q.reward.xp > 0) {
      stateManager.gainXP(q.reward.xp);
    }

    // Apply skill unlocks
    for (const skillId of q.reward.skills) {
      stateManager.setFlag(`skill_unlocked_${skillId}`, true);
    }

    // Mark quest complete — completionFlag is in flagBridge so it also
    // updates machine state where applicable
    stateManager.setFlag(q.completionFlag, true);

    // Persist
    stateManager.save();
  }
}
