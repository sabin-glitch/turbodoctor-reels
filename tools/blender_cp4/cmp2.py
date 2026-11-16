# Comparatie pe zona capului hidraulic: animatia three.js | Blender prima proba | Blender corectat
# utilizare: python3 cmp2.py original.png blender_v1.png blender_v2.png iesire.jpg
import sys
from PIL import Image, ImageDraw, ImageFont
o, v1, v2, out = sys.argv[1:5]
BOX = (335, 378, 911, 702)          # aceeasi zona in toate cele trei cadre 1080x1920
W, H, GAP = 1080, 607, 8
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
rows = [(o, 'ANIMAȚIA DE ACUM (three.js)', (47, 140, 255)), (v1, 'BLENDER, PRIMA PROBĂ', (150, 156, 165)), (v2, 'BLENDER, CORECTAT', (255, 106, 61))]
im = Image.new('RGB', (W, H * 3 + GAP * 2), (13, 16, 22))
for i, (p, lab, col) in enumerate(rows):
    a = Image.open(p).convert('RGB')
    assert a.size == (1080, 1920), (p, a.size)
    c = a.crop(BOX).resize((W, H), Image.LANCZOS)
    y = i * (H + GAP); im.paste(c, (0, y))
    d = ImageDraw.Draw(im, 'RGBA')
    tw = d.textlength(lab, font=F)
    d.rounded_rectangle((24, y + 22, 24 + tw + 44, y + 78), 12, fill=(13, 16, 22, 215))
    d.rectangle((24, y + 22, 32, y + 78), fill=col + (255,))
    d.text((48, y + 31), lab, font=F, fill=(255, 255, 255, 255))
im.save(out, quality=92)
print(out, im.size)
