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
- [ ] **Decide the footer line.** The covers read "Written with AI tools, checked in Greece" to keep the AI disclosure that is everywhere else. If you prefer "Written and checked in Greece", change `FOOTER` in `scripts/covers.py` and run `python3 scripts/covers.py` (then rebuild the site and the guides).
- [ ] The two bullet lines on each cover only repeat what the title or format already says, because the contents of the 9 existing PDFs were not available here. Replace them with real highlights from each PDF if you like (`GUIDES` in `scripts/covers.py`).

## 4c. Social calendar

- [ ] `docs/social-calendar.md`: 14 days, one carousel a day from Monday 9 to Sunday 22 November, with a ready TikTok caption and Instagram caption for each (AI label line and 6 hashtags included). Tick the boxes as you post. Regenerate with `python3 scripts/calendar.py` if you change the plan.

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

- GitHub warns that actions in `.github/workflows/deploy.yml` run on a Node 20 runtime that is being retired; bump `actions/checkout`, `setup-node`, `upload-pages-artifact` and `deploy-pages` to their latest major versions when convenient.
- With a custom domain (`SITE_URL`, `BASE_PATH=/`, `CNAME` variables), `robots.txt` will sit at the domain root and the Lighthouse SEO score rises from 92.
