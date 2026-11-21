# plansa de verificare din placi: python3 psheet.py out.jpg dir name1 name2 ... [--h 480]
import sys, cv2, numpy as np, os
out, d = sys.argv[1], sys.argv[2]; names = [x for x in sys.argv[3:] if not x.startswith('--')]
hh = int(sys.argv[sys.argv.index('--h') + 1]) if '--h' in sys.argv else 480
ims = []
for n in names:
    im = cv2.imread(os.path.join(d, n + '.png'), cv2.IMREAD_UNCHANGED)
    if im is None: print('missing', n); continue
    if im.shape[2] == 4:
        a = im[..., 3:4].astype(np.float32) / 255; bg = np.full_like(im[..., :3], (38, 26, 18), np.float32)
        im = (im[..., :3].astype(np.float32) * a + bg * (1 - a)).astype(np.uint8)
    im = cv2.resize(im, (int(im.shape[1] * hh / im.shape[0]), hh), interpolation=cv2.INTER_AREA)
    cv2.putText(im, n, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1); ims.append(im)
cv2.imwrite(out, np.concatenate(ims, 1), [cv2.IMWRITE_JPEG_QUALITY, 90])
