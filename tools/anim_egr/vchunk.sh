# vchunk.sh a b : render a chunk, retrying until all its frames exist
cd "$(dirname "$0")"; export HTML=egr-reel.html OUT=/home/claude/reels/egr_admisie_depuneri/frames_base
for try in 1 2 3 4 5 6; do node vframes.js $1 $2 >> vlog_$1.txt 2>&1; miss=0; for ((i=$1;i<$2;i++)); do [ -f $OUT/$(printf %05d $i).jpg ] || miss=$((miss+1)); done; [ $miss = 0 ] && { echo CHUNK_OK $1 $2; exit 0; }; done; echo CHUNK_FAIL $1 $2
