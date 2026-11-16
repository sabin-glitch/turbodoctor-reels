/* reel v2: stream 1 with (a) the part that runs inside the recirculation loop faded out while the loop is drawn by
   stream 4 and (b) an x-ray copy for the pressure pipe behind the section plane, shown while the diverter is fitted */
const s1X=makePts(N1,{max:24,soft:1.3,order:3});s1X.mat.depthTest=false;
function drawS1(G,S){
  s1Pts.begin();s1X.begin();const back=clamp(-S.v1/120,0,1),xr=S.dvOn?1:0;
  for(const p of s1){
    const d=((G+p.e)%p.per+p.per)%p.per;if(d>p.L5)continue;
    const prog=airPos(p,d,_v);if(_v.z>3)continue;
    let a=0.44*(1-sst(0.5,3,_v.z))*sst(0,10,d)*(1-sst(p.L5-5,p.L5,d));
    if(S.rec>0.01&&d>DJ-8&&d<p.L4+D_DVT+8)a*=1-S.rec;
    if(prog<0.2)_c.copy(AIR_C);else if(prog<0.4)_c.copy(AIR_C).lerp(AIR_W,(prog-0.2)/0.2);else{_c.copy(AIR_W);if(prog>0.45&&_v.x<-240&&_v.y<228)_c.lerp(AIR_C,clamp((228-_v.y)/70,0,1));}
    if(back>0)_c.lerp(WARN_C,back*0.85);
    const al=Math.min(0.9,a*(1+0.8*back)),sz=2.4*p.sz*(1+0.35*back);
    s1Pts.push(_v,_c,al,sz);
    if(xr&&_v.z<-12&&d>=p.L3+(TAU-p.pe)*58)s1X.push(_v,_c,al*0.5*sst(TY+66,TY+80,_v.y),sz);
  }
  s1Pts.end();s1X.end();
}
