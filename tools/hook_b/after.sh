#!/bin/bash
# after.sh <log to wait for ALL_RENDERS_DONE> <new log> slugs... : start the next render batch when the previous one ends
W=$1; O=$2; shift 2
until grep -q ALL_RENDERS_DONE "$W" 2>/dev/null; do sleep 15; done
bash "$(dirname "$0")/render_all.sh" "$@" > "$O" 2>&1
