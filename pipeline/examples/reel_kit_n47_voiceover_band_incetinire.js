// v2 – Reel „Ai BMW cu N47? Kitul de injecție” (clip de 8 s, fără voce: 2 injectoare și pompa pe masă · 4 injectoare pe platou · pompa pe platou)
// Cerut de Sabin pe 28.11.2026: „videoclipuri captivante cu hook puternic”, cu voice-over făcut cu vocea lui (ElevenLabs „Sabin”), ca să iasă profi.
// Clipul vine deja montat (3 cadre, tăieturi la 2,67 și 5,33 s) și avea ars textul alb „Kit sistem injectie N47” (y ≈ 1254–1324). Rămâne cu montajul lui.
// Sursa: textul vechi scos cu tools/vo_clip/caption_clean_tight.py (rămân urme fine pe platoul negru), peste zona lui stă un `band` opac (titlul lui, refăcut),
// subtitrările coboară sub bandă (capTop), fundalul e fix (bgFix), ca banda să rămână peste urme. Ultimele 1,2 s ale clipului sunt încetinite lin
// (de la viteza normală spre oprire, cadre intermediare cu minterpolate) -> povestea are 8,8 s și ultimul rând de voce încape fără cadru înghețat.
// Sunetul clipului (muzică necunoscută) nu se folosește: out/v2.json {"narrator": true, "orig_gain": 0.0}. Card de final scurt: vo_script.json "end_card": 5.0.
// Voice-over (tools/vo_clip/build_vo_clip.py), text al meu, de confirmat cu Sabin: „Ai BMW cu N47? / Uite kitul de injecție: patru injectoare și pompa de
// înaltă presiune. / Gata de montaj.” („Kit sistem injecție N47” e titlul lui; „BMW” și „Gata de montaj” sunt adăugate de mine.)
// Aprobat cu „Te rog să le postezi pe toate astăzi, acum” și publicat pe 28.11.2026 (Facebook, Instagram, TikTok, YouTube; etichetă AI pe Instagram și TikTok).
window.REEL_CFG = ({ aw, ew, S0, SEND, TEND }) => {
  const A = {
    ai: aw(1, 'Ai'), n47: aw(1, 'N47'),
    uite: aw(2, 'Uite'), kitul: aw(2, 'kitul'), patru: aw(2, 'patru'), pompa: aw(2, 'pompa'), presiuneE: ew(2, 'presiune'),
    gata: aw(3, 'Gata'), montaj: aw(3, 'montaj'),
  };
  const CUT1 = 2.667, CUT2 = 5.333;                    // tăieturile din clip
  const B1 = .04, B2 = A.n47 - .03, HB = CUT1 - .03;
  const Y1 = 300, Y2 = 486;
  return {
    hook: { tag: 'LABORATOR TURBO DOCTOR · INJECȚIE', end: HB - .04, y: -76 },
    bgFix: [[0, SEND]],
    capTop: 1344,
    hideCap: [[0, A.uite - .08]],
    tags: { 2: { kitul: 'y', injectie: 'c', patru: 'y', injectoare: 'c', pompa: 'c', inalta: 'c', presiune: 'c' }, 3: { gata: 'g', montaj: 'g' } },
    items: [
      { k: 'band', t0: 0, t1: SEND, y: 1290, w: 900, h: 96, kicker: 'KIT SISTEM DE INJECȚIE', ph: [[-1, 'BMW N47', 'TURBO DOCTOR']] },
      // ---- hook: întrebarea, pe cuvintele vocii ----
      { k: 'boom', t: B1, dur: HB - B1, txt: 'AI BMW CU', y: Y1, size: 136, col: '#FFFFFF', from: 2.6, sh: 14, ca: 16, riser: false, bg: .55, cg: .15, glow: 'rgba(98,216,255,.5)' },
      { k: 'boom', t: B2, dur: HB - B2, txt: 'N47?', y: Y2, size: 250, col: '#FFD21F', from: 3.6, sh: 24, ca: 28, riser: false, bg: .7, cg: .18 },
      // ---- rețeta: ce e în kit (listă bifată pe cuvintele vocii) ----
      { k: 'list', t0: CUT1 + .1, t1: SEND - .1, top: 268, ico: 'stethoscope', title: 'REȚETA TURBO DOCTOR · N47', w: 640,
        rows: [[A.patru - .03, '4 INJECTOARE'], [A.pompa - .03, 'POMPĂ DE ÎNALTĂ PRESIUNE']] },
      { k: 'scan', t0: CUT1 + .08, t1: CUT2 - .3, box: [90, 620, 900, 500], lab: 'SCANARE KIT...', lab2: '4 INJECTOARE', at2: A.patru, col2: '#4ADE80', labBelow: true },
      { k: 'scan', t0: CUT2 + .08, t1: A.gata - .12, box: [70, 580, 780, 540], lab: 'SCANARE KIT...', lab2: 'POMPĂ ÎNALTĂ PRESIUNE', at2: A.pompa, col2: '#4ADE80', labBelow: true },
      { k: 'stamp', t: A.gata - .03, t1: SEND - .12, x: 540, y: 880, txt: 'GATA DE MONTAJ', col: 'green', s: .92, rot: -7 },
    ],
    fx: [
      { k: 'flash', t: B1, a: .25 }, { k: 'flash', t: B2, a: .4 }, { k: 'shock', t: B2, x: 540, y: Y2, r: 620, col: '#FFD21F', col2: '#FFFFFF' },
      { k: 'glitch', t: HB - .02, d: .12 }, { k: 'flash', t: CUT2 - .02, a: .22 },
    ],
    sfx: [[CUT1 - .08, 'whoosh', .55], [CUT2 - .08, 'whoosh', .45]],
    bursts: [[A.gata + .02, 540, 880, 6, 430, 1.1]],
  };
};
