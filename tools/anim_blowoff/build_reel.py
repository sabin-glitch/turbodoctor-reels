# Builds blow-off-reel.html: the blow-off animation re-directed on the voice-over of the reel
# „Dacă ai diesel și auzi sunetul ăsta” (15.11.2026, v2). Same scene as the film (base/: turbo.html + b_parts/b_vgt/b_streams,
# unchanged copies of /mnt/project-files/animatii/sursa/blow-off/), plus the parts of the reel (r_parts.js: MAF sensor and
# factory recirculation valve; r_s1.js / r_streams.js: the recirculation loop). Timeline, camera, labels and HUD (r_*.js) run
# in voice time: every event is anchored on a word of vo/cues.json (written by make_vo.py).
#   python3 build_reel.py            -> blow-off-reel.html + vo/anchors.json
import os, json, re, unicodedata
D = os.path.dirname(os.path.abspath(__file__))
def rd(f): return open(os.path.join(D, f), encoding='utf8').read()
VO = 'vo' if os.path.exists(os.path.join(D, 'vo/cues.json')) else 'map'   # map/ = the committed copy of the timings this reel was rendered with (vo/ is not in git)
C = json.load(open(os.path.join(D, VO, 'cues.json'), encoding='utf8'))
def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); return ''.join(c for c in s if unicodedata.category(c) != 'Mn' and c.isalnum())
def W(i, word, occ=0):
    n = norm(word); k = 0
    for w in C['words']:
        if w['win'] == i and norm(w['text']) == n:
            if k == occ: return w['s']
            k += 1
    raise KeyError((i, word, occ))
S = lambda i: C['lines'][i]['start']
E = lambda i: C['lines'][i]['end']
SEND = C['end']; TU = round(SEND + 7.5 + 0.04, 2)
# hook sound: envelope of audio/hook_bed.wav (vo/hook_sfx.json, written by make_hook_sfx.py); the red bursts of the hook follow it
hp = os.path.join(D, VO, 'hook_sfx.json')
HFL = None
if os.path.exists(hp):
    h = json.load(open(hp)); HE = dict(t0=h['t0'], tb=h['tb'], v=h['env']); HFL = h.get('flutter')
else:
    HE = dict(t0=round(E(0) + .15, 3), tb=round(E(0) + .2, 3), v=[round(min(1, k / 3) * 2.718 ** (-max(0, k - 3) / 28), 3) for k in range(80)])
T_S = (E(11) + S(12)) / 2; T_W = (E(12) + S(13)) / 2; SP_C2 = W(12, 'supapă') - .25
K = dict(HZ=1.2, SEND=SEND, HE=HE, HFL=HFL,
    H_LIFT=HE['tb'] - .1, H_SLOW=S(1) - .15, H_DMG=W(1, 'semnul') - .15, H_SPK=W(1, 'distruge') - .15,
    # petrol, as it leaves the factory: recirculation (diverter) valve and MAF (rows 2-4)
    T_P=(E(1) + S(2)) / 2 + .02, P_IN=S(3) - .1, P_DV=W(3, 'supapă') - .15, P_LIFT=W(3, 'Când') - .1, P_C=W(3, 'clapeta') - .1,
    P_TRAP=W(3, 'aerul') - .1, P_L=W(3, 'Supapa', 1) - .1, P_BACK=W(3, 'înapoi') - .2, P_MAF=S(4) - .1, P_MAF1=W(4, 'aerul') - .1,
    P_CAP=W(4, 'captiv') - .1, P_OK=W(4, 'iar') - .1,
    # tuned petrol: blow-off (row 5)
    T_B=(E(4) + S(5)) / 2, B_TUN=W(5, 'mașinile') - .2, B_PROT=W(5, 'protejeze') - .2, B_ACC=W(5, 'accelerează') - .3, P2_C=W(5, 'adună') - .15,
    P2_NEED=W(5, 'motorul') - .1, P2_L=W(5, 'eliberat') - .25, B_SND=W(5, 'De', 1) - .1,
    # diesel (rows 6-11)
    T_D=(E(5) + S(6)) / 2, D_LIFT=W(6, 'Clapeta') - .3, D_AIR=W(6, 'aerul') - .1, D_NOBOV=W(6, 'De') - .2, D_NODV=W(6, 'nici') - .2, D_NOBO=W(6, 'nici', 1) - .2,
    D_ACC=S(7) - .1, D_TURBO=W(7, 'Din') - .1, O_R0=W(7, 'Când') - .1, O_R1=W(7, 'pe') + .3, O_P0=W(7, 'pe') - .1, O_P1=W(7, 'decât') + .3,
    O_AIR=W(7, 'mai') - .1, O_PRES=W(7, 'presiune') - .1,
    L_LIFT=W(8, 'ridici'), L_ENG=W(8, 'Motorul') - .1, L_COMP=W(8, 'compresorul') - .1, S_ON=W(9, 'întoarce') - .15,
    X_STR=W(10, 'tensiune') - .1, X_AX=W(10, 'împinge'), X_BRG0=W(10, 'lagărul'), X_BRG=W(11, 'Lagărul'), X_JOC=W(11, 'axul'), X_PAL=W(11, 'iar'), X_SPK=W(11, 'atingă'),
    # split screen (row 12)
    T_S=T_S, SP_C1=T_S + .75, SP_R1=SP_C2 - 1.45, SP_C2=SP_C2, SP_A0=W(12, 'Pe') - .2, SP_B0=W(12, 'Pe', 1) - .2,
    # closing: the causes (row 13), then lift-off and surge once more (row 14)
    T_W=T_W, W_Q=S(13) + .3, W_DG=W(13, 'geometria') - .5, W_ACT=W(13, 'problemă') - .15, W_OTH=W(13, 'sau') - .2, W_PRES=W(13, 'presiunea') - .2,
    W_LIFT=W(14, 'suflă') - .25, W_FIND=W(14, 'Găsește') - .2)
K = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in K.items()}
json.dump(dict(TU=TU, K=K), open(os.path.join(D, VO, 'anchors.json'), 'w'), indent=1)

L = rd('base/turbo.html').split('\n')
src = '\n'.join(L[1:1089])
def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, (old[:90], n)
    src = src.replace(old, new)
def between(a, b, new):
    global src
    i = src.index(a); j = src.index(b, i)
    src = src[:i] + new + src[j:]
for t in ['<!DOCTYPE html>\n', '<html lang="ro">\n', '<head>\n', '</head>\n', '<body>\n', '</body>\n', '</html>']:
    rep(t, '')
rep('<title>Turbosuflanta pe motor</title>', '<title>Blow-off pe diesel (reel)</title>')
rep('  --steel:#c3ccd6;\n', '  --steel:#c3ccd6;\n  --warn:#ff5a45;\n  --clean:#5fe0cf;\n  --vac:#5aa8ff;\n')
rep('</style>', '''.lb.warn{border-color:var(--warn);color:#ffe3dd}.lb.big{font-size:15.5px;padding:5px 9px;letter-spacing:.08em}.lb.big small{font-size:11px}
.hud dd.warn{color:var(--warn)}.hud dd.vac{color:var(--vac)}
#slowp{justify-self:end;font:600 10px/1 var(--display);letter-spacing:.1em;text-transform:uppercase;color:var(--ink);border:1px solid rgba(232,237,243,.45);padding:4px 6px;border-radius:2px;opacity:0;margin-top:1px;background:rgba(8,12,17,.6)}
#split{position:fixed;inset:0;pointer-events:none;display:none}
#split.on{display:block}
#split .sp{position:absolute;right:12px;display:flex;flex-direction:column;align-items:flex-end;text-align:right;gap:4px;background:rgba(8,12,17,.82);padding:9px 11px 10px;border-radius:3px;max-width:64%}
#split .sp b{font:700 17px/1 var(--display);letter-spacing:.07em;text-transform:uppercase}
#split .sp em{font:700 12px/1 var(--display);font-style:normal;letter-spacing:.12em;text-transform:uppercase;padding:4px 7px;border-radius:2px;margin-top:3px}
#split .ok b{color:var(--clean)}#split .ok em{background:var(--clean);color:#04201c}
#split .bad b{color:var(--warn)}#split .bad em{background:var(--warn);color:#2a0702}
#split .div{position:absolute;left:0;right:0;height:2px;background:rgba(232,237,243,.35)}
#split .dim{position:absolute;left:0;right:0;background:#06090d;opacity:0}
#split .cue{position:absolute;left:12px;font:700 13px/1 var(--display);letter-spacing:.1em;text-transform:uppercase;padding:6px 9px;border-radius:2px;background:#0b1016;color:var(--ink);border:1px solid rgba(232,237,243,.4);transform:translateY(-50%)}
#split .cue.lift{color:#1a0f02;background:var(--accent);border-color:var(--accent)}
/* vo mode (the reel): no title, caption or rail; read-outs top right; the scene sits between 13% and 66% of the height */
body.vo #title,body.vo #bottom{display:none!important}
body.vo #top{background:none;padding-top:20px;justify-content:flex-end}
body.vo .lb{font-size:14px;padding:4px 7px}body.vo .lb small{font-size:11.5px}body.vo .lb.big{font-size:18px}body.vo .lb.big small{font-size:12.5px}
body.vo .hud{background:rgba(8,12,17,.66);padding:9px 11px 9px 14px;border-radius:3px}
</style>''')
rep('aria-label="Animație 3D: gazele de evacuare din cilindru învârt turbina, axul pe lagăre unse cu ulei antrenează roata compresorului"',
    'aria-label="Animație 3D: de ce un diesel care suflă ca un blow-off are turbina în pompaj"')
rep('<h1>Cum funcționează <span>turbosuflanta</span></h1>', '<h1>Sunet de <span>blow-off</span> pe diesel</h1>')
rep('    <div id="h2" hidden><dt id="l2"></dt><dd id="v2"></dd></div>\n', '    <div id="h2" hidden><dt id="l2"></dt><dd id="v2"></dd></div>\n    <div id="slowp">Încetinitor</div>\n')
rep('<div id="fade" aria-hidden="true"></div>', '''<div id="split" aria-hidden="true">
  <div class="sp ok" id="spA"><b>Benzină · blow-off</b><em>Normal</em></div>
  <i class="div" id="spD"></i>
  <div class="sp bad" id="spB"><b>Diesel · pompaj</b><em>Defect</em></div>
  <i class="dim" id="spX"></i><i class="dim" id="spY"></i>
  <div class="cue" id="spC">Accelerezi</div>
</div>
<div id="fade" aria-hidden="true"></div>''')
rep('max="46"', 'max="%s"' % TU)
rep('const TU=46;', 'const TU=%s;' % TU)
between('/* ================= timeline ================= */', '/* ================= renderer ================= */', rd('r_timeline.js').replace('/*K*/{}/*K*/', json.dumps(K)) + '\n')
rep("  eng.add(revolvedMesh([[0,-2.2,1],[2.4,-1.2,1],[3.6,2.6],[3.6,20.5],[10.5,20.5],[10.5,64],[8,66],[8,96],[0,96]],M.injBody,C.inj,{seg:30}));",
    "  injMesh=revolvedMesh([[0,-2.2,1],[2.4,-1.2,1],[3.6,2.6],[3.6,20.5],[10.5,20.5],[10.5,64],[8,66],[8,96],[0,96]],M.injBody,C.inj,{seg:30});eng.add(injMesh);")
rep('/* cylinder head with ports */', 'let injMesh;\n/* cylinder head with ports */')
rep("const piston=new T.Group();eng.add(piston);", "const piston=new T.Group();eng.add(piston);\nconst pCrownD=new T.Group(),pCrownP=new T.Group();piston.add(pCrownD);piston.add(pCrownP);   /* diesel bowl / petrol dish */")
rep("""  piston.add(new T.Mesh(latheGeo(prof.slice(0,13),{closed:false,seg:56}),M.crown));
  piston.add(new T.Mesh(latheGeo(prof.slice(12),{closed:false,seg:56}),M.piston));
  {const cg=capGeo(prof);piston.add(new T.Mesh(cg,C.piston));edges(piston,cg);}""",
"""  const profP=[[0,-3.2,1],[14,-3.2,1],[21,-2.7,1],[26.5,-1.1,1],[29.5,0],[39.6,0],[40.6,-1],[40.6,-56],[37.4,-56],[37.4,-31],[33,-23.5,1],[26,-21.5,1],[0,-21.5]];
  pCrownD.add(new T.Mesh(latheGeo(prof.slice(0,13),{closed:false,seg:56}),M.crown));
  pCrownP.add(new T.Mesh(latheGeo(profP.slice(0,7),{closed:false,seg:56}),std(0x4d5157,.55,.58)));
  piston.add(new T.Mesh(latheGeo(prof.slice(12),{closed:false,seg:56}),M.piston));
  {const cg=capGeo(prof);pCrownD.add(new T.Mesh(cg,C.piston));edges(pCrownD,cg);}
  {const cg=capGeo(profP);pCrownP.add(new T.Mesh(cg,C.piston));edges(pCrownP,cg);}""")
rep("const NEX=5200,exP=[];\nconst EX_SPAN=lut(LUT.gex,TU)+700;", "const NEX=9600,exP=[];\nconst EX_SPAN=Math.max(lut(LV.main.gex,TU),lut(LV.top.gex,TU),lut(LV.bot.gex,TU))+700;")
rep("function drawExhaust(U){\n  const G=lut(LUT.gex,U);exPts.begin();",
    "const GAS_COOL=new T.Color(0.60,0.68,0.76);\nexP.forEach(p=>{p.cool={};for(const v in LV)p.cool[v]=LV[v].cool.some(q=>p.e>=q[0]&&p.e<q[1]);});\nfunction drawExhaust(G,variant){\n  exPts.begin();")
rep("    exPts.push(_v,_c,a,(prog<0.3?3.2:2.6)*p.sz);", "    if(p.cool[variant]){_c.copy(GAS_COOL);a*=0.5;}\n    exPts.push(_v,_c,a,(prog<0.3?3.2:2.6)*p.sz);")
rep('  cooler:stdC(0x7c858e,.85,.4), filter:std(0x272b30,.1,.8), dark:flat(0x0d1117)\n};', '  cooler:stdC(0x7c858e,.85,.4), filter:std(0x272b30,.1,.8), dark:flat(0x0d1117)\n};\nM.bronzeT=std(0xc08a4a,.95,.32);')
rep('axPart(turbo,[[-54.6,6.6],[-49.2,6.6],[-49.2,24.6],[-54.6,24.6]],M.bronze,C.bronze,{seg:40});', 'C.bronzeT=cut(0xc9945a,HB);axPart(turbo,[[-54.6,6.6],[-49.2,6.6],[-49.2,24.6],[-54.6,24.6]],M.bronzeT,C.bronzeT,{seg:40});')
# shorter intercooler, higher up, to leave room for the blow-off and the throttle body
rep("const box=new T.Mesh(new T.BoxGeometry(46,120,50),M.cooler);box.position.set(-266,160,-6);", "const box=new T.Mesh(new T.BoxGeometry(46,74,50),M.cooler);box.position.set(-266,190,-6);")
rep("ft.repeat.set(1,22);", "ft.repeat.set(1,14);")
rep("const face=new T.Mesh(new T.PlaneGeometry(46,120),new T.MeshBasicMaterial({map:ft,color:col(0xb8c2cc),toneMapped:false,side:T.DoubleSide}));face.position.set(-266,160,0.05);",
    "const face=new T.Mesh(new T.PlaneGeometry(46,74),new T.MeshBasicMaterial({map:ft,color:col(0xb8c2cc),toneMapped:false,side:T.DoubleSide}));face.position.set(-266,190,0.05);")
rep("edges(scene,new T.PlaneGeometry(46,120),0.06).position.set(-266,160,0.06);", "edges(scene,new T.PlaneGeometry(46,74),0.06).position.set(-266,190,0.06);")
rep('const FEED=curvePath(', rd('base/b_parts.js') + '\n' + rd('base/b_vgt.js') + '\n' + rd('r_parts.js') + '\nconst FEED=curvePath(')
# the air filter is shorter: the MAF tube sits between it and the compressor inlet
rep("g.add(new T.Mesh(axGeo([[-232,0],[-232,30],[-190,30],[-190,24]],{full:true,seg:40,closed:false}),M.filter));",
    "g.add(new T.Mesh(axGeo([[-232,0],[-232,30],[-208,30],[-208,26.5]],{full:true,seg:40,closed:false}),M.filter));")
rep("for(let k=0;k<12;k++){const r=new T.Mesh(axGeo([[-229+k*3.2,30.4],[-227.4+k*3.2,30.4]]", "for(let k=0;k<7;k++){const r=new T.Mesh(axGeo([[-229+k*3.2,30.4],[-227.4+k*3.2,30.4]]")
between('/* --- air: filter -> inducer', '/* --- gas inside the cylinder --- */', rd('base/b_streams.js') + '\n' + rd('r_streams.js') + '\n')
# the inlet stream starts inside the filter and passes the MAF; chevrons after the MAF; stream 1 with loop mask and x-ray copy
rep("s1.forEach(p=>{p.L1=100;", "s1.forEach(p=>{p.L1=112;")
rep("turboPt(-200+k*100,p.ri,p.psi+0.2*k,out)", "turboPt(-212+k*112,p.ri,p.psi+0.2*k,out)")
rep("const CH_X0=-196,CH_L=78;", "const CH_X0=-186,CH_L=70;")
between('function drawS1(G,S){', 'const N2=420,s2=[]', rd('r_s1.js'))
rep("  for(const q of cyl){", "  if(!FUEL){colA=c<180||c>=705?AIR_C:new T.Color().copy(AIR_C).lerp(AIR_W,0.4);al=0.3;}\n  al*=CYLA;\n  for(const q of cyl){")
between('/* establishing */', '/* ================= camera ================= */', rd('r_labels.js') + '\n')
rep('const pv=(a0,a1,b0,b1)=>U=>pulse(U,a0,a0+0.4,b1-0.4,b1);\n', '')
between('const SHOTS={', 'const user=', rd('r_cam.js'))
between('const STEPS=[', '/* ================= per-frame state ================= */', rd('r_ui.js') + '\n')
between('const vEl=[0];', '/* ================= interaction and loop ================= */', rd('r_apply.js') + '\n')
# render: normal or split screen; in vo mode the hook leaves room for the titles above the scene
rep('''function render(){
  const r=apply(u);placeCamera(u);placeLabels(u);updateUI(u,r.th,r.st);
  renderer.render(scene,camera);dirty=false;
}''', '''function frameShot(s,vw,vh){
  const tf=Math.tan(FOV*DEG/2),aspect=vw/vh;camera.aspect=aspect;
  const d=Math.max((s.h/2)/tf,(s.w/2)/(tf*aspect))/user.zoom;
  const az=clamp(s.az+user.az,-80,80)*DEG,el=clamp(s.el+user.el,-30,60)*DEG;
  camTarget.set(s.c[0],s.c[1],0);
  camera.position.set(camTarget.x+d*Math.sin(az)*Math.cos(el),camTarget.y+d*Math.sin(el),d*Math.cos(az)*Math.cos(el));
  camera.lookAt(camTarget);camera.near=Math.max(1,d*0.05);camera.far=d*8+1500;camera.updateProjectionMatrix();camera.updateMatrixWorld();
  shared.uScale.value=vh*DPR/(2*tf);
}
function render(){
  const split=u>=T_S&&u<T_W,vo=document.body.classList.contains('vo');
  $('split').classList.toggle('on',split);
  if(vo){padTop=VH*(u<T_P?0.30:0.13);padBot=VH-VH*0.66;padLeft=0;}
  if(!split){
    renderer.setScissorTest(false);renderer.setViewport(0,0,VW,VH);camera.aspect=VW/VH;
    const r=apply(u,'main');placeCamera(u);placeLabels(u);updateUI(u,r.S);
    renderer.render(scene,camera);dirty=false;return;
  }
  for(const L of labelDefs){L.el.style.opacity=0;L.ln.style.opacity=0;L.dot.style.opacity=0;}
  const y0=padTop+4,y1=VH-padBot,hh=Math.max(60,(y1-y0-8)/2);
  renderer.setScissorTest(true);renderer.setScissor(0,0,VW,VH);renderer.setViewport(0,0,VW,VH);renderer.clear();
  [['top',y0],['bot',y0+hh+8]].forEach(q=>{
    apply(u,q[0]);frameShot(q[0]==='top'?SPLIT_A:SPLIT_B,VW,hh);
    const yb=VH-(q[1]+hh);renderer.setViewport(0,yb,VW,hh);renderer.setScissor(0,yb,VW,hh);renderer.render(scene,camera);
  });
  renderer.setScissorTest(false);
  $('spA').style.top=(y0+hh-$('spA').offsetHeight-8)+'px';$('spB').style.top=(y0+2*hh+8-$('spB').offsetHeight-8)+'px';$('spD').style.top=(y0+hh+3)+'px';
  {const lift=(u>=K.SP_C1&&u<K.SP_R1)||u>=K.SP_C2,c=$('spC');c.style.top=(y0+hh+4)+'px';if(c.dataset.l!==String(lift)){c.dataset.l=String(lift);c.textContent=lift?'Ridici piciorul':'Accelerezi';c.classList.toggle('lift',lift);}}
  /* the half that is not being talked about is dimmed */
  {const X=$('spX'),Y=$('spY');X.style.top=y0+'px';X.style.height=hh+'px';Y.style.top=(y0+hh+8)+'px';Y.style.height=hh+'px';
   Y.style.opacity=(0.62*pulse(u,K.SP_A0,K.SP_A0+0.35,K.SP_B0-0.15,K.SP_B0+0.2)).toFixed(3);X.style.opacity=(0.62*sst(K.SP_B0-0.15,K.SP_B0+0.2,u)).toFixed(3);}
  updateUI(u,null);dirty=false;
}''')
rep("  padTop=$('title').getBoundingClientRect().bottom+8;padBot=sidePanel?18:VH-br.top-18;padLeft=sidePanel?br.right+8:0;",
    "  padTop=$('title').getBoundingClientRect().bottom+8;padBot=sidePanel?18:VH-br.top-18;padLeft=sidePanel?br.right+8:0;\n  if(document.body.classList.contains('vo')){padTop=VH*0.13;padBot=VH-VH*0.66;padLeft=0;}")
rep("if(location.hash==='#reel')document.body.classList.add('reel');", "document.body.classList.add('reel','vo');")
rep("matches){u=27.5;setPlaying(false);}", "matches){u=16;setPlaying(false);}")
rep("window.__TU=TU;", "window.__TU=TU;window.__vo=on=>{document.body.classList.toggle('vo',on!==false);resize();render();};window.__K=K;")
open(os.path.join(D, 'blow-off-reel.html'), 'w', encoding='utf8').write('<meta name="claude:viewport-fit-sides" content="cover">\n' + src.strip() + '\n')
print('TU', TU, 'SEND', round(SEND, 3), 'bytes', len(src)); print({k: v for k, v in K.items() if k != 'HE'})
