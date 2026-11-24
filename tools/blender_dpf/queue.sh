#!/bin/bash
# Renders every layer that is not on disk yet (safe to restart): wide plates first, then the masks, then the close-ups.
cd "$(dirname "$0")"
PY=${PY:-/home/claude/venv/bin/python}
for grp in "T1_sec T1_front T1_id" "T2_" "T8_ TA_ TB_"; do
  $PY dpf.py queue $grp 2>&1 | grep --line-buffered "DONE\|rror" >> out/queue.log
done
echo ALLDONE >> out/queue.log
