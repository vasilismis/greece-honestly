// Tiny static site builder for Greece, Honestly.
// Reads Markdown articles from src/articles, writes a complete static site to dist/.
import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync, cpSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { marked } from 'marked';
import { site, guides, guideGroups } from '../src/site.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'dist');
const B = site.basePath; // e.g. "/greece-honestly/"
const abs = (p = '') => site.url + B + p; // absolute URL for canonical, sitemap, RSS
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

// Markdown rendering: tables get a focusable scroll wrapper so they work at 360px.
// Links starting with "/" are treated as site-internal and get the base path.
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

// ---------- load articles ----------
const required = ['title', 'description', 'slug', 'guide', 'published', 'order', 'summary'];
const articles = readdirSync(join(root, 'src/articles'))
  .filter((f) => f.endsWith('.md'))
  .map((f) => {
    const { data, body } = parseFrontMatter(readFileSync(join(root, 'src/articles', f), 'utf8'), f);
    for (const k of required) if (!data[k]) throw new Error(`${f}: front matter needs "${k}"`);
    if (!guides[data.guide]) throw new Error(`${f}: unknown guide "${data.guide}" (see src/site.mjs)`);
    const words = body.replace(/[#|*_>`\-]/g, ' ').split(/\s+/).filter(Boolean).length;
    return {
      ...data,
      order: Number(data.order),
      modified: data.modified || data.published,
      lastChecked: data.lastChecked || site.lastChecked,
      html: marked.parse(body),
      words,
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
  .replace(/\n\s*/g, '')
  .replace(/\s*([{};:,])\s*/g, '$1');

const logo = `<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><circle cx="16" cy="16" r="15" fill="#FBF7EF"/><path d="M3 19c4-3 7-3 10 0s7 3 10 0 5-3 6-2v3a15 15 0 0 1-26 2z" fill="#2E86AB"/><circle cx="21" cy="11" r="4" fill="#D9A441"/></svg>`;

const nav = [
  ['', 'Home'],
  ['articles/', 'Articles'],
  ['guides/', 'Guides'],
  ['about/', 'About'],
];

function layout({ path, title, description, body, type = 'website', jsonld = [], published, modified }) {
  const fullTitle = path === '' ? `${site.name}: practical guides to Greece` : `${title} | ${site.name}`;
  const url = abs(path);
  const ld = jsonld.map((o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`).join('');
  return `<!doctype html>
<html lang="${site.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(fullTitle)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${url}">
<link rel="preload" href="${rel('fonts/noto-sans-latin-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="${rel('fonts/noto-serif-latin-700-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="${rel('favicon.svg')}" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="${esc(site.name)}" href="${abs('rss.xml')}">
<meta name="theme-color" content="#1F4E79">
<meta property="og:site_name" content="${esc(site.name)}">
<meta property="og:locale" content="en_GB">
<meta property="og:type" content="${type}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${url}">
${published ? `<meta property="article:published_time" content="${published}">\n<meta property="article:modified_time" content="${modified}">\n` : ''}<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="${esc(title)}">
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
<p>No cookies, no tracking.</p>
</div>
</footer>
</body>
</html>
`;
}

const priceLabel = (g) => (g.price === 'see shop' ? 'see shop for price' : g.price);

function cta(a) {
  const g = guides[a.guide];
  return `<aside class="cta" aria-labelledby="cta-h">
<h2 id="cta-h">Want the full checklist?</h2>
<p><a class="button" href="${g.url}">→ ${esc(g.name)} (${g.format}, ${priceLabel(g)})</a></p>
<p class="note" style="border:0;padding:0;margin:0">Sold through Payhip. Opens the shop page, where you can see what is inside before you decide.</p>
</aside>`;
}

function articleCard(a) {
  return `<li><article class="card"><h3><a href="${rel(`articles/${a.slug}/`)}">${esc(a.title)}</a></h3><p>${esc(a.summary)}</p></article></li>`;
}

function guideCard(key) {
  const g = guides[key];
  const related = articles.filter((a) => a.guide === key);
  return `<li><article class="card guide"><h3><a href="${g.url}">${esc(g.name)}</a></h3>${
    related.length
      ? `<p>Free reading first: ${related.map((a) => `<a href="${rel(`articles/${a.slug}/`)}">${esc(a.title)}</a>`).join('; ')}</p>`
      : ''
  }<p class="price">${g.price === 'free' ? 'Free' : g.price === 'see shop' ? 'Price: see shop' : g.price}</p></article></li>`;
}

const publisher = { '@type': 'Organization', name: site.name, url: abs() };

// ---------- pages ----------
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
cpSync(join(root, 'src/static'), out, { recursive: true });

// Article pages
for (const a of articles) {
  const path = `articles/${a.slug}/`;
  const others = articles.filter((o) => o !== a && o.guide === a.guide).concat(articles.filter((o) => o !== a && o.guide !== a.guide)).slice(0, 3);
  const body = `<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="${rel()}">Home</a></li><li><a href="${rel('articles/')}">Articles</a></li></ol></nav>
<article>
<h1>${esc(a.title)}</h1>
<p class="meta">Last checked: ${esc(a.lastChecked)} · About ${Math.max(1, Math.round(a.words / 220))} minutes to read</p>
${a.html}
${cta(a)}
<p class="note">General information, not legal, tax or medical advice. Rules change: check with the official source or a qualified professional before you act.</p>
</article>
<section aria-labelledby="more-h">
<h2 id="more-h">More free articles</h2>
<ul class="cards">${others.map(articleCard).join('')}</ul>
</section>
</div>`;
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
      jsonld: [
        {
          '@context': 'https://schema.org',
          '@type': 'Article',
          headline: a.title,
          description: a.description,
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
write(
  'index.html',
  layout({
    path: '',
    title: `${site.name}: practical guides to Greece`,
    description: site.description,
    jsonld: [{ '@context': 'https://schema.org', '@type': 'WebSite', name: site.name, url: abs(), inLanguage: site.lang }],
    body: `<div class="wrap wide">
<h1>Greece, without the sales talk</h1>
<p class="intro">Plain-English answers for people visiting or moving to Greece: residence permits, the 7% pension tax, healthcare, which island to pick, what to order in a taverna and enough Greek to get by.</p>
<p>The articles below are free. Where a topic needs a full checklist, each article links to a paid PDF guide at the end. You never need to buy anything to use this site.</p>
<h2>Free articles</h2>
<ul class="cards">${articles.map(articleCard).join('')}</ul>
<h2>The guides</h2>
<p>Downloadable guides sold through Payhip. <a href="${rel('guides/')}">See all guides</a> or <a href="${site.shopUrl}">visit the shop</a>.</p>
<ul class="cards">${['retire', 'nomad', 'islands', 'eat', 'phrases', 'alphabet'].map(guideCard).join('')}</ul>
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
    body: `<div class="wrap wide">
<h1>All articles</h1>
<p class="intro">Free, practical articles. Each one was last checked in ${esc(site.lastChecked)}.</p>
<ul class="cards">${articles.map(articleCard).join('')}</ul>
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
    body: `<div class="wrap wide">
<h1>Guides</h1>
<p class="intro">Our downloadable guides are sold through Payhip, a third-party shop. Each link opens the guide's shop page, where you can read the description before buying.</p>
${guideGroups.map((grp) => `<h2>${esc(grp.title)}</h2>\n<ul class="cards">${grp.keys.map(guideCard).join('')}</ul>`).join('\n')}
<p><a class="button" href="${site.shopUrl}">Browse the full shop</a></p>
<p class="note">Prices shown here may change; the price on the shop page is the one that applies.</p>
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
    body: `<div class="wrap">
<h1>About Greece, Honestly</h1>
<p class="intro">Greece, Honestly publishes practical English-language guides for people visiting or moving to Greece.</p>
<h2>How it works</h2>
<ul>
<li>The articles on this site are free. Some end with a link to a paid guide that goes into more detail.</li>
<li>The paid guides are PDFs sold through Payhip.</li>
<li>Greece, Honestly is presented by AI-generated characters. They are not real people, and we do not pretend otherwise.</li>
<li>Guides are written with AI tools and checked in Greece.</li>
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
    body: `<div class="wrap">
<h1>Privacy</h1>
<p class="intro">Short version: this site uses no cookies and no tracking.</p>
<h2>On this website</h2>
<ul>
<li>No cookies.</li>
<li>No analytics, no advertising and no third-party scripts.</li>
<li>No forms, no accounts and nothing that asks for your details.</li>
<li>Fonts are served from this site, not from a font service.</li>
</ul>
<h2>Hosting</h2>
<p>The site is hosted on GitHub Pages. Like any web host, GitHub may process technical data such as your IP address to deliver pages and keep the service secure. See GitHub's own privacy statement for details.</p>
<h2>Buying a guide</h2>
<p>Guides are sold through Payhip. When you follow a link to the shop you leave this site, and Payhip's own privacy policy applies to anything you do there, including payment.</p>
<h2>Contact</h2>
<p>${site.contactEmail ? `Email <a href="mailto:${esc(site.contactEmail)}">${esc(site.contactEmail)}</a>. We only use your email to reply to you.` : 'Contact is by email only. An address will be added here soon.'}</p>
<p class="meta">Last updated: ${esc(site.lastChecked)}</p>
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
    body: `<div class="wrap"><h1>Page not found</h1><p>Sorry, that page does not exist. Try the <a href="${rel()}">home page</a> or the <a href="${rel('articles/')}">list of articles</a>.</p></div>`,
  }).replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
);

// Favicon
write('favicon.svg', logo.replace('aria-hidden="true" focusable="false"', 'xmlns="http://www.w3.org/2000/svg"'));

// sitemap.xml
const pages = [
  ['', articles[0].modified],
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

console.log(`Built ${articles.length} articles → dist/ (base ${site.url}${B})`);
for (const a of articles) console.log(`  ${String(a.words).padStart(5)} words  ${a.file}`);
