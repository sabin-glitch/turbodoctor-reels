#!/bin/bash
# probe.sh out.jpg cols t1 t2 ...  : cadre compuse (imagine + texte) la jumatate de rezolutie, intr-o plansa
out=$1; cols=$2; shift 2
cd /home/claude/dpf/work
../venv2/bin/python story.py > /dev/null && node hud_probe.js "$@" && ../venv2/bin/python comp.py --scale 0.5 --t "$@" --sheet $cols --hud hud_t --out $out 2>&1 | grep -v "^t=" ; true
