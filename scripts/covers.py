"""Render every guide cover in one visual system (matches the Payhip covers).

Outputs covers/<key>-1600x2560.jpg (KDP/portrait) and covers/<key>-1000x1000.jpg (square).
Run from the repo root:  python3 scripts/covers.py

System: full-bleed photo from src/static/img; navy (8,22,38) gradient rising from ~30% to
~66% of the height plus a light navy fade at the top; ochre (232,178,72) dot + "GREECE, HONESTLY"
top-left; optional ochre pill badge top-right; big white serif title bottom-left; one serif
subtitle line; two small light bullet lines; an ochre bold Greek phrase with its italic
transliteration and meaning; a short ochre bar and the footer line.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'social', 'render'))
import greece_style as gs  # photo crop, gradient, tracked text, wrap

FONTS = os.path.join(ROOT, 'social', 'render', 'fonts')
OUT = os.path.join(ROOT, 'covers')
NAVY, OCHRE, WHITE, LIGHT = (8, 22, 38), (232, 178, 72), (255, 255, 255), (216, 223, 230)
# Honesty: the site, Payhip and social all disclose AI use, so the cover does too.
FOOTER = 'Written with AI tools, checked in Greece'

def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

# key: title, subtitle, bullets (only what the title/format already states), Greek phrase,
# transliteration — meaning (Greece, Honestly fact sheet), photo (as on the site), badge.
GUIDES = {
    'retire': ('Retire in Greece', 'The 2026 edition', ['For retirees moving to Greece', 'Plain English · PDF'],
               'Σιγά-σιγά', 'Sigá-sigá — slowly, slowly', 'coffee', '2026'),
    'nomad': ('Digital Nomad in Greece', 'The 2026 edition', ['For remote workers moving to Greece', 'Plain English · PDF'],
              'Καλημέρα', 'Kaliméra — good morning', 'laptop-sea', '2026'),
    'islands': ('Which Greek Island?', '35 islands compared', ['Find the island that fits your trip', 'Plain English · PDF'],
                'Καλό ταξίδι', 'Kaló taxídi — have a good trip', 'santorini-dome', None),
    'eat': ('What to Eat in Greece', 'The taverna menu decoder', ['For your first night in a taverna', 'Plain English · PDF'],
            'Καλή όρεξη', 'Kalí órexi — enjoy your meal', 'taverna-chairs', None),
    'phrases': ('Survival Greek', '150 phrases + audio', ['Everyday Greek for visitors', 'PDF + audio'],
                'Ευχαριστώ', 'Efcharistó — thank you', 'cyclades-chairs', None),
    'flashcards': ('Survival Greek Flashcards', 'Learn the essentials, card by card', ['For your first weeks in Greece', 'Plain English · PDF'],
                   'Παρακαλώ', 'Parakaló — please', 'athens-street', None),
    'first90': ('Your First 90 Days in Greece', 'The paperwork, in the right order', ['For people moving to Greece', 'Plain English · PDF'],
                'Καλό μήνα', 'Kaló mína — happy new month', 'cyclades-harbour', None),
    'renting': ('Renting in Greece', "The tenant's kit", ['For renting a home in Greece', 'Plain English · PDF'],
                'Γεια σας', 'Yiá sas — hello', 'athens-alley', None),
    'alphabet': ('The Greek Alphabet', 'Cheat sheet', ['Read Greek signs in minutes', 'Free PDF'],
                 'Λιμάνι', 'Limáni — port', 'greek-inscription', 'FREE'),
    'ionian': ('Lefkada & the Ionian Islands, Honestly', 'Six islands and the founder’s island in depth',
               ['Six islands · three itineraries', 'PDF + EPUB'], 'Γεια μας', 'Yiá mas — cheers', 'lefkada-green', None),
    'athens': ('Athens for New Residents', 'Your first weeks, in plain English',
               ['Neighbourhoods · transport · offices', 'PDF + EPUB'], 'Πού είναι…;', 'Pu íne…? — where is…?', 'athens-alley', None),
}


def gradient(im):
    # light navy fade at the top, clear middle, navy rising from 30% to 66% and holding to the bottom.
    # The square format holds proportionally more text, so the navy rises earlier there.
    if im.height / im.width < 1.2:
        return gs.apply_gradient(im, [(0, 0.55), (0.10, 0.15), (0.18, 0.30), (0.40, 0.90), (1, 0.97)])
    return gs.apply_gradient(im, [(0, 0.55), (0.12, 0.12), (0.30, 0.0), (0.66, 0.90), (1, 0.96)])


def badge(d, text, x_right, y, s):
    f = F('DejaVuSans-Bold.ttf', round(26 * s))
    tw = d.textlength(text, font=f) + 0.1 * f.size * (len(text) - 1)
    padx, h = round(22 * s), round(46 * s)
    x0 = x_right - tw - 2 * padx
    d.rounded_rectangle((x0, y, x_right, y + h), radius=h // 2, fill=OCHRE)
    gs.tracked(d, (x0 + padx, y + (h - f.size) // 2 - round(2 * s)), text, f, NAVY, 0.1)


def render(key, w, h):
    title, subtitle, bullets, greek, translit, photo, bdg = GUIDES[key]
    s = w / 1080
    m = round(76 * s)
    width = w - 2 * m
    im = gradient(gs.photo(photo, w, h))
    d = ImageDraw.Draw(im)
    gs.brand(d, w, s)
    if bdg:
        badge(d, bdg, w - m, round(66 * s), s)
    # measure the bottom block and shrink the title until everything fits below ~30% height
    limit = h * 0.30
    for tsize in range(round(118 * s), round(54 * s), -2):
        ft = F('DejaVuSerif-Bold.ttf', tsize)
        tl = gs.wrap(d, title, ft, width)
        if len(tl) > 4:
            continue
        fsub = F('DejaVuSerif.ttf', round(40 * s))
        sub = subtitle
        while d.textlength(sub, font=fsub) > width and fsub.size > round(26 * s):
            fsub = F('DejaVuSerif.ttf', fsub.size - 2)
        fb = F('DejaVuSans.ttf', round(28 * s))
        fg = F('DejaVuSerif-Bold.ttf', round(44 * s))
        fi = F('LiberationSerif-Italic.ttf', round(32 * s))
        ff = F('DejaVuSans.ttf', round(24 * s))
        lt, gap = round(tsize * 1.1), round(26 * s)
        block = (lt * len(tl) + gap + fsub.size + gap + 2 * round(fb.size * 1.5) + gap +
                 fg.size + round(10 * s) + fi.size + round(40 * s) + ff.size)
        if h - round(96 * s) - block >= limit:
            break
    y = h - round(96 * s) - block
    for line in tl:
        d.text((m, y), line, font=ft, fill=WHITE); y += lt
    y += gap
    d.text((m, y), sub, font=fsub, fill=WHITE); y += fsub.size + gap
    for b in bullets:
        d.text((m, y), '•  ' + b, font=fb, fill=LIGHT); y += round(fb.size * 1.5)
    y += gap
    d.text((m, y), greek, font=fg, fill=OCHRE); y += fg.size + round(10 * s)
    d.text((m, y), translit, font=fi, fill=LIGHT); y += fi.size + round(40 * s)
    bar_w = round(90 * s)
    d.rectangle((m, y + ff.size // 2 - round(4 * s), m + bar_w, y + ff.size // 2 + round(4 * s)), fill=OCHRE)
    d.text((m + bar_w + round(20 * s), y), FOOTER, font=ff, fill=LIGHT)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    for key in GUIDES:
        render(key, 1600, 2560).save(os.path.join(OUT, f'{key}-1600x2560.jpg'), quality=88, optimize=True, progressive=True)
        render(key, 1000, 1000).save(os.path.join(OUT, f'{key}-1000x1000.jpg'), quality=86, optimize=True, progressive=True)
        print('cover', key)
    # contact sheet for a quick visual check
    keys = list(GUIDES)
    tw, th, sq = 200, 320, 200
    sheet = Image.new('RGB', (len(keys) * (tw + 12) + 12, th + sq + 36), (251, 247, 239))
    for i, k in enumerate(keys):
        sheet.paste(Image.open(os.path.join(OUT, f'{k}-1600x2560.jpg')).resize((tw, th)), (12 + i * (tw + 12), 12))
        sheet.paste(Image.open(os.path.join(OUT, f'{k}-1000x1000.jpg')).resize((sq, sq)), (12 + i * (tw + 12), th + 24))
    sheet.save(os.path.join(OUT, 'contact-sheet.jpg'), quality=82)


if __name__ == '__main__':
    main()
