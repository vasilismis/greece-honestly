# Paid guides

Two guides, each in its own folder with `content.md` (the text), `sources.md` (sources and the Unchecked list) and `out/` (built files):

| Folder | Title | Suggested price |
|---|---|---|
| `ionian-islands-honestly/` | Lefkada & the Ionian Islands, Honestly | €9 |
| `athens-for-new-residents/` | Athens for New Residents | €9 |

Each `out/` folder holds the built files: `<slug>-A4.pdf`, `<slug>-Letter.pdf`, `<slug>.epub`, `cover-1600x2560.jpg` (KDP), `thumbnail-1000x1000.jpg` and the chapter opener images.

**This repository is public, so the paid material is not committed.** `content.md` (the full text) and the PDFs, EPUBs and openers are listed in `.gitignore`; only the build pipeline, `sources.md`, the cover and the thumbnail are in the repo. Keep `content.md` in a private place (a private repository or your own drive) and copy it into `guides/<slug>/` before building.

## Build

Needs Python 3 + Pillow, pandoc, and Node with Playwright (Chromium).

```bash
python3 guides/build.py                          # both guides
python3 guides/build.py athens-for-new-residents # one guide
```

- `build.py`: renders the cover, thumbnail and chapter openers with the shared visual system (`social/render/greece_style.py`), then makes the HTML and prints it to A4 and US Letter PDFs with Chromium (`pdf.cjs`), and makes the EPUB with pandoc.
- `print.css` / `print-template.html`: print layout (11pt body, page numbers, cover, title and contents pages). `epub.css`: e-reader styles.
- A chapter heading names its opener photo: `# Corfu {#corfu photo=corfu-boats kicker="Island 2"}`. The build stops if a chapter uses a photo whose file name names a different place.
