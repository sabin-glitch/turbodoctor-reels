"""Word timings measured by hand for this reel (run after build_timeline.py, before retime.py).
The bench is running in the clip, so the automatic alignment misplaces several words. The times below come from the
noise-subtracted voice envelope (syllable bursts), cross-checked with Parakeet token times and with Whisper on
progressively longer cuts. No cuts and speed 1.0, so output time = source time.
"injectoare" starts with a weak nasal before its first clear syllable (3.64 s) and "și acum" runs together, so those three starts
sit between the envelope and the recognisers (which agree with each other there)."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
W = [("Proces", .95, 1.30), ("de", 1.33, 1.44), ("testare", 1.48, 1.89), ("și", 1.92, 2.03), ("codare", 2.10, 2.56),
     ("injectoare", 3.52, 4.38), ("Bosch.", 4.73, 5.08),
     ("Injectoarele", 10.94, 11.50), ("au", 11.50, 11.60), ("fost", 11.60, 11.75), ("recondiționate", 11.77, 12.66), ("capital,", 12.70, 13.25),
     ("și", 13.45, 13.56), ("acum", 13.58, 13.92), ("sunt", 14.01, 14.11), ("în", 14.11, 14.16), ("procesul", 14.16, 14.63),
     ("final", 14.71, 14.99), ("de", 15.05, 15.21), ("codare.", 15.58, 15.90)]
p = f"{ROOT}/out/timeline.json"; tl = json.load(open(p))
assert not tl.get("speed"), "run right after build_timeline.py (before retime.py)"
assert [w["text"] for w in tl["words"]] == [w[0] for w in W], [w["text"] for w in tl["words"]]
for w, (_, s, e) in zip(tl["words"], W): w["s"] = w["os"] = s; w["e"] = w["oe"] = e
json.dump(tl, open(p, "w"), ensure_ascii=False, indent=1)
print("word timings fixed:", " ".join(f"{w['text']}@{w['os']:.2f}" for w in tl["words"]))
