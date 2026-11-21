#!/usr/bin/env python3
"""Build the 21 Nov 2026 world-news image: a dense 5x6 grid of 30 stories.

Programmatic Pillow layout, so every headline stays legible. Each card has a
region tag, a short headline and one supporting detail line.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
INK = (17, 24, 39)
MUTED = (75, 85, 99)

REGION_COLORS = {
    "EUROPE": (37, 99, 235),
    "UKRAINE": (202, 138, 4),
    "MIDDLE EAST": (190, 24, 93),
    "ASIA": (5, 150, 105),
    "MARKETS": (124, 58, 237),
    "SPACE": (13, 148, 136),
    "TECH": (2, 132, 199),
    "AFRICA": (217, 119, 6),
    "AMERICAS": (220, 38, 38),
    "CLIMATE": (22, 163, 74),
    "WORLD": (71, 85, 105),
    "HEALTH": (219, 39, 119),
}

STORIES = [
    ("CLIMATE", "COP31 runs into overtime in Antalya", "Nearly 200 countries deadlocked; draft drops fossil-fuel phase-out"),
    ("EUROPE", "Two Russian missiles and a drone land in Poland", "NATO jets scrambled; Warsaw calls it a deliberate provocation"),
    ("UKRAINE", "Russian strikes hit Kyiv bridges, kill 8, injure 28", "Attacks across nine regions overnight"),
    ("UKRAINE", "Ballistic missiles hit Kryvyi Rih", "A child and a paramedic killed; 21+ injured in a double-tap strike"),
    ("MIDDLE EAST", "Houthi missile hits Riyadh's PIF Tower", "Saudi civil defence alerts early Saturday; danger later passed"),
    ("MIDDLE EAST", "Houthis advance toward Aden", "Saudi replaces its Yemen commander; fighters within ~100 km of the port"),
    ("ASIA", "Cyclone Akvan makes landfall in Odisha", "370,000 evacuated; winds 70-80 km/h, heavy rain and floods"),
    ("EUROPE", "UK and EU sign post-Brexit reset deal", "Food trade, linked carbon markets and a youth mobility scheme"),
    ("MARKETS", "S&P 500 enters correction as AI stocks plunge", "S&P -3.7%; Nasdaq -5%; Nikkei -5.1%"),
    ("MARKETS", "Anthropic closes 17% above its IPO price", "$97.17; about $1.76tn valuation, the biggest IPO on record"),
    ("SPACE", "BepiColombo reaches Mercury after 8 years", "Twin probes enter orbit after a journey of about 10bn km"),
    ("MIDDLE EAST", "Trump weighs renewed strikes on Iran", "US and Israeli officials press him to act before year-end"),
    ("EUROPE", "Denmark foils Russian plot to kill a rapper", "Kyivstoner targeted in Denmark; Russia's defence attache expelled"),
    ("MIDDLE EAST", "Iraqi forces enter a Kataib Hezbollah stronghold", "Jurf al-Sakhar held by the militia for over a decade"),
    ("CLIMATE", "Ukraine blocks a Russian climate report at COP31", "Report used data from occupied territories"),
    ("EUROPE", "Estonia shuts its borders", "Russia complains of a 'new Iron Curtain' after a drone-maker attack"),
    ("TECH", "California subpoenas Nvidia over China chips", "Export-control concerns over AI chips"),
    ("AFRICA", "Dozens missing after a migrant boat capsizes off Senegal", "Rescue search under way"),
    ("ASIA", "Pakistan military kills 22 militants", "Raids near the Afghan border"),
    ("AMERICAS", "Haiti police kill 34 suspected gang members", "Raid in Port-au-Prince"),
    ("MIDDLE EAST", "Israel ends its tank operation in central Gaza", "Operation concluded"),
    ("CLIMATE", "AI data centres could sharply raise emissions", "Warning as AI power demand soars"),
    ("WORLD", "UN: 1 in 4 women cannot refuse sex with a partner", "Global report on consent"),
    ("AMERICAS", "Flash floods hit Florida; storms threaten California", "El Nino storm brings heavy rain"),
    ("WORLD", "Trump, Xi and Putin hold a first three-way summit", "Joint peace declaration signed in Shenzhen"),
    ("WORLD", "World Court: Myanmar committed genocide", "First such ruling against a state, over the Rohingya"),
    ("AMERICAS", "Melania Trump wishes for another Russia ceasefire", "Christmas wish list teases a new peace push"),
    ("TECH", "JPMorgan, Visa and Mastercard hit via vendors", "Third-party breach in an extortion attack"),
    ("WORLD", "Geneva agrees a text on killer robots", "Non-binding; binding rules still out of reach"),
    ("HEALTH", "Malaria vaccine shows 87% protection in first trial", "PfSPZ-LARC2 human efficacy trial"),
]

def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # Header
    d.rectangle([0, 0, W, 88], fill=(15, 23, 42))
    d.text((16, 12), "THE WORLD IN ONE PICTURE", font=font(30, True), fill=(255, 255, 255))
    d.text((16, 52), "SATURDAY, 21 NOVEMBER 2026  •  30 STORIES  •  12 SECTIONS", font=font(17), fill=(191, 219, 254))
    d.text((W - 16, 52), "make.fun", font=font(17, True), fill=(147, 197, 253), anchor="ra")
    # Grid: 5 cols x 6 rows
    margin, gap = 12, 8
    cols, rows = 5, 6
    cw = (W - 2 * margin - (cols - 1) * gap) // cols
    ch = (H - 88 - 28 - margin - (rows - 1) * gap) // rows
    top = 88 + 10
    for i, (region, head, detail) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = margin + c * (cw + gap)
        y = top + r * (ch + gap)
        color = REGION_COLORS[region]
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=8, fill=(248, 250, 252), outline=(226, 232, 240))
        d.rounded_rectangle([x, y, x + cw, y + 5], radius=3, fill=color)
        d.text((x + 8, y + 11), region, font=font(10, True), fill=color)
        d.text((x + cw - 8, y + 11), f"{i + 1:02d}", font=font(10, True), fill=color, anchor="ra")
        lines = wrap(d, head, font(13, True), cw - 16)[:3]
        ly = y + 30
        for ln in lines:
            d.text((x + 8, ly), ln, font=font(13, True), fill=INK)
            ly += 17
        dlines = wrap(d, detail, font(11), cw - 16)[:2]
        for ln in dlines:
            d.text((x + 8, ly + 2), ln, font=font(11), fill=MUTED)
            ly += 14
    d.text((16, H - 22), "Sources: Reuters, AP, OneTurn, Augerton  •  Headlines as reported on 21 Nov 2026", font=font(11), fill=MUTED)
    img.save("/home/hatch/workspace/makefun-news-20261121/entry.png", "PNG")
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
