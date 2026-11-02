"""Turn each rendered carousel into a 1080x1920 Instagram Reel (H.264 + AAC).

  python3 scripts/reels.py            # all 30
  python3 scripts/reels.py 15-lefkada-quiz

Slides: social/out/<slug>/tiktok-01..08.jpg (1080x1920). Each slide shows for about 3 s with a
gentle slow zoom (alternating in/out) and 0.5 s crossfades: 8 x 3.5 s - 7 x 0.5 s = 24.5 s.
The first frame is slide 1, the hook.

Music: put legally usable tracks (CC0 / public domain / Pixabay Content Licence) in
social/reels/music/ named by mood: islands.*, food.*, words.*, calm.* (mp3, m4a, wav, ogg),
and list them in social/reels/MUSIC-LICENCES.md. The script trims the track to the video,
fades it in and out and normalises it to about -14 LUFS. With no track for a mood it adds a
silent AAC track, so every file is still H.264 + AAC.
"""
import glob, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES = os.path.join(ROOT, 'social', 'out')
MUSIC = os.path.join(ROOT, 'social', 'reels', 'music')
OUT = os.path.join(ROOT, 'social', 'reels', 'out')
FPS, D, XF = 30, 3.5, 0.5   # seconds per clip, crossfade length

# Mood per carousel number (islands & Lefkada: summery acoustic; food & coffee: light acoustic,
# Greek feel; Greek words: playful; paperwork, nomad, retire, money: calm lo-fi)
MOOD = {}
for n in ['02', '11', '14', '15', '20', '21', '26', '27', '30']: MOOD[n] = 'islands'
for n in ['01', '03', '05', '29']: MOOD[n] = 'food'
for n in ['08', '09', '10', '13', '24']: MOOD[n] = 'words'
for n in ['04', '06', '07', '12', '16', '17', '18', '19', '22', '23', '25', '28']: MOOD[n] = 'calm'


def track_for(mood):
    files = sorted(f for f in glob.glob(os.path.join(MUSIC, mood + '.*')) if f.rsplit('.', 1)[-1] in ('mp3', 'm4a', 'wav', 'ogg', 'flac'))
    return files[0] if files else None


def build(slug):
    imgs = [os.path.join(SLIDES, slug, f'tiktok-{i:02d}.jpg') for i in range(1, 9)]
    for p in imgs:
        if not os.path.exists(p):
            raise SystemExit(f'missing {p}: run python3 social/render/render.py first')
    n = len(imgs)
    total = n * D - (n - 1) * XF
    frames = int(D * FPS)
    args = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error']
    for p in imgs:
        args += ['-loop', '1', '-t', str(D), '-framerate', str(FPS), '-i', p]
    mood = MOOD[slug[:2]]
    track = track_for(mood)
    if track:
        args += ['-i', track]
    else:
        args += ['-f', 'lavfi', '-t', str(total), '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']
    fc = []
    for i in range(n):
        # upscale first so the zoom is smooth; zoom 1.00 -> 1.06 on even slides, 1.06 -> 1.00 on odd ones
        z = "'min(1+0.06*on/%d,1.06)'" % frames if i % 2 == 0 else "'max(1.06-0.06*on/%d,1.0)'" % frames
        fc.append(f"[{i}:v]scale=2160:3840,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},"
                  f"setsar=1,format=yuv420p,trim=duration={D},setpts=PTS-STARTPTS[v{i}]")
    prev = 'v0'
    for i in range(1, n):
        off = round(i * (D - XF), 3)
        fc.append(f'[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={off}[x{i}]')
        prev = f'x{i}'
    a = n
    if track:
        fc.append(f'[{a}:a]atrim=0:{total},asetpts=PTS-STARTPTS,afade=t=in:d=1,afade=t=out:st={total - 2}:d=2,'
                  f'loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]')
    else:
        fc.append(f'[{a}:a]atrim=0:{total},asetpts=PTS-STARTPTS[aout]')
    dest = os.path.join(OUT, f'{slug}.mp4')
    args += ['-filter_complex', ';'.join(fc), '-map', f'[{prev}]', '-map', '[aout]',
             '-c:v', 'libx264', '-preset', 'slow', '-crf', '27', '-pix_fmt', 'yuv420p', '-r', str(FPS),
             '-profile:v', 'high', '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-t', str(total),
             '-movflags', '+faststart', dest]
    subprocess.run(args, check=True)
    return dest, mood, track


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    car = json.load(open(os.path.join(ROOT, 'docs', 'social', 'carousels.json')))
    report = []
    for c in car:
        if only and c['slug'] != only:
            continue
        dest, mood, track = build(c['slug'])
        report.append((c['slug'], mood, os.path.basename(track) if track else 'silent'))
        print('reel', c['slug'], mood, os.path.basename(track) if track else 'silent', f'{os.path.getsize(dest) / 1e6:.1f} MB')
    json.dump(report, open(os.path.join(OUT, 'audio-report.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
