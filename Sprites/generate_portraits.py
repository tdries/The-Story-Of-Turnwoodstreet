#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — NPC Portrait Sprites
==========================================
Generates 2-frame portrait sprite sheets for all 10 story NPCs.

  Frame 0: neutral  (mouth closed)
  Frame 1: talking  (mouth open — overlaid after full-body draw)

Canvas: 128×64 game-px  (2 × 64×64 per character)
Body below y=64 is naturally cropped → head + shoulders only.
Output PNG at out_scale=2: 256×128 px per character.
Phaser load: frameWidth=128, frameHeight=128.
"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from generate_sprites import SVGSheet
from generate_npcs import (
    draw_fatima, draw_omar, draw_baert, draw_reza, draw_el_osri,
    draw_yusuf, draw_aziz, draw_sofia, draw_hamza, draw_tine,
)

OUT_SCALE  = 2
FW, FH     = 64, 64          # portrait frame size (body below y=64 cropped)
NUM_FRAMES = 2               # 0 = idle/neutral, 1 = talking/mouth-open
OUT_DIR    = os.path.join(
    os.path.dirname(__file__), "..", "assets", "Sprites", "characters", "npcs", "portraits"
)


# ── background fill ───────────────────────────────────────────────────────────

def fill_bg(s: SVGSheet, ox: int) -> None:
    """Dark portrait background for one frame."""
    s.put(ox, 0, "night", FW, FH)


# ── open-mouth overlay ────────────────────────────────────────────────────────

def add_open_mouth(s: SVGSheet, ox: int, mouth_y: int = 22) -> None:
    """Overwrite the closed mouth with a small dark talking gap."""
    s.put(ox + 26, mouth_y,     "stone_dark", 6, 1)   # upper-lip pulled back
    s.put(ox + 27, mouth_y + 1, "night",      4, 1)   # dark oral cavity
    s.put(ox + 26, mouth_y + 2, "stone_dark", 6, 1)   # lower lip in shadow


# ── per-NPC config ────────────────────────────────────────────────────────────
#   (npc_id, draw_fn, mouth_y, skip_mouth_overlay)
#   mouth_y: row of the closed mouth line inside the 64px canvas
#   skip_mouth_overlay: True when mouth is hidden (beard, etc.)

NPCS = [
    ("fatima",  draw_fatima,  22, False),   # hijab head — mouth at oy+22
    ("omar",    draw_omar,    22, False),   # bare head
    ("baert",   draw_baert,   22, False),   # bare head (older)
    ("reza",    draw_reza,    22, False),   # bare head + waistcoat
    ("el_osri", draw_el_osri, 22, False),   # hijab head — green blazer
    ("yusuf",   draw_yusuf,   23, False),   # cap/helmet head — mouth at oy+23
    ("aziz",    draw_aziz,    22, True),    # white beard covers mouth
    ("sofia",   draw_sofia,   22, False),   # bare head
    ("hamza",   draw_hamza,   22, False),   # bare head — teen
    ("tine",    draw_tine,    22, False),   # bare head — teal tunic
]


# ── generator ─────────────────────────────────────────────────────────────────

def generate_portrait(npc_id: str, draw_fn, mouth_y: int, skip_mouth: bool) -> None:
    label  = f"{npc_id} portrait (2-frame)"
    sheet  = SVGSheet(FW * NUM_FRAMES, FH, label)

    # ── frame 0: neutral ─────────────────────────────────────────────────────
    fill_bg(sheet, 0)
    draw_fn(sheet, 0, 0, frame=0)

    # ── frame 1: talking ─────────────────────────────────────────────────────
    fill_bg(sheet, FW)
    draw_fn(sheet, FW, 0, frame=0)
    if not skip_mouth:
        add_open_mouth(sheet, FW, mouth_y)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{npc_id}_portrait.png")
    sheet.to_pil(out_path, out_scale=OUT_SCALE)


def main() -> None:
    print("=" * 60)
    print("Turnhoutsebaan NPC Portrait Generator")
    print(f"  Frame: {FW}×{FH} game-px  |  out_scale={OUT_SCALE}")
    print(f"  PNG per NPC: {FW*OUT_SCALE*NUM_FRAMES}×{FH*OUT_SCALE} px")
    print("=" * 60)
    for npc_id, draw_fn, mouth_y, skip_mouth in NPCS:
        print(f"\n● {npc_id}")
        generate_portrait(npc_id, draw_fn, mouth_y, skip_mouth)
    print(f"\n✓ All portraits → {OUT_DIR}")


if __name__ == "__main__":
    main()
