#!/bin/bash
# finisher.sh  -> asteapta cadrele fiecarui episod (logs/r_epN.done) si monteaza reelul, pe rand
cd /home/claude/w/serinj
declare -A NM=([7]=Benzina_Pusa_Din_Greseala [8]=AdBlue_In_Motorina [9]=Motorina_Care_Nu_Unge [10]=Pilitura_De_La_Pompa [11]=Fara_Cod_Si_Standard [12]=Defectele_Electrice [13]=Uzura_Normala)
while pgrep -f "finish_ep.sh 6" > /dev/null; do sleep 15; done
for N in 7 8 9 10 11 12 13; do
  EXP=$(python3 -c "import iser as S; E=S.Ep($N); print(round(E.TOTAL*30))")
  while true; do
    if [ -f logs/r_ep$N.done ]; then
      V=$(cat logs/r_ep$N.done)
      if [ "$V" = "$EXP" ]; then break; fi
      case "$V" in VALIDATE_FAIL*) echo "SKIP $N validate"; continue 2;; esac
    fi
    sleep 20
  done
  bash scripts/finish_ep.sh $N ${NM[$N]} > logs/finish_ep$N.log 2>&1
  echo "ep$N: $(tail -n 1 logs/finish_ep$N.log)"
done
echo ALLDONE
