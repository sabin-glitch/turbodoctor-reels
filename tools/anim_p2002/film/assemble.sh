#!/bin/bash
# Asamblarea finala: cate o bucata de film pentru fiecare plan (imagine + particule + texte), compuse in paralel,
# lipite apoi fara recodare.
#   ./assemble.sh [iesire.mp4] [plan ...]
#     fara planuri: compune tot ce lipseste din seg/ (sterge seg/ ca sa refaci tot)
#     cu planuri (de ex. s13 s14): reface doar acele bucati, apoi lipeste din nou tot filmul
#   N=4 implicit (cate procese in paralel); SKIP="s00 s01" sare peste planuri (de ex. cat inca se randeaza)
cd "$(dirname "$0")"
PY=${PY:-../venv2/bin/python}; N=${N:-4}; OUT=${1:-film.mp4}; shift
mkdir -p seg
for s in "$@"; do rm -f seg/$s.mp4; done
$PY -c "
import story
for s in story.SHOTS: print(s.id, s.t0, s.t1)" > seg/list.txt
todo=""
while read id t0 t1; do
  case " $SKIP " in *" $id "*) continue;; esac
  [ -s seg/$id.mp4 ] || todo="$todo $id:$t0:$t1"
done < seg/list.txt
if [ -n "$todo" ]; then
  echo $todo | tr ' ' '\n' | xargs -P $N -I{} bash -c 'IFS=: read id t0 t1 <<< "{}"; '"$PY"' comp.py --range $t0 $t1 --out seg/$id.tmp.mp4 > seg/$id.log 2>&1 && mv seg/$id.tmp.mp4 seg/$id.mp4; tail -n 1 seg/$id.log | sed "s/^/$id: /"'
fi
rm -f seg/concat.txt; ok=1
while read id t0 t1; do
  [ -s seg/$id.mp4 ] || { echo "lipseste $id"; ok=0; }
  echo "file '$id.mp4'" >> seg/concat.txt
done < seg/list.txt
[ $ok = 1 ] || exit 1
ffmpeg -y -loglevel error -f concat -safe 0 -i seg/concat.txt -c copy -movflags +faststart "$OUT" && \
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames:format=duration,bit_rate,size -of default=nw=1 "$OUT"
