// Minimal local preview server: serves dist/ under the configured base path.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { site } from '../src/site.mjs';

const dist = join(dirname(fileURLToPath(import.meta.url)), '..', 'dist');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8', '.md': 'text/markdown; charset=utf-8', '.svg': 'image/svg+xml', '.woff2': 'font/woff2' };
const port = Number(process.env.PORT || 4321);

createServer(async (req, res) => {
  let p = decodeURI(new URL(req.url, 'http://x').pathname);
  if (!p.startsWith(site.basePath)) { res.writeHead(302, { location: site.basePath }); return res.end(); }
  let file = join(dist, p.slice(site.basePath.length));
  try { if ((await stat(file)).isDirectory()) file = join(file, 'index.html'); } catch {}
  try {
    const body = await readFile(file);
    res.writeHead(200, { 'content-type': types[extname(file)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404, { 'content-type': types['.html'] });
    res.end(await readFile(join(dist, '404.html')));
  }
}).listen(port, () => console.log(`Preview: http://localhost:${port}${site.basePath}`));
