# Aplica peste sursa animatiei "Amorsare filtru motorina" modul `vo` (reel/patch/80_hud.js) si carligele pentru refacerea
# sectiunii CP4 cu randare Blender: camera si starea pompei impuse din afara (window.__OV), treceri separate pentru
# particule si HUD (window.__PASS = 'ovl' | 'add'), canvas WebGL cu alfa (window.__ALPHA).
import shutil, sys
def rep(path, pairs):
    s = open(path, encoding='utf8').read()
    for a, b in pairs:
        if a not in s: sys.exit('lipseste in %s: %s' % (path, a[:70]))
        s = s.replace(a, b, 1)
    open(path, 'w', encoding='utf8').write(s)
shutil.copy('reel/patch/80_hud.js', 'src/80_hud.js')
rep('src/00_core.js', [
 ("const renderer=new T.WebGLRenderer({canvas:document.getElementById('gl'),antialias:true});",
  "const renderer=new T.WebGLRenderer({canvas:document.getElementById('gl'),antialias:true,alpha:!!window.__ALPHA,preserveDrawingBuffer:!!window.__ALPHA});"),
 ("renderer.setClearColor(0x111417,1);", "renderer.setClearColor(0x111417,window.__ALPHA?0:1);"),
])
rep('src/40_scene.js', [
 ("function shotAt(t){\n", "function shotAt(t){\n  const O_=window.__OV;if(O_&&O_.shot)return Object.assign({gk:1,tk:1,cp:1},O_.shot);\n"),
 ("  const u=t-TT.cp;const phi=-CAMc(t);\n  const fuel=1-ease((u-4.4)/2.2),heat=ease((u-5.6)/2.4)*(0.78+0.22*Math.sin(t*23)),rot=ease((u-8.8)/2.6),dam=u>10.4?1:0;\n  CP.set({phi,spin:SPINc(t),rot,dam,fuel,heat});",
  "  const O=(window.__OV&&window.__OV.st)||null;const tp=O&&O.tp!=null?O.tp:t;\n  const u=t-TT.cp;const phi=O?O.phi:-CAMc(t);\n  const fuel=O?O.fuel:1-ease((u-4.4)/2.2),heat=O?O.heat:ease((u-5.6)/2.4)*(0.78+0.22*Math.sin(t*23)),rot=O?O.rot:ease((u-8.8)/2.6),dam=O?O.dam:(u>10.4?1:0);\n  CP.set({phi,spin:O?O.spin:SPINc(t),rot,dam,fuel,heat});"),
 ("const bk=ease((u-4.2)/1.0)*(1-ease((u-9)/3)*0.6);", "const bk=O&&O.bk!=null?O.bk:ease((u-4.2)/1.0)*(1-ease((u-9)/3)*0.6);"),
 ("const p=(t*0.55+rnd(i*3.1))%1;const onX=i%2;const a=rnd(i*5.7);", "const p=(tp*0.55+rnd(i*3.1))%1;const onX=i%2;const a=rnd(i*5.7);"),
 ("const sk=ease((u-6.2)/1.2);", "const sk=O&&O.sk!=null?O.sk:ease((u-6.2)/1.2);"),
 ("const life=(t*2.6+rnd(i*2.9))%1;", "const life=(tp*2.6+rnd(i*2.9))%1;"),
 ("const C=FX.chips;const c1=u-9.6;", "const C=FX.chips;const c1=O&&O.c1!=null?O.c1:u-9.6;"),
])
rep('src/80_hud.js', [
 # panoul CP4 poate fi stins din regie (window.__OV.panel): in prim-plan acoperea partea de sus a capului hidraulic
 ('g.save();g.globalAlpha=window.__VOHOOK?0:k;',
  'g.save();g.globalAlpha=window.__VOHOOK?0:k*((window.__OV&&window.__OV.panel!=null)?window.__OV.panel:1);'),
 ("  const dry=ease((u-4.4)/2.2);const x=90,y=VO_TOP+98,w=900;", "  const O=(window.__OV&&window.__OV.st)||null;const dry=O?1-O.fuel:ease((u-4.4)/2.2);const x=90,y=VO_TOP+98,w=900;"),
 ("  const kr=fade(t,69.2,73.6,0.4);\n  if(kr>0){const p=proj(cpP(0,CP.S.h+26,0));g.save();g.globalAlpha=k*kr;",
  "  const kr=O&&O.kr!=null?O.kr:fade(t,69.2,73.6,0.4);\n  if(kr>0){const p=proj(cpP(0,CP.S.h+26,0));g.save();g.globalAlpha=k*kr;"),
 ("    const turn=ease((u-8.8)/2.6);const rx=150,ry=42;g.ellipse(p[0],p[1],rx,ry,0,Math.PI*0.15,Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn));g.stroke();\n    const ang=Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn);const ex=p[0]+rx*Math.cos(ang),ey=p[1]+ry*Math.sin(ang);\n    g.fillStyle=C.warn;g.beginPath();g.moveTo(ex,ey);g.lineTo(ex+16,ey-6);g.lineTo(ex+4,ey+14);g.closePath();g.fill();\n    font(700,48,FD);shadowTxt(()=>txt(Math.round(turn*90)+'°',p[0]+rx+24,p[1]-34,C.warn,'left','middle'));g.restore();}\n}\nfunction legendVO",
  "    const turn=O?O.rot:ease((u-8.8)/2.6);const rx=150,ry=42;g.ellipse(p[0],p[1],rx,ry,0,Math.PI*0.15,Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn));g.stroke();\n    const ang=Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn);const ex=p[0]+rx*Math.cos(ang),ey=p[1]+ry*Math.sin(ang);\n    g.fillStyle=C.warn;g.beginPath();g.moveTo(ex,ey);g.lineTo(ex+16,ey-6);g.lineTo(ex+4,ey+14);g.closePath();g.fill();\n    font(700,48,FD);shadowTxt(()=>txt(Math.round(turn*90)+'°',p[0]+rx+24,p[1]-34,C.warn,'left','middle'));g.restore();}\n}\nfunction legendVO"),
 ("window.__vo=on=>{window.__VOM=on!==false;};",
  "window.__vo=on=>{window.__VOM=on!==false;};\n"
  "// treceri pentru compunerea peste randarea Blender: 'ovl' = particule cu amestec normal (bule, pilitura) + HUD, pe fond transparent; 'add' = scantei si stralucire, pe negru\n"
  "let _pp=false;\nfunction passPrep(shot){const P=window.__PASS;if(!P||P==='full'||!shot.cp)return;\n"
  "  if(!_pp){_pp=true;const dm=new T.MeshBasicMaterial({colorWrite:false});\n"
  "    CP.cut.traverse(o=>{if(o.isMesh){if(o.material.transparent)o.visible=false;else o.material=dm;}});\n"
  "    renderer.setClearColor(P==='add'?0x000000:0x111417,P==='add'?1:0);}\n"
  "  FX.bub.visible=FX.chips.visible=(P==='ovl');FX.sparks.visible=FX.glow.visible=(P==='add');}\n"
  "window.__grab=(fmt,q)=>{const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.drawImage(renderer.domElement,0,0,W,H);x.drawImage(cv,0,0);return c.toDataURL(fmt||'image/png',q);};\n// masca de acoperire (scena + HUD) la jumatate de rezolutie, pentru marcajul din fundal: 255 = acoperit, 0 = fundal liber\nwindow.__maskSetup=()=>{renderer.setSize(540,960,false);scene.traverse(o=>{if(!o.material)return;const u=o.material.uniforms;if(u&&u.uSh&&u.uF)o.visible=false;(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{if(m.blending===T.AdditiveBlending)m.colorWrite=false;});});};   // fara podea (se topeste in fundal) si fara materialele aditive (caroseria raze X, straluciri): prin ele fundalul se vede intreg\nwindow.__mask=()=>{const c=window.__mc||(window.__mc=Object.assign(document.createElement('canvas'),{width:540,height:960}));const x=c.getContext('2d',{willReadFrequently:true});x.clearRect(0,0,540,960);x.drawImage(renderer.domElement,0,0,540,960);x.drawImage(cv,0,0,540,960);const im=x.getImageData(0,0,540,960),a=im.data;for(let i=0;i<a.length;i+=4){a[i]=a[i+1]=a[i+2]=a[i+3];a[i+3]=255;}x.putImageData(im,0,0);return c.toDataURL('image/png');};\n"
  "window.__projCP=(x,y,z)=>proj(cpP(x,y,z));"),
 ("  const shot=shotAt(t);placeCam(shot.c,shot.az,shot.el,shot.d,shot.oy+(vo?voDy(t,shot):0));update3D(t,shot);renderer.render(scene,cam);\n  g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);\n  if(vo){\n",
  "  const shot=shotAt(t);placeCam(shot.c,shot.az,shot.el,shot.d,shot.oy+(vo?voDy(t,shot):0));update3D(t,shot);passPrep(shot);renderer.render(scene,cam);\n  g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);\n  if(vo&&window.__PASS==='add'&&shot.cp)return;\n  if(vo){\n"),
])
print('ok')
