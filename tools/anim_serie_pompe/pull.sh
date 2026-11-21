#!/bin/bash
# usage: pull.sh [ep...] -> takes the packs (sppk<asset>.mp4) from branch `sources` and splits them into ep<N>/vo_in (unpack.py);
# for the episodes named, adds the shared rows (s1, o1..o3) recorded for the earlier series. Each vo_in holds downloaded audio only.
W=/home/claude/w/serpmp; R=/home/claude/turbodoctor-reels
cd $R && git fetch -q --depth 1 --filter=blob:none origin sources || exit 1
cd $W && python3 -I $W/unpack.py || exit 1
cd $R
for N in "$@"; do
  D=$W/ep$N/vo_in; mkdir -p $D
  K=$(python3 -c "import json;print(len(json.load(open('$W/ep$N/vo_script.json'))))")
  git show FETCH_HEAD:sdt2_s1_b.mp4 > $D/p${N}_L01a.mp3
  for i in 1 2 3; do printf -v L "%02d" $((K-4+i)); git show FETCH_HEAD:sdt2_o${i}_a.mp4 > $D/p${N}_L${L}a.mp3; done
  echo "ep$N: $(ls $D | wc -l) files for $K rows"
done
