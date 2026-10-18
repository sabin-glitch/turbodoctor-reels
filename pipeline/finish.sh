#!/bin/bash
# Full render + audio + mux + cover + sync check for one reel (v2): finish.sh <slug> <Nume_Fisier>
# -> /home/claude/deliver/TurboDoctor_<Nume_Fisier>.mp4 + _coperta.jpg. Long job: run it in the background.
R=/home/claude/reels/$1; NAME=$2; cd "$R" || exit 1
python3 render.py --full > out/render.log 2>&1 || { echo "RENDER_FAIL $1"; exit 1; }
python3 audio.py > out/audio.log 2>&1 || { echo "AUDIO_FAIL $1"; exit 1; }
mkdir -p /home/claude/deliver
OUT=/home/claude/deliver/TurboDoctor_${NAME}.mp4
ffmpeg -hide_banner -loglevel error -y -i out/video_noaudio.mp4 -i audio/mix_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT" || { echo "MUX_FAIL $1"; exit 1; }
SZ=$(stat -c %s "$OUT"); if [ $SZ -gt 85000000 ]; then ffmpeg -hide_banner -loglevel error -y -i "$OUT" -c:v libx264 -preset medium -crf 20 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a copy -movflags +faststart "${OUT%.mp4}_tmp.mp4" && mv "${OUT%.mp4}_tmp.mp4" "$OUT"; fi
CT=$(python3 -c "import json,os;print(json.load(open('out/cover_t.json'))['t'] if os.path.exists('out/cover_t.json') else 1.2)")
ffmpeg -hide_banner -loglevel error -y -ss $CT -i "$OUT" -frames:v 1 -q:v 2 /home/claude/deliver/TurboDoctor_${NAME}_coperta.jpg
python3 verify_sync.py > out/verify.log 2>&1
echo "FINISH_OK $1 $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s $(du -h "$OUT" | cut -f1)"
