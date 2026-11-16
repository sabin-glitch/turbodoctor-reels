"""Hook-ul v6 e purtat de sunetul motorului care urcă încontinuu (audio/hook_bed.wav): bubuiturile titlurilor nu trebuie să-l acopere
și nici să pară salturi în urcare. Primul impact (pe primul cadru) rămâne mai prezent, cele din timpul urcării sunt doar o atingere.
Rulează după render.py, înainte de audio.py."""
import json
p = "out/sfx.json"; S = json.load(open(p)); k = 0
for c in S:
    if c["kind"] not in ("boom", "crack", "glitch", "hit", "whoosh", "rise"): continue
    if c["t"] < 0.5: c["gain"] = round(c["gain"] * 0.6, 3); k += 1
    elif c["t"] < 5.3: c["gain"] = round(c["gain"] * (0.11 if c["kind"] == "glitch" else 0.15), 4); k += 1
json.dump(S, open(p, "w"), indent=0); print("sfx tweaked:", k, "of", len(S))
