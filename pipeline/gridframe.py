"""python3 gridframe.py out.jpg t1 t2 ... -> frames_base at times, 432x768 each, grid every 120px (full-res coords labeled)"""
import cv2, numpy as np, sys
out = sys.argv[1]; ts = [float(x) for x in sys.argv[2:]]; ims = []
for t in ts:
    im = cv2.imread(f'frames_base/{int(round(t*30)):05d}.jpg'); im = cv2.resize(im, (432, 768)); s = 432 / 1080
    for v in range(0, 1080, 120): cv2.line(im, (int(v*s), 0), (int(v*s), 768), (0, 255, 0), 1); cv2.putText(im, str(v), (int(v*s)+2, 12), 0, .35, (0, 255, 255), 1)
    for v in range(0, 1920, 120): cv2.line(im, (0, int(v*s)), (432, int(v*s)), (0, 255, 0), 1); cv2.putText(im, str(v), (2, int(v*s)+12), 0, .35, (0, 255, 255), 1)
    cv2.putText(im, f't={t}', (300, 760), 0, .6, (0, 0, 255), 2); ims.append(im)
rows = [np.hstack(ims[i:i+4] + [np.zeros_like(ims[0])] * (4 - len(ims[i:i+4]))) for i in range(0, len(ims), 4)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
