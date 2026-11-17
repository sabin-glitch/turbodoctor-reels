"""List caption words whose start falls in silence (the recogniser stamped them early): python3 check_words.py <reel_dir>"""
import json, sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt
R = sys.argv[1]; x, sr = sf.read(f"{R}/audio/src48.wav", dtype="float32"); x = x if x.ndim == 1 else x.mean(axis=1)
y = sosfiltfilt(butter(4, [150, 4000], btype="band", fs=sr, output="sos"), x); hop = .01; n = int(hop * sr); N = len(y) // n
db = np.array([20 * np.log10(np.sqrt(np.mean(y[i * n:(i + 1) * n] ** 2)) + 1e-9) for i in range(N)]); mx = np.percentile(db, 99); thr = mx - 24
tl = json.load(open(f"{R}/out/timeline.json"))
for w in tl["words"]:
    i = int(w["s"] / hop)
    if db[i:i + 8].max() < thr:  # 80 ms of silence at the stamped start
        j = i
        while j < N - 4 and not (db[j:j + 4] > thr).all(): j += 1
        if (j - i) * hop > .1: print(f'win {w["win"]} {w["text"]:16s} stamped {w["s"]:6.2f} -> voice starts {j * hop:6.2f}  (+{(j - i) * hop:.2f})')
