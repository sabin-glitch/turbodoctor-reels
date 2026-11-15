#!/bin/bash
# renders the episodes listed in render_queue.txt, one after another, as they are added (a line END stops it)
cd /home/claude/w/serie/anim
i=0
while true; do
  mapfile -t Q < render_queue.txt
  if (( ${#Q[@]} > i )); then n=${Q[$i]}; [ "$n" = END ] && break
    while pgrep -f render_frames.js >/dev/null; do sleep 5; done
    EPS="$n" bash render_all.sh; i=$((i+1))
  else sleep 10; fi
done
