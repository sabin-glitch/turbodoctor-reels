"""Contact sheet: python3 sheet.py <video> <out.jpg> [n=14] [t0] [t1] [cols=7]"""
import sys, cv2, numpy as np
p, out = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 14
cap = cv2.VideoCapture(p); N = int(cap.get(7)); fps = cap.get(5)
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0; t1 = float(sys.argv[5]) if len(sys.argv) > 5 else (N - 1) / fps
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 7
tiles = []
for t in np.linspace(t0, t1, n):
    cap.set(1, int(round(t * fps))); ok, im = cap.read()
    if not ok: continue
    im = cv2.resize(im, (216, 384), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.1f}", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, .65, (0, 0, 0), 4); cv2.putText(im, f"{t:.1f}", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, .65, (0, 255, 255), 2)
    tiles.append(im)
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 86]); print(out, N, fps)
