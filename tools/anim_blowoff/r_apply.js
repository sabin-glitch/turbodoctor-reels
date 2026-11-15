const vEl=[0];
let FUEL=1,CYLA=1;
sparkFlash.material.map=glowTex;sparkFlash.material.needsUpdate=true;
mafGlow.material.map=glowTex;mafGlow.material.needsUpdate=true;
const MAF0=col(0x5a3410),MAF1=col(0xffc860);
M.wheelC.emissive=new T.Color(0,0,0);M.bronzeT.emissive=new T.Color(0,0,0);
const surgeGlow=new T.Sprite(new T.SpriteMaterial({map:glowTex,color:0xff3a20,blending:T.AdditiveBlending,depthWrite:false,transparent:true,opacity:0,toneMapped:false}));
surgeGlow.position.set(-86,TY,-6);surgeGlow.scale.set(90,90,1);scene.add(surgeGlow);
const BRZ=col(0xc9945a),BRR=col(0xff3b1f);
const WC_E=new T.Color(1,0.12,0.06),BR_E=new T.Color(1,0.28,0.06),VAC_E=new T.Color(0.15,0.55,1);
/* enlarged variable-geometry view: only in the closing, while the voice names it as one of the causes (main take only) */
const dgScale=U=>pulse(U,K.W_DG,K.W_DG+0.8,K.W_OTH+0.1,K.W_OTH+0.9);
function apply(U,variant){
  variant=variant||'main';
  const S=stateAt(U,variant),L=LV[variant];
  FUEL=S.fuelOn;CYLA=S.cylA;
  const th=lut(L.th,U),crown=-CLEAR-pistonDrop(th);crownNow=crown;
  piston.position.y=crown;rod.position.y=crown-COMP_H;rod.rotation.z=Math.asin(CRK*Math.sin(th*DEG)/ROD);
  const li=vLift(th,712,222),le=vLift(th,498,8);
  vIn.g.position.y=-li;vEx.g.position.y=-le;
  setHelix(vIn.sp.geometry,HEAD_H+1.3,22.4-li);setHelix(vEx.sp.geometry,HEAD_H+1.3,22.4-le);
  const st=drawCyl(th,crown);
  const burn=st.burn*FUEL,cy=Math.max(crown*0.5-3,-40);
  fireLight.intensity=1.6*burn;fireLight.position.set(EX,cy,10);
  glow.material.opacity=0.2*burn;glow.position.set(EX,cy-2,-8);const gs=60+26*burn+Math.min(-crown,60)*0.9;glow.scale.set(gs,gs*0.72,1);
  const petrol=S.fuel==='P';
  plugG.visible=petrol;injMesh.visible=!petrol;VGG.visible=!!S.vgtOn;pCrownP.visible=petrol;pCrownD.visible=!petrol;
  sparkFlash.material.opacity=petrol&&FUEL?0.95*pulse(st.c,343,346,351,355):0;
  /* turbo */
  rotor.rotation.x=lut(L.spin,U);
  rotor.position.set(S.jolt*1.7,S.surge*0.35*Math.sin(U*61),S.surge*0.35*Math.cos(U*53));
  tGlow.material.opacity=0.10*FUEL;
  M.wheelC.emissive.copy(WC_E).multiplyScalar(0.65*S.stress);
  M.bronzeT.emissive.copy(BR_E).multiplyScalar(1.5*S.brg);
  C.bronzeT.color.copy(BRZ).lerp(BRR,0.85*S.brg);
  surgeGlow.material.opacity=0.55*S.rev*S.surge;
  const beta=lerp(6,40,S.vgt)*DEG;
  vanesIn.forEach(g=>{g.rotation.x=beta;});
  /* throttle and blow-off */
  flap.rotation.z=lerp(0.12,Math.PI/2-0.06,S.thr);
  BV.visible=!!S.bovOn;vacHose.visible=vacNip.visible=!!S.bovOn;
  setBov(S.bovOn?S.lift:0);
  M.hoseV.emissive.copy(VAC_E).multiplyScalar(0.55*clamp(-S.map/0.7,0,1)*(S.bovOn?1:0));
  /* recirculation valve and MAF */
  DVG.visible=dvHose.visible=dvTap.visible=!!S.dvOn;
  setDv(S.dvOn?S.dvLift:0);
  mafEl.material.color.copy(MAF0).lerp(MAF1,clamp(S.maf,0,1));mafGlow.material.opacity=0.6*clamp(S.maf,0,1);
  const GX=lut(L.gex,U),G1=lut(L.g1,U);
  drawExhaust(GX,variant);
  drawS1(G1,S);drawS2(lut(L.g2,U));drawS3(lut(L.g3,U),S);drawS4(lut(L.g4,U),S);drawSparks(U,S);drawChev(G1,S);
  /* enlarged variable-geometry view */
  const sc=variant==='main'?dgScale(U):0;
  DG.visible=sc>0.01;conn.visible=DG.visible;
  if(DG.visible){
    DG.scale.setScalar(sc);
    vaneDep.uniforms.uDep.value=S.dep;
    dgVanes.forEach(g=>{g.rotation.z=vanePsi(g.userData.phi,beta);});
    dgWheel.rotation.z=lut(L.spin,U)*1.2;
    /* the actuator keeps trying to open the stuck vanes */
    const cmd=S.vgt+0.085*S.act*S.stuck*(0.5+0.5*Math.sin(U*6.5));
    const lam=(-110+40*cmd)*DEG,ex=dgLeverPiv.x+24*Math.cos(lam),ey=dgLeverPiv.y+24*Math.sin(lam);
    dgLever.position.set(dgLeverPiv.x+12*Math.cos(lam),dgLeverPiv.y+12*Math.sin(lam),2);dgLever.rotation.z=lam;
    const dx=dgActPos.x-ex,dy=dgActPos.y-ey,Lr=Math.hypot(dx,dy);
    dgRod.position.set((ex+dgActPos.x)/2,(ey+dgActPos.y)/2,3);dgRod.scale.set(1,Lr,1);dgRod.rotation.z=Math.atan2(dy,dx)-Math.PI/2;
    conn.material.opacity=0.85*pulse(U,K.W_DG+0.2,K.W_DG+0.6,K.W_OTH-0.1,K.W_OTH+0.5);
  }
  drawEmbers(GX,sc,S);
  const O=lut(LUT.oil,U);
  oilMats.forEach(m=>{m.uniforms.uHi.value=0;m.uniforms.uPhase.value=O*(m.uniforms.uLen.value>1.5?1.6:1.0);});
  drawDrops(U,0,1e5);
  const tr=t=>pulse(U,t-0.4,t-0.04,t+0.04,t+0.42);
  $('fade').style.opacity=Math.max(tr(T_P),tr(T_B),tr(T_D),tr(T_S),tr(T_W)).toFixed(3);
  return {th,st,S};
}
