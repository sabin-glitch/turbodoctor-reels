#!/bin/bash
# Animated narrator reel: full composite + SFX tweak + audio (narrator, music, sound bed) + mux + cover + sync check.
# Same steps as pipeline/finish.sh, with tweak_sfx.py between the render (which writes out/sfx.json) and audio.py.
R=/home/claude/reels/piezo_vs_magnetic; NAME=${1:-Reel_Injector_Piezo_vs_Magnetic}; cd "$R" || exit 1
python3 render.py --prep --full > out/render.log 2>&1 || { echo "RENDER_FAIL"; exit 1; }
python3 tweak_sfx.py >> out/render.log 2>&1 || { echo "SFX_FAIL"; exit 1; }
python3 audio.py > out/audio.log 2>&1 || { echo "AUDIO_FAIL"; exit 1; }
mkdir -p /home/claude/deliver
OUT=/home/claude/deliver/TurboDoctor_${NAME}.mp4; TMP=/home/claude/deliver/TurboDoctor_${NAME}_tmp.mp4
ffmpeg -hide_banner -loglevel error -y -i out/video_noaudio.mp4 -i audio/mix_final.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$TMP" && mv "$TMP" "$OUT" || { echo "MUX_FAIL"; exit 1; }
CT=$(python3 -c "import json,os;print(json.load(open('out/cover_t.json'))['t'] if os.path.exists('out/cover_t.json') else 1.2)")
ffmpeg -hide_banner -loglevel error -y -ss $CT -i "$OUT" -frames:v 1 -q:v 2 /home/claude/deliver/TurboDoctor_${NAME}_coperta.jpg
python3 verify_sync.py 0-6,17-34,46-63,68-84 > out/verify.log 2>&1
echo "FINISH_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s $(du -h "$OUT" | cut -f1)"
