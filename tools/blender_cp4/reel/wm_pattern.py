# Modelul marcajului "TURBO DOCTOR" din fundal, identic cu cel din seria turbinelor (tools/anim_serie_turbine: #wm in build_reel.py, placeWM in dir_post.js):
# randuri Anton 58 px, spatiere 5 px, la 176 px unul de altul, randurile impare decalate cu o jumatate de pas. Scrie wm/pattern.png (alfa plin) si wm/pattern.json (pasul).
import json, os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.environ.get('ANTON', '/home/claude/reels/amorsare_filtru/assets/fonts/Anton_400Regular.ttf')
CHROME = '/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None
html = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Anton;src:url(file://%s)}
html,body{margin:0;background:transparent}
#wm{position:absolute;left:0;top:0;height:2920px;overflow:hidden}
#wm .r{position:absolute;left:0;white-space:nowrap;font:400 58px/1 Anton;letter-spacing:5px;color:rgb(232,237,243)}
#wm .r b{font-weight:400;color:rgb(255,210,31)}
#wm .r span{display:inline-block;padding-right:150px}
</style></head><body><div id="wm"></div></body></html>""" % FONT
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME, args=['--allow-file-access-from-files', '--force-color-profile=srgb', '--font-render-hinting=none'])
    pg = b.new_page(viewport={'width': 800, 'height': 600}, device_scale_factor=1)
    open(os.path.join(HERE, 'wm/pattern.html'), 'w').write(html); pg.goto('file://' + os.path.join(HERE, 'wm/pattern.html'))
    pg.evaluate("document.fonts.load('58px Anton')"); pg.wait_for_function("document.fonts.check('58px Anton')")
    unit = pg.evaluate("""() => { const wm = document.getElementById('wm');
        for (let i = 0; i < 17; i++) { const r = document.createElement('div'); r.className = 'r'; r.style.top = (i * 176) + 'px';
            let h = ''; for (let k = 0; k < 14; k++) h += '<span>TURBO <b>DOCTOR</b></span>'; r.innerHTML = h; wm.appendChild(r); }
        const u = wm.firstChild.firstChild.getBoundingClientRect().width;
        [...wm.children].forEach((r, i) => { r.style.transform = 'translateX(' + (i % 2 ? -u / 2 : 0) + 'px)'; });
        wm.style.width = Math.ceil(2480 + 2 * u) + 'px'; return u; }""")
    Wd = int(-(-(2480 + 2 * unit) // 1))
    pg.set_viewport_size({'width': Wd, 'height': 2920})
    pg.screenshot(path=os.path.join(HERE, 'wm/pattern.png'), omit_background=True, clip={'x': 0, 'y': 0, 'width': Wd, 'height': 2920})
    b.close()
json.dump({'unit': unit, 'w': Wd, 'h': 2920}, open(os.path.join(HERE, 'wm/pattern.json'), 'w'))
print('pas', unit, 'latime', Wd)
