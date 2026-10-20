// Synthetic intro hook before the clip (graphics + generated voice, see intro_vo.py and out/intro.json).
// reel.js: intro: { type: 'dash' | 'board', tag: '...', cards: [[emoji, title, sub], ...] }
// Types:
//   dash  – instrument cluster: hard start (starter cranking), then Limp Mode (rpm capped, check engine), then the CTA
//   board – three symptom cards slam in, red strings tie them to one "?" (same cause), then the CTA
// Shared CTA: "ASCULTĂ MAI DEPARTE" pill + TURBO DOCTOR wordmark on the CTA phrase; everything flies out into the clip at S0.
window.INTRO_FX = (() => {
  let C = {}, P = null, svg = null; const IM = {};
  const f = x => (+x).toFixed(1);
  const IW = (x, k = 0) => { const n = norm(x); const c = WORDS.filter(w => w.win === -1 && norm(w.text) === n); if (!c[k]) throw new Error('intro anchor not found: ' + x + ' #' + k); return c[k]; };
  const ia = (x, k) => IW(x, k).os;
  const ph = i => P.phrases[Math.min(i, P.phrases.length - 1)];
  const TX = (x, y, txt, o = {}) => `<text x="${f(x)}" y="${f(y)}" font-family="${o.fam || 'Mont'}" font-weight="${o.w || 900}" font-size="${o.s || 40}" fill="${o.c || '#fff'}" text-anchor="${o.a || 'middle'}" letter-spacing="${o.ls ?? 1}"` +
    (o.st ? ` stroke="${o.stc || '#000'}" stroke-width="${o.st}" paint-order="stroke" stroke-linejoin="round"` : '') + (o.op != null ? ` opacity="${(+o.op).toFixed(3)}"` : '') + (o.tr ? ` transform="${o.tr}"` : '') + `>${txt}</text>`;
  const G = (x, y, s, o, inner) => `<g transform="translate(${f(x)} ${f(y)}) scale(${(+s).toFixed(4)})" opacity="${clamp(o).toFixed(3)}">${inner}</g>`;
  const pop = (t, t0, d = .3, back = 2.2) => { const k = t - t0; if (k < 0) return [0, 0]; const p = clamp(k / d); return [eBack(p, back), clamp(p * 3)]; };
  function mkImg(name, size) { if (IM[name]) return IM[name]; const im = document.createElement('img'); im.src = `assets/emoji/${name}.png`; im.className = 'abs emo';
    im.style.width = im.style.height = size + 'px'; $('intro').appendChild(im); IM[name] = im; return im; }
  // ---------- shared pieces ----------
  const tri = (x, y, s, col) => `<path d="M ${f(x)} ${f(y - s)} L ${f(x + s * 1.1)} ${f(y + s * .8)} L ${f(x - s * 1.1)} ${f(y + s * .8)} Z" fill="${col}" stroke="#000" stroke-width="3" stroke-linejoin="round"/>` +
    TX(x, y + s * .62, '!', { s: s * 1.25, c: '#000', w: 900, ls: 0 });
  function pill(x, y, w, h, fill, stroke, txt, o = {}) {
    return `<rect x="${f(x - w / 2)}" y="${f(y - h / 2)}" width="${f(w)}" height="${f(h)}" rx="${f(h / 2)}" fill="${fill}" stroke="${stroke}" stroke-width="${o.sw || 4}"/>` +
      (o.ico ? tri(x - w / 2 + h * .62, y + 2, h * .26, o.icoC || '#FFD21F') : '') + TX(x + (o.ico ? h * .28 : 0), y + (o.s || 40) * .36, txt, { s: o.s || 40, c: o.c || '#fff', w: 900, ls: o.ls ?? 1 });
  }
  function tag(t) {
    const out = ph(C.ctaPh).t0 - .15; if (t > out + .2) return '';
    const [s, o] = pop(t, .05, .28, 2); const fo = 1 - clamp((t - out) / .2); if (!o) return '';
    const txt = C.tag || 'ÎȚI SUNĂ CUNOSCUT?'; const w = txt.length * 19 + 96;
    const blink = Math.floor(t * 4) % 2 ? .3 : 1;
    return G(540, 200, s, o * fo, `<rect x="${f(-w / 2)}" y="-30" width="${f(w)}" height="60" rx="30" fill="rgba(6,10,18,.86)" stroke="rgba(255,75,75,.85)" stroke-width="3"/>` +
      `<circle cx="${f(-w / 2 + 34)}" cy="0" r="9" fill="#FF3B30" opacity="${blink}"/>` + TX(18, 10, txt, { fam: 'JB', w: 800, s: 28, ls: 2 }));
  }
  function cta(t) {
    const p0 = ph(C.ctaPh).t0; let s = '';
    let [ps, po] = pop(t, p0 - .04, .32, 2.4);
    if (po) { const pulse = 1 + .035 * Math.max(0, Math.sin((t - p0) * 7)); const w = 760;
      s += G(540, 770, ps * pulse, po, `<rect x="${-w / 2 - 10}" y="-62" width="${w + 20}" height="124" rx="62" fill="rgba(225,29,46,.35)"/>` +
        pill(0, 0, w, 104, '#E11D2E', '#fff', 'ASCULTĂ MAI DEPARTE', { s: 50, sw: 5 })); }
    const tt = C.brandAt ?? ia('Turbo') - .06; const [ws, wo] = pop(t, tt, .26, 1.6);
    if (wo) { const st = lerp(1.5, 1, eOut(clamp((t - tt) / .16)));
      s += G(540, 600, ws * st, wo, TX(0, 0, 'TURBO <tspan fill="#FFD21F">DOCTOR</tspan>', { fam: 'Anton', w: 400, s: 150, st: 16, ls: 2 })); }
    return s;
  }
  function ctaImgs(t) {
    const p0 = ph(C.ctaPh).t0; const im = mkImg('backhand_index_pointing_down', 110); const k = t - p0 - .15;
    if (k < 0 || t > S0 - .05) { hide(im); return; }
    const out = S0 - .4; const o = clamp(k / .2) * (1 - clamp((t - out) / .3));
    setT(im, 540, 902 + Math.abs(Math.sin(k * 6)) * 18, eBack(clamp(k / .3), 2.4) * outS(t), 0, o);
  }
  const outS = t => 1 + .14 * eIn(clamp((t - (S0 - .4)) / .35));
  const outO = t => 1 - clamp((t - (S0 - .4)) / .33);
  function grid(t) { let s = '';
    for (let x = 0; x <= 1080; x += 90) s += `<line x1="${x}" y1="0" x2="${x}" y2="1920" stroke="rgba(98,216,255,.07)" stroke-width="2"/>`;
    const off = (t * 40) % 90; for (let y = -90; y <= 1920; y += 90) s += `<line x1="0" y1="${f(y + off)}" x2="1080" y2="${f(y + off)}" stroke="rgba(98,216,255,.07)" stroke-width="2"/>`;
    return `<g opacity="${outO(t).toFixed(3)}">${s}</g>`; }

  // ---------- type: dash (instrument cluster) ----------
  const AG = v => (135 + 270 * v / 7) * Math.PI / 180;
  const PT = (cx, cy, r, v) => [cx + r * Math.cos(AG(v)), cy + r * Math.sin(AG(v))];
  function arc(cx, cy, r, v0, v1) { const [x0, y0] = PT(cx, cy, r, v0), [x1, y1] = PT(cx, cy, r, v1); return `M ${f(x0)} ${f(y0)} A ${r} ${r} 0 ${(v1 - v0) * 270 / 7 > 180 ? 1 : 0} 1 ${f(x1)} ${f(y1)}`; }
  const lampGlow = (x, y, on, col) => on ? `<circle cx="${f(x)}" cy="${f(y)}" r="52" fill="${col}" opacity=".18"/>` : '';
  const coil = (x, y, col) => `<path d="M ${f(x - 40)} ${f(y + 10)} h 10 c 0 -30 16 -30 16 0 c 0 -30 16 -30 16 0 c 0 -30 16 -30 16 0 h 12" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
  const engine = (x, y, col) => `<path transform="translate(${f(x)} ${f(y)})" d="M -38 -6 L -30 -6 L -30 -14 L -18 -14 L -18 -21 L 4 -21 L 4 -14 L 14 -14 L 20 -6 L 28 -6 L 28 -13 L 37 -13 L 37 17 L 28 17 L 28 10 L 20 10 L 14 21 L -20 21 L -26 13 L -30 13 L -30 21 L -38 21 Z" fill="none" stroke="${col}" stroke-width="6" stroke-linejoin="round"/>`;
  const battery = (x, y, col) => `<g transform="translate(${f(x)} ${f(y)})"><rect x="-34" y="-16" width="68" height="40" rx="5" fill="none" stroke="${col}" stroke-width="6"/><rect x="-24" y="-24" width="12" height="8" fill="${col}"/><rect x="12" y="-24" width="12" height="8" fill="${col}"/>` +
    `<path d="M -22 4 h 14 M -15 -3 v 14 M 9 4 h 14" stroke="${col}" stroke-width="5" stroke-linecap="round"/></g>`;
  const padlock = (x, y, col) => `<g transform="translate(${f(x)} ${f(y)})"><path d="M -12 -6 v -10 a 12 12 0 0 1 24 0 v 10" fill="none" stroke="${col}" stroke-width="6"/><rect x="-18" y="-7" width="36" height="28" rx="5" fill="${col}"/><circle cx="0" cy="6" r="4" fill="#000"/></g>`;
  const OFF = '#26303C';
  function rpmAt(t) {
    const p1 = ph(1).t0, av = ia('avarie'), acc = ia('accelerezi');
    if (t < .5) return 0;
    if (t < p1) { const k = t - .5; let r = .16 + .15 * Math.abs(Math.sin(2 * Math.PI * 4.4 * k)) + .03 * Math.sin(t * 37);
      const tr = 1.05; if (k > tr && k < tr + .55) r += .45 * Math.sin(Math.PI * (k - tr) / .55); return r; }   // a failed attempt to catch
    const up = av - .28;
    if (t < up) return lerp(.35, .85, eOut(clamp((t - p1) / .3))) + .02 * Math.sin(t * 31);
    const base = lerp(.85, 2.88, eOut(clamp((t - up) / .34)));
    let r = base + (t > up + .34 ? -.1 * Math.abs(Math.sin(t * 19)) - .04 * Math.sin(t * 47) : 0);
    const kk = t - acc; if (kk > 0 && kk < .5) r = Math.min(2.99, r + .1 * Math.sin(Math.PI * kk / .5));
    return Math.min(2.99, r);
  }
  function dash(t) {
    const p1 = ph(1).t0, ctaT = ph(C.ctaPh).t0, av = ia('avarie'), cx = 540, cy = 640, R = 232;
    const [ps, po] = pop(t, 0, .3, 1.6); const fo = 1 - clamp((t - (ctaT - .14)) / .24); const o = po * fo;
    if (o <= .003) return '';
    const sc = ps * lerp(1, .88, eIn(clamp((t - (ctaT - .14)) / .24)));
    const locked = t >= av - .12; const rpm = rpmAt(t);
    let s = `<rect x="100" y="300" width="880" height="660" rx="52" fill="rgba(5,8,13,.9)" stroke="#2B3540" stroke-width="6"/>` +
      `<rect x="112" y="312" width="856" height="636" rx="44" fill="none" stroke="rgba(98,216,255,.18)" stroke-width="2"/>`;
    s += `<circle cx="${cx}" cy="${cy}" r="${R + 26}" fill="#03060A" stroke="#1E2732" stroke-width="8"/>`;
    s += `<path d="${arc(cx, cy, R - 8, 5, 7)}" fill="none" stroke="#E11D2E" stroke-width="18" opacity="${locked ? .25 : 1}"/>`;
    if (locked) { const lp = clamp((t - (av - .12)) / .25);
      s += `<path d="${arc(cx, cy, R - 8, 3, 3 + 4 * lp)}" fill="none" stroke="#FF8A1F" stroke-width="18" stroke-dasharray="10 10" opacity=".85"/>`;
      const [lx, ly] = PT(cx, cy, R + 4, 3), [lx2, ly2] = PT(cx, cy, R - 60, 3);
      s += `<line x1="${f(lx)}" y1="${f(ly)}" x2="${f(lx2)}" y2="${f(ly2)}" stroke="#FF8A1F" stroke-width="8" stroke-linecap="round"/>`;
      const [px, py] = PT(cx, cy, R + 58, 3); s += G(px, py, eBack(lp, 2.6), lp, padlock(0, 0, '#FF8A1F')); }
    for (let v = 0; v <= 7.001; v += .5) { const maj = Math.abs(v - Math.round(v)) < .01; const [x0, y0] = PT(cx, cy, R - (maj ? 40 : 22), v), [x1, y1] = PT(cx, cy, R - 4, v);
      s += `<line x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}" stroke="${v >= 5 ? '#FF4B4B' : '#EAF6FF'}" stroke-width="${maj ? 7 : 4}" stroke-linecap="round" opacity="${locked && v > 3 ? .3 : 1}"/>`;
      if (maj) { const [nx, ny] = PT(cx, cy, R - 74, v); s += TX(nx, ny + 14, String(v), { s: 40, w: 800, c: v >= 5 ? '#FF6B6B' : '#EAF6FF', op: locked && v > 3 ? .35 : 1 }); } }
    s += TX(cx, cy - 92, 'x1000 RPM', { fam: 'JB', w: 700, s: 22, c: 'rgba(234,246,255,.55)', ls: 3 });
    s += TX(cx, cy + 128, String(Math.round(rpm * 1000 / 10) * 10).padStart(4, ' '), { fam: 'JB', w: 800, s: 50, c: locked ? '#FF8A1F' : '#EAF6FF', ls: 4 });
    const [nx, ny] = PT(cx, cy, R - 30, rpm), [bx, by] = PT(cx, cy, -34, rpm);
    s += `<line x1="${f(bx)}" y1="${f(by)}" x2="${f(nx)}" y2="${f(ny)}" stroke="#FF5A1F" stroke-width="22" stroke-linecap="round" opacity=".22"/>` +
      `<line x1="${f(bx)}" y1="${f(by)}" x2="${f(nx)}" y2="${f(ny)}" stroke="#FF5A1F" stroke-width="10" stroke-linecap="round"/>` +
      `<circle cx="${cx}" cy="${cy}" r="26" fill="#1B2430" stroke="#FF5A1F" stroke-width="5"/>`;
    // warning lamps: glow plug (pre-heat), battery (cranking), check engine (Limp Mode)
    const glowOn = t > .08 && t < .5, batOn = t >= .5 && t < p1 + .05 && Math.floor(t * 8) % 3 !== 0, mil = t >= av - .08, milOn = mil && Math.floor((t - av) * 5) % 2 === 0;
    s += lampGlow(190, 640, glowOn, '#FFB020') + coil(190, 646, glowOn ? '#FFB020' : OFF);
    s += lampGlow(190, 820, batOn, '#FF3B30') + battery(190, 820, batOn ? '#FF3B30' : OFF);
    s += lampGlow(890, 640, milOn, '#FFB020') + engine(890, 640, mil ? (milOn ? '#FFB020' : '#7A5208') : OFF);
    if (mil) s += TX(890, 724, 'CHECK', { fam: 'JB', w: 800, s: 20, c: '#FFB020', ls: 2, op: milOn ? 1 : .55 });
    s += TX(890, 455, 'MOTOR', { fam: 'JB', w: 800, s: 20, c: '#62D8FF', ls: 2 }) + TX(890, 482, 'RECE', { fam: 'JB', w: 800, s: 20, c: '#62D8FF', ls: 2 });
    let out = G(540, 630, sc, o, `<g transform="translate(-540 -630)">${s}</g>`);
    // status badge under the cluster
    const b1 = ia(C.badge1At || 'greu') - .05, b2 = av - .05;
    if (t >= b1 && t < ctaT) { const two = t >= b2; const [bs, bo] = pop(t, two ? b2 : b1, .26, 2.6);
      const txt = two ? (C.badge2 || 'MOD AVARIE · PUTERE LIMITATĂ') : (C.badge1 || 'PORNIRE GREA'); const w = Math.min(900, txt.length * 25 + 140);
      out += G(540, 1040, bs * sc, bo * fo, pill(0, 0, w, 96, two ? '#E11D2E' : 'rgba(6,10,18,.92)', two ? '#fff' : '#FFB020', txt, { s: 40, ico: true, icoC: two ? '#FFD21F' : '#FFB020', c: two ? '#fff' : '#FFB020' })); }
    return out;
  }
  function dashImgs(t) {
    const ctaT = ph(C.ctaPh).t0, fo = 1 - clamp((t - (ctaT - .14)) / .24);
    const key = mkImg('key', 96), sn = mkImg('snowflake', 74);
    const [ps, po] = pop(t, 0, .3, 1.6);
    if (po * fo > .003) { const k = clamp((t - .12) / .32); const rot = lerp(-55, 32, eOut(k)) + (t > .45 && t < ph(1).t0 ? 3 * Math.sin(t * 40) : 0);
      setT(key, 190, 455, ps, rot, po * fo); setT(sn, 890, 392, ps * (1 + .04 * Math.sin(t * 3)), t * 20, po * fo); }
    else { hide(key); hide(sn); }
  }

  // ---------- type: board (three symptoms -> one cause) ----------
  const CARD_Y = [430, 610, 790];
  function board(t) {
    const ctaT = ph(C.ctaPh).t0; const fo = 1 - clamp((t - (ctaT - .14)) / .24); if (fo <= .003) return '';
    const tr = ia(C.mergeAt || 'Trei') - .05, cz = ia(C.causeAt || 'aceeași') - .1;
    const m = eInOut(clamp((t - tr) / .38)); let s = '';
    const cards = C.cards || [];
    const ends = [];
    cards.forEach((c, i) => {
      const t0 = c[3] ?? (ph(i).t0 - .04); const k = t - t0; if (k < 0) return; const p = clamp(k / .3);
      const x = lerp(1500, 540, eBack(p, 1.4)), rot = lerp(14, i % 2 ? 1.5 : -1.5, eOut(p));
      const cx = lerp(x, 318, m), cy = lerp(CARD_Y[i], [468, 600, 732][i], m), sc = lerp(1, .6, m);
      const shake = k < .35 ? 7 * Math.exp(-k * 9) * Math.sin(k * 70) : 0;
      const card = `<rect x="-400" y="-74" width="800" height="148" rx="30" fill="#fff" stroke="#E11D2E" stroke-width="6"/>` +
        `<rect x="-400" y="-74" width="26" height="148" rx="13" fill="#E11D2E"/>` +
        `<circle cx="-300" cy="0" r="56" fill="#111827" stroke="#E11D2E" stroke-width="5"/>` +
        TX(-226, c[2] ? -2 : 18, c[1], { s: 52, c: '#0F1216', a: 'start', ls: 0 }) + (c[2] ? TX(-224, 40, c[2], { fam: 'JB', w: 800, s: 24, c: '#8A8F98', a: 'start', ls: 2 }) : '') +
        `<g transform="translate(330 0)">${'<path d="M -22 -22 L 22 22 M 22 -22 L -22 22" stroke="#E11D2E" stroke-width="12" stroke-linecap="round"/>'}</g>`;
      s += G(cx + shake, cy, sc, clamp(p * 3), `<g transform="rotate(${f(rot)})">${card}</g>`);
      ends.push([cx + 400 * sc, cy]); IM['c' + i] = [cx - 300 * sc + shake, cy, sc, clamp(p * 3), rot];
    });
    // strings to one cause
    const TXC = 820, TYC = 600;
    if (t >= cz - .3) {
      ends.forEach(([x, y], i) => { const p = eOut(clamp((t - (cz - .3 + i * .08)) / .26)); if (p <= 0) return;
        const xe = lerp(x, TXC - 110, p), ye = lerp(y, TYC + (i - 1) * 46, p);
        s += `<line x1="${f(x)}" y1="${f(y)}" x2="${f(xe)}" y2="${f(ye)}" stroke="#E11D2E" stroke-width="7" stroke-linecap="round"/>` +
          `<circle cx="${f(x)}" cy="${f(y)}" r="10" fill="#E11D2E" stroke="#fff" stroke-width="3"/>`; });
      const [qs, qo] = pop(t, cz, .3, 2.6);
      if (qo) { const rk = ((t - cz) % 1) / 1;
        s += `<circle cx="${TXC}" cy="${TYC}" r="${f(120 + rk * 60)}" fill="none" stroke="#FF3B30" stroke-width="6" opacity="${f(.8 * (1 - rk))}"/>`;
        s += G(TXC, TYC, qs, qo, `<circle r="120" fill="#E11D2E" stroke="#fff" stroke-width="8"/>` + TX(0, 70, '?', { fam: 'Anton', w: 400, s: 200, st: 10, ls: 0 })); }
      const [ls, lo] = pop(t, cz + .12, .28, 2);
      if (lo) s += G(540, 915, ls, lo, TX(0, 0, C.causeTxt || 'ACEEAȘI CAUZĂ', { fam: 'Anton', w: 400, s: 104, c: '#FFD21F', st: 14, ls: 2 }));
    }
    return `<g opacity="${fo.toFixed(3)}">${s}</g>`;
  }
  function boardImgs(t) {
    const ctaT = ph(C.ctaPh).t0; const fo = 1 - clamp((t - (ctaT - .14)) / .24);
    (C.cards || []).forEach((c, i) => { const im = mkImg(c[0], 78); const q = IM['c' + i];
      if (!q || fo <= .003 || t < (c[3] ?? (ph(i).t0 - .04))) { hide(im); return; }
      setT(im, q[0], q[1], q[2], q[4], q[3] * fo); });
  }

  // ---------- API ----------
  function build(cfg, intro) {
    C = Object.assign({ type: 'dash', ctaPh: 2 }, cfg || {}); P = intro;
    const d = document.createElement('div'); d.id = 'intro'; d.className = 'abs'; d.style.cssText = 'display:block;left:0;top:0;width:1080px;height:1920px';
    $('stage').insertBefore(d, $('items'));
    svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); svg.setAttribute('viewBox', '0 0 1080 1920'); svg.setAttribute('width', '1080'); svg.setAttribute('height', '1920');
    svg.style.cssText = 'position:absolute;left:0;top:0;overflow:visible'; d.appendChild(svg);
    if (C.type === 'dash') { mkImg('key', 96); mkImg('snowflake', 74); }
    if (C.type === 'board') (C.cards || []).forEach(c => mkImg(c[0], 78));
    mkImg('backhand_index_pointing_down', 110);
    // accents (camera + colour) on the strong beats
    if (C.type === 'dash') { const av = ia('avarie');
      CFG.fx.push({ k: 'punch', t: av, a: .05, sh: 8 }, { k: 'red', t0: av - .05, t1: ph(1).t1 + .15, max: 1.8 }, { k: 'punch', t: ia('accelerezi'), a: .03, sh: 5 }); }
    if (C.type === 'board') { (C.cards || []).forEach((c, i) => CFG.fx.push({ k: 'punch', t: (c[3] ?? (ph(i).t0 - .04)) + .12, a: .035, sh: 6 }));
      CFG.fx.push({ k: 'punch', t: ia(C.causeAt || 'aceeași'), a: .05, sh: 8 }); }
    CFG.fx.push({ k: 'punch', t: (C.brandAt ?? ia('Turbo') - .06) + .1, a: .04 }, { k: 'flash', t: S0 - .05, a: .32 });
  }
  function cues() {  // SFX land just before the words, quieter than the clip's, so the voice stays clear
    const ctaT = ph(C.ctaPh).t0, bt = C.brandAt ?? ia('Turbo') - .06;
    sfx(0, 'impact', .6); sfx(.02, 'glitch', .35);
    if (C.type === 'dash') { const av = ia('avarie');
      sfx(.1, 'beep', .4); sfx(.15, 'tick2', .45); sfx(.5, 'crank', .7); sfx(av - .5, 'riser', .3); sfx(av - .14, 'impact', .42); sfx(ia('accelerezi') + .5, 'alarm', .32);
      sfx(ia('greu') - .1, 'pop', .3); }
    if (C.type === 'board') { (C.cards || []).forEach((c, i) => { const t0 = c[3] ?? (ph(i).t0 - .04); sfx(t0 - .02, 'impact', .42); });
      const tr = ia(C.mergeAt || 'Trei') - .05, cz = ia(C.causeAt || 'aceeași') - .1;
      sfx(tr - .22, 'whoosh', .35); [0, 1, 2].forEach(i => sfx(cz - .3 + i * .08 + .24, 'lock', .28)); sfx(cz - .06, 'hit', .42); sfx(ia('cauză') + .5, 'stamp', .4); }
    sfx(ctaT - .2, 'whoosh', .45); sfx(ctaT - .06, 'pop', .35); sfx(bt - .02, 'pop', .3); sfx(ph(C.ctaPh).t1 + .05, 'shimmer', .5);
    sfx(S0 - 1.0, 'riser', .35); sfx(S0 - .45, 'whoosh', .8);
  }
  function render(t) {
    const d = $('intro'); if (!d) return;
    if (t >= S0) { if (d.style.display !== 'none') { d.style.display = 'none'; Object.values(IM).forEach(im => im instanceof HTMLElement && hide(im)); } return; }
    d.style.display = 'block';
    let s = grid(t) + tag(t);
    if (C.type === 'dash') s += dash(t);
    if (C.type === 'board') s += board(t);
    s += cta(t);
    svg.innerHTML = `<g transform="translate(540 960) scale(${outS(t).toFixed(4)}) translate(-540 -960)" opacity="${outO(t).toFixed(3)}">${s}</g>`;
    if (C.type === 'dash') dashImgs(t);
    if (C.type === 'board') boardImgs(t);
    ctaImgs(t);
  }
  return { build, cues, render };
})();
