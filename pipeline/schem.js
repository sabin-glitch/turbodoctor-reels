// Turbo Doctor – engineering schematics (blueprint style), drawn per frame as SVG strings.
// Every function: (tl, ph, pt, P, t, o) -> inner SVG for a 914 x H canvas.
//   tl = seconds since panel start, ph = current step index, pt = seconds since that step started, P = params.
// Original drawings for Turbo Doctor; simplified, generic mechanisms (no brand artwork).
window.SCHEM = (() => {
  const C = { cy: '#62D8FF', cyD: 'rgba(98,216,255,.38)', w: '#EAF6FF', dim: 'rgba(234,246,255,.6)', red: '#FF4B4B', yel: '#FFD21F', grn: '#4ADE80', org: '#FF8A3D',
    oil: '#E9A928', oilD: '#7A5208', steel: '#A9BCD0', steelD: '#5B6F86', body: '#0E2742', body2: '#13355A', bg: '#071425', smoke: '#9FB3C8' };
  const f = x => (+x).toFixed(1);
  const cl = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, p) => a + (b - a) * p;
  const eo = p => 1 - Math.pow(1 - cl(p), 3);
  const eio = p => { p = cl(p); return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  const P2 = (cx, cy, r, a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  const rad = d => d * Math.PI / 180;
  const T = (x, y, s, o = {}) => `<text x="${f(x)}" y="${f(y)}" font-family="${o.fam || 'JB'}" font-weight="${o.w || 800}" font-size="${o.s || 19}" fill="${o.c || C.w}" text-anchor="${o.a || 'start'}" letter-spacing="${o.ls ?? 1.5}"${o.op != null ? ` opacity="${o.op}"` : ''}>${s}</text>`;
  const tag = (x, y, s, col = C.cy, anchor = 'middle', size = 19, op = 1) => {
    const w = s.length * (size * 0.6 + 1.5) + 26, h = size * 1.55; const x0 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
    return `<g opacity="${op}"><rect x="${f(x0)}" y="${f(y - h / 2)}" width="${f(w)}" height="${f(h)}" rx="8" fill="rgba(7,20,37,.94)" stroke="${col}" stroke-width="2.5"/>` + T(x0 + w / 2, y + size * 0.36, s, { c: col, a: 'middle', s: size }) + '</g>';
  };
  const ARW = (x1, y1, x2, y2, col = C.cy, w = 4, h = 14) => {
    const a = Math.atan2(y2 - y1, x2 - x1); const p1 = [x2 - h * Math.cos(a - .45), y2 - h * Math.sin(a - .45)], p2 = [x2 - h * Math.cos(a + .45), y2 - h * Math.sin(a + .45)];
    const xe = x2 - h * .6 * Math.cos(a), ye = y2 - h * .6 * Math.sin(a);
    return `<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(xe)}" y2="${f(ye)}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/><path d="M ${f(x2)} ${f(y2)} L ${f(p1[0])} ${f(p1[1])} L ${f(p2[0])} ${f(p2[1])} Z" fill="${col}"/>`;
  };
  const DBL = (x1, y1, x2, y2, col = C.red, w = 4) => { const mx = (x1 + x2) / 2, my = (y1 + y2) / 2; return ARW(mx, my, x2, y2, col, w) + ARW(mx, my, x1, y1, col, w); };
  const drop = (x, y, r, col = C.oil, op = 1) => `<path d="M ${f(x)} ${f(y - r * 1.9)} C ${f(x + r * .9)} ${f(y - r * .6)} ${f(x + r)} ${f(y + r * .2)} ${f(x)} ${f(y + r)} C ${f(x - r)} ${f(y + r * .2)} ${f(x - r * .9)} ${f(y - r * .6)} ${f(x)} ${f(y - r * 1.9)} Z" fill="${col}" opacity="${op}"/>`;
  const glowC = (x, y, r, col, op) => `<circle cx="${f(x)}" cy="${f(y)}" r="${f(r)}" fill="${col}" opacity="${f(op)}"/>`;
  const rnd = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const xmark = (x, y, s = 30, col = C.red, w = 9) => `<path d="M ${f(x - s)} ${f(y - s)} L ${f(x + s)} ${f(y + s)} M ${f(x + s)} ${f(y - s)} L ${f(x - s)} ${f(y + s)}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
  const check = (x, y, s = 24, col = C.grn, w = 8) => `<path d="M ${f(x - s)} ${f(y)} L ${f(x - s * .3)} ${f(y + s * .7)} L ${f(x + s)} ${f(y - s * .8)}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const spark = (x, y, k, col = C.yel, n = 6, L = 20) => { let s = ''; for (let i = 0; i < n; i++) { const a = rad(i * 360 / n + k * 40); s += `<line x1="${f(x + Math.cos(a) * 6)}" y1="${f(y + Math.sin(a) * 6)}" x2="${f(x + Math.cos(a) * L)}" y2="${f(y + Math.sin(a) * L)}" stroke="${col}" stroke-width="4" stroke-linecap="round"/>`; } return s; };
  const emoji = (x, y, s, name) => `<image href="assets/emoji/${name}.png" x="${f(x - s / 2)}" y="${f(y - s / 2)}" width="${s}" height="${s}"/>`;

  // ---------- generic gauge (used by the gauge card) ----------
  function _gauge(fr, zones, ends, mid) {
    const cx = 298, cy = 262, R = 214; let s = '';
    const arc = (a0, a1, r, col, w) => { const [x0, y0] = P2(cx, cy, r, a0), [x1, y1] = P2(cx, cy, r, a1); return `<path d="M ${f(x0)} ${f(y0)} A ${r} ${r} 0 0 1 ${f(x1)} ${f(y1)}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="butt"/>`; };
    s += arc(Math.PI, 2 * Math.PI, R, 'rgba(255,255,255,.08)', 34);
    zones.forEach(([a, b, col]) => { s += arc(Math.PI + a * Math.PI, Math.PI + b * Math.PI, R, col, 30); });
    for (let i = 0; i <= 20; i++) { const a = Math.PI + i / 20 * Math.PI; const big = i % 5 === 0; const [x0, y0] = P2(cx, cy, R - 30, a), [x1, y1] = P2(cx, cy, R - (big ? 58 : 44), a);
      s += `<line x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}" stroke="${C.w}" stroke-width="${big ? 5 : 3}" opacity="${big ? .9 : .5}"/>`; }
    s += T(cx - R + 10, cy + 34, ends[0], { s: 22, c: C.dim, a: 'middle' }) + T(cx + R - 10, cy + 34, ends[1], { s: 22, c: C.dim, a: 'middle' });
    if (mid) s += T(cx, cy - 92, mid, { s: 22, c: C.dim, a: 'middle' });
    const a = Math.PI + cl(fr, 0, 1.02) * Math.PI; const [nx, ny] = P2(cx, cy, R - 40, a); const [bx1, by1] = P2(cx, cy, 16, a + Math.PI / 2), [bx2, by2] = P2(cx, cy, 16, a - Math.PI / 2);
    const ncol = fr > .8 ? C.red : fr > .6 ? C.yel : C.w;
    s += `<path d="M ${f(bx1)} ${f(by1)} L ${f(nx)} ${f(ny)} L ${f(bx2)} ${f(by2)} Z" fill="${ncol}" stroke="#000" stroke-opacity=".4" stroke-width="2"/>`;
    s += `<circle cx="${cx}" cy="${cy}" r="24" fill="#0B1F36" stroke="${C.w}" stroke-width="5"/>`;
    return s;
  }

  // ---------- shared turbo core (side section) ----------
  function turboCore(dx, dy, rot, opt = {}) {
    // housing (fixed), rotating assembly offset by dx,dy (and rot for broken part)
    let s = '';
    const yc = 215; // shaft centre line
    // compressor housing (left) & turbine housing (right) – fixed outlines
    s += `<path d="M 262 108 C 190 96 118 116 98 168 L 98 262 C 118 314 190 334 262 322" fill="none" stroke="${C.cyD}" stroke-width="6"/>`;
    s += `<path d="M 652 108 C 724 96 796 116 816 168 L 816 262 C 796 314 724 334 652 322" fill="none" stroke="${C.cyD}" stroke-width="6"/>`;
    s += T(150, 368, 'COMPRESOR', { s: 17, c: C.dim, a: 'middle' }) + T(764, 368, 'TURBINĂ', { s: 17, c: C.dim, a: 'middle' });
    // bearing housing (fixed)
    s += `<rect x="352" y="146" width="210" height="138" rx="18" fill="${C.body}" stroke="${C.cy}" stroke-width="4"/>`;
    s += `<rect x="440" y="104" width="34" height="46" fill="${opt.oilFeed ? C.oil : C.body2}" stroke="${C.cy}" stroke-width="3"/>`;
    s += `<rect x="440" y="282" width="34" height="34" fill="${C.body2}" stroke="${C.cy}" stroke-width="3"/>`;
    // seals at both ends (housing bore)
    const sc = opt.sealBad ? C.red : C.grn;
    s += `<rect x="350" y="${yc - 20}" width="8" height="40" fill="${sc}"/><rect x="556" y="${yc - 20}" width="8" height="40" fill="${sc}"/>`;
    // rotating assembly
    const brk = opt.breakX; // x of the break (turbine side moves with rot)
    const g1 = `<g transform="translate(${f(dx)} ${f(dy)})">`;
    let a = '';
    // shaft
    a += `<rect x="236" y="${yc - 9}" width="${brk ? brk - 236 : 446}" height="18" rx="4" fill="${C.steel}" stroke="${C.steelD}" stroke-width="2"/>`;
    // bearings (journal) – drawn with the shaft for clarity
    const bc = opt.bearBad ? C.red : C.body2;
    a += `<rect x="382" y="${yc - 26}" width="34" height="52" rx="5" fill="${bc}" stroke="${C.cy}" stroke-width="2.5"/><rect x="500" y="${yc - 26}" width="34" height="52" rx="5" fill="${bc}" stroke="${C.cy}" stroke-width="2.5"/>`;
    // compressor wheel (left)
    const spin = (opt.spin || 0);
    a += `<path d="M 248 ${yc - 70} L 248 ${yc + 70} L 172 ${yc + 46} Q 150 ${yc} 172 ${yc - 46} Z" fill="${C.body2}" stroke="${C.cy}" stroke-width="3.5"/>`;
    for (let i = 0; i < 5; i++) { const yy = yc - 56 + ((i * 28 + spin * 140) % 140); a += `<line x1="170" y1="${f(yc + (yy - yc) * .6)}" x2="246" y2="${f(yy)}" stroke="${C.cy}" stroke-width="2.5" opacity=".7"/>`; }
    let b = '';
    if (!brk) {
      b += `<path d="M 666 ${yc - 70} L 666 ${yc + 70} L 742 ${yc + 46} Q 764 ${yc} 742 ${yc - 46} Z" fill="${C.body2}" stroke="${C.cy}" stroke-width="3.5"/>`;
      for (let i = 0; i < 5; i++) { const yy = yc - 56 + ((i * 28 + spin * 140) % 140); b += `<line x1="744" y1="${f(yc + (yy - yc) * .6)}" x2="668" y2="${f(yy)}" stroke="${C.cy}" stroke-width="2.5" opacity=".7"/>`; }
      s += g1 + a + b + '</g>';
    } else {
      // broken: turbine side rotates down around the break point
      b += `<rect x="${brk + 6}" y="${yc - 9}" width="${682 - brk - 6}" height="18" rx="4" fill="${C.steel}" stroke="${C.steelD}" stroke-width="2"/>`;
      b += `<path d="M 666 ${yc - 70} L 666 ${yc + 70} L 742 ${yc + 46} Q 764 ${yc} 742 ${yc - 46} Z" fill="${C.body2}" stroke="${C.red}" stroke-width="3.5"/>`;
      s += g1 + a + '</g>' + `<g transform="translate(${f(dx)} ${f(dy + (opt.drop || 0))}) rotate(${f(rot)} ${brk} ${yc})">` + b + '</g>';
      // crack zigzag
      s += `<path d="M ${brk - 2} ${yc - 16} L ${brk + 6} ${yc - 6} L ${brk - 4} ${yc + 2} L ${brk + 7} ${yc + 16}" fill="none" stroke="${C.red}" stroke-width="4" stroke-linejoin="round"/>`;
    }
    return s;
  }

  // 1) turbo axial / radial play -> broken core (Ford Transit)
  function turboPlay(tl, ph, pt, P) {
    let s = ''; const r = eo(pt / .35);
    let dx = 0, dy = 0, rot = 0, dropY = 0;
    if (ph === 1) dx = 11 * Math.sin(pt * 11) * r;
    if (ph === 2) dy = 9 * Math.sin(pt * 13) * r;
    const broken = ph >= 3;
    if (broken) { rot = 9 * eo(pt / .45); dropY = 10 * eo(pt / .45); }
    s += turboCore(dx, dy, rot, { spin: broken ? 0 : tl * 2.4, breakX: broken ? 610 : 0, drop: dropY, sealBad: ph >= 3, bearBad: ph >= 1, oilFeed: true });
    s += T(457, 92, 'ULEI', { s: 17, c: C.oil, a: 'middle' });
    s += tag(457, 330 + 34, 'LAGĂRE', ph >= 1 ? C.red : C.cy, 'middle', 18);
    if (ph === 0) { s += tag(250, 48, 'AXUL TURBINEI (MIEZ)', C.cy, 'middle', 19); s += ARW(250, 66, 300, 204, C.cy, 3); }
    if (ph === 1) { s += DBL(300 + dx, 52, 614 + dx, 52, C.red, 5); s += tag(457 + dx, 52, 'JOC AXIAL', C.red, 'middle', 22); s += T(457, 404, 'AXUL SE MIȘCĂ PE LUNGIME (FAȚĂ-SPATE)', { s: 19, c: C.dim, a: 'middle' }); }
    if (ph === 2) { s += DBL(126, 120 + dy, 126, 310 + dy, C.red, 5) + DBL(788, 120 + dy, 788, 310 + dy, C.red, 5); s += tag(457, 52, 'JOC RADIAL', C.red, 'middle', 22);
      if (Math.abs(Math.sin(pt * 13)) > .85) { s += spark(176, 160 + dy, pt * 10, C.yel, 5, 18) + spark(740, 270 + dy, pt * 10 + 2, C.yel, 5, 18); }
      s += T(457, 404, 'AXUL SE MIȘCĂ LATERAL → ROȚILE ATING CARCASA', { s: 19, c: C.dim, a: 'middle' }); }
    if (broken) {
      const fl = Math.max(0, 1 - pt * 2); if (fl > 0) s += glowC(610, 215, 40 + 60 * (1 - fl), C.red, .5 * fl);
      s += tag(610, 52, 'MIEZ RUPT', C.red, 'middle', 24);
      for (let i = 0; i < 8; i++) { const k = ((pt * .9 + i / 8) % 1); const side = i % 2 ? 1 : -1; const x0 = side < 0 ? 350 : 564; s += drop(x0 + side * k * 120, 215 + 40 * k * k + (i % 3) * 8, 6, C.oil, 1 - k); }
      s += T(457, 404, 'PIERDERI DE ULEI PRIN ETANȘĂRI', { s: 19, c: C.oil, a: 'middle' });
    }
    return s;
  }

  // 2) turbo oil seals leak (Ford Focus)
  function turboOil(tl, ph, pt, P) {
    let s = turboCore(0, 0, 0, { spin: tl * 2.4, sealBad: ph >= 1, oilFeed: true });
    // oil circulation in centre housing
    for (let i = 0; i < 6; i++) { const k = ((tl * .8 + i / 6) % 1); const y = 110 + k * 200; s += drop(457, y, 6, C.oil, ph >= 1 ? .6 : .95); }
    s += T(492, 120, 'ULEI SPRE LAGĂRE', { s: 16, c: C.oil }) + T(492, 312, 'RETUR ÎN BAIE', { s: 16, c: C.oil });
    if (ph >= 1) {
      for (let i = 0; i < 10; i++) { const k = ((pt * .8 + i / 10) % 1); const side = i % 2 ? 1 : -1; const x0 = side < 0 ? 350 : 564; s += drop(x0 + side * k * 150, 215 + (i % 4 - 1.5) * 10, 6, C.oil, 1 - k * .8); }
      s += tag(457, 52, 'ETANȘĂRI UZATE', C.red, 'middle', 22);
    }
    if (ph >= 2) {
      s += tag(170, 404, 'ULEI ÎN ADMISIE', C.oil, 'middle', 18) + tag(720, 404, 'ULEI ÎN EVACUARE / DPF', C.oil, 'middle', 18);
      for (let i = 0; i < 5; i++) { const k = ((pt * .6 + i / 5) % 1); s += glowC(840 + k * 40, 180 - k * 120, 14 + k * 26, C.smoke, .35 * (1 - k)); }
    }
    return s;
  }

  // 3) injector over-fuelling -> melted / cracked piston (Suzuki SX4)
  function injectorSpray(tl, ph, pt, P) {
    let s = ''; const x0 = 307, x1 = 607, cx = 457;
    // head + walls
    s += `<rect x="250" y="40" width="414" height="64" fill="${C.body}" stroke="${C.cy}" stroke-width="4"/>`;
    s += `<line x1="${x0}" y1="104" x2="${x0}" y2="420" stroke="${C.cy}" stroke-width="6"/><line x1="${x1}" y1="104" x2="${x1}" y2="420" stroke="${C.cy}" stroke-width="6"/>`;
    // injector
    s += `<rect x="${cx - 16}" y="0" width="32" height="98" rx="6" fill="${C.steelD}" stroke="${ph >= 1 ? C.red : C.cy}" stroke-width="3"/><path d="M ${cx - 9} 98 L ${cx + 9} 98 L ${cx} 116 Z" fill="${C.steel}"/>`;
    s += tag(cx + 120, 30, 'INJECTOR', ph >= 1 ? C.red : C.cy, 'middle', 18);
    s += T(x0 - 14, 140, 'CILINDRUL 3', { s: 18, c: C.dim, a: 'end' });
    // piston (slight motion)
    const py = 262 + 10 * Math.sin(tl * 3.2) * (ph >= 3 ? 0 : 1);
    const heat = ph >= 2 ? eo(pt / 1.2) : 0; const melted = ph >= 3;
    const crown = heat > 0 ? `rgb(${Math.round(lerp(169, 255, heat))},${Math.round(lerp(188, 110, heat))},${Math.round(lerp(208, 40, heat))})` : C.steel;
    let top = `M ${x0 + 5} ${py} L ${cx - 70} ${py} Q ${cx} ${py + 46} ${cx + 70} ${py} L ${x1 - 5} ${py}`;
    if (melted) top = `M ${x0 + 5} ${py} L ${cx - 120} ${py} L ${cx - 104} ${py + 22} L ${cx - 86} ${py + 8} L ${cx - 70} ${py + 30} Q ${cx} ${py + 46} ${cx + 70} ${py} L ${x1 - 5} ${py}`;
    s += `<path d="${top} L ${x1 - 5} ${py + 150} L ${x0 + 5} ${py + 150} Z" fill="${crown}" stroke="${melted ? C.red : C.steelD}" stroke-width="3"/>`;
    for (let i = 0; i < 3; i++) s += `<line x1="${x0 + 5}" y1="${py + 22 + i * 12}" x2="${x1 - 5}" y2="${py + 22 + i * 12}" stroke="${C.steelD}" stroke-width="3"/>`;
    s += T(x1 + 18, py + 70, 'PISTON', { s: 18, c: C.dim });
    if (melted) { s += `<path d="M ${cx - 96} ${py + 16} L ${cx - 80} ${py + 52} L ${cx - 98} ${py + 80} L ${cx - 78} ${py + 118} L ${cx - 92} ${py + 148}" fill="none" stroke="${C.red}" stroke-width="5" stroke-linejoin="round"/>`;
      s += tag(160, py + 70, 'TOPIT + CRĂPAT', C.red, 'middle', 20); }
    if (heat > 0 && !melted) for (let i = 0; i < 4; i++) { const k = ((tl * 1.2 + i / 4) % 1); s += `<path d="M ${cx - 90 + i * 60} ${py - 6 - k * 40} q 8 -10 0 -20 q -8 -10 0 -20" fill="none" stroke="${C.org}" stroke-width="3" opacity="${f(1 - k)}"/>`; }
    // spray jets
    if (!melted) {
      const heavy = ph >= 1; const angs = [-62, -38, -14, 14, 38, 62]; const L = heavy ? (py - 116) / Math.cos(rad(14)) + 8 : 70; const n = heavy ? 9 : 5;
      const cyc = (tl * (heavy ? 2.2 : 3)) % 1; const show = heavy || cyc < .45;
      if (show) angs.forEach((ad, j) => { const a = rad(90 + ad); for (let i = 0; i < n; i++) { const k = (i + 1) / n; const rr = (heavy ? 5.5 : 3) * (heavy ? 1 : (1 - k * .5));
        const len = Math.min(L, Math.abs(ad) > 40 ? L * .85 : L); const x = cx + Math.cos(a) * len * k * (heavy ? 1 : cyc / .45 + .2), y = 116 + Math.sin(a) * len * k * (heavy ? 1 : cyc / .45 + .2);
        s += `<circle cx="${f(x)}" cy="${f(y)}" r="${f(rr)}" fill="${heavy ? C.yel : '#A5E9FF'}" opacity="${heavy ? .9 : .8}"/>`; } });
      if (!heavy && cyc > .4 && cyc < .7) { const q = Math.sin((cyc - .4) / .3 * Math.PI); s += `<ellipse cx="${cx}" cy="${f((116 + py) / 2)}" rx="${f(70 + 50 * q)}" ry="${f((py - 116) / 3)}" fill="#FFB347" opacity="${f(.5 * q)}"/><ellipse cx="${cx}" cy="${f((116 + py) / 2)}" rx="${f(30 + 30 * q)}" ry="${f((py - 116) / 6)}" fill="#FFE8A3" opacity="${f(.6 * q)}"/>`; s += T(cx + 200, 200, 'ARDERE NORMALĂ', { s: 16, c: C.dim, a: 'middle' }); }
      if (heavy) { s += tag(160, 200, 'PREA MULTĂ MOTORINĂ', C.yel, 'middle', 18); s += `<ellipse cx="${cx}" cy="${f(py + 6)}" rx="140" ry="9" fill="${C.yel}" opacity=".55"/>`; }
    } else {
      for (let i = 0; i < 7; i++) { const k = ((pt * .5 + i / 7) % 1); s += glowC(cx + (rnd(i) - .5) * 160 + k * 140, 220 - k * 170, 16 + k * 28, C.smoke, .45 * (1 - k)); }
      s += tag(cx + 230, 150, 'FUM ALBASTRU', C.smoke, 'middle', 18);
    }
    return s;
  }

  // 4) timing chain: tensioner fails -> chain goes slack -> skips a tooth -> engine out of time (Dacia 1.0 TCe)
  function chainSkip(tl, ph, pt, P) {
    let s = ''; const A = [360, 112], B = [614, 112], Cc = [487, 350], RA = 56, RC = 40;
    const skip = ph >= 2 ? 16 * eo(pt / .25) + (ph === 2 ? 3 * Math.exp(-pt * 6) * Math.sin(pt * 40) : 0) : 0;
    const run = ph >= 3 ? 0 : tl;
    const sprocket = (c, R, ang, col) => { let g = `<circle cx="${c[0]}" cy="${c[1]}" r="${R}" fill="${C.body}" stroke="${col}" stroke-width="4"/>`;
      for (let i = 0; i < 16; i++) { const a = rad(ang + i * 22.5); const [x0, y0] = P2(c[0], c[1], R - 2, a), [x1, y1] = P2(c[0], c[1], R + 7, a); g += `<line x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}" stroke="${col}" stroke-width="5"/>`; }
      g += `<circle cx="${c[0]}" cy="${c[1]}" r="${R * .3}" fill="${C.body2}" stroke="${col}" stroke-width="3"/>`; return g; };
    const camAng = run * 60 + skip, crankAng = run * 120;
    // left (slack-side) run between left cam and crank, with the tensioner pushing on it
    const P1 = [A[0] - RA - 6, A[1]], P2r = [Cc[0] - RC - 6, Cc[1]];
    const dx = P2r[0] - P1[0], dy = P2r[1] - P1[1], L = Math.hypot(dx, dy); const d = [dx / L, dy / L], n = [-d[1], d[0]]; // n points outward (left)
    const M = [(P1[0] + P2r[0]) / 2, (P1[1] + P2r[1]) / 2];
    const slack = ph === 0 ? 0 : (ph === 1 ? eo(pt / .5) : 1);
    let off = lerp(-12, 46, slack); if (ph >= 1 && ph < 3) off += (ph === 1 ? 10 : 6) * Math.sin(pt * 17) * (ph === 2 ? Math.exp(-pt * .8) + .3 : 1);
    const Cq = [M[0] + n[0] * off * 2, M[1] + n[1] * off * 2];
    const chainCol = ph >= 1 ? C.yel : C.steel;
    const path = `M ${A[0]} ${A[1] - RA - 6} L ${B[0]} ${B[1] - RA - 6} A ${RA + 6} ${RA + 6} 0 0 1 ${B[0] + RA + 6} ${B[1]} L ${Cc[0] + RC + 6} ${Cc[1]} A ${RC + 6} ${RC + 6} 0 0 1 ${f(P2r[0])} ${f(P2r[1])} Q ${f(Cq[0])} ${f(Cq[1])} ${f(P1[0])} ${f(P1[1])} A ${RA + 6} ${RA + 6} 0 0 1 ${A[0]} ${A[1] - RA - 6} Z`;
    s += `<path d="${path}" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="15"/><path d="${path}" fill="none" stroke="${chainCol}" stroke-width="9" stroke-dasharray="12 6" stroke-dashoffset="${f(-run * 90)}"/>`;
    s += sprocket(A, RA, camAng, C.cy) + sprocket(B, RA, camAng, C.cy) + sprocket(Cc, RC, crankAng, C.cy);
    // tensioner: shoe follows the run when healthy; retracted (failed) when slack
    const shoeOff = ph === 0 ? -12 + 14 : lerp(2, 78, slack);
    const S1 = [P1[0] + d[0] * 46 + n[0] * shoeOff, P1[1] + d[1] * 46 + n[1] * shoeOff], S2 = [P2r[0] - d[0] * 46 + n[0] * shoeOff, P2r[1] - d[1] * 46 + n[1] * shoeOff];
    const SM = [M[0] + n[0] * (shoeOff + (ph === 0 ? -12 : 0) * 2) , M[1] + n[1] * (shoeOff + (ph === 0 ? -12 : 0) * 2)];
    const sc = ph >= 1 ? C.red : C.grn;
    s += `<path d="M ${f(S1[0])} ${f(S1[1])} Q ${f(SM[0])} ${f(SM[1])} ${f(S2[0])} ${f(S2[1])}" fill="none" stroke="${sc}" stroke-width="13" stroke-linecap="round"/>`;
    const SB = [M[0] + n[0] * (shoeOff + 6), M[1] + n[1] * (shoeOff + 6)]; const body = [M[0] + n[0] * 150, M[1] + n[1] * 150];
    s += `<line x1="${f(SB[0])}" y1="${f(SB[1])}" x2="${f(body[0])}" y2="${f(body[1])}" stroke="${C.steel}" stroke-width="10"/>`;
    s += `<g transform="translate(${f(body[0])} ${f(body[1])}) rotate(${f(Math.atan2(n[1], n[0]) * 180 / Math.PI)})"><rect x="-6" y="-26" width="82" height="52" rx="8" fill="${C.body2}" stroke="${ph >= 1 ? C.red : C.cy}" stroke-width="4"/></g>`;
    s += tag(body[0] - 10, body[1] + 62, 'ÎNTINZĂTOR', ph >= 1 ? C.red : C.cy, 'middle', 18);
    if (ph === 0) s += ARW(body[0] - n[0] * 30, body[1] - n[1] * 30, SB[0] + n[0] * 22, SB[1] + n[1] * 22, C.grn, 5);
    // timing marks
    const mark = (c, R, ang) => { const a = rad(ang - 90); const [x, y] = P2(c[0], c[1], R - 14, a); return `<circle cx="${f(x)}" cy="${f(y)}" r="8" fill="${C.yel}"/><line x1="${c[0]}" y1="${f(c[1] - R - 30)}" x2="${c[0]}" y2="${f(c[1] - R - 12)}" stroke="${C.w}" stroke-width="5" stroke-linecap="round"/>`; };
    s += mark(A, RA, ph < 2 ? 0 : skip) + mark(B, RA, ph < 2 ? 0 : skip) + mark(Cc, RC, 0);
    s += T(A[0], 26, 'AX CU CAME', { s: 16, c: C.dim, a: 'middle' }) + T(B[0], 26, 'AX CU CAME', { s: 16, c: C.dim, a: 'middle' }) + T(Cc[0], 422, 'ARBORE COTIT', { s: 16, c: C.dim, a: 'middle' });
    if (ph === 0) s += tag(790, 250, 'SINCRONIZAT', C.grn, 'middle', 22);
    if (ph === 1) s += tag(790, 250, 'LANȚ SLĂBIT', C.red, 'middle', 22);
    if (ph >= 2) { [A, B].forEach(c => { const a0 = rad(-90), a1 = rad(skip - 90); const [x0, y0] = P2(c[0], c[1], RA + 22, a0), [x1, y1] = P2(c[0], c[1], RA + 22, a1); s += `<path d="M ${f(x0)} ${f(y0)} A ${RA + 22} ${RA + 22} 0 0 1 ${f(x1)} ${f(y1)}" fill="none" stroke="${C.red}" stroke-width="6"/>`; });
      s += tag(790, 222, 'A SĂRIT UN DINTE', C.red, 'middle', 20) + tag(790, 276, 'DEFAZAT', C.red, 'middle', 20); }
    if (ph >= 3) { s += xmark(Cc[0], Cc[1], 30, C.red, 10); s += tag(790, 340, 'NU MAI PORNEȘTE', C.red, 'middle', 21); }
    return s;
  }

  // 5) wastegate flap ("bănuț") worn -> rattles -> exhaust bypasses turbine -> underboost
  function wastegate(tl, ph, pt, P) {
    let s = ''; const wc = [300, 210];
    // turbine housing scroll + wheel
    s += `<path d="M 300 70 A 140 140 0 1 1 186 300" fill="none" stroke="${C.cy}" stroke-width="7"/>`;
    s += `<path d="M 60 360 L 186 300" stroke="${C.cy}" stroke-width="7"/><path d="M 60 410 L 230 330" stroke="${C.cy}" stroke-width="7"/>`;
    const slow = ph >= 2 ? .35 : ph === 1 ? .8 : 1; const ang = tl * 400 * slow;
    s += `<circle cx="${wc[0]}" cy="${wc[1]}" r="76" fill="${C.body}" stroke="${C.cy}" stroke-width="4"/>`;
    for (let i = 0; i < 9; i++) { const a = rad(ang + i * 40); const [x0, y0] = P2(wc[0], wc[1], 20, a), [x1, y1] = P2(wc[0], wc[1], 70, a + .5); s += `<path d="M ${f(x0)} ${f(y0)} Q ${f(wc[0] + Math.cos(a + .2) * 52)} ${f(wc[1] + Math.sin(a + .2) * 52)} ${f(x1)} ${f(y1)}" fill="none" stroke="${C.cy}" stroke-width="4"/>`; }
    s += T(wc[0], 395, 'TURBINĂ', { s: 17, c: C.dim, a: 'middle' });
    // outlet pipe
    s += `<path d="M 440 150 L 860 150 M 440 270 L 860 270" stroke="${C.cy}" stroke-width="7"/>`;
    // wastegate port + flap
    const open = ph === 0 ? 0 : ph === 1 ? 4 + 5 * Math.abs(Math.sin(pt * 22)) : 26 + 4 * Math.sin(pt * 18);
    s += `<rect x="500" y="270" width="64" height="16" fill="${C.body2}" stroke="${C.cy}" stroke-width="3"/>`;
    s += `<g transform="rotate(${f(-open)} 498 278)"><rect x="498" y="262" width="74" height="14" rx="5" fill="${ph >= 1 ? C.red : C.steel}"/><circle cx="498" cy="278" r="7" fill="${C.w}"/></g>`;
    s += `<line x1="572" y1="300" x2="700" y2="380" stroke="${C.steel}" stroke-width="6"/><rect x="690" y="350" width="120" height="70" rx="14" fill="${C.body}" stroke="${C.cyD}" stroke-width="3"/>`;
    s += T(750, 392, 'ACTUATOR', { s: 15, c: C.dim, a: 'middle' });
    s += tag(536, 330, 'BĂNUȚ (CLAPETĂ)', ph >= 1 ? C.red : C.cy, 'middle', 17);
    if (ph === 1) for (let i = 0; i < 3; i++) s += `<path d="M ${590 + i * 16} ${236 - i * 4} l 8 -8 l -8 -8 l 8 -8" fill="none" stroke="${C.yel}" stroke-width="3" opacity="${f(.5 + .5 * Math.sin(pt * 30 + i))}"/>`;
    // gas particles: through wheel (main) or bypass
    const bypassShare = ph === 0 ? 0 : ph === 1 ? .3 : .75;
    for (let i = 0; i < 14; i++) { const k = ((tl * (0.7 + .1 * (i % 3)) + i / 14) % 1); const by = rnd(i) < bypassShare;
      let x, y; if (!by) { if (k < .4) { x = lerp(80, 210, k / .4); y = lerp(380, 310, k / .4); } else if (k < .7) { const a = rad(lerp(150, 330, (k - .4) / .3)); x = wc[0] + Math.cos(a) * 100; y = wc[1] + Math.sin(a) * 100; } else { x = lerp(400, 860, (k - .7) / .3); y = 210; } }
      else { if (k < .5) { x = lerp(80, 520, k / .5); y = lerp(390, 300, k / .5); } else { x = lerp(540, 860, (k - .5) / .5); y = lerp(290, 240, (k - .5) / .5); } }
      s += `<circle cx="${f(x)}" cy="${f(y)}" r="7" fill="${by ? C.org : C.smoke}" opacity=".85"/>`; }
    // mini boost gauge
    const fr = ph === 0 ? .62 + .03 * Math.sin(tl * 3) : ph === 1 ? .5 : lerp(.5, .18, eo(pt / .8));
    s += `<g transform="translate(694 6) scale(.36)">${_gauge(fr, [[0, .35, '#FF4B4B'], [.35, .8, '#4ADE80'], [.8, 1, '#FFD21F']], ['MIN', 'MAX'], '')}</g>`;
    s += T(802, 128, 'PRESIUNE TURBO', { s: 15, c: C.dim, a: 'middle' });
    s += T(60, 424, 'GAZE DE EVACUARE', { s: 15, c: C.dim }) + T(860, 196, 'SPRE EVACUARE', { s: 15, c: C.dim, a: 'end' });
    if (ph >= 2) { s += tag(470, 60, 'UNDERBOOST', C.red, 'middle', 24); s += tag(640, 236, 'GAZELE OCOLESC TURBINA', C.org, 'middle', 16); }
    if (ph === 1) s += tag(470, 60, 'SUNET METALIC', C.yel, 'middle', 22);
    if (ph === 0) s += tag(470, 60, 'GAZELE ROTESC TURBINA', C.grn, 'middle', 19);
    return s;
  }

  // 6) overheating -> piston expands -> oil film breaks -> scuffing -> seized (Dacia Dokker)
  function pistonSeize(tl, ph, pt, P) {
    let s = ''; const x0 = 300, x1 = 614;
    s += `<line x1="${x0}" y1="40" x2="${x0}" y2="410" stroke="${C.cy}" stroke-width="7"/><line x1="${x1}" y1="40" x2="${x1}" y2="410" stroke="${C.cy}" stroke-width="7"/>`;
    const heat = ph >= 1 ? (ph === 1 ? eo(pt / 1.2) : 1) : 0;
    const gap = lerp(9, 0, heat); const seized = ph >= 3;
    const y = seized ? 190 + 3 * Math.sin(pt * 50) * Math.exp(-pt * 4) : 190 + 60 * Math.sin(tl * 4.2 * (ph === 2 ? .7 : 1));
    const col = `rgb(${Math.round(lerp(169, 255, heat))},${Math.round(lerp(188, 118, heat))},${Math.round(lerp(208, 52, heat))})`;
    s += `<rect x="${f(x0 + 4 + gap)}" y="${f(y)}" width="${f(x1 - x0 - 8 - 2 * gap)}" height="150" rx="6" fill="${col}" stroke="${seized ? C.red : C.steelD}" stroke-width="4"/>`;
    for (let i = 0; i < 3; i++) s += `<line x1="${f(x0 + 4 + gap)}" y1="${f(y + 18 + i * 12)}" x2="${f(x1 - 4 - gap)}" y2="${f(y + 18 + i * 12)}" stroke="${C.steelD}" stroke-width="3"/>`;
    s += `<rect x="${f(x0 + 70)}" y="${f(y + 150)}" width="${f(x1 - x0 - 140)}" height="70" fill="${C.steelD}" opacity=".7"/>`;
    // oil film
    const film = ph <= 1 ? 1 : ph === 2 ? 1 - eo(pt / .8) : 0;
    if (film > 0) { s += `<rect x="${x0 + 4}" y="40" width="5" height="370" fill="${C.oil}" opacity="${f(film)}"/><rect x="${x1 - 9}" y="40" width="5" height="370" fill="${C.oil}" opacity="${f(film)}"/>`; }
    if (ph >= 2) for (let i = 0; i < 9; i++) { const yy = 70 + i * 36; const k = cl((pt - i * .05) / .3); s += `<path d="M ${x0 + 3} ${yy} l 6 10 l -6 10 l 6 10" fill="none" stroke="${C.red}" stroke-width="3" opacity="${f(k)}"/><path d="M ${x1 - 3} ${yy + 14} l -6 10 l 6 10 l -6 10" fill="none" stroke="${C.red}" stroke-width="3" opacity="${f(k)}"/>`; }
    // labels
    s += T(x0 - 16, 70, 'CILINDRU', { s: 18, c: C.dim, a: 'end' });
    if (ph === 0) { s += DBL(x0 + 4, 120, x0 + 30, 120, C.yel, 3); s += tag(x0 - 90, 120, 'JOC + ULEI', C.yel, 'middle', 17); }
    if (ph <= 1) s += tag(x0 - 130, 300, 'PELICULĂ DE ULEI', C.oil, 'middle', 16);
    if (ph === 1) s += tag(457, 36, 'PISTONUL SE DILATĂ', C.org, 'middle', 21);
    if (ph === 2) s += tag(457, 36, 'ZGÂRIETURI PE CILINDRU', C.red, 'middle', 21);
    if (seized) s += tag(457, 36, 'PISTON BLOCAT (GRIPAT)', C.red, 'middle', 22);
    // thermometer
    const tx = 800; s += `<rect x="${tx - 16}" y="60" width="32" height="270" rx="16" fill="${C.body}" stroke="${C.cy}" stroke-width="3"/><circle cx="${tx}" cy="350" r="34" fill="${heat > .6 ? C.red : C.org}" stroke="${C.cy}" stroke-width="3"/>`;
    const lev = lerp(.35, 1, heat) * (1 + .02 * Math.sin(tl * 9)); s += `<rect x="${tx - 9}" y="${f(330 - 262 * lev)}" width="18" height="${f(262 * lev)}" rx="9" fill="${heat > .6 ? C.red : C.org}"/>`;
    s += T(tx, 40, heat > .6 ? 'TEMPERATURĂ CRITICĂ' : 'TEMPERATURĂ', { s: 15, c: heat > .6 ? C.red : C.dim, a: 'middle' });
    return s;
  }

  // 7) system status map (Ford Focus: intake, injectors, exhaust, turbo, DPF)
  function systemMap(tl, ph, pt, P, t) {
    let s = ''; const N = P.nodes; // [[x,y,label,emoji]]
    const st = N.map(() => 'n'); (P.events || []).forEach(([te, i, v]) => { if (t >= te) st[i] = v; });
    const colOf = v => v === 'bad' ? C.red : v === 'ok' ? C.grn : v === 'lab' ? '#38BDF8' : C.cy;
    (P.links || []).forEach(([a, b, dashed]) => { const [xa, ya] = N[a], [xb, yb] = N[b]; const ang = Math.atan2(yb - ya, xb - xa); const ox = Math.cos(ang), oy = Math.sin(ang);
      const sx = xa + ox * 122 * Math.abs(ox) + 0, sy = ya + oy * 50, ex = xb - ox * 122 * Math.abs(ox), ey = yb - oy * 50;
      s += ARW(sx, sy, ex, ey, dashed ? C.dim : C.cyD, 5, 16);
      for (let i = 0; i < 3; i++) { const k = ((tl * .6 + i / 3) % 1); s += `<circle cx="${f(lerp(sx, ex, k))}" cy="${f(lerp(sy, ey, k))}" r="6" fill="${C.cy}" opacity=".8"/>`; } });
    N.forEach(([x, y, lab, em], i) => { const c = colOf(st[i]); const pulse = st[i] === 'bad' ? 1 + .04 * Math.sin(tl * 8) : 1;
      s += `<g transform="translate(${x} ${y}) scale(${f(pulse)})"><rect x="-118" y="-46" width="236" height="92" rx="18" fill="${C.body}" stroke="${c}" stroke-width="5"/>` + emoji(-80, 0, 52, em) + T(-44, 9, lab, { s: 22, c: C.w }) + '</g>';
      const bx = x + 104, by = y - 40; if (st[i] === 'bad') s += `<circle cx="${bx}" cy="${by}" r="20" fill="${C.red}"/>` + T(bx, by + 8, '!', { s: 26, a: 'middle', c: '#fff' });
      if (st[i] === 'ok') s += `<circle cx="${bx}" cy="${by}" r="20" fill="${C.grn}"/>` + check(bx, by, 10, '#fff', 5);
      if (st[i] === 'lab') s += `<circle cx="${bx}" cy="${by}" r="20" fill="#38BDF8"/>` + T(bx, by + 7, 'L', { s: 22, a: 'middle', c: '#fff' }); });
    return s;
  }

  // 8) oil burning paths: worn rings (from below) + valve stem seals (from above) (Suzuki SX4)
  function oilPaths(tl, ph, pt, P) {
    let s = ''; const x0 = 300, x1 = 614;
    // head with valve
    s += `<rect x="240" y="20" width="434" height="110" fill="${C.body}" stroke="${C.cy}" stroke-width="4"/>`;
    s += `<rect x="548" y="20" width="24" height="98" fill="${C.body2}" stroke="${C.cyD}" stroke-width="2"/>`; // guide
    s += `<rect x="554" y="10" width="12" height="150" fill="${C.steel}"/><path d="M 512 160 L 608 160 L 590 148 L 530 148 Z" fill="${C.steel}"/>`;
    s += `<rect x="542" y="40" width="36" height="14" rx="4" fill="${ph >= 2 ? C.red : C.grn}"/>`;
    s += tag(700, 46, 'SEMERING SUPAPĂ', ph >= 2 ? C.red : C.cy, 'start', 16);
    // cylinder + piston
    s += `<line x1="${x0}" y1="130" x2="${x0}" y2="420" stroke="${C.cy}" stroke-width="6"/><line x1="${x1}" y1="130" x2="${x1}" y2="420" stroke="${C.cy}" stroke-width="6"/>`;
    const py = 250 + 8 * Math.sin(tl * 3);
    s += `<rect x="${x0 + 5}" y="${f(py)}" width="${x1 - x0 - 10}" height="120" rx="6" fill="${C.steel}" stroke="${C.steelD}" stroke-width="3"/>`;
    for (let i = 0; i < 3; i++) s += `<rect x="${x0 + 5}" y="${f(py + 14 + i * 13)}" width="${x1 - x0 - 10}" height="6" fill="${ph >= 1 ? C.red : C.steelD}"/>`;
    s += tag(x0 - 100, py + 30, 'SEGMENȚI', ph >= 1 ? C.red : C.cy, 'middle', 17);
    s += `<rect x="${x0 + 5}" y="404" width="${x1 - x0 - 10}" height="16" fill="${C.oil}" opacity=".9"/>`; s += T(x0 - 16, 416, 'ULEI', { s: 16, c: C.oil, a: 'end' });
    // chamber
    const smokeOn = ph >= 3;
    if (ph >= 1) for (let i = 0; i < 8; i++) { const k = ((tl * .7 + i / 8) % 1); const side = i % 2 ? x1 - 12 : x0 + 12; s += drop(side, lerp(400, py - 20, k), 5, C.oil, 1 - k * .6); }
    if (ph >= 2) for (let i = 0; i < 6; i++) { const k = ((tl * .8 + i / 6) % 1); s += drop(560 + 10, lerp(56, 200, k), 5, C.oil, 1 - k * .5); }
    if (smokeOn) { if (!P.noSmoke) { for (let i = 0; i < 8; i++) { const k = ((pt * .5 + i / 8) % 1); s += glowC(lerp(400, 820, k) + (rnd(i) - .5) * 30, lerp(200, 120, k), 16 + k * 26, C.smoke, .45 * (1 - k)); }
      s += tag(780, 200, 'FUM ALBASTRU', C.smoke, 'middle', 18); } else { const fl = .5 + .5 * Math.sin(tl * 12); s += `<ellipse cx="457" cy="190" rx="${f(110 + 10 * fl)}" ry="34" fill="${C.org}" opacity="${f(.25 + .2 * fl)}"/>`; s += tag(780, 200, 'ULEIUL ARDE AICI', C.org, 'middle', 18); }
      s += tag(780, 380, 'CONSUM DE ULEI', C.red, 'middle', 19); }
    return s;
  }

  // 9) common-rail pressure build-up while cranking (Renault Megane): healthy vs faulty
  function railPressure(tl, ph, pt, P) {
    let s = ''; const ox = 110, oy = 370, W = 740, H = 300;
    s += `<line x1="${ox}" y1="${oy}" x2="${ox + W}" y2="${oy}" stroke="${C.dim}" stroke-width="3"/><line x1="${ox}" y1="${oy}" x2="${ox}" y2="${oy - H}" stroke="${C.dim}" stroke-width="3"/>`;
    s += T(ox + W, oy + 32, 'TIMP DE PORNIRE', { s: 17, c: C.dim, a: 'end' }); s += T(ox - 10, oy - H - 14, 'PRESIUNE ÎN RAMPĂ', { s: 17, c: C.dim });
    const thr = oy - H * .55; s += `<line x1="${ox}" y1="${f(thr)}" x2="${ox + W}" y2="${f(thr)}" stroke="${C.yel}" stroke-width="3" stroke-dasharray="12 8"/>`;
    s += T(ox + W - 6, thr + 30, 'PRAG MINIM PENTRU INJECȚIE', { s: 16, c: C.yel, a: 'end' });
    const curve = (fn, upto, col) => { let d = ''; for (let i = 0; i <= 100; i++) { const x = i / 100; if (x > upto) break; d += (i ? 'L' : 'M') + f(ox + x * W) + ' ' + f(oy - fn(x) * H); } return `<path d="${d}" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`; };
    const good = x => .86 * (1 - Math.exp(-x / .09)), bad = x => .72 * (1 - Math.exp(-x / .42));
    if (ph >= 1) { s += curve(good, ph === 1 ? eo(pt / 1.0) : 1, C.grn); if (ph > 1 || pt > .8) s += tag(ox + 160, oy - H * .97, 'INSTALAȚIE SĂNĂTOASĂ: PORNEȘTE IMEDIAT', C.grn, 'start', 16); }
    if (ph >= 2) { s += curve(bad, ph === 2 ? eo(pt / 1.6) : 1, C.red); if (ph > 2 || pt > 1.2) s += tag(ox + W - 6, oy - H * .3, 'INJECTOARE / POMPĂ UZATE: PORNEȘTE GREU', C.red, 'end', 16); }
    if (ph >= 3) { const xg = ox + .092 * W, xb = ox + .607 * W; s += `<circle cx="${f(xg)}" cy="${f(thr)}" r="9" fill="${C.grn}"/><circle cx="${f(xb)}" cy="${f(thr)}" r="9" fill="${C.red}"/>`;
      s += DBL(xg, thr + 46, xb, thr + 46, C.yel, 4); s += tag((xg + xb) / 2, thr + 46, 'SECUNDE PIERDUTE LA PORNIRE', C.yel, 'middle', 16); }
    if (ph === 0) s += tag(ox + W / 2, oy - H * .3, 'CÂT DE REPEDE CREȘTE PRESIUNEA?', C.cy, 'middle', 19);
    return s;
  }

  // 10) engine swap (Dacia Dokker): old overheated engine out, ancillaries moved, new engine in
  function engineSwap(tl, ph, pt, P) {
    let s = '';
    const block = (x, y, col, glow, op = 1, dash = false) => { let g = `<g transform="translate(${f(x)} ${f(y)})" opacity="${f(op)}">`;
      const da = dash ? ' stroke-dasharray="14 9"' : '';
      g += `<rect x="-120" y="-40" width="240" height="150" rx="14" fill="${C.body}" stroke="${col}" stroke-width="6"${da}/><rect x="-108" y="-92" width="216" height="56" rx="10" fill="${C.body2}" stroke="${col}" stroke-width="5"${da}/>`;
      for (let i = 0; i < 4; i++) g += `<circle cx="${-78 + i * 52}" cy="-64" r="16" fill="none" stroke="${col}" stroke-width="4"/>`;
      g += `<path d="M -96 110 L 96 110 L 76 150 L -76 150 Z" fill="${C.body2}" stroke="${col}" stroke-width="5"${da}/>`;
      if (glow) g += `<rect x="-130" y="-102" width="260" height="262" rx="22" fill="none" stroke="${col}" stroke-width="3" opacity=".5"/>`;
      return g + '</g>'; };
    const OLD = 230, NEW = 684, Y = 200;
    const acc = [['gear', -150, -40], ['wrench', 150, -40], ['nutbolt', -150, 80], ['test_tube', 150, 80]];
    // old engine
    let oldX = OLD, oldOp = 1; if (ph === 2) { oldX = lerp(OLD, -260, eio(cl((pt - 1.0) / .7))); } if (ph >= 3) { oldX = -400; oldOp = 0; }
    if (oldOp > 0) s += block(oldX, Y, ph >= 1 ? C.red : C.org, false, oldOp);
    if (ph === 0) for (let i = 0; i < 5; i++) { const k = ((tl * 1.1 + i / 5) % 1); s += `<path d="M ${OLD - 80 + i * 40} ${100 - k * 70} q 10 -12 0 -24 q -10 -12 0 -24" fill="none" stroke="${C.org}" stroke-width="4" opacity="${f(1 - k)}"/>`; }
    if (ph === 1) { s += xmark(OLD, Y, 66, C.red, 13); }
    if (ph === 0) s += tag(OLD, 395, 'MOTOR VECHI', C.org, 'middle', 18);
    if (ph === 1) s += tag(OLD, 395, 'SUPRAÎNCĂLZIT', C.red, 'middle', 18);
    // new engine: arrives as an outline in ph1, gets ancillaries in ph2, goes live + centre in ph3
    let newX = 1150, newCol = C.dim, newDash = true, newOp = 1;
    if (ph === 1) newX = lerp(1150, NEW, eo(pt / .7));
    if (ph === 2) newX = NEW;
    if (ph >= 3) { newX = lerp(NEW, 457, eio(pt / .8)); newCol = C.grn; newDash = false; }
    if (ph >= 1) s += block(newX, Y, newCol, ph >= 3, newOp, newDash);
    if (ph === 1 || ph === 2) s += tag(NEW, 395, 'MOTOR NOU', C.dim, 'middle', 18);
    // ancillaries: on the old engine (ph0-1), travel (ph2), mounted on the new one (ph3)
    acc.forEach(([e, dx, dy], i) => {
      let x = OLD + dx * .62, y = Y + dy, sz = 50;
      if (ph === 2) { const k = eio(cl((pt - i * .14) / .75)); x = lerp(OLD + dx * .62, NEW + dx * .62, k); y = Y + dy - Math.sin(k * Math.PI) * 120; }
      if (ph >= 3) { x = newX + dx * .62; y = Y + dy; }
      if (ph <= 1) { x = oldX + dx * .62; }
      s += emoji(x, y, sz, e);
    });
    if (ph === 2) s += tag(457, 50, 'ANEXELE TRECUTE PE MOTORUL NOU', C.cy, 'middle', 19);
    if (ph >= 3 && pt > .7) s += tag(457, 395, 'MOTOR NOU, ECHIPAT', C.grn, 'middle', 20);
    return s;
  }

  // 11) cam timing offset + compression per cylinder (Mercedes C200)
  function camTiming(tl, ph, pt, P) {
    let s = ''; const A = [210, 130], Cc = [210, 340];
    const offOn = P.compFirst ? ph >= 2 : ph >= 1, compOn = P.compFirst ? ph >= 1 : ph >= 2; const offT = P.compFirst && ph === 2 ? pt : (P.compFirst ? 9 : pt);
    const off = offOn ? -32 * eo(offT / .6) : 0;
    const sp = (c, R, ang, col) => { let g = `<circle cx="${c[0]}" cy="${c[1]}" r="${R}" fill="${C.body}" stroke="${col}" stroke-width="4"/>`; for (let i = 0; i < 18; i++) { const a = rad(ang + i * 20); const [x0, y0] = P2(c[0], c[1], R - 2, a), [x1, y1] = P2(c[0], c[1], R + 7, a); g += `<line x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}" stroke="${col}" stroke-width="5"/>`; } return g; };
    s += `<path d="M ${A[0] - 66} ${A[1]} L ${Cc[0] - 46} ${Cc[1]} A 46 46 0 0 0 ${Cc[0] + 46} ${Cc[1]} L ${A[0] + 66} ${A[1]} A 66 66 0 0 0 ${A[0] - 66} ${A[1]} Z" fill="none" stroke="${offOn ? C.yel : C.steel}" stroke-width="8" stroke-dasharray="12 6" stroke-dashoffset="${f(-tl * 60)}"/>`;
    s += sp(A, 60, off, C.cy) + sp(Cc, 40, 0, C.cy);
    const [mx, my] = P2(A[0], A[1], 46, rad(off - 90)); s += `<circle cx="${f(mx)}" cy="${f(my)}" r="9" fill="${C.yel}"/><line x1="${A[0]}" y1="${A[1] - 96}" x2="${A[0]}" y2="${A[1] - 74}" stroke="${C.w}" stroke-width="6" stroke-linecap="round"/>`;
    if (offOn) { const a0 = rad(-90), a1 = rad(off - 90); const [x0, y0] = P2(A[0], A[1], 84, a0), [x1, y1] = P2(A[0], A[1], 84, a1); s += `<path d="M ${f(x0)} ${f(y0)} A 84 84 0 0 0 ${f(x1)} ${f(y1)}" fill="none" stroke="${C.red}" stroke-width="9" stroke-linecap="round"/>`; const [lx, ly] = P2(A[0], A[1], 60, rad(off - 90)); s += `<line x1="${A[0]}" y1="${A[1]}" x2="${f(lx)}" y2="${f(ly)}" stroke="${C.yel}" stroke-width="4" stroke-dasharray="6 5"/><line x1="${A[0]}" y1="${A[1]}" x2="${A[0]}" y2="${A[1] - 60}" stroke="${C.w}" stroke-width="4" stroke-dasharray="6 5"/>`; s += tag(330, 34, 'DEFAZAJ', C.red, 'middle', 21); }
    else s += tag(210, 22, 'REPERE ALINIATE', C.grn, 'middle', 18);
    s += T(210, 420, 'DISTRIBUȚIE', { s: 16, c: C.dim, a: 'middle' });
    // compression bars
    s += T(640, 40, 'COMPRESIE PE CILINDRI', { s: 18, c: C.dim, a: 'middle' });
    const base = 370, Hm = 260; [1, 2, 3, 4].forEach((c, i) => { const x = 470 + i * 92; const target = (c === 1 && compOn) ? .32 : .9; const cpt = P.compFirst ? (ph === 1 ? pt : 9) : pt; const grow = compOn ? eo(cl((cpt - i * .12) / .5)) : .9;
      const h = Hm * target * (compOn ? grow : 1); const col = (c === 1 && compOn) ? C.red : C.grn;
      s += `<rect x="${x}" y="${f(base - Hm)}" width="60" height="${Hm}" rx="8" fill="rgba(255,255,255,.06)"/><rect x="${x}" y="${f(base - h)}" width="60" height="${f(h)}" rx="8" fill="${col}"/>` + T(x + 30, base + 30, 'C' + c, { s: 20, a: 'middle', c: C.w }); });
    if (compOn) s += tag(500, 92, 'LIPSĂ COMPRESIE', C.red, 'middle', 17);
    return s;
  }

  // 12) hybrid cooling circuits (engine + inverter), leaks, pressure test (Nissan e-Power)
  function coolingHybrid(tl, ph, pt, P) {
    let s = '';
    if (ph >= 3) { // pressure test chart
      const ox = 110, oy = 360, W = 720, H = 260; const fade = eo(pt / .4);
      s += `<g opacity="${f(fade)}"><line x1="${ox}" y1="${oy}" x2="${ox + W}" y2="${oy}" stroke="${C.dim}" stroke-width="3"/><line x1="${ox}" y1="${oy}" x2="${ox}" y2="${oy - H}" stroke="${C.dim}" stroke-width="3"/>`;
      s += T(ox + W, oy + 32, 'TIMP', { s: 17, c: C.dim, a: 'end' }) + T(ox - 10, oy - H - 14, 'PRESIUNE ÎN SISTEMUL DE RĂCIRE', { s: 17, c: C.dim });
      const prog = eo(pt / 1.6); let d1 = '', d2 = ''; for (let i = 0; i <= 100; i++) { const x = i / 100; if (x > prog) break; d1 += (i ? 'L' : 'M') + f(ox + x * W) + ' ' + f(oy - .8 * H); d2 += (i ? 'L' : 'M') + f(ox + x * W) + ' ' + f(oy - (.8 - .32 * x) * H); }
      s += `<path d="${d1}" fill="none" stroke="${C.w}" stroke-width="4" stroke-dasharray="10 8"/><path d="${d2}" fill="none" stroke="${C.red}" stroke-width="7" stroke-linecap="round"/>`;
      s += T(ox + 20, oy - .8 * H - 16, 'SISTEM ETANȘ: PRESIUNEA RĂMÂNE CONSTANTĂ', { s: 15, c: C.w });
      if (prog > .7) s += tag(ox + W - 10, oy - .5 * H + 30, 'PRESIUNEA SCADE = PIERDERE', C.red, 'end', 18);
      return s + '</g>';
    }
    const loop = (x, y, w, h, col, sp) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="40" fill="none" stroke="${col}" stroke-width="8" stroke-dasharray="16 10" stroke-dashoffset="${f(-tl * sp)}"/>`;
    s += loop(40, 86, 400, 290, '#38BDF8', 60) + loop(474, 86, 400, 290, '#22D3EE', 60);
    const box = (x, y, lab, em, bad) => `<g transform="translate(${x} ${y})"><rect x="-96" y="-34" width="192" height="68" rx="14" fill="${C.body}" stroke="${bad ? C.red : C.cy}" stroke-width="4"/>` + emoji(-66, 0, 40, em) + T(-40, 8, lab, { s: 17 }) + '</g>';
    s += T(240, 30, 'CIRCUIT MOTOR TERMIC', { s: 17, c: C.dim, a: 'middle' }) + T(674, 30, 'CIRCUIT INVERTOR', { s: 17, c: C.dim, a: 'middle' });
    const egrBad = ph >= 1, invBad = ph >= 2;
    s += box(150, 86, 'MOTOR', 'gear', false) + box(330, 376, P.egrLab || 'RĂCITOR EGR', 'wrench', egrBad) + box(140, 376, 'VAS 1', 'droplet', false);
    s += box(584, 86, 'INVERTOR', 'battery', false) + box(770, 376, 'RADIATOR INV.', 'snowflake', invBad) + box(574, 376, 'VAS 2', 'droplet', false);
    if (egrBad) { for (let i = 0; i < 3; i++) { const k = ((tl * .9 + i / 3) % 1); s += drop(330 + (i - 1) * 18, 300 - k * 0 + 0, 6, '#38BDF8', 1 - k); } s += tag(330, 314, 'PIERDERE MICĂ', C.red, 'middle', 16); }
    if (invBad) { s += tag(770, 314, 'PIERDERE', C.red, 'middle', 16); }
    if (ph >= 1) s += tag(457, 230, 'TEST GARNITURĂ CHIULASĂ: NEGATIV', C.grn, 'middle', 16);
    return s;
  }

  // 13) oil filter clogged by sludge -> bypass valve opens -> unfiltered oil (Skoda)
  function oilFilter(tl, ph, pt, P) {
    let s = ''; const L = 300, R = 614;
    s += `<rect x="${L}" y="40" width="${R - L}" height="356" rx="24" fill="none" stroke="${C.cy}" stroke-width="6"/>`;
    const dirt = ph === 0 ? 0 : ph === 1 ? eo(pt / 1.6) : 1;
    const pc = `rgb(${Math.round(lerp(214, 26, dirt))},${Math.round(lerp(176, 22, dirt))},${Math.round(lerp(110, 18, dirt))})`;
    const zig = (xa, xb) => { let d = `M ${xa} 90`; for (let i = 0; i < 14; i++) { d += ` L ${i % 2 ? xa : xb} ${90 + (i + 1) * 20}`; } return d; };
    s += `<path d="${zig(342, 392)}" fill="none" stroke="${pc}" stroke-width="9" stroke-linejoin="round"/><path d="${zig(522, 572)}" fill="none" stroke="${pc}" stroke-width="9" stroke-linejoin="round"/>`;
    s += `<rect x="426" y="80" width="62" height="300" fill="${C.body}" stroke="${C.cy}" stroke-width="3"/>`; for (let i = 0; i < 8; i++) s += `<circle cx="${i % 2 ? 474 : 440}" cy="${100 + i * 36}" r="6" fill="${C.bg}" stroke="${C.cyD}" stroke-width="2"/>`;
    // bypass valve at top of centre tube
    const open = ph >= 2 ? eo(pt / .4) : 0; s += `<rect x="430" y="${f(64 - 18 * open)}" width="54" height="12" rx="5" fill="${ph >= 2 ? C.red : C.steel}"/>`; s += `<path d="M 444 ${f(40 - 18 * open)} l 8 8 l -8 8 l 8 8" fill="none" stroke="${C.steel}" stroke-width="3"/>`;
    s += tag(457 + 210, 64, 'SUPAPĂ BYPASS', ph >= 2 ? C.red : C.cy, 'middle', 16);
    s += T(457, 422, 'FILTRU DE ULEI · SECȚIUNE', { s: 16, c: C.dim, a: 'middle' });
    // particles
    for (let i = 0; i < 12; i++) { const k = ((tl * (ph === 1 ? .45 : .7) + i / 12) % 1); const left = i % 2 === 0;
      let x, y, col = C.oil;
      if (ph < 2) { if (k < .5) { x = left ? lerp(L + 14, 360, k / .5) : lerp(R - 14, 554, k / .5); y = 380 - i * 22; } else { x = lerp(left ? 380 : 534, 457, (k - .5) / .5); y = lerp(380 - i * 22, 60, (k - .5) / .5); col = ph === 1 ? '#9C7A2A' : C.oil; } if (ph === 1 && k > .35 && k < .5 && rnd(i) < dirt) { x = left ? 360 : 554; } }
      else { col = '#3B2A12'; if (k < .6) { x = left ? lerp(L + 14, 410, k / .6) : lerp(R - 14, 504, k / .6); y = lerp(360, 70, k / .6); } else { x = 457; y = lerp(60, 10, (k - .6) / .4); col = C.red; } }
      s += `<circle cx="${f(x)}" cy="${f(y)}" r="7" fill="${col}" opacity=".95"/>`; }
    s += ARW(457, 30, 457, -4, ph >= 2 ? C.red : C.grn, 6); s += T(520, 24, ph >= 2 ? 'ULEI NEFILTRAT SPRE MOTOR' : 'ULEI FILTRAT SPRE MOTOR', { s: 16, c: ph >= 2 ? C.red : C.grn });
    if (ph === 1) s += tag(160, 230, 'NĂMOL', C.org, 'middle', 22);
    if (ph >= 2) s += tag(160, 230, 'FILTRU BLOCAT', C.red, 'middle', 20);
    return s;
  }

  // 14) cam lobe + tappet: oil film breaks down -> metal contact -> wear (Opel Combo)
  function camWear(tl, ph, pt, P) {
    let s = ''; const cx = 457, cy = 300; const ang = tl * 2.2;
    const wear = ph >= 2 ? eo(pt / 1.2) : 0; const lift = (a) => { const c = Math.cos(a); return c > 0 ? Math.pow(c, 2) * (62 - 26 * wear) : 0; };
    let d = ''; for (let i = 0; i <= 72; i++) { const a = i / 72 * Math.PI * 2; const r = 70 + lift(a); const [x, y] = P2(cx, cy, r, a + ang - Math.PI / 2); d += (i ? 'L' : 'M') + f(x) + ' ' + f(y); }
    s += `<path d="${d} Z" fill="${C.body2}" stroke="${ph >= 2 ? C.red : C.cy}" stroke-width="5"/><circle cx="${cx}" cy="${cy}" r="18" fill="${C.steelD}"/>`;
    // contact point is at top (angle -90°): lift at the top = lift(-ang)
    const topR = 70 + lift(-ang); const tappetY = cy - topR; const film = ph === 0 ? 10 : ph === 1 ? lerp(10, 3, eo(pt / 1.2)) : 0;
    s += `<rect x="${cx - 60}" y="${f(tappetY - film - 120)}" width="120" height="120" rx="10" fill="${C.steel}" stroke="${ph >= 2 ? C.red : C.steelD}" stroke-width="4"/>`;
    if (film > 0) s += `<rect x="${cx - 60}" y="${f(tappetY - film)}" width="120" height="${f(film)}" fill="${ph === 1 ? '#8A5A0A' : C.oil}"/>`;
    s += tag(cx + 170, tappetY - 70, 'TACHET', ph >= 2 ? C.red : C.cy, 'middle', 18) + tag(cx - 210, cy + 20, 'CAMĂ', ph >= 2 ? C.red : C.cy, 'middle', 18);
    if (ph <= 1) s += tag(cx + 80, tappetY - 4, ph === 1 ? 'ULEI UZAT, PELICULĂ SUBȚIRE' : 'PELICULĂ DE ULEI', ph === 1 ? C.org : C.oil, 'start', 16);
    if (ph >= 2) { s += spark(cx, tappetY, tl * 8, C.yel, 7, 26); s += tag(cx, 36, 'CONTACT METAL PE METAL', C.red, 'middle', 22); for (let i = 0; i < 5; i++) s += `<circle cx="${cx - 40 + i * 20}" cy="${f(tappetY - 6)}" r="3" fill="${C.red}"/>`; }
    return s;
  }

  // 15) route: engine shipped from Germany to Piatra Neamț and back (Opel Combo)
  function route(tl, ph, pt, P) {
    let s = ''; const A = [180, 150], B = [740, 300];
    s += `<circle cx="${A[0]}" cy="${A[1]}" r="14" fill="${C.yel}"/><circle cx="${B[0]}" cy="${B[1]}" r="14" fill="${C.red}"/>`;
    s += tag(A[0], A[1] - 44, 'GERMANIA (CLIENT)', C.yel, 'middle', 18) + tag(B[0], B[1] + 46, 'TURBO DOCTOR PIATRA NEAMȚ', C.red, 'middle', 17);
    const ctrl = [460, 40]; const pth = `M ${A[0]} ${A[1]} Q ${ctrl[0]} ${ctrl[1]} ${B[0]} ${B[1]}`;
    s += `<path d="${pth}" fill="none" stroke="${C.cyD}" stroke-width="5" stroke-dasharray="14 10"/>`;
    const q = (k) => [ (1 - k) * (1 - k) * A[0] + 2 * (1 - k) * k * ctrl[0] + k * k * B[0], (1 - k) * (1 - k) * A[1] + 2 * (1 - k) * k * ctrl[1] + k * k * B[1] ];
    const k = ph === 0 ? eio(pt / 1.6) : ph === 1 ? 1 : 1 - eio(pt / 1.6); const [x, y] = q(k);
    s += emoji(x, y - 10, 70, 'gear');
    if (ph === 0) s += tag(457, 380, 'MOTORUL VINE LA RECONDIȚIONARE', C.cy, 'middle', 18);
    if (ph === 1) s += tag(457, 380, 'RECONDIȚIONARE COMPLETĂ', C.grn, 'middle', 20);
    if (ph >= 2) s += tag(457, 380, 'ÎNAPOI LA CLIENT', C.grn, 'middle', 20);
    return s;
  }

  return { _gauge, turboPlay, turboOil, injectorSpray, chainSkip, wastegate, pistonSeize, systemMap, oilPaths, railPressure, engineSwap, camTiming, coolingHybrid, oilFilter, camWear, route };
})();
