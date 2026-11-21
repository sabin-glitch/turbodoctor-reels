#!/bin/bash
# eq.sh [P] -> coada de episoade: ruleaza pe rand make_ep.sh N P validate pentru numerele din logs/eq.list (unul pe linie) care nu sunt inca in logs/eq.done
P=${1:-3}; cd /home/claude/w/serpmp || exit 1; touch logs/eq.list logs/eq.done
while true; do
  N=$(grep -vxFf logs/eq.done logs/eq.list | head -1)
  [ -z "$N" ] && break
  while pgrep -f "scripts/make_ep.sh" > /dev/null; do sleep 15; done
  echo "EQ_START $(date -u +%H:%M:%S) $N"
  bash scripts/make_ep.sh $N $P validate
  echo "$N" >> logs/eq.done
  echo "EQ_END $(date -u +%H:%M:%S) $N"
done
echo EQ_EMPTY
