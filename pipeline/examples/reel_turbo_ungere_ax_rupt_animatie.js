// v2 – „Nu schimba turbina defectă până nu vezi asta”: reel animat 3D cu vocea lui Sabin (ElevenLabs), 11.11.2026
// Sursa: animația turbosuflantei (tools/anim_turbo/reel.html) randată cadru cu cadru: axul care se rupe din lipsă de ungere,
// cum funcționează turbina, cauzele (pompă slăbită, depuneri pe tur), aceeași problemă la turbina nouă, ungerea rezolvată.
// Etichetele de pe piese, blitzul și zguduitura ruperii sunt în animație; compozitorul pune hook-ul boom, bara de etape, chip-uri, subtitrări.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const L = (i, w, k) => aw(i, w, k);
  const SNAP1 = aw(0, 'asta!') + .05, SNAP2 = aw(7, 'rupe.') + .1, SNAP3 = aw(10, 'problemă.') + .05;
  const HK = aw(2, 'Turbina') - .35;            // tăietura (dip la negru) din animație
  const T1 = aw(0, 'schimba') - .03, T2 = aw(0, 'defectă') - .03, T3 = aw(1, 'strice') - .03;
  const CY = 588;
  return {
    hideCap: [[0, HK - .05]],
    items: [
      // HOOK: „NU SCHIMBA” + „TURBINA DEFECTĂ” bubuie; titlul se rupe în două exact când se rupe axul („asta!”), apoi „SE STRICĂ DIN NOU!”
      { k: 'boom', t: T1, dur: T3 - .1 - T1, txt: 'NU SCHIMBA', y: 330, size: 190, col: '#FFFFFF', from: 3.4, sh: 20, ca: 26, riser: false, bg: .75, cg: .35, glow: 'rgba(255,75,75,.55)' },
      { k: 'boom', t: T2, dur: T3 - .1 - T2, txt: 'TURBINA DEFECTĂ', y: 520, size: 128, col: '#FFD21F', from: 3.0, sh: 16, ca: 22, riser: false, bg: .55, cg: .3, cut: [SNAP1, -7, 40, 10] },
      { k: 'boom', t: T3, dur: HK - T3, txt: 'SE STRICĂ DIN NOU!', y: 430, size: 118, col: '#FF4B4B', from: 2.8, sh: 14, ca: 20, riser: false, bg: .3, cg: 0, glow: 'rgba(255,75,75,.6)' },
      // cum funcționează
      { k: 'chip', t0: L(3, '100.000') - .1, t1: ew(4, 'ulei.') + .1, y: CY, ph: [[L(3, '100.000') - .1, 'rocket', 'PESTE 100.000 RPM', 'yellow'], [L(4, 'plutește') - .05, 'droplet', 'AXUL PLUTEȘTE PE ULEI', 'yellow']] },
      { k: 'chip', t0: L(5, 'nevoie') - .05, t1: aw(6, 'Când') - .3, y: CY, ph: [[L(5, 'nevoie') - .05, 'droplet', 'PRESIUNE CORECTĂ + DEBIT SUFICIENT', 'yellow']] },
      // cauzele
      { k: 'chip', t0: L(6, 'pompă') - .05, t1: L(7, 'Se') - .2, y: CY, ph: [[L(6, 'pompă') - .05, 'warning', 'POMPĂ DE ULEI SLĂBITĂ', 'red'], [L(6, 'depuneri') - .05, 'warning', 'DEPUNERI PE TURUL TURBINEI', 'red'], [L(6, 'lagărele') - .05, 'cross_mark', 'LAGĂRE FĂRĂ ULEI', 'red']] },
      { k: 'kin', t: SNAP2, dur: .8, txt: 'RUPT!', col: '#FF3B30', y: 650, size: 230, rot: -5 },
      { k: 'stamp', t: L(8, 'distrusă.') + .02, t1: aw(9, 'Foarte') - .4, y: 640, txt: 'DISTRUSĂ', col: 'red', s: .8, rot: -7 },
      // soluția
      { k: 'chip', t0: L(9, 'elimină') - .05, t1: aw(10, 'Altfel,') - .25, y: CY, ph: [[L(9, 'elimină') - .05, 'stethoscope', 'ELIMINĂ CAUZA LIPSEI DE UNGERE', 'yellow']] },
      { k: 'kin', t: SNAP3, dur: .9, txt: 'DIN NOU!', col: '#FF3B30', y: 650, size: 200, rot: -5 },
      { k: 'chip', t0: L(11, 'Întâi') - .05, t1: SEND - .2, y: 500, ph: [[L(11, 'Întâi') - .05, 'check_mark_button', '1 · REZOLVI UNGEREA', 'green'], [L(11, 'apoi') - .05, 'wrench', '2 · ABIA APOI MONTEZI TURBINA', 'green']] },
    ],
    fx: [
      { k: 'punch', t: T1, a: .12, sh: 26 }, { k: 'glitch', t: T1, d: .16 },
      { k: 'punch', t: T2, a: .08, sh: 16 },
      { k: 'punch', t: SNAP1, a: .18, sh: 38 }, { k: 'shock', t: SNAP1 + .01, x: 540, y: 1000, r: 760, n: 2, col: '#FFD21F', col2: '#FF4B4B' }, { k: 'glitch', t: SNAP1, d: .22 },
      { k: 'punch', t: T3, a: .08, sh: 14 },
      { k: 'punch', t: SNAP2, a: .14, sh: 30 }, { k: 'shock', t: SNAP2 + .01, x: 540, y: 1000, r: 680, n: 2, col: '#FFD21F', col2: '#FF4B4B' },
      { k: 'punch', t: SNAP3, a: .12, sh: 26 }, { k: 'shock', t: SNAP3 + .01, x: 540, y: 1000, r: 620, n: 1, col: '#FF4B4B' },
    ],
    stages: [[HK + .5, 'CUM FUNCȚIONEAZĂ'], [aw(6, 'Când') - .05, 'CAUZA'], [aw(7, 'Se') - .05, 'DEFECTUL'], [aw(9, 'Foarte') - .05, 'SOLUȚIA']],
    bgFix: [[0, SEND]],
    tags: {
      0: { schimba: 'r', defecta: 'r', asta: 'y' }, 1: { strice: 'r', nou: 'r' },
      2: { gazele: 'r', evacuare: 'r', presiunea: 'c', admisie: 'c' }, 3: { '100000': 'y', rotatii: 'y' },
      4: { pluteste: 'y', film: 'y', ulei: 'y' }, 5: { presiune: 'y', corecta: 'y', debit: 'y', suficient: 'y' },
      6: { pompa: 'r', slabita: 'r', depuneri: 'r', blocheaza: 'r', turul: 'y', lagarele: 'r' },
      7: { incing: 'r', gripeaza: 'r', rupe: 'r' }, 8: { distrusa: 'r' },
      9: { important: 'y', elimina: 'g', cauza: 'y', ungere: 'y' }, 10: { aceeasi: 'r', problema: 'r' },
      11: { rezolvi: 'g', ungerea: 'g', montezi: 'g' },
    },
  };
};
