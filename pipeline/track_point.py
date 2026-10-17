import os
import cv2, numpy as np, json, sys
F0, F1, REF, X, Y, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
P = np.array([X, Y])
def load(n):
    return cv2.resize(cv2.imread(f"frames_base/{n:05d}.jpg", cv2.IMREAD_GRAYSCALE), (540, 960))
def track(order):
    pos = {REF: P.copy()}; prev = load(order[0]); p = P.copy()
    for n in order[1:]:
        cur = load(n); m = np.zeros_like(prev); cv2.circle(m, (int(p[0] / 2), int(p[1] / 2)), 60, 255, -1)
        pts = cv2.goodFeaturesToTrack(prev, 60, 0.01, 5, mask=m)
        if pts is not None and len(pts) >= 4:
            nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, cur, pts, None, winSize=(31, 31), maxLevel=3)
            d = (nxt - pts)[st.ravel() == 1].reshape(-1, 2)
            if len(d): p = p + 2 * np.median(d, axis=0)
        pos[n] = p.copy(); prev = cur
    return pos
pos = {**track(list(range(REF, F0 - 1, -1))), **track(list(range(REF, F1 + 1)))}
json.dump({str(k): [round(float(v[0]), 1), round(float(v[1]), 1)] for k, v in sorted(pos.items())}, open(OUT, "w"))
tiles = []
for n in range(F0, F1 + 1, max(1, (F1 - F0) // 8)):
    im = cv2.imread(f"frames_base/{n:05d}.jpg"); x, y = pos[n]
    cv2.circle(im, (int(x), int(y)), 60, (0, 0, 255), 10); cv2.putText(im, str(n), (30, 120), 0, 3, (0, 255, 255), 6)
    tiles.append(cv2.resize(im, (200, 356)))
cv2.imwrite(OUT.replace(".json", ".jpg"), np.hstack(tiles))
