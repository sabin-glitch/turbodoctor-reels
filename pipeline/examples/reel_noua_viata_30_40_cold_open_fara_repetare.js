// v2 – „O nouă viață la doar 30–40% din costul unei turbine noi” (17.11.2026) – turbină recondiționată capital, cu ansamblu central nou-nouț
// clipuri (în reel): 0 finalul lui IMG_2564 (hook) · 7.167 IMG_2563 întreg · 26.700 IMG_2564 până la fraza mutată
// Cerut de Sabin: reel captivant cu hook-ul „O nouă viață la doar 30–40% din costul unei turbine noi”, apoi ce spune el despre recondiționare.
// Fraza e ultima din IMG_2564, așa că e pusă la început ca hook, cu imaginea și vocea ei (cold open făcut direct în sursă: tools/cold_open/build_src_noua_viata.py);
// restul rulează în ordinea filmată, fără tăieturi, iar fraza nu se mai repetă la final. Filmare doar cu piesele (fără față, fără plăcuțe).
// Pe hârtia de lângă geometria veche (fișa clientului) semnătura și scrisul de mână sunt estompate în sursă.
// Fără CTA pe imagine (25.10). Fără accente roșu/verde pe tot cadrul (neconfirmate).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    recond: aw(1, 'recondiționată'), capital: aw(1, 'capital,'), cu: aw(1, 'cu'), ansamblu: aw(1, 'ansamblu'), nou: aw(1, 'nou-nouț.'),
    va: aw(2, 'Va'), garantie: aw(2, 'garanție'), n24: aw(2, '24'), dar: aw(2, 'dar'), verif: aw(2, 'verificările'), reglajul: aw(2, 'reglajul'), bancul: aw(2, 'bancul'), variabileE: ew(2, 'variabile.'),
    ansamblul: aw(3, 'ansamblul'), joc: aw(3, 'joc'), considerabil: aw(3, 'considerabil.'),
    geometria: aw(4, 'Geometria'), si4: aw(4, 'și'), lovita: aw(4, 'lovită.'),
  };
  const CLIP = [0, 7.167, 26.700];
  // HOOK – momentele sunt luate din sunet (anvelopa vocii): „O” .12 · „viață” .60 · „la” 2.06 · „doar” 2.30 · „treizeci” 2.56 · „patruzeci” 3.02 · „la sută” 3.50 · „din” 4.02 · „costul” 4.22 · „unei” 4.72 · „turbine” 5.48 · „noi” 6.24 (sfârșit 6.45)
  // cinci rânduri: sus „O NOUĂ VIAȚĂ” / „LA DOAR” / „30–40%” (impactul mare), jos „DIN COSTUL UNEI” / „TURBINE NOI”; turbina rămâne la vedere la mijloc
  const B1 = .08, B2 = 2.03, B3 = 2.53, B4 = 3.99, B5 = 5.45, HEND = 7.12, Y1 = 290, Y2 = 428, Y3 = 606, Y4 = 1172, Y5 = 1378;
  const STG = A.variabileE + .2;   // ștampila „GARANȚIE 24 LUNI”, după ce se bifează lista
  const BACK = 37.72;              // camera ajunge înapoi pe turbina recondiționată (după panoramarea de la geometria veche)
  return {
    hook: { tag: 'TURBO DOCTOR · RECONDIȚIONARE CAPITALĂ', end: HEND, y: -76 },
    hideCap: [[0, CLIP[1] + .45]],   // și ultimul rând de subtitrări al hook-ului („turbine noi”), care altfel ar rămâne 0,3 s peste primul cadru al poveștii
    stages: [[CLIP[1] + .45, 'PACIENTUL'], [A.va - .12, 'GARANȚIA'], [A.dar - .1, 'CONTROL FINAL'], [CLIP[2] + .08, 'ÎNAINTE']],
    tags: {
      0: { viata: 'g', 3040: 'y', costul: 'y' },
      1: { capital: 'g', ansamblu: 'c', central: 'c', nounout: 'g' },
      2: { noi: '', luni: 'y', verificarile: 'g', calitate: 'g', reglajul: 'g', profesional: 'g', bancul: 'c', geometrii: 'c', variabile: 'c' },
      3: { ansamblul: 'c', central: 'c', vechi: 'r', considerabil: 'r' },
      4: { variabila: 'c' },
    },
    items: [
      // ---- HOOK (finalul lui IMG_2564: turbina recondiționată, vocea lui din spatele camerei): titlul bubuie pe cuvintele lui
      { k: 'boom', t: B1, dur: HEND - B1, txt: 'O NOUĂ <span style="color:#4ADE80">VIAȚĂ</span>', y: Y1, size: 148, col: '#FFFFFF', from: 2.8, sh: 14, ca: 16, riser: false, bg: .7, glow: 'rgba(74,222,128,.5)' },
      { k: 'boom', t: B2, dur: HEND - B2, txt: 'LA DOAR', y: Y2, size: 96, col: '#FFFFFF', from: 2.2, sh: 8, ca: 10, riser: false, bg: .35, cg: .25, glow: 'rgba(98,216,255,.45)' },
      { k: 'boom', t: B3, dur: HEND - B3, txt: '30–40%', y: Y3, size: 272, col: '#FFD21F', from: 3.8, sh: 28, ca: 32, bg: 1 },
      { k: 'boom', t: B4, dur: HEND - B4, txt: 'DIN COSTUL UNEI', y: Y4, size: 112, col: '#FFFFFF', from: 2.2, sh: 9, ca: 12, riser: false, bg: .4, cg: .3, glow: 'rgba(98,216,255,.45)' },
      { k: 'boom', t: B5, dur: HEND - B5, txt: 'TURBINE NOI', x: 524, y: Y5, size: 198, col: '#FFFFFF', from: 3.2, sh: 20, ca: 24, riser: false, bg: .85, glow: 'rgba(98,216,255,.55)' },

      // ---- IMG_2563: „Turbină recondiționată capital, cu ansamblu central nou-nouț.”
      { k: 'file', t0: CLIP[1] + .28, t1: A.cu - .32, top: 268, ecg: 'ok',
        rows: [[CLIP[1] + .55, 'PACIENT', 'TURBINĂ', 'c', 'svc_turbo'], [A.recond - .02, 'TRATAMENT', 'RECONDIȚIONARE CAPITALĂ', 'g', 'hammer_and_wrench']] },
      { k: 'def', t0: A.cu - .1, t1: A.va - .35, top: 262, term: 'ANSAMBLU CENTRAL', text: 'Miezul turbinei: axul cu cele două rotoare și lagărele lui.' },
      { k: 'stamp', t: A.nou + .02, t1: A.va - .4, y: 770, txt: 'NOU-NOUȚ', col: 'green', s: .9, rot: -7 },
      // ---- „Va pleca de la noi cu o garanție de 24 de luni…”
      { k: 'kin', t: A.n24 - .03, dur: 1.1, txt: '24 LUNI GARANȚIE', col: '#FFD21F', y: 600, size: 124, rot: -3 },
      { k: 'stk', ico: 'shield', t0: A.n24 + .05, t1: A.dar - .2, x: 150, y: 452, size: 132, rot: -12 },
      // ---- „…dar doar după verificările finale de calitate și reglajul profesional pe bancul de calibrare geometrii variabile.”
      { k: 'list', t0: A.dar - .08, t1: A.variabileE - .08, top: 268, ico: 'microscope', title: 'ÎNAINTE DE EXTERNARE',
        rows: [[A.verif, 'VERIFICĂRI FINALE DE CALITATE'], [A.reglajul, 'REGLAJ PROFESIONAL'], [A.bancul, '<span style="font-size:26px">BANC DE CALIBRARE · GEOMETRIE VARIABILĂ</span>']] },
      { k: 'stamp', t: STG, t1: CLIP[2] - .42, y: 600, txt: 'GARANȚIE 24 LUNI', col: 'green', s: .8, rot: -6 },

      // ---- IMG_2564: „Cam așa arăta și ansamblul central vechi: un joc destul de considerabil.”
      { k: 'scan', t0: A.ansamblul - .1, t1: A.considerabil + .42, box: [170, 600, 740, 640], lab: 'ANSAMBLU CENTRAL VECHI...', lab2: 'JOC CONSIDERABIL', at2: A.joc - .03 },
      // ---- „Geometria variabilă, și ea lovită.”
      { k: 'call', t0: A.geometria - .14, t1: A.si4 - .1, track: 'track_ring', p: [504, 950], lab: [440, 470], h: 'PIESA VECHE', v: 'GEOMETRIA VARIABILĂ', col: 'red', cps: 70 },   // eticheta stă mereu în stânga punctului urmărit (peste hârtie), ca să nu sară dintr-o parte în alta
      { k: 'stamp', t: A.lovita - .02, t1: A.lovita + 1.0, y: 620, txt: 'LOVITĂ', col: 'red', s: 1.0, rot: -8 },

      // ---- finalul: camera se întoarce la turbina recondiționată -> titlul hook-ului revine („O NOUĂ VIAȚĂ”) deasupra Rețetei (ce spune el, pe scurt); fraza nu se mai aude a doua oară
      { k: 'kin', t: BACK, dur: TEND - .2 - BACK, txt: '<span style="color:#fff">O NOUĂ</span> VIAȚĂ', col: '#4ADE80', y: 392, size: 150, rot: -3 },
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 520, title: 'REȚETA TURBO DOCTOR', sub: 'RECONDIȚIONARE CAPITALĂ · TURBINĂ', ico: 'stethoscope',
        rows: [[SEND + .35, 'gear', 'Ansamblu central nou-nouț'], [SEND + 1.0, 'microscope', 'Verificări finale + reglaj pe bancul de calibrare'],
          [SEND + 1.65, 'shield', 'Garanție 24 de luni'], [SEND + 2.3, 'money_bag', 'La doar <span style="color:#15803D">30–40%</span> din costul unei turbine noi']] },
    ],
    fx: [
      // hook
      { k: 'flash', t: B1 - .06, a: .4 }, { k: 'punch', t: B1, a: .09, sh: 16 }, { k: 'glitch', t: B1, d: .1 },
      { k: 'punch', t: B2, a: .05, sh: 10 },
      { k: 'flash', t: B3 - .11, a: .75 }, { k: 'punch', t: B3, a: .16, sh: 34 }, { k: 'glitch', t: B3, d: .18 }, { k: 'shock', t: B3 + .01, x: 540, y: Y3, r: 780, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'punch', t: B4, a: .05, sh: 10 },
      { k: 'flash', t: B5 - .11, a: .5 }, { k: 'punch', t: B5, a: .11, sh: 22 }, { k: 'shock', t: B5 + .01, x: 524, y: Y5, r: 620, n: 1, col: '#FFFFFF' },
      { k: 'glitch', t: HEND - .03, d: .14 }, { k: 'flash', t: CLIP[1] - .09, a: .45 },
      // IMG_2563
      { k: 'punch', t: A.recond, a: .04 }, { k: 'flash', t: A.nou - .08, a: .25 }, { k: 'punch', t: A.nou + .02, a: .07, sh: 12 },
      { k: 'flash', t: A.n24 - .13, a: .35 }, { k: 'punch', t: A.n24 - .03, a: .09, sh: 16 },
      { k: 'punch', t: STG, a: .06, sh: 10 },
      // IMG_2564
      { k: 'glitch', t: CLIP[2] - .05, d: .14 }, { k: 'flash', t: CLIP[2] - .07, a: .3 },
      { k: 'punch', t: A.joc, a: .08, sh: 16 },
      { k: 'flash', t: A.lovita - .12, a: .3 }, { k: 'punch', t: A.lovita - .02, a: .09, sh: 18 },
      { k: 'flash', t: BACK - .1, a: .35 }, { k: 'punch', t: BACK, a: .08, sh: 14 },
    ],
    sfx: [[HEND - .1, 'whoosh', .7], [CLIP[2] - .1, 'whoosh', .55], [BACK - .75, 'whoosh', .6], [A.nou + .06, 'shimmer', .5], [STG + .05, 'shimmer', .5]],
    bursts: [[A.nou + .06, 540, 770, 6, 330, .9], [A.n24 + .06, 540, 600, 6, 400, 1.0], [STG + .06, 540, 600, 6, 360, .9]],
  };
};
