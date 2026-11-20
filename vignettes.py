#!/usr/bin/env python3
"""Draw the 11 text-free vignette illustrations for news-image-20261119.

Flat editorial style (deep navy / warm ochre / paper), matching the
20261118 entry. Canvas 1200x320 (~tile aspect 3.75:1) so the tile crop
(242x64) barely crops; the lead band (1000x160, 6.25:1) centre-crops to
y 64..256, so every vignette keeps its key content inside y 60..260.
No text anywhere. Run: python3 vignettes.py  -> candidates/NN-*.png
"""
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "candidates")
W, H = 1200, 320

NAVY = (27, 42, 74)
NAVY_D = (16, 28, 52)
OCHRE = (217, 164, 65)
OCHRE_D = (186, 128, 42)
PAPER = (250, 247, 240)
RED = (179, 38, 30)
TEAL = (46, 125, 107)
TEAL_D = (28, 84, 72)
SKY = (168, 205, 225)
GOLD = (232, 190, 90)
WHITE = (255, 255, 255)
GREY = (120, 122, 126)
GREEN = (74, 140, 74)


def sky(d, top, bot, y0=0, y1=H):
    """Vertical gradient between two RGB colours."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)


def sun(d, cx, cy, r, colour=OCHRE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colour)
    d.ellipse((cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10),
              outline=colour, width=3)


def moon(d, cx, cy, r):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(245, 238, 214))
    d.ellipse((cx - r * 0.55, cy - r * 0.3, cx - r * 0.15, cy + r * 0.1),
              fill=(214, 203, 175))
    d.ellipse((cx + r * 0.1, cy + r * 0.35, cx + r * 0.45, cy + r * 0.7),
              fill=(214, 203, 175))


def ground(d, y, colour):
    d.rectangle((0, y, W, H), fill=colour)


def building(d, x, y_base, w, h, colour, windows=True, wc=(250, 220, 140)):
    d.rectangle((x, y_base - h, x + w, y_base), fill=colour)
    if windows:
        for wy in range(y_base - h + 12, y_base - 8, 18):
            for wx in range(x + 8, x + w - 8, 16):
                d.rectangle((wx, wy, wx + 7, wy + 9), fill=wc)


def palm(d, x, y_base, s=1.0, colour=(34, 110, 70)):
    """Small palm tree; (x, y_base) is the trunk base."""
    d.line((x, y_base, x + 6 * s, y_base - 70 * s), fill=(110, 80, 50),
           width=max(3, int(5 * s)))
    tx, ty = x + 6 * s, y_base - 70 * s
    for ang, ln in ((-160, 46), (-120, 52), (-80, 52), (-40, 46), (-200, 40),
                    (0, 40)):
        a = math.radians(ang)
        d.line((tx, ty, tx + ln * s * math.cos(a), ty + ln * s * math.sin(a) * 0.55),
               fill=colour, width=max(3, int(5 * s)))


def flagpole(d, x, y_base, h=150):
    d.line((x, y_base, x, y_base - h), fill=(60, 60, 60), width=4)
    d.ellipse((x - 4, y_base - h - 5, x + 4, y_base - h + 3), fill=OCHRE)


def flag_us(d, x, y, w, h):
    """Stars & Stripes, simplified: 7 stripes + blue canton with dots."""
    for i in range(7):
        d.rectangle((x, y + i * h / 7, x + w, y + (i + 1) * h / 7),
                    fill=RED if i % 2 == 0 else WHITE)
    cw, ch = w * 0.42, h * 4 / 7
    d.rectangle((x, y, x + cw, y + ch), fill=(32, 54, 120))
    for r in range(4):
        for c in range(5):
            px = x + 6 + c * (cw - 10) / 4
            py = y + 5 + r * (ch - 10) / 3
            d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=WHITE)


def flag_ru(d, x, y, w, h):
    for i, c in enumerate((WHITE, (0, 80, 170), RED)):
        d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)


def flag_cn(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), fill=(222, 41, 16))
    d.ellipse((x + 8, y + 6, x + 22, y + 20), fill=(255, 222, 0))
    for sx, sy in ((34, 8), (40, 16), (38, 26), (28, 28)):
        d.ellipse((x + sx, y + sy, x + sx + 5, y + sy + 5), fill=(255, 222, 0))


def flag_in(d, x, y, w, h):
    for i, c in enumerate(((255, 153, 51), WHITE, (19, 136, 8))):
        d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
    cx, cy, r = x + w / 2, y + h / 2, h / 6
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=NAVY, width=2)
    for k in range(8):
        a = math.radians(k * 45)
        d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)),
               fill=NAVY, width=1)


def flag_jp(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), fill=WHITE)
    d.ellipse((x + w / 2 - h * 0.3, y + h * 0.2, x + w / 2 + h * 0.3,
               y + h * 0.8), fill=RED)


def flag_br(d, x, y, w, h):
    d.rectangle((x, y, x + w, y + h), fill=(0, 140, 60))
    d.polygon([(x + w / 2, y + 4), (x + w - 6, y + h / 2),
               (x + w / 2, y + h - 4), (x + 6, y + h / 2)],
              fill=(255, 210, 0))
    d.ellipse((x + w / 2 - h * 0.28, y + h * 0.22, x + w / 2 + h * 0.28,
               y + h * 0.78), fill=(0, 60, 160))


def flag_ke(d, x, y, w, h):
    bands = ((0, 0, 0), RED, (0, 110, 60))
    for i, c in enumerate(bands):
        d.rectangle((x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
    cx, cy = x + w / 2, y + h / 2
    d.ellipse((cx - 12, cy - 16, cx + 12, cy + 16), fill=(140, 60, 30),
              outline=WHITE, width=2)


def spiral(d, cx, cy, r_max, colour, width=7, turns=2.6):
    """Cyclone spiral: Archimedean arms drawn as polylines."""
    for arm in range(3):
        pts = []
        steps = 90
        for i in range(steps + 1):
            t = i / steps
            ang = arm * 2 * math.pi / 3 + t * turns * 2 * math.pi
            r = 12 + t * (r_max - 12)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.82))
        d.line(pts, fill=colour, width=width, joint="curve")
    d.ellipse((cx - 14, cy - 11, cx + 14, cy + 11), fill=(240, 244, 248),
              outline=colour, width=3)


def waves(d, y0, y1, colour, amp=6, step=46):
    for y in range(y0, y1, 16):
        pts = []
        for x in range(0, W + step, step):
            pts.append((x, y + amp * math.sin(x / 55.0 + y)))
        d.line(pts, fill=colour, width=3, joint="curve")


def save(img, name):
    img.save(os.path.join(OUT, name), optimize=True)
    print("saved", name)


# ---------------------------------------------------------------- 1 LEAD
def v01():
    img = Image.new("RGB", (W, H), NAVY_D)
    d = ImageDraw.Draw(img)
    sky(d, (58, 48, 96), (214, 122, 62), 0, 250)  # dusk over Shenzhen
    sun(d, 600, 205, 42, (255, 176, 92))
    # Shenzhen skyline silhouette
    for x, w, h in ((30, 46, 120), (90, 34, 90), (150, 40, 150), (210, 30, 100),
                    (880, 40, 140), (940, 34, 95), (1000, 46, 160),
                    (1070, 36, 105), (1130, 40, 130)):
        building(d, x, 250, w, h, NAVY_D, windows=False)
    # Ping An Finance Centre: tall tapered tower, centre-right
    d.polygon([(770, 250), (782, 60), (798, 60), (810, 250)], fill=NAVY_D)
    d.polygon([(782, 60), (790, 38), (798, 60)], fill=OCHRE)
    # Kylin Villa pavilion, centre
    ground(d, 250, (52, 72, 46))
    d.rectangle((470, 218, 730, 250), fill=(120, 60, 40))      # villa body
    d.polygon([(450, 220), (600, 168), (750, 220)], fill=(150, 52, 36))
    d.polygon([(450, 220), (600, 168), (750, 220)], outline=OCHRE, width=3)
    d.rectangle((540, 196, 660, 200), fill=OCHRE)               # curved eave
    for wx in range(490, 720, 28):
        d.rectangle((wx, 226, wx + 14, 244), fill=(250, 220, 140))
    d.rectangle((592, 226, 608, 250), fill=(60, 30, 20))        # door
    # three flags in front of the villa
    for fx, fn in ((500, flag_cn), (590, flag_ru), (680, flag_us)):
        flagpole(d, fx, 250, 118)
        fn(d, fx + 4, 250 - 118, 62, 40)
    save(img, "01-trilateral.png")


# ---------------------------------------------------------------- 2 ICJ
def v02():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)
    sky(d, (140, 190, 220), (226, 232, 222), 0, 240)
    # Peace Palace: red-brick tower + hall
    ground(d, 240, (96, 140, 88))
    d.rectangle((120, 120, 420, 240), fill=(158, 74, 58))
    d.polygon([(110, 122), (270, 70), (430, 122)], fill=(120, 52, 40))
    d.rectangle((255, 60, 285, 240), fill=(140, 62, 48))        # clock tower
    d.polygon([(248, 62), (270, 28), (292, 62)], fill=(70, 90, 90))
    d.ellipse((258, 78, 282, 102), fill=PAPER)
    d.line((270, 90, 270, 82), fill=(40, 40, 40), width=2)
    d.line((270, 90, 277, 90), fill=(40, 40, 40), width=2)
    for wx in range(140, 410, 34):
        d.polygon([(wx, 240), (wx + 6, 190), (wx + 18, 190), (wx + 24, 240)],
                  fill=(40, 50, 70))
    # trees + path
    for tx in (60, 470, 520):
        d.ellipse((tx, 190, tx + 46, 240), fill=(52, 110, 66))
    d.polygon([(560, 240), (640, 240), (700, 320), (500, 320)], fill=(214, 206, 188))
    # Scales of justice, large, right of centre
    cx, cy = 880, 150
    d.line((cx, cy - 70, cx, cy + 110), fill=(150, 110, 40), width=7)
    d.line((cx - 95, cy - 58, cx + 95, cy - 58), fill=(150, 110, 40), width=6)
    d.ellipse((cx - 10, cy - 84, cx + 10, cy - 64), fill=OCHRE)
    for sgn in (-1, 1):
        px = cx + sgn * 95
        d.line((px, cy - 58, px - 26, cy + 6), fill=(150, 110, 40), width=3)
        d.line((px, cy - 58, px + 26, cy + 6), fill=(150, 110, 40), width=3)
        d.line((px, cy - 58, px, cy + 6), fill=(150, 110, 40), width=3)
        d.pieslice((px - 34, cy - 6, px + 34, cy + 30), 0, 180, fill=GOLD)
    d.rectangle((cx - 46, cy + 106, cx + 46, cy + 118), fill=(150, 110, 40))
    save(img, "02-icj.png")


# ---------------------------------------------------------------- 3 GTA VI
def v03():
    img = Image.new("RGB", (W, H), (28, 12, 52))
    d = ImageDraw.Draw(img)
    sky(d, (46, 18, 84), (214, 74, 140), 0, 235)  # Vice City neon dusk
    moon(d, 980, 105, 46)
    # art-deco skyline
    for x, w, h, c in ((20, 60, 150, (58, 32, 96)), (95, 44, 110, (72, 40, 110)),
                       (155, 70, 185, (48, 26, 84)), (240, 40, 120, (66, 36, 104)),
                       (700, 66, 170, (52, 30, 90)), (782, 44, 120, (70, 38, 108)),
                       (842, 58, 150, (46, 26, 82)), (1080, 60, 140, (60, 34, 98))):
        d.rectangle((x, 235 - h, x + w, 235), fill=c)
        for wy in range(235 - h + 10, 230, 20):
            for wx in range(x + 7, x + w - 6, 14):
                d.rectangle((wx, wy, wx + 5, wy + 8),
                            fill=(255, 120, 190) if (wx + wy) % 3 else (255, 210, 110))
    # neon sun strip on the horizon + ocean
    d.rectangle((0, 232, W, 240), fill=(255, 110, 170))
    d.rectangle((0, 240, W, H), fill=(24, 16, 66))
    for i, y in enumerate(range(250, 316, 12)):
        ln = 300 - i * 18
        d.line((600 - ln, y, 600 + ln, y), fill=(255, 110, 170), width=3)
    # palms framing
    palm(d, 330, 245, 1.1, colour=(20, 60, 46))
    palm(d, 1120, 245, 0.9, colour=(20, 60, 46))
    palm(d, 60, 250, 0.8, colour=(20, 60, 46))
    save(img, "03-gta.png")


# ---------------------------------------------------------------- 4 Anthropic
def v04():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    sky(d, (16, 28, 52), (40, 70, 120), 0, 250)
    # Nasdaq tower (Times Square): dark tower, glowing screen — large
    d.rectangle((90, 70, 330, 250), fill=(14, 22, 44))
    d.rectangle((112, 92, 308, 228), fill=(20, 160, 120))
    # rising chart on the screen
    pts = [(124, 212), (158, 188), (188, 194), (222, 152), (252, 132),
           (296, 92)]
    d.line(pts, fill=WHITE, width=6, joint="curve")
    for x, y in pts:
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=OCHRE)
    # candlesticks, left of the rocket
    for x, o, c in ((360, 200, 150), (392, 176, 128), (424, 150, 182)):
        d.rectangle((x, min(c, o), x + 18, max(c, o)), fill=(46, 200, 130))
        d.line((x + 9, min(c, o) - 14, x + 9, max(c, o) + 14),
               fill=(46, 200, 130), width=3)
    # second tower with lit windows, far right
    d.rectangle((1020, 110, 1130, 250), fill=(18, 28, 52))
    for wy in range(126, 240, 20):
        for wx in range(1032, 1118, 20):
            d.rectangle((wx, wy, wx + 9, wy + 10), fill=(250, 220, 140))
    # rocket launching, centre-right — bigger (flame stays above the
    # ground line at y=250 so it is not covered by the ground fill)
    rx, ry = 720, 130
    d.polygon([(rx, ry - 105), (rx - 36, ry - 14), (rx + 36, ry - 14)],
              fill=RED)
    d.rectangle((rx - 36, ry - 14, rx + 36, ry + 62), fill=WHITE)
    d.ellipse((rx - 14, ry - 60, rx + 14, ry - 28), fill=SKY,
              outline=NAVY, width=3)
    d.polygon([(rx - 36, ry + 62), (rx - 70, ry + 104), (rx - 36, ry + 78)],
              fill=OCHRE)
    d.polygon([(rx + 36, ry + 62), (rx + 70, ry + 104), (rx + 36, ry + 78)],
              fill=OCHRE)
    for i, (sx, sw) in enumerate(((rx - 22, 44), (rx - 12, 24), (rx - 5, 10))):
        d.polygon([(sx, ry + 104), (sx + sw, ry + 104),
                   (rx + 5, ry + 96 + i * 6)], fill=(255, 180 - i * 30, 60))
    # gold coins low, near the ground line
    for cx, cy, r in ((520, 222, 16), (566, 200, 11), (950, 220, 18),
                      (1000, 196, 12)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD,
                  outline=OCHRE_D, width=2)
    ground(d, 250, (12, 20, 40))
    save(img, "04-anthropic.png")


# ---------------------------------------------------------------- 5 Xavier
def v05():
    img = Image.new("RGB", (W, H), (30, 60, 80))
    d = ImageDraw.Draw(img)
    sky(d, (52, 84, 110), (150, 170, 180), 0, 210)
    # dark storm cloud band
    d.ellipse((-40, 20, 320, 90), fill=(70, 88, 104))
    d.ellipse((220, 8, 560, 74), fill=(84, 100, 116))
    d.ellipse((820, 16, 1240, 88), fill=(70, 88, 104))
    # ocean
    d.rectangle((0, 210, W, H), fill=(28, 96, 118))
    waves(d, 230, 310, (180, 220, 230), amp=5)
    # cyclone spiral, centre-left over the sea
    spiral(d, 430, 150, 105, (245, 245, 245), width=8)
    spiral(d, 430, 150, 105, (180, 200, 210), width=3)
    # island with shelter, right
    d.ellipse((820, 225, 1150, 285), fill=(86, 150, 84))
    d.rectangle((940, 205, 1060, 232), fill=(170, 120, 70))
    d.polygon([(925, 208), (1000, 168), (1075, 208)], fill=(150, 70, 50))
    d.rectangle((985, 214, 1015, 232), fill=(60, 40, 24))
    palm(d, 880, 240, 1.0)
    palm(d, 1100, 242, 0.85)
    # rain streaks
    for x in range(40, 1180, 52):
        d.line((x, 120, x - 14, 165), fill=(200, 215, 225), width=2)
    save(img, "05-xavier.png")


# ---------------------------------------------------------------- 6 Akvan
def v06():
    img = Image.new("RGB", (W, H), (40, 70, 90))
    d = ImageDraw.Draw(img)
    sky(d, (90, 120, 140), (200, 190, 160), 0, 200)
    sun(d, 1020, 90, 34, (255, 200, 110))
    # Bay of Bengal + Indian east coast (curved landmass, right)
    d.rectangle((0, 200, W, H), fill=(30, 100, 124))
    d.polygon([(760, 200), (900, 200), (980, 260), (1020, 320), (1200, 320),
               (1200, 200)], fill=(120, 150, 96))
    d.polygon([(760, 200), (900, 200), (980, 260), (1020, 320), (1200, 320),
               (1200, 200)], outline=(220, 210, 180), width=3)
    for tx, ty in ((830, 215), (950, 235), (1080, 250)):
        d.ellipse((tx, ty, tx + 34, ty + 22), fill=(52, 110, 66))
    # cyclone spiral offshore, left-centre
    spiral(d, 380, 140, 95, (245, 245, 245), width=8)
    # big waves + fishing boat
    waves(d, 225, 305, (200, 228, 235), amp=7)
    d.polygon([(620, 262), (700, 262), (680, 282), (640, 282)], fill=(140, 70, 40))
    d.line((660, 262, 660, 220), fill=(80, 50, 30), width=3)
    d.polygon([(660, 222), (700, 258), (660, 258)], fill=(250, 240, 210))
    # rain
    for x in range(60, 760, 60):
        d.line((x, 100, x - 12, 140), fill=(205, 218, 228), width=2)
    save(img, "06-akvan.png")


# ---------------------------------------------------------------- 7 2+2 Tokyo
def v07():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)
    sky(d, (150, 195, 225), (245, 225, 200), 0, 230)
    # Mt Fuji silhouette
    d.polygon([(60, 230), (330, 60), (600, 230)], fill=(120, 140, 165))
    d.polygon([(285, 98), (330, 60), (375, 98), (350, 116), (330, 104),
               (310, 116)], fill=WHITE)
    # Tokyo Tower: red-white lattice tower, centre
    tx = 700
    d.polygon([(tx - 58, 250), (tx - 14, 60), (tx + 14, 60), (tx + 58, 250)],
              fill=(200, 60, 40))
    d.rectangle((tx - 20, 52, tx + 20, 66), fill=(200, 60, 40))
    d.line((tx, 52, tx, 26), fill=(200, 60, 40), width=4)
    for y in (110, 160, 205):
        d.rectangle((tx - 44 + (y - 60) // 6, y, tx + 44 - (y - 60) // 6, y + 10),
                    fill=WHITE)
    # skyline blocks
    for x, w, h in ((430, 44, 90), (490, 36, 120), (820, 50, 110),
                    (890, 40, 80), (950, 46, 130), (1060, 40, 95)):
        building(d, x, 250, w, h, NAVY, windows=True)
    ground(d, 250, (90, 130, 90))
    # two flags: India + Japan
    flagpole(d, 560, 250, 120)
    flag_in(d, 564, 132, 64, 42)
    flagpole(d, 1010, 250, 120)
    flag_jp(d, 1014, 132, 64, 42)
    # cherry blossom petals
    for px, py in ((180, 90), (240, 140), (420, 80), (520, 120), (880, 70),
                   (1140, 130), (300, 200), (960, 200)):
        d.ellipse((px, py, px + 12, py + 9), fill=(245, 180, 200))
    save(img, "07-tokyo.png")


# ---------------------------------------------------------------- 8 COP31
def v08():
    img = Image.new("RGB", (W, H), (120, 190, 205))
    d = ImageDraw.Draw(img)
    sky(d, (140, 200, 225), (250, 230, 190), 0, 210)
    sun(d, 180, 95, 40)
    # Taurus mountains + Antalya coast
    d.polygon([(0, 210), (180, 120), (360, 190), (520, 130), (700, 205),
               (700, 210), (0, 210)], fill=(90, 120, 130))
    d.polygon([(180, 120), (150, 148), (210, 148)], fill=WHITE)
    d.rectangle((0, 210, W, 260), fill=(40, 150, 170))  # Mediterranean
    for x in range(0, W, 60):
        d.line((x, 232, x + 34, 232), fill=(200, 235, 240), width=3)
    # beach + palms
    d.rectangle((0, 260, W, H), fill=(238, 220, 180))
    palm(d, 90, 272, 1.0)
    palm(d, 1120, 274, 0.9)
    # draft papers on a table, centre — large so the "slimmed draft"
    # (144 -> 80 paragraphs) is the visible hook of the scene
    d.rectangle((480, 226, 900, 244), fill=(120, 80, 50))
    d.line((500, 244, 500, 306), fill=(120, 80, 50), width=7)
    d.line((880, 244, 880, 306), fill=(120, 80, 50), width=7)
    d.polygon([(520, 232), (540, 192), (640, 192), (622, 232)], fill=WHITE,
              outline=(180, 180, 180), width=2)   # sheet 1 (flat, lined)
    d.polygon([(650, 232), (672, 196), (772, 196), (752, 232)],
              fill=(235, 240, 235), outline=(180, 180, 180), width=2)
    for lx, ly in ((552, 202), (556, 212), (690, 206), (694, 216)):
        d.line((lx, ly, lx + 52, ly), fill=(90, 110, 90), width=3)
    # green leaf sprig on the papers
    d.ellipse((688, 178, 724, 200), fill=(60, 140, 80))
    d.ellipse((722, 186, 752, 202), fill=(74, 160, 90))
    save(img, "08-cop31.png")


# ---------------------------------------------------------------- 9 UniCredit
def v09():
    img = Image.new("RGB", (W, H), (200, 210, 220))
    d = ImageDraw.Draw(img)
    sky(d, (170, 195, 215), (235, 228, 205), 0, 240)
    # Frankfurt skyline: Commerzbank tower (triangular top) + Main Tower
    ground(d, 240, (70, 78, 88))
    d.polygon([(120, 240), (120, 90), (175, 60), (230, 90), (230, 240)],
              fill=(52, 66, 96))  # Commerzbank
    for wy in range(100, 230, 18):
        d.rectangle((140, wy, 210, wy + 8), fill=(250, 220, 140))
    d.rectangle((300, 110, 360, 240), fill=(70, 84, 112))  # Main Tower
    d.rectangle((368, 150, 420, 240), fill=(88, 100, 126))
    d.rectangle((450, 180, 500, 240), fill=(60, 74, 100))
    # second bank tower + bridge/arch joining them, right
    d.rectangle((760, 80, 830, 240), fill=(40, 56, 88))
    d.rectangle((860, 120, 920, 240), fill=(58, 72, 102))
    for wy in range(100, 230, 18):
        d.rectangle((772, wy, 818, wy + 8), fill=(250, 220, 140))
    # golden arch bridge between the two towers
    d.arc((700, 150, 960, 330), 180, 360, fill=OCHRE, width=10)
    # converging arrows above the bridge
    d.line((700, 130, 800, 90), fill=RED, width=6)
    d.polygon([(800, 90), (776, 88), (792, 108)], fill=RED)
    d.line((920, 130, 820, 90), fill=RED, width=6)
    d.polygon([(820, 90), (844, 88), (828, 108)], fill=RED)
    # gold coins at the base
    for cx, cy, r in ((560, 268, 18), (600, 252, 13), (640, 270, 15)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD,
                  outline=OCHRE_D, width=2)
    save(img, "09-unicredit.png")


# ---------------------------------------------------------------- 10 Lula
def v10():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)
    sky(d, (150, 195, 225), (250, 215, 160), 0, 235)  # sunrise over Brasilia
    sun(d, 150, 82, 40, (255, 190, 100))
    # National Congress: twin towers + bowl + dome
    ground(d, 235, (96, 150, 92))
    d.rectangle((470, 110, 500, 235), fill=WHITE)
    d.rectangle((510, 110, 540, 235), fill=WHITE)
    d.rectangle((460, 100, 550, 112), fill=(220, 220, 220))
    d.polygon([(380, 235), (380, 205), (465, 205), (465, 235)], fill=WHITE)
    d.pieslice((380, 150, 465, 235), 0, 180, fill=WHITE)  # dome up
    d.pieslice((545, 185, 630, 270), 180, 360, fill=WHITE)  # bowl down
    d.rectangle((545, 205, 630, 235), fill=WHITE)
    # Cathedral hyperboloid curves, right
    for k in range(7):
        x = 760 + k * 26
        d.arc((x - 40, 120, x + 40, 300), 200, 340, fill=WHITE, width=5)
    # Brazilian flag on a pole, left
    flagpole(d, 300, 235, 130)
    flag_br(d, 304, 108, 66, 44)
    # decree paper + seal, foreground centre-right — large and legible
    d.polygon([(680, 252), (800, 242), (824, 306), (704, 316)], fill=WHITE,
              outline=GREY, width=2)
    for i, y in enumerate((264, 276, 288)):
        d.line((698, y, 792, y - 5), fill=(100, 110, 120), width=3)
    d.ellipse((700, 292, 720, 310), fill=RED)  # seal
    save(img, "10-lula.png")


# ---------------------------------------------------------------- 11 Mrima Hill
def v11():
    img = Image.new("RGB", (W, H), (235, 210, 170))
    d = ImageDraw.Draw(img)
    sky(d, (160, 200, 225), (245, 220, 170), 0, 220)
    sun(d, 150, 90, 38, (255, 190, 100))
    # Mrima Hill: red-earth terraced open pit
    ground(d, 220, (150, 90, 60))
    d.polygon([(0, 220), (240, 150), (480, 190), (700, 140), (900, 185),
               (1200, 150), (1200, 320), (0, 320)], fill=(168, 96, 58))
    d.polygon([(0, 250), (300, 215), (600, 245), (900, 210), (1200, 240),
               (1200, 320), (0, 320)], fill=(140, 76, 46))
    d.polygon([(0, 285), (350, 260), (700, 288), (1050, 258), (1200, 280),
               (1200, 320), (0, 320)], fill=(116, 60, 38))
    # rare-earth crystals jutting from the terraces
    for cx, cy, s, c in ((420, 240, 26, (90, 130, 170)),
                         (455, 246, 18, (120, 160, 200)),
                         (820, 232, 30, (90, 130, 170)),
                         (860, 240, 20, (70, 110, 150)),
                         (1010, 250, 22, (120, 160, 200))):
        d.polygon([(cx - s, cy), (cx - s * 0.4, cy - s * 1.6),
                   (cx + s * 0.5, cy - s * 1.2), (cx + s, cy)],
                  fill=c, outline=(60, 80, 110), width=2)
    # acacia tree + Kenyan flag
    d.line((180, 230, 180, 150), fill=(90, 60, 30), width=6)
    d.ellipse((120, 128, 250, 152), fill=(70, 120, 60))
    flagpole(d, 1080, 250, 110)
    flag_ke(d, 1084, 142, 62, 40)
    # dump truck silhouette on a terrace
    d.rectangle((560, 268, 640, 292), fill=(40, 40, 40))
    d.rectangle((640, 276, 668, 292), fill=(40, 40, 40))
    d.ellipse((580, 288, 600, 308), fill=(20, 20, 20))
    d.ellipse((620, 288, 640, 308), fill=(20, 20, 20))
    d.ellipse((648, 288, 666, 306), fill=(20, 20, 20))
    save(img, "11-mrima.png")


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn in (v01, v02, v03, v04, v05, v06, v07, v08, v09, v10, v11):
        fn()


if __name__ == "__main__":
    main()
