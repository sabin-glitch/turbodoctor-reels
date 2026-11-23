"""Convert the Blender layers in out/ (16-bit PNG) to 8-bit PNG in layers8/ and pack them in layers.tar (for the repo)."""
import os, sys, glob, tarfile
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'out'); DST = os.path.join(HERE, 'layers8')
os.makedirs(DST, exist_ok=True)
names = sorted(glob.glob(os.path.join(SRC, '*.png')))
for p in names:
    a = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    if a.dtype == np.uint16: a = ((a.astype(np.float32) + 128.0) / 257.0).astype(np.uint8)
    cv2.imwrite(os.path.join(DST, os.path.basename(p)), a, [cv2.IMWRITE_PNG_COMPRESSION, 9])
for j in ('info.json', 'crops.json', 'geo.json', 'bbox.json'):
    if os.path.exists(os.path.join(SRC, j)): open(os.path.join(DST, j), 'wb').write(open(os.path.join(SRC, j), 'rb').read())
with tarfile.open(os.path.join(HERE, 'layers.tar'), 'w') as t:
    for p in sorted(os.listdir(DST)):
        t.add(os.path.join(DST, p), arcname='out/' + p)
print(len(names), 'layers ->', os.path.getsize(os.path.join(HERE, 'layers.tar')) / 1e6, 'MB')
