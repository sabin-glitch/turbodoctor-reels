// cadre de proba ale HUD-ului la anumite momente: node hud_probe.js t1 t2 ...  -> hud_t/<frame>.png
const { chromium } = require('/opt/node-tools/node_modules/playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const ts = process.argv.slice(2).filter(x => !x.startsWith('--')).map(parseFloat); const out = path.join(__dirname, 'hud_t'); fs.mkdirSync(out, { recursive: true });
  const prev = process.argv.includes('--preview');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('PAGEERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto('file://' + path.join(__dirname, 'hud.html')); await p.waitForFunction(() => window.__ready);
  if (prev) await p.evaluate(() => document.getElementById('hud').classList.add('preview'));
  for (const t of ts) { const f = Math.round(t * 30); await p.evaluate(f => window.setFrame(f), f);
    await p.screenshot({ path: path.join(out, String(f).padStart(5, '0') + '.png'), omitBackground: !prev, clip: { x: 0, y: 0, width: 1080, height: 1920 } }); }
  await b.close();
})();
