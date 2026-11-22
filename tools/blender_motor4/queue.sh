#!/bin/bash
# render queue: waits for a running render of the overview, then renders the detail shots (each skips existing frames)
# usage: VBPY=/path/to/vbpy/bin/python ./queue.sh [shot ...]
cd "$(dirname "$0")"
PY=${VBPY:-/home/claude/vbpy/bin/python}
SHOTS=${@:-D_cilindru E_supape B_pompa_inalta C_pompa_ulei}
while pgrep -f "render.py A_motor" > /dev/null; do sleep 10; done
for s in $SHOTS; do
  $PY render.py $s 0 999 100 8 >> out/log_$s.txt 2>&1
done
echo QUEUE_DONE >> out/log_queue.txt
