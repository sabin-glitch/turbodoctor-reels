#!/bin/bash
# bucata A2: planul larg (camera W), pana arborelui si bucla incinsa din prim-plan.
# Planul larg vine primul, ca montajul lui sa poata fi verificat cat se randeaza restul. Daca A1 inca ruleaza, asteapta sa termine.
cd "$(dirname "$0")"
while pgrep -f qA1.sh > /dev/null; do sleep 5; done
P="venv/bin/python -W ignore reel_scene.py"
run() { local S=$(date +%s); echo "== $* ($(date +%H:%M:%S))"; $P "$@" > out_reel/last2.log 2>&1 || { echo "EROARE la: $*"; tail -5 out_reel/last2.log; }; echo "   gata in $(( $(date +%s)-S )) s"; }
run plate W FUEL 64
run loop W FUEL R1 0 37 32
run loop W HOT R2 0 75 20
run plate W AIR 64
run plate W HOT 64
run loop W AIR R1 0 37 32
run loop W HOT R1 0 37 32
run loop C HOT R2 0 75 20
run loop C HOT R1 0 37 32
echo "A2 TERMINAT $(date +%H:%M:%S)"
