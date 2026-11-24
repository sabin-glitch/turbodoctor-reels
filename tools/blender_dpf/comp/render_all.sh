#!/bin/bash
# Composite the two films (with texts / clean) in parallel, then the stills. Needs the layers in ../out (python ../dpf.py queue, or tar xf ../layers.tar).
cd "$(dirname "$0")"
PY=${PY:-python3}
mkdir -p final stills
run() {  # CLEAN name
  local f="final/$2.mp4"
  CLEAN=$1 $PY comp.py --out "$f" --jobs 1 2>&1 | grep -v Fontconfig     # chapters are kept in $f.seg/ ; --force n renders one again
  echo "DONE $f $(du -h "$f" | cut -f1)"
}
run 0 TurboDoctor_DPF_Filtru_de_particule_9x16 &
run 1 TurboDoctor_DPF_Filtru_de_particule_curat_9x16 & wait
CLEAN=1 $PY comp.py --stills 2>&1 | grep -v Fontconfig
$PY comp.py --cover final/TurboDoctor_DPF_Filtru_de_particule_coperta.jpg 2>&1 | grep -v Fontconfig
echo ALLDONE
