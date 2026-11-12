// „Admisia plină de depuneri îți poate distruge turbina” — reel animat 3D (animația „Depuneri EGR în admisie”) cu vocea lui Sabin (ElevenLabs), 12.11.2026
// Hook pe loviturile din geometria variabilă, apoi traseul: motor → turbină → EGR → galeria N47 → depuneri → desprindere → motor / turbină → curățare.
// Animația e randată pe voce (tools/anim_egr: vo/umap.json → U pe cadru); etichetele și HUD-ul sunt în animație.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const HK = aw(1, 'Hai') - .1;
  const T1 = aw(0, 'admisia') - .03, T2 = aw(0, 'distruge') - .03, T3 = aw(0, 'motorul') - .03;
  return {
    hideCap: [[0, HK - .05]],
    items: [
      { k: 'boom', t: T1, dur: T2 - .08 - T1, txt: 'ADMISIA', y: 300, size: 190, col: '#FFFFFF', from: 3.4, sh: 18, ca: 24, riser: false, bg: .55, cg: .3 },
      { k: 'boom', t: T2, dur: HK - T2, txt: 'DISTRUGE TURBINA', y: 300, size: 122, col: '#F39237', from: 3.6, sh: 26, ca: 26, riser: false, bg: .7, cg: .35, glow: 'rgba(243,146,55,.55)' },
      { k: 'boom', t: T3, dur: HK - T3, txt: 'SAU MOTORUL!', y: 460, size: 128, col: '#FF4B3E', from: 3.0, sh: 18, ca: 22, riser: false, bg: .5, cg: .3, glow: 'rgba(255,75,62,.5)' },
      { k: 'stamp', t: aw(9, 'distruge') - .03, t1: aw(10, 'Dar') - .2, y: 1150, txt: 'MOTOR DISTRUS', col: 'red', s: .8 },
      { k: 'stamp', t: aw(13, 'avarie') - .03, t1: aw(14, 'De') - .2, y: 1150, txt: 'AVARIE', col: 'red', s: .85 },
      { k: 'stamp', t: aw(14, 'curățarea') - .03, t1: aw(15, 'Fără') - .2, y: 1150, txt: 'CURĂȚATĂ LA TIMP', col: 'green', s: .8 },
    ],
    fx: [
      { k: 'punch', t: T1, a: .08, sh: 14 },
      { k: 'punch', t: T2, a: .16, sh: 34 }, { k: 'glitch', t: T2, d: .16 }, { k: 'flash', t: T2 - .11, a: .75 },
      { k: 'shock', t: T2 + .01, x: 540, y: 820, r: 700, n: 2, col: '#F39237', col2: '#FF4B3E' },
      { k: 'punch', t: T3, a: .1, sh: 20 }, { k: 'glitch', t: T3, d: .12 },
    ],
    bgFix: [[0, SEND]],
    tags: {
      0: { admisia: 'c', depuneri: 'r', distruge: 'r', turbina: 'c', motorul: 'c' }, 1: { traseul: 'y' },
      2: { motorul: 'c' }, 3: { turbina: 'c', compresorul: 'c', presiune: 'y' }, 4: { egr: 'c', gazele: 'c', admisie: 'c' },
      5: { galeria: 'c', admisie: 'c', bmw: 'y', n47: 'y', canal: 'c' }, 6: { emisiile: 'g', funingine: 'r' },
      7: { funinginea: 'r', ulei: 'r', crusta: 'r', neagra: 'r', tare: 'r', infunda: 'r' }, 8: { desprinde: 'r' },
      9: { extreme: 'r', cilindru: 'c', piston: 'c', chiulasa: 'c', distruge: 'r' }, 10: { mici: 'y', viteza: 'r', turbina: 'c' },
      11: { paletele: 'c', geometriei: 'c', variabile: 'c', presiunea: 'y' }, 12: { calamina: 'r', caldura: 'r', lovesc: 'r', intepenesc: 'r' },
      13: { blocheaza: 'r', avarie: 'r' }, 14: { curatarea: 'g', timp: 'g', importanta: 'g' }, 15: { liber: 'g', corect: 'g' },
    },
  };
};
