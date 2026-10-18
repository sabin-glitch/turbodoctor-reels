import cv2, numpy as np, glob, sys
fs = sorted(glob.glob('preview/t*.jpg'))
ims = [cv2.resize(cv2.imread(f), (270, 480)) for f in fs]
for im, f in zip(ims, fs): cv2.putText(im, f.split('/t')[-1][:-4], (6, 28), 0, .8, (0, 0, 0), 4); cv2.putText(im, f.split('/t')[-1][:-4], (6, 28), 0, .8, (0, 255, 255), 2)
while len(ims) % 8: ims.append(np.zeros_like(ims[0]))
cv2.imwrite('preview/sheet.jpg', np.vstack([np.hstack(ims[i:i+8]) for i in range(0, len(ims), 8)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
