"""Base frames in OUTPUT order, NO stabilization: src/cfr.mp4 (720x1280) -> lanczos upscale 1080x1920.
Handles global speed (timeline 'speed'), in-reel B-roll (out/broll.json, same clip only) and the tip segment.
B-roll: [{"at": [win, "word", nth, offset_s] | seconds, "dur": s, "src": source_seconds, "speed": 1.0}]"""
import json, os, unicodedata, shutil
import cv2, numpy as np
ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(f"{ROOT}/out/timeline.json"))
FPS = tl["fps"]; n_out = int(round(tl["total"] * FPS)); SP = tl.get("speed", 1.0)
SEND = tl["story_end"]; TEND = tl.get("tip_end", SEND)
segs = tl["segments"]
ovr = next((s for s in segs if s["kind"] == "video_override"), None)
story = [s for s in segs if s["kind"] == "story"]
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isalnum())
def anchor(a):
    if isinstance(a, (int, float)): return float(a)
    win, word, nth, off = (list(a) + [0, 0])[:4]
    c = [w for w in tl["words"] if w["win"] == win and norm(w["text"]) == norm(word)]
    return c[nth]["os"] + off
BR = []
if os.path.exists(f"{ROOT}/out/broll.json"):
    for b in json.load(open(f"{ROOT}/out/broll.json")):
        a = anchor(b["at"]); BR.append(dict(out_a=round(a, 3), out_b=round(a + b["dur"], 3), src=b["src"], speed=b.get("speed", SP)))
json.dump(BR, open(f"{ROOT}/out/broll_resolved.json", "w"), indent=1)
def out_to_src(t):
    if SEND <= t < TEND and tl.get("tip_src") is not None:
        return tl["tip_src"] + (t - SEND) * tl.get("tip_speed", .7)
    for b in BR:
        if b["out_a"] <= t < b["out_b"] and t < SEND:
            return b["src"] + (t - b["out_a"]) * b["speed"]
    if ovr and t < tl["story_out0"]:
        return ovr["src_a"] + t * SP
    for s in story:
        d = (s["src_b"] - s["src_a"]) / SP
        if s["out_a"] - 1e-6 <= t < s["out_a"] + d:
            return s["src_a"] + (t - s["out_a"]) * SP
    return story[-1]["src_b"] - 1.0 / FPS
cap = cv2.VideoCapture(f"{ROOT}/src/cfr.mp4")
LAST = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
need = {}
for n in range(n_out):
    need.setdefault(max(0, min(LAST, int(round(out_to_src(n / FPS) * FPS)))), []).append(n)
shutil.rmtree(f"{ROOT}/frames_base", ignore_errors=True); os.makedirs(f"{ROOT}/frames_base", exist_ok=True)
i = 0; written = 0; last = max(need)
while i <= last:
    ok, fr = cap.read()
    if not ok: break
    if i in need:
        if fr.shape[1] != 1080 or fr.shape[0] != 1920:
            fr = cv2.resize(fr, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)
            bl = cv2.GaussianBlur(fr, (0, 0), 1.4); fr = cv2.addWeighted(fr, 1.30, bl, -0.30, 0)  # light sharpening only, no colour change
        for n in need[i]:
            cv2.imwrite(f"{ROOT}/frames_base/{n:05d}.jpg", fr, [cv2.IMWRITE_JPEG_QUALITY, 93]); written += 1
    i += 1
prev = None
for n in range(n_out):
    p = f"{ROOT}/frames_base/{n:05d}.jpg"
    if os.path.exists(p): prev = p
    elif prev: shutil.copyfile(prev, p); written += 1
print("output frames", n_out, "written", written, "broll", BR)
json.dump({"n_out": n_out}, open(f"{ROOT}/out/frames_meta.json", "w"))
