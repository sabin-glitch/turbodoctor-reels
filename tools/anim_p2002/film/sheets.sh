#!/bin/bash
# planse de contact din filmul codat: ./sheets.sh film.mp4 [pas_secunde] -> sc/final_XX.jpg (8 x 3 cadre pe plansa)
f=${1:-film.mp4}; step=${2:-1.5}
rm -f sc/final_*.jpg
ffmpeg -y -loglevel error -i "$f" -vf "fps=1/$step:start_time=0:round=down,scale=360:640,drawtext=text='%{pts\:hms}':x=8:y=h-22:fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6,tile=8x3" -q:v 3 sc/final_%02d.jpg
ls sc/final_*.jpg
