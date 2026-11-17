// v2 – Reel „Testare finală injectoare Bosch pe stand original Bosch DCI 700” (IMG_2565, un singur clip de 16,7 s, fără tăieturi, ritm natural)
// Cerut de Sabin pe 17.11.2026: editare „fain”, cu hook puternic, a clipului în care prezintă testarea și codarea finală a unor injectoare Bosch
// pe standul Bosch DCI 700. Textul hook-ului e cel dat de el: „Testare finală injectoare Bosch pe stand original Bosch DCI700”.
// Filmare fără față: standul (eticheta BOSCH DCI 700), injectoarele montate, prim-plan pe codul gravat pe un injector, apoi monitorul standului.
// Standul merge în tot clipul: sunetul trece întâi prin denoise_bench.py (zgomotul standului coboară sub voce), iar cuvintele au timpii puși de mână (fix_words.py).
// Ce spune el: „Proces de testare și codare injectoare Bosch. Injectoarele au fost recondiționate capital și acum sunt în procesul final de codare.”
// De pe imagine: codul piesei gravat pe injector (0445110 374, același cu cel de pe monitor: „0445110374 | CRI 2-16”) și pașii de verificare cu „Ok” de pe monitor.
// Explicația mea, de confirmat cu el: cardul „CODARE (IMA)”. Fără CTA pe imagine (25.10). Fără accente roșu/verde pe tot cadrul (neconfirmate).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    proces: aw(0, 'Proces'), testare: aw(0, 'testare'), codare: aw(0, 'codare'), injectoare: aw(0, 'injectoare'), bosch: aw(0, 'Bosch'), boschE: ew(0, 'Bosch'),
    injectoarele: aw(0, 'Injectoarele'), recond: aw(0, 'recondiționate'), capital: aw(0, 'capital'), capitalE: ew(0, 'capital'),
    si2: aw(0, 'și', 1), acum: aw(0, 'acum'), procesul: aw(0, 'procesul'), final: aw(0, 'final'), codare2: aw(0, 'codare', 1), codare2E: ew(0, 'codare', 1),
  };
  // HOOK: titlu boom în patru trepte, cu textul dat de Sabin. Primele trei rânduri cad înainte să înceapă vocea (ea pornește la 0,95 s),
  // iar impactul mare, „BOSCH DCI 700”, pe primul lui cuvânt („Proces”). După el nu mai e nicio bubuitură peste voce.
  // Două rânduri sus și două jos: eticheta standului, apoi injectoarele rămân la vedere în mijlocul cadrului.
  const B1 = .12, B2 = .40, B3 = .66, B4 = A.proces - .02, HB = 3.5;
  const Y1 = 285, Y2 = 452, Y3 = 1158, Y4 = 1345;
  // prim-planul fără voce (5,6–8,3 s): scanarea codului gravat pe injector; blocarea pe codul piesei
  const SC0 = 5.75, LOCK = 6.75, SC1 = 8.15;
  return {
    hook: { tag: 'LABORATOR TURBO DOCTOR · INJECȚIE', end: HB, y: -76 },
    hideCap: [[0, HB - .05]],
    stages: [[HB + .45, 'PACIENȚII'], [SC0 - .05, 'CODUL'], [A.injectoarele - .08, 'TRATAMENTUL']],
    tags: { 0: { testare: 'g', codare: 'y', injectoare: 'c', bosch: 'c', injectoarele: 'c', reconditionate: 'g', capital: 'g', final: 'y' } },
    items: [
      // ---- hook: boom în patru trepte
      { k: 'boom', t: B1, dur: HB - B1, txt: 'TESTARE FINALĂ', y: Y1, size: 150, col: '#FFFFFF', from: 2.6, sh: 14, ca: 16, riser: false, bg: .6, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'INJECTOARE BOSCH', y: Y2, size: 124, col: '#62D8FF', from: 2.4, sh: 12, ca: 14, riser: false, bg: .5, cg: .35, glow: 'rgba(98,216,255,.55)' },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'PE STAND ORIGINAL', y: Y3, size: 112, col: '#FFFFFF', from: 2.4, sh: 12, ca: 14, riser: false, bg: .5, cg: .35, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'BOSCH DCI 700', y: Y4, size: 168, col: '#FFD21F', from: 3.8, sh: 26, ca: 30, bg: 1 },
      // ---- fișa pacientului, pe „injectoare Bosch”
      { k: 'file', t0: HB + .05, t1: 7.0, top: 268, no: '2565', ecg: 'ok',
        rows: [[A.injectoare - .03, 'PACIENT', 'INJECTOARE BOSCH', 'c', 'svc_injector'], [A.bosch - .03, 'STAND', 'BOSCH DCI 700', 'y', 'microscope'],
          [A.boschE + .25, 'PROCEDURĂ', 'TESTARE + CODARE', 'g', 'test_tube']] },
      // ---- prim-planul: citirea codului gravat pe injector (codul piesei e cel care se vede pe injector și pe monitor)
      { k: 'scan', t0: SC0, t1: SC1, track: 'track_code', box: [0, -15, 430, 390], lab: 'CITIRE COD INJECTOR...', lab2: 'BOSCH 0 445 110 374', at2: LOCK, col2: '#4ADE80' },
      // ---- ce înseamnă codarea (explicația mea, de confirmat cu Sabin)
      { k: 'def', t0: 7.3, t1: A.injectoarele - .35, top: 268, term: 'CODARE (IMA)', text: 'După testare, fiecare injector primește un cod de corecție, calculat din măsurătorile de pe stand.' },
      // ---- tratamentul: pașii se aprind pe ce spune
      { k: 'pipe', t0: A.injectoarele - .05, t1: SEND - .12, top: 268, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.recond - .03, 'hammer_and_wrench', 'RECONDIȚIONARE<br>CAPITALĂ'], [A.acum - .03, 'microscope', 'TESTARE<br>PE STAND'], [A.codare2 - .03, 'counter', 'CODARE<br>FINALĂ']] },
      { k: 'stamp', t: A.recond - .03, t1: A.si2 - .2, y: 760, txt: 'RECONDIȚIONATE CAPITAL', col: 'green', s: .78, rot: -6 },
      // ---- monitorul standului: pașii de verificare făcuți până acum au „Ok”
      { k: 'call', t0: 15.2, t1: SEND - .1, track: 'track_mon', p: [450, 815], lab: [372, 1212], h: 'PAȘI DE VERIFICARE', v: 'OK · OK · OK', col: 'green', cps: 60 },
    ],
    fx: [
      // hook: patru impacturi (ultimul = cel mare)
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 },
      { k: 'punch', t: B2, a: .05, sh: 10 }, { k: 'punch', t: B3, a: .05, sh: 10 },
      { k: 'flash', t: B4 - .11, a: .75 }, { k: 'punch', t: B4, a: .16, sh: 34 }, { k: 'glitch', t: B4, d: .2 }, { k: 'shock', t: B4 + .01, x: 540, y: Y4, r: 760, n: 2, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'punch', t: LOCK, a: .06, sh: 8 }, { k: 'glitch', t: 7.2, d: .1 },
      { k: 'glitch', t: A.injectoarele - .15, d: .12 }, { k: 'flash', t: A.recond - .14, a: .3 }, { k: 'punch', t: A.recond - .03, a: .09, sh: 16 },
      { k: 'punch', t: A.codare2, a: .07, sh: 10 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.codare2 + .04, 'shimmer', .5]],
    bursts: [[A.recond + .03, 540, 760, 6, 440, 1.0], [A.codare2 + .08, 880, 420, 5, 150, .8]],
  };
};
