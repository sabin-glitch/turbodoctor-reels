// v2 – DPF Doctor · „Top 3 lucruri care îți strică DPF-ul” (TikTok 7689702802909695254, 4:30, selfie în atelier)
// Footage exactly as filmed (selfie + short cutaways: engine 6 s, DPF on the floor and engine block ~78–86 s), natural pace, no separate hook.
// Old burned title „Top 3 lucruri ce îți distrug DPF-ul” removed (caption_clean --band) → it is the hook now.
// Very close selfie: graphics compact in the top band (stage bar, chips y 330, short cards from y 262), never over the face.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    top: W('Top', .47), strica: W('strică', 2.98), particuleE0: WE('particule', 5.58),
    filtrul1: W('Filtrul', 7.58), dupa: W('după', 9.89), doar: W('doar', 12.93), pm1: W('PM2.5', 14.21), cancerul: W('cancerul', 17.49), dar1: W('Dar', 18.6), ca2: W('că', 21.73), plat: W('plat', 26.93), asaE2: WE('așa', 27.73),
    incepem: W('Începem', 28.6), trei: W('3', 29.39), exploatezi: W('exploatezi', 31.39), inseamna34: W('Înseamnă', 34.51), regenerari38: W('regenerări', 39.6),
    regenerarea42: W('Regenerarea', 42.1), drum: W('drum', 44.81), temperatura: W('temperatură', 48.17), turatia: W('turația', 51.5), asta54: W('Asta', 54.01), luna: W('lună', 56.64), oras59: W('oraș', 59.68),
    daca63: W('Dacă', 63.13), subturat: W('subturat', 65.04), vacanta: W('vacanță', 68.8), probabil: W('probabil', 72.31), curatam: W('curățăm', 73.9), numarul2: W('Numărul', 75.66), doi: W('2', 76.38), intretinerea: W('întreținerea', 77.82),
    trebuie80: W('Trebuie', 80.34), toate84: W('toate', 84.38), si87: W('Și', 87.96), orice92: W('orice', 92.03), admisie94: W('admisie', 94.43), injectie95: W('injecție', 95.23), motor96: W('motor', 96.75),
    dezechilibru98: W('dezechilibru', 98.73), acel: W('Acel', 101.59), asa106: W('Așa', 106.71), senzor107: W('senzor', 107.52), amanati: W('amânați', 109.42), prematura: W('prematură', 114.54), particuleE116: WE('particule', 116.06),
    filtrul117: W('Filtrul', 117.37), ignoranta: W('ignoranță', 121.12), daca122: W('Dacă', 122.23), mii123: W('mii', 123.28), putem: W('putem', 127.38), turbina129: W('turbină', 129.85), senzor131: W('senzor', 131.77),
    inhibarea: W('inhibarea', 133.85), acesta: W('Acesta', 136.98), portofelul: W('portofelul', 140.41), iar: W('Iar', 142.26), unu: W('1', 143.21), mecanicul: W('mecanicul', 146.59), masinaE148: WE('mașina', 148.83),
    si149: W('Și', 149.69), sute: W('sute', 153.7), masinile158: W('Mașinile', 158.94), cap: W('cap', 162.77), diferit: W('diferit', 165.46), de168: W('De', 168.34), ulei: W('ulei', 169.77),
    daca173: W('dacă', 173.82), distrugerea: W('distrugerea', 182.5), nu185: W('Nu', 185.85), fortate: W('forțate', 187.6), killer: W('killer-ul', 189.84), nou: W('nou', 197.2), curatati: W('curățați', 199.3),
    desi: W('Deși', 201.66), totusi: W('Totuși', 210.49), gratuita216: W('gratuită', 216.4), bucuresti: W('București', 218.81), iasi: W('Iași', 219.44), galati: W('Galați', 219.84), piatra: W('Piatra', 220.32),
    in221: W('În', 221.4), gratuita228: W('gratuită', 228.43), si232: W('și', 232.44), tineti: W('Țineți', 235.93), programari: W('programări', 238.27), avem: W('Avem', 242.26), youtube245: W('YouTube', 245.45),
    totodata: W('Totodată', 258.23), canalul: W('canalul', 258.94),
  };
  const HOOK_OUT = A.particuleE0 + .25;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF', l1: 'TOP 3 LUCRURI', l1At: A.top - .05, l2: 'CARE ÎȚI STRICĂ DPF-UL', l2At: A.strica - .04, l2Col: '#FF3B30', y: -30, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT - .05]],
    stages: [[A.incepem - .1, 'GREȘEALA 3'], [A.numarul2 - .1, 'GREȘEALA 2'], [A.iar - .1, 'GREȘEALA 1'], [A.totusi - .1, 'SOLUȚIA']],
    tags: {
      1: { pm25: 'y', cancerul: 'r', pulmonar: 'r', scot: 'r' }, 2: { cancer: 'r', pulmonar: 'r', pm25: 'y', plat: 'y' }, 3: { exploatezi: 'y', regenerari: 'g', complete: 'g', corecte: 'g' },
      4: { regenerarea: 'g', drum: 'g', lung: 'g', temperatura: 'g', constanta: 'g' }, 5: { luna: 'y', oras: 'y', regenerari: 'g', corect: 'g' }, 6: { oras: 'r', subturat: 'r', vacanta: 'g' },
      7: { 2: 'y', intretinerea: 'y' }, 9: { admisie: 'c', injectie: 'c', motor: 'c' }, 10: { dezechilibru: 'r', ardere: 'r' }, 11: { senzor: 'c', amanati: 'r', prematura: 'r' },
      12: { ignoranta: 'r', kilometri: 'y' }, 13: { turbina: 'c', senzor: 'c', inhibarea: 'r' }, 14: { portofelul: 'r', 1: 'y' }, 15: { mecanicul: 'r', sute: 'y' },
      16: { cap: 'g', diferit: 'y' }, 17: { ulei: 'c' }, 18: { infundarea: 'r', distrugerea: 'r' }, 19: { fortate: 'r', killerul: 'r', nou: 'r', lei: 'y' },
      21: { diagnoza: 'g', gratuita: 'g', bucuresti: 'y', iasi: 'y', galati: 'y', piatra: 'y', neamt: 'y' }, 22: { complet: 'g', gratuita: 'g' }, 23: { programari: 'c' }, 24: { youtube: 'c' }, 26: { youtube: 'c' },
    },
    items: [
      // intro: what the DPF is for
      { k: 'chip', t0: A.filtrul1 - .1, t1: A.doar - .25, y: 330, ph: [[A.filtrul1 - .1, 'gear', 'DPF: DUPĂ TURBINĂ, PE EVACUARE', 'blue']] },
      { k: 'def', t0: A.doar - .1, t1: A.dar1 - .25, top: 262, sc: .9, term: 'PM2.5', text: 'Particulele fine din evacuare pe care le reține DPF-ul.' },
      { k: 'chip', t0: A.dar1 - .1, t1: A.incepem - .3, y: 330, ph: [[A.dar1 - .1, 'scissors', '„ȘTIU EI MAI BINE” ȘI ÎL SCOT', 'red'], [A.plat - .1, 'thinking_face', '„PĂMÂNTUL E PLAT”...', 'yellow']] },
      // #3 – how you drive it
      { k: 'kin', t: A.trei - .02, dur: 1.0, txt: 'GREȘEALA #3', col: '#FFD21F', y: 330, size: 110, rot: -3 },
      { k: 'chip', t0: A.exploatezi - .1, t1: A.regenerarea42 - .25, y: 330, ph: [[A.exploatezi - .1, 'automobile', 'CUM EXPLOATEZI MAȘINA', 'yellow'], [A.inseamna34 - .05, 'fire', 'REGENERĂRI COMPLETE ȘI CORECTE', 'green']] },
      { k: 'list', t0: A.regenerarea42 - .1, t1: A.asta54 - .25, top: 262, sc: .82, ico: 'fire', title: 'REGENERAREA CORECTĂ', rows: [[A.drum - .05, 'DRUM LUNG'], [A.temperatura - .05, 'MOTOR LA TEMPERATURĂ IDEALĂ'], [A.turatia - .05, 'TURAȚIE CONSTANTĂ']] },
      { k: 'chip', t0: A.asta54 - .1, t1: A.daca63 - .25, y: 330, ph: [[A.asta54 - .1, 'calendar', 'O DATĂ PE LUNĂ: IEȘI DIN ORAȘ', 'green']] },
      { k: 'chip', t0: A.daca63 - .1, t1: A.numarul2 - .3, y: 330, ph: [[A.daca63 - .1, 'warning', 'NUMAI ORAȘ + SUBTURAT', 'red'], [A.probabil - .1, 'soap', 'AJUNGI LA CURĂȚAT', 'yellow']] },
      // #2 – maintenance
      { k: 'kin', t: A.doi - .02, dur: 1.0, txt: 'GREȘEALA #2', col: '#FFD21F', y: 330, size: 110, rot: -3 },
      { k: 'chip', t0: A.intretinerea - .1, t1: A.si87 - .25, y: 330, ph: [[A.intretinerea - .1, 'wrench', 'ÎNTREȚINEREA MAȘINII', 'yellow'], [A.toate84 - .1, 'dashing_away', 'DPF-UL PRIMEȘTE TOATE GAZELE', 'blue']] },
      { k: 'chain', t0: A.orice92 - .1, t1: A.particuleE116 + .4, top: 262, sc: .76, title: 'DE CE CONTEAZĂ', sub: 'CAUZĂ › EFECT', ico: 'magnifying_glass_tilted_left',
        nodes: [[A.orice92, 'warning', 'NEREGULĂ', 'ADMISIE · INJECȚIE · MOTOR', 'y'], [A.dezechilibru98 - .05, 'fire', 'EFECT', 'DEZECHILIBRU ÎN ARDERE', 'r'],
          [A.amanati - .05, 'hourglass', 'AMÂNI REPARAȚIA', 'DEFECȚIUNE PREMATURĂ A DPF-ULUI', 'r']] },
      { k: 'def', t0: A.filtrul117 - .1, t1: A.putem - .25, top: 262, sc: .9, term: 'DPF-UL NU E SENSIBIL...', text: '...dar e sensibil la ignoranță: mii de km cu probleme nerezolvate.' },
      { k: 'chip', t0: A.putem - .1, t1: A.iar - .25, y: 330, ph: [[A.putem - .1, 'gear', 'O MICĂ PROBLEMĂ PE TURBINĂ', 'red'], [A.senzor131 - .1, 'counter', 'UN SENZOR PE ADMISIE', 'red'],
        [A.inhibarea - .1, 'cross_mark', 'REGENERAREA E BLOCATĂ', 'red'], [A.portofelul - .1, 'money_with_wings', 'SUFERĂ ȘI PORTOFELUL', 'red']] },
      // #1 – the mechanic
      { k: 'kin', t: A.unu - .02, dur: 1.0, txt: 'GREȘEALA #1', col: '#FF3B30', y: 330, size: 110, rot: -3 },
      { k: 'stamp', t: A.mecanicul - .03, t1: A.masinaE148 + .3, y: 330, txt: 'MECANICUL', col: 'red', s: .7, rot: -4 },
      { k: 'chip', t0: A.si149 - .1, t1: A.masinile158 - .25, y: 330, ph: [[A.si149 - .1, 'automobile', 'SUTE DE MAȘINI PE LUNĂ', 'blue']] },
      { k: 'chip', t0: A.masinile158 - .1, t1: A.de168 - .25, y: 330, ph: [[A.masinile158 - .1, 'brain', 'CU DPF: REPARATĂ CU CAP', 'green'], [A.diferit - .1, 'wrench', 'DIFERIT DE MAȘINILE VECHI', 'yellow']] },
      { k: 'chip', t0: A.de168 - .1, t1: A.nu185 - .25, y: 330, ph: [[A.de168 - .1, 'oil_drum', 'DE LA ULEI...', 'blue'], [A.daca173 - .1, 'warning', 'O REPARAȚIE GREȘITĂ...', 'red'], [A.distrugerea - .5, 'cross_mark', '...ÎNFUNDĂ SAU DISTRUGE DPF-UL', 'red']] },
      { k: 'cmp', t0: A.nu185 - .1, t1: A.desi - .25, top: 262, sc: .86, title: 'REGENERĂRI FORȚATE', ico: 'fire', aCls: 'bad', bCls: 'ok',
        a: [A.killer - .05, 'cross_mark', 'DES FORȚATE', 'DPF NOU'], b: [A.curatati - .3, 'check_mark_button', 'LA TIMP', 'DOAR CURĂȚARE'] },
      { k: 'chip', t0: A.desi - .1, t1: A.totusi - .25, y: 330, ph: [[A.desi - .1, 'warning', 'PROBLEME TOT MAI MARI, ZILNIC', 'red']] },
      // solution
      { k: 'chip', t0: A.totusi - .1, t1: A.in221 - .25, y: 330, ph: [[A.totusi - .1, 'stethoscope', 'DIAGNOZĂ GRATUITĂ', 'green'], [A.bucuresti - .05, 'round_pushpin', 'BUCUREȘTI', ''], [A.iasi - .05, 'round_pushpin', 'IAȘI', ''],
        [A.galati - .05, 'round_pushpin', 'GALAȚI', ''], [A.piatra - .05, 'round_pushpin', 'PIATRA NEAMȚ', 'blue']] },
      { k: 'chip', t0: A.in221 - .1, t1: A.tineti - .25, y: 330, ph: [[A.in221 - .1, 'stethoscope', 'NU TE COSTĂ NIMIC', 'green'], [A.si232 - .1, 'magnifying_glass_tilted_left', 'AFLI STAREA DPF-ULUI', 'blue']] },
      { k: 'chip', t0: A.tineti - .1, t1: A.avem - .25, y: 330, ph: [[A.tineti - .1, 'calendar', 'PE BAZĂ DE PROGRAMARE', 'blue'], [A.programari + .4, 'phone', '0739 065 065', 'yellow']] },
      { k: 'chip', t0: A.avem - .1, t1: SEND - .05, y: 330, ph: [[A.avem - .1, 'camera', 'VLOG DETALIAT PE YOUTUBE', 'red'], [A.canalul - .1, 'camera', 'YOUTUBE: TURBO DOCTOR OFICIAL', 'red']] },
    ],
    fx: [
      { k: 'punch', t: A.strica, a: .05, sh: 6 }, { k: 'red', t0: A.strica - .05, t1: A.particuleE0 + .2, max: 1.2 },
      { k: 'green', t0: A.regenerarea42 - .05, t1: A.regenerarea42 + .8, silent: true },
      { k: 'red', t0: A.subturat - .05, t1: A.subturat + .9, max: 1.0 },
      { k: 'red', t0: A.dezechilibru98 - .05, t1: A.dezechilibru98 + 1.0, max: 1.0 },
      { k: 'punch', t: A.ignoranta, a: .04, sh: 5 },
      { k: 'punch', t: A.mecanicul, a: .06, sh: 8 }, { k: 'red', t0: A.mecanicul - .05, t1: A.masinaE148 + .2, max: 1.2 },
      { k: 'punch', t: A.killer, a: .05, sh: 6 }, { k: 'red', t0: A.killer - .05, t1: A.killer + 1.2, max: 1.2 },
      { k: 'green', t0: A.gratuita216 - .05, t1: A.gratuita216 + .9 },
    ],
    sfx: [],
    bursts: [[A.gratuita216, 540, 330, 6, 300, .7]],
  };
};
