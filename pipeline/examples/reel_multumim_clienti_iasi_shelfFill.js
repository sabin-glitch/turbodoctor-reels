// v2 – Reel „Vă mulțumesc că mă chinuiți în două moduri” – Turbo Doctor Iași, mulțumire către clienți (18.11.2026)
// 5 clipuri lipite în ordinea filmării, fără tăieturi, ritm natural:
//   0 IMG_2575 (selfie afară, parcarea) · 20.37 IMG_2576 (rafturi cu turbine) · 29.94 IMG_2578 (tăvi cu injectoare)
//   · 37.43 IMG_2579 (DPF-uri, admisii) · 46.09 IMG_2580 (selfie în hală, mulțumirile)
// Hook cerut de Sabin: „puternic, despre cele două lucruri prin care mă chinuiți și îmi plac, cum spun în video, apoi încep prezentarea”:
// titlu boom în patru trepte din primele cadre: sus „VĂ MULȚUMESC CĂ / MĂ CHINUIȚI”, jos (sub bărbie) „ÎN DOUĂ MODURI / …ȘI-MI PLACE!”;
// rândurile își repetă impactul când el rostește aceleași cuvinte („mulțumesc”, „chinuiți”, „două moduri”).
// Selfie de aproape: subtitrările coborâte sub bărbie (capTop), chip-urile deasupra capului; pe B-roll schema nouă `shelfFill` (rafturile se umplu pe ce enumeră).
// Fără CTA pe imagine (25.10); „diagnoza e mereu gratuită” o spune el: doar subtitrări + chip. Se termină pe selfie -> fără Rețetă.
// out/v2.json: {"cuts": false, "speed": 1.0, "music_gain": 0.5} · out/cover_t.json: {"t": 4.70} · cuvintele: tools/words/snap_words.py
// Aprobat de Sabin pe 18.11.2026 și programat în aceeași zi pe brandul Turbo Doctor: YouTube 13:00, Facebook 16:00, TikTok 19:00, Instagram 21:00.
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    turbo0: aw(0, 'Turbo'), iasi0: aw(0, 'Iași!'), in0: aw(0, 'În'), multumesc0: aw(0, 'mulțumesc'), chinuiti0: aw(0, 'chinuiți'), doua0: aw(0, 'două'), moduriE: ew(0, 'moduri.'),
    unu1: aw(1, 'Unu.'), nu1: aw(1, 'Nu'), parchez1: aw(1, 'parchez'), deoarece1: aw(1, 'deoarece'), plina1: aw(1, 'plină'), masinile1: aw(1, 'mașinile'),
    si2: aw(2, 'Și'), doi2: aw(2, 'doi,'), pentru2: aw(2, 'pentru'), investitii2: aw(2, 'investiții'), multe2: aw(2, 'multe'), rafturi2: aw(2, 'rafturi,'),
    ca3: aw(3, 'că'), pline3: aw(3, 'pline'), de3: aw(3, 'de'), turbinele3: aw(3, 'turbinele'), injectoarele3: aw(3, 'injectoarele'), pompele3: aw(3, 'pompele'),
    sistemele3: aw(3, 'sistemele'), pilitura3: aw(3, 'pilitură,'),
    dpf4: aw(4, 'DPF-urile,'), catalizatoarele4: aw(4, 'catalizatoarele,'), sistemele4: aw(4, 'sistemele'), pe4: aw(4, 'pe'), curatare4: aw(4, 'curățare'),
    va5: aw(5, 'Vă'), continuati5: aw(5, 'continuați'), abuz5: aw(5, 'abuz'), pentru5: aw(5, 'pentru'),
    va6: aw(6, 'Vă'), cei6: aw(6, 'cei'), si6: aw(6, 'și'), la6: aw(6, 'la', 1), si6b: aw(6, 'Și', 1), faceti6: aw(6, 'faceți'), povestea6: aw(6, 'povestea'),
    sa6: aw(6, 'să', 1), mai6: aw(6, 'mai', 1),
    va7: aw(7, 'Vă'), diagnoza7: aw(7, 'diagnoza'), pentru7: aw(7, 'pentru'),
  };
  const CLIP = [0, 20.37, 29.94, 37.43, 46.09];
  // HOOK: patru trepte; impactul mare pe primul cuvânt („Bună” .44), apoi „Turbo” 1.54 și „Iași” 2.16 (anvelopa vocii).
  const B1 = .12, B2 = .44, B3 = 1.54, B4 = 2.16, HB = A.moduriE + .38;
  const Y1 = 244, Y2 = 426, Y3 = 1548, Y4 = 1690;
  const BAND_END = CLIP[4] - .06;
  return {
    hook: { tag: 'TURBO DOCTOR IAȘI · MULȚUMIRI', y: -84, end: HB },
    capTop: 1400,
    hideCap: [[0, A.unu1 - .2]],
    tags: {
      0: { turbo: 'g', doctor: 'g', iasi: 'c', multumesc: 'g', chinuiti: 'r', doua: 'y', moduri: 'y' },
      1: { unu: 'y', parchez: 'r', aproape: 'r', parcarea: 'r', plina: 'r', masinile: 'c', clientilor: 'g' },
      2: { doi: 'y', investitii: 'y', rafturi: 'c' },
      3: { pline: 'r', turbinele: 'c', injectoarele: 'c', pompele: 'c', injectie: 'c', pilitura: 'r' },
      4: { dpfurile: 'c', catalizatoarele: 'c', admisie: 'c', curatare: 'g', profesionala: 'g' },
      5: { continuati: 'r', abuz: 'r', turbo: 'g', doctor: 'g' },
      6: { multumim: 'g', profesionale: 'g', compromis: 'g', preturi: 'y', corecte: 'y', turbo: 'g', doctor: 'g', profesionalism: 'g', garantie: 'y' },
      7: { multumim: 'g', diagnoza: 'g', gratuita: 'g', problema: 'c' },
    },
    items: [
      // ---- hook: boom în patru trepte (fără scântei pe titluri: cadru curat pentru copertă)
      { k: 'boom', t: B1, dur: HB - B1, txt: 'VĂ MULȚUMESC CĂ', y: Y1, size: 96, col: '#FFFFFF', from: 2.4, sh: 10, ca: 12, riser: false, bg: .5, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'MĂ CHINUIȚI', y: Y2, size: 156, col: '#FF3B30', from: 3.8, sh: 26, ca: 30, bg: .8, glow: 'rgba(255,75,75,.6)' },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'ÎN DOUĂ MODURI', y: Y3, size: 122, col: '#FFD21F', from: 2.8, sh: 14, ca: 18, riser: false, bg: .45, cg: .3 },
      { k: 'boom', t: B4, dur: HB - B4, txt: '…ȘI-MI PLACE!', y: Y4, size: 112, col: '#4ADE80', from: 2.8, sh: 14, ca: 18, riser: false, bg: .45, cg: .3, glow: 'rgba(74,222,128,.55)' },

      // ---- MODUL 1: parcarea plină (selfie afară: chip-uri deasupra capului)
      { k: 'band', t0: A.unu1 - .1, t1: BAND_END, y: 214, w: 980, h: 76, kicker: 'CUM NE CHINUIȚI',
        ph: [[A.unu1 - .1, 'MODUL 1 · PARCAREA PLINĂ', '1 / 2'], [A.si2 - .05, 'MODUL 2 · RAFTURILE PLINE', '2 / 2']] },
      { k: 'chip', t0: A.nu1 - .08, t1: CLIP[1] - .1, y: 330, ph: [[A.nu1 - .08, 'cross_mark', 'NU-MI DAȚI VOIE SĂ PARCHEZ APROAPE', 'red'],
        [A.deoarece1 - .05, 'automobile', 'PARCAREA E PLINĂ...', 'yellow'], [A.masinile1 - .05, 'check_mark_button', '...DE MAȘINILE CLIENȚILOR NOȘTRI', 'green']] },
      { k: 'stk', t0: A.plina1 - .05, t1: CLIP[1] - .15, ico: 'automobile', x: 938, y: 600, size: 128, rot: 6 },

      // ---- MODUL 2: rafturile (B-roll fără față: schema sus, kin și ștampile pe mijloc)
      { k: 'kin', t: A.si2 - .02, dur: 1.15, txt: 'MODUL #2', col: '#FFD21F', y: 900, size: 170, rot: -4 },
      { k: 'schem', t0: A.pentru2 - .08, t1: CLIP[4] - .08, top: 268, h: 360, type: 'shelfFill', title: 'RAFTURILE TURBO DOCTOR', sub: 'IAȘI · INVENTAR',
        P: { racks: [A.pentru2 - .1, A.investitii2 + .02, A.multe2 - .02],
          items: [[A.de3 - .1, 'turbo', 7], [A.injectoarele3 - .05, 'injector', 5], [A.pompele3 - .05, 'pump', 3], [A.sistemele3 - .05, 'rail', 3],
            [A.dpf4 - .05, 'dpf', 4], [A.catalizatoarele4 - .05, 'cat', 3], [A.sistemele4 - .05, 'intake', 2]],
          pil: A.pilitura3 - .02, clean: A.curatare4 - .02 },
        stepNames: ['INVESTIȚIA', 'RAFTURI NOI', 'PLINE DE...', 'PLINE DE...', 'PILITURĂ', 'PLINE DE...', 'CURĂȚARE'],
        steps: [[A.pentru2 - .08, 'Ne puneți la investiții...', ''], [A.multe2 - .05, '...în cât mai multe rafturi!', 'y'], [A.ca3 - .05, 'Pline de turbinele voastre', ''],
          [A.injectoarele3 - .05, 'Injectoarele și pompele voastre', ''], [A.sistemele3 - .05, 'Sisteme de injecție care au generat pilitură', 'r'],
          [A.dpf4 - .05, 'DPF-uri, catalizatoare, sisteme de admisie', ''], [A.pe4 - .05, 'Aduse la noi pentru curățare profesională', 'g']],
        sfx: [[A.investitii2 + .05, 'lock', .5], [A.multe2, 'lock', .5], [A.pilitura3, 'impact', .45]] },
      { k: 'stamp', t: A.pline3 - .03, t1: A.turbinele3 + .6, txt: 'PLINE!', y: 1010, col: 'red', s: .95, rot: -8 },
      { k: 'kin', t: A.pilitura3 - .03, dur: 1.25, txt: 'PILITURĂ!', col: '#FF3B30', y: 1010, size: 150, rot: -4 },
      { k: 'stamp', t: A.curatare4 - .03, t1: CLIP[4] - .15, txt: 'CURĂȚARE PROFESIONALĂ', y: 1010, col: 'green', s: .66, rot: -6 },

      // ---- mulțumirile (selfie în hală, de aproape: chip-urile sus, la y 236)
      { k: 'chip', t0: A.va5 - .08, t1: A.va6 - .3, y: 236, ph: [[A.va5 - .08, 'folded_hands', 'VĂ RUGĂM FRUMOS...', 'blue'], [A.continuati5 - .05, 'fire', 'CONTINUAȚI ACEST ABUZ!', 'red'],
        [A.pentru5 - .05, 'round_pushpin', 'ÎN TOATE LOCAȚIILE TURBO DOCTOR', 'blue']] },
      { k: 'chip', t0: A.va6 - .05, t1: A.si6b - .3, y: 236, ph: [[A.va6 - .05, 'handshake', 'VĂ MULȚUMIM, CLIENȚILOR!', 'green'], [A.cei6 - .05, 'wrench', 'CARE APELAȚI LA SERVICIILE NOASTRE', 'blue'],
        [A.si6 - .05, 'shield', 'REPARAȚII FĂRĂ COMPROMIS', 'green'], [A.la6 - .05, 'money_bag', 'LA PREȚURI CORECTE', 'yellow']] },
      { k: 'chip', t0: A.si6b - .05, t1: A.va7 - .3, y: 236, ph: [[A.si6b - .05, 'handshake', 'VĂ MULȚUMIM!', 'green'], [A.faceti6 - .05, 'calendar', 'CĂ ÎN FIECARE ZI...', 'blue'],
        [A.povestea6 - .05, 'rocket', 'POVESTEA TURBO DOCTOR MERGE MAI DEPARTE', 'green'], [A.sa6 - .05, 'hammer_and_wrench', 'PROFESIONALISM ÎN REPARAȚII', 'blue'],
        [A.mai6 - .05, 'shield', 'ȘI MULȚI ANI DUPĂ GARANȚIE', 'yellow']] },
      { k: 'chip', t0: A.va7 - .05, t1: SEND - .15, y: 236, ph: [[A.va7 - .05, 'folded_hands', 'VĂ MULȚUMIM!', 'green'], [A.diagnoza7 - .08, 'stethoscope', 'LA NOI, DIAGNOZA E MEREU GRATUITĂ', 'green'],
        [A.pentru7 - .05, 'magnifying_glass_tilted_left', 'PENTRU A DETERMINA PROBLEMA', 'blue']] },
    ],
    fx: [
      // hook: patru impacturi (al doilea = cel mare), apoi rândurile „bat” din nou pe cuvintele rostite
      { k: 'flash', t: B1 - .08, a: .35 }, { k: 'punch', t: B1, a: .07, sh: 14 },
      { k: 'flash', t: B2 - .11, a: .75 }, { k: 'punch', t: B2, a: .16, sh: 34 }, { k: 'glitch', t: B2, d: .2 }, { k: 'shock', t: B2 + .01, x: 540, y: Y2, r: 720, n: 2, col: '#FF4B4B' },
      { k: 'flash', t: B3 - .11, a: .4 }, { k: 'punch', t: B3, a: .08, sh: 16 },
      { k: 'flash', t: B4 - .11, a: .4 }, { k: 'punch', t: B4, a: .08, sh: 16 }, { k: 'shock', t: B4 + .01, x: 540, y: Y4, r: 520, n: 1, col: '#4ADE80' },
      { k: 'punch', t: A.multumesc0 + .02, a: .05, sh: 8 },
      { k: 'flash', t: A.chinuiti0 - .1, a: .3 }, { k: 'punch', t: A.chinuiti0, a: .1, sh: 20 }, { k: 'shock', t: A.chinuiti0 + .01, x: 540, y: Y2, r: 560, n: 1, col: '#FF4B4B' },
      { k: 'punch', t: A.doua0 + .06, a: .07, sh: 14 }, { k: 'shock', t: A.doua0 + .07, x: 540, y: Y3, r: 520, n: 1, col: '#FFD21F' },
      { k: 'glitch', t: HB - .05, d: .14 },
      // trecerile dintre clipuri
      { k: 'glitch', t: CLIP[1] - .04, d: .12 }, { k: 'glitch', t: CLIP[2] - .04, d: .12 }, { k: 'glitch', t: CLIP[3] - .04, d: .12 }, { k: 'glitch', t: CLIP[4] - .04, d: .14 },
      { k: 'punch', t: A.si2, a: .06, sh: 12 }, { k: 'punch', t: A.pline3, a: .06, sh: 10 },
      { k: 'flash', t: A.pilitura3 - .12, a: .3 }, { k: 'punch', t: A.pilitura3, a: .08, sh: 14 },
      { k: 'punch', t: A.curatare4, a: .05 }, { k: 'punch', t: A.abuz5, a: .05, sh: 8 },
    ],
    sfx: [[HB - .1, 'whoosh', .6], [A.curatare4 + .05, 'shimmer', .45], [A.va6 + .1, 'shimmer', .3]],
    bursts: [[A.pilitura3 + .02, 540, 1010, 6, 300, .9]],
  };
};
