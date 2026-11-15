/* =====================================================================
   SERIES FX LAYER („De ce se strică turbinele”): everything is driven by plain numbers in FX
   ===================================================================== */
const FX={gas:1,airK:1,dirty:0,score:0,rub:0,showFilt:0,filt:0,bypass:0,dirt:0,soak:0,hotT:0,coke:0,smoke:0,
  flood:0,leak:0,blue:0,oilAir:0,pool:0,blowby:0,dclog:0,vcrust:0,prime:-1,low:0,only:-1,cold:0,leakSide:0};
window.__FX=FX;
const OIL_BASE0=OIL_BASE.clone(),OIL_HOT0=OIL_HOT.clone(),OILC0=OILC.clone(),OIL_DIRTY=col(0x2c1c08),OIL_DIRTYH=col(0x5a3e16),OIL_COKE=col(0x0c0906),OIL_COLD=col(0x8a7a52);
const POOL0=oilPool.material.color.clone(),POOLB0=oilPoolBack.material.color.clone();
/* turbine-side oil (gallery branch, drop to the bearing, bearing films) gets its own colours so it can coke on its own */
const OIL_T=OIL_BASE.clone(),OIL_TH=OIL_HOT.clone();
[2,4,14,15,16,17,18,19,20,21].forEach(i=>{const m=oilNet[i];m.uniforms.uBase={value:OIL_T};m.uniforms.uHot={value:OIL_TH};});
const ptsFront=(n,o)=>{const p=makePts(n,o);p.mat.depthTest=false;return p;};

/* ---- dirt carried by the oil: feed line -> inlet -> gallery -> bearings ---- */
const dirtRoutes=[-34,28,-52].map((bx,i)=>{
  const pts=FEED.path.P.filter(p=>true).map(p=>p.clone());
  const a=(x,y)=>pts.push(new T.Vector3(x,TY+y,0.4));
  a(OIL_A,18);a(bx,18);
  if(i<2){a(bx,9.4);a(bx+(i?5.5:-5.5),9.4);}else{a(-52,13);a(-55,13);a(-55,7);}
  return polyPath(pts);
});
const DIRT=[];for(let i=0;i<420;i++)DIRT.push({k:i%5<2?0:(i%5<4?1:2),ph:rnd(),sz:0.8+0.9*rnd(),j:[rnd()*2-1,rnd()*2-1],a:rnd()});
const dirtPts=ptsFront(420,{max:14,soft:0.5,order:5});
const DIRT_C=new T.Color(0.05,0.035,0.02);
function drawDirt(O){
  dirtPts.begin();
  if(FX.dirt>0.01)for(const q of DIRT){if(q.a>FX.dirt)continue;const path=dirtRoutes[q.k],d=((q.ph+O*0.5)%1)*path.len;path.at(d,_v);if(_v.z<-14&&_v.y>TY-70)continue;
    const w=d<FEED.path.len-10?1.5:(d<FEED.path.len+34?1.6:0.9);_v.x+=q.j[0]*w;_v.y+=q.j[1]*w;
    dirtPts.push(_v,DIRT_C,0.95*sst(0,20,d),1.25*q.sz);}
  dirtPts.end();
}
/* ---- scoring bands on the journals ---- */
const scoreMat=new T.MeshBasicMaterial({color:col(0x1c1510),transparent:true,opacity:0,toneMapped:false});
[-39,-37.2,-35.9,-33.4,-31.8,-29.6].forEach((x,i)=>rotC.add(new T.Mesh(axGeo([[x,5.08],[x+0.35+0.3*(i%2),5.08]],{full:true,seg:36,closed:false}),scoreMat)));
[23,24.6,26.9,28.4,30.6,32.5].forEach((x,i)=>rotT.add(new T.Mesh(axGeo([[x,5.08],[x+0.35+0.3*(i%2),5.08]],{full:true,seg:36,closed:false}),scoreMat)));
/* ---- blades rubbing the housings ---- */
const rubPts=ptsFront(500,{add:true,max:14,soft:0.8,order:7});
const RUB=[];for(let i=0;i<500;i++)RUB.push({ph:rnd(),a:rnd(),s:rnd(),sp:0.5+rnd(),side:i%2?1:-1,j:rnd()*2-1,w:i%4===0?1:0});
function drawRub(t){
  rubPts.begin();
  if(FX.rub>0.01)for(const q of RUB){if(q.a>FX.rub||(FX.rubSide>0.5&&FX.rubSide<1.5&&q.w)||(FX.rubSide>1.5&&!q.w))continue;const life=0.3,tt=((t*1.9+q.ph)%life)/life;
    let x,r;if(q.w){const p=tTip(0.15+0.7*q.s);x=p[0];r=p[1];}else{const p=cTip(0.35+0.65*q.s);x=p[0];r=p[1];}
    const ang=q.side*(Math.PI/2-0.05-0.5*tt*q.sp);turboPt(x+q.j*tt*5-(q.w?-1:1)*tt*7*q.sp,r+0.6+tt*9*q.sp,ang,_v);_v.y-=tt*tt*8;_v.z=Math.min(_v.z,-0.2)+2.5;
    _c.copy(SP_C).lerp(SP_H,tt);rubPts.push(_v,_c,(1-tt)*0.95,1.15);}
  rubPts.end();
}
/* ---- oil filter in section (spin-on, on the block) with by-pass valve ---- */
const filt=new T.Group();scene.add(filt);filt.visible=false;
const FLT={x0:-86,x1:-40,yc:-128,ro:24,ri:5,e0:8,e1:20};
const filtEl=[],filtValve=new T.Group();
(function(){
  const z=0.05,R_=(x0,y0,x1,y1,mat,zz)=>{const g=polyGeo([[x0,y0],[x1,y0],[x1,y1],[x0,y1]]);const m=new T.Mesh(g,mat);m.position.z=zz===undefined?z:zz;filt.add(m);edges(filt,g,(zz===undefined?z:zz)+0.01);return m;};
  const F=FLT,shell=flat(0x30363d),inner=flat(0x0d1117);
  R_(F.x0+4,F.yc-F.ro-3,F.x1+3,F.yc+F.ro+3,shell);           /* can */
  R_(F.x0+7,F.yc-F.ro,F.x1,F.yc+F.ro,inner,0.06);              /* inside */
  R_(F.x0,F.yc-F.ro-6,F.x0+4,F.yc+F.ro+6,C.block.clone?flat(0x4c535c):shell); /* mounting face */
  /* pleated element: two bands (section of the paper cylinder) */
  const pleat=document.createElement('canvas');pleat.width=64;pleat.height=8;const g2=pleat.getContext('2d');g2.fillStyle='#d9c28e';g2.fillRect(0,0,64,8);g2.fillStyle='#8f7a4a';for(let i=0;i<64;i+=8)g2.fillRect(i,0,3,8);
  const pt=new T.CanvasTexture(pleat);pt.wrapS=pt.wrapT=T.RepeatWrapping;pt.repeat.set(0.25,1);
  [1,-1].forEach(s=>{const g=polyGeo([[F.x0+10,F.yc+s*F.e0],[F.x1-7,F.yc+s*F.e0],[F.x1-7,F.yc+s*F.e1],[F.x0+10,F.yc+s*F.e1]]);
    const uv=g.attributes.uv,P=g.attributes.position;for(let i=0;i<P.count;i++)uv.setXY(i,P.getX(i),P.getY(i)/12);
    const m=new T.Mesh(g,new T.MeshBasicMaterial({map:pt,color:new T.Color(1,1,1),toneMapped:false,side:T.DoubleSide}));m.position.z=0.07;filt.add(m);edges(filt,g,0.08);filtEl.push(m);});
  /* end cap of the element and by-pass valve (disc + spring) at the closed end */
  R_(F.x1-7,F.yc+F.e0,F.x1-5.4,F.yc+F.e1,flat(0x5a626b),0.07);R_(F.x1-7,F.yc-F.e1,F.x1-5.4,F.yc-F.e0,flat(0x5a626b),0.07);
  const disc=new T.Mesh(polyGeo([[0,-F.e0+0.4],[1.6,-F.e0+0.4],[1.6,F.e0-0.4],[0,F.e0-0.4]]),flat(0xd4a02a));disc.position.set(F.x1-7,F.yc,0.09);filtValve.add(disc);
  const sp=[];for(let i=0;i<=8;i++)sp.push([F.x1-7-1.2-i*1.5,F.yc+(i%2?2.6:-2.6)]);
  const spg=new T.Mesh(ribbon(sp,0.35,0.09,0),flat(0xc3c9d0));filtValve.add(spg);filtValve.userData={disc,spg};filt.add(filtValve);
  /* short passages to the block gallery */
  R_(F.x0-6,F.yc+F.ro-5,F.x0+7,F.yc+F.ro-1,inner,0.06);R_(F.x0-6,F.yc-2.5,F.x0+7,F.yc+2.5,inner,0.06);
})();
const FLO=[];for(let i=0;i<360;i++)FLO.push({ph:rnd(),xc:FLT.x0+12+rnd()*(FLT.x1-FLT.x0-22),s:i%2?1:-1,r:rnd(),r2:rnd(),dirt:i%4===0,sz:0.8+0.5*rnd(),j:rnd()*2-1});
const filtPts=ptsFront(360,{max:14,soft:0.6,order:6});
const _fl=[new T.Vector3(),new T.Vector3(),new T.Vector3(),new T.Vector3(),new T.Vector3()];
function drawFilter(O){
  filt.visible=FX.showFilt>0.01;filtPts.begin();if(!filt.visible){filtPts.end();return;}
  const F=FLT,op=FX.bypass;
  filtEl.forEach(m=>m.material.color.setRGB(1,1,1).lerp(new T.Color(0.16,0.11,0.06),FX.filt));
  filtValve.userData.disc.position.x=F.x1-7-4.5*op;filtValve.userData.spg.scale.x=1;   /* disc lifts off its seat towards the centre tube */
  for(const q of FLO){
    const yo=F.yc+q.s*(F.ro-2.2+q.j*1.2),yi=F.yc+q.s*(1+2.2*Math.abs(q.j));
    const byp=q.r<op*0.9;let stop=false;
    _fl[0].set(F.x0-5,F.yc+F.ro-3,0.5);_fl[1].set(F.x0+9,yo,0.5);
    let pts;
    if(byp){_fl[2].set(F.x1-2.5,yo,0.5);_fl[3].set(F.x1-3,yi,0.5);_fl[4].set(F.x0-5,yi,0.5);pts=5;}
    else{_fl[2].set(q.xc,yo,0.5);_fl[3].set(q.xc,yi,0.5);_fl[4].set(F.x0-5,yi,0.5);pts=5;stop=q.dirt||q.r2<FX.filt;}
    let L=0;const seg=[];for(let i=1;i<pts;i++){const l=_fl[i].distanceTo(_fl[i-1]);seg.push(l);L+=l;}
    let d=((q.ph+O*0.9)%1)*150;if(d>L)continue;
    if(stop){const lim=seg[0]+seg[1]+(F.ro-2.2-F.e1)-0.4+q.r*1.2;if(d>lim){if(!q.dirt)continue;d=lim;}}
    let i=0;while(i<seg.length-1&&d>seg[i]){d-=seg[i];i++;}
    _v.copy(_fl[i]).lerp(_fl[i+1],clamp(d/seg[i],0,1));
    if(q.dirt){if(FX.dirt<0.02&&FX.filt<0.02&&q.r>0.35)continue;filtPts.push(_v,DIRT_C,0.95,1.5*q.sz);}
    else filtPts.push(_v,OILC,0.9,1.25*q.sz);
  }
  filtPts.end();
}
/* ---- heat soak after a hot shut-down: glow creeping from the turbine side, coke, smoke ---- */
const soakSpr=[[64,70,62],[47,34,44],[30,30,34],[8,30,30],[-20,30,26]].map((a,i)=>{const s=new T.Sprite(new T.SpriteMaterial({map:glowTex,blending:T.AdditiveBlending,depthWrite:false,depthTest:false,transparent:true,opacity:0,toneMapped:false,color:i?0xff3a10:0xff5a1c}));
  s.position.set(a[0],TY,5);s.scale.set(a[1]*1.5,a[2]*1.5,1);s.renderOrder=11;scene.add(s);return s;});
const THOUSE_E=new T.Color(),WHEELT_E=new T.Color();
const coke=new T.Group();turbo.add(coke);
(function(){
  const mat=flat(0x0b0806),mat2=flat(0x1d140c);let n=0;
  const add=(x,y,r,k)=>{const m=new T.Mesh(new T.CircleGeometry(r,9),(n++%3)?mat:mat2);m.position.set(x,y,0.12+0.002*n);m.userData.k=k;coke.add(m);};
  const h=i=>{const x=Math.sin(i*127.1+3.3)*43758.5453;return x-Math.floor(x);};
  for(let i=0;i<34;i++){const s=i%2?1:-1;add(22+12*h(i),s*(9.4+0.7*(h(i+50)-0.5)),0.55+0.75*h(i+9),0.15+0.3*h(i+20));}         /* outer film, turbine bearing */
  for(let i=0;i<22;i++){const s=i%2?1:-1;add(34+9*h(i+70),s*(7.0+2.4*h(i+80)),0.5+0.7*h(i+90),0.05+0.3*h(i+95));}               /* between bearing and seal ring */
  for(let i=0;i<10;i++){const s=i%2?1:-1;add(43.6+2.6*h(i+100),s*(7.2+0.5*h(i+110)),0.45+0.4*h(i+120),0.0+0.2*h(i+130));}       /* seal ring groove */
  for(let i=0;i<16;i++)add(28+1.6*(h(i+140)-0.5)*1.4,10.4+7.4*h(i+150),0.55+0.6*h(i+160),0.3+0.35*h(i+170));                     /* drop to the bearing */
  for(let i=0;i<20;i++)add(2+26*h(i+180),18+1.9*(h(i+190)-0.5)*1.5,0.55+0.6*h(i+200),0.45+0.4*h(i+210));                         /* gallery branch */
  for(let i=0;i<18;i++){const u=h(i+220);add(22-14*u*0.95,-13.2-20*u-1.2*h(i+230),0.7+0.9*h(i+240),0.4+0.5*h(i+250));}           /* drain cavity, turbine-side wall */
  for(let i=0;i<10;i++)add(-13+20*h(i+260),-35-12*h(i+270),0.8+1.0*h(i+280),0.6+0.4*h(i+290));                                    /* drain outlet */
})();
const SMK=[];for(let i=0;i<260;i++)SMK.push({ph:rnd(),x:rnd(),a:rnd(),sz:0.8+1.2*rnd(),j:rnd()*2-1});
const smkPts=ptsFront(260,{max:40,soft:1.8,order:8});const SMK_C=new T.Color(0.62,0.62,0.66),SMK_B=new T.Color(0.52,0.66,1.0),SMK_K=new T.Color(0.045,0.04,0.036);
function drawSmoke(t){
  smkPts.begin();
  if(FX.smoke>0.01)for(const q of SMK){if(q.a>FX.smoke)continue;const tt=(t*0.22+q.ph)%1;
    _v.set(18+30*q.x+q.j*8*tt+3*Math.sin(t*1.3+q.ph*20),TY+(q.a<0.5?9:-9)*(1-tt)+tt*(26+30*q.x)+tt*tt*14,1.5);
    smkPts.push(_v,SMK_C,0.3*Math.sin(Math.PI*Math.min(1,tt*1.15))*FX.smoke,5+12*tt*q.sz);}
  if(FX.blue>0.01)for(const q of SMK){if(q.a>FX.blue*0.75)continue;const tt=(t*0.5+q.ph)%1;
    _v.set(82+86*tt,TY+q.j*(9+9*tt)+2*Math.sin(t*2+q.ph*30),-2-10*q.x);
    smkPts.push(_v,SMK_B,0.42*Math.sin(Math.PI*Math.min(1,tt*1.1))*FX.blue,5+10*tt*q.sz);}
  if(FX.sootOut>0.01)for(const q of SMK){if(q.a>FX.sootOut*0.92)continue;const tt=(t*0.55+q.ph)%1;
    _v.set(84+112*tt,TY+q.j*(10+13*tt)+2*Math.sin(t*2+q.ph*30)+7*tt*tt,1.2);
    smkPts.push(_v,SMK_K,0.72*Math.sin(Math.PI*Math.min(1,tt*1.1))*FX.sootOut,6+13*tt*q.sz);}
  smkPts.end();
}
/* ---- blocked oil return / crankcase pressure ---- */
const dclog=new T.Group();scene.add(dclog);
(function(){const mat=flat(0x0b0806),mat2=flat(0x1d140c);
  for(let i=0;i<34;i++){const f=0.075+0.09*(i/33),p=DRAIN.curve.getPointAt(f);const m=new T.Mesh(new T.CircleGeometry(1.5+1.7*((i*37)%10)/10,9),i%3?mat:mat2);
    m.position.set(p.x+Math.sin(i*2.3)*3.6,p.y+Math.cos(i*1.7)*2,0.2+0.002*i);m.userData.k=((i*13)%34)/34;m.renderOrder=9;m.material.depthTest=false;dclog.add(m);}})();
const DCLOG_D=DRAIN.path.len*0.11;
const floodPlane=new T.Plane(new T.Vector3(0,-1,0),0);
const floodMat=new T.MeshBasicMaterial({color:col(0xc98a12),transparent:true,opacity:0.9,toneMapped:false,side:T.DoubleSide,clippingPlanes:[floodPlane]});
const flood=new T.Group();turbo.add(flood);
(function(){
  const add=pts=>{const m=new T.Mesh(polyGeo(pts),floodMat);m.position.z=-0.3;flood.add(m);};
  add([[-28,-12.6],[22,-12.6],[22,-14],[8,-34],[8,-48],[-14,-48],[-14,-34],[-28,-14]]);
  add([[-28,-12.6],[22,-12.6],[22,12.5],[-28,12.5]]);
  add([[-49,-8],[-40,-8],[-40,8],[-49,8]]);add([[-40,-10],[-28,-10],[-28,10],[-40,10]]);add([[22,-10],[42,-10],[42,10],[22,10]]);
  add([[-61,-7.6],[-49,-7.6],[-49,7.6],[-61,7.6]]);add([[42,-7.6],[50,-7.6],[50,7.6],[42,7.6]]);
  /* oil standing in the return hose above the blockage */
  const c=new T.CatmullRomCurve3(DRAIN.curve.getSpacedPoints(160).slice(0,20),false,'centripetal');
  const m=new T.Mesh(new T.TubeGeometry(c,30,3.2,10,false),new T.MeshBasicMaterial({color:col(0xc98a12),toneMapped:false,transparent:true,opacity:0.95,depthTest:false}));m.renderOrder=8;flood.userData.hose=m;scene.add(m);
})();
/* oil pushed past the seal rings: compressor side and turbine side, top and bottom of the cut */
const leakPaths=[];
[1,-1].forEach(s=>{
  leakPaths.push(polyPath([[-57,TY+s*7.4,0.6],[-65.5,TY+s*7.4,0.6],[-70.2,TY+s*7.8,0.6],[-70.6,TY+s*27,0.6],[-73,TY+s*30,0.6],[-82,TY+s*44,0.6]]));
  leakPaths.push(polyPath([[38,TY+s*7.3,0.6],[45,TY+s*7.3,0.6],[52.4,TY+s*8,0.6],[54.4,TY+s*20,0.6],[60,TY+s*27,0.6],[72,TY+s*22,0.6],[96,TY+s*14,0.6]]));
});
const LEAK=[];for(let i=0;i<440;i++)LEAK.push({k:i%4,ph:rnd(),a:rnd(),sz:0.8+0.6*rnd(),j:rnd()*2-1});
const leakPts=ptsFront(440,{max:16,soft:0.8,order:7});
function drawLeak(t){
  leakPts.begin();
  if(FX.leak>0.01)for(const q of LEAK){if(q.a>FX.leak||(FX.leakSide===1&&q.k%2===0)||(FX.leakSide===2&&q.k%2===1))continue;const path=leakPaths[q.k],u=(q.ph+t*0.16)%1,d=u*path.len;path.at(d,_v);
    _v.x+=q.j*0.5;_v.y+=q.j*0.5*(u>0.4?2:1);
    if(q.k%2&&u>0.62)_c.copy(OILC).lerp(SMK_B,(u-0.62)/0.38);else _c.copy(OILC);
    leakPts.push(_v,_c,0.95*sst(0,0.06,u)*(1-sst(0.86,1,u)),1.35*q.sz*(q.k%2&&u>0.62?1+3*(u-0.62):1));}
  leakPts.end();
}
/* oil collected in the intercooler */
const poolIC=new T.Mesh(polyGeo([[-288,100.5],[-244,100.5],[-244,122],[-288,122]]),new T.MeshBasicMaterial({color:col(0xb07810),toneMapped:false,transparent:true,opacity:0.95}));
poolIC.position.z=0.09;poolIC.renderOrder=6;scene.add(poolIC);
/* blow-by past the piston rings and pressure in the crankcase, pushing up the return hose */
const BB=[];for(let i=0;i<620;i++)BB.push({k:i%3,ph:rnd(),a:rnd(),x:rnd()*2-1,y:rnd(),s:i%2?1:-1,sz:0.8+0.8*rnd(),j:rnd()*2-1});
const bbPts=ptsFront(620,{max:22,soft:1.4,order:7});const BB_C=new T.Color(0.80,0.82,0.86);
const DRAIN_UP=polyPath(DRAIN.path.P.slice().reverse().map(p=>new T.Vector3(p.x,p.y,0.8)));
function drawBlowby(t,crown){
  bbPts.begin();
  if(FX.blowby>0.01)for(const q of BB){if(q.a>FX.blowby)continue;
    if(q.k===0){const u=(q.ph+t*0.45)%1;_v.set(EX+q.s*(R-0.4+q.j*0.7),lerp(crown-2,BLOCK_BOT-6,u),0.6);bbPts.push(_v,BB_C,0.7*sst(0,0.1,u)*(1-sst(0.85,1,u)),2.0*q.sz);}
    else if(q.k===1){const w=t*0.5+q.ph*30;_v.set(EX+q.x*58+4*Math.sin(w*1.3),-150-34*q.y+3*Math.cos(w),0.6);bbPts.push(_v,BB_C,0.34+0.2*Math.sin(w*2),4.2*q.sz);}
    else{const u=(q.ph+t*0.11)%1,d=u*(DRAIN_UP.len-DCLOG_D*0.2);DRAIN_UP.at(d,_v);_v.x+=q.j*2.6;bbPts.push(_v,BB_C,0.75*sst(0,0.05,u)*(1-sst(0.9,1,u)),2.4*q.sz);}
  }
  bbPts.end();
}
/* burnt-oil crust at the turbine inlet throat (variable geometry area) */
const vcrust=new T.Group();turbo.add(vcrust);
(function(){const mat=flat(0x0b0806),mat2=flat(0x241a10);const h=i=>{const x=Math.sin(i*91.7+1.3)*43758.5453;return x-Math.floor(x);};
  for(let i=0;i<44;i++){const s=i%2?1:-1,m=new T.Mesh(new T.CircleGeometry(0.8+1.3*h(i),9),i%3?mat:mat2);m.position.set(58+10*h(i+30),s*(29.5+7*h(i+60)),0.14+0.002*i);m.userData.k=h(i+90)*0.7;vcrust.add(m);}})();

const growSet=(grp,v,spread)=>grp.children.forEach(m=>{const k=clamp((v*(1+spread)-m.userData.k*spread)*1.0,0,1);m.visible=k>0.02;m.scale.setScalar(0.15+0.85*k);});
function applyFX(t,U,crown){
  const O=lut(LUT.oil,U);
  /* oil colour: clean -> dirty; cold oil a little paler */
  OIL_BASE.copy(OIL_BASE0).lerp(OIL_DIRTY,FX.dirty).lerp(OIL_COLD,FX.cold*0.5);OIL_HOT.copy(OIL_HOT0).lerp(OIL_DIRTYH,FX.dirty);
  OILC.copy(OILC0).lerp(OIL_DIRTYH,FX.dirty*0.9);
  OIL_T.copy(OIL_BASE).lerp(OIL_COKE,FX.coke);OIL_TH.copy(OIL_HOT).lerp(OIL_COKE,FX.coke);
  oilPool.material.color.copy(POOL0).lerp(OIL_DIRTY,FX.dirty*0.85);oilPoolBack.material.color.copy(POOLB0).lerp(OIL_DIRTY,FX.dirty*0.85);
  const ls=1-0.78*FX.low;oilPool.scale.y=ls;oilPool.position.y=-204*(1-ls);oilPoolBack.position.y=-14*(1-ls);
  scoreMat.opacity=0.85*FX.score;
  drawDirt(O);drawRub(t);drawFilter(O);drawSmoke(t);drawLeak(t);drawBlowby(t,crown);
  /* heat soak */
  soakSpr.forEach((s,i)=>{const k=i?clamp(FX.soak*4.6-(i-1)*1.0,0,1):Math.max(FX.hotT,FX.soak);s.material.opacity=(i?0.5:0.42)*k*(0.9+0.1*Math.sin(t*5+i));});
  M.tHouse.emissive.copy(THOUSE_E.setRGB(0.9,0.16,0.02)).multiplyScalar(0.55*FX.hotT);M.wheelT.emissive.copy(WHEELT_E.setRGB(1.0,0.2,0.03)).multiplyScalar(0.5*FX.hotT);
  tGlow.material.opacity=0.10+0.5*FX.hotT;
  growSet(coke,FX.coke,0.9);growSet(dclog,FX.dclog,0.5);growSet(vcrust,FX.vcrust,0.6);
  /* flood level in the bearing housing */
  flood.visible=FX.flood>0.004;flood.userData.hose.visible=FX.dclog>0.3&&FX.flood>0.004;
  floodPlane.constant=TY+lerp(-50,3,FX.flood);
  poolIC.visible=FX.pool>0.01;poolIC.scale.y=Math.max(0.02,FX.pool);poolIC.position.y=100.5*(1-Math.max(0.02,FX.pool));
  /* priming: the oil front travels through the feed line and the bearing housing */
  if(FX.prime>=0){const FL=FEED.path.len,pf=FX.prime*(FL+190);
    feedOil.uniforms.uHi.value=1;feedOil.uniforms.uFront.value=pf;oilNet.forEach(m=>{m.uniforms.uHi.value=1;m.uniforms.uFront.value=pf-FL;});
    drainOil.uniforms.uHi.value=1;drainOil.uniforms.uFront.value=(pf-FL-150)*6;}
  if(FX.dclog>0.5){drainOil.uniforms.uHi.value=1;drainOil.uniforms.uFront.value=DCLOG_D-14;}
  /* post-process the gas and air particles */
  const eA=exPts.A,eP=exPts.P,eC=exPts.C,eS=exPts.S,ne=exPts.g.drawRange.count;
  for(let i=0;i<ne;i++){eA[i]*=FX.gas;if(FX.blue>0.01&&eP[i*3]>80){const k=FX.blue*sst(80,100,eP[i*3]);eC[i*3]=lerp(eC[i*3],0.50,k);eC[i*3+1]=lerp(eC[i*3+1],0.64,k);eC[i*3+2]=lerp(eC[i*3+2],1.0,k);eA[i]=Math.min(1,eA[i]*(1+1.6*k));eS[i]*=1+1.8*k;}}
  const aA=airPts.A,aP=airPts.P,aC=airPts.C,na=airPts.g.drawRange.count;
  for(let i=0;i<na;i++){aA[i]*=FX.airK;if(FX.oilAir>0.01&&(aP[i*3+1]>TY+56||aP[i*3]<-190)){const k=FX.oilAir*0.75;aC[i*3]=lerp(aC[i*3],0.72,k);aC[i*3+1]=lerp(aC[i*3+1],0.46,k);aC[i*3+2]=lerp(aC[i*3+2],0.10,k);}}
}
