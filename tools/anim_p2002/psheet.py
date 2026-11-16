# foaie de contact din cadre: psheet.py <iesire.jpg> <coloane> [crop_y0 crop_y1] -- <fisiere...>
import sys, cv2, numpy as np, os
out = sys.argv[1]; cols = int(sys.argv[2]); i = sys.argv.index('--'); crop = [int(v) for v in sys.argv[3:i]]; files = sys.argv[i + 1:]
ims = []
for f in files:
    im = cv2.imread(f)
    if im is None: print('lipseste', f); continue
    if crop: im = np.ascontiguousarray(im[crop[0]:crop[1]])
    cv2.putText(im, os.path.basename(f).replace('.jpg', ''), (20, im.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
    ims.append(im)
rows = [np.concatenate(ims[j:j + cols] + [np.zeros_like(ims[0])] * (cols - len(ims[j:j + cols])), 1) for j in range(0, len(ims), cols)]
sh = np.concatenate(rows, 0); sc = min(1.0, 2160.0 / sh.shape[1])
if sc < 1: sh = cv2.resize(sh, (int(sh.shape[1] * sc), int(sh.shape[0] * sc)), interpolation=cv2.INTER_AREA)
cv2.imwrite(out, sh, [cv2.IMWRITE_JPEG_QUALITY, 88]); print(sh.shape)
