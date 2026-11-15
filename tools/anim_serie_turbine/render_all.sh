#!/bin/bash
# renders every episode's frames (resumable): 4 interleaved processes per episode
cd "$(dirname "$0")"
for n in ${EPS:-1 2 3 4}; do
  NF=$(python3 -c "import json;print(int(json.load(open('ep$n/vo/cues.json'))['end']*30)+1)")
  for k in 0 1 2 3; do node render_frames.js ep$n /home/claude/w/serie/frames/ep$n $k $NF 4 > log_ep${n}_$k.txt 2>&1 & done
  wait
  echo "EP$n DONE $(ls /home/claude/w/serie/frames/ep$n | wc -l)/$((NF+1))" >> render_status.txt
done
