#!/bin/bash
# usage: vo.sh N [tail-lines]  -> assembles the voice track of episode N from ep<N>/vo_in (make_vo.py lines), log in ep<N>/vo.log
N=$1; W=/home/claude/w/serpmp; E=$W/ep$N
cp $W/{make_vo.py,vo_qc.py,asr2.py,run_iso.sh} $E/
cd $E && bash run_iso.sh make_vo.py lines vo_in > vo.log 2>&1; echo "ep$N rc=$?"; tail -${2:-25} vo.log
