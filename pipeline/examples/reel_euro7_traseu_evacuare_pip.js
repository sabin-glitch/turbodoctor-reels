// v2 – Reel r_euro7 – „Euro 7 este aici: ce ne așteaptă pe evacuare” (3 clipuri în ordinea filmării, fără tăieturi)
// clipuri: 0 IMG_9820 · 26.03 IMG_9821 · 145.46 IMG_9822 · cameră spate + PiP cu fața în dreapta sus (x 690–1050, y 25–510):
// nimic în zona PiP, fără bara de etape; grafica stă de la y ≈ 520 în jos. Fără CTA pe imagine (regula din 25.10).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    aici0: aw(0, 'aici:'), n4: aw(0, '4'), n2: aw(0, '2'), dpf0: aw(0, 'DPF,'), doc0: aw(0, 'DOC,'),
    doua: aw(1, 'două'), incalz1: aw(1, 'încălzitor'), n4b: aw(1, '4'), probabil1: aw(1, 'probabil'),
    diesel: aw(2, 'diesel'),
    aici3: aw(3, 'Aici'), dar3: aw(3, 'dar'), hai: aw(3, 'Hai'), in3: aw(3, 'În'),
    totul: aw(4, 'totul'), va4: aw(4, 'Va', 1), avem5: aw(5, 'Avem'), primul6: aw(6, 'primul'), dupa7: aw(7, 'După'),
    dupa8: aw(8, 'După'), acest8: aw(8, 'Acest'), avem8: aw(8, 'Avem', 2),
    probabil9: aw(9, 'probabil'), si9: aw(9, 'și', 1), cam9: aw(9, 'Cam'), voi: aw(9, 'Voi'),
    o10: aw(10, 'O'), mai11: aw(11, 'Mai'), tocmai: aw(11, 'Tocmai'), cu11: aw(11, 'cu'), exact: aw(11, 'Exact'), pentru11: aw(11, 'pentru'),
    nu11: aw(11, 'nu'), ci11: aw(11, 'ci'), probleme11: aw(11, 'probleme'),
    si12: aw(12, 'și'), indisp: aw(12, 'indisponibilizată'), comentariu: aw(13, 'comentariu'),
  };
  const CLIP = [0, 26.03, 145.46];
  return {
    // hook: titlul sub PiP (y +330), apoi inventarul Euro 7 care se umple pe ce enumeră el
    hook: { tag: 'ANALIZĂ TEHNICĂ · EURO 7', y: 330, l1: 'EURO 7 ESTE AICI!', l1At: .1, l2: 'IATĂ CE NE AȘTEAPTĂ', l2At: A.aici0 - .04, l2Col: '#FFD21F',
      stk1: 'face_screaming_in_fear', end: A.n4 - .1 },
    hideCap: [[0, A.n4 - .12]],
    items: [
      { k: 'eq', t0: A.n4 - .08, t1: A.aici3 - .3, top: 540, ico: 'counter', title: 'EURO 7 · EVACUAREA DIESEL', sub: 'CE CONȚINE',
        lines: [[A.n4, '4 × MONOLITURI CERAMICE', 'w'], [A.n2, '2 × SCR', 'c'], [A.dpf0 - .3, '1 × DPF', 'c'], [A.doc0 - .3, '1 × DOC', 'c'],
          [A.doua, '2 × INJECTOARE ADBLUE', 'c'], [A.incalz1, '1 × ÎNCĂLZITOR ELECTRIC', 'y'], [A.n4b, '4 × SENZORI NOx', 'r'], [A.probabil1, '2-3 × SENZORI TEMPERATURĂ', 'r']] },
      { k: 'chip', t0: A.aici3 - .05, t1: A.in3 - .3, y: 590, ph: [[A.aici3 - .05, 'gear', 'PROIECTAT PENTRU CAMIOANE', 'blue'], [A.dar3 - .05, 'automobile', 'ȘI LA DIESELURILE MICI: LA FEL', 'yellow'],
        [A.hai - .05, 'magnifying_glass_tilted_left', 'TRASEUL GAZELOR: TURBINĂ → TOBĂ', 'blue']] },
      // schema traseului, sincronizată pe piesa la care ajunge
      { k: 'schem', t0: A.in3 - .05, t1: A.voi - .3, top: 520, h: 260, type: 'euro7Line', title: 'SCHEMĂ · EVACUAREA EURO 7', sub: 'TRASEUL GAZELOR',
        stepNames: ['TRASEU', 'ÎNCĂLZITOR', 'ÎNCĂLZITOR', 'ADBLUE 1', 'SCR 1', 'DOC', 'DPF', 'DPF', 'ADBLUE 2', 'OXIGEN', 'SCR 2', 'EURO 7'],
        steps: [[A.in3 - .05, 'De la turbină până la toba finală', '', 0], [A.totul - .05, 'Totul trece printr-un încălzitor electric suplimentar', 'y', 1],
          [A.va4 - .05, 'Ca mașina să fie în standardele de poluare de la prima pornire', 'y', 1],
          [A.avem5 - .05, 'Primul injector de AdBlue și primul senzor NOx', '', 2], [A.primul6 - .05, 'Senzor de temperatură + primul SCR: reducerea NOx', 'g', 3],
          [A.dupa7 - .05, 'Gazele ajung în DOC', '', 4], [A.dupa8 - .05, 'Încă un senzor de temperatură și DPF-ul', '', 5],
          [A.acest8 - .05, 'De aici, totul seamănă cu un Euro 6 standard', '', 5],
          [A.avem8 - .05, 'Încă un injector de AdBlue, un senzor NOx și unul de temperatură', 'y', 6], [A.probabil9 - .05, 'Probabil și un senzor de oxigen', '', 7],
          [A.si9 - .05, 'Ultimul SCR + temperatură, NOx și probabil o sondă de oxigen', 'g', 8], [A.cam9 - .05, 'Cam așa arată sistemul', 'y', 9]] },
      // întrebarea și concluzia
      { k: 'chip', t0: A.voi - .05, t1: A.tocmai - .3, y: 590, ph: [[A.voi - .05, 'thinking_face', 'VOI CE PĂRERI AVEȚI?', 'yellow'], [A.o10 - .05, 'warning', 'O SĂ EXISTE PROBLEME CU EL?', 'red']] },
      { k: 'stamp', t: A.mai11 - .04, t1: A.tocmai + .6, y: 820, txt: 'MAI MULT CA SIGUR!', col: 'red', s: .85, rot: -7 },
      { k: 'chip', t0: A.tocmai - .05, t1: A.exact - .3, y: 590, ph: [[A.tocmai - .05, 'hammer_and_wrench', 'PRODUCĂTORII: SISTEM SERVISABIL', 'blue'], [A.cu11 - .05, 'calendar', 'CU INTERVALE DE SERVICE', 'blue']] },
      { k: 'chip', t0: A.exact - .05, t1: A.nu11 - .6, y: 590, ph: [[A.exact - .05, 'stethoscope', 'EXACT CE VĂ SPUNEAM ȘI NOI', 'green'], [A.pentru11 - .05, 'gear', 'TRATAREA GAZELOR: ÎN FUNCȚIUNE CORECT', 'blue']] },
      { k: 'cmp', t0: A.nu11 - .35, t1: A.probleme11 - .5, top: 540, ico: 'stethoscope', title: 'SISTEMUL DE TRATARE A GAZELOR', dimA: true,
        a: [A.nu11, 'wrench', 'NU DOAR', 'REPARAT CÂND SE STRICĂ'], b: [A.ci11, 'check_mark_button', 'CI', 'SERVISAT DIN TIMP'] },
      { k: 'list', t0: A.probleme11 - .2, t1: CLIP[2] - .2, top: 540, ico: 'shield', title: 'AȘA TE ASIGURI CĂ', rows: [[A.probleme11, 'NU AI PROBLEME SERIOASE'], [A.indisp, 'MAȘINA NU STĂ MULT ÎN SERVICE']] },
      // ultimul clip: doar întrebarea lui, fără elemente de tip CTA
      { k: 'chip', t0: A.comentariu - .05, t1: SEND - .2, y: 590, ph: [[A.comentariu - .05, 'speech_balloon', 'CÂT DE DES VA AJUNGE ÎN SERVICE?', 'yellow']] },
    ],
    fx: [
      { k: 'punch', t: A.aici0, a: .05 }, { k: 'punch', t: A.n4, a: .04 }, { k: 'glitch', t: A.aici3 - .1, d: .12 }, { k: 'glitch', t: A.in3 - .1, d: .12 },
      { k: 'punch', t: A.mai11, a: .05 }, { k: 'punch', t: A.ci11, a: .04 },
    ],
    sfx: [],
    bursts: [],
  };
};
