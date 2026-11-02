"""Render the 20 carousel scripts (docs/social/carousels.json) to JPGs.

Outputs social/out/<slug>/tiktok-NN.jpg (1080x1920), instagram-NN.jpg (1080x1350),
contact-sheet.jpg, and social/out/index.md with every caption.

Run from the repo root:  python3 scripts/social.py && python3 social/render/render.py
"""
import json, os, re, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from greece_style import slide, font, ROOT, IMG_DIR, NAVY, CREAM, INK, OCHRE

OUT = os.path.join(ROOT, 'social', 'out')
DATA = os.path.join(ROOT, 'docs', 'social', 'carousels.json')
SIZES = {'tiktok': (1080, 1920), 'instagram': (1080, 1350)}
# Rhythm across 8 slides: cover at the bottom, then alternate, call to action on a card.
LAYOUTS = ['bottom', 'top', 'card', 'bottom', 'top', 'card', 'bottom', 'card']
# Keep text clear of TikTok's on-screen buttons and caption at the bottom.
SAFE_BOTTOM = {'tiktok': 330, 'instagram': 110}

PLACES = ['santorini', 'lefkada', 'corfu', 'crete', 'athens', 'rhodes', 'paxos', 'kefalonia', 'zakynthos', 'ithaca',
          'mykonos', 'naxos', 'paros', 'syros', 'milos', 'sifnos', 'folegandros', 'thessaloniki', 'piraeus', 'cyclades', 'ionian']


def place_check(carousels):
    """A slide may not pair a place name with a photo whose file name names a different place."""
    problems = []
    for c in carousels:
        for i, s in enumerate(c['slides'], 1):
            text = f"{s['kicker']} {s['headline']} {s['line']}".lower()
            named = {p for p in PLACES if p in text}
            in_photo = {p for p in PLACES if p in s['photo']}
            if named and in_photo and not (named & in_photo):
                problems.append(f"{c['slug']} slide {i}: text names {sorted(named)} but photo is {s['photo']}")
            if not os.path.exists(os.path.join(IMG_DIR, s['photo'] + '.jpg')):
                problems.append(f"{c['slug']} slide {i}: missing photo {s['photo']}")
    return problems


def contact_sheet(paths_t, paths_i, title, dest):
    tw, th = 180, 320          # TikTok thumbs
    iw, ih = 180, 225          # Instagram thumbs
    gap, pad, head = 14, 30, 70
    W = pad * 2 + 8 * tw + 7 * gap
    H = head + 24 + th + 30 + ih + pad
    sheet = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(sheet)
    d.text((pad, 22), title, font=font('serif-bold', 30), fill=INK)
    d.text((pad, head + 2), '1080×1920', font=font('sans', 16), fill=INK)
    for k, p in enumerate(paths_t):
        sheet.paste(Image.open(p).resize((tw, th), Image.LANCZOS), (pad + k * (tw + gap), head + 24))
    y2 = head + 24 + th + 30
    d.text((pad, y2 - 22), '1080×1350', font=font('sans', 16), fill=INK)
    for k, p in enumerate(paths_i):
        sheet.paste(Image.open(p).resize((iw, ih), Image.LANCZOS), (pad + k * (iw + gap), y2))
    sheet.save(dest, quality=82, optimize=True, progressive=True)


def main(only=None):
    carousels = json.load(open(DATA))
    problems = place_check(carousels)
    if problems:
        print('\n'.join(problems)); sys.exit(1)
    index = ['# Rendered carousels', '',
             'JPGs for TikTok (1080×1920) and Instagram (1080×1350), rendered by `social/render/render.py` from the scripts in `docs/social/`. '
             'Photos are illustrative and are not always of the place named on a slide; no slide pairs a place name with a photo of a different named place.', '']
    for c in carousels:
        if only and c['slug'] != only:
            continue
        folder = os.path.join(OUT, c['slug'])
        os.makedirs(folder, exist_ok=True)
        made = {k: [] for k in SIZES}
        n = len(c['slides'])
        for i, s in enumerate(c['slides'], 1):
            for kind, (w, h) in SIZES.items():
                im = slide(s['photo'], w, h, LAYOUTS[(i - 1) % len(LAYOUTS)], s['kicker'], s['headline'], s['line'],
                           counter=f'{i}/{n}', safe_bottom=SAFE_BOTTOM[kind], head_size=88 if i == 1 else 80)
                path = os.path.join(folder, f'{kind}-{i:02d}.jpg')
                im.save(path, quality=80, optimize=True, progressive=True)
                made[kind].append(path)
        contact_sheet(made['tiktok'], made['instagram'], c['title'], os.path.join(folder, 'contact-sheet.jpg'))
        index += [f"## {c['title']}", '', f"Folder: [`{c['slug']}/`]({c['slug']}/) · format: {c['fmt']} · links to {c['article']}", '',
                  f"![Contact sheet]({c['slug']}/contact-sheet.jpg)", '', '**Caption**', '', c['caption'], '']
        print('rendered', c['slug'])
    if not only:
        open(os.path.join(OUT, 'index.md'), 'w').write('\n'.join(index))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
