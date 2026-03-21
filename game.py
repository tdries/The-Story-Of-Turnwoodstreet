#!/usr/bin/env python3
"""
Turnhoutsebaan RPG  —  Borgerhout, Antwerpen
Zelda: Link's Awakening engine  ×  Oblique-3D voxel buildings

Engine:
  - Tile-based world (48 px tiles, 280 × 15 map)
  - Painter-algorithm depth layers  +  Y-sorted entities
  - Oblique 3D buildings: flat roof tile  +  south/north wall face
  - Smooth 8-dir movement, momentum physics
  - Room-transition interiors (like Zelda)
  - Quest FSM, save / load

Controls:  WASD / Arrows=move  B=bike  E=interact  I=inventory  S=save  ESC=back
"""

import pygame, sys, os, json, math, random

# ══════════════════════════════════════════════════════════════════════════════
#  DISPLAY
# ══════════════════════════════════════════════════════════════════════════════
W, H    = 1280, 720
HUD_H   =  80
VIEW_H  = H - HUD_H            # 640

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Turnhoutsebaan RPG  ·  Borgerhout")
clock  = pygame.time.Clock()

# ══════════════════════════════════════════════════════════════════════════════
#  TILE CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════
TS = 48           # tile size px

# tile-type IDs
T_VOID, T_ROAD, T_SIDEW, T_TRAM = 0, 1, 2, 3
T_BT, T_BB = 4, 5        # building-top / building-bottom (solid)
T_DOOR_T, T_DOOR_B = 6, 7
T_CROSS = 8

SOLID = {T_BT, T_BB, T_VOID}
BIKE_OK = {T_ROAD, T_SIDEW, T_TRAM, T_CROSS, T_DOOR_T, T_DOOR_B}
WALK_OK = {T_SIDEW, T_DOOR_T, T_DOOR_B, T_CROSS}

# Map geometry (rows from north to south)
MAP_ROWS = 15
MAP_COLS = 300
WORLD_W  = MAP_COLS * TS   # 14 400 px
WORLD_H  = MAP_ROWS * TS   #    720 px
CAM_Y    = (WORLD_H - VIEW_H) // 2   # 40 px fixed vertical crop

# Row indices
R_BT   = (0,1,2,3)   # top buildings
R_TS   = 4            # top sidewalk
R_TRM1 = 5
R_ROAD = (6,7,8)
R_TRM2 = 9
R_BS   = 10           # bottom sidewalk
R_BB   = (11,12,13,14)  # bottom buildings

FACE_TOP_WORLD_Y = 4 * TS    # 192  south face of top buildings starts here
FACE_BOT_WORLD_Y = 11 * TS   # 528  north face of bottom buildings starts here

SAVE_FILE = os.path.join(os.path.dirname(__file__), "savegame.json")

# ══════════════════════════════════════════════════════════════════════════════
#  FONTS
# ══════════════════════════════════════════════════════════════════════════════
def mf(sz, bold=False):
    for n in ["Courier New","Lucida Console","Consolas","Courier"]:
        f = pygame.font.SysFont(n, sz, bold=bold)
        if f: return f
    return pygame.font.Font(None, sz+8)

F = { "xl":mf(28,True), "lg":mf(18,True), "md":mf(13), "sm":mf(10), "xs":mf(8) }

def txt(surf, s, pos, col, fn="md", anchor="topleft", shadow=True):
    f = F[fn]
    if shadow:
        sh = f.render(s, True, (0,0,0))
        surf.blit(sh, sh.get_rect(**{anchor:(pos[0]+1, pos[1]+1)}))
    r2 = f.render(s, True, col)
    rr = r2.get_rect(**{anchor: pos})
    surf.blit(r2, rr)
    return rr

# ══════════════════════════════════════════════════════════════════════════════
#  COLOUR HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def dk(c,a=28): return tuple(max(0,v-a)   for v in c[:3])
def lt(c,a=28): return tuple(min(255,v+a) for v in c[:3])
def bl(a,b,t=.5): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))

def R(s,c,x,y,w,h):
    if w>0 and h>0: pygame.draw.rect(s,c,(int(x),int(y),int(w),int(h)))

def L(s,c,x1,y1,x2,y2,w=1):
    pygame.draw.line(s,c,(int(x1),int(y1)),(int(x2),int(y2)),w)

def C(s,c,x,y,r,w=0):
    pygame.draw.circle(s,c,(int(x),int(y)),r,w)

def P(s,c,pts,w=0):
    pygame.draw.polygon(s,c,[(int(x),int(y)) for x,y in pts],w)

# ══════════════════════════════════════════════════════════════════════════════
#  PALETTE
# ══════════════════════════════════════════════════════════════════════════════
COL = {
    # environment
    "sky":       (120,175,228), "sky2":  (195,222,248), "cloud": (240,245,252),
    "road":      ( 66, 64, 58), "road_mk":(222,200, 45),
    "sidew":     (192,183,167), "curb":  (158,150,136),
    "tram_bed":  ( 82, 78, 72), "rail":  (154,150,146),
    "cross":     (228,222,210),
    # brick / façade
    "br_red":    (152, 68, 40), "br_dk": (120, 50, 28), "mortar":(210,195,172),
    "cream":     (238,220,174), "ochre": (218,175, 82),
    "terra":     (200, 98, 50), "sage":  (128,162,110),
    "grey":      (158,154,146), "white_f":(242,240,234),
    "tan":       (210,192,156), "brown": (150,110, 74),
    # awning
    "aw_red":    (200, 32, 16), "aw_blu":( 28, 92,156),
    "aw_grn":    ( 28,128, 72), "aw_org":(220,120, 20),
    "aw_yel":    (210,185, 20), "aw_tea":( 20,148,148),
    "aw_pur":    (140, 60,180),
    # glass / frame
    "glass":     (168,202,236), "frame": ( 36, 30, 24),
    "wood":      ( 90, 55, 25),
    # UI
    "hud":       ( 18, 16, 14), "hud_fg":(230,212,152),
    "hud_dim":   (110,100, 80),
    "white":     (255,255,255), "black": (  0,  0,  0),
    "gold":      (255,200,  0), "gold_dk":(175,128,  0),
    "green_ui":  ( 60,200, 80), "red_ui":(220, 60, 60),
}
FC_MAP = {
    "f_brick":"br_red","f_cream":"cream","f_ochre":"ochre","f_terra":"terra",
    "f_sage":"sage","f_grey":"grey","f_white":"white_f","f_tan":"tan","f_brown":"brown",
}
AW_MAP = {
    "aw_red":"aw_red","aw_blue":"aw_blu","aw_green":"aw_grn","aw_orange":"aw_org",
    "aw_yellow":"aw_yel","aw_teal":"aw_tea","aw_purple":"aw_pur",
}

# ══════════════════════════════════════════════════════════════════════════════
#  REAL HERENTALSEBAAN SHOPS
# ══════════════════════════════════════════════════════════════════════════════
#  (id, street_num, name, type, side, aw_key, fc_key, floors, subtitle)
_DEFS = [
    ("zeeman",      69, "Wibra",              "clothing", "top","aw_blue",  "f_white", 2, "Mode & Textiel"),
    ("indien",     127, "Cinar Bazar",         "variety",  "bot","aw_orange","f_cream", 2, "Alles voor €2"),
    ("indboutiq",  137, "Indian Boutique",     "clothing", "top","aw_purple","f_ochre", 2, "Ethnische Mode"),
    ("charif",     189, "Bakkerij Charif",     "bakery",   "bot","aw_yellow","f_cream", 3, "Vers brood"),
    ("kruidvat",   229, "Kruidvat",            "pharmacy", "top","aw_green", "f_white", 2, "Drogisterij"),
    ("beobank",    252, "Beobank",             "bank",     "bot","aw_blue",  "f_grey",  3, "Uw bank"),
    ("hammam",     260, "Hammam Borgerhout",   "hammam",   "top","aw_teal",  "f_terra", 3, "حمام · Bain Maure"),
    ("thegarden",  147, "The Garden",          "bar",      "bot","aw_green", "f_sage",  3, "Bar & Terras"),
    ("aladdin",    170, "Patisserie Aladdin",  "patisserie","top","aw_yellow","f_cream", 3, "Marokkaans Gebak"),
    ("frituur",    200, "Frituur de Tram",     "frituur",  "bot","aw_red",   "f_white", 2, "Vlaamse Frieten"),
    ("theehuys",   215, "Theehuys Amal",       "tearoom",  "top","aw_teal",  "f_ochre", 3, "شاي · Thee"),
    ("nachtw",     240, "Nacht Winkel",        "nightshop","bot","aw_purple","f_grey",  2, "24/7 Open"),
    ("borgerHub",  284, "Borger Hub",          "office",   "top","aw_teal",  "f_grey",  4, "Gemeenschapscentrum"),
    ("budgetmkt",  326, "Budget Market",       "market",   "bot","aw_red",   "f_brick", 4, "Uw buurtsuper"),
    ("basic_fit",  360, "Basic-Fit",           "gym",      "top","aw_blue",  "f_grey",  3, "24/7 Fitness"),
    ("newstar",    370, "New Star Kebab",      "kebab",    "bot","aw_red",   "f_terra", 3, "Vers bereid"),
]

def _num_to_wx(n):
    return int((n - 60) / (380 - 60) * (WORLD_W - 1600) + 800)

SHOP_BY_ID = {}
for _d in _DEFS:
    sid,num,name,stype,side,aw,fc,floors,sub = _d
    wx = _num_to_wx(num)
    bw = 130 + floors * 22
    SHOP_BY_ID[sid] = dict(
        id=sid, num=num, name=name, type=stype, side=side,
        aw=aw, fc=fc, floors=floors, subtitle=sub,
        wx=wx, width=bw,
    )

# ══════════════════════════════════════════════════════════════════════════════
#  QUEST FSM
# ══════════════════════════════════════════════════════════════════════════════
QUESTS = {
    "ACT1": dict(
        title="De Droom",
        hint="Ga naar Budget Market — zoek een pand.",
        type="shop", target="budgetmkt",
        reward=None, next="ACT2",
    ),
    "ACT2": dict(
        title="Het Kapitaal",
        hint="Haal €50 sponsorgeld bij The Garden, Patisserie Aladdin en Frituur de Tram.",
        type="collect", targets=["thegarden","aladdin","frituur"], done=[],
        reward="PARAPLU", next="ACT3",
    ),
    "ACT3": dict(
        title="De Vergunning",
        hint="Borger Hub heeft jouw dossier — ga ernaar toe.",
        type="shop", target="borgerHub",
        reward="PERMIT", next="ACT4",
    ),
    "ACT4": dict(
        title="De Ingrediënten",
        hint="Haal spullen bij Bakkerij Charif, Hammam en Theehuys Amal.",
        type="collect", targets=["charif","hammam","theehuys"], done=[],
        reward="KEBAB_SIGN", next="FINALE",
    ),
    "FINALE": dict(
        title="De Opening!",
        hint="Terug naar Budget Market om te openen!",
        type="shop", target="budgetmkt",
        reward=None, next=None,
    ),
}

DIALOGUES = {
    "budgetmkt_ACT1"    : ["Eigenaar: 'Youssef! Het pand op nr.326 is nog vrij.'",
                            "'Huurprijs: €450/maand. Vind eerst wat sponsors op straat.'"],
    "budgetmkt_FINALE"  : ["GEFELICITEERD!", "'New Star Kebab' is open op de Turnhoutsebaan!",
                            "Heel Borgerhout ruikt het al..."],
    "thegarden_ACT2"    : ["Barman: 'Goede zaak, Youssef. Hier €50 van The Garden!'"],
    "aladdin_ACT2"      : ["Aladdin: 'Bismillah — hier €50 van de patisserie.'"],
    "frituur_ACT2"      : ["Frituur: 'Keepe goe! Hier €50 voor jouw droom.'"],
    "borgerHub_ACT3"    : ["Ambtenaar: 'Aanvraag goedgekeurd!'",
                            "'Vergunning nr.2024-KB-0042 — proficiat.'"],
    "charif_ACT4"       : ["Charif: 'Vers pitabrood voor de zaak — hier!'"],
    "hammam_ACT4"       : ["Hammam: 'Kruiden en specerijen — de beste van de stad.'"],
    "theehuys_ACT4"     : ["Amal: 'Munt, kaneel, kardemom — hier zijn ze.'"],
    "generic"           : ["'Succes met je zaak, Youssef!'"],
}

ITEM_DESC = {
    "PARAPLU":    "Stevig paraplu — symbool van bescherming.",
    "PERMIT":     "Officiële vergunning nr.2024-KB-0042.",
    "KEBAB_SIGN": "Het bord voor jouw toekomstige kebabzaak.",
}

# ══════════════════════════════════════════════════════════════════════════════
#  PSEUDO-RANDOM
# ══════════════════════════════════════════════════════════════════════════════
def prng(s): return ((s * 1664525 + 1013904223) & 0xFFFFFFFF) / 0xFFFFFFFF

# ══════════════════════════════════════════════════════════════════════════════
#  TILE MAP GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
def build_tilemap(shops_by_id):
    tm = [[T_VOID]*MAP_COLS for _ in range(MAP_ROWS)]

    # Fill rows
    for c in range(MAP_COLS):
        for r in R_BT:   tm[r][c] = T_BT
        tm[R_TS][c]    = T_SIDEW
        tm[R_TRM1][c]  = T_TRAM
        for r in R_ROAD: tm[r][c] = T_ROAD
        tm[R_TRM2][c]  = T_TRAM
        tm[R_BS][c]    = T_SIDEW
        for r in R_BB:   tm[r][c] = T_BB

    # Zebra crossings every 18 tiles
    for cx in range(8, MAP_COLS, 18):
        for r in R_ROAD: tm[r][cx] = T_CROSS

    # Place shop doors
    for sh in shops_by_id.values():
        dc = sh["wx"] // TS + sh["width"] // (2*TS)
        dc = max(1, min(MAP_COLS-2, dc))
        if sh["side"] == "top":
            tm[3][dc] = T_DOOR_T
        else:
            tm[11][dc] = T_DOOR_B

    return tm

# ══════════════════════════════════════════════════════════════════════════════
#  BUILDING RIBBON GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
FC_FILLS = ["f_cream","f_ochre","f_terra","f_sage","f_brick","f_grey","f_white","f_tan"]
AW_FILLS = ["aw_red","aw_blue","aw_green","aw_orange","aw_yellow","aw_teal","aw_purple"]
ROOF_STYLES = ["flat","cornice","stepped","gable"]

def _pick(seed,lst): return lst[int(prng(seed)*len(lst))]

def build_ribbon(side, shops_by_id):
    ordered = sorted([s for s in shops_by_id.values() if s["side"]==side],
                     key=lambda s: s["wx"])
    out = []; x = 200; seed = 0x1A3C if side=="top" else 0x5D7E
    while x < WORLD_W - 400:
        placed = next((s for s in ordered if abs(s["wx"]-x)<60), None)
        if placed:
            floors = placed["floors"]
            bw     = placed["width"]
            fh     = min(130, 55 + floors*22)
            out.append(dict(
                wx=x, width=bw, floors=floors, fh=fh,
                fc=placed["fc"], aw=placed["aw"],
                name=placed["name"], num=placed["num"], subtitle=placed.get("subtitle",""),
                id=placed["id"], side=side,
                roof=_pick(seed^x, ROOF_STYLES), is_shop=True,
                type=placed.get("type","generic"),
            ))
            x += bw
        else:
            seed = (seed*6364136223846793005+1442695040888963407)&0xFFFFFFFFFFFFFFFF
            fl = 2 + int(prng(seed)*4)
            bw = 80 + int(prng(seed+1)*130)
            for s in ordered:
                if s["wx"]>x and s["wx"]<x+bw+80:
                    bw = max(55, s["wx"]-x-10); break
            if bw < 50: x+=60; continue
            fh = min(130, 52+fl*22)
            out.append(dict(
                wx=x, width=bw, floors=fl, fh=fh,
                fc=_pick(seed+3,FC_FILLS), aw=_pick(seed+4,AW_FILLS),
                name=None, num=None, subtitle="", id=None, side=side,
                roof=_pick(seed+5,ROOF_STYLES), is_shop=False, type="generic",
            ))
            x += bw
    return out

# ══════════════════════════════════════════════════════════════════════════════
#  WORLD-TO-SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def wx2s(wx, cam_x): return int(wx - cam_x)
def wy2s(wy):        return int(wy - CAM_Y)          # apply fixed vertical crop

# ══════════════════════════════════════════════════════════════════════════════
#  DRAW FLOOR TILES  (layer 1)
# ══════════════════════════════════════════════════════════════════════════════
def draw_floor(surf, tilemap, cam_x, tick):
    col_of = {
        T_ROAD: COL["road"], T_SIDEW: COL["sidew"],
        T_TRAM: COL["tram_bed"], T_CROSS: COL["cross"],
        T_DOOR_T: COL["sidew"], T_DOOR_B: COL["sidew"],
        T_BT: COL["br_red"], T_BB: COL["br_red"],
    }
    c0 = max(0, int(cam_x//TS)-1)
    c1 = min(MAP_COLS, c0 + W//TS + 3)
    for row in range(MAP_ROWS):
        for col in range(c0, c1):
            tt = tilemap[row][col]
            if tt == T_VOID: continue
            sx = col*TS - int(cam_x); sy = wy2s(row*TS)
            col_c = col_of.get(tt, COL["road"])
            R(surf, col_c, sx, sy, TS, TS)
            # details
            if tt == T_ROAD:
                # lane markings
                if row == 7:
                    mk_x = sx; off = (tick*2 + col*TS) % (TS*2)
                    R(surf, COL["road_mk"], sx + TS//4 - off%(TS//2), sy+TS//2-2, TS//2, 4)
            elif tt == T_TRAM:
                R(surf, COL["tram_bed"], sx, sy, TS, TS)
                for tx in range(sx, sx+TS, 12): R(surf, (55,50,45), tx, sy+1, 8, TS-2)
                R(surf, COL["rail"], sx, sy+4, TS, 3)
                R(surf, COL["rail"], sx, sy+TS-7, TS, 3)
            elif tt == T_SIDEW:
                # kerb lines
                if row == R_TS: R(surf, COL["curb"], sx, sy+TS-3, TS, 3)
                if row == R_BS: R(surf, COL["curb"], sx, sy, TS, 3)
            elif tt == T_CROSS:
                for sy2 in range(sy, sy+TS, 8):
                    R(surf, COL["cross"], sx, sy2, TS, 4)
            elif tt == T_DOOR_T:
                R(surf, COL["sidew"], sx, sy, TS, TS)
                R(surf, COL["frame"], sx+TS//2-8, sy+TS//2-4, 16, TS//2+4)
                R(surf, COL["wood"], sx+TS//2-6, sy+TS//2-2, 12, TS//2+2)
            elif tt == T_DOOR_B:
                R(surf, COL["sidew"], sx, sy, TS, TS)
                R(surf, COL["frame"], sx+TS//2-8, sy, 16, TS//2+4)
                R(surf, COL["wood"], sx+TS//2-6, sy+2, 12, TS//2+2)

# ══════════════════════════════════════════════════════════════════════════════
#  DRAW BUILDING ROOF (top view, oblique-3D top face)
# ══════════════════════════════════════════════════════════════════════════════
def draw_roof(surf, bld, cam_x):
    sx = wx2s(bld["wx"], cam_x); bw = bld["width"]
    if sx+bw<0 or sx>W: return
    fc  = COL[FC_MAP.get(bld["fc"], "cream")]
    top = bld["side"] == "top"
    # Roof tiles span the building tile rows
    if top:
        sy = wy2s(0); rh = 4*TS          # rows 0-3
    else:
        sy = wy2s(11*TS); rh = 4*TS      # rows 11-14
    R(surf, fc, sx, sy, bw, rh)
    # Brick texture on roof for brick buildings
    if bld["fc"] == "f_brick":
        for ry in range(sy, sy+rh, 12):
            pygame.draw.line(surf, COL["mortar"], (sx,ry),(sx+bw,ry), 1)
            off = 20 if ((ry-sy)//12)%2 else 0
            for cx in range(sx+off, sx+bw, 40):
                pygame.draw.line(surf, COL["mortar"], (cx,ry),(cx,ry+12), 1)
    else:
        # Roof color slightly different (top-face lighter)
        R(surf, lt(fc,12), sx, sy, bw, rh)
        # Roof edge lines
        pygame.draw.rect(surf, dk(fc,25), (sx, sy, bw, rh), 1)
    # Stepped gable silhouette on roof
    if bld["roof"] == "stepped":
        cnc = dk(fc,30)
        for step in range(4):
            sw = bw - step*(bw//5); sx2 = sx+(bw-sw)//2
            sy2 = (sy if top else sy+rh-6) + (-step*6 if top else step*6)
            R(surf, cnc, sx2, sy2, sw, 6)
    # Chimney
    if prng(bld["wx"]^0xAB) > 0.7:
        cx2 = sx + int(prng(bld["wx"])*bw*0.6)+bw//5
        R(surf, (90,82,74), cx2, sy + (2 if top else rh-18), 10, 18)
        R(surf, dk((90,82,74),20), cx2-2, sy + (0 if top else rh-20), 14, 6)

# ══════════════════════════════════════════════════════════════════════════════
#  DRAW BUILDING FACE  (oblique-3D south/north wall  — the KEY 3D effect)
# ══════════════════════════════════════════════════════════════════════════════
def draw_building_face(surf, bld, cam_x, q_id=None):
    sx = wx2s(bld["wx"], cam_x); bw = bld["width"]
    if sx+bw<0 or sx>W: return

    fc    = COL[FC_MAP.get(bld["fc"],  "cream")]
    aw_c  = COL[AW_MAP.get(bld["aw"],  "aw_red")]
    top   = bld["side"] == "top"
    fh    = bld["fh"]             # face height (px)
    fl    = bld["floors"]

    # Face starts at the edge between building tiles and sidewalk
    if top:
        fy = wy2s(FACE_TOP_WORLD_Y)  # face hangs DOWN from here
        fdir = 1                      # downward
    else:
        fy = wy2s(FACE_BOT_WORLD_Y)  # face hangs UP from here
        fdir = -1                     # upward

    # Face bounding box
    face_y = fy if top else fy - fh
    face_h = fh

    # ── Background facade ────────────────────────────────────────────────
    if bld["fc"] == "f_brick":
        R(surf, fc, sx, face_y, bw, face_h)
        for ry in range(face_y, face_y+face_h, 11):
            pygame.draw.line(surf, COL["mortar"], (sx,ry),(sx+bw,ry), 1)
            off = 20 if ((ry-face_y)//11)%2 else 0
            for cx in range(sx+off, sx+bw, 38):
                pygame.draw.line(surf, COL["mortar"], (cx,ry),(cx,ry+11), 1)
    else:
        R(surf, fc, sx, face_y, bw, face_h)

    # ── Pilasters ────────────────────────────────────────────────────────
    pw = 8
    R(surf, lt(fc,14), sx, face_y, pw, face_h)
    R(surf, lt(fc,14), sx+bw-pw, face_y, pw, face_h)

    # ── Upper floor windows (arched) ──────────────────────────────────
    GF_H = min(60, int(face_h*0.45))    # ground floor section height
    UF_H = face_h - GF_H               # upper floor band
    if fl >= 2 and UF_H > 20:
        ww, wh = 22, 32
        cols = max(1, (bw-20)//(ww+16))
        row_count = max(1, fl-1)
        rh2 = max(wh+8, UF_H//row_count)
        for ri in range(row_count):
            ry = face_y + ri*rh2 + (rh2-wh)//2
            if ry + wh > face_y + UF_H: break
            for ci in range(cols):
                wx2 = sx + pw + 10 + ci*(ww+16)
                if wx2+ww > sx+bw-pw-4: break
                # Arched window
                ah = ww//2
                pygame.draw.ellipse(surf, COL["frame"], (wx2, ry, ww, ah*2))
                pygame.draw.ellipse(surf, COL["glass"], (wx2+3,ry+3,ww-6,ah*2-6))
                R(surf, COL["frame"], wx2, ry+ah, ww, wh-ah)
                R(surf, COL["glass"], wx2+3, ry+ah, ww-6, wh-ah-3)
                # Glazing bar
                pygame.draw.line(surf, COL["frame"],
                    (wx2+ww//2,ry+ah),(wx2+ww//2,ry+wh), 2)
                pygame.draw.line(surf, COL["frame"],
                    (wx2+3,ry+ah+(wh-ah)//2),(wx2+ww-3,ry+ah+(wh-ah)//2), 2)
                # Keystone
                kx = wx2+ww//2-4
                P(surf, lt(COL["mortar"],22), [(kx,ry),(kx+8,ry),(kx+6,ry+7),(kx+2,ry+7)])
                # Reflection
                R(surf, lt(COL["glass"],50), wx2+4, ry+ah+2, 4, wh-ah-8)
                # Flower box
                R(surf, (100,70,35), wx2, ry+wh, ww, 5)
                for fi,fc2 in enumerate([(190,50,50),(200,170,10),(190,50,50)]):
                    R(surf, fc2, wx2+3+fi*6, ry+wh-3, 5, 5)

    # ── Ground floor ─────────────────────────────────────────────────────
    gf_y = face_y + UF_H
    gf_h = GF_H
    R(surf, dk(fc, 18), sx, gf_y, bw, gf_h)

    if bld["is_shop"]:
        # Sign board
        sign_h = 20
        R(surf, dk(aw_c,12), sx+2, gf_y, bw-4, sign_h)
        R(surf, lt(aw_c,40), sx+2, gf_y, bw-4, 3)
        ns = F["xs"].render(bld["name"][:20], True, COL["white"])
        surf.blit(ns, ns.get_rect(center=(sx+bw//2, gf_y+sign_h//2)))
        # Subtitle (smaller, second line)
        if bld.get("subtitle"):
            ss = F["xs"].render(bld["subtitle"][:22], True, lt(aw_c,100))
            sr = ss.get_rect(center=(sx+bw//2, gf_y+sign_h-5))
            if sr.bottom <= gf_y+sign_h: surf.blit(ss, sr)

        # Display window
        dw = bw-30; dy2 = gf_y+sign_h+2; dh2 = gf_h-sign_h-28
        if dh2 > 4:
            R(surf, COL["frame"], sx+12, dy2, dw, dh2)
            R(surf, COL["glass"], sx+14, dy2+2, dw-4, dh2-4)
            R(surf, lt(COL["glass"],55), sx+14, dy2+2, 5, dh2-4)
            # Shop-type decorations in window
            t = bld.get("type","generic")
            if t == "bakery":
                for bi in range(3):
                    R(surf, (220,180,80), sx+18+bi*14, dy2+dh2-14, 12, 10)
            elif t == "butcher":
                R(surf, (180,50,50), sx+20, dy2+4, 6, dh2-8)
                R(surf, (180,50,50), sx+32, dy2+4, 6, dh2-8)
            elif t in ("market","nightshop"):
                for bi in range(4):
                    R(surf, (80,160,60), sx+16+bi*12, dy2+4, 10, 8)

        # Awning above display window
        aw_y = gf_y + sign_h - 2
        aw_h = 12
        R(surf, aw_c, sx+4, aw_y, bw-8, aw_h)
        sw = max(8, (bw-8)//6)
        for ii in range(0, bw-8, sw*2):
            R(surf, lt(aw_c,60), sx+4+ii, aw_y, min(sw,bw-8-ii), aw_h)
        R(surf, dk(aw_c,30), sx+4, aw_y+aw_h-4, bw-8, 4)
        # Scallop
        for sc_x in range(sx+4, sx+bw-4, 10):
            C(surf, dk(aw_c,30), sc_x+5, aw_y+aw_h+4, 5)

        # Arched door
        dw2 = 24; door_x = sx+bw//2-dw2//2
        door_y = gf_y + gf_h - 44
        if door_y > gf_y and door_y < gf_y+gf_h-4:
            R(surf, COL["frame"], door_x, door_y, dw2, 44)
            R(surf, COL["wood"],  door_x+3, door_y+3, dw2-6, 41)
            pygame.draw.ellipse(surf, COL["frame"], (door_x, door_y-10, dw2, 20))
            pygame.draw.ellipse(surf, COL["wood"],  (door_x+3, door_y-7, dw2-6,14))
            C(surf, (200,175,55), door_x+dw2-6, door_y+22, 2)
        # Street number
        if bld["num"]:
            ns2 = F["xs"].render(str(bld["num"]), True, COL["hud_fg"])
            surf.blit(ns2, (sx+3, gf_y+gf_h-12))
    else:
        # Residential door
        rdx = sx+bw//2-9; rdy = gf_y+gf_h-34
        if rdy > gf_y:
            R(surf, dk(fc,45), rdx, rdy, 18, 34)
            pygame.draw.ellipse(surf, dk(fc,30), (rdx-2, rdy-9, 22, 18))
            R(surf, COL["frame"], rdx, rdy, 18, 34)
            R(surf, (55,45,36), rdx+3, rdy+3, 12, 31)

    # ── Top cornice or gable ──────────────────────────────────────────────
    cnc = dk(fc, 28)
    cy = face_y
    if bld["roof"] == "gable":
        mid = sx+bw//2
        P(surf, fc, [(sx,cy),(sx+bw,cy),(mid,cy-20)])
        P(surf, cnc, [(sx,cy),(sx+bw,cy),(mid,cy-20)], 2)
    R(surf, cnc, sx, cy, bw, 7)
    R(surf, lt(fc,25), sx, cy, bw, 3)
    for di in range(sx+6, sx+bw-6, 18): R(surf, dk(cnc,22), di, cy-5, 9, 5)

    # ── 2.5-D side face ───────────────────────────────────────────────────
    R(surf, dk(fc,55), sx+bw, face_y, 6, face_h)

    # ── Quest marker ──────────────────────────────────────────────────────
    if q_id and bld.get("id"):
        q = QUESTS.get(q_id, {})
        is_target = (
            (q.get("type")=="shop"    and q.get("target")==bld["id"]) or
            (q.get("type")=="collect" and bld["id"] in q.get("targets",[])
             and bld["id"] not in q.get("done",[]))
        )
        if is_target:
            bob = int(math.sin(pygame.time.get_ticks()*0.004)*4)
            mx  = sx+bw//2
            my  = face_y - 26 + bob
            C(surf, COL["gold"],    mx, my, 12)
            C(surf, COL["gold_dk"], mx, my, 12, 2)
            ms = F["md"].render("!", True, COL["black"])
            surf.blit(ms, ms.get_rect(center=(mx,my)))

# ══════════════════════════════════════════════════════════════════════════════
#  STREET PROPS
# ══════════════════════════════════════════════════════════════════════════════
def draw_lamp(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -10 or sx > W: return
    R(surf, (72,68,62), sx+4, sy-60, 5, 60)
    R(surf, (72,68,62), sx-8, sy-62, 20, 5)
    C(surf, (255,242,180), sx-4, sy-64, 7)
    C(surf, (255,225,100), sx-4, sy-64, 4)

def draw_tree(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -10 or sx > W: return
    R(surf, (90,60,30), sx+8, sy-20, 8, 22)
    C(surf, (40,130,55), sx+12, sy-40, 22)
    C(surf, (50,150,65), sx+4, sy-36, 16)
    C(surf, (60,145,70), sx+18, sy-32, 14)

def draw_bench(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -10 or sx > W: return
    R(surf, (140,100,60), sx, sy-10, 36, 6)
    R(surf, (110,78,40), sx+4, sy-4, 4, 10)
    R(surf, (110,78,40), sx+28, sy-4, 4, 10)

def draw_bin(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -10 or sx > W: return
    R(surf, (38,120,55), sx, sy-22, 14, 22)
    R(surf, (30,100,45), sx, sy-24, 14, 4)

def draw_bollard(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -10 or sx > W: return
    R(surf, (40,40,40), sx+3, sy-14, 8, 14)
    R(surf, (240,200,0),sx+2, sy-16, 10, 4)

def draw_sign(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -10 or sx > W: return
    R(surf, (72,68,62), sx+6, sy-36, 4, 36)
    R(surf, (28,92,156), sx, sy-36, 60, 22)
    R(surf, (255,255,255), sx, sy-36, 60, 2)
    st = F["xs"].render("Turnhoutsebaan", True, COL["white"])
    surf.blit(st, (sx+2, sy-34))
    st2 = F["xs"].render("Borgerhout", True, lt(COL["aw_blu"],80))
    surf.blit(st2, (sx+2, sy-24))

# ══════════════════════════════════════════════════════════════════════════════
#  CHARACTER SPRITES  (4-dir, 2-frame)
# ══════════════════════════════════════════════════════════════════════════════
CHAR_DEFS = {
    # type: (body_col, skin, hair, extra)
    "ouma":        ((155,89,182),(253,187,180),(145,140,135),"cart"),
    "hipster":     ((46,204,113),(253,187,180),(28, 22, 18),"beanie"),
    "youth":       ((52,152,219),(200,155,120),(44, 28, 16),"phone"),
    "shopkeeper":  ((250,250,250),(253,187,180),(44, 28, 16),"apron"),
    "hijab_woman": ((60,160,200),(220,170,130),(28, 22, 18),"hijab"),
    "djellaba_man":((235,220,195),(190,140, 90),(28, 22, 18),"djellaba"),
    "child":       ((255,150, 50),(253,187,180),(80, 50, 25),"small"),
    "delivery":    ((240,120, 20),(240,185,150),(44, 28, 16),"vest"),
}

def draw_char(surf, char_type, wx, world_y, cam_x, frame=0, facing=1, scale=1):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx < -30 or sx > W+30: return
    body,skin,hair,extra = CHAR_DEFS.get(char_type, CHAR_DEFS["youth"])
    small = (extra == "small")
    sc = 0.75 if small else 1.0
    leg_s = int(5*sc); ls = leg_s if frame else -leg_s

    def sr(c,x,y,w,h): R(surf,c,sx+int(x*sc),sy+int(y*sc),max(1,int(w*sc)),max(1,int(h*sc)))
    def sc2(c,x,y,r): C(surf,c,sx+int(x*sc),sy+int(y*sc),max(1,int(r*sc)))

    # Legs
    sr(dk(body,20), -6, -8, 6, 16+ls)
    sr(dk(body,20),  1, -8, 6, 16-ls)
    # Shoes
    sr((30,24,18), -7,  8+ls, 8, 4)
    sr((30,24,18),  1,  8-ls, 8, 4)

    # Body
    if extra == "djellaba":
        sr((230,215,190), -9,-22,18,26)
    elif extra == "apron":
        sr((250,250,250), -8,-22,16,22)
        sr(body, -5,-22,10,20)
    else:
        sr(body, -8,-22,16,20)

    # Arms
    arm_s = -ls//2
    sr(body, -12,-20+arm_s,  5,12)
    sr(body,   7,-20-arm_s,  5,12)

    # Extras
    if extra == "cart":
        sr((170,170,170), 10,-12,20,16)
        sc2((110,110,110),22,4,4); sc2((110,110,110),26,4,4)
    elif extra == "phone":
        sr((20,20,20), 9,-14,6,9)
        sr((100,160,220),10,-13,4,7)
    elif extra == "vest":
        sr((240,120,20),-9,-22,2,20)
        sr((240,120,20),  7,-22,2,20)
    elif extra == "hijab":
        pygame.draw.ellipse(surf, (50,130,175),
            (sx+int(-10*sc),sy+int(-32*sc),int(20*sc),int(24*sc)))

    # Head
    sc2(skin, 0,-30,9)
    # Hair / hat
    if extra == "beanie":
        pygame.draw.ellipse(surf,(230,125,33),(sx-8,sy-42,16,12))
    elif extra == "hijab":
        pass  # already drawn
    else:
        pygame.draw.ellipse(surf, hair, (sx+int(-8*sc),sy+int(-42*sc),int(16*sc),int(13*sc)))

    # Shadow
    shadow_surf = pygame.Surface((18,6), pygame.SRCALPHA)
    shadow_surf.fill((0,0,0,0))
    pygame.draw.ellipse(shadow_surf,(0,0,0,80),(0,0,18,6))
    surf.blit(shadow_surf, (sx-9, sy+12))

# ══════════════════════════════════════════════════════════════════════════════
#  PLAYER SPRITE
# ══════════════════════════════════════════════════════════════════════════════
def draw_player(surf, px, py, cam_x, on_bike, frame, facing):
    sx = wx2s(px, cam_x); sy = wy2s(py)

    if on_bike:
        # Wheels
        for wx2, wy2 in [(-16,6),(16,6)]:
            C(surf,(32,32,32), sx+wx2, sy+wy2, 12)
            C(surf,(75,75,75), sx+wx2, sy+wy2, 12, 2)
            C(surf,(130,130,130),sx+wx2,sy+wy2,4)
        # Spokes
        for ang in range(0,360,60):
            ra = math.radians(ang)
            for wo,wx2,wy2 in [(-16,0,6),(16,0,6)]:
                pygame.draw.line(surf,(90,90,90),
                    (sx+wo+int(math.cos(ra)*4), sy+wy2+int(math.sin(ra)*4)),
                    (sx+wo+int(math.cos(ra)*11),sy+wy2+int(math.sin(ra)*11)),1)
        # Frame
        pygame.draw.line(surf,(50,50,50),(sx-16,sy+6),(sx,sy-6),3)
        pygame.draw.line(surf,(50,50,50),(sx+16,sy+6),(sx,sy-6),3)
        pygame.draw.line(surf,(50,50,50),(sx-16,sy+6),(sx+16,sy+6),3)
        pygame.draw.line(surf,(50,50,50),(sx,sy-6),(sx,sy-14),2)
        R(surf,(55,52,48),sx+facing*6-4,sy-16,8,3)   # handlebar
        # Rider body
        R(surf,(44,55,90), sx-8,sy-28,16,16)
        C(surf,(253,187,180),sx,sy-34,9)
        pygame.draw.ellipse(surf,(208,32,16),(sx-9,sy-46,18,13))  # helmet
        ls = 5 if frame else -3
        R(surf,(44,55,90),sx-4,sy-12,5,14+ls)
        R(surf,(44,55,90),sx+1, sy-12,5,14-ls)
    else:
        ls = 5 if frame else -5
        R(surf,(44,56,88),sx-6,sy-8,6,18+ls)
        R(surf,(44,56,88),sx+1,sy-8,6,18-ls)
        R(surf,(30,24,18),sx-7,sy+10,8,5)
        R(surf,(30,24,18),sx+1,sy+10,8,5)
        R(surf,(220,48,32),sx-9,sy-24,18,18)
        ar_s = -ls//2
        R(surf,(220,48,32),sx-13,sy-23+ar_s,5,14)
        R(surf,(220,48,32),sx+8, sy-23-ar_s,5,14)
        C(surf,(253,187,180),sx,sy-32,9)
        pygame.draw.ellipse(surf,(44,24,16),(sx-8,sy-44,16,13))

    # Shadow
    sh = pygame.Surface((28,8),pygame.SRCALPHA); sh.fill((0,0,0,0))
    pygame.draw.ellipse(sh,(0,0,0,90),(0,0,28,8))
    surf.blit(sh,(sx-14,sy+14))

# ══════════════════════════════════════════════════════════════════════════════
#  TRAM SPRITE
# ══════════════════════════════════════════════════════════════════════════════
TRAM_W = 320; TRAM_H2 = 52

def draw_tram(surf, wx, cam_x, world_y, doors_open=False):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx+TRAM_W<0 or sx>W: return
    # Body
    R(surf,(242,242,242),sx,sy,TRAM_W,TRAM_H2)
    R(surf,(210,210,210),sx,sy,TRAM_W,10)          # roof
    R(surf,(28,95,160),sx,sy+18,TRAM_W,14)         # blue stripe
    R(surf,(240,192,0),sx,sy+15,TRAM_W,3)           # yellow band
    # Cabs
    for cx2 in [sx, sx+TRAM_W-16]:
        R(surf,(210,210,210),cx2,sy,16,TRAM_H2)
        R(surf,COL["glass"],cx2+3,sy+3,10,10)
        R(surf,COL["frame"],cx2,sy+18,16,4)
    # Windows
    for wi in range(4):
        wxx=sx+20+wi*70; R(surf,(20,20,20),wxx,sy+3,26,18)
        R(surf,COL["glass"],wxx+2,sy+5,22,14)
        R(surf,lt(COL["glass"],45),wxx+2,sy+5,3,14)
    # Doors
    for di in [88,192]:
        R(surf,(20,20,20),sx+di,sy+2,40,TRAM_H2-4)
        if doors_open:
            R(surf,(130,128,125),sx+di+2,sy+4,8,TRAM_H2-8)
            R(surf,(130,128,125),sx+di+30,sy+4,8,TRAM_H2-8)
        else:
            R(surf,(145,140,135),sx+di+2,sy+4,17,TRAM_H2-8)
            R(surf,(145,140,135),sx+di+21,sy+4,17,TRAM_H2-8)
    # De Lijn logo
    R(surf,(28,95,160),sx+130,sy+32,52,14)
    dl=F["xs"].render("De Lijn",True,COL["white"])
    surf.blit(dl,dl.get_rect(center=(sx+156,sy+39)))
    # Destination
    R(surf,(12,12,12),sx+18,sy,68,10)
    ds=F["xs"].render("10 Wijnegem",True,(240,192,0))
    surf.blit(ds,(sx+20,sy+1))
    # Wheels
    for wx2 in [sx+20,sx+TRAM_W-46]:
        R(surf,(38,38,38),wx2,sy+TRAM_H2,36,12)
        R(surf,(65,65,65),wx2+2,sy+TRAM_H2+2,32,8)
    # Pantograph
    pygame.draw.line(surf,(150,148,145),(sx+160,sy-8),(sx+140,sy),2)
    pygame.draw.line(surf,(150,148,145),(sx+160,sy-8),(sx+180,sy),2)
    R(surf,(170,168,164),sx+132,sy-10,56,4)

# ══════════════════════════════════════════════════════════════════════════════
#  BUS SPRITE
# ══════════════════════════════════════════════════════════════════════════════
BUS_W=200; BUS_H=52
def draw_bus(surf, wx, cam_x, world_y, direction=1):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx+BUS_W<0 or sx>W: return
    R(surf,(28,142,72),sx,sy,BUS_W,BUS_H)
    R(surf,(22,112,58),sx,sy,BUS_W,8)
    R(surf,(240,192,0),sx,sy+BUS_H-10,BUS_W,10)
    for wi in range(3):
        wx2=sx+20+wi*58; R(surf,(16,16,16),wx2,sy+8,44,24)
        R(surf,COL["glass"],wx2+2,sy+10,40,20)
    R(surf,(16,16,16),sx+10,sy+4,36,28)
    R(surf,COL["glass"],sx+12,sy+6,32,24)
    R(surf,(20,100,50),sx+80,sy+16,50,14)
    bl2=F["xs"].render("De Lijn",True,COL["white"])
    surf.blit(bl2,bl2.get_rect(center=(sx+105,sy+23)))
    for wx2 in [sx+16,sx+BUS_W-44]:
        R(surf,(30,30,30),wx2,sy+BUS_H,38,12)
        R(surf,(58,58,58),wx2+2,sy+BUS_H+2,34,8)

# ══════════════════════════════════════════════════════════════════════════════
#  CAR SPRITES  (3 variants)
# ══════════════════════════════════════════════════════════════════════════════
CAR_COLORS = [(180,30,30),(40,80,180),(60,140,60),(120,80,40),(200,200,50),(80,80,80)]
CAR_W=96; CAR_H=40

def draw_car(surf, wx, cam_x, world_y, variant=0):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    if sx+CAR_W<0 or sx>W: return
    bc = CAR_COLORS[variant % len(CAR_COLORS)]
    R(surf,bc,sx,sy+10,CAR_W,CAR_H-10)
    R(surf,bc,sx+16,sy,CAR_W-32,16)
    R(surf,(180,178,172),sx,sy+10,CAR_W,4)
    # Windows
    R(surf,COL["glass"],sx+20,sy+2,24,14); R(surf,COL["glass"],sx+52,sy+2,24,14)
    # Wheels
    for wx2 in [sx+8,sx+CAR_W-22]:
        C(surf,(28,28,28),wx2+8,sy+CAR_H,10); C(surf,(68,68,68),wx2+8,sy+CAR_H,6)
    # Headlights
    R(surf,(255,255,200),sx+2,sy+16,8,6); R(surf,(200,40,40),sx+CAR_W-10,sy+16,8,6)

# ══════════════════════════════════════════════════════════════════════════════
#  BICYCLE (solo, no rider — for props)
# ══════════════════════════════════════════════════════════════════════════════
def draw_bicycle_prop(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    for dx in [-14,14]: C(surf,(30,30,30),sx+dx,sy,10); C(surf,(80,80,80),sx+dx,sy,10,2)
    pygame.draw.line(surf,(50,50,50),(sx-14,sy),(sx,sy-10),2)
    pygame.draw.line(surf,(50,50,50),(sx+14,sy),(sx,sy-10),2)
    pygame.draw.line(surf,(50,50,50),(sx-14,sy),(sx+14,sy),2)
    R(surf,(55,52,48),sx+4,sy-14,12,3)

# ══════════════════════════════════════════════════════════════════════════════
#  SCOOTER  (delivery)
# ══════════════════════════════════════════════════════════════════════════════
def draw_scooter(surf, wx, cam_x, world_y):
    sx = wx2s(wx, cam_x); sy = wy2s(world_y)
    R(surf,(240,120,20),sx-20,sy-20,50,22)
    R(surf,(200,90,10), sx-20,sy-22,50,4)
    C(surf,(28,28,28),sx-12,sy+4,9); C(surf,(28,28,28),sx+20,sy+4,9)
    R(surf,(55,52,48),sx+10,sy-28,8,8)
    # Box on back
    R(surf,(240,120,20),sx-30,sy-24,18,20)
    F["xs"].render("",True,COL["white"])  # placeholder

# ══════════════════════════════════════════════════════════════════════════════
#  INTERIOR ROOMS
# ══════════════════════════════════════════════════════════════════════════════
INTERIOR_DEFS = {
    "bakery":    dict(floor=(230,215,180), wall=(240,225,190)),
    "butcher":   dict(floor=(200,185,165), wall=(215,200,180)),
    "patisserie":dict(floor=(245,230,200), wall=(255,240,210)),
    "frituur":   dict(floor=(200,190,170), wall=(215,205,185)),
    "tearoom":   dict(floor=(210,195,170), wall=(225,210,185)),
    "nightshop": dict(floor=(180,175,165), wall=(50,48,44)),
    "hammam":    dict(floor=(180,200,210), wall=(160,190,205)),
    "office":    dict(floor=(200,195,185), wall=(215,210,200)),
    "market":    dict(floor=(200,195,180), wall=(215,210,195)),
    "pharmacy":  dict(floor=(220,235,230), wall=(235,248,245)),
    "generic":   dict(floor=(210,200,185), wall=(225,215,200)),
}

def draw_interior(surf, shop_type, shop_name, p_ix, p_iy):
    """Full-screen interior view."""
    R(surf,(14,12,10),0,0,W,VIEW_H)

    idef = INTERIOR_DEFS.get(shop_type, INTERIOR_DEFS["generic"])
    floor_col = idef["floor"]; wall_col = idef["wall"]

    # Room walls
    R(surf, wall_col, 80, 60, W-160, VIEW_H-200)
    # Floor
    floor_y = VIEW_H-200
    R(surf, floor_col, 80, floor_y, W-160, 200)
    # Checkerboard floor
    ts2 = 40
    for fy in range(floor_y, VIEW_H, ts2):
        for fx in range(80, W-80, ts2):
            if ((fy//ts2)+(fx//ts2))%2:
                R(surf, dk(floor_col,12), fx, fy, ts2, ts2)

    # Back wall details
    R(surf, dk(wall_col,15), 80, 60, W-160, 6)  # baseboard top
    R(surf, dk(wall_col,10), 80, floor_y-6, W-160, 6)  # baseboard bottom

    # Shop-specific furniture
    if shop_type in ("bakery","patisserie"):
        # Counter
        R(surf,(180,150,100),200,floor_y-60,300,60)
        R(surf,(200,170,120),200,floor_y-60,300,8)
        # Shelves of bread/pastries
        for si in range(3):
            R(surf,dk(wall_col,8),120,100+si*60,W-280,50)
            for bi in range(6):
                R(surf,(220,185,90),130+bi*60,106+si*60,44,38)
    elif shop_type == "butcher":
        R(surf,(180,150,100),200,floor_y-60,320,60)
        for mi in range(4):
            R(surf,(160,60,60),150+mi*80,130,14,90)
            R(surf,(140,50,50),155+mi*80,140,10,80)
        R(surf,(100,80,70),150,120,8,10)
    elif shop_type == "tearoom":
        for ti in range(3):
            R(surf,(140,100,60),150+ti*160,floor_y-50,80,50)
            R(surf,(160,120,80),150+ti*160,floor_y-52,80,8)
            C(surf,(200,180,150),190+ti*160,floor_y-30,15)
            C(surf,(180,160,130),190+ti*160,floor_y-30,12)
    elif shop_type == "nightshop":
        for ri in range(3):
            R(surf,dk(wall_col,5),120,100+ri*60,W-280,52)
            for gi in range(8):
                col_g = [(200,50,50),(50,150,200),(100,200,50),(220,180,50)][gi%4]
                R(surf,col_g,126+gi*50,106+ri*60,40,40)
    elif shop_type == "hammam":
        R(surf,(80,160,180),80,60,W-160,VIEW_H-260)
        for pi in range(4):
            R(surf,(60,140,165),80+pi*(W-160)//4,60,(W-160)//4,VIEW_H-260)
            if pi%2: R(surf,(50,120,145),80+pi*(W-160)//4,60,4,VIEW_H-260)
        R(surf,(200,210,220),80,floor_y-20,W-160,20)
    elif shop_type == "office":
        for di in range(4):
            R(surf,(100,95,85),130+di*160,floor_y-80,100,80)
            R(surf,dk(floor_col,10),130+di*160+4,floor_y-80,92,74)
            R(surf,(220,215,205),130+di*160+10,floor_y-60,80,30)
    else:  # generic / market
        for si in range(3):
            R(surf,dk(wall_col,8),120,100+si*55,W-280,46)
            for gi in range(6):
                col_g = [(200,60,60),(60,180,80),(220,180,50),(50,120,200)][gi%4]
                R(surf,col_g,126+gi*64,106+si*55,54,32)

    # Shop name header
    R(surf,(18,16,14),0,0,W,55)
    txt(surf, f"  {shop_name}", (W//2, 28), COL["gold"], "lg", "center")
    txt(surf, "ESC = terug naar buiten", (W-16,28), COL["hud_dim"], "xs", "midright")

    # Player inside
    sx2 = max(80+20, min(W-80-20, p_ix))
    sy2 = max(floor_y+10, min(VIEW_H-20, p_iy))
    draw_player(surf, sx2, sy2+CAM_Y, 0, False, 0, 1)  # fixed at cam=0 for interior

    # Counter NPC
    R(surf,(250,250,250), W//2-30, floor_y-68, 60, 68)
    C(surf,(253,187,180), W//2, floor_y-80, 10)
    txt(surf, "Goeiendag!", (W//2, floor_y-105), COL["gold"], "sm", "center")

# ══════════════════════════════════════════════════════════════════════════════
#  HUD
# ══════════════════════════════════════════════════════════════════════════════
def draw_hud(surf, state):
    R(surf, COL["hud"], 0, VIEW_H, W, HUD_H)
    pygame.draw.line(surf,(45,40,34),(0,VIEW_H),(W,VIEW_H),2)
    # Coin
    C(surf,(200,160,0),30,VIEW_H+24,14)
    C(surf,COL["gold"],30,VIEW_H+24,14,2)
    txt(surf,"€",(30,VIEW_H+24),COL["black"],"md","center",False)
    txt(surf,str(state["coins"]),(52,VIEW_H+16),COL["gold"],"lg")
    # Quest
    q = QUESTS.get(state["quest"])
    if q:
        txt(surf,q["title"],(W//2,VIEW_H+8),COL["gold"],"lg","midtop")
        txt(surf,q["hint"],(W//2,VIEW_H+30),COL["hud_dim"],"sm","midtop")
    # Inventory icons
    ix = W-16
    for item in reversed(state["inventory"]):
        R(surf,(50,46,40),ix-36,VIEW_H+8,34,34)
        txt(surf,item[:6],(ix-19,VIEW_H+14),COL["hud_fg"],"xs","center")
        ix -= 40
    # Controls
    txt(surf,"WASD=beweeg  B=fiets  E=praat  I=inv  S=sla op",
        (W//2,VIEW_H+HUD_H-12),COL["hud_dim"],"xs","midbottom")
    # Mode badge
    mode = "🚲 FIETS" if state.get("on_bike") else "🚶 STAP"
    txt(surf,mode,(W-16,VIEW_H+HUD_H-12),COL["hud_fg"],"xs","bottomright")

# ══════════════════════════════════════════════════════════════════════════════
#  DIALOGUE BOX
# ══════════════════════════════════════════════════════════════════════════════
def draw_dialogue(surf, lines, idx):
    if not lines: return
    bx,by,bw,bh = 80,VIEW_H-150,W-160,120
    R(surf,(18,14,10),bx,by,bw,bh)
    pygame.draw.rect(surf,COL["gold"],(bx,by,bw,bh),2)
    line = lines[idx] if idx<len(lines) else ""
    words = line.split()
    cur=""; out=[]
    for w2 in words:
        test=(cur+" "+w2).strip()
        if F["md"].size(test)[0]<bw-32: cur=test
        else: out.append(cur); cur=w2
    if cur: out.append(cur)
    for li,ln in enumerate(out[:3]):
        txt(surf,ln,(bx+16,by+14+li*28),COL["white"],"md",shadow=True)
    if idx<len(lines)-1:
        txt(surf,"▼ E om door te gaan",(bx+bw-12,by+bh-12),COL["hud_dim"],"xs","bottomright")
    else:
        txt(surf,"E om te sluiten",(bx+bw-12,by+bh-12),COL["gold"],"xs","bottomright")

# ══════════════════════════════════════════════════════════════════════════════
#  INVENTORY SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def draw_inventory(surf, state):
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,185)); surf.blit(ov,(0,0))
    R(surf,(22,18,14),120,80,W-240,H-160)
    pygame.draw.rect(surf,COL["gold"],(120,80,W-240,H-160),2)
    txt(surf,"INVENTARIS",(W//2,100),COL["gold"],"xl","midtop")
    txt(surf,f"Geld: €{state['coins']}",(W//2,150),COL["hud_fg"],"lg","midtop")
    for ii,item in enumerate(state["inventory"]):
        iy=200+ii*65; R(surf,(40,36,30),150,iy,W-300,55)
        txt(surf,item,(170,iy+10),COL["gold"],"lg")
        txt(surf,ITEM_DESC.get(item,""),(170,iy+32),COL["hud_dim"],"sm")
    if not state["inventory"]:
        txt(surf,"(leeg)",(W//2,240),COL["hud_dim"],"lg","midtop")
    txt(surf,"I of ESC om te sluiten",(W//2,H-110),COL["hud_dim"],"sm","midtop")

# ══════════════════════════════════════════════════════════════════════════════
#  SAVE / LOAD
# ══════════════════════════════════════════════════════════════════════════════
def save_game(state, player):
    q = QUESTS.get(state["quest"],{})
    data = dict(
        quest=state["quest"],
        quest_done=q.get("done",[]),
        coins=state["coins"],
        inventory=state["inventory"],
        px=player["x"], py=player["y"],
        on_bike=player["on_bike"],
    )
    with open(SAVE_FILE,"w") as f: json.dump(data,f,indent=2)
    state["save_flash"]=120

def load_game(state, player):
    if not os.path.exists(SAVE_FILE): return False
    try:
        with open(SAVE_FILE) as f: d=json.load(f)
        state["quest"]=d.get("quest","ACT1")
        state["coins"]=d.get("coins",0)
        state["inventory"]=d.get("inventory",[])
        player["x"]=d.get("px",3200.0)
        player["y"]=float(R_TS*TS+TS//2)
        player["on_bike"]=d.get("on_bike",True)
        q=QUESTS.get(state["quest"],{})
        if q.get("type")=="collect": q["done"]=d.get("quest_done",[])
        return True
    except Exception as e:
        print(f"Load error: {e}"); return False

# ══════════════════════════════════════════════════════════════════════════════
#  QUEST INTERACTION
# ══════════════════════════════════════════════════════════════════════════════
def try_interact(state, player, shops_by_id):
    px, py = player["x"], player["y"]
    q = QUESTS.get(state["quest"])
    if not q: return None, None

    # Find nearest shop in reach
    nearest = None; best_d = 120
    for sh in shops_by_id.values():
        cx = sh["wx"] + sh["width"]//2
        if abs(px-cx) < best_d:
            # Side check: player must be on the correct sidewalk
            if sh["side"]=="top" and py > R_TS*TS+TS: continue
            if sh["side"]=="bot" and py < R_BS*TS:    continue
            best_d = abs(px-cx); nearest = sh

    if not nearest: return None, None

    sid = nearest["id"]
    # Enter building (interior)
    enter = abs(player["y"] - (R_TS*TS+TS//2)) < TS*1.5 or \
            abs(player["y"] - (R_BS*TS+TS//2)) < TS*1.5

    dlg_key = f"{sid}_{state['quest']}"
    lines = DIALOGUES.get(dlg_key, DIALOGUES["generic"])

    # Advance quest on talk
    if q["type"]=="shop" and q.get("target")==sid:
        rw=q.get("reward")
        if rw and rw not in state["inventory"]: state["inventory"].append(rw)
        nxt=q.get("next")
        state["quest"]=nxt if nxt else "DONE"
        if nxt:
            nq=QUESTS.get(nxt,{})
            if nq.get("type")=="collect": nq["done"]=[]
        bonus={"borgerHub":50,"budgetmkt":200}.get(sid,0)
        state["coins"]+=bonus

    elif q["type"]=="collect" and sid in q.get("targets",[]):
        if sid not in q["done"]:
            q["done"].append(sid); state["coins"]+=50
        if set(q["done"])>=set(q["targets"]):
            rw=q.get("reward")
            if rw and rw not in state["inventory"]: state["inventory"].append(rw)
            nxt=q.get("next"); state["quest"]=nxt if nxt else "DONE"
            if nxt:
                nq=QUESTS.get(nxt,{})
                if nq.get("type")=="collect": nq["done"]=[]

    return lines, nearest

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    shops = SHOP_BY_ID
    tilemap = build_tilemap(shops)
    ribbon_top = build_ribbon("top", shops)
    ribbon_bot = build_ribbon("bot", shops)

    # Props list: (type, wx, world_y)
    props = []
    for i in range(0, WORLD_W, 680):  # lamps
        props.append(("lamp",  i+120, R_TS*TS))
        props.append(("lamp",  i+400, R_BS*TS+TS))
    for i in range(0, WORLD_W, 1400): # trees
        props.append(("tree",  i+200, R_TS*TS+TS-10))
        props.append(("tree",  i+900, R_BS*TS+8))
    for i in range(0, WORLD_W, 2200): # benches
        props.append(("bench", i+350, R_TS*TS+TS-8))
        props.append(("bench", i+1600,R_BS*TS+8))
    for i in range(0, WORLD_W, 1100): # bins
        props.append(("bin",   i+600, R_TS*TS+TS-6))
    for i in range(0, WORLD_W, 3000): # signs
        props.append(("sign",  i+100, R_TS*TS+TS))
    for i in range(0, WORLD_W, 800):  # bollards
        props.append(("bollard", i+50, R_TS*TS+TS-4))
        props.append(("bollard", i+50, R_BS*TS+4))
    for i in range(0, WORLD_W, 1800): # parked bicycles
        props.append(("bicycle", i+300, R_TS*TS+TS))

    # Trams
    trams = [
        {"x":1200.0,"vx": 2.2,"y":float(R_TRM1*TS+8),"doors":False},
        {"x":7000.0,"vx": 2.2,"y":float(R_TRM1*TS+8),"doors":False},
        {"x":3500.0,"vx":-2.2,"y":float(R_TRM2*TS+8),"doors":False},
        {"x":11000.0,"vx":-2.2,"y":float(R_TRM2*TS+8),"doors":False},
    ]
    # Buses
    buses = [
        {"x":4000.0,"vx":1.8,"y":float(R_ROAD[1]*TS+4)},
        {"x":9000.0,"vx":-1.8,"y":float(R_ROAD[1]*TS+4)},
    ]
    # Cars
    cars=[{"x":float(500+i*600),"vx":(1.5+prng(i*7)*1.5)*(1 if i%2==0 else -1),
           "y":float(R_ROAD[0 if i%3==0 else 2]*TS+8),
           "v":i%len(CAR_COLORS)} for i in range(12)]
    # Scooters
    scooters=[{"x":float(1200+i*1800),"vx":(2.5)*(1 if i%2 else -1),
               "y":float(R_ROAD[1]*TS+20)} for i in range(4)]

    # NPCs
    CHAR_TYPES = list(CHAR_DEFS.keys())
    npcs=[]
    rng_seed=0xDEAD
    for i in range(60):
        rng_seed=(rng_seed*1664525+1013904223)&0xFFFFFFFF
        nx=400+int(prng(rng_seed)*(WORLD_W-800))
        ny=float(R_TS*TS+TS//2 if prng(rng_seed+1)>0.5 else R_BS*TS+TS//2)
        npcs.append({"x":float(nx),"y":ny,
                     "vx":(prng(rng_seed+2)-0.5)*1.6,
                     "type":CHAR_TYPES[i%len(CHAR_TYPES)],
                     "frame":0,"ftick":0})

    # Player
    player = {"x":3200.0, "y":float(R_TS*TS+TS//2),
              "vx":0.0,"vy":0.0, "facing":1,
              "on_bike":True,"anim_frame":0,"anim_tick":0}

    # State
    state = {"quest":"ACT1","coins":0,"inventory":[],"save_flash":0,
             "on_bike":True}

    # UI
    cam_x  = 0.0
    dlg_lines = []; dlg_idx = 0
    show_inv   = False
    show_title = True
    in_interior = False
    interior_shop = None
    ix_player = W//2; iy_player = VIEW_H-160

    loaded = load_game(state, player)
    state["on_bike"] = player["on_bike"]

    tick = 0
    running = True
    while running:
        dt = clock.tick(60)/1000.0
        tick += 1

        # ── Events ──────────────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: running=False
            elif ev.type == pygame.KEYDOWN:
                k = ev.key
                if show_title:
                    show_title=False; continue
                if in_interior:
                    if k == pygame.K_ESCAPE:
                        in_interior=False; interior_shop=None
                    continue
                if dlg_lines:
                    if k in (pygame.K_e,pygame.K_SPACE,pygame.K_RETURN):
                        dlg_idx+=1
                        if dlg_idx>=len(dlg_lines): dlg_lines=[]
                    continue
                if k == pygame.K_ESCAPE:
                    if show_inv: show_inv=False
                    else: running=False
                elif k == pygame.K_i:
                    show_inv = not show_inv
                elif k == pygame.K_b:
                    player["on_bike"] = not player["on_bike"]
                    state["on_bike"]  = player["on_bike"]
                elif k in (pygame.K_e, pygame.K_SPACE):
                    if not show_inv:
                        lines, sh = try_interact(state, player, shops)
                        if sh:
                            # Check if close enough to enter
                            dlg_lines=lines or []; dlg_idx=0
                            cx=sh["wx"]+sh["width"]//2
                            if abs(player["x"]-cx)<80:
                                in_interior=True
                                interior_shop=sh
                                ix_player=W//2
                                iy_player=VIEW_H-130
                elif k == pygame.K_s:
                    save_game(state, player)

        # ── Interior movement ───────────────────────────────────────────
        if in_interior and not dlg_lines:
            keys=pygame.key.get_pressed()
            spd=3.0
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]: ix_player-=int(spd*3)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: ix_player+=int(spd*3)
            if keys[pygame.K_UP]    or keys[pygame.K_w]: iy_player-=int(spd*2)
            if keys[pygame.K_DOWN]  or keys[pygame.K_s]: iy_player+=int(spd*2)
            ix_player=max(100,min(W-100,ix_player))
            iy_player=max(VIEW_H-220,min(VIEW_H-40,iy_player))

        # ── Overworld movement ──────────────────────────────────────────
        elif not show_title and not dlg_lines and not show_inv and not in_interior:
            keys=pygame.key.get_pressed()
            spd = 7.5 if player["on_bike"] else 3.8
            fx=fy=0.0
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]: fx-=1; player["facing"]=-1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: fx+=1; player["facing"]= 1
            if keys[pygame.K_UP]    or keys[pygame.K_w]: fy-=1
            if keys[pygame.K_DOWN]  or keys[pygame.K_s]: fy+=1

            if fx!=0 and fy!=0: fx*=0.707; fy*=0.707

            # Momentum
            player["vx"]=player["vx"]*0.75+fx*spd*0.25 if fx!=0 else player["vx"]*0.80
            player["vy"]=player["vy"]*0.75+fy*spd*0.25 if fy!=0 else player["vy"]*0.80
            if abs(player["vx"])<0.05: player["vx"]=0
            if abs(player["vy"])<0.05: player["vy"]=0

            # Tile-collision  X
            nx=player["x"]+player["vx"]
            tx=int(nx//TS); ty=int(player["y"]//TS)
            tx=max(0,min(MAP_COLS-1,tx)); ty=max(0,min(MAP_ROWS-1,ty))
            tile=tilemap[ty][tx]
            allowed = BIKE_OK if player["on_bike"] else WALK_OK
            if tile in SOLID or (not player["on_bike"] and tile not in WALK_OK and tile not in {T_ROAD,T_TRAM,T_CROSS}):
                player["vx"]=0
            else:
                player["x"]=max(TS,min(WORLD_W-TS,nx))

            # Tile-collision  Y
            ny=player["y"]+player["vy"]
            tx2=int(player["x"]//TS); ty2=int(ny//TS)
            tx2=max(0,min(MAP_COLS-1,tx2)); ty2=max(0,min(MAP_ROWS-1,ty2))
            tile2=tilemap[ty2][tx2]
            if tile2 in SOLID:
                player["vy"]=0
            else:
                # Allow bike anywhere on street, walk only sidewalk
                if not player["on_bike"]:
                    road_ok = tile2 in WALK_OK or tile2 in {T_ROAD,T_TRAM,T_CROSS}
                    if road_ok: player["y"]=max(TS,min(WORLD_H-TS,ny))
                    else: player["vy"]=0
                else:
                    player["y"]=max(TS,min(WORLD_H-TS,ny))

            # Animation
            moving=player["vx"]!=0 or player["vy"]!=0
            if moving:
                player["anim_tick"]+=1
                if player["anim_tick"]>9:
                    player["anim_tick"]=0
                    player["anim_frame"]=1-player["anim_frame"]
            else:
                player["anim_frame"]=0

        # ── Camera (smooth follow, X only) ──────────────────────────────
        target_cam=player["x"]-W*0.42
        cam_x+=(target_cam-cam_x)*0.14
        cam_x=max(0,min(WORLD_W-W,cam_x))

        # ── Update vehicles ─────────────────────────────────────────────
        for t in trams:
            t["x"]+=t["vx"]
            if t["vx"]>0 and t["x"]>WORLD_W+TRAM_W: t["x"]=-TRAM_W
            if t["vx"]<0 and t["x"]<-TRAM_W:         t["x"]=WORLD_W+TRAM_W
        for b in buses:
            b["x"]+=b["vx"]
            if b["vx"]>0 and b["x"]>WORLD_W+BUS_W: b["x"]=-BUS_W
            if b["vx"]<0 and b["x"]<-BUS_W:         b["x"]=WORLD_W+BUS_W
        for car in cars:
            car["x"]+=car["vx"]
            if car["vx"]>0 and car["x"]>WORLD_W+CAR_W: car["x"]=-CAR_W
            if car["vx"]<0 and car["x"]<-CAR_W:         car["x"]=WORLD_W+CAR_W
        for sc in scooters:
            sc["x"]+=sc["vx"]
            if sc["vx"]>0 and sc["x"]>WORLD_W+100: sc["x"]=-100
            if sc["vx"]<0 and sc["x"]<-100:         sc["x"]=WORLD_W+100

        # ── Update NPCs ─────────────────────────────────────────────────
        for npc in npcs:
            npc["x"]+=npc["vx"]
            if npc["x"]<200:       npc["vx"]=abs(npc["vx"])
            if npc["x"]>WORLD_W:   npc["vx"]=-abs(npc["vx"])
            npc["ftick"]+=1
            if npc["ftick"]>16: npc["ftick"]=0; npc["frame"]=1-npc["frame"]

        # ════════════════════════════════════════════════════════════════
        #  RENDER
        # ════════════════════════════════════════════════════════════════
        if show_title:
            screen.fill((10,8,6))
            R(screen,COL["hud"],0,0,W,H)
            # Sky gradient
            for yy in range(VIEW_H):
                t2=yy/VIEW_H
                col2=bl(COL["sky"],COL["sky2"],t2)
                pygame.draw.line(screen,col2,(0,yy),(W,yy))
            txt(screen,"TURNHOUTSEBAAN",(W//2,H//2-130),COL["gold"],"xl","center",True)
            txt(screen,"R P G",(W//2,H//2-90),COL["gold_dk"],"xl","center",True)
            txt(screen,"Borgerhout · Antwerpen",(W//2,H//2-50),COL["hud_fg"],"lg","center")
            txt(screen,"Youssef's droom: een kebabzaak op de Turnhoutsebaan",(W//2,H//2+10),COL["hud_dim"],"md","center")
            txt(screen,"Druk op een toets om te starten",(W//2,H//2+80),COL["hud_fg"],"md","center")
            if loaded:
                txt(screen,"✓ Opgeslagen spel gevonden",(W//2,H//2+110),COL["green_ui"],"sm","center")
            txt(screen,"WASD=beweeg  B=fiets/stap  E=praat  S=sla op",(W//2,H-30),COL["hud_dim"],"xs","midbottom")
            pygame.display.flip(); continue

        if in_interior and interior_shop:
            draw_interior(screen, interior_shop.get("type","generic"),
                         interior_shop["name"], ix_player, iy_player)
            if dlg_lines: draw_dialogue(screen, dlg_lines, dlg_idx)
            if state.get("save_flash",0)>0:
                state["save_flash"]-=1
                txt(screen,"✓ OPGESLAGEN",(W//2,VIEW_H-40),COL["green_ui"],"lg","midtop",True)
            draw_hud(screen, state)
            pygame.display.flip(); continue

        # ── Layer 1: Sky ─────────────────────────────────────────────────
        for yy in range(VIEW_H):
            t2 = yy/VIEW_H
            col2 = bl(COL["sky"], COL["sky2"], t2*0.5)
            pygame.draw.line(screen, col2, (0,yy),(W,yy))
        # Clouds (slow parallax)
        cx_base=int(cam_x*0.22)
        for ci in range(10):
            seed2=ci*137
            cx2=(int(prng(seed2)*W*3)-cx_base)%(W*3)-W//3
            cy2=int(prng(seed2+1)*30)+8
            cw2=int(prng(seed2+2)*90)+50; ch2=int(prng(seed2+3)*22)+12
            if cx2>W: continue
            pygame.draw.ellipse(screen,COL["cloud"],(cx2,cy2,cw2,ch2))
            pygame.draw.ellipse(screen,COL["cloud"],(cx2-cw2//4,cy2+6,cw2//2,ch2//2))

        # ── Layer 2: Building roofs (all) ────────────────────────────────
        for bld in ribbon_top + ribbon_bot:
            draw_roof(screen, bld, int(cam_x))

        # ── Layer 3: Floor tiles ─────────────────────────────────────────
        draw_floor(screen, tilemap, cam_x, tick)

        # ── Layer 4: Top building south faces (3D wall) ──────────────────
        for bld in ribbon_top:
            draw_building_face(screen, bld, int(cam_x), state["quest"])

        # ── Layer 5: Bottom building north faces ─────────────────────────
        for bld in ribbon_bot:
            draw_building_face(screen, bld, int(cam_x), state["quest"])

        # ── Layer 6: Y-sorted entities ───────────────────────────────────
        entities = []

        # Props (by world_y for sort)
        for ptype, pwx, pwy in props:
            psy = pwy; entities.append((psy, ptype, pwx, pwy))

        # NPCs
        for npc in npcs:
            entities.append((npc["y"], "npc", npc))

        # Vehicles
        for t in trams:    entities.append((t["y"]+TRAM_H2//2, "tram", t))
        for b in buses:    entities.append((b["y"]+BUS_H//2,   "bus",  b))
        for car in cars:   entities.append((car["y"]+CAR_H//2, "car",  car))
        for sc in scooters:entities.append((sc["y"]+20,        "scoot",sc))

        # Player
        entities.append((player["y"], "player", None))

        entities.sort(key=lambda e: e[0])

        for e in entities:
            ky = e[0]
            if e[1] in ("lamp","tree","bench","bin","sign","bollard","bicycle"):
                pwx=e[2]; pwy=e[3]
                if   e[1]=="lamp":    draw_lamp(screen, pwx, int(cam_x), pwy)
                elif e[1]=="tree":    draw_tree(screen, pwx, int(cam_x), pwy)
                elif e[1]=="bench":   draw_bench(screen, pwx, int(cam_x), pwy)
                elif e[1]=="bin":     draw_bin(screen, pwx, int(cam_x), pwy)
                elif e[1]=="sign":    draw_sign(screen, pwx, int(cam_x), pwy)
                elif e[1]=="bollard": draw_bollard(screen, pwx, int(cam_x), pwy)
                elif e[1]=="bicycle": draw_bicycle_prop(screen, pwx, int(cam_x), pwy)
            elif e[1]=="npc":
                npc=e[2]
                draw_char(screen,npc["type"],npc["x"],npc["y"],int(cam_x),
                          npc["frame"],1 if npc["vx"]>=0 else -1)
            elif e[1]=="tram":
                t=e[2]; draw_tram(screen,t["x"],int(cam_x),t["y"],t["doors"])
            elif e[1]=="bus":
                b=e[2]; draw_bus(screen,b["x"],int(cam_x),b["y"])
            elif e[1]=="car":
                car=e[2]; draw_car(screen,car["x"],int(cam_x),car["y"],car["v"])
            elif e[1]=="scoot":
                sc=e[2]; draw_scooter(screen,sc["x"],int(cam_x),sc["y"])
            elif e[1]=="player":
                draw_player(screen,player["x"],player["y"],int(cam_x),
                            player["on_bike"],player["anim_frame"],player["facing"])

        # ── HUD ──────────────────────────────────────────────────────────
        draw_hud(screen, state)

        # ── Interact hint ─────────────────────────────────────────────────
        if not dlg_lines and not show_inv:
            for sh in shops.values():
                cx=sh["wx"]+sh["width"]//2
                if abs(player["x"]-cx)<100:
                    if (sh["side"]=="top" and player["y"]<=R_TS*TS+TS) or \
                       (sh["side"]=="bot" and player["y"]>=R_BS*TS):
                        txt(screen,f"E — praat / ga naar binnen: {sh['name']}",
                            (W//2,VIEW_H-18),COL["gold"],"sm","midbottom",True)
                        break

        # ── Dialogue / Inventory / Save flash ────────────────────────────
        if dlg_lines:      draw_dialogue(screen, dlg_lines, dlg_idx)
        if show_inv:       draw_inventory(screen, state)
        if state.get("save_flash",0)>0:
            state["save_flash"]-=1
            txt(screen,"✓ OPGESLAGEN",(W//2,VIEW_H-45),COL["green_ui"],"lg","midtop",True)

        pygame.display.flip()

    pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()
