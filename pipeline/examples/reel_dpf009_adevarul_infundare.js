// v2 – DPF Doctor · „Adevărul despre înfundarea DPF” (TikTok 7692701804835933463, 2:19, răspuns la comentariu, selfie în mașină)
// Footage exactly as filmed, natural pace, no separate hook. Close selfie (face y 420–1570): graphics in the top band only.
// The TikTok reply bubble (0–23.45 s) is covered by our comment card; the hook lines sit to its right, above his head.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    adica: W('adică', 4.89), diagnosticata: W('diagnosticată', 10.09), nu12: W('Nu', 12.79), capE: WE('cap', 18.62), am19: W('Am', 19.77), filtrul24: W('filtrul', 24.09), cauza27: W('cauza', 27.84),
    unor: W('unor', 30.77), cauza35: W('Cauza', 35.16), cauzele: W('Cauzele', 39.17), multeE: WE('multe', 40.93), si41: W('Și', 41.75), filtrul45: W('Filtrul', 45.9), corectE: WE('corect', 47.82),
    acuma: W('Acuma', 48.76), da54: W('Da', 54.26), infundat: W('înfundat', 56.99), dat59: W('dat', 59.29), dupa63: W('după', 63.42), stai: W('stai', 67.13), si69: W('Și', 69.91),
    dupa74: W('după', 74.06), dom77: W('dom\'le', 77.82), mort: W('mort', 79.02), elE: WE('el', 80.38), la80: W('La', 80.61), n800: W('800.000', 83.25), doar: W('doar', 86.93),
    totusi: W('Totuși', 94.14), unor99: W('unor', 99.63), acoloE: WE('acolo', 102.11), tineti: W('Țineți', 102.87), cumparatorul: W('cumpărătorul', 111.58), si116: W('Și', 116.22),
    trafic: W('trafic', 118.77), anulateE: WE('anulate', 122.29), nu123: W('Nu', 123.26), dar133: W('dar', 133.01), noastreE: WE('noastre', 138.45),
  };
  const BUBBLE_OUT = 23.45;
  return {
    hook: { tag: 'RĂSPUNS LA COMENTARIU · DPF', tagY: 150, l1: 'DIAGNOSTICATĂ', l1At: A.diagnosticata - .05, l2: 'NU ANULATĂ!', l2At: A.nu12 - .04, l2Col: '#FF3B30',
      x: 818, w: 450, l1Y: 300, l2Y: 425, end: A.capE + .2 },
    stages: [[A.am19 - .1, 'CAUZA'], [A.acuma - .1, 'GREȘEALA'], [A.la80 - .1, 'DOVADA'], [A.tineti - .1, 'RISCURI']],
    tags: {
      0: { diagnosticata: 'g', rezolvata: 'g' }, 1: { anulata: 'r', carpita: 'r' }, 2: { vehement: 'y', infunda: 'r', cauza: 'y' }, 3: { cauze: 'y', cauza: 'y', cautata: 'g', cauzele: 'y' },
      4: { gasita: 'g', indepartata: 'g', corect: 'g' }, 6: { infundat: 'r', km: 'y', goana: 'r' }, 7: { tester: 'y' }, 8: { regenerari: 'r', fortate: 'r', km: 'y', mort: 'r' },
      9: { km: 'y', active: 'g', curatare: 'g' }, 10: { bine: 'g', mersi: 'g', anuleaza: 'r', km: 'y', habarnisti: 'r' }, 11: { problema: 'r', ilegale: 'r' }, 12: { probleme: 'r', anulate: 'r' },
      13: { corect: 'g', gandim: 'g' },
    },
    items: [
      { k: 'note', t0: 0, t1: BUBBLE_OUT, hard: true, box: [68, 197, 568, 578], fs: 34, label: 'COMENTARIU',
        text: '„Incorect: Passat CC 2009, Euro 5, CBAB, 389.xxx km. Încă e activ, după 2 curățări și eliminarea cauzei înfundării.”' },
      { k: 'chip', t0: A.adica - .1, t1: A.diagnosticata - .25, x: 818, y: 300, ph: [[A.adica - .1, 'brain', 'CU CAPUL PE UMERI', 'green']] },
      { k: 'chip', t0: A.am19 - .1, t1: BUBBLE_OUT - .1, x: 818, y: 300, ph: [[A.am19 - .1, 'speech_balloon', 'O SPUNEM VEHEMENT', 'blue']] },
      { k: 'chip', t0: BUBBLE_OUT, t1: A.cauza35 - .25, y: 300, ph: [[BUBBLE_OUT, 'warning', 'DPF-UL SE ÎNFUNDĂ DIN CAUZA...', 'red'], [A.unor - .05, 'magnifying_glass_tilted_left', '...UNOR CAUZE!', 'yellow']] },
      { k: 'chip', t0: A.cauza35 - .1, t1: A.si41 - .25, y: 300, ph: [[A.cauza35 - .1, 'magnifying_glass_tilted_left', 'CAUZA TREBUIE CĂUTATĂ', 'yellow'], [A.cauzele - .05, 'warning', 'DE OBICEI SUNT MAI MULTE', 'red']] },
      { k: 'chip', t0: A.si41 - .1, t1: A.filtrul45 - .2, y: 300, ph: [[A.si41 - .1, 'check_mark_button', 'CAUZĂ GĂSITĂ + ÎNDEPĂRTATĂ', 'green']] },
      { k: 'stamp', t: A.filtrul45 - .03, t1: A.corectE + .5, y: 320, txt: 'DPF FUNCȚIONEAZĂ CORECT', col: 'green', s: .55, rot: -4 },
      // the classic „own experience”, step by step
      { k: 'chip', t0: A.acuma - .1, t1: A.da54 - .25, y: 300, ph: [[A.acuma - .1, 'speech_balloon', '„DIN PROPRIA EXPERIENȚĂ...”', 'blue']] },
      { k: 'chip', t0: A.da54 - .1, t1: A.dupa63 - .25, y: 300, ph: [[A.da54 - .1, 'warning', 'PASUL 1: DPF ÎNFUNDAT', 'red'], [A.dat59 - .3, 'racing_car', 'PASUL 2: 1000 KM ÎN GOANĂ', 'yellow']] },
      { k: 'chip', t0: A.dupa63 - .1, t1: A.si69 - .25, y: 300, ph: [[A.dupa63 - .1, 'wrench', 'PASUL 3: „TE REZOLV DIN TESTER”', 'yellow']] },
      { k: 'chip', t0: A.si69 - .1, t1: A.dom77 - .25, y: 300, ph: [[A.si69 - .1, 'fire', 'PASUL 4: 7 REGENERĂRI FORȚATE', 'red'], [A.dupa74 - .05, 'counter', '+10.000 KM', 'red']] },
      { k: 'stamp', t: A.dom77 - .03, t1: A.elE + .3, y: 320, txt: '„FILTRUL E MORT”', col: 'red', s: .62, rot: -4 },
      // proof
      { k: 'stat', t0: A.la80 - .1, t1: A.totusi - .3, top: 262, sc: .86, title: 'MAȘINI CU DPF ACTIV LA', ico: 'automobile', to: 800000, step: 10000, at: A.n800 - .3, dur: .9, unit: 'KM',
        sub: 'doar curățare + cauza înlăturată', subIco: 'check_mark_button' },
      { k: 'chip', t0: A.totusi - .1, t1: A.tineti - .25, y: 300, ph: [[A.totusi - .1, 'scissors', 'ANULAT DEJA LA 80.000 KM', 'red'], [A.unor99 - .3, 'thinking_face', 'PE MÂNA UNOR HABARNIȘTI', 'yellow']] },
      // risks
      { k: 'list', t0: A.tineti - .1, t1: A.anulateE + .4, top: 262, sc: .8, ico: 'warning', title: 'CU DPF-UL ANULAT', rows: [[A.tineti + .3, 'PROBLEMA RĂMÂNE A TA', 'bad'],
        [A.cumparatorul - .05, 'LA VÂNZARE: ACUZAȚII', 'bad'], [A.trafic - .05, 'ÎN TRAFIC: PROBLEME', 'bad']] },
      { k: 'chip', t0: A.nu123 - .1, t1: SEND - .05, y: 300, ph: [[A.nu123 - .1, 'handshake', 'NU DOAR LA TURBO DOCTOR', 'blue'], [A.dar133 - .05, 'brain', 'GÂNDEȘTE ÎNAINTE SĂ ACȚIONEZI', 'green']] },
    ],
    fx: [
      { k: 'punch', t: A.nu12, a: .05, sh: 6 }, { k: 'red', t0: A.nu12 - .05, t1: A.nu12 + 1.4, max: 1.2 },
      { k: 'green', t0: A.filtrul45 - .05, t1: A.corectE + .3 },
      { k: 'punch', t: A.mort, a: .05, sh: 6 }, { k: 'red', t0: A.mort - .05, t1: A.elE + .2, max: 1.2 },
      { k: 'green', t0: A.n800 - .05, t1: A.n800 + .9, silent: true },
    ],
    sfx: [],
    bursts: [[A.n800 + .6, 540, 360, 6, 320, .7]],
  };
};
