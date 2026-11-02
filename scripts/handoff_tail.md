## 4. The two new paid guides

| Guide | Listing | Cover (KDP) | Thumbnail | Suggested price |
|---|---|---|---|---|
| Lefkada & the Ionian Islands, Honestly | `guides/ionian-islands-honestly/listing.md` | `guides/ionian-islands-honestly/out/cover-1600x2560.jpg` | `…/out/thumbnail-1000x1000.jpg` | €9 |
| Athens for New Residents | `guides/athens-for-new-residents/listing.md` | `guides/athens-for-new-residents/out/cover-1600x2560.jpg` | `…/out/thumbnail-1000x1000.jpg` | €9 |

- [ ] **The PDFs and EPUBs are not in this repository** (it is public, so they would be free to download). Use the newest zip handed over on 2 November (`greece-honestly-paid-guides-v3.zip`: it has the Lafcadio Hearn fix and the new covers) (it contains `content.md`, A4 and US Letter PDFs, EPUB, cover, thumbnail). Keep it somewhere private.
- [ ] Run the EPUBs through epubcheck or the store's own validator before uploading (could not be run in the build environment).
- [ ] Create both products on Payhip, then add their Payhip links to `src/site.mjs` (`guides`), to the "Our other guides" lists at the end of each guide's `content.md`, and rebuild (`python3 guides/build.py`).

## 4b. Covers (one system for everything)

- [ ] All 11 covers are in `covers/` (`<key>-1600x2560.jpg` for KDP / portrait, `<key>-1000x1000.jpg` for Payhip thumbnails). See `covers/README.md` for which file belongs to which guide, and `covers/contact-sheet.jpg` for an overview.
- [ ] Upload the square covers as the Payhip product images for the 9 existing guides, so the shop matches the site (the site's guide cards and product boxes already use them).
- **Cover footer:** "Written with AI tools, checked in Greece". Approved by the founder on 2 November 2026; keep it everywhere (`FOOTER` in `scripts/covers.py`).
- [ ] The two bullet lines on each cover only repeat what the title or format already says, because the contents of the 9 existing PDFs were not available here. Replace them with real highlights from each PDF if you like (`GUIDES` in `scripts/covers.py`).

## 4c. Social calendar

- [ ] `docs/social-calendar.md`: 14 days, one carousel a day from Monday 9 to Sunday 22 November, with a ready TikTok caption and Instagram caption for each (AI label line and 6 hashtags included). Tick the boxes as you post. Regenerate with `python3 scripts/calendar.py` if you change the plan.

## 4d. Pinterest (new photo-system pins)

The old flat navy pins are being deleted. The new set is in `social/pinterest/` (see `contact-sheet-pins.jpg`):

- 33 pins at 1000×1500 in `social/pinterest/pins/`: 22 articles (each links to its article) and 11 products (each links to its Payhip page). There are 33 rather than 30 because the plan was one per article plus one per product.
- **Boards:** Moving to Greece: Checklists & Tips · Learn Greek: Phrases & Alphabet · Greek Islands: Where to Go · Greek Food: What to Eat in Greece · Living in Greece, Honestly · Lefkada & the Ionian.
- `social/pinterest/pins.csv` has file, title (100 characters max), description (500 characters max, ending "AI characters, written in Greece."), destination URL and board.
- `social/pinterest/pinterest-bulk.csv` is in Pinterest's bulk-create format (Title, Media URL, Pinterest board, Description, Link, Keywords). The media URLs point at raw.githubusercontent.com, so they work once this is on `main`.

To do:
- [ ] Create the six boards with exactly these names before importing.
- [ ] Upload `pinterest-bulk.csv` (Pinterest: Create → bulk create pins), or post the pins by hand from `pins.csv`.
- [ ] **Pins 32 and 33** (Lefkada & the Ionian, Athens for New Residents) link to the Payhip shop page for now. Put their product URLs in `PRODUCTS` in `scripts/pins.py` once the products exist, run `python3 scripts/pins.py`, and edit the two pins on Pinterest.
- [ ] Space the pins out (for example 2–3 a day) rather than publishing all 33 at once.

## 4e. Instagram Reels (audio baked in)

- 30 reels in `social/reels/out/<slug>.mp4`. Each is 1080×1920, H.264 + AAC, 24.5 s: 8 slides of about 3 s each, a gentle slow zoom and 0.5 s crossfades. The first frame is the hook slide. Rebuild with `python3 scripts/reels.py`.
- Captions are in `social/reels/captions.md`: same short tone as the TikTok ones, with the AI line and 6 hashtags.
- [ ] **Music is missing: every reel currently has a silent audio track.** This build environment's network policy blocked every legal music source (Pixabay, Free Music Archive, archive.org, Wikimedia, incompetech, OpenGameArt, ccMixter). There are two ways to fix it:
  - Allow one of those domains in the cloud environment's network settings (environment menu → Edit → Network access → Allowed domains; docs: https://code.claude.com/docs/en/cloud-environments#network-access) and ask Claude to finish the job.
  - Or download four tracks yourself (`islands`, `food`, `words`, `calm`) into `social/reels/music/`, record them in `social/reels/MUSIC-LICENCES.md`, and run `python3 scripts/reels.py`. It trims, fades and normalises to about −14 LUFS.
- [ ] Post as Reels, not carousels. Pick the cover in Instagram's editor if it doesn't default to the first frame.

## 4f. Gumroad listings

- [ ] `docs/gumroad-update.md` covers all 9 Gumroad products: the cover and thumbnail files from `covers/`, a description and up to 8 tags for each. Paste the real "What is inside" list from each Payhip listing where marked; those texts were not available here. Confirm the three prices shown as "see shop" on the site.

## 5. Things that need a human (could not be confirmed online)

- [ ] **Navagio (Zakynthos):** the access ban ran to 31 October 2026 (Gazette B' 3033/28.05.2026). No follow-up decision had been published on 2 November. Update the Ionian guide and `ionian-islands-compared` when it is.
- [ ] **1 May 2027:** falls on Holy Saturday. Watch for a Ministry of Labour decision (in 2024 the holiday moved to 7 May for the public sector) and update `greek-public-holidays-2027` and the Athens guide.
- [ ] **S1 registration:** GOV.UK says EOPYY; EOPYY's own cross-border page says e-EFKA. A phone call to a KEP or EOPYY would settle it; the texts currently state both.
- [ ] **Department of Aliens of Athens opening hours:** not published reliably. Phone 210 340 5807 or email tallodathinon@astynomia.gr and add the hours to the Athens guide.
- [ ] **Rental deposits:** no legal cap or refund deadline was found. A Greek lawyer could confirm there is none.
- [ ] **Pharmacy phrases and Athens phrases 13–20:** standard Greek, but not found word for word in a cited source. A Greek speaker should read them once.
- [ ] **Guide prices shown as "see shop"** (Survival Greek, First 90 Days, Renting kit): add the real prices to `src/site.mjs` if you want them on the site.
- [ ] **Contact email:** still a placeholder on About and Privacy (set the `CONTACT_EMAIL` repository variable).

## 6. Housekeeping (optional)

- `actions/checkout` and `actions/setup-node` were bumped to v5 (Node 24) on 2 November. `upload-pages-artifact@v3` and `deploy-pages@v4` were left as they are. Check their release notes before bumping: newer upload-pages-artifact versions may skip hidden files such as `.nojekyll`.
- With a custom domain (`SITE_URL`, `BASE_PATH=/`, `CNAME` variables), `robots.txt` will sit at the domain root and the Lighthouse SEO score rises from 92.
