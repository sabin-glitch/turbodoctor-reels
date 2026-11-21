#!/bin/bash
# render_ep.sh N [parts] [fresh]  -> valideaza povestea (o foaie cu un cadru mic la fiecare 0,2 s), apoi randeaza cadrele in out/epN/frames_base (reia ce lipseste)
N=${1:?}; P=${2:-3}; W=/home/claude/w/serpmp; cd $W || exit 1
V=/tmp/claude-0/-home-claude/a3683645-8faf-50c2-b360-38bf0dd6a2fe/scratchpad/val; mkdir -p $V
rm -f "$W/logs/r_ep${N:?}.done"
TS=$(python3 -c "import json;T=json.load(open('ep$N/vo/timeline.json'))['total'];print(' '.join('%.2f'%(i*0.2) for i in range(int(T/0.2))))")
python3 icomp.py ep$N --t $TS --sheet 30 --scale 0.12 --out $V/v$N.jpg > logs/val_ep$N.log 2>&1 || { echo "VALIDATE_FAIL $N" > logs/r_ep$N.done; exit 1; }
[ "$3" = "fresh" ] && rm -rf "$W/out/ep${N:?}/frames_base"
mkdir -p out/ep$N/frames_base
for ((i=0; i<P; i++)); do python3 icomp.py ep$N --out out/ep$N/frames_base --part $i $P > logs/r_ep${N}_$i.log 2>&1 & done
wait; ls out/ep$N/frames_base | grep -c "^[0-9]*\.jpg$" > logs/r_ep$N.done
