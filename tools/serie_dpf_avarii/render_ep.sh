#!/bin/bash
# render_ep.sh N  -> final/TurboDoctor_DPF_avarii_epNN_<nume>.mp4 (imagine în două jumătăți, pe 2 nuclee, apoi vocea)
cd "$(dirname "$0")"; N=$1; T=$(printf "ep%02d" $N); PY=/home/claude/cvenv/bin/python; mkdir -p final seg
NAME=$($PY - <<P
import re, unicodedata, sys
sys.path.insert(0, '.')
from episoade import EP
e = [x for x in EP if x['n'] == $N][0]
s = unicodedata.normalize('NFD', e['nume'].lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
print(re.sub(r'[^a-z0-9]+', '_', s).strip('_'))
P
)
NF=$(EP=$N $PY comp/serie.py --cues 2>/dev/null | awk '{print $3}'); H=$((NF / 2))
$PY vo_ep.py $N || exit 1
EP=$N $PY comp/serie.py --out seg/${T}_a.tmp.mp4 --frames 0 $H 2>seg/${T}_a.log &
EP=$N $PY comp/serie.py --out seg/${T}_b.tmp.mp4 --frames $H $NF 2>seg/${T}_b.log &
wait
printf "file '%s_a.tmp.mp4'\nfile '%s_b.tmp.mp4'\n" $T $T > seg/$T.txt
ffmpeg -y -nostdin -loglevel error -f concat -safe 0 -i seg/$T.txt -i vo/$T/vo_track.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -ar 48000 -shortest -movflags +faststart final/tmp_$T.mp4 && mv final/tmp_$T.mp4 "final/TurboDoctor_DPF_avarii_${T}_${NAME}.mp4" && rm -f seg/${T}_a.tmp.mp4 seg/${T}_b.tmp.mp4
EP=$N $PY comp/serie.py --png 3.4 2>/dev/null; ffmpeg -y -nostdin -loglevel error -i comp/proof/${T}_003.4.png -q:v 3 "final/TurboDoctor_DPF_avarii_${T}_coperta.jpg"
echo "DONE $T $(date +%H:%M:%S)"
