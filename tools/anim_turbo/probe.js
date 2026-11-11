// node probe.js -> vo/probe.json : animation state sampled at 200 Hz (wobble, sparks, time since the shaft broke, heat, compressor spin factor)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--no-sandbox', '--allow-file-access-from-files'] });
  const page = await (await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
  await page.goto('file://' + path.resolve(__dirname, 'reel.html') + '?scale=0.2&aa=0');
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
  const d = await page.evaluate(() => { const o = [], N = Math.ceil(window.__end * 200); for (let i = 0; i <= N; i++) o.push(window.__probe(i / 200).map((v) => +v.toFixed(4))); return o; });
  fs.writeFileSync(path.resolve(__dirname, 'vo/probe.json'), JSON.stringify({ hz: 200, cols: ['wobble', 'sparks', 'snapAge', 'heat', 'spin'], data: d }));
  console.log('probe samples', d.length);
  await browser.close();
})();
