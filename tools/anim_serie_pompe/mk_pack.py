"""Voice takes of the pump series: maps each creative_generate_speech call of this session (prompt -> generation ids, read from the
session transcript) to sp<N>L<NN><a|b>, and prints sandbox `inputs` chunks (<=20) for the takes not packed yet.
  mk_pack.py inputs [ep...]   -> prints chunks of inputs JSON for creative_execute_sandbox (pack = cat of the mp3s + manifest "name size")
  mk_pack.py urls             -> reads sandbox results (manifest + asset id) and creative_get_available_assets results from the
                                 transcript, writes packs.json and fetch_list.txt (sppk<assetid>=preview_url), prints asset ids lacking a url
  mk_pack.py credits          -> credits spent so far on speech (sum of credit_costs)"""
import json, sys, os, glob, re
HERE = os.path.dirname(os.path.abspath(__file__))
PS = glob.glob('/root/.claude/projects/-home-claude/a3683645-8faf-50c2-b360-38bf0dd6a2fe*.jsonl')
PR = {p['prompt']: (p['ep'], p['line']) for p in json.load(open(f'{HERE}/prompts.json'))}
if os.path.exists(f'{HERE}/prompts_fix.json'):
    for p in json.load(open(f'{HERE}/prompts_fix.json')): PR[p['prompt']] = (p['ep'], p['line'])
uses = {}; res = {}; cost = {}; sand = []; assets = {}
def texts(b):
    cc = b.get('content'); return [cc] if isinstance(cc, str) else [x.get('text', '') for x in (cc or []) if isinstance(x, dict)]
for P in PS:
  for line in open(P):
    if 'creative_' not in line and 'content_asset_id' not in line and 'preview_url' not in line: continue
    try: d = json.loads(line)
    except Exception: continue
    c = d.get('message', {}).get('content')
    if not isinstance(c, list): continue
    for b in c:
        if not isinstance(b, dict): continue
        if b.get('type') == 'tool_use' and b.get('name', '').endswith('creative_generate_speech'):
            if not b['input'].get('estimate_only'): uses[b['id']] = b['input'].get('prompt')
        elif b.get('type') == 'tool_result':
            for t in texts(b):
                try: j = json.loads(t)
                except Exception: continue
                if not isinstance(j, dict): continue
                if 'results' in j and 'session_ids' in j:
                    res[b['tool_use_id']] = [k for r in j['results'] if r.get('success') for k in r.get('credit_costs', {})]
                    cost[b['tool_use_id']] = sum(v for r in j['results'] if r.get('success') for v in r.get('credit_costs', {}).values())
                elif 'outputs' in j and 'stdout' in j and j.get('status') in ('done', 'completed', 'succeeded', 'finished'): sand.append(j)
                elif 'assets' in j:
                    for a in j['assets']:
                        if a.get('preview_url'): assets[a['asset_id']] = a['preview_url']
by = {}; unk = []
for tid, pr in uses.items():
    k = PR.get(pr)
    if tid not in res: continue
    if k is None: unk.append(pr); continue
    by.setdefault(k, []).extend(res[tid])
names = {}
for (ep, ln), gl in sorted(by.items()):
    for x, g in zip('abcdefgh', gl): names[f"sp{ep}L{ln:02d}{x}"] = g
json.dump(names, open(f'{HERE}/take_names.json', 'w'), indent=0)
FJ = f'{HERE}/fetched.json'; done = json.load(open(FJ)) if os.path.exists(FJ) else {}
packs = []
for j in sand:
    man = [l.split() for l in j['stdout'].splitlines() if re.match(r'^sp\d+L\d\d[a-z] \d+ [\d.]+$', l)]   # name bytes seconds (packs with 0.6 s gaps)
    aid = [o.get('content_asset_id') for o in j['outputs'] if o.get('content_asset_id') and o.get('filename', '').startswith('pk')]
    if man and aid: packs.append(dict(asset=aid[0], man=[(n, int(s), float(d)) for n, s, d in man]))
packed = {m[0] for p in packs for m in p['man']}
mode = sys.argv[1]
if mode == 'inputs':
    want = [int(x) for x in sys.argv[2:]]
    todo = [n for n in names if n not in done and n not in packed and (not want or int(n[2:n.index('L')]) in want)]
    need = {(p['ep'], p['line']) for p in json.load(open(f'{HERE}/prompts.json')) if not want or p['ep'] in want}
    print('missing lines', sorted(need - set(by)), '| unknown prompts', len(unk), '| takes to pack', len(todo))
    for i in range(0, len(todo), 20):
        print(json.dumps([dict(generation_id=names[n], filename=n + '.mp3') for n in todo[i:i + 20]], separators=(',', ':')))
elif mode == 'credits':
    print('speech calls', len(res), 'credits', sum(cost.values()), '| lines done', len(by), 'of', len(PR))
    for u in unk: print('  unknown prompt:', u[:90])
else:
    json.dump(packs, open(f'{HERE}/packs.json', 'w'))
    got = json.load(open(f'{HERE}/packs_got.json')) if os.path.exists(f'{HERE}/packs_got.json') else []
    out = [(p['asset'], assets[p['asset']]) for p in packs if p['asset'] in assets and p['asset'] not in got]
    print('packs', len(packs), 'with url, not fetched yet', len(out), '| no url yet:', json.dumps([p['asset'] for p in packs if p['asset'] not in assets and p['asset'] not in got]))
    open(f'{HERE}/fetch_list.txt', 'w').write(''.join(f"sppk{a}={u}\n" for a, u in out))
