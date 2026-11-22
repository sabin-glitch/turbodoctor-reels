"""Contact sheet of an MP4: one frame every <step> seconds, tiled. python3 sheet.py in.mp4 out.jpg [step] [cols]"""
import sys, subprocess, json, cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]
step = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
cols = int(sys.argv[4]) if len(sys.argv) > 4 else 9
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
tiles = []; t = 0.0
while t * fps < n:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps)); ok, f = cap.read()
    if not ok: break
    h, w = f.shape[:2]; s = 300 / max(h, w)
    f = cv2.resize(f, (int(w * s), int(h * s)))
    cv2.putText(f, f'{t:.0f}s', (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    tiles.append(f); t += step
th, tw_ = tiles[0].shape[:2]
rows = (len(tiles) + cols - 1) // cols
sheet = np.zeros((rows * th, cols * tw_, 3), np.uint8)
for i, f in enumerate(tiles):
    r, c = divmod(i, cols); sheet[r * th:r * th + f.shape[0], c * tw_:c * tw_ + f.shape[1]] = f
cv2.imwrite(dst, sheet, [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(tiles), 'tiles', n, 'frames', fps, 'fps')
