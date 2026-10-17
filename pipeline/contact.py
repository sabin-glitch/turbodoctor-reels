"""Contact sheet: python3 contact.py <video> <out.jpg> [every_seconds=3]"""
import sys, cv2, numpy as np
cap = cv2.VideoCapture(sys.argv[1]); step = float(sys.argv[3]) if len(sys.argv) > 3 else 3
dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / (cap.get(cv2.CAP_PROP_FPS) or 30); tiles = []; t = 0.0
while t < dur:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = cap.read()
    if ok: f = cv2.resize(f, (135, 240)); cv2.putText(f, f"{t:.0f}", (4, 22), 0, .7, (0, 255, 255), 2); tiles.append(f)
    t += step
while len(tiles) % 12: tiles.append(np.zeros((240, 135, 3), np.uint8))
cv2.imwrite(sys.argv[2], np.vstack([np.hstack(tiles[i:i + 12]) for i in range(0, len(tiles), 12)]))
