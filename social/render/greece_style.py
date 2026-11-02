"""Greece, Honestly visual system for images (carousels, guide covers, section openers).

Approved system: full-bleed photo (cover-crop), dark navy gradient (#081626) for contrast,
ochre dot + "GREECE, HONESTLY" top-left, page counter top-right, ochre uppercase kicker,
white bold serif headline, light grey body, short ochre bar at the bottom.
Three layouts: text at the bottom, text at the top, or a cream card centred on the photo.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG_DIR = os.path.join(ROOT, 'src', 'static', 'img')
FONT_DIR = os.path.join(HERE, 'fonts')

NAVY = (8, 22, 38)          # #081626
OCHRE = (232, 178, 72)      # #E8B248
OCHRE_DEEP = (138, 90, 11)  # #8A5A0B, kicker on cream (AA contrast)
CREAM = (251, 247, 239)     # #FBF7EF
WHITE = (255, 255, 255)
LIGHT = (216, 223, 230)     # light grey body
INK = (34, 49, 63)          # #22313F
AEGEAN = (31, 78, 121)      # #1F4E79 (navy headline on the card)

_fonts = {}
def font(kind, size):
    name = {'sans': 'DejaVuSans.ttf', 'sans-bold': 'DejaVuSans-Bold.ttf', 'serif-bold': 'DejaVuSerif-Bold.ttf'}[kind]
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _fonts[key]


def photo(name, w, h):
    """Open src/static/img/<name>.jpg and cover-crop it to w×h."""
    im = Image.open(os.path.join(IMG_DIR, name + '.jpg')).convert('RGB')
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def gradient(w, h, stops):
    """Navy overlay. stops: list of (y_fraction, alpha 0..1), linearly interpolated, top to bottom."""
    col = Image.new('L', (1, h))
    for y in range(h):
        f = y / max(1, h - 1)
        for (f0, a0), (f1, a1) in zip(stops, stops[1:]):
            if f0 <= f <= f1:
                t = 0 if f1 == f0 else (f - f0) / (f1 - f0)
                col.putpixel((0, y), round(255 * (a0 + (a1 - a0) * t)))
                break
    mask = col.resize((w, h))
    layer = Image.new('RGB', (w, h), NAVY)
    return layer, mask


def apply_gradient(im, stops):
    layer, mask = gradient(im.width, im.height, stops)
    im.paste(layer, (0, 0), mask)
    return im


def tracked(draw, xy, text, fnt, fill, tracking=0.0, anchor_right=False):
    """Draw text with letter spacing (tracking in em). Returns the width drawn."""
    x, y = xy
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * fnt.size * (len(text) - 1)
    if anchor_right:
        x -= total
    for ch, cw in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += cw + tracking * fnt.size
    return total


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        test = (cur + ' ' + wd).strip()
        if draw.textlength(test, font=fnt) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, kind, size, width, max_lines, min_size=24):
    """Largest font size (down from size) that wraps text into max_lines within width."""
    while size >= min_size:
        f = font(kind, size)
        lines = wrap(draw, text, f, width)
        if len(lines) <= max_lines and all(draw.textlength(l, font=f) <= width for l in lines):
            return f, lines
        size -= 2
    f = font(kind, min_size)
    return f, wrap(draw, text, f, width)


def brand(draw, w, scale, counter=None, on_light=False):
    """Ochre dot + GREECE, HONESTLY top-left; optional n/N top-right."""
    m = round(72 * scale)
    y = round(78 * scale)
    r = round(11 * scale)
    fb = font('sans-bold', round(28 * scale))
    draw.ellipse((m, y + fb.size // 2 - r + 2, m + 2 * r, y + fb.size // 2 + r + 2), fill=OCHRE)
    tracked(draw, (m + 2 * r + round(16 * scale), y), 'GREECE, HONESTLY', fb, INK if on_light else WHITE, 0.08)
    if counter:
        fc = font('sans', round(28 * scale))
        tracked(draw, (w - m, y), counter, fc, INK if on_light else WHITE, 0.05, anchor_right=True)


def block_height(parts):
    return sum(h for h, _ in parts)


def text_block(draw, x, y, width, kicker, headline, body, scale, on_card=False, head_size=84, max_head_lines=4, measure=False):
    """Kicker / headline / body stacked from (x, y). Returns total height."""
    fk = font('sans-bold', round(32 * scale))
    fh, hl = fit(draw, headline, 'serif-bold', round(head_size * scale), width, max_head_lines, round(40 * scale))
    fbody, bl = fit(draw, body, 'sans', round(40 * scale), width, 5, round(28 * scale)) if body else (None, [])
    gap1, gap2 = round(22 * scale), round(28 * scale)
    lh = round(fh.size * 1.16)
    lb = round(fbody.size * 1.42) if fbody else 0
    total = (fk.size + gap1 if kicker else 0) + lh * len(hl) + (gap2 + lb * len(bl) if bl else 0)
    if measure:
        return total
    cy = y
    if kicker:
        tracked(draw, (x, cy), kicker.upper(), fk, OCHRE_DEEP if on_card else OCHRE, 0.12)
        cy += fk.size + gap1
    for line in hl:
        draw.text((x, cy), line, font=fh, fill=AEGEAN if on_card else WHITE)
        cy += lh
    if bl:
        cy += gap2
        for line in bl:
            draw.text((x, cy), line, font=fbody, fill=INK if on_card else LIGHT)
            cy += lb
    return total


def ochre_bar(draw, x, y, scale):
    draw.rectangle((x, y, x + round(110 * scale), y + round(10 * scale)), fill=OCHRE)


def slide(photo_name, w, h, layout, kicker, headline, body, counter=None, safe_bottom=None, head_size=84):
    """Render one slide. layout: 'bottom', 'top' or 'card'."""
    scale = w / 1080
    m = round(72 * scale)
    width = w - 2 * m
    im = photo(photo_name, w, h)
    if layout == 'bottom':
        im = apply_gradient(im, [(0, 0.78), (0.1, 0.35), (0.2, 0.0), (0.38, 0.05), (0.62, 0.78), (1, 0.95)])
    elif layout == 'top':
        im = apply_gradient(im, [(0, 0.95), (0.45, 0.75), (0.7, 0.1), (0.86, 0.0), (1, 0.55)])
    else:
        im = apply_gradient(im, [(0, 0.78), (0.12, 0.3), (0.82, 0.25), (1, 0.6)])
    d = ImageDraw.Draw(im)
    brand(d, w, scale, counter)
    bottom_margin = safe_bottom if safe_bottom is not None else round(110 * scale)
    bar_y = h - bottom_margin
    if layout == 'card':
        pad = round(64 * scale)
        cw = w - 2 * round(64 * scale)
        inner = cw - 2 * pad
        th = text_block(d, 0, 0, inner, kicker, headline, body, scale, True, head_size, measure=True)
        ch = th + 2 * pad + round(10 * scale) + round(34 * scale)
        cx, cy = (w - cw) // 2, (h - ch) // 2
        shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rounded_rectangle((cx, cy + 14, cx + cw, cy + ch + 14), 34, fill=(0, 0, 0, 90))
        im.paste(shadow.filter(ImageFilter.GaussianBlur(18)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(18)))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((cx, cy, cx + cw, cy + ch), 34, fill=CREAM)
        text_block(d, cx + pad, cy + pad, inner, kicker, headline, body, scale, True, head_size)
        ochre_bar(d, cx + pad, cy + ch - pad + round(14 * scale), scale)
    elif layout == 'top':
        y0 = round(190 * scale)
        text_block(d, m, y0, width, kicker, headline, body, scale, False, head_size)
        ochre_bar(d, m, bar_y, scale)
    else:
        th = text_block(d, m, 0, width, kicker, headline, body, scale, False, head_size, measure=True)
        y0 = bar_y - round(44 * scale) - th
        text_block(d, m, y0, width, kicker, headline, body, scale, False, head_size)
        ochre_bar(d, m, bar_y, scale)
    return im
