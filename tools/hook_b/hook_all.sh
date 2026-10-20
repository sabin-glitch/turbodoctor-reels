#!/bin/bash
# per reel: prep (reel.js + intro_script from hook_specs) -> intro voice -> timeline/frames/track shift/cover -> intro test frames. 3 reels at a time.
H=$(cd "$(dirname "$0")" && pwd); P=$(cd "$H/../../pipeline" && pwd)
cd /home/claude/reels
one() {
  python3 $H/prep_hook.py $1 > /dev/null 2>&1 || { echo "PREP_FAIL $1"; return; }
  cp $P/intro_vo.py $1/
  (cd $1 && python3 intro_vo.py > out/intro_vo.log 2>&1) || { echo "VO_FAIL $1"; return; }
  bash $H/post_vo.sh $1
}
L=("$@"); [ ${#L[@]} -gt 0 ] || { echo "usage: hook_all.sh <slug>..."; exit 1; }
for ((i = 0; i < ${#L[@]}; i += 3)); do
  for r in "${L[@]:i:3}"; do one $r & done; wait
done
echo ALL_HOOKS_DONE
