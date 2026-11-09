// v2 – Reel #8 din vlogul „Top 3 simptome injector defect” – ce se strică în interiorul injectorului (sursa 572.42–642.55)
// Hook: cold open din același clip (sursa 604.82–610.87, „De cele mai multe ori, problemele apar la nivelul supapei de retur sau la nivelul pulverizatorului.”),
// cu imaginea din același moment, apoi povestea de la început. Toată secvența e cu injectorul în mână (fără față), deci schemele stau deasupra cadrului.
// Eticheta veche a vlogului („PRINCIPII FUNCȚIONARE”) e acoperită de lbl. Schema nouă `injectorParts` e în pipeline/schem.js din 09.11.2026.
// cardul de final al seriei „simptome injector” (cerut de Sabin pe 08.11.2026, doar pentru această serie): cardul standard + „Experți în diagnosticarea sistemelor de injecție” + telefonul
// Telefonul de pe cardul de final (ENDCARD) a fost cerut DOAR pentru seria asta; implicit nu se pune (regula din 25.10.2026). Seria a fost aprobată și programată pe 09.11.2026.
const ENDCARD = (TEND, TOTAL) => [
  { k: 'lbl', t0: TEND + .12, t1: TOTAL + 1, x: 540, y: 236, w: 960, h: 176, ph: [[TEND + .12, '', '<span style="color:#fff">EXPERȚI ÎN DIAGNOSTICAREA</span><br>SISTEMELOR DE INJECȚIE', 'y']] },
  { k: 'eq', t0: TEND + 2.45, t1: TOTAL + 1, top: 1172, ico: 'phone', title: 'PROGRAMĂRI', sub: '', lines: [[TEND + 2.7, '0739 065 065', 'big y']] },
];
window.REEL_CFG = ({ aw, ew, cw, cwe, S0, SEND, TEND, TOTAL }) => {
  const A = {
    bosch0: aw(0, 'Bosch'), delphi: aw(0, 'Delphi'), continental: aw(0, 'Continental'), denso: aw(0, 'Denso'),
    in1: aw(1, 'În'), supapa: aw(1, 'supapa'), magnetice1: aw(1, 'magnetice'),
    pulv2: aw(2, 'pulverizatorul'), duza: aw(2, 'duza'), ardere: aw(2, 'ardere'),
    in3: aw(3, 'În'), magnetice3: aw(3, 'magnetice'), foarte: aw(3, 'foarte'), magnetii: aw(3, 'magneții'),
    de4: aw(4, 'De'), supapei4: aw(4, 'supapei'), pulv4: aw(4, 'pulverizatorului'),
    de5: aw(5, 'De'), impuritati: aw(5, 'impurități'), apei: aw(5, 'apei'), factori: aw(5, 'factori'),
    in6: aw(6, 'În'), piezo6: aw(6, 'piezoelectrice'), problemele6: aw(6, 'problemele'),
    piezo7: aw(7, 'piezoelectric'),
  };
  const T1 = cw('De') + .02, T2 = cw('supapei') - .02, T3 = cw('pulverizatorului') - .02;
  return {
    stages: [[S0, 'PRINCIPII'], [A.in1 - .1, 'COMPONENTE'], [A.de4 - .1, 'DEFECTE'], [A.de5 - .1, 'CAUZE'], [A.in6 - .1, 'PIEZO']],
    items: [
      // HOOK (cold open din același clip)
      { k: 'chip', t0: .05, t1: S0, y: 172, ph: [[.05, 'magnifying_glass_tilted_left', 'CE SE STRICĂ CEL MAI DES LA INJECTOR?', 'yellow']] },
      { k: 'boom', t: T1, dur: S0 - T1, txt: 'DE CELE MAI MULTE ORI', y: 372, size: 92, col: '#FFFFFF', from: 3.2, sh: 16, ca: 20, bg: 1 },
      { k: 'boom', t: T2, dur: S0 - T2, txt: 'SUPAPA DE RETUR', y: 600, size: 128, col: '#FFD21F', from: 3.6, sh: 26, ca: 30, bg: 1 },
      { k: 'kin', t: T3, dur: S0 - T3 + .05, txt: 'SAU PULVERIZATORUL', col: '#FFFFFF', y: 1640, size: 90, rot: -3 },
      // eticheta veche a vlogului, acoperită
      { k: 'lbl', t0: S0, t1: S0 + 5.25, x: 300, y: 937, w: 540, h: 108, ph: [[S0, 'INJECTOARE DIESEL', 'PRINCIPII DE FUNCȚIONARE']] },
      { k: 'list', t0: A.bosch0 - .35, t1: A.in1 - .3, top: 268, ico: 'gear', title: 'PRINCIPII ASEMĂNĂTOARE', rows: [
        [A.bosch0 - .05, 'Bosch', 'ok'], [A.delphi - .05, 'Delphi', 'ok'], [A.continental - .05, 'Continental', 'ok'], [A.denso - .05, 'Denso', 'ok']] },
      // anatomia injectorului magnetic, pe ce spune
      { k: 'schem', t0: A.in1 - .1, t1: A.in6 - .2, top: 268, h: 300, type: 'injectorParts', title: 'ÎN INTERIORUL INJECTORULUI', sub: 'INJECTOR MAGNETIC',
        stepNames: ['INTERIOR', 'SUPAPA DE CONTROL', 'PULVERIZATORUL', 'MAGNEȚII', 'CEL MAI DES', 'CAUZE'],
        steps: [[A.in1 - .1, 'Două componente principale', 'y', 0], [A.supapa - .05, 'Supapa de control', 'y', 1],
                [A.pulv2 - .05, 'Duza injectează motorina în camera de ardere', 'g', 2], [A.magnetice3 - .05, 'Magneții care comandă injectorul: foarte rar', 'y', 3],
                [A.de4 - .05, 'Problemele apar la supapa de retur sau la duză', 'r', 4], [A.impuritati - .05, 'Impurități sau apă în combustibil', 'r', 5]] },
      { k: 'schem', t0: A.in6 - .05, t1: SEND - .15, top: 268, h: 300, type: 'injectorParts', title: 'INJECTOR PIEZOELECTRIC', sub: 'CA CEL DIN MÂNĂ',
        stepNames: ['INJECTOR PIEZO', 'ÎN PLUS'],
        steps: [[A.in6 - .05, 'Aceleași probleme la supapa de retur și la duză', 'r', 6], [A.piezo7 - .05, 'Și elementul piezoelectric, care acționează injectorul', 'r', 7]] },
      { k: 'kin', t: A.foarte - .02, dur: 2.3, txt: 'FOARTE RAR', col: '#FFD21F', y: 1640, size: 120, rot: -3 },
      { k: 'kin', t: A.supapei4 - .02, dur: A.pulv4 - A.supapei4 - .08, txt: 'SUPAPA DE RETUR', col: '#FF3B30', y: 1640, size: 100, rot: -3 },
      { k: 'kin', t: A.pulv4 - .02, dur: 1.75, txt: 'SAU PULVERIZATORUL', col: '#FF3B30', y: 1640, size: 90, rot: -3 },
      { k: 'kin', t: A.impuritati - .02, dur: A.apei - A.impuritati - .08, txt: 'IMPURITĂȚI', col: '#FF8A3D', y: 1640, size: 120, rot: -3 },
      { k: 'kin', t: A.apei - .02, dur: 2.2, txt: 'APĂ ÎN COMBUSTIBIL', col: '#62D8FF', y: 1640, size: 90, rot: -3 },
      { k: 'kin', t: A.piezo7 - .02, dur: SEND - A.piezo7 - .1, txt: 'ELEMENTUL PIEZOELECTRIC', col: '#FF3B30', y: 1640, size: 76, rot: -3 },
      ...ENDCARD(TEND, TOTAL),
    ],
    fx: [
      { k: 'flash', t: T1 - .11, a: .4 }, { k: 'punch', t: T1, a: .08, sh: 16 }, { k: 'glitch', t: T1, d: .12 },
      { k: 'flash', t: T2 - .11, a: .75 }, { k: 'punch', t: T2, a: .16, sh: 34 }, { k: 'glitch', t: T2, d: .2 }, { k: 'shock', t: T2 + .01, x: 540, y: 600, r: 780, n: 2, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'punch', t: T3, a: .08, sh: 16 }, { k: 'glitch', t: S0 - .02, d: .14 },
      { k: 'punch', t: A.foarte, a: .05, sh: 10 }, { k: 'punch', t: A.supapei4, a: .07, sh: 14 }, { k: 'punch', t: A.pulv4, a: .06, sh: 12 },
      { k: 'punch', t: A.impuritati, a: .05, sh: 10 }, { k: 'punch', t: A.apei, a: .05, sh: 10 }, { k: 'glitch', t: A.piezo7 - .03, d: .14 }, { k: 'punch', t: A.piezo7, a: .08, sh: 16 },
    ],
    bursts: [[T2 + .04, 540, 600, 8, 460, 1.3]],
  };
};
