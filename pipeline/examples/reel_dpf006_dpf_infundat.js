// v2 – DPF Doctor · „Ce se întâmplă dacă mergi cu DPF-ul înfundat?” (TikTok 7684883127470279958, 67 s, Sabin în halat)
// Footage exactly as filmed: wide shot by the car, DPF + turbo on the bench, wide shot by the engine, medium shot. Natural pace, no separate hook.
// The old teal word-boxes were replaced (caption_clean --txtbox fill) by our dark boxes on the same line; our captions sit on them (capTop).
// Lower rail (y ≈ 1300, under the captions) for cards when the face/engine fill the top of the frame.
window.REEL_CFG = ({ S0, SEND, TEND, WORDS }) => {
  const nn = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const near = (x, t) => { const c = WORDS.filter(w => nn(w.text) === nn(x)); if (!c.length) throw new Error('anchor not found: ' + x);
    const b = c.reduce((a, w) => Math.abs(w.os - t) < Math.abs(a.os - t) ? w : a); if (Math.abs(b.os - t) > 1.5) throw new Error('anchor too far: ' + x + ' ' + t + ' -> ' + b.os.toFixed(2)); return b; };
  const W = (x, t) => near(x, t).os, WE = (x, t) => near(x, t).oe;
  const A = {
    ce0: W('Ce', .22), cu0: W('cu', 2.24), infundat0: W('înfundat', 3.68), infundatE0: WE('înfundat', 3.68),
    ce1: W('Ce', 4.72), dupa: W('după', 9.12), turboE: WE('turbosuflantă', 9.68), un: W('Un', 10.96), infundat2: W('înfundat', 12.16), evacuarea: W('evacuarea', 14.4),
    in16: W('în', 16.16), uzura: W('uzura', 18.16), distrugerea: W('distrugerea', 19.52), turbosuflanteiE: WE('turbosuflantei', 20.16),
    problema: W('Problema', 21.34), un22: W('un', 22.69), nu24: W('nu', 24.45), strica: W('strica', 26.05), dar: W('dar', 28.21), aparitia: W('apariția', 29.57),
    interiorul: W('interiorul', 32.53), anexelor: W('anexelor', 34.93), rularea: W('Rularea', 36.53), distrugerea2: W('distrugerea', 41.65), motorE: WE('motor', 42.61),
    desigur: W('Desigur', 43.01), exceptionaleE: WE('excepționale', 44.61), ce45: W('Ce', 45.57), turbo48: W('Turbo', 48.21), diagnoza: W('Diagnoza', 50.77),
    gratuita: W('gratuită', 53.25), bucuresti: W('București', 55.41), iasi: W('Iași', 56.13), galati: W('Galați', 56.45), piatra: W('Piatra', 57.01),
    de58: W('De', 57.97), pentru: W('Pentru', 58.69), particuleE: WE('particule', 63.49), programeaza: W('Programează-te', 64.09), gratuitaE: WE('gratuită', 66.33),
  };
  const CUT1 = 4.57, CUT2 = 21.13, CUT3 = 36.53;   // wide → bench close-up → wide by the engine → medium shot
  return {
    capTop: 965, capLeft: 110, capHold: 1.6, capNoFade: true,   // captions on our dark boxes (old caption line, y 1038–1133), never leaving a box empty
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF', l1: 'CE SE ÎNTÂMPLĂ DACĂ MERGI', l1At: A.ce0 - .05, l2: 'CU DPF-UL ÎNFUNDAT?', l2At: A.cu0 - .04, l2Col: '#FF3B30', end: CUT1 - .05 },
    stages: [[A.ce1 - .1, 'RISC: TURBO'], [A.problema - .1, 'RISC: MOTOR'], [A.ce45 - .1, 'SOLUȚIA']],
    tags: {
      0: { infundat: 'r', turbosuflanta: 'c', incarcat: 'r', uzura: 'r', prematura: 'r', distrugerea: 'r', turbosuflantei: 'r' },
      1: { problema: 'r', strica: 'y', uzurii: 'r', premature: 'r', anexelor: 'c', distrugerea: 'r' },
      2: { exceptionale: 'y', diagnoza: 'g', complet: 'g', gratuita: 'g', bucuresti: 'y', iasi: 'y', galati: 'y', piatra: 'y', neamt: 'y', scuza: 'y' },
      3: { programeazate: 'g', diagnoza: 'g', complet: 'g', gratuita: 'g' },
    },
    items: [
      // bench close-up: DPF and turbo (wall at the top is free)
      { k: 'chip', t0: A.ce1 - .1, t1: A.un - .3, y: 330, ph: [[A.ce1 - .1, 'magnifying_glass_tilted_left', 'ATENȚIE:', 'blue'], [A.dupa - .05, 'dashing_away', 'DPF-UL E MONTAT DUPĂ TURBO', 'blue']] },
      { k: 'schem', t0: A.un - .15, t1: A.in16 - .25, top: 250, sc: .78, type: 'dpfFlow', title: 'SCHEMĂ · DPF ÎNFUNDAT', sub: 'SECȚIUNE', stepNames: ['ÎNFUNDAT'],
        steps: [[A.un - .15, 'Înfundat, încărcat: gazele nu mai ies corect', 'r', 'clog']] },
      { k: 'chip', t0: A.in16 - .1, t1: A.distrugerea - .3, y: 330, ph: [[A.in16 - .1, 'warning', 'PRIMA AFECTATĂ: TURBOSUFLANTA', 'red'], [A.uzura - .05, 'warning', 'UZURĂ PREMATURĂ', 'red']] },
      { k: 'stamp', t: A.distrugerea - .03, t1: CUT2 - .1, y: 330, txt: 'TURBO DISTRUS', col: 'red', s: .65, rot: -5 },
      // wide shot by the engine: patient file on the lower rail (under the captions)
      { k: 'file', t0: A.problema - .1, t1: CUT3 - .2, top: 1225, sc: .84, no: 'DPF', ecg: 'crit',
        rows: [[A.problema, 'PACIENT', 'DPF CU PROBLEME', 'c', 'stethoscope'], [A.nu24, 'PE MOMENT', 'NU STRICĂ NIMIC', 'y', 'hourglass'],
          [A.dar, 'ÎN TIMP', 'UZURĂ PREMATURĂ', 'r', 'warning'], [A.interiorul, 'AFECTEAZĂ', 'MOTORUL + ANEXELE', 'r', 'gear']] },
      // medium shot: face top-left, engine right → lower rail
      { k: 'stamp', t: A.distrugerea2 - .03, t1: A.motorE + .4, y: 1330, txt: 'MOTOR DISTRUS', col: 'red', s: .65, rot: -4 },
      { k: 'chip', t0: A.desigur - .1, t1: A.ce45 - .25, y: 1310, ph: [[A.desigur - .1, 'warning', 'ÎN SITUAȚII EXCEPȚIONALE', 'yellow']] },
      { k: 'chip', t0: A.ce45 - .1, t1: A.diagnoza - .25, y: 1310, ph: [[A.ce45 - .1, 'handshake', 'TURBO DOCTOR VĂ AJUTĂ', 'green']] },
      { k: 'chip', t0: A.diagnoza - .1, t1: A.de58 - .25, y: 1310, ph: [[A.diagnoza - .1, 'stethoscope', 'DIAGNOZĂ COMPLET GRATUITĂ', 'green'], [A.bucuresti - .05, 'round_pushpin', 'BUCUREȘTI', ''],
        [A.iasi - .05, 'round_pushpin', 'IAȘI', ''], [A.galati - .05, 'round_pushpin', 'GALAȚI', ''], [A.piatra - .05, 'round_pushpin', 'PIATRA NEAMȚ', 'blue']] },
      { k: 'chip', t0: A.de58 - .1, t1: A.programeaza - .25, y: 1310, ph: [[A.de58 - .1, 'thinking_face', 'DE CE?', 'yellow'], [A.pentru - .05, 'check_mark_button', 'CA SĂ N-AI NICIO SCUZĂ', 'green']] },
      { k: 'chip', t0: A.programeaza - .1, t1: SEND - .05, y: 1310, ph: [[A.programeaza - .1, 'calendar', 'PROGRAMEAZĂ-TE ACUM!', 'green']] },
    ],
    fx: [
      { k: 'red', t0: A.infundat0 - .05, t1: A.infundatE0 + .4, max: 1.2 }, { k: 'punch', t: A.infundat0, a: .05, sh: 6 },
      { k: 'red', t0: A.infundat2 - .05, t1: A.infundat2 + 1.0, max: 1.0 },
      { k: 'punch', t: A.distrugerea, a: .06, sh: 8 }, { k: 'red', t0: A.distrugerea - .05, t1: A.turbosuflanteiE + .3, max: 1.4 },
      { k: 'punch', t: A.distrugerea2, a: .06, sh: 8 }, { k: 'red', t0: A.distrugerea2 - .05, t1: A.motorE + .3, max: 1.2 },
      { k: 'green', t0: A.gratuita - .05, t1: A.gratuita + .9 },
      { k: 'green', t0: A.programeaza - .05, t1: A.gratuitaE, silent: true },
    ],
    sfx: [],
    bursts: [[A.gratuita, 540, 1310, 6, 300, .7]],
  };
};
