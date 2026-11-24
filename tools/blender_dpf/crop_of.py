"""crop (tier px) of a 3D box:  python3 crop_of.py <tier> x0 x1 z0 z1 [y0 y1] [pad]"""
import json, sys, numpy as np
I = json.load(open('out/info.json')); M = np.array(I['M']); k = I['lens'] / I['sensor']; S = I['base']
def proj(p):
    q = M @ np.array([p[0], p[1], p[2], 1.0]); return (0.5 + k * q[0] / -q[2]) * S, (0.5 - k * q[1] / -q[2]) * S
t = int(sys.argv[1]); x0, x1, z0, z1 = map(float, sys.argv[2:6]); y0, y1 = (float(sys.argv[6]), float(sys.argv[7])) if len(sys.argv) > 7 else (0.0, 0.0)
pad = int(sys.argv[8]) if len(sys.argv) > 8 else 10
P = np.array([proj((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]) * t
print(','.join(str(int(v)) for v in (P[:, 0].min() - pad, P[:, 1].min() - pad, P[:, 0].max() + pad, P[:, 1].max() + pad)))
