"""Sunetul din hook („dacă ai diesel și auzi sunetul ăsta...”): taie efectul ales, îl pune în pauza dintre rândul 0 și rândul 1 al vocii
și scrie anvelopa lui, pe care animația o urmează (pulsurile roșii de aer întors din hook).
  ./run_iso.sh make_hook_sfx.py <efect.wav|mp3> <a> <b> [--shape] [--lead <fișier> <a> <b>]
    a, b      = secundele din efect care se păstrează
    --shape   = adâncește pulsurile (raportul dintre anvelopa de 6 ms și cea de 60 ms) și ridică puțin coada, ca „tu-tu-tu”-ul să nu se piardă
    --lead    = o bucată pusă înainte (sfârșitul unei accelerări), cu 9 dB mai încet
    --comp    = apropie coada de rafala de la început (compresie 2:1 pe anvelopa de 60 ms, cel mult +6 dB), ca fâlfâitul să se audă și pe difuzorul telefonului
    Pentru o înregistrare reală (varianta 2, 15.11.2026: o mașină care trece, cu fâlfâit de turbină și blow-off):
    --hp <Hz>             = taie frecvențele joase (zgomotul motorului), filtru trece-sus de ordinul 2
    --shelf <Hz> <dB>     = ridică înaltele (acolo stă șuieratul supapei)
    --fadein <s>          = intrare lină (apropierea mașinii); implicit 0,004 s
    --tail <t> <dB>       = ridică încet coada (de la secunda t din înregistrare), ca „pșș”-ul de după fâlfâit să nu se piardă
    --pre <dB>            = cât de încet rămâne apropierea mașinii față de eveniment (ex. -7), ca blow-off-ul să fie cel care se aude; cere --event
    --t0off <s>           = pauza dintre sfârșitul rândului 0 și sunet (implicit 0,15 s)
    --event <t>           = secunda din înregistrare la care începe evenimentul (ridicarea piciorului): devine `tb`, iar anvelopa e zero înaintea lui
    --flutter <a> <b>     = fereastra fâlfâitului în înregistrare -> `flutter` (față de tb); animația pâlpâie la 10 Hz în ea
    --acc <t1,t2,...>     = accentele pentru titluri (secunde din înregistrare) -> `accents`;  --psh <t> -> `psh` (momentul „pșș”-ului)
  -> vo/hook_bed.wav (48 kHz mono, vârf -3 dBFS) și vo/hook_sfx.json {t0, dur, tb, env (60 Hz, 0..1), accents, flutter, psh}
Sunetul intră la t0 = sfârșitul rândului 0 + 0,15 s și trebuie să se termine cu cel puțin 0,12 s înainte de rândul 1 (altfel scriptul se oprește).
În reel: out/v2.json -> "beds": [{"wav": "audio/hook_bed.wav", "t": t0, "gain": g, "duck": 0.6}]."""
import os, sys, json, subprocess, numpy as np, wave
from scipy import signal
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
def opt(name, n, cast=float):
    """--name v1 [v2]: scos din A; None dacă lipsește"""
    if name not in A: return None
    i = A.index(name); v = [cast(z) for z in A[i + 1:i + 1 + n]]; del A[i:i + 1 + n]; return v if n > 1 else v[0]
HP = opt("--hp", 1); SHELF = opt("--shelf", 2); FADEIN = opt("--fadein", 1) or .004; TAIL = opt("--tail", 2); T0OFF = opt("--t0off", 1)
PRE = opt("--pre", 1); EVENT = opt("--event", 1); FLUT = opt("--flutter", 2); ACC = opt("--acc", 1, str); PSH = opt("--psh", 1)
T0OFF = .15 if T0OFF is None else T0OFF
if "--lead" in A: i = A.index("--lead"); lead = (A[i + 1], float(A[i + 2]), float(A[i + 3])); del A[i:i + 4]
A = [a for a in A if a not in ("--shape", "--comp")]; f, a, b = A[0], float(A[1]), float(A[2])
if HP or SHELF:
    # filtrele se aplică pe toată înregistrarea (fără tranzitorii la capetele tăieturii), apoi se taie
    x = load(f, 0, 1e9)
    if HP: x = signal.sosfiltfilt(signal.butter(2, HP, "highpass", fs=SR, output="sos"), x)
    if SHELF: x = x + (10 ** (SHELF[1] / 20) - 1) * signal.sosfiltfilt(signal.butter(1, SHELF[0], "highpass", fs=SR, output="sos"), x)
    x = x[int(a * SR):int(b * SR)].copy()
else: x = load(f, a, b)
if TAIL:
    t = np.arange(len(x)) / SR + a; x = x * 10 ** (np.clip((t - TAIL[0]) / .15, 0, 1) ** 2 * (3 - 2 * np.clip((t - TAIL[0]) / .15, 0, 1)) * TAIL[1] / 20)
if PRE and EVENT is not None:
    t = np.arange(len(x)) / SR + a; u = np.clip((t - (EVENT - .14)) / .12, 0, 1); x = x * 10 ** ((1 - u * u * (3 - 2 * u)) * PRE / 20)
if shape:
    mod = np.clip(env(x, .006) / env(x, .06), .25, 2.5) ** 0.8; t = np.arange(len(x)) / SR
    x = x * mod * 10 ** (np.clip((t - .25) / .9, 0, 1) * 7 / 20)
if comp: e6 = env(x, .06); x = x * np.clip((e6 / e6.max()) ** -0.5, 1, 2.0)
x = fade(x, FADEIN, .18 if FADEIN > .01 else .12); x = x / np.abs(x).max()
lead_n = 0
if lead:
    l = fade(load(*lead), .30, .03); l = l / np.abs(l).max() * 10 ** (-9 / 20); lead_n = len(l); x = np.concatenate([l, x])
x = x * 10 ** (-3 / 20)
C = json.load(open(f"{D}/vo/cues.json")); t0 = round(C["lines"][0]["end"] + T0OFF, 3); dur = len(x) / SR; gap_end = C["lines"][1]["start"]
assert t0 + dur <= gap_end - .12 + 1e-6, f"sunetul ({dur:.2f} s) nu încape în pauză: se termină la {t0 + dur:.2f}, rândul 1 începe la {gap_end:.2f}"
w = wave.open(f"{D}/vo/hook_bed.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
e = env(x, .05); e[:lead_n] = 0
meta = dict(src=os.path.basename(f), cut=[a, b], shape=shape, comp=comp)
if EVENT is not None:
    # înregistrare reală: anvelopa pornește la eveniment (apropierea mașinii nu mișcă nimic în animație), accentele sunt date
    ke = int((EVENT - a) * SR); tt = np.arange(len(x)) / SR; e = e * np.clip((tt - (EVENT - a) + .06) / .06, 0, 1); e = e / e[ke:].max()
    tb = round(t0 + EVENT - a, 3); acc = [round(t0 + float(z) - a, 3) for z in ACC.split(",")] if ACC else [tb]
    if FLUT: meta["flutter"] = [round(FLUT[0] - EVENT, 3), round(FLUT[1] - EVENT, 3)]
    if PSH is not None: meta["psh"] = round(t0 + PSH - a, 3)
    meta.update(hp=HP, shelf=SHELF, fadein=FADEIN, tail=TAIL, pre=PRE, event=EVENT)
else:
    e = e / e.max()
    # accents for the titles and the shock rings: the loudest moment (the burst), then the flutter in visible steps
    k0 = int(np.argmax(e)); fl0 = k0 / SR + .34; acc = [round(t0 + k0 / SR - .03, 3)]; tb = round(t0 + k0 / SR, 3)
    tt = fl0
    while tt < dur - .25 and len(acc) < 6:
        if e[int(tt * SR)] > .12: acc.append(round(t0 + tt, 3))
        tt += .2
step = SR // 60; ev = [round(float(v), 3) for v in np.clip(e, 0, 1)[::step]]
json.dump(dict(t0=t0, dur=round(dur, 3), lead=round(lead_n / SR, 3), tb=tb, env=ev, accents=acc, **meta), open(f"{D}/vo/hook_sfx.json", "w"))
print(f"hook_bed.wav: {dur:.2f} s, intră la {t0:.2f}, se termină la {t0 + dur:.2f} (rândul 1 la {gap_end:.2f}); tb {tb}; accente {acc}; {meta}")
