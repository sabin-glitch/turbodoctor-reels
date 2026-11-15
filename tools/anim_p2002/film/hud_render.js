// Randarea textelor de pe ecran (HUD) ca imagini PNG transparente: node hud_render.js [f0 f1] [--every n] [--part i n] [--out dir]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const a = process.argv.slice(2); const get = (k, d) => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; };
  const out = get('--out', path.join(__dirname, 'hud')); fs.mkdirSync(out, { recursive: true });
  const every = parseInt(get('--every', '1')); const part = get('--part', null);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('PAGEERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto('file://' + path.join(__dirname, 'hud.html')); await p.waitForFunction(() => window.__ready);
  const info = await p.evaluate(() => ({ n: Math.round(window.TL.total * window.TL.fps), fonts: [...document.fonts].filter(f => f.status === 'loaded').length }));
  let f0 = 0, f1 = info.n; const pos = a.filter((x, i) => /^\d+$/.test(x) && !(i > 0 && a[i - 1].startsWith('--')));
  if (pos.length >= 2) { f0 = parseInt(pos[0]); f1 = parseInt(pos[1]); }
  let list = []; for (let f = f0; f < f1; f += every) list.push(f);
  if (part) { const [pi, pn] = [parseInt(part), parseInt(a[a.indexOf('--part') + 2])]; list = list.filter((_, i) => i % pn === pi); }
  console.log('cadre', list.length, 'fonturi incarcate', info.fonts);
  const t0 = Date.now();
  for (let i = 0; i < list.length; i++) {
    const f = list[i];
    await p.evaluate(f => window.setFrame(f), f);
    await p.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.png'), omitBackground: true, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    if (i % 200 === 199) console.log(i + 1, '/', list.length, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  await b.close(); console.log('gata', ((Date.now() - t0) / 1000).toFixed(0) + 's');
})();
