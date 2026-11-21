#!/bin/bash
# setup_reel.sh N  -> /home/claude/reels/serie_pmp_NN gata de randare (vocea si momentele din epN/vo; cadrele in out/epN/frames_base)
N=${1:?}; NN=$(printf %02d $N); SLUG=serie_pmp_$NN; W=/home/claude/w/serpmp; E=$W/ep$N/vo
S=/tmp/claude-0/-home-claude/a3683645-8faf-50c2-b360-38bf0dd6a2fe/scratchpad; mkdir -p $S
TOT=$(python3 -c "import json;print(json.load(open('$E/timeline.json'))['total'])")
NOUT=$(python3 -c "print(round($TOT*30))")
rm -rf "/home/claude/reels/serie_pmp_${NN:?}"
cd /home/claude/turbodoctor-reels && ffmpeg -hide_banner -loglevel error -y -f lavfi -i color=c=black:s=1080x1920:r=30 -f lavfi -i anullsrc=r=48000:cl=mono -t $TOT -c:v libx264 -preset ultrafast -crf 30 -c:a aac -shortest $S/black_pmp_$N.mp4 || exit 1
bash new_reel.sh $SLUG $S/black_pmp_$N.mp4 2>&1 | tail -1
cd /home/claude/reels/$SLUG || exit 1
cp $E/vo_track.wav audio/vo_track.wav && cp $E/timeline.json out/timeline.json || exit 1
echo '{"narrator": true, "orig_gain": 0, "music": false, "sfx": false}' > out/v2.json
python3 retime.py > /dev/null || exit 1
echo "{\"n_out\": $NOUT}" > out/frames_meta.json
rmdir frames_base 2>/dev/null; mkdir -p $W/out/ep$N/frames_base
ln -sfn $W/out/ep$N/frames_base frames_base
python3 $W/scripts/mk_reeljs_pmp.py $N /home/claude/reels/$SLUG || exit 1
echo "SETUP_OK $SLUG total=$TOT n_out=$NOUT"
