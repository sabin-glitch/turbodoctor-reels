#!/bin/bash
# runs /home/claude/queue/todo/*.job in name order, one at a time, forever (until STOP file)
while [ ! -f /home/claude/queue/STOP ]; do
  j=$(ls /home/claude/queue/todo/*.job 2>/dev/null | head -1)
  if [ -z "$j" ]; then sleep 5; continue; fi
  mv "$j" /home/claude/queue/running.job
  echo "$(date +%H:%M:%S) START $(basename $j): $(cat /home/claude/queue/running.job)"
  bash /home/claude/queue/running.job 2>&1 | tail -3
  echo "$(date +%H:%M:%S) END $(basename $j)"
  mv /home/claude/queue/running.job /home/claude/queue/done/$(basename $j)
done
