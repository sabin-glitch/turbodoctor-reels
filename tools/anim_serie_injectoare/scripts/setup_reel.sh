#!/bin/bash
# setup_reel.sh N  -> /home/claude/reels/serie_inj_NN gata de randare (vocea si momentele din epN/vo; cadrele in out/epN/frames_base)
N=$1; NN=$(printf %02d $N); SLUG=serie_inj_$NN; E=/home/claude/w/serinj/ep$N/vo
S=/tmp/claude-0/-home-claude/77ff75bb-68c8-5682-967c-243fa44cac4d/scratchpad; mkdir -p $S
TOT=$(python3 -c "import json;print(json.load(open('$E/timeline.json'))['total'])")
NOUT=$(python3 -c "print(round($TOT*30))")
rm -rf /home/claude/reels/$SLUG
cd /home/claude/turbodoctor-reels && ffmpeg -hide_banner -loglevel error -y -f lavfi -i color=c=black:s=1080x1920:r=30 -f lavfi -i anullsrc=r=48000:cl=mono -t $TOT -c:v libx264 -preset ultrafast -crf 30 -c:a aac -shortest $S/black_$N.mp4 || exit 1
bash new_reel.sh $SLUG $S/black_$N.mp4 2>&1 | tail -1
cd /home/claude/reels/$SLUG || exit 1
cp $E/vo_track.wav audio/vo_track.wav && cp $E/timeline.json out/timeline.json
echo '{"narrator": true, "orig_gain": 0, "music": false, "sfx": false}' > out/v2.json
python3 retime.py > /dev/null
echo "{\"n_out\": $NOUT}" > out/frames_meta.json
rmdir frames_base 2>/dev/null; rm -f frames_base; mkdir -p /home/claude/w/serinj/out/ep$N/frames_base
ln -s /home/claude/w/serinj/out/ep$N/frames_base frames_base
python3 /home/claude/w/serinj/scripts/mk_reeljs.py $N /home/claude/reels/$SLUG
echo "SETUP_OK $SLUG total=$TOT n_out=$NOUT"
