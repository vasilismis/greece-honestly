"""Render the Pinterest set (1000x1500) in the photo system and write the CSVs.

Outputs:
  social/pinterest/pins/<NN-slug>.jpg     33 pins: one per site article (22) + one per product (11)
  social/pinterest/pins.csv               file, title, description, destination URL, board
  social/pinterest/pinterest-bulk.csv     Pinterest bulk-create format (Title, Media URL, Pinterest board,
                                          Description, Link, Keywords) with raw.githubusercontent media URLs
  social/pinterest/contact-sheet-pins.jpg overview
Run from the repo root:  python3 scripts/pins.py
Texts reuse the checked article facts only.
"""
import ast, csv, os, re, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'social', 'render'))
import greece_style as gs

OUT = os.path.join(ROOT, 'social', 'pinterest')
PINS = os.path.join(OUT, 'pins')
SITE = 'https://vasilismis.github.io/greece-honestly/articles/'
RAW = 'https://raw.githubusercontent.com/vasilismis/greece-honestly/main/social/pinterest/pins/'
SHOP = 'https://payhip.com/GreeceHonestly'
AI = 'AI characters, written in Greece.'
W, H = 1000, 1500
STRIP = 120
NAVY, OCHRE, WHITE, LIGHT, CREAM, INK, AEGEAN = gs.NAVY, gs.OCHRE, gs.WHITE, gs.LIGHT, gs.CREAM, gs.INK, gs.AEGEAN

B_MOVE = 'Moving to Greece: Checklists & Tips'
B_GREEK = 'Learn Greek: Phrases & Alphabet'
B_ISL = 'Greek Islands: Where to Go'
B_FOOD = 'Greek Food: What to Eat in Greece'
B_LIVE = 'Living in Greece, Honestly'
B_ION = 'Lefkada & the Ionian'

# Article pins: slug, board, photo, kicker, headline, line, keywords
ARTICLES = [
 ('retiring-to-greece-2026', B_MOVE, 'mountain-village', 'Moving to Greece', 'Retiring to Greece in 2026', 'Residence, the 7% tax and healthcare, in the right order.', 'retire in Greece, retirement visa Greece, Greece 7% tax, S1 Greece'),
 ('greece-7-percent-flat-tax-foreign-pensions', B_MOVE, 'athens-street', 'Money numbers', 'The 7% pension tax, explained', '€2,800 instead of about €8,900 on a €40,000 pension.', 'Greece 7% tax, foreign pension Greece, retire in Greece tax, article 5B'),
 ('greece-digital-nomad-visa-2026', B_MOVE, 'laptop-sea', 'Remote work', 'Greece digital nomad visa 2026', '€3,500 a month net, and a visa from the consulate first.', 'Greece digital nomad visa, remote work Greece, work from Greece, nomad visa 2026'),
 ('which-greek-island-is-right-for-you', B_ISL, 'santorini-wide', 'Island guide', 'Which Greek island is right for you?', 'Seven island groups and a quick quiz.', 'Greek islands, best Greek island, Cyclades, Ionian islands, Greece travel'),
 ('greek-island-hopping-three-routes', B_ISL, 'ferry', 'Island hopping', 'Three island routes that work', 'Two or three islands beat five. Three nights each.', 'Greek island hopping, Greece itinerary, Cyclades route, ferry Greece'),
 ('what-to-order-in-a-greek-taverna', B_FOOD, 'taverna-tables', 'Food and drink', 'What to order in a Greek taverna', 'Ten classic dishes and how the bill works.', 'Greek food, Greek taverna, what to eat in Greece, Greek dishes'),
 ('greek-phrases-for-your-first-week', B_GREEK, 'cyclades-chairs', 'Speak a little Greek', '20 Greek phrases for week one', 'Kaliméra, efcharistó, parakaló, with simple pronunciation.', 'learn Greek, Greek phrases, Greek for travellers, basic Greek'),
 ('how-to-read-greek-signs-alphabet', B_GREEK, 'greek-inscription', 'Greek alphabet', 'Read Greek signs in ten minutes', 'Ρ is r, Η is i and Β is v.', 'Greek alphabet, read Greek, learn Greek letters, Greek signs'),
 ('lefkada-travel-guide', B_ION, 'lefkada-green', 'The island you can drive to', 'Lefkada: a practical guide', 'Beaches as they are today, villages and when to go.', 'Lefkada, Lefkas, Lefkada beaches, Ionian islands, Porto Katsiki'),
 ('ionian-islands-compared', B_ION, 'corfu-boats', 'Six islands side by side', 'The Ionian islands compared', 'Corfu, Paxos, Lefkada, Kefalonia, Ithaca and Zakynthos.', 'Ionian islands, Corfu, Kefalonia, Zakynthos, Paxos, Ithaca'),
 ('renting-a-flat-in-greece', B_MOVE, 'athens-alley', 'Renting', 'Renting a flat in Greece', 'The three-year rule binds you too. Read this first.', 'rent in Greece, Greek lease, renting Athens, tenant Greece'),
 ('first-90-days-in-greece', B_MOVE, 'cyclades-harbour', 'Moving to Greece', 'Your first 90 days in Greece', 'AFM, phone, lease, bank, AMKA, in the right order.', 'moving to Greece, Greece checklist, AFM, AMKA, expat Greece'),
 ('how-to-order-coffee-in-greece', B_FOOD, 'coffee', 'Coffee', 'How to order coffee in Greece', 'Skétos, métrios or glykós: say it when you order.', 'Greek coffee, freddo espresso, frappé, Greece cafe'),
 ('greek-taverna-etiquette', B_FOOD, 'taverna-chairs', 'Taverna etiquette', 'Eating out in Greece: the unwritten rules', 'Bread, fish by the kilo, the bill and the tip.', 'Greek taverna, eating out Greece, tipping in Greece, Greek food'),
 ('getting-an-afm-greek-tax-number', B_MOVE, 'laptop-sea', 'Paperwork', 'Get your Greek AFM first', 'Apply online, then a video call or a tax office visit.', 'AFM Greece, Greek tax number, moving to Greece, myAADE'),
 ('amka-explained', B_MOVE, 'mountain-village', 'Paperwork', 'AMKA explained', 'Who can get Greece’s social security number, and how.', 'AMKA Greece, Greek social security, healthcare Greece, expat Greece'),
 ('opening-a-greek-bank-account', B_MOVE, 'athens-street', 'Paperwork', 'Opening a Greek bank account', 'Passport, AFM, proof of address, and your rights.', 'Greek bank account, banking Greece, expat Greece, moving to Greece'),
 ('where-to-live-in-athens', B_LIVE, 'athens-alley', 'Athens', 'Where to live in Athens', 'Koukaki, Pangrati, Kypseli, Glyfada and Kifisia.', 'Athens neighbourhoods, living in Athens, rent Athens, expat Athens'),
 ('greek-islands-in-october-and-november', B_ISL, 'crete-rocks', 'Out of season', 'Greek islands in autumn', 'Big islands keep living. Small islands go to sleep.', 'Greek islands October, Greece in November, Crete autumn, off season Greece'),
 ('greek-ferries-how-to-book', B_ISL, 'ferry', 'Ferries', 'Greek ferries: how to book', 'E-tickets, ID and arriving an hour early.', 'Greek ferries, ferry tickets Greece, island hopping, Greece travel tips'),
 ('greek-public-holidays-2027', B_LIVE, 'santorini-dome', 'Dates', 'Greek public holidays 2027', 'Orthodox Easter is on 2 May 2027.', 'Greek holidays 2027, Greek Easter 2027, Greece calendar, public holidays Greece'),
 ('greek-phrases-for-the-pharmacy-and-doctor', B_GREEK, 'cyclades-harbour', 'Speak a little Greek', 'Greek for the pharmacy', 'Symptoms, allergies and emergencies in simple Greek.', 'Greek phrases, pharmacy Greece, travel health Greece, learn Greek'),
]
# Product pins: key, board, photo, badge-ish kicker, headline, line, URL, keywords
PRODUCTS = [
 ('retire', B_MOVE, 'coffee', 'PDF guide · 2026', 'Retire in Greece 2026', 'For retirees moving to Greece.', 'https://payhip.com/b/vrQHk', 'retire in Greece, Greece retirement guide, 7% tax Greece'),
 ('nomad', B_MOVE, 'laptop-sea', 'PDF guide · 2026', 'Digital Nomad in Greece 2026', 'For remote workers moving to Greece.', 'https://payhip.com/b/Eniwq', 'digital nomad Greece, remote work Greece, nomad visa guide'),
 ('islands', B_ISL, 'santorini-dome', 'PDF guide', 'Which Greek Island?', '35 islands compared.', 'https://payhip.com/b/MiE5C', 'Greek islands guide, best Greek island, island comparison'),
 ('eat', B_FOOD, 'taverna-chairs', 'PDF guide', 'What to Eat in Greece', 'The taverna menu decoder.', 'https://payhip.com/b/9avjp', 'Greek food guide, Greek menu, taverna, what to eat in Greece'),
 ('phrases', B_GREEK, 'cyclades-chairs', 'PDF + audio', 'Survival Greek', '150 phrases + audio.', 'https://payhip.com/b/7oGHa', 'learn Greek, Greek phrasebook, Greek audio, Survival Greek'),
 ('flashcards', B_GREEK, 'athens-street', 'PDF', 'Survival Greek Flashcards', 'Survival Greek, card by card.', 'https://payhip.com/b/EIdK0', 'Greek flashcards, learn Greek, Greek vocabulary'),
 ('first90', B_MOVE, 'cyclades-harbour', 'PDF guide', 'Your First 90 Days in Greece', 'For people moving to Greece.', 'https://payhip.com/b/PT5D7', 'moving to Greece, Greece relocation guide, AFM AMKA'),
 ('renting', B_LIVE, 'athens-alley', 'PDF guide', 'Renting in Greece', "The tenant's kit.", 'https://payhip.com/b/d2DGi', 'renting in Greece, Greek lease, tenant guide Greece'),
 ('alphabet', B_GREEK, 'greek-inscription', 'Free download', 'Greek Alphabet Cheat Sheet', 'Free. Read Greek signs.', 'https://payhip.com/b/pY9Ot', 'Greek alphabet, free Greek cheat sheet, learn Greek letters'),
 ('ionian', B_ION, 'lefkada-bay', 'New guide · PDF + EPUB', 'Lefkada & the Ionian Islands, Honestly', 'Six islands and three itineraries.', SHOP, 'Lefkada guide, Ionian islands guide, Corfu Kefalonia Zakynthos'),
 ('athens', B_LIVE, 'athens-street', 'New guide · PDF + EPUB', 'Athens for New Residents', 'Neighbourhoods, transport and offices.', SHOP, 'moving to Athens, Athens guide, living in Athens'),
]
GUIDE_NAMES = {'retire': 'Retire in Greece 2026', 'nomad': 'Digital Nomad in Greece 2026', 'islands': 'Which Greek Island? 35 islands compared',
               'eat': 'What to Eat in Greece', 'phrases': 'Survival Greek: 150 phrases + audio', 'flashcards': 'Survival Greek Flashcards',
               'first90': 'Your First 90 Days in Greece', 'renting': "Renting in Greece: the tenant's kit", 'alphabet': 'FREE Greek Alphabet Cheat Sheet',
               'ionian': 'Lefkada & the Ionian Islands, Honestly', 'athens': 'Athens for New Residents'}
# Free reading on the site that goes with each product (used in descriptions).
PRODUCT_ARTICLES = {'retire': 'retiring to Greece and the 7% tax', 'nomad': 'the digital nomad visa', 'islands': 'choosing an island and island hopping',
                    'eat': 'what to order in a taverna', 'phrases': '20 phrases for your first week', 'flashcards': '20 phrases for your first week',
                    'first90': 'your first 90 days, the AFM and the AMKA', 'renting': 'renting a flat and where to live in Athens',
                    'alphabet': 'reading Greek signs', 'ionian': 'Lefkada and the Ionian islands compared', 'athens': 'Athens neighbourhoods and renting'}

PLACES = {'santorini': {'santorini', 'cyclades'}, 'lefkada': {'lefkada', 'ionian'}, 'corfu': {'corfu', 'ionian'}, 'crete': {'crete'},
          'athens': {'athens'}, 'cyclades': {'cyclades', 'santorini', 'naxos', 'paros', 'milos', 'sifnos', 'folegandros', 'syros'}}
PLACE_WORDS = ['santorini', 'lefkada', 'corfu', 'crete', 'athens', 'cyclades', 'ionian', 'paxos', 'kefalonia', 'ithaca', 'zakynthos',
               'rhodes', 'mykonos', 'naxos', 'paros', 'syros', 'milos', 'sifnos', 'folegandros']


def place_ok(photo, text):
    named = {p for p in PLACE_WORDS if p in text.lower()}
    in_photo = [k for k in PLACES if k in photo]
    if not named or not in_photo:
        return True
    return any(named & PLACES[k] for k in in_photo)


def crop(name, focus, zoom):
    """Cover-crop with a focus point and zoom, so the same photo can look different."""
    im = Image.open(os.path.join(gs.IMG_DIR, name + '.jpg')).convert('RGB')
    scale = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    fx, fy = focus
    left = min(max(0, round(im.width * fx - W / 2)), im.width - W)
    top = min(max(0, round(im.height * fy - H / 2)), im.height - H)
    return im.crop((left, top, left + W, top + H))


def F(kind, size):
    return gs.font(kind, size)


def render(photo, layout, focus, zoom, kicker, headline, line, strip_text):
    im = crop(photo, focus, zoom)
    s = W / 1080
    hh = H - STRIP
    if layout == 'bottom':
        im = gs.apply_gradient(im, [(0, 0.7), (0.1, 0.2), (0.3, 0.0), (0.55, 0.75), (0.92, 0.95), (1, 0.97)])
    elif layout == 'top':
        im = gs.apply_gradient(im, [(0, 0.95), (0.42, 0.8), (0.62, 0.1), (0.85, 0.15), (1, 0.6)])
    else:
        im = gs.apply_gradient(im, [(0, 0.75), (0.15, 0.3), (0.85, 0.3), (1, 0.7)])
    d = ImageDraw.Draw(im)
    gs.brand(d, W, s)
    m = round(72 * s)
    width = W - 2 * m
    fk = F('sans-bold', round(30 * s))
    if layout == 'card':
        pad = round(56 * s)
        cw = W - 2 * round(60 * s)
        inner = cw - 2 * pad
        fh, hl = gs.fit(d, headline, 'serif-bold', round(84 * s), inner, 4, round(48 * s))
        fl, ll = gs.fit(d, line, 'sans', round(38 * s), inner, 3, round(28 * s))
        lh, lb = round(fh.size * 1.14), round(fl.size * 1.4)
        ch = pad * 2 + fk.size + round(20 * s) + lh * len(hl) + round(24 * s) + lb * len(ll) + round(40 * s)
        cx, cy = (W - cw) // 2, (hh - ch) // 2 + round(30 * s)
        d.rounded_rectangle((cx, cy, cx + cw, cy + ch), 34, fill=CREAM)
        y = cy + pad
        gs.tracked(d, (cx + pad, y), kicker.upper(), fk, gs.OCHRE_DEEP, 0.12); y += fk.size + round(20 * s)
        for t in hl:
            d.text((cx + pad, y), t, font=fh, fill=AEGEAN); y += lh
        y += round(24 * s)
        for t in ll:
            d.text((cx + pad, y), t, font=fl, fill=INK); y += lb
        d.rectangle((cx + pad, y + round(14 * s), cx + pad + round(100 * s), y + round(24 * s)), fill=OCHRE)
    else:
        fh, hl = gs.fit(d, headline, 'serif-bold', round(104 * s), width, 4, round(56 * s))
        fl, ll = gs.fit(d, line, 'sans', round(42 * s), width, 3, round(30 * s))
        lh, lb = round(fh.size * 1.12), round(fl.size * 1.4)
        block = fk.size + round(22 * s) + lh * len(hl) + round(26 * s) + lb * len(ll) + round(40 * s)
        y = round(190 * s) if layout == 'top' else hh - round(70 * s) - block
        gs.tracked(d, (m, y), kicker.upper(), fk, OCHRE, 0.12); y += fk.size + round(22 * s)
        for t in hl:
            d.text((m, y), t, font=fh, fill=WHITE); y += lh
        y += round(26 * s)
        for t in ll:
            d.text((m, y), t, font=fl, fill=LIGHT); y += lb
        d.rectangle((m, y + round(16 * s), m + round(100 * s), y + round(26 * s)), fill=OCHRE)
    # clean bottom strip
    d.rectangle((0, hh, W, H), fill=NAVY)
    d.rectangle((0, hh, W, hh + 4), fill=OCHRE)
    fs = F('sans-bold', round(28 * s))
    r = round(9 * s)
    cy = hh + STRIP // 2
    d.ellipse((m, cy - r, m + 2 * r, cy + r), fill=OCHRE)
    txt = strip_text
    while d.textlength(txt, font=fs) > width - 3 * r and len(txt) > 10:
        txt = txt[:-2].rstrip() + '…'
    d.text((m + 3 * r, cy - fs.size // 2 - 2), txt, font=fs, fill=WHITE)
    return im


def pin_variants(i):
    layouts = ['bottom', 'top', 'card']
    focuses = [(0.5, 0.5), (0.32, 0.5), (0.68, 0.5), (0.5, 0.35), (0.5, 0.65), (0.4, 0.45), (0.6, 0.55)]
    zooms = [1.0, 1.18, 1.32]
    return layouts[i % 3], focuses[i % len(focuses)], zooms[(i // 3) % 3]


def article_descriptions():
    src = open(os.path.join(ROOT, 'scripts', 'pinterest.py')).read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'P':
            return ast.literal_eval(node.value)
    raise SystemExit('P not found in scripts/pinterest.py')


def main():
    os.makedirs(PINS, exist_ok=True)
    P = article_descriptions()
    rows, errors, n = [], [], 0
    for slug, board, photo, kicker, headline, line, kw in ARTICLES:
        n += 1
        title, desc, _tags = P[slug][0]
        rows.append(dict(file=f'{n:02d}-{slug}.jpg', title=title, desc=f'{desc} Free on our website. {AI}', url=SITE + slug + '/',
                         board=board, kw=kw, photo=photo, kicker=kicker, headline=headline, line=line, strip='greece-honestly site · free article'))
    for key, board, photo, kicker, headline, line, url, kw in PRODUCTS:
        n += 1
        name = GUIDE_NAMES[key]
        free = 'free' if key == 'alphabet' else 'a downloadable guide'
        desc = (f'{name} is {free} from Greece, Honestly, in plain English. Start with our free articles on {PRODUCT_ARTICLES[key]}, '
                f'then get the guide on Payhip, where you can see what is inside before you decide. {AI}')
        rows.append(dict(file=f'{n:02d}-guide-{key}.jpg', title=f'{name} | Greece, Honestly guide', desc=desc, url=url, board=board, kw=kw,
                         photo=photo, kicker=kicker, headline=headline, line=line, strip=name))
    for i, r in enumerate(rows):
        layout, focus, zoom = pin_variants(i)
        if len(r['title']) > 100: errors.append(f"{r['file']}: title {len(r['title'])}")
        if len(r['desc']) > 500: errors.append(f"{r['file']}: description {len(r['desc'])}")
        if not r['desc'].endswith(AI): errors.append(f"{r['file']}: AI line")
        if not place_ok(r['photo'], r['headline'] + ' ' + r['line'] + ' ' + r['kicker']):
            errors.append(f"{r['file']}: place rule ({r['photo']})")
        r['layout'] = layout
    if errors:
        raise SystemExit('\n'.join(errors))
    for i, r in enumerate(rows):
        layout, focus, zoom = pin_variants(i)
        render(r['photo'], layout, focus, zoom, r['kicker'], r['headline'], r['line'], r['strip']).save(
            os.path.join(PINS, r['file']), quality=84, optimize=True, progressive=True)
    with open(os.path.join(OUT, 'pins.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['file', 'title', 'description', 'destination_url', 'board'])
        for r in rows:
            w.writerow([f"social/pinterest/pins/{r['file']}", r['title'], r['desc'], r['url'], r['board']])
    with open(os.path.join(OUT, 'pinterest-bulk.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['Title', 'Media URL', 'Pinterest board', 'Description', 'Link', 'Keywords'])
        for r in rows:
            w.writerow([r['title'], RAW + r['file'], r['board'], r['desc'], r['url'], r['kw']])
    # contact sheet
    tw, th, cols = 160, 240, 11
    rws = (len(rows) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (tw + 10) + 10, rws * (th + 10) + 10), CREAM)
    for i, r in enumerate(rows):
        sheet.paste(Image.open(os.path.join(PINS, r['file'])).resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    sheet.save(os.path.join(OUT, 'contact-sheet-pins.jpg'), quality=82)
    print(f'{len(rows)} pins rendered; CSVs written')


if __name__ == '__main__':
    main()
