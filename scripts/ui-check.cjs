const { chromium } = require('playwright');
const fs = require('fs');
// Visual and UI check: every page, phone and desktop, light and dark device settings.
// Flags sideways scroll, broken images, missing alt text, small tap targets, low text contrast and h1 count.
// Usage: npm run build && npm run ui   (needs Playwright with Chromium; screenshots go to SHOTS dir if set)
const { spawn } = require('child_process');
const path = require('path');
const S = process.env.SHOTS || '';
const PORT = process.env.PORT || '4399';
(async () => {
  const server = spawn(process.execPath, [path.join(__dirname, 'serve.mjs')], { env: { ...process.env, PORT }, stdio: ['ignore', 'pipe', 'inherit'] });
  await new Promise((r) => server.stdout.once('data', r));
  const BASE = 'http://localhost:' + PORT + (process.env.BASE_PATH || require('fs').readFileSync(path.join(__dirname, '..', 'src', 'site.mjs'), 'utf8').match(/basePath:[^'"]*['"]([^'"]*)/)[1]).replace(/\/$/, '');
  const b = await chromium.launch();
  const pages = fs.readdirSync('dist/articles').filter(a=>!a.includes('.')).map(a => '/articles/' + a + '/');
  const all = ['/', '/guides/', '/start-here/', '/articles/', ...pages].filter((v,i,a)=>a.indexOf(v)===i);
  const out = [];
  for (const [vw, vh, tag] of [[375, 812, 'mobile'], [1366, 900, 'desktop']]) {
    for (const scheme of ['light', 'dark']) {
      const ctx = await b.newContext({ viewport: { width: vw, height: vh }, colorScheme: scheme });
      const p = await ctx.newPage();
      for (const u of all) {
        const r = await p.goto(BASE + u, { waitUntil: 'load' }).catch(e => null);
        if (!r || r.status() !== 200) { if (tag==='mobile'&&scheme==='light') out.push(`${u} status ${r && r.status()}`); continue; }
        const res = await p.evaluate(() => {
          const issues = [];
          const W = document.documentElement.clientWidth;
          if (document.documentElement.scrollWidth > W + 1) {
            const wide = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > W + 1 && getComputedStyle(e).position !== 'fixed').slice(0, 3).map(e => e.tagName + '.' + e.className);
            issues.push('horizontal scroll ' + document.documentElement.scrollWidth + ' > ' + W + ' ' + wide.join(','));
          }
          document.querySelectorAll('img').forEach(i => { if (!i.hasAttribute('alt')) issues.push('img no alt ' + i.src); if (i.complete && i.naturalWidth === 0) issues.push('broken img ' + i.src); });
          const small = [...document.querySelectorAll('a, button')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0 && r.height < 24 && !e.closest('p, li, td, figcaption'); }).map(e => (e.textContent || '').trim().slice(0, 25));
          if (small.length) issues.push('small tap targets: ' + small.slice(0, 4).join(' | '));
          // contrast check on text
          function lum(c){const m=c.match(/[\d.]+/g);if(!m)return null;const [r,g,bb]=m.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return [.2126*r+.7152*g+.0722*bb, m[3]!==undefined?+m[3]:1]}
          function bg(e){while(e){const s=getComputedStyle(e);if(s.backgroundImage!=='none')return null;const c=s.backgroundColor;const l=lum(c);if(l&&l[1]>0.9)return l[0];e=e.parentElement}return lum(getComputedStyle(document.body).backgroundColor)[0]}
          const bad=new Set();
          document.querySelectorAll('p, li, a, h1, h2, h3, td, th, span, figcaption, small, label').forEach(e=>{ if(!e.childNodes.length||![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return; const s=getComputedStyle(e); if(s.visibility==='hidden'||s.display==='none')return; const f=lum(s.color); const b2=bg(e); if(!f||b2==null)return; const cr=(Math.max(f[0],b2)+.05)/(Math.min(f[0],b2)+.05); const big=parseFloat(s.fontSize)>=24||(parseFloat(s.fontSize)>=18.6&&+s.fontWeight>=700); if(cr<(big?3:4.5)) bad.add(e.tagName+' "'+e.textContent.trim().slice(0,30)+'" '+cr.toFixed(2)); });
          if (bad.size) issues.push('low contrast: ' + [...bad].slice(0,4).join(' | '));
          const h1 = document.querySelectorAll('h1').length; if (h1 !== 1) issues.push('h1 count ' + h1);
          return issues;
        });
        res.forEach(i => out.push(`[${tag}/${scheme}] ${u}: ${i}`));
      }
      if (S && (scheme==='light' || tag==='mobile')) for (const u of ['/', '/articles/renting-a-flat-in-greece/', '/guides/']) { await p.goto(BASE + u); await p.screenshot({ path: `${S}/${tag}-${scheme}-${u.replace(/\W+/g,'_')}.png`, fullPage: false }); }
      await ctx.close();
    }
  }
  console.log(all.length + ' pages x 4 modes'); console.log(out.join('\n') || 'no issues');
  await b.close();
  server.kill();
  process.exit(out.length ? 1 : 0);
})();
