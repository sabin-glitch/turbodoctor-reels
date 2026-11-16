"""Scrie reel.js pentru un episod al seriei injectoarelor din momentele vocii (titlurile boom din hook pe cuvinte).
python3 mk_reeljs.py <n> <folderul reel-ului> [cues.json]"""
import json, sys, unicodedata
from PIL import ImageFont
FONT = '/home/claude/turbodoctor-reels/assets/fonts/Anton_400Regular.ttf'
NAMES = {1: 'PARTICULELE DIN MOTORINĂ', 2: 'APA DIN MOTORINĂ', 3: 'DEPUNERILE DIN INTERIOR', 4: 'CALAMINA DIN GĂURILE DUZEI',
         5: 'ȘAIBA DE ETANȘARE', 6: 'MURDĂRIA ȘI GREȘELILE DE LA MONTAJ', 7: 'BENZINA PUSĂ DIN GREȘEALĂ', 8: 'ADBLUE ÎN REZERVORUL DE MOTORINĂ',
         9: 'MOTORINA CARE NU UNGE', 10: 'PILITURA DE LA POMPĂ', 11: 'FĂRĂ COD ȘI FĂRĂ STANDARD', 12: 'DEFECTELE ELECTRICE', 13: 'UZURA NORMALĂ'}
DESC = {1: 'particulele din motorină', 2: 'apa din motorină', 3: 'depunerile din interior', 4: 'calamina din găurile duzei', 5: 'șaiba de etanșare',
        6: 'murdăria și greșelile de la montaj', 7: 'benzina pusă din greșeală', 8: 'AdBlue în rezervorul de motorină', 9: 'motorina care nu unge',
        10: 'pilitura de la pompă', 11: 'injectorul fără cod și recondiționarea fără standard', 12: 'defectele electrice', 13: 'uzura normală'}
# cuvintele colorate din subtitrări, pe rândurile de explicație (0 = primul rând după „Vezi toate cauzele…”)
TAGS = {
 1: {0: {'bosch': 'y', 'murdara': 'r', 'cedeaza': 'r'}, 1: {'jocuri': 'y', 'microni': 'y', 'par': 'c'}, 2: {'particulele': 'r', 'vezi': 'y', 'rau': 'r'},
     3: {'supapa': 'y', 'bila': 'y', 'milimetru': 'y', 'deschide': 'c', 'opreste': 'c'}, 4: {'prinse': 'r', 'adancituri': 'r', 'sapa': 'r', 'canal': 'r'},
     5: {'etanseaza': 'r', 'returul': 'y', 'creste': 'r', 'tarziu': 'r'}, 6: {'smirghel': 'r', 'macina': 'r', 'duza': 'y', 'jetul': 'r'},
     7: {'martorul': 'y', 'putere': 'r', 'opreste': 'r'}, 8: {'eviti': 'g', 'filtru': 'g', 'calitate': 'g', 'intervalul': 'g', 'serioase': 'g'}},
 2: {0: {'bosch': 'y', 'apa': 'c', 'doua': 'y'}, 1: {'metal': 'y', 'apa': 'c', 'rugina': 'r'}, 2: {'rugina': 'r', 'macina': 'r', 'blocheaza': 'r'},
     3: {'apa': 'c', 'unge': 'r', 'lubrifiant': 'y'}, 4: {'condensul': 'c', 'rezervor': 'y', 'benzinarii': 'y', 'filtrul': 'y', 'scursa': 'r'},
     5: {'separa': 'c', 'pahar': 'y', 'scursa': 'r', 'pompa': 'r', 'injectoare': 'r'}, 6: {'pornire': 'r', 'neregulat': 'r', 'putere': 'r', 'fum': 'r'},
     7: {'eviti': 'g', 'serioase': 'g', 'timp': 'g', 'martorul': 'y', 'scursa': 'g'}},
}
def nrm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')
def width(txt, size):
    f = ImageFont.truetype(FONT, size); return f.getlength(txt) + 3 * len(txt) + 18
def fit(txt, size, wmax=960):
    while size > 60 and width(txt, size) > wmax: size -= 2
    return size
def split2(name):
    w = name.split(); best = None
    for i in range(1, len(w)):
        a, b = ' '.join(w[:i]), ' '.join(w[i:]); d = abs(len(a) - len(b))
        if best is None or d < best[0]: best = (d, a, b)
    return best[1], best[2]

def main():
    n = int(sys.argv[1]); R = sys.argv[2]; cp = sys.argv[3] if len(sys.argv) > 3 else f'/home/claude/w/serinj/ep{n}/vo/cues.json'
    c = json.load(open(cp)); L = c['lines']; NL = len(L)
    def W(i, w, k=0): return [x for x in c['words'] if x['win'] == i and nrm(x['text']) == nrm(w)][k]['s']
    def find(word):
        for l in L:
            if any(nrm(x['text']) == nrm(word) for x in c['words'] if x['win'] == l['i']): return l['i']
    iv = find('vezi'); ic = find('cauza'); name = NAMES[n]; first = name.split()[0]
    first_spoken = {11: 'injectorul'}.get(n, first)
    T1 = L[0]['start'] + .02; T2 = W(0, 'injectoarele') - .03; T3 = W(ic, 'cauza') - .03; T4 = W(ic, first_spoken) - .03
    S1 = L[iv]['start']; HK = L[iv + 1]['start'] - .3
    items = [
        f"{{ k: 'boom', t: T1, dur: T3 - .12 - T1, txt: 'DE CE SE STRICĂ', y: 430, size: 126, col: '#FFFFFF', from: 3.2, sh: 18, ca: 22, riser: false, bg: .6, cg: .3 }}",
        f"{{ k: 'boom', t: T2, dur: T3 - .12 - T2, txt: 'INJECTOARELE?', y: 590, size: {fit('INJECTOARELE?', 170)}, col: '#FFD21F', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3 }}",
        f"{{ k: 'boom', t: T3, dur: HK - .1 - T3, txt: 'CAUZA {n} DIN 13', y: 430, size: 140, col: '#FFD21F', from: 3.2, sh: 18, ca: 22, riser: false, bg: .6, cg: .3 }}",
    ]
    if width(name, 150) <= 960:
        items.append(f"{{ k: 'boom', t: T4, dur: HK - .1 - T4, txt: '{name}', y: 590, size: {fit(name, 160)}, col: '#FF4B4B', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3, glow: 'rgba(255,75,75,.6)' }}")
    else:
        a, b = split2(name); sz = min(fit(a, 150), fit(b, 150))
        items.append(f"{{ k: 'boom', t: T4, dur: HK - .1 - T4, txt: '{a}', y: 575, size: {sz}, col: '#FF4B4B', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3, glow: 'rgba(255,75,75,.6)' }}")
        items.append(f"{{ k: 'boom', t: T4 + .1, dur: HK - .2 - T4, txt: '{b}', y: {575 + int(sz * 1.08)}, size: {sz}, col: '#FF4B4B', from: 3.0, sh: 20, ca: 24, riser: false, bg: .4, cg: .2, glow: 'rgba(255,75,75,.6)' }}")
    items.append("{ k: 'chip', t0: S1 + .9, t1: HK - .15, y: 1226, ph: [[S1 + .9, 'eyes', 'TOATE CAUZELE: TIKTOK · FACEBOOK · YOUTUBE', 'yellow']] }")
    tags = {iv: {'tiktok': 'c', 'facebook': 'c', 'youtubeul': 'c'}}
    for k, v in TAGS.get(n, {}).items(): tags[iv + 1 + k] = v
    o = NL - 3
    tags[o] = {'turbo': 'y', 'doctor': 'y', 'experti': 'y'}; tags[o + 1] = {'evita': 'g', 'tarziu': 'g'}; tags[o + 2] = {'diagnoza': 'g', 'gratuita': 'g'}
    js = f"""// v2 – Seria „De ce se strică injectoarele”, cauza {n} din 13: {DESC[n]} (15–16.11.2026)
// Reel animat 3D în secțiune (cadre Blender + montaj în Python, /home/claude/w/serinj, episodul ep{n}), cu vocea „Sabin” din ElevenLabs, rând cu rând.
// Formula seriei (ca la turbine): începe cu numele seriei și „cauza X din 13”, se termină cu „La Turbo Doctor suntem experți…”
// și cu ecranul de final cu diagnoză gratuită, numărul de telefon și pictogramele serviciilor (endPhone + endIcons).
// Etichetele de pe piese, insigna „Cauza {n} din 13” și marcajul din fundal sunt în cadre; compozitorul pune titlurile boom, subtitrările și ecranul de final.
window.REEL_CFG = ({{ aw, ew, S0, SEND, TEND }}) => {{
  const T1 = {T1:.2f}, T2 = {T2:.2f}, T3 = {T3:.2f}, T4 = {T4:.2f}, S1 = {S1:.2f}, HK = {HK:.2f};
  return {{
    hook: null,
    stages: null,
    endIcons: true,
    endPhone: true,
    hideCap: [[0, S1 - .1]],
    items: [
      {(',' + chr(10) + '      ').join(items)},
    ],
    fx: [
      {{ k: 'punch', t: T1, a: .08, sh: 16 }}, {{ k: 'punch', t: T2, a: .1, sh: 22 }}, {{ k: 'glitch', t: T2, d: .14 }},
      {{ k: 'punch', t: T3, a: .08, sh: 16 }}, {{ k: 'punch', t: T4, a: .14, sh: 30 }}, {{ k: 'glitch', t: T4, d: .18 }},
    ],
    bgFix: [[0, SEND]],
    tags: {json.dumps({str(k): v for k, v in sorted(tags.items())}, ensure_ascii=False)},
  }};
}};
"""
    open(f'{R}/reel.js', 'w').write(js)
    json.dump({'t': round(T4 + .9, 2)}, open(f'{R}/out/cover_t.json', 'w'))
    print(n, 'ok', round(T1, 2), round(T2, 2), round(T3, 2), round(T4, 2), round(S1, 2), round(HK, 2))
main()
