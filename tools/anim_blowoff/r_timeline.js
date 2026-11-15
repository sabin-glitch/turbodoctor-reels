/* ================= timeline (reel, in voice time) ================= */
/* K = anchors computed by build_reel.py from vo/cues.json (word starts of the voice-over), all in seconds of the reel.
   Phases:
   H  hook: diesel without blow-off, vanes stuck -> lift-off at K.H_LIFT, the surge bursts follow the hook sound (K.HE),
      then slow-motion pulses and the damage look
   P  petrol engine with blow-off: throttle closes at K.P_C, the valve lifts at K.P_L
   N  the diesel story, one continuous take: healthy lift-off (D_LIFT..D_ACC) -> how the vanes work (G_*) ->
      soot blocks them closed (C_*) -> overspeed and overboost (O_*) -> lift-off (L_LIFT) -> surge (S_ON) -> damage (X_*)
   S  split screen: top = petrol + blow-off, bottom = diesel in surge; both lift off at SP_C1 and SP_C2
   W  closing: surge once more, then the enlarged variable-geometry view */
const K=/*K*/{}/*K*/;
const T_P=K.T_P,T_D=K.T_D,T_S=K.T_S,T_W=K.T_W;
const NS=Math.ceil(TU*240);
const kf=(t,a)=>{if(t<=a[0][0])return a[0][1];for(let i=1;i<a.length;i++){if(t<a[i][0]){const p=a[i-1],q=a[i];return lerp(p[1],q[1],sst(p[0],q[0],t));}}return a[a.length-1][1];};
function vLift(th,open,close){const x=((th-open)%720+720)%720,dur=((close-open)%720+720)%720;if(x>dur)return 0;const s=Math.sin(Math.PI*x/dur);return LIFT_V*s*s;}
function phaseOf(U,variant){if(variant==='top')return 'P';if(variant==='bot')return 'B';return U<T_P?'H':U<T_D?'P':U<T_S?'N':U<T_W?'S':'W';}
/* petrol: throttle closes at c, opens again at r; B = boost, ld = delay until the blow-off lifts */
function petrolEvent(s,t,c,r,B,ld){
  const k=sst(c,c+0.3,t)*(1-sst(r,r+0.45,t));               /* throttle closed amount */
  const L=sst(c+ld,c+ld+0.4,t)*(1-sst(r-0.15,r+0.25,t));     /* blow-off lift */
  const Rb=150000;
  s.thr=1-k;s.lift=L;
  if(t<c){s.p=B;s.map=B;s.rpm=Rb;}
  else if(t<r+0.2){
    const spike=0.3*sst(c,c+0.3+ld*0.4,t)*(1-L);
    s.p=lerp(B+spike,0.12,sst(c+ld,c+ld+1.6,t));s.map=lerp(B,-0.7,sst(c,c+0.25+ld*0.6,t));s.rpm=Rb*lerp(1,0.8,sst(c+0.2,c+ld+3.0,t));
  }else{
    const q=sst(r+0.1,r+1.3,t);
    s.p=lerp(0.12,B,q);s.map=lerp(-0.7,B,sst(r,r+1.0,t));s.rpm=Rb*lerp(0.8,1,q);
  }
  s.v1=150*(s.rpm/150000)*(1-k*(1-L)*0.96);
  s.v2=lerp(150,6,k);
  s.v3=k*L*lerp(150,330,clamp(s.p/B+0.25,0,1));
  s.vent=k*L*(1-0.8*sst(c+ld+1.8,c+ld+3.4,t));               /* the trapped air runs out */
  /* overrun: no fuel, the engine slows down and breathes almost nothing past the closed throttle */
  s.fuelOn=k>0.5?0:1;s.eng=lerp(1,0.62,k);s.exh=lerp(1,0.22,k);s.cylA=lerp(1,0.35,k);
}
/* diesel, variable geometry stuck closed, turbo in overspeed: lift-off at c, the compressor surges from c+d (slow
   motion: pulses at hz) until r. loop: the turbo winds down and spools up again after r */
function surge(s,t,c,d,r,hz,loop){
  const k=sst(c,c+0.35,t)*(1-sst(r,r+0.5,t));
  const on=sst(c+d,c+d+0.5,t)*(1-sst(r-0.45,r+0.15,t));
  const q=(t-c-d)*hz;
  const w=clamp((Math.sin(TAU*q)+0.25)/1.25,0,1),rev=Math.pow(w,1.4)*on;   /* the reverse part of each pulse lasts a little longer */
  const dk=loop?sst(c+d+0.4,r,t)*(1-sst(r+0.2,r+1.4,t)):0;
  s.fuel='D';s.bovOn=0;s.vgtOn=1;s.vgt=0;s.stuck=1;s.dep=0.6;s.act=1;
  s.fuelOn=k>0.5?0:1;s.eng=lerp(1.1,0.68,k);s.exh=lerp(1.15,0.7,k);
  s.surge=on;s.rev=rev;s.q=q;
  const vf=lerp(185,lerp(110,48,sst(c+0.4,c+d+0.2,t)),k);
  s.v1=vf-(vf+270)*rev;s.v2=lerp(185,62,sst(c,c+0.6,t)*(1-sst(r,r+0.5,t)));
  s.p=lerp(2.3+0.15*k*sst(c+0.3,Math.max(c+d,c+0.8),t),1.3,dk)-0.55*rev;s.map=s.p-0.12;
  s.stress=on*(0.3+0.7*rev);
  s.jolt=on*(Math.sin(TAU*q*2)*0.5+rev*0.5);
  s.rpm=lerp(192000,150000,dk)-24000*rev;
}
const hookEnv=t=>{const x=(t-K.HE.t0)*60,v=K.HE.v;if(x<0||x>=v.length-1)return 0;const i=Math.floor(x);return v[i]+(v[i+1]-v[i])*(x-i);};
/* hook: the same fault in real time. The reverse bursts follow the chuffs of the hook sound, then slow motion */
function hookState(s,t){
  surge(s,t,K.H_LIFT,K.H_SLOW-K.H_LIFT,1e4,1.5,false);
  const slow=s.surge,rs=s.rev;
  /* the burst is solid, then the flutter flickers at 10 Hz while the sound decays */
  const fl=lerp(1,0.4+0.6*Math.pow(0.5+0.5*Math.cos(TAU*10*(t-K.HE.tb)),0.8),sst(0.22,0.36,t-K.HE.tb));
  const rb=Math.pow(hookEnv(t),0.55)*fl*(1-slow);
  const on=Math.max(slow,sst(K.H_LIFT+0.05,K.H_LIFT+0.25,t)),rev=Math.max(rs,rb);
  s.surge=on;s.rev=rev;
  const vf=lerp(185,48,sst(K.H_LIFT,K.H_LIFT+0.3,t));
  s.v1=vf-(vf+270)*rs-(vf+900)*rb;
  s.p=2.3-0.55*rev-0.5*sst(K.H_LIFT+0.2,K.H_SLOW,t)*(1-slow);s.map=s.p-0.12;
  s.stress=on*(0.3+0.7*rev);
  const d=sst(K.H_DMG,K.H_DMG+1.2,t);
  s.jolt=(slow*(Math.sin(TAU*s.q*2)*0.5+rs*0.5)+rb*0.9)*(1+1.4*d);
  s.rpm=192000-24000*rev-16000*sst(K.H_LIFT+0.2,K.H_SLOW,t)-22000*sst(K.H_SPK,K.H_SPK+2.5,t);
  s.brg=on*d*(0.55+0.45*rev);
  s.spark=sst(K.H_SPK,K.H_SPK+0.35,t)*(0.5+0.5*rev);
}
/* the diesel story (rows 4-13 of the voice-over), as keyframed tracks */
const TR=(function(){
  const a=K;
  return {
    eng:[[0,1],[a.D_LIFT,1],[a.D_LIFT+1,0.62],[a.D_ACC,0.62],[a.D_ACC+0.8,1],[a.G_LOW,1],[a.G_LOW+1.0,0.55],[a.G_HIGH,0.55],[a.G_HIGH+1.1,1.15],
         [a.C_LOW,1.15],[a.C_LOW+1.0,0.55],[a.C_TRY-0.2,0.55],[a.C_TRY+1.2,1.1],[a.L_LIFT,1.1],[a.L_LIFT+0.35,0.68]],
    exh:[[0,1],[a.D_LIFT,1],[a.D_LIFT+1,0.75],[a.D_ACC,0.75],[a.D_ACC+0.8,1],[a.G_LOW,1],[a.G_LOW+1.0,0.7],[a.G_HIGH,0.7],[a.G_HIGH+1.1,1.15],
         [a.C_LOW,1.15],[a.C_LOW+1.0,0.7],[a.C_TRY-0.2,0.7],[a.C_TRY+1.2,1.15],[a.L_LIFT,1.15],[a.L_LIFT+0.35,0.7]],
    vgt:[[0,0.55],[a.D_LIFT,0.55],[a.D_LIFT+3,0.9],[a.D_ACC,0.9],[a.D_ACC+2.2,0.55],[a.G_SWEEP,0.55],[a.G_SWEEP+0.75,0.9],[a.G_SWEEP+1.7,0.2],[a.G_SWEEP+2.4,0.5],
         [a.G_CLOSE,0.5],[a.G_CLOSE+1.0,0.06],[a.G_OPEN,0.06],[a.G_OPEN+1.0,0.95],[a.C_LOW+0.2,0.95],[a.C_LOW+2.0,0.05],[a.C_STUCK,0.02],[a.C_STUCK+0.5,0]],
    rpm:[[0,140000],[a.D_LIFT,140000],[a.D_LIFT+4,80000],[a.D_ACC,80000],[a.D_ACC+2.5,150000],[a.G_LOW,150000],[a.G_LOW+1.6,104000],[a.G_CLOSE+1.4,112000],
         [a.G_HIGH,112000],[a.G_HIGH+1.8,150000],[a.C_LOW,150000],[a.C_LOW+1.6,106000],[a.C_TRY,112000],[a.C_TRY+1.6,150000],[a.O_R0,150000],[a.O_R1,192000]],
    p:[[0,1.2],[a.D_LIFT,1.2],[a.D_LIFT+3,0.12],[a.D_ACC,0.12],[a.D_ACC+2.2,1.2],[a.G_LOW,1.2],[a.G_LOW+1.6,0.7],[a.G_CLOSE+1.4,1.0],
       [a.G_HIGH,1.0],[a.G_HIGH+1.8,1.3],[a.C_LOW,1.3],[a.C_LOW+1.6,0.9],[a.C_TRY,1.0],[a.C_TRY+1.8,1.3],[a.O_P0,1.3],[a.O_P1,2.3]],
    v:[[0,150],[a.D_LIFT,150],[a.D_LIFT+3,85],[a.D_ACC,85],[a.D_ACC+2.2,150],[a.G_LOW,150],[a.G_LOW+1.2,95],[a.G_HIGH,95],[a.G_HIGH+1.4,165],
       [a.C_LOW,165],[a.C_LOW+1.2,95],[a.C_TRY,95],[a.C_TRY+1.4,160],[a.O_R0,160],[a.O_R1,185]]
  };
})();
function dieselStory(s,t){
  s.fuel='D';s.bovOn=0;s.vgtOn=1;
  if(t>=K.L_LIFT){
    surge(s,t,K.L_LIFT,K.S_ON-K.L_LIFT,1e4,K.HZ,false);
    const wear=0.3*sst(K.X_BRG0,K.X_BRG0+0.8,t)+0.7*sst(K.X_BRG,K.X_BRG+1.4,t);
    s.jolt*=1+1.6*sst(K.X_JOC,K.X_JOC+1.5,t);
    s.brg=s.surge*wear*(0.55+0.45*s.rev);
    s.spark=sst(K.X_SPK,K.X_SPK+0.4,t)*(0.5+0.5*s.rev);
    s.rpm-=30000*sst(K.X_SPK+0.5,K.X_SPK+4.5,t);
    return;
  }
  s.fuelOn=(t>=K.D_LIFT&&t<K.D_ACC)?0:1;
  s.eng=kf(t,TR.eng);s.exh=kf(t,TR.exh);s.vgt=kf(t,TR.vgt);s.rpm=kf(t,TR.rpm);s.p=kf(t,TR.p);s.map=s.p-0.04;
  s.v1=s.v2=kf(t,TR.v);
  s.stuck=sst(K.C_STUCK,K.C_STUCK+0.5,t);s.dep=0.6*sst(K.C_DEP,K.C_STUCK+0.5,t);s.act=sst(K.C_TRY,K.C_TRY+0.5,t);
}
function stateAt(U,variant){
  const ph=phaseOf(U,variant);
  const s={ph,fuel:'P',fuelOn:1,eng:1,exh:1,cylA:1,thr:1,bovOn:1,lift:0,p:1.2,map:1.2,rpm:150000,v1:150,v2:150,v3:0,vent:0,surge:0,rev:0,q:0,stress:0,jolt:0,spark:0,brg:0,vgt:0.55,vgtOn:0,stuck:0,dep:0,act:0};
  if(ph==='P'){
    if(variant==='top'){if(U<K.SP_C2)petrolEvent(s,U,K.SP_C1,K.SP_R1,1.2,0.32);else petrolEvent(s,U,K.SP_C2,1e4,1.2,0.32);}
    else petrolEvent(s,U,K.P_C,1e4,1.2,K.P_L-K.P_C);
  }else if(ph==='B'){
    if(U<K.SP_C2)surge(s,U,K.SP_C1,0.1,K.SP_R1,K.HZ,true);else surge(s,U,K.SP_C2,0.1,1e4,K.HZ,false);
  }else if(ph==='H')hookState(s,U);
  else if(ph==='N')dieselStory(s,U);
  else if(ph==='W')surge(s,U,K.W_LIFT,0.1,K.W_ACC,K.HZ,true);
  else{s.fuel='D';s.bovOn=0;s.vgtOn=1;}
  return s;
}
/* look-up tables per variant: crank angle, exhaust gas, the three air streams, rotor angle;
   cool = exhaust intervals (in gas distance) emitted with the fuel cut */
const LUT={oil:new Float32Array(NS+1)};
const LV={};
(function(){
  const dt=1/240;
  for(let i=0,oi=0;i<=NS;i++){LUT.oil[i]=oi;oi+=dt*0.42;}
  ['main','top','bot'].forEach(v=>{
    const F=()=>new Float32Array(NS+1);
    const A={th:F(),gex:F(),g1:F(),g2:F(),g3:F(),spin:F(),cool:[]};
    let th=200,g=0,g1=0,g2=0,g3=0,sp=0,was=1,ca=0;
    for(let i=0;i<=NS;i++){
      const U=i*dt,s=stateAt(U,v);
      A.th[i]=th;A.gex[i]=g;A.g1[i]=g1;A.g2[i]=g2;A.g3[i]=g3;A.spin[i]=sp;
      if(was&&!s.fuelOn)ca=g;else if(!was&&s.fuelOn)A.cool.push([ca,g]);
      was=s.fuelOn;
      const r=560*s.eng,le=vLift(th,498,8)/LIFT_V;
      g+=dt*(r/720)*300*(0.22+1.5*le)*s.exh;th+=dt*r;
      g1+=dt*s.v1;g2+=dt*s.v2;g3+=dt*s.v3;sp+=dt*TAU*1.15*(s.rpm/150000);
    }
    if(!was)A.cool.push([ca,1e9]);
    LV[v]=A;
  });
})();
const lut=(arr,U)=>{const x=clamp(U,0,TU)*240,i=Math.min(NS-1,Math.floor(x));return arr[i]+(arr[i+1]-arr[i])*(x-i);};
