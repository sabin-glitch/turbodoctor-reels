"""endbg_fix.py <reel dir> x0,y0,x1,y1 -> assets/end_bg.jpg rebuilt from the last story frame with the burned-in text in the box painted out
(the blurred end-card background otherwise keeps a coloured smear of the old title). Same blur/darkening as render.py prep(). Run after --prep."""
import sys, json, cv2, numpy as np
R = sys.argv[1].rstrip("/"); x0, y0, x1, y1 = map(int, sys.argv[2].split(","))
tl = json.load(open(f"{R}/out/timeline.json")); n = int(tl.get("tip_end", tl["story_end"]) * tl["fps"]) - 1
fr = cv2.imread(f"{R}/frames_base/{n:05d}.jpg"); roi = fr[y0:y1, x0:x1].astype(np.int32)
b, g, r = roi[..., 0], roi[..., 1], roi[..., 2]
m = ((r > 140) & (r - np.maximum(g, b) > 55)).astype(np.uint8) * 255          # red title
m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
M = np.zeros(fr.shape[:2], np.uint8); M[y0:y1, x0:x1] = m
fr = cv2.inpaint(fr, M, 9, cv2.INPAINT_TELEA)
cv2.imwrite(f"{R}/preview/endbg_src.jpg", fr)
fr = cv2.GaussianBlur(fr, (0, 0), 24); fr = (fr.astype(np.float32) * 0.40).astype(np.uint8)
cv2.imwrite(f"{R}/assets/end_bg.jpg", fr, [cv2.IMWRITE_JPEG_QUALITY, 92]); print("end_bg rebuilt from frame", n, "mask px", int((M > 0).sum()))
