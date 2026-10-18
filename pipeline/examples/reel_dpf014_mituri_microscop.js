// v2 – DPF Doctor · „Myth Busters: curățarea distruge DPF-ul?” (TikTok 7693185855095344407, 2:58, răspuns la comentariu)
// Footage exactly as filmed: selfie, cut-open DPF (Q5 aftermarket), microscope on a monitor, ultrasonic bath, selfie. Natural pace, no separate hook.
// Old burned texts removed (TikTok „Amintire 5 oct 2025” label, „Myth Busters - Turbo Doctor!” title). The reply bubble (0–68.8 s) is covered
// by our card, which turns into the test sheet („FIȘA TESTULUI”) while the experiment runs. Then cards over the wall, above the monitor.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    salutare: W('Salutare', .66), distrugem: W('distrugem', 3.69), miturieE: WE('mituri', 4.57), despre: W('Despre', 5.66), ca10: W('că', 10.45), ca14: W('că', 14.13), hai: W('Hai', 17.59),
    avem: W('Avem', 22.65), am32: W('Am', 31.96), acum: W('Acum', 39.19), am47: W('Am', 47.67), ceea: W('Ceea', 53.08), ce58: W('Ce', 58.55), negru: W('negru', 59.5), vom: W('Vom', 66.14),
    solutia: W('Soluția', 89.46), sub79: W('sub', 79.38), ce86: W('ce', 86.39), astfel98: W('Astfel', 98.3), niciodata: W('niciodată', 102.07), solutieE: WE('soluție', 104.06), filtrul106: W('Filtrul', 106.39), temperaturi: W('temperaturi', 109.26),
    forte: W('forțe', 112.22), particuleE118: WE('particule', 117.97), apa: W('Apa', 119.0), nu121: W('nu', 121.79), particuleE124: WE('particule', 124.35), dupa126: W('După', 126.78), ultrasunete: W('ultrasunete', 131.8),
    cam150: W('Cam', 150.2), micile: W('Micile', 154.67), sub158: W('sub', 158.11), initialaE: WE('inițială', 161.95), astfel163: W('Astfel', 163.73), la166: W('la', 166.21), reparatia: W('reparația', 169.65),
    diagnoza: W('diagnoza', 173.89), te176: W('Te', 176.61),
  };
  const BUBBLE_OUT = 68.85;
  const HOOK_OUT = A.despre - .1;
  const F = (t, lab, txt, fs = 36, ico = 'test_tube') => [t, lab, txt, fs, ico, '#0369A1'];
  return {
    hook: { tag: 'MYTH BUSTERS · TURBO DOCTOR', tagY: 1295, l1: 'DISTRUGEM', l1At: A.salutare - .05, l2: 'MITURI DESPRE DPF', l2At: A.distrugem - .04, l2Col: '#FFD21F',
      w: 900, l1Y: 1395, l2Y: 1515, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT - .05]],
    tags: {
      1: { mituri: 'y', platina: 'c', distruge: 'r', regenereaza: 'g', microscop: 'c', ceramica: 'c' }, 2: { q5: 'y', aftermarket: 'y', didactic: 'c' }, 3: { microscopul: 'c', microporii: 'c' },
      4: { apei: 'c', solutiei: 'c' }, 5: { microscop: 'c', galbui: 'y' }, 6: { negru: 'r', depunerile: 'r', carbon: 'r' }, 9: { solutia: 'c', carbon: 'r' }, 11: { niciodata: 'g', afectata: 'g' },
      12: { mecanice: 'y', esapament: 'c' }, 13: { nu: 'g', pot: 'g', afecta: 'g' }, 14: { ultrasunete: 'c' }, 15: { curatare: 'g', 1: 'y', cenusa: 'y', funingine: 'r' },
      16: { turbinelor: 'c', injectoarelor: 'c', curatarea: 'g', diagnoza: 'g', complet: 'g', gratuita: 'g' },
    },
    items: [
      // reply bubble: our card on the same spot; it becomes the test sheet
      { k: 'note', t0: 0, t1: BUBBLE_OUT, hard: true, box: [30, 187, 535, 476], fs: 38,
        ph: [[0, 'COMENTARIU', '„Spălarea lărgește microporii, la testele de noxe nu are efect.”', 40, 'speech_balloon'],
          F(A.ca10 - .05, 'MITUL 1', 'La curățare <b>„pleacă platina la plimbare”</b>.', 40, 'thinking_face'),
          F(A.ca14 - .05, 'MITUL 2', 'Curățarea <b>distruge filtrul</b> și nu se mai regenerează.', 38, 'thinking_face'),
          F(A.avem - .05, 'PACIENTUL', 'DPF <b>Audi Q5</b>, aftermarket, devenit <b>material didactic</b>.', 38, 'automobile'),
          F(A.am32 - .05, 'TESTUL 1', '<b>Microporii</b> ceramicii, la microscop.', 40, 'microscope'),
          F(A.acum - .05, 'TESTUL 2', 'O bucată de DPF: întâi <b>apă</b>, apoi <b>soluția</b> de curățare.', 36, 'test_tube'),
          F(A.ceea - .05, 'LA MICROSCOP', '<b>Gălbui</b> = ceramica. <b style="color:#C81E2C">Negru</b> = depunerile de carbon.', 36, 'microscope'),
          F(A.vom - .05, 'TESTUL 2', 'Bucata, <b>spreiată cu soluție</b>, înapoi sub microscop.', 36, 'test_tube')] },
      // after the bubble: cards over the wall, above the monitor
      { k: 'chip', t0: BUBBLE_OUT, t1: A.solutia - .3, y: 330, ph: [[BUBBLE_OUT, 'test_tube', 'TESTUL 2: CU SOLUȚIA DE CURĂȚARE', 'blue'], [A.sub79 - .05, 'microscope', 'ÎNAPOI SUB MICROSCOP', 'blue'],
        [A.ce86 - .05, 'eyes', 'CE SE ÎNTÂMPLĂ?', 'yellow']] },
      { k: 'def', t0: A.solutia - .1, t1: A.solutieE + .5, top: 262, term: 'SOLUȚIA DE CURĂȚARE', text: 'Atacă depunerile de carbon. Monolitul ceramic nu e afectat.' },
      { k: 'chip', t0: A.filtrul106 - .1, t1: A.apa - .25, y: 330, ph: [[A.filtrul106 - .1, 'fire', 'GÂNDIT PENTRU TEMPERATURI ÎNALTE', 'red'], [A.forte - .05, 'dashing_away', '+ FORȚE MECANICE MARI', 'red']] },
      { k: 'stamp', t: A.nu121 - .03, t1: A.dupa126 - .2, y: 360, txt: 'MIT DEMONTAT', col: 'green', s: .75, rot: -5 },
      { k: 'chip', t0: A.dupa126 - .1, t1: A.cam150 - .3, y: 330, ph: [[A.dupa126 - .1, 'soap', 'APOI: BAIE CU ULTRASUNETE', 'blue']] },
      { k: 'chip', t0: A.cam150 - .1, t1: A.sub158 - 1.3, y: 330, ph: [[A.cam150 - .1, 'sparkles', 'AȘA ARATĂ DUPĂ CURĂȚARE', 'green']] },
      { k: 'stat', t0: A.sub158 - 1.1, t1: A.astfel163 - .3, top: 262, title: 'DEPUNERI RĂMASE DUPĂ CURĂȚARE', ico: 'microscope', from: 100, to: 1, at: A.sub158 - .8, dur: .9,
        fmt: v => v > 1 ? v + '%' : 'SUB 1%', sub: 'din masa inițială de cenușă și funingine', subIco: 'check_mark_button' },
      // selfie outro: thin band above his hair
      { k: 'chip', t0: A.la166 - .1, t1: A.diagnoza - .25, y: 250, ph: [[A.la166 - .1, 'stethoscope', 'TURBO DOCTOR', 'blue'], [A.reparatia - .05, 'hammer_and_wrench', 'TURBINE · INJECTOARE · DPF', 'blue']] },
      { k: 'chip', t0: A.diagnoza - .1, t1: SEND - .05, y: 250, ph: [[A.diagnoza - .1, 'stethoscope', 'DIAGNOZĂ COMPLET GRATUITĂ', 'green']] },
    ],
    fx: [
      { k: 'punch', t: A.distrugem, a: .05, sh: 6 },
      { k: 'red', t0: A.negru - .05, t1: A.negru + 1.2, max: 1.0 },
      { k: 'green', t0: A.niciodata - .05, t1: A.solutieE + .3, silent: true },
      { k: 'punch', t: A.nu121, a: .05, sh: 6 }, { k: 'green', t0: A.nu121 - .05, t1: A.particuleE124 + .3 },
      { k: 'green', t0: A.sub158 - .05, t1: A.initialaE + .3, silent: true },
    ],
    sfx: [],
    bursts: [[A.nu121 + .1, 540, 360, 6, 320, .8]],
  };
};
