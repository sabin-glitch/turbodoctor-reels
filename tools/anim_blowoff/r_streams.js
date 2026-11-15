/* --- reel v2, stream 4: the recirculation loop of the diverter valve (petrol, throttle closed, valve open):
       compressor inlet -> wheel -> scroll -> pressure pipe -> tap -> return hose -> valve -> back in front of the wheel --- */
const D_DVT=(function(){for(let d=0;d<INP.len;d+=0.5){INP.at(d,_v);if(_v.x<=DV_TAPX)return d;}return 120;})();
const DJ=90;                                                    /* the returned air joins the inlet stream again at x = -122 */
const RC=(function(){
  const hose=DVH_PTS.slice().reverse().map(p=>[p[0],p[1],p[2]]);hose[0][1]+=2;
  const L=(x,y)=>[DV_X+x,DV_Y+y,0];
  return curvePath(hose.concat([L(-15,21),L(-12,18.6),L(-8,17.2),L(-3.5,16),L(-0.5,13.2),L(0,6),L(0,-2),L(0.5,-7),L(4,-12.5),L(10,-17.5),L(16,-20.5)]),170).path;
})();
function rcD(x,y){let best=0,bd=1e9;for(let d=0;d<RC.len;d+=0.5){RC.at(d,_v);const e=Math.abs(_v.x-x)+Math.abs(_v.y-y);if(e<bd){bd=e;best=d;}}return best;}
const RC_V=rcD(DV_X-14,DV_Y+21),RC_S=rcD(DV_X-0.5,DV_Y+13.2);  /* into the valve chamber, down the stub */
const REC_C=new T.Color(0.37,0.88,0.81);
const N4=900,s4=[];
for(let i=0;i<N4;i++){
  const p={e:rnd(),psi:(rnd()-0.5)*2.6,ri:3+13*Math.sqrt(rnd()),j:[rnd()*2-1,rnd()*2-1,rnd()],sz:0.8+0.6*rnd()};
  p.L1=112;p.L2=p.L1+40;p.L3=p.L2+22;p.pe=((p.psi+1.6)%TAU+TAU)%TAU;p.L4=p.L3+(TAU-p.pe)*58+CV.outlet;
  p.LA=p.L4+D_DVT-DJ;p.per=p.LA+RC.len;p.a0=new T.Vector3();p.a1=new T.Vector3();airPos(p,DJ,p.a0);airPos(p,p.L4+D_DVT,p.a1);
  s4.push(p);
}
const s4Pts=makePts(N4,{max:26,soft:1.3}),s4X=makePts(N4,{max:24,soft:1.3,order:3});s4X.mat.depthTest=false;
function drawS4(G,S){
  s4Pts.begin();s4X.begin();
  if(S.rec>0.01)for(const p of s4){
    const s=((G+p.e*p.per)%p.per+p.per)%p.per;let a=0.62,hid=0;
    if(s<p.LA){
      const d=DJ+s;airPos(p,d,_v);
      if(d>=p.L4)hid=1;                                                             /* pressure pipe, behind the section plane */
      else if(d>=p.L3+(TAU-p.pe)*58){a*=sst(TY+66,TY+80,_v.y);hid=1;}              /* riser: shown only above the scroll */
      else if(_v.z>3)continue;else a*=1-sst(0.5,3,_v.z);
    }else{
      const b=s-p.LA;RC.at(b,_v);
      const inV=sst(RC_V-12,RC_V,b),rr=lerp(5.2,lerp(2.5,4.2,sst(RC_S-3,RC_S+5,b)),inV);
      _v.x+=p.j[0]*rr*0.7;_v.y+=p.j[1]*rr*lerp(0.7,0.55,inV);_v.z=lerp(_v.z-p.j[2]*rr*0.8,0.5+0.9*p.j[2],inV);
      if(b<14)_w.copy(_v),_v.copy(p.a1).lerp(_w,sst(0,14,b));
      if(b>RC.len-16)_v.lerp(p.a0,sst(RC.len-16,RC.len,b));
      hid=_v.z<-7.5?1:0;
    }
    (hid?s4X:s4Pts).push(_v,REC_C,a*S.rec*(hid?0.6:1),2.8*p.sz);
  }
  s4Pts.end();s4X.end();
}
