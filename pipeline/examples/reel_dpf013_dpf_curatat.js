// v2 – DPF Doctor · „Așa iese un DPF de la curățat” (TikTok 7694363419725630742, 16 s, DPF în mașina de curățat, la stand)
// Footage exactly as filmed, natural pace, no separate hook. Old burned title and date removed (caption_clean). The old price/warranty
// block („500 Lei / 24 de luni garanție”) is covered by our card on the same spot (price not re-added: can't check it is still current);
// captions sit just above the card. Short clip: no stage bar.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    cam: W('Cam', 2.42), curat: W('curat', 2.89), dupa5: W('după', 5.45), curatat: W('curățat', 6.25), profesional: W('profesional', 6.97), doctorE: WE('Doctor', 8.62),
    dupa10: W('După', 10.55), iese: W('iese', 13.5), apa: W('apă', 14.62), curataE: WE('curată', 14.82),
  };
  return {
    hook: { tag: 'CURĂȚARE DPF · TURBO DOCTOR', l1: 'AȘA IESE UN <span class="c">DPF</span>', l1At: .25, l2: 'DE LA CURĂȚAT!', l2At: A.curat - .04, l2Col: '#4ADE80', y: -40, end: A.dupa5 - .1 },
    hideCap: [[0, A.cam - .2]],
    tags: { 0: { curat: 'g', curatat: 'g', profesional: 'g' }, 1: { apa: 'c', curata: 'g' } },
    capTop: 1035,
    items: [
      { k: 'note', t0: 0, t1: SEND, hard: true, box: [130, 1290, 950, 1578], fs: 50,
        ph: [[0, 'CURĂȚARE DPF · TURBO DOCTOR', 'Așa iese un filtru de particule <b style="color:#15803D">de la curățat</b>.', 48, 'soap', '#15803D'],
          [A.curatat - .05, 'CURĂȚARE DPF · TURBO DOCTOR', '<b style="color:#15803D">Curățat profesional</b> la Turbo Doctor.', 50, 'stethoscope', '#15803D'],
          [A.dupa10 - .05, 'TESTUL CU APĂ', 'Din filtrul de particule iese <b style="color:#0369A1">apă curată</b>.', 50, 'droplet', '#0369A1']] },
      { k: 'stamp', t: A.apa - .03, t1: SEND - .05, y: 340, txt: 'APĂ CURATĂ', col: 'green', s: .7, rot: -5 },
    ],
    fx: [
      { k: 'green', t0: A.curat - .05, t1: A.curat + .9, silent: true },
      { k: 'punch', t: A.apa, a: .05, sh: 5 }, { k: 'green', t0: A.apa - .05, t1: A.curataE + .6 },
    ],
    sfx: [[A.apa, 'shimmer', .55]],
    bursts: [[A.apa + .1, 540, 340, 6, 300, .8]],
  };
};
