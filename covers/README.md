# Guide covers

One cover system for every guide, matching the Payhip covers. Rendered by `scripts/covers.py`:

```bash
python3 scripts/covers.py
```

| Key | Guide | Photo | Badge |
|---|---|---|---|
| retire | Retire in Greece 2026 | coffee | 2026 |
| nomad | Digital Nomad in Greece 2026 | laptop-sea | 2026 |
| islands | Which Greek Island? 35 islands compared | santorini-dome | – |
| eat | What to Eat in Greece: the taverna menu decoder | taverna-chairs | – |
| phrases | Survival Greek: 150 phrases + audio | cyclades-chairs | – |
| flashcards | Survival Greek Flashcards | athens-street | – |
| first90 | Your First 90 Days in Greece | cyclades-harbour | – |
| renting | Renting in Greece: the tenant's kit | athens-alley | – |
| alphabet | FREE Greek Alphabet Cheat Sheet | greek-inscription | FREE |
| ionian | Lefkada & the Ionian Islands, Honestly | lefkada-green | – |
| athens | Athens for New Residents | athens-alley | – |

Each key has `<key>-1600x2560.jpg` (KDP / portrait) and `<key>-1000x1000.jpg` (square, Payhip thumbnail). Photos are the same ones the site uses for each guide.

- The two bullet lines only repeat what the guide's title or format already says.
- The Greek phrases and meanings come from the Greece, Honestly fact sheet.
- The footer reads "Written with AI tools, checked in Greece", to match the AI disclosure everywhere else. It is the `FOOTER` constant in `scripts/covers.py`.
- Fonts: DejaVu (Bitstream Vera licence) and Liberation Serif Italic (SIL Open Font License), in `social/render/fonts/`.
