/* =====================================================================
   SERIES FX LAYER, part 2 (episodes 5–13): foreign objects, overheated gas, overspeed, variable geometry,
   particle filter, leaks on the air and gas path, fitting mistakes. Everything is driven by plain numbers in FX.
   ===================================================================== */
Object.assign(FX,{sand:0,sandB:0,sandMetal:0,afTorn:0,afClog:0,afHide:0,chipC:0,chipT:0,gasHot:0,crack:0,crackW:0,grow:0,rubSide:0,
  sootGas:0,sootOut:0,inset:0,insetKind:0,vgtPos:0.5,vgtSoot:0,vgtJit:0,vgtBent:0,peel:0,showDpf:0,dpfClog:0,gasIn:0,hoseLeak:0,manLeak:0,sil:0,chips:0});
const fmat=(h,x)=>flat(h,Object.assign({depthTest:false,transparent:true},x||{}));
const addF=(parent,geo,mat,order,z)=>{const m=new T.Mesh(geo,mat);m.renderOrder=order;if(z!==undefined)m.position.z=z;parent.add(m);return m;};
const hsh=i=>{const x=Math.sin(i*127.1+11.7)*43758.5453;return x-Math.floor(x);};
const ngon=(r,n,a0)=>{const p=[];for(let i=0;i<n;i++){const a=(a0||0)+i*TAU/n;p.push([r*Math.cos(a),r*Math.sin(a)]);}return p;};
function holed(outer,rh){const s=new T.Shape(outer.map(p=>V2(p[0],p[1])));const h=new T.Path();h.absarc(0,0,rh,0,TAU,true);s.holes.push(h);return new T.ShapeGeometry(s,20);}
const glowSpr=(c,o,sx,sy,order)=>{const s=new T.Sprite(new T.SpriteMaterial({map:glowTex,blending:T.AdditiveBlending,depthWrite:false,depthTest:false,transparent:true,opacity:o,toneMapped:false,color:c}));s.scale.set(sx,sy,1);s.renderOrder=order||13;return s;};

/* ---- foreign object on the intake side: nut / washer / ice from the filter housing into the compressor wheel ---- */
const fodG=new T.Group();fodG.visible=false;scene.add(fodG);
fodG.add(glowSpr(0xffffff,0.28,34,34,13));
const fodKinds=[
  {geo:holed(ngon(5.8,6,0),2.5),edge:polyGeo(ngon(6.8,6,0)),c:0xe6ebf0},
  {geo:holed(ngon(5.6,30,0),2.7),edge:polyGeo(ngon(6.5,30,0)),c:0xdfe5ea},
  {geo:polyGeo([[-6,-2],[-3.5,-5],[2,-5.5],[6,-2.5],[5,3],[1,5.6],[-4,4.5]]),edge:polyGeo([[-7,-2.3],[-4,-5.9],[2.3,-6.5],[7,-2.9],[5.9,3.5],[1.2,6.6],[-4.7,5.3]]),c:0xbfeaff}
].map(k=>{const g=new T.Group();addF(g,k.edge,fmat(0x05080b),14);addF(g,k.geo,fmat(k.c),15,0.01);fodG.add(g);return g;});
/* window.FODS=[[t0,t1,kind,hold]]: flies from the filter housing (t0) to the wheel (t1); with hold it lies in the housing from that time on */
function placeFod(t){
  let cur=null;for(const f of (window.FODS||[]))if(t>=(f[3]!==undefined?f[3]:f[0])&&t<f[1])cur=f;
  fodG.visible=!!cur;if(!cur)return;
  const k=clamp((t-cur[0])/(cur[1]-cur[0]),0,1),f=Math.pow(k,1.5),py=TY+8*Math.sin(f*11+1)*(1-0.5*f);
  fodKinds.forEach((g,i)=>g.visible=i===cur[2]);
  fodG.position.set(lerp(-224,-104,f),cur[3]!==undefined?lerp(TY-20,py,sst(0,0.3,k)):py,1.5);fodKinds[cur[2]].rotation.z=-f*13;
}
const hitK=(L,t)=>{let k=-1;for(const h of (L||[]))if(t>=h&&t<h+1.15)k=(t-h)/1.15;return k;};
/* ---- fragment coming from the engine through the exhaust manifold into the turbine wheel ---- */
const fodTPath=(function(){const pts=EXP.P.map(p=>p.clone());
  for(let i=1;i<=24;i++){const ph=i/24*Math.PI/2;pts.push(turboPt(TV.a0,TV.r(ph),ph,new T.Vector3()));}
  pts.push(new T.Vector3(63,TY+40,0),new T.Vector3(59.5,TY+29.5,0));return polyPath(pts);})();
const fodTG=new T.Group();fodTG.visible=false;scene.add(fodTG);
fodTG.add(glowSpr(0xff8a3a,0.55,40,40,13));
const fodTM=new T.Group();fodTG.add(fodTM);
addF(fodTM,polyGeo([[-5.6,-1.9],[-1.9,-5],[4.3,-3.8],[6.1,1.2],[1.9,5.2],[-4.4,3.8]]),fmat(0x05080b),14);
addF(fodTM,polyGeo([[-4.5,-1.5],[-1.5,-4],[3.5,-3],[5,1],[1.5,4.2],[-3.5,3]]),fmat(0xffc27a),15,0.01);
function placeFodT(t){
  /* window.FODT=[[t0,t1,hold,f0]]: flies from the exhaust valve (t0) to the turbine wheel (t1); with hold it lies in the manifold at fraction f0 from that time on */
  let cur=null;for(const q of (window.FODT||[]))if(t>=(q[2]!==undefined?q[2]:q[0])&&t<q[1])cur=q;
  fodTG.visible=!!cur;if(!cur)return;
  const k=clamp((t-cur[0])/(cur[1]-cur[0]),0,1),f0=cur[3]||0,f=f0+(1-f0)*(0.5*k+0.5*k*k);
  fodTPath.at(f*fodTPath.len,_v);fodTG.position.set(_v.x,_v.y-(cur[2]!==undefined?7*(1-sst(0,0.2,k)):0),_v.z+1.5);fodTM.rotation.z=f*26;
}
/* ---- bursts of sparks and chips at the wheels ---- */
const BUR=[];for(let i=0;i<260;i++)BUR.push({a:rnd()*TAU,v:0.35+0.65*rnd(),r:rnd(),chip:i%4===0,sz:0.8+0.8*rnd()});
const burPts=ptsFront(560,{add:true,max:14,soft:0.8,order:16}),burChip=ptsFront(160,{max:14,soft:0.25,order:16});
const CHIP_C=new T.Color(0.86,0.89,0.93),CHIP_T=new T.Color(0.62,0.55,0.5);
function burst(k,x0,y0,yoff,ysp,dirx,chipCol,ylim){
  if(k<0||k>=1)return;
  for(const q of BUR){const tt=k/(0.45+0.55*q.v);if(tt>1)continue;
    const vx=dirx*(26+84*q.v)*(0.35+0.65*Math.abs(Math.cos(q.a)))+16*Math.cos(q.a),vy=Math.sin(q.a)*(26+60*q.v);
    _v.set(x0+vx*tt*0.9,clamp(y0+(q.r<0.5?-1:1)*yoff+(q.r-0.5)*ysp+vy*tt*0.9-60*tt*tt,y0-ylim,y0+ylim),1.2);
    if(q.chip)burChip.push(_v,chipCol,(1-tt*tt)*0.95,1.7*q.sz);
    else{_c.copy(SP_C).lerp(SP_H,tt);burPts.push(_v,_c,(1-tt)*0.95,1.25*q.sz);}
  }
}
/* ---- sand and dust drawn in with the air (through a torn filter, or through a cracked hose after the filter) ---- */
const SAND=[];for(let i=0;i<420;i++)SAND.push({ph:rnd(),a:rnd(),y:rnd()*2-1,sz:0.7+0.6*rnd(),b:i%3===0,sp:0.7+0.6*rnd()});
const sandPts=ptsFront(420,{max:10,soft:0.35,order:9});const SAND_C=new T.Color(0.90,0.72,0.42);
const sandBPath=polyPath([[-143,TY+78,1],[-149,TY+44,1],[-151,TY+23,1],[-146,TY+12,1],[-128,TY+8,1],[-101,TY+10,1]]);
function drawSand(t){
  sandPts.begin();const cc=FX.sandMetal>0.5?CHIP_C:SAND_C;
  if(FX.sand>0.01||FX.sandB>0.01)for(const q of SAND){
    let u,al;
    if(q.b){if(q.a>FX.sandB)continue;u=(q.ph+t*0.5*q.sp)%1;sandBPath.at(u*sandBPath.len,_v);_v.x+=q.y*(u<0.3?5*(1-u/0.3)+1.2:1.5);_v.y+=q.y*5*sst(0.4,0.8,u);al=sst(0,0.08,u);}
    else{if(q.a>FX.sand)continue;u=(q.ph+t*0.42*q.sp)%1;const x=lerp(-262,-99,u);_v.set(x,TY+q.y*(x<-232?10+16*sst(-262,-232,x):(x<-190?24-8*sst(-212,-190,x):15)),1);al=sst(0,0.1,u);}
    if(u>0.93){const k=(u-0.93)/0.07;_v.y+=(q.y<0?-1:1)*k*15;_v.x-=k*5;al*=1-k;}
    sandPts.push(_v,cc,0.95*al,1.5*q.sz);
  }
  sandPts.end();
}
/* torn / clogged air filter, cracked hose between the filter and the compressor, chips left in the intake and in the intercooler */
const afTear=new T.Group();afTear.position.set(-214,TY+3,30.9);scene.add(afTear);
(function(){const P=[[-5,-13],[1,-9],[-2,-4],[4,0],[-1,5],[5,11],[0,14],[-6,9],[-3,3],[-8,-2],[-4,-7]];
  const a=new T.Mesh(polyGeo(P.map(p=>[p[0]*1.25,p[1]*1.12])),flat(0xa58d57));afTear.add(a);const b=new T.Mesh(polyGeo(P),flat(0x030507));b.position.z=0.05;afTear.add(b);})();
const afGroup=turbo.children.find(c=>c.isGroup&&c.children.length===13&&c.children[0].material===M.filter);
const afDirt=new T.Group();scene.add(afDirt);
(function(){const m1=flat(0x3a2a18),m2=flat(0x1e150c);for(let i=0;i<90;i++){const x=-230+38*hsh(i),dy=-27+54*hsh(i+40);
  const m=new T.Mesh(new T.CircleGeometry(1.8+3.4*hsh(i+80),9),i%3?m1:m2);m.position.set(x,TY+dy,Math.sqrt(900-dy*dy)+0.5+0.004*i);m.userData.k=hsh(i+120)*0.85;afDirt.add(m);}})();
const ductCrack=new T.Mesh(polyGeo([[-154,18.4],[-150.6,20.2],[-152.4,22],[-149,23.6],[-150.8,25.6],[-147.6,25.6],[-146.4,23.2],[-149,21.6],[-147.4,19.8],[-149.6,18.4]]),flat(0x030507));
ductCrack.position.z=0.06;turbo.add(ductCrack);
const CHP=[];for(let i=0;i<90;i++)CHP.push({x:rnd(),y:rnd(),k:i%2,sz:0.9+0.9*rnd(),ph:rnd()*TAU});
const chpPts=ptsFront(90,{max:12,soft:0.2,order:9});
function drawChips(t){
  chpPts.begin();
  if(FX.chips>0.01)for(const q of CHP){if(q.x>FX.chips*1.2&&q.k)continue;
    if(q.k)_v.set(-285+38*q.x,101.5+5*q.y*q.y,0.8);else _v.set(-186+70*q.x,TY-18.2+2.6*q.y*q.y,0.8);
    _c.copy(CHIP_C).multiplyScalar(0.78+0.22*Math.sin(t*3+q.ph));chpPts.push(_v,_c,0.95*clamp(FX.chips*2,0,1),1.5*q.sz);}
  chpPts.end();
}
/* ---- damaged blades (geometry swap) and radial growth of the compressor wheel at overspeed ---- */
const cWheel=rotC.children.slice(0,13),cBlades=rotC.children.slice(1,13),tBlades=rotT.children.slice(1,12);
const cTipD=s=>{const t=cTip(s),h=cHub(s),k=1-sst(0.08,0.46,s);return [t[0],lerp(t[1],h[1]+(t[1]-h[1])*0.3,k)];};
const cThB=(s,q)=>cTh(s,q)+0.6*q*(1-sst(0,0.45,s));
const cGeo0=cBlades[0].geometry,cGeoD=[bladeGeo(cHub,cTipD,cTh,0.06,0.9),bladeGeo(cHub,cTip,cThB,0,0.9)];
const tGeo0=tBlades[0].geometry,tGeoD=[bladeGeo(tHub,tTip,tTh,0.2,1.1),bladeGeo(tHub,tTip,tTh,0.12,1.1)];
/* ---- cracks: turbine housing (static) and turbine wheel (rotating) ---- */
const crackG=new T.Group();turbo.add(crackG);
(function(){const hot=fmat(0xffd98a),dark=fmat(0x120a06);
  const lines=[[[59.5,31.5],[62.6,35.5],[60.6,39.5],[63.8,43.5],[62,47.5],[65,51.5],[63.4,56],[66.6,60],[65,64.5]],
    [[84,-27.2],[88,-30.2],[92,-28],[96,-31.4],[100.5,-29],[104.5,-31.6]],
    [[58,-32],[61.2,-36],[59.4,-40],[62.6,-43.6],[61,-48],[64.6,-51.6]]];
  lines.forEach((L,li)=>{for(let i=0;i<L.length-1;i++){const seg=[L[i],L[i+1]],k=(li*0.16+i/(L.length-1)*0.62);
    const a=addF(crackG,ribbon(seg,1.25,0.3,0),dark,10);a.userData.k=k;const b=addF(crackG,ribbon(seg,0.5,0.32,0),hot,11);b.userData.k=k;}});})();
const crackWMat=new T.MeshBasicMaterial({color:0xffcf7a,toneMapped:false,transparent:true,opacity:0});
[0,2.2,4.3].forEach(b=>{const pts=[];for(let i=0;i<=16;i++){const s=0.06+0.7*i/16,h=tHub(s),r=h[1]+0.35,th=b+0.14*Math.sin(i*1.9)+0.25*s;pts.push(new T.Vector3(h[0],r*Math.sin(th),-r*Math.cos(th)));}
  rotT.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts),40,0.42,6,false),crackWMat));});
/* ---- magnifier insets: variable-geometry ring seen from the front (kind 0), back face of the compressor wheel (kind 1) ---- */
const INS=[{x:66,y:TY+140,r:54,to:[59,TY+33]},{x:-20,y:TY+136,r:50,to:[-70,TY+17]}];
const insG=INS.map(I=>{const g=new T.Group();g.position.set(I.x,I.y,2);g.visible=false;scene.add(g);
  const dx=I.to[0]-I.x,dy=I.to[1]-I.y,a=Math.atan2(dy,dx),p1=[I.r*Math.cos(a+1.05),I.r*Math.sin(a+1.05)],p2=[I.r*Math.cos(a-1.05),I.r*Math.sin(a-1.05)];
  addF(g,polyGeo([p1,p2,[dx,dy]]),fmat(0xffffff,{opacity:0.10}),18);
  addF(g,ribbon([p1,[dx,dy]],0.35,0,0),fmat(0xffd21f,{opacity:0.8}),18);addF(g,ribbon([p2,[dx,dy]],0.35,0,0),fmat(0xffd21f,{opacity:0.8}),18);
  addF(g,new T.CircleGeometry(I.r,72),fmat(0x0b1016),19);addF(g,new T.RingGeometry(I.r,I.r+1.8,72),fmat(0xffd21f),19);return g;});
const VG={n:11,rp:33,vanes:[],wheel:new T.Group(),soot:new T.Group(),mat:fmat(0xc3cad1)};
(function(){const g=insG[0],R0=INS[0].r;
  addF(g,new T.RingGeometry(46,R0-1,72),fmat(0x6a5c50),20);
  addF(VG.wheel,new T.CircleGeometry(22,48),fmat(0x1a1613),20);
  for(let k=0;k<11;k++){const pts=[];for(let i=0;i<=10;i++){const r=7+14.4*i/10,a=k*TAU/11+0.8*Math.pow(i/10,1.2);pts.push([r*Math.cos(a),r*Math.sin(a)]);}addF(VG.wheel,ribbon(pts,1.15,0,0),fmat(0xa59a92),21);}
  addF(VG.wheel,new T.CircleGeometry(7.6,32),fmat(0x8a8079),21);addF(VG.wheel,polyGeo(ngon(3.2,6,0.2)),fmat(0xcfd5dc),22);g.add(VG.wheel);
  const vg=polyGeo([[-9.4,0],[-4.5,1.9],[3,1.6],[9.4,0],[3,-1.2],[-4.5,-1.4]]);
  for(let k=0;k<VG.n;k++){const a=k*TAU/VG.n,m=addF(g,vg,VG.mat,22);m.position.set(VG.rp*Math.cos(a),VG.rp*Math.sin(a),0);m.userData.a=a;VG.vanes.push(m);
    const d=addF(g,new T.CircleGeometry(1.5,10),fmat(0x15181c),23);d.position.copy(m.position);}
  g.add(VG.soot);const m1=fmat(0x0b0806),m2=fmat(0x241a10);
  for(let i=0;i<70;i++){const r=25+20*hsh(i+3),a=TAU*hsh(i+31),m=addF(VG.soot,new T.CircleGeometry(1.1+2.3*hsh(i+60),9),i%3?m1:m2,24);m.position.set(r*Math.cos(a),r*Math.sin(a),0);m.userData.k=hsh(i+90)*0.8;}
})();
const VGP=[];for(let i=0;i<260;i++)VGP.push({a:rnd()*TAU,ph:rnd(),sz:0.8+0.6*rnd(),j:rnd()*2-1,q:rnd()});
const vgPts=ptsFront(260,{max:16,soft:1.1,order:21});
const VANE_C=new T.Color(),VANE_C0=col(0xc3cad1),VANE_C1=col(0x33291f);
const BENT=[0,0,0.85,0,0,0,-0.7,0,0,0.6,0];
function drawVgt(t,spin){
  vgPts.begin();if(!insG[0].visible){vgPts.end();return;}
  const pos=clamp(FX.vgtPos,0,1),del=lerp(0.2,0.95,pos);
  VG.vanes.forEach((m,k)=>{m.rotation.z=m.userData.a+Math.PI/2+del+BENT[k]*FX.vgtBent+0.035*FX.vgtJit*Math.sin(t*23+k);});
  VG.mat.color.copy(VANE_C.copy(VANE_C0).lerp(VANE_C1,FX.vgtSoot*0.85));growSet(VG.soot,FX.vgtSoot,0.7);VG.wheel.rotation.z=spin;
  const it=1/Math.tan(lerp(0.3,0.95,pos)),rate=lerp(1.25,0.6,pos),g=clamp(FX.gas,0,1);
  for(const q of VGP){if(q.q>g)continue;const u=(q.ph+t*rate*0.5)%1,r=lerp(50,9,u),th=q.a+Math.log(50/Math.max(r,22))*it+(r<22?(22-r)*0.07:0);
    _v.set(INS[0].x+(r+q.j*1.2)*Math.cos(th),INS[0].y+(r+q.j*1.2)*Math.sin(th),2.2);
    _c.copy(GAS_HOT).lerp(GAS_MID,sst(0.5,1,u));vgPts.push(_v,_c,0.85*sst(0,0.08,u)*(1-sst(0.82,1,u))*FX.inset,1.9*q.sz);}
  vgPts.end();
}
const PEEL={};
(function(){const g=insG[1];
  PEEL.disc=new T.Group();g.add(PEEL.disc);
  addF(PEEL.disc,new T.CircleGeometry(40,72),fmat(0xc6ced6),20);[13,22,31].forEach(r=>addF(PEEL.disc,new T.RingGeometry(r,r+0.45,72),fmat(0xa3acb5),21));
  const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d');
  for(let i=0;i<2600;i++){const a=TAU*hsh(i+5),r=Math.sqrt(hsh(i+1700))*250,px=256+r*Math.cos(a),py=256+r*Math.sin(a),s=4+6*hsh(i+900);
    let gr=x.createRadialGradient(px,py,0,px,py,s);gr.addColorStop(0,'rgba(52,58,66,0.62)');gr.addColorStop(1,'rgba(52,58,66,0)');x.fillStyle=gr;x.beginPath();x.arc(px,py,s,0,TAU);x.fill();
    gr=x.createRadialGradient(px-s*0.45,py-s*0.45,0,px-s*0.45,py-s*0.45,s*0.5);gr.addColorStop(0,'rgba(255,255,255,0.42)');gr.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=gr;x.beginPath();x.arc(px-s*0.45,py-s*0.45,s*0.5,0,TAU);x.fill();}
  PEEL.tex=addF(PEEL.disc,new T.CircleGeometry(40,72),new T.MeshBasicMaterial({map:new T.CanvasTexture(c),transparent:true,opacity:0,depthTest:false,toneMapped:false}),22);
  addF(PEEL.disc,new T.CircleGeometry(6.4,32),fmat(0x8f969e),23);addF(PEEL.disc,new T.CircleGeometry(4.3,32),fmat(0x15181c),23);
})();
/* ---- particle filter (or catalyst / silencer) after the turbine, in section ---- */
const dpfG=new T.Group();dpfG.visible=false;turbo.add(dpfG);
const DPFB={x0:194,x1:282,r:39,brick:null,soot:null};
(function(){const wall=cut(0x8a949e,HA),z=0.05;
  const half=[[[150,22.2],[170,22.2],[170,27],[150,27]],[[170,22.2],[188,42],[188,46.8],[170,27]],[[188,42],[288,42],[288,46.8],[188,46.8]],[[288,42],[306,22.2],[306,27],[288,46.8]],[[306,22.2],[344,22.2],[344,27],[306,27]]];
  const back=new T.Mesh(polyGeo([[150,-22.2],[170,-22.2],[188,-42],[288,-42],[306,-22.2],[344,-22.2],[344,22.2],[306,22.2],[288,42],[188,42],[170,22.2],[150,22.2]]),flat(0x2a231d));back.position.z=-0.6;dpfG.add(back);
  [1,-1].forEach(s=>half.forEach(P=>{const pts=P.map(p=>[p[0],s*p[1]]);if(s<0)pts.reverse();const g=polyGeo(pts);const m=new T.Mesh(g,wall);m.position.z=z;dpfG.add(m);edges(dpfG,g,z+0.01);}));
  const c=document.createElement('canvas');c.width=352;c.height=320;const x=c.getContext('2d');x.fillStyle='#d9ccb4';x.fillRect(0,0,352,320);
  for(let i=0;i<16;i++){x.fillStyle='#4b4239';x.fillRect(0,i*20+3,352,14);x.fillStyle='#d9ccb4';if(i%2)x.fillRect(0,i*20+3,18,14);else x.fillRect(334,i*20+3,18,14);}
  const B=DPFB,bg=polyGeo([[B.x0,-B.r],[B.x1,-B.r],[B.x1,B.r],[B.x0,B.r]]),uv=bg.attributes.uv,P=bg.attributes.position;for(let i=0;i<P.count;i++)uv.setXY(i,(P.getX(i)-B.x0)/(B.x1-B.x0),(P.getY(i)+B.r)/(2*B.r));
  B.brick=new T.Mesh(bg,new T.MeshBasicMaterial({map:new T.CanvasTexture(c),toneMapped:false,side:T.DoubleSide}));B.brick.position.z=-0.3;dpfG.add(B.brick);
  B.soot=new T.Mesh(polyGeo([[0,-B.r],[1,-B.r],[1,B.r],[0,B.r]]),flat(0x0a0705,{transparent:true,opacity:0.82}));B.soot.position.set(B.x0,0,-0.25);dpfG.add(B.soot);
})();
const DPP=[];for(let i=0;i<620;i++)DPP.push({ph:rnd(),y:rnd()*2-1,q:rnd(),sz:0.8+0.6*rnd(),j:rnd()*2-1,row:Math.floor(rnd()*8)});
const dpPts=ptsFront(620,{max:22,soft:1.3,order:6});const GAS_CLEAN=new T.Color(0.74,0.80,0.86);
function drawDpf(t){
  dpPts.begin();dpfG.visible=FX.showDpf>0.5;if(!dpfG.visible){dpPts.end();return;}
  const B=DPFB,cl=clamp(FX.dpfClog,0,1);
  B.brick.material.color.setRGB(1,1,1).lerp(_c.setRGB(0.3,0.26,0.22),cl);B.soot.scale.x=Math.max(0.01,(B.x1-B.x0)*(0.06+0.9*cl));B.soot.material.opacity=0.2+0.66*cl;
  for(const q of DPP){
    if(q.q<cl*0.93){   /* held back in front of the brick: a dense, hot, slow cloud between the wheel and the filter */
      const x=lerp(90,B.x0-1,Math.pow(q.ph,0.75))+2.2*Math.sin(t*5+q.ph*40),hw=x<150?19:(x<170?19:lerp(19,38,(x-170)/18));
      _v.set(x,TY+q.y*hw+1.6*Math.cos(t*4+q.ph*31),0.9);_c.copy(GAS_HOT);dpPts.push(_v,_c,0.6,3.4*q.sz);continue;}
    const u=(q.ph+t*lerp(0.36,0.14,cl))%1,x=lerp(96,344,u);let y;
    if(x<170)y=q.y*19;else if(x<188)y=q.y*lerp(19,38,(x-170)/18);else if(x<B.x0)y=q.y*38;else if(x<B.x1)y=((q.row*2+(x<B.x0+8?0:1))-7.5)*(B.r/8);else if(x<288)y=((q.row*2+1)-7.5)*(B.r/8);else if(x<306)y=q.y*lerp(38,19,(x-288)/18);else y=q.y*19;
    _v.set(x,TY+y+q.j*0.8,0.9);
    if(x<B.x0)_c.copy(GAS_MID).lerp(GAS_OUT,sst(96,B.x0,x));else _c.copy(GAS_OUT).lerp(GAS_CLEAN,sst(B.x0,B.x1,x));
    dpPts.push(_v,_c,0.55*sst(0,0.05,u)*(1-sst(0.94,1,u)),(x>B.x0?1.9:2.6)*q.sz);
  }
  dpPts.end();
}
/* ---- hot gas pushed past the turbine-side seal ring into the bearing housing ---- */
const gasInPaths=[1,-1].map(s=>polyPath([[66,TY+s*30,0.7],[58,TY+s*27,0.7],[54.4,TY+s*20,0.7],[52.6,TY+s*8.2,0.7],[45,TY+s*7.3,0.7],[38,TY+s*7.6,0.7],[30,TY+s*9.6,0.7],[16,TY+s*11,0.7],[0,TY+s*11.4,0.7]]));
const GIN=[];for(let i=0;i<220;i++)GIN.push({k:i%2,ph:rnd(),a:rnd(),sz:0.8+0.6*rnd(),j:rnd()*2-1});
const ginPts=ptsFront(220,{max:16,soft:1.0,order:8});
/* ---- leaks: boost hose (air jet), exhaust manifold / missing gasket (hot gas jet) ---- */
const JET=[];for(let i=0;i<360;i++)JET.push({k:i%2,ph:rnd(),a:rnd(),ang:rnd()*2-1,sz:0.8+0.8*rnd(),sp:0.6+0.8*rnd()});
const jetPts=ptsFront(360,{max:22,soft:1.2,order:9});const JET_AIR=new T.Color(0.80,0.92,1.0);
const HOSE_X=-279,HOSE_Y=248,MAN_X=-84,MAN_Y=44;
const hoseCrack=new T.Mesh(polyGeo([[-282,240],[-279.2,243],[-281,246],[-278.4,249],[-280.4,252],[-277.6,256],[-276.6,252.4],[-278.2,249.4],[-276.4,246],[-278,243],[-276.6,240]]),fmat(0x030507));hoseCrack.renderOrder=9;hoseCrack.position.z=0.3;scene.add(hoseCrack);
const manCrack=new T.Mesh(polyGeo([[-87.5,41.2],[-84.6,43],[-86,45],[-83.2,46.6],[-80.6,45.4],[-82.4,43.4],[-80.4,41.6]]),fmat(0x030507));manCrack.renderOrder=9;manCrack.position.z=0.3;scene.add(manCrack);
const manSoot=new T.Group();scene.add(manSoot);
(function(){const m=fmat(0x0b0806,{opacity:0.85});for(let i=0;i<26;i++){const c=addF(manSoot,new T.CircleGeometry(1.4+2.6*hsh(i+7),9),m,8);c.position.set(MAN_X-6+18*hsh(i+20),MAN_Y+2+16*hsh(i+50),0.25);c.userData.k=hsh(i+70)*0.8;}})();
function drawJets(t){
  jetPts.begin();ginPts.begin();
  hoseCrack.visible=FX.hoseLeak>0.02;manCrack.visible=FX.manLeak>0.02;growSet(manSoot,FX.manLeak,0.6);
  for(const q of JET){
    if(q.k===0){if(q.a>FX.hoseLeak)continue;const u=(q.ph+t*1.1*q.sp)%1,an=Math.PI+0.22+q.ang*0.6,d=3+70*u;
      _v.set(HOSE_X+d*Math.cos(an),HOSE_Y+d*Math.sin(an)+8*u*u,0.9);jetPts.push(_v,JET_AIR,0.75*sst(0,0.06,u)*(1-u),(1.6+4.5*u)*q.sz);}
    else{if(q.a>FX.manLeak)continue;const u=(q.ph+t*1.0*q.sp)%1,an=1.75+q.ang*0.5,d=2+62*u;
      _v.set(MAN_X+d*Math.cos(an),MAN_Y+d*Math.sin(an),0.9);_c.copy(GAS_HOT).lerp(GAS_OUT,u);jetPts.push(_v,_c,0.8*sst(0,0.06,u)*(1-u),(1.8+5*u)*q.sz);}
  }
  if(FX.gasIn>0.01)for(const q of GIN){if(q.a>FX.gasIn)continue;const p=gasInPaths[q.k],u=(q.ph+t*0.3)%1;p.at(u*p.len,_v);_v.x+=q.j*0.6;_v.y+=q.j*0.6;
    ginPts.push(_v,GAS_HOT,0.9*sst(0,0.08,u)*(1-sst(0.85,1,u)),1.7*q.sz);}
  jetPts.end();ginPts.end();
}
/* ---- silicone squeezed into the oil inlet (sealant on the oil flange) ---- */
const silG=new T.Group();turbo.add(silG);
(function(){const m1=fmat(0xeef2f5),m2=fmat(0xcfd6dd);
  const P=[[-6.2,44.4,2.3],[-5.2,43.2,1.9],[-4.4,44.8,1.7],[0.2,44.2,2.3],[-0.8,43.4,1.8],[-1.5,44.9,1.6],[-4.6,41.6,1.5],[-1.4,41.9,1.4],[-3.9,40.2,1.2],[-2.2,40.6,1.1],[-3.6,45.6,1.4],[-2.5,45.7,1.3],[-5.6,46.4,1.5],[-0.4,46.3,1.5],[-3.2,38.9,1.0]];
  P.forEach((p,i)=>{const c=addF(silG,new T.CircleGeometry(p[2],12),i%3?m1:m2,10);c.position.set(p[0],p[1],0.2+0.002*i);c.userData.k=i/P.length*0.8;});})();
/* ---- read-out panel: a bar with a limit mark (speed of the turbine, temperature of the gas) ---- */
let gaugeEl=null;
function drawGauge(t){
  const G=window.GAUGE;if(!G)return;
  if(!gaugeEl){gaugeEl=document.createElement('div');gaugeEl.id='yy';gaugeEl.style.top='372px';gaugeEl.style.height='172px';
    gaugeEl.innerHTML='<div class="tl"></div><div class="th"></div><div class="tv" style="font-size:66px;top:22px"></div><div class="tb"><i></i><b></b></div>';
    document.getElementById('stage').appendChild(gaugeEl);gaugeEl.children[0].textContent=G.title;}
  const o=G.vis(t);gaugeEl.style.opacity=o.toFixed(3);if(o<0.01)return;
  const v=G.val(t),st=G.state?G.state(v):{hot:v>1.0,sub:v>1.0?G.over:G.sub,txt:v>1.0?G.hotTxt:G.okTxt};gaugeEl.className=st.hot?'hot':'';
  gaugeEl.children[1].textContent=st.sub;gaugeEl.children[2].textContent=st.txt;
  gaugeEl.children[3].firstChild.style.width=(clamp(v/1.25,0,1)*100).toFixed(1)+'%';
}

function applyFX2(t,U,crown){
  const spin=arr(SA,t);
  placeFod(t);placeFodT(t);drawSand(t);drawChips(t);drawJets(t);drawDpf(t);
  burPts.begin();burChip.begin();burst(hitK(window.HITC,t),-104,TY,0,30,-1,CHIP_C,17.5);burst(hitK(window.HITT,t),59,TY,29,5,1,CHIP_T,90);burPts.end();burChip.end();
  if(afGroup)afGroup.visible=FX.afHide<0.5;afTear.visible=FX.afTorn>0.02;afTear.scale.setScalar(0.3+0.7*clamp(FX.afTorn,0,1));growSet(afDirt,FX.afClog,0.7);ductCrack.visible=FX.sandB>0.01;
  const cd=FX.chipC>0.5;cBlades[0].geometry=cd?cGeoD[0]:cGeo0;cBlades[4].geometry=cd?cGeoD[1]:cGeo0;cBlades[6].geometry=cd?cGeoD[0]:cGeo0;
  const td=FX.chipT>0.5;[0,3,4,7,9].forEach((k,i)=>{tBlades[k].geometry=td?tGeoD[i%2]:tGeo0;});
  const gs=1+0.06*FX.grow;cWheel.forEach(m=>m.scale.set(1,gs,gs));
  growSet(crackG,FX.crack,0.9);crackWMat.opacity=clamp(FX.crackW,0,1);growSet(silG,FX.sil,0.7);
  const ik=clamp(Math.round(FX.insetKind),0,1);insG.forEach((g,i)=>{g.visible=i===ik&&FX.inset>0.02;if(g.visible)g.scale.setScalar(0.6+0.4*sst(0,1,FX.inset));});
  drawVgt(t,spin*0.5);
  PEEL.tex.material.opacity=clamp(FX.peel,0,1);PEEL.disc.scale.setScalar(1+0.07*FX.grow);
  if(FX.gasHot>0.01){const eP=exPts.P,eC=exPts.C,eS=exPts.S,eA=exPts.A,ne=exPts.g.drawRange.count,k=FX.gasHot*0.85;
    for(let i=0;i<ne;i++){eC[i*3]=lerp(eC[i*3],1.0,k);eC[i*3+1]=lerp(eC[i*3+1],0.93,k);eC[i*3+2]=lerp(eC[i*3+2],0.66,k);eS[i]*=1+0.4*FX.gasHot;eA[i]=Math.min(1,eA[i]*(1+0.7*FX.gasHot));}}
  if(FX.sootGas>0.01){const eC=exPts.C,eS=exPts.S,eA=exPts.A,ne=exPts.g.drawRange.count,k=FX.sootGas*0.85;
    for(let i=0;i<ne;i++){eC[i*3]=lerp(eC[i*3],0.07,k);eC[i*3+1]=lerp(eC[i*3+1],0.06,k);eC[i*3+2]=lerp(eC[i*3+2],0.05,k);eS[i]*=1+0.35*FX.sootGas;eA[i]=Math.min(1,eA[i]*(1+0.9*FX.sootGas));}}
  drawGauge(t);
}
