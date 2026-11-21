"""Scrie reel.js (titlurile boom din primele secunde, culorile din subtitrari, ecranul de final) si textul postarii
pentru un episod al seriei „De ce se strica pompele de inalta presiune”.
    python3 mk_reeljs_pmp.py <n> <folderul reel-ului>
Citeste pdata_eps.py, epN/vo/cues.json si epN/vo_script.json; scrie <reel>/reel.js, <reel>/out/cover_t.json si post/epN.txt."""
import json, sys, unicodedata, re, os
from PIL import ImageFont
HERE = '/home/claude/w/serpmp'; sys.path.insert(0, HERE)
import pdata_eps as PD
FONT = '/home/claude/turbodoctor-reels/assets/fonts/Anton_400Regular.ttf'
NT = 17

def nrm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')
def width(txt, size):
    f = ImageFont.truetype(FONT, size); return f.getlength(txt) + 3 * len(txt) + 18
def fit(txt, size, wmax=960):
    while size > 56 and width(txt, size) > wmax: size -= 2
    return size

# titlul din primele 3 secunde, pe randuri (ultimul rand e galben)
HOOK = {1: ['UN SCHIMB DE FILTRU', 'POATE STRICA POMPA'], 2: ['PE ULTIMII LITRI,', 'POMPA TRAGE AER'], 3: ['BENZINA SPALĂ', 'UNGEREA POMPEI'],
        4: ['NU ORICE MOTORINĂ', 'UNGE POMPA'], 5: ['PRAFUL PE CARE NU-L VEZI', 'ROADE POMPA'], 6: ['APA DIN MOTORINĂ', 'RUGINEȘTE POMPA', 'PE DINĂUNTRU'],
        7: ['ADBLUE ÎN MOTORINĂ:', 'NU PUNE CONTACTUL'], 8: ['MOTORINA VECHE', 'LIPEȘTE PISTOANELE', 'POMPEI'], 9: ['FILTRUL ÎNFUNDAT', 'ÎNFOMETEAZĂ POMPA'],
        10: ['POMPA MICĂ DIN REZERVOR', 'O STRICĂ PE CEA MARE'], 11: ['BULELE DIN CONDUCTĂ', 'NU SUNT NEVINOVATE'],
        12: ['O SUPAPĂ CÂT DEGETUL', 'HOTĂRĂȘTE PRESIUNEA', 'DIN RAMPĂ'], 13: ['UN SFERT DE TURĂ', 'ȘI POMPA FACE PILITURĂ'], 14: ['ȘI O POMPĂ ÎNGRIJITĂ', 'SE UZEAZĂ'],
        15: ['POMPA NOUĂ SE POATE STRICA', 'LA PRIMA PORNIRE'], 16: ['POMPĂ NOUĂ,', 'PILITURĂ VECHE'], 17: ['PE DINAFARĂ,', 'TOATE POMPELE', 'ARATĂ BINE']}
# numele cauzei (rosu), pe unul sau doua randuri
NAME = {1: ['AERUL RĂMAS DUPĂ', 'SCHIMBUL DE FILTRU'], 2: ['REZERVORUL GOLIT ȘI', 'MERSUL PE ULTIMII LITRI'], 3: ['BENZINA PUSĂ', 'DIN GREȘEALĂ'], 4: ['MOTORINA', 'CARE NU UNGE'],
        5: ['PARTICULELE ȘI', 'FILTRUL NESCHIMBAT'], 6: ['APA DIN MOTORINĂ'], 7: ['ADBLUE PUS ÎN', 'REZERVORUL DE MOTORINĂ'], 8: ['MOTORINA ÎMBĂTRÂNITĂ ȘI', 'BACTERIILE DIN REZERVOR'],
        9: ['FILTRUL ÎNFUNDAT ȘI', 'MOTORINA ÎNGHEȚATĂ'], 10: ['POMPA DE ALIMENTARE', 'DIN REZERVOR, SLĂBITĂ'], 11: ['AERUL TRAS', 'PE LA RACORDURI'], 12: ['REGULATORUL', 'DE DEBIT BLOCAT'],
        13: ['TACHETUL', 'POMPEI CP4'], 14: ['UZURA NORMALĂ ȘI', 'GARNITURILE ÎMBĂTRÂNITE'], 15: ['GREȘELILE', 'DE MONTAJ'], 16: ['POMPA SCHIMBATĂ FĂRĂ', 'CURĂȚAREA INSTALAȚIEI'],
        17: ['POMPA LA', 'MÂNA A DOUA']}
FIRST = {1: 'aerul', 2: 'rezervorul', 3: 'benzina', 4: 'motorina', 5: 'particulele', 6: 'apa', 7: 'adblue', 8: 'motorina', 9: 'filtrul', 10: 'pompa',
         11: 'aerul', 12: 'regulatorul', 13: 'tachetul', 14: 'uzura', 15: 'greselile', 16: 'pompa', 17: 'pompa'}
HASH = {1: '#schimbfiltru #filtrumotorina #amorsare', 2: '#rezervorgol #ultimiilitri', 3: '#benzinaindiesel #alimentaregresita', 4: '#motorina #lubrifiere',
        5: '#filtrumotorina #particule', 6: '#apainmotorina #rugina', 7: '#adblue #adblueinmotorina', 8: '#motorinaveche #bacterii', 9: '#filtruinfundat #iarna',
        10: '#pompaalimentare #pompadinrezervor', 11: '#aerininstalatie #racorduri', 12: '#regulatordebit #presiunerampa', 13: '#cp4 #boschcp4 #tachet',
        14: '#uzura #garnituri', 15: '#montaj #montajpompa', 16: '#pilitura #curatareinstalatie', 17: '#dezmembrari #pompasecondhand'}
# culorile din subtitrari, pe cuvinte: y = piesa / marime, r = defect, c = aer / apa / frig, g = rezolvare
KW = {'y': 'pompa pompe pompei pompele filtru filtrul filtrului filtre cama rola pistonul piston pistoane pistoanele pistonas pistonasul tachet tachetul regulator regulatorul '
           'rampa injectoare injectoarele rezervor rezervorul rezervorului rezervoarele motorina motorinei motorine retur supapa supape supapele garnitura garnituri garniturile '
           'racorduri racordurile conducta conducte conductele presiune presiunea debit debitul bari microni milimetru kilometri calculator calculatorul martorul arborele '
           'cilindru cilindri instalatia instalatiei instalatie separator separatorul sita demaror demarorul carcasa bila furtunurile coliere cuple cuplele pelicula ungere ungerea '
           'lubrifiant biodiesel biodieselul turbo doctor cp4',
      'r': 'zgarie zgariata zgariate zgarieturi pilitura uzura uzat uzata uzate uzeaza rugina roada roasa roase strica defecte defectul blocat intepenita intepenite crapa crapata '
           'crapate fisuri greu opreste opriri scade pierde pierdere pierderea eroarea erori erorile avarie paguba metal abraziv coroziv coroziunea corodate depuneri depunerile depun '
           'lacul rasini namol murdaria murdarie mizerie impuritati particule particulele particula praf nisip smirghel aschii fulgi fulgii infunda infometata flamanda strangulat '
           'ineaca gresit greseala nepotrivit netestata nesigure ghicite benzina benzinei bacterii ciuperci acizi acizii oxidare oxideaza imbatraneste imbatranita imbatranesc '
           'uscat goala gol slab slabeste lipsa bataie zgomot bazait neregulat',
      'c': 'aer aerul aerului bule bulele bula apa condens umezeala adblue uree cristale iarna frigul parafina grade minus',
      'g': 'eviti umple aeriseste aerisit procedura amorsare desfacem verificam reconditionam reconditionata testam testata curatam curatarea curatat curatata inlocuim inlocuiesc '
           'schimbam masuram cautam gasim garantie banc stand microscop ultrasunete test testul fisa proba corect corecta curat curata calitate interval intervalul recomandam'}
KWM = {w: c for c, ws in KW.items() for w in ws.split()}
TAGS = {}       # corecturi pe episod: {n: {rand: {cuvant: culoare | None}}}

def boom(t, dur, txt, y, size, col, frm=3.1, sh=18, ca=22, bg=.65, cg=.3, glow=None):
    g = f", glow: '{glow}'" if glow else ''
    return f"      {{ k: 'boom', t: {t}, dur: {dur}, txt: {json.dumps(txt, ensure_ascii=False)}, y: {y}, size: {size}, col: '{col}', from: {frm}, sh: {sh}, ca: {ca}, riser: false, bg: {bg}, cg: {cg}{g} }},"

def main():
    n = int(sys.argv[1]); R = sys.argv[2]; E = PD.EP[n - 1]; EP = f'{HERE}/ep{n}'
    c = json.load(open(f'{EP}/vo/cues.json')); L = c['lines']; NL = len(L)
    def W(i, w, k=0): return [x for x in c['words'] if x['win'] == i and nrm(x['text']) == nrm(w)][k]['s']
    T1 = L[0]['start'] + .02; TP = W(0, 'pompele') - .03; TI = W(0, 'inalta') - .03; T3 = W(0, 'cauza') - .03; T4 = W(0, FIRST[n]) - .03
    S1 = L[1]['start']; HK = L[2]['start'] - .3; o = NL - 3
    items = []; fx = []
    # 1. titlul din primele secunde (fara voce)
    H = HOOK[n]; nh = len(H); ys = [448, 606] if nh == 2 else [404, 528, 652]; T0 = .15; TE = L[0]['start'] - .1
    for k, line in enumerate(H):
        sz = fit(line, 140 if nh == 2 else 112); tk = T0 + .4 * k; last = k == nh - 1
        items.append(boom(f'{tk:.2f}', f'{TE - tk:.2f}', line, ys[k], sz, '#FFD21F' if last else '#FFFFFF'))
        fx.append(f"{{ k: 'punch', t: {tk:.2f}, a: {.1 if last else .08}, sh: {22 if last else 16} }}")
    fx.append(f"{{ k: 'glitch', t: {T0 + .4 * (nh - 1):.2f}, d: .14 }}")
    # 2. numele seriei, pe cuvintele vocii
    items.append(boom('T1', 'T3 - .12 - T1', 'DE CE SE STRICĂ', 404, 112, '#FFFFFF', frm=3.2, bg=.6))
    items.append(boom('TP', 'T3 - .12 - TP', 'POMPELE DE', 528, 112, '#FFFFFF', frm=3.1, bg=.5))
    items.append(boom('TI', 'T3 - .12 - TI', 'ÎNALTĂ PRESIUNE?', 652, fit('ÎNALTĂ PRESIUNE?', 124), '#FFD21F', frm=3.0, sh=20, ca=24, bg=.7))
    # 3. cauza si numele ei
    items.append(boom('T3', 'HK - .1 - T3', f'CAUZA {n} DIN {NT}', 430, 140, '#FFD21F', frm=3.2, bg=.6))
    nm = NAME[n]
    if len(nm) == 1:
        items.append(boom('T4', 'HK - .1 - T4', nm[0], 590, fit(nm[0], 160), '#FF4B4B', frm=3.0, sh=20, ca=24, bg=.7, glow='rgba(255,75,75,.6)'))
    else:
        sz = min(fit(nm[0], 150), fit(nm[1], 150))
        items.append(boom('T4', 'HK - .1 - T4', nm[0], 575, sz, '#FF4B4B', frm=3.0, sh=20, ca=24, bg=.7, glow='rgba(255,75,75,.6)'))
        items.append(boom('T4 + .1', 'HK - .2 - T4', nm[1], 575 + int(sz * 1.08), sz, '#FF4B4B', frm=3.0, sh=20, ca=24, bg=.4, cg=.2, glow='rgba(255,75,75,.6)'))
    items.append("      { k: 'chip', t0: S1 + .9, t1: HK - .15, y: 1226, ph: [[S1 + .9, 'eyes', 'TOATE CAUZELE: TIKTOK · FACEBOOK · YOUTUBE', 'yellow']] },")
    # culorile subtitrarilor
    tags = {}
    for i in range(2, o):
        t = {}
        for x in c['words']:
            if x['win'] == i and nrm(x['text']) in KWM: t[nrm(x['text'])] = KWM[nrm(x['text'])]
        for w, col in TAGS.get(n, {}).get(i, {}).items():
            if col is None: t.pop(w, None)
            else: t[w] = col
        tags[i] = t
    tags[1] = {'tiktok': 'c', 'facebook': 'c', 'youtubeul': 'c'}
    tags[o] = {'turbo': 'y', 'doctor': 'y', 'experti': 'y'}; tags[o + 1] = {'evita': 'g', 'tarziu': 'g'}; tags[o + 2] = {'diagnoza': 'g', 'gratuita': 'g'}
    js = f"""// v2 – Seria „De ce se strică pompele de înaltă presiune”, cauza {n} din {NT}: {E['nume']} (21.11.2026)
// Reel animat 3D în secțiune (plăci Blender + montaj în Python, sursa în tools/anim_serie_pompe, episodul ep{n}), cu vocea „Sabin” din ElevenLabs, rând cu rând.
// Formula seriilor: titlul-cârlig în primele 3 secunde, apoi numele seriei, „cauza X din {NT}” și numele cauzei; la sfârșit „Ce facem noi la Turbo Doctor”,
// „La Turbo Doctor suntem experți…” și ecranul de final cu diagnoză gratuită, numărul de telefon și pictogramele serviciilor (endPhone + endIcons).
// Etichetele de pe piese, insigna „Cauza {n} din {NT}” și marcajul din fundal sunt în cadre; aici sunt titlurile boom, subtitrările și ecranul de final.
window.REEL_CFG = ({{ aw, ew, S0, SEND, TEND }}) => {{
  const T1 = {T1:.2f}, TP = {TP:.2f}, TI = {TI:.2f}, T3 = {T3:.2f}, T4 = {T4:.2f}, S1 = {S1:.2f}, HK = {HK:.2f};
  return {{
    hook: null,
    stages: null,
    endIcons: true,
    endPhone: true,
    hideCap: [[0, S1 - .1]],
    items: [
{chr(10).join(items)}
    ],
    fx: [
      {', '.join(fx)},
      {{ k: 'punch', t: T1, a: .08, sh: 16 }}, {{ k: 'punch', t: TI, a: .1, sh: 22 }}, {{ k: 'glitch', t: TI, d: .14 }},
      {{ k: 'punch', t: T3, a: .08, sh: 16 }}, {{ k: 'punch', t: T4, a: .14, sh: 30 }}, {{ k: 'glitch', t: T4, d: .18 }},
    ],
    bgFix: [[0, SEND]],
    tags: {json.dumps({str(k): v for k, v in sorted(tags.items())}, ensure_ascii=False)},
  }};
}};
"""
    open(f'{R}/reel.js', 'w').write(js)
    json.dump({'t': round(T0 + .4 * (nh - 1) + 1.3, 2)}, open(f'{R}/out/cover_t.json', 'w'))
    # textul postarii, din textul vocii
    sc = json.load(open(f'{EP}/vo_script.json')); tx = [re.sub(r'\{([^|}]*)\|[^}]*\}', r'\1', l['text']) for l in sc][2:o]
    # in textul scris, cifrele se scriu cu cifre (vocea le are in litere, pentru pronuntie)
    for a, b in (('douăsprezece luni', '12 luni'), ('două mii patru sute de bari', '2.400 de bari'), ('patru sute șaizeci de microni', '460 de microni'),
                 ('două mii de bari', '2.000 de bari'), ('șapte la sută', '7%'), ('minus șapte grade', 'minus 7 grade')):
        tx = [t.replace(a, b) for t in tx]
    ie = next((i for i, t in enumerate(tx) if t.startswith('Cum eviți')), len(tx)); iw = next((i for i, t in enumerate(tx) if t.startswith('Ce facem noi')), len(tx))
    body = ' '.join(tx[:min(ie, iw)]); ev = ' '.join(tx[ie:iw]) if ie < iw else ' '.join(tx[ie:]); we = ' '.join(tx[iw:]) if iw < len(tx) else ''
    ttl = f"cauza {n} din {NT}: {E['nume']}"
    yt = f"De ce se strică pompele de înaltă presiune? {ttl[0].upper() + ttl[1:]}"
    if len(yt) > 100: yt = f"Pompe de înaltă presiune, {ttl}"
    post = f"""TITLU (YouTube): {yt}
TITLU (TikTok): De ce se strică pompele de înaltă presiune · {ttl}

TEXT POSTARE:
Seria „De ce se strică pompele de înaltă presiune” · {ttl}. ⚙️

🔧 {body}
""" + (f"\n✅ {ev}\n" if ev else '') + (f"\n🛠️ {we}\n" if we else '') + f"""
Urmărește pagina pentru toate cele {NT} cauze.

📍 Turbo Doctor · Galați · București · Iași · Piatra Neamț · diagnoză gratuită · 0739 065 065

#turbodoctor #pompadeinaltapresiune #pompadeinalta #commonrail #diesel #reconditionarepompe {HASH[n]} #decesestricapompeledeinaltapresiune
"""
    os.makedirs(f'{HERE}/post', exist_ok=True); open(f'{HERE}/post/ep{n}.txt', 'w').write(post)
    print(n, 'ok', round(T1, 2), round(TP, 2), round(TI, 2), round(T3, 2), round(T4, 2), round(S1, 2), round(HK, 2), '| yt', len(yt))
main()
