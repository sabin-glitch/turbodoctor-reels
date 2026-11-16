#!/bin/bash
# queue_final.sh N1 N2 ...  -> randeaza si monteaza episoadele cu vocea reala, pe rand; randarea episodului urmator merge cat se monteaza cel dinainte
cd /home/claude/w/serinj
declare -A NM=([3]=Depunerile_Din_Interior [4]=Calamina_Din_Gaurile_Duzei [5]=Saiba_De_Etansare [6]=Murdaria_Si_Montajul [7]=Benzina_Pusa_Din_Greseala [8]=AdBlue_In_Motorina [9]=Motorina_Care_Nu_Unge [10]=Pilitura_De_La_Pompa [11]=Fara_Cod_Si_Standard [12]=Defectele_Electrice [13]=Uzura_Normala)
PREV=""
for N in "$@"; do
  until [ -f logs/vo_ok_ep$N ]; do sleep 10; done
  echo "ep$N render start $(date -u +%H:%M)" >> logs/final.log
  bash scripts/render_ep.sh $N 2 fresh
  V=$(cat logs/r_ep$N.done)
  EXP=$(python3 -c "import json;print(round(json.load(open('ep$N/vo/timeline.json'))['total']*30))")
  case "$V" in VALIDATE_FAIL*) echo "ep$N VALIDATE_FAIL" >> logs/final.log; continue;; esac
  [ "$V" = "$EXP" ] || echo "ep$N frames $V != $EXP" >> logs/final.log
  [ -n "$PREV" ] && wait $PREV
  (bash scripts/finish_ep.sh $N ${NM[$N]} > logs/finish_ep$N.log 2>&1; echo "ep$N: $(tail -n 1 logs/finish_ep$N.log) $(date -u +%H:%M)" >> logs/final.log) &
  PREV=$!
done
wait
echo ALLDONE >> logs/final.log
