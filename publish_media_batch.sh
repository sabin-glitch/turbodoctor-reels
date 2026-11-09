#!/bin/bash
# Publish a batch of approved reels for Metricool: ./publish_media_batch.sh <list.txt> [source_dir]
# list.txt: one line per reel, "n file slug" (n = reel number, file = name inside source_dir, slug = yyyy-mm-dd_name).
# Each file goes to the `media` branch as a NORMAL commit on top of the current branch head (no force push), and the
# printed raw URL is pinned to that commit's SHA, so other chats publishing the same week (with this script or with
# publish_media.sh's force push) cannot break a URL before Metricool copies the video. Used for the 12 injector reels
# (09.11.2026): ~316 MB in ~8 min, run in the background while the posts were being created.
# Output per reel: "#n push_ok=1 HTTP 200 <url>"; the last line is "ALL_PUSHED". Files over 95 MB are re-encoded first.
LIST=$(realpath "$1" 2>/dev/null); SRC=$(realpath "${2:-/home/claude/deliver}" 2>/dev/null)
[ -f "$LIST" ] && [ -d "$SRC" ] || { echo "usage: $0 <list.txt> [source_dir]   (list lines: n file slug)"; exit 1; }
REPO=${TD_REPO:-https://github.com/sabin-glitch/turbodoctor-reels}
BASE=${TD_TMP:-/home/claude}; [ -d "$BASE" ] || BASE=${TMPDIR:-/tmp}
W=$(mktemp -d -p "$BASE")
git clone -q --depth 1 --branch media --single-branch "$REPO" "$W/m" < /dev/null || { echo CLONE_FAIL; exit 1; }
cd "$W/m" || exit 1
while read -r n file slug <&3; do
  [ -z "$n" ] && continue
  IN="$SRC/$file"; [ -f "$IN" ] || { echo "#$n MISSING $IN"; continue; }
  if [ "$(stat -c %s "$IN")" -gt 95000000 ]; then
    ffmpeg -nostdin -hide_banner -loglevel error -y -i "$IN" -c:v libx264 -preset medium -crf 23 -maxrate 3.6M -bufsize 7M \
      -pix_fmt yuv420p -profile:v high -c:a aac -b:a 160k -movflags +faststart "$W/$slug.mp4"
    IN="$W/$slug.mp4"
    [ "$(stat -c %s "$IN")" -lt 99000000 ] || { echo "#$n STILL_TOO_BIG $IN"; continue; }
  fi
  ok=0
  for i in 1 2 3 4 5; do
    if git fetch -q --depth 1 origin media < /dev/null && git checkout -q -B media FETCH_HEAD < /dev/null; then
      cp "$IN" "$slug.mp4" && git add "$slug.mp4" && \
        git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "media: $slug" < /dev/null
      if git push -q origin HEAD:media < /dev/null 2>>"$W/push.err"; then ok=1; break; fi
    fi
    sleep $((2**i))
  done
  SHA=$(git rev-parse HEAD)
  URL="https://raw.githubusercontent.com/${REPO#https://github.com/}/$SHA/$slug.mp4"
  code=$(curl -s -o /dev/null -w '%{http_code}' -I -L "$URL" < /dev/null)
  echo "#$n push_ok=$ok HTTP $code $URL"
done 3< "$LIST"
tail -3 "$W/push.err" 2>/dev/null
cd / && rm -rf "$W"
echo "ALL_PUSHED"
