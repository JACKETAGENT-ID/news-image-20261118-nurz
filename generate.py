#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Original code-drawn newspaper: masthead + lead story + six illustrated
panels + an "In brief" strip. All artwork is drawn with PIL primitives;
no photos or downloaded images. Run: python3 generate.py [out.png]
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (22, 22, 22)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GREY = (90, 88, 80)
PANEL_BG = (255, 252, 244)
RULE = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left",
               max_w=None):
    """Draw lines; returns y just below the last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in lines:
        lx = x
        if align == "center" and max_w is not None:
            lx = x + (max_w - draw.textlength(line, font=fnt)) // 2
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- scenes
def scene_skyline(draw, box):
    """Shenzhen skyline at dusk for the APEC lead story."""
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0)
        c = tuple(int(a + (b - a) * t) for a, b in
                  zip((253, 214, 150), (70, 90, 130)))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    draw.ellipse([x1 - 78, y0 + 14, x1 - 28, y0 + 64], fill=(255, 236, 170))
    base = y1 - 8
    buildings = [(0, 90, 46), (48, 130, 66), (116, 100, 52), (170, 150, 78),
                 (250, 110, 56), (308, 140, 52)]
    for bx, bh, bw in buildings:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base],
                       fill=(38, 48, 66))
        for wy in range(base - bh + 10, base - 8, 16):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 6, 14):
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 220, 120))
    # spire on the tallest tower
    draw.line([(x0 + 170 + 39, base - 150), (x0 + 170 + 39, base - 168)],
              fill=(38, 48, 66), width=4)
    draw.rectangle([x0, base, x1, y1], fill=(24, 32, 48))


def scene_gulf(draw, box):
    """Dusk sky, a drone and radar arcs over the Gulf."""
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0)
        c = tuple(int(a + (b - a) * t) for a, b in
                  zip((250, 196, 140), (96, 110, 150)))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    cx, cy = (x0 + x1) // 2, y0 + 34
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 240, 200))
    # sea
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(52, 96, 128))
    # drone
    dx, dy = x0 + 78, y0 + 42
    draw.line([(dx - 22, dy - 8), (dx + 22, dy - 8)], fill=INK, width=3)
    draw.line([(dx - 22, dy + 8), (dx + 22, dy + 8)], fill=INK, width=3)
    draw.ellipse([dx - 10, dy - 6, dx + 10, dy + 6], fill=INK)
    for rx, ry in [(-22, -8), (22, -8), (-22, 8), (22, 8)]:
        draw.ellipse([dx + rx - 9, dy + ry - 3, dx + rx + 9, dy + ry + 3],
                     outline=INK, width=2)
    # radar arcs
    rx0, ry0 = x1 - 52, y1 - 26
    for r in (18, 32, 46):
        draw.arc([rx0 - r, ry0 - r, rx0 + r, ry0 + r], 180, 360,
                 fill=(255, 255, 255), width=2)
    draw.ellipse([rx0 - 3, ry0 - 3, rx0 + 3, ry0 + 3], fill=(255, 255, 255))


def scene_chip(draw, box):
    """Green AI chip on a circuit board."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 66, 44))
    for i in range(0, (x1 - x0), 26):
        draw.line([(x0 + i, y0), (x0 + i, y1)], fill=(24, 92, 62), width=1)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    s = 34
    for k in range(-2, 3):
        draw.line([(cx - s - 14, cy + k * 14), (cx - s, cy + k * 14)],
                  fill=(190, 220, 200), width=3)
        draw.line([(cx + s, cy + k * 14), (cx + s + 14, cy + k * 14)],
                  fill=(190, 220, 200), width=3)
        draw.line([(cx + k * 14, cy - s - 14), (cx + k * 14, cy - s)],
                  fill=(190, 220, 200), width=3)
        draw.line([(cx + k * 14, cy + s), (cx + k * 14, cy + s + 14)],
                  fill=(190, 220, 200), width=3)
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(34, 150, 80),
                   outline=(220, 240, 220), width=2)
    draw.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                   outline=(220, 240, 220), width=2)
    draw.text((cx, cy), "AI", font=font(SANS_B, 20), fill=(255, 255, 255),
              anchor="mm")


def scene_dove(draw, box):
    """White dove with an olive branch on a calm blue sky."""
    x0, y0, x1, y1 = box
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0)
        c = tuple(int(a + (b - a) * t) for a, b in
                  zip((214, 232, 244), (150, 186, 214)))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    # body + head + beak
    draw.ellipse([cx - 52, cy - 18, cx + 30, cy + 20], fill=(255, 255, 255))
    draw.ellipse([cx + 18, cy - 30, cx + 48, cy - 2], fill=(255, 255, 255))
    draw.polygon([(cx + 46, cy - 20), (cx + 62, cy - 14), (cx + 46, cy - 10)],
                 fill=(230, 150, 40))
    draw.ellipse([cx + 32, cy - 22, cx + 38, cy - 16], fill=INK)
    # raised wing (behind the body, clear of the head)
    draw.polygon([(cx - 40, cy + 2), (cx - 62, cy - 46), (cx - 16, cy - 34),
                  (cx - 2, cy - 4)], fill=(235, 238, 242))
    draw.polygon([(cx - 40, cy + 2), (cx - 56, cy - 38), (cx - 22, cy - 26)],
                 fill=(255, 255, 255))
    # tail
    draw.polygon([(cx - 50, cy - 4), (cx - 78, cy + 12), (cx - 48, cy + 16)],
                 fill=(235, 238, 242))
    # olive branch
    bx, by = x0 + 30, y1 - 22
    draw.line([(bx, by), (bx + 74, by - 14)], fill=(74, 110, 58), width=3)
    for k in range(4):
        lx, ly = bx + 12 + k * 18, by - 4 - k * 3
        draw.ellipse([lx - 9, ly - 12, lx + 9, ly + 2], fill=(88, 130, 66))
        draw.ellipse([lx - 9, ly + 2, lx + 9, ly + 14], fill=(74, 110, 58))


def scene_cricket(draw, box):
    """Cricket stumps, bat and ball on a green outfield."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(74, 140, 74))
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(52, 110, 52))
    # pitch strip
    draw.rectangle([x0 + 96, y0, x1 - 96, y1], fill=(196, 164, 110))
    # stumps
    sx = (x0 + x1) // 2
    for k in (-14, 0, 14):
        draw.rectangle([sx + k - 3, y0 + 22, sx + k + 3, y0 + 58],
                       fill=(240, 210, 110))
    draw.rectangle([sx - 17, y0 + 16, sx + 17, y0 + 21], fill=(240, 210, 110))
    # bat leaning against the stumps, handle up
    draw.polygon([(sx - 52, y1 - 22), (sx - 38, y1 - 22), (sx - 22, y0 + 52),
                  (sx - 32, y0 + 48)], fill=(222, 184, 120),
                 outline=(150, 110, 60))
    # red ball
    draw.ellipse([x1 - 52, y1 - 46, x1 - 26, y1 - 20], fill=(178, 34, 34),
                 outline=(255, 255, 255), width=2)


def scene_cyclone(draw, box):
    """Spiral cyclone over the Bay of Bengal."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(206, 226, 238))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in range(8, 62, 9):
        a0 = r * 4
        draw.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
                 fill=(24, 84, 140), width=5)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(24, 84, 140))
    # clouds
    for ox, oy, ow in [(x0 + 8, y0 + 8, 40), (x1 - 62, y0 + 14, 46),
                       (x0 + 20, y1 - 30, 44)]:
        draw.ellipse([ox, oy, ox + ow, oy + 16], fill=(255, 255, 255))
        draw.ellipse([ox + 10, oy - 8, ox + ow - 8, oy + 10],
                     fill=(255, 255, 255))


def scene_voyager(draw, box):
    """Voyager 1 in deep space, one light-day out."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(8, 12, 28))
    rng = random.Random(18112026)
    for _ in range(46):
        sx = rng.randint(x0 + 3, x1 - 3)
        sy = rng.randint(y0 + 3, y1 - 3)
        r = rng.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r],
                     fill=(255, 255, 255))
    # probe: gold body, white dish, antenna
    px, py = (x0 + x1) // 2 - 10, (y0 + y1) // 2
    draw.line([(px - 8, py - 6), (px - 34, py - 26)], fill=(200, 200, 210),
              width=2)
    draw.ellipse([px - 38, py - 30, px - 30, py - 22], fill=(220, 220, 230))
    draw.polygon([(px + 26, py - 22), (px + 6, py - 6), (px + 6, py + 10),
                  (px + 26, py + 2)], fill=(255, 255, 255),
                 outline=(200, 200, 210))
    draw.rectangle([px - 14, py - 8, px + 8, py + 8], fill=(212, 175, 55),
                   outline=(150, 120, 40), width=2)
    draw.line([(px - 14, py + 8), (px - 40, py + 30)], fill=(200, 200, 210),
              width=2)
    # faint signal rings from the dish
    for r in (18, 28):
        draw.arc([px + 26 - r, py - 10 - r, px + 26 + r, py - 10 + r],
                 -50, 50, fill=(140, 180, 255), width=2)


# ---------------------------------------------------------------- page
PANELS = [
    ("THE GULF", "GULF ON EDGE AS DRONE STRIKES GO ON",
     "Bahrain gives the all-clear after an overnight threat warning. "
     "Kuwait says it intercepted a drone. Iran-US strikes go on over "
     "Qeshm and Bahrain.", scene_gulf),
    ("TECH", "NVIDIA DOUBLES REVENUE TO $115.84BN",
     "Quarterly revenue hits $115.84bn, twice last year's. The board "
     "rejects the return of CEO Jensen Huang. Trump backs Huang's "
     "comeback.", scene_chip),
    ("GAZA", "GAZA CEASEFIRE 'FACES COLLAPSE'",
     "The Board of Peace warns the Gaza ceasefire faces collapse "
     "without action. WFP: one hot meal every two days in the camps.",
     scene_dove),
    ("SPORT", "DHONI CALLS TIME ON IPL",
     "MS Dhoni announces his retirement from the IPL and becomes a "
     "mentor at Chennai Super Kings.", scene_cricket),
    ("WEATHER", "CYCLONE AKVAN STRENGTHENS",
     "Cyclone Akvan strengthens in the Bay of Bengal and is forecast "
     "to become a severe cyclone on 19 November.", scene_cyclone),
    ("SPACE", "VOYAGER 1 NEARS ONE LIGHT-DAY",
     "NASA's Voyager 1 nears one light-day from Earth - the first "
     "human-made object to travel so far.", scene_voyager),
]

BRIEF = ("Latvia's parliament approves a new Kulbergs government  •  "
         "UN: at least 372 civilians killed in Ukraine in October  •  "
         "Baidu chief warns of an AI bubble ahead of APEC talks  •  "
         "Judge extends Trump's deposition deadline in the $10bn BBC suit "
         "to 22 January")


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---- masthead
    f_mast = font(SERIF, 88)
    title = "THE WORLD"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 6), title, font=f_mast, fill=INK)
    rule(d, mx, 116, W - mx, 3)
    f_date = font(SANS_B, 23)
    date = "WEDNESDAY  •  18 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 124), date, font=f_date, fill=RED)
    rule(d, mx, 158, W - mx, 1, fill=RULE)

    # ---- lead story: APEC
    ly = 170
    f_lead = font(SERIF, 38)
    f_deck = font(SANS, 18)
    d.text((mx, ly), "APEC OPENS", font=f_lead, fill=INK)
    d.text((mx, ly + 44), "IN SHENZHEN", font=f_lead, fill=INK)
    rule(d, mx, ly + 96, 600, 2, fill=RED)
    deck = ("Leaders gather for the 18-19 November summit. Trump is in "
            "Manila for Quad talks before heading to China. Xi meets "
            "Canada's Carney as Ottawa and Beijing extend trade "
            "cooperation.")
    text_block(d, mx, ly + 108, wrap(d, deck, f_deck, 560), f_deck,
               leading=24)
    scene_skyline(d, (636, ly + 4, W - mx, ly + 184))
    d.rectangle([636, ly + 4, W - mx, ly + 184], outline=INK, width=2)
    d.text((636, ly + 188), "SHENZHEN, CHINA", font=font(SANS_B, 12),
           fill=GREY)
    rule(d, mx, 378, W - mx, 1, fill=RULE)

    # ---- six panels, 2 rows x 3 cols
    gx, gy = mx, 384
    pw, ph = 309, 244
    gap = 12
    f_kick = font(SANS_B, 13)
    f_head = font(SANS_B, 20)
    f_body = font(SANS, 14)
    for i, (kicker, head, body, scene) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=PANEL_BG,
                    outline=INK, width=1)
        scene(d, (x0 + 1, y0 + 1, x0 + pw - 1, y0 + 96))
        d.line([(x0, y0 + 96), (x0 + pw, y0 + 96)], fill=INK, width=1)
        d.text((x0 + 10, y0 + 104), kicker, font=f_kick, fill=RED)
        hy = text_block(d, x0 + 10, y0 + 124,
                        wrap(d, head, f_head, pw - 20), f_head, leading=23)
        text_block(d, x0 + 10, hy + 2,
                   wrap(d, body, f_body, pw - 20), f_body, leading=18)

    # ---- in brief strip
    by = 896
    rule(d, mx, by, W - mx, 2)
    f_brief = font(SANS, 14)
    f_brief_b = font(SANS_B, 14)
    d.text((mx, by + 10), "IN BRIEF", font=f_brief_b, fill=RED)
    text_block(d, mx, by + 30, wrap(d, BRIEF, f_brief, W - 2 * mx),
               f_brief, leading=19)
    rule(d, mx, 994, W - mx, 1, fill=RULE)
    f_foot = font(SANS, 12)
    foot = "THE WORLD  •  Wednesday 18 November 2026  •  One day's world news in one image"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 1000), foot, font=f_foot, fill=GREY)

    img.save(path, "PNG", optimize=True)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
