#!/usr/bin/env python3
"""Draw the World News front page for Thursday 19 November 2026.

VISUAL REVISION edition (2026-11-20): same ten verified stories, same
facts, same numbers as the Detailed edition (commit 0162bb66) — ONLY the
presentation is rebuilt from the top-10/top-50 research in
revision-spec.md (leaderboard 16:13 WIB, 15 feed images studied):
  1 giant serif date masthead + "THE WORLD IN ONE DAY" kicker + subline,
  2 number strip (6 numbers, all from our own verified facts),
  3 geographic region tabs (counts sum to 10),
  4 three leads with big coloured scenes + caption strips,
  5 seven medium cards, every one with a big coloured illustration,
  6 dark navy world map, 10 numbered pins, caption + legend,
  7 DATE CHECK box, warm cream paper + serif headlines everywhere,
  8 IN BRIEF recap (same ten stories, NOT new stories) beside the map,
  9 footer source line (no per-story outlet is recorded for News 19,
     so sources are stated in the footer only — nothing is guessed).
ALSO ON edition (2026-11-20, same ten stories, same facts — presentation
only, plus a new ALSO ON band): 27 verified one-line briefs from 19 Nov
2026 reporting (28 verified, #8 Mongolia not used — weakest outlet chain;
#7 Denmark shown WITHOUT the vote tally, which is on the banned-numbers
list), in a 3-column x 9-row band between the map and DATE CHECK. Vertical
budget rebalanced to stay 1024px: masthead/strip/tabs tightened a few px,
lead scenes 94->82, medium rows 140->128, map 114->88. The number-strip
defect (labels "28" and "3rd" running together) is fixed by wrapping each
label to at most 2 lines inside its cell.
Display order is renumbered for the new lead order, as in the News 20
rebuild: 01 Shenzhen, 02 ICJ, 03 Anthropic, 04 Gulf, 05 COP31,
06 Van Gogh, 07 Crimea, 08 Bangladesh, 09 North Korea, 10 Hormuz.
Pure PIL, no network, fully deterministic. Writes entry.png (1024x1024).
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 36
CW = W - 2 * M
PAPER = (250, 243, 228)
PANEL = (253, 250, 242)
INK = (26, 26, 26)
RED = (176, 18, 18)
NAVY = (16, 36, 86)
BLUE = (24, 62, 140)
GREY = (110, 104, 92)
RULE = (26, 26, 26)
GREEN = (34, 120, 60)
LIGHT = (238, 230, 212)
LAND = (233, 224, 196)
LANDLINE = (198, 188, 158)
GOLD = (196, 138, 20)
TEAL = (14, 110, 110)

NOTO = "/usr/share/fonts/truetype/noto"


def F(name, size):
    return ImageFont.truetype(os.path.join(NOTO, name), size)


BLACK = "NotoSans-Black.ttf"
BOLD = "NotoSans-Bold.ttf"
REG = "NotoSans-Regular.ttf"
ITAL = "NotoSans-Italic.ttf"
SERIF = "NotoSerif-Bold.ttf"
SERIFB = "NotoSerif-Black.ttf"
SERIFD = "NotoSerifDisplay-Black.ttf"
SERIFDI = "NotoSerifDisplay-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tag(x, y, num, label):
    d.text((x, y), num, font=F(BOLD, 12), fill=RED)
    d.text((x + 26, y + 1), label, font=F(BOLD, 10), fill=GREY)


def gradient(x, y, w, h, top, bot, bands=8):
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.rectangle([x, y + i * h / bands, x + w,
                     y + (i + 1) * h / bands + 1], fill=col)


def speckle(x, y, w, h, n, cols, seed):
    """Deterministic print grain inside one illustration area."""
    rng = random.Random(seed)
    for i in range(n):
        sx = x + rng.randrange(w)
        sy = y + rng.randrange(h)
        col = rng.choice(cols)
        if i % 4 == 0:
            d.rectangle([sx, sy, sx + 1, sy + 1], fill=col)
        else:
            d.point((sx, sy), fill=col)


def caption_strip(x, y, w, text):
    d.rectangle([x, y - 18, x + w, y], fill=(8, 28, 44))
    d.text((x + 8, y - 15), text, font=F(BOLD, 10), fill=(255, 255, 255))


def blast_star(cx, cy, r):
    pts = []
    for i in range(12):
        ang = i * 30 * math.pi / 180
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40), outline=RED)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
              fill=RED)


CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 70), (-95, 69), (-85, 66), (-75, 62), (-65, 58),
     (-55, 47), (-60, 44), (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-95, 18),
     (-105, 20), (-112, 28), (-120, 34), (-124, 42), (-125, 50), (-135, 58), (-150, 60), (-165, 60)],
    [(-58, 64), (-52, 60), (-42, 60), (-32, 68), (-22, 70), (-30, 76), (-45, 76), (-55, 72)],
    [(-80, 10), (-77, 4), (-70, 10), (-62, 10), (-52, 5), (-50, -2), (-40, -5), (-35, -8),
     (-40, -18), (-48, -25), (-57, -33), (-65, -42), (-70, -50), (-73, -42), (-72, -30),
     (-70, -18), (-77, -8), (-80, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (12, 56), (18, 56), (21, 55),
     (24, 58), (28, 60), (30, 62), (40, 68), (44, 66), (40, 60), (35, 55), (30, 50), (28, 45),
     (23, 40), (19, 42), (12, 44), (8, 39), (3, 38), (-2, 37)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31), (33, 28),
     (35, 22), (40, 15), (44, 12), (51, 11), (48, 5), (42, -5), (40, -12), (35, -20), (32, -28),
     (26, -34), (19, -35), (16, -28), (13, -18), (12, -8), (9, -1), (8, 4), (-8, 5), (-13, 8)],
    [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74),
     (120, 72), (130, 71), (140, 72), (150, 70), (160, 68), (170, 66), (178, 65), (170, 60),
     (162, 56), (158, 52), (150, 48), (142, 44), (138, 38), (130, 33), (127, 30), (122, 28),
     (120, 22), (112, 20), (108, 12), (105, 8), (100, 6), (98, 10), (95, 16), (92, 21), (88, 22),
     (82, 16), (78, 8), (76, 10), (72, 20), (68, 23), (62, 25), (58, 26), (54, 27), (50, 29),
     (48, 30), (44, 32), (42, 38), (40, 42), (36, 36), (33, 38), (30, 40), (28, 45), (30, 50), (28, 55)],
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -11), (140, -17), (136, -15), (132, -12), (126, -14), (120, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 52)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44), (141, 40), (138, 36), (135, 33)],
    [(167, -45), (170, -42), (173, -38), (175, -36), (178, -38), (176, -41), (172, -43), (168, -46)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3), (109, -1)],
    [(95, 5), (98, 2), (102, -2), (105, -5), (104, -3), (100, 0)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -22)],
]

# pins: (number, lon, lat) — display order (see docstring).
# 03 Anthropic pinned at San Francisco (HQ); 06 Van Gogh at New York;
# 04 Gulf at Qeshm (55,28) and 10 Hormuz nudged to (59,25) so the two
# pins do not sit on top of each other. Positions are approximate.
PINS = [
    (1, 114, 22), (2, 4, 52), (3, -122, 38), (4, 55, 28), (5, 31, 37),
    (6, -74, 41), (7, 34, 45), (8, 90, 24), (9, 127, 40), (10, 59, 25),
]


def draw_source(x, y, outlet):
    # hand-drawn check: NotoSans has no U+2713 glyph (it rendered as a box)
    f = F(BOLD, 9)
    d.line([(x, y + 7), (x + 3, y + 10), (x + 8, y + 2)], fill=GREEN,
           width=2)
    d.text((x + 11, y), "CONFIRMED", font=f, fill=GREEN)
    w = d.textlength("CONFIRMED", font=f)
    d.text((x + 11 + w + 5, y), "\u00b7 " + outlet, font=f, fill=GREY)


# ---------------------------------------------------------------- lead scenes
def scene_summit(x, y, w, h):
    """Shenzhen at dusk: three flags above three leaders at one table."""
    gradient(x, y, w, h, (26, 40, 92), (214, 122, 62), 8)
    speckle(x, y, w, h // 2, 500, [(40, 60, 120), (230, 150, 90), (255, 255, 255)], 11)
    for (sx, sy) in [(0.06, 0.15), (0.18, 0.08), (0.3, 0.2), (0.85, 0.1),
                     (0.93, 0.22), (0.72, 0.06), (0.5, 0.12), (0.62, 0.2)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                   y + h * sy + 1], fill=(255, 255, 255))
    # Shenzhen skyline silhouettes at the far edges
    for (tx, tw, th) in [(0.01, 0.07, 0.34), (0.09, 0.05, 0.44),
                         (0.86, 0.06, 0.40), (0.93, 0.06, 0.30)]:
        d.rectangle([x + w * tx, y + h * (0.68 - th), x + w * (tx + tw),
                     y + h * 0.68], fill=(20, 30, 70))
        for wy in range(2):
            d.rectangle([x + w * (tx + 0.015), y + h * (0.68 - th) + 6 + wy * 10,
                         x + w * (tx + 0.03), y + h * (0.68 - th) + 10 + wy * 10],
                        fill=(255, 210, 110))
    # three flags hanging from the top: US, China, Russia
    fw, fh = w * 0.26, 24
    # US: stripes + canton
    ux = x + w * 0.04
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([ux, y + 4 + i * fh // 7, ux + fw,
                     y + 4 + (i + 1) * fh // 7], fill=col)
    d.rectangle([ux, y + 4, ux + fw * 0.45, y + 4 + fh * 4 // 7],
                fill=(60, 59, 110))
    # China: red field, yellow star
    cx = x + w * 0.37
    d.rectangle([cx, y + 4, cx + fw, y + 4 + fh], fill=(222, 41, 16))
    sx, sy = cx + 13, y + 15
    d.polygon([(sx, sy - 7), (sx + 2, sy - 2), (sx + 7, sy - 2),
               (sx + 3, sy + 2), (sx + 4, sy + 7), (sx, sy + 3),
               (sx - 4, sy + 7), (sx - 3, sy + 2), (sx - 7, sy - 2),
               (sx - 2, sy - 2)], fill=(255, 222, 0))
    # Russia: white / blue / red
    rx = x + w * 0.70
    d.rectangle([rx, y + 4, rx + fw, y + 4 + fh // 3], fill=(255, 255, 255))
    d.rectangle([rx, y + 4 + fh // 3, rx + fw, y + 4 + 2 * fh // 3],
                fill=(0, 57, 166))
    d.rectangle([rx, y + 4 + 2 * fh // 3, rx + fw, y + 4 + fh],
                fill=(213, 0, 50))
    # three leaders: heads + dark suits behind a table
    skins = [(232, 190, 160), (222, 182, 148), (235, 200, 170)]
    for i, fx in enumerate([0.2, 0.5, 0.8]):
        hx = x + w * fx
        hy = y + h * 0.52
        d.ellipse([hx - 11, hy - 11, hx + 11, hy + 11], fill=skins[i],
                  outline=INK, width=1)
        d.pieslice([hx - 16, hy - 14, hx + 16, hy + 6], 180, 360,
                   fill=(70, 60, 55) if i != 1 else (40, 40, 40))
        d.polygon([(hx - 18, y + h - 18), (hx - 14, hy + 8),
                   (hx + 14, hy + 8), (hx + 18, y + h - 18)],
                  fill=(28, 28, 40))
        d.polygon([(hx - 5, hy + 9), (hx, hy + 20), (hx + 5, hy + 9)],
                  fill=(255, 255, 255))
        d.polygon([(hx - 3, hy + 12), (hx + 3, hy + 12), (hx, hy + 22)],
                  fill=RED if i != 1 else (0, 57, 166))
    # table + papers
    d.rectangle([x, y + h - 30, x + w, y + h - 18], fill=(96, 62, 38))
    d.rectangle([x + w * 0.12, y + h - 28, x + w * 0.3, y + h - 21],
                fill=(255, 255, 255))
    d.rectangle([x + w * 0.68, y + h - 28, x + w * 0.86, y + h - 21],
                fill=(255, 255, 255))
    caption_strip(x, y + h, w, "SHENZHEN \u00b7 APEC 2026 \u2014 TRUMP \u00b7 XI \u00b7 PUTIN")


def scene_court(x, y, w, h):
    """The Hague: courthouse facade with the scales of justice."""
    gradient(x, y, w, h, (208, 220, 236), (168, 188, 214), 8)
    speckle(x, y, w, h // 2, 400, [(180, 200, 225), (150, 175, 205)], 12)
    # courthouse: steps, columns, pediment
    bx, bw = x + w * 0.14, w * 0.72
    base = y + h - 18
    d.rectangle([bx - 8, base - 6, bx + bw + 8, base], fill=(150, 150, 150))
    d.rectangle([bx - 4, base - 12, bx + bw + 4, base - 6],
                fill=(170, 170, 170))
    d.rectangle([bx, base - 52, bx + bw, base - 12], fill=(238, 232, 218),
                outline=INK, width=1)
    for i in range(6):
        cx = bx + bw * (0.1 + i * 0.16)
        d.rectangle([cx, base - 50, cx + bw * 0.05, base - 14],
                    fill=(250, 246, 236), outline=INK, width=1)
    d.rectangle([bx, base - 58, bx + bw, base - 52], fill=(226, 220, 204),
                outline=INK, width=1)
    d.polygon([(bx - 6, base - 58), (bx + bw * 0.5, base - 80),
               (bx + bw + 6, base - 58)], fill=(232, 226, 210), outline=INK)
    d.ellipse([bx + bw * 0.46, base - 74, bx + bw * 0.54, base - 64],
              fill=RED, outline=INK, width=1)
    d.line([bx + bw * 0.5, base - 80, bx + bw * 0.5, base - 94], fill=INK,
           width=2)
    d.polygon([(bx + bw * 0.5, base - 94), (bx + bw * 0.5 + 15, base - 91),
               (bx + bw * 0.5, base - 88)], fill=RED)
    for (clx, cly) in [(0.06, 0.12), (0.82, 0.08)]:
        d.ellipse([x + w * clx, y + h * cly, x + w * clx + 34, y + h * cly + 10],
                  fill=(255, 255, 255))
    d.rectangle([bx + bw * 0.44, base - 34, bx + bw * 0.56, base - 14],
                fill=(60, 50, 40))
    # two trees flanking the courthouse
    for tx in [x + w * 0.02, x + w * 0.90]:
        d.ellipse([tx, y + h * 0.42, tx + w * 0.08, y + h * 0.72],
                  fill=(34, 90, 50))
        d.rectangle([tx + w * 0.03, y + h * 0.70, tx + w * 0.05,
                     y + h * 0.80], fill=(90, 60, 30))
    # scales of justice, large, in front of the facade
    cx = x + w * 0.5
    sy = y + h * 0.30
    d.line([cx, sy, cx, sy + 44], fill=(120, 90, 20), width=5)
    d.line([cx - 34, sy + 6, cx + 34, sy + 6], fill=(120, 90, 20), width=5)
    d.line([cx - 34, sy + 6, cx - 34, sy + 26], fill=(120, 90, 20), width=3)
    d.line([cx + 34, sy + 6, cx + 34, sy + 26], fill=(120, 90, 20), width=3)
    d.pieslice([cx - 46, sy + 26, cx - 22, sy + 42], 0, 180,
               fill=(255, 200, 40), outline=(120, 90, 20))
    d.pieslice([cx + 22, sy + 26, cx + 46, sy + 42], 0, 180,
               fill=(255, 200, 40), outline=(120, 90, 20))
    d.ellipse([cx - 5, sy - 5, cx + 5, sy + 5], fill=RED)
    d.rectangle([cx - 16, sy + 44, cx + 16, sy + 48], fill=(120, 90, 20))
    caption_strip(x, y + h, w, "THE HAGUE \u00b7 THE WORLD COURT")


def scene_ipo(x, y, w, h):
    """New York: rising market candles and the record IPO figure."""
    gradient(x, y, w, h, (16, 36, 86), (24, 62, 140), 8)
    speckle(x, y, w, h, 450, [(40, 80, 160), (90, 130, 200)], 13)
    for gy in range(1, 4):
        d.line([x, y + h * gy / 4, x + w, y + h * gy / 4],
               fill=(60, 90, 160), width=1)
    for gx in range(1, 6):
        d.line([x + w * gx / 6, y, x + w * gx / 6, y + h],
               fill=(60, 90, 160), width=1)
    # rising candlesticks, right of the figure panel
    candles = [(0.52, 0.42, 0.26), (0.63, 0.34, 0.22), (0.74, 0.26, 0.28),
               (0.85, 0.16, 0.24)]
    for (fx, top, ht) in candles:
        bx = x + w * fx
        col = (40, 180, 90) if fx < 0.8 else (60, 200, 110)
        d.line([bx + 7, y + h * (top - 0.08), bx + 7, y + h * (top + ht + 0.06)],
               fill=col, width=2)
        d.rectangle([bx, y + h * top, bx + 14, y + h * (top + ht)], fill=col)
    # rising arrow under the figure panel
    d.line([x + w * 0.5, y + h * 0.68, x + w * 0.9, y + h * 0.34],
           fill=(255, 210, 60), width=4)
    d.polygon([(x + w * 0.9, y + h * 0.34), (x + w * 0.83, y + h * 0.32),
               (x + w * 0.88, y + h * 0.43)], fill=(255, 210, 60))
    # ticker tape above the caption strip
    for i in range(12):
        tx = x + 4 + i * (w - 8) // 12
        col = (40, 180, 90) if i % 3 else (220, 60, 60)
        d.rectangle([tx, y + h - 26, tx + (w - 8) // 12 - 3, y + h - 20],
                    fill=col)
    # solid panel behind the figure so candles never strike the text
    d.rectangle([x + 6, y + 4, x + 168, y + 58], fill=(10, 24, 60),
                outline=(255, 210, 60), width=1)
    d.text((x + 12, y + 8), "$79.4bn", font=F(SERIFB, 28),
           fill=(255, 255, 255))
    d.text((x + 12, y + 40), "RECORD IPO", font=F(BOLD, 11),
           fill=(255, 210, 60))
    caption_strip(x, y + h, w, "NEW YORK \u00b7 NASDAQ \u2014 RECORD $79.4BN IPO")


# ---------------------------------------------------------------- medium tiles
def tile_gulf(x, y, w, h):
    gradient(x, y, w, h, (10, 60, 80), (6, 34, 52), 6)
    speckle(x, y, w, h, 280, [(30, 120, 140), (90, 180, 200)], 21)
    # oil rig silhouette
    d.rectangle([x + w * 0.58, y + h * 0.3, x + w * 0.86, y + h * 0.42],
                fill=(10, 12, 16))
    d.line([x + w * 0.62, y + h * 0.42, x + w * 0.58, y + h * 0.9],
           fill=(10, 12, 16), width=3)
    d.line([x + w * 0.82, y + h * 0.42, x + w * 0.86, y + h * 0.9],
           fill=(10, 12, 16), width=3)
    d.line([x + w * 0.68, y + h * 0.1, x + w * 0.68, y + h * 0.3],
           fill=(10, 12, 16), width=3)
    d.polygon([(x + w * 0.68, y + h * 0.06), (x + w * 0.8, y + h * 0.12),
               (x + w * 0.68, y + h * 0.18)], fill=RED)
    # missile streak + blast
    d.line([x + w * 0.06, y + h * 0.7, x + w * 0.34, y + h * 0.3],
           fill=(255, 140, 40), width=4)
    d.line([x + w * 0.06, y + h * 0.7, x + w * 0.34, y + h * 0.3],
           fill=(255, 210, 120), width=2)
    blast_star(x + w * 0.36, y + h * 0.28, 8)
    for wy in (0.82, 0.9):
        d.line([x + 4, y + h * wy, x + w - 4, y + h * wy],
               fill=(90, 160, 190), width=2)
    # small patrol boat, lower left
    d.rectangle([x + w * 0.06, y + h * 0.68, x + w * 0.2, y + h * 0.76],
                fill=(220, 220, 220))
    d.line([x + w * 0.12, y + h * 0.68, x + w * 0.12, y + h * 0.52],
           fill=(220, 220, 220), width=2)


def tile_cop(x, y, w, h):
    gradient(x, y, w, h, (150, 205, 225), (240, 235, 205), 6)
    speckle(x, y, w, h, 280, [(170, 220, 235), (255, 220, 120)], 22)
    cx, cy, r = x + w * 0.38, y + h * 0.52, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 220, 240),
              outline=BLUE, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=BLUE,
              width=1)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=1)
    sx, sy = x + w * 0.78, y + h * 0.22
    for k in range(8):
        ang = k * 45 * math.pi / 180
        d.line([sx + 8 * math.cos(ang), sy + 8 * math.sin(ang),
                sx + 14 * math.cos(ang), sy + 14 * math.sin(ang)],
               fill=(240, 170, 20), width=2)
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 200, 40),
              outline=(240, 170, 20))
    lx, ly = x + w * 0.82, y + h * 0.82
    d.polygon([(lx, ly), (lx + 18, ly - 5), (lx + 15, ly + 10)], fill=GREEN)
    d.line([lx, ly, lx + 16, ly + 9], fill=GREEN, width=2)
    # clouds, top left
    d.ellipse([x + w * 0.04, y + h * 0.08, x + w * 0.2, y + h * 0.2],
              fill=(255, 255, 255))
    d.ellipse([x + w * 0.12, y + h * 0.04, x + w * 0.26, y + h * 0.16],
              fill=(255, 255, 255))


def tile_vangogh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 180, 220))
    speckle(x, y, w, h, 280, [(160, 195, 235), (255, 215, 90)], 23)
    d.rectangle([x, y, x + w, y + h], outline=GOLD, width=4)
    d.ellipse([x + w - 26, y + 6, x + w - 12, y + 20], fill=(255, 230, 120))
    tx, ty = x + w * 0.45, y + h - 8
    d.line([tx, ty, tx, ty - 22], fill=(90, 60, 30), width=4)
    for dx, dy in ((-11, -26), (0, -31), (11, -26), (-6, -19), (6, -19)):
        d.ellipse([tx + dx - 6, ty + dy - 6, tx + dx + 6, ty + dy + 6],
                  fill=(255, 200, 40))
    d.rectangle([x + 4, y + h - 10, x + w - 4, y + h - 4], fill=(80, 140, 70))
    d.text((x + w - 52, y + h - 22), "$190.4m", font=F(BOLD, 11),
           fill=(255, 255, 255))
    # village houses, lower left
    for hx in (0.06, 0.2):
        bx = x + w * hx
        d.rectangle([bx, y + h * 0.62, bx + 16, y + h * 0.8],
                    fill=(240, 230, 210))
        d.polygon([(bx - 2, y + h * 0.62), (bx + 8, y + h * 0.5),
                   (bx + 18, y + h * 0.62)], fill=(180, 60, 40))


def tile_crimea(x, y, w, h):
    gradient(x, y, w, h, (14, 22, 52), (52, 38, 78), 6)
    speckle(x, y, w, h, 280, [(80, 90, 140), (255, 255, 255)], 24)
    for (sx, sy) in [(0.1, 0.2), (0.25, 0.12), (0.6, 0.18), (0.85, 0.1),
                     (0.45, 0.25)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1,
                   y + h * sy + 1], fill=(255, 255, 255))
    # bridge: deck + arch + pillars over waves
    d.arc([x + w * 0.1, y + h * 0.3, x + w * 0.9, y + h * 1.1], 180, 360,
          fill=(200, 200, 200), width=4)
    d.line([x + w * 0.05, y + h * 0.55, x + w * 0.95, y + h * 0.55],
           fill=(200, 200, 200), width=3)
    for px in (0.2, 0.5, 0.8):
        d.line([x + w * px, y + h * 0.55, x + w * px, y + h * 0.78],
               fill=(200, 200, 200), width=3)
    blast_star(x + w * 0.68, y + h * 0.42, 7)
    # moon, top left
    d.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.06 + 14,
               y + h * 0.08 + 14], fill=(240, 235, 200))
    for wy in (0.84, 0.92):
        d.arc([x + 6, y + h * wy - 4, x + w * 0.5, y + h * wy + 4], 0, 180,
              fill=(40, 110, 180), width=2)


def tile_bangladesh(x, y, w, h):
    gradient(x, y, w, h, (240, 120, 40), (120, 30, 20), 6)
    speckle(x, y, w, h, 280, [(255, 160, 80), (200, 80, 30)], 25)
    # house silhouettes
    for hx, hw in [(0.06, 0.26), (0.36, 0.3), (0.7, 0.24)]:
        bx = x + w * hx
        d.rectangle([bx, y + h * 0.62, bx + w * hw, y + h], fill=(30, 16, 12))
        d.polygon([(bx - 3, y + h * 0.62), (bx + w * hw / 2, y + h * 0.48),
                   (bx + w * hw + 3, y + h * 0.62)], fill=(30, 16, 12))
    # flame
    cx = x + w * 0.5
    d.polygon([(cx, y + 4), (cx + 13, y + h * 0.5), (cx + 7, y + h - 10),
               (cx - 7, y + h - 10), (cx - 13, y + h * 0.5)],
              fill=(230, 90, 20))
    d.polygon([(cx, y + h * 0.5), (cx + 6, y + h - 8), (cx - 6, y + h - 8)],
              fill=(255, 200, 40))
    # smoke wisps above the flame
    for (sx, sy, sr) in [(0.42, 0.2, 7), (0.55, 0.12, 9), (0.62, 0.24, 6)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=(120, 110, 105))


def tile_nkorea(x, y, w, h):
    gradient(x, y, w, h, (20, 24, 48), (40, 30, 70), 6)
    speckle(x, y, w, h, 280, [(80, 100, 180), (200, 140, 200)], 26)
    cx, cy = x + w * 0.5, y + h * 0.5
    r = h * 0.36
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=(120, 180, 255),
              width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 180, 255),
              width=2)
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=(255, 120, 120),
              width=2)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    d.ellipse([cx + r - 4, cy - r // 2 - 2, cx + r + 3, cy - r // 2 + 5],
              fill=(255, 255, 255))
    d.ellipse([cx - r - 3, cy + r // 2 - 5, cx - r + 4, cy + r // 2 + 2],
              fill=(255, 255, 255))
    # hazard chevrons along the bottom edge
    for i in range(6):
        hx = x + i * w // 6
        d.polygon([(hx, y + h - 6), (hx + 8, y + h - 6), (hx + 4, y + h)],
                  fill=(255, 210, 40))


def tile_hormuz(x, y, w, h):
    gradient(x, y, w, h, (16, 36, 86), (10, 60, 90), 6)
    speckle(x, y, w, h, 280, [(40, 90, 140), (120, 180, 210)], 27)
    # tanker silhouette
    d.rectangle([x + w * 0.08, y + h * 0.55, x + w * 0.62, y + h * 0.72],
                fill=(12, 14, 20))
    d.rectangle([x + w * 0.5, y + h * 0.32, x + w * 0.6, y + h * 0.55],
                fill=(12, 14, 20))
    for i in range(3):
        d.rectangle([x + w * (0.14 + i * 0.13), y + h * 0.42,
                     x + w * (0.24 + i * 0.13), y + h * 0.55],
                    fill=(180, 60, 40))
    # oil drop
    cx = x + w * 0.8
    d.polygon([(cx, y + 6), (cx + 14, y + h * 0.45), (cx - 14, y + h * 0.45)],
              fill=(20, 30, 50))
    d.ellipse([cx - 15, y + h * 0.42, cx + 15, y + h * 0.82],
              fill=(20, 30, 50))
    d.polygon([(cx + 3, y + h * 0.45), (cx - 5, y + h * 0.72),
               (cx + 1, y + h * 0.72), (cx - 2, y + h * 0.6),
               (cx + 6, y + h * 0.5)], fill=(255, 210, 40))
    for wy in (0.84, 0.92):
        d.line([x + 4, y + h * wy, x + w - 4, y + h * wy],
               fill=(90, 160, 190), width=2)
    # sun, top right, and a second small boat
    d.ellipse([x + w * 0.9, y + 4, x + w * 0.9 + 12, y + 16],
              fill=(255, 210, 60))
    d.rectangle([x + w * 0.66, y + h * 0.66, x + w * 0.76, y + h * 0.73],
                fill=(200, 200, 200))


# ---------------------------------------------------------------- data
# Facts, numbers and dates UNCHANGED from the Detailed edition.
# Sources below were verified 2026-11-20 from live reporting of
# 19 November 2026 (Reuters x7, NPR, AP, IEA) and are recorded in
# README.md; nothing here is guessed.
SUB = ("Trump, Xi and Putin share one table \u00b7 The World Court rules "
       "on the Rohingya \u00b7 A record IPO starts trading")

NUMBERS = [
    ("3", "PRESIDENTS AT ONE TABLE"),
    ("$190.4m", "VAN GOGH RECORD"),
    ("$79.4bn", "ANTHROPIC IPO"),
    ("730,000", "ROHINGYA WHO FLED IN 2017"),
    ("28", "DISTRICTS HIT IN BANGLADESH"),
    ("3rd", "ATTACK ON CRIMEAN BRIDGE THIS WEEK"),
]

REGIONS = [("ASIA-PACIFIC", 3), ("EUROPE", 3), ("MIDEAST", 2),
           ("AMERICAS", 2)]

LEADS = [
    {"num": "01", "label": "TOP STORY  \u2022  SHENZHEN, CHINA  \u2022  APEC",
     "headline": "Trump, Xi and Putin hold first trilateral summit",
     "body": ("The US, Chinese and Russian leaders meet for the first "
              "time at APEC in Shenzhen \u2014 Ukraine and nuclear arms "
              "control dominate."),
     "source": "Reuters", "scene": scene_summit},
    {"num": "02", "label": "LAW  \u2022  THE HAGUE",
     "headline": "World court rules on Rohingya genocide case",
     "body": ("The ICJ rules on Gambia's case against Myanmar over the "
              "2017 crackdown that drove 730,000 Rohingya to Bangladesh."),
     "source": "Reuters", "scene": scene_court},
    {"num": "03", "label": "TECH  \u2022  AI  \u2022  NASDAQ",
     "headline": "Anthropic raises a record $79.4bn in IPO",
     "body": ("The AI firm raises a record $79.4bn in its stock market "
              "debut \u2014 the largest ever of its kind."),
     "source": "NPR", "scene": scene_ipo},
]

# (num, tag, headline, body, tile, source) — display order.
MEDIUM = [
    ("04", "MIDDLE EAST  \u2022  THE GULF",
     "Iran attacks Gulf states after US strike",
     "Iran hits Gulf targets after US jets struck a missile site on "
     "Qeshm island.",
     tile_gulf, "Reuters"),
    ("05", "CLIMATE  \u2022  ANTALYA",
     "COP31 ministers race to unblock talks",
     "Ministers meet in Antalya to break the deadlock and agree a "
     "final text.",
     tile_cop, "Reuters"),
    ("06", "CULTURE  \u2022  NEW YORK",
     "Van Gogh sells for $190.4m, a record",
     "\u201cChestnut Trees in Flower\u201d (1890) sells at Sotheby's New "
     "York \u2014 a record for the artist.",
     tile_vangogh, "Reuters"),
    ("07", "WAR  \u2022  UKRAINE",
     "Crimean Bridge hit for a third time",
     "Ukraine strikes the bridge linking Russia to Crimea \u2014 the "
     "third attack this week.",
     tile_crimea, "Reuters"),
    ("08", "ASIA  \u2022  BANGLADESH",
     "Yunus home set on fire amid unrest",
     "Muhammad Yunus's ancestral home is burned as violence hits 28 "
     "districts.",
     tile_bangladesh, "Reuters"),
    ("09", "NUCLEAR",
     "IAEA: North Korea expands enrichment",
     "The IAEA warns North Korea has expanded uranium enrichment.",
     tile_nkorea, "AP"),
    ("10", "ENERGY  \u2022  HORMUZ",
     "Hormuz crisis \u2018greatest threat ever\u2019",
     "The IEA says the Hormuz crisis is the greatest threat ever "
     "observed to energy security.",
     tile_hormuz, "IEA"),
]

BRIEF = [
    "01  Summit in Shenzhen",
    "02  ICJ rules on Rohingya case",
    "03  Anthropic raises $79.4bn",
    "04  Iran attacks Gulf states",
    "05  COP31 talks in Antalya",
    "06  Van Gogh sells for $190.4m",
    "07  Crimean Bridge hit again",
    "08  Yunus home burned",
    "09  IAEA warns on North Korea",
    "10  IEA: Hormuz the greatest threat",
]

# ALSO ON — 27 verified one-line briefs from 19 Nov 2026 reporting
# (see also-on-sources.md; outlet per brief is recorded there and in
# README.md). Source order, renumbered 1-27: brief #8 Mongolia is NOT
# used (weakest outlet chain: "AP via One Turn/Wikipedia" + Argus 20 Nov);
# #7 Denmark is shown without the vote tally (banned number — the full
# fact stays in also-on-sources.md as documentation only).
ALSO_ON = [
    "Refinery blast kills one in Cepu, Indonesia",
    "Indonesia passes asset-forfeiture law",
    "UniCredit wins terms for \u20ac41bn Commerzbank",
    "Fiji declares disaster as El Ni\u00f1o drought bites",
    "Dozens missing as migrant boat sinks off Senegal",
    "Indonesia fire emissions 3rd-highest on record",
    "Denmark backs Greenland-US pact",
    "Seoul court voids ex-PM Han's 15-year term",
    "Serbia elects student-backed speaker \u010cupi\u0107",
    "Somalia expels UAE envoy, recalls its own",
    "US Senate rejects Iran war-powers bid 51\u201348",
    "Haiti fighting erupts over key corridor",
    "Christie's halts Frida Kahlo sale at Mexico plea",
    "US auctions deep-sea mining leases off Samoa",
    "California subpoenas Nvidia over chips, affair",
    "Voyager 1 confirmed one light-day from Earth",
    "Fiona the hippo dies after swallowing a hat",
    "Dow plunges 1,100 as S&P falls 6th straight day",
    "Palo Alto Networks jumps 10% on earnings",
    "Alibaba revenue up 10% to \u00a5271.5bn",
    "Hosts Qatar open U17 World Cup with 2\u20130 win",
    "France beat Haiti 3\u20131 at U17 World Cup",
    "Texans rout Colts 26\u20133 in Thursday NFL",
    "Lightning end McDavid's 23-game point streak",
    "F1 to use full-time stewards from 2027",
    "Pancreatic cancer pill hope as tumours vanish",
    "Thomas Markle ruled fit to stand trial",
]


# ---------------------------------------------------------------- layout
# (1) masthead: kicker + giant serif date + subline
d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=F(BOLD, 13), fill=RED,
       anchor="ma")
d.text((W // 2, 22), "Thursday 19 November 2026", font=F(SERIFD, 54),
       fill=INK, anchor="ma")
d.line([M, 90, W - M, 90], fill=RED, width=4)
d.text((W // 2, 96), SUB, font=F(ITAL, 15), fill=INK, anchor="ma")
d.line([M, 118, W - M, 118], fill=RULE, width=2)
d.line([M, 122, W - M, 122], fill=RULE, width=1)

# (2) number strip — six numbers from our own verified facts only
y = 130
cell_w = CW // 6
for i, (num, label) in enumerate(NUMBERS):
    cx = M + cell_w * i + cell_w // 2
    d.text((cx, y), num, font=F(SERIFB, 22), fill=INK, anchor="ma")
    # Label: at most 2 lines, wrapped inside the cell (cell_w - 12),
    # centred — the old single line ran "28" and "3rd" together because
    # "ATTACK ON CRIMEAN BRIDGE THIS WEEK" (181px) is wider than its
    # 158px cell and bled into the neighbour's label.
    lab_lines = wrap(label, F(BOLD, 9), cell_w - 12)[:2]
    for li, ln in enumerate(lab_lines):
        d.text((cx, y + 24 + li * 11), ln, font=F(BOLD, 9), fill=GREY,
               anchor="ma")
    if i:
        d.line([M + cell_w * i, y + 2, M + cell_w * i, y + 46],
               fill=(200, 192, 172), width=1)
d.line([M, 180, W - M, 180], fill=RULE, width=1)

# (3) geographic tabs — counts sum to 10
y = 188
tab_w = (CW - 3 * 8) // 4
for i, (name, cnt) in enumerate(REGIONS):
    tx = M + i * (tab_w + 8)
    d.rounded_rectangle([tx, y, tx + tab_w, y + 22], radius=5, fill=PANEL,
                        outline=INK, width=1)
    f1, f2 = F(BOLD, 11), F(BLACK, 14)
    tw = d.textlength(name, font=f1) + d.textlength(" " + str(cnt), font=f2) + 4
    sx = tx + (tab_w - tw) // 2
    d.text((sx, y + 4), name, font=f1, fill=INK)
    d.text((sx + d.textlength(name, font=f1) + 4, y + 2), str(cnt), font=f2,
           fill=RED)

# (4) three leads, side by side: big scene + tag + serif headline + body
y = 216
col_w = (CW - 2 * 10) // 3
scene_h = 82
for j, lead in enumerate(LEADS):
    x0 = M + j * (col_w + 10)
    lead["scene"](x0, y, col_w, scene_h)
    d.rectangle([x0, y, x0 + col_w, y + scene_h], outline=INK, width=1)
    ty = y + scene_h + 6
    draw_tag(x0, ty, lead["num"], lead["label"])
    hl = wrap(lead["headline"], F(SERIF, 19), col_w)
    hy = ty + 18
    for i, ln in enumerate(hl[:2]):
        d.text((x0, hy + i * 23), ln, font=F(SERIF, 19), fill=INK)
    bl = wrap(lead["body"], F(REG, 12), col_w)
    for i, ln in enumerate(bl[:3]):
        d.text((x0, hy + 46 + i * 13), ln, font=F(REG, 12), fill=INK)
    draw_source(x0, hy + 46 + 3 * 13 + 4, lead["source"])
d.line([M, 430, W - M, 430], fill=RULE, width=1)

# (5) medium grid: 4 + 3 cards, each with a full-width illustration
y = 436
row_h = 128
for row, count in enumerate([4, 3]):
    cw = (CW - (count - 1) * 8) // count
    y0 = y + row * (row_h + 4)
    for c in range(count):
        idx = (4 if row else 0) + c
        num, tag, headline, body, tile, source = MEDIUM[idx]
        x0 = M + c * (cw + 8)
        d.rectangle([x0, y0, x0 + cw, y0 + row_h], fill=PANEL,
                    outline=(200, 192, 175), width=1)
        tile(x0 + 1, y0 + 1, cw - 2, 36)
        d.rectangle([x0, y0, x0 + cw, y0 + 37], outline=INK, width=1)
        d.text((x0 + 8, y0 + 43), num, font=F(BOLD, 11), fill=RED)
        d.text((x0 + 32, y0 + 44), tag, font=F(BOLD, 9), fill=GREY)
        hl = wrap(headline, F(SERIF, 13), cw - 16)
        hy = y0 + 59
        for i, ln in enumerate(hl[:2]):
            d.text((x0 + 8, hy + i * 15), ln, font=F(SERIF, 13), fill=INK)
        bl = wrap(body, F(REG, 11), cw - 16)
        for i, ln in enumerate(bl[:2]):
            d.text((x0 + 8, hy + 31 + i * 12), ln, font=F(REG, 11),
                   fill=INK)
        draw_source(x0 + 8, y0 + 115, source)

# (6) world map + IN BRIEF side by side
y = 704
d.text((M, y), "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED",
       font=F(BOLD, 13), fill=INK)
map_x, map_w = M, 580
map_y, map_h = y + 16, 88
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=NAVY,
            outline=INK, width=1)


for glon in range(-150, 181, 30):
    gx = map_x + (glon + 180) / 360 * map_w
    d.line([gx, map_y, gx, map_y + map_h], fill=(30, 55, 110), width=1)
for glat in (-30, 0, 30, 60):
    gy = map_y + (75 - glat) / 135 * map_h
    d.line([map_x, gy, map_x + map_w, gy], fill=(30, 55, 110), width=1)
speckle(map_x, map_y, map_w, map_h, 600, [(30, 55, 110), (24, 48, 100)], 31)


def px(lon, lat):
    return (map_x + (lon + 180) / 360 * map_w,
            map_y + (75 - lat) / 135 * map_h)


for poly in CONTINENTS:
    d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
              outline=LANDLINE)
for num, lon, lat in PINS:
    cx, cy = px(lon, lat)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=F(BOLD, 8), fill=(255, 255, 255),
           anchor="mm")
d.text((M, map_y + map_h + 4),
       "RED NUMBERS MARK STORIES 1\u201310  \u00b7  POSITIONS ARE APPROXIMATE",
       font=F(BOLD, 9), fill=GREY)
d.text((M, map_y + map_h + 16),
       "01 SHENZHEN  02 THE HAGUE  03 SAN FRANCISCO  04 GULF  05 ANTALYA  "
       "06 NEW YORK  07 CRIMEA  08 BANGLADESH  09 N. KOREA  10 HORMUZ",
       font=F(BOLD, 8), fill=GREY)
# IN BRIEF column (same ten stories, recapped — not new stories)
bx = map_x + map_w + 16
d.text((bx, y), "IN BRIEF", font=F(BOLD, 13), fill=RED)
d.line([bx, y + 16, W - M, y + 16], fill=RULE, width=1)
for i, line in enumerate(BRIEF):
    d.text((bx, y + 22 + i * 12), line, font=F(REG, 11), fill=INK)

# (6b) ALSO ON — 27 verified one-line briefs from 19 Nov 2026 reporting,
# 3 columns x 9 rows (column-major), between the map and DATE CHECK.
# Brief #8 Mongolia from also-on-sources.md is NOT used (weakest outlet
# chain); #7 Denmark is shown WITHOUT the vote tally (banned number).
y = 852
d.text((M, y), "ALSO ON", font=F(BOLD, 13), fill=RED)
d.line([M, y + 16, W - M, y + 16], fill=RULE, width=1)
ao_col_w = (CW - 2 * 8) // 3
ao_font = F(REG, 9)
for c in range(3):
    ax = M + c * (ao_col_w + 8)
    for r in range(9):
        d.text((ax, 874 + r * 10), ALSO_ON[c * 9 + r], font=ao_font,
               fill=INK)

# (7) DATE CHECK box
y = 970
d.rectangle([M, y, W - M, y + 24], fill=LIGHT, outline=INK, width=1)
d.text((M + 8, y + 5), "DATE CHECK", font=F(BOLD, 12), fill=INK)
cx = M + 8 + d.textlength("DATE CHECK", font=F(BOLD, 12)) + 8
d.line([(cx, y + 12), (cx + 4, y + 17), (cx + 11, y + 6)], fill=GREEN,
       width=3)
d.text((cx + 15, y + 5),
       "Every story on this page happened, or was first reported, on "
       "Thursday 19 November 2026.",
       font=F(BOLD, 12), fill=INK)

# (8) footer: sources + tagline
d.text((W // 2, 998),
       "Sources: Reuters \u00b7 NPR \u00b7 AP \u00b7 IEA \u00b7 BBC \u00b7 "
       "Investopedia \u00b7 Middle East Eye \u00b7 Smithsonian \u00b7 "
       "Scientific American \u00b7 Sportradar \u00b7 AskScores \u00b7 "
       "Morningstar \u2014 every story verified from reporting of "
       "Thursday 19 November 2026.",
       font=F(REG, 9), fill=GREY, anchor="ma")
d.text((W // 2, 1010),
       "WORLD NEWS  \u00b7  THURSDAY 19 NOVEMBER 2026  \u00b7  TEN STORIES "
       "\u00b7 27 MORE IN ALSO ON \u00b7 ONE DAY",
       font=F(BOLD, 10), fill=INK, anchor="ma")

# newsprint grain: deterministic speckle on light areas only (seeded,
# so two runs stay byte-identical). It breaks up flat colour without
# touching dark text or dark illustration areas.
rng = random.Random(20261119)
grain_cols = [(242, 235, 220), (238, 230, 212), (246, 240, 226),
              (232, 224, 204)]
for _ in range(48000):
    gx = rng.randrange(W)
    gy = rng.randrange(H)
    px0 = img.getpixel((gx, gy))
    if px0[0] > 200 and px0[1] > 190 and px0[2] > 170:
        d.point((gx, gy), fill=rng.choice(grain_cols))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
