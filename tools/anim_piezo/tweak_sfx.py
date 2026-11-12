"""Narrator reel: the hook's opening hit/glitch/whoosh land on the narrator's first word, so they are halved (run after render.py, before audio.py)."""
import json
p = "out/sfx.json"; S = json.load(open(p)); k = 0
for c in S:
    if c["t"] < 0.3 and c["kind"] in ("hit", "glitch", "whoosh"): c["gain"] = round(c["gain"] * 0.5, 3); k += 1
json.dump(S, open(p, "w"), indent=0); print("sfx tweaked:", k, "of", len(S))
