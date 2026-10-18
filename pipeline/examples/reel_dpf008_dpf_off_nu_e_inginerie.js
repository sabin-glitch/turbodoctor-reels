// v2 – DPF Doctor · „DPF OFF nu e inginerie” (TikTok 7688412379931053334, 2:10, răspuns la comentariu, selfie pe balcon)
// Footage exactly as filmed, natural pace, no separate hook. Very close selfie (face y 400–1550): graphics only in the top band
// (stage bar, chips y 300, compact cards from y 262) — never over the face. The TikTok reply bubble (0–5.4 s) is covered by our comment card.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    operatiune: W('operațiune', 5.84), complexa: W('complexă', 6.96), offE0: WE('OFF', 9.36), uite: W('Uite', 10.3), bormasina: W('bormașină', 13.66), makita: W('Makita', 14.69),
    ca17: W('ca', 16.77), offE1: WE('OFF', 18.11), la19: W('La', 19.13), sute: W('sute', 20.85), procesul: W('procesul', 23.04), dpf24: W('DPF', 24.76), ilegal: W('ilegal', 26.19),
    putem: W('Putem', 28.03), dar33: W('dar', 32.99), alegem: W('alegem', 36.73), clientii: W('clienții', 39.84), mediu: W('mediu', 41.76), mediuE: WE('mediu', 41.76),
    iar: W('Iar', 43.03), scoate: W('scoate', 49.05), kmE: WE('kilometraj', 54.16), ca55: W('Ca', 55.48), doua: W('două', 58.67), trebuie60: W('trebuie', 60.83), eiE63: WE('ei', 63.03),
    de63: W('De', 63.58), dpfuri: W('DPF-uri', 65.25), turbine: W('turbine', 66.77), injectoare: W('injectoare', 67.41), motoare: W('motoare', 68.13), capcoada: W('cap-coadă', 73.01), trebuieE78: WE('trebuie', 78.05),
    dpful79: W('DPF-ul', 79.1), admisie: W('admisie', 82.77), daca85: W('Dacă', 85.59), se89: W('Se', 88.94), infunda: W('înfunda', 89.5), nouE: WE('nou', 90.3),
    n60: W('60', 91.39), p70: W('70%', 92.27), lucruriE: WE('lucruri', 101.23), si102: W('Și', 102.2), ele: W('Ele', 107.39), eiE110: WE('ei', 109.95),
    dpful110: W('DPF-ul', 110.81), primul: W('primul', 113.24), daca116: W('dacă', 116.72), costurile: W('costurile', 118.55), in120: W('În', 120.14), dpfOff: W('DPF', 123.82),
    lasi: W('lași', 124.96), mergi: W('mergi', 128.38), fara: W('fără', 129.66), problemeE: WE('probleme', 129.98),
  };
  const BUBBLE_OUT = 5.4;   // the TikTok reply bubble disappears here
  return {
    // hook lines appear when the reply bubble is gone; tag on its own line at the top
    hook: { tag: 'RĂSPUNS LA COMENTARIU · DPF OFF', tagY: 175, l1: '„MARE <span class="y">INGINERIE</span>”', l1At: BUBBLE_OUT + .05, l2: 'SĂ FACI DPF OFF?!', l2At: A.complexa - .04, l2Col: '#FF3B30',
      y: -20, end: A.offE0 + .3 },
    stages: [[A.uite - .1, 'COMENTARIUL'], [A.la19 - .1, 'REALITATEA'], [A.dpful79 - .1, 'CAUZA'], [A.dpful110 - .1, 'SOLUȚIA']],
    tags: {
      0: { inginerie: 'y', off: 'r', complexa: 'y' }, 1: { bormasina: 'y', makita: 'y', off: 'r' }, 2: { activat: 'g', sute: 'g' }, 3: { off: 'r', ilegal: 'r' },
      4: { corecte: 'g', termen: 'g', lung: 'g', mediu: 'g' }, 5: { curatatul: 'g' }, 6: { cenusa: 'y', regenerare: 'g' }, 7: { paste: 'y', craciun: 'y', mintile: 'g' },
      8: { turbine: 'c', injectoare: 'c', motoare: 'c', capcoada: 'g', curatate: 'g' }, 9: { problema: 'r', admisie: 'c', injectie: 'c', motor: 'c' },
      10: { infunda: 'r', nou: 'r' }, 11: { nespecializate: 'r', eroare: 'r' }, 12: { mintile: 'g' }, 13: { primul: 'y', semn: 'y', timp: 'g' },
      14: { scad: 'g', off: 'r', on: 'g', fara: 'g', probleme: 'g' },
    },
    items: [
      // the comment he answers (covers the burned TikTok reply bubble, same place, until it disappears)
      { k: 'note', t0: 0, t1: BUBBLE_OUT, hard: true, box: [64, 304, 584, 686], fs: 34, label: 'COMENTARIU',
        text: '„Păi voi nu puteți face DPF OFF. Voi le spălați și țin la fel ca spălatul covoarelor: le speli de 2 ori pe an, de Paște și de Crăciun.”' },
      { k: 'chip', t0: A.uite - .1, t1: A.la19 - .3, y: 300, ph: [[A.uite - .1, 'wrench', 'DONEAZĂ-NE O BORMAȘINĂ...', 'yellow'], [A.ca17 - .05, 'scissors', '...CA SĂ FACEM ȘI NOI DPF OFF', 'red']] },
      // reality
      { k: 'chip', t0: A.la19 - .1, t1: A.dpf24 - .25, y: 300, ph: [[A.la19 - .1, 'check_mark_button', 'SUTE DE DPF-URI REACTIVATE', 'green'], [A.procesul - .05, 'gear', 'PROCESUL INVERS', 'blue']] },
      { k: 'stamp', t: A.ilegal - .03, t1: A.putem - .3, y: 320, txt: 'DPF OFF = ILEGAL', col: 'red', s: .62, rot: -4 },
      { k: 'chip', t0: A.putem - .1, t1: A.alegem - .3, y: 300, ph: [[A.putem - .1, 'thinking_face', 'PUTEAM FACE ȘI DPF OFF...', 'yellow'], [A.dar33 - .05, 'check_mark_button', '...DAR ALEGEM CE E CORECT', 'green']] },
      { k: 'chip', t0: A.alegem - .1, t1: A.mediuE + .3, y: 300, ph: [[A.alegem - .1, 'handshake', 'CORECT, PE TERMEN LUNG', 'green'], [A.clientii - .05, 'leaf', 'PENTRU CLIENȚI ȘI MEDIU', 'green']] },
      { k: 'def', t0: A.iar - .1, t1: A.kmE + .3, top: 262, sc: .92, term: 'CURĂȚAREA DPF', text: 'Scoate cenușa pe care regenerarea nu o mai poate scoate, după un anumit kilometraj.' },
      { k: 'chip', t0: A.ca55 - .1, t1: A.eiE63 + .3, y: 300, ph: [[A.ca55 - .1, 'calendar', '„DE PAȘTE ȘI DE CRĂCIUN”?', 'yellow'], [A.trebuie60 - .05, 'wrench', 'FĂ MAȘINA SĂ MEARGĂ CORECT', 'green']] },
      { k: 'pipe', t0: A.de63 - .1, t1: A.trebuieE78 + .3, top: 262, sc: .9, ico: 'hammer_and_wrench', title: 'TURBO DOCTOR: MAȘINA CAP-COADĂ',
        steps: [[A.dpfuri - .05, 'soap', 'DPF'], [A.turbine - .05, 'gear', 'TURBINE'], [A.injectoare - .05, 'droplet', 'INJECTOARE'], [A.motoare - .05, 'wrench', 'MOTOARE']] },
      // cause
      { k: 'chip', t0: A.dpful79 - .1, t1: A.daca85 - .25, y: 300, ph: [[A.dpful79 - .1, 'warning', 'DPF CU PROBLEME = SEMNAL', 'red'], [A.admisie - .05, 'magnifying_glass_tilted_left', 'ADMISIE · INJECȚIE · MOTOR', 'blue']] },
      { k: 'chip', t0: A.daca85 - .1, t1: A.se89 - .2, y: 300, ph: [[A.daca85 - .1, 'soap', 'DOAR ÎL CURĂȚI?', 'yellow']] },
      { k: 'stamp', t: A.se89 - .03, t1: A.nouE + .5, y: 320, txt: 'SE ÎNFUNDĂ DIN NOU', col: 'red', s: .6, rot: -4 },
      { k: 'stat', t0: A.n60 - .15, t1: A.lucruriE + .4, top: 262, sc: .9, title: 'ATELIERE NESPECIALIZATE', ico: 'warning', from: 0, to: 70, at: A.n60, dur: 1.0,
        fmt: v => v < 60 ? v + '%' : '60–70%', sub: 'doar curăță DPF-ul când apare eroarea' },
      { k: 'chip', t0: A.si102 - .1, t1: A.eiE110 + .3, y: 300, ph: [[A.si102 - .1, 'gear', 'NU DOAR PENTRU DPF...', 'blue'], [A.ele - .05, 'automobile', '...CI CA MAȘINA SĂ MEARGĂ BINE', 'green']] },
      // solution
      { k: 'chip', t0: A.dpful110 - .1, t1: A.costurile - .25, y: 300, ph: [[A.dpful110 - .1, 'bell', 'DPF-UL E PRIMUL SEMNAL', 'yellow'], [A.daca116 - .05, 'hourglass', 'INTERVINO LA TIMP', 'green']] },
      { k: 'cmp', t0: A.costurile - .1, t1: SEND - .05, top: 262, sc: .92, title: 'ÎN URMĂTOARELE 12 LUNI', ico: 'calendar', aCls: 'bad', bCls: 'ok',
        a: [A.in120 - .05, 'scissors', 'DPF OFF', 'MOTOR + TURBINĂ'], b: [A.lasi - .05, 'check_mark_button', 'DPF ON + REPARAȚIE', 'FĂRĂ PROBLEME'] },
    ],
    fx: [
      { k: 'punch', t: A.ilegal, a: .05, sh: 6 }, { k: 'red', t0: A.ilegal - .05, t1: A.ilegal + 1.2, max: 1.2 },
      { k: 'green', t0: A.mediu - .05, t1: A.mediuE + .5, silent: true },
      { k: 'punch', t: A.infunda, a: .05, sh: 6 }, { k: 'red', t0: A.infunda - .05, t1: A.nouE + .3, max: 1.1 },
      { k: 'green', t0: A.costurile - .05, t1: A.costurile + .8, silent: true },
      { k: 'green', t0: A.fara - .05, t1: A.problemeE + .3 },
    ],
    sfx: [],
    bursts: [[A.fara, 540, 360, 6, 320, .7]],
  };
};
