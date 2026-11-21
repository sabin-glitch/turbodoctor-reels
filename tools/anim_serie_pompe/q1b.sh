#!/bin/bash
# coada 1b: buclele de miscare ale pompei (cadrele in miscare la 20 de esantioane)
cd /home/claude/w/serpmp
venv_bpy/bin/python pplate.py pc:dry pc:fuel pw:dry ph:fuel --loop --lspp 20 2>&1 | grep --line-buffered "PLATE\|LOOP\|KEY\|DONE\|Error\|Traceback\|Saved" >> logs/q1b.log
echo Q1B_DONE >> logs/q1b.log
