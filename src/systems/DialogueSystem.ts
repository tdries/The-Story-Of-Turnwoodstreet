import { InputHandler }  from '@core/InputHandler';
import { stateManager }  from '@core/StateManager';
import { gameEventLogger } from '@core/GameEventLogger';
import { QuestSystem }   from '@systems/QuestSystem';
import { DialogueBox }   from '@ui/DialogueBox';
import { localeManager } from '@i18n/LocaleManager';
import dialogueData from '@data/dialogue.json';

// ── Types ──────────────────────────────────────────────────────────────────

export interface DialogueLine {
  speaker:     string;
  text?:       string;
  flag?:       string;
  flagVal?:    boolean | string | number;
  flag2?:      string;
  flagVal2?:   boolean | string | number;
  item?:       string;          // add this item to inventory when line is shown
  removeItem?: string;          // remove this item from inventory when line is shown
  coins?:      number;          // add/subtract coins when line is shown
  choice?:     DialogueChoice[];
}

export interface DialogueChoice {
  label:    string;
  next?:    string;             // jump to another dialogue node
  flag?:    string;
  flagVal?: boolean | string | number;
  item?:    string;
  coins?:   number;
}

/** Conditions that must ALL pass for a node to be routed to via an NPC. */
export interface DialogueConditions {
  flags?:    Record<string, boolean | string | number>;  // each flag must === value
  items?:    string[];    // player must carry ALL of these
  notItems?: string[];    // player must NOT carry ANY of these
}

/** A self-describing dialogue node: declares which NPC it belongs to,
 *  what conditions activate it, and what lines it contains.
 *  Nodes with no `npc` field are jump-target-only (choice.next / direct open()). */
export interface DialogueNode {
  npc?:       string;               // NPC id (absent = non-routable, zone/gate/battle)
  priority:   number;               // higher = evaluated first; 0 = fallback
  conditions: DialogueConditions;
  lines:      DialogueLine[];
}

export type DialogueData = Record<string, DialogueNode>;

export const DIALOGUES = dialogueData as DialogueData;

/**
 * DialogueSystem — drives branching dialogue nodes.
 *
 * Supports:
 *   - Linear sequences of lines (advance with action key)
 *   - Per-line flag setting, item grants/removals, coin changes
 *   - Choice branches: up to 4 options, navigate with up/down, confirm with action
 *   - Jumps to other nodes via choice.next
 *   - QuestSystem.checkAll() called after every node completion
 */
export class DialogueSystem {
  private box:           DialogueBox;
  private lines:         DialogueLine[] = [];
  private lineIdx        = 0;
  private _isOpen        = false;
  private _isRaw         = false;  // true when opened via openRaw — skip quest/save on close
  private pendingChoices: DialogueChoice[] | null = null;
  private dialogueId     = '';   // tracks current node for locale lookups
  private _pendingItem:  { itemId: string; speaker: string } | null = null;

  onClose:        (() => void) | null = null;
  /** If set, item grants are deferred: handler shows the item-receive animation,
   *  then calls done() which adds the item and continues the dialogue. */
  onItemReceived: ((itemId: string, speaker: string, done: () => void) => void) | null = null;

  constructor(box: DialogueBox) {
    this.box = box;
  }

  get isOpen(): boolean { return this._isOpen; }

  // ── Public ─────────────────────────────────────────────────────────────────

  open(dialogueId: string): void {
    const node = DIALOGUES[dialogueId];
    if (!node || node.lines.length === 0) return;

    gameEventLogger.logDialogue(dialogueId);
    this.dialogueId     = dialogueId;
    this.lines          = node.lines;
    this.lineIdx        = 0;
    this._isOpen        = true;
    this._isRaw         = false;
    this.pendingChoices = null;
    this.showLine();
  }

  /** Show arbitrary text via the dialogue UI without triggering quest checks or auto-save. */
  openRaw(speaker: string, ...lines: string[]): void {
    this.dialogueId     = '';
    this.lines          = lines.map(text => ({ speaker, text }));
    this.lineIdx        = 0;
    this._isOpen        = true;
    this._isRaw         = true;
    this.pendingChoices = null;
    this.showLine();
  }

  update(input: InputHandler): void {
    if (!this._isOpen) return;

    if (this.box.inChoiceMode) {
      if (input.upJustPressed)    this.box.moveCursor(-1);
      if (input.downJustPressed)  this.box.moveCursor(1);
      if (input.actionJustPressed) this.confirmChoice();
      return;
    }

    if (input.actionJustPressed) {
      if (this.box.isTyping) {
        this.box.skipType();
        return;
      }
      this.advance();
    }

    if (input.cancelJustPressed) this.close();
  }

  // ── Private ────────────────────────────────────────────────────────────────

  private showLine(): void {
    const line = this.lines[this.lineIdx];
    if (!line) { this.close(); return; }

    this.applyLineEffects(line);

    const displayText = localeManager.dialogueText(this.dialogueId, this.lineIdx) ?? line.text;

    if (line.choice && line.choice.length > 0) {
      if (displayText) {
        this.box.show(line.speaker, displayText);
        this.pendingChoices = line.choice;
      } else {
        this.presentChoices(line.choice);
      }
    } else if (displayText) {
      this.box.show(line.speaker, displayText);
      this.pendingChoices = null;
    } else {
      this.advance();
    }
  }

  private advance(): void {
    if (this.pendingChoices) {
      this.presentChoices(this.pendingChoices);
      return;
    }

    // Item-receive animation: pause dialogue until player dismisses the overlay
    if (this._pendingItem) {
      const pi = this._pendingItem;
      this._pendingItem = null;
      this._isOpen = false;
      this.onItemReceived!(pi.itemId, pi.speaker, () => {
        stateManager.addItem(pi.itemId);
        this._isOpen = true;
        this.lineIdx++;
        if (this.lineIdx >= this.lines.length) {
          this.close();
        } else {
          this.showLine();
        }
      });
      return;
    }

    this.lineIdx++;
    if (this.lineIdx >= this.lines.length) {
      this.close();
    } else {
      this.showLine();
    }
  }

  private presentChoices(choices: DialogueChoice[]): void {
    this.pendingChoices = null;
    const translatedLabels = localeManager.dialogueChoices(this.dialogueId, this.lineIdx);
    const labels = choices.map((c, i) => translatedLabels?.[i] ?? c.label);
    this.box.showChoices(labels);
  }

  private confirmChoice(): void {
    const line = this.lines[this.lineIdx];
    const choices = line?.choice ?? [];
    if (choices.length === 0) { this.advance(); return; }

    const selected = choices[this.box.selectedChoice];
    if (!selected) { this.advance(); return; }

    if (selected.flag !== undefined && selected.flagVal !== undefined) {
      stateManager.setFlag(selected.flag, selected.flagVal);
    }
    if (selected.item)  stateManager.addItem(selected.item);
    if (selected.coins) stateManager.addCoins(selected.coins);

    if (selected.next) {
      this.open(selected.next);
    } else {
      this.lineIdx++;
      if (this.lineIdx >= this.lines.length) {
        this.close();
      } else {
        this.showLine();
      }
    }
  }

  private applyLineEffects(line: DialogueLine): void {
    if (line.flag       !== undefined && line.flagVal  !== undefined) stateManager.setFlag(line.flag,  line.flagVal);
    if (line.flag2      !== undefined && line.flagVal2 !== undefined) stateManager.setFlag(line.flag2, line.flagVal2);
    if (line.removeItem) stateManager.removeItem(line.removeItem);
    if (line.coins)      stateManager.addCoins(line.coins);
    if (line.item) {
      if (this.onItemReceived) {
        // Defer: show animation before adding to inventory
        this._pendingItem = { itemId: line.item, speaker: line.speaker ?? '' };
      } else {
        stateManager.addItem(line.item);
      }
    }
  }

  private close(): void {
    this._isOpen        = false;
    this.pendingChoices = null;
    this.box.hide();
    if (!this._isRaw) {
      QuestSystem.checkAll();
      stateManager.save();
    }
    this._isRaw = false;
    this.onClose?.();
  }
}
