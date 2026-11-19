"""Генератор демо-відео: сцена (scenes/<slug>.html) -> video/<slug>.mp4 + .jpg.

Потрібно: pip install playwright (використовується встановлений Chrome), ffmpeg у PATH.
Запуск:  python -X utf8 tools/video/render.py [slug ...]   (без аргументів — усі сцени)
Сцена задає window.DUR, window.CUR, window.CAPS, window.POSTER (секунда для постера).
Кадри знімаються детерміновано через window.setT(t), без запису екрана.
"""
import os, subprocess, sys, tempfile, shutil, glob
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "video")
FPS = 15

def page_html(slug):
    css = open(os.path.join(HERE, "base.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "engine.js"), encoding="utf-8").read()
    body = open(os.path.join(HERE, "scenes", slug + ".html"), encoding="utf-8").read()
    return f"""<!doctype html><html lang="uk"><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="brand"><i>Л</i>Лад · ladtech.com.ua</div>
{body}
<div class="cap"><div class="pill" id="pill"><i></i><span></span></div></div>
<svg id="cur" viewBox="0 0 24 24"><path d="M3 2l15 9-6.5 1.5L8 19z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>
<div id="ring"></div>
<script>{js}</script></body></html>"""

def render(slug, pw):
    tmp = tempfile.mkdtemp()
    b = pw.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.set_content(page_html(slug))
    pg.wait_for_timeout(300)
    dur = pg.evaluate("window.DUR"); poster = pg.evaluate("window.POSTER")
    n = int(dur * FPS)
    for i in range(n):
        pg.evaluate(f"setT({i / FPS})")
        pg.screenshot(path=os.path.join(tmp, f"f{i:04d}.jpg"), type="jpeg", quality=92)
    pg.evaluate(f"setT({poster})")
    pg.screenshot(path=os.path.join(OUT, slug + ".jpg"), type="jpeg", quality=88)
    b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.jpg"),
                    "-c:v", "libx264", "-crf", "30", "-preset", "slow", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", os.path.join(OUT, slug + ".mp4")], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(slug, os.path.getsize(os.path.join(OUT, slug + ".mp4")), "bytes")

if __name__ == "__main__":
    slugs = sys.argv[1:] or [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(HERE, "scenes", "*.html"))]
    with sync_playwright() as pw:
        for s in slugs:
            render(s, pw)
