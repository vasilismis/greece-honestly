// Checks every internal link and asset in dist/. With --external, also requests each external URL.
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { site } from '../src/site.mjs';

const dist = join(dirname(fileURLToPath(import.meta.url)), '..', 'dist');
const B = site.basePath;
const files = [];
(function walk(d) {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p);
    else if (f.endsWith('.html')) files.push(p);
  }
})(dist);

const external = new Map();
let broken = 0;
let checked = 0;
const ids = (html) => new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));

for (const file of files) {
  const html = readFileSync(file, 'utf8');
  const page = '/' + file.slice(dist.length + 1).replace(/\\/g, '/');
  for (const [, raw] of html.matchAll(/\s(?:href|src)="([^"]+)"/g)) {
    const url = raw.replace(/&amp;/g, '&');
    checked++;
    if (/^https?:\/\//.test(url)) {
      if (url.startsWith(site.url + B)) {
        // absolute link to our own site (canonical, og:url, RSS): check it locally
        resolve(url.slice(site.url.length), page);
      } else {
        if (!external.has(url)) external.set(url, new Set());
        external.get(url).add(page);
      }
      continue;
    }
    if (/^(mailto:|tel:)/.test(url)) continue;
    if (url.startsWith('#')) {
      if (url.length > 1 && !ids(html).has(url.slice(1))) report(page, url, 'missing anchor');
      continue;
    }
    if (!url.startsWith('/')) { report(page, url, 'relative link (use a root path)'); continue; }
    resolve(url, page);
  }
}

function resolve(url, page) {
  const [path, hash] = url.split('#');
  if (!path.startsWith(B)) return report(page, url, `outside base path ${B}`);
  let target = join(dist, decodeURI(path.slice(B.length)));
  if (path.endsWith('/')) target = join(target, 'index.html');
  if (!existsSync(target)) return report(page, url, 'file not found');
  if (hash && target.endsWith('.html') && !ids(readFileSync(target, 'utf8')).has(hash)) report(page, url, 'missing anchor');
}

function report(page, url, why) {
  broken++;
  console.error(`BROKEN  ${page}  →  ${url}  (${why})`);
}

if (process.argv.includes('--external')) {
  for (const [url, pages] of external) {
    try {
      const res = await fetch(url, { method: 'GET', redirect: 'follow', signal: AbortSignal.timeout(20000) });
      if (res.status >= 400) report([...pages][0], url, `HTTP ${res.status}`);
      else console.log(`ok ${res.status}  ${url}`);
    } catch (e) {
      report([...pages][0], url, `request failed: ${e.cause?.code || e.message}`);
    }
  }
}

console.log(`${files.length} pages, ${checked} links checked, ${external.size} distinct external URLs${process.argv.includes('--external') ? ' (requested)' : ' (not requested; use --external)'}.`);
if (broken) {
  console.error(`${broken} broken link(s).`);
  process.exit(1);
}
console.log('No broken links.');
