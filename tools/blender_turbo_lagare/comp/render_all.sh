#!/bin/bash
# Composite the 8 films (A/B x 9:16/16:9 x with texts / clean), two at a time, then the stills.
cd "$(dirname "$0")"
mkdir -p final stills
run() {  # VAR FMT CLEAN name
  local f="final/$4.mp4"
  [ -s "$f" ] && { echo "skip $f"; return; }
  CLEAN=$3 FMT=$2 VAR=$1 python3 comp.py --out "$f.tmp.mp4" 2>&1 | grep -v Fontconfig
  mv "$f.tmp.mp4" "$f" && echo "DONE $f $(du -h "$f" | cut -f1)"
}
run A V 0 TurboDoctor_Turbina_Lagare_Flotante_9x16 &
run A H 0 TurboDoctor_Turbina_Lagare_Flotante_16x9 & wait
for f in trB_oil_feed trB_oil_outer trB_oil_inner trB_oil_holes trP_oil_outer trP_oil_inner; do
  while [ ! -s ../out/$f.png ]; do sleep 20; done
done
sleep 5
run B V 0 TurboDoctor_Turbina_Lagar_Fix_9x16 &
run B H 0 TurboDoctor_Turbina_Lagar_Fix_16x9 & wait
run A V 1 TurboDoctor_Turbina_Lagare_Flotante_curat_9x16 &
run A H 1 TurboDoctor_Turbina_Lagare_Flotante_curat_16x9 & wait
run B V 1 TurboDoctor_Turbina_Lagar_Fix_curat_9x16 &
run B H 1 TurboDoctor_Turbina_Lagar_Fix_curat_16x9 & wait
for v in A B; do for f in V H; do CLEAN=1 FMT=$f VAR=$v python3 comp.py --stills 2>&1 | grep -v Fontconfig; done; done
echo ALLDONE
