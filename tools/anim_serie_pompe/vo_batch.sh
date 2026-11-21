#!/bin/bash
# usage: vo_batch.sh N...  -> pull.sh, then for each episode: vo.sh (assembly) and the Whisper cross-check; log in logs/vob_<first>.out
cd /home/claude/w/serpmp
O=logs/vob_$1.out; : > $O
./pull.sh "$@" >> $O 2>&1 || { echo PULL_FAIL >> $O; exit 1; }
for N in "$@"; do
  nice -n 8 ./vo.sh $N > logs/vo$N.out 2>&1; echo "ep$N vo rc=$?" >> $O; tail -n 3 logs/vo$N.out >> $O
  nice -n 8 bash run_iso.sh wchk.py ep$N > logs/wchk$N.out 2>&1; echo "ep$N wchk rc=$?" >> $O; grep -i "differ\|DIFF\|!!\|slip\|bad" logs/wchk$N.out | head -n 30 >> $O
done
echo VOB_DONE >> $O
