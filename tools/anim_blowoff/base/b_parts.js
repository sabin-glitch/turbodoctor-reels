/* =====================================================================
   BLOW-OFF VALVE (poppet + diaphragm), THROTTLE BODY, SPARK PLUG, VGT VANES
   ===================================================================== */
const BOV_Y=128,THR_Y=100,PIPE_X=-266,BOV_W0=22,BOV_W1=36,BOV_OUT=29;   /* outlet window along the valve axis, outlet centre */
M.bovBody=stdC(0x2457b8,.72,.3);M.bovCap=stdC(0x1b2a44,.7,.34);M.alu=stdC(0xbcc3ca,.92,.28);
M.rubber=stdC(0x24272b,.1,.75);M.brass=stdC(0xb79d62,.95,.3);M.tbHouse=stdC(0x8f989f,.85,.42);M.plastic=stdC(0x26292d,.15,.6);
M.bovSpring=stdC(0xd7dce2,1,.22);M.hoseV=stdC(0x202327,.15,.7);
M.poppet=stdC(0xc9a85c,.95,.26);C.poppet=cut(0xd8bd78,HB);C.bov=cut(0x7f9fd8,HB);C.bovCap=cut(0x5a6f96,HA);C.alu=cut(0xb8c0c8,HA);C.rub=cut(0x34383d,HA);C.tb=cut(0xa3acb4,HB);
/* half lathe around Y with explicit phi range (back half by default) */
function latheArc(profile,phi0,phiLen,seg,closed){
  const pts=[],push=p=>pts.push(V2(Math.max(p[0],1e-4),p[1]));
  profile.forEach(p=>{push(p);if(!p[2])push(p);});if(closed)push(profile[0]);
  return new T.LatheGeometry(pts,seg||40,phi0===undefined?Math.PI/2:phi0,phiLen===undefined?Math.PI:phiLen);
}
function capPoly(parent,pts,mat,z){const g=polyGeo(pts);const m=new T.Mesh(g,mat);m.position.z=z||0.01;parent.add(m);edges(parent,g,(z||0.01)+0.01);return m;}
const BV=new T.Group();BV.position.set(PIPE_X,BOV_Y,0);BV.rotation.z=Math.PI/2;scene.add(BV);   /* local +Y = world -X */
const BVm=new T.Group();BV.add(BVm);                                                             /* moving poppet */
let bovDia,bovDiaCap,bovSpring;
(function(){
  const OUT_D=Math.asin(7.4/17);
  /* weld-on stub */
  revolved(BV,[[9,7],[11.5,7],[11.5,18.5],[9,18.5]],M.alu,C.alu,{seg:32});
  revolved(BV,[[11.5,10.2],[12.9,10.2],[12.9,14.6],[11.5,14.6]],M.steel,cut(0xc4cad1,HB),{seg:32});
  {const sc=new T.Mesh(new T.BoxGeometry(5,4.4,6),M.steel);sc.position.set(13.5,12.4,-9);BV.add(sc);}
  /* lower body: outer and inner skins, side window where the outlet joins */
  const full=(prof)=>BV.add(new T.Mesh(latheArc(prof,Math.PI/2,Math.PI,44,false),M.bovBody));
  const part=(prof)=>BV.add(new T.Mesh(latheArc(prof,Math.PI/2,Math.PI-OUT_D,44,false),M.bovBody));
  full([[9,18,1],[17,18,1],[17,BOV_W0,1]]);part([[17,BOV_W0,1],[17,BOV_W1,1]]);full([[17,BOV_W1,1],[17,47,1],[19,47,1],[19,50.5,1],[12.5,50.5,1],[12.5,BOV_W1,1]]);
  part([[12.5,BOV_W1,1],[12.5,BOV_W0,1]]);full([[12.5,BOV_W0,1],[12.5,20.5,1],[9,20.5,1],[9,18,1]]);
  /* partition with stem guide */
  revolved(BV,[[3,41],[12.5,41],[12.5,44],[5.2,44],[5.2,46.5],[3,46.5]],M.bovBody,C.bov,{seg:40});
  /* section faces of the body */
  capPoly(BV,[[9,18],[17,18],[17,47],[19,47],[19,50.5],[12.5,50.5],[12.5,20.5],[9,20.5]],C.bov);
  capPoly(BV,[[-9,18],[-17,18],[-17,BOV_W0],[-12.5,BOV_W0],[-12.5,20.5],[-9,20.5]],C.bov);
  capPoly(BV,[[-12.5,BOV_W1],[-17,BOV_W1],[-17,47],[-19,47],[-19,50.5],[-12.5,50.5]],C.bov);
  /* side outlet (to atmosphere), along local -X */
  const op=[[5.6,12.5],[7.2,12.5],[7.2,27],[9.8,33.5],[9.8,35],[8.2,35],[5.6,29]];
  const og=latheArc(op,Math.PI/2,Math.PI,32,true);og.rotateZ(Math.PI/2);og.translate(0,BOV_OUT,0);BV.add(new T.Mesh(og,M.bovBody));
  const oc=capGeo(op);oc.rotateZ(Math.PI/2);oc.translate(0,BOV_OUT,0.01);BV.add(new T.Mesh(oc,C.bov));edges(BV,oc,0.02);
  /* cap with spring chamber and vacuum nipple */
  revolved(BV,[[12.5,50.6],[20,50.6],[20,54],[16.8,57],[13.4,65],[6,69.4],[3.4,70],[3.4,79],[1.3,79],[1.3,68.6],[4.2,67],[11.2,63.4],[14.6,56],[14.6,52.2],[12.5,52.2]],M.bovCap,C.bovCap,{seg:44});
  /* bolts on the flange (back side) */
  [-0.55,0.55].forEach(a=>{const b=new T.Mesh(new T.CylinderGeometry(1.8,1.8,5,6),M.steel);const ph=Math.PI+a;b.position.set(19.5*Math.sin(ph),53,19.5*Math.cos(ph));BV.add(b);});
  /* poppet: valve disc + stem, diaphragm plate */
  revolved(BVm,[[0,20.5],[9.3,20.5],[9.3,21.2],[11.6,21.2],[11.6,22.6],[8.6,23.9],[2.6,24.5],[2.6,47.2],[0,47.2]],M.poppet,C.poppet,{seg:40});
  revolved(BVm,[[9.3,20.5],[11.4,20.5],[11.4,21.2],[9.3,21.2]],M.rubber,C.rub,{seg:40});
  revolved(BVm,[[0,47.2],[11,47.2],[11,49],[0,49]],M.steel,cut(0xd0d6dc,HB),{seg:40});
  bovSpring=new T.Mesh(makeHelix(7.4,0.95,5),M.bovSpring);BV.add(bovSpring);
  bovDia=new T.Mesh(new T.BufferGeometry(),M.rubber);BV.add(bovDia);
  bovDiaCap=new T.Mesh(new T.BufferGeometry(),C.rub);bovDiaCap.position.z=0.012;BV.add(bovDiaCap);
})();
let diaLift=-1;
function setBov(lift){
  const y=lift*7;BVm.position.y=y;
  setHelix(bovSpring.geometry,49+y,64.5-(49+y));
  if(Math.abs(lift-diaLift)<0.002)return;diaLift=lift;
  const prof=[[11,49.2+y],[13.2,49.7+y*0.8-0.9],[15.6,50.2+y*0.4-0.9],[18.5,50.6]];
  const top=prof.map(p=>[p[0],p[1]+0.9]);
  const pts=prof.concat(top.slice().reverse());
  bovDia.geometry.dispose();bovDia.geometry=latheArc(pts.map(p=>[p[0],p[1],1]),Math.PI/2,Math.PI,40,true);bovDia.geometry.computeVertexNormals();
  bovDiaCap.geometry.dispose();bovDiaCap.geometry=new T.ShapeGeometry([new T.Shape(pts.map(p=>V2(p[0],p[1]))),new T.Shape(pts.map(p=>V2(-p[0],p[1])).reverse())]);
}
setBov(0);
/* vacuum hose: from the nipple to the intake after the throttle */
const VACH=curvePath([[PIPE_X-79,BOV_Y,-3],[PIPE_X-84,BOV_Y-8,-5],[PIPE_X-86,BOV_Y-40,-9],[PIPE_X-72,58,-12],[PIPE_X-34,52,-14],[PIPE_X-14,54,-10]],80);
M.hoseV.emissive=new T.Color(0,0,0);
const vacHose=new T.Mesh(new T.TubeGeometry(VACH.curve,80,2.3,12,false),M.hoseV);scene.add(vacHose);
const vacNip=new T.Mesh(new T.CylinderGeometry(2.4,2.8,6,12),M.alu);vacNip.rotation.z=Math.PI/2;vacNip.position.set(PIPE_X-12,54,-10);scene.add(vacNip);
/* throttle body on the vertical run */
const TB=new T.Group();TB.position.set(PIPE_X,THR_Y,0);scene.add(TB);
const flap=new T.Mesh(new T.CylinderGeometry(12.4,12.4,1.1,44),M.brass);
(function(){
  revolved(TB,[[13.1,-10],[17.5,-10],[17.5,-7],[20,-7],[20,7],[17.5,7],[17.5,10],[13.1,10]],M.tbHouse,C.tb,{seg:44});
  TB.add(flap);
  const sh=new T.Mesh(new T.CylinderGeometry(1.5,1.5,46,10),M.steel.clone());sh.material.clippingPlanes=CLIP;sh.rotation.x=Math.PI/2;sh.position.z=-8;TB.add(sh);
  const boss=new T.Mesh(new T.CylinderGeometry(4.6,4.6,12,16),M.tbHouse);boss.rotation.x=Math.PI/2;boss.position.z=-26;TB.add(boss);
  const act=new T.Mesh(new T.BoxGeometry(34,24,20),M.plastic);act.position.set(30,0,-16);TB.add(act);
  const mot=new T.Mesh(new T.CylinderGeometry(8,8,22,22),std(0x3a4047,.6,.45));mot.rotation.z=Math.PI/2;mot.position.set(30,-2,-4);TB.add(mot);
  const plug=new T.Mesh(new T.BoxGeometry(10,9,8),std(0x15171a,.1,.7));plug.position.set(42,11,-16);TB.add(plug);
})();
/* spark plug + ignition coil (petrol), swapped with the injector for the diesel part */
const plugG=new T.Group();eng.add(plugG);
(function(){
  const cer=std(0xeeeae0,.05,.3),cerC=cut(0xf2efe8,HA);
  plugG.add(revolvedMesh([[2.2,0.4],[3.65,0.4],[3.65,20.5],[9.2,20.5],[9.2,28.5],[6.4,30],[2.2,30]],M.steel,cut(0xc4cad1,HB),{seg:30}));
  plugG.add(revolvedMesh([[0,0.2],[1.5,0.2],[2.2,4],[2.2,30],[5.6,30],[5.6,46],[4.4,49],[3.2,52],[3.2,58],[0,58]],cer,cerC,{seg:30}));
  plugG.add(revolvedMesh([[0,-1.8],[0.8,-1.8],[0.8,0.4],[0,0.4]],M.steel,cut(0xc4cad1,HB),{seg:12}));
  const ge=new T.Mesh(new T.BoxGeometry(1.2,3.2,1.6),M.steel);ge.position.set(3,-1.0,-0.8);plugG.add(ge);
  const ge2=new T.Mesh(new T.BoxGeometry(3.4,1.0,1.6),M.steel);ge2.position.set(1.8,-2.4,-0.8);plugG.add(ge2);
  plugG.add(revolvedMesh([[5.8,44],[7.6,42],[9.4,46],[10.2,48],[10.2,92],[0,92],[0,60],[3.4,58],[3.4,52],[5.8,50]],std(0x1d2024,.1,.7),cut(0x3a3f45,HA),{seg:30}));
  const head=new T.Mesh(new T.BoxGeometry(34,18,30),std(0x17191c,.2,.5));head.position.set(6,100,-12);plugG.add(head);
  const con=new T.Mesh(new T.BoxGeometry(10,10,10),std(0x3d434a,.3,.5));con.position.set(24,104,-12);plugG.add(con);
})();
const sparkFlash=new T.Sprite(new T.SpriteMaterial({map:null,color:0xbfe0ff,blending:T.AdditiveBlending,depthTest:false,depthWrite:false,transparent:true,opacity:0,toneMapped:false}));
sparkFlash.renderOrder=11;sparkFlash.scale.set(12,12,1);sparkFlash.position.set(EX,-1.8,1);scene.add(sparkFlash);
/* variable-geometry vanes in the turbine (diesel only) */
const vanesIn=[],VGG=new T.Group();turbo.add(VGG);
(function(){
  const vm=stdC(0x9b948d,.9,.38),geo=new T.BoxGeometry(6.5,9,1.3);
  for(let k=0;k<11;k++){const piv=new T.Group();piv.rotation.x=k*TAU/11;VGG.add(piv);
    const v=new T.Group();v.position.set(61.5,0,-33.5);piv.add(v);v.add(new T.Mesh(geo,vm));vanesIn.push(v);}
  axPart(VGG,[[57.6,29],[58.6,29],[58.6,38.5],[57.6,38.5]],std(0x6e655d,.8,.5),C.tHouse,{seg:40});
})();
