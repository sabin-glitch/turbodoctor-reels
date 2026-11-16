// „Eroarea P2002: ce înseamnă de cele mai multe ori pe 2.0 Euro 6 din gama VAG” — reel animat 3D (filmul Blender „Eroarea de eficiență DPF la EA288”,
// remontat pe voce) cu vocea lui Sabin (ElevenLabs), 15.11.2026
// Hook cerut de Sabin: „Eroarea P2002, eficiență. Ce înseamnă de cele mai multe ori pe motoarele 2.0 Euro 6 de pe gama VAG.” -> titluri boom pe cuvintele lui,
// în două faze (eroarea, apoi întrebarea), peste motorul care se rotește; apoi răspunsul și explicația.
// Cadrele (frames_base) vin din tools/anim_p2002: fiecare plan al filmului e legat de cuvintele vocii (reel_story.py), cu titlurile, etichetele și widgetul
// „calculat / măsurat” desenate în cadre. Aici sunt doar titlurile din hook, culorile din subtitrări și cardul de final.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const B1 = .12, P = aw(0, 'P2002') - .03, EF = aw(0, 'eficiență') - .03, FP = aw(0, 'filtru') - .03;
  const Q = aw(0, 'Ce') - .03, M = aw(0, 'de', 1) - .03, V = aw(0, '2.0') - .03, G = aw(0, 'gama') - .03;
  const HE = ew(0, 'VAG') + .22;                    // titlurile ies; motorul se apropie pentru răspuns
  const HK = aw(1, 'De') - .12;                     // de aici încep subtitrările
  const QA = Q - .03;                               // faza 1 iese chiar înainte de întrebare
  const RED = '#FF3B30', YEL = '#FFD21F', WH = '#FFFFFF';
  const b = (t, t1, txt, y, size, col, o = {}) => ({ k: 'boom', t, dur: t1 - t, txt, y, size, col, riser: false, from: 3.0, sh: 14, ca: 18, ...o });
  return {
    hideCap: [[0, HK - .05]],
    items: [
      // ---- faza 1: eroarea
      b(B1, QA, 'EROAREA', 385, 140, WH, { from: 2.4, sh: 12, ca: 14, glow: 'rgba(98,216,255,.45)' }),
      b(P, QA, 'P2002', 606, 290, RED, { from: 3.8, sh: 26, ca: 30, glow: 'rgba(255,59,48,.6)' }),
      b(EF, QA, 'EFICIENȚĂ', 826, 132, YEL, { from: 3.2, sh: 18, ca: 22 }),
      b(FP, QA, 'FILTRU DE PARTICULE', 940, 80, WH, { from: 2.4, sh: 10, ca: 12, glow: 'rgba(98,216,255,.45)' }),
      // ---- faza 2: întrebarea (rămâne până la răspuns; ultimul cadru complet e coperta)
      b(Q, HE, `EROAREA <span style="color:${RED}">P2002</span>`, 350, 100, WH, { from: 1.7, sh: 8, ca: 10, glow: 'rgba(255,59,48,.45)' }),
      b(Q + .03, HE, 'CE ÎNSEAMNĂ', 480, 136, WH, { from: 3.4, sh: 20, ca: 24, glow: 'rgba(98,216,255,.5)' }),
      b(M, HE, 'DE CELE MAI', 622, 136, YEL, { from: 3.6, sh: 22, ca: 26 }),
      b(M + .34, HE, 'MULTE ORI?', 764, 136, YEL, { from: 3.2, sh: 18, ca: 22 }),
      b(V, HE, '2.0 EURO 6', 895, 86, WH, { x: 287, from: 2.8, sh: 12, ca: 14, glow: 'rgba(98,216,255,.5)' }),
      b(G, HE, 'GAMA VAG', 869, 86, WH, { x: 784, from: 2.8, sh: 12, ca: 14, glow: 'rgba(98,216,255,.5)' }),
    ],
    fx: [
      { k: 'flash', t: P - .11, a: .75 }, { k: 'shock', t: P + .01, x: 540, y: 606, r: 760, n: 2, col: RED, col2: YEL },
      { k: 'flash', t: EF - .11, a: .4 },
      { k: 'flash', t: Q - .1, a: .5 },
      { k: 'flash', t: M - .11, a: .5 }, { k: 'shock', t: M + .01, x: 540, y: 690, r: 620, n: 1, col: YEL },
      { k: 'flash', t: V - .1, a: .3 }, { k: 'flash', t: G - .1, a: .25 },
      { k: 'flash', t: HE - .12, a: .4 },                  // fără glitch: pe fundalul închis al animației, fâșiile lui ies ca niște dreptunghiuri negre
    ],
    bgFix: [[0, SEND]],
    tags: {
      0: { p2002: 'r', eficienta: 'y', multe: 'y', ori: 'y', euro: 'c', vag: 'c' },
      1: { multe: 'y', ori: 'y', filtrul: 'c', nimic: 'g', problema: 'r', egr: 'r', racitorul: 'r', gaze: 'r' },
      2: { gazele: 'y', motor: 'c', turbina: 'c', catalizator: 'c', filtrul: 'c', particule: 'c' },
      3: { filtru: 'c', parte: 'y', intoarce: 'y', admisie: 'c', racitorul: 'c', gaze: 'c', supapa: 'c', egr: 'c' },
      4: { filtru: 'c', gazele: 'y', trec: 'g', peretii: 'c', porosi: 'c', funinginea: 'r', ramane: 'r', canale: 'c' },
      5: { calculatorul: 'c', nu: 'r', vede: 'r', masoara: 'y', presiunea: 'y', inainte: 'c', dupa: 'c' },
      6: { calculeaza: 'c', funingine: 'y', masoara: 'y', mult: 'r', putin: 'r', filtrul: 'c', retine: 'r', eroarea: 'r' },
      7: { des: 'y', racitorul: 'r', gaze: 'r', infunda: 'r', depuneri: 'r', putine: 'y', calculatorul: 'c' },
      8: { presiunea: 'y', filtru: 'c', mica: 'r', asteptata: 'c', eroarea: 'r', filtrul: 'c', bun: 'g' },
      9: { racitorul: 'c', fisurat: 'r', pierde: 'r', antigel: 'y', nicio: 'y', pata: 'y' },
      10: { doua: 'y', cauza: 'y', supapa: 'r', egr: 'r', intepenita: 'r', depuneri: 'r', deschide: 'r', acelasi: 'y' },
      11: { eroare: 'r', furtunas: 'c', crapat: 'r', infundat: 'r', senzorul: 'c', presiune: 'c', aerul: 'c', pierdut: 'r', admisie: 'c', debitmetru: 'c', gresit: 'r' },
      12: { filtrul: 'c', chiar: 'y', suferit: 'r', injector: 'c', picura: 'r', multa: 'r', funingine: 'r', calcul: 'c' },
      13: { filtrul: 'c', regenereaza: 'y', des: 'y', fierbinte: 'r', crapa: 'r', nou: 'y', fel: 'r' },
      14: { uleiul: 'y', segmenti: 'c', axul: 'c', turbinei: 'c', arde: 'r', cenusa: 'r', iese: 'r', filtru: 'c', regenerare: 'y' },
      15: { inainte: 'y', schimbi: 'y', filtrul: 'c', cauta: 'g', cauza: 'g', eroarea: 'r', filtru: 'c', diagnoza: 'g' },
    },
  };
};
