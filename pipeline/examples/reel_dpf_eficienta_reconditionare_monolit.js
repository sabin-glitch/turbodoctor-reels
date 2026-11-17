// v2 – Reel „Probleme de eficiență DPF? Recondiționare DPF!” (IMG_2562, un singur clip, fără tăieturi, ritm natural)
// Cerut de Sabin pe 17.11.2026: „Hook-ul să fie unul puternic, recondiționare DPF, probleme de eficiență DPF.”
// Filmare doar cu piesele (carcasa DPF recondiționată + miezul vechi scos din ea), fără față, fără plăcuțe de înmatriculare -> schemele și cardurile mari stau sus.
// Hook `boom` în patru trepte cu textul dat de el: sus „PROBLEME DE / EFICIENȚĂ DPF?”, jos „RECONDIȚIONARE / DPF!”, piesa rămâne la vedere la mijloc.
// Scheme noi: `dpfRecon` (se schimbă întregul monolit ceramic + upgrade), `coreMaterial` (cordierită vs carbură de siliciu: căldură, fisuri),
// `dpfCoating` (aftermarket „virgin”, fără rodiu / paladiu / platină -> eroare de eficiență; cele OK se apropie de prețul recondiționării).
// Fără CTA pe imagine (25.10). Fără accente roșu/verde pe tot cadrul (neconfirmate).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    daca: aw(0, 'Dacă'),
    degeaba: aw(1, 'degeaba'), ca1: aw(1, 'că'), asta: aw(1, 'Asta'), prin: aw(1, 'prin'), dupa1: aw(1, 'După'), acest1: aw(1, 'acest'), original1: aw(1, 'original'),
    ajuns: aw(1, 'ajuns'), recondit: aw(1, 'recondiționat'), cu1: aw(1, 'cu'), si1: aw(1, 'Și', 1), dupa1b: aw(1, 'După', 1), miezul: aw(1, 'miezul'), iar: aw(1, 'iar'), asa: aw(1, 'așa'),
    carbura2: aw(2, 'Carbura'), si2: aw(2, 'și'), acest2: aw(2, 'Acest'), multi: aw(2, 'mulți'), tineti: aw(2, 'Țineți'), aceasta: aw(2, 'această'), costul: aw(2, 'costul'), atentie: aw(2, 'Atenție!'),
    nu3: aw(3, 'Nu'), nici: aw(3, 'nici'), si3: aw(3, 'și'), sigur: aw(3, 'Sigur'), dar4: aw(4, 'dar'),
  };
  // HOOK: titlu boom în patru trepte cu textul cerut de Sabin. Momentele sunt începuturile de cuvânt din anvelopa vocii
  // („filtru” 1.22 · „ajunge” 1.92 · „târziu” 2.60); primul rând e pe ecran din primele cadre. Fără scântei pe titluri (cadru curat pentru copertă, 4.40 s).
  const B1 = .12, B2 = 1.22, B3 = 1.92, B4 = 2.60, HB = 4.80, Y1 = 262, Y2 = 484, Y3 = 1142, Y4 = 1400;   // între „RECONDIȚIONARE” și „DPF!” rămâne loc pentru virgula lui Ț
  // momentele-cheie citite din anvelopa vocii (vocala cuvântului)
  const SPART = 6.40, TOPIT = 6.76, CRAPAT = 7.24, RECOND = 13.62, UPG = 25.50, P3040 = 51.00, ATT = 56.62, AFT = 58.92, RH = 63.14, PD = 63.48, PT = 63.88, ERR = 65.04;
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · FILTRU DE PARTICULE', end: HB, y: -76 },
    hideCap: [[0, A.daca - .04]],   // subtitrările revin abia cu fraza următoare („Dacă filtrul…”), nu peste titlurile care se sting
    stages: [[HB + .3, 'PROBLEMA'], [A.asta - .1, 'SOLUȚIA'], [A.si1 - .1, 'UPGRADE'], [A.tineti - .1, 'COSTUL']],
    tags: {
      0: { filtru: 'c', filtrul: 'c', particule: 'c', tarziu: 'r', curatarea: '', nul: 'r', salveaza: 'r', spart: 'r', topit: 'r', crapat: 'r' },
      1: { degeaba: 'r', curatam: '', nu: 'r', mearga: 'r', masina: '', rezolva: 'g', reconditionare: 'g', filtru: 'c', particule: 'c', original: 'g', volkswagen: 'y', noi: '',
        reconditionat: 'g', complet: 'g', schimbarea: 'g', monolit: 'c', ceramic: 'c', upgrade: 'g', miezul: 'c', vechi: 'r', cordierita: 'r', nou: 'g', carbura: 'g', siliciu: 'g', vremuri: 'y' },
      2: { carbura: 'g', siliciu: 'g', topeste: 'r', mult: 'y', greu: 'g', putin: 'g', susceptibila: '', crape: 'r', cordierita: 'r', filtru: 'c', particule: 'c', montat: 'g', masina: '',
        multi: 'y', kilometri: 'y', fara: 'g', probleme: 'g', reparatie: 'g', doar: 'y', costul: 'y', original: 'y', atentie: 'r' },
      3: { aftermarket: 'y', virgine: 'r', nu: '', incarcatura: 'c', rodiu: 'c', paladiu: 'c', platina: 'c', eroare: 'r', eficienta: 'r', majoritatea: 'r' },
      4: { filtre: 'c', aftermarket: 'y', ok: 'g', pretul: 'y', reconditionarii: 'g' },
    },
    items: [
      // ---- hook: boom în patru trepte (sus întrebarea, jos răspunsul)
      { k: 'boom', t: B1, dur: HB - B1, txt: 'PROBLEME DE', y: Y1, size: 136, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .55, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'EFICIENȚĂ DPF?', y: Y2, size: 168, col: '#FF3B30', from: 3.8, sh: 26, ca: 30, bg: 1, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'RECONDIȚIONARE', y: Y3, size: 152, col: '#4ADE80', from: 3.0, sh: 16, ca: 20, riser: false, bg: .8, glow: 'rgba(74,222,128,.55)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'DPF!', y: Y4, size: 250, col: '#FFD21F', from: 3.6, sh: 22, ca: 26, riser: false, bg: .95 },
      // ---- problema: spart, topit sau crăpat -> degeaba îl curățăm
      { k: 'chip', t0: A.daca + .1, t1: A.degeaba - .25, y: 330, ph: [[A.daca + .1, 'warning', 'CURĂȚAREA NU-L MAI SALVEAZĂ', 'red']] },
      { k: 'kin', t: SPART, dur: TOPIT - SPART - .02, txt: 'SPART', col: '#FF3B30', y: 1090, size: 250, rot: -4 },
      { k: 'kin', t: TOPIT, dur: CRAPAT - TOPIT - .02, txt: 'TOPIT', col: '#FF8A3D', y: 1090, size: 250, rot: 3 },
      { k: 'kin', t: CRAPAT, dur: 1.0, txt: 'CRĂPAT', col: '#FF3B30', y: 1090, size: 250, rot: -4 },
      { k: 'scan', t0: 6.98, t1: 7.92, track: 'track_crack', box: [0, 0, 470, 340], lab: 'SCANARE MIEZ...', lab2: 'DEFECT DETECTAT', at2: CRAPAT + .02 },
      { k: 'chip', t0: A.degeaba - .03, t1: A.asta - .25, y: 330, ph: [[A.degeaba - .03, 'cross_mark', 'DEGEABA ÎL CURĂȚĂM', 'red'], [A.ca1 - .02, 'automobile', 'NU O SĂ MEARGĂ CUM TREBUIE PE MAȘINĂ', 'red']] },
      // ---- soluția: recondiționare
      { k: 'chip', t0: A.asta - .03, t1: RECOND - .12, y: 330, ph: [[A.asta - .03, 'hammer_and_wrench', 'ASTA SE REZOLVĂ PRIN...', 'blue']] },
      { k: 'kin', t: RECOND, dur: 1.5, txt: 'RECONDIȚIONARE', col: '#4ADE80', y: 1090, size: 132, rot: -4 },
      // ---- fișa pacientului
      { k: 'file', t0: A.acest1 - .15, t1: A.cu1 - .3, top: 268, no: '2562', ecg: 'ok',
        rows: [[A.acest1 - .05, 'PACIENT', '<span style="font-size:30px;white-space:nowrap">FILTRU DE PARTICULE</span>', 'c', 'svc_dpf'],
          [A.original1 - .03, 'PROVENIENȚĂ', '<span style="font-size:28px;white-space:nowrap">ORIGINAL · VOLKSWAGEN</span>', 'y', 'automobile'],
          [A.ajuns - .08, 'INTERNAT LA', 'TURBO DOCTOR', 'y', 'stethoscope'],
          [A.recondit - .03, 'TRATAMENT', '<span style="font-size:26px;white-space:nowrap">RECONDIȚIONAT COMPLET</span>', 'g', 'hammer_and_wrench']] },
      // ---- se schimbă întregul monolit ceramic + upgrade
      { k: 'schem', t0: A.cu1 - .12, t1: A.dupa1b - .3, top: 268, h: 360, type: 'dpfRecon', title: 'SCHEMĂ · RECONDIȚIONARE DPF', sub: 'MONOLIT CERAMIC',
        P: { open: A.cu1 - .05, out: A.cu1 + .25, in: 22.05, close: 22.78, weld: 23.0, up: UPG - .02 },
        stepNames: ['REPARAȚIA', 'UPGRADE'],
        steps: [[A.cu1 - .12, 'Se schimbă întregul monolit ceramic', '', 'swap'], [A.si1 - .03, 'Și pe lângă asta a primit și un upgrade', 'g', 'upgrade']],
        sfx: [[A.cu1 + .3, 'whoosh', .4], [22.08, 'whoosh', .4], [22.75, 'lock', .5], [UPG - .02, 'ding', .5]] },
      { k: 'kin', t: UPG, dur: 1.2, txt: 'UPGRADE!', col: '#4ADE80', y: 1090, size: 230, rot: -4 },
      // ---- miezul vechi (cordierită) vs miezul nou (carbură de siliciu)
      { k: 'schem', t0: A.miezul - .15, t1: A.acest2 - .3, top: 268, h: 360, type: 'coreMaterial', title: 'SCHEMĂ · MATERIALUL MIEZULUI', sub: 'VECHI VS NOU',
        P: { melt: 35.9, crack: 40.55 },
        stepNames: ['MIEZ VECHI', 'MIEZ NOU', 'CA PE VREMURI', 'CĂLDURĂ', 'FISURI'],
        steps: [[A.miezul - .15, 'Miezul vechi este din cordierită', 'y', 'old'], [A.iar - .05, 'Miezul nou este din carbură de siliciu', 'g', 'new'],
          [A.asa - .03, 'Așa cum se făcea pe vremuri', 'y', 'retro'], [A.carbura2 - .05, 'Se topește mult, mult mai greu', 'g', 'melt'],
          [A.si2 + .1, 'Mult mai puțin susceptibilă să se crape', 'g', 'crack']],
        sfx: [[A.iar + .25, 'ding', .45], [A.carbura2 + 1.0, 'impact', .45], [A.si2 + .4, 'crack', .4]] },
      // ---- urmează montajul: mulți kilometri fără probleme
      { k: 'ecg', t0: A.acest2 - .05, t1: A.tineti - .35, top: 268, label: 'PULS FILTRU', ico: 'stethoscope', states: [[A.acest2 - .05, 'ok', 'URMEAZĂ MONTAJUL'], [A.multi - .05, 'ok', 'MULȚI KM FĂRĂ PROBLEME']] },
      // ---- costul: 30–40% din costul schimbării unui filtru original
      { k: 'chip', t0: A.tineti - .03, t1: P3040 - .75, y: 330, ph: [[A.tineti - .03, 'exclamation', 'ȚINEȚI MINTE!', 'yellow']] },
      { k: 'bars', t0: P3040 - .45, t1: ATT - .25, top: 268, ico: 'euro_banknote', title: 'CÂT COSTĂ REPARAȚIA', sub: 'FAȚĂ DE UN FILTRU ORIGINAL',
        bars: [[P3040 - .02, 'RECONDIȚIONARE', .35, 'g', '30–40%'], [A.costul - .55, 'SCHIMBAREA CU UN FILTRU ORIGINAL', 1, 'r', '100%']] },
      { k: 'kin', t: P3040, dur: 1.6, txt: '30–40%', col: '#FFD21F', y: 1090, size: 250, rot: -4 },
      // ---- atenție: aftermarket
      { k: 'stamp', t: ATT, t1: A.nu3 - .1, y: 470, txt: 'ATENȚIE!', col: 'red', s: 1.05, rot: -7 },
      { k: 'chip', t0: A.nu3 - .03, t1: AFT - .2, y: 330, ph: [[A.nu3 - .03, 'warning', 'NU VORBIM DE CELE AFTERMARKET', 'yellow']] },
      { k: 'schem', t0: AFT, t1: SEND - .2, top: 268, h: 360, type: 'dpfCoating', title: 'SCHEMĂ · FILTRE AFTERMARKET', sub: 'METALE PREȚIOASE',
        P: { rh: RH, pd: PD, pt: PT },
        stepNames: ['AFTERMARKET', 'CE LIPSEȘTE', 'EFECTUL', 'EXCEPȚIA', 'PREȚUL'],
        steps: [[AFT, 'Cele aftermarket: unele sunt virgine', 'y', 'virgin'], [A.nici - .03, 'Nu au rodiu, paladiu, platină', 'r', 'metals'],
          [A.si3 - .03, 'O să aveți eroare de eficiență', 'r', 'error'], [A.sigur - .03, 'Există și filtre aftermarket OK', 'g', 'ok'],
          [A.dar4 - .03, 'Dar se apropie de prețul recondiționării', 'y', 'price']],
        sfx: [[RH, 'stamp', .5], [PD, 'stamp', .5], [PT, 'stamp', .5], [A.sigur + .4, 'ding', .45]] },
      { k: 'kin', t: ERR, dur: 1.7, txt: 'EROARE DE EFICIENȚĂ', col: '#FF3B30', y: 1090, size: 104, rot: -4 },
      // ---- Rețeta (trei sfaturi luate din ce spune el)
      { k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 470, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · DPF', ico: 'stethoscope',
        rows: [[SEND + .35, 'warning', 'Filtru spart, topit sau crăpat? Curățarea nu-l mai salvează'],
          [SEND + 1.45, 'hammer_and_wrench', 'Recondiționarea costă doar 30–40% din costul unui filtru original'],
          [SEND + 2.55, 'magnifying_glass_tilted_left', 'Atenție la aftermarket: fără rodiu, paladiu, platină ai eroare de eficiență']] },
    ],
    fx: [
      // hook: patru impacturi (al doilea = cel mare)
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: Y2, r: 760, n: 2, col: '#FF4B4B' },
      { k: 'flash', t: B3 - .11, a: .4 }, { k: 'punch', t: B3, a: .09, sh: 16 },
      { k: 'flash', t: B4 - .11, a: .5 }, { k: 'punch', t: B4, a: .11, sh: 20 }, { k: 'shock', t: B4 + .01, x: 540, y: Y4, r: 560, n: 1, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'punch', t: SPART, a: .08, sh: 16 }, { k: 'punch', t: TOPIT, a: .08, sh: 16 }, { k: 'flash', t: CRAPAT - .11, a: .3 }, { k: 'punch', t: CRAPAT, a: .1, sh: 20 },
      { k: 'glitch', t: A.asta - .15, d: .12 }, { k: 'flash', t: RECOND - .11, a: .3 }, { k: 'punch', t: RECOND, a: .08, sh: 14 },
      { k: 'glitch', t: A.acest1 - .25, d: .12 }, { k: 'glitch', t: A.cu1 - .2, d: .12 }, { k: 'punch', t: UPG, a: .08, sh: 14 },
      { k: 'glitch', t: A.miezul - .25, d: .12 }, { k: 'punch', t: A.carbura2 + 1.05, a: .05 }, { k: 'punch', t: A.si2 + .45, a: .05 },
      { k: 'glitch', t: A.acest2 - .15, d: .12 }, { k: 'glitch', t: A.tineti - .12, d: .12 },
      { k: 'flash', t: P3040 - .11, a: .4 }, { k: 'punch', t: P3040, a: .1, sh: 20 },
      { k: 'flash', t: ATT - .11, a: .4 }, { k: 'punch', t: ATT, a: .09, sh: 18 },
      { k: 'glitch', t: AFT - .1, d: .12 }, { k: 'punch', t: RH, a: .04 }, { k: 'punch', t: PD, a: .04 }, { k: 'punch', t: PT, a: .05 },
      { k: 'flash', t: ERR - .11, a: .35 }, { k: 'punch', t: ERR, a: .1, sh: 20 }, { k: 'glitch', t: A.sigur - .12, d: .12 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.multi, 'shimmer', .45]],
    bursts: [[CRAPAT + .02, 540, 1100, 6, 300, .9], [RECOND + .05, 540, 1100, 6, 340, .9], [UPG + .05, 540, 1100, 6, 300, .9], [P3040 + .05, 540, 1100, 6, 320, 1.0]],
  };
};
