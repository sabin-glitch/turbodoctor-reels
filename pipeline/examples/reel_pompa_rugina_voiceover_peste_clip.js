// v2 – Reel „Pompa nu bagă motorină? Am desfăcut-o: rugină” (IMG_7264, un singur clip de 29,3 s, fără tăieturi, ritm natural)
// Cerut de Sabin pe 28.11.2026: „videoclipuri captivante cu hook puternic”, cu voice-over făcut cu vocea lui (ElevenLabs „Sabin”), ca să iasă profi.
// În clip se aude o singură frază, la început: „Clientul nostru susține că mașina nu a mai pornit și pompa nu bagă motorină.” Restul e filmat fără voce:
// pompa de înaltă presiune desfăcută, cu rugină în carcasă, pe rotor, pe regulator și pe arcul unui element de pompare.
// Hook: fraza lui, cu vocea lui din clip (curățată cu denoise_bench.py); titluri boom în două etape: sus „CLIENTUL SUSȚINE: / NU A MAI PORNIT!”
// (înaintea vocii, cu un impact mic din nou pe „pornit”), jos „POMPA NU BAGĂ / MOTORINĂ!” pe cuvintele lui, peste capacul neclar din prim-plan.
// După hook: voice-over (tools/vo_clip/build_vo_clip.py, vo_script.json), 5 rânduri puse pe ce se vede. Textul e al meu, de confirmat cu Sabin:
// „Am desfăcut pompa de înaltă presiune. Și uite ce am găsit. / Rugină. Pe fiecare piesă din interior. / O pompă care lucrează în motorină n-are cum să
// ruginească. / Decât într-un singur caz: când în motorină ajunge apă. / Motorina unge pompa. Apa o distruge.”
// Sunetul clipului rămâne doar pe fraza de hook (după ea se aude un radio în atelier). out/v2.json: {"narrator": true, "orig_gain": 1.0, "orig_duck": 0.0}. Coperta: out/cover_t.json {"t": 7.0}.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    pornit: aw(0, 'pornit'), pompa0: aw(0, 'pompa'), motorina0: aw(0, 'motorină'),
    am: aw(1, 'Am'), uite: aw(1, 'uite'),
    rugina: aw(2, 'Rugină'), pe2: aw(2, 'Pe'), interiorE: ew(2, 'interior'),
    o3: aw(3, 'O'), nare: aw(3, 'n-are'), rugineascaE: ew(3, 'ruginească'),
    decat: aw(4, 'Decât'), cand: aw(4, 'când'), apa4: aw(4, 'apă'),
    motorina5: aw(5, 'Motorina'), apa5: aw(5, 'Apa'), distruge: aw(5, 'distruge'),
  };
  // HOOK: sus, două rânduri înaintea vocii (ea pornește la 1,14 s); jos, două rânduri pe cuvintele lui („pompa”, „motorină”)
  const B1 = .12, B2 = .80, HA = 5.12, B3 = A.pompa0 - .03, B4 = A.motorina0 - .02, HB = 7.32;
  const Y1 = 290, Y2 = 452, Y3 = 1172, Y4 = 1356;
  const LOCK = 8.95;   // scanarea arcului ruginit, în prim-plan
  return {
    hook: { tag: 'ANALIZĂ TEHNICĂ · CAZ #7264', end: HB, y: -76 },
    hideCap: [[0, HB - .05]],
    stages: [[HB + .1, 'SIMPTOME'], [A.am + .5, 'INVESTIGAȚIE'], [A.decat - .05, 'CAUZA']],
    tags: { 1: { pompa: 'c', inalta: 'c', presiune: 'c', gasit: 'y' }, 2: { rugina: 'r', piesa: 'c' }, 3: { pompa: 'c', motorina: 'c', rugineasca: 'r' },
      4: { singur: 'y', motorina: 'c', apa: 'r' }, 5: { motorina: 'c', unge: 'g', pompa: 'c', apa: 'r', distruge: 'r' } },
    items: [
      // ---- hook: boom în două etape
      { k: 'boom', t: B1, dur: HA - B1, txt: 'CLIENTUL SUSȚINE:', y: Y1, size: 106, col: '#FFFFFF', from: 2.6, sh: 14, ca: 16, riser: false, bg: .6, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HA - B2, txt: 'NU A MAI PORNIT!', y: Y2, size: 150, col: '#FF4B4B', from: 3.8, sh: 26, ca: 30, bg: 1, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'POMPA NU BAGĂ', y: Y3, size: 128, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .45, cg: .15, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'MOTORINĂ!', y: Y4, size: 182, col: '#FFD21F', from: 3.4, sh: 22, ca: 26, riser: false, bg: .55, cg: .15 },
      // ---- prim-planul: scanarea arcului ruginit de pe elementul de pompare
      { k: 'scan', t0: HB + .18, t1: 9.5, track: 'track_spring', box: [0, 4, 450, 330], lab: 'ANALIZĂ INTERIOR POMPĂ...', lab2: 'DEFECT DETECTAT', at2: LOCK },
      // ---- „Rugină.”
      { k: 'kin', t: A.rugina - .02, dur: 1.05, txt: 'RUGINĂ', col: '#FF4B4B', x: 792, y: 352, size: 168, rot: -4 },
      { k: 'call', t0: 12.72, t1: 13.72, track: 'track_rotor', p: [455, 780], lab: [612, 468], h: 'ROTOR', v: 'RUGINĂ PE CANELURI', col: 'red', cps: 44 },
      // ---- fișa pacientului, cât mută capacul și ia regulatorul
      { k: 'file', t0: A.o3 - .12, t1: A.rugineascaE + .12, top: 268, no: '7264', ecg: 'crit',
        rows: [[A.o3, 'PACIENT', 'POMPĂ DE ÎNALTĂ PRESIUNE', 'c', 'fuel_pump'], [A.o3 + .55, 'SIMPTOME', 'MAȘINA NU MAI PORNEȘTE', 'r', 'warning'],
          [A.nare - .1, 'ANALIZE', 'RUGINĂ ÎN INTERIOR', 'r', 'microscope']], stamp: [A.nare + .55, 'GRAV', 'red'] },
      // ---- regulatorul, cu vârful ruginit
      { k: 'call', t0: 20.72, t1: A.apa4 - .3, track: 'track_reg', p: [650, 1000], lab: [468, 462], h: 'REGULATOR', v: 'RUGINIT', col: 'red', cps: 40 },
      // ---- cauza
      { k: 'stamp', t: A.apa4 - .03, t1: 24.95, x: 540, y: 352, txt: 'APĂ ÎN MOTORINĂ', col: 'blue', s: .84, rot: -5 },
      // ---- de ce: ungerea pompei
      { k: 'schem', t0: A.motorina5 - .15, t1: SEND - .12, top: 268, type: 'pumpLube', title: 'SCHEMĂ · ELEMENTUL DE POMPARE', sub: 'POMPA DE ÎNALTĂ PRESIUNE', stepNames: ['UNGEREA', 'APA'],
        P: { heads: { water: ['APĂ ÎN MOTORINĂ: RUGINĂ', '#FF4B4B'] } },
        steps: [[A.motorina5 - .15, 'Pistonul pompei lucrează într-un film de motorină', 'g', 'ok'], [A.apa5 - .06, 'Apa strică ungerea și ruginește piesele', 'r', 'water']] },
    ],
    fx: [
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: Y2, r: 760, n: 2, col: '#FF4B4B' },
      { k: 'punch', t: A.pornit, a: .05, sh: 8 },
      { k: 'punch', t: B3, a: .07, sh: 12 },
      { k: 'flash', t: B4 - .11, a: .55 }, { k: 'punch', t: B4, a: .13, sh: 26 }, { k: 'shock', t: B4 + .01, x: 540, y: Y4, r: 700, n: 2, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 },
      { k: 'punch', t: LOCK, a: .06, sh: 8 },
      { k: 'flash', t: A.rugina - .1, a: .4 }, { k: 'punch', t: A.rugina, a: .1, sh: 18 },
      { k: 'glitch', t: A.o3 - .2, d: .1 },
      { k: 'flash', t: A.apa4 - .1, a: .3 }, { k: 'punch', t: A.apa4, a: .09, sh: 14 },
      { k: 'punch', t: A.apa5, a: .06, sh: 10 },
    ],
    sfx: [[HB - .1, 'whoosh', .6]],
    bursts: [[B2 + .04, 540, Y2, 6, 480, 1.3]],
  };
};
