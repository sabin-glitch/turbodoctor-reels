#!/bin/bash
# montage of each episode as soon as its frames are complete (EPn DONE in anim/render_status.txt); episodes given as arguments
cd /home/claude/w/serie
declare -A NM=([5]=Reel_Serie_Turbine_05_Corpuri_Straine_Admisie [6]=Reel_Serie_Turbine_06_Corpuri_Straine_Evacuare [7]=Reel_Serie_Turbine_07_Temperatura_Gazelor [8]=Reel_Serie_Turbine_08_Supraturarea [9]=Reel_Serie_Turbine_09_Geometria_Blocata [10]=Reel_Serie_Turbine_10_DPF_Infundat [11]=Reel_Serie_Turbine_11_Scapari_Infundari [12]=Reel_Serie_Turbine_12_Greseli_Montaj [13]=Reel_Serie_Turbine_13_Uzura_Motorului)
for n in "$@"; do
  until grep -q "EP$n DONE" anim/render_status.txt 2>/dev/null; do sleep 20; done
  S=$(python3 -c "import json;print(json.load(open('slugs.json'))['$n'])")
  (cd /home/claude/reels/$S && python3 render.py --prep > out/prep.log 2>&1)
  bash /home/claude/reels/$S/finish.sh $S ${NM[$n]} >> finish5_status.txt 2>&1
  echo "FIN$n $(date -u +%H:%M)" >> finish5_status.txt
done
