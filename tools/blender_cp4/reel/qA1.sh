#!/bin/bash
# bucata A1: prim-planul (camera C) pentru hook si pentru partea cu rotirea tachetului
cd "$(dirname "$0")"
P="venv/bin/python -W ignore reel_scene.py"
run() { local S=$(date +%s); echo "== $* ($(date +%H:%M:%S))"; $P "$@" > out_reel/last.log 2>&1 || { echo "EROARE la: $*"; tail -5 out_reel/last.log; }; echo "   gata in $(( $(date +%s)-S )) s"; }
run plate C HOT 128
run loop C ROT0 R1 0 58 32
run loop C ROT1 R1 51 89 32
run loop C CROSS R1 0 37 32
echo "A1 TERMINAT $(date +%H:%M:%S)"
