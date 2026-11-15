// latimea titlurilor boom (Anton, contur 18 px): node measure.cjs "TEXT|size" ...
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file:///home/claude/reels/p2002_ea288/compositor.html').catch(e => console.log('goto', e.message));
  await p.waitForTimeout(1500);
  const out = await p.evaluate(async (items) => {
    await document.fonts.ready; const r = [];
    for (const it of items) { const [txt, size] = it.split('|'); const d = document.createElement('div'); d.className = 'boom'; d.style.position = 'absolute'; d.style.fontSize = size + 'px'; d.innerHTML = txt; document.body.appendChild(d);
      r.push([txt.replace(/<[^>]+>/g, ''), +size, d.offsetWidth, d.offsetHeight, getComputedStyle(d).fontFamily]); d.remove(); }
    return r; }, process.argv.slice(2));
  out.forEach(o => console.log(o.join(' | '))); await b.close();
})();
