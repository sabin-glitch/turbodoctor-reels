/* ================= REEL (video build): director for „Nu schimba turbina până nu vezi asta” ================= */
const CU=window.CUES||{end:50,lines:[],words:[]};
const nrm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const Ts=i=>CU.lines[i].start,Te=i=>CU.lines[i].end,END=CU.end;
function W(i,word,nth){const ws=CU.words.filter(w=>w.win===i&&nrm(w.text)===nrm(word)),w=ws[(nth||1)-1];if(!w){console.warn('CUE_MISSING '+i+' '+word);return Ts(i);}return w.s;}
function track(tr,t){let i=0;while(i<tr.length-2&&t>tr[i+1][0])i++;const a=tr[i],b=tr[i+1];return lerp(a[1],b[1],sst(a[0],b[0],t));}
let crownNow=-CLEAR;
const U0=16;                 /* engine and turbo at full speed for the whole reel */
const Uof=t=>U0+t;

/* ---------- key moments ---------- */
const SNAP1=W(0,'asta')+0.05, SNAP2=W(7,'rupe')+0.1, SNAP3=W(10,'problemă')+0.05;
const NEW1=Ts(2)-0.3, NEW2=Ts(9)-0.35, NEW3=Ts(10)-0.3, CLEAN=W(11,'rezolvi');
const DIPS=[NEW1,NEW2,NEW3];
/* failure tracks */
const TR={
  starve:[[0,1],[NEW1-.01,1],[NEW1,0],[W(6,'lagărele')-.2,0],[Te(6)+.1,1],[NEW2-.01,1],[NEW2,.85],[NEW3-.01,.85],[NEW3,0],[W(10,'turbină')+.2,0],[SNAP3-.4,1],[CLEAN-.01,1],[CLEAN+.9,0],[END+3,0]],
  clog:[[0,1],[NEW1-.01,1],[NEW1,0],[W(6,'depuneri')-.1,0],[W(6,'turul')+.4,1],[CLEAN,1],[CLEAN+.9,0],[END+3,0]],
  pump:[[0,0],[W(6,'pompă')-.2,0],[W(6,'slăbită')+.3,1],[CLEAN,1],[CLEAN+.7,0],[END+3,0]],
  heat:[[0,.55],[SNAP1,1],[NEW1-.01,.8],[NEW1,0],[Ts(7)-.1,0],[W(7,'încing')+.5,.85],[SNAP2,1],[NEW2-.01,.75],[NEW2,.55],[NEW3-.01,.55],[NEW3,0],[W(10,'orice')+.4,0],[SNAP3,1],[CLEAN-.01,.6],[CLEAN+.2,0],[END+3,0]],
  wobble:[[0,.55],[SNAP1-.05,1],[SNAP1,0],[W(7,'gripează')-.2,0],[W(7,'gripează')+.3,1],[SNAP2-.05,1],[SNAP2,0],[W(10,'pune')-.1,0],[SNAP3-.2,1],[SNAP3,0],[END+3,0]],
  sparks:[[0,.6],[SNAP1-.05,1],[SNAP1,0],[W(7,'gripează')-.1,0],[W(7,'gripează')+.25,1],[SNAP2,1],[SNAP2+.01,0],[W(10,'pune'),0],[SNAP3-.3,1],[SNAP3,0],[END+3,0]],
  top:[[0,720],[NEW1-.4,720],[NEW1+.6,560],[END+3,560]]
};
function snapAge(t){
  if(t<NEW1&&t>=SNAP1)return t-SNAP1;
  if(t>=SNAP2&&t<NEW3)return t-SNAP2;
  if(t>=SNAP3&&t<CLEAN-.01)return t-SNAP3;
  return -1;
}
/* compressor half spins down after the break; the turbine half keeps turning on the exhaust gas */
function spinAfter(snapT,s){const base=lut(LUT.spin,Uof(snapT)),w=TAU*revs(Uof(snapT)),k=2.6;return base+w*(1-Math.exp(-k*s))/k;}

/* ---------- labels ---------- */
const labelDefs=[],svg=$('leaders'),labBox=$('labels');
function addLabel(text,sub,anchor,side,dx,dy,vis,cls){
  const el=document.createElement('div');el.className='lb'+(side<0?' l':'')+(cls?' '+cls:'');el.textContent=text;
  if(sub){const s=document.createElement('small');s.textContent=sub;el.appendChild(s);}
  labBox.appendChild(el);
  const ln=document.createElementNS('http://www.w3.org/2000/svg','line'),dot=document.createElementNS('http://www.w3.org/2000/svg','circle');
  dot.setAttribute('r','5');svg.appendChild(ln);svg.appendChild(dot);
  const L={el,ln,dot,anchor:typeof anchor==='function'?anchor:()=>anchor,side,dx,dy,vis,w:0,h:0};labelDefs.push(L);return L;
}
const win=(a,b,fi,fo)=>t=>pulse(t,a,a+(fi||.3),b-(fo||.3),b);
/* hook */
addLabel('Ax rupt',null,()=>[FRAC_A+2,TY-6,2],1,22,-22,win(SNAP1+.25,NEW1-.05),'bad');
addLabel('Lagăre fără ulei',null,[-34,TY+6.2,0],-1,26,26,win(.15,SNAP1+.2),'bad');
/* how it works */
addLabel('Gaze de evacuare','~750 °C',()=>[30,62,-44],1,30,-10,win(W(2,'gazele')-.2,W(2,'ridică')+.2),'fire');
addLabel('Turbină',null,[86,TY+36,-10],1,16,20,win(W(2,'învârtită')-.2,W(2,'ridică')+.4),'fire');
addLabel('Compresor',null,[-104,TY+40,-10],1,20,40,win(W(2,'ridică')-.1,Te(2)+.3),'air');
addLabel('Presiune pe admisie','+1,2 bar',[-266,200,0],1,30,-30,win(W(2,'presiunea')-.1,Te(2)+.3),'air');
addLabel('>100.000 rpm',null,()=>[-14,TY+5,5],-1,20,-30,win(W(3,'100.000')-.2,Te(3)+.25),'num');
addLabel('Film de ulei','axul plutește',[28,TY+5.6,0],1,24,22,win(W(4,'plutește')-.3,Te(4)+.3),'oil');
addLabel('Film de ulei',null,[-34,TY-9.4,0],-1,22,-20,win(W(4,'film')-.2,Te(4)+.3),'oil');
addLabel('Presiune corectă','~3 bar',[OIL_A,TY+52,0],1,20,10,win(W(5,'presiune')-.2,Te(5)+.3),'oil');
addLabel('Debit suficient',null,()=>{const p=FEED.curve.getPointAt(0.72);return [p.x,p.y,p.z];},-1,18,-6,win(W(5,'debit')-.2,Te(5)+.3),'oil');
/* failure causes */
addLabel('Pompă de ulei slăbită',null,[EX+40,-186,0],1,30,24,win(W(6,'pompă')-.1,W(6,'depuneri')-.1),'bad');
addLabel('Depuneri pe tur',null,()=>{const p=FEED.curve.getPointAt(0.86);return [p.x,p.y,p.z];},-1,22,8,win(W(6,'depuneri')-.05,W(6,'lagărele')),'bad');
addLabel('Lagăre fără ulei',null,[-34,TY+6.2,0],-1,26,26,win(W(6,'lagărele')+.1,W(7,'încing')+.2),'bad');
addLabel('Se încing',null,[28,TY+8.8,0],1,24,22,win(W(7,'încing')-.05,W(7,'gripează')),'bad');
addLabel('Se gripează',null,[28,TY+8.8,0],1,24,22,win(W(7,'gripează')-.05,SNAP2),'bad');
addLabel('Ax rupt',null,()=>[FRAC_A+2,TY-6,2],1,22,-22,win(SNAP2+.2,NEW2-.05),'bad');
/* the cause stays */
addLabel('Cauza',"pompa de ulei",[EX+40,-186,0],1,30,24,win(W(9,'important')-.2,NEW3-.05),'bad');
addLabel('Cauza','depuneri pe tur',()=>{const p=FEED.curve.getPointAt(0.86);return [p.x,p.y,p.z];},-1,22,8,win(W(9,'important'),NEW3-.05),'bad');
addLabel('Turbină nouă',null,[0,TY+34,0],1,22,30,win(NEW3+.1,W(10,'aceeași')-.3),'good');
addLabel('Aceeași problemă',null,()=>[FRAC_A+2,TY-6,2],1,22,-22,win(SNAP3+.15,CLEAN-.05),'bad');
addLabel('Ungere rezolvată',null,[OIL_A,TY+52,0],1,20,10,win(CLEAN+.6,END+3),'good');
addLabel('Turbina pe ulei',null,[28,TY+5.6,0],1,24,22,win(W(11,'montezi')-.1,END+3),'oil');

/* ---------- camera ---------- */
const SHOTS={
  hook:{c:[-6,TY+2],w:150,h:118,az:16,el:5},
  brg:{c:[-8,TY+3],w:112,h:84,az:9,el:3},
  shaft:{c:[-6,TY+4],w:210,h:150,az:20,el:6},
  wide:{c:[-70,70],w:430,h:300,az:16,el:7},
  turb:{c:[60,TY-20],w:230,h:260,az:28,el:9},
  comp:{c:[-150,TY-10],w:300,h:230,az:-8,el:6},
  chraIn:{c:[-10,TY+28],w:130,h:120,az:8,el:3},
  pump:{c:[EX+20,-170],w:240,h:150,az:10,el:6},
  feedTop:{c:[-14,TY+40],w:120,h:110,az:14,el:4},
  mid:{c:[-80,-10],w:400,h:300,az:12,el:6},
  cause:{c:[-60,5],w:380,h:375,az:10,el:5}
};
const CAM=[
  [0,'brg'],[SNAP1-.2,'hook'],[NEW1-.001,'hook'],
  [NEW1,'wide'],[W(2,'gazele')-.2,'wide'],[W(2,'evacuare'),'turb'],[W(2,'ridică')-.1,'turb'],[W(2,'admisie'),'comp'],[Te(2)+.15,'comp'],
  [Ts(3)-.1,'shaft'],[Te(3),'shaft'],[Ts(4)+.2,'brg'],[Te(4),'brg'],[Ts(5)+.3,'chraIn'],[Te(5)+.2,'chraIn'],
  [Ts(6)+.2,'mid'],[W(6,'pompă')-.1,'pump'],[W(6,'depuneri')-.4,'pump'],[W(6,'depuneri')+.3,'feedTop'],[W(6,'lagărele')-.3,'feedTop'],[W(6,'lagărele')+.3,'brg'],
  [Ts(7),'brg'],[SNAP2-.2,'hook'],[Te(8),'shaft'],[NEW2-.001,'shaft'],
  [NEW2,'cause'],[NEW3-.001,'cause'],
  [NEW3,'shaft'],[W(10,'turbină')+.3,'shaft'],[SNAP3-.3,'hook'],[CLEAN-.3,'hook'],
  [CLEAN+.2,'cause'],[W(11,'montezi'),'shaft'],[END+3,'shaft']
];
const VW=1080,VH=1920,PADBOT=VH-1280,LABBOT=1250;let padTop=560,pxPerMm=1;
const camTarget=new T.Vector3(),tmpV=new T.Vector3();
function shotAt(t){
  let i=0;while(i<CAM.length-2&&t>CAM[i+1][0])i++;
  const a=SHOTS[CAM[i][1]],b=SHOTS[CAM[i+1][1]],k=sst(CAM[i][0],CAM[i+1][0],t);
  const lw=Math.exp(lerp(Math.log(a.w),Math.log(b.w),k)),lh=Math.exp(lerp(Math.log(a.h),Math.log(b.h),k));
  return {cx:lerp(a.c[0],b.c[0],k),cy:lerp(a.c[1],b.c[1],k),w:lw,h:lh,az:lerp(a.az,b.az,k),el:lerp(a.el,b.el,k)};
}
function placeCamera(t){
  const s=shotAt(t),tf=Math.tan(FOV*DEG/2),aspect=VW/VH,safeH=VH-padTop-PADBOT,safeW=VW-64;
  const d=Math.max((s.h/2)/tf*(VH/safeH),(s.w/2)/(tf*aspect)*(VW/safeW)),az=s.az*DEG,el=s.el*DEG;
  camTarget.set(s.cx,s.cy,0);
  camera.position.set(camTarget.x+d*Math.sin(az)*Math.cos(el),camTarget.y+d*Math.sin(el),d*Math.cos(az)*Math.cos(el));
  camera.lookAt(camTarget);
  camera.updateMatrixWorld();tmpV.setFromMatrixColumn(camera.matrixWorld,1);
  camera.position.addScaledVector(tmpV,((padTop-PADBOT)/2)/VH*(2*d*tf));
  /* shake: grinding before the break, a hard kick at the break */
  const wob=track(TR.wobble,t),sa=snapAge(t);
  let amp=d*0.0035*wob;if(sa>=0&&sa<0.9)amp+=d*0.02*Math.exp(-sa*5);
  if(amp>0){camera.position.x+=amp*Math.sin(t*97);camera.position.y+=amp*Math.cos(t*83);}
  camera.near=Math.max(1,d*0.05);camera.far=d*8+1500;camera.updateProjectionMatrix();
  camera.updateMatrixWorld();
  pxPerMm=VH/(2*d*tf);shared.uScale.value=VH*DPR/(2*tf);
}
function placeLabels(t){
  for(const L of labelDefs){
    let o=L.vis(t);
    if(o>=0.02){const a=L.anchor();tmpV.set(a[0],a[1],a[2]).project(camera);L.sx=(tmpV.x*0.5+0.5)*VW;L.sy=(-tmpV.y*0.5+0.5)*VH;o*=sst(padTop-140,padTop-80,L.sy)*(1-sst(LABBOT+10,LABBOT+60,L.sy))*sst(-10,30,L.sx)*(1-sst(VW-30,VW+10,L.sx));}
    if(o<0.02){L.el.style.opacity=0;L.ln.style.opacity=0;L.dot.style.opacity=0;continue;}
    const x=L.sx,y=L.sy;if(!L.w){L.w=L.el.offsetWidth;L.h=L.el.offsetHeight;}
    const dx=clamp(L.dx*pxPerMm,30,260),ty=clamp(y-L.dy*pxPerMm,padTop+L.h/2+8,LABBOT-L.h/2);let ex,lx;
    if(L.side>0){lx=Math.min(x+dx,VW-L.w-(ty>800?112:34));ex=lx;}else{ex=Math.max(x-dx,L.w+34);lx=ex-L.w;}
    L.el.style.transform='translate('+lx.toFixed(1)+'px,'+(ty-L.h/2).toFixed(1)+'px)';
    L.el.style.opacity=o;L.ln.style.opacity=o;L.dot.style.opacity=o;
    L.ln.setAttribute('x1',x.toFixed(1));L.ln.setAttribute('y1',y.toFixed(1));L.ln.setAttribute('x2',ex.toFixed(1));L.ln.setAttribute('y2',ty.toFixed(1));
    L.dot.setAttribute('cx',x.toFixed(1));L.dot.setAttribute('cy',y.toFixed(1));
  }
}

/* ---------- per-frame state ---------- */
function apply(t){
  const U=Uof(t);
  const th=lut(LUT.th,U),crown=-CLEAR-pistonDrop(th);crownNow=crown;
  piston.position.y=crown;rod.position.y=crown-COMP_H;rod.rotation.z=Math.asin(CRK*Math.sin(th*DEG)/ROD);
  const li=vLift(th,712,222),le=vLift(th,498,8);
  vIn.g.position.y=-li;vEx.g.position.y=-le;
  setHelix(vIn.sp.geometry,HEAD_H+1.3,22.4-li);setHelix(vEx.sp.geometry,HEAD_H+1.3,22.4-le);
  const st=drawCyl(th,crown);
  const cy=Math.max(crown*0.5-3,-40);
  fireLight.intensity=1.6*st.burn;fireLight.position.set(EX,cy,10);
  glow.material.opacity=0.2*st.burn;glow.position.set(EX,cy-2,-8);const gs=60+26*st.burn+Math.min(-crown,60)*0.9;glow.scale.set(gs,gs*0.72,1);
  tGlow.material.opacity=0.10;
  drawExhaust(U);drawAir(U);
  const O=lut(LUT.oil,U);
  oilMats.forEach(m=>{m.uniforms.uHi.value=0;m.uniforms.uFront.value=1e5;m.uniforms.uPhase.value=O*(m.uniforms.uLen.value>1.5?1.6:1.0);});
  oilNet.blockMat.uniforms.uFront.value=1e5;
  /* failure layer */
  const sa=snapAge(t);
  FAIL.starve=track(TR.starve,t);FAIL.clog=track(TR.clog,t);FAIL.pump=track(TR.pump,t);FAIL.heat=track(TR.heat,t);
  FAIL.wobble=track(TR.wobble,t);FAIL.sparks=track(TR.sparks,t);FAIL.snap=sa;
  FAIL.spinC=null;FAIL.spinT=null;FAIL.air=1;
  if(sa>=0){const snapT=t-sa;FAIL.spinC=spinAfter(snapT,sa);FAIL.air=Math.exp(-sa*1.6);}
  drawDrops(U,0,1e5);
  applyFail(t,lut(LUT.spin,U));
  return {th,st};
}

/* ---------- frame API ---------- */
const dipEl=$('dip'),flashEl=$('flash');
function frame(t){
  padTop=track(TR.top,t);
  apply(t);placeCamera(t);placeLabels(t);
  let dp=0;for(const c of DIPS)dp=Math.max(dp,1-Math.abs(t-c)/0.22);dipEl.style.opacity=clamp(dp,0,1);
  let fl=0;for(const c of [SNAP1,SNAP2,SNAP3]){const q=t-c;if(q>=-0.03&&q<0.5)fl=Math.max(fl,q<0?1+q/0.03:Math.exp(-q*7));}flashEl.style.opacity=(0.85*fl).toFixed(3);
  renderer.render(scene,camera);
}
renderer.setSize(VW,VH,false);camera.aspect=VW/VH;camera.updateProjectionMatrix();svg.setAttribute('viewBox','0 0 '+VW+' '+VH);
window.__frame=frame;window.__end=END;
/* sound-bed probe: turbo whine level, grinding, break, compressor spin-down */
window.__probe=t=>{const sa=snapAge(t);return [track(TR.wobble,t),track(TR.sparks,t),sa,track(TR.heat,t),sa>=0?Math.exp(-sa*2.6):1];};
window.__info={snaps:[SNAP1,SNAP2,SNAP3],dips:DIPS,clean:CLEAN,end:END};
frame(0);
const boot=()=>{frame(0);window.__ready=true;};
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(boot);else boot();
