# foaie de contact: python sheet.py out.jpg img1.png img2.png ... [--cols N] [--w 270]
import sys, cv2, numpy as np, os
a = sys.argv[1:]; out = a[0]; cols = int(a[a.index('--cols') + 1]) if '--cols' in a else 6
tw = int(a[a.index('--w') + 1]) if '--w' in a else 270
fs = [x for x in a[1:] if not x.startswith('--') and os.path.exists(x)]
ims = []
for f in fs:
    im = cv2.imread(f, cv2.IMREAD_UNCHANGED)
    if im.shape[2] == 4:
        al = im[..., 3:4].astype(np.float32) / 255; bg = np.full_like(im[..., :3], (22, 18, 15)); im = (im[..., :3] * al + bg * (1 - al)).astype(np.uint8)
    h = int(im.shape[0] * tw / im.shape[1]); im = cv2.resize(im, (tw, h), interpolation=cv2.INTER_AREA)
    cv2.putText(im, os.path.basename(f).replace('.png', '').replace('.jpg', '')[:28], (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (80, 255, 255), 1, cv2.LINE_AA)
    ims.append(im)
H = max(i.shape[0] for i in ims); ims = [np.pad(i, ((0, H - i.shape[0]), (0, 0), (0, 0))) for i in ims]
while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[i:i + cols]) for i in range(0, len(ims), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(out)
