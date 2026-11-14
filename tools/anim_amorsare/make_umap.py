"""vo/cues.json + vo_script.json -> vo/umap.json (segmente voce -> U) și vo/uframes.json (U pe fiecare cadru, 30 fps).
Rândul 0 (hook) merge liniar pe intervalul lui; de la rândul 1, începutul fiecărui rând se leagă de u0 al lui, iar între ancore
U urmează o curbă monotonă PCHIP (viteza nu sare). Ultimul rând ajunge la u1 la story_end; pe cardul de final U rămâne pe loc."""
import json, os
import numpy as np
from scipy.interpolate import PchipInterpolator
H = os.path.dirname(os.path.abspath(__file__)); FPS = 30
S = json.load(open(f"{H}/vo_script.json")); C = json.load(open(f"{H}/vo/cues.json")); tl = json.load(open(f"{H}/vo/timeline.json"))
st = [l["start"] for l in C["lines"]]; end = C["end"]
h1 = st[1] - 0.05                                   # tăietura după hook, chiar înaintea rândului 1
xs = [h1] + st[1:] + [end]; us = [S[1]["u"][0]] + [S[i]["u"][0] for i in range(1, len(S))] + [S[-1]["u"][1]]
xs[1] = st[1]; xs = [st[1]] + st[2:] + [end]; us = [S[i]["u"][0] for i in range(1, len(S))] + [S[-1]["u"][1]]
f = PchipInterpolator(xs, us)
n = int(round(tl["total"] * FPS)); U = []
for i in range(n):
    t = i / FPS
    if t < h1: a, b = S[0]["u"]; U.append(a + (b - a) * t / h1)
    elif t < st[1]: U.append(S[1]["u"][0])
    elif t <= end: U.append(float(f(t)))
    else: U.append(float(f(end)))
segs = [[0.0, st[1], *S[0]["u"]]] + [[st[i], (st[i + 1] if i + 1 < len(st) else end), *S[i]["u"]] for i in range(1, len(S))]
json.dump(dict(end=end, segs=segs), open(f"{H}/vo/umap.json", "w"), indent=0)
json.dump([round(u, 4) for u in U], open(f"{H}/vo/uframes.json", "w"))
print(n, "cadre; U", round(min(U), 2), "->", round(max(U), 2)); 
for s in segs: print(" %.2f-%.2f  U %.1f-%.1f  x%.2f" % (s[0], s[1], s[2], s[3], (s[3]-s[2])/max(.01,s[1]-s[0])))
