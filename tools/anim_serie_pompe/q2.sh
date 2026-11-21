#!/bin/bash
# coada 2: filtrul, atelierul, modulul din rezervor, injectorul (placi fixe)
cd /home/claude/w/serpmp
venv_bpy/bin/python pplate.py fl:fempty fl:ffull wm:wk wm:wkdam wb:wk wi:wk wu:wk wu:wkup tm:tmfuel tm:tmdry ij:inj 2>&1 | grep --line-buffered "PLATE\|DONE\|Error\|Traceback\|lipseste" >> logs/q2.log
echo Q2_DONE >> logs/q2.log
