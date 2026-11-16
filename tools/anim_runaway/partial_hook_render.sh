#!/bin/bash
# Hook v7: se schimbă doar titlurile din primele secunde, deci randez doar cadrele 0..308 (până la cadrul-cheie de la 10,3 s al randării v6)
# și le lipesc, fără recodare, de restul randării v6 (identic). Verifică numărul de cadre și îmbinarea.
set -e
R=/home/claude/reels/runaway_diesel; V6=/tmp/v6_reel/video_noaudio_v6.mp4; K=309
cd "$R"
python3 render.py --prep --full --end $K > out/render_hook.log 2>&1 || { echo "RENDER_FAIL"; tail -5 out/render_hook.log; exit 1; }
grep -q "errors: \[\]" out/render_hook.log || { echo "RENDER_ERRORS"; tail -3 out/render_hook.log; }
mv out/video_noaudio.mp4 out/video_hook.mp4
[ -f out/video_tail_v6.mp4 ] || ffmpeg -hide_banner -loglevel error -y -ss 10.3 -i "$V6" -c copy -avoid_negative_ts make_zero out/video_tail_v6.mp4
printf "file '%s'\nfile '%s'\n" "$R/out/video_hook.mp4" "$R/out/video_tail_v6.mp4" > out/concat.txt
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i out/concat.txt -c copy -movflags +faststart out/video_noaudio.mp4
NH=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 out/video_hook.mp4)
NT=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 out/video_tail_v6.mp4)
NA=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 out/video_noaudio.mp4)
echo "PARTIAL_OK hook $NH + tail $NT = $NA frames, dur $(ffprobe -v error -show_entries format=duration -of csv=p=0 out/video_noaudio.mp4)"
