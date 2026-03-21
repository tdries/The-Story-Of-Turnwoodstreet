import { InputHandler }  from '@core/InputHandler';
import { stateManager }  from '@core/StateManager';
import { QuestSystem }   from '@systems/QuestSystem';
import { DialogueBox }   from '@ui/DialogueBox';
import { localeManager } from '@i18n/LocaleManager';
import dialogueData from '@data/dialogue.json';

interface DialogueLine {
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

interface DialogueChoice {
  label:    string;
  next?:    string;           // jump to another dialogue tree
  flag?:    string;
  flagVal?: boolean | string | number;
  item?:    string;
  coins?:   number;
}

type DialogueTree = DialogueLine[];
const DIALOGUES = dialogueData as Record<string, DialogueTree>;

/**
 * DialogueSystem — drives branching dialogue trees.
 *
 * Supports:
 *   - Linear sequences of lines (advance with action key)
 *   - Per-line flag setting, item grants, coin changes
 *   - Choice branches: up to 4 options, navigate with up/down, confirm with action
 *   - Jumps to other dialogue trees via choice.next
 *   - QuestSystem.checkAll() called after every tree completion
 */
export class DialogueSystem {
  private box:          DialogueBox;
  private lines:        DialogueLine[] = [];
  private lineIdx       = 0;
  private _isOpen       = false;
  private pendingChoices: DialogueChoice[] | null = null;
  private dialogueId    = '';   // tracks current tree for locale lookups

  onClose: (() => void) | null = null;

  constructor(box: DialogueBox) {
    this.box = box;
  }

  get isOpen(): boolean { return this._isOpen; }

  // ── Public ─────────────────────────────────────────────────────────────────

  open(dialogueId: string): void {
    const tree = DIALOGUES[dialogueId];
    if (!tree || tree.length === 0) return;

    this.dialogueId       = dialogueId;
    this.lines            = tree;
    this.lineIdx          = 0;
    this._isOpen          = true;
    this.pendingChoices   = null;
    this.showLine();
  }

  update(input: InputHandler): void {
    if (!this._isOpen) return;

    if (this.box.inChoiceMode) {
      // Choice navigation
      if (input.upJustPressed)   this.box.moveCursor(-1);
      if (input.downJustPressed) this.box.moveCursor(1);
      if (input.actionJustPressed) this.confirmChoice();
      return;
    }

    if (input.actionJustPressed) {
      if (this.box.isTyping) {
        this.box.skipType();   // reveal full text instantly, wait for next press to advance
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

    // Apply side effects of showing this line
    this.applyLineEffects(line);

    // Resolve translated text (falls back to NL original when locale is nl
    // or when no translation exists for this entry)
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
    // Reconstruct which choices were being presented
    // They were already shown; find the current line's choices or a stored ref
    const line = this.lines[this.lineIdx];
    const choices = line?.choice ?? [];
    if (choices.length === 0) { this.advance(); return; }

    const selected = choices[this.box.selectedChoice];
    if (!selected) { this.advance(); return; }

    // Apply choice effects
    if (selected.flag !== undefined && selected.flagVal !== undefined) {
      stateManager.setFlag(selected.flag, selected.flagVal);
    }
    if (selected.item) stateManager.addItem(selected.item);
    if (selected.coins) stateManager.addCoins(selected.coins);

    // Jump to another tree or continue
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
    if (line.item)       stateManager.addItem(line.item);
    if (line.removeItem) stateManager.removeItem(line.removeItem);
    if (line.coins)      stateManager.addCoins(line.coins);
  }

  private close(): void {
    this._isOpen      = false;
    this.pendingChoices = null;
    this.box.hide();
    QuestSystem.checkAll();  // check for newly-completed quests after every dialogue
    this.onClose?.();
  }
}
