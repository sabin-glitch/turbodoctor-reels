// node stills.js <outPrefix> t1,t2,... [cols] [scale]  -> JPEG frames of reel.html at those video times + a contact sheet
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const sharp = require('/opt/npm-tools/node_modules/sharp');
const path = require('path');
(async () => {
  const [prefix, times, cols, scale] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--no-sandbox', '--allow-file-access-from-files', '--force-color-profile=srgb', '--hide-scrollbars'] });
  const page = await (await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
  const msgs = [];
  page.on('console', (m) => { if (m.type() !== 'log' && !/GPU stall|ReadPixels/.test(m.text())) msgs.push(m.type() + ': ' + m.text()); });
  page.on('pageerror', (e) => msgs.push('pageerror: ' + e.message));
  await page.goto('file://' + path.resolve(__dirname, 'reel.html') + '?scale=' + (scale || '0.75'));
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 }).catch(() => console.log('NOT READY'));
  const files = [];
  for (const t of times.split(',')) {
    const s = Date.now();
    await page.evaluate((x) => window.__frame(x), +t);
    const f = `${prefix}_${String(t).replace('.', '_')}.jpg`;
    await page.screenshot({ path: f, type: 'jpeg', quality: 90 });
    files.push(f); process.stdout.write(`${t}:${Date.now() - s}ms `);
  }
  console.log();
  if (cols) {
    const c = +cols, tw = 432, th = 768, rows = Math.ceil(files.length / c);
    const tiles = await Promise.all(files.map((f) => sharp(f).resize(tw, th).toBuffer()));
    await sharp({ create: { width: tw * c, height: th * rows, channels: 3, background: '#222' } })
      .composite(tiles.map((b, i) => ({ input: b, left: (i % c) * tw, top: Math.floor(i / c) * th }))).jpeg({ quality: 88 }).toFile(prefix + '_sheet.jpg');
    console.log('sheet', prefix + '_sheet.jpg');
  }
  const info = await page.evaluate(() => window.__info);
  require('fs').writeFileSync(path.resolve(__dirname, 'vo/info.json'), JSON.stringify(info, null, 1));
  if (msgs.length) console.log('MESSAGES:\n' + [...new Set(msgs)].slice(0, 25).join('\n'));
  await browser.close();
})();
