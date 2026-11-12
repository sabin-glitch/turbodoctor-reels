"""Builds reel.html (1080x1920 video version of the artifact „Injector piezo vs. magnetic”) from index_src.html + reel_tail.js + vo/cues.json.
The 3D models, the simulation and the oscilloscope come from the artifact source; the director (camera, pulses, labels, cards) is reel_tail.js."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'index_src.html'), encoding='utf-8').read()
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
def cut(a, b):
    i = js.index(a); return js[i:js.index(b, i)]
head = cut("const cv=document.getElementById('cv')", '/* ---------- Camera ---------- */')
def rep(a, b):
    global head
    assert head.count(a) == 1, ('count', head.count(a), a[:80]); head = head.replace(a, b)
rep("multi:{mag:[[0.25,0.55],[1.35,2.35],[3.05,3.35]],piezo:[[0.2,0.33],[0.55,0.68],[1.3,2.2],[2.55,2.68],[3.05,3.18]],max:4.0}",
    "multi:{mag:[[0.25,0.55],[1.35,2.35],[3.05,3.35]],piezo:[[0.15,0.28],[0.5,0.63],[0.85,0.98],[1.25,1.9],[2.15,2.28],[2.5,2.63],[2.85,2.98],[3.2,3.33],[3.5,3.63],[3.78,3.9]],max:4.2}")
rep("renderer.setClearColor(0x111417,1);", "renderer.setClearColor(0x0d1116,1);")
parts = [head, cut('const _p=new T.Vector3();', '/* ================= HUD 2D'), cut('function font(', '// etichete:'),
         cut('function fieldLines', 'function tags('), cut('function scope(', 'const CAP=['), cut('function bar(', 'function vis(')]
tail = open(os.path.join(HERE, 'reel_tail.js'), encoding='utf-8').read()
cues = json.load(open(os.path.join(HERE, 'vo/cues.json'), encoding='utf-8'))
open(os.path.join(HERE, 'vo/cues.js'), 'w', encoding='utf-8').write('window.CUES=' + json.dumps(cues, ensure_ascii=False) + ';\n')
css = ''
for fam, pre in (('Barlow', 'barlow'), ('Barlow Condensed', 'barlow-condensed')):
    for w in (500, 600, 700):
        for sub, rng in (('latin', 'U+0000-00FF,U+2000-206F,U+2190-21FF,U+2212'), ('latin-ext', 'U+0100-02AF,U+0218-021B')):
            css += '@font-face{font-family:"%s";font-weight:%d;src:url(fonts/%s-%s-%d-normal.woff2) format("woff2");unicode-range:%s}\n' % (fam, w, pre, sub, w, rng)
css += 'html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0d1116}canvas{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block}\n'
body = '\n'.join(parts) + '\n' + tail
html = '<!DOCTYPE html>\n<html lang="ro"><head><meta charset="utf-8"><title>Reel piezo</title><style>%s</style></head>\n<body><canvas id="gl" width="1080" height="1920"></canvas><canvas id="cv" width="1080" height="1920"></canvas>\n<script src="three.min.js"></script>\n<script src="vo/cues.js"></script>\n<script>\n(()=>{\n%s\n})();\n</script>\n</body></html>\n' % (css, body)
open(os.path.join(HERE, 'reel.html'), 'w', encoding='utf-8').write(html)
open(os.path.join(HERE, 'reel_check.js'), 'w', encoding='utf-8').write(body)
print('reel.html', len(html))
