// node render_frames.js <outDir> <firstFrame> <lastFrame> [step] [query]
// Renders reel.html frame by frame (30 fps) as JPEG q92 into <outDir>/NNNNN.jpg. Frames that already exist are skipped,
// so the job can be restarted. Each file is written under a temporary name and renamed when complete.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const [outDir, a, b, step, query] = process.argv.slice(2);
  const A = String(a).includes(',') ? 0 : +a, B = +b, S = +(step || 1), Q = query || 'scale=0.75&aa=0';
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--no-sandbox', '--allow-file-access-from-files', '--force-color-profile=srgb', '--hide-scrollbars'] });
  const page = await (await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
  const msgs = new Set();
  page.on('console', (m) => { if (m.type() !== 'log' && !/GPU stall|ReadPixels/.test(m.text())) msgs.add(m.type() + ': ' + m.text()); });
  page.on('pageerror', (e) => msgs.add('pageerror: ' + e.message));
  await page.goto('file://' + path.resolve(__dirname, 'reel.html') + '?' + Q);
  await page.waitForFunction('window.__ready === true', null, { timeout: 60000 });
  const t0 = Date.now(); let done = 0, skipped = 0;
  const LIST = String(a).includes(',') ? String(a).split(',').map(Number) : null;
  for (let n = A, i = 0; LIST ? i < LIST.length : n <= B; n += S, i++) {
    if (LIST) n = LIST[i];
    const f = path.join(outDir, String(n).padStart(5, '0') + '.jpg');
    if (fs.existsSync(f)) { skipped++; continue; }
    await page.evaluate((x) => window.__frame(x), n / 30);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    fs.writeFileSync(f + '.tmp', buf); fs.renameSync(f + '.tmp', f); done++;
    if (done % 100 === 0) { const el = (Date.now() - t0) / 1000; console.log(`frame ${n}/${B} done ${done} ${(el / done).toFixed(2)} s/frame, eta ${(((B - n) / S) * el / done / 60).toFixed(1)} min`); }
  }
  console.log(`FRAMES_DONE ${A}-${B} step ${S}: rendered ${done}, skipped ${skipped}, ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  if (msgs.size) console.log('MESSAGES:\n' + [...msgs].slice(0, 20).join('\n'));
  await browser.close();
})().catch((e) => { console.log('RENDER_FAIL ' + e.message); process.exit(1); });
