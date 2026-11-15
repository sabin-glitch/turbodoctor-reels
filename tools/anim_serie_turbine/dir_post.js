/* ================= SERIES DIRECTOR, part 2: time integrals, camera, labels, per-frame state ================= */
const DEF=Object.assign({starve:0,clog:0,pump:0,heat:0,wobble:0,sparks:0,top:560,eng:1,spn:1,air:1,shake:0},FX);DEF.prime=-1;DEF.only=-1;DEF.leakSide=0;
const trk=(k,t)=>TR[k]?track(TR[k],t):DEF[k];
if(!TR.top)TR.top=[[0,720],[HOOK_END-.4,720],[HOOK_END+.6,560],[END+3,560]];
/* engine time (U) and turbo angle follow the eng / spn tracks */
const NT=Math.ceil((END+4)*120),UA=new Float32Array(NT+1),SA=new Float32Array(NT+1);
(function(){let u=U0,s=0;const w=TAU*revs(16);for(let i=0;i<=NT;i++){const t=i/120;UA[i]=u;SA[i]=s;u+=trk('eng',t)/120;s+=w*trk('spn',t)/120;}})();
const arr=(A,t)=>{const x=clamp(t,0,NT/120)*120,i=Math.min(NT-1,Math.floor(x));return A[i]+(A[i+1]-A[i])*(x-i);};
const Uof=t=>arr(UA,t);
function snapAge(t){for(const s of SNAPS)if(t>=s[0]&&t<s[1])return t-s[0];return -1;}
function spinAfter(snapT,s){const w=TAU*revs(16)*trk('spn',snapT),k=2.6;return arr(SA,snapT)+w*(1-Math.exp(-k*s))/k;}

/* badge: which cause this is, on screen for the whole film */
(function(){const b=document.createElement('div');b.id='badge';
  b.innerHTML='<i>SERIA „DE CE SE STRICĂ TURBINELE”</i><b>CAUZA '+EP_N+' DIN '+SERIES_TOTAL+'</b><u>'+EP_NAME+'</u>';
  document.getElementById('stage').appendChild(b);})();
const badgeEl=$('badge');
/* brand watermark: rows of TURBO DOCTOR behind the scene, drifting slowly along their own direction */
const wmEl=$('wm'),wmRows=[];let wmUnit=0;
(function(){for(let i=0;i<17;i++){const r=document.createElement('div');r.className='r';r.style.top=(i*176)+'px';
  let h='';for(let k=0;k<9;k++)h+='<span>TURBO <b>DOCTOR</b></span>';r.innerHTML=h;wmEl.appendChild(r);wmRows.push(r);}})();
function placeWM(t){if(!wmUnit)wmUnit=wmRows[0].firstChild.offsetWidth||640;
  wmRows.forEach((r,i)=>{const off=((t*9+(i%2?wmUnit*0.5:0))%wmUnit+wmUnit)%wmUnit;r.style.transform='translateX('+(off-wmUnit).toFixed(1)+'px)';});}

const CAMK=CAM.slice().sort((a,b)=>a[0]-b[0]);
const VW=1080,VH=1920,PADBOT=VH-1280,LABBOT=1250;let padTop=560,pxPerMm=1;
const camTarget=new T.Vector3(),tmpV=new T.Vector3();
function shotAt(t){
  let i=0;while(i<CAMK.length-2&&t>CAMK[i+1][0])i++;
  const a=SHOTS[CAMK[i][1]],b=SHOTS[CAMK[i+1][1]],k=sst(CAMK[i][0],CAMK[i+1][0],t);
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
  const wob=Math.max(trk('wobble',t),trk('shake',t)),sa=snapAge(t);
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
const FXK=Object.keys(FX);
function apply(t){
  const U=Uof(t);
  const th=lut(LUT.th,U),crown=-CLEAR-pistonDrop(th);crownNow=crown;
  piston.position.y=crown;rod.position.y=crown-COMP_H;rod.rotation.z=Math.asin(CRK*Math.sin(th*DEG)/ROD);
  const li=vLift(th,712,222),le=vLift(th,498,8);
  vIn.g.position.y=-li;vEx.g.position.y=-le;
  setHelix(vIn.sp.geometry,HEAD_H+1.3,22.4-li);setHelix(vEx.sp.geometry,HEAD_H+1.3,22.4-le);
  const st=drawCyl(th,crown);const run=clamp(trk('eng',t)*4,0,1);
  const cy=Math.max(crown*0.5-3,-40);
  fireLight.intensity=1.6*st.burn*run;fireLight.position.set(EX,cy,10);
  glow.material.opacity=0.2*st.burn*run;glow.position.set(EX,cy-2,-8);const gs=60+26*st.burn+Math.min(-crown,60)*0.9;glow.scale.set(gs,gs*0.72,1);
  for(const k of FXK)FX[k]=trk(k,t);
  FX.only=TR.only?Math.round(track(TR.only,t)):-1;FX.leakSide=TR.leakSide?Math.round(track(TR.leakSide,t)):0;
  FAIL.only=FX.only>=0?FX.only:null;
  const sa=snapAge(t);
  FAIL.starve=trk('starve',t);FAIL.clog=trk('clog',t);FAIL.pump=trk('pump',t);FAIL.heat=trk('heat',t);
  FAIL.wobble=trk('wobble',t);FAIL.sparks=trk('sparks',t);FAIL.snap=sa;
  FAIL.spinC=null;FAIL.spinT=null;FAIL.air=trk('air',t);
  if(sa>=0){const snapT=t-sa;FAIL.spinC=spinAfter(snapT,sa);FAIL.air*=Math.exp(-sa*1.6);}
  drawExhaust(U);drawAir(U);
  const O=lut(LUT.oil,U);
  oilMats.forEach(m=>{m.uniforms.uHi.value=0;m.uniforms.uFront.value=1e5;m.uniforms.uPhase.value=O*(m.uniforms.uLen.value>1.5?1.6:1.0);});
  oilNet.blockMat.uniforms.uFront.value=1e5;
  const FL=FEED.path.len;
  if(FX.prime>=0)drawDrops(U,1,(FX.prime*(FL+190)-FL-60)*3);
  else if(FX.dclog>0.5)drawDrops(U,1,DCLOG_D+34);
  else drawDrops(U,0,1e5);
  applyFail(t,arr(SA,t));
  if(FX.only>=0)heatSpr.forEach((s,i)=>{if(i!==FX.only)s.material.opacity=0;});
  applyFX(t,U,crown);applyFX2(t,U,crown);
  return {th,st};
}
const dipEl=$('dip'),flashEl=$('flash');
function frame(t){
  padTop=track(TR.top,t);
  apply(t);placeCamera(t);placeLabels(t);
  let dp=0;for(const c of DIPS)dp=Math.max(dp,1-Math.abs(t-c)/0.22);dipEl.style.opacity=clamp(dp,0,1);
  let fl=0;for(const c of FLASHES){const q=t-c;if(q>=-0.03&&q<0.5)fl=Math.max(fl,q<0?1+q/0.03:Math.exp(-q*7));}flashEl.style.opacity=(0.85*fl).toFixed(3);
  badgeEl.style.opacity=sst(0.5,1.0,t).toFixed(3);
  placeWM(t);
  renderer.render(scene,camera);
}
renderer.setSize(VW,VH,false);camera.aspect=VW/VH;camera.updateProjectionMatrix();svg.setAttribute('viewBox','0 0 '+VW+' '+VH);
window.__frame=frame;window.__end=END;
window.__info={snaps:SNAPS,dips:DIPS,flashes:FLASHES,hookEnd:HOOK_END,end:END};
frame(0);
const boot=()=>{wmUnit=0;frame(0);window.__ready=true;};
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(boot);else boot();
