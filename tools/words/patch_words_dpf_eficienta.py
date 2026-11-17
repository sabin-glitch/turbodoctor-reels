"""Fix word start times where the recogniser stamped a word early (in the silence before it) or where the curated text differs from
what it heard. Times are read from the voice envelope (check_words.py). python3 patch_words.py <reel_dir>
Natural pace, no cuts: output time = source time."""
import json, sys, unicodedata
R = sys.argv[1]
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())
FIX = [  # (window, word, nth, new start)
    (0, "Atunci", 0, 0.55), (0, "când", 0, 0.96), (0, "un", 0, 1.12), (0, "filtru", 0, 1.22), (0, "de", 0, 1.44), (0, "particule", 0, 1.56),
    (1, "recondiționare", 0, 13.62), (1, "După", 0, 14.62), (1, "a", 0, 18.25), (1, "ajuns", 0, 18.36), (1, "și", 0, 19.25), (1, "a", 1, 19.36), (1, "fost", 0, 19.46),
    (1, "cu", 0, 20.86), (1, "ceramic", 0, 22.52), (1, "a", 2, 24.86), (1, "primit", 0, 24.96), (1, "miezul", 0, 27.67),
    (2, "Carbura", 0, 34.92), (2, "să", 0, 40.59), (2, "se", 1, 40.82), (2, "crape", 0, 41.22), (2, "față", 0, 41.86), (2, "Țineți", 0, 48.68), (2, "costul", 0, 52.98),
    (3, "cele", 1, 59.27), (3, "celor", 0, 68.30),
]
END = [(3, "aftermarket", 0, 58.86)]  # (window, word, nth, new end): the word ends here, the next (unclear) connective is left out of the captions
for name in ("timeline.json", "timeline_1x.json"):
    p = f"{R}/out/{name}"; tl = json.load(open(p)); W = tl["words"]
    for win, word, nth, s in FIX:
        idx = [i for i, w in enumerate(W) if w["win"] == win and norm(w["text"]) == norm(word)][nth]
        W[idx]["s"] = W[idx]["os"] = s
    for i, w in enumerate(W):
        nx = W[i + 1]["s"] if i + 1 < len(W) else w["e"]
        assert i + 1 >= len(W) or nx > w["s"], f'order: {w["text"]} {w["s"]} -> {W[i + 1]["text"]} {nx}'
        if w["e"] <= w["s"] + .05: w["e"] = min(nx, w["s"] + 1.1)
        if w["e"] > nx: w["e"] = nx
        w["e"] = round(max(w["e"], w["s"] + .06), 3); w["oe"] = round(max(w["os"] + .08, w["e"]), 3)
    for win, word, nth, e in END:
        w = [w for w in W if w["win"] == win and norm(w["text"]) == norm(word)][nth]; w["e"] = w["oe"] = e
    json.dump(tl, open(p, "w"), ensure_ascii=False, indent=1)
print("patched", len(FIX), "words")
