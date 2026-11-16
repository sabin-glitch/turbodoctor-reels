import json, re, sys
from collections import Counter, defaultdict
SP='/tmp/claude-0/-home-claude/77ff75bb-68c8-5682-967c-243fa44cac4d/scratchpad/vo'
p='/root/.claude/projects/-home-claude/77ff75bb-68c8-5682-967c-243fa44cac4d.jsonl'
uses={}; gens={}
with open(p) as f:
    for line in f:
        try: d=json.loads(line)
        except: continue
        if d.get('timestamp','')<'2026-11-16T06:50': continue
        c=d.get('message',{}).get('content')
        if not isinstance(c,list): continue
        for b in c:
            if b.get('type')=='tool_use' and 'get_flow_run_status' in b.get('name',''):
                uses[b['id']]=b['input']
            if b.get('type')=='tool_result' and b.get('tool_use_id') in uses:
                cc=b.get('content')
                texts=[cc] if isinstance(cc,str) else [x.get('text','') for x in cc if isinstance(x,dict)]
                for t in texts:
                    j=json.loads(t)
                    def walk(o):
                        if isinstance(o,dict):
                            if 'content_url' in o and 'id' in o: gens[o['id']]=o
                            for v in o.values(): walk(v)
                        elif isinstance(o,list):
                            for v in o: walk(v)
                    walk(j)
S=json.load(open(SP+'/sessions.json'))
sess2=defaultdict(list)
for g in gens.values():
    m=re.search(r'/content_generation/([^/]+)/([^/]+)/content\.mp3',g['content_url'])
    sess2[m.group(1)].append(g)
print('generations',len(gens),'distinct url sessions',len(sess2), Counter(len(v) for v in sess2.values()))
out=[]; bad=0
for e in S:
    takes=[]
    for s in e['sessions']:
        gl=sorted(sess2.get(s,[]),key=lambda g:g['created_at_unix_ms'])
        takes+=gl
    if len(takes)!=2: print('!! takes',e['ep'],e['line'],len(takes)); bad+=1
    for k,g in zip('ab',takes):
        if g['prompt']!=e['prompt']: print('!! prompt mismatch',e['ep'],e['line']); bad+=1
        out.append((e['ep'],e['line'],k,g['content_url'],g['duration_secs']))
print('entries',len(out),'bad',bad)
lines=[f"si{ep}L{ln:02d}{k}={u}" for ep,ln,k,u,_ in out]
txt='\n'.join(lines)
print('chars',len(txt))
open(SP+'/fetch_all.txt','w').write(txt+'\n')
json.dump([dict(ep=ep,line=ln,take=k,dur=dd) for ep,ln,k,u,dd in out],open(SP+'/takes.json','w'),indent=0)
