"""Speed up the whole story (cold open + story) by SPEED and add the optional 'engineer tip' segment.
Reads out/timeline.json produced by build_timeline2.py (1x), keeps a copy in out/timeline_1x.json.
Config: out/v2.json {"speed": 1.0, "tip": {"dur": 3.4, "src": 12.0, "speed": 0.7}} (speed default 1.0 = natural pace)"""
import json, os
ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
p = f"{ROOT}/out/timeline.json"; p1 = f"{ROOT}/out/timeline_1x.json"
tl = json.load(open(p))
if tl.get("speed"): tl = json.load(open(p1))
else: json.dump(tl, open(p1, "w"), ensure_ascii=False, indent=1)
cfg = json.load(open(f"{ROOT}/out/v2.json")) if os.path.exists(f"{ROOT}/out/v2.json") else {}
SP = float(cfg.get("speed", 1.0)); tip = cfg.get("tip", {"dur": 0})  # default 1.0: natural pace (Sabin, 18.10.2026)
assert not (tl.get("intro") and abs(SP - 1) > 1e-3), "synthetic intro needs speed 1.0"
for s in tl["segments"]: s["out_a"] = round(s["out_a"] / SP, 4)
for w in tl["words"]: w["os"] = round(w["os"] / SP, 4); w["oe"] = round(w["oe"] / SP, 4)
for w in tl["cold_words"]: w["os"] = round(w["os"] / SP, 4); w["oe"] = round(w["oe"] / SP, 4)
tl["story_out0"] = round(tl["story_out0"] / SP, 4); tl["story_end"] = round(tl["story_end"] / SP, 4)
tl["speed"] = SP
tl["tip_end"] = round(tl["story_end"] + float(tip.get("dur", 0)), 4); tl["tip_src"] = tip.get("src"); tl["tip_speed"] = float(tip.get("speed", .7))
tl["total"] = round(tl["tip_end"] + tl["end_card"], 4)
json.dump(tl, open(p, "w"), ensure_ascii=False, indent=1)
print(f"speed {SP}  hook {tl['story_out0']:.2f}s  story end {tl['story_end']:.2f}s  tip end {tl['tip_end']:.2f}s  total {tl['total']:.2f}s")
