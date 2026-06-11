/**
 * Persistence regression — play to the geest, "refresh" (fresh module graph,
 * same localStorage), and verify all progress survives. Guards the
 * save -> localStorage -> restore cycle including reward/skill state and the
 * savedAt stamp used by the newer-wins cloud merge.
 */
import { describe, it, expect, vi } from 'vitest';

// Minimal localStorage shim shared across module reloads
const store = new Map<string, string>();
const localStorageShim = {
  getItem: (k: string) => (store.has(k) ? store.get(k)! : null),
  setItem: (k: string, v: string) => { store.set(k, String(v)); },
  removeItem: (k: string) => { store.delete(k); },
  clear: () => store.clear(),
};
vi.stubGlobal('localStorage', localStorageShim);

const PLAY_TO_GEEST = [
  'met_yusuf', 'delivery_accepted', 'delivered_137', 'delivered_170',
  'delivered_284', 'delivery_done',
  'met_fatima', 'fabric_quest_accepted', 'stunt_quest_active', 'stunt_quest_done',
  'oud_quest_accepted', 'has_oud_string_item', 'reza_quest_done',
  'flour_quest_accepted', 'has_flour', 'omar_flour_done',
  'sig_fatima', 'sig_omar', 'sig_reza', 'sig_baert', 'sig_aziz',
  'geest_encountered',
];

describe('refresh persistence round-trip', () => {
  it('progress written by save() survives a module reload (page refresh)', async () => {
    vi.resetModules();
    const { stateManager: sm1 } = await import('../src/core/StateManager');
    const { QuestSystem: qs1 } = await import('../src/systems/QuestSystem');

    for (const f of PLAY_TO_GEEST) sm1.setFlag(f, true);
    qs1.checkAll();           // grants rewards, calls save()
    sm1.save();               // explicit save like dialogue close

    const raw = localStorage.getItem('tbaan_save_v2');
    expect(raw, 'save blob must exist in localStorage').toBeTruthy();
    const blob = JSON.parse(raw!);
    expect(blob.machineSnapshot?.value?.geest).toBe('encountered');
    expect(blob.machineSnapshot?.value?.delivery).toBe('rewarded');
    expect(Date.parse(blob.savedAt), 'savedAt stamp must be a valid timestamp').toBeGreaterThan(0);

    // ── simulate refresh: fresh module graph, same localStorage ──
    vi.resetModules();
    const { stateManager: sm2 } = await import('../src/core/StateManager');

    const flags = sm2.getFlags();
    expect(flags.geest_encountered, 'geest progress must survive refresh').toBe(true);
    expect(flags.delivery_done, 'delivery progress must survive refresh').toBe(true);
    expect(flags.stunt_quest_done).toBe(true);
    expect(flags.speculator_threatened).toBe(true);
    expect(sm2.getSnapshot().context.skills).toContain('samen_aan_tafel');
    expect(sm2.hasSave()).toBe(true);
  });
});
