#!/bin/bash
# make_ep.sh N [parts] [validate]  -> cadrele care lipsesc, apoi montajul, copiile in /mnt/project-files/animatii/ si verificarea finala; jurnal in logs/make_epN.log
N=${1:?}; P=${2:-4}; W=/home/claude/w/serpmp; cd $W || exit 1
{
  date -u +"start %H:%M:%S"
  if [ "$3" = "validate" ]; then bash scripts/render_ep.sh $N $P; else bash scripts/fill_ep.sh $N $P; fi
  NEED=$(python3 -c "import json;print(round(json.load(open('ep$N/vo/timeline.json'))['total']*30))"); HAVE=$(cat logs/r_ep$N.done)
  echo "frames $HAVE / $NEED"; date -u +"frames %H:%M:%S"
  [ "$HAVE" = "$NEED" ] || { echo "MAKE_FAIL $N frames"; exit 1; }
  bash scripts/finish_ep.sh $N || { echo "MAKE_FAIL $N finish"; exit 1; }
  bash scripts/qc_final.sh $N; date -u +"done %H:%M:%S"; echo "MAKE_OK $N"
} > logs/make_ep$N.log 2>&1
tail -n 4 logs/make_ep$N.log
