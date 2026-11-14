// v2 – Range Rover Velar 3.0 biturbo, „revizia de 80.000 km” (14.11.2026), IMG_2487 (motorul coborât de sub mașină, fără față)
// Sursa (src/cfr.mp4): 0–5.2 cadru AI „omul care plânge” (Veo 3.1 Fast, ElevenLabs, cu suspinele lui în audio/hook_bed.wav) peste
// „Range Rover, 3.0, Velar, biturbo” · 5.2 IMG_2487 de la „Venit la revizie” (imaginea în ordinea filmată, vocea neatinsă).
// Cerut de Sabin: hook puternic „mașina a venit la revizia de 80.000 km” + un om care plânge; părți interesante când vorbește de
// Range Rover; la final ecranul de diagnoză gratuită cu pictogramele serviciilor (turbine, injectoare, DPF, motoare) → endIcons.
// Reel organic: fără CTA grafic; îndemnul lui vorbit de la final („Vă așteptăm… la o diagnoză gratuită”) rămâne doar cu subtitrări.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    range0: aw(0, 'Range'), three: aw(0, '3.0'), velar: aw(0, 'Velar'), biturbo: aw(0, 'biturbo'), venit: aw(0, 'Venit'), revizie0: aw(0, 'revizie'),
    cum: aw(0, 'cum'), noi: aw(0, 'noi'),
    la1: aw(1, 'La'), daca: aw(1, 'dacă'), revizia1: aw(1, 'revizia'), n80: aw(1, '80.000'), km: aw(1, 'km'), se: aw(1, 'se'), schimbarea: aw(1, 'schimbarea'),
    turbinelor: aw(1, 'turbinelor'), curatarea: aw(1, 'curățarea'), admisie1: aw(1, 'admisie'), uneori: aw(1, 'Uneori'), surprize: aw(1, 'surprize'), motor1: aw(1, 'motor'),
    ce: aw(2, 'Ce'), bine: aw(2, 'bine'), turbo2: aw(2, 'Turbo'), ajuta2: aw(2, 'ajuta'), putem2b: aw(2, 'putem', 1), face2: aw(2, 'face'), profesional: aw(2, 'profesional'), toate: aw(2, 'toate'),
    sunt3: aw(3, 'Sunt'), frumoase: aw(3, 'frumoase'), pretentioase: aw(3, 'pretențioase'), probleme: aw(3, 'probleme'), la3: aw(3, 'La'), rezolvarea3: aw(3, 'rezolvarea'),
    corecta: aw(3, 'corectă'), atentie: aw(3, 'Atenție'), motorizari: aw(3, 'motorizări'), mainile: aw(3, 'mâinile'), habar: aw(3, 'habarniștilor'),
    devin: aw(4, 'devin'), daune1: aw(4, 'daune'), mii1: aw(4, 'mii'), zeci: aw(4, 'zeci'), euro2: aw(4, 'euro', 1), va4: aw(4, 'Vă'),
  };
  const CUT = 156 / 30;                                  // cadrul AI → IMG_2487 (chiar înainte de „Venit”)
  const T1 = .10, T2 = .46, T3 = .86;                     // impacturile titlului din hook
  const HD = CUT - .06;                                   // titlul hook-ului stă până la tăietură
  const BOOM2_END = A.va4 + .3;
  return {
    hook: null,
    stages: null,
    endIcons: true,                                       // pictogramele serviciilor pe ecranul de final (cerute de Sabin)
    hideCap: [[0, CUT + .02]],
    tags: {
      0: { range: 'c', rover: 'c', 30: 'y', velar: 'c', biturbo: 'c', revizie: 'y' },
      1: { range: 'c', rover: 'c', revizia: 'y', 80000: 'y', km: 'y', schimbarea: 'r', turbinelor: 'r', curatarea: 'r', admisie: 'c', surprize: 'r', motor: 'r' },
      2: { turbo: 'g', doctor: 'g', profesional: 'g', toate: 'g' },
      3: { frumoase: 'g', pretentioase: 'r', probleme: 'r', cunoscute: 'r', turbo: 'g', doctor: 'g', rezolvarea: 'g', corecta: 'g', atentie: 'r', habarnistilor: 'r' },
      4: { daune: 'r', mii: 'y', euro: 'y', zeci: 'r', diagnoza: 'g', gratuita: 'g', admisie: 'c', injectie: 'c', evacuare: 'c', motor: 'c' },
    },
    items: [
      // HOOK (cadru AI: omul plânge cu factura în mână; fața sus, titlul jos peste geacă)
      { k: 'boom', t: T1, dur: HD - T1, txt: 'A VENIT LA', y: 1185, size: 90, col: '#FFFFFF', from: 3.0, sh: 14, ca: 18, riser: false, bg: .7, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: T2, dur: HD - T2, txt: 'REVIZIA', y: 1318, size: 190, col: '#FFD21F', from: 3.6, sh: 28, ca: 30, riser: false, bg: 1 },
      { k: 'boom', t: T3, dur: HD - T3, txt: 'DE 80.000 KM', y: 1462, size: 120, col: '#FF4B4B', from: 3.4, sh: 22, ca: 26, riser: false, bg: .85, glow: 'rgba(255,75,75,.55)' },
      { k: 'stk', t0: T3 + .22, t1: HD - .04, ico: 'loudly_crying_face', x: 232, y: 1180, size: 118, rot: -10 },
      { k: 'chip', t0: A.range0 - .05, t1: HD, y: 186, ph: [[A.range0 - .05, 'automobile', 'RANGE ROVER', 'blue'], [A.three - .04, 'automobile', 'RANGE ROVER 3.0', 'blue'],
        [A.velar - .04, 'automobile', 'RANGE ROVER VELAR 3.0', 'blue'], [A.biturbo - .04, 'automobile', 'RANGE ROVER VELAR 3.0 BITURBO', 'blue']] },

      // IMG_2487: banda de sus pe tot reel-ul (fără partea cu îndemnul vorbit)
      { k: 'band', t0: CUT + .02, t1: A.va4 - .08, y: 222, kicker: 'RANGE ROVER', ph: [[CUT + .02, 'VELAR 3.0 BITURBO', 'PACIENT'], [A.revizia1 - .05, 'REVIZIA DE 80.000 KM', 'PACIENT'],
        [A.ce - .05, 'LA TURBO DOCTOR', 'TRATAMENT'], [A.sunt3 - .05, 'FRUMOASE, DAR PRETENȚIOASE', ''], [A.atentie - .05, 'ATENȚIE LA HABARNIȘTI', '']] },

      // „Venit la revizie, cum spunem noi” (cadre mișcate): fișa pacientului
      { k: 'file', t0: CUT + .04, t1: 8.35, top: 296, ecg: 'crit', rows: [
        [CUT + .1, 'PACIENT', 'Range Rover Velar', 'c', 'automobile'],
        [CUT + .2, 'UNITATE', '3.0 biturbo', 'c', 'gear'],
        [CUT + .3, 'RULAJ', '80.000 km', 'y', 'counter'],
        [A.revizie0 - .02, 'INTERNAT PENTRU', '„Revizie”', 'r', 'hammer_and_wrench']], stamp: [A.cum - .02, 'REVIZIE?!', 'red'] },

      // motorul coborât, cadru larg: „La Range Rover, dacă nu știați,”
      { k: 'chip', t0: A.daca - .05, t1: A.revizia1 - .3, y: 330, ph: [[A.daca - .05, 'eyes', 'DACĂ NU ȘTIAȚI...', 'yellow']] },
      // „revizia de 80.000 de km”: kilometrajul urcă până la 80.000
      { k: 'stat', t0: A.revizia1 - .05, t1: A.se - .25, top: 296, ico: 'counter', title: 'REVIZIA DE LA', unit: 'KM', from: 0, to: 80000, step: 1000, at: A.n80 - .45, dur: .85,
        sub: 'LA RANGE ROVER', subIco: 'automobile' },
      // „se face cu schimbarea turbinelor, curățarea întregului sistem de admisie. Uneori mai avem surprize și pe motor.”
      { k: 'list', t0: A.se - .05, t1: A.ce - .3, top: 296, ico: 'hammer_and_wrench', title: '„REVIZIA” DE 80.000 KM', rows: [
        [A.schimbarea - .03, 'SCHIMBAREA TURBINELOR'], [A.curatarea - .03, 'CURĂȚAREA SISTEMULUI DE ADMISIE'], [A.surprize - .03, 'SURPRIZE ȘI PE MOTOR', 'bad']] },
      { k: 'kin', t: A.turbinelor + .06, dur: 1.25, txt: 'BITURBO = 2 TURBINE', y: 1060, size: 96, col: '#FFD21F' },
      { k: 'stamp', t: A.motor1 - .02, t1: A.ce - .35, txt: 'SURPRIZĂ!', col: 'red', y: 1040, rot: -8 },

      // „Ce este bine, în schimb, este că la Turbo Doctor vă putem ajuta și le putem face profesional pe toate.”
      { k: 'chip', t0: A.ce - .05, t1: A.turbo2 - .3, y: 330, ph: [[A.ce - .05, 'sparkles', 'PARTEA BUNĂ', 'green']] },
      { k: 'pipe', t0: A.turbo2 - .1, t1: A.sunt3 - .3, top: 296, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR', steps: [
        [A.ajuta2 - .03, 'svc_turbo', 'TURBINE'], [A.putem2b - .03, 'broom', 'ADMISIE'], [A.face2 - .03, 'svc_motor', 'MOTOR']] },
      { k: 'stamp', t: A.profesional - .02, t1: A.sunt3 - .35, txt: 'PROFESIONAL', col: 'green', y: 1040, rot: -6 },

      // „Sunt niște mașini foarte frumoase, dar foarte pretențioase, cu niște probleme cunoscute.”
      { k: 'gauge', t0: A.sunt3 - .05, t1: A.la3 - .3, top: 296, ico: 'automobile', title: 'NIVEL DE PRETENȚII', sub: 'RANGE ROVER', ends: ['MIC', 'MAXIM'],
        needle: [[A.sunt3, .12], [A.frumoase, .3], [A.pretentioase, .97]],
        read: [[A.frumoase, 'FOARTE FRUMOASE', '#4ADE80'], [A.pretentioase, 'FOARTE PRETENȚIOASE', '#FF4B4B'], [A.probleme - .03, 'PROBLEME CUNOSCUTE', '#FF4B4B']] },
      // „La Turbo Doctor vă putem ajuta cu rezolvarea corectă a lor.”
      { k: 'chip', t0: A.la3 - .05, t1: A.atentie - .3, y: 330, ph: [[A.la3 - .05, 'stethoscope', 'LA TURBO DOCTOR', 'blue'], [A.rezolvarea3 - .05, 'check_mark_button', 'REZOLVARE CORECTĂ', 'green']] },

      // „Atenție, deoarece atunci când aceste motorizări ajung pe mâinile habarniștilor,”
      { k: 'stamp', t: A.atentie - .02, t1: A.motorizari - .3, txt: 'ATENȚIE!', col: 'red', y: 640, rot: -7 },
      { k: 'chip', t0: A.motorizari - .05, t1: A.habar - .45, y: 330, ph: [[A.motorizari - .05, 'gear', 'ACESTE MOTORIZĂRI', 'blue'], [A.mainile - .05, 'warning', 'PE MÂINI GREȘITE...', 'red']] },
      { k: 'def', t0: A.habar - .15, t1: A.devin - .3, top: 296, term: 'HABARNIST', text: 'Cel care repară fără să aibă habar și învață pe mașina ta.' },

      // „devin efectiv niște daune de mii de euro, daune de zeci de mii de euro.”
      { k: 'chip', t0: A.devin - .05, t1: A.mii1 - .35, y: 330, ph: [[A.devin - .05, 'money_with_wings', 'DEVIN EFECTIV DAUNE', 'red']] },
      { k: 'boom', t: A.mii1, dur: BOOM2_END - A.mii1, txt: 'MII DE €', y: 560, size: 170, col: '#FFD21F', from: 3.0, sh: 18, ca: 22, riser: false, bg: .55, cg: .35 },
      { k: 'boom', t: A.zeci, dur: BOOM2_END - A.zeci, txt: 'ZECI DE MII DE €!', y: 780, size: 116, col: '#FF4B4B', from: 3.4, sh: 26, ca: 28, riser: false, bg: .7, cg: .4, glow: 'rgba(255,75,75,.6)' },
      { k: 'stk', t0: A.mii1 + .1, t1: BOOM2_END, ico: 'money_with_wings', x: 160, y: 1000, size: 130, rot: -12 },
      { k: 'stk', t0: A.zeci + .1, t1: BOOM2_END, ico: 'money_with_wings', x: 915, y: 960, size: 120, rot: 10 },
    ],
    fx: [
      // hook
      { k: 'punch', t: T1, a: .06, sh: 12 }, { k: 'glitch', t: T1, d: .12 },
      { k: 'flash', t: T2 - .11, a: .7 }, { k: 'punch', t: T2, a: .15, sh: 32 }, { k: 'glitch', t: T2, d: .16 },
      { k: 'shock', t: T2 + .01, x: 540, y: 1318, r: 700, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'punch', t: T3, a: .1, sh: 22 }, { k: 'shock', t: T3 + .01, x: 540, y: 1462, r: 620, n: 1, col: '#FF4B4B' },
      // intrarea în filmarea lui
      { k: 'glitch', t: CUT - .03, d: .12 },
      { k: 'punch', t: A.n80, a: .05, sh: 10 }, { k: 'punch', t: A.turbinelor, a: .05, sh: 10 }, { k: 'punch', t: A.motor1, a: .05, sh: 12 },
      { k: 'punch', t: A.pretentioase, a: .05, sh: 10 }, { k: 'punch', t: A.atentie, a: .06, sh: 14 },
      // daunele
      { k: 'punch', t: A.mii1, a: .07, sh: 14 }, { k: 'shock', t: A.mii1 + .01, x: 540, y: 560, r: 560, n: 1, col: '#FFD21F' },
      { k: 'flash', t: A.zeci - .11, a: .45 }, { k: 'punch', t: A.zeci, a: .12, sh: 26 }, { k: 'glitch', t: A.zeci, d: .16 },
      { k: 'shock', t: A.zeci + .01, x: 540, y: 780, r: 640, n: 2, col: '#FF4B4B', col2: '#FFFFFF' },
    ],
    sfx: [[CUT - .12, 'whoosh', .5]],
    bursts: [[T2 + .04, 540, 1318, 8, 460, 1.3], [T3 + .04, 540, 1462, 6, 380, 1.1], [A.zeci + .04, 540, 780, 7, 420, 1.2]],
  };
};
