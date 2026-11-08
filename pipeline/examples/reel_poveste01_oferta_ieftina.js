// v2 – Poveste AI #01 „POV: cea mai ieftină ofertă” (stil Workerr, refăcută 07.11.2026 cu buze sincronizate)
// Cadre: A duba + Clientul la telefon (minimax + Sync 3) · B Mecanicul peste umăr (Kling 4 + Sync 3) · C/E/F/H Doctorul · D/G/I Clientul
// (Kling 4 cu un singur vorbitor pe cadru + Sync 3 pe replica exactă ElevenLabs) · Z semnătura și plecarea (fără dialog).
// Fețele sunt în prim-plan: chip-urile și textul cinetic stau jos (y ≈ 1190, deasupra subtitrărilor), ștampilele pe piept, banda sus.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    gata: aw(0, 'Gata,'), tiam: aw(0, 'Ți-am'), lei800: aw(0, '800'), brici: aw(0, 'brici.'), ce0: aw(0, 'Ce'), lei1200: aw(0, '1.200'),
    deci: aw(1, 'Deci'), treia1: aw(1, 'treia'), am: aw(1, 'Am'), chilipir: aw(1, 'chilipir.'),
    ax: aw(2, 'Ax'), joc: aw(2, 'joc,'), cauza: aw(2, 'cauza'), opt: aw(2, '800'), suma: aw(2, '2.400.'),
    o3: aw(3, 'O'), corect: aw(3, 'corect'), odata: aw(3, 'o'), ieftin3: aw(3, '„Ieftin”'), dublu: aw(3, 'dublu.'), merge: aw(3, 'merge.'), merge_e: ew(3, 'merge.'),
    da: aw(4, 'Da,'), sarac: aw(4, 'sărac'), ieftine_e: ew(4, 'ieftine.'), exact: aw(4, 'Exact.'), carte: aw(4, 'carte,'),
    fao: aw(5, 'Fă-o'), stresul: aw(5, 'stresul'), asta_e: ew(5, 'ăsta.'),
  };
  // începutul fiecărui cadru în sursă (build_pov01_v2.py)
  const SH = { A: 0, B: 8.8, C: 18.59, D: 24.01, E: 26.89, F: 34.70, G: 43.61, H: 48.27, I: 51.89, Z: 55.50 };
  const HEND = 4.3, CHD = 1.45, CY = 1190;  // CY = rândul de chip-uri, deasupra subtitrărilor
  const items = [], fx = [];

  // ---- capitolele poveștii, pe cadrul înghețat de la finalul replicii precedente
  [[8.0, 'CU 3 SĂPTĂMÂNI ÎN URMĂ', 'LA „CELĂLALT SERVICE”', 'TURBINĂ DE LA DEZMEMBRĂRI · 800 LEI'],
   [17.6, 'AZI', 'LA TURBO DOCTOR', 'A TREIA OARĂ CU ACEEAȘI PROBLEMĂ']].forEach(([t, k, title, sub]) => {
    fx.push({ k: 'veil', t0: t, t1: t + CHD - .05, out: .16 }, { k: 'flash', t, a: .4 }, { k: 'glitch', t, d: .12 });
    items.push({ k: 'chap', t0: t, t1: t + CHD, kicker: k, title, sub, y: 880 });
  });
  // ---- bara poveștii, sus
  items.push({ k: 'band', t0: HEND, t1: SEND, y: 222, w: 980, h: 76, kicker: 'POVESTE',
    ph: [[HEND, 'CEA MAI IEFTINĂ OFERTĂ', 'EPISODUL 1'], [8.0, '„CELĂLALT SERVICE”', '3 SĂPT. ÎN URMĂ'], [17.6, 'TURBO DOCTOR', 'AZI · A 3-A OARĂ'],
      [SH.E, 'DIAGNOZA', 'AX CU JOC · CAUZA NEATINSĂ'], [A.suma - .05, 'SOCOTEALA', '800 × 3 = 2.400 LEI'], [A.da - .05, 'CONCLUZIA', 'CA LA CARTE, O DATĂ']] });

  // ---- B · flashback: oferta ieftină
  items.push({ k: 'chip', t0: A.lei800 - .05, t1: 17.5, y: CY, ph: [[A.lei800 - .05, 'money_bag', 'DEZMEMBRĂRI: 800 LEI', 'yellow'], [A.ce0 - .05, 'wrench', 'RECONDIȚIONATĂ: 1.200 LEI', 'blue']] });
  items.push({ k: 'stamp', t: A.brici - .03, t1: A.ce0 - .15, y: 1000, txt: 'MERGE BRICI', col: 'green', s: .72, rot: -6 });

  // ---- C/D · recepția: a treia oară
  items.push({ k: 'chip', t0: A.treia1 - .05, t1: SH.D + .1, y: CY, ph: [[A.treia1 - .05, 'warning', 'ACEEAȘI PROBLEMĂ · A 3-A OARĂ', 'red']] });
  items.push({ k: 'chip', t0: A.am - .05, t1: SH.E - .1, y: CY, ph: [[A.am - .05, 'money_with_wings', '„AM REPARAT IEFTIN”', 'yellow']] });
  items.push({ k: 'stamp', t: A.chilipir - .03, t1: SH.E - .1, y: 1000, txt: 'CHILIPIR?', col: 'red', s: .78, rot: -8 });

  // ---- E/F · bancul: constatarea și socoteala
  items.push({ k: 'chip', t0: A.joc - .05, t1: A.opt - .25, y: CY, ph: [[A.joc - .05, 'gear', 'AX CU JOC', 'red'], [A.cauza - .05, 'magnifying_glass_tilted_left', 'CAUZA: NEATINSĂ', 'red']] });
  items.push({ k: 'cmp', t0: A.opt - .1, t1: A.merge_e + .5, top: 1010, w: 760, ico: 'money_bag', title: 'IEFTIN vs. CORECT', dimA: true,
    a: [A.opt, 'money_with_wings', 'DEZMEMBRĂRI', '800 LEI × 3 = 2.400'], b: [A.o3, 'check_mark_button', 'RECONDIȚIONATĂ', '1.200 LEI · O DATĂ'] });
  items.push({ k: 'kin', t: A.dublu - .02, dur: 1.5, txt: 'DUBLU. ȘI TOT NU MERGE', col: '#FF3B30', y: 900, size: 56, rot: -3 });

  // ---- G/H/I · realizarea și decizia
  items.push({ k: 'chip', t0: A.sarac - .05, t1: A.ieftine_e + .5, y: CY, ph: [[A.sarac - .05, 'brain', '„PREA SĂRAC PENTRU LUCRURI IEFTINE”', 'yellow']] });
  items.push({ k: 'kin', t: A.carte - .02, dur: 1.6, txt: 'CA LA CARTE, O DATĂ', col: '#4ADE80', y: CY, size: 66, rot: -3 });
  items.push({ k: 'chip', t0: A.fao - .05, t1: A.asta_e + .6, y: CY, ph: [[A.fao - .05, 'check_mark_button', 'FĂ-O CUM TREBUIE', 'green']] });
  items.push({ k: 'stamp', t: SH.Z + 1.2, t1: SH.Z + 4.2, y: 1000, txt: 'GATA DE PREDARE', col: 'green', s: .78, rot: -6 });

  fx.push({ k: 'punch', t: A.chilipir, a: .05, sh: 8 }, { k: 'punch', t: A.suma, a: .06, sh: 10 }, { k: 'punch', t: A.dublu, a: .07, sh: 12 }, { k: 'punch', t: A.carte, a: .05 });

  return {
    hook: { tag: 'POVESTE · FIȘA PACIENTULUI', l1: 'POV: CÂND AI LUAT', l1At: .15, l2: 'CEA MAI <span class="w">IEFTINĂ</span> OFERTĂ', l2At: .8, l2Col: '#FFD21F',
      car: 'ȘI A ȚINUT 3 SĂPTĂMÂNI', carAt: 2.0, stk1: 'money_with_wings', y: -40, end: HEND },
    stages: null,
    tags: {
      0: { trage: 'r', treia: 'y', oara: 'y', turbo: 'c', doctor: 'c', dezmembrari: 'r', 800: 'y', brici: 'g', 1200: 'y', reconditionata: 'c' },
      1: { pacientul: 'c', problema: 'r', treia: 'y', oara: 'y', ieftin: 'r', chilipir: 'r' },
      2: { ax: 'c', joc: 'r', cauza: 'r', nimeni: 'r', 800: 'y', trei: 'y', 2400: 'y' },
      3: { reconditionata: 'c', corect: 'g', 1200: 'y', singura: 'g', data: 'g', ieftin: 'r', dublu: 'r', merge: 'r' },
      4: { dreptate: 'g', sarac: 'y', ieftine: 'r', exact: 'g', carte: 'g', singura: 'g', data: 'g' },
      5: { trebuie: 'g', stresul: 'r' },
    },
    items, fx, sfx: [], bursts: [],
  };
};
