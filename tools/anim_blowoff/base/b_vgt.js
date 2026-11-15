/* =====================================================================
   ENLARGED VARIABLE-GEOMETRY VIEW (same model as in the EGR film): vane ring seen along the shaft,
   turbine wheel, actuator with lever and rod; soot on the vanes
   ===================================================================== */
/* soot shader */
const NOISE_GL=[
'float h3(vec3 p){p=fract(p*0.3183099+0.1);p*=17.0;return fract(p.x*p.y*p.z*(p.x+p.y+p.z));}',
'float vn(vec3 x){vec3 i=floor(x),f=fract(x);f=f*f*(3.0-2.0*f);',
' return mix(mix(mix(h3(i),h3(i+vec3(1,0,0)),f.x),mix(h3(i+vec3(0,1,0)),h3(i+vec3(1,1,0)),f.x),f.y),',
'  mix(mix(h3(i+vec3(0,0,1)),h3(i+vec3(1,0,1)),f.x),mix(h3(i+vec3(0,1,1)),h3(i+vec3(1,1,1)),f.x),f.y),f.z);}',
'float fbm(vec3 p){return 0.55*vn(p)+0.3*vn(p*2.13)+0.15*vn(p*4.7);}'].join('\n');
const DEP_VS='varying vec3 vP;varying vec2 vUv;void main(){vUv=uv;vec4 w=modelMatrix*vec4(position,1.0);vP=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}';
const DEP_FS=[NOISE_GL,
'uniform float uDep,uWipe,uMode,uBase,uBase2,uClipZ,uClipY,uWipeZ;uniform vec4 uHole;uniform vec3 uA,uB;varying vec3 vP;varying vec2 vUv;',
'void main(){',
' float n=fbm(vP*0.16);',
' float w=clamp(uBase+exp(-distance(vP,uA)/42.0)+0.85*exp(-distance(vP,uB)/34.0),0.0,1.0);',
' float cov=uDep*(0.45+0.75*w);',
' if(cov<0.002)discard;',
' float lim=cov*(0.5+0.75*n);',
' if(uMode<0.5){if(vUv.y>lim)discard;}',
' else{if(n>cov*uBase2)discard;}',
' if(vP.x<uWipe||vP.z>uWipeZ||vP.z>uClipZ||vP.y>uClipY)discard;',
' if(uHole.w>0.0&&distance(vP,uHole.xyz)<uHole.w*(0.75+0.5*n))discard;',
' float n2=vn(vP*1.4);',
' vec3 c=mix(vec3(0.05,0.04,0.032),vec3(0.21,0.15,0.1),n2*n2);',
' c+=vec3(0.08,0.065,0.045)*smoothstep(0.78,0.95,vn(vP*0.8+3.0));',
' float e=(1.0-smoothstep(0.0,4.0,vP.x-uWipe))*step(-5000.0,uWipe);',
' e=max(e,(1.0-smoothstep(0.0,5.0,uWipeZ-vP.z))*step(uWipeZ,5000.0));',
' c=mix(c,vec3(0.5,0.95,0.88),e);',
' if(uMode<0.5)c+=vec3(0.16,0.11,0.07)*smoothstep(lim-0.07,lim,vUv.y);',
' gl_FragColor=vec4(c,1.0);',
'}'].join('\n');
const depMats=[];
function depMat(mode,o){
  o=o||{};
  const m=new T.ShaderMaterial({vertexShader:DEP_VS,fragmentShader:DEP_FS,side:T.DoubleSide,
    polygonOffset:mode>0.5,polygonOffsetFactor:-2,polygonOffsetUnits:-2,
    uniforms:{uDep:{value:0},uWipe:{value:-1e4},uMode:{value:mode},uBase:{value:o.base===undefined?0.25:o.base},uBase2:{value:o.cov||0.62},uClipZ:{value:o.mf?0.02:1e4},uClipY:{value:1e4},uWipeZ:{value:1e4},uHole:{value:new T.Vector4(0,0,0,0)},
      uA:{value:o.a||new T.Vector3(-266,58,-6)},uB:{value:o.b||new T.Vector3(-246,31,-8)}}});
  m.userData.group=o.group||'in';depMats.push(m);return m;
}
function rectCut(x0,y0,x1,y1,mat,parent){const g=polyGeo([[x0,y0],[x1,y0],[x1,y1],[x0,y1]]);const m=new T.Mesh(g,mat);parent.add(m);edges(parent,g);return m;}
const DGP=new T.Vector3(300,TY,0),DG=new T.Group();DG.position.copy(DGP);scene.add(DG);
const VG={rp:72,n:11,cIn:-11,cOut:27};
const dgVanes=[],dgActPos=new T.Vector2(142,-128),dgLeverPiv=new T.Vector2(104,-74);
let dgWheel,dgLever,dgRod;
const vaneDep=depMat(1,{base:1,group:'vgt',cov:0.9});
(function(){
  const chan=flat(0x2a231e);
  const ring=(r0,r1,mat,z)=>{const m=new T.Mesh(new T.RingGeometry(r0,r1,128),mat);m.position.z=z;DG.add(m);return m;};
  ring(92,112,chan,-10);
  ring(40,92,std(0x57514b,.85,.45),-7);
  const wall=ring(112,121,C.tHouse,0);edges(DG,wall.geometry,0.02);
  const ch=new T.Mesh(polyGeo([[0,92],[178,92],[178,112],[0,112]]),chan);ch.position.z=-10;DG.add(ch);
  rectCut(0,112,178,121,C.tHouse,DG);rectCut(36,83,178,92,C.tHouse,DG);
  /* wheel */
  dgWheel=new T.Group();DG.add(dgWheel);
  const wm=std(0x8a8079,.95,.34);
  const back=new T.Mesh(new T.CircleGeometry(50,64),std(0x6f665f,.9,.4));back.position.z=-5;dgWheel.add(back);
  const hub=new T.Mesh(new T.CylinderGeometry(19,22,12,40),wm);hub.rotation.x=Math.PI/2;hub.position.z=1;dgWheel.add(hub);
  const nut=new T.Mesh(new T.CylinderGeometry(7,7,14,6),M.steel);nut.rotation.x=Math.PI/2;nut.position.z=2;dgWheel.add(nut);
  const up=[],dn=[],N=12;
  for(let i=0;i<=N;i++){const r=lerp(18,50,i/N),a=0.55*Math.pow(i/N,1.4),hw=lerp(1.6,1.0,i/N),x=r*Math.cos(a),y=r*Math.sin(a),nx=-Math.sin(a),ny=Math.cos(a);up.push(V2(x+nx*hw,y+ny*hw));dn.push(V2(x-nx*hw,y-ny*hw));}
  const bg=new T.ExtrudeGeometry(new T.Shape(up.concat(dn.reverse())),{depth:9,bevelEnabled:false});bg.translate(0,0,-4.5);
  for(let k=0;k<11;k++){const b=new T.Mesh(bg,wm);b.rotation.z=k*TAU/11;dgWheel.add(b);}
  /* vanes: cambered airfoils on pivot pins */
  const UP=[],LO=[],NA=16;
  for(let i=0;i<=NA;i++){const s=i/NA,x=lerp(VG.cIn,VG.cOut,s),yt=28.5*(0.2969*Math.sqrt(s)-0.126*s-0.3516*s*s+0.2843*s*s*s-0.1015*s*s*s*s),yc=2.0*Math.sin(Math.PI*s);UP.push(V2(x,yc+yt));LO.push(V2(x,yc-yt));}
  const vg=new T.ExtrudeGeometry(new T.Shape(UP.concat(LO.reverse())),{depth:12,bevelEnabled:false});vg.translate(0,0,-6);
  const vmat=std(0xa59e97,.9,.35);
  for(let k=0;k<VG.n;k++){
    const phi=k*TAU/VG.n,g=new T.Group();g.position.set(VG.rp*Math.cos(phi),VG.rp*Math.sin(phi),0);g.userData.phi=phi;
    g.add(new T.Mesh(vg,vmat));g.add(new T.Mesh(vg,vaneDep));
    const pin=new T.Mesh(new T.CircleGeometry(2.6,16),flat(0x1e2328));pin.position.z=6.3;g.add(pin);
    DG.add(g);dgVanes.push(g);
  }
  /* actuator, lever, rod */
  const act=new T.Mesh(new T.BoxGeometry(56,36,22),std(0x23272c,.3,.6));act.position.set(dgActPos.x+28,dgActPos.y,-2);DG.add(act);
  const can=new T.Mesh(new T.CylinderGeometry(15,15,20,28),std(0x353b42,.5,.5));can.rotation.x=Math.PI/2;can.position.set(dgActPos.x+30,dgActPos.y,8);DG.add(can);
  dgLever=new T.Mesh(new T.BoxGeometry(30,6,4),std(0xb8bec5,.95,.3));DG.add(dgLever);
  dgRod=new T.Mesh(new T.CylinderGeometry(1.8,1.8,1,10),M.steel);DG.add(dgRod);
  const lp=new T.Mesh(new T.CircleGeometry(4,16),flat(0x1e2328));lp.position.set(dgLeverPiv.x,dgLeverPiv.y,3);DG.add(lp);
})();
function vanePsi(phi,beta){const tx=-Math.sin(phi),ty=Math.cos(phi),rx=Math.cos(phi),ry=Math.sin(phi);return Math.atan2(ty*Math.cos(beta)-ry*Math.sin(beta),tx*Math.cos(beta)-rx*Math.sin(beta));}
const conn=new T.Line(new T.BufferGeometry().setFromPoints([new T.Vector3(61.5,TY+38,-4),new T.Vector3(DGP.x-86,DGP.y+86,0)]),
  new T.LineDashedMaterial({color:0xffb224,dashSize:5,gapSize:4,transparent:true,opacity:0,toneMapped:false}));
conn.computeLineDistances();scene.add(conn);
