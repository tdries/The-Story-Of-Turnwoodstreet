import { stateManager } from '@core/StateManager';
import { QuestSystem }  from '@systems/QuestSystem';

/**
 * GateSystem — determines whether the player may enter a given zone.
 *
 * Pure TypeScript — no Phaser imports.
 *
 * Zone layout (world pixel x-coordinates, WORLD_W = 2880):
 *   Zone 1:  x =    0 –  576   Borgerhout West   (nos.   1–110)  no gate
 *   Zone 2:  x =  576 – 1152   Borgerhout Central (nos. 110–200) gate: has_community_trust
 *   Zone 3:  x = 1152 – 1728   Borgerhout East    (nos. 200–300) gate: reza_quest_done
 *   Zone 4:  x = 1728 – 2304   Deurne             (nos. 300–400) gate: has_permit_doc
 *   Zone 5:  x = 2304 – 2880   The 2km Table      (nos. 400+)    gate: 7 factions
 *
 * Usage:
 *   const result = GateSystem.canEnter(2);
 *   if (!result.open) showHint(result.hint);
 */

export interface GateResult {
  open:  boolean;
  hint?: string;   // shown to player in DialogueBox when gate is closed
}

/** World x-coordinate where each zone begins. */
export const ZONE_STARTS: Record<number, number> = {
  1:  0,
  2:  576,
  3:  1152,
  4:  1728,
  5:  2304,
};

/** Returns the zone number (1–5) for a given world x-coordinate. */
export function zoneForX(x: number): number {
  if (x >= ZONE_STARTS[5]) return 5;
  if (x >= ZONE_STARTS[4]) return 4;
  if (x >= ZONE_STARTS[3]) return 3;
  if (x >= ZONE_STARTS[2]) return 2;
  return 1;
}

export class GateSystem {

  /**
   * Returns whether the player can enter the given zone.
   * Always returns open=true for zones <= the player's current zone
   * (backtracking is always allowed).
   */
  static canEnter(zone: number): GateResult {
    switch (zone) {
      case 1:
        return { open: true };

      case 2:
        if (stateManager.getFlag('has_community_trust') === true) {
          return { open: true };
        }
        return {
          open: false,
          hint: 'De poort blijft gesloten voor vreemden. Spreek eerst met Fatima aan het begin van de straat.',
        };

      case 3:
        if (stateManager.getFlag('reza_quest_done') === true) {
          return { open: true };
        }
        return {
          open: false,
          hint: "De deur van De Roma opent alleen voor wie de taal van de straat begrijpt. Zoek Reza's oud-snaar.",
        };

      case 4:
        if (stateManager.getFlag('has_permit_doc') === true) {
          return { open: true };
        }
        return {
          open: false,
          hint: 'De grenswachter vraagt naar uw papieren. Versla de Bulldozer-bureaucraat en draag zijn vergunning.',
        };

      case 5: {
        const count = QuestSystem.getFactionCount();
        if (count >= 7) {
          return { open: true };
        }
        const remaining = 7 - count;
        return {
          open: false,
          hint: `De Grote Tafel is nog niet klaar. Je hebt nog ${remaining} ${remaining === 1 ? 'factie' : 'facties'} nodig.`,
        };
      }

      default:
        return { open: false, hint: 'Dit gebied is niet toegankelijk.' };
    }
  }

  /**
   * Returns the gate result for crossing from the player's current x
   * toward a new x.  Only triggers when moving east across a zone boundary.
   * Returns null if no gate is being crossed.
   */
  static checkTransition(fromX: number, toX: number): GateResult | null {
    const fromZone = zoneForX(fromX);
    const toZone   = zoneForX(toX);

    if (toZone <= fromZone) return null;   // moving west or same zone — always allowed

    const result = GateSystem.canEnter(toZone);
    return result.open ? null : result;    // null = no block; GateResult = blocked
  }
}
