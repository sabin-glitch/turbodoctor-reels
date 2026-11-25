#!/bin/bash
# vo_fetch.sh "nume=URL nume=URL ..."  -> pornește workflow-ul fetch-sources (GitHub descarcă fișierele și le pune pe ramura `sources`)
gh api repos/sabin-glitch/turbodoctor-reels/actions/workflows/fetch-sources.yml/dispatches -f ref=main -f "inputs[urls]=$1"
