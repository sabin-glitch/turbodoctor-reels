"""Packs the rendered layers (out/*.png, converted to 8 bit) + the json files into layers.tar, so the films can be composited again without Blender."""
import os, glob, io, tarfile, cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
with tarfile.open(os.path.join(HERE, 'layers.tar'), 'w') as tar:
    for p in sorted(glob.glob(os.path.join(HERE, 'out', '*.png'))):
        a = cv2.imread(p, cv2.IMREAD_UNCHANGED)
        if a.dtype == np.uint16: a = ((a.astype(np.float32) + 128.0) / 257.0).astype(np.uint8)
        ok, buf = cv2.imencode('.png', a, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        ti = tarfile.TarInfo('out/' + os.path.basename(p)); ti.size = len(buf); tar.addfile(ti, io.BytesIO(buf.tobytes()))
    for n in ('info.json', 'crops.json', 'lattice.json', 'bbox.json'):
        tar.add(os.path.join(HERE, 'out', n), 'out/' + n)
print('layers.tar', os.path.getsize(os.path.join(HERE, 'layers.tar')) // 2 ** 20, 'MB')
