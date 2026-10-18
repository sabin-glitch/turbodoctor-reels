// v2 – DPF Doctor · „Oil ash, soot accumulation, presiune diferențială” (TikTok 7694329560896130326, 59 s, răspuns la comentariu, alt prezentator, în mașină)
// Footage exactly as filmed, natural pace, no separate hook. The TikTok reply bubble is on screen for the whole clip: covered by our
// comment card (same place, same size). Right column (x 600–1060, above his head) for hook + chips; lower area (chest) for the cards.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    intrebare: W('Întrebare', 1.42), zona: W('zona', 4.46), mare: W('Mare', 5.42), perioadaE: WE('perioadă', 9.34),
    multa: W('Multă', 10.74), oil1: W('oil', 12.25), soot1: W('soot', 13.53), presiunea: W('presiunea', 15.29), valoarea: W('valoarea', 17.53), masurata: W('măsurată', 19.61),
    deci: W('Deci', 22.39), avem: W('avem', 24.81), oil3: W('Oil', 26.65), partea29: W('partea', 29.11), nu34: W('nu', 34.38), eliminaE: WE('elimină', 34.86), in36: W('În', 36.14),
    readaptarii: W('readaptării', 38.35), rezolva: W('rezolvă', 40.59), iar: W('iar', 43.61), partea45: W('partea', 44.93), funingine1: W('funingine', 49.82),
    dispara: W('dispară', 53.18), regenerariiE: WE('regenerării', 55.34), mare57: W('Mare', 57.02), problemeE: WE('probleme', 58.7),
  };
  const RX = 822;   // right column centre
  return {
    hook: { tag: 'RĂSPUNS LA COMENTARIU · DPF', tagY: 175, l1: '<span class="y">OIL ASH</span> LA DPF', l1At: A.intrebare - .05, l2: 'MARE GRIJĂ!', l2At: A.mare - .04, l2Col: '#FF3B30',
      x: RX, w: 440, l1Y: 360, l2Y: 490, end: A.perioadaE + .2 },
    stages: [[A.multa - .1, 'CONFUZIA'], [A.oil3 - .1, 'OIL ASH'], [A.partea45 - .1, 'SOOT']],
    tags: {
      0: { vag: 'y', mare: 'r', grija: 'r', probleme: 'r' }, 1: { oil: 'y', ashul: 'y', soot: 'y', accumulation: 'y', presiunea: 'c', diferentiala: 'c' },
      2: { calculata: 'c', masurata: 'c', vag: 'y', oil: 'y', ash: 'y' }, 3: { cenusa: 'y', nu: 'r', elimina: 'r', curatarii: 'g' },
      4: { readaptarii: 'g', rezolva: 'g', oil: 'y', ash: 'y' }, 5: { soot: 'y', accumulation: 'y', funingine: 'r', dispara: 'g', regenerarii: 'g', mare: 'r', grija: 'r', probleme: 'r' },
    },
    items: [
      { k: 'note', t0: 0, t1: SEND, hard: true, box: [66, 307, 582, 650], fs: 33, label: 'COMENTARIU',
        text: '„Poți detalia, te rog, problema cu «oil ash» la filtrul de particule? Am înțeles că nu se elimină prin regenerare.”' },
      // what people confuse: right column, above his head (nothing in the bottom band, where the TikTok/IG text sits)
      { k: 'chip', free: true, sc: .86, t0: A.multa - .1, t1: A.deci - .3, x: RX, y: 380, ph: [[A.multa - .1, 'thinking_face', 'SE CONFUNDĂ DES:', 'yellow'], [A.oil1 - .05, 'test_tube', 'OIL ASH', ''],
        [A.soot1 - .05, 'fire', 'SOOT ACCUMULATION', ''], [A.presiunea - .05, 'counter', 'PRESIUNE DIFERENȚIALĂ', 'blue'], [A.valoarea - .05, 'counter', 'CALCULAT / MĂSURAT', 'blue']] },
      { k: 'chip', free: true, sc: .9, t0: A.deci - .1, t1: A.partea29 - .25, x: RX, y: 380, ph: [[A.deci - .1, 'automobile', 'PE VAG: OIL ASH', 'blue']] },
      { k: 'chip', free: true, sc: .9, t0: A.partea29 - .1, t1: A.in36 - .25, x: RX, y: 380, ph: [[A.partea29 - .1, 'test_tube', 'OIL ASH = CENUȘĂ', ''], [A.nu34 - .05, 'cross_mark', 'NU ARDE LA REGENERARE', 'red']] },
      { k: 'chip', free: true, sc: .9, t0: A.in36 - .1, t1: A.iar - .2, x: RX, y: 380, ph: [[A.in36 - .1, 'soap', 'SOLUȚIA: CURĂȚARE', 'green'], [A.readaptarii - .05, 'gear', '+ READAPTARE', 'green']] },
      { k: 'chip', free: true, sc: .9, t0: A.partea45 - .1, t1: A.mare57 - .25, x: RX, y: 380, ph: [[A.partea45 - .1, 'fire', 'SOOT = FUNINGINE', ''], [A.dispara - .05, 'check_mark_button', 'ARDE LA REGENERARE', 'green']] },
      { k: 'stamp', t: A.mare57 - .03, t1: SEND - .05, x: RX, y: 400, txt: 'MARE GRIJĂ!', col: 'red', s: .6, rot: -5 },
      { k: 'kin', t: A.partea29 + .55, dur: 1.3, txt: 'CENUȘĂ', col: '#C9CED4', x: RX, y: 540, size: 110, rot: -3 },
      { k: 'kin', t: A.funingine1 - .03, dur: 1.3, txt: 'FUNINGINE', col: '#FF8A3D', x: RX, y: 540, size: 100, rot: -3 },
    ],
    fx: [
      { k: 'punch', t: A.mare, a: .05, sh: 6 }, { k: 'red', t0: A.mare - .05, t1: A.mare + 1.0, max: 1.0 },
      { k: 'red', t0: A.nu34 - .05, t1: A.eliminaE + .3, max: 1.0 },
      { k: 'green', t0: A.rezolva - .05, t1: A.rezolva + .8, silent: true },
      { k: 'punch', t: A.mare57, a: .05, sh: 6 },
    ],
    sfx: [],
    bursts: [],
  };
};
