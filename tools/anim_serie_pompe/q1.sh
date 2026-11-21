#!/bin/bash
# coada 1: placile pompei + buclele (sub 2 ore)
cd /home/claude/w/serpmp
venv_bpy/bin/python pplate.py px:full pw:fuel pw:dry pc:fuel pc:dry pc:dam pc:damf ph:fuel pm:fuel pm:dry >> logs/q1.log 2>&1
venv_bpy/bin/python pplate.py pw:fuel pc:dry pc:fuel pw:dry ph:fuel --loop >> logs/q1.log 2>&1
echo Q1_DONE >> logs/q1.log
