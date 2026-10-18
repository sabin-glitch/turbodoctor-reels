"""Check the W('word', t) / WE('word', t) anchors of reel.js against out/timeline.json before rendering:
python3 anchors_check.py  (in a reel folder) -> lists anchors that are missing or more than 1.5 s from the given time."""
import json, re, unicodedata
tl = json.load(open("out/timeline.json"))
def nn(s):
    s = unicodedata.normalize("NFD", s); s = "".join(c for c in s if unicodedata.category(c) != "Mn"); return re.sub(r"[^a-z0-9]", "", s.lower())
src = open("reel.js").read(); bad = 0
for name, word, t in re.findall(r"(\w+): WE?\('([^']+)', ([0-9.]+)\)", src):
    t = float(t); c = [w for w in tl["words"] if nn(w["text"]) == nn(word)]
    if not c: print("MISSING", name, word); bad += 1; continue
    b = min(c, key=lambda w: abs(w["os"] - t))
    if abs(b["os"] - t) > 1.5: print("FAR", name, word, t, "->", round(b["os"], 2)); bad += 1
print("anchors ok" if not bad else f"{bad} bad anchors")
