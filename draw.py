#!/usr/bin/env python3
"""Draw the World News front page for Thursday 19 November 2026.

Detailed edition: every story gets a number, a section label, a bold
headline and a 2-3 line body drawn ONLY from the ten verified facts in
README.md (no invented numbers, quotes or details), plus an IN BRIEF
strip that recaps all ten stories. This revision also fixes the known
gap in the first edition: the Rohingya panel now says the 2017
crackdown drove 730,000 Rohingya TO BANGLADESH. Pure PIL, no network,
fully deterministic. Writes entry.png (1024x1024) next to this file.
"""
import math
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_BLACK = font("NotoSans-Black.ttf", 84)
F_DATE = font("NotoSans-Bold.ttf", 34)
F_LEAD_HEAD = font("NotoSans-Black.ttf", 34)
F_LEAD_DECK = font("NotoSans-Bold.ttf", 23)
F_LEAD_BODY = font("NotoSans-Regular.ttf", 20)
F_HEAD = font("NotoSans-Bold.ttf", 21)
F_BODY = font("NotoSans-Regular.ttf", 15)
F_TAG = font("NotoSans-Bold.ttf", 14)
F_BRIEF_LABEL = font("NotoSans-Bold.ttf", 13)
F_BRIEF = font("NotoSans-Regular.ttf", 13)
F_FOOT = font("NotoSans-Regular.ttf", 14)
F_FLAGCAP = font("NotoSans-Bold.ttf", 13)

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (176, 30, 36)
NAVY = (24, 52, 96)
TEAL = (14, 110, 110)
GOLD = (196, 138, 20)
GREY = (90, 86, 78)
LINE = (200, 192, 175)
CELL_BG = (255, 255, 255)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_flags(d, x, y, w):
    """China / US / Russia flags side by side, with a caption."""
    fw, fh = (w - 16) // 3, 46
    # China: red field, one yellow star
    d.rectangle([x, y, x + fw, y + fh], fill=(222, 41, 16))
    cx, cy = x + 14, y + 14
    d.polygon([(cx, cy - 8), (cx + 2, cy - 2), (cx + 8, cy - 2),
               (cx + 3, cy + 2), (cx + 5, cy + 8), (cx, cy + 4),
               (cx - 5, cy + 8), (cx - 3, cy + 2), (cx - 8, cy - 2),
               (cx - 2, cy - 2)], fill=(255, 222, 0))
    # US: red/white stripes, blue canton
    ux = x + fw + 8
    for i in range(7):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([ux, y + i * fh // 7, ux + fw, y + (i + 1) * fh // 7],
                    fill=col)
    d.rectangle([ux, y, ux + fw // 2, y + fh * 4 // 7], fill=(60, 59, 110))
    # Russia: white / blue / red tricolour
    rx = x + 2 * fw + 16
    d.rectangle([rx, y, rx + fw, y + fh // 3], fill=(255, 255, 255),
                outline=LINE)
    d.rectangle([rx, y + fh // 3, rx + fw, y + 2 * fh // 3],
                fill=(0, 57, 166))
    d.rectangle([rx, y + 2 * fh // 3, rx + fw, y + fh], fill=(213, 0, 50))
    cap = "US  \u2022  CHINA  \u2022  RUSSIA"
    cw = d.textlength(cap, font=F_FLAGCAP)
    d.text((x + (w - cw) / 2, y + fh + 8), cap, font=F_FLAGCAP, fill=GREY)


def icon_scales(d, x, y, s):
    # scales of justice
    cx = x + s // 2
    d.line([cx, y + 8, cx, y + s - 18], fill=NAVY, width=5)
    d.line([x + 8, y + 18, x + s - 8, y + 18], fill=NAVY, width=5)
    d.arc([x + 2, y + 16, x + s // 3 + 6, y + s - 6], start=0, end=180,
          fill=NAVY, width=4)
    d.arc([x + 2 * s // 3 - 6, y + 16, x + s - 2, y + s - 6], start=0,
          end=180, fill=NAVY, width=4)
    d.ellipse([cx - 5, y + 4, cx + 5, y + 14], fill=RED)


def icon_bridge(d, x, y, s):
    # arched bridge over waves
    d.arc([x + 4, y + 2, x + s - 4, y + s - 6], start=180, end=360,
          fill=GREY, width=6)
    d.line([x + 4, y + s // 2, x + s - 4, y + s // 2], fill=GREY, width=4)
    for px in (x + 12, x + s // 2, x + s - 12):
        d.line([px, y + s // 2 - 12, px, y + s // 2], fill=GREY, width=4)
    for i in range(3):
        wx = x + 8 + i * (s - 16) // 2
        d.arc([wx, y + 2 * s // 3, wx + (s - 16) // 2, y + s - 4],
              start=0, end=180, fill=(40, 110, 180), width=4)


def icon_missile(d, x, y, s):
    # missile streak + impact burst
    d.polygon([(x + 8, y + s // 2 - 6), (x + s // 2, y + s // 2 - 6),
               (x + s // 2 + 14, y + s // 2), (x + s // 2, y + s // 2 + 6),
               (x + 8, y + s // 2 + 6)], fill=(60, 60, 66))
    d.polygon([(x + 8, y + s // 2 - 6), (x + 8, y + s // 2 + 6),
               (x - 2, y + s // 2)], fill=RED)
    bx, by = x + 3 * s // 4, y + s // 2
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([bx, by, bx + int(16 * math.cos(a)),
                by + int(16 * math.sin(a))], fill=(230, 120, 20), width=4)
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(230, 120, 20))


def icon_globe_leaf(d, x, y, s):
    # globe with a green leaf
    cx, cy = x + s // 2 - 6, y + s // 2
    r = s // 2 - 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL,
              width=3)
    d.line([cx - r, cy, cx + r, cy], fill=TEAL, width=3)
    lx, ly = x + s - 26, y + s - 30
    d.polygon([(lx, ly), (lx + 24, ly - 6), (lx + 20, ly + 14)],
              fill=(34, 139, 34))
    d.line([lx, ly, lx + 22, ly + 12], fill=(34, 139, 34), width=3)


def icon_painting(d, x, y, s):
    # framed canvas: blue sky, yellow blossom tree
    d.rectangle([x + 4, y + 4, x + s - 4, y + s - 4], outline=GOLD, width=5)
    d.rectangle([x + 10, y + 10, x + s - 10, y + s - 10],
                fill=(140, 180, 220))
    d.ellipse([x + s - 30, y + 12, x + s - 14, y + 28], fill=(255, 230, 120))
    tx, ty = x + s // 2, y + s - 18
    d.line([tx, ty, tx, ty - 22], fill=(90, 60, 30), width=5)
    for dx, dy in ((-12, -26), (0, -32), (12, -26), (-6, -20), (6, -20)):
        d.ellipse([tx + dx - 7, ty + dy - 7, tx + dx + 7, ty + dy + 7],
                  fill=(255, 200, 40))
    d.rectangle([x + 10, y + s - 16, x + s - 10, y + s - 10],
                fill=(80, 140, 70))


def icon_chart(d, x, y, s):
    # rising bars + arrow
    base = y + s - 10
    d.line([x + 6, y + 8, x + 6, base], fill=NAVY, width=4)
    d.line([x + 6, base, x + s - 4, base], fill=NAVY, width=4)
    heights = [14, 24, 20, 34]
    bw = (s - 20) // 4
    for i, h in enumerate(heights):
        bx = x + 12 + i * bw
        d.rectangle([bx, base - h, bx + bw - 5, base], fill=TEAL)
    d.line([x + 10, base - 16, x + s - 8, y + 10], fill=RED, width=5)
    d.polygon([(x + s - 8, y + 10), (x + s - 22, y + 8),
               (x + s - 10, y + 22)], fill=RED)


def icon_flame(d, x, y, s):
    # flame over rooftops
    cx = x + s // 2
    d.polygon([(cx, y + 4), (cx + 14, y + s // 2), (cx + 8, y + s - 12),
               (cx - 8, y + s - 12), (cx - 14, y + s // 2)], fill=(230, 90, 20))
    d.polygon([(cx, y + s // 2 + 4), (cx + 7, y + s - 6),
               (cx - 7, y + s - 6)], fill=(255, 200, 40))
    d.line([x + 4, y + s - 6, x + s - 4, y + s - 6], fill=NAVY, width=4)


def icon_atom(d, x, y, s):
    # nucleus + three orbits (uranium enrichment)
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 6
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=NAVY,
              width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=TEAL,
              width=3)
    d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=RED,
              width=3)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    d.ellipse([cx + r - 5, cy - r // 2 - 2, cx + r + 3, cy - r // 2 + 6],
              fill=NAVY)
    d.ellipse([cx - r - 3, cy + r // 2 - 6, cx - r + 5, cy + r // 2 + 2],
              fill=NAVY)


def icon_drop(d, x, y, s):
    # oil drop with a lightning bolt (energy security)
    cx = x + s // 2
    d.polygon([(cx, y + 4), (cx + 18, y + s // 2 + 4),
               (cx - 18, y + s // 2 + 4)], fill=(40, 60, 90))
    d.ellipse([cx - 20, y + s // 2 - 2, cx + 20, y + s - 6],
              fill=(40, 60, 90))
    d.polygon([(cx + 4, y + s // 2 + 2), (cx - 6, y + s - 16),
               (cx + 1, y + s - 16), (cx - 3, y + s - 6),
               (cx + 8, y + s // 2 + 12)], fill=(255, 210, 40))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- masthead: navy band, white title, gold rule, red date
    d.rectangle([0, 0, W, 120], fill=NAVY)
    title = "WORLD NEWS"
    tw = d.textlength(title, font=F_BLACK)
    d.text(((W - tw) / 2, 6), title, font=F_BLACK, fill=(255, 255, 255))
    d.rectangle([M, 126, W - M, 130], fill=GOLD)
    date = "THURSDAY 19 NOVEMBER 2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 140), date, font=F_DATE, fill=RED)
    d.line([M, 184, W - M, 184], fill=INK, width=2)

    # ---- lead story 01: summit (headline + deck + 2-line body, flags right)
    ly, lh = 194, 172
    d.rectangle([M, ly, W - M, ly + lh], fill=CELL_BG, outline=LINE, width=2)
    d.rectangle([M, ly, M + 6, ly + lh], fill=NAVY)
    fx = W - M - 196
    icon_flags(d, fx, ly + 46, 180)
    tx = M + 20
    d.text((tx, ly + 12), "01  \u2014  LEAD  \u2022  SHENZHEN, CHINA  \u2022  APEC",
           font=F_TAG, fill=RED)
    head = wrap(d, "Trump, Xi and Putin hold first trilateral summit",
                F_LEAD_HEAD, fx - tx - 16)
    draw_lines(d, head, tx, ly + 34, F_LEAD_HEAD, INK, 39)
    body = wrap(d, "The US, Chinese and Russian leaders meet for the "
                   "first time at APEC in Shenzhen \u2014 Ukraine and "
                   "nuclear arms control dominate.",
                F_LEAD_BODY, fx - tx - 16)
    draw_lines(d, body, tx, ly + 118, F_LEAD_BODY, INK, 25)

    # ---- grid of stories 02-10: tag + number, icon, headline, 2-3 line body
    # Bodies below restate ONLY the verified facts from README.md.
    stories = [
        ("02", "LAW  \u2022  THE HAGUE",
         "World court rules on Rohingya genocide case",
         "The ICJ rules on Gambia's case against Myanmar over the "
         "2017 crackdown that drove 730,000 Rohingya to Bangladesh.",
         icon_scales, RED),
        ("03", "WAR  \u2022  UKRAINE",
         "Crimean Bridge hit for a third time this week",
         "Ukraine strikes the bridge linking Russia to Crimea again "
         "\u2014 the third attack this week.",
         icon_bridge, RED),
        ("04", "MIDDLE EAST  \u2022  THE GULF",
         "Iran attacks Gulf states after US strike on Qeshm",
         "Iran hits Gulf targets after US jets struck a missile site "
         "on Qeshm island, at the Strait of Hormuz.",
         icon_missile, RED),
        ("05", "CLIMATE  \u2022  ANTALYA",
         "COP31 ministers race to unblock climate talks",
         "Ministers meet in Antalya to break the deadlock and agree "
         "a final text.",
         icon_globe_leaf, TEAL),
        ("06", "CULTURE  \u2022  NEW YORK",
         "Van Gogh sells for $190.4m, a record",
         "\u201cChestnut Trees in Flower\u201d (1890) sells at "
         "Sotheby's New York \u2014 the most ever paid for the artist.",
         icon_painting, GOLD),
        ("07", "TECH  \u2022  AI",
         "Anthropic raises a record $79.4bn in IPO",
         "The AI firm's stock market debut is the largest ever of "
         "its kind.",
         icon_chart, NAVY),
        ("08", "ASIA  \u2022  BANGLADESH",
         "Yunus home set on fire amid unrest",
         "Muhammad Yunus's ancestral home is burned as violence "
         "hits 28 districts.",
         icon_flame, RED),
        ("09", "NUCLEAR",
         "IAEA: North Korea expands uranium enrichment",
         "The IAEA warns North Korea has expanded uranium "
         "enrichment.",
         icon_atom, NAVY),
        ("10", "ENERGY  \u2022  HORMUZ",
         "Hormuz crisis \u2018greatest threat ever\u2019 to energy",
         "The IEA says the Hormuz crisis is the greatest threat "
         "ever observed to energy security.",
         icon_drop, NAVY),
    ]
    gy = 376
    cw = (W - 2 * M - 24) // 3
    ch = 184
    for i, (num, tag, headline, body, icon, col) in enumerate(stories):
        r, c = divmod(i, 3)
        x0 = M + c * (cw + 12)
        y0 = gy + r * (ch + 10)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CELL_BG, outline=LINE,
                    width=2)
        d.rectangle([x0, y0, x0 + 5, y0 + ch], fill=col)
        d.text((x0 + 14, y0 + 8), f"{num}  \u2022  {tag}", font=F_TAG,
               fill=col)
        icon(d, x0 + cw - 70, y0 + 4, 58)
        hl = wrap(d, headline, F_HEAD, cw - 28)
        y = draw_lines(d, hl, x0 + 14, y0 + 66, F_HEAD, INK, 25)
        bp = wrap(d, body, F_BODY, cw - 28)
        draw_lines(d, bp, x0 + 14, y + 6, F_BODY, GREY, 19)

    # ---- IN BRIEF strip: one-line recap of all ten stories, no new facts
    by = 958
    d.line([M, by, W - M, by], fill=INK, width=2)
    d.text((M, by + 6), "IN BRIEF", font=F_BRIEF_LABEL, fill=RED)
    brief = ("Summit in Shenzhen  \u2022  ICJ rules on Rohingya case  "
             "\u2022  Crimean Bridge hit again  \u2022  Iran attacks Gulf "
             "states  \u2022  COP31 talks in Antalya  \u2022  Van Gogh "
             "sells for $190.4m  \u2022  Anthropic raises $79.4bn  "
             "\u2022  Yunus home burned  \u2022  IAEA warns on North Korea "
             " \u2022  IEA: Hormuz the greatest threat to energy")
    bl = wrap(d, brief, F_BRIEF, W - 2 * M - 92)
    draw_lines(d, bl, M + 92, by + 6, F_BRIEF, INK, 17)

    # ---- footer
    d.line([M, 1002, W - M, 1002], fill=INK, width=2)
    foot = "WORLD NEWS  \u2022  THURSDAY 19 NOVEMBER 2026  \u2022  TEN STORIES, ONE DAY"
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, 1008), foot, font=F_FOOT, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
