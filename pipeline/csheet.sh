#!/bin/bash
# csheet.sh <video> <out.jpg> <step_s> [start] [dur]  -> tiles 180x320 with timestamps, 8 per row (single ffmpeg pass)
V=$1; O=$2; S=$3; SS=${4:-0}; D=${5:-999}
ffmpeg -hide_banner -loglevel error -y -ss $SS -t $D -i "$V" -vf "fps=1/$S,scale=180:320,drawtext=fontfile=/home/claude/turbodoctor-reels/assets/fonts/Montserrat_900Black.ttf:text='%{eif\:t+$SS\:d}':x=6:y=6:fontsize=26:fontcolor=yellow:borderw=3,tile=8x6" -frames:v 1 -q:v 3 "$O"
