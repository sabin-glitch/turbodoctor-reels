#!/bin/bash
# finish_ep.sh N Nume  -> reelul de previzualizare (vocea provizorie) in /mnt/project-files/animatii/ (+ coperta, + textul postarii daca exista)
N=$1; NAME=$2; NN=$(printf %02d $N); SLUG=serie_inj_$NN; H=/home/claude/w/serinj
bash $H/scripts/setup_reel.sh $N > $H/logs/setup_ep$N.log 2>&1 || { echo "SETUP_FAIL $N"; exit 1; }
cd /home/claude/reels/$SLUG && python3 render.py --prep > out/prep.log 2>&1 || { echo "PREP_FAIL $N"; exit 1; }
FN=Reel_Serie_Injectoare_${NN}_${NAME}
if [ -f $H/ep$N/vo/PROVIZORIU ]; then FN=${FN}_PREVIZUALIZARE; fi
bash finish.sh $SLUG $FN || { echo "FINISH_FAIL $N"; exit 1; }
D=/mnt/project-files/animatii/
cp /home/claude/deliver/TurboDoctor_${FN}.mp4 /home/claude/deliver/TurboDoctor_${FN}_coperta.jpg $D
[ -f $H/post/ep$N.txt ] && cp $H/post/ep$N.txt ${D}TurboDoctor_${FN}_text_postare.txt
echo "DELIVERED $N $FN"
