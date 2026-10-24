#!/bin/bash
# Create a working folder for one reel: ./new_reel.sh <name> <source video>
# -> /home/claude/reels/<name> with scripts, compositor template, assets, 30 fps source, audio tracks, contact sheet.
set -e
NAME=$1; SRC=$2; [ -n "$NAME" ] && [ -f "$SRC" ] || { echo "usage: $0 <name> <video>"; exit 1; }
HERE=$(cd "$(dirname "$0")" && pwd); R=/home/claude/reels/$NAME
mkdir -p "$R"/{src,frames,frames_base,audio,out,preview,assets}
cp "$HERE"/pipeline/*.py "$HERE"/pipeline/*.sh "$HERE"/pipeline/art.js "$HERE"/pipeline/schem.js "$HERE"/pipeline/intro.js "$R"/
[ -f "$R/reel.js" ] || cp "$HERE/pipeline/reel_example.js" "$R/reel.js"
[ -f "$R/compositor.html" ] || cp "$HERE/pipeline/compositor_template.html" "$R/compositor.html"
cp "$HERE/pipeline/map.json" "$R/out/map.json"; cp -r "$HERE"/assets/* "$R/assets/"
# HDR phone clips (HLG/PQ) are tone-mapped to SDR BT.709 - a raw conversion looks pale and over-lit (rejected by Sabin, 24.10.2026)
TRC=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$SRC" | head -1); TRC=${TRC%%,*}  # side data adds a trailing comma
case "$TRC" in arib-std-b67|smpte2084) TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p," ;; *) TM="" ;; esac
ffmpeg -hide_banner -loglevel error -y -i "$SRC" -vf "fps=30,${TM}format=yuv420p" -c:v libx264 -preset veryfast -crf 10 -pix_fmt yuv420p -c:a aac -b:a 256k "$R/src/cfr.mp4"
ffmpeg -hide_banner -loglevel error -y -i "$R/src/cfr.mp4" -vn -ac 1 -ar 16000 "$R/audio/voice16k.wav"
ffmpeg -hide_banner -loglevel error -y -i "$R/src/cfr.mp4" -vn -ac 1 -ar 48000 "$R/audio/src48.wav"
python3 "$R/contact.py" "$R/src/cfr.mp4" "$R/frames/contact.jpg" 3
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of compact "$R/src/cfr.mp4"
echo "reel folder: $R"
