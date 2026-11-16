import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
# usage: cmp.py newWide newClose out.jpg
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
def old(t):
    p = 'cmp/o_full_%s.png' % t
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i','/mnt/project-files/animatii/TurboDoctor_Animatie_3D_Amorsare_Filtru_Motorina.mp4','-frames:v','1',p], check=True)
    return Image.open(p).convert('RGB')
pairs = [(old(62), Image.open(sys.argv[1]).convert('RGB')), (old(70.5), Image.open(sys.argv[2]).convert('RGB'))]
out = Image.new('RGB', (1080, 1920), (18, 20, 24)); d = ImageDraw.Draw(out)
for r, (a, b) in enumerate(pairs):
    for c, im in enumerate((a, b)):
        out.paste(im.resize((540, 960), Image.LANCZOS), (c * 540, r * 960))
    for c, txt in enumerate(('ACUM (three.js)', 'BLENDER (Cycles)')):
        x, y = c * 540 + 20, r * 960 + 20 if r else 960 - 70
        y = r * 960 + 880
        bb = d.textbbox((x, y), txt, font=F); d.rectangle((bb[0]-10, bb[1]-8, bb[2]+10, bb[3]+8), fill=(0, 0, 0))
        d.text((x, y), txt, font=F, fill=(255, 255, 255) if c == 0 else (90, 170, 255))
d.line((540, 0, 540, 1920), fill=(0, 0, 0), width=4); d.line((0, 960, 1080, 960), fill=(0, 0, 0), width=4)
out.save(sys.argv[3], quality=92)
