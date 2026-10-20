#!/bin/bash
# after intro_vo.py: timeline, frames, track shift, cover, intro test frames -> preview/intro_sheet.jpg
H=$(cd "$(dirname "$0")" && pwd); R=/home/claude/reels/$1; cd "$R" || exit 1
# --light: timeline and frames unchanged (only reel.js / compositor changed)
[ "$2" = "--light" ] || { python3 build_timeline.py > out/bt.log 2>&1 && python3 retime.py > out/rt.log 2>&1 && python3 extract_frames.py > out/ef.log 2>&1; } || { echo "PREP_FAIL $1"; exit 1; }
python3 $H/prep_hook.py $1 --stage post > out/post.log 2>&1 || { echo "POST_FAIL $1"; exit 1; }
TT=$(python3 - <<'EOF'
import json
ij = json.load(open("out/intro.json")); P = ij["phrases"]; cz = json.load(open("out/cover_t.json"))["t"]
print(",".join(f"{t:.2f}" for t in [P[0]["t1"] - .1, P[2]["t1"], cz, P[-1]["t0"] + 1.2, ij["dur"] + 1.0]))
EOF
)
rm -f preview/t*.jpg; python3 render.py --test $TT > out/test.log 2>&1
grep -q "CFG_ERR" out/test.log && { echo "CFG_ERR $1: $(grep CFG_ERR out/test.log)"; exit 1; }
python3 - <<'EOF'
from PIL import Image; import glob
fs = sorted(glob.glob("preview/t*.jpg")); W, H = 324, 576
sheet = Image.new("RGB", (W * len(fs), H), "black")
for i, f in enumerate(fs): sheet.paste(Image.open(f).resize((W, H)), (i * W, 0))
sheet.save("preview/intro_sheet.jpg", quality=86)
EOF
echo "TEST_OK $1 $TT"
