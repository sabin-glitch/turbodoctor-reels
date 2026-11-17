"""Corectează începutul unor cuvinte din out/timeline.json după anvelopa vocii (rulat între build_timeline.py și retime.py).
Primul token al unei ferestre ASR și cuvintele de după o pauză primesc uneori un timp prea devreme (0,2–0,5 s): subtitrarea ar apărea înaintea vorbei.
out/word_fix.json: [[fereastră, "cuvânt", nth, start_s], ...] (timpul din sursă; merge cu "cuts": false, "speed": 1.0, fără cold open)."""
import json, os, unicodedata
ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
p = f"{ROOT}/out/timeline.json"; tl = json.load(open(p)); assert not tl.get("speed"), "run right after build_timeline.py, before retime.py"
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn"); return "".join(c for c in s if c.isalnum())
W = tl["words"]; n = 0
for win, word, nth, t in json.load(open(f"{ROOT}/out/word_fix.json")):
    c = [i for i, w in enumerate(W) if w["win"] == win and norm(w["text"]) == norm(word)]; i = c[nth]; w = W[i]
    d = t - w["s"]; w["s"] = round(t, 3); w["os"] = round(w["os"] + d, 3); w["e"] = max(w["e"], round(w["s"] + .08, 3)); w["oe"] = max(w["oe"], round(w["os"] + .08, 3))
    if i and W[i - 1]["win"] == win and W[i - 1]["oe"] > w["os"]: W[i - 1]["oe"] = w["os"]; W[i - 1]["e"] = w["s"]
    n += 1
for a, b in zip(W, W[1:]): assert b["os"] > a["os"], (a, b)
json.dump(tl, open(p, "w"), ensure_ascii=False, indent=1); print("word starts fixed:", n)
