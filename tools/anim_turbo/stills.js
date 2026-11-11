// node stills.js <outPrefix> t1,t2,... [cols] [scale]  -> JPEG frames of reel.html at those video times + a contact sheet
const { chromium } = require('playwright');
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
    const c = +cols, rows = Math.ceil(files.length / c);
    require('child_process').execFileSync('ffmpeg', ['-v', 'error', '-y', ...files.flatMap((f) => ['-i', f]), '-filter_complex',
      files.map((f, i) => `[${i}]scale=432:768[v${i}]`).join(';') + ';' + files.map((f, i) => `[v${i}]`).join('') + `xstack=inputs=${files.length}:layout=` +
      files.map((f, i) => `${(i % c) * 432}_${Math.floor(i / c) * 768}`).join('|') + ':fill=#222222', '-q:v', '3', prefix + '_sheet.jpg']);
    console.log('sheet', prefix + '_sheet.jpg');
  }
  const info = await page.evaluate(() => window.__info);
  require('fs').writeFileSync(path.resolve(__dirname, 'vo/info.json'), JSON.stringify(info, null, 1));
  if (msgs.length) console.log('MESSAGES:\n' + [...new Set(msgs)].slice(0, 25).join('\n'));
  await browser.close();
})();
