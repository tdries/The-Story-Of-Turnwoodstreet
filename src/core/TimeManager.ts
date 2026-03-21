/**
 * TimeManager — drives the in-game clock.
 *
 * Time scale: 1 real second = 1 game minute  →  1 real minute = 1 game hour.
 * A complete 24-hour game day takes 24 real minutes.
 * Day starts at 09:00.
 */
export class TimeManager {
  private _totalMin: number;

  constructor(startHour = 9) {
    this._totalMin = startHour * 60;
  }

  update(delta: number): void {
    this._totalMin = (this._totalMin + delta / 1000) % 1440;
  }

  // ── Accessors ──────────────────────────────────────────────────────────────

  get hours():          number { return Math.floor(this._totalMin / 60); }
  get minutes():        number { return Math.floor(this._totalMin % 60); }
  get fractionalHour(): number { return this._totalMin / 60; }

  get timeString(): string {
    return `${String(this.hours).padStart(2, '0')}:${String(this.minutes).padStart(2, '0')}`;
  }

  // ── Time-of-day flags ──────────────────────────────────────────────────────

  get isNight(): boolean {
    const h = this.hours; return h >= 21 || h < 6;
  }

  get isRushHour(): boolean {
    const h = this.hours;
    return (h >= 6 && h < 9) || (h >= 16 && h < 19);
  }

  /** Late-evening hours where smokers & drinkers gather on the pavement */
  get isNightlife(): boolean {
    const h = this.hours; return h >= 20 || h < 4;
  }

  // ── Density scalars (0 – 1) ────────────────────────────────────────────────

  /** How packed the street crowd should be */
  get crowdDensity(): number {
    const h = this.hours;
    if (h < 5)  return 0.05;   // deep night — nearly empty
    if (h < 6)  return 0.18;   // pre-dawn stragglers
    if (h < 9)  return 1.00;   // morning rush — max crowd
    if (h < 12) return 0.45;
    if (h < 14) return 0.55;   // lunch bump
    if (h < 16) return 0.38;   // afternoon lull
    if (h < 19) return 1.00;   // evening rush — max crowd
    if (h < 21) return 0.28;
    return 0.10;
  }

  /** How many vehicles should be active on the road */
  get trafficDensity(): number {
    const h = this.hours;
    if (h < 5)  return 0.15;
    if (h < 6)  return 0.35;
    if (h < 9)  return 1.00;
    if (h < 16) return 0.65;
    if (h < 19) return 1.00;
    if (h < 21) return 0.50;
    return 0.20;
  }
}
