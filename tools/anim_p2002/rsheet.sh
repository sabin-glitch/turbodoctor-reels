#!/bin/bash
# foaie de proba cu textele de pe ecran: rsheet.sh <iesire.jpg> <t1> <t2> ...
cd /home/claude/dpf/work || exit 1
out=$1; shift
ts=$(echo "$@" | tr ' ' ',')
../venv2/bin/python reel_story.py > /dev/null && rm -rf hudr_t && node hud_reel_render.js --out hudr_t --t "$ts" > /dev/null && ../venv2/bin/python comp_reel.py --hud hudr_t --guides --sheet 4 --crop 150 1560 --out "$out" --t "$@" 2>&1 | tail -1
