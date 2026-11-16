"""Voce provizorie pentru episoadele fara voce (creditele ElevenLabs terminate pe 15.11.2026):
momente pe cuvinte estimate (durata = 0,072 + 0,060 x litere, calibrata pe ep1/ep2) + pauzele din vo_script.json;
randurile refolosite (formula, „Vezi toate cauzele…”, finalul) iau momentele si sunetul reale din ep1.
python3 prov_vo.py 3 4 ...  ->  epN/vo/{cues.json, timeline.json, vo_track.wav, PROVIZORIU}"""
import json, re, sys, os, unicodedata
import numpy as np, soundfile as sf
HERE = '/home/claude/w/serinj'
def nrm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')
E1 = json.load(open(f'{HERE}/ep1/vo/cues.json'))
A1, SR = sf.read(f'{HERE}/ep1/vo/vo_track.wav', dtype='float32')
if A1.ndim > 1: A1 = A1.mean(1)

def ep1_words(i, upto=None):
    ws = [w for w in E1['words'] if w['win'] == i]
    if upto: ws = ws[:upto]
    return ws

def est_words(text):
    """cuvintele afisate (cifre) cu durate dupa forma rostita"""
    out = []
    for m in re.finditer(r'\{([^|}]*)\|([^}]*)\}|(\S+)', text):
        if m.group(3):
            tok = m.group(3); spoken = tok; out.append([tok, spoken]); continue
        disp, spoken = m.group(1), m.group(2)
        # cifra lipita de punctuatie care urmeaza (ex. „{13|treisprezece}:”)
        out.append([disp, spoken])
    # lipeste punctuatia care a ramas separata
    res = []
    for d, s in out:
        if res and not nrm(d) and d.strip():
            res[-1][0] += d; res[-1][1] += d
        else: res.append([d, s])
    return res

def build(n):
    rows = json.load(open(f'{HERE}/ep{n}/vo_script.json')); rows = rows['rows'] if isinstance(rows, dict) else rows
    # punctuatia de dupa acolade: „{13|treisprezece}:” -> lipita la cuvant
    lines = []; words = []; t = 0.0; audio = []
    for i, r in enumerate(rows):
        t += r['gap']
        if r['id'] == 'intro':
            ws = ep1_words(0, 6); base = E1['lines'][0]['start']
            for w in ws: words.append({'text': w['text'], 's': round(t + w['s'] - base, 3), 'e': round(t + w['e'] - base, 3), 'win': i})
            end = t + ws[-1]['e'] - base; audio.append((0.0, 3.16, t - base))
        elif r['id'] in ('s1', 'o1', 'o2', 'o3'):
            src = {'s1': 1, 'o1': 11, 'o2': 12, 'o3': 13}[r['id']]; ws = ep1_words(src); base = E1['lines'][src]['start']
            for w in ws: words.append({'text': w['text'], 's': round(t + w['s'] - base, 3), 'e': round(t + w['e'] - base, 3), 'win': i})
            end = t + E1['lines'][src]['end'] - base
            audio.append((E1['lines'][src]['start'] - 0.06, E1['lines'][src]['end'] + 0.12, t - base))
        else:
            tt = t
            for d, s in est_words(re.sub(r'\}(\S)', lambda m: '}' + m.group(1), r['text'])):
                k = nrm(s); dur = 0.072 + 0.060 * len(k)
                words.append({'text': d, 's': round(tt, 3), 'e': round(tt + dur, 3), 'win': i})
                tt += dur
                if d[-1] in ',;': tt += 0.16
                elif d[-1] in '.:?!”': tt += 0.34
            end = words[-1]['e']
        disp = re.sub(r'\{([^|}]*)\|([^}]*)\}', r'\1', r['text'])
        lines.append({'i': i, 'start': round(words[[w['win'] for w in words].index(i)]['s'] if r['id'] not in ('intro',) else t, 3), 'end': round(end, 3), 'text': disp})
        t = end
    story_end = round(t + 0.98, 3); total = round(story_end + 7.5, 3)
    od = f'{HERE}/ep{n}/vo'; os.makedirs(od, exist_ok=True)
    json.dump({'end': story_end, 'lines': lines, 'words': words}, open(f'{od}/cues.json', 'w'), ensure_ascii=False)
    tl = {'fps': 30, 'width': 1080, 'height': 1920, 'total': total, 'story_out0': 0.0, 'story_end': story_end, 'end_card': 7.5,
          'segments': [{'kind': 'story', 'src_a': 0.0, 'src_b': story_end, 'out_a': 0.0, 'zg': 0}],
          'words': [dict(w, os=w['s'], oe=w['e']) for w in words], 'sentences': lines, 'narrator': True, 'cold_words': [], 'provisional': True}
    json.dump(tl, open(f'{od}/timeline.json', 'w'), ensure_ascii=False, indent=1)
    out = np.zeros(int((total + 0.5) * SR), np.float32)
    for a, b, dst in audio:
        seg = A1[int(a * SR):int(b * SR)].copy(); f = int(0.02 * SR)
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        i0 = int((dst + a) * SR); out[i0:i0 + len(seg)] += seg
    sf.write(f'{od}/vo_track.wav', out, SR)
    open(f'{od}/PROVIZORIU', 'w').write('voce provizorie: momente estimate, doar randurile refolosite au sunet\n')
    print(n, 'story_end', story_end, 'total', total, 'lines', len(lines))

for a in sys.argv[1:]: build(int(a))
