#!/bin/bash
# Promo reparații motoare: scaffold the reel folder from the compilation and transcribe it with one window per sequence.
set -e
R=/home/claude/reels/promo_motoare
bash /home/claude/turbodoctor-reels/new_reel.sh promo_motoare /home/claude/promo/all.mp4
# lossless voice track (separated / loudness-matched) instead of the AAC re-encode
cp /home/claude/promo/all_voice48.wav "$R/audio/src48.wav"
cp /home/claude/promo/all_voice16.wav "$R/audio/voice16k.wav"
cp /home/claude/promo/segs.json "$R/out/segs.json"
python3 - <<'EOF'
import json
S = json.load(open('/home/claude/promo/segs.json'))
wins = []
for s in S:
    a, b = s['out_t0'], s['out_t1']
    if s['name'] == 'trust':  # 21 s of speech: split at the pause after „ne apucăm de treabă.” (source 117.10-117.50)
        m = round(a + (117.30 - s['src_t0']), 3); wins += [(a, m), (m, b)]
    else: wins.append((a, b))
json.dump([(round(a, 3), round(b, 3)) for a, b in wins], open('/home/claude/reels/promo_motoare/out/wins.json', 'w'))
print(wins)
EOF
cd "$R" && python3 transcribe.py && python3 transcribe2.py && cat out/tr2.log
