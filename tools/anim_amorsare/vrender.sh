#!/bin/bash
# 4 procese intercalate, cu reluare
cd "$(dirname "$0")"; N=${N:-4}
run(){ for try in 1 2 3 4 5 6; do node vframes.cjs $1 $N >> vlog$1.txt 2>&1 && break; sleep 3; done; }
for ((k=0;k<N;k++)); do run $k & done; wait
echo "RENDER_DONE $(ls $OUT | grep -c 'jpg$')"
