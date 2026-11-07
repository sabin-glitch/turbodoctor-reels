// v2 – „Asamblarea unei turbine, pas cu pas” – VARIANTA NORMALĂ (viteză naturală, ~4:08): clipul de 5:34 din 06.11.2026 fără cadrele moarte (EDL în tools/asamblare/),
// narator cu vocea clonată a lui Sabin (ElevenLabs), scenariu simplu, cu analogii (jaluzele, axul de bicicletă, roata, ușa și tocul, pietricica în pantof)
// Tăieturile (în timpul final) sunt mascate cu glitch + flash (CUTS); pașii 1-3 rulează continuu (4.8-66 s din sursă, cu 3 momente statice întinse).
// Fără față în cadru: turbina și mâinile stau în mijloc (y ≈ 300–1050). Grafica stă pe masă, JOS (cardTop 1080), subtitrările mai jos (capTop 1640),
// bara de pași sus (band y 222). Fiecare pas = capitol („PASUL n / 7”) cu veil + flash + glitch, ca la „Reparații în lucru” (01.11.2026).
// Pașii: 1 geometria variabilă (verificare) · 2 cartușul · 3 fixarea cartușului · 4 actuatorul · 5 carcasa de compresor · 6 tija actuatorului · 7 controlul final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    asa0: aw(0, 'Așa'), pas0: aw(0, 'pas'), lab0: aw(0, 'laboratorul'),
    avem1: aw(1, 'Începem'), carcasa1: aw(1, 'carcasa'), geometria1: aw(1, 'geometria'), inelul1: aw(1, 'inel'),
    inainte2: aw(2, 'Paletele'), paletele2: aw(2, 'verificăm'), liber2: aw(2, 'liber.'), blocare2: ew(2, 'liber.'), jaluzelele2: aw(2, 'jaluzelele'),
    urmeaza3: aw(3, 'Urmează'), axul3: aw(3, 'axul'), rotorT3: aw(3, 'ax'), rotorC3: aw(3, 'rotor'), carcasa3: aw(3, 'lagăre'),
    iar4: aw(4, 'Rotorul'), exact4: aw(4, 'exact'), cartusul4: aw(4, 'cartușul'),
    aici5: aw(5, 'Aici'), uniform5: aw(5, 'Strângem'), perfect5: aw(5, 'roată:'),
    orice6: aw(6, 'De'), in7: aw(7, 'La'), sutimi7: aw(7, 'hârtie'), de7: aw(7, 'diferența'),
    urmeaza8: aw(8, 'Urmează'), el9: aw(9, 'Se'), tija9: aw(9, 'Tija'), un10: aw(10, 'Un'), reglat10: aw(10, 'reglat'),
    un11: aw(11, 'Un'), rotorul11: aw(11, 'rotorul'), liber11: aw(11, 'liber,'), jocE11: ew(11, 'joace.'),
    acum12: aw(12, 'Acum'), ea12: aw(12, 'Se'), peste12: aw(12, 'peste'), orienteaza12: aw(12, 'rotește'),
    elementele13: aw(13, 'Elementele'), monteaza13: aw(13, 'pun'), cheia13: aw(13, 'cheia,'), uniform13: aw(13, 'uniform,'),
    aici14: aw(14, 'Și'), intotdeauna15: aw(15, 'Lucrăm'), manusi15: aw(15, 'mănuși'), impuritate15: aw(15, 'nisip'),
    odata16: aw(16, 'Cu'), fixata16: aw(16, 'fixată,'), protejat16: aw(16, 'protejat,'), ansamblu16: aw(16, 'ansamblu'),
    urmeaza17: aw(17, 'Urmează'), parghia17: aw(17, 'pârghia'), iar18: aw(18, 'Lungimea'), apoi19: aw(19, 'Apoi'), fix19: aw(19, 'fix'),
    ultima20: aw(20, 'Ultima'), strangere21: aw(21, 'strângere'), mecanismul21: aw(21, 'mecanismul'), cursa21: aw(21, 'cursa.'),
    iar22: aw(22, 'Reglajul'), milimetru22: aw(22, 'milimetru'), comportamentul22: aw(22, 'merge'),
    iar23: aw(23, 'Iar'), curata23: aw(23, 'curată,'), reglataE23: ew(23, 'reglată.'), asa24: aw(24, 'Așa'),
    ulei25: aw(25, 'ulei'), amorseaza25: aw(25, 'amorsează'),
  };
  const HEND = A.avem1 - .15;
  const CHD = 1.65;  // cât stă cardul de capitol
  // capitolele: [t, kicker, titlu, sub, textul de pe bară]
  const CH = [[A.avem1 - .05, 'PASUL 1 / 7', 'GEOMETRIA VARIABILĂ', 'INELUL CU PALETE MOBILE', 'GEOMETRIA VARIABILĂ'],
              [A.urmeaza3 - .05, 'PASUL 2 / 7', 'CARTUȘUL', 'AX · ROTOARE · LAGĂRE', 'CARTUȘUL'],
              [A.aici5 - .05, 'PASUL 3 / 7', 'FIXAREA CARTUȘULUI', 'PE CARCASA DE TURBINĂ', 'FIXAREA CARTUȘULUI'],
              [A.urmeaza8 - .05, 'PASUL 4 / 7', 'ACTUATORUL', 'COMANDA GEOMETRIEI', 'ACTUATORUL'],
              [A.acum12 - .05, 'PASUL 5 / 7', 'CARCASA DE COMPRESOR', 'AȘEZARE · ORIENTARE · STRÂNGERE', 'CARCASA DE COMPRESOR'],
              [A.urmeaza17 - .05, 'PASUL 6 / 7', 'TIJA ACTUATORULUI', 'CUPLARE ȘI REGLAJ', 'TIJA ACTUATORULUI'],
              [A.ultima20 - .05, 'PASUL 7 / 7', 'CONTROLUL FINAL', 'VERIFICĂRI ȘI REGLAJ FIN', 'CONTROLUL FINAL']];
  const S = CH.map(c => c[0]);
  const items = [], fx = [];
  CH.forEach(([t, k, title, sub]) => {
    fx.push({ k: 'veil', t0: t, t1: t + CHD - .05, out: .16 }, { k: 'flash', t, a: .45 }, { k: 'glitch', t, d: .12 });
    items.push({ k: 'chap', t0: t, t1: t + CHD, kicker: k, title, sub, y: 880 });
  });
  items.push({ k: 'band', t0: HEND, t1: SEND, y: 222, w: 980, h: 76, kicker: 'ASAMBLARE TURBINĂ',
    ph: CH.map(([t, k, , , txt]) => [t, txt, k.replace('PASUL ', 'PASUL ').replace(/ \/ /, '/')]) });
  const Y = 1100;  // chip-urile, jos, pe masă

  // ---- HOOK (0 – prima frază): titlul peste carcasa din menghină
  items.push({ k: 'scan', t0: .4, t1: HEND - .2, box: [380, 400, 360, 380], lab: 'SCANARE...', lab2: 'CARCASĂ DE TURBINĂ', at2: A.lab0 - .1, labBelow: false });

  // ---- 1 · GEOMETRIA VARIABILĂ: fișa + definiție + verificarea paletelor
  items.push({ k: 'file', t0: S[0] + CHD + .05, t1: A.inainte2 - .3, no: '', ecg: 'ok', rows: [[S[0] + CHD + .1, 'PACIENT', 'TURBOSUFLANTĂ', 'c', 'gear'],
    [A.geometria1, 'TIP', 'GEOMETRIE VARIABILĂ', 'c', 'dashing_away'], [A.geometria1 + .5, 'INTERVENȚIE', 'ASAMBLARE COMPLETĂ', 'y', 'hammer_and_wrench'],
    [A.inelul1, 'UNITATE', 'LABORATOR TURBO DOCTOR', 'g', 'microscope']] });
  items.push({ k: 'def', t0: A.inainte2 - .05, t1: S[1] - .3, term: 'GEOMETRIE VARIABILĂ',
    text: 'Palete mobile care dozează gazele spre turbină, ca jaluzelele unei ferestre: se închid la turații mici, se deschid la turații mari.' });
  items.push({ k: 'scan', t0: A.inainte2 - .05, t1: S[1] - .4, box: [470, 430, 320, 300], lab: 'VERIFICARE PALETE...', lab2: 'PALETE: LIBERE', at2: A.liber2 + .1 });
  items.push({ k: 'stamp', t: A.blocare2 - .3, t1: S[1] - .3, txt: 'SE MIȘCĂ LIBER', y: 800, col: 'green', s: .78, rot: -7 });

  // ---- 2 · CARTUȘUL: componentele, pe ce enumeră
  items.push({ k: 'list', t0: S[1] + CHD + .05, t1: A.iar4 - .3, ico: 'gear', title: 'CARTUȘUL · INIMA TURBINEI',
    rows: [[A.axul3, 'CA AXUL UNEI ROȚI DE BICICLETĂ'], [A.rotorT3, 'UN AX CU UN ROTOR LA FIECARE CAPĂT'], [A.carcasa3, 'LAGĂRE UNSE CU ULEI']] });
  items.push({ k: 'chip', t0: A.iar4 - .05, t1: S[2] - .3, y: Y, ph: [[A.iar4 - .05, 'gear', 'ROTORUL INTRĂ ÎN INELUL CU PALETE', 'blue'],
    [A.cartusul4 - .05, 'check_mark_button', 'CARTUȘUL, AȘEZAT PE CARCASĂ', 'green']] });
  items.push({ k: 'stamp', t: A.exact4 - .03, t1: A.exact4 + 1.6, txt: 'EXACT ÎN MIJLOC', y: 760, col: 'green', s: .8, rot: -6 });

  // ---- 3 · FIXAREA CARTUȘULUI: strângere uniformă, centrare, toleranțe
  items.push({ k: 'chip', t0: S[2] + CHD + .05, t1: A.orice6 - .3, y: Y, ph: [[S[2] + CHD + .05, 'nutbolt', 'CARTUȘ FIXAT PE CARCASA DE TURBINĂ', 'blue'],
    [A.uniform5 - .05, 'wrench', 'PUȚIN CÂTE PUȚIN, PE RÂND', 'yellow'], [A.perfect5 - .05, 'check_mark_button', 'CA LA MONTAREA UNEI ROȚI', 'green']] });
  items.push({ k: 'def', t0: A.orice6 - .05, t1: A.in7 - .3, term: 'DE CE ATÂTA GRIJĂ?',
    text: 'Turbina se învârte de sute de mii de ori pe minut, de zeci de ori mai repede decât motorul: orice abatere devine vibrație și uzură.' });
  items.push({ k: 'kin', t: A.sutimi7 - .02, dur: 1.7, txt: 'CÂT O FOAIE DE HÂRTIE', col: '#FFD21F', y: 1150, size: 80, rot: -3 });
  items.push({ k: 'chip', t0: A.de7 - .05, t1: S[3] - .3, y: Y, ph: [[A.de7 - .05, 'warning', 'FACE DIFERENȚA: ȚINE SAU SE STRICĂ', 'yellow']] });

  // ---- 4 · ACTUATORUL: definiție, schema capsulei, montajul pe suport, controlul rotorului
  items.push({ k: 'def', t0: S[3] + CHD + .05, t1: A.el9 - .3, term: 'ACTUATORUL',
    text: 'Mușchiul turbinei: primește comanda de la motor și trage de tijă, iar tija rotește paletele geometriei.' });
  items.push({ k: 'schem', t0: A.el9 - .05, t1: A.un11 - .3, h: 370, type: 'vacuumCapsule', title: 'SCHEMĂ · ACTUATOR ȘI GEOMETRIE', sub: 'PASUL 4',
    stepNames: ['MONTAJ', 'COMANDĂ', 'REGLAJ'],
    steps: [[A.el9 - .05, 'Actuatorul se montează pe suportul de pe carcasă', '', 'ok'], [A.tija9 - .05, 'Tija trage de pârghie și rotește toate paletele deodată', 'y', 'ok'],
      [A.un10 - .05, 'Reglat bine: răspuns imediat la accelerație', 'g', 'ok']] });
  items.push({ k: 'scan', t0: A.un10 - .05, t1: A.un11 - .4, box: [430, 740, 290, 280], lab: 'ACTUATOR...', lab2: 'MONTAT PE SUPORT', at2: A.reglat10 - .05 });
  items.push({ k: 'chip', t0: A.un11 - .05, t1: S[4] - .3, y: Y, ph: [[A.un11 - .05, 'magnifying_glass_tilted_left', 'CONTROL: ROTORUL DE COMPRESOR', 'blue'],
    [A.liber11 - .05, 'check_mark_button', 'SE ÎNVÂRTE LIBER, CA O ROATĂ BINE UNSĂ', 'green']] });
  items.push({ k: 'scan', t0: A.rotorul11 - .05, t1: S[4] - .4, box: [600, 420, 300, 230], lab: 'ROTOR COMPRESOR...', lab2: 'ROTIRE LIBERĂ', at2: A.liber11 + .05 });
  items.push({ k: 'stamp', t: A.jocE11 - .1, t1: S[4] - .3, txt: 'FĂRĂ JOC', y: 760, col: 'green', s: .8, rot: -6 });

  // ---- 5 · CARCASA DE COMPRESOR: așezare, orientare, strângere, jocul rotor–carcasă, curățenie
  items.push({ k: 'scan', t0: S[4] + CHD + .05, t1: A.orienteaza12 + 2.2, box: [560, 220, 440, 420], lab: 'CARCASA DE COMPRESOR', lab2: 'PESTE ROTOR', at2: A.peste12, labBelow: true });
  items.push({ k: 'chip', t0: A.ea12 - .05, t1: A.elementele13 - .3, y: Y, ph: [[A.ea12 - .05, 'package', 'SE AȘAZĂ PESTE ROTOR', 'blue'],
    [A.orienteaza12 - .05, 'round_pushpin', 'ROTITĂ DUPĂ CONDUCTELE MAȘINII', 'yellow']] });
  items.push({ k: 'list', t0: A.elementele13 - .05, t1: A.aici14 - .3, ico: 'wrench', title: 'STRÂNGEREA CARCASEI',
    rows: [[A.monteaza13, 'PRINDERILE, PUSE PE RÂND'], [A.cheia13, 'STRÂNSE CU CHEIA'], [A.uniform13, 'UNIFORM, DE JUR ÎMPREJUR']] });
  items.push({ k: 'def', t0: A.aici14 - .05, t1: A.intotdeauna15 - .3, term: 'JOCUL ROTOR – CARCASĂ',
    text: 'Ca distanța dintre ușă și toc: prea mare = pierzi presiune, prea mică = se freacă și se strică.' });
  items.push({ k: 'list', t0: A.intotdeauna15 - .05, t1: A.odata16 - .3, ico: 'sparkles', title: 'CURĂȚENIE LA MONTAJ',
    rows: [[A.manusi15, 'MĂNUȘI ȘI PIESE CURATE'], [A.impuritate15, 'UN FIR DE NISIP = O PIETRICICĂ ÎN PANTOF', 'bad']] });
  items.push({ k: 'chip', t0: A.odata16 - .05, t1: S[5] - .3, y: Y, ph: [[A.odata16 - .05, 'check_mark_button', 'CARCASA DE COMPRESOR: FIXATĂ', 'green'],
    [A.protejat16 - .05, 'shield', 'ROTORUL ESTE PROTEJAT', 'blue'], [A.ansamblu16 - .05, 'gear', 'ANSAMBLU COMPLET', 'yellow']] });
  items.push({ k: 'stamp', t: A.fixata16 - .03, t1: A.fixata16 + 1.6, txt: 'FIXATĂ', y: 760, col: 'green', s: .85, rot: -7 });

  // ---- 6 · TIJA ACTUATORULUI: cuplare, reglaj, asigurare
  items.push({ k: 'scan', t0: S[5] + CHD + .05, t1: A.iar18 - .3, box: [520, 520, 180, 280], lab: 'TIJA ACTUATORULUI', lab2: 'CUPLATĂ LA PÂRGHIE', at2: A.parghia17 - .05 });
  items.push({ k: 'def', t0: A.iar18 - .05, t1: A.apoi19 - .3, term: 'REGLAJUL TIJEI',
    text: 'Ca sfoara unei jaluzele: prea lungă sau prea scurtă, și paletele nu se mai deschid cum trebuie.' });
  items.push({ k: 'chip', t0: A.apoi19 - .05, t1: S[6] - .3, y: Y, ph: [[A.apoi19 - .05, 'nutbolt', 'TIJA SE ASIGURĂ', 'blue'],
    [A.fix19 - .05, 'check_mark_button', 'REGLAJ FIX: VIBRAȚII · CĂLDURĂ', 'green']] });

  // ---- 7 · CONTROLUL FINAL: verificări, reglaj fin, gata de predare
  items.push({ k: 'list', t0: S[6] + CHD + .05, t1: A.iar22 - .3, ico: 'magnifying_glass_tilted_left', title: 'CONTROLUL FINAL',
    rows: [[A.strangere21, 'FIECARE STRÂNGERE, VERIFICATĂ'], [A.mecanismul21, 'GEOMETRIA, ACȚIONATĂ MANUAL'], [A.cursa21 - .3, 'PALETELE RĂSPUND PE TOATĂ CURSA']] });
  items.push({ k: 'chip', t0: A.iar22 - .05, t1: A.iar23 - .3, y: Y, ph: [[A.iar22 - .05, 'wrench', 'REGLAJ FIN, CU RĂBDARE', 'yellow'],
    [A.comportamentul22 - .05, 'gear', 'SE SIMTE ÎN CUM MERGE MAȘINA', 'blue']] });
  items.push({ k: 'kin', t: A.milimetru22 - .02, dur: 1.6, txt: 'UN MILIMETRU CONTEAZĂ', col: '#FFD21F', y: 1150, size: 80, rot: -3 });
  items.push({ k: 'scan', t0: A.iar23 - .05, t1: SEND - .3, box: [380, 330, 600, 620], lab: 'CONTROL VIZUAL...', lab2: 'VERIFICATĂ', at2: A.reglataE23 - .1, labBelow: true });
  items.push({ k: 'stamp', t: A.reglataE23 + .05, t1: SEND - .2, txt: 'GATA DE PREDARE', y: 950, col: 'green', s: .9, rot: -6 });
  items.push({ k: 'chip', t0: A.asa24 - .05, t1: SEND - .2, y: Y, ph: [[A.asa24 - .05, 'sparkles', 'AȘA LUCRĂM LA TURBO DOCTOR', 'yellow']] });

  // ---- Rețeta Turbo Doctor (pe cadrul încetinit de la final)
  items.push({ k: 'tip', t0: SEND + .1, t1: TEND - .15, top: 560, title: 'REȚETA TURBO DOCTOR', sub: 'SFAT DE INGINER · DUPĂ MONTAJ', ico: 'stethoscope',
    rows: [[SEND + .7, 'oil_drum', 'Ulei și filtru noi la montajul turbinei'], [A.amorseaza25 - .05, 'droplet', 'Amorsează turbina cu ulei înainte de prima pornire'],
      [TEND - 2.4, 'stopwatch', 'Înainte de oprire, lasă motorul puțin la ralanti']] });

  const CUTS = [64.05, 136.05, 142.05, 150.05, 156.05, 162.05, 166.05, 190.05, 210.05, 218.05, 224.05];  // tăieturile din tools/asamblare/v1_cut_edl.json (timp final)
  CUTS.forEach(t => fx.push({ k: 'glitch', t: t - .04, d: .14 }, { k: 'flash', t: t - .02, a: .2 }));
  fx.push({ k: 'punch', t: A.exact4, a: .05, sh: 7 }, { k: 'punch', t: A.jocE11 - .1, a: .05, sh: 7 }, { k: 'punch', t: A.fixata16, a: .05, sh: 7 },
    { k: 'punch', t: A.reglataE23 + .05, a: .06, sh: 8 }, { k: 'glitch', t: A.sutimi7 - .02, d: .12 }, { k: 'glitch', t: A.milimetru22 - .02, d: .12 });

  return {
    capTop: 1640, cardTop: 1080,
    hook: { tag: 'LABORATOR TURBO DOCTOR · ASAMBLARE', l1: 'ASAMBLAREA UNEI TURBINE', l1At: .35, l2: 'PAS CU PAS', l2At: A.pas0 + .02, l2Col: '#FFD21F',
      car: 'TURBINĂ CU GEOMETRIE VARIABILĂ', carAt: A.lab0, y: 420, end: HEND },
    hideCap: [[0, HEND]],
    tags: { 0: { turbina: 'c', turbo: 'y', doctor: 'y' }, 1: { geometria: 'c', variabila: 'c', palete: 'c' }, 2: { jaluzelele: 'y', liber: 'g' },
      3: { cartusul: 'c', bicicleta: 'y', rotor: 'c', lagare: 'c' }, 4: { exact: 'g', centrul: 'g' }, 5: { rand: 'y', roata: 'y', niciodata: 'r' },
      6: { sute: 'y', mii: 'y', zeci: 'y' }, 7: { hartie: 'y', tine: 'g', strica: 'r' }, 8: { actuatorul: 'c', muschiul: 'y', tija: 'c' },
      9: { tija: 'c', parghia: 'c', jaluzele: 'y' }, 10: { bine: 'g', imediat: 'g', gol: 'r' }, 11: { liber: 'g', unsa: 'g', frece: 'r', joace: 'r' },
      12: { carcasa: 'c', compresor: 'c', capacul: 'y' }, 13: { uniform: 'y', cheia: 'c' }, 14: { usa: 'y', toc: 'y', presiune: 'r', strica: 'r' },
      15: { curate: 'g', nisip: 'r', pietricica: 'y', rau: 'r' }, 16: { fixata: 'g', protejat: 'g', complet: 'g' },
      17: { tija: 'c', parghia: 'c', actuator: 'c' }, 18: { milimetru: 'y', jaluzea: 'y', sfoara: 'y' }, 19: { fix: 'g', vibratii: 'r', caldura: 'r' },
      20: { final: 'y' }, 21: { verificata: 'g', manual: 'y', cursa: 'c' }, 22: { milimetru: 'y', rabdare: 'g', masina: 'c' },
      23: { curata: 'g', corect: 'g', reglata: 'g' }, 24: { turbo: 'y', doctor: 'y' }, 25: { ulei: 'c', filtru: 'c', amorseaza: 'g', uscat: 'r' } },
    items, fx,
    sfx: [[A.liber2 + .1, 'scan', .4]],
    bursts: [],
  };
};
