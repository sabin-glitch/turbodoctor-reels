/* --- air, as three streams: (1) filter -> compressor -> pipe up to the blow-off tap,
       (2) tap -> intercooler -> throttle -> port -> cylinder, (3) tap -> blow-off -> atmosphere --- */
const INP=(function(){const pts=INT.path.P.slice();PORTPTS.in.slice().reverse().forEach((p,i)=>{if(i>0)pts.push(p);});pts.push(new T.Vector3(EX-XV,-6,0));return polyPath(pts);})();
function nearestD(x,y){let best=0,bd=1e9;for(let d=0;d<INP.len;d+=0.5){INP.at(d,_v);const e=Math.abs(_v.x-x)+Math.abs(_v.y-y)+Math.abs(_v.z);if(e<bd){bd=e;best=d;}}return best;}
const D_TAP=nearestD(PIPE_X,BOV_Y),D_THR=nearestD(PIPE_X,THR_Y);
const WARN_C=new T.Color(1.0,0.3,0.22);
const N1=1100,s1=[];
for(let i=0;i<N1;i++){s1.push({e:rnd()*4000,psi:rnd()*TAU,ri:2+14*Math.sqrt(rnd()),j:[rnd()*2-1,rnd()*2-1,rnd()],q:rnd(),sz:0.8+0.6*rnd()});}
s1.forEach(p=>{p.L1=100;p.L2=p.L1+40;p.L3=p.L2+22;p.pe=((p.psi+1.6)%TAU);p.L4=p.L3+(TAU-p.pe)*58+CV.outlet;p.L5=p.L4+D_TAP;p.per=p.L5+60;});
const s1Pts=makePts(N1,{max:26,soft:1.3});
function airPos(p,d,out){
  if(d<p.L1){const k=d/p.L1;turboPt(-200+k*100,p.ri,p.psi+0.2*k,out);return 0;}
  if(d<p.L2){const s=(d-p.L1)/40,h=cHub(s),t=cTip(s),q=clamp((p.ri-7)/13,0,1)*0.8+0.1;turboPt(lerp(h[0],t[0],q),lerp(h[1],t[1],q),p.psi+0.2+1.1*s,out);return 0.2*s;}
  if(d<p.L3){const k=(d-p.L2)/22;turboPt(lerp(-74,CV.a0+3,k),lerp(29,CV.r(p.pe)-CV.rho(p.pe)*0.5,k),p.psi+1.3+0.3*k,out);return 0.2+0.2*k;}
  if(d<p.L4){
    const sd=d-p.L3,spiral=(TAU-p.pe)*58;
    if(sd<spiral){const ph=p.pe+sd/58,rho=CV.rho(ph)*0.7;turboPt(CV.a0+p.j[0]*rho,CV.r(ph)+p.j[1]*rho,ph,out);}
    else{const y=sd-spiral,rho=CV.rho(TAU)*0.7;out.set(CV.a0+p.j[0]*rho,TY+y,-CV.r(TAU)+p.j[1]*rho);}
    return 0.4;
  }
  INP.at(d-p.L4,out);const rr=10;out.x+=p.j[0]*rr*0.7;out.y+=p.j[1]*rr*0.7;out.z-=p.j[2]*rr*0.6;
  return 0.5;
}
function drawS1(G,S){
  s1Pts.begin();const back=clamp(-S.v1/120,0,1);
  for(const p of s1){
    const d=((G+p.e)%p.per+p.per)%p.per;if(d>p.L5)continue;
    const prog=airPos(p,d,_v);if(_v.z>3)continue;
    const a=0.44*(1-sst(0.5,3,_v.z))*sst(0,10,d)*(1-sst(p.L5-5,p.L5,d));
    if(prog<0.2)_c.copy(AIR_C);else if(prog<0.4)_c.copy(AIR_C).lerp(AIR_W,(prog-0.2)/0.2);else{_c.copy(AIR_W);if(prog>0.45&&_v.x<-240&&_v.y<228)_c.lerp(AIR_C,clamp((228-_v.y)/70,0,1));}
    if(back>0)_c.lerp(WARN_C,back*0.85);
    s1Pts.push(_v,_c,Math.min(0.9,a*(1+0.8*back)),2.4*p.sz*(1+0.35*back));
  }
  s1Pts.end();
}
const N2=420,s2=[],L2S=INP.len-D_TAP,PER2=L2S+40;
for(let i=0;i<N2;i++)s2.push({e:rnd()*PER2,j:[rnd()*2-1,rnd()*2-1,rnd()],sz:0.8+0.6*rnd()});
const s2Pts=makePts(N2,{max:26,soft:1.3});
function drawS2(G){
  s2Pts.begin();
  for(const p of s2){
    const d=((G+p.e)%PER2+PER2)%PER2;if(d>L2S)continue;
    const D=D_TAP+d;INP.at(D,_v);const rr=D<D_THR+30?10:8;_v.x+=p.j[0]*rr*0.7;_v.y+=p.j[1]*rr*0.7;_v.z-=p.j[2]*rr*0.6;
    if(_v.z>3)continue;
    const a=0.44*(1-sst(0.5,3,_v.z))*sst(0,4,d)*(1-sst(L2S-30,L2S,d));
    _c.copy(AIR_C);
    s2Pts.push(_v,_c,a,2.4*p.sz);
  }
  s2Pts.end();
}
/* blow-off vent: world coordinates (the valve axis points to -X, outlet points down) */
const VENT=polyPath([[PIPE_X,BOV_Y,-1],[PIPE_X-14,BOV_Y,-1],[PIPE_X-20.5,BOV_Y-0.5,-1],[PIPE_X-24.5,BOV_Y-5,-1],[PIPE_X-27,BOV_Y-12,-1],[PIPE_X-BOV_OUT,BOV_Y-20,-1],[PIPE_X-BOV_OUT,BOV_Y-36,-1]].map(p=>new T.Vector3(p[0],p[1],p[2])));
const VENT_C=new T.Color().copy(AIR_C).lerp(new T.Color(1,1,1),0.5);
const VEXT=50,N3=480,s3=[],PER3=VENT.len+VEXT+20;
for(let i=0;i<N3;i++)s3.push({e:rnd()*PER3,j:[rnd()*2-1,rnd()*2-1,rnd()*2-1],sz:0.8+0.7*rnd(),sp:0.5+rnd()});
const s3Pts=makePts(N3,{max:30,soft:1.2});
function drawS3(G,S){
  s3Pts.begin();
  const vis=S.bovOn?S.vent:0;
  if(vis>0.01)for(const p of s3){
    const d=((G*p.sp+p.e)%PER3+PER3)%PER3;if(d>VENT.len+VEXT)continue;
    let a;
    if(d<VENT.len){VENT.at(d,_v);const rr=d<18?6.5:d<34?3.4:5;_v.x+=p.j[0]*rr*0.7;_v.y+=p.j[1]*rr*(d<18?0.9:0.4);_v.z+=-Math.abs(p.j[2])*rr*0.6;a=0.5;}
    else{const k=(d-VENT.len)/VEXT;_v.set(PIPE_X-BOV_OUT+p.j[0]*(5+30*k),BOV_Y-36-k*VEXT,p.j[2]*(4+26*k)-2);a=0.5*(1-k);}
    if(_v.z>2&&d<VENT.len)continue;
    _c.copy(VENT_C);
    s3Pts.push(_v,_c,a*vis*sst(0,6,d),2.6*p.sz);
  }
  s3Pts.end();
}
/* sparks where the compressor blades touch the housing */
const sparkPts=makePts(260,{max:14,soft:0.8,add:true,order:4});
const SPK_C=new T.Color(1.0,0.72,0.3),SPK_H=new T.Color(1,0.95,0.75);
function drawSparks(U,S){
  sparkPts.begin();
  if(S.spark>0.01)for(let i=0;i<260;i++){
    const life=0.42,age=((U*1.0+i*0.0137)%life+life)%life,seed=Math.floor((U+i*0.0137)/life)*977+i*31;
    const r1=((Math.sin(seed*12.9898)*43758.5453)%1+1)%1,r2=((Math.sin(seed*78.233)*24634.6345)%1+1)%1;
    const sg=i%2?1:-1,ph=sg*(Math.PI/2-0.35*r1),a0=-80+r2*5;turboPt(a0,27.6,ph,_v);
    const ty=Math.cos(ph),tz=Math.sin(ph),sp=70+90*r2;
    _v.x+=(-25-40*r1)*age;_v.y+=(ty*sp+sg*40)*age-90*age*age;_v.z+=tz*sp*age*0.5;
    if(_v.z>8)continue;
    _c.copy(SPK_H).lerp(SPK_C,age/life);
    sparkPts.push(_v,_c,S.spark*(1-age/life),2.0);
  }
  sparkPts.end();
}
/* flow-direction chevrons in the compressor inlet duct: blue towards the wheel, red when the air comes back */
const chevs=[];
(function(){
  const g=new T.ShapeGeometry(new T.Shape([V2(-4.5,-7.5),V2(-0.8,-7.5),V2(4.8,0),V2(-0.8,7.5),V2(-4.5,7.5),V2(1.1,0)]));
  for(let i=0;i<3;i++){
    const grp=new T.Group();grp.position.set(0,TY,0.9);scene.add(grp);
    const o=new T.Mesh(g,new T.MeshBasicMaterial({color:0x070b10,transparent:true,opacity:0,depthWrite:false,toneMapped:false,side:T.DoubleSide}));o.scale.set(1.34,1.26,1);o.position.x=0.3;o.renderOrder=6;grp.add(o);
    const m=new T.Mesh(g,new T.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0,depthWrite:false,toneMapped:false,side:T.DoubleSide}));m.position.z=0.05;m.renderOrder=7;grp.add(m);
    chevs.push({grp,o,m});
  }
})();
const CH_X0=-196,CH_L=78;
const CHEV_F=new T.Color(0.30,0.70,1.0),CHEV_B=new T.Color(1.0,0.27,0.17);
function drawChev(G,S){
  const dir=S.v1>=0?1:-1,sp=Math.min(1,Math.abs(S.v1)/55);
  chevs.forEach((c,i)=>{
    const s=(((G*0.42+i*CH_L/3)%CH_L)+CH_L)%CH_L,a=sp*sst(0,9,s)*(1-sst(CH_L-9,CH_L,s));
    c.grp.position.x=CH_X0+s;c.grp.scale.x=dir;
    c.m.material.color.copy(dir>0?CHEV_F:CHEV_B);c.m.material.opacity=0.95*a;c.o.material.opacity=0.6*a;
  });
}
/* --- exhaust gas in the enlarged variable-geometry view (local coordinates of DG) --- */
const NEM=260,embers=[];
for(let i=0;i<NEM;i++){const turns=0.35+rnd()*0.9;embers.push({off:rnd(),turns,j:rnd()*2-1,sz:0.8+0.6*rnd(),vf:0.85+0.3*rnd(),per:178+turns*TAU*92+32+26});}
const _e=new T.Vector3();
function emPos(e,s,out,sw){
  const L1=178;
  if(s<L1){out.set(178-s,102+e.j*7,3);return 1;}
  s-=L1;const R0=102+e.j*6,ang=e.turns*TAU,L2=ang*92;
  if(s<L2){const q=s/L2,a=Math.PI/2+q*ang,r=lerp(R0,82,q);out.set(r*Math.cos(a),r*Math.sin(a),3);return 2;}
  s-=L2;const a0=Math.PI/2+ang,L3=32;
  if(s<L3){const q=s/L3,r=lerp(82,50,q),a=a0+sw*q;out.set(r*Math.cos(a),r*Math.sin(a),3);return 3;}
  s-=L3;const q=Math.min(1,s/26),r=lerp(50,24,q),a=a0+sw+0.9*q;out.set(r*Math.cos(a),r*Math.sin(a),3);return 4;
}
const emPts=makePts(NEM*4,{max:30,soft:1.0,add:true,order:5});
const EMB_C=new T.Color(1.0,0.5,0.16),EMB_F=new T.Color(1.0,0.84,0.5);
function drawEmbers(G,sc,S){
  emPts.begin();
  if(sc>0.01){
    const fast=clamp(1-S.vgt/0.55,0,1),sw=lerp(0.55,1.2,fast);   /* closed vanes: the gas enters the wheel faster and more tangentially */
    for(const e of embers){
      const s=(((G*1.9*e.vf+e.off*e.per)%e.per)+e.per)%e.per;
      const ph=emPos(e,s,_e,sw);
      _v.copy(_e).multiplyScalar(sc).add(DGP);
      const a=sst(0,14,s)*(ph===4?1-sst(0,1,(s-(e.per-26))/26):1);
      _c.copy(EMB_C);if(ph>=3)_c.lerp(EMB_F,0.7*fast);
      emPts.push(_v,_c,a,4.2*e.sz*sc);
      for(let q=1;q<=3;q++){emPos(e,Math.max(0,s-q*9),_e,sw);_w.copy(_e).multiplyScalar(sc).add(DGP);emPts.push(_w,_c,0.4*a/q,3.2*e.sz*sc);}
    }
  }
  emPts.end();
}
