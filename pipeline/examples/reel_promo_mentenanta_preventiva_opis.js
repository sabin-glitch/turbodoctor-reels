// v2 – PROMO plătit (28.10.2026): „Mentenanța preventivă: ce fac și eu la mașinile mele” – ulei, admisie, DPF, EGR, injectoare
// 7 clipuri lipite în ordinea filmării, fără tăieturi: 0 IMG_1901 (motor) · 11.41 IMG_1902 (selfie) · 20.35 IMG_1903 (chiulasă cu depuneri) ·
// 27.02 IMG_1907 (galeria de admisie) · 53.43 IMG_1908 (admisie + DPF) · 78.68 IMG_1911 (EGR, injectoare) · 118.92 IMG_1914 (selfie, oferta)
// Cerut de Sabin: la final un opis cu lucrările recomandate + telefonul + locațiile, toate pe același ecran (endCard: false + piesa opis).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND, TOTAL }) => {
  const A = {
    turbina: aw(0, 'turbina'), motorul0: aw(0, 'motorul'), dpful0: aw(0, 'DPF-ul'), defectiunile: aw(0, 'defecțiunile'),
    ei: aw(1, 'Ei'), dau: aw(1, 'dau'), fac: aw(1, 'fac'), fiecare1: aw(1, 'fiecare'), daca1: aw(1, 'Dacă'), nu1: aw(1, 'nu'), in1: aw(1, 'în'),
    schimbul: aw(1, 'schimbul'), k1015: aw(1, '10-15.000'), k30: aw(1, '30.000'), nuLa: aw(1, 'nu', 1),
    dupa: aw(2, 'După'), curatarea2: aw(2, 'curățarea'), curatarea2b: aw(2, 'curățarea', 1), simpla: aw(2, 'simplă'), cost: aw(2, 'cost'),
    defectiuni3: aw(3, 'defecțiuni'), functioneaza: aw(3, 'funcționează'),
    odata: aw(4, 'Odată'), dpful4: aw(4, 'DPF-ul'), daca4: aw(4, 'dacă'), fiecare4: aw(4, 'fiecare'), o4: aw(4, 'o'), ce4: aw(4, 'ce'), duce: aw(4, 'duce'),
    si5: aw(5, 'și'),
    alaturi: aw(6, 'Alături'), curatarea6: aw(6, 'curățarea'), egr: aw(6, 'EGR-ului'), dar6: aw(6, 'Dar'), curatarea6b: aw(6, 'curățarea', 1), si6: aw(6, 'Și', 2),
    injectoarele: aw(7, 'injectoarele'), jos: aw(7, 'jos'), saibele: aw(7, 'șaibele'), garniturile: aw(7, 'garniturile'), verificam: aw(7, 'verificăm'),
    daca8: aw(8, 'Dacă'), curatare8: aw(8, 'curățare'),
    recalibrare: aw(9, 'recalibrare'), l250: aw(9, '250'), minim: aw(9, 'minim'),
    acestea: aw(10, 'Acestea'), mii10: aw(10, 'mii'), pe10: aw(10, 'pe'), daca10: aw(10, 'dacă'),
    acum: aw(11, 'Acum'), comentarii11: aw(11, 'comentarii'),
    pentru12: aw(12, 'Pentru'), voi12b: aw(12, 'voi', 1), voi12c: aw(12, 'voi', 2), pe12: aw(12, 'Pe'), stati: aw(12, 'Stați'),
    pentru13: aw(13, 'Pentru'), va13: aw(13, 'vă'),
    va14: aw(14, 'Vă'), programa: aw(14, 'programa'), numarul: aw(14, 'numărul'), sau14: aw(14, 'sau'), diagnoza14: aw(14, 'diagnoză'), starea: aw(14, 'starea'),
    problemele14: aw(14, 'problemele'), stadiul: aw(14, 'stadiul'), decidem: aw(14, 'decidem'),
  };
  const CLIP = [0, 11.41, 20.35, 27.02, 53.43, 78.68, 118.92];
  const RT = TEND + .5, RS = .28;  // opis rows: start + spacing
  const OPIS = [
    [null, 'LA 10–15.000 KM'],
    ['oil_drum', 'Schimb de ulei (nu la 30.000)'],
    [null, 'LA FIECARE 100.000 KM'],
    ['dashing_away', 'Curățarea galeriei de admisie'],
    ['broom', 'Curățarea DPF-ului (scoate cenușa)'],
    ['bubbles', 'Curățarea EGR-ului și a răcitorului'],
    ['test_tube', 'Injectoare: șaibe, garnituri, verificare'],
  ].map((r, i) => [RT + i * RS, r[0], r[1]]);
  return {
    hook: { tag: 'ÎNTREBAREA DIN COMENTARII', l1: 'CUM PROTEJEZI', l1At: .3, end: 7.1 },
    hideCap: [[0, 7.05]],
    stages: [[A.schimbul - .05, 'ULEI'], [A.curatarea2 - .05, 'ADMISIE'], [A.dpful4 - .05, 'DPF'], [A.egr - .05, 'EGR'], [A.injectoarele - .05, 'INJECTOARE']],
    stageY: 205, cardTop: 262,
    tags: {
      0: { turbina: 'c', motorul: 'c', dpful: 'c', defectiunile: 'r', costisitoare: 'r' },
      1: { ulei: 'c', km: 'y', final: 'y' },
      2: { curatarea: 'g', galeriei: 'c', admisie: 'c', simpla: 'g', cost: 'y', scazut: 'g' },
      3: { catastrofale: 'r', curata: 'g', bun: 'g' },
      4: { curete: 'g', dpful: 'c', oras: 'y', cenusa: 'r', curatare: 'g', descarcarea: 'g', completa: 'g' },
      5: { eficienta: 'g' },
      6: { egrului: 'c', racitorului: 'c', impact: 'y', profund: 'y', dpfului: 'c', dpf: 'c', mentenanta: 'g', corecta: 'g', preventie: 'g' },
      7: { injectoarele: 'c', saibele: 'c', garniturile: 'c', profesional: 'g' },
      8: { curatare: 'g' },
      9: { recalibrare: 'g', reconditionare: 'r' },
      10: { salveaza: 'g', mii: 'r', euro: 'r' },
      11: { bani: 'y' },
      12: { defecte: 'r', incasam: 'y', grija: 'g' },
      13: { grija: 'g', preventiv: 'g' },
      14: { programa: 'g', telefon: 'y', ecran: 'y', diagnoza: 'g', gratuita: 'g', filtrului: 'c', impreuna: 'g' },
    },
    items: [
      // HOOK (IMG_1901, motorul secționat, fără față): întrebarea din comentarii + turbina / motorul / DPF-ul
      { k: 'kin', t: A.turbina - .02, dur: 7.15 - A.turbina, txt: 'TURBINA', col: '#62D8FF', y: 600, size: 150, rot: -4 },
      { k: 'kin', t: A.motorul0 - .02, dur: 7.15 - A.motorul0, txt: 'MOTORUL', col: '#62D8FF', y: 770, size: 150, rot: -4 },
      { k: 'kin', t: A.dpful0 - .02, dur: 7.15 - A.dpful0, txt: 'DPF-UL?', col: '#FFD21F', y: 940, size: 150, rot: -4 },
      { k: 'stamp', t: A.defectiunile - .03, t1: CLIP[1] - .2, y: 660, txt: 'DEFECȚIUNI COSTISITOARE', col: 'red', s: .78, rot: -7 },
      // IMG_1902 (selfie)
      { k: 'chip', t0: A.ei - .05, t1: CLIP[2] - .15, y: 300, ph: [[A.ei - .05, 'eyes', 'STAI PÂNĂ LA FINAL', 'yellow'], [A.dau - .05, 'speech_balloon', 'DAU DIN CASĂ', 'blue'],
        [A.fac - .05, 'wrench', 'CE FAC LA MAȘINILE MELE', 'blue'], [A.fiecare1 - .05, 'counter', 'LA FIECARE 100–150.000 KM', 'yellow']] },
      // IMG_1903: chiulasa plină de depuneri → schimbul de ulei
      { k: 'scan', t0: CLIP[2] + .12, t1: A.in1 + .1, box: [140, 470, 800, 1000], lab: 'SCANARE CHIULASĂ...', lab2: 'DEPUNERI DE ULEI', at2: A.nu1 - .02 },
      { k: 'cmp', t0: A.in1 + .25, t1: CLIP[3] - .5, w: 760, big: true, ico: 'oil_drum', title: 'SCHIMBUL DE ULEI (KM)', aCls: 'ok', bCls: 'bad',
        a: [A.k1015 - .05, 'check_mark_button', 'SCHIMB LA', '10–15.000'], b: [A.nuLa - .05, 'cross_mark', 'NU LA', '30.000'] },
      // IMG_1907: galeria de admisie
      { k: 'chip', t0: A.dupa - .05, t1: A.curatarea2 - .3, y: 300, ph: [[A.dupa - .05, 'calendar', 'APOI, LA FIECARE 100.000 KM', 'yellow']] },
      { k: 'def', t0: A.curatarea2 - .05, t1: A.simpla - 1.4, term: 'GALERIA DE ADMISIE', text: 'Duce aerul spre cilindri. La diesel se umple în timp cu depuneri de ulei și funingine.' },
      { k: 'list', t0: A.simpla - 1.15, t1: CLIP[4] - .25, ico: 'broom', title: 'CURĂȚAREA GALERIEI DE ADMISIE', w: 700, rows: [
        [A.simpla - .05, 'Operațiune destul de simplă'], [A.cost - .05, 'Cost relativ scăzut'], [A.defectiuni3 - .05, 'Scapi de defecțiuni la motor și turbină'],
        [A.functioneaza - .05, 'Diesel-ul merge mult mai bine']] },
      // IMG_1908: DPF-ul
      { k: 'chip', t0: A.odata - .05, t1: A.o4 - .35, y: 300, ph: [[A.odata - .05, 'broom', 'ODATĂ CU ADMISIA:', 'blue'], [A.dpful4 - .05, 'broom', 'CURĂȚAREA DPF-ULUI', 'green'],
        [A.daca4 - .05, 'automobile', 'MAI ALES DACĂ MERGI MULT ÎN ORAȘ', 'yellow'], [A.fiecare4 - .2, 'calendar', 'LA FIECARE 100.000 KM', 'yellow']] },
      { k: 'schem', t0: A.o4 - .05, t1: CLIP[5] - .25, type: 'dpfFlow', title: 'FILTRUL DE PARTICULE · SECȚIUNE', sub: 'CURĂȚARE PREVENTIVĂ',
        stepNames: ['CENUȘĂ', 'REGENERARE', 'CURĂȚARE', 'REZULTAT'],
        P: { modes: ['ash', 'regen', 'clean', 'flow'], labels: { ash: ['CENUȘA SE ADUNĂ ÎN FILTRU', '#C9CED4'], regen: ['REGENERAREA ARDE DOAR FUNINGINEA', '#FFD21F'],
          clean: ['CURĂȚARE: DPF COMPLET DESCĂRCAT', '#4ADE80'], flow: ['REGENERĂRI EFICIENTE', '#4ADE80'] } },
        steps: [[A.o4 - .05, 'Cenușa se adună în filtru', 'y', 0], [A.ce4, 'Regenerarea nu poate scoate cenușa', 'r', 1],
          [A.duce, 'Curățarea scoate toată cenușa', 'g', 2], [A.si5, 'Apoi regenerarea e eficientă', 'g', 3]] },
      // IMG_1911: EGR + răcitor, apoi injectoarele
      { k: 'chip', t0: A.alaturi - .05, t1: A.curatarea6 - .3, y: 300, ph: [[A.alaturi - .05, 'check_mark_button', 'ALĂTURI DE ADMISIE ȘI DPF', 'blue']] },
      { k: 'def', t0: A.curatarea6 - .05, t1: A.dar6 - .3, term: 'EGR + RĂCITORUL EGR', text: 'Trimit o parte din gazele de evacuare, răcite, înapoi în admisie. În timp se încarcă cu funingine.' },
      { k: 'chip', t0: A.dar6 - .05, t1: A.si6 - .3, y: 300, ph: [[A.dar6 - .05, 'rocket', 'CEL MAI MARE IMPACT:', 'green'], [A.curatarea6b - .05, 'broom', 'ADMISIA + DPF-UL', 'green']] },
      { k: 'chip', t0: A.si6 - .05, t1: A.injectoarele - .35, y: 300, ph: [[A.si6 - .05, 'stethoscope', 'MENTENANȚĂ CORECTĂ', 'blue']] },
      { k: 'pipe', t0: A.injectoarele - .1, t1: A.daca8 - .3, ico: 'test_tube', title: 'INJECTOARELE, ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.jos - .05, 'wrench', 'DEMONTARE'], [A.saibele - .05, 'nutbolt', 'ȘAIBE DE FOC<br>NOI'], [A.garniturile - .05, 'nutbolt', 'GARNITURI<br>NOI'], [A.verificam - .05, 'microscope', 'VERIFICARE<br>PROFESIONALĂ']] },
      { k: 'chip', t0: A.daca8 - .05, t1: A.l250 - .73, y: 300, ph: [[A.daca8 - .05, 'magnifying_glass_tilted_left', 'PROBLEMĂ PRINSĂ LA TIMP', 'green'], [A.curatare8 - .05, 'broom', 'CURĂȚARE + RECALIBRARE', 'green']] },
      { k: 'cmp', t0: A.l250 - .45, t1: CLIP[6] - .25, w: 760, big: true, ico: 'money_bag', title: 'COST PE INJECTOR', aCls: 'ok', bCls: 'bad',
        a: [A.l250 - .05, 'check_mark_button', 'PRINSĂ LA TIMP', '250 LEI'], b: [A.minim - .05, 'cross_mark', 'RECONDIȚIONARE', '500+ LEI'] },
      // IMG_1914 (selfie): ce te salvează, comentariul care sigur apare, oferta
      { k: 'chip', t0: A.acestea - .05, t1: A.mii10 - .75, y: 300, ph: [[A.acestea - .05, 'shield', 'OPERAȚIUNILE CARE TE SALVEAZĂ', 'green']] },
      { k: 'boom', t: A.mii10, dur: 2.75, txt: 'MII DE EURO', y: 312, size: 124, col: '#FF4B4B', from: 3.2, sh: 22, ca: 24, bg: .9, glow: 'rgba(255,75,75,.55)' },
      { k: 'chip', t0: A.mii10 + 2.85, t1: A.acum - .3, y: 300, ph: [[A.mii10 + 2.85, 'counter', 'LA 200–250.000 KM', 'yellow'], [A.daca10 - .05, 'warning', 'DACĂ NU LE FACI LA TIMP', 'red']] },
      { k: 'comment', t0: A.comentarii11 - .15, t1: A.pentru12 - .25, head: 'Comentariul care sigur o să apară:', text: 'Normal că tu faci asta și recomanzi, să faci bani!', y: 262, s: .88 },
      { k: 'chip', t0: A.pentru12 - .05, t1: A.pentru13 - .3, y: 300, ph: [[A.pentru12 - .05, 'person_raising_hand', 'PENTRU VOI:', 'blue'], [A.voi12b - .05, 'cross_mark', 'NU VENIȚI LA PREVENȚIE', 'red'],
        [A.voi12c - .05, 'collision', 'VENIȚI CU PIESELE DEFECTE', 'red'], [A.pe12 - .05, 'money_bag', 'NOI ÎNCASĂM MAI MULT', 'yellow'], [A.stati - .05, 'folded_hands', 'STAȚI FĂRĂ GRIJĂ', 'green']] },
      { k: 'chip', t0: A.pentru13 - .05, t1: A.programa - .45, y: 300, ph: [[A.pentru13 - .05, 'handshake', 'PENTRU CEI CARE AU GRIJĂ DE MAȘINĂ', 'green'], [A.va13 - .05, 'stethoscope', 'VĂ AȘTEPTĂM LA MENTENANȚĂ PREVENTIVĂ', 'green']] },
      { k: 'eq', t0: A.programa - .2, t1: A.diagnoza14 - .3, top: 258, ico: 'calendar', title: 'PROGRAMEAZĂ-TE', sub: 'MENTENANȚĂ PREVENTIVĂ',
        lines: [[A.programa + .1, 'turbodoctor.ro', 'c'], [A.numarul - .1, '0739 065 065', 'big y']] },
      { k: 'chip', t0: A.diagnoza14 - .05, t1: SEND - .15, y: 300, ph: [[A.diagnoza14 - .05, 'stethoscope', 'SAU VINO LA DIAGNOZĂ GRATUITĂ', 'green'], [A.starea - .05, 'magnifying_glass_tilted_left', 'VEDEM ÎNCĂRCAREA FILTRULUI', 'blue'],
        [A.problemele14 - .05, 'stethoscope', 'ȘI PROBLEMELE GENERALE', 'blue'], [A.stadiul - .05, 'automobile', 'ȘI STADIUL MAȘINII', 'blue'], [A.decidem - .05, 'handshake', 'DECIDEM ÎMPREUNĂ CE MERITĂ', 'green']] },
      // FINAL: opisul cu lucrările + telefonul + locațiile, pe același ecran
      { k: 'opis', t0: TEND + .22, t1: TOTAL + 1, top: 150, sub: 'MENTENANȚĂ PREVENTIVĂ', subIco: 'stethoscope', kicker: 'OPIS · CE FAC ȘI LA MAȘINILE MELE', head: 'LUCRĂRI RECOMANDATE',
        rows: OPIS, phoneLab: 'PROGRAMĂRI · DIAGNOZĂ GRATUITĂ', phone: '0739 065 065', phoneAt: RT + OPIS.length * RS + .25, site: 'turbodoctor.ro',
        cities: ['GALAȚI', 'BUCUREȘTI', 'IAȘI', 'PIATRA NEAMȚ'], citiesAt: RT + OPIS.length * RS + .75 },
    ],
    endCard: false,
    fx: [
      { k: 'punch', t: A.turbina, a: .05, sh: 8 }, { k: 'punch', t: A.motorul0, a: .05, sh: 8 }, { k: 'punch', t: A.dpful0, a: .06, sh: 10 },
      { k: 'flash', t: A.defectiunile - .1, a: .3 }, { k: 'punch', t: A.defectiunile, a: .08, sh: 16 },
      { k: 'punch', t: A.nu1, a: .05, sh: 8 }, { k: 'punch', t: A.nuLa, a: .05, sh: 8 },
      { k: 'punch', t: A.minim, a: .05, sh: 8 },
      { k: 'flash', t: A.mii10 - .11, a: .55 }, { k: 'punch', t: A.mii10, a: .12, sh: 24 }, { k: 'glitch', t: A.mii10, d: .16 },
      ...CLIP.slice(1).map(c => ({ k: 'glitch', t: c - .04, d: .12 })),
    ],
    sfx: [...CLIP.slice(1).map(c => [c - .1, 'whoosh', .45]), [92.5, 'whoosh', .5], [A.numarul - .1, 'impact', .4]],
    bursts: [[A.mii10 + .04, 540, 312, 6, 420, 1.1]],
  };
};
