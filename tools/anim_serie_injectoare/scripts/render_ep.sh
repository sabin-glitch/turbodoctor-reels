#!/bin/bash
# render_ep.sh N [parts] [fresh]  -> valideaza povestea (cadre mici la fiecare 0,2 s), apoi randeaza cadrele in out/epN/frames_base (reia ce lipseste)
N=$1; P=${2:-2}; cd /home/claude/w/serinj
V=/tmp/claude-0/-home-claude/77ff75bb-68c8-5682-967c-243fa44cac4d/scratchpad/val$N; rm -rf $V; mkdir -p $V
TS=$(python3 -c "import json;T=json.load(open('ep$N/vo/timeline.json'))['total'];print(' '.join('%.2f'%(i*0.2) for i in range(int(T/0.2))))")
python3 icomp.py ep$N --t $TS --scale 0.12 --out $V/v.jpg > logs/val_ep$N.log 2>&1 || { echo "VALIDATE_FAIL $N" > logs/r_ep$N.done; exit 1; }
rm -rf $V
[ "$3" = "fresh" ] && rm -rf out/ep$N/frames_base
mkdir -p out/ep$N/frames_base; rm -f logs/r_ep$N.done
for ((i=0; i<P; i++)); do python3 icomp.py ep$N --out out/ep$N/frames_base --part $i $P > logs/r_ep${N}_$i.log 2>&1 & done
wait; ls out/ep$N/frames_base | grep -c jpg > logs/r_ep$N.done
