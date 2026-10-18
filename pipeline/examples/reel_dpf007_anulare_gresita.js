// v2 – DPF Doctor · „Anularea DPF făcută greșit: problema era altundeva” (TikTok 7690078738301685014, 68 s, alt prezentator, platou cu motor)
// Footage exactly as filmed (incl. the intercooler-hose cutaway 14.7–18.4 s), natural pace, no separate hook.
// Old title „DESPRE ANULARE DPF” and the old white word-captions were removed (caption_clean --band / --dyntext);
// our captions sit on the old caption line (capTop) and cover what is left of it. Face top-left (y 320–600): graphics above the head or over the torso.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    anulat: W('anulat', 5.49), tot: W('tot', 7.6), fum: W('fum', 8.24), departeE: WE('departe', 10.16), cand: W('Când', 10.56), fasaia: W('fâșâia', 11.92),
    simptom: W('simptom', 14.0), furtun: W('furtun', 14.8), spartaE: WE('spartă', 17.2), si18: W('Și', 18.0), evacuarile: W('evacuările', 20.96), masiniiE: WE('mașinii', 23.28),
    zic: W('Zic', 23.87), furtun2: W('furtun', 25.41), masina27: W('Mașina', 26.91), incarcat: W('încărcat', 30.03), sa31: W('s-a', 31.15), taiat: W('tăiat', 32.58), dpfE: WE('DPF-ul', 32.91),
    si34: W('Și', 34.26), tot35: W('tot', 35.53), mergeE: WE('merge', 35.85), merge36: W('Merge', 36.66), fumE: WE('fum', 40.35),
    ajungeti: W('Ajungeți', 41.28), ideea: W('ideea', 44.24), trebuie: W('trebuie', 47.52), si50: W('Și', 50.0), importanta: W('importantă', 54.24), consider: W('Consider', 54.8),
    serviceE: WE('service', 58.0), daca: W('Dacă', 58.94), diagnosticare: W('diagnosticare', 61.81), mecanicul: W('mecanicul', 63.73), are: W('are', 64.61), p90: W('90%', 64.95), rezolvateE: WE('rezolvate', 66.29),
  };
  const CUT1 = 14.7, CUT2 = 18.4;    // intercooler-hose cutaway
  return {
    capTop: 1200,                      // captions on the old caption line (~y 1320)
    hook: { tag: 'CAZ REAL · DPF ANULAT', l1: 'I-A ANULAT <span class="r">DPF-UL</span>...', l1At: .3, l2: '...ȘI TOT SCOATE FUM!', l2At: A.tot - .04, l2Col: '#FF3B30',
      y: 420, end: A.departeE + .2 },
    stages: [[.2, 'CAZUL'], [A.zic - .1, 'GREȘEALA'], [A.ajungeti - .1, 'LECȚIA']],
    tags: {
      0: { anulat: 'r', fum: 'r', fasaia: 'r', furtun: 'c', turbo: 'c', spart: 'r', sparta: 'r', admisie: 'c', evacuarile: 'c' },
      1: { furtun: 'c', turbo: 'c', spart: 'r', incarcat: 'r', dorel: 'y', taiat: 'r' }, 2: { merge: 'r', fum: 'r' },
      3: { anularii: 'r', schimbarii: 'y', constatari: 'g', corecte: 'g', diagnosticarea: 'g' }, 4: { corecta: 'g', importanta: 'g', diagnosticianul: 'g', important: 'g' },
      5: { diagnosticianul: 'g', bun: 'g', diagnosticare: 'g', corecta: 'g', rezolvate: 'g' },
    },
    items: [
      { k: 'chip', t0: A.cand - .1, t1: CUT1 - .2, y: 290, ph: [[A.cand - .1, 'speech_balloon', 'LA PLECARE: FÂȘÂIA', 'blue']] },
      { k: 'call', t0: CUT1 + .15, t1: CUT2 - .15, p: [610, 760], lab: [470, 420], h: 'SIMPTOM DE', v: 'FURTUN TURBO SPART', cps: 36, col: 'red' },
      { k: 'chip', t0: CUT2 + .05, t1: A.masiniiE + .3, y: 290, ph: [[CUT2 + .05, 'dashing_away', 'FUM ÎN SPATELE MAȘINII', 'red']] },
      // what really happened: cause -> effect (over his torso, under the face)
      { k: 'chain', t0: A.zic - .1, t1: A.dpfE + .6, top: 630, sc: .8, title: 'CE S-A ÎNTÂMPLAT DE FAPT', sub: 'CAUZĂ › EFECT', ico: 'magnifying_glass_tilted_left',
        nodes: [[A.furtun2 - .05, 'warning', 'CAUZA', 'FURTUN DE TURBO SPART', 'r'], [A.masina27 - .05, 'gear', 'EFECT', 'MOTORUL NU FUNCȚIONA CORECT', 'y'],
          [A.incarcat - .05, 'dashing_away', 'APOI', 'S-A ÎNCĂRCAT DPF-UL', 'r'], [A.sa31 - .05, 'scissors', 'LA „DOREL”', 'I-A TĂIAT DPF-UL', 'r']] },
      { k: 'stamp', t: A.tot35 - .03, t1: A.merge36 - .1, y: 780, txt: 'TOT NU MERGE!', col: 'red', s: .7, rot: -5 },
      { k: 'chip', t0: A.merge36 - .05, t1: A.fumE + .4, y: 780, ph: [[A.merge36 - .05, 'cross_mark', 'NU TRAGE, TOT SCOATE FUM', 'red']] },
      // the lesson
      { k: 'chip', t0: A.ideea - .1, t1: A.si50 - .25, y: 290, ph: [[A.ideea - .1, 'thinking_face', 'ANULARE? SCHIMBARE?', 'yellow'], [A.trebuie - .05, 'magnifying_glass_tilted_left', 'ÎNTÂI: CONSTATARE CORECTĂ', 'green']] },
      { k: 'def', t0: A.si50 - .1, t1: A.serviceE + .3, top: 650, sc: .9, term: 'DIAGNOSTICIANUL', text: 'Cel mai important om dintr-un service: diagnoza corectă e cea mai importantă.' },
      { k: 'chip', t0: A.daca - .1, t1: A.mecanicul - .3, y: 290, ph: [[A.daca - .1, 'stethoscope', 'DIAGNOSTICIAN BUN', 'green'], [A.diagnosticare - .05, 'check_mark_button', 'DIAGNOZĂ CORECTĂ', 'green']] },
      { k: 'stat', t0: A.mecanicul - .1, t1: SEND - .05, top: 650, title: 'PROBLEME REZOLVATE DEJA', ico: 'hammer_and_wrench', to: 90, at: A.p90 - .15, dur: .6, fmt: v => v + '%', sub: 'pentru mecanic, după o diagnoză corectă' },
    ],
    fx: [
      { k: 'punch', t: A.fum, a: .05, sh: 6 }, { k: 'red', t0: A.fum - .05, t1: A.departeE, max: 1.3 },
      { k: 'punch', t: A.taiat, a: .06, sh: 8 }, { k: 'red', t0: A.taiat - .05, t1: A.dpfE + .4, max: 1.2 },
      { k: 'red', t0: A.tot35 - .05, t1: A.mergeE + .4, max: 1.0 },
      { k: 'green', t0: A.importanta - .05, t1: A.importanta + .8, silent: true },
      { k: 'green', t0: A.p90 - .05, t1: A.p90 + .9 },
    ],
    sfx: [],
    bursts: [[A.p90 + .1, 540, 800, 6, 320, .8]],
  };
};
