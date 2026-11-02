"""Build a Greece, Honestly guide: cover, thumbnail, section openers, print PDFs (A4 + US Letter) and EPUB.

Usage (from the repo root):  python3 guides/build.py <slug>
Needs: Python 3 + Pillow, pandoc, Node + Playwright (Chromium).

Source: guides/<slug>/content.md. A chapter heading can name an opener photo and a kicker:
    # Lefkada in depth {#lefkada photo=lefkada-green kicker="The founder's island"}
Outputs go to guides/<slug>/out/.
"""
import json, os, re, shutil, subprocess, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'social', 'render'))
import greece_style as gs  # noqa: E402

BOOKS = {
    'ionian-islands-honestly': dict(
        title='Lefkada & the Ionian Islands, Honestly',
        subtitle='Six islands, three itineraries and the founder’s home island in depth',
        kicker='A Greece, Honestly guide',
        cover_photo='lefkada-green', thumb_photo='lefkada-bay',
        description='A practical guide to Lefkada, Corfu, Paxos, Kefalonia, Ithaca and Zakynthos.',
    ),
    'athens-for-new-residents': dict(
        title='Athens for New Residents',
        subtitle='Neighbourhoods, transport, offices and your first week, in plain English',
        kicker='A Greece, Honestly guide',
        cover_photo='athens-alley', thumb_photo='athens-street',
        description='A practical guide for people moving to Athens: where to rent, how to get around and where to go for paperwork.',
    ),
}
DISCLOSURE = ('Greece, Honestly is presented by AI-generated characters. This guide was written with AI tools and '
              'checked in Greece. General information, not legal, tax or medical advice.')


def cover(book, w, h, dest):
    scale = w / 1080
    im = gs.photo(book['cover_photo'], w, h)
    if h / w < 1.2:  # square thumbnail: text starts higher, so darken earlier
        im = gs.apply_gradient(im, [(0, 0.85), (0.12, 0.3), (0.28, 0.45), (0.45, 0.88), (1, 0.97)])
    else:
        im = gs.apply_gradient(im, [(0, 0.85), (0.14, 0.25), (0.42, 0.1), (0.66, 0.85), (1, 0.97)])
    d = ImageDraw.Draw(im)
    gs.brand(d, w, scale)
    m = round(72 * scale)
    width = w - 2 * m
    # title block above the bottom
    fk = gs.font('sans-bold', round(30 * scale))
    ft, tl = gs.fit(d, book['title'], 'serif-bold', round(104 * scale), width, 4, round(56 * scale))
    fs, sl = gs.fit(d, book['subtitle'], 'sans', round(40 * scale), width, 4, round(28 * scale))
    lt, ls = round(ft.size * 1.12), round(fs.size * 1.4)
    fd = gs.font('sans', round(24 * scale))
    dl = gs.wrap(d, 'Written with AI tools, checked in Greece', fd, width)
    block = fk.size + round(28 * scale) + lt * len(tl) + round(34 * scale) + ls * len(sl)
    bottom = h - round(150 * scale)
    y = bottom - block
    gs.tracked(d, (m, y), book['kicker'].upper(), fk, gs.OCHRE, 0.12)
    y += fk.size + round(28 * scale)
    for line in tl:
        d.text((m, y), line, font=ft, fill=gs.WHITE); y += lt
    y += round(34 * scale)
    for line in sl:
        d.text((m, y), line, font=fs, fill=gs.LIGHT); y += ls
    gs.ochre_bar(d, m, h - round(110 * scale), scale)
    for i, line in enumerate(dl):
        d.text((m + round(140 * scale), h - round(118 * scale) + i * round(30 * scale)), line, font=fd, fill=gs.LIGHT)
    im.save(dest, quality=90, optimize=True, progressive=True)


def opener(photo, kicker, number, dest, w=1600, h=820):
    scale = w / 1080
    im = gs.photo(photo, w, h)
    im = gs.apply_gradient(im, [(0, 0.55), (0.3, 0.05), (0.6, 0.2), (1, 0.88)])
    d = ImageDraw.Draw(im)
    gs.brand(d, w, scale * 0.8)
    m = round(72 * scale * 0.8)
    fn = gs.font('serif-bold', round(120 * scale * 0.8))
    fk = gs.font('sans-bold', round(30 * scale * 0.8))
    y = h - round(80 * scale * 0.8) - fn.size - round(6 * scale)
    d.text((m, y), f'{number:02d}', font=fn, fill=gs.WHITE)
    gs.ochre_bar(d, m, h - round(56 * scale * 0.8), scale * 0.8)
    im.save(dest, quality=84, optimize=True, progressive=True)


HEAD = re.compile(r'^# (?P<title>.+?) \{(?P<attrs>[^}]*)\}\s*$', re.M)


def preprocess(md, out):
    """Insert an opener image before every chapter heading that names a photo."""
    n = 0
    def repl(m):
        nonlocal n
        attrs = m.group('attrs')
        photo = re.search(r'photo=([\w-]+)', attrs)
        kicker = re.search(r'kicker="([^"]+)"', attrs)
        ident = re.search(r'#([\w-]+)', attrs)
        if not photo:
            return m.group(0)
        places = ['santorini', 'lefkada', 'corfu', 'crete', 'athens', 'cyclades', 'paxos', 'kefalonia', 'ithaca', 'zakynthos']
        in_photo = {p for p in places if p in photo.group(1)}
        in_title = {p for p in places if p in m.group('title').lower()}
        if in_photo and in_title and not in_photo & in_title:
            sys.exit(f"place rule: chapter '{m.group('title')}' uses photo {photo.group(1)}")
        if in_photo and not in_title and m.group('title').lower() not in ('how to use this guide', 'three sample itineraries'):
            sys.exit(f"place rule: chapter '{m.group('title')}' uses place photo {photo.group(1)}")
        n += 1
        name = f'opener-{n:02d}.jpg'
        opener(photo.group(1), kicker.group(1) if kicker else '', n, os.path.join(out, name))
        alt = gs_alt(photo.group(1))
        k = f'<p class="kicker">{kicker.group(1)}</p>\n\n' if kicker else ''
        return (f'![{alt}]({name}){{.opener}}\n\n{k}# {m.group("title")} {{#{ident.group(1) if ident else "ch" + str(n)} .chapter}}')
    return HEAD.sub(repl, md)


def gs_alt(photo):
    # Alt text comes from the site's image catalogue (src/images.mjs).
    src = open(os.path.join(ROOT, 'src', 'images.mjs')).read()
    m = re.search(r"'?%s'?: \{ alt: '([^']+)'" % re.escape(photo), src)
    return m.group(1) if m else 'Photo'


def main(slug):
    book = BOOKS[slug]
    base = os.path.join(HERE, slug)
    out = os.path.join(base, 'out')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    # 1. Cover (KDP 1600x2560) and square thumbnail
    # Covers come from the shared cover system (scripts/covers.py -> covers/), so site, Payhip and stores match.
    key = {'ionian-islands-honestly': 'ionian', 'athens-for-new-residents': 'athens'}[slug]
    shared = os.path.join(ROOT, 'covers')
    if not os.path.exists(os.path.join(shared, f'{key}-1600x2560.jpg')):
        subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'covers.py')], check=True)
    shutil.copy(os.path.join(shared, f'{key}-1600x2560.jpg'), os.path.join(out, 'cover-1600x2560.jpg'))
    shutil.copy(os.path.join(shared, f'{key}-1000x1000.jpg'), os.path.join(out, 'thumbnail-1000x1000.jpg'))
    # 2. Content with openers
    md = open(os.path.join(base, 'content.md')).read()
    md = preprocess(md, out)
    open(os.path.join(out, 'book.md'), 'w').write(md)
    shutil.copy(os.path.join(HERE, 'print.css'), os.path.join(out, 'print.css'))
    shutil.copy(os.path.join(HERE, 'epub.css'), os.path.join(out, 'epub.css'))
    for f in os.listdir(os.path.join(ROOT, 'src', 'static', 'fonts')):
        if f.endswith('.woff2'):
            os.makedirs(os.path.join(out, 'fonts'), exist_ok=True)
            shutil.copy(os.path.join(ROOT, 'src', 'static', 'fonts', f), os.path.join(out, 'fonts', f))
    meta = ['--metadata', f'title={book["title"]}', '--metadata', f'subtitle={book["subtitle"]}',
            '--metadata', 'author=Greece, Honestly', '--metadata', 'lang=en-GB',
            '--metadata', f'description={book["description"]}', '--metadata', f'rights={DISCLOSURE}']
    # 3. HTML for print
    subprocess.run(['pandoc', 'book.md', '-f', 'markdown-implicit_figures', '-t', 'html5', '-s', '--toc', '--toc-depth=1',
                    '--template', os.path.join(HERE, 'print-template.html'), '-c', 'print.css',
                    '-V', f'disclosure={DISCLOSURE}', '-o', 'book.html'] + meta, cwd=out, check=True)
    # 4. PDFs (A4 and US Letter) with Chromium
    subprocess.run(['node', os.path.join(HERE, 'pdf.cjs'), os.path.join(out, 'book.html'), os.path.join(out, f'{slug}-A4.pdf'), 'A4'], check=True)
    subprocess.run(['node', os.path.join(HERE, 'pdf.cjs'), os.path.join(out, 'book.html'), os.path.join(out, f'{slug}-Letter.pdf'), 'Letter'], check=True)
    # 5. EPUB
    subprocess.run(['pandoc', 'book.md', '-f', 'markdown-implicit_figures', '-t', 'epub3', '--toc', '--toc-depth=1', '--split-level=1',
                    '--epub-cover-image=cover-1600x2560.jpg', '--css', 'epub.css', '-o', f'{slug}.epub'] + meta,
                   cwd=out, check=True)
    for f in ['book.md', 'book.html', 'print.css', 'epub.css']:
        os.remove(os.path.join(out, f))
    shutil.rmtree(os.path.join(out, 'fonts'))
    print('built', slug, sorted(os.listdir(out)))


if __name__ == '__main__':
    for s in (sys.argv[1:] or BOOKS):
        main(s)
