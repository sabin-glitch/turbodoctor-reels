// v2 – PROMO plătit (28.10.2026): „A venit iarna și mașina pornește tot mai greu” → injectoare + pompa de înaltă presiune la Turbo Doctor
// Sursa (hook_src.mp4): 0 cadru AI „pornește greu” (demaror care se chinuie, motorul prinde după „greu”) · 4.933 cadru AI „motor care trepidează”
// · 7.833 IMG_1879 (selfie, de la „Ei bine”) · 12.353 IMG_1880 (pompa + injectorul) · 21.205 IMG_1881 (pompa + injectorul) · 31.905 IMG_1882 (selfie, oferta)
// Hook cerut de Sabin: un motor care pornește greu, apoi un motor care trepidează; sunetul real al cadrelor AI e în audio/hook_bed.wav (out/v2.json „beds”).
// Promo cu programare (el spune „numărul de telefon de pe ecran”): telefonul pe video când îl spune și pe cardul de final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    a0: aw(0, 'A'), iarna: aw(0, 'iarna'), porneste: aw(0, 'pornește'), greu: aw(0, 'greu'), sau0: aw(0, 'Sau'), trep: aw(0, 'trepidații'),
    ei: aw(1, 'Ei'), de1: aw(1, 'de'), problema: aw(1, 'problema'), sistemul: aw(1, 'sistemul'), un1: aw(1, 'Un'), injector1: aw(1, 'injector'), uzat: aw(1, 'uzat'),
    pompa1: aw(1, 'pompă'), obosita: aw(1, 'obosită'),
    isi: aw(2, 'își'), sezonul: aw(2, 'sezonul'), partea: aw(2, 'Partea'), turbo2: aw(2, 'Turbo'), verif2: aw(2, 'verificarea'), repar2: aw(2, 'reparația'),
    pretul: aw(2, 'prețul'), mic: aw(2, 'mic'),
    nu3: aw(3, 'Nu'), diagnoza3: aw(3, 'diagnoză'), gratuita3: aw(3, 'gratuită'), oferim: aw(3, 'oferim'), locatie: aw(3, 'locație'), buc: aw(3, 'București'),
    iasi: aw(3, 'Iași'), galati: aw(3, 'Galați'), piatra: aw(3, 'Piatra'), cazul: aw(3, 'cazul'), demontate: aw(3, 'demontate'), verif3: aw(3, 'verificarea'),
    n75: aw(3, '75'), injectoarelor: aw(3, 'injectoarelor'), verif3b: aw(3, 'verificarea', 1), pompei: aw(3, 'pompei'), n150: aw(3, '150'), n350: aw(3, '350'),
    asa4: aw(4, 'Așa'), ajuta4: aw(4, 'ajuta'), diag4: aw(4, 'diagnosticarea'), inainte4: aw(4, 'înainte'), banii: aw(4, 'banii'),
    te5: aw(5, 'Te'), programa: aw(5, 'programa'), numarul: aw(5, 'numărul'),
  };
  const CUT1 = 148 / 30, CUT2 = 235 / 30, CATCH = 4.615;           // cadrul cu motorul care trepidează · intrarea lui Sabin · motorul „prinde”
  const CLIP = [0, CUT1, CUT2, 12.353, 21.205, 31.905];
  const T1 = .14, T2 = .56, T3 = CUT1 + .04;                        // impacturile titlurilor din hook
  const BOOM_END = A.locatie - .25;
  return {
    hook: null,
    stages: null,
    hideCap: [[0, CUT2 + .02]],
    tags: {
      0: { iarna: 'c', trepidatii: 'r' },
      1: { problema: 'r', sistemul: 'c', inalta: 'c', presiune: 'c', obosita: 'r' },
      2: { sezonul: 'c', rece: 'c', verificarea: 'g', profesionala: 'g', reparatia: 'g', mic: 'g' },
      3: { diagnoza: 'g', gratuita: 'g', bucuresti: 'y', iasi: 'y', galati: 'y', piatra: 'y', neamt: 'y', demontate: 'c', injectoarelor: 'c', pompei: 'c', lei: 'y', bucata: 'y' },
      4: { diagnosticarea: 'g', perfecta: 'g', banii: 'y', reparatii: 'y' },
      5: { programa: 'g', numarul: 'y', telefon: 'y', ecran: 'y' },
    },
    items: [
      // HOOK 1 (cadru AI, bordul și cheia): demarorul se chinuie, motorul prinde abia după „greu”
      { k: 'boom', t: T1, dur: CUT1 - .06 - T1, txt: 'PORNEȘTE', y: 335, size: 165, col: '#FFFFFF', from: 3.2, sh: 18, ca: 22, riser: false, bg: .8, glow: 'rgba(98,216,255,.55)' },
      { k: 'boom', t: T2, dur: CUT1 - .06 - T2, txt: 'GREU?', y: 592, size: 255, col: '#FFD21F', from: 3.6, sh: 26, ca: 30, riser: false, bg: 1 },
      { k: 'chip', t0: A.a0 - .05, t1: CUT1 - .1, y: 172, ph: [[A.a0 - .05, 'snowflake', 'A VENIT IARNA', 'blue']] },
      // HOOK 2 (cadru AI, motorul care trepidează)
      { k: 'boom', t: T3, dur: CUT2 - .06 - T3, txt: 'TREPIDAȚII?', y: 420, size: 190, col: '#FF4B4B', from: 3.6, sh: 30, ca: 30, riser: false, bg: 1, glow: 'rgba(255,75,75,.55)' },

      // IMG_1879 (selfie, capul aproape de cameră): cauza
      { k: 'chip', t0: A.de1 - .05, t1: A.un1 - .35, y: 236, ph: [[A.de1 - .05, 'magnifying_glass_tilted_left', 'DE CELE MAI MULTE ORI', 'yellow'], [A.sistemul - .05, 'stethoscope', 'DIAGNOSTIC: SISTEMUL DE INJECȚIE', 'blue']] },

      // IMG_1880 (pompa și injectorul pe masă, fără față): fișa pacientului
      { k: 'file', t0: CLIP[3] + .05, t1: CLIP[4] - .15, top: 168, ecg: 'crit', rows: [
        [CLIP[3] + .15, 'PACIENT', 'Motor diesel', 'c', 'automobile'],
        [CLIP[3] + .3, 'SIMPTOME', 'Pornește greu, trepidații', 'r', 'snowflake'],
        [A.injector1, 'SUSPECT 1', 'Injector uzat', 'r', 'warning'],
        [A.pompa1, 'SUSPECT 2', 'Pompă de înaltă presiune obosită', 'r', 'warning']], stamp: [A.sezonul - .03, 'SEZONUL RECE', 'red'] },

      // IMG_1881: tratamentul
      { k: 'pipe', t0: A.partea - .1, t1: CLIP[5] - .2, top: 196, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR', steps: [
        [A.verif2 - .05, 'microscope', 'VERIFICARE<br>PROFESIONALĂ'], [A.repar2 - .05, 'hammer_and_wrench', 'REPARAȚIE,<br>DUPĂ CAZ'], [A.pretul - .05, 'money_bag', 'PREȚ CÂT<br>MAI MIC']] },

      // IMG_1882 (selfie): oferta — DIAGNOZĂ ... GRATUITĂ! (boom pe fiecare cuvânt, deasupra capului)
      { k: 'boom', t: A.diagnoza3, dur: BOOM_END - A.diagnoza3, txt: 'DIAGNOZĂ', y: 224, size: 112, col: '#FFFFFF', from: 2.8, sh: 14, ca: 18, riser: false, bg: .6, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: A.gratuita3, dur: BOOM_END - A.gratuita3, txt: 'GRATUITĂ!', y: 380, size: 142, col: '#4ADE80', from: 3.6, sh: 26, ca: 28, bg: 1, glow: 'rgba(74,222,128,.6)' },
      { k: 'chip', t0: BOOM_END + .05, t1: A.buc - .5, y: 330, ph: [[BOOM_END + .05, 'round_pushpin', 'ÎN ORICE LOCAȚIE TURBO DOCTOR', 'blue']] },
      { k: 'eq', t0: A.buc - .25, t1: A.cazul - .3, top: 196, ico: 'round_pushpin', title: 'DIAGNOZĂ GRATUITĂ', sub: 'ORICE LOCAȚIE',
        lines: [[A.buc - .05, 'BUCUREȘTI · IAȘI', 'c'], [A.galati - .05, 'GALAȚI · PIATRA NEAMȚ', 'c']] },
      { k: 'chip', t0: A.cazul - .1, t1: A.verif3 - .3, y: 330, ph: [[A.cazul - .1, 'wrench', 'AI DEJA PIESELE DEMONTATE?', 'yellow']] },
      { k: 'eq', t0: A.verif3 - .1, t1: A.asa4 - .3, top: 138, ico: 'microscope', title: 'VERIFICARE PIESE DEMONTATE', sub: 'PREȚ',
        lines: [[A.injectoarelor - .05, 'INJECTOR · 75 LEI/BUC', 'big y'], [A.pompei - .05, 'POMPĂ · 150–350 LEI', 'big y']] },
      { k: 'chip', t0: A.ajuta4 - .1, t1: A.te5 - .35, y: 330, ph: [[A.ajuta4 - .1, 'stethoscope', 'DIAGNOSTICARE PERFECTĂ', 'green'], [A.inainte4 - .05, 'money_bag', 'ÎNAINTE SĂ BAGI BANII ÎN REPARAȚII', 'yellow']] },
      // programarea: telefonul, mare, exact când spune „numărul de telefon de pe ecran”
      { k: 'chip', t0: A.te5 - .05, t1: A.programa - .4, y: 330, ph: [[A.te5 - .05, 'round_pushpin', 'TE AȘTEPTĂM LA NOI!', 'green']] },
      { k: 'eq', t0: A.programa - .12, t1: SEND + .2, top: 196, ico: 'phone', title: 'PROGRAMEAZĂ-TE', sub: 'LA TELEFON',
        lines: [[A.programa + .02, '0739 065 065', 'big y']] },
      // cardul de final standard + telefonul (doar pe promo)
      { k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1160, ico: 'phone', title: 'PROGRAMEAZĂ-TE', sub: 'DIAGNOZĂ GRATUITĂ',
        lines: [[TEND + 2.7, '0739 065 065', 'big y']] },
    ],
    fx: [
      // hook 1
      { k: 'punch', t: T1, a: .1, sh: 22 }, { k: 'glitch', t: T1, d: .14 }, { k: 'shock', t: T1 + .01, x: 540, y: 335, r: 620, n: 1, col: '#FFFFFF' },
      { k: 'flash', t: T2 - .11, a: .45 }, { k: 'punch', t: T2, a: .12, sh: 28 }, { k: 'shock', t: T2 + .01, x: 540, y: 592, r: 720, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'punch', t: CATCH, a: .035, sh: 12 },
      // hook 2
      { k: 'flash', t: CUT1 - .09, a: .6 }, { k: 'glitch', t: CUT1 - .02, d: .16 }, { k: 'punch', t: T3, a: .13, sh: 30 },
      { k: 'shock', t: T3 + .01, x: 540, y: 420, r: 700, n: 2, col: '#FF4B4B', col2: '#FFFFFF' },
      // intrarea lui Sabin și schimbările de cadru
      { k: 'glitch', t: CUT2 - .03, d: .12 }, { k: 'glitch', t: CLIP[3] - .04, d: .12 }, { k: 'glitch', t: CLIP[4] - .04, d: .12 }, { k: 'glitch', t: CLIP[5] - .04, d: .12 },
      { k: 'punch', t: A.uzat, a: .04, sh: 8 }, { k: 'punch', t: A.obosita, a: .04, sh: 8 },
      // oferta
      { k: 'flash', t: A.diagnoza3 - .1, a: .35 }, { k: 'punch', t: A.diagnoza3, a: .06, sh: 12 },
      { k: 'flash', t: A.gratuita3 - .11, a: .65 }, { k: 'punch', t: A.gratuita3, a: .14, sh: 30 }, { k: 'glitch', t: A.gratuita3, d: .2 },
      { k: 'shock', t: A.gratuita3 + .01, x: 540, y: 372, r: 640, n: 2, col: '#4ADE80', col2: '#FFFFFF' },
      { k: 'punch', t: A.n75, a: .05, sh: 10 }, { k: 'punch', t: A.n150, a: .05, sh: 10 },
      { k: 'punch', t: A.programa + .02, a: .06, sh: 12 },
    ],
    sfx: [[CUT2 - .12, 'whoosh', .45], [CLIP[3] - .1, 'whoosh', .45], [CLIP[4] - .1, 'whoosh', .45], [CLIP[5] - .1, 'whoosh', .45]],
    bursts: [[T2 + .04, 540, 592, 8, 460, 1.3], [T3 + .04, 540, 420, 7, 420, 1.2], [A.gratuita3 + .04, 540, 372, 8, 460, 1.4]],
  };
};
