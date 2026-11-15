# Coperta: cadrul fix „hero” la rezolutie plina + textele de la secunda 3 (titlu, cardul P2002, textul de jos)
import sys, os, subprocess, cv2, numpy as np
import comp
W, H = 1080, 1920
t = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0; out = sys.argv[2] if len(sys.argv) > 2 else 'cover.jpg'
subprocess.run(['node', 'hud_probe.js', str(t)], check=True)
p, z, J = comp.plate('heroB', 'solid', W, H)
bg = comp.background(W, H); img = bg * (1 - p[..., 3:4]) + p[..., :3]
img = comp.with_hud(img, int(round(t * 30)), W, H, 'hud_t')
cv2.imwrite(out, comp.to8(img), [cv2.IMWRITE_JPEG_QUALITY, 93]); print(out)
