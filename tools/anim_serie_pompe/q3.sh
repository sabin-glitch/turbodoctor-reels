#!/bin/bash
cd /home/claude/w/serpmp
venv_bpy/bin/python pplate.py pm:dam pm:damf > logs/q3.log 2>&1
echo Q3_DONE >> logs/q3.log
