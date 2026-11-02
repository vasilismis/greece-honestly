# Regenerates docs/saturday-handoff.md from the blog drafts and carousel data.
# Posts listed in POSTED are marked as already published.
import json, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTED = {'01', '02', '03'}
car = json.load(open(os.path.join(ROOT, 'docs/social/carousels.json')))
posts = sorted(f for f in glob.glob(os.path.join(ROOT, 'docs/payhip-blog/[0-9]*.md')) if not f.endswith('.sources.md'))
L = [open(os.path.join(ROOT, 'scripts/handoff_head.md')).read().rstrip(), '',
     '## 2. Payhip blog drafts to post', '',
     'Folder: `docs/payhip-blog/`. Post the `.md` file; **do not** post the matching `.sources.md` (it is for checking). Each post ends with one product link, one site link and the AI disclosure.', '',
     '| Post | File | Status |', '|---|---|---|']
for f in posts:
    n = os.path.basename(f)[:2]
    title = open(f).readline().lstrip('# ').strip()
    L.append(f"| {title} | `{os.path.basename(f)}` | {'posted (per the founder)' if n in POSTED else '[ ] not posted'} |")
L += ['', '## 3. Carousels ready to post (TikTok and Instagram)', '',
      'Folder: `social/out/<slug>/`. `tiktok-01.jpg` … `tiktok-08.jpg` are 1080×1920; `instagram-01.jpg` … `instagram-08.jpg` are 1080×1350. Each folder has a `contact-sheet.jpg`. Post the slides in order with the caption below (it already ends with "AI characters, written in Greece." and 6 hashtags). All captions are also in `social/out/index.md`.', '']
for c in car:
    L += [f"### {c['title']}  ·  `social/out/{c['slug']}/`", '', '- [ ] TikTok  - [ ] Instagram', '', f"> {c['caption']}", '']
L.append(open(os.path.join(ROOT, 'scripts/handoff_tail.md')).read())
open(os.path.join(ROOT, 'docs/saturday-handoff.md'), 'w').write('\n'.join(L))
print(len(posts), 'posts,', len(car), 'carousels')
