// Original vector illustrations for the reel (drawn for Turbo Doctor; no third-party artwork).
window.ART = (() => {
  const blades = (n, r0, r1, fill, stroke) => {
    let s = '';
    for (let i = 0; i < n; i++) {
      s += `<path transform="rotate(${(360 / n) * i})" d="M -6 ${-r0} C 8 ${-r0 - 18} 16 ${-(r0 + r1) / 2 - 8} 10 ${-r1} L 22 ${-r1 + 2} C 26 ${-(r0 + r1) / 2 - 4} 16 ${-r0 - 12} 6 ${-r0 + 1} Z" fill="${fill}" stroke="${stroke}" stroke-width="2.5" stroke-linejoin="round"/>`;
    }
    return s;
  };
  const hex = (r) => Array.from({ length: 6 }, (_, i) => {
    const a = Math.PI / 6 + (i * Math.PI) / 3; return `${(r * Math.cos(a)).toFixed(1)},${(r * Math.sin(a)).toFixed(1)}`;
  }).join(' ');

  function turbo(p = 't') {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 340" width="420" height="340">
<defs>
 <linearGradient id="${p}Alu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="#D6DCE2"/><stop offset=".75" stop-color="#9CA6B1"/><stop offset="1" stop-color="#6C7683"/></linearGradient>
 <linearGradient id="${p}Iron" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C08456"/><stop offset=".55" stop-color="#7E4B2E"/><stop offset="1" stop-color="#3C2215"/></linearGradient>
 <linearGradient id="${p}Steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C3CAD2"/><stop offset="1" stop-color="#5B6470"/></linearGradient>
 <radialGradient id="${p}Bore" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3B424B"/><stop offset="1" stop-color="#0E1115"/></radialGradient>
</defs>
<g transform="translate(300 200)">
 <rect x="-44" y="62" width="88" height="54" rx="8" fill="#6E4129" stroke="#26150C" stroke-width="5"/>
 <circle r="90" fill="url(#${p}Iron)" stroke="#26150C" stroke-width="5"/>
 <path d="M -78 -44 A 90 90 0 0 1 30 -84" fill="none" stroke="#E2AC7C" stroke-width="7" stroke-linecap="round" opacity=".55"/>
 <circle r="40" fill="#2B1A11" stroke="#160C07" stroke-width="5"/><circle r="22" fill="#4C3425"/>
</g>
<rect x="196" y="148" width="74" height="104" rx="14" fill="url(#${p}Steel)" stroke="#2C323A" stroke-width="5"/>
<rect x="214" y="122" width="38" height="32" rx="7" fill="#8C959F" stroke="#2C323A" stroke-width="5"/>
<g transform="translate(150 190)">
 <path d="M -112 0 L -112 -158 L -50 -158 L -50 -60 Z" fill="url(#${p}Alu)" stroke="#39414B" stroke-width="5" stroke-linejoin="round"/>
 <rect x="-124" y="-176" width="86" height="24" rx="7" fill="#CDD3DA" stroke="#39414B" stroke-width="5"/>
 <circle r="112" fill="url(#${p}Alu)" stroke="#39414B" stroke-width="6"/>
 <path d="M 18 -110 A 112 112 0 0 0 -100 50" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" opacity=".6"/>
 <path d="M 0 -96 A 96 96 0 1 1 -88 38" fill="none" stroke="#8D97A2" stroke-width="3" opacity=".7"/>
 <circle r="72" fill="#7E8893" stroke="#39414B" stroke-width="5"/>
 <circle r="62" fill="url(#${p}Bore)"/>
 <g>${blades(10, 15, 58, '#E9EDF1', '#56606B')}</g>
 <circle r="17" fill="#F3F5F7" stroke="#56606B" stroke-width="3"/>
 <polygon points="${hex(8)}" fill="#8E98A3"/>
</g>
</svg>`;
  }

  function core(broken = true, p = 'c') {
    const tw = broken ? 'transform="translate(26 14) rotate(7 330 150)"' : '';
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300" width="480" height="300">
<defs>
 <linearGradient id="${p}Alu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".4" stop-color="#D3D9DF"/><stop offset="1" stop-color="#7A8490"/></linearGradient>
 <linearGradient id="${p}Steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9D0D7"/><stop offset=".5" stop-color="#8E98A3"/><stop offset="1" stop-color="#555E6A"/></linearGradient>
 <linearGradient id="${p}Hot" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9C8270"/><stop offset=".5" stop-color="#6A5446"/><stop offset="1" stop-color="#3A2C24"/></linearGradient>
</defs>
<path d="M 178 48 L 178 252 L 162 252 C 122 236 92 188 70 162 L 70 138 C 92 112 122 64 162 48 Z" fill="url(#${p}Alu)" stroke="#39414B" stroke-width="5" stroke-linejoin="round"/>
<g fill="none" stroke="#6E7884" stroke-width="3" stroke-linecap="round">
 <path d="M 80 146 C 104 120 134 86 174 62"/><path d="M 80 154 C 104 180 134 214 174 238"/>
 <path d="M 92 132 C 120 112 146 96 174 92"/><path d="M 92 168 C 120 188 146 204 174 208"/>
 <path d="M 100 150 L 174 150"/>
</g>
<rect x="52" y="138" width="22" height="24" rx="4" fill="#9AA3AD" stroke="#39414B" stroke-width="4"/>
<rect x="178" y="78" width="132" height="144" rx="18" fill="url(#${p}Steel)" stroke="#2C323A" stroke-width="5"/>
<rect x="222" y="40" width="44" height="44" rx="8" fill="#9AA3AD" stroke="#2C323A" stroke-width="5"/>
<rect x="230" y="216" width="28" height="40" rx="6" fill="#7F8994" stroke="#2C323A" stroke-width="5"/>
<path d="M 196 96 L 292 96" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".45"/>
${broken ? `<rect x="296" y="138" width="40" height="22" fill="#B8C0C8" stroke="#2C323A" stroke-width="4"/>
<path d="M 302 70 L 288 108 L 304 128 L 286 156 L 306 182 L 292 230" fill="none" stroke="#FF3B3B" stroke-width="22" opacity=".35" stroke-linejoin="round"/>
<path d="M 302 70 L 288 108 L 304 128 L 286 156 L 306 182 L 292 230" fill="none" stroke="#FF2A2A" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>` : `<rect x="300" y="140" width="22" height="20" fill="#B8C0C8" stroke="#2C323A" stroke-width="4"/>`}
<g ${tw}>
 <path d="M 318 70 L 318 230 L 330 230 C 362 214 386 180 404 160 L 404 140 C 386 120 362 86 330 70 Z" fill="url(#${p}Hot)" stroke="#2A1F19" stroke-width="5" stroke-linejoin="round"/>
 <g fill="none" stroke="#2A1F19" stroke-width="3" opacity=".6"><path d="M 396 146 C 376 128 354 104 324 84"/><path d="M 396 154 C 376 172 354 196 324 216"/><path d="M 392 150 L 324 150"/></g>
 <rect x="402" y="140" width="18" height="20" rx="4" fill="#7A6658" stroke="#2A1F19" stroke-width="4"/>
</g>
${broken ? `<g fill="#3B424B"><path d="M 350 52 l 14 -6 l 4 12 z"/><path d="M 382 248 l 12 8 l -10 8 z"/><path d="M 300 28 l 10 -2 l -2 12 z"/></g>` : ''}
</svg>`;
  }

  function dpf(p = 'd') {
    let clean = '', soot = '';
    const cols = 10, rows = 6, pitch = 18, x0 = 171, y0 = 76;
    let seed = 7;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      const x = x0 + c * pitch, y = y0 + r * pitch;
      clean += `<rect x="${x}" y="${y}" width="14" height="14" rx="2" fill="#F5EFE4"/>`;
      const g = Math.floor(18 + rnd() * 30);
      soot += `<rect x="${x}" y="${y}" width="14" height="14" rx="2" fill="rgb(${g},${g},${g})"/>`;
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" width="520" height="260">
<defs>
 <linearGradient id="${p}Body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7CDB1"/><stop offset=".35" stop-color="#B98C66"/><stop offset=".75" stop-color="#7C573E"/><stop offset="1" stop-color="#4D3424"/></linearGradient>
 <linearGradient id="${p}Steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D2D8DE"/><stop offset="1" stop-color="#626B77"/></linearGradient>
</defs>
<rect x="0" y="106" width="66" height="50" rx="8" fill="url(#${p}Steel)" stroke="#33302C" stroke-width="5"/>
<rect x="454" y="106" width="66" height="50" rx="8" fill="url(#${p}Steel)" stroke="#33302C" stroke-width="5"/>
<path d="M 60 98 L 112 50 L 112 210 L 60 162 Z" fill="url(#${p}Body)" stroke="#33261C" stroke-width="5" stroke-linejoin="round"/>
<path d="M 460 98 L 408 50 L 408 210 L 460 162 Z" fill="url(#${p}Body)" stroke="#33261C" stroke-width="5" stroke-linejoin="round"/>
<rect x="100" y="40" width="320" height="180" rx="38" fill="url(#${p}Body)" stroke="#33261C" stroke-width="6"/>
<path d="M 132 58 L 388 58" stroke="#FFF6EA" stroke-width="8" stroke-linecap="round" opacity=".55"/>
<path d="M 140 44 L 140 216 M 380 44 L 380 216" stroke="#33261C" stroke-width="5" opacity=".7"/>
<rect x="164" y="68" width="192" height="122" rx="14" fill="#0D0D0D" stroke="#F0E6D8" stroke-width="5"/>
<g id="${p}Clean">${clean}</g>
<g id="${p}Soot">${soot}</g>
</svg>`;
  }

  function pipe(p = 'p') {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 300" width="840" height="300">
<defs>
 <linearGradient id="${p}Steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E3E8ED"/><stop offset=".5" stop-color="#A5AEB8"/><stop offset="1" stop-color="#5E6774"/></linearGradient>
 <clipPath id="${p}OilClip"><rect id="${p}OilRect" x="100" y="100" width="300" height="100"/></clipPath>
</defs>
<path d="M 120 150 L 600 150" stroke="#39414B" stroke-width="58" stroke-linecap="round"/>
<path d="M 120 150 L 600 150" stroke="url(#${p}Steel)" stroke-width="46" stroke-linecap="round"/>
<path d="M 120 150 L 600 150" stroke="#1E2228" stroke-width="26" stroke-linecap="round"/>
<g clip-path="url(#${p}OilClip)"><path id="${p}Oil" d="M 120 150 L 610 150" stroke="#F4A30C" stroke-width="18" stroke-dasharray="30 16" stroke-linecap="round"/></g>
<g id="${p}Clog" transform="translate(372 150)">
 <path d="M -30 -10 C -34 -26 -8 -30 4 -22 C 20 -32 38 -16 32 0 C 40 14 22 30 6 22 C -10 32 -36 22 -30 6 Z" fill="#141414" stroke="#FF3B3B" stroke-width="5"/>
 <circle cx="-8" cy="-4" r="5" fill="#3A3A3A"/><circle cx="12" cy="8" r="4" fill="#2C2C2C"/><circle cx="6" cy="-12" r="3" fill="#444"/>
</g>
<g transform="translate(120 150)"><circle r="42" fill="url(#${p}Steel)" stroke="#39414B" stroke-width="5"/><polygon points="${hex(24)}" fill="#7D8792" stroke="#39414B" stroke-width="4"/><circle r="9" fill="#39414B"/></g>
<g transform="translate(600 150)"><circle r="42" fill="url(#${p}Steel)" stroke="#39414B" stroke-width="5"/><polygon points="${hex(24)}" fill="#7D8792" stroke="#39414B" stroke-width="4"/><circle r="9" fill="#39414B"/></g>
</svg>`;
  }

  function gauge(p = 'g') {
    // 270 deg sweep from -225 (min) to +45 (max)
    const R = 112, cx = 160, cy = 160;
    const pt = (a, r) => [cx + r * Math.cos((a * Math.PI) / 180), cy + r * Math.sin((a * Math.PI) / 180)];
    const arc = (a0, a1, r, col, w) => {
      const [x0, y0] = pt(a0, r), [x1, y1] = pt(a1, r);
      return `<path d="M ${x0.toFixed(1)} ${y0.toFixed(1)} A ${r} ${r} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1.toFixed(1)} ${y1.toFixed(1)}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="butt"/>`;
    };
    let ticks = '';
    for (let i = 0; i <= 10; i++) {
      const a = -225 + 27 * i; const [x0, y0] = pt(a, 96), [x1, y1] = pt(a, i % 5 === 0 ? 74 : 82);
      ticks += `<line x1="${x0.toFixed(1)}" y1="${y0.toFixed(1)}" x2="${x1.toFixed(1)}" y2="${y1.toFixed(1)}" stroke="#1F242A" stroke-width="${i % 5 === 0 ? 6 : 4}" stroke-linecap="round"/>`;
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" width="320" height="320">
<defs><linearGradient id="${p}Bezel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F1F4F7"/><stop offset=".5" stop-color="#9AA4AF"/><stop offset="1" stop-color="#4F5865"/></linearGradient></defs>
<circle cx="160" cy="160" r="152" fill="url(#${p}Bezel)" stroke="#2C323A" stroke-width="5"/>
<circle cx="160" cy="160" r="132" fill="#FFFFFF" stroke="#2C323A" stroke-width="4"/>
${arc(-225, -184, R, '#FF3B3B', 16)}${arc(-184, -157, R, '#FFC21A', 16)}${arc(-157, 18, R, '#22C55E', 16)}${arc(18, 45, R, '#FF9F1C', 16)}
${ticks}
<text x="160" y="232" text-anchor="middle" font-family="Mont" font-weight="900" font-size="26" fill="#1F242A">BAR</text>
<g id="${p}Needle" transform="rotate(-225 160 160)">
 <path d="M 160 150 L 262 158 L 262 162 L 160 170 Z" fill="#E11D2E" stroke="#7A0E17" stroke-width="2"/>
</g>
<circle cx="160" cy="160" r="20" fill="#1F242A"/><circle cx="160" cy="160" r="7" fill="#9AA4AF"/>
</svg>`;
  }

  function intake(p = 'i') {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 300" width="460" height="300">
<defs><linearGradient id="${p}Alu" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F6F8"/><stop offset="1" stop-color="#7C8691"/></linearGradient>
<linearGradient id="${p}Pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A626C"/><stop offset="1" stop-color="#22272D"/></linearGradient></defs>
<g fill="none" stroke-linecap="round">
 ${[150, 220, 290, 360].map((x, i) => `<path d="M ${x} 110 C ${x} 160 ${x - 20 + i * 4} 190 ${x - 22 + i * 6} 226" stroke="#1B1F24" stroke-width="50"/><path d="M ${x} 110 C ${x} 160 ${x - 20 + i * 4} 190 ${x - 22 + i * 6} 226" stroke="url(#${p}Pl)" stroke-width="40"/><path d="M ${x - 10} 120 C ${x - 10} 160 ${x - 28 + i * 4} 188 ${x - 30 + i * 6} 218" stroke="#7D8792" stroke-width="7" opacity=".55"/>`).join('')}
</g>
<rect x="96" y="222" width="300" height="38" rx="9" fill="#7A838E" stroke="#2C323A" stroke-width="5"/>
<rect x="92" y="38" width="320" height="84" rx="42" fill="url(#${p}Pl)" stroke="#16191D" stroke-width="6"/>
<path d="M 128 56 L 378 56" stroke="#9AA3AD" stroke-width="8" stroke-linecap="round" opacity=".5"/>
<g transform="translate(78 80)"><circle r="52" fill="url(#${p}Alu)" stroke="#2C323A" stroke-width="6"/><circle r="34" fill="#1C2026"/><path d="M -26 18 L 26 -18" stroke="#B9C1CA" stroke-width="7" stroke-linecap="round"/></g>
</svg>`;
  }

  function ecg(w, h, color, id) {
    // one heartbeat every 300px
    let d = `M 0 ${h / 2}`; const m = h / 2;
    for (let x = 0; x < w; x += 300) {
      d += ` L ${x + 110} ${m} L ${x + 128} ${m - h * 0.12} L ${x + 146} ${m} L ${x + 160} ${m} L ${x + 172} ${m + h * 0.16} L ${x + 188} ${m - h * 0.46} L ${x + 204} ${m + h * 0.38} L ${x + 218} ${m} L ${x + 246} ${m} L ${x + 266} ${m - h * 0.14} L ${x + 286} ${m} L ${x + 300} ${m}`;
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<path d="${d}" fill="none" stroke="${color}" stroke-width="14" stroke-linejoin="round" opacity=".25" id="${id}Glow"/>
<path d="${d}" fill="none" stroke="${color}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round" id="${id}"/>
</svg>`;
  }

  const SHIELD = 'M180 14 L340 64 L332 222 C324 320 252 380 180 410 C108 380 36 320 28 222 L20 64 Z';
  function shield(p = 's') {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 424" width="360" height="424">
<defs><linearGradient id="${p}Navy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1C4377"/><stop offset="1" stop-color="#0A1A33"/></linearGradient>
<linearGradient id="${p}Gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE48A"/><stop offset=".5" stop-color="#F5C542"/><stop offset="1" stop-color="#C8921A"/></linearGradient></defs>
<path d="${SHIELD}" fill="url(#${p}Navy)" stroke="url(#${p}Gold)" stroke-width="14" stroke-linejoin="round"/>
<path d="${SHIELD}" transform="translate(180 212) scale(.88) translate(-180 -212)" fill="none" stroke="#F5C542" stroke-width="3" opacity=".55"/>
</svg>`;
  }


  function injector(p = 'j') {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 470" width="220" height="470">
<defs><linearGradient id="${p}St" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6B7480"/><stop offset=".35" stop-color="#E9EDF1"/><stop offset=".6" stop-color="#B7C0C9"/><stop offset="1" stop-color="#5A636F"/></linearGradient>
<linearGradient id="${p}Pl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1E2227"/><stop offset=".4" stop-color="#4A525C"/><stop offset="1" stop-color="#16191D"/></linearGradient>
<linearGradient id="${p}Br" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7A5A2E"/><stop offset=".4" stop-color="#E2B866"/><stop offset="1" stop-color="#6E4F24"/></linearGradient></defs>
<rect x="58" y="14" width="104" height="70" rx="14" fill="url(#${p}Pl)" stroke="#0E1013" stroke-width="5"/>
<rect x="74" y="0" width="72" height="26" rx="8" fill="#2E343B" stroke="#0E1013" stroke-width="5"/>
<rect x="160" y="34" width="22" height="34" rx="6" fill="#2E343B" stroke="#0E1013" stroke-width="5"/>
<rect x="66" y="82" width="88" height="128" rx="12" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5"/>
<path d="M 66 116 L 154 116 M 66 150 L 154 150 M 66 184 L 154 184" stroke="#2C323A" stroke-width="4"/>
<g transform="translate(154 128)"><rect x="0" y="0" width="38" height="30" rx="5" fill="url(#${p}Br)" stroke="#3B2A12" stroke-width="5"/><rect x="34" y="-4" width="20" height="38" rx="5" fill="#C99A4A" stroke="#3B2A12" stroke-width="5"/></g>
<path d="M 74 208 L 146 208 L 138 338 L 82 338 Z" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5" stroke-linejoin="round"/>
<rect x="70" y="330" width="80" height="54" rx="8" fill="url(#${p}Br)" stroke="#3B2A12" stroke-width="5"/>
<path d="M 92 384 L 128 384 L 122 440 C 120 456 100 456 98 440 Z" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5" stroke-linejoin="round"/>
<path d="M 84 96 L 84 200" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".5"/>
</svg>`;
  }

  function rocker(broken = true, p = 'r') {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 240" width="460" height="240">
<defs><linearGradient id="${p}St" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9EDF1"/><stop offset=".5" stop-color="#9AA4AF"/><stop offset="1" stop-color="#4F5865"/></linearGradient>
<radialGradient id="${p}Ro" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="#B9C1CA"/><stop offset="1" stop-color="#555E6A"/></radialGradient></defs>
<path d="M 40 150 C 40 118 70 104 104 108 L 196 116 L 196 168 L 100 176 C 64 180 40 176 40 150 Z" fill="url(#${p}St)" stroke="#2C323A" stroke-width="6" stroke-linejoin="round"/>
<circle cx="74" cy="146" r="20" fill="#3B424B" stroke="#2C323A" stroke-width="4"/>
<g ${broken ? 'transform="translate(30 18) rotate(10 260 140)"' : ''}>
 <path d="M 226 116 L 352 106 C 392 104 420 120 420 146 C 420 170 396 180 360 176 L 226 168 Z" fill="url(#${p}St)" stroke="#2C323A" stroke-width="6" stroke-linejoin="round"/>
 <path d="M 370 128 L 404 128 L 404 162 L 370 162 Z" fill="#7D8792" stroke="#2C323A" stroke-width="4"/>
</g>
<circle cx="212" cy="142" r="46" fill="url(#${p}Ro)" stroke="#2C323A" stroke-width="6"/>
<circle cx="212" cy="142" r="14" fill="#5B6470" stroke="#2C323A" stroke-width="4"/>
${broken ? `<path d="M 238 96 L 226 122 L 244 140 L 228 160 L 246 188" fill="none" stroke="#FF3B3B" stroke-width="20" opacity=".35" stroke-linejoin="round"/>
<path d="M 238 96 L 226 122 L 244 140 L 228 160 L 246 188" fill="none" stroke="#FF2A2A" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
<g fill="#3B424B"><path d="M 250 60 l 14 -6 l 4 12 z"/><path d="M 280 214 l 12 8 l -10 8 z"/><path d="M 214 44 l 10 -2 l -2 12 z"/></g>` : ''}
</svg>`;
  }

  function intakeDirty(p = 'id') {
    let soot = '';
    let seed = 5; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    for (let i = 0; i < 46; i++) {
      const onPl = i < 22; const x = onPl ? 110 + rnd() * 290 : 120 + rnd() * 260; const y = onPl ? 48 + rnd() * 68 : 120 + rnd() * 100;
      soot += `<ellipse cx="${x.toFixed(0)}" cy="${y.toFixed(0)}" rx="${(6 + rnd() * 16).toFixed(0)}" ry="${(4 + rnd() * 10).toFixed(0)}" fill="#050505" opacity="${(.55 + rnd() * .4).toFixed(2)}"/>`;
    }
    return intake(p).replace('</svg>', `<g>${soot}</g><g transform="translate(78 80)"><circle r="34" fill="#0A0A0A"/><path d="M -24 6 C -10 -14 12 18 26 -4" stroke="#1F1A12" stroke-width="10" fill="none"/></g>
<path d="M 30 150 C 18 186 46 200 36 236" stroke="#111" stroke-width="10" fill="none" stroke-linecap="round" opacity=".85"/><circle cx="36" cy="246" r="9" fill="#111" opacity=".85"/></svg>`);
  }

  function head(p = 'h') {
    let ch = '';
    for (let i = 0; i < 4; i++) {
      const cx = 100 + i * 108, cy = 128;
      ch += `<circle cx="${cx}" cy="${cy}" r="46" fill="#7E8893" stroke="#39414B" stroke-width="5"/>
<circle cx="${cx - 18}" cy="${cy - 18}" r="15" fill="#3A414A" stroke="#C9D0D7" stroke-width="4"/><circle cx="${cx + 18}" cy="${cy - 18}" r="15" fill="#3A414A" stroke="#C9D0D7" stroke-width="4"/>
<circle cx="${cx - 18}" cy="${cy + 18}" r="13" fill="#4A3324" stroke="#C9D0D7" stroke-width="4"/><circle cx="${cx + 18}" cy="${cy + 18}" r="13" fill="#4A3324" stroke="#C9D0D7" stroke-width="4"/>
<circle cx="${cx}" cy="${cy}" r="6" fill="#1F242A"/>`;
    }
    let bolts = '';
    for (let i = 0; i < 5; i++) { const x = 46 + i * 108; bolts += `<circle cx="${x}" cy="60" r="9" fill="#2C323A"/><circle cx="${x}" cy="196" r="9" fill="#2C323A"/>`; }
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" width="520" height="260">
<defs><linearGradient id="${p}Al" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F6F8"/><stop offset=".5" stop-color="#C3CAD2"/><stop offset="1" stop-color="#7C8691"/></linearGradient></defs>
<rect x="14" y="30" width="492" height="196" rx="26" fill="url(#${p}Al)" stroke="#39414B" stroke-width="6"/>
<path d="M 40 44 L 480 44" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".6"/>
${bolts}${ch}
<rect x="30" y="206" width="460" height="10" rx="5" fill="#9AA4AF" opacity=".6"/>
</svg>`;
  }

  function glowplug(p = 'gp') {
    let th = '';
    for (let y = 140; y < 228; y += 12) th += `<path d="M 44 ${y} L 96 ${y + 8}" stroke="#4F5865" stroke-width="4"/>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 470" width="140" height="470">
<defs><linearGradient id="${p}St" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E6773"/><stop offset=".38" stop-color="#EEF1F4"/><stop offset=".62" stop-color="#B5BEC8"/><stop offset="1" stop-color="#555E6A"/></linearGradient>
<linearGradient id="${p}Hot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9AA4AF"/><stop offset=".55" stop-color="#B98A5A"/><stop offset=".78" stop-color="#FF7A1A"/><stop offset=".92" stop-color="#FFC24A"/><stop offset="1" stop-color="#FFF3C4"/></linearGradient></defs>
<rect x="63" y="0" width="14" height="44" rx="5" fill="url(#${p}St)" stroke="#2C323A" stroke-width="4"/>
<rect x="48" y="30" width="44" height="22" rx="8" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5"/>
<path d="M 36 64 L 104 64 L 104 132 L 36 132 Z" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5" stroke-linejoin="round"/>
<path d="M 58 64 L 58 132 M 82 64 L 82 132" stroke="#3A414A" stroke-width="3" opacity=".6"/>
<rect x="44" y="132" width="52" height="100" rx="6" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5"/>${th}
<path d="M 50 232 L 90 232 L 82 262 L 58 262 Z" fill="url(#${p}St)" stroke="#2C323A" stroke-width="5" stroke-linejoin="round"/>
<path d="M 60 262 L 80 262 L 80 440 C 80 456 60 456 60 440 Z" fill="url(#${p}Hot)" stroke="#2C323A" stroke-width="5" stroke-linejoin="round"/>
<path d="M 66 272 L 66 420" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".45"/>
</svg>`;
  }

  return { turbo, core, dpf, pipe, gauge, intake, ecg, shield, SHIELD, injector, rocker, intakeDirty, head, glowplug };
})();
