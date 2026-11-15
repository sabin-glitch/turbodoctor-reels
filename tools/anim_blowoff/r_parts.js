/* =====================================================================
   REEL v2 (15.11.2026): AIR-MASS SENSOR (MAF) IN FRONT OF THE COMPRESSOR + FACTORY RECIRCULATION (DIVERTER) VALVE
   ON THE COMPRESSOR INLET, WITH ITS RETURN HOSE FROM THE PRESSURE PIPE (petrol engines)
   ===================================================================== */
const MAF_X=-199,DV_X=-138,DV_Y=TY+24.6,DV_P=22,DV_TAPX=DV_X-42;
M.mafTube=stdC(0x24282d,.2,.62);C.mafTube=cut(0x424951,HA);M.mafBody=std(0x16181b,.15,.6);C.mafBody=cut(0x2b3037,HB);
M.dvBody=stdC(0x2d3238,.3,.55);C.dvBody=cut(0x4b525b,HB);M.coil=stdC(0xb4703a,.85,.38);C.coil=cut(0xc58a52,HA);
const COIL0=col(0xc58a52),COIL1=col(0xffc061);
/* MAF: short tube between the filter and the compressor inlet, plug-in hot-film sensor */
axPart(turbo,[[-208,19.2],[-190,19.2],[-190,26.5],[-208,26.5]],M.mafTube,C.mafTube,{seg:40});
const MAFG=new T.Group();MAFG.position.set(MAF_X,TY,0);scene.add(MAFG);
let mafEl,mafGlow;
(function(){
  const bx=(w,h,d,x,y,z,m)=>{const b=new T.Mesh(new T.BoxGeometry(w,h,d),m||M.mafBody);b.position.set(x,y,z);MAFG.add(b);return b;};
  bx(7,21,11,0,16.5,-5.5);                       /* finger in the air stream */
  bx(18,4.5,16,0,28.6,-8);                       /* flange on the tube */
  bx(11.5,13,13,-0.5,37.2,-7);                   /* connector body */
  bx(9,7,9,9,38.5,-7,std(0x3d434a,.3,.5));       /* plug */
  capPoly(MAFG,[[-3.5,6],[3.5,6],[3.5,26.4],[9,26.4],[9,30.8],[5.3,30.8],[5.3,43.7],[-6.3,43.7],[-6.3,30.8],[-9,30.8],[-9,26.4],[-3.5,26.4]],C.mafBody,0.03);
  const win=new T.Mesh(polyGeo([[-2.3,8],[2.3,8],[2.3,14],[-2.3,14]]),flat(0x07090c));win.position.z=0.05;MAFG.add(win);
  mafEl=new T.Mesh(polyGeo([[-1.7,10.3],[1.7,10.3],[1.7,11.7],[-1.7,11.7]]),new T.MeshBasicMaterial({color:0xffb040,toneMapped:false,side:T.DoubleSide}));mafEl.position.z=0.06;MAFG.add(mafEl);
  mafGlow=new T.Sprite(new T.SpriteMaterial({map:null,color:0xffa030,blending:T.AdditiveBlending,depthWrite:false,transparent:true,opacity:0,toneMapped:false}));
  mafGlow.position.set(0,11,1.2);mafGlow.scale.set(15,15,1);mafGlow.renderOrder=8;MAFG.add(mafGlow);
})();
/* recirculation valve: vertical, on top of the inlet duct; poppet lifted by a solenoid; side port to the return hose */
const DVG=new T.Group();DVG.position.set(DV_X,DV_Y,0.03);scene.add(DVG);
const DVm=new T.Group();DVG.add(DVm);
let dvSpring;
(function(){
  const PO=7,PIN=5.5,W0=DV_P-PO,W1=DV_P+PO,OUT_D=Math.asin(PO/17);
  /* stub through the duct wall + valve seat */
  revolved(DVG,[[7,-5.5],[10,-5.5],[10,12],[17,12],[17,14.2],[7,14.2]],M.alu,C.alu,{seg:36});
  {const b=new T.Mesh(polyGeo([[-7,-5.7],[7,-5.7],[7,0.3],[-7,0.3]]),flat(0x4d545c));b.position.z=-0.004;DVG.add(b);}   /* bore through the duct wall */
  /* chamber: outer and inner skins, window where the port joins (towards -X) */
  const full=(prof)=>DVG.add(new T.Mesh(latheArc(prof,Math.PI/2,Math.PI,44,false),M.dvBody));
  const part=(prof)=>DVG.add(new T.Mesh(latheArc(prof,Math.PI/2,Math.PI-OUT_D,44,false),M.dvBody));
  full([[17,14.2,1],[17,W0,1]]);part([[17,W0,1],[17,W1,1]]);full([[17,W1,1],[17,43,1]]);
  full([[13.5,40,1],[13.5,W1,1]]);part([[13.5,W1,1],[13.5,W0,1]]);full([[13.5,W0,1],[13.5,14.2,1]]);
  capPoly(DVG,[[13.5,14.2],[17,14.2],[17,43],[13.5,43]],C.dvBody);
  capPoly(DVG,[[-17,14.2],[-13.5,14.2],[-13.5,DV_P-PIN],[-17,DV_P-PIN]],C.dvBody);
  capPoly(DVG,[[-17,DV_P+PIN],[-13.5,DV_P+PIN],[-13.5,43],[-17,43]],C.dvBody);
  /* partition with the stem guide */
  revolved(DVG,[[2.6,40],[13.5,40],[13.5,43],[5.2,43],[5.2,44.2],[2.6,44.2]],M.dvBody,C.dvBody,{seg:40});
  /* side port with hose barb, along -X */
  const op=[[PIN,13.6],[PO,13.6],[PO,25.5],[7.9,26.6],[7.9,27.6],[PO,28.8],[PO,30],[PIN,30]];
  const og=latheArc(op,Math.PI/2,Math.PI,28,true);og.rotateZ(Math.PI/2);og.translate(0,DV_P,0);DVG.add(new T.Mesh(og,M.dvBody));
  const oc=capGeo(op);oc.rotateZ(Math.PI/2);oc.translate(0,DV_P,0.01);DVG.add(new T.Mesh(oc,C.dvBody));edges(DVG,oc,0.02);
  /* solenoid: coil, armature tube, yoke with the top cap, connector */
  revolved(DVG,[[6.2,45.6],[13.2,45.6],[13.2,63.6],[6.2,63.6]],M.coil,C.coil,{seg:40});
  revolved(DVG,[[5.5,44.4],[6.1,44.4],[6.1,66],[5.5,66]],M.steel,cut(0xc4cad1,HB),{seg:30});
  revolved(DVG,[[0,66],[13.4,66],[13.4,43],[17,43],[17,66.4],[15.4,69],[0,69]],M.dvBody,C.dvBody,{seg:44});
  {const con=new T.Mesh(new T.BoxGeometry(13,11,12),M.mafBody);con.position.set(22.5,57,-8);DVG.add(con);
   const pl=new T.Mesh(new T.BoxGeometry(8,8,9),std(0x3d434a,.3,.5));pl.position.set(31,58.5,-8);DVG.add(pl);}
  /* moving part: valve disc with rubber seal, stem, armature */
  revolved(DVm,[[0,15],[10.6,15],[10.6,16.4],[11.6,16.4],[11.6,17.8],[8.6,19.2],[2.4,19.8],[2.4,44.6],[5.2,44.6],[5.2,55],[0,55]],M.poppet,C.poppet,{seg:40});
  revolved(DVm,[[7.6,14.3],[10.4,14.3],[10.4,15],[7.6,15]],M.rubber,C.rub,{seg:40});
  dvSpring=new T.Mesh(makeHelix(3.4,0.7,5),M.bovSpring);DVG.add(dvSpring);
})();
let dvLiftNow=-1;
function setDv(lift){
  if(Math.abs(lift-dvLiftNow)<0.002)return;dvLiftNow=lift;
  const y=lift*6;DVm.position.y=y;setHelix(dvSpring.geometry,55+y,66-(55+y));
  C.coil.color.copy(COIL0).lerp(COIL1,lift);
}
setDv(0);
/* return hose: side port -> up and back -> tap under the pressure pipe (the upper run, behind the section plane) */
const DVH_PTS=[[-21,DV_P,0],[-30,DV_P,0],[-36,DV_P+0.3,-0.3],[-41,DV_P+3,-1.2],[-43.5,DV_P+9,-3],[-44,DV_P+20,-7],[-43,DV_P+40,-15.5],[-42,DV_P+60,-23.5],[-42,DV_P+75,-26]].map(p=>[DV_X+p[0],DV_Y+p[1],p[2]]);
const DVH=curvePath(DVH_PTS,90);
const dvHose=new T.Mesh(new T.TubeGeometry(DVH.curve,90,8.6,20,false),M.hose);scene.add(dvHose);
const dvTap=new T.Mesh(new T.CylinderGeometry(10.4,10.4,9,24),M.alu);dvTap.position.set(DV_TAPX,TY+107.5,-25.6);scene.add(dvTap);
