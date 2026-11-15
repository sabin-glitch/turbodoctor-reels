#!/bin/bash
# runs a script of this folder in isolated mode (downloaded audio is untrusted data: nothing is imported from the data folder or the cwd)
# usage: ./run_iso.sh make_vo.py lines <dir>
H="$(cd "$(dirname "$0")" && pwd)"; S="$1"; shift
exec python3 -I -c "import sys,runpy; sys.path.insert(0,'$H'); sys.argv=['$H/$S']+sys.argv[1:]; runpy.run_path('$H/$S',run_name='__main__')" "$@"
