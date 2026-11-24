// v2 – Reel „Echipa Turbo Doctor la Bosch Budapesta” (curs de formare, 19.11.2026) – cerut de Sabin pe 23.11.2026
// Cerința lui: un videoclip captivant care pornește de la ideea că colegii sunt acolo, arată puțin ce fac și transmite că investim constant
// în pregătirea echipei ca să oferim cele mai bune reparații; el a cerut explicit SELECȚIA celor mai interesante cadre (nu clipurile întregi).
// Sursa (tools: /home/claude/work/scripts/build_montage.py): momente alese din fiecare clip, în ordinea filmării, tăieturile pe bătaia muzicii (104 bpm).
// Fiecare bucată are imaginea și sunetul ei. Vorbirea în română (hook, CP4/CP5, impresiile de la final) e pe pista vocii, cu subtitrări;
// sunetul real al celorlalte bucăți (instructorul, în maghiară/engleză, atelierul) e în audio/amb_bed.wav (beds), fără lanțul vocii.
//  0.00 IMG_7422 selfie în fața clădirii Bosch · 6.37 2c60881a dispozitivul de injectoare · 10.40 același, prim-plan · 13.27 IMG_7427 pompă pe stand
//  16.17 IMG_7432 „Un CP4 și un CP5. Ce diferență!” · 22.50 IMG_7433 · 25.40 IMG_7434 · 27.10 IMG_7435 (piese mici, mâini)
//  29.43 IMG_7436 postul de lucru · 35.20 IMG_7436 zâmbetul · 37.50 IMG_7437 colegul la stația de lucru, sigla pe spate
// 24.11 (feedback Sabin): fără vorbele de pe fundal în bucățile cu colegii la lucru (beds scos din out/v2.json) și fără fraza de la final
// („niște măruntaie…”: pista vocii tăcută de la 37.49, fereastra 2 scoasă din transcript_ctx/curated) -> acolo e doar muzica.
//  44.37 cadrul final aproape înghețat (out/v2.json tip) cu mesajul cerut de Sabin · 47.97 cardul de final standard.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const CUT = [0, 6.367, 10.4, 13.267, 16.167, 22.5, 25.4, 27.1, 29.433, 35.2, 37.5, 44.367];
  const A = {
    astazi: aw(0, 'Astăzi'), echipa: aw(0, 'echipa'), turbo: aw(0, 'Turbo'), curs: aw(0, 'curs'), formare: aw(0, 'formare'), bosch: aw(0, 'Bosch'), budapesta: aw(0, 'Budapesta.'),
    un1: aw(1, 'Un'), cp4: aw(1, 'CP4'), cp5: aw(1, 'CP5.'), ce: aw(1, 'Ce'), diferenta: aw(1, 'diferență!'),
  };
  // HOOK: titlu boom în patru trepte, toate în prima secundă; impactul mare („LA BOSCH!”) pe primul lui cuvânt, după el doar bubuituri mici
  const B1 = .12, B2 = A.astazi - .02, B3 = .64, B4 = .92, HB = CUT[1] - .06;
  const Y1 = 262, Y2 = 400, Y3 = 1360, Y4 = 1502;
  // mesajul de final, pe cadrul aproape înghețat cu sigla TURBO DOCTOR pe spate
  const M1 = SEND + .12, M2 = SEND + .55, M3 = SEND + 1.25, M4 = SEND + 1.7, MEND = TEND - .06;
  return {
    hook: { tag: 'DOCTORII LA SPECIALIZARE', y: -84, end: HB },
    hideCap: [[0, CUT[1]]],
    bgFix: [[CUT[10], TEND]],                       // ultimul cadru + mesajul: fără zoom, ca sigla TURBO DOCTOR să rămână întreagă în cadru
    tags: {
      0: { echipa: 'g', turbo: 'g', doctor: 'g', curs: 'y', formare: 'y', bosch: 'c', budapesta: 'c' },
      1: { cp4: 'c', cp5: 'c', diferenta: 'y' },
    },
    items: [
      // ---- hook: patru trepte
      { k: 'boom', t: B1, dur: HB - B1, txt: 'ECHIPA TURBO DOCTOR', y: Y1, size: 96, col: '#FFFFFF', from: 2.4, sh: 10, ca: 12, riser: false, bg: .45, cg: .3, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'LA BOSCH!', y: Y2, size: 158, col: '#FFD21F', from: 3.6, sh: 26, ca: 30, bg: 1 },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'CURS DE FORMARE', y: Y3, size: 116, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .32, cg: .18, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'BUDAPESTA', y: Y4, size: 128, col: '#62D8FF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .32, cg: .18, glow: 'rgba(98,216,255,.55)' },

      // ---- 1 · INJECTOARE (dispozitivul de prindere, apoi prim-planul): eticheta jos, peste banc
      { k: 'chip', t0: CUT[1] + .06, t1: CUT[3] - .08, y: 1480, ph: [[CUT[1] + .06, 'svc_injector', 'INJECTOARE COMMON RAIL', 'blue'],
        [CUT[2] + .04, 'hammer_and_wrench', 'PROCEDURA BOSCH, PAS CU PAS', 'blue']] },

      // ---- 2 · POMPE (pompa pe stand, apoi „Un CP4 și un CP5. Ce diferență!”): sus, deasupra pompei
      { k: 'chip', t0: CUT[3] + .06, t1: CUT[5] - .08, y: 300, ph: [[CUT[3] + .06, 'fuel_pump', 'POMPE DE ÎNALTĂ PRESIUNE', 'blue'],
        [CUT[3] + 1.5, 'microscope', 'TESTARE PE STANDUL BOSCH', 'blue'], [A.un1 - .08, 'fuel_pump', 'CP4 vs CP5', 'yellow']] },
      { k: 'stk', t0: A.diferenta - .04, t1: CUT[5] - .1, ico: 'eyes', x: 900, y: 560, size: 130, rot: 8 },

      // ---- 3 · PRECIZIE (trei colegi, piese mici): jos pe primele două cadre, sus pe prim-planul cu mâinile
      { k: 'chip', t0: CUT[5] + .06, t1: CUT[7] - .08, y: 1480, ph: [[CUT[5] + .06, 'microscope', 'PIESE DE PRECIZIE', 'blue'],
        [CUT[6] + .04, 'gear', 'PE APARATURA BOSCH', 'blue']] },
      { k: 'chip', t0: CUT[7] + .06, t1: CUT[8] - .08, y: 330, ph: [[CUT[7] + .06, 'magnifying_glass_tilted_left', 'TOLERANȚE DE MICRONI', 'yellow']] },

      // ---- 4 · CURĂȚENIE: ce explică instructorul (în maghiară) despre postul de lucru, pe cadrul larg; prim-planul rămâne curat
      { k: 'def', t0: CUT[8] + .08, t1: 32.55, top: 232, term: 'POST ÎN SUPRAPRESIUNE', text: 'Aerul filtrat iese din post: murdăria poate doar să iasă, nu să intre în piese.' },

      // ---- zâmbetul
      { k: 'kin', t: CUT[9] + .12, dur: CUT[10] - CUT[9] - .22, txt: 'ÎNVĂȚĂM CU PLĂCERE!', col: '#4ADE80', y: 250, size: 92, rot: -3 },

      // ---- 5 · colegul cu sigla pe spate: doar muzica, fără text (24.11)

      // ---- mesajul (cerut de Sabin), pe cadrul aproape înghețat, cu sigla la vedere dedesubt
      { k: 'boom', t: M1, dur: MEND - M1, txt: 'INVESTIM CONSTANT', y: 300, size: 112, col: '#FFFFFF', from: 2.4, sh: 10, ca: 12, riser: false, bg: .4, cg: .25, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: M2, dur: MEND - M2, txt: 'ÎN PREGĂTIREA ECHIPEI', y: 440, size: 100, col: '#FFD21F', from: 2.6, sh: 14, ca: 16, riser: false, bg: .55, cg: .3 },
      { k: 'boom', t: M3, dur: MEND - M3, txt: 'CA SĂ-ȚI OFERIM', y: 600, size: 82, col: '#FFFFFF', from: 2.2, sh: 8, ca: 10, riser: false, bg: .3, cg: .2, glow: 'rgba(98,216,255,.45)' },
      { k: 'boom', t: M4, dur: MEND - M4, txt: 'CELE MAI BUNE REPARAȚII', y: 728, size: 98, col: '#4ADE80', from: 3.0, sh: 18, ca: 20, bg: .75, glow: 'rgba(74,222,128,.6)' },
    ],
    fx: [
      // hook: patru impacturi (al doilea = cel mare, pe primul cuvânt), apoi rândurile „bat” din nou, doar vizual, când le rostește
      { k: 'flash', t: B1 - .08, a: .3 }, { k: 'punch', t: B1, a: .06, sh: 12 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: Y2, r: 760, n: 2, col: '#FFD21F' },
      { k: 'punch', t: B3, a: .05, sh: 10 }, { k: 'punch', t: B4, a: .05, sh: 10 },
      { k: 'punch', t: A.turbo, a: .04, sh: 6 }, { k: 'shock', t: A.turbo + .01, x: 540, y: Y1, r: 520, n: 1, col: '#62D8FF' },
      { k: 'punch', t: A.curs, a: .04, sh: 6 }, { k: 'shock', t: A.curs + .01, x: 540, y: Y3, r: 520, n: 1, col: '#FFFFFF' },
      { k: 'flash', t: A.bosch - .1, a: .22 }, { k: 'punch', t: A.bosch, a: .08, sh: 14 }, { k: 'shock', t: A.bosch + .01, x: 540, y: Y2, r: 600, n: 1, col: '#FFD21F' },
      { k: 'punch', t: A.budapesta, a: .05, sh: 8 }, { k: 'shock', t: A.budapesta + .01, x: 540, y: Y4, r: 520, n: 1, col: '#62D8FF' },
      { k: 'glitch', t: HB - .04, d: .14 },
      // tăieturile (pe bătaia muzicii): glitch la capitole, punch mic pe celelalte
      { k: 'glitch', t: CUT[3] - .04, d: .12 }, { k: 'glitch', t: CUT[5] - .04, d: .12 }, { k: 'glitch', t: CUT[8] - .04, d: .12 }, { k: 'glitch', t: CUT[10] - .04, d: .12 },
      { k: 'flash', t: CUT[3] - .06, a: .22 }, { k: 'flash', t: CUT[5] - .06, a: .22 }, { k: 'flash', t: CUT[8] - .06, a: .22 }, { k: 'flash', t: CUT[10] - .06, a: .22 },
      { k: 'punch', t: CUT[2], a: .04 }, { k: 'punch', t: CUT[4], a: .04 }, { k: 'punch', t: CUT[6], a: .04 }, { k: 'punch', t: CUT[7], a: .04 }, { k: 'punch', t: CUT[9], a: .05, sh: 8 },
      { k: 'punch', t: A.diferenta, a: .05, sh: 8 },
      // mesajul de final
      { k: 'flash', t: M4 - .1, a: .35 }, { k: 'shock', t: M4 + .01, x: 540, y: 728, r: 640, n: 1, col: '#4ADE80' },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [CUT[3] - .12, 'whoosh', .45], [CUT[5] - .12, 'whoosh', .45], [CUT[8] - .12, 'whoosh', .45], [CUT[10] - .12, 'whoosh', .45],
      [CUT[9] + .12, 'pop', .35], [M4 + .1, 'shimmer', .45]],
    bursts: [],
  };
};
