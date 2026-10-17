#!/bin/bash
# Publish an approved reel so Metricool can fetch it: ./publish_media.sh <final.mp4> <yyyy-mm-dd_slug>
# Re-encodes to <= ~95 MB if needed (GitHub hard limit is 100 MB/file), force-pushes a one-file orphan commit to the
# `media` branch and prints the public raw URL. Older media files leave the branch head - fine, because Metricool copies
# the video to its own storage when the post is created. So: publish -> schedule, one video at a time.
set -e
IN=$1; SLUG=$2; [ -f "$IN" ] && [ -n "$SLUG" ] || { echo "usage: $0 <video.mp4> <yyyy-mm-dd_slug>"; exit 1; }
REPO=${TD_REPO:-https://github.com/sabin-glitch/turbodoctor-reels}
W=$(mktemp -d); OUT="$W/$SLUG.mp4"
SIZE=$(stat -c %s "$IN")
if [ "$SIZE" -gt 95000000 ]; then
  ffmpeg -hide_banner -loglevel error -y -i "$IN" -c:v libx264 -preset medium -crf 21 -maxrate 5M -bufsize 10M -pix_fmt yuv420p -profile:v high -c:a aac -b:a 160k -movflags +faststart "$OUT"
else cp "$IN" "$OUT"; fi
[ "$(stat -c %s "$OUT")" -lt 99000000 ] || { echo "still >= 99 MB, lower the bitrate"; exit 1; }
cd "$W" && git init -q && git checkout -q --orphan media && git add "$SLUG.mp4" && \
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "media: $SLUG" && \
git push -q -f "$REPO" media
URL="https://raw.githubusercontent.com/${REPO#https://github.com/}/media/$SLUG.mp4"
code=$(curl -s -o /dev/null -w '%{http_code}' -I -L "$URL"); echo "HTTP $code  $URL"
