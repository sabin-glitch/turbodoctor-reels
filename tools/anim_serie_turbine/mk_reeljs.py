"""Writes reel.js for each episode of the series from its voice cues (numbers baked in, so the hook titles sit on the words)."""
import json, unicodedata, sys
slugs = json.load(open('slugs.json'))
EPS = {
 1: dict(name='LIPSA UNGERII', size=160, first='lipsa', desc='lipsa ungerii',
         tags={2:{'300000':'y','film':'y','ulei':'y','pluteste':'y'},3:{'metalul':'r','metal':'r','freaca':'r'},4:{'incing':'r','gripeaza':'r','rupe':'r'},
               5:{'nivel':'r','scazut':'r','pompa':'r','slabita':'r','depuneri':'r'},6:{'noua':'c','fara':'r','amorsata':'r'},7:{'turezi':'r','rece':'c'},
               8:{'eviti':'g','nivel':'g','timp':'g','curate':'g','fara':'g'}}),
 2: dict(name='ULEIUL MURDAR', size=160, first='uleiul', desc='uleiul murdar',
         tags={2:{'film':'y','ulei':'y','pluteste':'y'},3:{'murdar':'r','particulele':'r','smirghel':'r'},4:{'zgarie':'r','jocul':'r','creste':'r'},5:{'bata':'r','carcasa':'r','distrusa':'r'},
               6:{'mizeria':'r','amanat':'r','infunda':'r','ocolire':'y','nefiltrat':'r'},7:{'funinginea':'r','motorina':'r','spanul':'r'},8:{'eviti':'g','timp':'g','noi':'g','noua':'c'}}),
 3: dict(name='OPRIREA LA CALD', size=140, first='oprirea', desc='oprirea motorului la cald',
         tags={2:{'fierbinte':'r'},3:{'uleiul':'y','caldura':'r'},4:{'opresti':'r','imediat':'r','pompa':'y','loc':'r'},5:{'caldura':'r','coace':'r','calamina':'r'},
               6:{'calamina':'r','infunda':'r','putin':'r'},7:{'cedeaza':'r','lagarul':'y','segmentul':'y'},8:{'eviti':'g','ralanti':'g','minut':'g','trei':'g','minute':'g'},9:{'linistit':'g','raceasca':'c'}}),
 4: dict(name='ULEIUL NU SE MAI SCURGE', size=96, first='uleiul', desc='uleiul care nu se mai poate scurge',
         tags={2:{'presiune':'y','singur':'y','retur':'y'},3:{'infundat':'r','calamina':'r','indoit':'r'},4:{'carter':'y','presiune':'r','infundata':'r','uzati':'r','milibari':'y'},
               5:{'aduna':'r','impins':'r','etansari':'y','admisie':'c','evacuare':'r'},6:{'fum':'c','albastru':'c','intercooler':'c','consum':'r','cauza':'y'},
               7:{'ars':'r','incleiaza':'r','supraturari':'r','necontrolate':'r'},8:{'problema':'r','ramane':'r'},9:{'eviti':'g','curat':'g','corect':'g','silicon':'y','verificata':'g','maxim':'g'}}),
 5: dict(name='CORPURI STRĂINE: ADMISIE', size=90, first='corpurile', desc='corpurile străine din admisie',
         tags={2:{'aluminiu':'y','300000':'y'},3:{'loveste':'r','paletele':'y','nisip':'r','saiba':'r','gheata':'r'},4:{'ciupita':'r','indoita':'r','dezechilibreaza':'r','lagarele':'y'},
               5:{'rupt':'r','infundat':'r','lipseste':'r','fisurat':'r','nefiltrat':'r'},6:{'uitate':'r','surub':'r','saiba':'r','piulita':'r'},7:{'repetate':'r','noua':'c','cedeaza':'r'},
               8:{'eviti':'g','calitate':'g','timp':'g','fara':'g','cureti':'g'}}),
 6: dict(name='CORPURI STRĂINE: EVACUARE', size=86, first='corpurile', desc='corpurile străine din evacuare',
         tags={2:{'cilindru':'y','galeria':'y','turbinei':'y'},3:{'rupe':'r','supapa':'r','segment':'r','galerie':'r','paletele':'y'},4:{'rup':'r','indoaie':'r'},5:{'rupte':'r','dezechilibrat':'r'},
               6:{'victima':'y','motor':'r'},7:{'noua':'c','resturile':'r','distrug':'r'},8:{'eviti':'g','gasesti':'g','repari':'g','cureti':'g'}}),
 7: dict(name='GAZE PREA FIERBINȚI', size=113, first='temperatura', desc='temperatura prea mare a gazelor de evacuare',
         tags={2:{'plaja':'y','temperaturi':'y'},3:{'depasesc':'r','crapa':'r','oboseste':'r','coace':'r'},4:{'calamina':'r','infunda':'r','ungerii':'y'},5:{'secunde':'r'},
               6:{'soft':'r','modificat':'r','ardere':'r','injectie':'r','injectoare':'y','pompa':'y'},7:{'oprirea':'r','cald':'r'},8:{'eviti':'g','parametri':'g','verificate':'g','fara':'g'}}),
 8: dict(name='SUPRATURAREA', size=160, first='supraturarea', desc='supraturarea',
         tags={2:{'maxima':'y','centrifuga':'r','aluminiu':'y'},3:{'creste':'r','atinge':'r','rupe':'r'},4:{'coaja':'y','portocala':'y','supraturarii':'r'},5:{'secunde':'r'},
               6:{'soft':'r','modificat':'r','blocata':'r','inchis':'r','calamina':'r','fisurat':'r','actuatorul':'y','membrana':'y'},7:{'repetate':'r','obosesc':'r'},8:{'eviti':'g','fara':'g','curata':'g','verificata':'g'}}),
 9: dict(name='GEOMETRIA BLOCATĂ', size=126, first='geometria', desc='geometria variabilă blocată',
         tags={2:{'palete':'y','mobile':'y','inchid':'c','deschid':'c'},3:{'funinginea':'r','ars':'r','intepenesc':'r'},4:{'deschis':'r','presiune':'y','avarie':'r'},5:{'inchis':'r','maxima':'y','supraturarea':'r'},
               6:{'funingine':'r','recircularea':'y','proasta':'r','carter':'y','scurte':'r'},7:{'eviti':'g','curat':'g','buna':'g','lung':'g'}}),
 10: dict(name='DPF ÎNFUNDAT', size=160, first='filtrul', desc='filtrul de particule înfundat',
         tags={2:{'plin':'r','dop':'r'},3:{'fierbinti':'r','presiunea':'r','temperatura':'r'},4:{'etansare':'y','coc':'r','infunda':'r','uzeaza':'r'},5:{'impins':'r','compresorului':'c','calamina':'r'},
               6:{'crapa':'r','oboseala':'r'},7:{'noua':'c','fara':'r','cedeze':'r'},8:{'eviti':'g','verifici':'g','curatarea':'g'}}),
 11: dict(name='SCĂPĂRI ȘI ÎNFUNDĂRI', size=107, first='scăpările', desc='scăpările și înfundările de pe traseul de aer și de gaze',
         tags={2:{'scapare':'r','infundare':'r'},3:{'infundat':'r','vid':'r','ulei':'y'},4:{'fisurat':'r','slabit':'r','repede':'r'},5:{'crapata':'r','lipsa':'r','fura':'r'},6:{'infundat':'r','caldura':'r'},
               7:{'suieratul':'y','negru':'r','putere':'r','uleiul':'y'},8:{'eviti':'g','timp':'g','verificate':'g','ignora':'g'}}),
 12: dict(name='GREȘELILE DE MONTAJ', size=113, first='greșelile', desc='greșelile de montaj',
         tags={2:{'noi':'c','montaj':'r'},3:{'prima':'y','amorsata':'r','turat':'r'},4:{'doua':'y','silicon':'r','invers':'r','ingusteaza':'r'},5:{'treia':'y','vechi':'r','calamina':'r'},
               6:{'patra':'y','neschimbate':'r','resturile':'r'},7:{'regula':'y','cauza':'y'},8:{'eviti':'g','amorsata':'g','noi':'g','curatate':'g','corecte':'g','fara':'g'}}),
 13: dict(name='UZURA MOTORULUI', size=140, first='uzura', desc='uzura motorului',
         tags={2:{'segmentii':'y','cilindrii':'y','scapa':'r','carter':'y'},3:{'presiunea':'r','scurge':'r','impins':'r'},4:{'funingine':'r','murdar':'r','zgarie':'r'},5:{'albastru':'c','consum':'r','ambele':'y'},
               6:{'martorul':'y','bolnavul':'r'},7:{'motorul':'y','sanatos':'g'},8:{'eviti':'g','verifici':'g'}}),
}
ONLY = [int(x) for x in sys.argv[1:]]
def nrm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if c.isalnum() and unicodedata.category(c) != 'Mn')
for n, E in EPS.items():
    if ONLY and n not in ONLY: continue
    c = json.load(open(f'ep{n}/vo/cues.json')); L = c['lines']; NL = len(L)
    def W(i, w, k=0): return [x for x in c['words'] if x['win'] == i and nrm(x['text']) == nrm(w)][k]['s']
    T1 = L[0]['start'] + .02; T2 = W(0, 'turbinele') - .03; T3 = W(0, 'cauza') - .03; T4 = W(0, E['first']) - .03
    HK = L[2]['start'] - .3; S1 = L[1]['start']
    tags = dict(E['tags']); o = NL - 3
    tags[1] = {'tiktok': 'c', 'facebook': 'c', 'youtubeul': 'c'}
    tags[o] = {'turbo': 'y', 'doctor': 'y', 'experti': 'y'}; tags[o + 1] = {'evita': 'g', 'tarziu': 'g'}; tags[o + 2] = {'diagnoza': 'g', 'gratuita': 'g'}
    js = f"""// v2 – Seria „De ce se strică turbinele”, cauza {n} din 13: {E['desc']} (15.11.2026)
// Reel animat 3D în secțiune (tools/anim_serie_turbine, episodul ep{n}), cu vocea „Sabin” din ElevenLabs, rând cu rând.
// Cerut de Sabin: fiecare film începe cu numele seriei și „cauza X din 13”, se termină cu „La Turbo Doctor suntem experți…”
// și cu ecranul de final cu diagnoză gratuită, numărul de telefon și pictogramele serviciilor (endPhone + endIcons).
// Etichetele de pe piese și eticheta „Cauza {n} din 13” sunt în animație; compozitorul pune titlurile boom din hook, subtitrările și ecranul de final.
window.REEL_CFG = ({{ aw, ew, S0, SEND, TEND }}) => {{
  const T1 = {T1:.2f}, T2 = {T2:.2f}, T3 = {T3:.2f}, T4 = {T4:.2f}, S1 = {S1:.2f}, HK = {HK:.2f};
  return {{
    hook: null,
    stages: null,
    endIcons: true,
    endPhone: true,
    hideCap: [[0, S1 - .1]],
    items: [
      {{ k: 'boom', t: T1, dur: T3 - .12 - T1, txt: 'DE CE SE STRICĂ', y: 448, size: 132, col: '#FFFFFF', from: 3.2, sh: 18, ca: 22, riser: false, bg: .6, cg: .3 }},
      {{ k: 'boom', t: T2, dur: T3 - .12 - T2, txt: 'TURBINELE?', y: 612, size: 180, col: '#FFD21F', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3 }},
      {{ k: 'boom', t: T3, dur: HK - .1 - T3, txt: 'CAUZA {n} DIN 13', y: 455, size: 150, col: '#FFD21F', from: 3.2, sh: 18, ca: 22, riser: false, bg: .6, cg: .3 }},
      {{ k: 'boom', t: T4, dur: HK - .1 - T4, txt: '{E['name']}', y: 612, size: {E['size']}, col: '#FF4B4B', from: 3.0, sh: 20, ca: 24, riser: false, bg: .7, cg: .3, glow: 'rgba(255,75,75,.6)' }},
      {{ k: 'chip', t0: S1 + .9, t1: HK - .15, y: 1226, ph: [[S1 + .9, 'eyes', 'TOATE CAUZELE: TIKTOK · FACEBOOK · YOUTUBE', 'yellow']] }},
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
    open(f"/home/claude/reels/{slugs[str(n)]}/reel.js", 'w').write(js)
    json.dump({'t': round(T4 + .9, 2)}, open(f"/home/claude/reels/{slugs[str(n)]}/out/cover_t.json", 'w'))
    print(n, 'ok', T1, T2, T3, T4, HK)
