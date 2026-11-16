#!/bin/bash
# Mastile de acoperire pentru marcajul din fundal (mask2_list.json -> mask2/), cu randarea Blender pusa pe pauza cat ruleaza
# (Chromium are prioritate si altfel o injumatateste). Blender porneste la loc la iesire.
cd "$(dirname "$0")/../anim"; export NODE_PATH=/opt/node-tools/node_modules
trap 'pkill -CONT -f reel_scene.py' EXIT
pkill -STOP -f reel_scene.py
S=$(date +%s)
node amask.cjs /home/claude/reels/amorsare_filtru/vo/uframes.json ../reelbl/mask2_list.json ../reelbl/mask2 0 2 > ../reelbl/mask_a.log 2>&1 &
node amask.cjs /home/claude/reels/amorsare_filtru/vo/uframes.json ../reelbl/mask2_list.json ../reelbl/mask2 1 2 > ../reelbl/mask_b.log 2>&1 &
wait
echo "masti gata in $(( $(date +%s)-S )) s"; tail -q -n 1 ../reelbl/mask_a.log ../reelbl/mask_b.log
ls ../reelbl/mask2 | wc -l
