#!/bin/bash
# finish_ep.sh N  -> reelul final in /home/claude/deliver si in /mnt/project-files/animatii/ (+ coperta, + textul postarii)
N=${1:?}; NN=$(printf %02d $N); SLUG=serie_pmp_$NN; H=/home/claude/w/serpmp
NAME=$(cd $H && python3 -c "import pdata_eps as P; print(P.EP[$N-1]['fisier'])") || exit 1
bash $H/scripts/setup_reel.sh $N > $H/logs/setup_ep$N.log 2>&1 || { echo "SETUP_FAIL $N"; exit 1; }
cd /home/claude/reels/$SLUG && python3 render.py --prep > out/prep.log 2>&1 || { echo "PREP_FAIL $N"; exit 1; }
FN=Reel_Serie_Pompe_${NN}_${NAME}
bash finish.sh $SLUG $FN || { echo "FINISH_FAIL $N"; exit 1; }
D=/mnt/project-files/animatii/
cp /home/claude/deliver/TurboDoctor_${FN}.mp4 /home/claude/deliver/TurboDoctor_${FN}_coperta.jpg $D || { echo "COPY_FAIL $N"; exit 1; }
[ -f $H/post/ep$N.txt ] && cp $H/post/ep$N.txt ${D}TurboDoctor_${FN}_text_postare.txt
echo "DELIVERED $N $FN"
