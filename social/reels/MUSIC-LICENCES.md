# Music licences for the Reels

**Status (2 November 2026): no music has been added yet. Every reel currently has a silent AAC audio track.**

The build environment's network policy blocked every legal music source we tried: pixabay.com, cdn.pixabay.com, freemusicarchive.org, files.freemusicarchive.org, archive.org, commons.wikimedia.org, upload.wikimedia.org, incompetech.com, opengameart.org and ccmixter.org. We did not take audio from unverified mirrors, because the licence could not be proven.

## How to add music

1. Download one track per mood from a source whose licence allows use in social video **without attribution problems**:
   - Pixabay Music (Pixabay Content Licence)
   - Free Music Archive tracks marked CC0
   - public-domain recordings
2. Save them in `social/reels/music/` with these names (any of mp3, m4a, wav, ogg or flac):

| File | Mood | Used for carousels |
|---|---|---|
| `islands.mp3` | summery acoustic | 02, 11, 14, 15, 20, 21, 26, 27, 30 (islands and Lefkada) |
| `food.mp3` | light acoustic, Greek feel | 01, 03, 05, 29 (food and coffee) |
| `words.mp3` | playful | 08, 09, 10, 13, 24 (Greek words) |
| `calm.mp3` | calm lo-fi | 04, 06, 07, 12, 16, 17, 18, 19, 22, 23, 25, 28 (paperwork, nomad, retire, money) |

3. Fill in the table below for every track, then run `python3 scripts/reels.py`. It trims each track to the reel, fades it in and out, and normalises it to about −14 LUFS (true peak −1.5 dB).

## Tracks in use

| File | Title | Artist | URL | Licence | Downloaded |
|---|---|---|---|---|---|
| islands.* | – | – | – | – | not yet |
| food.* | – | – | – | – | not yet |
| words.* | – | – | – | – | not yet |
| calm.* | – | – | – | – | not yet |

Keep a screenshot or saved copy of each track's licence page with the download date.
