// v2 – Reel „Injectorul de Volvo care își măsoară singur presiunea” (Denso i-ART, procesul de curățare; clip de 30 s, fără voce)
// Cerut de Sabin pe 28.11.2026: „videoclipuri captivante cu hook puternic”, cu voice-over făcut cu vocea lui (ElevenLabs „Sabin”), ca să iasă profi.
// Clipul vine deja montat (CapCut): fiecare cadru e o fereastră care crește pe fundal negru și are ars sus titlul roșu „Proces curățare Denso i-Art Volvo”.
// Rămâne cu montajul lui (PREFERINTE: clipurile deja editate nu se retaie, nu se decupează). Titlul vechi e acoperit, pe toată durata, de un `lbl` opac
// (y 232–396) al cărui rând mare urmărește vocea; fundalul e fix (bgFix), ca eticheta să rămână peste titlu. Ștergerea titlului (inpaint) lăsa pete.
// Sunetul clipului (muzică necunoscută) nu se folosește: out/v2.json {"narrator": true, "orig_gain": 0.0}.
// Voice-over (tools/vo_clip/build_vo_clip.py, vo_script.json), 7 rânduri puse pe cadre. Textul e al meu, de confirmat cu Sabin:
// „Injectorul ăsta de Volvo își măsoară singur presiunea. / E un Denso i-ART. Și uite cum îl curățăm. / Îl desfacem complet, până la ultima piesă. /
// La asemenea precizie, orice impuritate contează. / De aceea se lucrează curat și cu răbdare. / Arcuri, șaibe și știfturi de câțiva milimetri. /
// Fiecare piesă e curățată și verificată, apoi injectorul se asamblează la loc.” (i-ART = senzor de presiune în fiecare injector: verificat la Volvo și Denso.)
// Cadre (fereastra repornește): 0,20 injectorul în dispozitiv · 3,90 mâini cu placa supapei (de la ~7,8 corpul văzut de sus) · 10,63 · 13,97 corpul, alte unghiuri ·
// 19,10 piese mici în palmă · 23,87 și 27,43 piesele așezate pe hârtie. Coperta: out/cover_t.json.
// Aprobat cu „Te rog să le postezi pe toate astăzi, acum” și publicat pe 28.11.2026 (Facebook, Instagram, TikTok, YouTube; etichetă AI pe Instagram și TikTok).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    inj: aw(1, 'Injectorul'), volvo: aw(1, 'Volvo'), isi: aw(1, 'își'), pres: aw(1, 'presiunea'),
    e2: aw(2, 'E'), denso: aw(2, 'Denso'), iart: aw(2, 'i-ART'), si2: aw(2, 'Și'), curatam: aw(2, 'curățăm'), curatamE: ew(2, 'curățăm'),
    il3: aw(3, 'Îl'), complet: aw(3, 'complet'), ultima: aw(3, 'ultima'),
    la4: aw(4, 'La'), conteazaE: ew(4, 'contează'),
    de5: aw(5, 'De'), curat: aw(5, 'curat'), rabdare: aw(5, 'răbdare'), rabdareE: ew(5, 'răbdare'),
    arcuri: aw(6, 'Arcuri'), saibe: aw(6, 'șaibe'), stifturi: aw(6, 'știfturi'), cativa: aw(6, 'câțiva'), milimetriE: ew(6, 'milimetri'),
    fiecare: aw(7, 'Fiecare'), curatata: aw(7, 'curățată'), verificata: aw(7, 'verificată'), apoi: aw(7, 'apoi'), asambleaza: aw(7, 'asamblează'),
  };
  const B1 = .12, B2 = A.volvo - .03, B3 = A.isi - .03, B4 = A.pres - .02, HB = 3.86;   // 3,90: fereastra repornește (cadrul 2)
  const Y1 = 520, Y2 = 672, Y3 = 1172, Y4 = 1356;
  const K = 'PROCES DE CURĂȚARE · DENSO i-ART VOLVO', TOP = 424;
  return {
    hook: null,
    bgFix: [[0, SEND]],
    hideCap: [[0, A.e2 - .08]],
    tags: {
      2: { denso: 'y', iart: 'y', curatam: 'g' }, 3: { desfacem: 'c', complet: 'y', ultima: 'y', piesa: 'c' }, 4: { precizie: 'y', impuritate: 'r', conteaza: 'r' },
      5: { curat: 'g', rabdare: 'g' }, 6: { arcuri: 'c', saibe: 'c', stifturi: 'c', cativa: 'y', milimetri: 'y' },
      7: { piesa: 'c', curatata: 'g', verificata: 'g', injectorul: 'c', asambleaza: 'g' },
    },
    items: [
      { k: 'lbl', t0: 0, t1: SEND, y: 314, w: 930, h: 164, ph: [
        [-1, 'LABORATOR TURBO DOCTOR · INJECȚIE', 'INJECTOR DENSO i-ART · VOLVO', ''],
        [A.si2 - .05, K, 'CUM ÎL CURĂȚĂM', 'y'],
        [A.il3 - .05, K, 'DEMONTARE COMPLETĂ', 'c'],
        [A.la4 - .05, K, 'ORICE IMPURITATE CONTEAZĂ', 'y'],
        [A.de5 - .05, K, 'CURAT ȘI CU RĂBDARE', 'g'],
        [A.arcuri - .05, K, 'PIESELE DIN INTERIOR', 'c'],
        [A.fiecare - .05, K, 'CURĂȚARE ȘI VERIFICARE', 'g'],
        [A.apoi - .05, K, 'ASAMBLARE', 'g'],
      ] },
      // ---- hook: titluri pe cuvintele vocii ----
      { k: 'boom', t: B1, dur: HB - B1, txt: 'INJECTORUL ĂSTA', y: Y1, size: 124, col: '#FFFFFF', from: 2.6, sh: 14, ca: 16, riser: false, bg: .55, cg: .15, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'DE VOLVO', y: Y2, size: 150, col: '#62D8FF', from: 3.0, sh: 14, ca: 16, riser: false, bg: .45, cg: .12, glow: 'rgba(98,216,255,.6)' },
      { k: 'boom', t: B3, dur: HB - B3, txt: 'ÎȘI MĂSOARĂ SINGUR', y: Y3, size: 104, col: '#FFFFFF', from: 2.6, sh: 12, ca: 14, riser: false, bg: .45, cg: .12, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B4, dur: HB - B4, txt: 'PRESIUNEA!', y: Y4, size: 182, col: '#FFD21F', from: 3.4, sh: 22, ca: 26, riser: false, bg: .6, cg: .15 },
      // ---- 2: fișa pacientului ----
      { k: 'file', t0: A.e2 - .12, t1: A.curatamE + .1, top: TOP, ecg: 'ok',
        rows: [[A.denso - .05, 'PACIENT', 'INJECTOR DENSO', 'c', 'svc_injector'], [A.iart - .03, 'MODEL', 'i‑ART · VOLVO', '', 'automobile'],
          [A.curatam - .12, 'TRATAMENT', 'CURĂȚARE COMPLETĂ', 'g', 'soap']] },
      // ---- 3: demontare ----
      { k: 'scan', t0: A.il3 + .08, t1: 10.42, box: [330, 770, 400, 400], lab: 'DEMONTARE...', lab2: 'DEMONTAT COMPLET', at2: A.complet + .2, col2: '#4ADE80' },
      { k: 'kin', t: A.ultima - .02, dur: .58, txt: 'ULTIMA PIESĂ', col: '#FFD21F', y: 560, size: 150, rot: -3 },
      // ---- 4: de ce contează ----
      { k: 'def', t0: A.la4 - .12, t1: A.conteazaE + .15, top: TOP, term: 'DENSO i-ART', text: 'Fiecare injector are propriul senzor de presiune.' },
      // ---- 5: cum se lucrează ----
      { k: 'list', t0: A.de5 - .1, t1: A.rabdareE + .2, top: TOP, ico: 'test_tube', title: 'ÎN LABORATORUL TURBO DOCTOR', rows: [[A.curat - .03, 'LUCRU CURAT'], [A.rabdare - .03, 'RĂBDARE LA FIECARE PIESĂ']] },
      // ---- 6: piesele mici ----
      { k: 'chip', t0: A.arcuri - .08, t1: A.milimetriE + .35, y: 470, ph: [[A.arcuri - .08, 'nutbolt', 'ARCURI', 'blue'], [A.saibe - .03, 'nutbolt', 'ARCURI · ȘAIBE', 'blue'], [A.stifturi - .03, 'nutbolt', 'ARCURI · ȘAIBE · ȘTIFTURI', 'blue']] },
      { k: 'scan', t0: A.arcuri + .1, t1: A.milimetriE + .3, box: [340, 800, 400, 300], lab: 'ANALIZĂ...', lab2: 'CÂȚIVA MILIMETRI', at2: A.cativa, col2: '#4ADE80' },
      // ---- 7: tratamentul ----
      { k: 'pipe', t0: A.fiecare - .15, t1: SEND - .12, top: TOP, ico: 'test_tube', title: 'TRATAMENT ÎN LABORATORUL TURBO DOCTOR',
        steps: [[A.fiecare, 'wrench', 'DEMONTARE'], [A.curatata, 'soap', 'CURĂȚARE'], [A.verificata, 'microscope', 'VERIFICARE'], [A.asambleaza, 'hammer_and_wrench', 'ASAMBLARE']] },
    ],
    fx: [
      { k: 'flash', t: B1, a: .16 }, { k: 'flash', t: B2, a: .16 }, { k: 'flash', t: B3, a: .2 },
      { k: 'flash', t: B4, a: .45 },
      { k: 'glitch', t: HB - .04, d: .14 },
      { k: 'flash', t: A.ultima, a: .25 },
    ],
    sfx: [[HB - .1, 'whoosh', .6]],
    bursts: [[A.asambleaza + .08, 880, 545, 5, 150, .75]],
  };
};
