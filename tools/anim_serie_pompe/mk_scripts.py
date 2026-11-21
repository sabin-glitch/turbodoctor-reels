"""Writes epN/vo_script.json (N = 1..17) for the series „De ce se strică pompele de înaltă presiune” from pdata_eps.py (names) + pdata_vo.py
(body rows, the texts of the approved document), and prompts.json (what is sent to ElevenLabs, one generation per row).
Rows longer than MAXC are split at sentence ends (eleven_v4 keeps the tone tags for about 10 s)."""
import re, json, os
from pdata_eps import EP
from pdata_vo import V
HERE = os.path.dirname(os.path.abspath(__file__)); MAXC = 178; HOOK = 3.0
NUM = {1: "unu", 2: "doi", 3: "trei", 4: "patru", 5: "cinci", 6: "șase", 7: "șapte", 8: "opt", 9: "nouă", 10: "zece", 11: "unsprezece", 12: "doisprezece",
       13: "treisprezece", 14: "paisprezece", 15: "cincisprezece", 16: "șaisprezece", 17: "șaptesprezece"}
# pronunciation: {shown|spoken}
SAYMAP = [("CP4", "{CP4|ce pe patru}"), ("Biodieselul", "{Biodieselul|Biodizelul}"), ("biodiesel", "{biodiesel|biodizel}")]
def mark(t):
    for a, b in SAYMAP: t = t.replace(a, b)
    return t
def split(line):
    if len(line) <= MAXC: return [line]
    s = re.split(r'(?<=[.!?])\s+', line); best = None
    for k in range(1, len(s)):
        a, b = ' '.join(s[:k]), ' '.join(s[k:]); c = max(len(a), len(b))
        if best is None or c < best[0]: best = (c, a, b)
    return split(best[1]) + split(best[2]) if best else [line]
SAY = lambda t: re.sub(r'\{[^|]*\|([^}]*)\}', r'\1', t)
prompts = []; tot = 0
for e in EP:
    n = e['n']; rows = V[n]; S = []
    S.append(dict(text=f"Seria „De ce se strică pompele de înaltă presiune”. Astăzi prezentăm cauza {{{n}|{NUM[n]}}} din {{17|șaptesprezece}}: {mark(e['nume'])}.",
                  gap=HOOK, tags="[serious] [matter of fact] [conversational tone]", id=f"p{n}h", doc=1))
    S.append(dict(text="Vezi toate cauzele pe TikTok, Facebook și YouTube-ul nostru.", gap=.35, id="s1", doc=1))
    k = 0
    for j, r in enumerate(rows):
        parts = split(r)
        for pi, p in enumerate(parts):
            g = .6 if (j == 0 and pi == 0) else (.34 if pi else (.6 if p.startswith('Ce facem noi') else (.5 if p.startswith('Cum eviți') else .42)))
            S.append(dict(text=mark(p), gap=g, id=f"p{n}b{k}", doc=j + 2)); k += 1
    S += [dict(text="La Turbo Doctor suntem experți în aceste probleme.", gap=.8, id="o1"),
          dict(text="Acum că știi cum poți evita această problemă, ar trebui să ajungi cât mai târziu la noi.", gap=.4, id="o2"),
          dict(text="Iar dacă ai nevoie de noi, la noi diagnoza este gratuită.", gap=.4, id="o3")]
    os.makedirs(f'{HERE}/ep{n}', exist_ok=True)
    json.dump(S, open(f'{HERE}/ep{n}/vo_script.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for i, s in enumerate(S):
        if s['id'].startswith('p'):
            p = (s.get('tags') or '[calm] [matter of fact]') + ' ' + SAY(s['text']); prompts.append(dict(ep=n, line=i, prompt=p)); tot += len(p)
    print(n, len(S), 'rows', max(len(s['text']) for s in S), 'max chars', e['titlu'])
assert len({p['prompt'] for p in prompts}) == len(prompts), 'duplicate prompts'
json.dump(prompts, open(f'{HERE}/prompts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(prompts), 'prompts', tot, 'chars; two takes each =', 2 * tot, 'chars')
