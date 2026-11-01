"""Check CSRT plate tracks (promo flote, 01.11.2026): draws each tracked box on its frame and tiles 360x200 crops around it, 6 per row.
   python3 -I verify_track.py <video> <track.json> <out.jpg> <name1,name2,...> <step_frames>"""
import cv2, json, sys, numpy as np
vid, tj, out = sys.argv[1], sys.argv[2], sys.argv[3]; names = sys.argv[4].split(","); step = int(sys.argv[5])
T = json.load(open(tj)); cap = cv2.VideoCapture(vid); tiles = []
for name in names:
    fr = sorted(int(k) for k in T[name])
    for f in fr[::step] + [fr[-1]]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read(); x0, y0, x1, y1 = T[name][str(f)]
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; X0, Y0 = max(0, min(1080 - 360, cx - 180)), max(0, min(1920 - 200, cy - 100))
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2); c = im[Y0:Y0 + 200, X0:X0 + 360].copy()
        cv2.putText(c, f"{name} {f/30:.2f}", (4, 18), 0, .55, (0, 255, 255), 2); tiles.append(c)
rows = [np.hstack(tiles[i:i + 6] + [np.zeros_like(tiles[0])] * (6 - len(tiles[i:i + 6]))) for i in range(0, len(tiles), 6)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(len(tiles))
