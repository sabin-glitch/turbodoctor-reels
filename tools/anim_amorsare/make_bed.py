"""Sunet de fond pentru reel-ul „Amorsare filtru motorină”: demarorul (U 56,1–60,2) și frecarea metal pe metal din pompa CP4
care merge cu aer (U 66,4–78,6, crește odată cu scânteile), pe momentele din vo/uframes.json.   python3 make_bed.py <out.wav>"""
import json, sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
U = np.array(json.load(open(f"{HERE}/vo/uframes.json"))); n = int(len(U) / 30 * SR)
u = np.interp(np.arange(n) / SR, np.arange(len(U)) / 30, U); t = np.arange(n) / SR; rng = np.random.default_rng(4)
sm = lambda x: np.clip(x, 0, 1) ** 2 * (3 - 2 * np.clip(x, 0, 1))
noise = rng.standard_normal(n)
# frecare: zgomot trecut prin bandă, modulat de trecerea camei (2 lobi pe tură)
g = sm((u - 66.4) / 2.5) * (1 - sm((u - 77.6) / 1.0))
ph = np.cumsum(np.where(g > 0, 9.0, 0)) / SR * 2 * np.pi
grind = sosfilt(butter(2, [1800, 5200], "bp", fs=SR, output="sos"), noise) * (.55 + .45 * np.abs(np.sin(ph))) \
      + .5 * sosfilt(butter(2, [220, 700], "bp", fs=SR, output="sos"), noise) * (.4 + .6 * np.abs(np.sin(ph * .5)))
# demaror: puls grav repetat
c = sm((u - 56.1) / .3) * (1 - sm((u - 59.9) / .4)); pc = np.cumsum(np.where(c > 0, 7.5, 0)) / SR * 2 * np.pi
crank = (np.sin(2 * np.pi * 95 * t) * .6 + sosfilt(butter(2, [300, 1400], "bp", fs=SR, output="sos"), noise) * .5) * (.35 + .65 * np.maximum(0, np.sin(pc)) ** 2)
out = .11 * g * grind / (np.abs(grind).max() + 1e-9) * 4 + .16 * c * crank
# la tăietura hook -> poveste (U sare înapoi) sunetul se stinge în 80 ms
out = np.clip(out, -.6, .6).astype(np.float32); sf.write(sys.argv[1], out, SR); print("bed", n / SR, "s", "peak", float(np.abs(out).max()))
