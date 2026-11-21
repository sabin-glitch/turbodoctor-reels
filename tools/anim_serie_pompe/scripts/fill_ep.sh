#!/bin/bash
# fill_ep.sh N [parts]  -> randeaza doar cadrele care lipsesc din out/epN/frames_base (fara foaia de validare); scrie numarul lor in logs/r_epN.done
N=${1:?}; P=${2:-4}; W=/home/claude/w/serpmp; cd $W || exit 1
rm -f "$W/logs/r_ep${N:?}.done"; mkdir -p out/ep$N/frames_base
for ((i=0; i<P; i++)); do python3 icomp.py ep$N --out out/ep$N/frames_base --part $i $P > logs/r_ep${N}_$i.log 2>&1 & done
wait; ls out/ep$N/frames_base | grep -c "^[0-9]*\.jpg$" > logs/r_ep$N.done
