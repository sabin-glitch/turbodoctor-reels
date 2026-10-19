"""plates_keep.py <dense.json> [keep=3,4] [skip=5,9] [drop=10:3.55-4.55]: after looking at the plates.py sheet, fix the blur list.
  keep=  tracks that ARE plates but were marked skip (e.g. a plate the coarse pass missed),
  skip=  tracks that are NOT plates (sticker, lift branding, a logo on a jacket),
  drop=  removes the samples of one track inside a time range (the track jumped onto a logo for a moment).
Edits the JSON in place and prints the tracks that caption_clean.py --plates will blur."""
import sys, json
p = sys.argv[1]; D = json.load(open(p)); keep, skip = set(), set()
drops = []
for a in sys.argv[2:]:
    k, v = a.split("=")
    if k == "drop":
        tid, rng = v.split(":"); t0, t1 = map(float, rng.split("-")); drops.append((int(tid), t0, t1)); continue
    s = {int(x) for x in v.split(",") if x}
    (keep if k == "keep" else skip).update(s)
for tid, t0, t1 in drops:
    for tr in D["tracks"]:
        if tr["id"] == tid:
            tr["boxes"] = [r for r in tr["boxes"] if not (t0 <= r[0] <= t1)]
            tr["t0"], tr["t1"], tr["n"] = tr["boxes"][0][0], tr["boxes"][-1][0], len(tr["boxes"])
for tr in D["tracks"]:
    if tr["id"] in keep: tr.pop("skip", None)
    if tr["id"] in skip: tr["skip"] = True
json.dump(D, open(p, "w"), indent=1)
print("blur:", [tr["id"] for tr in D["tracks"] if not tr.get("skip")])
