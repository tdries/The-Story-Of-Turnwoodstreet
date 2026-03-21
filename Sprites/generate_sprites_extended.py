#!/usr/bin/env python3
"""
Turnhoutsebaan RPG — Extended Sprite Generator
================================================
Generates all remaining sprites based on the 3 Gemini reference images.
Covers: food/items, UI/HUD, street details, vehicles, NPCs, FX, building tiles.

Run: python3 generate_sprites_extended.py
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_sprites import SVGSheet, p, hex_color, SPRITES_DIR

# ── Sheet 7: Food & Goods ─────────────────────────────────────────────────────
# Ref: gemini_ref_sprite_sheet.png "FOOD & GOODS" + gemini_ref_new_collection.png "CULTURAL FOOD"

def draw_coin_item(s, ox, oy):
    """20×20 gold Euro coin — main currency."""
    # Coin body
    s.put(ox+2, oy+2, "gold", 16, 16)
    s.put(ox+1, oy+4, "gold", 18, 12)
    s.put(ox+4, oy+1, "gold", 12, 18)
    # Shine (NW)
    s.put(ox+3, oy+3, "white",  6, 3)
    s.put(ox+3, oy+3, "white",  3, 6)
    # Edge shadow (SE)
    s.put(ox+14,oy+4, "ochre", 2, 12)
    s.put(ox+4, oy+14,"ochre", 12, 2)
    # € symbol (simplified)
    s.put(ox+8, oy+6,  "ochre", 5, 1)
    s.put(ox+7, oy+7,  "ochre", 2, 1)
    s.put(ox+7, oy+8,  "ochre", 6, 1)
    s.put(ox+7, oy+9,  "ochre", 2, 1)
    s.put(ox+7, oy+10, "ochre", 5, 1)
    s.put(ox+11,oy+7,  "ochre", 2, 5)

def draw_smoske(s, ox, oy):
    """28×16 Belgian smoske sandwich."""
    # Bread top half
    s.put(ox, oy, "cream_mid", 28, 7)
    s.put(ox, oy, "cream_light", 28, 1)
    s.put(ox, oy, "cream_light",  1, 7)
    s.put(ox+1, oy+1, "mortar", 3, 2)       # crust detail
    # Filling layers
    s.put(ox+2, oy+7, "brick_light", 24, 2) # meat (salami)
    s.put(ox+2, oy+9, "grass", 24, 1)       # lettuce
    s.put(ox+2, oy+10,"cream_mid",24, 1)    # cheese
    s.put(ox+2, oy+11,"brick_mid",24, 1)    # tomato slice
    # Bread bottom half
    s.put(ox, oy+12, "cream_mid", 28, 4)
    s.put(ox, oy+15, "cream_dark", 28, 1)
    # Sesame seeds on top
    for sx, sy in [(4,1),(8,2),(14,1),(20,2),(24,1)]:
        s.put(ox+sx, oy+sy, "cream_light", 1, 1)

def draw_friet(s, ox, oy):
    """16×20 Belgian fries in paper cone."""
    # Cone (paper)
    s.put(ox+4, oy+10, "cream_light", 8, 10)
    s.put(ox+4, oy+10, "cream_mid",   1, 10)  # left crease
    s.put(ox+11,oy+10, "cream_dark",  1, 10)  # right shadow
    # Cone point
    s.put(ox+7, oy+18, "cream_mid", 2, 2)
    # Frites sticking out
    frite_cols = [(4,0),(5,0),(6,1),(7,0),(8,0),(9,1),(10,0),(11,0)]
    for fx, fy in frite_cols:
        s.put(ox+fx, oy+fy, "ochre", 2, 10)
        s.put(ox+fx, oy+fy, "de_lijn_yellow", 1, 1)  # crispy tip
        s.put(ox+fx, oy+fy+8, "cream_dark", 1, 2)    # shadow base
    # Mayonnaise blob on top
    s.put(ox+5, oy+2, "white", 6, 3)
    s.put(ox+6, oy+1, "white", 4, 1)

def draw_mint_tea(s, ox, oy):
    """12×20 glass of Moroccan mint tea."""
    # Glass body
    s.put(ox+1, oy+4, "glass", 10, 14)
    # Tea liquid (amber/gold)
    s.put(ox+2, oy+5, "ochre", 8, 11)
    s.put(ox+2, oy+5, "de_lijn_yellow", 8, 1)  # surface reflection
    # Mint leaves
    s.put(ox+3, oy+3, "grass", 3, 3)
    s.put(ox+5, oy+2, "grass", 3, 4)
    s.put(ox+7, oy+3, "grass", 2, 3)
    # Leaf vein
    s.put(ox+4, oy+3, "stone_dark", 1, 2)
    # Glass highlight
    s.put(ox+1, oy+5, "sky_pale", 2, 10)
    s.put(ox+1, oy+4, "sky_pale", 10, 1)
    # Saucer
    s.put(ox, oy+18, "stone_light", 12, 2)
    s.put(ox, oy+18, "white", 12, 1)
    s.put(ox, oy+19, "stone_mid", 12, 1)
    # Gold rim on glass
    s.put(ox+1, oy+4, "de_lijn_yellow", 10, 1)
    s.put(ox+1, oy+17,"de_lijn_yellow", 10, 1)
    # Handle
    s.put(ox+11, oy+8,  "de_lijn_yellow", 2, 1)
    s.put(ox+12, oy+9,  "de_lijn_yellow", 1, 4)
    s.put(ox+11, oy+13, "de_lijn_yellow", 2, 1)

def draw_baklava(s, ox, oy):
    """16×12 diamond-shaped baklava piece."""
    # Pastry layers
    s.put(ox+2, oy+2, "cream_mid", 12, 8)
    # Phyllo layers (thin lines)
    for ly in range(3, 9):
        s.put(ox+3, oy+ly, "cream_light", 10, 1) if ly % 2 == 0 else None
    # Honey glaze (ochre overlay)
    s.put(ox+2, oy+2, "ochre", 12, 2)
    # Pistachio garnish (centre)
    s.put(ox+6, oy+4, "grass", 4, 3)
    s.put(ox+7, oy+4, "stone_dark", 2, 1)  # pistachio detail
    # Golden top crust
    s.put(ox+3, oy+2, "de_lijn_yellow", 10, 2)
    s.put(ox+2, oy+2, "de_lijn_yellow", 1, 2)
    # Diamond outline (shadow)
    s.put(ox+2, oy+9, "cream_dark", 12, 1)
    s.put(ox+14,oy+2, "cream_dark", 1, 8)

def draw_pomegranate(s, ox, oy):
    """16×16 pomegranate fruit."""
    # Main fruit body
    s.put(ox+1, oy+3, "red_ui", 14, 11)
    s.put(ox+3, oy+1, "red_ui", 10, 13)
    s.put(ox+2, oy+2, "red_ui", 12, 12)
    # Skin highlight (NW)
    s.put(ox+3, oy+3, "brick_light", 5, 4)
    s.put(ox+3, oy+3, "brick_light", 3, 5)
    # Dark bottom
    s.put(ox+4, oy+12, "brick_dark", 8, 2)
    # Crown (calyx top)
    s.put(ox+5, oy,  "brick_dark", 6, 3)
    s.put(ox+6, oy,  "brick_mid",  4, 2)
    # Crown spikes
    s.put(ox+5, oy-1,"brick_dark", 1, 2)
    s.put(ox+7, oy-1,"brick_dark", 1, 2)
    s.put(ox+9, oy-1,"brick_dark", 1, 2)
    s.put(ox+11,oy-1,"brick_dark", 1, 2)
    # Seeds visible (small)
    s.put(ox+6, oy+8, "cream_light", 2, 1)
    s.put(ox+9, oy+9, "cream_light", 2, 1)
    s.put(ox+8, oy+7, "cream_light", 1, 1)

def draw_orange(s, ox, oy):
    """14×14 orange fruit."""
    s.put(ox+1, oy+2, "ochre", 12, 10)
    s.put(ox+3, oy+1, "ochre", 8, 12)
    s.put(ox+2, oy+2, "ochre", 10, 10)
    # Highlight
    s.put(ox+3, oy+3, "de_lijn_yellow", 4, 3)
    s.put(ox+3, oy+3, "de_lijn_yellow", 3, 4)
    # Shadow
    s.put(ox+9, oy+8, "cream_dark", 3, 4)
    # Texture dots
    for (dx,dy) in [(5,5),(8,4),(6,9),(10,7)]:
        s.put(ox+dx, oy+dy, "cream_dark", 1, 1)
    # Stem + leaf
    s.put(ox+6, oy,  "wood_dark",  2, 2)
    s.put(ox+5, oy,  "grass",      3, 1)
    s.put(ox+8, oy,  "grass",      3, 1)

def draw_bread_loaf(s, ox, oy):
    """20×12 Belgian-style bread loaf."""
    # Loaf body
    s.put(ox, oy+3, "cream_mid", 20, 9)
    s.put(ox+2, oy, "cream_mid", 16, 12)
    s.put(ox+3, oy, "cream_mid", 14, 3)
    # Crust color (brown)
    s.put(ox, oy+3, "wood_light", 20, 1)    # top edge
    s.put(ox+2, oy,  "ochre",     16, 3)    # top dome
    s.put(ox+3, oy,  "de_lijn_yellow", 14, 1)  # crust top highlight
    # Score marks
    for sx in [5, 9, 13]:
        s.put(ox+sx, oy+1, "cream_dark", 1, 6)
    # Bottom crust
    s.put(ox, oy+11, "wood_dark", 20, 1)
    # Side shadow
    s.put(ox+18,oy+4, "cream_dark", 2, 8)

def draw_spice_sack(s, ox, oy):
    """12×16 burlap spice sack (cumin/ras el hanout)."""
    # Sack body
    s.put(ox+1, oy+4, "wood_light", 10, 12)
    s.put(ox, oy+6, "wood_light", 12, 8)
    # Burlap texture
    for ty in range(5, 14, 2):
        s.put(ox+2, oy+ty, "wood_dark", 8, 1)
    for tx in range(2, 10, 2):
        s.put(ox+tx, oy+5, "wood_dark", 1, 9)
    # Tie at top
    s.put(ox+3, oy+2, "wood_dark", 6, 3)
    s.put(ox+4, oy+1, "wood_dark", 4, 2)
    # Spice colour (cumin = brown, saffron = yellow, paprika = red)
    s.put(ox+3, oy+3, "ochre", 6, 1)    # spice peek at top
    # Shadow
    s.put(ox+9, oy+6, "wood_dark", 2, 10)

def draw_couscous_bowl(s, ox, oy):
    """20×14 tagine/couscous serving bowl."""
    # Bowl base
    s.put(ox+1, oy+6, "cream_mid", 18, 8)
    s.put(ox, oy+9, "cream_mid", 20, 5)
    s.put(ox+2, oy+6, "cream_light", 16, 1)  # rim highlight
    s.put(ox, oy+13, "cream_dark", 20, 1)    # bottom shadow
    # Couscous/food filling
    s.put(ox+3, oy+3, "mortar", 14, 4)       # couscous pale
    s.put(ox+3, oy+3, "cream_light", 14, 1)  # top highlight
    # Vegetable pieces
    s.put(ox+5, oy+4,  "grass",    3, 2)     # zucchini
    s.put(ox+10,oy+4,  "brick_mid",3, 2)     # tomato
    s.put(ox+14,oy+4,  "ochre",    2, 2)     # carrot
    # Meat (on top)
    s.put(ox+8, oy+2,  "wood_light",4, 3)    # chicken piece
    s.put(ox+8, oy+2,  "wood_dark", 1, 1)    # char
    # Rim detail
    s.put(ox+2, oy+13, "cream_mid", 16, 1)
    # Blue ceramic accent (Moroccan style)
    s.put(ox+1, oy+8, "de_lijn_blue", 1, 4)
    s.put(ox+18,oy+8, "de_lijn_blue", 1, 4)

def draw_kebab_doner(s, ox, oy):
    """12×20 rotating doner kebab spit."""
    # Spit rod
    s.put(ox+5, oy, "stone_mid", 2, 20)
    s.put(ox+5, oy, "stone_light", 1, 20)
    # Meat layers (stacked ovals)
    for layer in range(5):
        ly = oy + 2 + layer * 3
        lw = 8 + (layer % 2)
        lx = ox + 2 - (layer % 2)
        s.put(lx, ly, "wood_light", lw, 2)
        s.put(lx, ly, "brick_light", lw, 1)  # crispy edge
    # Fat lines
    for layer in range(5):
        ly = oy + 3 + layer * 3
        s.put(ox+3, ly, "cream_mid", 6, 1)
    # Bottom drip plate
    s.put(ox+1, oy+17, "stone_mid", 10, 3)
    s.put(ox+2, oy+18, "ochre",     8, 1)   # dripping juices
    # Top heat element
    s.put(ox+4, oy, "ochre", 4, 1)

def draw_paraplu(s, ox, oy):
    """20×28 blue umbrella reward item."""
    # Canopy
    s.put(ox+2, oy+8, "de_lijn_blue", 16, 8)
    s.put(ox, oy+10, "de_lijn_blue", 20, 6)
    # Scalloped edge
    for seg in range(5):
        sx = ox + seg * 4
        s.put(sx, oy+15, "de_lijn_blue", 4, 2)
        s.put(sx+1, oy+17, "de_lijn_blue", 2, 1)
    # Canopy top
    s.put(ox+9, oy+4, "de_lijn_blue", 2, 5)
    s.put(ox+8, oy+6, "de_lijn_blue", 4, 4)
    # Highlight stripes (NW light on canopy)
    s.put(ox+3, oy+10, "sky_pale", 2, 5)
    s.put(ox+8, oy+10, "sky_pale", 2, 5)
    s.put(ox+13,oy+10, "sky_pale", 2, 5)
    # Handle shaft
    s.put(ox+9, oy+2, "stone_dark", 2, 24)
    s.put(ox+9, oy+2, "stone_light", 1, 24)
    # Crook handle
    s.put(ox+9, oy+25, "stone_dark", 4, 2)
    s.put(ox+13,oy+24, "stone_dark", 2, 4)
    s.put(ox+13,oy+28, "stone_mid",  2, 1)
    # Handle highlight
    s.put(ox+9, oy+25, "stone_light", 4, 1)

def draw_permit_doc(s, ox, oy):
    """20×24 official permit document."""
    # Paper
    s.put(ox, oy, "white", 20, 24)
    s.put(ox, oy, "cream_light", 20, 24)
    # Header stripe (blue official)
    s.put(ox, oy, "de_lijn_blue", 20, 4)
    s.put(ox+2, oy+1, "white", 12, 2)    # title text
    # Belgian emblem (simplified)
    s.put(ox+14, oy+1, "gold", 4, 3)
    s.put(ox+15, oy+1, "black", 2, 3)    # lion silhouette
    # Text lines
    for ty in [6, 9, 12, 15, 18]:
        s.put(ox+2, oy+ty, "stone_dark", 16, 1)
    s.put(ox+2, oy+9, "stone_dark", 10, 1)  # shorter line
    # Stamp (red circle)
    s.put(ox+12, oy+15, "red_ui", 6, 6)
    s.put(ox+13, oy+16, "cream_light", 4, 4)  # stamp interior
    s.put(ox+13, oy+17, "red_ui", 2, 2)       # stamp mark
    # Signature line
    s.put(ox+2, oy+21, "stone_dark", 12, 1)
    s.put(ox+4, oy+22, "stone_mid", 8, 1)
    # Fold crease
    s.put(ox+10, oy, "stone_light", 1, 24)
    # Shadow
    s.put(ox+18, oy+2, "stone_mid", 2, 22)
    s.put(ox+2, oy+22, "stone_mid", 18, 2)

def generate_food_sheet():
    s = SVGSheet(256, 80, "FOOD & GOODS — Turnhoutsebaan cultural items")
    items = [
        ("coin",        0,  0,  draw_coin_item),
        ("smoske",      24, 0,  draw_smoske),
        ("friet",       56, 0,  draw_friet),
        ("mint_tea",    76, 0,  draw_mint_tea),
        ("baklava",     92, 0,  draw_baklava),
        ("pomegranate", 112,0,  draw_pomegranate),
        ("orange",      132,0,  draw_orange),
        ("bread",       150,0,  draw_bread_loaf),
        ("spice_sack",  174,0,  draw_spice_sack),
        ("couscous",    190,0,  draw_couscous_bowl),
        ("kebab_doner", 214,0,  draw_kebab_doner),
        ("paraplu",     230,0,  draw_paraplu),
    ]
    for name, x, y, fn in items:
        fn(s, x, y + 4)
        s.label(x, 74, name[:9])
    svg = os.path.join(SPRITES_DIR, "items/food_goods_sheet.svg")
    png = os.path.join(SPRITES_DIR, "items/food_goods_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Sheet 8: UI / HUD Elements ────────────────────────────────────────────────

def draw_hud_coin(s, ox, oy):
    """16×16 HUD coin icon."""
    s.put(ox+2, oy+2,  "gold", 12, 12)
    s.put(ox+1, oy+4,  "gold", 14, 8)
    s.put(ox+4, oy+1,  "gold", 8, 14)
    s.put(ox+3, oy+3,  "white", 4, 2)
    s.put(ox+3, oy+3,  "white", 2, 4)
    s.put(ox+10,oy+8,  "ochre", 2, 5)
    s.put(ox+6, oy+5,  "ochre", 1, 1)
    s.put(ox+7, oy+5,  "ochre", 3, 1)
    s.put(ox+6, oy+6,  "ochre", 1, 1)
    s.put(ox+6, oy+7,  "ochre", 4, 1)
    s.put(ox+6, oy+8,  "ochre", 1, 1)
    s.put(ox+6, oy+9,  "ochre", 3, 1)

def draw_hud_heart(s, ox, oy):
    """16×16 HUD heart (HP)."""
    heart = [
        "..XXXX.XXXX.",
        ".XXXXXXXXXXXXXXX"[:13],
        "XXXXXXXXXXXXXXXX"[:16],
        "XXXXXXXXXXXXXXXX"[:16],
        ".XXXXXXXXXXXXXX."[:16],
        "..XXXXXXXXXXXX.."[:16],
        "...XXXXXXXXXX..."[:16],
        "....XXXXXXXX...."[:16],
        ".....XXXXXX....."[:16],
        "......XXXX......"[:16],
        ".......XX......."[:16],
    ]
    row_data = [
        (2, 2, 12, 2),
        (1, 3, 14, 1),
        (0, 4, 16, 1),
        (0, 5, 16, 1),
        (0, 6, 16, 1),
        (0, 7, 16, 1),
        (1, 8, 14, 1),
        (2, 9, 12, 1),
        (3, 10, 10, 1),
        (4, 11, 8, 1),
        (5, 12, 6, 1),
        (6, 13, 4, 1),
        (7, 14, 2, 1),
    ]
    for (hx, hy, hw, hh) in row_data:
        s.put(ox + hx, oy + hy, "red_ui", hw, hh)
    # Highlight
    s.put(ox+2, oy+4, "brick_light", 5, 3)
    s.put(ox+2, oy+4, "brick_light", 3, 4)
    s.put(ox+9, oy+4, "brick_light", 5, 3)

def draw_hud_quest_dot(s, ox, oy):
    """8×8 quest objective marker."""
    s.put(ox+1, oy+1, "gold", 6, 6)
    s.put(ox+2, oy,   "gold", 4, 8)
    s.put(ox,   oy+2, "gold", 8, 4)
    s.put(ox+2, oy+2, "white", 2, 2)  # shine
    s.put(ox+5, oy+5, "ochre", 2, 2)  # shadow

def draw_hud_map_pin(s, ox, oy):
    """10×16 map location pin."""
    # Pin head (circle)
    s.put(ox+1, oy+1, "red_ui", 8, 8)
    s.put(ox+2, oy,   "red_ui", 6, 10)
    s.put(ox,   oy+2, "red_ui", 10, 6)
    s.put(ox+2, oy+2, "brick_light", 4, 4)  # centre dot
    s.put(ox+3, oy+3, "white", 2, 2)  # shine
    # Pin shaft
    s.put(ox+4, oy+9, "red_ui", 2, 5)
    s.put(ox+5, oy+13,"red_ui", 1, 3)

def draw_hud_bar_bg(s, ox, oy):
    """64×8 HUD background bar panel."""
    s.put(ox, oy, "black", 64, 8)
    s.put(ox+1,oy+1,"asphalt_dark", 62, 6)
    s.put(ox, oy, "stone_dark", 64, 1)
    s.put(ox, oy, "stone_dark", 1, 8)
    s.put(ox+63, oy,"stone_dark", 1, 8)
    s.put(ox, oy+7, "stone_dark", 64, 1)

def draw_hud_action_btn(s, ox, oy, label_col):
    """20×16 action button (SHOP / DELIVER / MAP / HEAL)."""
    s.put(ox, oy, "asphalt_dark", 20, 16)
    s.put(ox+1,oy+1,label_col, 18, 14)
    # Button bevel
    s.put(ox+1, oy+1, "white", 18, 1)
    s.put(ox+1, oy+1, "white", 1, 14)
    s.put(ox+1, oy+14,"stone_dark", 18, 1)
    s.put(ox+18,oy+1, "stone_dark", 1, 14)
    # Icon placeholder (text bar)
    s.put(ox+4, oy+6, "white", 12, 2)
    s.put(ox+4, oy+10,"white", 8, 2)

def draw_minimap_frame(s, ox, oy):
    """40×40 corner minimap border."""
    # Background
    s.put(ox, oy, "black", 40, 40)
    s.put(ox+2, oy+2, "asphalt_dark", 36, 36)
    # Gold border
    s.put(ox, oy, "gold", 40, 2)
    s.put(ox, oy, "gold", 2, 40)
    s.put(ox+38,oy, "gold", 2, 40)
    s.put(ox, oy+38,"gold", 40, 2)
    # Corner ornaments
    s.put(ox, oy, "ochre", 6, 6)
    s.put(ox+34,oy, "ochre", 6, 6)
    s.put(ox, oy+34,"ochre", 6, 6)
    s.put(ox+34,oy+34,"ochre",6,6)
    # Dot pattern
    for dx in range(4, 36, 4):
        for dy in range(4, 36, 4):
            s.put(ox+dx, oy+dy, "asphalt_mid", 1, 1)

def draw_inventory_slot(s, ox, oy):
    """20×20 inventory slot with dark inset."""
    s.put(ox, oy, "black", 20, 20)
    s.put(ox+2, oy+2, "asphalt_dark", 16, 16)
    # Inset bevel
    s.put(ox+2, oy+2, "stone_dark", 16, 1)
    s.put(ox+2, oy+2, "stone_dark", 1, 16)
    s.put(ox+2, oy+17,"asphalt_mid", 16, 1)
    s.put(ox+17,oy+2, "asphalt_mid", 1, 16)
    # Gold corner accent
    s.put(ox, oy, "gold", 3, 1)
    s.put(ox, oy, "gold", 1, 3)
    s.put(ox+17,oy,  "gold", 3, 1)
    s.put(ox+19,oy,  "gold", 1, 3)

def draw_dialogue_ninesl(s, ox, oy):
    """80×20 dialogue box (9-slice portion)."""
    # Main box
    s.put(ox, oy, "black", 80, 20)
    s.put(ox+2, oy+2, "asphalt_dark", 76, 16)
    # Border
    s.put(ox, oy, "gold", 80, 2)
    s.put(ox, oy, "gold", 2, 20)
    s.put(ox+78,oy, "gold", 2, 20)
    s.put(ox, oy+18,"gold", 80, 2)
    # Corner filigree
    s.put(ox+2, oy+2, "ochre", 4, 4)
    s.put(ox+74,oy+2, "ochre", 4, 4)
    # Text area placeholder lines
    s.put(ox+6, oy+5, "stone_mid", 68, 2)
    s.put(ox+6, oy+10,"stone_mid", 50, 2)
    s.put(ox+6, oy+14,"stone_mid", 60, 2)
    # Speech tail
    s.put(ox+10, oy+19,"gold", 6, 1)
    s.put(ox+11, oy+19,"asphalt_dark", 4, 1)

def generate_ui_sheet():
    s = SVGSheet(320, 80, "UI / HUD ELEMENTS — Turnhoutsebaan RPG")
    draw_hud_coin(s, 0, 0)
    s.label(0, 20, "coin16")
    draw_hud_heart(s, 20, 0)
    s.label(20, 20, "heart16")
    draw_hud_quest_dot(s, 40, 4)
    s.label(40, 20, "quest8")
    draw_hud_map_pin(s, 52, 0)
    s.label(52, 20, "map_pin")
    draw_hud_bar_bg(s, 0, 28)
    s.label(0, 40, "bar_bg64")
    btn_cols = ["de_lijn_blue", "brick_mid", "grass", "stone_dark"]
    btn_labels = ["btn_shop", "btn_deliv", "btn_map", "btn_heal"]
    for i, (bc, bl) in enumerate(zip(btn_cols, btn_labels)):
        draw_hud_action_btn(s, i*24, 44, bc)
        s.label(i*24, 63, bl)
    draw_minimap_frame(s, 100, 0)
    s.label(100, 44, "minimap")
    draw_inventory_slot(s, 148, 0)
    s.label(148, 24, "inv_slot")
    draw_dialogue_ninesl(s, 0, 66)
    s.label(0, 78, "dialogue80")
    svg = os.path.join(SPRITES_DIR, "ui/ui_sheet.svg")
    png = os.path.join(SPRITES_DIR, "ui/ui_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Sheet 9: Street Details ───────────────────────────────────────────────────

def draw_traffic_light(s, ox, oy, state="red"):
    """10×28 Belgian traffic light."""
    # Housing
    s.put(ox+1, oy, "black", 8, 26)
    s.put(ox+1, oy, "stone_dark", 1, 26)
    s.put(ox+8, oy, "stone_dark", 1, 26)
    s.put(ox+1, oy, "stone_dark", 8, 1)
    s.put(ox+1, oy+25,"stone_dark",8, 1)
    # Three lights
    light_colors = {
        "red":   ["red_ui",      "stone_dark",  "stone_dark"],
        "amber": ["stone_dark",  "de_lijn_yellow","stone_dark"],
        "green": ["stone_dark",  "stone_dark",   "grass"],
    }
    cols = light_colors.get(state, light_colors["red"])
    for i, col in enumerate(cols):
        ly = oy + 2 + i * 8
        s.put(ox+2, ly, col, 6, 6)
        s.put(ox+3, ly, col, 4, 6)
        s.put(ox+2, ly+1, col, 6, 4)
        if col != "stone_dark":
            s.put(ox+3, ly+1, "white", 2, 2)  # shine
    # Post
    s.put(ox+4, oy+26, "stone_dark", 2, 12)
    s.put(ox+4, oy+26, "stone_mid",  1, 12)
    # Base
    s.put(ox+2, oy+37, "stone_dark", 6, 2)

def draw_bus_stop_sign(s, ox, oy):
    """16×32 De Lijn bus stop pole+sign."""
    # Pole
    s.put(ox+7, oy+8, "stone_mid", 2, 24)
    s.put(ox+7, oy+8, "stone_light", 1, 24)
    # Sign board (De Lijn blue)
    s.put(ox, oy, "de_lijn_blue", 16, 9)
    # White border
    s.put(ox, oy, "white", 16, 1)
    s.put(ox, oy+8, "white", 16, 1)
    s.put(ox, oy, "white", 1, 9)
    s.put(ox+15,oy, "white", 1, 9)
    # Bus icon (simplified)
    s.put(ox+2, oy+2, "white", 6, 5)     # bus body
    s.put(ox+3, oy+2, "de_lijn_blue", 4, 2)  # windows
    s.put(ox+2, oy+6, "stone_dark", 2, 1)  # wheel
    s.put(ox+5, oy+6, "stone_dark", 2, 1)
    # Route number
    s.put(ox+10, oy+2, "de_lijn_yellow", 4, 5)
    s.put(ox+11, oy+3, "black", 2, 3)
    # Info panel below sign
    s.put(ox+1, oy+10, "white", 14, 10)
    s.put(ox+2, oy+11, "stone_dark", 12, 1)
    s.put(ox+2, oy+13, "stone_dark", 8, 1)
    s.put(ox+2, oy+15, "stone_dark", 10, 1)
    s.put(ox+2, oy+17, "stone_dark", 6, 1)
    # Ground base
    s.put(ox+5, oy+31, "stone_dark", 6, 1)

def draw_cafe_terrace(s, ox, oy):
    """32×24 outdoor café table + 2 chairs."""
    # Table
    s.put(ox+8, oy+6, "wood_light", 16, 2)   # tabletop
    s.put(ox+8, oy+6, "wood_dark", 16, 1)    # top edge highlight
    s.put(ox+8, oy+7, "cream_dark", 16, 1)   # underside shadow
    s.put(ox+15,oy+8, "wood_dark", 2, 10)    # centre leg
    s.put(ox+15,oy+8, "wood_light", 1, 10)
    s.put(ox+8, oy+17,"wood_dark", 16, 2)    # base spread
    # Left chair
    s.put(ox, oy+8, "wood_light", 6, 2)      # seat
    s.put(ox, oy+8, "wood_dark", 6, 1)
    s.put(ox+1, oy+4, "wood_light", 2, 5)    # back left
    s.put(ox+3, oy+4, "wood_light", 2, 5)    # back right
    s.put(ox+1, oy+4, "wood_light", 4, 1)    # back top rail
    s.put(ox, oy+10, "wood_dark", 2, 6)      # front leg
    s.put(ox+4, oy+10,"wood_dark", 2, 6)     # back leg
    # Right chair
    s.put(ox+26,oy+8, "wood_light", 6, 2)
    s.put(ox+26,oy+8, "wood_dark", 6, 1)
    s.put(ox+27,oy+4, "wood_light", 2, 5)
    s.put(ox+29,oy+4, "wood_light", 2, 5)
    s.put(ox+27,oy+4, "wood_light", 4, 1)
    s.put(ox+26,oy+10,"wood_dark", 2, 6)
    s.put(ox+30,oy+10,"wood_dark", 2, 6)
    # Coffee cups on table
    s.put(ox+10,oy+4, "white", 4, 3)
    s.put(ox+11,oy+5, "wood_dark", 2, 1)     # coffee
    s.put(ox+18,oy+4, "white", 4, 3)
    s.put(ox+19,oy+5, "wood_dark", 2, 1)
    # Shadow on ground
    s.put(ox+6, oy+22, "asphalt_dark", 20, 2)

def draw_merch_crate(s, ox, oy):
    """20×16 fruit/vegetable crate display outside shop."""
    # Wooden crate
    s.put(ox, oy+6, "wood_light", 20, 10)
    s.put(ox, oy+6, "wood_dark", 20, 1)
    s.put(ox, oy+6, "wood_dark", 1, 10)
    s.put(ox+19,oy+6,"wood_dark",1, 10)
    s.put(ox, oy+15,"wood_dark",20, 1)
    # Slat lines
    for sx in [4, 9, 14]:
        s.put(ox+sx, oy+7, "wood_dark", 1, 8)
    # Produce (tomatoes, oranges, lemons)
    tomatoes = [(1,2),(3,2),(6,2),(8,2),(11,2),(13,2),(16,2),(18,2)]
    for (tx, ty) in tomatoes:
        s.put(ox+tx, oy+ty, "brick_mid", 2, 3)
        s.put(ox+tx, oy+ty, "brick_light", 2, 1)
    oranges = [(2,0),(5,0),(8,0),(11,0),(14,0),(17,0)]
    for (ox2, oy2) in oranges:
        s.put(ox+ox2, oy+oy2, "ochre", 2, 3)
        s.put(ox+ox2, oy+oy2, "de_lijn_yellow", 2, 1)
    # Herb bunches (dark green)
    s.put(ox+1, oy+4, "grass", 4, 2)
    s.put(ox+10,oy+4, "grass", 4, 2)
    # Price sign
    s.put(ox+8, oy+11, "white", 8, 4)
    s.put(ox+9, oy+12, "stone_dark", 6, 1)

def draw_street_cat(s, ox, oy):
    """12×12 sitting street cat."""
    # Body (sitting, compact)
    s.put(ox+2, oy+5, "stone_mid", 8, 7)   # lower body
    s.put(ox+3, oy+2, "stone_mid", 6, 5)   # upper body
    # Head
    s.put(ox+3, oy, "stone_mid", 6, 4)
    # Ears (triangles)
    s.put(ox+3, oy, "stone_dark", 2, 2)
    s.put(ox+7, oy, "stone_dark", 2, 2)
    # Eyes
    s.put(ox+4, oy+2, "night", 1, 1)
    s.put(ox+7, oy+2, "night", 1, 1)
    # Eye shine
    s.put(ox+5, oy+2, "gold", 1, 1)
    s.put(ox+8, oy+2, "gold", 1, 1)
    # Nose + mouth
    s.put(ox+6, oy+3, "brick_light", 1, 1)
    # Tail
    s.put(ox+10,oy+8, "stone_mid", 2, 4)
    s.put(ox+10,oy+11,"stone_mid", 1, 1)
    # Paws
    s.put(ox+3, oy+11,"stone_light",3, 1)
    s.put(ox+7, oy+11,"stone_light",3, 1)
    # Fur highlight (NW)
    s.put(ox+4, oy+1, "stone_light", 3, 2)
    s.put(ox+4, oy+4, "stone_light", 2, 2)

def draw_balcony(s, ox, oy):
    """24×12 Belgian cast-iron balcony detail."""
    # Floor slab
    s.put(ox, oy, "stone_mid", 24, 3)
    s.put(ox, oy, "stone_light", 24, 1)
    s.put(ox, oy+2, "stone_dark", 24, 1)
    # Cast iron railing posts
    for px in [1, 5, 9, 13, 17, 21]:
        s.put(ox+px, oy+3, "stone_dark", 2, 9)
        s.put(ox+px, oy+3, "stone_mid", 1, 9)   # highlight
    # Top rail
    s.put(ox, oy+3, "stone_dark", 24, 1)
    s.put(ox, oy+3, "stone_mid", 24, 1)
    # Bottom rail
    s.put(ox, oy+10,"stone_dark", 24, 1)
    # Decorative floral motifs between posts
    for fx in [2, 6, 10, 14, 18]:
        s.put(ox+fx, oy+6, "stone_mid", 2, 1)   # horizontal bar
        s.put(ox+fx+1,oy+5,"stone_mid", 1, 3)   # vertical
        # Small circle motif
        s.put(ox+fx, oy+5, "stone_light", 1, 1)
        s.put(ox+fx+2,oy+5,"stone_light",1, 1)
    # Flower pot on balcony
    s.put(ox+10, oy, "brick_light", 4, 2)
    s.put(ox+10, oy-2,"grass", 4, 3)
    s.put(ox+11, oy-3,"grass", 2, 2)

def draw_belgian_flag(s, ox, oy):
    """12×20 Belgian flag on pole — black, yellow, red."""
    # Pole
    s.put(ox, oy, "stone_dark", 2, 20)
    s.put(ox, oy, "stone_light", 1, 20)
    # Flag (3 vertical stripes)
    s.put(ox+2, oy+1, "black", 4, 12)
    s.put(ox+6, oy+1, "gold",  4, 12)
    s.put(ox+10,oy+1, "red_ui",4, 12)
    # Flag highlight + wave
    s.put(ox+2, oy+1, "stone_dark", 4, 1)
    s.put(ox+2, oy+4, "stone_dark", 3, 1)  # wave crease
    s.put(ox+6, oy+4, "ochre", 3, 1)
    s.put(ox+10,oy+4, "brick_light", 3, 1)
    # Finial
    s.put(ox, oy, "gold", 2, 2)
    # Shadow
    s.put(ox+1, oy+19, "asphalt_dark", 4, 1)

def generate_street_details_sheet():
    s = SVGSheet(256, 80, "STREET DETAILS — Traffic light, bus stop, café, crates, cat, balcony")
    draw_traffic_light(s,   0,  0, "red")
    s.label(0,  44, "tl_red")
    draw_traffic_light(s, 14,  0, "amber")
    s.label(14, 44, "tl_amb")
    draw_traffic_light(s, 28,  0, "green")
    s.label(28, 44, "tl_grn")
    draw_bus_stop_sign(s, 44,  0)
    s.label(44, 44, "bus_stop")
    draw_cafe_terrace(s,  64,  0)
    s.label(64, 44, "cafe_ter")
    draw_merch_crate(s,  100,  0)
    s.label(100,44, "merch_cr")
    draw_street_cat(s,  124,  4)
    s.label(124,44, "cat")
    draw_balcony(s,     140,  4)
    s.label(140,44, "balcony")
    draw_belgian_flag(s,168,  0)
    s.label(168,44, "flag_be")
    svg = os.path.join(SPRITES_DIR, "environment/props/street_details_sheet.svg")
    png = os.path.join(SPRITES_DIR, "environment/props/street_details_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Sheet 10: Extended Vehicles ───────────────────────────────────────────────
# Ref: gemini_ref_new_collection.png "NEW VEHICLE SPRITES"

def draw_delivery_bakfiets(s, ox, oy):
    """40×28 delivery cargo bike (front-loading box)."""
    # Front cargo box
    s.put(ox, oy+4, "wood_light", 20, 16)    # box sides
    s.put(ox, oy+4, "wood_dark",  20, 1)     # box top
    s.put(ox, oy+4, "wood_dark",  1, 16)     # box left
    s.put(ox+19,oy+4,"wood_dark", 1, 16)     # box right
    s.put(ox, oy+19,"wood_dark",  20, 1)     # box bottom
    s.put(ox+2, oy+5, "cream_light", 16, 2)  # box interior top
    # Box content (vegetables/packages)
    s.put(ox+3, oy+7, "grass", 4, 8)        # leafy greens
    s.put(ox+8, oy+7, "brick_mid", 4, 8)    # tomatoes
    s.put(ox+13,oy+7, "ochre", 4, 8)        # oranges
    # Box logo/branding
    s.put(ox+2, oy+16,"de_lijn_blue", 16, 3) # blue stripe
    s.put(ox+6, oy+17,"white", 8, 1)         # text
    # Frame connecting box to rear
    s.put(ox+18,oy+14,"stone_dark", 10, 2)  # top tube
    s.put(ox+18,oy+14,"stone_mid",  10, 1)
    s.put(ox+22,oy+14,"stone_dark", 2, 6)   # down tube
    # Rear wheel (large)
    r_cx, r_cy = ox+32, oy+20
    for (rx,ry) in [(0,2),(0,3),(0,4),(1,6),(2,7),(3,8),(4,8),(5,8),
                    (6,7),(7,6),(8,4),(8,3),(8,2),(7,0),(6,0),(5,0),
                    (4,0),(3,0),(2,0),(1,0)]:
        s.put(r_cx+rx-4, r_cy+ry-4, "stone_dark", 1, 1)
    s.put(r_cx-2,r_cy-2,"stone_mid",4,4)    # hub
    # Front small wheel
    f_cx, f_cy = ox+10, oy+22
    for (rx,ry) in [(0,1),(0,2),(0,3),(1,4),(2,5),(3,5),(4,5),(5,4),(5,3),(5,2),(5,1),(4,0),(3,0),(2,0),(1,0)]:
        s.put(f_cx+rx-2, f_cy+ry-2, "stone_dark", 1, 1)
    s.put(f_cx-1,f_cy-1,"stone_mid",2,2)
    # Handlebars + rider seat
    s.put(ox+26,oy+8, "stone_dark", 6, 2)   # handlebar
    s.put(ox+27,oy+8, "stone_mid",  1, 2)
    s.put(ox+29,oy+10,"stone_dark", 1, 4)   # fork
    # Seat
    s.put(ox+22,oy+6, "stone_dark", 6, 2)
    s.put(ox+23,oy+6, "stone_light",4, 1)
    # Chain
    s.put(ox+24,oy+18,"stone_light",8, 1)
    # Shadow
    s.put(ox+4, oy+26, "asphalt_dark", 32, 2)

def draw_transport_bakfiets(s, ox, oy):
    """48×28 large transport cargo bakfiets."""
    # Large cargo box (longer)
    s.put(ox, oy+4, "wood_light", 28, 18)
    s.put(ox, oy+4, "wood_dark",  28, 1)
    s.put(ox, oy+4, "wood_dark",  1, 18)
    s.put(ox+27,oy+4,"wood_dark", 1, 18)
    s.put(ox, oy+21,"wood_dark",  28, 1)
    # Box shelves/tarp
    s.put(ox+2, oy+5, "de_lijn_blue", 24, 12)  # blue tarp
    s.put(ox+2, oy+5, "sky_pale", 24, 1)        # tarp shine
    # Rope securing tarp
    for ry in [8, 12]:
        s.put(ox+1, oy+ry, "ochre", 26, 1)
    # Bakfiets frame
    s.put(ox+26,oy+10,"stone_dark",10, 2)
    s.put(ox+30,oy+10,"stone_dark",2, 10)
    # Wheels
    for wx, wy, wr in [(10, 22, 5), (38, 20, 6)]:
        for ang in range(12):
            import math
            a = ang * math.pi / 6
            rx = int(math.cos(a) * wr)
            ry = int(math.sin(a) * wr)
            s.put(ox+wx+rx, oy+wy+ry, "stone_dark", 1, 1)
        s.put(ox+wx-1, oy+wy-1, "stone_mid", 2, 2)
    # Rider
    s.put(ox+34,oy+4, "de_lijn_blue", 6, 8)   # rider body
    s.put(ox+35,oy+2, "cream_mid", 4, 4)       # head
    s.put(ox+34,oy+4, "stone_dark", 2, 8)      # jacket side
    # Shadow
    s.put(ox+4, oy+27,"asphalt_dark",40, 1)

def draw_snellevering_scooter(s, ox, oy):
    """32×24 orange delivery scooter."""
    # Body
    s.put(ox+4, oy+8, "ochre", 20, 12)       # main body orange
    s.put(ox+4, oy+8, "de_lijn_yellow", 20, 1)  # top shine
    # Fairing / windscreen
    s.put(ox+16,oy+4, "glass", 8, 8)
    s.put(ox+17,oy+5, "sky_pale", 4, 3)      # reflection
    s.put(ox+16,oy+4, "stone_dark", 1, 8)    # fairing edge
    # Delivery box (rear)
    s.put(ox, oy+6, "ochre", 8, 12)
    s.put(ox, oy+6, "cream_dark", 8, 1)
    s.put(ox+7, oy+6, "cream_dark", 1, 12)
    s.put(ox+2, oy+10,"white", 4, 4)         # logo area
    s.put(ox+3, oy+11,"red_ui", 2, 2)        # logo
    # Seat
    s.put(ox+8, oy+6, "stone_dark", 12, 3)
    s.put(ox+9, oy+6, "stone_light", 10, 1)
    # Handlebars
    s.put(ox+22,oy+6, "stone_dark", 8, 2)
    s.put(ox+26,oy+5, "stone_dark", 1, 4)
    # Exhaust
    s.put(ox+4, oy+18,"stone_dark", 4, 2)
    s.put(ox, oy+19,  "stone_mid", 4, 1)
    # Wheels
    for wx, wy, wr in [(6, 20, 5), (26, 20, 5)]:
        for ang in range(8):
            import math
            a = ang * math.pi / 4
            rx = int(math.cos(a) * wr)
            ry = int(math.sin(a) * wr)
            s.put(ox+wx+rx, oy+wy+ry, "black", 1, 1)
        s.put(ox+wx-1, oy+wy-1, "stone_mid", 3, 3)
    # Rider (simplified — orange vest, helmet)
    s.put(ox+14,oy, "stone_dark", 8, 8)      # rider body
    s.put(ox+15,oy-3,"stone_dark",6, 4)      # helmet
    s.put(ox+16,oy-2,"ochre",    4, 3)       # orange vest peek
    s.put(ox+14,oy,  "ochre",    8, 1)       # vest shoulder
    # Shadow
    s.put(ox+4, oy+24,"asphalt_dark",24, 1)

def draw_antwerp_bicycle(s, ox, oy):
    """32×24 classic Antwerp city bicycle."""
    # Rear wheel
    for (rx, ry) in [(4,0),(3,0),(2,0),(1,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                      (1,7),(2,8),(3,8),(4,8),(5,8),(6,8),(7,7),(8,6),(8,5),(8,4),
                      (8,3),(8,2),(8,1),(7,0),(6,0),(5,0)]:
        s.put(ox+rx, oy+8+ry, "stone_dark", 1, 1)
    s.put(ox+3,oy+11,"stone_mid",3,3)   # rear hub
    # Frame
    s.put(ox+8,  oy+8, "stone_dark", 12, 1)   # top tube
    s.put(ox+8,  oy+8, "stone_mid", 12, 1)
    s.put(ox+8,  oy+9, "stone_dark", 1, 9)    # seat tube
    s.put(ox+8,  oy+17,"stone_dark",12, 1)    # chain stay
    s.put(ox+16, oy+8, "stone_dark", 1, 9)    # down tube
    # Front fork
    s.put(ox+19, oy+8, "stone_dark", 1, 12)
    s.put(ox+20, oy+8, "stone_dark", 4, 1)
    s.put(ox+20, oy+9, "stone_dark", 1, 9)
    # Front wheel
    for (rx,ry) in [(4,0),(3,0),(2,0),(1,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                     (1,7),(2,8),(3,8),(4,8),(5,8),(6,8),(7,7),(8,6),(8,5),(8,4),
                     (8,3),(8,2),(8,1),(7,0),(6,0),(5,0)]:
        s.put(ox+20+rx, oy+8+ry, "stone_dark", 1, 1)
    s.put(ox+23,oy+11,"stone_mid",3,3)
    # Handlebar
    s.put(ox+18,oy+4, "stone_dark", 5, 2)
    s.put(ox+18,oy+4, "stone_light",5, 1)
    s.put(ox+18,oy+5, "stone_dark",1, 4)
    # Seat
    s.put(ox+6, oy+4, "stone_dark", 6, 2)
    s.put(ox+7, oy+4, "stone_light",4, 1)
    s.put(ox+9, oy+5, "stone_dark",1, 3)  # seatpost
    # Basket (front)
    s.put(ox+20,oy+8, "wood_light",6, 6)
    s.put(ox+20,oy+8, "wood_dark", 6, 1)
    for bx in [21,23,25]:
        s.put(ox+bx,oy+9,"wood_dark",1,5)
    # Bell
    s.put(ox+21,oy+6, "stone_light",2, 2)
    # Shadow
    s.put(ox+2, oy+18,"asphalt_dark",26,1)

def generate_vehicles_extended_sheet():
    s = SVGSheet(320, 80, "VEHICLES EXTENDED — Bakfiets, scooter, bicycle")
    draw_delivery_bakfiets(s, 0, 4)
    s.label(0, 74, "bakfiets_del")
    draw_transport_bakfiets(s, 44, 4)
    s.label(44, 74, "bakfiets_tr")
    draw_snellevering_scooter(s, 96, 8)
    s.label(96, 74, "scooter_del")
    draw_antwerp_bicycle(s, 132, 4)
    s.label(132,74, "bicycle_ant")
    svg = os.path.join(SPRITES_DIR, "vehicles/vehicles_extended_sheet.svg")
    png = os.path.join(SPRITES_DIR, "vehicles/vehicles_extended_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Sheet 11: Additional NPCs ─────────────────────────────────────────────────
# Ref: gemini_ref_new_collection.png "CHARACTER SPRITES"

def draw_npc_musician(s, ox, oy, stride=False):
    """20×48 Street musician with oud (Arabic lute)."""
    # HEAD
    s.put(ox+7, oy+4, "ochre", 6, 8)         # face (warm skin)
    s.put(ox+6, oy+2, "wood_dark", 8, 4)     # dark hair
    s.put(ox+8, oy+8, "black", 1, 1)         # eye L
    s.put(ox+11,oy+8, "black", 1, 1)         # eye R
    s.put(ox+7, oy+11,"stone_dark",6, 2)     # beard/moustache
    # BODY — white shirt, dark waistcoat
    s.put(ox+5, oy+12,"white",    10, 14)    # shirt
    s.put(ox+5, oy+12,"stone_dark",2, 14)    # waistcoat left
    s.put(ox+13,oy+12,"stone_dark",2, 14)    # waistcoat right
    s.put(ox+5, oy+12,"stone_dark",10,2)     # waistcoat top
    # Buttons
    for by in [14,17,20]:
        s.put(ox+9, oy+by, "gold", 2, 1)
    # Arms
    s.put(ox+2, oy+13,"ochre", 4, 10)        # left arm (holding neck)
    s.put(ox+2, oy+13,"cream_light",1,10)
    s.put(ox+14,oy+13,"white", 4, 10)        # right arm (strumming)
    # PANTS
    s.put(ox+5, oy+26,"stone_dark",10,16)
    s.put(ox+4, oy+26,"black",1,16)
    # SHOES
    s.put(ox+5, oy+40,"black",4,6)
    s.put(ox+5, oy+40,"stone_dark",1,6)
    s.put(ox+9, oy+40,"black",4,4)
    # OUD (Arabic lute) — the key prop
    # Body (pear-shaped resonator)
    s.put(ox-4, oy+16,"wood_light",12,14)    # oud body
    s.put(ox-4, oy+16,"wood_dark", 12,1)
    s.put(ox-4, oy+16,"wood_dark", 1,14)
    s.put(ox+7, oy+16,"wood_dark", 1,14)
    # Oud sound hole
    s.put(ox, oy+20,   "black",    4, 4)
    s.put(ox, oy+21,   "stone_dark",2,2)
    # Oud neck + tuning pegs
    s.put(ox+2, oy+10, "wood_light",2,8)
    s.put(ox+1, oy+10, "wood_dark", 1,6)
    for pg in [10,12,14]:
        s.put(ox, oy+pg,  "wood_dark",1,1)    # peg left
        s.put(ox+4,oy+pg, "wood_dark",1,1)    # peg right
    # Strings (thin lines)
    for sx in range(4):
        s.put(ox+sx+1, oy+10, "stone_light",1,18)
    # NW highlight on oud
    s.put(ox-4,oy+17, "cream_light",8,2)

def draw_npc_woman_boxes(s, ox, oy, stride=False):
    """20×48 Woman carrying shopping boxes."""
    leg_off = 2 if stride else 0
    # HEAD + HAIR
    s.put(ox+7, oy+4, "cream_light", 6, 8)   # face
    s.put(ox+6, oy+2, "wood_dark",   8, 5)   # dark hair
    s.put(ox+14,oy+4, "wood_dark",   2, 6)   # hair side
    s.put(ox+8, oy+9, "black", 1, 1)         # eye
    s.put(ox+11,oy+9, "black", 1, 1)
    s.put(ox+9, oy+11,"brick_light",2,1)     # lips
    # BODY — colourful dress/blouse
    s.put(ox+4, oy+12,"brick_light",12,14)   # blouse (warm pink)
    s.put(ox+4, oy+12,"brick_mid",  12,1)    # collar
    s.put(ox+4, oy+12,"brick_mid",  1,14)
    s.put(ox+15,oy+12,"brick_dark", 1,14)
    # SKIRT
    s.put(ox+3, oy+26,"cream_mid",  14,14)
    s.put(ox+2, oy+26,"cream_dark", 1,14)
    s.put(ox+16,oy+26,"cream_dark", 1,14)
    # LEGS + SHOES
    s.put(ox+5, oy+40,"cream_light",4,6)
    s.put(ox+9, oy+40+leg_off,"cream_light",4,4)
    s.put(ox+5, oy+44,"wood_dark",4,2)
    s.put(ox+9, oy+44,"wood_dark",4,2)
    # ARMS (outstretched holding boxes)
    s.put(ox+1, oy+13,"brick_light",4,10)
    s.put(ox+1, oy+13,"brick_dark", 1,10)
    s.put(ox+15,oy+13,"brick_light",4,10)
    s.put(ox+18,oy+13,"brick_dark", 1,10)
    # LEFT BOX (shopping)
    s.put(ox-4, oy+16,"cream_light",8,10)
    s.put(ox-4, oy+16,"stone_mid",  8,1)
    s.put(ox-4, oy+16,"stone_mid",  1,10)
    s.put(ox+3, oy+16,"stone_mid",  1,10)
    s.put(ox-4, oy+25,"stone_mid",  8,1)
    # Box logo
    s.put(ox-3, oy+18,"de_lijn_blue",6,3)
    s.put(ox-2, oy+19,"white",4,1)
    # Handles
    s.put(ox-3, oy+16,"stone_dark",2,2)
    s.put(ox+0, oy+16,"stone_dark",2,2)
    # RIGHT BOX
    s.put(ox+17,oy+16,"cream_light",8,10)
    s.put(ox+17,oy+16,"stone_mid",  8,1)
    s.put(ox+17,oy+16,"stone_mid",  1,10)
    s.put(ox+24,oy+16,"stone_mid",  1,10)
    s.put(ox+17,oy+25,"stone_mid",  8,1)
    s.put(ox+18,oy+18,"brick_light",6,3)
    s.put(ox+19,oy+19,"white",4,1)
    # NW highlight
    s.put(ox+4, oy+12,"brick_light",12,1)
    s.put(ox+4, oy+12,"cream_light",1,14)

def generate_npcs_extra_sheet():
    s = SVGSheet(320, 100, "NPC EXTRA — Musician, Woman with boxes (idle+stride)")
    draw_npc_musician(s, 8, 2, stride=False)
    s.label(8, 96, "musician")
    draw_npc_musician(s, 36, 2, stride=True)
    s.label(36,96, "musn_str")
    draw_npc_woman_boxes(s, 72, 2, stride=False)
    s.label(72,96, "w_boxes")
    draw_npc_woman_boxes(s, 100, 2, stride=True)
    s.label(100,96,"wb_str")
    svg = os.path.join(SPRITES_DIR, "characters/npcs/npc_extra_sheet.svg")
    png = os.path.join(SPRITES_DIR, "characters/npcs/npc_extra_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Sheet 12: FX Sprites ──────────────────────────────────────────────────────

def draw_fx_coin_sparkle(s, ox, oy, frame=0):
    """32×32 coin pickup sparkle — 4 frames."""
    rays = [
        [(16,0),(16,2),(16,4),(16,6),(0,16),(2,16),(4,16),(6,16),
         (26,6),(24,6),(22,8),(10,8),(8,8),(8,10),(26,26),(6,26)],
        [(14,0),(14,2),(14,4),(18,4),(18,2),(18,0),(0,14),(2,14),(4,14),
         (28,14),(26,14),(24,14),(0,18),(28,18),(8,6),(22,6),(6,22),(22,22)],
        [(12,4),(12,6),(16,0),(20,4),(20,6),(4,12),(4,20),(28,12),(28,20),
         (6,8),(10,6),(22,6),(26,8),(6,24),(26,24)],
        [(10,8),(8,10),(8,22),(10,24),(22,8),(24,10),(24,22),(22,24),
         (16,2),(16,28),(2,16),(28,16)],
    ]
    sizes = [2, 2, 1, 1]
    for (rx, ry) in rays[frame]:
        s.put(ox+rx, oy+ry, "gold", sizes[frame], sizes[frame])
        if sizes[frame] > 1:
            s.put(ox+rx, oy+ry, "white", 1, 1)
    # Coin in centre
    s.put(ox+12,oy+12,"gold", 8, 8)
    s.put(ox+12,oy+12,"white",3, 3)

def draw_fx_dust(s, ox, oy, frame=0):
    """24×16 dust puff — 4 frames (emitted while bike rides fast)."""
    clouds = [
        [(0,8,6,6),(4,6,6,6),(8,4,8,8)],
        [(0,8,8,6),(6,4,8,8),(12,6,6,6)],
        [(2,6,10,8),(10,4,10,8),(18,6,4,6)],
        [(4,6,12,8),(14,4,6,8),(20,4,2,6)],
    ]
    for (cx, cy, cw, ch) in clouds[frame]:
        s.put(ox+cx, oy+cy, "stone_pale", cw, ch)
    s.put(ox, oy+13, "sidewalk", 24, 1)  # ground hint

def draw_fx_tram_spark(s, ox, oy, frame=0):
    """8×8 overhead wire spark — 4 frames."""
    sparks = [
        [(3,0),(4,0),(3,1),(4,1),(2,2),(5,2),(1,3),(6,3)],
        [(3,0),(4,0),(2,1),(5,1),(1,2),(6,2),(0,3),(7,3),(2,4),(5,4)],
        [(2,0),(5,0),(1,1),(6,1),(0,2),(7,2),(3,3),(4,3),(1,4),(6,4),(2,5),(5,5)],
        [(3,2),(4,2),(2,3),(5,3),(3,4),(4,4)],
    ]
    colors = ["de_lijn_yellow","white","white","gold"]
    for (rx, ry) in sparks[frame]:
        s.put(ox+rx, oy+ry, colors[frame], 1, 1)

def draw_fx_exclamation(s, ox, oy, frame=0):
    """12×20 '!' pop — 2 frames NPC reaction."""
    # Bubble
    s.put(ox+1, oy+1, "white", 10, 14)
    s.put(ox, oy+2, "white", 12, 12)
    s.put(ox, oy+2, "stone_dark", 12, 1)
    s.put(ox, oy+2, "stone_dark", 1, 12)
    s.put(ox+11,oy+2,"stone_dark",1, 12)
    s.put(ox, oy+13,"stone_dark",12, 1)
    # Bubble tail
    s.put(ox+4, oy+14,"white", 4, 3)
    s.put(ox+4, oy+14,"stone_dark",1,3)
    s.put(ox+7, oy+14,"stone_dark",1,3)
    s.put(ox+5, oy+16,"stone_dark",1,1)
    # Exclamation mark
    s.put(ox+5, oy+3, "red_ui", 2, 7)
    s.put(ox+5, oy+11,"red_ui", 2, 2)
    if frame == 0:
        # Frame 0: full size, yellow glow around bubble
        s.put(ox-1,oy,    "gold", 14, 1)
        s.put(ox-1,oy,    "gold", 1, 16)
        s.put(ox+13,oy,   "gold", 1, 16)
        s.put(ox-1,oy+15, "gold", 14, 1)

def generate_fx_sheet():
    s = SVGSheet(256, 80, "FX SPRITES — Coin, dust, tram sparks, exclamation")
    # Coin sparkle — 4 frames
    for f in range(4):
        draw_fx_coin_sparkle(s, f*36, 0, f)
        s.label(f*36, 36, f"coin_f{f}")
    # Dust — 4 frames
    for f in range(4):
        draw_fx_dust(s, f*28, 40, f)
        s.label(f*28, 60, f"dust_f{f}")
    # Tram sparks — 4 frames
    for f in range(4):
        draw_fx_tram_spark(s, 144+f*12, 40, f)
        s.label(144+f*12, 60, f"spk_f{f}")
    # Exclamation — 2 frames
    draw_fx_exclamation(s, 200, 0, frame=0)
    s.label(200,24,"exc_f0")
    draw_fx_exclamation(s, 216, 0, frame=1)
    s.label(216,24,"exc_f1")
    svg = os.path.join(SPRITES_DIR, "fx/fx_sheet.svg")
    png = os.path.join(SPRITES_DIR, "fx/fx_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Sheet 13: Specific Shop Building Tiles ────────────────────────────────────
# Based on gemini_ref_new_collection.png "NEW BUILDINGS & TILES"

def draw_hammam_tile(s, ox, oy):
    """32×32 Hammam Borgerhout — ornate terracotta + teal mosaic tile."""
    # Terracotta render base
    s.put(ox, oy, "brick_light", 32, 32)
    s.put(ox, oy, "ochre", 32, 32)  # warm terracotta base
    # Teal arch (geometric mosaic pattern)
    # Central arch
    s.put(ox+8, oy+4,  "de_lijn_blue", 16, 20)  # arch fill
    s.put(ox+6, oy+8,  "de_lijn_blue", 20, 16)
    # Arch cutout (interior)
    s.put(ox+10,oy+6,  "stone_dark", 12, 18)
    s.put(ox+8, oy+10, "stone_dark", 16, 14)
    # Geometric border tiles
    for ty in range(0, 32, 4):
        s.put(ox, oy+ty, "de_lijn_blue", 6, 4) if ty%8==0 else s.put(ox, oy+ty, "ochre", 6, 4)
        s.put(ox+26,oy+ty,"de_lijn_blue",6,4) if ty%8==4 else s.put(ox+26,oy+ty,"ochre",6,4)
    # Star pattern in mosaic
    for tx in range(4, 28, 8):
        s.put(ox+tx, oy+26, "de_lijn_yellow", 4, 4)
        s.put(ox+tx+1,oy+27,"stone_dark", 2, 2)
    # Highlights
    s.put(ox, oy, "cream_light", 32, 1)
    s.put(ox, oy, "cream_light", 1, 32)

def draw_aladdin_tile(s, ox, oy):
    """32×32 Patisserie Aladdin — cream render, yellow awning detail."""
    s.put(ox, oy, "cream_mid", 32, 32)
    # Yellow awning
    s.put(ox, oy+18, "de_lijn_yellow", 32, 8)
    # Awning stripes
    for ax in range(0, 32, 6):
        s.put(ox+ax, oy+18, "ochre", 3, 8)
    s.put(ox, oy+18, "ochre", 32, 1)      # top edge
    s.put(ox, oy+25, "cream_dark", 32, 1) # bottom edge
    # Arabic arch window
    s.put(ox+8, oy+2, "glass", 16, 14)
    s.put(ox+9, oy+3, "sky_pale", 8, 4)  # reflection
    # Arch points (Moorish)
    s.put(ox+14,oy+2, "cream_mid", 4, 2)
    s.put(ox+13,oy+3, "cream_mid", 6, 1)
    # Arabic text (decorative bars)
    s.put(ox+8, oy+26,"stone_dark", 16, 2)
    s.put(ox+10,oy+26,"cream_light",12, 1)
    # Pastry in window
    s.put(ox+10,oy+10,"ochre", 4, 4)     # baklava tray
    s.put(ox+15,oy+10,"cream_mid",4,4)   # pastry shapes
    # Signage
    s.put(ox+2, oy+27,"de_lijn_yellow",28,3)
    s.put(ox+6, oy+28,"black",16,1)
    # NW highlight
    s.put(ox, oy, "cream_light", 32, 1)
    s.put(ox, oy, "cream_light", 1, 32)

def draw_frituur_tile(s, ox, oy):
    """32×32 Frituur de Tram — white/red Belgian chip shop."""
    s.put(ox, oy, "white", 32, 32)
    # Red awning / canopy
    s.put(ox, oy+16, "red_ui", 32, 10)
    # Awning stripes
    for ax in range(0, 32, 6):
        s.put(ox+ax, oy+16, "white", 3, 10)
    s.put(ox, oy+16, "brick_dark", 32, 1)  # awning top edge
    # Menu board (exterior)
    s.put(ox+2, oy+2, "stone_dark", 28, 12)
    # Menu items (illustrated)
    s.put(ox+4, oy+4,  "ochre",  4, 4)   # fries image
    s.put(ox+10,oy+4,  "brick_light",4,4)  # burger
    s.put(ox+16,oy+4,  "red_ui", 4, 4)   # tomato/ketchup
    s.put(ox+22,oy+4,  "de_lijn_yellow",4,4)  # mayo
    # Price text
    s.put(ox+4, oy+9, "white", 24, 2)
    # "FRITUUR" text bar
    s.put(ox+4, oy+27,"red_ui", 24, 3)
    s.put(ox+8, oy+28,"white", 16, 1)
    # Window display
    s.put(ox+6, oy+12,"glass", 20, 4)
    s.put(ox+7, oy+12,"sky_pale",8,2)
    # NW
    s.put(ox, oy, "stone_light", 32, 1)
    s.put(ox, oy, "stone_light", 1, 32)

def draw_theehuys_tile(s, ox, oy):
    """32×32 Theehuys Amal — ochre walls, teal shutters."""
    s.put(ox, oy, "ochre", 32, 32)
    s.put(ox, oy, "cream_mid", 32, 32)    # base
    s.put(ox, oy, "ochre", 32, 20)        # ochre upper portion
    # Teal shutters
    s.put(ox+4, oy+4,  "de_lijn_blue", 10, 14)  # left shutter
    s.put(ox+4, oy+4,  "stone_dark", 10, 1)
    for sy in range(5, 17, 2):
        s.put(ox+5, oy+sy, "night", 8, 1)
    s.put(ox+18,oy+4,  "de_lijn_blue", 10, 14)  # right shutter
    s.put(ox+18,oy+4,  "stone_dark", 10, 1)
    for sy in range(5, 17, 2):
        s.put(ox+19,oy+sy, "night", 8, 1)
    # Glass between shutters (open view)
    s.put(ox+14,oy+4,  "glass", 4, 14)
    s.put(ox+14,oy+5,  "sky_pale", 2, 4)
    # Arabic + Dutch sign
    s.put(ox+2, oy+20, "cream_light", 28, 10)
    s.put(ox+4, oy+22, "stone_dark",  24, 2)   # Arabic script bar
    s.put(ox+4, oy+26, "stone_dark",  18, 2)   # Dutch text bar
    # Tea glass icon on sign
    s.put(ox+22,oy+22, "ochre", 4, 6)
    s.put(ox+23,oy+23, "glass", 2, 3)
    # Door
    s.put(ox+13,oy+20, "wood_dark", 6, 12)
    s.put(ox+14,oy+21, "glass",     4, 10)
    s.put(ox+15,oy+22, "sky_pale",  2, 4)
    # NW
    s.put(ox, oy, "cream_light", 32, 1)
    s.put(ox, oy, "cream_light", 1, 32)

def draw_couture_tile(s, ox, oy):
    """32×32 Couture El Fessi — textile/fashion boutique."""
    s.put(ox, oy, "cream_mid", 32, 32)
    # Display window (large plate glass)
    s.put(ox+2, oy+2, "glass", 28, 22)
    s.put(ox+3, oy+3, "sky_light", 8, 6)   # reflection
    s.put(ox+3, oy+3, "cloud",     4, 3)
    # Mannequin in window (simplified)
    s.put(ox+8,  oy+6, "stone_pale", 4, 14)  # dress form
    s.put(ox+8,  oy+6, "de_lijn_blue", 4, 8) # fabric on mannequin
    s.put(ox+8,  oy+5, "cream_light", 4, 2)  # shoulder
    s.put(ox+18, oy+6, "stone_pale", 4, 14)
    s.put(ox+18, oy+6, "brick_light", 4, 8)  # different outfit
    s.put(ox+18, oy+5, "cream_light", 4, 2)
    # Fabric bolt display
    s.put(ox+10,oy+16, "red_ui", 3, 6)
    s.put(ox+14,oy+16, "de_lijn_blue",3,6)
    s.put(ox+18,oy+16, "ochre",3,6)
    # Awning (dark blue with gold fringe)
    s.put(ox, oy+24, "stone_dark", 32, 6)
    for ax in range(0, 32, 4):
        s.put(ox+ax, oy+24, "night", 2, 6)
    s.put(ox, oy+29, "gold", 32, 1)    # gold fringe line
    # "COUTURE EL FESSI" signage
    s.put(ox+4, oy+26,"cream_light",24,2)
    s.put(ox+4, oy+27,"stone_pale",16,1)
    # NW
    s.put(ox, oy, "cream_light", 32, 1)
    s.put(ox, oy, "cream_light", 1, 32)

def generate_building_tiles_sheet():
    s = SVGSheet(320, 80, "BUILDING TILES — Specific Turnhoutsebaan shops (32×32 each)")
    tiles = [
        ("hammam",    0,   draw_hammam_tile),
        ("aladdin",   36,  draw_aladdin_tile),
        ("frituur",   72,  draw_frituur_tile),
        ("theehuys",  108, draw_theehuys_tile),
        ("couture",   144, draw_couture_tile),
    ]
    for name, x, fn in tiles:
        fn(s, x, 0)
        s.label(x+2, 36, name)
    svg = os.path.join(SPRITES_DIR, "environment/buildings/shop_tiles_sheet.svg")
    png = os.path.join(SPRITES_DIR, "environment/buildings/shop_tiles_sheet.png")
    s.save(svg); s.to_pil(png)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Turnhoutsebaan RPG — Extended Sprite Generator")
    print("Based on Gemini reference images analysis")
    print("=" * 48)

    print("\n[7/13] Food & goods sheet...")
    generate_food_sheet()

    print("\n[8/13] UI / HUD elements sheet...")
    generate_ui_sheet()

    print("\n[9/13] Street details (traffic lights, café, crates, cat, flag)...")
    generate_street_details_sheet()

    print("\n[10/13] Extended vehicles (bakfiets, scooter, bicycle)...")
    generate_vehicles_extended_sheet()

    print("\n[11/13] Extra NPCs (musician, woman with boxes)...")
    generate_npcs_extra_sheet()

    print("\n[12/13] FX sprites (coin sparkle, dust, sparks, exclamation)...")
    generate_fx_sheet()

    print("\n[13/13] Shop building tiles (Hammam, Aladdin, Frituur, Theehuys, Couture)...")
    generate_building_tiles_sheet()

    print("\nAll extended sprites generated!")
