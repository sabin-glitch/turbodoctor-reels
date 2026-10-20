#!/bin/bash
# full render (finish.sh) + QA for the given reels, 2 workers in parallel. QA: intro ASR on the final mix, loudness intro vs clip, 12-frame sheet.
H=$(cd "$(dirname "$0")" && pwd)
cd /home/claude/reels
name() { python3 -c "import sys; sys.path.insert(0,'$H'); from hook_specs import SPECS; print(SPECS['$1']['name'])"; }
qa() {
  local r=$1 n=$(name $1); local F=/home/claude/deliver/TurboDoctor_$n.mp4
  local IE=$(python3 -c "import json; print(json.load(open('$r/out/timeline.json'))['intro']['dur'])")
  ffmpeg -hide_banner -loglevel error -y -i $F -t $(python3 -c "print($IE + .6)") -ac 1 -ar 48000 $r/out/qa_intro.wav
  local heard=$(python3 $H/asr.py $r/out/qa_intro.wav 2>&1 | grep "|" | cut -d'|' -f2)
  local li=$(ffmpeg -hide_banner -nostats -t $IE -i $F -af ebur128 -f null - 2>&1 | grep -A1 "Integrated" | grep "I:" | awk '{print $2}')
  local ls=$(ffmpeg -hide_banner -nostats -ss $(python3 -c "print($IE + .5)") -i $F -af ebur128 -f null - 2>&1 | grep -A1 "Integrated" | grep "I:" | awk '{print $2}')
  (cd $r && python3 qsheet.py $F preview/q.jpg 12 > /dev/null 2>&1)
  echo "QA $r dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F | cut -c1-5)s intro=${IE}s LUFS intro/clip=$li/$ls heard:$heard"
}
work() { for r in "$@"; do bash $r/finish.sh $r $(name $r) | tail -n 1; qa $r; done; }
L=(${@})
A=(); B=(); for ((i = 0; i < ${#L[@]}; i++)); do if ((i % 2)); then B+=(${L[i]}); else A+=(${L[i]}); fi; done
work "${A[@]}" & work "${B[@]}" & wait
echo ALL_RENDERS_DONE
