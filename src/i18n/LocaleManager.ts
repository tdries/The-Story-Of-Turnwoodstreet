import { UI } from './ui';
import { DIALOGUE_LOCALES } from './dialogueLocales';
import { ITEM_LOCALES }     from './itemLocales';
import { QUEST_LOCALES }    from './questLocales';

export type Locale = 'nl' | 'en' | 'fr' | 'ar';

export const LOCALES:      Locale[]               = ['nl', 'en', 'fr', 'ar'];
export const LOCALE_NAMES: Record<Locale, string> = { nl: 'NL', en: 'EN', fr: 'FR', ar: 'AR' };
export const LOCALE_LABELS: Record<Locale, string> = {
  nl: '🇧🇪 NL', en: '🇬🇧 EN', fr: '🇫🇷 FR', ar: '🇲🇦 AR',
};

const STORAGE_KEY = 'game_locale';

class LocaleManager {
  private _locale: Locale = 'nl';

  constructor() {
    if (typeof localStorage !== 'undefined') {
      const saved = localStorage.getItem(STORAGE_KEY) as Locale | null;
      if (saved && (LOCALES as string[]).includes(saved)) this._locale = saved;
    }
  }

  get locale(): Locale { return this._locale; }

  /** True for right-to-left script (Arabic). */
  get isRTL(): boolean { return this._locale === 'ar'; }

  /**
   * Font family to use for Phaser text.
   * Arabic requires a system font; other locales use the pixel-art font.
   */
  get gameFont(): string {
    return this._locale === 'ar'
      ? '"Segoe UI", "Arial", "Helvetica Neue", Arial, sans-serif'
      : '"Press Start 2P"';
  }

  setLocale(locale: Locale): void {
    this._locale = locale;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, locale);
    }
  }

  // ── UI strings ──────────────────────────────────────────────────────────────

  /** Translate a UI key. Falls back to NL, then to the key itself. */
  t(key: string): string {
    return UI[this._locale]?.[key] ?? UI.nl[key] ?? key;
  }

  // ── Dialogue ────────────────────────────────────────────────────────────────

  /**
   * Returns the translated text for a dialogue step, or null if NL should be
   * used (either because the locale is NL or no translation exists).
   */
  dialogueText(dialogueId: string, stepIndex: number): string | null {
    if (this._locale === 'nl') return null;
    return DIALOGUE_LOCALES[this._locale]?.[dialogueId]?.[stepIndex]?.text ?? null;
  }

  /**
   * Returns translated choice labels for a dialogue step, or null if NL should
   * be used.  The array is 1-to-1 with the choices array in dialogue.json.
   */
  dialogueChoices(dialogueId: string, stepIndex: number): string[] | null {
    if (this._locale === 'nl') return null;
    return DIALOGUE_LOCALES[this._locale]?.[dialogueId]?.[stepIndex]?.choices ?? null;
  }

  // ── Items ───────────────────────────────────────────────────────────────────

  /** Translated item name, or null to use the NL original from items.json. */
  itemName(itemId: string): string | null {
    if (this._locale === 'nl') return null;
    return ITEM_LOCALES[this._locale]?.[itemId]?.name ?? null;
  }

  /** Translated item description, or null to use the NL original. */
  itemDescription(itemId: string): string | null {
    if (this._locale === 'nl') return null;
    return ITEM_LOCALES[this._locale]?.[itemId]?.description ?? null;
  }

  // ── Quests ──────────────────────────────────────────────────────────────────

  /** Translated quest title, or null to use the NL original from quests.json. */
  questTitle(questId: string): string | null {
    if (this._locale === 'nl') return null;
    return QUEST_LOCALES[this._locale]?.[questId]?.title ?? null;
  }

  /** Translated quest description, or null to use the NL original. */
  questDescription(questId: string): string | null {
    if (this._locale === 'nl') return null;
    return QUEST_LOCALES[this._locale]?.[questId]?.description ?? null;
  }

  /** Translated objective description, or null to use the NL original. */
  questObjective(questId: string, objectiveId: string): string | null {
    if (this._locale === 'nl') return null;
    return QUEST_LOCALES[this._locale]?.[questId]?.objectives?.[objectiveId] ?? null;
  }
}

export const localeManager = new LocaleManager();
