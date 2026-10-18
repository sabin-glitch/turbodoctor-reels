// v2 – DPF Doctor · „Ce face un filtru de particule” (TikTok 7691032957343108374, 34 s, prezentator în picioare, DPF secționat pe masă)
// Footage exactly as filmed (static camera), natural pace, no separate hook.
// The old word-by-word captions (blue boxes over his chest) were inpainted (caption_clean --dynbox); our captions sit on that same line
// (capTop), so they also cover the little smears where his hands pass. Cards go over his torso, between chin and captions, never over the face.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    filtrul: W('Filtrul', .22), odata: W('odată', 3.68), euro: W('Euro', 5.12), euroE: WE('4', 5.68),
    pe1: W('Pe', 6.23), dupa: W('după', 8.38), n2020E: WE('2020', 9.82), dar: W('dar', 10.54), focusam: W('focusăm', 12.14), dieselE1: WE('diesel', 14.49),
    acest: W('Acest', 15.9), scop: W('scop', 17.57), reduca: W('reducă', 19.17), pm: W('PM2.5', 20.45), dieselE2: WE('diesel', 23.63),
    iar: W('Iar', 24.05), montat: W('montat', 26.69), evacuarea: W('evacuarea', 27.17), si: W('și', 28.77), capteaza: W('captează', 29.09),
    funingine: W('funingine', 31.41), regenerarii: W('regenerării', 33.17), regenerariiE: WE('regenerării', 33.17),
  };
  const HOOK_OUT = A.euroE + .15;
  return {
    capTop: 1055,                // captions on the line of the removed blue-box captions (just above the cut DPF on the table)
    // hook below his chin (face: y 200–800), over his chest; nothing over the DPF on the table
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF', l1: 'FILTRUL DE <span class="y">PARTICULE</span>', l1At: A.filtrul - .05, l2: 'ODATĂ CU EURO 4', l2At: A.odata - .04, l2Col: '#62D8FF',
      y: 620, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT - .05]],
    stages: [[A.pe1 - .1, 'ISTORIC'], [A.acest - .1, 'SCOPUL'], [A.iar - .1, 'MONTAJ'], [A.si - .1, 'FUNCȚIONARE']],
    tags: { 0: { particule: 'c', euro: 'y' }, 1: { benzina: 'c', diesel: 'c' }, 2: { scop: 'y', reduca: 'g', pm25: 'y', funingine: 'r', regenerarii: 'g' } },
    items: [
      { k: 'cmp', t0: A.pe1 - .1, t1: A.dar - .3, top: 830, sc: .86, title: 'DE CÂND AU MAȘINILE DPF?', ico: 'calendar', aCls: 'nt', bCls: 'nt', big: true,
        a: [A.pe1 - .1, 'fuel_pump', 'DIESEL', 'EURO 4'], b: [A.dupa - .05, 'fuel_pump', 'BENZINĂ', 'DUPĂ 2020'] },
      { k: 'chip', t0: A.dar - .1, t1: A.dieselE1 + .3, y: 900, ph: [[A.dar - .1, 'magnifying_glass_tilted_left', 'AZI: DPF-UL DE PE DIESEL', 'blue']] },
      { k: 'def', t0: A.acest - .1, t1: A.dieselE2 + .3, top: 840, sc: .9, term: 'SCOPUL DPF', text: 'Reduce depunerile de tip PM2.5 emise de motoarele diesel.' },
      { k: 'call', t0: A.montat - .1, t1: SEND - .1, p: [560, 1330], lab: [360, 1000], h: 'MONTAT PE', v: 'EVACUAREA MAȘINII', cps: 36 },
      // too little room under his chin for the schematic: short chips instead
      { k: 'chip', t0: A.capteaza - .1, t1: SEND - .05, y: 880, ph: [[A.capteaza - .1, 'magnifying_glass_tilted_left', 'CAPTEAZĂ FUNINGINEA', 'red'], [A.regenerarii - .1, 'fire', 'APOI: REGENERARE', 'yellow']] },
    ],
    fx: [
      { k: 'green', t0: A.reduca - .05, t1: A.reduca + .8, silent: true },
      { k: 'red', t0: A.funingine - .05, t1: A.funingine + .9, max: 1.0 },
    ],
    sfx: [],
    bursts: [],
  };
};
