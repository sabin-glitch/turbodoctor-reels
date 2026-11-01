"""Full-resolution crops with a 60 px grid (1080x1920 coords), to place plate keyframes and to check the blur:
   python3 fullcrop.py <video> <out.jpg> x0 y0 x1 y1 t1 t2 ...   (6 crops per row)"""
import cv2, numpy as np, sys
vid, out = sys.argv[1], sys.argv[2]; X0, Y0, X1, Y1 = map(int, sys.argv[3:7]); ts = [float(x) for x in sys.argv[7:]]
cap = cv2.VideoCapture(vid); fps = cap.get(cv2.CAP_PROP_FPS); ims = []
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps))); ok, im = cap.read()
    if im.shape[1] != 1080: im = cv2.resize(im, (1080, 1920))
    im = im[Y0:Y1, X0:X1].copy()
    for v in range(((X0 + 59) // 60) * 60, X1, 60): cv2.line(im, (v - X0, 0), (v - X0, im.shape[0]), (0, 200, 0), 1); cv2.putText(im, str(v), (v - X0 + 2, 12), 0, .4, (0, 255, 255), 1)
    for v in range(((Y0 + 59) // 60) * 60, Y1, 60): cv2.line(im, (0, v - Y0), (im.shape[1], v - Y0), (0, 200, 0), 1); cv2.putText(im, str(v), (2, v - Y0 + 12), 0, .4, (0, 255, 255), 1)
    cv2.putText(im, f"t={t:.2f}", (5, im.shape[0] - 8), 0, .7, (0, 0, 255), 2); ims.append(im)
rows = [np.hstack(ims[i:i + 6] + [np.zeros_like(ims[0])] * (6 - len(ims[i:i + 6]))) for i in range(0, len(ims), 6)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
