#!/bin/bash
# Dupa ce randarile Blender sunt gata: compune cadrele cu pompa, trece compozitorul peste hook si peste partea cu pompa, lipeste si codeaza reelul.
#   endgame.sh [Nume_Fisier]
S="$(cd "$(dirname "$0")" && pwd)"; cd "$S"; T0=$(date +%s)
./assemble.sh bl || { echo "ASSEMBLE_FAIL"; exit 1; }
echo "compunere: $(( $(date +%s)-T0 )) s"
python3 render_seg.py 0 174 > seg_A.log 2>&1 &
sleep 8; WRITE_DATA=0 python3 render_seg.py 2180 3039 > seg_C.log 2>&1 &
wait; tail -q -n 1 seg_A.log seg_C.log
echo "compozitor: $(( $(date +%s)-T0 )) s"
./finish_bl.sh "${1:-Reel_Amorsare_Filtru_Motorina_Blender}"
echo "total: $(( $(date +%s)-T0 )) s"
