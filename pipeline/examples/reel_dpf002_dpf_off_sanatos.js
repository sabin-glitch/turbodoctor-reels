// v2 – DPF Doctor · „DPF/EGR OFF = motor sănătos?” (TikTok 7685256912702688534, răspuns la comentariu)
// Footage exactly as filmed (teaser 0–3.3 s, selfie, Euro 6 cu DPF, BMW F30 DPF/EGR OFF), natural pace, no separate hook.
// The burned TikTok reply bubble is covered by our own comment card glued to the same spot for the whole clip.
// Old burned title „Bmw Seria 3 F30 DPF-EGR OFF” removed (caption_clean, 0–3.3 s) → now in the hook car chip. Plate blurred 10.55–11.45 s.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    nu: aw(0, 'Nu'), nimic: aw(0, 'nimic'), sanatos0: aw(0, 'sănătos'), dpf0: aw(0, 'DPF/EGR'), offE: ew(0, 'OFF'),
    hai1: aw(1, 'hai'), ceE1: ew(1, 'ce'), masina: aw(1, 'Mașină'), euro1: aw(1, 'Euro'), toate: aw(1, 'toate'), activeE: ew(1, 'active'),
    praf: aw(2, 'Praf'), pe: aw(2, 'Pe'), evacE: ew(2, 'evacuare'), si2: aw(2, 'Și'), tot: aw(2, 'tot'), sixE: ew(2, '6'),
    cunoasteti: aw(3, 'Cunoașteți'), seria: aw(3, 'Seria'), f30E: ew(3, 'F30'), hopa: aw(3, 'Hopa'),
    ce4: aw(4, 'Ce'), aiciE: ew(4, 'aici'), asta4: aw(4, 'Asta'), sanatos4: aw(4, 'sănătos'), daca4: aw(4, 'Dacă'), sanatos4b: aw(4, 'sănătos', 1),
    inseamna: aw(5, 'înseamnă'), problema: aw(5, 'problemă'), astaE5: ew(5, 'asta'),
  };
  const HOOK_OUT = 3.25;          // teaser (finger in the black tailpipe) ends at 3.30 s → selfie
  return {
    // hook over the teaser only (no speech there); stack sits low so the comment card (top-left) and the black fingertip stay visible
    hook: { tag: 'ANALIZĂ TEHNICĂ · DPF/EGR OFF', l1: 'DPF OFF = MOTOR <span class="g">SĂNĂTOS</span>?', l1At: .3, l2: 'FALS!', l2At: 1.25, l2Col: '#FF3B30',
      car: 'BMW SERIA 3 F30 · DPF + EGR OFF', carAt: 2.0, y: 900, end: HOOK_OUT },
    hideCap: [[0, HOOK_OUT + .03]],
    stages: [[A.masina - .05, 'DPF ACTIV'], [A.si2 - .05, 'DPF/EGR OFF'], [A.ce4 - .1, 'VERDICT']],
    tags: {
      0: { sanatos: 'g', dpfegr: 'r', off: 'r' }, 1: { euro: 'c', antipoluare: 'g', active: 'g' },
      2: { praf: 'g', euro: 'c' }, 3: { seria: 'c', hopa: 'r' }, 4: { sanatos: 'r' }, 5: { problema: 'r', mare: 'r' },
    },
    items: [
      // the comment he answers (replaces the burned TikTok reply bubble: same place, same size, glued to the footage)
      { k: 'note', t0: 0, t1: SEND, hard: true, box: [66, 314, 590, 650], fs: 38, label: 'COMENTARIU',
        text: '„Te contrazic: dacă faci DPF/EGR OFF, va fi un motor sănătos și de lungă durată”' },
      // selfie: compact, right of the card, above his head
      { k: 'chip', t0: A.nimic - .1, t1: A.offE + .35, x: 812, y: 410, ph: [[A.nimic - .1, 'thinking_face', '„SĂNĂTOS”?', ''], [A.dpf0 - .05, 'cross_mark', 'NU CU DPF OFF!', 'red']] },
      // Euro 6 with all anti-pollution systems on (10–29 s: chips on the lower rail, above the captions, so the tailpipes stay clear)
      { k: 'chip', t0: A.masina - .1, t1: A.activeE + .3, y: 1150, ph: [[A.masina - .1, 'check_mark_button', 'MAȘINĂ EURO 6', 'green'], [A.toate - .05, 'shield', 'ANTIPOLUARE: TOATE ACTIVE', 'green']] },
      { k: 'chip', t0: A.praf - .1, t1: A.evacE + .4, y: 1150, ph: [[A.praf - .1, 'sparkles', 'DOAR PRAF', 'green'], [A.pe - .05, 'check_mark_button', 'EVACUARE CURATĂ', 'green']] },
      // BMW F30 with DPF + EGR OFF
      // wide shots of the BMW (pipe low in frame) → chips up over the bumper; close-up of the pipe (from ~26 s) → lower rail
      { k: 'chip', t0: A.si2 - .1, t1: A.sixE + .3, y: 800, ph: [[A.si2 - .1, 'magnifying_glass_tilted_left', 'ACUM: TOT UN EURO 6', 'blue']] },
      { k: 'chip', t0: A.cunoasteti - .1, t1: A.seria - .45, y: 800, ph: [[A.cunoasteti - .1, 'automobile', 'BMW SERIA 3 F30', '']] },
      { k: 'chip', t0: A.seria - .05, t1: A.hopa - .25, y: 1150, ph: [[A.seria - .05, 'cross_mark', 'BMW F30 · DPF + EGR OFF', 'red']] },
      { k: 'stamp', t: A.hopa - .03, t1: A.hopa + 1.6, y: 760, txt: 'FUNINGINE!', col: 'red', s: .7, rot: -5 },
      { k: 'kin', t: A.sanatos4 - .03, dur: 1.1, txt: 'SĂNĂTOS?!', col: '#FF3B30', y: 760, size: 150, rot: -4 },
      // verdict = the finger test
      { k: 'cmp', t0: A.daca4 - .15, t1: A.astaE5 + .3, top: 690, title: 'TESTUL DEGETULUI', ico: 'magnifying_glass_tilted_left', aCls: 'ok', bCls: 'bad', big: true,
        a: [A.daca4 + .1, 'check_mark_button', 'EURO 6 CU DPF', 'PRAF'], b: [A.sanatos4b, 'cross_mark', 'DPF/EGR OFF', 'FUNINGINE'] },
    ],
    fx: [
      { k: 'xray', t0: .15, t1: .72 }, { k: 'punch', t: .8, a: .05, sh: 6 }, { k: 'red', t0: .8, t1: 2.1, max: 1.3 },
      { k: 'green', t0: A.praf - .05, t1: A.praf + .9, silent: true },
      { k: 'punch', t: A.seria, a: .03, sh: 4 },
      { k: 'punch', t: A.hopa, a: .06, sh: 8 }, { k: 'red', t0: A.hopa - .05, t1: A.hopa + 1.5, max: 1.5 },
      { k: 'red', t0: A.sanatos4 - .05, t1: A.sanatos4 + 1.0, max: 1.0 }, { k: 'punch', t: A.sanatos4, a: .04, sh: 5 },
      { k: 'punch', t: A.problema, a: .04, sh: 5 }, { k: 'red', t0: A.problema - .05, t1: A.astaE5, max: 1.3 },
    ],
    sfx: [[A.praf, 'shimmer', .5]],
    bursts: [],
  };
};
