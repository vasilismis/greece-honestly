# Greece, Honestly: notes for Claude

A static English-language site (GitHub Pages) of practical, dated articles about visiting and moving to Greece, linking to paid guides sold on Payhip. Live at https://vasilismis.github.io/greece-honestly/. Read `docs/saturday-handoff.md` for the current state of everything outside the site.

## Content rules (non-negotiable)

- **Facts only from a source.** Every number, date, fee or rule needs a source in the article's `## Sources` section, or "Greece, Honestly fact sheet, checked in Greece". Never invent a fact. If something cannot be confirmed, say so in the text ("no decision had been announced in …") rather than guessing.
- **British English, sentence case** for titles and headings. Plain, short sentences.
- **AI disclosure:** the site, guides and covers say they are written with AI tools and checked in Greece. Cover footer text is fixed: `Written with AI tools, checked in Greece`.
- **No** fake reviews or testimonials, invented author biographies, countdowns, false urgency, tracking or cookies.
- **Photos:** a photo whose file name names a place (santorini, lefkada, corfu, crete, athens…) may only appear next to content about that place.
- **Look:** the site is dark blue for every visitor (the founder's choice). Do not reintroduce a light theme. Colours are tokens at the top of `src/style.css` plus the "dark blue theme" block; change them there.

## Commands

```bash
npm run build          # dist/ from src/ (articles in src/articles/*.md, site settings in src/site.mjs)
npm run check          # internal link check over dist/
node scripts/check-links.mjs --external   # also checks outside links (needs open network; CI runs it)
npm run ui             # visual/UI check: all pages, phone + desktop, light + dark device settings
npm test               # build + links + UI
npm run serve          # preview at http://localhost:4321/greece-honestly/
```

Other generators (Python 3 + Pillow; outputs are committed unless noted):

- `python3 scripts/covers.py` → `covers/` (guide covers, 1600×2560 and 1000×1000)
- `python3 guides/build.py <slug>` → paid guide PDFs and EPUB in `guides/<slug>/out/` (gitignored; `content.md` is private and gitignored too: never commit paid content)
- `python3 scripts/social.py`, `scripts/pins.py`, `scripts/reels.py`, `scripts/calendar.py` → `social/` and `docs/`
- `python3 scripts/handoff.py` → `docs/saturday-handoff.md` (edit `scripts/handoff_head.md` / `handoff_tail.md`, not the output)

## Article format

Front matter needs `title, description, slug, guide, published, order, summary, hero` (build fails otherwise). `hero` and `::figure` names must exist in `src/images.mjs`. Custom blocks: `:::facts`, `:::steps`, `:::note Title`, `::figure name | caption`. End every article with `## Sources`, starting "Checked in <Month Year>. Rules change: check the official source before you act."

The build also writes `/llms.txt` and a Markdown copy of each article at `articles/<slug>/index.md` for AI assistants.

## Git and deploy

- Work on the branch named in the session; PRs are squash-merged into `main`, and a push to `main` deploys via `.github/workflows/deploy.yml`.
- Force-push is blocked. Before new work: `git fetch origin main && git checkout -B <branch> origin/main`; before pushing: `git fetch origin <branch> && git merge -s ours origin/<branch>`, then push.
- Keep `upload-pages-artifact@v3` (newer versions may drop `.nojekyll`).

## Open items

Unconfirmed facts and owner-only tasks are listed in `docs/saturday-handoff.md`. Check there before re-researching anything.
