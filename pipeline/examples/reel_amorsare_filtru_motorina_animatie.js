// „Un banal schimb de filtru de motorină te poate costa peste 2.000 de euro” — reel animat 3D (animația „Amorsare filtru motorină”) cu vocea lui Sabin (ElevenLabs), 14.11.2026
// Hook pe pompa CP4 în secțiune care merge cu aer (tachetul se rotește, rola taie cama), apoi: circuitul tur/retur → schimb filtru → amorsare din diagnoză → fără amorsare → CP4 → contaminare.
// Animația e randată pe voce (tools/anim_amorsare: vo/uframes.json → U pe cadru); etichetele, testerul și panourile sunt în animație (modul `vo`).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const HK = aw(1, 'Hai') - .1;
  const T1 = aw(0, 'schimb') - .03, T2 = aw(0, 'peste') - .03;
  return {
    hideCap: [[0, HK - .05]],
    items: [
      { k: 'boom', t: T1, dur: HK - T1, txt: 'SCHIMB DE FILTRU', y: 290, size: 124, col: '#FFFFFF', from: 3.4, sh: 18, ca: 24, riser: false, bg: .6, cg: .3 },
      { k: 'boom', t: T2, dur: HK - T2, txt: 'PESTE 2.000 €', y: 440, size: 150, col: '#FF4B3E', from: 3.6, sh: 26, ca: 26, riser: false, bg: .6, cg: .35, glow: 'rgba(255,75,62,.5)' },
      { k: 'stamp', t: aw(14, 'autodistruge') - .03, t1: aw(15, 'Pilitura') - .2, y: 1120, txt: 'POMPĂ DISTRUSĂ', col: 'red', s: .8 },
      { k: 'stamp', t: aw(16, 'contaminat') - .03, t1: aw(16, 'De') - .2, y: 1120, txt: 'SISTEM CONTAMINAT', col: 'red', s: .8 },
      { k: 'stamp', t: aw(16, 'peste') - .03, t1: aw(17, 'Așa') - .2, y: 1120, txt: 'PESTE 2.000 €', col: 'red', s: .85 },
      { k: 'stamp', t: aw(17, 'amorsarea') - .03, t1: aw(18, 'Acum') - .2, y: 1120, txt: 'AMORSARE DIN DIAGNOZĂ', col: 'green', s: .75 },
    ],
    fx: [
      { k: 'punch', t: T1, a: .08, sh: 14 },
      { k: 'punch', t: T2, a: .16, sh: 34 }, { k: 'glitch', t: T2, d: .16 }, { k: 'flash', t: T2 - .11, a: .75 },
      { k: 'shock', t: T2 + .01, x: 540, y: 820, r: 700, n: 2, col: '#FF4B3E', col2: '#F39237' },
    ],
    bgFix: [[0, SEND]],
    tags: {
      0: { filtru: 'c', motorina: 'c', 2000: 'y', euro: 'y' }, 1: { distrugerea: 'r', pompei: 'c', inalta: 'c', presiune: 'c', injectie: 'c', filtru: 'c' },
      2: { alimentare: 'c', tur: 'c', retur: 'y' }, 3: { rezervor: 'c', pompa: 'c', electrica: 'c', auxiliara: 'c', tur: 'c' },
      4: { filtru: 'c', rezervor: 'c', pompa: 'c' }, 5: { pompa: 'c', 2000: 'y', bari: 'y', rampa: 'c', injectoare: 'c' },
      6: { retur: 'y', rezervor: 'c' }, 7: { filtrul: 'c', gol: 'r', aer: 'r' }, 8: { corect: 'g', amorsarea: 'g', diagnoza: 'g', testerul: 'c', cicluri: 'y' },
      9: { aerul: 'r', retur: 'y', plin: 'g', pornesti: 'g' }, 10: { sari: 'r', cheie: 'r', aerul: 'r', pompa: 'c' },
      11: { bosch: 'y', cp4: 'y', cama: 'c', tachetul: 'c', rola: 'c', pistonul: 'c', motorina: 'c' },
      12: { aer: 'r', dispare: 'r', blocheaza: 'r', freaca: 'r' }, 13: { tachetul: 'c', roteste: 'r', rola: 'c', taie: 'r' },
      14: { pilitura: 'r', metalica: 'r', autodistruge: 'r' }, 15: { pilitura: 'r', rampa: 'c', injectoare: 'c', rezervor: 'c' },
      16: { contaminat: 'r', pompa: 'c', injectoarele: 'c', rampa: 'c', conductele: 'c', rezervorul: 'c', 2000: 'y', euro: 'y' },
      17: { amorsarea: 'g', corecta: 'g', diagnoza: 'g' }, 18: { pilitura: 'r' }, 19: { injectie: 'c', turbo: 'y', doctor: 'y', ajuta: 'g' },
    },
  };
};
