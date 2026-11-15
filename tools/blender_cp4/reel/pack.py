# Impacheteaza un dosar in arhive tar de cel mult LIM octeti (fara compresie: PNG/JPG sunt deja comprimate).
#   python3 pack.py <baza> <cale relativa> <prefix iesire> [extra1 extra2 ...]   -> <prefix>_01.tar, _02.tar ...
import os, sys, tarfile
base, rel, pref = sys.argv[1:4]; extra = sys.argv[4:]
LIM = 88 * 1024 * 1024
files = []
p = os.path.join(base, rel)
if os.path.isdir(p):
    for d, _, fs in sorted(os.walk(p)):
        for f in sorted(fs): files.append(os.path.relpath(os.path.join(d, f), base))
else: files.append(rel)
files += extra
n, cur, size, out = 1, [], 0, []
def flush():
    global n, cur, size
    if not cur: return
    name = '%s_%02d.tar' % (pref, n)
    with tarfile.open(name, 'w') as t:
        for f in cur: t.add(os.path.join(base, f), arcname=f)
    out.append((name, len(cur), os.path.getsize(name))); n += 1; cur, size = [], 0
for f in files:
    s = os.path.getsize(os.path.join(base, f)) + 1024
    if size + s > LIM: flush()
    cur.append(f); size += s
flush()
for o in out: print('%s  %d fisiere  %.1f MB' % (os.path.basename(o[0]), o[1], o[2] / 1e6))
