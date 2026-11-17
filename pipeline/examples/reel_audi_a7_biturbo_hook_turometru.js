// v2 – Reel „Audi A7 biturbo, în reparație la Turbo Doctor” (IMG_2552, un singur clip, fără tăieturi, ritm natural)
// Cerut de Sabin pe 17.11.2026: „hook puternic, Audi A7 biturbo și cu un turometru care se accelerează puternic, în reparație la Turbo Doctor”.
// HOOK: titlu boom în patru rânduri cu textul dat de el („AUDI A7 / BITURBO / ÎN REPARAȚIE LA / TURBO DOCTOR”) + piesa nouă `tach`:
// un turometru al cărui ac NU e animat de mână, ci urmează turația unei turări reale de turbodiesel (Freesound 865222, CC0) care se aude în hook
// (tools/tach/build_tach_bed.py -> audio/hook_bed.wav + out/track_tach.json). Prima turare e în cele 1,5 s de liniște de la început
// („BITURBO” bubuie când acul intră în zona roșie), a doua în pauza dinaintea cuvântului lui „Biturbo” (titlul mai bubuie o dată pe cuvânt).
// Filmare doar cu motorul (fără față, fără plăcuțe de înmatriculare) -> cardurile stau sus. Fără CTA pe imagine (25.10). Fără accente roșu/verde pe tot cadrul.
// Livrat lui Sabin pe 17.11.2026, în așteptarea aprobării. out/v2.json: {"tip": {"dur": 3.4, "src": 39.45, "speed": 0.07}, "beds": [{"wav": "audio/hook_bed.wav", "t": 0, "gain": 1.0, "duck": 0}], "music_in": 4.6};
// out/cover_t.json: {"t": 4.1}; fixwords.py 1=2.35 2=3.68 15=9.27 42=20.08 51=25.46 53=26.05 76=35.88; build_tach_bed.py <reel> 1.00 3.66 4.90 cu TACH_DUCK='[[1.50,2.98,-9],[3.62,5.0,-11]]'.
// Urmăriri (track_point.py): track_turbo 240 304 270 810 1110 · track_chra 396 440 408 385 965 · track_wheel 655 706 678 604 795. Pașii: tools/tach/README.md.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    motorizarea: aw(1, 'motorizarea'), bitdi: aw(1, 'BiTDI'), ajunsa: aw(1, 'ajunsă'), lanoi: aw(1, 'noi', 0), probleme: aw(1, 'probleme'), zona: aw(1, 'zona'), supra: aw(1, 'supraalimentare'),
    turbinele: aw(1, 'Turbinele'), recond: aw(1, 'recondiționate'), complet: aw(1, 'complet'), cu1: aw(1, 'cu', 0), ansamble: aw(1, 'ansamble'), centrale: aw(1, 'centrale'), noi2: aw(1, 'noi', 1),
    si1: aw(1, 'și'), urmeaza: aw(1, 'urmează'), aceasta: aw(1, 'această'), plece: aw(1, 'plece'), cu2: aw(1, 'cu', 1), garantie: aw(1, 'garanție'), n24: aw(1, '24'), luni: aw(1, 'luni'),
    fara: aw(1, 'fără'), limita: aw(1, 'limită'), km: aw(1, 'kilometri'), cu3: aw(1, 'cu', 2), turbine: aw(1, 'turbine'), ca: aw(1, 'ca', 1), noi4: aw(1, 'noi', 3),
    reducerea: aw(2, 'Reducerea'), fata: aw(2, 'față'), schimbarea: aw(2, 'schimbarea'), cuT: aw(2, 'cu'), e2: aw(2, 'e'), ordinul: aw(2, 'ordinul'), miilor: aw(2, 'miilor'), euro2: aw(2, 'euro'),
    clientul: aw(3, 'Clientul'), vina: aw(3, 'vină'), timp: aw(3, 'timp'), recond3: aw(3, 'recondiționarea'), posibila: aw(3, 'posibilă'), devizul: aw(3, 'devizul'), scazut: aw(3, 'scăzut'), mii: aw(3, 'mii'),
  };
  // HOOK. Momentele sunt începuturile de cuvânt din anvelopa vocii (Audi 1,55 · 3.0 2,35 · Biturbo 3,68 · motorizarea 5,01); primele 1,5 s sunt fără voce.
  // B2 = momentul în care acul ajunge sus prima dată (T_top1 din build_tach_bed.py); K = cuvântul lui „Biturbo” (acul e din nou sus, T_top2 = 3,66).
  const B1 = .12, B2 = 1.00, B3 = 1.55, B4 = 2.35, K = 3.68, HB = 4.85;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · 3.0 BiTDI', end: HB },
    hideCap: [[0, HB - .05]],
    stages: [[HB + .45, 'PACIENTUL'], [A.turbinele - .35, 'TRATAMENTUL'], [A.si1 - .05, 'GARANȚIA'], [A.reducerea - .08, 'ECONOMIA']],
    tags: {
      0: { audi: 'c' },
      1: { biturbo: 'c', motorizarea: 'c', bitdi: 'y', 'noi#0': '', zona: 'c', supraalimentare: 'c', turbinele: 'c', complet: 'g', ansamble: 'c', centrale: 'c', 'noi#2': '', luni: 'y', fara: 'g', limita: 'g', kilometri: 'y' },
      2: { reducerea: 'g', noi: '', ordinul: '', miilor: 'y', euro: 'y' },
      3: { timp: 'g', noi: '', reconditionarea: 'g', posibila: 'g', devizul: 'c', scazut: 'g', mii: 'y', euro: 'y' },
    },
    items: [
      // ---- hook: turometrul (sub titluri) + boom în patru rânduri; „BITURBO” mai bubuie o dată pe cuvântul lui
      { k: 'tach', t0: -.4, t1: HB - .12, x: 540, y: 985, s: .82, kick: [B2, K] },
      { k: 'boom', t: B1, dur: HB - B1, txt: 'AUDI A7', y: 368, size: 190, col: '#FFFFFF', from: 2.4, sh: 12, ca: 14, riser: false, bg: .55, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: K - B2 + .06, txt: 'BITURBO', y: 592, size: 256, col: '#FFD21F', from: 3.8, sh: 24, ca: 30, riser: false, bg: 1 },
      { k: 'boom', t: K, dur: HB - K, txt: 'BITURBO', y: 592, size: 256, col: '#FFD21F', from: 1.7, sh: 22, ca: 30, riser: false, bg: .45, cg: .12 },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'ÎN REPARAȚIE LA', y: 1318, size: 100, col: '#FFFFFF', from: 2.4, sh: 10, ca: 12, riser: false, bg: .45, cg: .3, glow: 'rgba(98,216,255,.45)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'TURBO <span style="color:#FFD21F">DOCTOR</span>', y: 1466, size: 132, col: '#FFFFFF', from: 2.8, sh: 16, ca: 20, riser: false, bg: .7 },
      // ---- fișa pacientului („motorizarea BiTDI, ajunsă la noi pentru mai multe probleme pe zona de supraalimentare”)
      { k: 'file', t0: A.motorizarea - .08, t1: A.turbinele - .4, top: 268, no: '2552', ecg: 'crit',
        rows: [[A.motorizarea, 'PACIENT', 'AUDI A7 · 3.0 BiTDI', 'c', 'automobile'], [A.lanoi - .22, 'INTERNAT LA', 'TURBO DOCTOR', 'y', 'round_pushpin'],
          [A.probleme - .02, 'SIMPTOME', '<span style="font-size:29px">PROBLEME PE ZONA DE SUPRAALIMENTARE</span>', 'r', 'warning']] },
      { k: 'scan', t0: A.zona - .2, t1: 9.72, track: 'track_turbo', box: [0, 0, 480, 480], lab: 'SCANARE...', lab2: 'SUPRAALIMENTARE', at2: A.supra - .03 },
      // ---- tratamentul („Turbinele au fost recondiționate complet, cu ansamble centrale noi”)
      { k: 'ecg', t0: A.turbinele - .38, t1: A.ansamble - .1, top: 268, label: 'PULS TURBINE', ico: 'stethoscope',   // intră în pauza dinaintea frazei: alarma EKG-ului nu acoperă „Turbinele”
        states: [[A.turbinele - .38, 'crit', 'ÎN TRATAMENT'], [A.recond - .02, 'ok', 'RECONDIȚIONATE'], [A.complet - .02, 'ok', 'RECONDIȚIONATE COMPLET']] },
      { k: 'def', t0: A.ansamble + .08, t1: A.aceasta - .15, top: 262, term: 'ANSAMBLU CENTRAL', text: 'Miezul turbinei: axul cu cele două rotoare și lagărele lui.' },
      { k: 'call', t0: A.cu1 - .2, t1: 14.26, track: 'track_chra', p: [385, 965], lab: [560, 1200], h: 'ANSAMBLU CENTRAL', v: 'NOU', col: 'green', cps: 60 },
      // ---- garanția („urmează ca această mașină să plece de la noi cu o garanție de 24 de luni, fără limită de kilometri, cu turbine ca noi”)
      { k: 'chip', t0: A.aceasta - .05, t1: A.cu2 - .2, y: 330, ph: [[A.aceasta - .05, 'automobile', 'URMEAZĂ EXTERNAREA', 'green']] },
      { k: 'stat', t0: A.cu2 - .02, t1: A.cu3 - .25, top: 268, ico: 'shield', title: 'GARANȚIE', to: 24, unit: 'LUNI', at: A.n24 - .38, dur: .5 },
      { k: 'stamp', t: A.fara + .03, t1: A.cu3 - .3, y: 700, txt: 'FĂRĂ LIMITĂ DE KM', col: 'green', s: .8, rot: -5 },
      { k: 'ring', t0: A.turbine - .1, t1: 23.36, track: 'track_wheel', p: [604, 795], r: 185, col: '#4ADE80' },
      { k: 'stamp', t: A.ca - .02, t1: 23.5, y: 1150, txt: 'CA NOI', col: 'green', s: 1.0, rot: -6 },
      // ---- economia („Reducerea față de schimbarea cu turbine noi e de ordinul miilor de euro”)
      { k: 'chip', t0: A.reducerea - .05, t1: A.fata - .2, y: 330, ph: [[A.reducerea - .05, 'chart_down', 'REDUCEREA', 'green']] },
      { k: 'cmp', t0: A.fata - .06, t1: A.e2 - .2, top: 268, ico: 'euro_banknote', title: 'RECONDIȚIONARE vs. TURBINE NOI', aCls: 'ok', bCls: 'bad',
        a: [A.fata + .02, 'hammer_and_wrench', 'RECONDIȚIONARE', 'COST REDUS'], b: [A.cuT - .02, 'money_with_wings', 'TURBINE NOI', 'PREȚ ÎNTREG'] },
      { k: 'chip', t0: A.e2 - .02, t1: A.clientul - .3, y: 330, ph: [[A.e2 - .02, 'money_bag', 'REDUCERE DE ORDINUL...', 'yellow']] },
      { k: 'kin', t: A.miilor - .02, dur: 1.75, txt: 'MII DE EURO', col: '#FFD21F', y: 1080, size: 190, rot: -4 },
      // ---- bilanțul („Clientul a reușit să vină la timp la noi, recondiționarea a fost posibilă și devizul final a fost scăzut cu mii de euro”)
      { k: 'list', t0: A.clientul - .08, t1: SEND - .3, top: 268, ico: 'stethoscope', title: 'BILANȚUL CAZULUI', w: 640,
        rows: [[A.timp - .02, 'CLIENTUL A VENIT LA TIMP'], [A.posibila - .02, 'RECONDIȚIONARE POSIBILĂ'], [A.scazut - .02, 'DEVIZ FINAL SCĂZUT']] },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · TURBO', ico: 'stethoscope',
        rows: [[SEND + .35, 'stopwatch', 'Luată la timp, turbina se poate recondiționa'], [SEND + 1.15, 'gear', 'Recondiționare cu ansamble centrale noi'],
          [SEND + 1.95, 'shield', 'Garanție 24 de luni, fără limită de kilometri']] },
    ],
    fx: [
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: 592, r: 760, n: 2, col: '#FFD21F' },
      { k: 'punch', t: B3, a: .05, sh: 10 }, { k: 'flash', t: B4 - .11, a: .4 }, { k: 'punch', t: B4, a: .08, sh: 16 },
      { k: 'flash', t: K - .11, a: .55 }, { k: 'punch', t: K, a: .13, sh: 28 },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'punch', t: A.supra, a: .06, sh: 10 }, { k: 'glitch', t: A.turbinele - .42, d: .12 }, { k: 'punch', t: A.complet, a: .05, sh: 6 },
      { k: 'glitch', t: A.si1 - .12, d: .12 }, { k: 'punch', t: A.n24, a: .07, sh: 10 }, { k: 'punch', t: A.fara + .16, a: .05, sh: 8 }, { k: 'punch', t: A.ca, a: .06, sh: 10 },
      { k: 'glitch', t: A.reducerea - .15, d: .12 }, { k: 'flash', t: A.miilor - .12, a: .4 }, { k: 'punch', t: A.miilor, a: .1, sh: 18 },
      { k: 'punch', t: A.timp, a: .04, sh: 6 }, { k: 'punch', t: A.scazut, a: .06, sh: 10 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.complet + .05, 'shimmer', .5], [A.n24 + .12, 'shimmer', .45], [A.scazut + .1, 'shimmer', .5]],
    bursts: [[A.n24 + .14, 540, 430, 6, 360, .9], [A.miilor + .08, 540, 1080, 6, 440, 1.0], [A.scazut + .1, 560, 860, 6, 300, .9]],
  };
};
