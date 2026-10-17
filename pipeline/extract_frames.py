"""Write base frames in OUTPUT order (cold open + tightened story) as JPEGs: frames_base/%05d.jpg"""
import json, os, cv2

ROOT = os.environ.get("REEL_ROOT") or os.path.dirname(os.path.abspath(__file__))
tl = json.load(open(f"{ROOT}/out/timeline.json"))
FPS = tl["fps"]
n_out = int(round(tl["total"] * FPS))
segs = tl["segments"]
ovr = next((s for s in segs if s["kind"] == "video_override"), None)  # cold-open visuals (optional)
story = [s for s in segs if s["kind"] == "story"]


def out_to_src(t):
    if ovr and t < ovr["src_b"] - ovr["src_a"]:
        return ovr["src_a"] + t
    for s in story:
        d = s["src_b"] - s["src_a"]
        if s["out_a"] - 1e-6 <= t < s["out_a"] + d:
            return s["src_a"] + (t - s["out_a"])
    return story[-1]["src_b"] - 1.0 / FPS  # end card: last frame


LAST = int(cv2.VideoCapture(f"{ROOT}/src/stab.mp4").get(cv2.CAP_PROP_FRAME_COUNT)) - 1
need = {}
for n in range(n_out):
    src_idx = min(LAST, int(round(out_to_src(n / FPS) * FPS)))
    need.setdefault(src_idx, []).append(n)

os.makedirs(f"{ROOT}/frames_base", exist_ok=True)
cap = cv2.VideoCapture(f"{ROOT}/src/stab.mp4")
i = 0; written = 0
last = max(need)
while i <= last:
    ok, fr = cap.read()
    if not ok:
        break
    if i in need:
        for n in need[i]:
            cv2.imwrite(f"{ROOT}/frames_base/{n:05d}.jpg", fr, [cv2.IMWRITE_JPEG_QUALITY, 94]); written += 1
    i += 1
print("output frames", n_out, "written", written)
json.dump({"n_out": n_out}, open(f"{ROOT}/out/frames_meta.json", "w"))
