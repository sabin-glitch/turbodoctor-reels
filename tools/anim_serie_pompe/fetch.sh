#!/bin/bash
# usage: fetch.sh  -> reads packs from the transcript (mk_pack.py urls), dispatches fetch-sources (chunks of 40 name=URL pairs)
cd /home/claude/w/serpmp && python3 mk_pack.py urls || exit 1
[ -s fetch_list.txt ] || { echo "nothing to fetch"; exit 0; }
split -l 40 -d fetch_list.txt fl_
for f in fl_*; do
python3 -c "
import json,sys;json.dump({'ref':'main','inputs':{'urls':open('$f').read().strip()}},open('disp.json','w'))"
curl -sS -w '%{http_code}\n' -X POST -H 'Accept: application/vnd.github+json' -H 'Content-Type: application/json' https://api.github.com/repos/sabin-glitch/turbodoctor-reels/actions/workflows/fetch-sources.yml/dispatches -d @disp.json
rm $f disp.json; sleep 2
done
