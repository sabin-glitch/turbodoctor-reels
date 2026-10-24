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

  // 16) rail pressure sensor -> ECU feedback loop: healthy / wrong readings / ECU blind -> injection goes haywire (BMW N47)
  //     P.real = real rail pressure (bar). Steps: 0 sensor OK, 1 sensor defective, 2 wrong/incoherent data, 3 ECU blind, 4 injection haywire
  function sensorFeedback(tl, ph, pt, P) {
    let s = ''; const bad = ph >= 1;
    // rail + injectors
    const rx = 60, ry = 300, rw = 470;
    s += `<rect x="${rx}" y="${ry - 22}" width="${rw}" height="44" rx="22" fill="${C.body2}" stroke="${C.cy}" stroke-width="5"/>`;
    s += T(rx + rw / 2, ry + 112, 'RAMPA COMUNĂ + INJECTOARE', { s: 17, c: C.dim, a: 'middle' });
    for (let i = 0; i < 4; i++) { const x = rx + 70 + i * 105; const wild = ph >= 4; const amp = wild ? (.4 + .6 * rnd(i + Math.floor(tl * 6))) : .55;
      s += `<rect x="${x - 11}" y="${ry + 22}" width="22" height="46" rx="5" fill="${C.steelD}" stroke="${wild ? C.red : C.cy}" stroke-width="3"/>`;
      const cyc = ((tl * (wild ? 3.3 + i * .7 : 2.4)) + i * .25) % 1; if (cyc < .4) { const k = cyc / .4; for (let j = 0; j < 3; j++) s += `<circle cx="${f(x + (j - 1) * 12 * k)}" cy="${f(ry + 74 + 26 * k * amp * 2)}" r="${f(4 * (1 - k * .4))}" fill="${wild ? C.yel : '#A5E9FF'}" opacity="${f(1 - k * .6)}"/>`; } }
    // fuel moving inside the rail
    for (let i = 0; i < 7; i++) { const k = ((tl * .5 + i / 7) % 1); s += `<circle cx="${f(rx + 24 + k * (rw - 48))}" cy="${ry}" r="7" fill="${C.cy}" opacity=".75"/>`; }
    s += tag(rx + rw / 2 - 40, ry - 58, 'PRESIUNE REALĂ ÎN RAMPĂ', C.cy, 'middle', 18);
    // sensor at the rail end
    const sx = rx + rw + 30, sy = ry; const scol = bad ? C.red : C.grn; const pulse = bad ? 1 + .06 * Math.sin(tl * 10) : 1;
    s += `<g transform="translate(${sx} ${sy}) scale(${f(pulse)})"><rect x="-30" y="-24" width="60" height="48" rx="10" fill="${C.body}" stroke="${scol}" stroke-width="5"/><rect x="-46" y="-11" width="16" height="22" fill="${C.steel}"/>` +
      (bad ? xmark(0, 0, 11, C.red, 6) : check(0, 0, 12, C.grn, 6)) + '</g>';
    s += T(sx, sy + 58, 'SENZOR', { s: 17, c: scol, a: 'middle' });
    // ECU
    const ex = 770, ey = 120; const blind = ph >= 3;
    s += `<rect x="${ex - 112}" y="${ey - 72}" width="224" height="144" rx="16" fill="${C.body}" stroke="${blind ? C.red : C.cy}" stroke-width="5"/>`;
    s += T(ex, ey - 40, 'CALCULATOR', { s: 17, c: C.dim, a: 'middle' }) + T(ex, ey - 18, 'INJECȚIE', { s: 17, c: C.dim, a: 'middle' });
    // ECU display: what the ECU "believes" (bar) vs the real rail pressure (cyan marker)
    const bx0 = ex - 86, bw = 172, by = ey + 4, lvl = .62; let rd = lvl, rcol = C.grn;
    if (ph === 1 || ph === 2) { const q = Math.floor(tl * (ph === 2 ? 9 : 4)); rd = .1 + .85 * rnd(q + 3); rcol = C.red; }
    if (blind) { const k = .5 + .5 * Math.sin(tl * 8); s += T(ex, ey + 50, '???', { s: 46, c: C.red, a: 'middle', op: f(.6 + .4 * k) }); }
    else { s += `<rect x="${bx0}" y="${by}" width="${bw}" height="26" rx="6" fill="rgba(255,255,255,.08)"/><rect x="${bx0}" y="${by}" width="${f(bw * rd)}" height="26" rx="6" fill="${rcol}"/>`;
      s += `<line x1="${f(bx0 + bw * lvl)}" y1="${by - 8}" x2="${f(bx0 + bw * lvl)}" y2="${by + 34}" stroke="${C.cy}" stroke-width="4"/>`;
      s += T(ex, by + 56, rcol === C.grn ? 'CITIRE = REALĂ' : 'CITIRE GREȘITĂ', { s: 15, c: rcol, a: 'middle' }); }
    // signal wire sensor -> ECU
    const wx0 = sx, wy0 = sy - 26, wx1 = ex, wy1 = ey + 72; const path = `M ${wx0} ${wy0} L ${wx0} ${ey + 150} L ${wx1} ${ey + 150} L ${wx1} ${wy1}`;
    s += `<path d="${path}" fill="none" stroke="${bad ? 'rgba(255,75,75,.45)' : C.cyD}" stroke-width="5" stroke-dasharray="10 7"/>`;
    const segL = [(wy0 - (ey + 150)), (wx1 - wx0), ((ey + 150) - wy1)]; const tot = segL.reduce((a, b) => a + Math.abs(b), 0);
    const ptOn = k => { let d = k * tot; if (d < Math.abs(segL[0])) return [wx0, wy0 - d]; d -= Math.abs(segL[0]); if (d < segL[1]) return [wx0 + d, ey + 150]; d -= segL[1]; return [wx1, ey + 150 - d]; };
    for (let i = 0; i < 4; i++) { const k = ((tl * .9 + i / 4) % 1); let [x, y] = ptOn(k); if (bad) { x += (rnd(i + Math.floor(tl * 12)) - .5) * 18; y += (rnd(i + 7 + Math.floor(tl * 12)) - .5) * 18; }
      s += bad ? `<rect x="${f(x - 7)}" y="${f(y - 7)}" width="14" height="14" fill="${C.red}" transform="rotate(45 ${f(x)} ${f(y)})"/>` : `<circle cx="${f(x)}" cy="${f(y)}" r="7" fill="${C.grn}"/>`; }
    s += T((wx0 + wx1) / 2 + 30, ey + 182, ph >= 2 ? 'SEMNAL INCOERENT' : 'SEMNAL', { s: 16, c: bad ? C.red : C.dim, a: 'middle' });
    // ECU commands -> rail (regulator / injectors)
    const cmdCol = blind ? C.red : C.cy; const jit = ph >= 4 ? (rnd(Math.floor(tl * 10)) - .5) * 30 : 0;
    s += ARW(ex - 112, ey, rx + rw / 2 + 60 + jit, ry - 84, cmdCol, 4, 16);
    s += T(ex - 300, ey + 34, 'COMANDĂ', { s: 16, c: cmdCol, a: 'middle' });
    if (ph >= 4) { s += tag(300, 34, 'INJECȚIA O IA RAZNA', C.red, 'middle', 21); }
    else if (ph === 0) s += tag(300, 34, 'CITIRE CORECTĂ = INJECȚIE CORECTĂ', C.grn, 'middle', 18);
    else if (ph === 3) s += tag(300, 34, 'NU MAI ȘTIE PRESIUNEA REALĂ', C.red, 'middle', 19);
    return s;
  }

  // 18) diesel filter not replaced: filter clogs -> dirt reaches the HP pump -> pump wears -> metal shavings in rail + injectors
  function fuelFilterFlow(tl, ph, pt, P) {
    let s = '';
    const pl = pts => { const L = []; let tot = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; }
      return k => { let d = cl(k) * tot; for (let i = 0; i < L.length; i++) { if (d <= L[i] || i === L.length - 1) { const q = L[i] ? d / L[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], q), lerp(pts[i][1], pts[i + 1][1], q)]; } d -= L[i]; } }; };
    const pipe = (pts, col, w = 14) => { const d = pts.map((p, i) => (i ? 'L' : 'M') + p[0] + ' ' + p[1]).join(' ');
      return `<path d="${d}" fill="none" stroke="${C.cy}" stroke-width="${w + 8}" stroke-linejoin="round" stroke-linecap="round" opacity=".9"/><path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"/>`; };
    const A = [[105, 300], [105, 236], [258, 236]], B = [[300, 132], [300, 96], [392, 96], [392, 252], [428, 252]], Cc = [[492, 176], [492, 68], [572, 68]], R = [[572, 68], [866, 68]];
    const injX = [622, 694, 766, 838];
    const clog = ph === 0 ? 0 : ph === 1 ? eo(pt / 1.4) : 1; const pumpBad = ph >= 3; const shav = ph >= 3; const injBad = ph >= 4;
    // tank
    s += `<rect x="30" y="300" width="150" height="104" rx="14" fill="${C.body}" stroke="${C.cy}" stroke-width="5"/><rect x="36" y="350" width="138" height="48" rx="9" fill="${C.oil}" opacity=".55"/>`;
    s += T(105, 428, 'REZERVOR', { s: 16, c: C.dim, a: 'middle' });
    // pipes
    s += pipe(A, C.body2) + pipe(B, C.body2) + pipe(Cc, C.body2);
    // rail
    s += `<rect x="560" y="46" width="320" height="44" rx="22" fill="${C.body2}" stroke="${injBad ? C.red : C.cy}" stroke-width="5"/>`;
    s += T(720, 30, 'RAMPA COMUNĂ', { s: 16, c: injBad ? C.red : C.dim, a: 'middle' });
    injX.forEach((x, i) => { s += `<rect x="${x - 12}" y="90" width="24" height="88" rx="6" fill="${C.steelD}" stroke="${injBad ? C.red : C.cy}" stroke-width="3"/><path d="M ${x - 7} 178 L ${x + 7} 178 L ${x} 194 Z" fill="${C.steel}"/>`;
      if (injBad) s += xmark(x, 226, 13, C.red, 6);
      else { const cyc = (tl * 2.4 + i * .25) % 1; if (cyc < .4) { const k = cyc / .4; for (let j = 0; j < 3; j++) s += `<circle cx="${f(x + (j - 1) * 10 * k)}" cy="${f(198 + 26 * k)}" r="${f(3.6 * (1 - k * .4))}" fill="#A5E9FF" opacity=".85"/>`; } } });
    s += T(730, 268, 'INJECTOARE', { s: 16, c: injBad ? C.red : C.dim, a: 'middle' });
    // filter (vertical cartridge with pleats); dirt fills it from the bottom
    const fx0 = 248, fx1 = 352, fy0 = 132, fy1 = 340; const fcol = clog > .5 ? C.red : clog > 0 ? C.org : C.grn;
    s += `<rect x="${fx0}" y="${fy0}" width="${fx1 - fx0}" height="${fy1 - fy0}" rx="18" fill="${C.body}" stroke="${fcol}" stroke-width="6"/>`;
    const dirtH = (fy1 - fy0 - 16) * (.08 + .8 * clog); s += `<rect x="${fx0 + 8}" y="${f(fy1 - 8 - dirtH)}" width="${fx1 - fx0 - 16}" height="${f(dirtH)}" rx="10" fill="#4A3417" opacity="${f(.25 + .65 * clog)}"/>`;
    for (let i = 0; i < 9; i++) { const x = fx0 + 18 + i * 8.6; const pc = `rgb(${Math.round(lerp(236, 92, clog))},${Math.round(lerp(214, 66, clog))},${Math.round(lerp(160, 30, clog))})`;
      s += `<line x1="${f(x)}" y1="${fy0 + 26}" x2="${f(x)}" y2="${fy1 - 26}" stroke="${pc}" stroke-width="4"/>`; }
    s += T(300, 372, 'FILTRU DE', { s: 16, c: fcol === C.grn ? C.dim : fcol, a: 'middle' }) + T(300, 392, 'MOTORINĂ', { s: 16, c: fcol === C.grn ? C.dim : fcol, a: 'middle' });
    // high-pressure pump (piston going up and down)
    const px0 = 428, px1 = 556, py0 = 176, py1 = 330; const shake = pumpBad ? (rnd(Math.floor(tl * 20)) - .5) * 5 : 0;
    s += `<g transform="translate(${f(shake)} 0)"><rect x="${px0}" y="${py0}" width="${px1 - px0}" height="${py1 - py0}" rx="14" fill="${C.body}" stroke="${pumpBad ? C.red : ph >= 2 ? C.org : C.cy}" stroke-width="5"/>`;
    const pst = 236 + 26 * Math.sin(tl * 7); s += `<rect x="470" y="${f(pst)}" width="44" height="66" rx="5" fill="${C.steel}" stroke="${C.steelD}" stroke-width="3"/><rect x="484" y="${f(pst - 50)}" width="16" height="52" fill="${C.steelD}"/>`;
    if (pumpBad) for (let i = 0; i < 3; i++) s += spark(470 + rnd(i * 3 + Math.floor(tl * 8)) * 44, pst + rnd(i * 5 + Math.floor(tl * 8)) * 60, tl * 6 + i, C.yel, 6, 15);
    s += '</g>' + T(492, 356, 'POMPĂ DE', { s: 16, c: pumpBad ? C.red : C.dim, a: 'middle' }) + T(492, 376, 'ÎNALTĂ PRESIUNE', { s: 16, c: pumpBad ? C.red : C.dim, a: 'middle' });
    // flow: fuel droplets + dirt (+ metal shavings from the pump)
    const pA = pl(A), pB = pl(B), pC = pl(Cc), pR = pl(R); const sp = 1 - .55 * clog;
    for (let i = 0; i < 6; i++) { const k = (tl * .55 * sp + i / 6) % 1; const [x, y] = pA(k); s += `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="#A5E9FF" opacity=".8"/>`; }
    for (let i = 0; i < 7; i++) { const k = (tl * .5 * sp + i / 7) % 1; const [x, y] = pB(k); s += `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="#A5E9FF" opacity=".8"/>`; }
    for (let i = 0; i < 6; i++) { const k = (tl * .7 + i / 6) % 1; const [x, y] = k < .45 ? pC(k / .45) : pR((k - .45) / .55); s += `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="#A5E9FF" opacity=".8"/>`; }
    // dirt: stopped at the filter while it is good; passes it from step 2
    for (let i = 0; i < 5; i++) { const k = (tl * .45 + i / 5 + .1) % 1;
      if (ph < 2) { const [x, y] = pA(Math.min(k * 1.3, 1)); s += `<rect x="${f(x - 6)}" y="${f(y - 6)}" width="12" height="12" fill="#5A3D16" stroke="#000" stroke-opacity=".5" stroke-width="2" transform="rotate(${f(k * 360)} ${f(x)} ${f(y)})"/>`; }
      else { const [x, y] = k < .45 ? pA(k / .45) : pB((k - .45) / .55); s += `<rect x="${f(x - 6)}" y="${f(y - 6)}" width="12" height="12" fill="#7A4A12" stroke="${C.org}" stroke-width="2" transform="rotate(${f(k * 360)} ${f(x)} ${f(y)})"/>`; } }
    if (shav) for (let i = 0; i < 7; i++) { const k = (tl * .6 + i / 7) % 1; let x, y;
      if (!injBad) { [x, y] = k < .45 ? pC(k / .45) : pR((k - .45) / .55); }
      else { const j = i % 4; if (k < .55) { [x, y] = k < .25 ? pC(k / .25) : pR(((k - .25) / .3) * ((injX[j] - 572) / 294)); } else { x = injX[j]; y = lerp(68, 180, (k - .55) / .45); } }
      s += `<path d="M ${f(x)} ${f(y - 9)} L ${f(x + 7)} ${f(y + 6)} L ${f(x - 7)} ${f(y + 6)} Z" fill="#E8EEF4" stroke="${C.red}" stroke-width="2" transform="rotate(${f(k * 540)} ${f(x)} ${f(y)})"/>`; }
    // headline tag per step
    const H = [['FILTRUL REȚINE IMPURITĂȚILE', C.grn], ['FILTRU ÎMBÂCSIT, NESCHIMBAT LA TIMP', C.org], ['IMPURITĂȚILE TREC SPRE POMPĂ', C.red], ['POMPA SE UZEAZĂ: APARE PILITURA', C.red], ['PILITURĂ ÎN RAMPĂ ȘI INJECTOARE', C.red]][Math.min(ph, 4)];
    s += tag(250, 34, H[0], H[1], 'middle', 18);
    return s;
  }

  // 19) rail pressure regulator: hard acceleration -> ECU asks for high pressure -> faulty regulator can't raise it fast enough -> error + Limp Mode
  function pressureLag(tl, ph, pt, P) {
    let s = ''; const ox = 110, oy = 382, W = 740, H = 290;
    s += `<line x1="${ox}" y1="${oy}" x2="${ox + W}" y2="${oy}" stroke="${C.dim}" stroke-width="3"/><line x1="${ox}" y1="${oy}" x2="${ox}" y2="${oy - H}" stroke="${C.dim}" stroke-width="3"/>`;
    s += T(ox + W, oy + 32, 'TIMP', { s: 17, c: C.dim, a: 'end' }); s += T(ox - 10, oy - H - 16, 'PRESIUNE ÎN RAMPĂ', { s: 17, c: C.dim });
    const xa = .22; const req = x => x < xa ? .3 : .9;
    const good = x => x < xa ? .3 : .3 + .58 * (1 - Math.exp(-(x - xa) / .05));
    const bad = x => x < xa ? .3 : .3 + .26 * (1 - Math.exp(-(x - xa) / .45));
    const curve = (fn, upto, col, w = 7, dash = '') => { let d = ''; for (let i = 0; i <= 120; i++) { const x = i / 120; if (x > upto) break; d += (i ? 'L' : 'M') + f(ox + x * W) + ' ' + f(oy - fn(x) * H); }
      return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"${dash ? ` stroke-dasharray="${dash}"` : ''}/>`; };
    // pedal mark at the hard acceleration
    s += `<line x1="${f(ox + xa * W)}" y1="${oy}" x2="${f(ox + xa * W)}" y2="${oy - H}" stroke="${C.cyD}" stroke-width="3" stroke-dasharray="6 8"/>`;
    s += tag(ox + xa * W, oy - H + 14, 'ACCELERARE BRUSCĂ', C.cy, 'middle', 16);
    s += curve(req, ph === 0 ? eo(pt / .8) : 1, C.yel, 5, '14 10'); if (ph > 0 || pt > .6) s += T(ox + W - 6, oy - .9 * H - 24, 'PRESIUNE CERUTĂ DE CALCULATOR', { s: 16, c: C.yel, a: 'end' });
    s += curve(good, ph === 0 ? eo((pt - .3) / 1.0) : 1, ph >= 1 ? 'rgba(74,222,128,.45)' : C.grn); if (ph === 0 && pt > 1.0 || ph >= 1) s += T(ox + .36 * W, oy - .86 * H + 34, 'REGULATOR BUN', { s: 16, c: ph >= 1 ? 'rgba(74,222,128,.7)' : C.grn });
    if (ph >= 1) { s += curve(bad, ph === 1 ? eo(pt / 2.0) : 1, C.red, 8); if (ph > 1 || pt > 1.2) s += T(ox + W - 6, oy - bad(1) * H + 36, 'REGULATOR DEFECT', { s: 16, c: C.red, a: 'end' });
      if (ph > 1 || pt > 1.6) { const xg = ox + .62 * W; s += DBL(xg, oy - .9 * H + 8, xg, oy - bad(.62) * H - 8, C.red, 4); s += tag(xg - 150, oy - .62 * H, 'PREA LENT', C.red, 'middle', 18); } }
    if (ph >= 2) { const k = .55 + .45 * Math.sin(tl * 9); s += `<rect x="${ox + 8}" y="${oy - H - 2}" width="${W - 8}" height="${H}" fill="${C.red}" opacity="${f(.07 + .06 * k)}"/>`;
      s += tag(ox + W / 2 + 40, oy - H * .17, '⚠ PRESIUNE PREA MICĂ → EROARE · LIMP MODE', C.red, 'middle', 19); }
    return s;
  }

  // 20) winter + low tank: lots of humid air above the fuel -> condensation on the walls -> water at the bottom -> sucked into the injection system
  function tankCondens(tl, ph, pt, P) {
    let s = ''; const tx0 = 70, tx1 = 470, ty0 = 70, ty1 = 360;
    const lvl = ph === 0 ? .82 : ph === 1 ? lerp(.82, .16, eo(pt / 1.2)) : .16; const ly = ty1 - (ty1 - ty0) * lvl;
    // tank shell + fuel
    s += `<rect x="${tx0}" y="${ty0}" width="${tx1 - tx0}" height="${ty1 - ty0}" rx="26" fill="${C.body}" stroke="${ph >= 1 ? C.red : C.cy}" stroke-width="6"/>`;
    s += `<rect x="${tx0 + 6}" y="${f(ly)}" width="${tx1 - tx0 - 12}" height="${f(ty1 - ly - 6)}" rx="18" fill="${C.oil}" opacity=".55"/>`;
    s += T((tx0 + tx1) / 2, ty1 + 34, 'REZERVOR · SECȚIUNE', { s: 16, c: C.dim, a: 'middle' });
    // humid air above the fuel
    const air = (ly - ty0 - 12); const nAir = Math.round(4 + 14 * (air / (ty1 - ty0)));
    for (let i = 0; i < nAir; i++) { const x = tx0 + 30 + rnd(i) * (tx1 - tx0 - 60), y = ty0 + 16 + ((rnd(i + 9) * air + tl * 14 * (rnd(i + 3) + .4)) % Math.max(10, air)); s += `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="#A5E9FF" opacity=".35"/>`; }
    if (air > 70) s += T((tx0 + tx1) / 2, ty0 + 44, 'AER UMED', { s: 17, c: '#A5E9FF', a: 'middle', op: .9 });
    // condensation on the walls, dripping into the fuel; water layer at the bottom
    const wet = ph >= 2 ? eo(pt / 1.4) * (ph === 2 ? 1 : 1) : 0; const water = ph >= 2 ? (ph === 2 ? eo(pt / 2.5) : 1) : 0;
    if (wet > 0 || ph >= 3) { for (let i = 0; i < 10; i++) { const side = i % 2 ? tx1 - 14 : tx0 + 14; const k = (tl * .5 + rnd(i)) % 1; const y = lerp(ty0 + 20, ly, k);
        s += drop(side + (i % 2 ? -4 : 4), y, 7, '#A5E9FF', .9); } }
    if (water > 0) { const wh = 30 * water; s += `<rect x="${tx0 + 6}" y="${f(ty1 - 6 - wh)}" width="${tx1 - tx0 - 12}" height="${f(wh)}" rx="12" fill="#3FA9F5" opacity=".85"/>`;
      s += tag(tx0 + 120, ty1 - 6 - wh / 2, 'APĂ', '#62D8FF', 'middle', 17); }
    // pickup line -> filter -> pump -> injectors
    const lx = tx1, lyy = ty1 - 24; const path = [[tx1 - 70, ty1 - 18], [tx1 - 70, ty1 + 0], [560, ty1 + 0], [560, 200], [640, 200], [640, 120], [860, 120]];
    const d = path.map((p, i) => (i ? 'L' : 'M') + p[0] + ' ' + p[1]).join(' ');
    s += `<path d="${d}" fill="none" stroke="${C.cy}" stroke-width="20" stroke-linejoin="round" opacity=".9"/><path d="${d}" fill="none" stroke="${C.body2}" stroke-width="12" stroke-linejoin="round"/>`;
    const inj = ph >= 3; s += `<rect x="600" y="170" width="80" height="80" rx="12" fill="${C.body}" stroke="${inj ? C.red : C.cy}" stroke-width="4"/>` + T(640, 274, 'POMPĂ', { s: 15, c: inj ? C.red : C.dim, a: 'middle' });
    s += `<rect x="660" y="98" width="214" height="44" rx="22" fill="${C.body2}" stroke="${inj ? C.red : C.cy}" stroke-width="4"/>`;
    [700, 760, 820].forEach(x => { s += `<rect x="${x - 10}" y="142" width="20" height="60" rx="5" fill="${C.steelD}" stroke="${inj ? C.red : C.cy}" stroke-width="3"/>`; if (inj) s += xmark(x, 226, 11, C.red, 5); });
    s += T(767, 84, 'SISTEM DE INJECȚIE', { s: 15, c: inj ? C.red : C.dim, a: 'middle' });
    // flow
    const L = []; let tot = 0; for (let i = 1; i < path.length; i++) { const dd = Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]); L.push(dd); tot += dd; }
    const at = k => { let dd = k * tot; for (let i = 0; i < L.length; i++) { if (dd <= L[i] || i === L.length - 1) { const q = dd / L[i]; return [lerp(path[i][0], path[i + 1][0], q), lerp(path[i][1], path[i + 1][1], q)]; } dd -= L[i]; } };
    for (let i = 0; i < 8; i++) { const k = (tl * .4 + i / 8) % 1; const [x, y] = at(k); const isW = inj && i % 2 === 0;
      s += isW ? drop(x, y + 4, 7, '#3FA9F5', 1) : `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="${C.oil}" opacity=".9"/>`; }
    const H = [['REZERVOR PLIN: PUȚIN AER, PUȚIN CONDENS', C.grn], ['NIVEL FOARTE JOS: MULT AER UMED', C.org], ['APARE CONDENS ÎN CANTITATE MARE', '#62D8FF'], ['APA AJUNGE ÎN SISTEMUL DE INJECȚIE', C.red]][Math.min(ph, 3)];
    s += tag(457, 30, H[0], H[1], 'middle', 18);
    return s;
  }

  // 21) live data on the diagnosis tool: sensor fault = physically impossible jumps; regulator fault = unstable (hunting) regulation
  function liveData(tl, ph, pt, P) {
    let s = ''; const x0 = 70, x1 = 880, y0 = 60, y1 = 330, span = 5;
    s += `<rect x="${x0 - 14}" y="${y0 - 14}" width="${x1 - x0 + 28}" height="${y1 - y0 + 28}" rx="14" fill="rgba(0,0,0,.35)" stroke="${C.cyD}" stroke-width="3"/>`;
    for (let i = 1; i < 6; i++) { const y = y0 + (y1 - y0) * i / 6; s += `<line x1="${x0}" y1="${f(y)}" x2="${x1}" y2="${f(y)}" stroke="rgba(98,216,255,.12)" stroke-width="2"/>`; }
    for (let i = 1; i < 10; i++) { const x = x0 + (x1 - x0) * i / 10; s += `<line x1="${f(x)}" y1="${y0}" x2="${f(x)}" y2="${y1}" stroke="rgba(98,216,255,.08)" stroke-width="2"/>`; }
    const req = u => .52 + .14 * Math.sin(u * .8) + .05 * Math.sin(u * 2.1);
    const realF = (u, p) => { if (p === 1) { const q = Math.floor(u * 2.6); return req(u) + (rnd(q + 11) > .45 ? (rnd(q + 3) - .5) * .7 : 0); }
      if (p === 2) return req(u) + .13 * Math.sin(u * 7.5) + .04 * Math.sin(u * 17); return req(u) + .012 * Math.sin(u * 9); };
    const Y = v => y1 - cl(v, .02, .98) * (y1 - y0);
    let dq = '', dr = ''; const N = 220; const spk = [];
    for (let i = 0; i <= N; i++) { const k = i / N; const x = x0 + k * (x1 - x0); const age = (1 - k) * span; const u = tl - age;
      const p = age < pt ? ph : (ph === 2 ? 0 : Math.max(0, ph - 1)); dq += (i ? 'L' : 'M') + f(x) + ' ' + f(Y(req(u)));
      const v = realF(u, p); dr += (i ? 'L' : 'M') + f(x) + ' ' + f(Y(v)); if (ph === 1 && p === 1 && Math.abs(v - req(u)) > .2 && i % 6 === 0) spk.push([x, Y(v)]); }
    s += `<path d="${dq}" fill="none" stroke="${C.yel}" stroke-width="4" stroke-dasharray="12 8"/>`;
    const rc = ph === 1 ? C.red : ph === 2 ? C.org : C.cy;
    s += `<path d="${dr}" fill="none" stroke="${rc}" stroke-width="6" stroke-linejoin="round"/>`;
    spk.slice(-4).forEach(([x, y]) => { s += `<circle cx="${f(x)}" cy="${f(y)}" r="16" fill="none" stroke="${C.red}" stroke-width="4"/>`; });
    s += `<circle cx="${x1}" cy="${f(Y(realF(tl, ph)))}" r="9" fill="#fff"/>`;
    // legend
    s += `<line x1="${x0 + 10}" y1="${y0 + 16}" x2="${x0 + 50}" y2="${y0 + 16}" stroke="${C.yel}" stroke-width="4" stroke-dasharray="10 6"/>` + T(x0 + 60, y0 + 22, 'PRESIUNE CERUTĂ', { s: 15, c: C.yel });
    s += `<line x1="${x0 + 290}" y1="${y0 + 16}" x2="${x0 + 330}" y2="${y0 + 16}" stroke="${rc}" stroke-width="6"/>` + T(x0 + 340, y0 + 22, 'PRESIUNE CITITĂ', { s: 15, c: rc });
    s += T(x1, y0 - 22, 'VALORI REALE · LIVE', { s: 15, c: C.dim, a: 'end' });
    const H = [['VALORI NORMALE', C.grn], ['SARE BRUSC: FIZIC IMPOSIBIL → SENZOR', C.red], ['REGLARE INSTABILĂ → REGULATOR', C.org]][Math.min(ph, 2)];
    s += tag(457, 392, H[0], H[1], 'middle', 20);
    return s;
  }

  // 22) impurities / metal shavings in the injectors -> return flow too big -> rail pressure drops -> pressure error
  function injectorReturn(tl, ph, pt, P) {
    let s = ''; const injX = [220, 360, 500, 640], ry0 = 74, ry1 = 116, retY = 180;
    const dirt = ph >= 1 ? (ph === 1 ? eo(pt / 1.2) : 1) : 0; const big = ph >= 2 ? (ph === 2 ? eo(pt / 1.0) : 1) : 0;
    const press = lerp(.86, .34, big); const pcol = big > .5 ? C.red : C.grn;
    // rail + pressure gauge
    s += `<rect x="150" y="${ry0}" width="560" height="${ry1 - ry0}" rx="21" fill="${C.body2}" stroke="${big > .5 ? C.red : C.cy}" stroke-width="5"/>`;
    s += T(430, ry0 - 18, 'RAMPA COMUNĂ', { s: 16, c: big > .5 ? C.red : C.dim, a: 'middle' });
    const gx = 76, gy = 95, gr = 50; s += `<circle cx="${gx}" cy="${gy}" r="${gr}" fill="${C.body}" stroke="${pcol}" stroke-width="5"/>`;
    for (let i = 0; i <= 8; i++) { const a = rad(150 + i * 30); const [x1, y1] = P2(gx, gy, gr - 6, a), [x2, y2] = P2(gx, gy, gr - 16, a); s += `<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" stroke="${C.dim}" stroke-width="3"/>`; }
    const na = rad(150 + 240 * (press + (big > .5 ? .03 * Math.sin(tl * 13) : .008 * Math.sin(tl * 5)))); const [nx, ny] = P2(gx, gy, gr - 12, na);
    s += `<line x1="${gx}" y1="${gy}" x2="${f(nx)}" y2="${f(ny)}" stroke="${pcol}" stroke-width="6" stroke-linecap="round"/><circle cx="${gx}" cy="${gy}" r="7" fill="${pcol}"/>`;
    s += T(gx, gy + gr + 24, 'PRESIUNE', { s: 15, c: pcol, a: 'middle' }) + `<line x1="${gx + gr}" y1="${gy}" x2="150" y2="${gy}" stroke="${C.cy}" stroke-width="6"/>`;
    // metal shavings travelling along the rail into the injectors
    if (dirt > 0) for (let i = 0; i < 9; i++) { const k = (tl * .45 + i / 9) % 1; const x = 170 + k * 640; const y = ry0 + 12 + rnd(i * 7) * 18;
      s += `<rect x="${f(x)}" y="${f(y)}" width="9" height="5" rx="1.5" fill="${C.steel}" transform="rotate(${f(rnd(i) * 180)} ${f(x + 4)} ${f(y + 2)})" opacity="${f(dirt)}"/>`; }
    // return line (top side of the injectors -> back to the tank)
    s += `<path d="M ${injX[0] + 22} ${retY} L 880 ${retY}" fill="none" stroke="${big > .5 ? C.org : C.cyD}" stroke-width="12" stroke-linecap="round"/>`;
    s += T(884, retY - 18, big > .5 ? 'RETUR PREA MARE!' : 'RETUR', { s: 16, c: big > .5 ? C.org : C.dim, a: 'end' }) + T(884, retY + 32, '→ REZERVOR', { s: 14, c: C.dim, a: 'end' });
    injX.forEach((x, i) => {
      const bad = dirt > .5; const oc = big > .5 ? C.red : bad ? C.org : C.cy;
      s += `<rect x="${x - 16}" y="${ry1}" width="32" height="170" rx="8" fill="${C.steelD}" stroke="${oc}" stroke-width="3"/><rect x="${x - 9}" y="${ry1 + 172}" width="18" height="22" rx="4" fill="${C.steel}"/><path d="M ${x - 6} ${ry1 + 194} L ${x + 6} ${ry1 + 194} L ${x} ${ry1 + 208} Z" fill="${C.steel}"/>`;
      s += `<line x1="${x + 16}" y1="${retY}" x2="${x + 22}" y2="${retY}" stroke="${C.steelD}" stroke-width="10"/>`;
      if (bad) for (let j = 0; j < 4; j++) s += `<rect x="${f(x - 10 + rnd(i * 5 + j) * 16)}" y="${f(ry1 + 40 + rnd(i * 3 + j) * 110)}" width="7" height="4" rx="1" fill="${C.yel}" opacity=".85"/>`;
      // spray at the nozzle: weaker when the pressure drops
      const cyc = (tl * 2.4 + i * .25) % 1; if (cyc < .4) { const k = cyc / .4, sp = lerp(1, .45, big); for (let j = 0; j < 3; j++) s += `<circle cx="${f(x + (j - 1) * 12 * k * sp)}" cy="${f(ry1 + 214 + 34 * k * sp)}" r="${f(3.8 * (1 - k * .4))}" fill="#A5E9FF" opacity=".85"/>`; }
    });
    // return flow: a few drops when healthy, a stream when the injectors leak back
    const nR = Math.round(lerp(3, 14, big)), spR = lerp(.22, .9, big);
    for (let i = 0; i < nR; i++) { const k = (tl * spR + i / nR) % 1; const x = injX[0] + 26 + k * (880 - injX[0] - 40); s += `<circle cx="${f(x)}" cy="${retY}" r="${f(lerp(4, 6, big))}" fill="${big > .5 ? C.org : '#A5E9FF'}" opacity=".9"/>`; }
    const H = [['INJECTOARE BUNE · RETUR MIC', C.grn], ['IMPURITĂȚI / PILITURĂ ÎN INJECTOARE', C.org], ['PRESIUNEA SCADE ÎN RAMPĂ', C.red], ['⚠ EROARE: PRESIUNE ÎN RAMPA COMUNĂ', C.red]][Math.min(ph, 3)];
    if (ph >= 3) { const k = .55 + .45 * Math.sin(tl * 9); s += `<rect x="150" y="${ry0}" width="560" height="${ry1 - ry0}" rx="21" fill="${C.red}" opacity="${f(.15 + .15 * k)}"/>`; }
    s += tag(457, 404, H[0], H[1], 'middle', 19);
    return s;
  }

  // 23) low-pressure supply: in-tank pump -> fuel filter -> high-pressure pump -> rail; a clogged filter or a weak tank pump starves the HP pump -> low rail pressure (looks like a bad regulator)
  function supplyChain(tl, ph, pt, P) {
    let s = '';
    const pl = pts => { const L = []; let tot = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; }
      return k => { let d = cl(k) * tot; for (let i = 0; i < L.length; i++) { if (d <= L[i] || i === L.length - 1) { const q = L[i] ? d / L[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], q), lerp(pts[i][1], pts[i + 1][1], q)]; } d -= L[i]; } }; };
    const pipe = (pts, col, w = 14) => { const d = pts.map((p, i) => (i ? 'L' : 'M') + p[0] + ' ' + p[1]).join(' ');
      return `<path d="${d}" fill="none" stroke="${C.cyD}" stroke-width="${w + 8}" stroke-linejoin="round" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"/>`; };
    const clog = ph === 1 ? eo(pt / 1.2) : ph === 2 ? 1 : 0; const weak = ph === 3 ? eo(pt / 1.0) : ph >= 4 ? 1 : 0; const starve = Math.max(clog, weak);
    const flash = ph === 2 || ph >= 4;
    // tank with the electric low-pressure pump inside
    const tx0 = 26, tx1 = 214, ty0 = 200, ty1 = 334;
    s += `<rect x="${tx0}" y="${ty0}" width="${tx1 - tx0}" height="${ty1 - ty0}" rx="18" fill="${C.body}" stroke="${C.cy}" stroke-width="5"/><rect x="${tx0 + 6}" y="${ty0 + 50}" width="${tx1 - tx0 - 12}" height="${ty1 - ty0 - 56}" rx="12" fill="${C.oil}" opacity=".5"/>`;
    const pc = weak > .5 ? C.red : C.cy; const px = 120, py = 266;
    s += `<rect x="${px - 30}" y="${py - 44}" width="60" height="78" rx="10" fill="${C.body2}" stroke="${pc}" stroke-width="4"/>`;
    const rot = tl * lerp(9, 1.6, weak); for (let i = 0; i < 4; i++) { const a = rot + i * Math.PI / 2; const [x2, y2] = P2(px, py, 20, a); s += `<line x1="${px}" y1="${py}" x2="${f(x2)}" y2="${f(y2)}" stroke="${pc}" stroke-width="5" stroke-linecap="round"/>`; }
    s += `<circle cx="${px}" cy="${py}" r="6" fill="${pc}"/>`;
    s += T((tx0 + tx1) / 2, ty1 + 26, 'REZERVOR', { s: 15, c: C.dim, a: 'middle' }) + T((tx0 + tx1) / 2, ty1 + 46, 'POMPA DE JOASĂ', { s: 15, c: weak > .5 ? C.red : C.cy, a: 'middle' });
    // pipes: tank pump -> filter -> HP pump -> rail
    const A = [[120, 222], [120, 168], [270, 168]], B = [[330, 110], [330, 70], [432, 70], [432, 220], [462, 220]], Cc = [[526, 150], [526, 64], [620, 64]];
    s += pipe(A, C.body2) + pipe(B, C.body2) + pipe(Cc, C.body2);
    // fuel filter (pleated cartridge, darkens when clogged)
    const fx0 = 270, fx1 = 390, fy0 = 110, fy1 = 310; const fcol = clog > .5 ? C.red : clog > 0 ? C.org : C.grn;
    s += `<rect x="${fx0}" y="${fy0}" width="${fx1 - fx0}" height="${fy1 - fy0}" rx="18" fill="${C.body}" stroke="${fcol}" stroke-width="6"/>`;
    const dirtH = (fy1 - fy0 - 16) * (.06 + .86 * clog); s += `<rect x="${fx0 + 8}" y="${f(fy1 - 8 - dirtH)}" width="${fx1 - fx0 - 16}" height="${f(dirtH)}" rx="10" fill="#4A3417" opacity="${f(.2 + .7 * clog)}"/>`;
    for (let i = 0; i < 10; i++) { const x = fx0 + 18 + i * 9.4; const c2 = `rgb(${Math.round(lerp(236, 92, clog))},${Math.round(lerp(214, 66, clog))},${Math.round(lerp(160, 30, clog))})`; s += `<line x1="${f(x)}" y1="${fy0 + 24}" x2="${f(x)}" y2="${fy1 - 24}" stroke="${c2}" stroke-width="4"/>`; }
    s += T((fx0 + fx1) / 2, fy1 + 26, clog > .5 ? 'FILTRU ÎNFUNDAT' : 'FILTRU', { s: 15, c: clog > .5 ? C.red : C.dim, a: 'middle' }) + T((fx0 + fx1) / 2, fy1 + 46, 'COMBUSTIBIL', { s: 15, c: clog > .5 ? C.red : C.dim, a: 'middle' });
    // high-pressure pump
    const hx0 = 462, hx1 = 590, hy0 = 150, hy1 = 300; const hcol = starve > .5 ? C.org : C.cy;
    s += `<rect x="${hx0}" y="${hy0}" width="${hx1 - hx0}" height="${hy1 - hy0}" rx="14" fill="${C.body}" stroke="${hcol}" stroke-width="5"/>`;
    const pst = 206 + 24 * Math.sin(tl * 7); s += `<rect x="504" y="${f(pst)}" width="44" height="60" rx="5" fill="${C.steel}" stroke="${C.steelD}" stroke-width="3"/><rect x="518" y="${f(pst - 46)}" width="16" height="48" fill="${C.steelD}"/>`;
    s += T(526, hy1 + 26, 'POMPA DE', { s: 15, c: starve > .5 ? C.org : C.dim, a: 'middle' }) + T(526, hy1 + 46, 'ÎNALTĂ PRESIUNE', { s: 15, c: starve > .5 ? C.org : C.dim, a: 'middle' });
    if (starve > .5) s += tag(526, hy0 - 26, 'NU PRIMEȘTE DESTUL', C.org, 'middle', 15);
    // rail + gauge
    s += `<rect x="610" y="44" width="280" height="40" rx="20" fill="${C.body2}" stroke="${flash ? C.red : C.cy}" stroke-width="5"/>` + T(750, 30, 'RAMPA COMUNĂ', { s: 15, c: flash ? C.red : C.dim, a: 'middle' });
    const press = lerp(.84, .3, starve); const gcol = starve > .5 ? C.red : C.grn; const gx = 780, gy = 196, gr = 54;
    s += `<line x1="${gx}" y1="84" x2="${gx}" y2="${gy - gr}" stroke="${C.cy}" stroke-width="6"/><circle cx="${gx}" cy="${gy}" r="${gr}" fill="${C.body}" stroke="${gcol}" stroke-width="5"/>`;
    for (let i = 0; i <= 8; i++) { const a = rad(150 + i * 30); const [x1, y1] = P2(gx, gy, gr - 6, a), [x2, y2] = P2(gx, gy, gr - 16, a); s += `<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" stroke="${C.dim}" stroke-width="3"/>`; }
    const [nx, ny] = P2(gx, gy, gr - 12, rad(150 + 240 * (press + .01 * Math.sin(tl * 6)))); s += `<line x1="${gx}" y1="${gy}" x2="${f(nx)}" y2="${f(ny)}" stroke="${gcol}" stroke-width="6" stroke-linecap="round"/><circle cx="${gx}" cy="${gy}" r="7" fill="${gcol}"/>`;
    s += T(gx, gy + gr + 26, starve > .5 ? 'PRESIUNE PREA MICĂ' : 'PRESIUNE OK', { s: 15, c: gcol, a: 'middle' });
    // flow droplets (slower and sparser when the supply is starved)
    const pA = pl(A), pB = pl(B), pC = pl(Cc); const sA = lerp(1, .3, weak), sB = lerp(1, .25, starve);
    const dots = (fn, n, sp, off) => { let o = ''; const m = Math.max(2, Math.round(n * (.35 + .65 * sp))); for (let i = 0; i < m; i++) { const k = (tl * .55 * sp + i / m + off) % 1; const [x, y] = fn(k); o += `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="#A5E9FF" opacity=".85"/>`; } return o; };
    s += dots(pA, 5, sA, 0) + dots(pB, 7, sB, .2) + dots(pC, 5, sB, .4);
    if (flash) { const k = .55 + .45 * Math.sin(tl * 9); s += `<rect x="610" y="44" width="280" height="40" rx="20" fill="${C.red}" opacity="${f(.15 + .15 * k)}"/>`; }
    const H = [['ALIMENTARE NORMALĂ · PRESIUNE CORECTĂ', C.grn], ['FILTRUL ÎNFUNDAT BLOCHEAZĂ ALIMENTAREA', C.red], ['⚠ SIMPTOME CA LA UN REGULATOR DEFECT', C.red], ['POMPA DE JOASĂ PRESIUNE FUNCȚIONEAZĂ DEFECTUOS', C.red], ['⚠ ERORI CA LA REGULATORUL DE PE RAMPĂ', C.red]][Math.min(ph, 4)];
    s += tag(457, 412, H[0], H[1], 'middle', 18);
    return s;
  }

  // 24) how it works: rail pressure sensor -> injection ECU -> two regulators (flow regulator on the HP pump, pressure regulator on the rail)
  function controlLoop(tl, ph, pt, P) {
    let s = '';
    const pl = pts => { const L = []; let tot = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(d); tot += d; }
      return k => { let d = cl(k) * tot; for (let i = 0; i < L.length; i++) { if (d <= L[i] || i === L.length - 1) { const q = L[i] ? d / L[i] : 0; return [lerp(pts[i][0], pts[i + 1][0], q), lerp(pts[i][1], pts[i + 1][1], q)]; } d -= L[i]; } }; };
    const wire = (pts, col, on) => { const d = pts.map((q, i) => (i ? 'L' : 'M') + q[0] + ' ' + q[1]).join(' ');
      return `<path d="${d}" fill="none" stroke="${on ? col : 'rgba(234,246,255,.18)'}" stroke-width="${on ? 5 : 3}" stroke-dasharray="12 9" stroke-linecap="round"/>`; };
    const pulses = (pts, col, n, sp) => { const fn = pl(pts); let o = ''; for (let i = 0; i < n; i++) { const k = (tl * sp + i / n) % 1; const [x, y] = fn(k); o += `<circle cx="${f(x)}" cy="${f(y)}" r="7" fill="${col}"/><circle cx="${f(x)}" cy="${f(y)}" r="14" fill="${col}" opacity=".25"/>`; } return o; };
    const glow = (x, y, r, col) => { const k = .5 + .5 * Math.sin(tl * 6); return `<circle cx="${x}" cy="${y}" r="${f(r + 6 * k)}" fill="none" stroke="${col}" stroke-width="4" opacity="${f(.5 + .4 * k)}"/>`; };
    // ECU
    s += `<rect x="330" y="24" width="260" height="96" rx="14" fill="${C.body}" stroke="${ph >= 1 ? C.cy : C.cyD}" stroke-width="5"/>`;
    for (let i = 0; i < 6; i++) s += `<line x1="${352 + i * 43}" y1="24" x2="${352 + i * 43}" y2="14" stroke="${C.steelD}" stroke-width="4"/>`;
    s += T(460, 64, 'CALCULATOR', { s: 18, c: C.w, a: 'middle' }) + T(460, 90, 'DE INJECȚIE', { s: 18, c: C.w, a: 'middle' });
    if (ph >= 1) s += T(460, 112, ph >= 2 ? 'COMANDĂ CORECT' : 'PRIMEȘTE PRESIUNEA', { s: 13, c: ph >= 2 ? C.grn : C.yel, a: 'middle' });
    // HP pump + flow regulator on top
    s += `<rect x="60" y="262" width="160" height="124" rx="14" fill="${C.body}" stroke="${C.cy}" stroke-width="5"/>` + T(140, 316, 'POMPA DE', { s: 13, c: C.dim, a: 'middle', ls: .5 }) + T(140, 338, 'ÎNALTĂ PRESIUNE', { s: 13, c: C.dim, a: 'middle', ls: .5 });
    const dOn = ph === 3; s += `<rect x="112" y="214" width="46" height="48" rx="8" fill="${C.body2}" stroke="${dOn ? C.grn : ph >= 2 ? C.cy : C.steelD}" stroke-width="5"/>`;
    s += T(170, 242, 'REGULATOR DE DEBIT', { s: 15, c: dOn ? C.grn : C.dim });
    if (dOn) s += glow(135, 238, 40, C.grn);
    // pump -> rail
    s += `<line x1="220" y1="330" x2="360" y2="330" stroke="${C.cyD}" stroke-width="20" stroke-linecap="round"/><line x1="220" y1="330" x2="360" y2="330" stroke="${C.body2}" stroke-width="12" stroke-linecap="round"/>`;
    // rail, pressure regulator (left end), sensor (right end)
    s += `<rect x="360" y="300" width="480" height="44" rx="22" fill="${C.body2}" stroke="${C.cy}" stroke-width="5"/>`;
    for (let i = 0; i < 7; i++) { const k = (tl * .5 + i / 7) % 1; s += `<circle cx="${f(380 + k * 440)}" cy="322" r="5" fill="#A5E9FF" opacity=".85"/>`; }
    const pOn = ph === 4; s += `<rect x="382" y="252" width="46" height="48" rx="8" fill="${C.body2}" stroke="${pOn ? C.grn : ph >= 2 ? C.cy : C.steelD}" stroke-width="5"/>`;
    if (pOn) s += glow(405, 276, 40, C.grn);
    const sOn = ph <= 1; s += `<rect x="790" y="262" width="40" height="38" rx="6" fill="${C.body2}" stroke="${sOn ? C.yel : C.cy}" stroke-width="5"/><rect x="800" y="248" width="20" height="14" fill="${C.steelD}"/>`;
    if (ph === 0) s += glow(810, 280, 36, C.yel);
    s += T(405, 374, 'REGULATOR DE PRESIUNE', { s: 15, c: pOn ? C.grn : C.dim, a: 'middle' }) + T(615, 374, 'RAMPA COMUNĂ', { s: 15, c: C.dim, a: 'middle' }) + T(810, 374, 'SENZOR DE PRESIUNE', { s: 15, c: sOn ? C.yel : C.dim, a: 'middle' });
    // signal + commands
    const SIG = [[810, 248], [810, 72], [590, 72]], CMD1 = [[330, 72], [135, 72], [135, 214]], CMD2 = [[405, 120], [405, 252]];
    s += wire(SIG, C.yel, ph >= 1) + wire(CMD1, C.grn, ph >= 2) + wire(CMD2, C.grn, ph >= 2);
    if (ph >= 1) s += pulses(SIG, C.yel, 3, .6);
    if (ph >= 2) { s += pulses(CMD1, C.grn, ph === 3 ? 3 : 2, .55) + pulses(CMD2, C.grn, ph === 4 ? 3 : 1, .7); }
    const H = [['SENZORUL CITEȘTE PRESIUNEA DIN RAMPĂ', C.yel], ['INFORMAȚIA AJUNGE LA CALCULATOR', C.yel], ['CALCULATORUL COMANDĂ 2 COMPONENTE VITALE', C.grn], ['REGULATORUL DE DEBIT · POMPA DE ÎNALTĂ', C.grn], ['REGULATORUL DE PRESIUNE · RAMPA COMUNĂ', C.grn]][Math.min(ph, 4)];
    s += tag(457, 412, H[0], H[1], 'middle', 18);
    return s;
  }

  // 25) oscilloscope: how the sensor and the regulator talk to the injection ECU (CH1 sensor signal, CH2 PWM command)
  function scopeTrace(tl, ph, pt, P) {
    let s = ''; const x0 = 40, x1 = 700, y0 = 34, y1 = 350;
    s += `<rect x="${x0 - 20}" y="${y0 - 20}" width="${x1 - x0 + 220}" height="${y1 - y0 + 40}" rx="22" fill="${C.body}" stroke="${C.steelD}" stroke-width="5"/>`;
    s += `<rect x="${x0}" y="${y0}" width="${x1 - x0}" height="${y1 - y0}" rx="8" fill="#03101C" stroke="${C.cyD}" stroke-width="3"/>`;
    for (let i = 1; i < 10; i++) { const x = x0 + (x1 - x0) * i / 10; s += `<line x1="${f(x)}" y1="${y0}" x2="${f(x)}" y2="${y1}" stroke="rgba(98,216,255,${i === 5 ? .22 : .09})" stroke-width="2"/>`; }
    for (let i = 1; i < 8; i++) { const y = y0 + (y1 - y0) * i / 8; s += `<line x1="${x0}" y1="${f(y)}" x2="${x1}" y2="${f(y)}" stroke="rgba(98,216,255,${i === 4 ? .22 : .09})" stroke-width="2"/>`; }
    // knobs / channel buttons
    const kx = x1 + 100; [[92, C.yel], [182, C.cy], [272, C.steel]].forEach(([y, c], i) => { s += `<circle cx="${kx}" cy="${y}" r="30" fill="${C.body2}" stroke="${c}" stroke-width="5"/>`; const [ax, ay] = P2(kx, y, 22, tl * (i === 2 ? .4 : 0) - 1.2 + i); s += `<line x1="${kx}" y1="${y}" x2="${f(ax)}" y2="${f(ay)}" stroke="${c}" stroke-width="5" stroke-linecap="round"/>`; });
    s += T(kx, 138, 'CH1', { s: 14, c: C.yel, a: 'middle' }) + T(kx, 228, 'CH2', { s: 14, c: C.cy, a: 'middle' }) + T(kx, 318, 'TIMP', { s: 14, c: C.dim, a: 'middle' });
    // CH1: sensor signal (analog, follows the rail pressure), upper half
    const on1 = ph === 0 || ph >= 2, on2 = ph >= 1; const sc = tl * 1.6; let d1 = '', d2 = '';
    for (let i = 0; i <= 160; i++) { const k = i / 160, u = k * 6 + sc; const x = x0 + k * (x1 - x0);
      const v = .5 + .28 * Math.sin(u * .9) + .06 * Math.sin(u * 4.3); d1 += (i ? 'L' : 'M') + f(x) + ' ' + f(y0 + 20 + (1 - v) * 130); }
    // CH2: PWM command from the ECU to the regulator, lower half (duty follows CH1)
    let prev = null; for (let i = 0; i <= 320; i++) { const k = i / 320, u = k * 6 + sc; const x = x0 + k * (x1 - x0); const duty = .35 + .3 * (.5 + .5 * Math.sin(u * .9));
      const hi = ((u * 3) % 1) < duty; const y = hi ? y0 + 196 : y0 + 288; if (prev !== null && prev !== y) d2 += 'L' + f(x) + ' ' + f(prev); d2 += (i ? 'L' : 'M') + f(x) + ' ' + f(y); prev = y; }
    s += `<path d="${d1}" fill="none" stroke="${C.yel}" stroke-width="${on1 ? 5 : 3}" opacity="${on1 ? 1 : .35}" stroke-linejoin="round"/>`;
    s += `<path d="${d2}" fill="none" stroke="${C.cy}" stroke-width="${on2 ? 5 : 3}" opacity="${on2 ? 1 : .35}" stroke-linejoin="round"/>`;
    s += T(x0 + 12, y0 + 24, 'CH1 · SEMNAL SENZOR PRESIUNE', { s: 15, c: C.yel, op: on1 ? 1 : .5 }) + T(x0 + 12, y0 + 180, 'CH2 · COMANDĂ CALCULATOR → REGULATOR', { s: 15, c: C.cy, op: on2 ? 1 : .5 });
    const H = [['OSCILOSCOP · SEMNALUL SENZORULUI', C.yel], ['COMANDA CALCULATORULUI CĂTRE REGULATOR', C.cy], ['CUM COMUNICĂ CU CALCULATORUL DE INJECȚIE', C.grn]][Math.min(ph, 2)];
    s += tag(457, 412, H[0], H[1], 'middle', 18);
    return s;
  }

  function wearCurve(tl, ph, pt, P) {
    let s = ''; const x0 = 96, x1 = 860, y0 = 30, y1 = 330;
    const X = k => x0 + k * (x1 - x0), Y = v => y1 - cl(v, 0, 1) * (y1 - y0);
    const w = k => .05 + 1.1 * Math.pow(k, 1.7);
    // zones: normal / high wear / failure
    [[0, .45, C.grn, 'NORMAL'], [.45, .75, C.yel, 'UZURĂ RIDICATĂ'], [.75, 1, C.red, 'DEFECȚIUNE']].forEach(([a, b, c, l]) => {
      s += `<rect x="${x0}" y="${f(Y(b))}" width="${x1 - x0}" height="${f(Y(a) - Y(b))}" fill="${c}" opacity=".09"/>`;
      s += T(x0 + 14, Y(b) + 22, l, { s: 13, c, a: 'start', op: .85 }); });
    s += `<line x1="${x0}" y1="${y1}" x2="${x1 + 14}" y2="${y1}" stroke="${C.steel}" stroke-width="4"/><line x1="${x0}" y1="${y1}" x2="${x0}" y2="${y0 - 10}" stroke="${C.steel}" stroke-width="4"/>`;
    s += T(x0 - 18, (y0 + y1) / 2, 'UZURĂ', { s: 16, c: C.dim, a: 'middle' }).replace('<text ', `<text transform="rotate(-90 ${x0 - 18} ${(y0 + y1) / 2})" `);
    s += T(x1, y1 + 30, 'TIMP · KILOMETRI →', { s: 15, c: C.dim, a: 'end' });
    // periodic check-ups
    const ks = [.2, .4, .6];
    const kc = ph === 0 ? Math.min(.6, .04 + pt * .16) : .6;
    ks.forEach((k, i) => { const on = kc >= k - .001; const warn = i === 2 && ph >= 1; const col = warn ? C.yel : on ? C.grn : C.steelD;
      s += `<line x1="${f(X(k))}" y1="${y0 + 18}" x2="${f(X(k))}" y2="${y1}" stroke="${col}" stroke-width="3" stroke-dasharray="8 8" opacity="${on ? .9 : .5}"/>`;
      s += T(X(k), y1 + 30, 'DIAGNOZĂ ' + (i + 1), { s: 14, c: col, a: 'middle' });
      if (on && !warn) s += check(X(k), y0 + 6, 11, C.grn, 5); });
    // wear curve up to the current point
    let d = ''; const N = 90; for (let i = 0; i <= N; i++) { const k = kc * i / N; d += (i ? 'L' : 'M') + f(X(k)) + ' ' + f(Y(w(k))); }
    s += `<path d="${d}" fill="none" stroke="${ph >= 1 ? C.yel : C.cy}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
    const px = X(kc), py = Y(w(kc));
    if (ph >= 1) { const pr = (pt * 1.4) % 1; s += `<circle cx="${f(px)}" cy="${f(py)}" r="${f(14 + pr * 34)}" fill="none" stroke="${C.yel}" stroke-width="4" opacity="${f(ph === 1 ? 1 - pr : .3 * (1 - pr))}"/>`; }
    s += `<circle cx="${f(px)}" cy="${f(py)}" r="11" fill="${ph >= 1 ? C.yel : C.cy}" stroke="#071425" stroke-width="3"/>`;
    if (ph === 1) s += tag(px - 16, py - 44, 'UZURĂ RIDICATĂ!', C.yel, 'end', 17);
    // without intervention the wear keeps rising (ghost, then the failure)
    if (ph >= 2) { const kg = ph === 2 ? Math.min(.74, .6 + pt * .05) : Math.min(.88, .74 + pt * .14); let g = '';
      for (let i = 0; i <= 40; i++) { const k = .6 + (kg - .6) * i / 40; g += (i ? 'L' : 'M') + f(X(k)) + ' ' + f(Y(w(k))); }
      s += `<path d="${g}" fill="none" stroke="${C.red}" stroke-width="${ph === 3 ? 7 : 4}" stroke-dasharray="${ph === 3 ? 'none' : '12 9'}" opacity="${ph === 3 ? 1 : .55}" stroke-linecap="round"/>`;
      if (ph === 3 && kg >= .86) { const bx = X(kg), by = Y(w(kg)); const pu = 1 + .12 * Math.sin(pt * 12); let st = '';
        for (let i = 0; i < 16; i++) { const r = (i % 2 ? 16 : 36) * pu, [sx, sy] = P2(bx, by, r, rad(i * 22.5 - 90)); st += (i ? 'L' : 'M') + f(sx) + ' ' + f(sy); }
        s += `<path d="${st}Z" fill="${C.red}" stroke="${C.yel}" stroke-width="4"/>` + tag(bx - 46, by + 10, 'CATASTROFĂ', C.red, 'end', 19); }
      // intervention in time: wear drops back and stays low
      const kr = ph === 2 ? Math.min(1, .6 + pt * .16) : 1; let r = `M ${f(X(.6))} ${f(Y(w(.6)))}`;
      for (let i = 1; i <= 40; i++) { const k = .6 + (kr - .6) * i / 40; const v = k < .63 ? lerp(w(.6), .1, (k - .6) / .03) : .1 + .08 * Math.pow((k - .63) / .37, 1.4); r += ' L' + f(X(k)) + ' ' + f(Y(v)); }
      s += `<path d="${r}" fill="none" stroke="${C.grn}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
      s += tag(X(.8), Y(.1) - 34, 'INTERVENIM LA TIMP', C.grn, 'middle', 17); }
    const H = [['DIAGNOZĂ PERIODICĂ · PARAMETRII REALI', C.cy], ['DETERMINĂM UZURA SISTEMULUI DE INJECȚIE', C.yel], ['INTERVENIM LA TIMP · PREVENIM DEFECȚIUNEA', C.grn], ['⚠ ÎN LOC SĂ TRATĂM O CATASTROFĂ', C.red]][Math.min(ph, 3)];
    s += tag(457, 412, H[0], H[1], 'middle', 18);
    return s;
  }

  // ---------- DPF (wall-flow) in section: flow, loading, regeneration, ash, clogging, cleaned ----------
  // phase = step[3] name ('flow' | 'load' | 'regen' | 'ash' | 'clog' | 'clean') or index into P.modes
  function dpfFlow(tl, ph, pt, P) {
    const mode = typeof ph === 'string' ? ph : (P.modes || ['flow', 'load', 'regen', 'ash'])[ph] || 'flow';
    const X0 = 176, X1 = 738, Y0 = 104, Y1 = 326, N = 6, CH = (Y1 - Y0 - 12) / N, PL = 26; let s = '';
    let soot = .3, ash = .12, glow = 0, block = 0;
    if (mode === 'flow') soot = .22 + .12 * eo(pt / 3);
    if (mode === 'load') soot = lerp(.3, .92, eo(pt / 2.6));
    const BURN = P.burn || 2.4; // seconds the soot takes to burn off in the regen step
    if (mode === 'regen') { soot = lerp(.92, .04, eio(pt / BURN)); ash = lerp(.12, .3, eo(pt / BURN)); glow = cl(pt / .5) * (pt < BURN ? 1 : cl(1 - (pt - BURN) / .8)); }
    if (mode === 'ash') { soot = .04; ash = .32 + .04 * Math.sin(tl * 4); }
    if (mode === 'clog') { soot = 1; ash = .62; block = 1; }
    if (mode === 'clean') { soot = 0; ash = 0; }
    // inlet / outlet pipes + cones
    s += `<path d="M 26 194 L 120 194 L ${X0} ${Y0 + 10} L ${X0} ${Y1 - 10} L 120 236 L 26 236" fill="${C.body}" stroke="${C.cy}" stroke-width="5" stroke-linejoin="round"/>`;
    s += `<path d="M 888 194 L 794 194 L ${X1} ${Y0 + 10} L ${X1} ${Y1 - 10} L 794 236 L 888 236" fill="${C.body}" stroke="${C.cy}" stroke-width="5" stroke-linejoin="round"/>`;
    s += `<rect x="${X0}" y="${Y0}" width="${X1 - X0}" height="${Y1 - Y0}" rx="16" fill="${C.body2}" stroke="${C.cy}" stroke-width="6"/>`;
    if (glow > 0) s += `<rect x="${X0 + 4}" y="${Y0 + 4}" width="${X1 - X0 - 8}" height="${Y1 - Y0 - 8}" rx="13" fill="${C.org}" opacity="${f(.28 * glow * (.85 + .15 * Math.sin(tl * 9)))}"/>`;
    for (let i = 0; i < N; i++) {
      const y0 = Y0 + 6 + i * CH, y1 = y0 + CH, inlet = i % 2 === 0;
      // plugs: inlet channels closed at the outlet end, outlet channels closed at the inlet end
      s += inlet ? `<rect x="${X1 - PL}" y="${f(y0 + 1)}" width="${PL - 4}" height="${f(CH - 2)}" fill="${C.steelD}"/>` : `<rect x="${X0 + 4}" y="${f(y0 + 1)}" width="${PL - 4}" height="${f(CH - 2)}" fill="${C.steelD}"/>`;
      if (inlet) {
        const th = soot * (CH / 2 - 3); // soot cake on both walls of the inlet channel
        if (th > .5) { const sc = block ? '#050505' : '#151515';
          s += `<rect x="${X0 + 6}" y="${f(y0 + 1)}" width="${X1 - X0 - PL - 8}" height="${f(th)}" fill="${sc}"/><rect x="${X0 + 6}" y="${f(y1 - 1 - th)}" width="${X1 - X0 - PL - 8}" height="${f(th)}" fill="${sc}"/>`;
          if (glow > .05) for (let k = 0; k < 7; k++) { const xx = X0 + 40 + k * 72 + 20 * Math.sin(tl * 3 + k + i); const fl = .5 + .5 * Math.sin(tl * 13 + k * 2 + i);
            s += `<circle cx="${f(xx)}" cy="${f(y0 + th * .6)}" r="${f(3 + 3 * fl)}" fill="${C.yel}" opacity="${f(glow * .9)}"/><circle cx="${f(xx + 30)}" cy="${f(y1 - th * .6)}" r="${f(3 + 3 * (1 - fl))}" fill="${C.org}" opacity="${f(glow * .9)}"/>`; } }
        const aw = ash * 150; if (aw > 1) s += `<rect x="${f(X1 - PL - aw)}" y="${f(y0 + 2)}" width="${f(aw)}" height="${f(CH - 4)}" rx="4" fill="#8E949C" opacity=".95"/>`;
      }
    }
    for (let i = 1; i < N; i++) { const y = Y0 + 6 + i * CH; s += `<line x1="${X0 + 4}" y1="${f(y)}" x2="${X1 - 4}" y2="${f(y)}" stroke="${C.cyD}" stroke-width="4" stroke-dasharray="12 7"/>`; }
    // moving gas (cyan) and soot (black) particles
    const speed = block ? .18 : .55;
    for (let j = 0; j < 18; j++) {
      const i = (j % 3) * 2; const y0 = Y0 + 6 + i * CH; const k = ((tl * speed + rnd(j) ) % 1); const isSoot = j % 3 === 1 && mode !== 'clean';
      let x, y;
      if (k < .18) { x = lerp(30, X0 + 8, k / .18); y = lerp(215, y0 + CH / 2, k / .18); }
      else if (k < .62) { x = lerp(X0 + 8, X0 + 70 + rnd(j + 7) * (X1 - X0 - 180), (k - .18) / .44); y = y0 + CH / 2; }
      else if (isSoot) { x = X0 + 70 + rnd(j + 7) * (X1 - X0 - 180); y = y0 + CH / 2 + (rnd(j + 3) > .5 ? -1 : 1) * (CH / 2 - 4 - soot * (CH / 2 - 6)); }
      else if (block) { x = X0 + 70 + rnd(j + 7) * (X1 - X0 - 180) + 4 * Math.sin(tl * 9 + j); y = y0 + CH / 2; }
      else { const xs = X0 + 70 + rnd(j + 7) * (X1 - X0 - 180); const yo = y0 + CH / 2 + CH * (rnd(j + 3) > .5 ? 1 : -1) * (i === 0 ? 1 : (i === N - 2 ? -1 : 1));
        if (k < .74) { x = xs; y = lerp(y0 + CH / 2, yo, (k - .62) / .12); } else { x = lerp(xs, 900, (k - .74) / .26); y = x > X1 ? lerp(yo, 215, cl((x - X1) / 60)) : yo; } }
      s += isSoot ? `<circle cx="${f(x)}" cy="${f(y)}" r="7" fill="#111" stroke="#bbb" stroke-width="1.5"/>` : `<circle cx="${f(x)}" cy="${f(y)}" r="5" fill="${C.cy}" opacity=".85"/>`;
    }
    // labels
    s += tag(10, 160, mode === 'clean' ? 'GAZE' : 'GAZE + FUNINGINE', mode === 'clean' ? C.cy : C.dim, 'start', 15);
    s += tag(904, 160, block ? 'BLOCAT' : 'GAZE CURATE', block ? C.red : C.grn, 'end', 15);
    const L = Object.assign({ flow: ['FILTREAZĂ PARTICULELE', C.cy], load: ['SE ÎNCARCĂ CU FUNINGINE', C.red], regen: ['REGENERARE: FUNINGINEA ARDE', C.yel], ash: ['RĂMÂNE CENUȘA', '#C9CED4'],
      clog: ['DPF ÎNFUNDAT', C.red], clean: ['CURĂȚAT', C.grn] }, P.labels || {})[mode];
    s += tag(457, 372, L[0], L[1], 'middle', 22);
    if (mode === 'clog') { s += xmark(457, 215, 34, C.red, 10); s += tag(457, 62, 'CONTRAPRESIUNE MARE', C.red, 'middle', 17); }
    if (mode === 'clean') s += check(457, 215, 34, C.grn, 10);
    s += T(457, 420, P.cap || 'FILTRU DE PARTICULE · SECȚIUNE', { s: 15, c: C.dim, a: 'middle' });
    return s;
  }

  // ---------- DPF: the three regeneration types (passive / active / forced) ----------
  // ph = 0 pasivă, 1 activă, 2 forțată (index of the highlighted panel); P.all = true shows all three lit
  function regenModes(tl, ph, pt, P) {
    let s = ''; const cols = [[152, 'PASIVĂ', 'racing_car', ['MERS LUNG, TURAȚIE', 'ARDE SINGURĂ'], C.grn], [457, 'ACTIVĂ', 'brain', ['CALCULATORUL VEDE', 'DPF ÎNCĂRCAT'], C.yel], [762, 'FORȚATĂ', 'wrench', ['ÎN SERVICE,', 'CU TESTERUL'], C.org]];
    cols.forEach(([x, lab, em, lines, col], i) => {
      const on = P.all || i === ph, seen = i <= ph || P.all, k = i === ph ? eo(pt / .45) : 1;
      if (!seen) { s += `<rect x="${x - 136}" y="58" width="272" height="300" rx="20" fill="${C.body}" stroke="${C.cyD}" stroke-width="3" stroke-dasharray="10 8" opacity=".55"/>` + T(x, 220, '?', { s: 64, a: 'middle', c: C.dim }); return; }
      const op = on ? 1 : .45; const sc = i === ph ? lerp(.82, 1, k) : 1;
      s += `<g transform="translate(${x} 208) scale(${f(sc)}) translate(${-x} -208)" opacity="${op}">`;
      s += `<rect x="${x - 136}" y="58" width="272" height="300" rx="20" fill="${C.body}" stroke="${on ? col : C.cyD}" stroke-width="${on ? 6 : 3}"/>`;
      s += T(x, 104, lab, { s: 30, a: 'middle', c: col, ls: 3 });
      s += emoji(x, 176, 84, em);
      // little DPF bar: soot level falls as it burns
      const lvl = i === 0 ? .55 - .25 * cl(pt / 2) : i === 1 ? .9 - .6 * cl(pt / 2.2) : 1 - .85 * cl(pt / 2.4);
      s += `<rect x="${x - 96}" y="236" width="192" height="26" rx="8" fill="${C.body2}" stroke="${C.cy}" stroke-width="3"/><rect x="${x - 93}" y="239" width="${f(186 * (i === ph || P.all ? lvl : .3))}" height="20" rx="6" fill="#151515"/>`;
      if (i === ph) s += glowC(x - 93 + 186 * lvl, 249, 14 + 4 * Math.sin(tl * 9), C.org, .55);
      s += T(x, 300, lines[0], { s: 17, a: 'middle', c: C.w, ls: 1 }) + T(x, 326, lines[1], { s: 17, a: 'middle', c: C.w, ls: 1 });
      s += '</g>';
    });
    s += T(457, 404, P.cap || 'REGENERAREA FILTRULUI DE PARTICULE · 3 TIPURI', { s: 15, c: C.dim, a: 'middle' });
    return s;
  }

  // ---------- post-injection: fuel injected late (exhaust stroke) burns in the DPF and heats it for regeneration ----------
  // phase = 'main' | 'post' | 'weak' (worn injector: too little post-injection, DPF stays cold) or index into P.modes
  function postInject(tl, ph, pt, P) {
    const mode = typeof ph === 'string' ? ph : (P.modes || ['main', 'post', 'weak'])[ph] || 'main';
    let s = ''; const cx = 230, cyl = [150, 70, 310, 330];
    // piston position: main = near TDC, post/weak = moving down then up (exhaust stroke)
    const cyc = (tl * .7) % 1; const py = mode === 'main' ? 150 + 20 * Math.sin(tl * 3) : 150 + 120 * Math.sin(cyc * Math.PI);
    s += `<rect x="${cyl[0]}" y="${cyl[1]}" width="${cyl[2] - cyl[0]}" height="${cyl[3] - cyl[1]}" fill="${C.body2}" stroke="${C.cy}" stroke-width="6" rx="6"/>`;
    s += `<rect x="${cyl[0] + 8}" y="${f(py)}" width="${cyl[2] - cyl[0] - 16}" height="70" rx="6" fill="${C.steelD}" stroke="${C.steel}" stroke-width="3"/>`;
    s += `<line x1="${cx}" y1="${f(py + 70)}" x2="${cx}" y2="400" stroke="${C.steel}" stroke-width="12"/>`;
    // injector on top
    s += `<rect x="${cx - 14}" y="18" width="28" height="64" rx="6" fill="${C.steel}"/>` + T(cx, 14, 'INJECTOR', { s: 15, a: 'middle', c: C.dim });
    // exhaust valve + pipe to the DPF
    s += `<path d="M ${cyl[2]} 92 L 520 92 L 520 128 L ${cyl[2]} 128" fill="${C.body}" stroke="${C.cy}" stroke-width="5"/>`;
    const hot = mode === 'post' ? cl(pt / 1.6) : 0, cold = mode === 'weak';
    const sprayAmt = mode === 'main' ? 1 : mode === 'post' ? .75 : .22;
    const sprayOn = mode === 'main' ? (Math.sin(tl * 6) > -.2) : (cyc > .05 && cyc < .4);
    if (sprayOn) for (let i = -2; i <= 2; i++) { const a = rad(90 + i * 14); const L = 30 + 60 * sprayAmt; s += `<line x1="${cx}" y1="84" x2="${f(cx + Math.cos(a) * L)}" y2="${f(84 + Math.sin(a) * L)}" stroke="${C.oil}" stroke-width="${f(3 + 4 * sprayAmt)}" stroke-linecap="round" opacity=".9"/>`; }
    if (mode === 'main') { const fl = .6 + .4 * Math.sin(tl * 11); s += glowC(cx, 120, 46 * fl, C.org, .45) + glowC(cx, 120, 24 * fl, C.yel, .6); s += tag(457, 372, 'INJECȚIA PRINCIPALĂ: ARDE ÎN CILINDRU', C.cy, 'middle', 16); }
    // fuel vapour travelling to the DPF
    if (mode !== 'main') for (let i = 0; i < 8; i++) { const k = ((tl * .5 + i / 8) % 1); const x = lerp(cyl[2], 600, k); s += `<circle cx="${f(x)}" cy="${f(110 + 6 * Math.sin(k * 9 + i))}" r="${f(mode === 'weak' ? 4 : 7)}" fill="${C.oil}" opacity="${f((mode === 'weak' ? .45 : .9) * (1 - k * .3))}"/>`; }
    // DPF block at right
    const X0 = 600, X1 = 880, Y0 = 70, Y1 = 330;
    s += `<rect x="${X0}" y="${Y0}" width="${X1 - X0}" height="${Y1 - Y0}" rx="16" fill="${C.body2}" stroke="${C.cy}" stroke-width="6"/>`;
    s += `<path d="M 520 92 L ${X0} ${Y0 + 30} M 520 128 L ${X0} ${Y0 + 70}" stroke="${C.cy}" stroke-width="5"/>`;
    const soot = mode === 'post' ? lerp(.9, .15, eio(cl(pt / 3))) : mode === 'weak' ? .9 - .1 * cl(pt / 3) : .6;
    for (let i = 0; i < 6; i++) { const y = Y0 + 16 + i * 40; s += `<rect x="${X0 + 14}" y="${y}" width="${f((X1 - X0 - 28) * soot)}" height="22" rx="5" fill="#151515"/>`; }
    if (hot > 0) s += `<rect x="${X0 + 4}" y="${Y0 + 4}" width="${X1 - X0 - 8}" height="${Y1 - Y0 - 8}" rx="13" fill="${C.org}" opacity="${f(.32 * hot * (.85 + .15 * Math.sin(tl * 9)))}"/>`;
    if (hot > .3) for (let k = 0; k < 6; k++) s += glowC(X0 + 40 + k * 40 + 10 * Math.sin(tl * 4 + k), Y0 + 40 + (k % 3) * 80, 6 + 3 * Math.sin(tl * 12 + k), C.yel, .8 * hot);
    s += T((X0 + X1) / 2, Y0 - 14, 'DPF', { s: 22, a: 'middle', c: C.cy });
    if (mode === 'post') { s += tag(712, 372, 'DPF ÎNCINS: FUNINGINEA ARDE', C.yel, 'middle', 15); s += tag(250, 372, 'POST-INJECȚIE PE EVACUARE', C.oil, 'middle', 15); }
    if (mode === 'weak') { s += tag(712, 372, 'REGENERARE INCOMPLETĂ', C.red, 'middle', 15); s += tag(250, 372, 'INJECTOR UZAT: PREA PUȚIN', C.red, 'middle', 15); s += xmark(840, 40, 18, C.red, 7); }
    s += T(457, 420, P.cap || 'POST-INJECȚIA · CUM SE ÎNCĂLZEȘTE DPF-UL', { s: 15, c: C.dim, a: 'middle' });
    return s;
  }

  // ---------- EGR loop: part of the exhaust gas goes back to the intake through the EGR valve ----------
  // phase = 'ok' | 'dirty' (deposits, valve stuck open: too much gas back -> incomplete burn -> more soot to the DPF) or index into P.modes
  function egrLoop(tl, ph, pt, P) {
    const mode = typeof ph === 'string' ? ph : (P.modes || ['ok', 'dirty'])[ph] || 'ok';
    const bad = mode === 'dirty'; let s = '';
    // engine block in the middle
    s += `<rect x="330" y="150" width="254" height="200" rx="18" fill="${C.body2}" stroke="${C.cy}" stroke-width="6"/>` + T(457, 262, 'MOTOR', { s: 26, a: 'middle', c: C.w });
    const fl = .6 + .4 * Math.sin(tl * 10); s += glowC(457, 300, 22 * fl, bad ? C.smoke : C.org, bad ? .5 : .5);
    // intake (left) and exhaust (right) pipes
    s += `<path d="M 30 250 L 330 250" stroke="${C.cy}" stroke-width="30" stroke-linecap="round" opacity=".35"/>` + T(40, 226, 'AER PROASPĂT', { s: 15, c: C.cy });
    s += `<path d="M 584 250 L 890 250" stroke="${C.smoke}" stroke-width="30" stroke-linecap="round" opacity=".35"/>` + T(880, 226, 'SPRE DPF', { s: 15, c: bad ? C.red : C.smoke, a: 'end' });
    // EGR loop on top: exhaust -> valve -> intake
    s += `<path d="M 700 250 L 700 70 L 214 70 L 214 250" fill="none" stroke="${C.smoke}" stroke-width="22" stroke-linejoin="round" opacity=".35"/>`;
    const vx = 457, vy = 70; const open = bad ? 1 : .35 + .3 * Math.sin(tl * 1.4);
    s += `<circle cx="${vx}" cy="${vy}" r="40" fill="${C.body}" stroke="${bad ? C.red : C.cy}" stroke-width="6"/>`;
    s += `<line x1="${f(vx - 30 * Math.cos(open * 1.4))}" y1="${f(vy - 30 * Math.sin(open * 1.4))}" x2="${f(vx + 30 * Math.cos(open * 1.4))}" y2="${f(vy + 30 * Math.sin(open * 1.4))}" stroke="${C.w}" stroke-width="8" stroke-linecap="round"/>`;
    if (bad) for (let i = 0; i < 9; i++) { const a = rad(i * 40 + 10); s += `<circle cx="${f(vx + Math.cos(a) * 30)}" cy="${f(vy + Math.sin(a) * 30)}" r="7" fill="#111"/>`; }
    s += T(vx, 140, bad ? 'EGR ÎNCĂRCAT · NU MAI ÎNCHIDE' : 'SUPAPA EGR', { s: 16, a: 'middle', c: bad ? C.red : C.cy });
    // particles: fresh air (cyan), recirculated gas (grey), soot (black)
    const nR = bad ? 12 : 5;
    for (let i = 0; i < nR; i++) { const k = ((tl * .45 + i / nR) % 1); let x, y;
      if (k < .2) { x = 700; y = lerp(250, 70, k / .2); } else if (k < .8) { x = lerp(700, 214, (k - .2) / .6); y = 70; } else { x = 214; y = lerp(70, 250, (k - .8) / .2); }
      s += `<circle cx="${f(x)}" cy="${f(y)}" r="7" fill="${C.smoke}" opacity=".9"/>`; }
    const nA = bad ? 3 : 7;
    for (let i = 0; i < nA; i++) { const k = ((tl * .6 + i / nA) % 1); s += `<circle cx="${f(lerp(30, 330, k))}" cy="${f(250 + 6 * Math.sin(i))}" r="7" fill="${C.cy}"/>`; }
    const nS = bad ? 10 : 3;
    for (let i = 0; i < nS; i++) { const k = ((tl * .6 + i / nS) % 1); s += `<circle cx="${f(lerp(584, 890, k))}" cy="${f(250 + 8 * Math.sin(i * 2))}" r="${bad ? 8 : 6}" fill="#111" stroke="#bbb" stroke-width="1.5"/>`; }
    if (bad) { s += tag(457, 392, 'ARDERE INCOMPLETĂ → MAI MULTĂ FUNINGINE ÎN DPF', C.red, 'middle', 17); }
    else s += tag(457, 392, 'RECIRCULĂ DOAR O PARTE DIN GAZE', C.grn, 'middle', 17);
    return s;
  }
  return { _gauge, turboPlay, turboOil, injectorSpray, chainSkip, wastegate, pistonSeize, systemMap, oilPaths, railPressure, engineSwap, camTiming, coolingHybrid, oilFilter, camWear, route, sensorFeedback, fuelFilterFlow, pressureLag, tankCondens, liveData, injectorReturn, supplyChain, controlLoop, scopeTrace, wearCurve, dpfFlow, regenModes, postInject, egrLoop };
})();
