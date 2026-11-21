#!/bin/bash
# bq.sh -> coada Blender: ruleaza pe rand liniile din logs/bq.list (argumente pentru pplate.py); liniile facute se trec in logs/bq.done
cd /home/claude/w/serpmp
touch logs/bq.done logs/bq.list
while true; do
  L=$(grep -vxFf logs/bq.done logs/bq.list 2>/dev/null | head -1)
  [ -z "$L" ] && break
  echo "BQ_START $(date -u +%H:%M:%S) $L"
  nice -n 10 venv_bpy/bin/python pplate.py $L 2>&1 | grep -E "PLATE|LOOP|Error|Traceback|error" | grep -v CUEW | cut -c1-300
  echo "$L" >> logs/bq.done
  echo "BQ_END $(date -u +%H:%M:%S) $L"
done
echo BQ_EMPTY
