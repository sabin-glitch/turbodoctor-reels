"""Compact voice envelope: python3 env2.py <wav> a b  -> one line per second, a digit (0-9) per 20 ms (150-4000 Hz RMS), plus the onset times."""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
wav, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); hop = .02
x, sr = sf.read(wav, dtype="float32"); x = x if x.ndim == 1 else x.mean(axis=1)
y = sosfiltfilt(butter(4, [150, 4000], btype="band", fs=sr, output="sos"), x); n = int(hop * sr)
N = len(y) // n; db = np.array([20 * np.log10(np.sqrt(np.mean(y[i * n:(i + 1) * n] ** 2)) + 1e-9) for i in range(N)])
mx = np.percentile(db, 99); lo = mx - 40
on = []
for i in range(max(2, int(a / hop)), min(N, int(b / hop))):
    if db[i] > mx - 26 and db[i] - min(db[i - 1], db[i - 2]) > 8: 
        if not on or i * hop - on[-1] > .06: on.append(round(i * hop, 2))
s = int(a)
while s < b:
    seg = db[int(s / hop):int((s + 1) / hop)]
    print(f"{s:3d} " + "".join(str(int(np.clip((d - lo) / 40 * 9.99, 0, 9))) for d in seg))
    s += 1
print("onsets:", " ".join(f"{t:.2f}" for t in on))
