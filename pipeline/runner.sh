#!/bin/bash
# Serial job queue: runs /home/claude/queue/todo/*.job in name order, one at a time, until a STOP file appears.
# Background commands are killed after 2 h, so the runner stops taking new jobs after ROTATE_S (default 85 min) and exits;
# start it again (run_in_background) when it reports RUNNER_ROTATE. Put transcriptions in the same queue as renders:
# two Whisper/Parakeet runs (or one + a render) at the same time can exceed the 8 GB memory limit (OOM kill).
ROTATE_S=${ROTATE_S:-5100}; T0=$(date +%s)
mkdir -p /home/claude/queue/todo /home/claude/queue/done
while [ ! -f /home/claude/queue/STOP ]; do
  [ $(( $(date +%s) - T0 )) -gt $ROTATE_S ] && { echo "$(date +%H:%M:%S) RUNNER_ROTATE"; exit 0; }
  j=$(ls /home/claude/queue/todo/*.job 2>/dev/null | head -1)
  if [ -z "$j" ]; then sleep 5; continue; fi
  mv "$j" /home/claude/queue/running.job
  echo "$(date +%H:%M:%S) START $(basename $j)"
  bash /home/claude/queue/running.job 2>&1 | tail -3
  echo "$(date +%H:%M:%S) END $(basename $j)"
  mv /home/claude/queue/running.job /home/claude/queue/done/$(basename $j)
done
