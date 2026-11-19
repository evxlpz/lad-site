#!/usr/bin/env python3
"""Квадратний логотип 512x512 (logo.png) за мотивом favicon.svg: темний квадрат із лаймовою лінією-«пульсом».
Запуск: python tools/make_logo.py  (потрібен Pillow). Результат лежить у корені репозиторію."""
import os
from PIL import Image, ImageDraw

S, SS = 512, 4            # розмір і супер-семплінг для гладких країв
K = S * SS / 32           # favicon.svg має viewBox 32x32
BG, FG = (22, 24, 29), (198, 242, 107)   # #16181D, #C6F26B
PTS = [(6, 16), (12, 16), (16, 7), (20, 25), (24, 16), (26, 16)]   # path "M6 16h6l4-9 4 18 4-9h2"
W = 2.6 * K

img = Image.new('RGB', (S * SS, S * SS), BG)
d = ImageDraw.Draw(img)
pts = [(x * K, y * K) for x, y in PTS]
d.line(pts, fill=FG, width=round(W), joint='curve')
r = W / 2
for x, y in (pts[0], pts[-1]):   # круглі кінці лінії
    d.ellipse((x - r, y - r, x + r, y + r), fill=FG)
img = img.resize((S, S), Image.LANCZOS)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logo.png')
img.save(out, optimize=True)
print('ok', out)
