#!/bin/bash
# Asteapta sa se termine a doua coada de randare Blender, apoi face montajul final (endgame.sh).
S="$(cd "$(dirname "$0")" && pwd)"; cd "$S"; LOG=../bl/out_reel/qA2.log
while pgrep -f 'qA2\.sh' > /dev/null; do sleep 5; done
echo "coada A2 s-a oprit la $(date -u +%H:%M:%S)"; cat $LOG
grep -q "A2 TERMINAT" $LOG || { echo "A2 NU S-A TERMINAT (oprita?)"; exit 2; }
if grep -q "EROARE" $LOG; then echo "A2 ARE ERORI"; exit 3; fi
./endgame.sh "$@"
