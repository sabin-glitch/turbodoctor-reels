#!/bin/bash
# Stabilize + upscale to 1080x1920 -> src/stab.mp4. Input: src/clean.mp4 (watermark removed) if present, else src/cfr.mp4.
# Run ONE instance only (it writes out/transforms.trf). Takes ~8-10 min for 100 s on 2 CPUs: run in background.
cd "$(dirname "$0")"; IN=src/cfr.mp4; [ -f src/clean.mp4 ] && IN=src/clean.mp4
UP="scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0"
if ffmpeg -hide_banner -filters 2>/dev/null | grep -q vidstabdetect; then
  ffmpeg -hide_banner -loglevel error -y -i $IN -vf "vidstabdetect=shakiness=6:accuracy=15:result=out/transforms.trf" -f null - && \
  ffmpeg -hide_banner -loglevel error -y -i $IN -vf "vidstabtransform=input=out/transforms.trf:smoothing=12:optzoom=1:interpol=bicubic,$UP" -c:v libx264 -preset medium -crf 14 -pix_fmt yuv420p -an src/stab.mp4
else
  ffmpeg -hide_banner -loglevel error -y -i $IN -vf "$UP" -c:v libx264 -preset medium -crf 14 -pix_fmt yuv420p -an src/stab.mp4
fi && echo STAB_OK
