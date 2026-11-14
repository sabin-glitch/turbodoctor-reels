"""Crop the public-domain S63 engine photo (Commons: File:BMW X5M Engine.JPG, PD-user) to the schematic panel size.
usage: python3 -I prep_photo.py <in.jpg> <out.jpg> x0 y0 x1 y1 W H"""
import sys, cv2, numpy as np
src, out = sys.argv[1], sys.argv[2]; x0, y0, x1, y1, W, H = map(int, sys.argv[3:9])
im = cv2.imread(src)[y0:y1, x0:x1]
im = cv2.resize(im, (W, H), interpolation=cv2.INTER_AREA)
# light local contrast + sharpening only (no colour cast): the 2009 compact-camera photo is a little flat
lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB); l = lab[..., 0]
lab[..., 0] = cv2.createCLAHE(clipLimit=1.6, tileGridSize=(4, 8)).apply(l)
im = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
bl = cv2.GaussianBlur(im, (0, 0), 1.2); im = cv2.addWeighted(im, 1.35, bl, -0.35, 0)
cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 93]); print(out, im.shape)
