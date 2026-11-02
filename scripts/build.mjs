// Tiny static site builder for Greece, Honestly.
// Reads Markdown articles from src/articles, writes a complete static site to dist/.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync, cpSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import sharp from 'sharp';
import { site, guides, guideGroups } from '../src/site.mjs';
import { images, guideCovers } from '../src/images.mjs';
import { icon } from '../src/icons.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'dist');
const B = site.basePath; // e.g. "/greece-honestly/"
const abs = (p = '') => site.url + B + p; // absolute URL for canonical, sitemap, RSS, og:image
const rel = (p = '') => B + p; // root-relative link used inside pages

// ---------- helpers ----------
const esc = (s) =>
  String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function parseFrontMatter(src, file) {
  const m = src.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!m) throw new Error(`${file}: missing front matter`);
  const data = {};
  for (const line of m[1].split(/\r?\n/)) {
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const i = line.indexOf(':');
    if (i < 0) throw new Error(`${file}: bad front matter line "${line}"`);
    let v = line.slice(i + 1).trim();
    if (/^(['"]).*\1$/.test(v)) v = v.slice(1, -1);
    data[line.slice(0, i).trim()] = v;
  }
  return { data, body: m[2] };
}

function write(path, content) {
  const full = join(out, path);
  mkdirSync(dirname(full), { recursive: true });
  writeFileSync(full, content);
}

// ---------- images ----------
// Every photo is cropped to 16:9 and written as 480px, 800px and 1600px WebP, plus a 1200×630 JPEG for og:image.
const W = [480, 800, 1600];
const used = new Set();
function checkImage(name, where) {
  if (!images[name]) throw new Error(`${where}: unknown image "${name}" (add it to src/images.mjs)`);
  if (!existsSync(join(root, 'src/static/img', name + '.jpg'))) throw new Error(`${where}: src/static/img/${name}.jpg not found`);
  used.add(name);
}
async function renderImages() {
  mkdirSync(join(out, 'img'), { recursive: true });
  await Promise.all(
    [...used].map(async (name) => {
      const src = join(root, 'src/static/img', name + '.jpg');
      const position = images[name].pos || 'centre';
      for (const w of W) {
        await sharp(src).resize(w, Math.round((w * 9) / 16), { fit: 'cover', position }).webp({ quality: 70 }).toFile(join(out, 'img', `${name}-${w}.webp`));
      }
      await sharp(src).resize(1200, 630, { fit: 'cover', position }).jpeg({ quality: 78, mozjpeg: true }).toFile(join(out, 'img', `${name}-og.jpg`));
    })
  );
  // Guide covers from the shared cover system (scripts/covers.py -> covers/): square for guide cards,
  // portrait for the product card at the end of each article.
  await Promise.all(
    Object.keys(guides).map(async (key) => {
      const sq = join(root, 'covers', `${key}-1000x1000.jpg`);
      const pt = join(root, 'covers', `${key}-1600x2560.jpg`);
      if (!existsSync(sq) || !existsSync(pt)) throw new Error(`missing cover for ${key}: run python3 scripts/covers.py`);
      for (const w of [480, 800]) await sharp(sq).resize(w, w).webp({ quality: 78 }).toFile(join(out, 'img', `cover-${key}-sq-${w}.webp`));
      for (const w of [320, 640]) await sharp(pt).resize(w, Math.round(w * 1.6)).webp({ quality: 78 }).toFile(join(out, 'img', `cover-${key}-pt-${w}.webp`));
    })
  );
}
const srcset = (name) => W.map((w) => `${rel(`img/${name}-${w}.webp`)} ${w}w`).join(', ');
function img(name, { sizes = '100vw', eager = false, lazy = true, cls = '', alt } = {}) {
  checkImage(name, 'img()');
  const a = alt ?? images[name].alt;
  return `<img${cls ? ` class="${cls}"` : ''} src="${rel(`img/${name}-800.webp`)}" srcset="${srcset(name)}" sizes="${sizes}" width="1600" height="900" alt="${esc(a)}" ${
    eager ? 'fetchpriority="high" decoding="async"' : lazy ? 'loading="lazy" decoding="async"' : 'decoding="async"'
  }>`;
}

// ---------- Markdown with a few content blocks ----------
// ::figure name | caption                 → photo with caption
// :::note Title  … :::                     → "Good to know" box (Markdown inside)
// :::quote … :::                           → pull quote
// :::facts  icon | label | value  … :::    → key facts with icons
// :::steps  title | text  … :::            → numbered step strip
marked.use({
  gfm: true,
  renderer: {
    table(token) {
      const html = marked.Renderer.prototype.table.call(this, token);
      return `<div class="table-wrap" role="region" aria-label="Table, scrolls sideways on small screens" tabindex="0">${html}</div>\n`;
    },
  },
  walkTokens(token) {
    if (token.type === 'link' && token.href.startsWith('/') && !token.href.startsWith('//')) {
      token.href = rel(token.href.slice(1));
    }
  },
});
const oneLine = (html) => html.replace(/\n+/g, ' ').trim();
const inline = (s) => marked.parseInline(s.trim());

function blocks(body, file) {
  const fail = (msg) => {
    throw new Error(`${file}: ${msg}`);
  };
  body = body.replace(/^::figure (.+)$/gm, (_, rest) => {
    const [name, caption] = rest.split('|').map((s) => s.trim());
    checkImage(name, file);
    return `<figure class="photo">${img(name, { sizes: '(min-width: 760px) 720px, 100vw' })}${caption ? `<figcaption>${inline(caption)}</figcaption>` : ''}</figure>`;
  });
  return body.replace(/^:::(note|quote|facts|steps)(?: (.*))?\n([\s\S]*?)\n:::$/gm, (_, kind, arg, inner) => {
    const lines = inner.split('\n').filter((l) => l.trim());
    if (kind === 'note') {
      return oneLine(`<aside class="note-box">${icon('info')}<div><p class="note-title">${esc(arg || 'Good to know')}</p>${marked.parse(inner)}</div></aside>`);
    }
    if (kind === 'quote') return oneLine(`<blockquote class="pull"><p>${inline(inner)}</p></blockquote>`);
    const rows = lines.map((l) => l.split('|').map((s) => s.trim()));
    if (kind === 'facts') {
      for (const r of rows) if (r.length !== 3) fail(`facts lines need "icon | label | value": ${r.join('|')}`);
      return `<ul class="facts">${rows.map(([ic, label, value]) => `<li>${icon(ic)}<span class="fact-label">${inline(label)}</span><span class="fact-value">${inline(value)}</span></li>`).join('')}</ul>`;
    }
    for (const r of rows) if (r.length !== 2) fail(`steps lines need "title | text": ${r.join('|')}`);
    return `<ol class="steps">${rows.map(([t, d]) => `<li><span class="step-title">${inline(t)}</span><span class="step-text">${inline(d)}</span></li>`).join('')}</ol>`;
  });
}

// ---------- load articles ----------
const kickers = {
  retire: 'Moving to Greece',
  nomad: 'Moving to Greece',
  first90: 'Moving to Greece',
  renting: 'Moving to Greece',
  islands: 'Islands',
  eat: 'Food and drink',
  phrases: 'Speaking Greek',
  flashcards: 'Speaking Greek',
  alphabet: 'Speaking Greek',
};
const required = ['title', 'description', 'slug', 'guide', 'published', 'order', 'summary', 'hero'];
const articles = readdirSync(join(root, 'src/articles'))
  .filter((f) => f.endsWith('.md'))
  .map((f) => {
    const { data, body } = parseFrontMatter(readFileSync(join(root, 'src/articles', f), 'utf8'), f);
    for (const k of required) if (!data[k]) throw new Error(`${f}: front matter needs "${k}"`);
    if (!guides[data.guide]) throw new Error(`${f}: unknown guide "${data.guide}" (see src/site.mjs)`);
    checkImage(data.hero, f);
    const words = body.replace(/^:::?\w+.*$/gm, '').replace(/[#|*_>`\-]/g, ' ').split(/\s+/).filter(Boolean).length;
    return {
      ...data,
      order: Number(data.order),
      modified: data.modified || data.published,
      lastChecked: data.lastChecked || site.lastChecked,
      kicker: data.kicker || kickers[data.guide],
      html: marked.parse(blocks(body, f)),
      words,
      source: body,
      file: f,
    };
  })
  .sort((a, b) => a.order - b.order);

const slugs = new Set();
for (const a of articles) {
  if (slugs.has(a.slug)) throw new Error(`duplicate slug ${a.slug}`);
  slugs.add(a.slug);
}

// ---------- layout ----------
const css = readFileSync(join(root, 'src/style.css'), 'utf8')
  .replace(/FONTS\//g, rel('fonts/'))
  .replace(/\/\*[\s\S]*?\*\//g, '')
  .replace(/\n\s*/g, '')
  .replace(/\s*([{};:,>])\s*/g, '$1');

const logo = `<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="15" fill="#FBF7EF"/><path d="M3 19c4-3 7-3 10 0s7 3 10 0 5-3 6-2v3a15 15 0 0 1-26 2z" fill="#2E86AB"/><circle cx="21" cy="11" r="4" fill="#D9A441"/></svg>`;

const nav = [
  ['', 'Home'],
  ['start-here/', 'Start here'],
  ['articles/', 'Articles'],
  ['guides/', 'Guides'],
  ['about/', 'About'],
];

function layout({ path, title, description, body, type = 'website', jsonld = [], published, modified, hero }) {
  const fullTitle = path === '' ? `${site.name}: practical guides to Greece` : `${title} | ${site.name}`;
  const url = abs(path);
  const ld = jsonld.map((o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`).join('');
  const og = hero
    ? `<meta property="og:image" content="${abs(`img/${hero}-og.jpg`)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${esc(images[hero].alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="${abs(`img/${hero}-og.jpg`)}">
<meta name="twitter:image:alt" content="${esc(images[hero].alt)}">`
    : `<meta name="twitter:card" content="summary">`;
  return `<!doctype html>
<html lang="${site.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${url}">
${hero ? `<link rel="preload" as="image" type="image/webp" imagesrcset="${srcset(hero)}" imagesizes="100vw" fetchpriority="high">\n` : ''}<link rel="preload" href="${rel('fonts/noto-sans-latin-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="${rel('fonts/noto-serif-latin-700-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="${rel('favicon.svg')}" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="${esc(site.name)}" href="${abs('rss.xml')}">
<meta name="theme-color" content="#163A5B">
<meta property="og:site_name" content="${esc(site.name)}">
<meta property="og:locale" content="en_GB">
<meta property="og:type" content="${type}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${url}">
${og}
${published ? `<meta property="article:published_time" content="${published}">\n<meta property="article:modified_time" content="${modified}">\n` : ''}<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(description)}">
<style>${css}</style>
${ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="wrap wide">
<a class="brand" href="${rel()}">${logo}<span>${esc(site.name)}</span></a>
<nav class="nav" aria-label="Main"><ul>${nav
    .map(([p, label]) => `<li><a href="${rel(p)}"${p === path ? ' aria-current="page"' : ''}>${label}</a></li>`)
    .join('')}</ul></nav>
</div>
</header>
<main id="main">
${body}
</main>
<footer class="site-footer">
<div class="wrap wide">
<ul>
<li><a href="${rel('articles/')}">Articles</a></li>
<li><a href="${rel('guides/')}">Guides</a></li>
<li><a href="${rel('about/')}">About</a></li>
<li><a href="${rel('privacy/')}">Privacy</a></li>
<li><a href="${rel('rss.xml')}">RSS feed</a></li>
<li><a href="${site.shopUrl}">Shop on Payhip</a></li>
</ul>
<p>${esc(site.footerNote)}</p>
<p>No cookies, no tracking. Photos: Unsplash.</p>
</div>
</footer>
</body>
</html>
`;
}

const priceLabel = (g) => (g.price === 'see shop' ? 'see shop for price' : g.price);
const priceShort = (g) => (g.price === 'free' ? 'Free' : g.price === 'see shop' ? 'Price: see shop' : g.price);

// A "cover" for a guide: the stand-in photo with the guide's name set on it.
// The guide's cover from covers/ (same artwork as Payhip and the stores).
function cover(key, sizes, lazy = true, shape = 'sq') {
  const g = guides[key];
  const ws = shape === 'sq' ? [480, 800] : [320, 640];
  const [w, h] = shape === 'sq' ? [800, 800] : [640, 1024];
  const set = ws.map((x) => `${rel(`img/cover-${key}-${shape}-${x}.webp`)} ${x}w`).join(', ');
  return `<img class="cover-img cover-${shape}" src="${rel(`img/cover-${key}-${shape}-${ws[0]}.webp`)}" srcset="${set}" sizes="${sizes}" width="${w}" height="${h}" alt="Cover of the guide ${esc(g.name)}" ${lazy ? 'loading="lazy" ' : ''}decoding="async">`;
}

function productCard(key) {
  const g = guides[key];
  return `<aside class="product" aria-labelledby="product-h">
${cover(key, '(min-width: 640px) 200px, 220px', true, 'pt')}
<div class="product-body">
<p class="kicker">Want the full checklist?</p>
<h2 id="product-h">${esc(g.name)}</h2>
<p class="product-meta">${icon('doc')}<span>${g.format}, ${priceLabel(g)}</span></p>
<p><a class="button" href="${g.url}">→ ${esc(g.name)} (${g.format}, ${priceLabel(g)})</a></p>
<p class="small">Sold through Payhip. The shop page shows what is inside before you decide.</p>
</div>
</aside>`;
}

function articleCard(a, h = 'h3', lazy = true) {
  return `<li><article class="card">${img(a.hero, { sizes: '(min-width: 1040px) 320px, (min-width: 700px) 45vw, 100vw', lazy })}<div class="card-body"><p class="kicker">${esc(a.kicker)}</p><${h}><a class="stretched" href="${rel(`articles/${a.slug}/`)}">${esc(a.title)}</a></${h}><p>${esc(a.summary)}</p></div></article></li>`;
}

function guideCard(key, i = 9) {
  const g = guides[key];
  const related = articles.filter((a) => a.guide === key);
  return `<li><article class="card guide">${cover(key, '(min-width: 1040px) 320px, (min-width: 700px) 45vw, 100vw', i > 1)}<div class="card-body"><h3><a href="${g.url}">${esc(g.name)}</a></h3>${
    related.length ? `<p>Free reading first: ${related.map((a) => `<a href="${rel(`articles/${a.slug}/`)}">${esc(a.title)}</a>`).join('; ')}</p>` : ''
  }<p class="price">${priceShort(g)}</p></div></article></li>`;
}

const publisher = { '@type': 'Organization', name: site.name, url: abs() };

// ---------- pages ----------
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
cpSync(join(root, 'src/static'), out, { recursive: true, filter: (src) => !src.includes(join('src', 'static', 'img')) });

// Article pages
for (const a of articles) {
  const path = `articles/${a.slug}/`;
  const others = articles
    .filter((o) => o !== a && o.guide === a.guide)
    .concat(articles.filter((o) => o !== a && o.guide !== a.guide))
    .slice(0, 3);
  const body = `<article>
<header class="hero hero-article">
${img(a.hero, { eager: true })}
<div class="hero-text wrap">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="${rel()}">Home</a></li><li><a href="${rel('articles/')}">Articles</a></li></ol></nav>
<p class="kicker">${esc(a.kicker)}</p>
<h1>${esc(a.title)}</h1>
<p class="meta">${icon('calendar')}<span>Last checked: ${esc(a.lastChecked)}</span><span aria-hidden="true">·</span><span>About ${Math.max(1, Math.round(a.words / 220))} minutes to read</span></p>
</div>
</header>
<div class="wrap article-body">
${a.html}
${productCard(a.guide)}
<p class="note">General information, not legal, tax or medical advice. Rules change: check with the official source or a qualified professional before you act.</p>
</div>
</article>
<section class="wrap wide more" aria-labelledby="more-h">
<p class="kicker">Keep reading</p>
<h2 id="more-h">More free articles</h2>
<ul class="cards">${others.map((o) => articleCard(o)).join('')}</ul>
</section>`;
  write(
    path + 'index.html',
    layout({
      path,
      title: a.title,
      description: a.description,
      body,
      type: 'article',
      published: a.published,
      modified: a.modified,
      hero: a.hero,
      jsonld: [
        {
          '@context': 'https://schema.org',
          '@type': 'Article',
          headline: a.title,
          description: a.description,
          image: abs(`img/${a.hero}-og.jpg`),
          datePublished: a.published,
          dateModified: a.modified,
          inLanguage: site.lang,
          mainEntityOfPage: abs(path),
          url: abs(path),
          author: publisher,
          publisher,
        },
        {
          '@context': 'https://schema.org',
          '@type': 'BreadcrumbList',
          itemListElement: [
            { '@type': 'ListItem', position: 1, name: 'Home', item: abs() },
            { '@type': 'ListItem', position: 2, name: 'Articles', item: abs('articles/') },
            { '@type': 'ListItem', position: 3, name: a.title, item: abs(path) },
          ],
        },
      ],
    })
  );
}

// Home
const homeHero = 'santorini-wide';
const featured = articles.filter((a) => a.featured === 'true');
checkImage(homeHero, 'home');
write(
  'index.html',
  layout({
    path: '',
    title: `${site.name}: practical guides to Greece`,
    description: site.description,
    hero: homeHero,
    jsonld: [{ '@context': 'https://schema.org', '@type': 'WebSite', name: site.name, url: abs(), inLanguage: site.lang }],
    body: `<header class="hero hero-home">
${img(homeHero, { eager: true })}
<div class="hero-text wrap wide">
<p class="kicker">Practical guides to Greece</p>
<h1>Greece, without the sales talk</h1>
<p class="hero-intro">Plain-English answers for people visiting or moving to Greece: residence permits, the 7% pension tax, which island to pick, what to order in a taverna and enough Greek to get by.</p>
<p class="hero-actions"><a class="button" href="${rel('start-here/')}">Start here</a><a class="button button-ghost" href="${rel('articles/')}">Read the free articles</a></p>
</div>
</header>
<div class="wrap wide">
<ul class="trust">
<li>${icon('calendar')}<span><strong>Dated.</strong> Every article shows when it was last checked.</span></li>
<li>${icon('shield')}<span><strong>Checked in Greece.</strong> Written with AI tools, checked by people who live here.</span></li>
<li>${icon('check')}<span><strong>No tracking.</strong> No cookies, no ads, nothing to sign up for.</span></li>
</ul>
${featured
  .map(
    (a) => `<section class="feature" aria-labelledby="feat-${a.slug}">
${img('lefkada-bay', { sizes: '(min-width: 1040px) 1000px, 100vw' })}
<div class="feature-text">
<p class="kicker">Featured guide</p>
<h2 id="feat-${a.slug}"><a class="stretched" href="${rel(`articles/${a.slug}/`)}">${esc(a.title)}</a></h2>
<p>${esc(a.summary)}</p>
</div>
</section>`
  )
  .join('')}
<p class="kicker section-kicker">Free to read</p>
<h2>Articles</h2>
<ul class="cards">${articles.filter((a) => !featured.includes(a)).map((a) => articleCard(a)).join('')}</ul>
<p class="kicker section-kicker">Downloadable PDFs</p>
<h2>The guides</h2>
<p>Sold through Payhip. Each article above links to the guide that goes with it. You never need to buy anything to use this site. <a href="${rel('guides/')}">See all guides</a>.</p>
<ul class="cards">${['retire', 'nomad', 'first90', 'renting', 'islands', 'eat', 'phrases', 'alphabet'].map((k) => guideCard(k)).join('')}</ul>
</div>`,
  })
);

// Article index
write(
  'articles/index.html',
  layout({
    path: 'articles/',
    title: 'All articles',
    description: 'Free articles about living in and visiting Greece: visas, tax, healthcare, islands, food and the Greek language.',
    body: `<div class="wrap wide page">
<p class="kicker">Free to read</p>
<h1>All articles</h1>
<p class="intro">Practical articles, each one dated with the month it was last checked.</p>
<ul class="cards">${articles.map((a, i) => articleCard(a, 'h2', i > 1)).join('')}</ul>
</div>`,
  })
);

// Guides
write(
  'guides/index.html',
  layout({
    path: 'guides/',
    title: 'Guides',
    description: 'Downloadable guides from Greece, Honestly: retiring, digital nomad life, islands, food, Survival Greek and a free alphabet cheat sheet.',
    body: `<div class="wrap wide page">
<p class="kicker">Downloadable PDFs</p>
<h1>Guides</h1>
<p class="intro">Our downloadable guides are sold through Payhip, a third-party shop. Each link opens the guide's shop page, where you can read the description before buying.</p>
${guideGroups.map((grp) => `<h2>${esc(grp.title)}</h2>\n<ul class="cards">${grp.keys.map((k, i) => guideCard(k, grp === guideGroups[0] ? i : 9)).join('')}</ul>`).join('\n')}
<p><a class="button" href="${site.shopUrl}">Browse the full shop</a></p>
<p class="note">Prices shown here may change; the price on the shop page is the one that applies. Cover images on this site are photos standing in for the guide covers.</p>
</div>`,
  })
);

// Start here: route visitors by situation
const bySlug = Object.fromEntries(articles.map((a) => [a.slug, a]));
const routes = [
  {
    id: 'visiting', icon: 'sun', title: 'I am visiting Greece',
    intro: 'Choosing an island, getting around by ferry, eating out and a few words of Greek.',
    slugs: ['which-greek-island-is-right-for-you', 'greek-island-hopping-three-routes', 'greek-ferries-how-to-book', 'greek-taverna-etiquette', 'how-to-order-coffee-in-greece', 'greek-phrases-for-your-first-week'],
    guides: ['islands', 'eat', 'phrases'],
  },
  {
    id: 'moving', icon: 'home', title: 'I am moving to Greece',
    intro: 'The paperwork in the right order: tax number, a flat, a bank account and your social security number.',
    slugs: ['first-90-days-in-greece', 'getting-an-afm-greek-tax-number', 'renting-a-flat-in-greece', 'opening-a-greek-bank-account', 'amka-explained', 'where-to-live-in-athens'],
    guides: ['first90', 'renting'],
  },
  {
    id: 'retiring', icon: 'leaf', title: 'I am retiring to Greece',
    intro: 'Residence permits, the 7% flat tax on foreign pensions, and healthcare with an S1 or full health insurance.',
    slugs: ['retiring-to-greece-2026', 'greece-7-percent-flat-tax-foreign-pensions', 'first-90-days-in-greece', 'amka-explained'],
    guides: ['retire', 'first90'],
  },
  {
    id: 'remote', icon: 'phone', title: 'I want to work remotely from Greece',
    intro: 'The digital nomad visa, the income rule, tax residence and setting up your first months.',
    slugs: ['greece-digital-nomad-visa-2026', 'first-90-days-in-greece', 'getting-an-afm-greek-tax-number', 'where-to-live-in-athens'],
    guides: ['nomad', 'first90'],
  },
];
for (const r of routes) for (const s of r.slugs) if (!bySlug[s]) throw new Error(`start-here: unknown article ${s}`);
write(
  'start-here/index.html',
  layout({
    path: 'start-here/',
    title: 'Start here',
    description: 'Not sure where to begin? Pick your situation — visiting, moving, retiring or working remotely — and see the articles and guides that fit.',
    body: `<div class="wrap wide page">
<p class="kicker">Start here</p>
<h1>Where are you in your Greece plans?</h1>
<p class="intro">Pick the line that fits you best. Each one lists the free articles to read first, in a sensible order, and the guide that goes deeper.</p>
<ul class="route-picker">${routes.map((r) => `<li><a href="#${r.id}">${icon(r.icon)}<span>${esc(r.title)}</span></a></li>`).join('')}</ul>
${routes
  .map(
    (r) => `<section class="route" id="${r.id}" aria-labelledby="${r.id}-h">
<p class="kicker">${icon(r.icon)} Your route</p>
<h2 id="${r.id}-h">${esc(r.title)}</h2>
<p>${esc(r.intro)}</p>
<ul class="cards">${r.slugs.map((s, i) => articleCard(bySlug[s], 'h3', i > 2 || r !== routes[0])).join('')}</ul>
<h3 class="route-guides">The guides for this route</h3>
<ul class="cards">${r.guides.map((k) => guideCard(k)).join('')}</ul>
</section>`
  )
  .join('\n')}
<p class="note">General information, not legal, tax or medical advice. Every article shows when it was last checked and lists its sources.</p>
</div>`,
  })
);

// About
write(
  'about/index.html',
  layout({
    path: 'about/',
    title: 'About',
    description: 'What Greece, Honestly is, how the guides are made, and what it is not.',
    body: `<div class="wrap page">
<p class="kicker">About</p>
<h1>About Greece, Honestly</h1>
<p class="intro">Greece, Honestly publishes practical English-language guides for people visiting or moving to Greece.</p>
<h2>How it works</h2>
<ul>
<li>The articles on this site are free. Some end with a link to a paid guide that goes into more detail.</li>
<li>The paid guides are PDFs sold through Payhip.</li>
<li>Greece, Honestly is presented by AI-generated characters. They are not real people, and we do not pretend otherwise.</li>
<li>Guides are written with AI tools and checked in Greece.</li>
<li>Photos come from Unsplash. They illustrate the articles and are not always of the exact place described.</li>
</ul>
<h2>What we are not</h2>
<p>We are not lawyers, accountants or doctors. Everything here is general information, not legal, tax or medical advice. Rules in Greece change, sometimes quickly. Before you make a big decision, check with the official source, the Greek consulate, or a qualified professional.</p>
<h2>What you will not find here</h2>
<p>No invented author biographies, no reviews or testimonials, no countdown timers and no tracking. Each article shows when it was last checked.</p>
<h2>Spotted a mistake?</h2>
<p>${site.contactEmail ? `Please email <a href="mailto:${esc(site.contactEmail)}">${esc(site.contactEmail)}</a>.` : 'A contact email address will be added here soon.'}</p>
</div>`,
  })
);

// Privacy
write(
  'privacy/index.html',
  layout({
    path: 'privacy/',
    title: 'Privacy',
    description: 'Greece, Honestly uses no cookies and no tracking.',
    body: `<div class="wrap page">
<p class="kicker">Privacy</p>
<h1>Privacy</h1>
<p class="intro">Short version: this site uses no cookies and no tracking.</p>
<h2>On this website</h2>
<ul>
<li>No cookies.</li>
<li>No analytics, no advertising and no third-party scripts.</li>
<li>No forms, no accounts and nothing that asks for your details.</li>
<li>Fonts and photos are served from this site, not from outside services.</li>
</ul>
<h2>Hosting</h2>
<p>The site is hosted on GitHub Pages. Like any web host, GitHub may process technical data such as your IP address to deliver pages and keep the service secure. See GitHub's own privacy statement for details.</p>
<h2>Buying a guide</h2>
<p>Guides are sold through Payhip. When you follow a link to the shop you leave this site, and Payhip's own privacy policy applies to anything you do there, including payment.</p>
<h2>Contact</h2>
<p>${site.contactEmail ? `Email <a href="mailto:${esc(site.contactEmail)}">${esc(site.contactEmail)}</a>. We only use your email to reply to you.` : 'Contact is by email only. An address will be added here soon.'}</p>
<p class="meta-plain">Last updated: ${esc(site.lastChecked)}</p>
</div>`,
  })
);

// 404
write(
  '404.html',
  layout({
    path: '404.html',
    title: 'Page not found',
    description: 'This page does not exist.',
    body: `<div class="wrap page"><h1>Page not found</h1><p>Sorry, that page does not exist. Try the <a href="${rel()}">home page</a> or the <a href="${rel('articles/')}">list of articles</a>.</p></div>`,
  }).replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
);

// Favicon
write('favicon.svg', logo.replace('aria-hidden="true" focusable="false"', 'xmlns="http://www.w3.org/2000/svg"'));

// sitemap.xml
const pages = [
  ['', articles[0].modified],
  ['start-here/', articles[0].modified],
  ['articles/', articles[0].modified],
  ...articles.map((a) => [`articles/${a.slug}/`, a.modified]),
  ['guides/', articles[0].modified],
  ['about/', articles[0].modified],
  ['privacy/', articles[0].modified],
];
write(
  'sitemap.xml',
  `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages.map(([p, d]) => `<url><loc>${abs(p)}</loc><lastmod>${d}</lastmod></url>`).join('\n')}
</urlset>
`
);

// robots.txt (only meaningful at a domain root; harmless under a sub-path)
write('robots.txt', `User-agent: *\nAllow: /\n\nSitemap: ${abs('sitemap.xml')}\n`);

// Plain-text copies for AI assistants and other readers: /llms.txt and articles/<slug>/index.md
const mdCopy = (a) => `# ${a.title}

${a.description}

- URL: ${abs(`articles/${a.slug}/`)}
- Published: ${a.published}. Last checked: ${a.lastChecked}.
- ${site.name} is written with AI tools and checked in Greece. General information, not legal, tax or medical advice.

${a.source.trim().replace(/\]\(\//g, `](${abs()}`)}
`;
for (const a of articles) write(`articles/${a.slug}/index.md`, mdCopy(a));
write(
  'llms.txt',
  `# ${site.name}

> ${site.description}

Practical, dated articles in British English for people visiting or moving to Greece. Every article lists its sources and the month it was last checked. Written with AI tools and checked in Greece; general information, not legal, tax or medical advice. Each article has a plain Markdown copy at the same address plus index.md.

## Articles

${articles.map((a) => `- [${a.title}](${abs(`articles/${a.slug}/`)}): ${a.summary} Last checked ${a.lastChecked}. Markdown: ${abs(`articles/${a.slug}/index.md`)}`).join('\n')}

## Optional

- [Start here](${abs('start-here/')}): which articles to read first, by situation
- [Guides](${abs('guides/')}): paid downloadable PDF guides
- [About](${abs('about/')}): who is behind the site and how it is checked
- [RSS feed](${abs('rss.xml')})
`
);

// RSS
const rfc822 = (d) => new Date(d + 'T09:00:00Z').toUTCString();
write(
  'rss.xml',
  `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>${esc(site.name)}</title>
<link>${abs()}</link>
<description>${esc(site.description)}</description>
<language>en-gb</language>
<atom:link href="${abs('rss.xml')}" rel="self" type="application/rss+xml"/>
${[...articles]
  .sort((a, b) => b.published.localeCompare(a.published) || a.order - b.order)
  .map(
    (a) => `<item><title>${esc(a.title)}</title><link>${abs(`articles/${a.slug}/`)}</link><guid>${abs(`articles/${a.slug}/`)}</guid><pubDate>${rfc822(a.published)}</pubDate><description>${esc(a.description)}</description></item>`
  )
  .join('\n')}
</channel>
</rss>
`
);

// GitHub Pages: don't run Jekyll. Optional custom domain.
write('.nojekyll', '');
if (process.env.CNAME) write('CNAME', process.env.CNAME.trim() + '\n');

await renderImages();

console.log(`Built ${articles.length} articles and ${used.size} photos → dist/ (base ${site.url}${B})`);
for (const a of articles) console.log(`  ${String(a.words).padStart(5)} words  ${a.file}`);
