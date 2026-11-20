#!/usr/bin/env python3
"""Compose the news-image-20261119 front page (1024x1024) — layout D.

Adapted from the 20261118 entry's compose.py (same layout-D formula that
was submitted + accepted): masthead with big date, full-width lead image
band + headline band, 4-column tile grid of illustrated stories 2-11,
world map with 11 numbered pins as a grid cell, two-column index 12-35,
sources line. All text rendered in PIL with real fonts; the 11 vignettes
are text-free illustrations drawn for this entry (vignettes.py); the world
map is drawn from Natural Earth 110m land polygons (public data).

Story text follows research-notes.md (Pass 2 FINAL) exactly: figures are
the verified 19 Nov figures (GTA ~19.1M / ~$1.84B; Anthropic $1.76T at
close, no "~$1.08T"; UniCredit $1.4T, no "$1.43T"; McBride lead 248
votes). Borderline items are framed as documented: #18 Iran/Hormuz as an
UNCONFIRMED claim, #31 Kwara as the 19 Nov NCoS response, #32 NSA as day
3 of the outage, #30 Melbourne Cups as the 19 Nov police reveal +
charges.

Usage: python3 compose.py
Outputs: entry.png (1024x1024) in this directory + layouts/layout-d.png
and a 300px preview.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(HERE, "candidates")
OUT = os.path.join(HERE, "layouts")
W, H = 1024, 1024

PAPER = (250, 247, 240)
CARD = (255, 255, 255)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RULE = (215, 210, 198)
RED = (179, 38, 30)
NAVY = (27, 42, 74)
SEA = (220, 233, 242)
LAND = (232, 224, 208)
LAND_LINE = (190, 180, 158)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

MARG, GUT = 12, 8


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_w):
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


def crop_to_aspect(im, tw, th, roi=None, anchor=(0.5, 0.5)):
    iw, ih = im.size
    if roi is not None:
        x0, y0, x1, y1 = roi
        im = im.crop((int(iw * x0), int(ih * y0), int(iw * x1), int(ih * y1)))
        iw, ih = im.size
    target = tw / th
    src = iw / ih
    if src > target:
        nw = int(ih * target)
        x = int((iw - nw) * anchor[0])
        im = im.crop((x, 0, x + nw, ih))
    else:
        nh = int(iw / target)
        y = int((ih - nh) * anchor[1])
        im = im.crop((0, y, iw, y + nh))
    return im.resize((tw, th), Image.LANCZOS)


# ------------------------------------------------------------------ data
STORIES = [
    dict(num=1, file="01-trilateral.png", region="ASIA",
         headline="FIRST-EVER XI\u2013PUTIN\u2013TRUMP TRILATERAL",
         sub="Four-point peace declaration at Kylin Villa; no deal on "
             "Ukraine, Iran or trade. US\u2013China truce extended.",
         lat=22.55, lon=114.06),
    dict(num=2, file="02-icj.png", region="EUROPE",
         headline="ICJ: MYANMAR GUILTY OF GENOCIDE",
         sub="First state genocide verdict in 80 years; 9\u20136.",
         lat=52.09, lon=4.31),
    dict(num=3, file="03-gta.png", region="OCEANIA",
         headline="GTA VI LAUNCHES WORLDWIDE",
         sub="~19.1M copies, ~$1.84B; Metacritic 99.",
         lat=-36.85, lon=174.76),
    dict(num=4, file="04-anthropic.png", region="NORTH AMERICA",
         headline="ANTHROPIC DEBUTS ON NASDAQ",
         sub="First trade $111.50; close $97.17 (+17.1%).",
         lat=40.71, lon=-74.01),
    dict(num=5, file="05-xavier.png", region="OCEANIA",
         headline="CYCLONE XAVIER, CAT 4",
         sub="Bears down on northern Cook Islands.",
         lat=-10.8, lon=-162.8),
    dict(num=6, file="06-akvan.png", region="ASIA",
         headline="CYCLONE AKVAN, BAY OF BENGAL",
         sub="Severe storm; landfall near Gopalpur.",
         lat=14.5, lon=85.3),
    dict(num=7, file="07-tokyo.png", region="ASIA",
         headline="INDIA\u2013JAPAN 2+2 IN TOKYO",
         sub="Joint statement; supply chains, UNSC seats.",
         lat=35.68, lon=139.69),
    dict(num=8, file="08-cop31.png", region="EUROPE",
         headline="COP31 DRAFT DROPS FOSSIL FUELS",
         sub="Draft cut 144\u219280 paragraphs in Antalya.",
         lat=36.90, lon=30.71),
    dict(num=9, file="09-unicredit.png", region="EUROPE",
         headline="UNICREDIT\u2013COMMERZBANK DEAL",
         sub="Broad agreement; combined assets $1.4T.",
         lat=50.11, lon=8.68),
    dict(num=10, file="10-lula.png", region="SOUTH AMERICA",
         headline="LULA ENDS BRAZIL'S 6x1 WEEK",
         sub="Decree signed; 44\u219240 hours by Dec 2027.",
         lat=-15.79, lon=-47.88),
    dict(num=11, file="11-mrima.png", region="AFRICA",
         headline="KENYA AWARDS MRIMA HILL MINE",
         sub="US-led group wins rare-earth minerals.",
         lat=-4.43, lon=39.25),
]

INDEX = [
    (12, "M4.6 quake hits Negros, Philippines \u2014 no damage expected."),
    (13, "ATP Finals: Zverev beats Fils 6-4, 7-6(6); 3-0 in group."),
    (14, "McBride elected House Democrats co-chair with 248 votes."),
    (15, "Hegseth arrives in Honduras on four-country tour."),
    (16, "NASA holds Voyager 1 \u2018Light-Day\u2019 presser at JPL."),
    (17, "Gaza operation ends; Salah al-Din road reopens."),
    (18, "UNCONFIRMED claim: IRGC says two tankers hit in Hormuz."),
    (19, "Kerch Bridge rail hit again; rail traffic halted."),
    (20, "TSMC, Samsung pause some chip shipments to China."),
    (21, "Argentina logs $3.39bn October trade surplus; record exports."),
    (22, "Colombia president denies NYT joint-ops claim."),
    (23, "Jepchirchir gets 3-year EPO ban; Sydney title stripped."),
    (24, "South Africa beat Bangladesh by 9 wickets, 1st Test."),
    (25, "Kenya launches 10.8m mosquito-net campaign."),
    (26, "Wall St sell-off: Dow -1,101, Nasdaq -2.25%."),
    (27, "Senegal president forces revised budget by decree."),
    (28, "Coalition of the Willing meets in Berlin; nearly 40 leaders."),
    (29, "Albanese to Putin at APEC: \u2018end your war, end it now\u2019."),
    (30, "Fourth Melbourne Cup theft revealed; two men charged."),
    (31, "NCoS chief blames negligence after Kwara jailbreak."),
    (32, "NSA classified network still down on third day."),
    (33, "Kenya Red Cross adds 31 boat engines for flood rescues."),
    (34, "Indonesia passes asset-forfeiture law after 18 years."),
    (35, "Oceania Challenge bowls opens in \u014crewa, New Zealand."),
]

SOURCES = ("Sources: Reuters, AP, AFP, Xinhua, UN News, Fiji Met, IMD, "
           "NASA, PHIVOLCS, Cricinfo, Victoria Police. The day\u2019s news, "
           "Thursday 19 November 2026. Original drawings.")

JUDGE_LINE = ("Every story below happened, or was first reported, "
              "on 19 November 2026.")

VIGNETTES = {s["file"]: Image.open(os.path.join(CAND, s["file"])).convert("RGB")
             for s in STORIES}

with open(os.path.join(HERE, "ne_110m_land.geojson")) as fh:
    GEO = json.load(fh)

LAT_TOP, LAT_BOT = 74.0, -56.0

# Pin nudges as fractions of map width / height: The Hague and Frankfurt
# would otherwise overlap.
PIN_NUDGE = {
    2: (-0.014, -0.05),   # The Hague: up-left
    9: (0.014, 0.05),     # Frankfurt: down-right
}


# ------------------------------------------------------------------ page
class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.warnings = []

    def header(self, rule_y):
        d = self.d
        f_mast = load_font(SERIF_B, 58)
        title = "THE WORLD TODAY"
        tw = d.textlength(title, font=f_mast)
        d.text(((W - tw) / 2, 2), title, fill=INK, font=f_mast)
        f_date = load_font(SANS_B, 17)
        dateline = "THURSDAY 19 NOVEMBER 2026"
        dw = d.textlength(dateline, font=f_date)
        d.text(((W - dw) / 2, 62), dateline, fill=INK, font=f_date)
        f_cnt = load_font(SANS_B, 15)
        count = "35 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY"
        cw = d.textlength(count, font=f_cnt)
        d.text(((W - cw) / 2, 84), count, fill=RED, font=f_cnt)
        f_j = load_font(SERIF_I, 13)
        jw = d.textlength(JUDGE_LINE, font=f_j)
        d.text(((W - jw) / 2, 104), JUDGE_LINE, fill=GREY, font=f_j)
        d.line((MARG, rule_y, W - MARG, rule_y), fill=INK, width=2)

    def badge(self, x, y, r, num, size=14):
        d = self.d
        cx, cy = x + r, y + r
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED)
        f = load_font(SANS_B, size)
        t = str(num)
        d.text((cx - d.textlength(t, font=f) / 2, cy - size / 2 - 1),
               t, fill=CARD, font=f)

    def tile(self, box, story, img_h, hl_size=15, sub_size=11,
             badge_r=12, max_hl=2, max_sub=1):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in box)
        d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RULE, width=1)
        w = x1 - x0
        pic = crop_to_aspect(VIGNETTES[story["file"]], w - 2, img_h,
                             roi=story.get("roi"),
                             anchor=story.get("anchor", (0.5, 0.5)))
        self.img.paste(pic, (x0 + 1, y0 + 1))
        self.badge(x0 + 6, y0 + 6, badge_r, story["num"],
                   size=14 if badge_r >= 12 else 12)
        ty = y0 + 1 + img_h + 5
        d.text((x0 + 6, ty), story["region"], fill=NAVY,
               font=load_font(SANS_B, 10))
        ty += 13
        size = hl_size
        while size > 10:
            f_h = load_font(SANS_B, size)
            if len(wrap_text(d, story["headline"], f_h, w - 12)) <= max_hl:
                break
            size -= 1
        if size <= 10:
            self.warnings.append(f"tile {story['num']}: headline hit shrink floor")
        f_h = load_font(SANS_B, size)
        for line in wrap_text(d, story["headline"], f_h, w - 12)[:max_hl]:
            if ty + size > y1 - 2:
                self.warnings.append(f"tile {story['num']}: headline clipped")
                break
            d.text((x0 + 6, ty), line, fill=INK, font=f_h)
            ty += size + 2
        sub = story["sub"]
        size = sub_size
        while size > 9:
            f_s = load_font(SANS, size)
            if len(wrap_text(d, sub, f_s, w - 12)) <= max_sub:
                break
            size -= 1
        if size <= 9:
            self.warnings.append(f"tile {story['num']}: sub hit shrink floor")
        f_s = load_font(SANS, size)
        for line in wrap_text(d, sub, f_s, w - 12)[:max_sub]:
            if ty + size > y1 - 2:
                self.warnings.append(f"tile {story['num']}: sub clipped")
                break
            d.text((x0 + 6, ty), line, fill=GREY, font=f_s)
            ty += size + 2

    def lead_band(self, img_box, text_box):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in img_box)
        d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RULE, width=1)
        pic = crop_to_aspect(VIGNETTES[STORIES[0]["file"]], x1 - x0 - 2,
                             y1 - y0 - 2)
        self.img.paste(pic, (x0 + 1, y0 + 1))
        self.badge(x0 + 6, y0 + 6, 14, 1, size=16)
        x0, y0, x1, y1 = (int(v) for v in text_box)
        d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RULE, width=1)
        tx, ty = x0 + 10, y0 + 6
        d.text((tx, ty), "ASIA", fill=NAVY, font=load_font(SANS_B, 11))
        ty += 16
        f_h = load_font(SANS_B, 26)
        for line in wrap_text(d, STORIES[0]["headline"], f_h, x1 - tx - 10):
            d.text((tx, ty), line, fill=INK, font=f_h)
            ty += 30
        f_s = load_font(SANS, 13)
        for line in wrap_text(d, STORIES[0]["sub"], f_s, x1 - tx - 10):
            if ty + 13 > y1 - 4:
                self.warnings.append("lead band: sub clipped")
                break
            d.text((tx, ty), line, fill=GREY, font=f_s)
            ty += 17

    def world_map(self, box, pin_r=9):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in box)
        f_t = load_font(SANS_B, 15)
        d.text((x0, y0), "WHERE IT HAPPENED", fill=NAVY, font=f_t)
        d.text((x0 + d.textlength("WHERE IT HAPPENED", font=f_t) + 10, y0 + 2),
               "the 11 pictured stories, numbered", fill=GREY,
               font=load_font(SANS, 12))
        top = y0 + 22
        mw, mh = x1 - x0, y1 - top
        d.rectangle((x0, top, x1, y1), fill=SEA, outline=RULE, width=1)

        def proj(lon, lat):
            px = x0 + (lon + 180.0) / 360.0 * mw
            py = top + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
            return (px, py)

        for feat in GEO["features"]:
            geom = feat["geometry"]
            rings = []
            if geom["type"] == "Polygon":
                rings = geom["coordinates"]
            elif geom["type"] == "MultiPolygon":
                for part in geom["coordinates"]:
                    rings.extend(part)
            for ring in rings:
                pts, prev = [], None
                for lon, lat in ring:
                    if lat > LAT_TOP or lat < LAT_BOT:
                        continue
                    if prev is not None and abs(lon - prev) > 180:
                        if len(pts) > 2:
                            d.polygon(pts, fill=LAND, outline=LAND_LINE)
                        pts = []
                    pts.append(proj(lon, lat))
                    prev = lon
                if len(pts) > 2:
                    d.polygon(pts, fill=LAND, outline=LAND_LINE)

        f_pin = load_font(SANS_B, 11 if pin_r <= 9 else 13)
        for s in STORIES:
            cx, cy = proj(s["lon"], s["lat"])
            fx, fy = PIN_NUDGE.get(s["num"], (0.0, 0.0))
            px, py = cx + fx * mw, cy + fy * mh
            if (fx, fy) != (0.0, 0.0):
                d.line((cx, cy, px, py), fill=RED, width=1)
            d.ellipse((px - pin_r - 1, py - pin_r - 1, px + pin_r + 1,
                       py + pin_r + 1), fill=CARD)
            d.ellipse((px - pin_r, py - pin_r, px + pin_r, py + pin_r),
                      fill=RED)
            t = str(s["num"])
            tw = d.textlength(t, font=f_pin)
            d.text((px - tw / 2, py - f_pin.size / 2 - 1), t, fill=CARD,
                   font=f_pin)

    def index(self, box, cols, font_size, row_h):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in box)
        f_t = load_font(SANS_B, 15)
        d.text((x0, y0), "ALSO ON THIS DAY", fill=NAVY, font=f_t)
        d.text((x0 + d.textlength("ALSO ON THIS DAY", font=f_t) + 10, y0 + 2),
               "stories 12-35", fill=GREY, font=load_font(SANS, 12))
        top = y0 + 22
        f_n = load_font(SANS_B, font_size)
        f_i = load_font(SANS, font_size)
        cw = (x1 - x0 - (cols - 1) * 16) / cols
        per_col = (len(INDEX) + cols - 1) // cols
        for i, (num, text) in enumerate(INDEX):
            c, r = divmod(i, per_col)
            cx = x0 + c * (cw + 16)
            cy = top + r * row_h
            if cy + font_size > y1:
                self.warnings.append(f"index {num}: row past box bottom")
            d.text((cx, cy), f"{num}.", fill=RED, font=f_n)
            nw = d.textlength(f"{num}. ", font=f_n)
            if d.textlength(text, font=f_i) > cw - nw:
                self.warnings.append(f"index {num}: line too wide "
                                     f"({d.textlength(text, font=f_i):.0f}px > "
                                     f"{cw - nw:.0f}px)")
            d.text((cx + nw, cy), text, fill=INK, font=f_i)

    def sources(self, y):
        d = self.d
        d.line((MARG, y - 6, W - MARG, y - 6), fill=RULE, width=1)
        f_s = load_font(SANS, 11)
        for j, line in enumerate(wrap_text(d, SOURCES, f_s, W - 2 * MARG)):
            d.text((MARG, y + j * 14), line, fill=GREY, font=f_s)


# ---------------------------------------------------------------- layout D
def col_x(c, cw):
    return MARG + c * (cw + GUT)


def layout_d():
    """Lead-band + 4-col hybrid (20261118 layout D): full-width lead image
    band + headline band; 2 rows x 4 tiles; row 3 = 2 tiles + map cell
    (2 cols); 2-col index; sources."""
    p = Page()
    p.header(122)
    p.lead_band((MARG, 130, W - MARG, 290), (MARG, 290, W - MARG, 360))
    cw = (W - 2 * MARG - 3 * GUT) / 4  # 244
    for c in range(4):
        p.tile((col_x(c, cw), 368, col_x(c, cw) + cw, 500), STORIES[1 + c],
               img_h=64, hl_size=15, sub_size=11)
    for c in range(4):
        p.tile((col_x(c, cw), 508, col_x(c, cw) + cw, 640), STORIES[5 + c],
               img_h=64, hl_size=15, sub_size=11)
    for c in range(2):
        p.tile((col_x(c, cw), 648, col_x(c, cw) + cw, 776), STORIES[9 + c],
               img_h=62, hl_size=15, sub_size=11)
    p.world_map((col_x(2, cw), 648, W - MARG, 776), pin_r=9)
    p.index((MARG, 784, W - MARG, 968), cols=2, font_size=11, row_h=13.5)
    p.sources(974)
    return p


def main():
    os.makedirs(OUT, exist_ok=True)
    page = layout_d()
    path = os.path.join(OUT, "layout-d.png")
    page.img.save(path, optimize=True)
    page.img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(OUT, "layout-d-300.png"))
    entry = os.path.join(HERE, "entry.png")
    page.img.save(entry, optimize=True)
    size = os.path.getsize(entry)
    print(f"entry.png: {size:,} bytes "
          f"({'OK <=1MiB' if size <= 1048576 else 'OVER 1MiB!'})")
    for w in page.warnings:
        print(f"  WARNING: {w}")
    if not page.warnings:
        print("  no warnings")


if __name__ == "__main__":
    main()
