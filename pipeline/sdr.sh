#!/bin/bash
# Normalise one phone clip to 1080x1920 / 30 fps / SDR BT.709: ./sdr.sh <in> <out.mp4>
# iPhone clips are usually HDR (HLG or PQ, BT.2020, Dolby Vision). Converting them without tone mapping gives the pale,
# washed-out "lighting filter" look Sabin rejected on 24.10.2026 - so HDR is always tone-mapped (hable) to BT.709 here.
set -e
IN=$1; OUT=$2
TRC=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$IN" | head -1)
case "$TRC" in
  arib-std-b67|smpte2084) TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p," ;;
  *) TM="" ;;
esac
ffmpeg -hide_banner -loglevel error -y -i "$IN" -map 0:v:0 -map 0:a:0 -vf "fps=30,${TM}scale=1080:1920:flags=lanczos,format=yuv420p,setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709" \
  -c:v libx264 -preset veryfast -crf 12 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 256k -ar 48000 -ac 1 "$OUT"
echo "SDR_OK $(basename "$IN") trc=${TRC:-unknown}${TM:+ (tone-mapped)}"
