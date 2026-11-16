#!/bin/bash
# Cadrele de baza ale reelului refacut, in /home/claude/reels/amorsare_filtru/frames_base/:
#   assemble.sh rest [n]  -> cadrele care nu se schimba, cu marcajul din fundal (frames_src + mask2 -> frames_wm); se poate rula cat randeaza Blender
#   assemble.sh bl        -> cele 1.033 de cadre cu pompa din Blender (compose.py -> frames_bl)
#   WM=0 assemble.sh ...  -> fara marcaj: cadrele originale neschimbate + pompa din Blender (frames_bl_nowm)
set -e
S="$(cd "$(dirname "$0")" && pwd)"; R=/home/claude/reels/amorsare_filtru; cd "$S"; mkdir -p $R/frames_base
WM=${WM:-1}
if [ "$1" = "rest" ]; then
  if [ "$WM" = "0" ]; then
    python3 -c "
import json, shutil
D = set(r['f'] for r in json.load(open('director.json'))['frames'])
for f in range(4348):
    if f not in D: shutil.copyfile('$R/frames_src/%05d.jpg' % f, '$R/frames_base/%05d.jpg' % f)"
  else
    N=${2:-3}
    for k in $(seq 0 $((N-1))); do python3 wmapply.py director.json $R/frames_src mask2 frames_wm $k $N > wmapply$k.log 2>&1 & done
    wait; tail -q -n 1 wmapply?.log
    cp frames_wm/[0-9]*.jpg $R/frames_base/
  fi
elif [ "$1" = "bl" ]; then
  if [ "$WM" = "0" ]; then BLD=frames_bl_nowm; else BLD=frames_bl; fi
  i=0
  for rg in "0 173" "2180 2466" "2467 2752" "2753 3038"; do WM=$WM python3 compose.py director.json $BLD $rg > compose_$i.log 2>&1 & i=$((i+1)); done
  wait; tail -q -n 1 compose_?.log
  n=$(ls $BLD | grep -c '^[0-9]*\.jpg$'); [ "$n" = "1033" ] || { echo "compose incomplet: $n cadre"; exit 1; }
  cp $BLD/[0-9]*.jpg $R/frames_base/
else echo "assemble.sh rest|bl"; exit 1; fi
echo "frames_base: $(ls $R/frames_base | wc -l) cadre"
