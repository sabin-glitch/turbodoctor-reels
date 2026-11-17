#!/bin/bash
# Re-render only the first K frames of a reel and splice them, without re-encoding, onto the rest of the previous full render.
# partial_head_render.sh <slug> <K> <prev video_noaudio.mp4>   (K = index of a keyframe of the previous render; its time = K/30)
# Use when only the hook changed (titles, positions): ~1 min instead of a full render. Checks the frame count of the result.
set -e
R=/home/claude/reels/$1; K=$2; PREV=$3; cd "$R"
python3 render.py --full --end $K > out/render_hook.log 2>&1 || { echo "RENDER_FAIL"; tail -5 out/render_hook.log; exit 1; }
grep -q "errors: \[\]" out/render_hook.log || { echo "RENDER_ERRORS"; tail -3 out/render_hook.log; }
mv out/video_noaudio.mp4 out/video_hook.mp4
T=$(python3 -c "print(f'{$K/30:.6f}')")
ffmpeg -hide_banner -loglevel error -y -ss $T -i "$PREV" -c copy -avoid_negative_ts make_zero out/video_tail.mp4
printf "file '%s'\nfile '%s'\n" "$R/out/video_hook.mp4" "$R/out/video_tail.mp4" > out/concat.txt
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i out/concat.txt -c copy -movflags +faststart out/video_noaudio.mp4
n() { ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 "$1"; }
echo "PARTIAL_OK head $(n out/video_hook.mp4) + tail $(n out/video_tail.mp4) = $(n out/video_noaudio.mp4) frames, $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video_noaudio.mp4)s"
