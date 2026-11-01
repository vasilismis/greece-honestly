# Greece, Honestly

Practical English-language guides for visiting and moving to Greece. This repository is the static website: free articles that answer real questions and link to the paid guides on Payhip.

- No server, no database, no forms, no cookies, no tracking, no third-party scripts.
- Fonts (Noto Sans and Noto Serif, Latin + Greek, SIL Open Font License) are self-hosted in `src/static/fonts/`.
- Built by one small Node script (`scripts/build.mjs`), with `marked` as the only dependency.

## Add a new article (one Markdown file)

1. Create a file in `src/articles/`, for example `src/articles/greek-ferries-explained.md`.
2. Start it with this front matter, then write the article in Markdown underneath:

   ```markdown
   ---
   title: Greek ferries explained: tickets, ports and delays
   description: One or two sentences for Google and social previews (about 150 characters).
   slug: greek-ferries-explained
   guide: islands
   published: 2026-12-01
   order: 9
   summary: One short line shown on the article cards.
   ---

   Your intro paragraph…

   ## A heading

   More text, lists and tables (GitHub-style Markdown tables work).
   ```

   - `slug` becomes the URL: `/articles/greek-ferries-explained/`.
   - `guide` picks the call-to-action box at the end. Use one of: `retire`, `nomad`, `islands`, `eat`, `phrases`, `flashcards`, `first90`, `renting`, `alphabet` (defined in `src/site.mjs`).
   - `order` sets the position in lists (lower comes first).
   - Optional: `modified: 2027-01-15` when you update an article, and `lastChecked: January 2027` to override the default "Last checked" line.
   - Link to other articles with root paths, e.g. `[island groups](/articles/which-greek-island-is-right-for-you/)`. The build adds the base path for you.

3. Run `npm test` (build + link check). Commit and push to `main`; the site redeploys automatically. The article also appears on the home page, the articles list, `sitemap.xml` and `rss.xml`.

Use only facts you have checked, and keep each article dated with its "last checked" month.

## Local development

```bash
npm ci
npm run build      # writes dist/
npm run check      # checks internal links (add --external to also request Payhip URLs)
npm run serve      # preview at http://localhost:4321/greece-honestly/
```

## Configuration

Site-wide settings and the guide list (names, prices, Payhip links) are in `src/site.mjs`. These are set at build time by environment variables, or by repository **Variables** (Settings → Secrets and variables → Actions → Variables) in GitHub Actions:

| Variable | Default | Purpose |
|---|---|---|
| `SITE_URL` | `https://<owner>.github.io` | Origin used for canonical URLs, sitemap and RSS |
| `BASE_PATH` | `/<repository-name>/` | Path the site lives under |
| `CNAME` | empty | Custom domain; writes a `CNAME` file |
| `CONTACT_EMAIL` | empty | Shows a contact address on About and Privacy |

**Custom domain later:** set `SITE_URL=https://www.example.com`, `BASE_PATH=/` and `CNAME=www.example.com`, add the domain in Settings → Pages, and point DNS at GitHub Pages. With a domain at the root, `robots.txt` is also served where search engines look for it.

## Deploy

`.github/workflows/deploy.yml` builds on every push and pull request and deploys `main` to GitHub Pages. One-time setup: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
