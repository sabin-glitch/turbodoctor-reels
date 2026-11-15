"""Sunetul din hook („dacă ai diesel și auzi sunetul ăsta...”): taie efectul ales, îl pune în pauza dintre rândul 0 și rândul 1 al vocii
și scrie anvelopa lui, pe care animația o urmează (pulsurile roșii de aer întors din hook).
  ./run_iso.sh make_hook_sfx.py <efect.wav|mp3> <a> <b> [--shape] [--lead <fișier> <a> <b>]
    a, b      = secundele din efect care se păstrează
    --shape   = adâncește pulsurile (raportul dintre anvelopa de 6 ms și cea de 60 ms) și ridică puțin coada, ca „tu-tu-tu”-ul să nu se piardă
    --lead    = o bucată pusă înainte (sfârșitul unei accelerări), cu 9 dB mai încet
    --comp    = apropie coada de rafala de la început (compresie 2:1 pe anvelopa de 60 ms, cel mult +6 dB), ca fâlfâitul să se audă și pe difuzorul telefonului
  -> vo/hook_bed.wav (48 kHz mono, vârf -3 dBFS) și vo/hook_sfx.json {t0, dur, env (60 Hz, 0..1), accents}
Sunetul intră la t0 = sfârșitul rândului 0 + 0,15 s și trebuie să se termine cu cel puțin 0,12 s înainte de rândul 1 (altfel scriptul se oprește).
În reel: out/v2.json -> "beds": [{"wav": "audio/hook_bed.wav", "t": t0, "gain": g, "duck": 0.6}]."""
import os, sys, json, subprocess, numpy as np, wave
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000
def load(f, a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64); return x[int(a * SR):int(b * SR)].copy()
def fade(x, a, b):
    x = x.copy(); na, nb = int(a * SR), int(b * SR)
    if na: x[:na] *= np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    if nb: x[-nb:] *= np.cos(np.linspace(0, np.pi / 2, nb)) ** 2
    return x
def env(x, win):
    n = max(1, int(win * SR)); return np.sqrt(np.convolve(x ** 2, np.ones(n) / n, "same") + 1e-12)
A = sys.argv[1:]; shape = "--shape" in A; comp = "--comp" in A; lead = None
if "--lead" in A: i = A.index("--lead"); lead = (A[i + 1], float(A[i + 2]), float(A[i + 3])); del A[i:i + 4]
A = [a for a in A if a not in ("--shape", "--comp")]; f, a, b = A[0], float(A[1]), float(A[2])
x = load(f, a, b)
if shape:
    mod = np.clip(env(x, .006) / env(x, .06), .25, 2.5) ** 0.8; t = np.arange(len(x)) / SR
    x = x * mod * 10 ** (np.clip((t - .25) / .9, 0, 1) * 7 / 20)
if comp: e6 = env(x, .06); x = x * np.clip((e6 / e6.max()) ** -0.5, 1, 2.0)
x = fade(x, .004, .12); x = x / np.abs(x).max()
lead_n = 0
if lead:
    l = fade(load(*lead), .30, .03); l = l / np.abs(l).max() * 10 ** (-9 / 20); lead_n = len(l); x = np.concatenate([l, x])
x = x * 10 ** (-3 / 20)
C = json.load(open(f"{D}/vo/cues.json")); t0 = round(C["lines"][0]["end"] + .15, 3); dur = len(x) / SR; gap_end = C["lines"][1]["start"]
assert t0 + dur <= gap_end - .12 + 1e-6, f"sunetul ({dur:.2f} s) nu încape în pauză: se termină la {t0 + dur:.2f}, rândul 1 începe la {gap_end:.2f}"
w = wave.open(f"{D}/vo/hook_bed.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
e = env(x, .05); e[:lead_n] = 0; e = e / e.max(); step = SR // 60; ev = [round(float(v), 3) for v in e[::step]]
# accents for the titles and the shock rings: the loudest moment (the burst), then the flutter in visible steps
k0 = int(np.argmax(e)); fl0 = k0 / SR + .34; acc = [round(t0 + k0 / SR - .03, 3)]
tt = fl0
while tt < dur - .25 and len(acc) < 6:
    if e[int(tt * SR)] > .12: acc.append(round(t0 + tt, 3))
    tt += .2
json.dump(dict(t0=t0, dur=round(dur, 3), lead=round(lead_n / SR, 3), tb=round(t0 + k0 / SR, 3), env=ev, accents=acc, src=os.path.basename(f), cut=[a, b], shape=shape, comp=comp), open(f"{D}/vo/hook_sfx.json", "w"))
print(f"hook_bed.wav: {dur:.2f} s, intră la {t0:.2f}, se termină la {t0 + dur:.2f} (rândul 1 la {gap_end:.2f}); accente {acc}")
