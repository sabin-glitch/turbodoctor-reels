#!/bin/bash
# Rulează pe GitHub Actions (tts-elevenlabs.yml): generează replicile jobului cu ElevenLabs, apoi le urcă pe branch-ul `sources`
# în tts/<job>/ (câte un MP3 pe replică + <job>.json cu textul și durata fiecăreia). Claude le aduce cu `git show origin/sources:tts/<job>/<id>.mp3`.
set -euo pipefail
JOB=$1; ROOT=$(pwd); SRC=$(mktemp -d); OUT=$(mktemp -d)
[ -f "tools/tts/jobs/$JOB.json" ] || { echo "nu există tools/tts/jobs/$JOB.json"; exit 1; }
[ -n "${ELEVENLABS_API_KEY:-}" ] || { echo "lipsește secretul ELEVENLABS_API_KEY"; exit 1; }
python3 tools/tts/elevenlabs_tts.py "tools/tts/jobs/$JOB.json" "$OUT/$JOB"
REMOTE="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}"
cd "$SRC" && git init -q && git remote add origin "$REMOTE"
if git fetch -q --depth 1 origin sources 2>/dev/null; then git checkout -q -b sources FETCH_HEAD; else git checkout -q --orphan sources; fi
mkdir -p tts && rm -rf "tts/$JOB" && cp -r "$OUT/$JOB" "tts/$JOB"
git config user.name "tts-elevenlabs"; git config user.email "actions@users.noreply.github.com"
git add tts && git commit -q -m "tts: $JOB ($(ls tts/$JOB/*.mp3 | wc -l) replici)" && git push -q origin sources
echo "OK tts/$JOB"
