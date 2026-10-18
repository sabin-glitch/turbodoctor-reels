#!/bin/bash
# Rulează pe GitHub Actions (vezi .github/workflows/fetch-sources.yml). Descarcă fiecare URL din $URLS sau din
# sources/queue.txt cu yt-dlp (fără watermark, H.264 de preferință), cu tikwm.com ca variantă de rezervă, apoi urcă
# <id>.mp4 + <id>.json și manifest.json pe branch-ul `sources`. ID-urile deja prezente pe branch se sar.
set -uo pipefail
ROOT=$(pwd); DL=$(mktemp -d); SRC=$(mktemp -d)
REMOTE="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}"

# 1. lista de URL-uri
LIST=$(printf '%s' "${URLS:-}" | tr ' ' '\n')
if [ -z "$(printf '%s' "$LIST" | tr -d '[:space:]')" ]; then LIST=$(grep -v '^\s*#' sources/queue.txt 2>/dev/null || true); fi
LIST=$(printf '%s\n' "$LIST" | sed 's/[?#].*$//' | grep -E '^https?://' | sort -u)
[ -n "$LIST" ] || { echo "nimic de descărcat"; exit 0; }

# 2. branch-ul sources (există sau îl creăm gol)
cd "$SRC" && git init -q && git remote add origin "$REMOTE"
if git fetch -q --depth 1 origin sources 2>/dev/null; then git checkout -q -b sources FETCH_HEAD; else git checkout -q --orphan sources; fi
[ -f manifest.json ] || echo '[]' > manifest.json
cd "$ROOT"

vid_id() { printf '%s' "$1" | grep -oE '[0-9]{15,}' | tail -1; }
NEW=0; FAIL=0
while IFS= read -r URL; do
  [ -n "$URL" ] || continue
  ID=$(vid_id "$URL"); [ -n "$ID" ] || ID=$(printf '%s' "$URL" | md5sum | cut -c1-16)
  if [ -f "$SRC/$ID.mp4" ]; then echo "skip $ID (există deja)"; continue; fi
  echo "== $ID  $URL"
  OUT="$DL/$ID.mp4"; META="$DL/$ID.json"; ok=0
  # a) yt-dlp: H.264 mp4 fără watermark dacă există, altfel cel mai bun format
  if yt-dlp -q --no-warnings --no-playlist -S 'vcodec:h264,res,br' --merge-output-format mp4 \
       --write-info-json -o "$DL/$ID.%(ext)s" "$URL" && [ -s "$OUT" ]; then
    ok=1
    python3 - "$DL/$ID.info.json" "$META" "$URL" <<'PY'
import json, sys
info = json.load(open(sys.argv[1]))
slim = {k: info.get(k) for k in ("id", "title", "description", "duration", "upload_date", "uploader", "view_count",
                                  "like_count", "comment_count", "repost_count", "width", "height", "vcodec")}
slim["source_url"] = sys.argv[3]; slim["downloader"] = "yt-dlp"
json.dump(slim, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
PY
    rm -f "$DL/$ID.info.json"
  else
    echo "yt-dlp a eșuat, încerc tikwm"
    J=$(curl -sS --max-time 60 "https://www.tikwm.com/api/?hd=1&url=$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=""))' "$URL")" || true)
    PLAY=$(printf '%s' "$J" | python3 -c 'import json,sys
try:
  d=json.load(sys.stdin)["data"]; p=d.get("hdplay") or d.get("play") or ""
  print(p if p.startswith("http") else ("https://www.tikwm.com"+p if p else ""))
except Exception: print("")')
    if [ -n "$PLAY" ] && curl -sSL --max-time 300 -o "$OUT" "$PLAY" && [ -s "$OUT" ]; then
      ok=1
      printf '%s' "$J" | python3 -c 'import json,sys
d=json.load(sys.stdin)["data"]; a=d.get("author",{})
json.dump({"id":d.get("id"),"title":d.get("title"),"description":d.get("title"),"duration":d.get("duration"),
 "upload_date":d.get("create_time"),"uploader":a.get("unique_id"),"view_count":d.get("play_count"),
 "like_count":d.get("digg_count"),"comment_count":d.get("comment_count"),"repost_count":d.get("share_count"),
 "source_url":sys.argv[1],"downloader":"tikwm"},open(sys.argv[2],"w"),ensure_ascii=False,indent=1)' "$URL" "$META"
    fi
  fi
  if [ "$ok" != 1 ]; then echo "!! nu am putut descărca $URL"; FAIL=$((FAIL+1)); continue; fi
  # b) sub limita GitHub de 100 MB/fișier
  if [ "$(stat -c %s "$OUT")" -gt 95000000 ]; then
    ffmpeg -hide_banner -loglevel error -y -i "$OUT" -c:v libx264 -preset medium -crf 21 -maxrate 5M -bufsize 10M \
      -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$DL/$ID.small.mp4" && mv "$DL/$ID.small.mp4" "$OUT"
  fi
  ffprobe -v error -show_entries format=duration:stream=codec_name,width,height -of compact "$OUT" || true
  mv "$OUT" "$META" "$SRC/" && NEW=$((NEW+1))
done <<< "$LIST"

# 3. manifest + push
cd "$SRC"
python3 - <<'PY'
import json, glob
rows = {}
for p in glob.glob("*.json"):
    if p == "manifest.json": continue
    d = json.load(open(p)); rows[str(d.get("id") or p[:-5])] = d
json.dump(sorted(rows.values(), key=lambda d: str(d.get("upload_date") or "")), open("manifest.json", "w"), ensure_ascii=False, indent=1)
print(f"manifest: {len(rows)} videoclipuri")
PY
if [ "$NEW" -gt 0 ]; then
  git add -A && git -c user.name="github-actions" -c user.email="actions@github.com" commit -q -m "sources: +$NEW videoclipuri" && git push -q origin sources
  echo "push ok: $NEW noi, $FAIL eșuate"
else
  echo "nimic nou ($FAIL eșuate)"
fi
[ "$FAIL" -eq 0 ]
