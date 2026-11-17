"""Verificare cadru cu cadru a unei estompări fine (semnătură, scris de mână): contrast local x4, ca să se vadă și urmele slabe de pix.
   python3 sigcheck.py <video> <out.jpg> <decalaj cadre> <f0-f1> <x0,y0,x1,y1> <coloane> [pas]"""
import cv2, numpy as np, sys
vid, out, off = sys.argv[1], sys.argv[2], int(sys.argv[3]); rng = list(map(int, sys.argv[4].split('-'))); x0,y0,x1,y1 = map(int, sys.argv[5].split(',')); cols = int(sys.argv[6]); step = int(sys.argv[7]) if len(sys.argv) > 7 else 1
cap = cv2.VideoCapture(vid); tiles = []
for n in range(rng[0], rng[1] + 1, step):
    cap.set(cv2.CAP_PROP_POS_FRAMES, n + off); ok, fr = cap.read(); f = fr[y0:y1, x0:x1].astype(np.float32)
    bl = cv2.GaussianBlur(f, (0,0), 25); d = np.clip(128 + (f - bl) * 4.0, 0, 255).astype(np.uint8)
    cv2.putText(d, f"f{n}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 255), 3); tiles.append(cv2.resize(d, None, fx=.6, fy=.6))
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[i:i+cols]) for i in range(0, len(tiles), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
