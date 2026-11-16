#!/bin/bash
# qc_final.sh N  -> durata, sunetul (LUFS, varf) si o foaie de contact (un cadru la 4,5 s) pentru reelul final al episodului N
N=$1; NN=$(printf %02d $N); S=/tmp/claude-0/-home-claude/77ff75bb-68c8-5682-967c-243fa44cac4d/scratchpad
F=$(ls /home/claude/deliver/TurboDoctor_Reel_Serie_Injectoare_${NN}_*.mp4 | grep -v PREVIZUALIZARE | grep -v coperta | head -1)
[ -f "$F" ] || { echo "lipseste ep$N"; exit 1; }
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
V=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$F")
L=$(ffmpeg -hide_banner -nostats -i "$F" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)" | tr -s ' ' | tr '\n' ' ')
echo "ep$N $(basename "$F") | ${D}s | $V | $L"
ffmpeg -hide_banner -loglevel error -y -i "$F" -vf "fps=1/4.5,scale=180:320,tile=6x3:padding=4:color=white" -frames:v 1 -update 1 $S/csf_$NN.jpg
