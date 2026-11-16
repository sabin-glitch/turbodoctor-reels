"""Măsoară fiecare variantă a rândului de hook: ce aude ASR-ul, unde sunt propozițiile, nivelul și înălțimea vocii pe fiecare propoziție."""
import sys, glob, os, subprocess, numpy as np, soundfile as sf, importlib.util
from scipy.signal import resample_poly
sys.argv = [sys.argv[0]] + sys.argv[1:]
spec = importlib.util.spec_from_file_location("mv", "/tmp/hookvo2/make_vo_lib.py"); mv = importlib.util.module_from_spec(spec); spec.loader.exec_module(mv)
def db(y): return 20 * np.log10(np.sqrt((np.asarray(y, np.float64) ** 2).mean()) + 1e-12)
def f0_med(x, sr):
    # autocorelație pe cadre de 40 ms, 90–320 Hz
    out = []; n = int(.04 * sr); hop = int(.01 * sr)
    for i in range(0, len(x) - n, hop):
        s = x[i:i + n] * np.hanning(n)
        if db(s) < -38: continue
        ac = np.correlate(s, s, "full")[n - 1:]; lo, hi = int(sr / 320), int(sr / 90); k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.45 * ac[0]: out.append(sr / k)
    return (float(np.median(out)), float(np.percentile(out, 90))) if len(out) > 4 else (0.0, 0.0)
for p in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "/tmp/hookvo2/takes/*.mp4")):
    w = p[:-4] + ".wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", "48000", w], check=True)
    x, sr = sf.read(w, dtype="float32"); x16 = resample_poly(x, 1, 3).astype(np.float32)
    toks, ts, text = mv.heard(x16)
    h = int(.01 * sr); e = 20 * np.log10(np.sqrt((x[:len(x) // h * h].reshape(-1, h) ** 2).mean(1)) + 1e-9); on = e > -45
    ed = np.flatnonzero(np.diff(np.concatenate([[0], on.astype(int), [0]]))); iv = []
    for a, b in zip(ed[::2], ed[1::2]):
        a, b = a * .01, b * .01
        if iv and a - iv[-1][1] < 0.22: iv[-1] = (iv[-1][0], b)
        elif b - a > 0.04: iv.append((a, b))
    print(f"{os.path.basename(p):14s} {len(x)/sr:4.2f}s  ASR: {text!r}")
    for a, b in iv:
        seg = x[int(a * sr):int(b * sr)]; f0, f90 = f0_med(seg, sr)
        print(f"     {a:4.2f}-{b:4.2f}  nivel {db(seg):6.1f} dB  vârf {20*np.log10(np.abs(seg).max()+1e-9):5.1f}  F0 {f0:4.0f} Hz (p90 {f90:4.0f})")
