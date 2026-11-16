#!/bin/bash
# Reel „Turbina o ia pe ulei”, hook v7 (16.11): vocea „Turbina o ia pe ulei! Află de ce.” peste motorul care se turează.
# Imaginea de după 10,3 s și sunetul de după 9,8 s rămân identice cu v6 (copiile din /tmp/v6_reel), aprobat de Sabin ca „bun”.
#   ./finish_v7.sh [T_A=0.30] [cover_t=4.85]
set -e
T_A=${1:-0.30}; COVER=${2:-4.85}
R=/home/claude/reels/runaway_diesel; H=/home/claude/runaway; OUT=/home/claude/deliver/TurboDoctor_Turbina_pe_ulei.mp4
cd "$H" && python3 splice_hook_vo2.py "$T_A" 0 1.0 > /tmp/v7_splice.log                 # vocea + cronologia (rândul 0 nou, rândul 1 = „Știi de ce…”)
"$H/partial_hook_render.sh"                                                             # cadrele 0..308 cu titlurile noi + restul randării v6
cd "$R" && python3 tweak_sfx.py                                                         # impacturile titlurilor, încet (vorbește vocea)
cd "$H" && HOOK_UNDER_DB=-27 HOOK_UNDER_SLOPE=0.6 HOOK_DUCK=-14 python3 make_hook_bed7.py 5.4 7.1 > /tmp/v7_bed.log   # motorul: sub voce, apoi urlet
cd "$R" && python3 audio.py > out/audio.log 2>&1 && python3 finish_hook_audio.py -15.0 > out/hook_audio.log 2>&1
ffmpeg -hide_banner -loglevel error -y -i out/video_noaudio.mp4 -i audio/mix_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "${OUT%.mp4}_tmp.mp4"
mv "${OUT%.mp4}_tmp.mp4" "$OUT"
ffmpeg -hide_banner -loglevel error -y -ss "$COVER" -i "$OUT" -frames:v 1 -q:v 2 "${OUT%.mp4}_coperta.jpg"
python3 verify_sync.py 0.1-3.7,5.2-9.1,10.3-16,60.4-66,165.6-174.3 > out/verify.log 2>&1 || true
echo "FINISH_V7_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s $(stat -c %s "$OUT")"
