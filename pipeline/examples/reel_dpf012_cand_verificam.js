// v2 – DPF Doctor · „Când verificăm prima dată filtrul de particule?” (TikTok 7693999509533134102, 1:28)
// Footage exactly as filmed: engine/DPF cutaway with his voice (0–7.5 s), selfie, cutaways (35–61 s), selfie. Natural pace, no separate hook.
// Old static title „Când verificăm Filtrul de particule?” removed (caption_clean --band); it is now the hook.
// Very close selfie (face y 380–1770): selfie graphics stay in the top band; the schematic goes over the cutaway.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    la3: W('la', 3.04), verificam: W('verificăm', 5.52), particuleE0: WE('particule', 6.56), iar: W('Iar', 8.28), n100: W('100.000', 11.55), diagnoza14: W('diagnoză', 14.35), incarcareE: WE('încărcare', 16.91),
    dar20: W('Dar', 20.06), diagnoza24: W('diagnoză', 24.65), admisie28: W('admisie', 28.41), injectie29: W('injecție', 29.62), evacuare30: W('evacuare', 30.49), senzorii: W('senzorii', 31.61), sistemeE: WE('sisteme', 34.97),
    asta: W('Asta', 35.86), infunda: W('înfundă', 39.69), singurE: WE('singur', 40.73), de41: W('De', 41.69), cauzate: W('cauzate', 47.36), admisie51: W('admisie', 51.12), injectie51: W('injecție', 51.6),
    evacuare52: W('evacuare', 52.32), alte54: W('alte', 54.01), motor55: W('motor', 55.36), incapacitate: W('incapacitate', 58.4), particuleE61: WE('particule', 61.6),
    astfel: W('Astfel', 62.68), puteti: W('puteți', 66.2), voastreE: WE('voastre', 69.31), la70: W('La', 70.33), bucuresti: W('București', 72.24), iasi: W('Iași', 72.96), galati: W('Galați', 73.44), piatra: W('Piatra', 74.16),
    diagnoza75: W('diagnoza', 75.04), gratuita: W('gratuită', 76.32), in77: W('în', 77.05), dar80: W('Dar', 80.38), m1015: W('10-15', 84.71), gratuitE: WE('gratuit', 86.93),
  };
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF', l1: 'LA CÂȚI <span class="y">KILOMETRI</span>', l1At: A.la3 - .05, l2: 'VERIFICI DPF-UL?', l2At: A.verificam - .04, l2Col: '#62D8FF', end: A.particuleE0 + .5 },
    hideCap: [[0, A.particuleE0 + .45]],
    stages: [[A.iar - .1, 'CÂND?'], [A.dar20 - .1, 'CE VERIFICĂM'], [A.asta - .1, 'DE CE'], [A.astfel - .1, 'SOLUȚIA']],
    tags: {
      0: { kilometri: 'y', verificam: 'g' }, 1: { simplu: 'g', km: 'y', diagnoza: 'g', incarcare: 'y' }, 2: { important: 'y', diagnoza: 'g' }, 3: { senzorii: 'c', clapete: 'c' },
      4: { infunda: 'r', singur: 'r' }, 5: { probleme: 'r', cauzate: 'r', componente: 'c' }, 6: { incapacitate: 'r', regenerare: 'g' }, 7: { verificand: 'g', timp: 'g', evita: 'g', defectiuni: 'r' },
      8: { bucuresti: 'y', iasi: 'y', galati: 'y', piatra: 'y', neamt: 'y', diagnoza: 'g', complet: 'g', gratuita: 'g', programari: 'c' }, 9: { minute: 'y', complet: 'g', gratuit: 'g' },
    },
    items: [
      { k: 'stat', t0: A.iar - .1, t1: A.incarcareE + .4, top: 262, sc: .88, title: 'PRIMA VERIFICARE A DPF', ico: 'counter', to: 100000, step: 1000, at: A.n100 - .3, dur: .9, unit: 'KM',
        sub: 'diagnoză: starea de încărcare', subIco: 'stethoscope' },
      { k: 'pipe', t0: A.dar20 - .1, t1: A.sistemeE + .3, top: 262, sc: .9, ico: 'stethoscope', title: 'DIAGNOZA COMPLETĂ (+ SENZORI ȘI CLAPETE)',
        steps: [[A.diagnoza24 - .05, 'soap', 'DPF'], [A.admisie28 - .05, 'dashing_away', 'ADMISIE'], [A.injectie29 - .05, 'droplet', 'INJECȚIE'], [A.evacuare30 - .05, 'fire', 'EVACUARE']] },
      // cutaway: engine section + DPF
      { k: 'stamp', t: A.infunda - .03, t1: A.de41 - .1, y: 330, txt: 'NU SE ÎNFUNDĂ SINGUR!', col: 'red', s: .58, rot: -4 },
      { k: 'schem', t0: A.de41 - .1, t1: A.particuleE61 + .4, top: 262, sc: .86, type: 'systemMap', title: 'SCHEMĂ · DE UNDE VIN PROBLEMELE DPF', sub: 'CAUZE', stepNames: ['FAPT', 'CAUZE', 'CAUZE', 'EFECT'],
        P: { nodes: [[150, 70, 'ADMISIE', 'dashing_away'], [457, 70, 'INJECȚIE', 'droplet'], [764, 70, 'EVACUARE', 'fire'], [457, 215, 'MOTOR', 'gear'], [457, 360, 'DPF', 'warning']],
          links: [[0, 3], [1, 3], [2, 3], [3, 4]],
          events: [[A.admisie51, 0, 'bad'], [A.injectie51, 1, 'bad'], [A.evacuare52, 2, 'bad'], [A.motor55, 3, 'bad'], [A.incapacitate, 4, 'bad']] },
        steps: [[A.de41 - .1, 'Problemele DPF-ului au, de fapt, alte cauze', ''], [A.cauzate - .05, 'Admisie, injecție, evacuare...', 'r'], [A.alte54 - .05, '...sau alte componente din motor', 'r'],
          [A.incapacitate - .1, 'Iar DPF-ul nu se mai poate regenera corect', 'r']] },
      // selfie: solution
      { k: 'chip', t0: A.astfel - .1, t1: A.voastreE + .3, y: 300, ph: [[A.astfel - .1, 'check_mark_button', 'VERIFICĂ TOTUL DIN TIMP', 'green'], [A.puteti - .05, 'shield', 'EVIȚI DEFECȚIUNI MARI', 'green']] },
      { k: 'chip', t0: A.la70 - .1, t1: A.dar80 - .25, y: 300, ph: [[A.la70 - .1, 'round_pushpin', 'TURBO DOCTOR', ''], [A.bucuresti - .05, 'round_pushpin', 'BUCUREȘTI', ''], [A.iasi - .05, 'round_pushpin', 'IAȘI', ''],
        [A.galati - .05, 'round_pushpin', 'GALAȚI', ''], [A.piatra - .05, 'round_pushpin', 'PIATRA NEAMȚ', 'blue'], [A.diagnoza75 - .05, 'stethoscope', 'DIAGNOZĂ COMPLET GRATUITĂ', 'green'],
        [A.in77 - .05, 'calendar', 'PE BAZĂ DE PROGRAMARE', 'blue']] },
      { k: 'stat', t0: A.m1015 - .55, t1: SEND - .05, top: 262, sc: .88, title: 'VERIFICAREA DUREAZĂ', ico: 'stopwatch', from: 0, to: 15, at: A.m1015 - .3, dur: .7, fmt: v => v < 10 ? String(v) : '10–15',
        unit: 'MIN', sub: 'complet gratuit', subIco: 'check_mark_button' },
    ],
    fx: [
      { k: 'punch', t: A.n100, a: .04, sh: 4 },
      { k: 'punch', t: A.infunda, a: .05, sh: 6 }, { k: 'red', t0: A.infunda - .05, t1: A.singurE + .3, max: 1.2 },
      { k: 'red', t0: A.incapacitate - .05, t1: A.incapacitate + 1.0, max: 1.0 },
      { k: 'green', t0: A.gratuita - .05, t1: A.gratuita + .9 },
      { k: 'green', t0: A.gratuitE - .5, t1: A.gratuitE + .3, silent: true },
    ],
    sfx: [],
    bursts: [[A.gratuita, 540, 300, 6, 300, .7]],
  };
};
