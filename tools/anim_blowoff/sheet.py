# python3 sheet.py t1,t2,... out.png [dir] [cols] -> contact sheet of stills (s_<t>.png), time stamped
import sys
from PIL import Image, ImageDraw
ts = sys.argv[1].split(','); out = sys.argv[2]; d = sys.argv[3] if len(sys.argv) > 3 else 'stills'; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
ims = [Image.open(f'{d}/s_{t}.png').convert('RGB') for t in ts]
w, h = ims[0].size; sc = 360 / w; w2, h2 = 360, int(h * sc); n = len(ims); cols = min(n, cols); rows = (n + cols - 1) // cols
S = Image.new('RGB', (w2 * cols, h2 * rows))
for i, im in enumerate(ims):
    im = im.resize((w2, h2)); ImageDraw.Draw(im).text((6, 4), ts[i], fill=(255, 255, 0)); S.paste(im, ((i % cols) * w2, (i // cols) * h2))
S.save(out)
