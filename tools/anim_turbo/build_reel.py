"""Builds reel.html (1080x1920 video version of the turbocharger animation) from index_src.html (artifact „Turbosuflanta pe motor”) + reel_tail.js."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'index_src.html'), encoding='utf-8').read()
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
head = js[:js.index('/* ================= labels ================= */')]
def rep(a, b):
    global head
    assert head.count(a) == 1, ('count', head.count(a), a[:80])
    head = head.replace(a, b)
rep("try{renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'high-performance'});}catch(e){fail();return;}\nconst DPR=Math.min(window.devicePixelRatio||1,2);",
    "const QS=new URLSearchParams(location.search),SCALE=parseFloat(QS.get('scale')||'0.75'),AA=QS.get('aa')!=='0';\ntry{renderer=new T.WebGLRenderer({canvas,antialias:AA,alpha:true,powerPreference:'high-performance'});}catch(e){fail();return;}\nconst DPR=SCALE;")
cues = json.load(open(os.path.join(HERE, 'vo/cues.json'), encoding='utf-8'))
rep("const TU=46;", "const TU=Math.ceil(16+%.2f+4);" % cues['end'])
tail = open(os.path.join(HERE, 'reel_tail.js'), encoding='utf-8').read()
open(os.path.join(HERE, 'vo/cues.js'), 'w', encoding='utf-8').write('window.CUES=' + json.dumps(cues, ensure_ascii=False) + ';\n')
F = 'fonts/'
css = '''
@font-face{font-family:Mont;src:url(%sMontserrat_600SemiBold.ttf);font-weight:600}
@font-face{font-family:Mont;src:url(%sMontserrat_700Bold.ttf);font-weight:700}
@font-face{font-family:Mont;src:url(%sMontserrat_800ExtraBold.ttf);font-weight:800}
@font-face{font-family:Mont;src:url(%sMontserrat_900Black.ttf);font-weight:900}
@font-face{font-family:Anton;src:url(%sAnton_400Regular.ttf)}
@font-face{font-family:JB;font-weight:700;src:url(%sjetbrains-mono-latin-700-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:JB;font-weight:700;src:url(%sjetbrains-mono-latin-ext-700-normal.woff2) format('woff2');unicode-range:U+0100-02AF}
@font-face{font-family:JB;font-weight:800;src:url(%sjetbrains-mono-latin-800-normal.woff2) format('woff2');unicode-range:U+0000-00FF,U+2000-206F}
@font-face{font-family:JB;font-weight:800;src:url(%sjetbrains-mono-latin-ext-800-normal.woff2) format('woff2');unicode-range:U+0100-02AF}
''' % ((F,) * 9) + '''
*{box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0b1016;color:#e8edf3;font-family:Mont,sans-serif}
#stage{position:absolute;left:0;top:0;width:1080px;height:1920px;background:
  linear-gradient(rgba(232,237,243,.034) 2px,transparent 2px) 0 0/108px 108px,
  linear-gradient(90deg,rgba(232,237,243,.034) 2px,transparent 2px) 0 0/108px 108px,
  radial-gradient(110% 70% at 50% 44%,#1c2733 0%,#0e141b 56%,#06090d 100%)}
#gl{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block}
#leaders{position:absolute;left:0;top:0;width:1080px;height:1920px}
#leaders line{stroke:rgba(232,237,243,.8);stroke-width:2.5}
#leaders circle{fill:#fff}
#labels{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}
.lb{position:absolute;top:0;left:0;font:800 34px/1.1 Mont;letter-spacing:.02em;text-transform:uppercase;white-space:nowrap;color:#fff;padding:11px 18px 12px;background:rgba(8,12,17,.84);border-left:6px solid #FFD21F;border-radius:3px;opacity:0}
.lb.l{border-left:0;border-right:6px solid #FFD21F}
.lb small{display:block;font:700 24px/1.15 Mont;letter-spacing:.04em;color:#b6c2cf;margin-top:6px}
.lb.num{font:800 50px/1 JB;color:#FFD21F;letter-spacing:0;padding:10px 16px}
#xx{position:absolute;left:44px;top:300px;width:992px;height:206px;border-radius:14px;background:rgba(8,12,17,.62);border:2px solid rgba(232,237,243,.13)}
#strip{position:absolute;left:26px;top:8px;width:940px;height:190px}
#xx{opacity:0}
#strip::before{content:"";position:absolute;left:0;right:0;bottom:48px;height:3px;background:rgba(232,237,243,.4)}
.ttl{position:absolute;left:0;top:6px;font:700 22px/1 JB;letter-spacing:.1em;color:#9aa7b5}
.ev{position:absolute;bottom:51px;max-height:84px;background:rgba(255,178,36,.5);border:3px solid #ffb224;border-bottom:0;border-radius:5px 5px 0 0}
.ev.on{background:#ffd21f;border-color:#fff3b0;box-shadow:0 0 34px rgba(255,210,31,.95)}
.ev.ghost{background:transparent;border-style:dashed;opacity:.55}
.ev.miss{background:transparent;border-color:#ff4b4b;border-style:dashed}
.evl{position:absolute;bottom:8px;transform:translateX(-50%);font:800 30px/1 Mont;letter-spacing:.05em;color:#9fb0c0;white-space:nowrap}
.evl.pre{transform:translateX(-100%)}
.evl.main{transform:none}
.evl.on{color:#ffd21f}
.evl.miss{color:#ff4b4b;text-decoration:line-through}
.tick{position:absolute;top:36px;bottom:48px;width:0;border-left:2px dashed rgba(232,237,243,.38)}
.tick::after{content:attr(data-l);position:absolute;top:0;left:8px;font:700 24px/1 JB;font-style:normal;color:#cbd5e1}
.head{position:absolute;left:0;top:40px;bottom:40px;width:5px;margin-left:-2.5px;background:#fff;box-shadow:0 0 14px #fff;border-radius:3px;opacity:0}
#clog{display:none}
#yy{position:absolute;left:44px;top:300px;width:992px;height:206px;border-radius:14px;background:rgba(8,12,17,.72);border:2px solid rgba(232,237,243,.13);opacity:0}
#yy .tl{position:absolute;left:30px;top:30px;font:700 27px/1 JB;letter-spacing:.08em;color:#b6c2cf}
#yy .th{position:absolute;left:30px;top:84px;font:800 30px/1 Mont;letter-spacing:.03em;color:#ffd21f;text-transform:uppercase}
#yy .tv{position:absolute;right:34px;top:14px;font:400 122px/1 Anton;color:#fff;letter-spacing:2px}
#yy.hot .tv{color:#ff7a2e;text-shadow:0 0 34px rgba(255,106,43,.75)}
#yy .tb{position:absolute;left:30px;right:34px;bottom:28px;height:20px;border-radius:10px;background:rgba(232,237,243,.16)}
#yy .tb i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:10px;background:linear-gradient(90deg,#ffb224,#ff5a1f)}
#yy .tb b{position:absolute;left:80%;top:-9px;bottom:-9px;width:0;border-left:4px solid #fff}
#dip{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#06090d;opacity:0}
'''

css += """
.lb.oil{border-color:#f0b43a}.lb.air{border-color:#7ccaf5}.lb.fire{border-color:#ff6a2b}.lb.bad{border-color:#ff4b4b;color:#ffd2d2}.lb.good{border-color:#3ddc84}
.lb.bad.l,.lb.oil.l,.lb.air.l,.lb.fire.l,.lb.good.l{border-left:0}
#flash{position:absolute;left:0;top:0;width:1080px;height:1920px;background:radial-gradient(60% 40% at 50% 52%,#fff6d8 0%,#ffb35a 40%,rgba(255,90,20,0) 100%);opacity:0;mix-blend-mode:screen}
"""
html = """<!DOCTYPE html>
<html lang="ro"><head><meta charset="utf-8"><title>Reel turbo</title><style>%s</style></head>
<body>
<div id="stage"><canvas id="gl"></canvas><svg id="leaders"></svg><div id="labels"></div></div>
<div id="flash"></div>
<div id="dip"></div>
<script src="three.min.js"></script>
<script src="vo/cues.js"></script>
<script>
(function(){
'use strict';
const T=window.THREE;
const $=id=>document.getElementById(id);
const fail=()=>{document.body.style.background='red';};
%s
%s
})();
</script>
</body></html>
""" % (css, head.split("const fail=()=>document.body.classList.add('fail');\nif(!T){fail();return;}",1)[1], tail)
open(os.path.join(HERE, 'reel.html'), 'w', encoding='utf-8').write(html)
open(os.path.join(HERE, 'reel_check.js'), 'w', encoding='utf-8').write(head + tail)
print('reel.html', len(html))
