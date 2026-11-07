// v2 – „Asamblarea unei turbine, pas cu pas” – VARIANTA ACCELERATĂ (~1:30): timelapse cu viteză variabilă (2–4×, EDL în tools/asamblare/),
// narator scurt pe fiecare pas cu vocea clonată a lui Sabin (ElevenLabs), cu analogii (jaluzele, axul de bicicletă, roata, ușa și tocul)
// Fără față în cadru: grafica stă jos, pe masă (cardTop 1080, capTop 1640), bara de pași sus (band y 222), capitole scurte (1,2 s) pe fiecare pas. Fără Rețetă (reel scurt).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    pas0: aw(0, 'pas'), lab0: aw(0, 'laboratorul'),
    intai1: aw(1, 'Întâi,'), paletele1: aw(1, 'paletele'), liber1: aw(1, 'liber.'),
    urmeaza2: aw(2, 'Urmează'), axul2: aw(2, 'cartușul,'), rotorul2: aw(2, 'ax'), cel2: aw(2, 'axul'), carcasa2: aw(2, 'bicicletă.'),
    apoi3: aw(3, 'Cartușul'), fixeaza3: aw(3, 'strânge'), centrat3: aw(3, 'roată'),
    urmeaza4: aw(4, 'Apoi'), capsula4: aw(4, 'capsula'), montata4: aw(4, 'rotește'),
    un5: aw(5, 'Un'), liber5: aw(5, 'liber,'), jocE5: ew(5, 'joc.'),
    acum6: aw(6, 'Acum'), peste6: aw(6, 'așază,'), orienteaza6: aw(6, 'orientează'), uniform6: aw(6, 'uniform.'),
    aici7: aw(7, 'Distanța'), jocul7: aw(7, 'ușă'), corect7: aw(7, 'freacă.'),
    urmeaza8: aw(8, 'Tija'), parghia8: aw(8, 'pârghie'), precizie8: aw(8, 'milimetru,'),
    iar9: aw(9, 'La'), strangere9: aw(9, 'strângere,'), cursa9: aw(9, 'cursa'), reglajul9: aw(9, 'reglajul'),
    acum10: aw(10, 'Turbina'), curata10: aw(10, 'curată,'), gata10: aw(10, 'gata'), predareE10: ew(10, 'predare.'), asa11: aw(11, 'Așa'),
  };
  const HEND = A.intai1 - .15;
  const CHD = 1.2;
  const CH = [[A.intai1 - .05, 'PASUL 1 / 7', 'GEOMETRIA VARIABILĂ', 'INELUL CU PALETE MOBILE', 'GEOMETRIA VARIABILĂ'],
              [A.urmeaza2 - .05, 'PASUL 2 / 7', 'CARTUȘUL', 'AX · ROTOARE · LAGĂRE', 'CARTUȘUL'],
              [16.45, 'PASUL 3 / 7', 'FIXAREA CARTUȘULUI', 'PE CARCASA DE TURBINĂ', 'FIXAREA CARTUȘULUI'],
              [23.12, 'PASUL 4 / 7', 'ACTUATORUL', 'COMANDA GEOMETRIEI', 'ACTUATORUL'],
              [A.acum6 - .05, 'PASUL 5 / 7', 'CARCASA DE COMPRESOR', 'AȘEZARE · ORIENTARE · STRÂNGERE', 'CARCASA DE COMPRESOR'],
              [A.urmeaza8 - .05, 'PASUL 6 / 7', 'TIJA ACTUATORULUI', 'CUPLARE ȘI REGLAJ', 'TIJA ACTUATORULUI'],
              [A.iar9 - .05, 'PASUL 7 / 7', 'CONTROLUL FINAL', 'VERIFICĂRI ȘI REGLAJ FIN', 'CONTROLUL FINAL']];
  const S = CH.map(c => c[0]);
  const items = [], fx = [];
  CH.forEach(([t, k, title, sub]) => {
    fx.push({ k: 'veil', t0: t, t1: t + CHD - .05, out: .14 }, { k: 'flash', t, a: .4 }, { k: 'glitch', t, d: .12 });
    items.push({ k: 'chap', t0: t, t1: t + CHD, kicker: k, title, sub, y: 880 });
  });
  items.push({ k: 'band', t0: HEND, t1: SEND, y: 222, w: 980, h: 76, kicker: 'TIMELAPSE',
    ph: CH.map(([t, k, , , txt]) => [t, txt, k.replace(/ \/ /, '/')]) });
  const Y = 1100;

  // ---- HOOK
  items.push({ k: 'scan', t0: .3, t1: HEND - .2, box: [380, 400, 360, 380], lab: 'SCANARE...', lab2: 'CARCASĂ DE TURBINĂ', at2: A.lab0 - .1, labBelow: false });

  // ---- 1 · geometria variabilă
  items.push({ k: 'chip', t0: S[0] + CHD + .05, t1: S[1] - .3, y: Y, ph: [[S[0] + CHD + .05, 'dashing_away', 'PALETE MOBILE, CA NIȘTE JALUZELE', 'blue'],
    [A.liber1 - .05, 'check_mark_button', 'PALETELE SE MIȘCĂ LIBER', 'green']] });
  items.push({ k: 'scan', t0: S[0] + CHD, t1: S[1] - .4, box: [470, 430, 320, 300], lab: 'VERIFICARE PALETE...', lab2: 'PALETE: LIBERE', at2: A.liber1 });

  // ---- 2 · cartușul
  items.push({ k: 'list', t0: S[1] + CHD + .05, t1: S[2] - .3, ico: 'gear', title: 'CE ESTE CARTUȘUL',
    rows: [[A.axul2, 'INIMA TURBINEI'], [A.rotorul2, 'UN AX CU DOUĂ ROTOARE'], [A.cel2, 'CA AXUL UNEI ROȚI DE BICICLETĂ']] });

  // ---- 3 · fixarea cartușului
  items.push({ k: 'chip', t0: S[2] + CHD + .05, t1: S[3] - .3, y: Y, ph: [[S[2] + CHD + .05, 'nutbolt', 'CARTUȘUL INTRĂ ÎN CARCASĂ', 'blue'],
    [A.fixeaza3 - .05, 'wrench', 'SE STRÂNGE PE RÂND', 'yellow'], [A.centrat3 - .05, 'check_mark_button', 'CA O ROATĂ DE MAȘINĂ', 'green']] });

  // ---- 4 · actuatorul + controlul rotorului
  items.push({ k: 'def', t0: S[3] + CHD + .05, t1: A.un5 - .3, term: 'ACTUATORUL',
    text: 'Mușchiul turbinei: primește comanda și trage de tijă, iar tija rotește paletele geometriei.' });
  items.push({ k: 'chip', t0: A.un5 - .05, t1: S[4] - .3, y: Y, ph: [[A.un5 - .05, 'magnifying_glass_tilted_left', 'CONTROL: ROTORUL DE COMPRESOR', 'blue'],
    [A.liber5 - .05, 'check_mark_button', 'SE ÎNVÂRTE LIBER, CA O ROATĂ BINE UNSĂ', 'green']] });
  items.push({ k: 'scan', t0: A.un5 + .2, t1: S[4] - .4, box: [600, 420, 300, 230], lab: 'ROTOR COMPRESOR...', lab2: 'ROTIRE LIBERĂ', at2: A.liber5 + .05 });

  // ---- 5 · carcasa de compresor
  items.push({ k: 'chip', t0: S[4] + CHD + .05, t1: A.aici7 - .3, y: Y, ph: [[S[4] + CHD + .05, 'package', 'SE AȘAZĂ PESTE ROTOR', 'blue'],
    [A.orienteaza6 - .05, 'round_pushpin', 'ORIENTATĂ DUPĂ CONDUCTE', 'yellow'], [A.uniform6 - .05, 'wrench', 'STRÂNSĂ UNIFORM, PE RÂND', 'green']] });
  items.push({ k: 'def', t0: A.aici7 - .05, t1: S[5] - .3, term: 'JOCUL ROTOR – CARCASĂ',
    text: 'Ca distanța dintre ușă și toc: prea mare = pierzi presiune, prea mică = se freacă și se strică.' });

  // ---- 6 · tija actuatorului
  items.push({ k: 'chip', t0: S[5] + CHD + .05, t1: S[6] - .3, y: Y, ph: [[S[5] + CHD + .05, 'nutbolt', 'TIJA, CUPLATĂ LA PÂRGHIE', 'blue'],
    [A.precizie8 - .05, 'check_mark_button', 'REGLATĂ LA MILIMETRU, CA SFOARA JALUZELEI', 'green']] });
  items.push({ k: 'scan', t0: S[5] + CHD, t1: A.precizie8 - .2, box: [520, 520, 180, 280], lab: 'TIJA ACTUATORULUI', lab2: 'CUPLATĂ LA PÂRGHIE', at2: A.parghia8 - .05 });

  // ---- 7 · controlul final
  items.push({ k: 'list', t0: S[6] + CHD + .05, t1: A.acum10 - .3, ico: 'magnifying_glass_tilted_left', title: 'CONTROLUL FINAL',
    rows: [[A.strangere9 - .2, 'FIECARE STRÂNGERE, VERIFICATĂ'], [A.cursa9 - .1, 'PALETELE RĂSPUND PE TOATĂ CURSA'], [A.reglajul9 - .05, 'REGLAJUL FIN AL TIJEI']] });
  items.push({ k: 'scan', t0: A.acum10 - .05, t1: SEND - .3, box: [380, 330, 600, 620], lab: 'CONTROL VIZUAL...', lab2: 'VERIFICATĂ', at2: A.gata10 - .05, labBelow: true });
  items.push({ k: 'stamp', t: A.gata10 - .03, t1: SEND - .2, txt: 'GATA DE PREDARE', y: 950, col: 'green', s: .9, rot: -6 });
  items.push({ k: 'chip', t0: A.asa11 - .05, t1: SEND - .2, y: Y, ph: [[A.asa11 - .05, 'sparkles', 'AȘA LUCRĂM LA TURBO DOCTOR', 'yellow']] });

  fx.push({ k: 'punch', t: A.centrat3, a: .05, sh: 7 }, { k: 'punch', t: A.gata10, a: .06, sh: 8 });

  return {
    capTop: 1640, cardTop: 1080,
    hook: { tag: 'LABORATOR TURBO DOCTOR · TIMELAPSE', l1: 'ASAMBLAREA UNEI TURBINE', l1At: .3, l2: 'PAS CU PAS', l2At: A.pas0 + .02, l2Col: '#FFD21F',
      car: 'TURBINĂ CU GEOMETRIE VARIABILĂ', carAt: A.lab0, y: 420, end: HEND },
    hideCap: [[0, HEND]],
    tags: { 0: { turbina: 'c', turbo: 'y', doctor: 'y' }, 1: { geometria: 'c', variabila: 'c', jaluzele: 'y', liber: 'g' }, 2: { cartusul: 'c', inima: 'y', bicicleta: 'y' },
      3: { rand: 'y', roata: 'y' }, 4: { actuatorul: 'c', muschiul: 'y', tija: 'c' }, 5: { liber: 'g', frecare: 'r', joc: 'r' },
      6: { carcasa: 'c', compresor: 'c', capacul: 'y', uniform: 'g' }, 7: { usa: 'y', toc: 'y', presiune: 'r', freaca: 'r' }, 8: { tija: 'c', parghie: 'c', milimetru: 'y', jaluzele: 'y' },
      9: { strangere: 'c', cursa: 'c', fin: 'y' }, 10: { curata: 'g', corect: 'g', reglata: 'g', gata: 'g', predare: 'g' }, 11: { turbo: 'y', doctor: 'y' } },
    items, fx, sfx: [], bursts: [],
  };
};
