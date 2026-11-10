"""Builds reel.html (the 1080x1920 video version of the injection animation) from the published page's source + reel_tail.js."""
import re, json, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.environ.get('ANIM_SRC') or os.path.join(HERE, 'index_src.html'), encoding='utf-8').read()  # sursa paginii publicate (artifact „Injecție diesel în 3D”)
js = src[src.rindex('<script>') + 8:src.rindex('</script>')]
head = js[:js.index('/* ================= labels ================= */')]

def rep(a, b):
    global head
    assert head.count(a) == 1, ('count', head.count(a), a[:80])
    head = head.replace(a, b)

# renderer: internal 3D resolution is a fraction of the 1080x1920 frame (text overlays stay full resolution)
rep("try{renderer=new T.WebGLRenderer({canvas,antialias:true,alpha:true,powerPreference:'high-performance'});}catch(e){fail();return;}\nconst DPR=Math.min(window.devicePixelRatio||1,2);",
    "const QS=new URLSearchParams(location.search),SCALE=parseFloat(QS.get('scale')||'0.75'),AA=QS.get('aa')!=='0';\ntry{renderer=new T.WebGLRenderer({canvas,antialias:AA,alpha:true,powerPreference:'high-performance'});}catch(e){fail();return;}\nconst DPR=SCALE;")
# injection signals with modes: regen (adds the late post-injection), nopilot / harsh (pilot missing -> late, abrupt ignition)
a = head.index('function sig(u){'); b = head.index('const pistonDrop=')
head = head[:a] + '''const MODE={regen:0,nopilot:0,harsh:0},PO0=14.72,PO1=14.96;
function sig(u){
  const pil=MODE.nopilot?0:1,po=MODE.regen?1:0;
  return {
    sol:pil*pulse(u,6.75,6.78,7.25,7.28)+pulse(u,8.55,8.58,10.60,10.63)+po*pulse(u,PO0-0.03,PO0-0.02,PO1-0.03,PO1-0.02),
    ball:pil*pulse(u,6.77,6.86,7.26,7.35)+pulse(u,8.57,8.66,10.61,10.70)+po*pulse(u,PO0-0.02,PO0,PO1-0.02,PO1),
    pc:1-0.8*(pil*pulse(u,6.79,6.93,7.28,7.45)+pulse(u,8.59,8.73,10.63,10.82)+po*pulse(u,PO0-0.01,PO0+0.02,PO1-0.01,PO1+0.03)),
    needle:pil*0.7*pulse(u,6.90,7.02,7.37,7.47)+pulse(u,8.69,8.87,10.72,10.88)+po*0.65*pulse(u,PO0,PO0+0.03,PO1,PO1+0.03),
    refill:pil*pulse(u,7.26,7.31,7.45,7.53)+pulse(u,10.61,10.66,10.82,10.92)
  };
}
const burnOf=u=>MODE.harsh?1.7*pulse(u,9.52,9.6,10.3,11.8):(MODE.nopilot?0:0.28*pulse(u,7.45,7.65,8.0,8.6))+pulse(u,9.0,10.5,12.6,14.1);
''' + head[b:]
# droplets: one material factory, used for the pilot+main spray and for the post-injection spray
a = head.index('/* --- liquid droplets --- */'); b = head.index('/* --- flame --- */')
head = head[:a] + r'''/* --- liquid droplets --- */
const JETS=[0,3,4,5];
function makeDropMat(o){
  return new T.ShaderMaterial({transparent:true,depthWrite:false,blending:T.AdditiveBlending,
    uniforms:Object.assign({uWin:{value:new T.Vector4(o.win[0],o.win[1],o.win[2],o.win[3])},uSoft:{value:1.1},uL:{value:new T.Vector2(o.L[0],o.L[1])},uV:{value:new T.Vector2(o.V[0],o.V[1])},
      uLife:{value:new T.Vector2(o.life[0],o.life[1])},uSlide:{value:o.slide},uColA:{value:new T.Color(o.colA[0],o.colA[1],o.colA[2])},uColB:{value:new T.Color(o.colB[0],o.colB[1],o.colB[2])},uGainD:{value:o.gain||1},uTd:{value:0}},shared),
    vertexShader:[
     'attribute vec4 aA;attribute vec3 aO;uniform float uTd,uScale,uPix,uSlide,uGainD;uniform vec4 uWin;uniform vec2 uL,uV,uLife;uniform vec3 uColA,uColB;varying vec3 vCol;varying float vAl;',
     GL_JET,
     'void main(){',
     ' float pilot=step(aA.w,0.10);float mist=aO.z;',
     ' float tb=mix(uWin.z+aA.y*uWin.w,uWin.x+aA.y*uWin.y,pilot);',
     ' float a=uTd-tb;float life=mix(uLife.x,uLife.y,pilot)*(0.75+0.7*fract(aA.w*7.31))*(1.0+1.1*mist);',
     ' float L=mix(uL.x,uL.y,pilot);float v0=mix(uV.x,uV.y,pilot)*aA.z*(1.0-0.2*mist);',
     ' float s=L*(1.0-exp(-v0*max(a,0.0)/L));float k=s/L;',
     ' vec3 o,d,e1,e2;jet(aA.x,o,d,e1,e2);',
     ' float spread=0.12+(0.13+0.09*mist)*s+2.3*smoothstep(0.72,1.0,k)*(0.4+aA.z);',
     ' vec3 p=o+d*s+(e1*aO.x+e2*aO.y)*spread;',
     ' p+=(e1*sin(a*11.0+aA.w*40.0)+e2*cos(a*9.0+aA.w*23.0))*0.04*s;',
     ' p.y-=uSlide*smoothstep(0.78,1.0,k)*fract(aA.w*3.7);',
     ' float vis=step(0.0,a)*step(a,life);',
     ' vec4 mv=modelViewMatrix*vec4(p,1.0);gl_Position=projectionMatrix*mv;',
     ' if(vis<0.5)gl_Position=vec4(2.0,2.0,2.0,1.0);',
     ' float size=mix(mix(0.62,0.26,smoothstep(0.0,0.5,k)),1.5+2.2*k,mist)*(1.0+0.7*smoothstep(0.6,1.0,a/life));',
     ' gl_PointSize=max(size*uScale/-mv.z,1.3*uPix);',
     ' vAl=smoothstep(0.0,0.03,a)*(1.0-smoothstep(0.45,1.0,a/life))*mix(0.72,0.055,mist)*uGainD*(1.0-smoothstep(2.5,4.5,p.z));',
     ' vCol=mix(uColA,uColB,smoothstep(0.1,0.85,k));',
     '}'].join('\n'),
    fragmentShader:SOFT_FS});
}
const dropMat=makeDropMat({win:[WIN.pilotDrop[0],WIN.pilotDrop[1],WIN.mainDrop[0],WIN.mainDrop[1]],L:[21,11.5],V:[84,58],life:[0.36,0.3],slide:3.2,colA:[1,0.72,0.2],colB:[1,0.86,0.5]});
let DROPGEO,GASGEO;
(function(){
  const n=9000,A=new Float32Array(n*4),O=new Float32Array(n*3);
  for(let i=0;i<n;i++){const d=disc(),rr=Math.hypot(d[0],d[1]),j=rnd();
    A[i*4]=JETS[j<0.3?0:(j<0.6?1:(j<0.8?2:3))];A[i*4+1]=rnd();A[i*4+2]=1.2-0.6*rr+0.1*rnd();A[i*4+3]=rnd();O[i*3]=d[0];O[i*3+1]=d[1];O[i*3+2]=rnd()<0.26?1:0;}
  DROPGEO=points(n,{aA:{a:A,n:4},aO:{a:O,n:3}},dropMat).geometry;
})();
''' + head[b:]
rep(" float size=mix((1.7+4.4*k)*(1.0+1.5*big),0.9+1.6*k,pilot);"," float size=mix((1.7+4.4*k)*(1.0+1.5*big),1.3+2.8*k,pilot);")
rep("*uGain*(1.0-0.55*big)*(1.0-smoothstep(-1.0,1.0,p.z));","*uGain*(1.0-0.55*big)*mix(1.0,2.6,pilot)*(1.0-smoothstep(-1.0,1.0,p.z));")
rep("const a=points(n,{aHome:{a:H,n:3},aR:{a:Rr,n:4}},airMat);", "const a=points(n,{aHome:{a:H,n:3},aR:{a:Rr,n:4}},airMat);GASGEO=a.geometry;")
tail = open('reel_tail.js', encoding='utf-8').read()
cues = json.load(open('vo/cues.json', encoding='utf-8'))
open('vo/cues.js', 'w', encoding='utf-8').write('window.CUES=' + json.dumps(cues, ensure_ascii=False) + ';\n')
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
#stripBox{position:absolute;left:44px;top:300px;width:992px;height:206px;border-radius:14px;background:rgba(8,12,17,.62);border:2px solid rgba(232,237,243,.13)}
#strip{position:absolute;left:26px;top:8px;width:940px;height:190px}
#stripBox{opacity:0}
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
#temp{position:absolute;left:44px;top:300px;width:992px;height:206px;border-radius:14px;background:rgba(8,12,17,.72);border:2px solid rgba(232,237,243,.13);opacity:0}
#temp .tl{position:absolute;left:30px;top:30px;font:700 27px/1 JB;letter-spacing:.08em;color:#b6c2cf}
#temp .th{position:absolute;left:30px;top:84px;font:800 30px/1 Mont;letter-spacing:.03em;color:#ffd21f;text-transform:uppercase}
#temp .tv{position:absolute;right:34px;top:14px;font:400 122px/1 Anton;color:#fff;letter-spacing:2px}
#temp.hot .tv{color:#ff7a2e;text-shadow:0 0 34px rgba(255,106,43,.75)}
#temp .tb{position:absolute;left:30px;right:34px;bottom:28px;height:20px;border-radius:10px;background:rgba(232,237,243,.16)}
#temp .tb i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:10px;background:linear-gradient(90deg,#ffb224,#ff5a1f)}
#temp .tb b{position:absolute;left:80%;top:-9px;bottom:-9px;width:0;border-left:4px solid #fff}
#dip{position:absolute;left:0;top:0;width:1080px;height:1920px;background:#06090d;opacity:0}
'''
html = '''<!DOCTYPE html>
<html lang="ro"><head><meta charset="utf-8"><title>Reel injecție</title><style>%s</style></head>
<body>
<div id="stage"><canvas id="gl"></canvas><svg id="leaders"></svg><div id="labels"></div></div>
<div id="stripBox"><div id="strip"><span class="ttl">MOMENTUL INJECȚIEI</span></div></div>
<div id="temp"><div class="tl">TEMPERATURĂ ÎN FILTRU</div><div class="th">Peste 600 °C arde funinginea</div><div class="tv" id="tempV">250 °C</div><div class="tb"><i id="tempBar"></i><b></b></div></div>
<div id="clog">FILTRU ÎNFUNDAT</div>
<div id="dip"></div>
<script src="three.min.js"></script>
<script src="vo/cues.js"></script>
<script>
%s
%s
</script>
</body></html>
''' % (css, head, tail)
open('reel.html', 'w', encoding='utf-8').write(html)
jsall = head + tail
open('reel_check.js', 'w', encoding='utf-8').write(jsall)
print('reel.html', len(html))
