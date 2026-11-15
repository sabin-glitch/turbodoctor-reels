#!/bin/bash
# Fisierul livrat: lipeste segmentele compozitorului (render_seg.py), pune sunetul NESCHIMBAT al variantei 2 (audio/mix_final.wav),
# codeaza o singura data la debitul final, scoate coperta si verifica sincronizarea.
#   finish_bl.sh [Nume_Fisier]  -> /home/claude/deliver/TurboDoctor_<Nume_Fisier>.mp4 + _coperta.jpg
R=/home/claude/reels/amorsare_filtru; NAME=${1:-Reel_Amorsare_Filtru_Motorina_Blender}; cd "$R" || exit 1
: > out/segs.txt
for s in 00000_00174 00174_02180 02180_03039 03039_04348; do
  [ -f out/seg_$s.mp4 ] || { echo "LIPSA segmentul $s"; exit 1; }
  echo "file 'seg_$s.mp4'" >> out/segs.txt
done
mkdir -p /home/claude/deliver; OUT=/home/claude/deliver/TurboDoctor_${NAME}.mp4
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i out/segs.txt -i audio/mix_final.wav -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf ${CRF:-20} -maxrate ${MAXRATE:-4.6M} -bufsize 9.2M -profile:v high -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT" || { echo "ENC_FAIL"; exit 1; }
CT=$(python3 -c "import json,os;print(json.load(open('out/cover_t.json'))['t'] if os.path.exists('out/cover_t.json') else 1.2)")
ffmpeg -hide_banner -loglevel error -y -ss $CT -i "$OUT" -frames:v 1 -q:v 2 /home/claude/deliver/TurboDoctor_${NAME}_coperta.jpg
python3 verify_sync.py > out/verify.log 2>&1
echo "FINISH_OK $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s $(du -h "$OUT" | cut -f1) $(ffprobe -v error -select_streams v -show_entries stream=nb_frames,color_space,color_range -of csv=p=0 "$OUT")"
