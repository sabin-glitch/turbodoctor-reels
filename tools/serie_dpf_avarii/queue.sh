#!/bin/bash
cd "$(dirname "$0")"
for N in "$@"; do T=$(printf "ep%02d" $N); ls final/TurboDoctor_DPF_avarii_${T}_*.mp4 >/dev/null 2>&1 && continue; ./render_ep.sh $N >> queue.log 2>&1 < /dev/null; done
echo ALLDONE >> queue.log
