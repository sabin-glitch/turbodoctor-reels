#!/bin/bash
# batch.sh P N1 N2 ...  -> make_ep.sh pentru fiecare episod, pe rand (P procese de randare); rezumat in logs/batch_<N1>.log
P=${1:?}; shift; W=/home/claude/w/serpmp; cd $W || exit 1; F=logs/batch_$1.log; : > $F
for N in "$@"; do bash scripts/make_ep.sh $N $P validate >> $F 2>&1; done
echo BATCH_DONE >> $F; cat $F
