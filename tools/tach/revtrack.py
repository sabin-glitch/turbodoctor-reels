"""Firing-frequency tracker for an engine recording (sub-harmonic summation + Viterbi continuity).
track(x, sr, t0, t1) -> times (s, absolute), f0 (Hz, firing frequency), salience."""
import numpy as np
from scipy.signal import get_window
def track(x, sr, t0, t1, fmin=24.0, fmax=150.0, nfft=16384, win=6144, hop=240, nh=8, decay=0.84, jump=14.0):
    a, b = int(t0 * sr), int(t1 * sr); seg = x[a:b].astype(np.float64)
    w = get_window("hann", win); nfr = 1 + (len(seg) - win) // hop
    cand = fmin * (fmax / fmin) ** (np.arange(160) / 159.0)             # log-spaced candidates
    S = np.zeros((nfr, len(cand))); fbin = sr / nfft
    for i in range(nfr):
        X = np.abs(np.fft.rfft(seg[i * hop:i * hop + win] * w, nfft))
        X = X / (X.max() + 1e-12)
        for h in range(1, nh + 1):
            idx = cand * h / fbin; i0 = np.floor(idx).astype(int); fr = idx - i0
            ok = i0 + 1 < len(X); v = np.zeros(len(cand)); v[ok] = X[i0[ok]] * (1 - fr[ok]) + X[i0[ok] + 1] * fr[ok]
            S[i] += decay ** (h - 1) * v
    # Viterbi: maximise salience - jump * |delta log2 f|
    lg = np.log2(cand); pen = jump * np.abs(lg[:, None] - lg[None, :])
    D = S[0].copy(); bp = np.zeros((nfr, len(cand)), int)
    for i in range(1, nfr):
        M = D[None, :] - pen; bp[i] = M.argmax(1); D = M.max(1) + S[i]
    path = np.zeros(nfr, int); path[-1] = D.argmax()
    for i in range(nfr - 1, 0, -1): path[i - 1] = bp[i][path[i]]
    f0 = cand[path]
    # parabolic refinement on the strongest partial near h*f0 (h=1,2) is skipped: log grid step is ~1.2%
    t = t0 + (np.arange(nfr) * hop + win / 2) / sr
    return t, f0, S[np.arange(nfr), path]
def smooth(f, n=9):
    k = np.hanning(n); k /= k.sum(); return np.convolve(np.pad(f, n // 2, mode="edge"), k, mode="valid")
if __name__ == "__main__":
    import sys, soundfile as sf, json
    path, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    x, sr = sf.read(path, dtype="float32"); x = x.mean(1) if x.ndim > 1 else x
    t, f, s = track(x, sr, t0, t1); fs = smooth(f)
    for k in range(0, len(t), 10): print(f"{t[k]:7.2f}  {fs[k]:6.1f} Hz  {30 * fs[k]:6.0f} rpm(4cyl)  sal {s[k]:.2f}")
    json.dump({"t": t.tolist(), "f": fs.tolist()}, open(sys.argv[4] if len(sys.argv) > 4 else "/tmp/track.json", "w"))
