/* ================= REEL (video build): director, post-injection, exhaust aftertreatment ================= */
const CU=window.CUES||{end:60,lines:[],words:[]};
const nrm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const Ts=i=>CU.lines[i].start,Te=i=>CU.lines[i].end,END=CU.end;
function W(i,word,nth){const ws=CU.words.filter(w=>w.win===i&&nrm(w.text)===nrm(word)),w=ws[(nth||1)-1];if(!w){console.warn('CUE_MISSING '+i+' '+word);return Ts(i);}return w.s;}
const fr=(a,b,k)=>a+(b-a)*k;
let crownNow=-CLEAR,armNow=0,tNow=0;

/* ---------- post-injection spray and fuel vapour ---------- */
const postMat=makeDropMat({win:[-100,1,0,2.0],L:[38,11.5],V:[80,58],life:[0.8,0.3],slide:16,colA:[1,0.82,0.4],colB:[0.97,0.94,0.82],gain:0.9});
{const p=new T.Points(DROPGEO,postMat);p.frustumCulled=false;model.add(p);}
const vaporMat=gasMat(1);
{const p=new T.Points(GASGEO,vaporMat);p.frustumCulled=false;model.add(p);}
vaporMat.uniforms.uSize.value=3.4;vaporMat.uniforms.uB0.value.copy(PORT.ex.throat);vaporMat.uniforms.uB1.value.copy(PORT.ex.bend);vaporMat.uniforms.uB2.value.copy(PORT.ex.mouth);vaporMat.uniforms.uValveR.value=RV_EX+0.9;
vaporMat.uniforms.uColor.value.setRGB(1.0,0.74,0.22);
let cumPost=0;

/* ---------- exhaust line: pipe, oxidation catalyst (DOC), particulate filter (DPF) ---------- */
const EX0=HALF_W,EY=31,DOC=[92,160],DPF=[180,338],BR=59.6,NCH=12,PITCH=2*BR/NCH,PLUG=7;
const exh=new T.Group();model.add(exh);
const sootMeshes=[],sootMat=new T.MeshBasicMaterial({color:0x0b0b0d,toneMapped:false});
let docGlow,dpfGlow,docSprite,dpfSprite,docFaceMat;
(function(){
  const X=y=>EX0+y;
  const shell=revolved([[11.9,0],[11.9,50],[62.4,83],[62.4,347],[14.4,381],[14.4,440],[12,440],[12,380],[60,346],[60,84],[9.5,50],[9.5,0]],std(0x858c94,.95,.34),cut(0x5f6771,HA),{seg:44});
  shell.rotation.z=-Math.PI/2;shell.position.set(EX0,EY,0);exh.add(shell);
  [84,346].forEach(y=>{const c=revolved([[62.4,y-4],[66.5,y-4],[66.5,y+4],[62.4,y+4]],std(0x4f565d,.9,.42),cut(0x3d444c,HB),{seg:44});c.rotation.z=-Math.PI/2;c.position.set(EX0,EY,0.01);exh.add(c);});
  const brick=std(0xb3ab9c,.05,.92,{envMapIntensity:.25});
  [DOC,DPF].forEach(b=>{const m=new T.Mesh(latheGeo([[0.001,b[0]],[BR,b[0]],[BR,b[1]],[0.001,b[1]]],{closed:false,seg:44}),brick);m.rotation.z=-Math.PI/2;m.position.set(EX0,EY,0);exh.add(m);});
  const rect=(x0,y0,x1,y1,mat,z)=>{const m=new T.Mesh(polyGeo([[x0,y0],[x1,y0],[x1,y1],[x0,y1]]),mat);m.position.z=z;exh.add(m);return m;};
  /* DOC cut face: straight-through channels */
  const c1=document.createElement('canvas');c1.width=8;c1.height=32;const g1=c1.getContext('2d');g1.fillStyle='#a89f8d';g1.fillRect(0,0,8,32);g1.fillStyle='#4a453c';g1.fillRect(0,0,8,7);
  const t1=new T.CanvasTexture(c1);t1.wrapS=t1.wrapT=T.RepeatWrapping;t1.repeat.set(1/8,1/4.5);t1.anisotropy=4;
  const docFace=rect(X(DOC[0]),EY-BR,X(DOC[1]),EY+BR,new T.MeshBasicMaterial({map:t1,toneMapped:false}),0.02);edges(exh,docFace.geometry,0.03);docFaceMat=docFace.material;
  /* DPF cut face: wall-flow channels, plugged at alternate ends */
  const dpfFace=rect(X(DPF[0]),EY-BR,X(DPF[1]),EY+BR,flat(0xc4bdae),0.02);edges(exh,dpfFace.geometry,0.03);
  const chan=flat(0x1b1e23),hh=PITCH/2-0.9;
  for(let i=0;i<NCH;i++){
    const yc=EY-BR+(i+0.5)*PITCH,inlet=i%2===0;
    rect(X(DPF[0]+(inlet?0:PLUG)),yc-hh,X(DPF[1]-(inlet?PLUG:0)),yc+hh,chan,0.03);
    if(inlet){const m=new T.Mesh(new T.PlaneGeometry(1,1),sootMat);m.position.set(0,yc,0.04);m.userData={x1:X(DPF[1]-PLUG),len:DPF[1]-DPF[0]-PLUG,h:hh*2};exh.add(m);sootMeshes.push(m);}
  }
  const add=new T.MeshBasicMaterial({color:0xff5a0c,transparent:true,opacity:0,blending:T.AdditiveBlending,depthWrite:false,toneMapped:false});
  docGlow=rect(X(DOC[0]),EY-BR,X(DOC[1]),EY+BR,add,0.06).material;
  dpfGlow=rect(X(DPF[0]),EY-BR,X(DPF[1]),EY+BR,add.clone(),0.06).material;
  const sp=(x,sx,sy)=>{const s=new T.Sprite(new T.SpriteMaterial({map:glowTex,blending:T.AdditiveBlending,depthTest:false,depthWrite:false,transparent:true,opacity:0,toneMapped:false}));s.position.set(x,EY,6);s.scale.set(sx,sy,1);s.renderOrder=10;exh.add(s);return s;};
  docSprite=sp(X((DOC[0]+DOC[1])/2),190,210);dpfSprite=sp(X((DPF[0]+DPF[1])/2),330,230);
})();
/* gas stream through the line (CPU particles, a pure function of time) */
const NSTR=1300,strSeed=[],strPos=new Float32Array(NSTR*3),strCol=new Float32Array(NSTR*4),strSize=new Float32Array(NSTR);
for(let i=0;i<NSTR;i++){const r=rnd(),ch=Math.floor(rnd()*6)*2;strSeed.push({p0:rnd(),a:rnd()*2-1,b:rnd(),kind:r<0.62?0:(r<0.74?1:2),ch,out:ch===0?1:(rnd()<0.5?ch+1:ch-1),cross:rnd(),sp:0.85+0.3*rnd(),j:rnd()-0.5});}
const strGeo=new T.BufferGeometry();strGeo.setAttribute('position',new T.BufferAttribute(strPos,3));strGeo.setAttribute('aCol',new T.BufferAttribute(strCol,4));strGeo.setAttribute('aSize',new T.BufferAttribute(strSize,1));
const strMat=new T.ShaderMaterial({transparent:true,depthWrite:false,uniforms:{uScale:shared.uScale,uPix:shared.uPix},
  vertexShader:'attribute vec4 aCol;attribute float aSize;uniform float uScale,uPix;varying vec4 vC;void main(){vC=aCol;vec4 mv=modelViewMatrix*vec4(position,1.0);gl_Position=projectionMatrix*mv;if(aCol.a<0.01)gl_Position=vec4(2.0,2.0,2.0,1.0);gl_PointSize=max(aSize*uScale/-mv.z,1.2*uPix);}',
  fragmentShader:'varying vec4 vC;void main(){vec2 c=gl_PointCoord-0.5;float d=dot(c,c)*4.0;if(d>1.0)discard;gl_FragColor=vec4(vC.rgb,vC.a*pow(1.0-d,1.3));}'});
{const p=new T.Points(strGeo,strMat);p.frustumCulled=false;exh.add(p);}
const radAt=y=>y<50?8.2:(y<84?lerp(8.2,56,(y-50)/34):(y<346?56:(y<380?lerp(56,10.5,(y-346)/34):10.5)));
function updateExhaust(t,S){
  for(let i=0;i<NSTR;i++){
    const q=strSeed[i],s=((q.p0+S.phase*q.sp)%1+1)%1,y=-12+s*452,R=radAt(y);
    let yo=q.a*R;
    const inDoc=sst(DOC[0]-6,DOC[0],y)*(1-sst(DOC[1],DOC[1]+6,y)),inDpf=sst(DPF[0]-8,DPF[0],y)*(1-sst(DPF[1],DPF[1]+8,y));
    if(inDoc>0)yo=lerp(yo,Math.round(q.a*56/4.5)*4.5,inDoc);
    let cr=0;
    if(inDpf>0){const yin=-BR+(q.ch+0.5)*PITCH,yout=-BR+(q.out+0.5)*PITCH,yc=DPF[0]+20+q.cross*(DPF[1]-DPF[0]-46);cr=sst(yc-6,yc+6,y);yo=lerp(yo,lerp(yin,yout,cr)+q.j*3.2,inDpf);}
    const hollow=1-Math.max(inDoc,inDpf),k3=i*3,k4=i*4;
    strPos[k3]=EX0+y;strPos[k3+1]=EY+yo;strPos[k3+2]=lerp(0.9,-q.b*R*0.75,hollow);
    const ends=sst(0,0.03,s)*(1-sst(0.955,1,s));let r,g,b,a,sz;
    if(q.kind===0){const hot=S.doc*sst(DOC[0]+20,DOC[1],y);r=lerp(0.62,1.0,hot);g=lerp(0.6,0.56,hot);b=lerp(0.58,0.2,hot);a=lerp(0.3,0.5,hot);sz=3.0;}
    else if(q.kind===1){r=0.05;g=0.05;b=0.06;a=0.8*S.sootFlow*(1-cr)*(1-sst(DPF[1]-4,DPF[1]+2,y));sz=1.3;}
    else{const ox=sst(DOC[0]+6,DOC[1]-6,y);r=1;g=lerp(0.76,0.97,ox);b=lerp(0.24,0.75,ox);a=0.9*S.vapor*(s<S.vfront?1:0)*(1-sst(DOC[0]+26,DOC[1]-2,y));sz=lerp(2.3,3.6,ox);}
    strCol[k4]=r;strCol[k4+1]=g;strCol[k4+2]=b;strCol[k4+3]=a*ends;strSize[i]=sz;
  }
  strGeo.attributes.position.needsUpdate=true;strGeo.attributes.aCol.needsUpdate=true;strGeo.attributes.aSize.needsUpdate=true;
  const soot=clamp(S.soot,0,1),burn=clamp(S.burn,0,1);
  sootMeshes.forEach((m,i)=>{const d=m.userData,len=Math.max(0.01,d.len*clamp(soot*(0.9+0.2*Math.sin(i*2.3)),0,1));m.scale.set(len,d.h,1);m.position.x=d.x1-len/2;});
  sootMat.color.setRGB(lerp(0.045,1.0,burn),lerp(0.045,0.3,burn),lerp(0.05,0.04,burn));
  docFaceMat.color.setRGB(1,lerp(1,0.5,S.doc),lerp(1,0.16,S.doc));
  docGlow.opacity=0.2*S.doc;dpfGlow.opacity=0.07*burn+0.04*S.doc;docSprite.material.opacity=0.24*S.doc;dpfSprite.material.opacity=0.17*burn;
}

/* ---------- timeline of the reel ---------- */
const HK=Ts(2)-0.45,TDASH=W(21,'nu')-.1,KNOCKS=[W(7,'bate'),W(20,'bate')];
const SEG=[
  {t0:0,t1:fr(0,HK,.05),u0:6.84,u1:6.92,m:'R'},{t0:fr(0,HK,.05),t1:fr(0,HK,.25),u0:6.92,u1:7.6,m:'R'},{t0:fr(0,HK,.25),t1:fr(0,HK,.31),u0:7.6,u1:8.6,m:'R'},
  {t0:fr(0,HK,.31),t1:fr(0,HK,.60),u0:8.6,u1:10.4,m:'R'},{t0:fr(0,HK,.60),t1:fr(0,HK,.72),u0:10.4,u1:14.66,m:'R'},{t0:fr(0,HK,.72),t1:fr(0,HK,.93),u0:14.66,u1:15.12,m:'R'},{t0:fr(0,HK,.93),t1:HK,u0:15.12,u1:15.5,m:'R'},
  {t0:HK,t1:W(3,'injectorul'),u0:1.4,u1:4.9},
  {t0:W(3,'injectorul'),t1:Te(3)+.15,u0:6.6,u1:7.5},{t0:Te(3)+.15,t1:Te(4)+.15,u0:7.5,u1:8.5},{t0:Te(4)+.15,t1:Te(5)+.15,u0:8.5,u1:10.3},{t0:Te(5)+.15,t1:Ts(7)-.05,u0:10.3,u1:13.9},
  {t0:Ts(7)-.05,t1:W(7,'dozată'),u0:6.5,u1:8.62,m:'K'},{t0:W(7,'dozată'),t1:W(7,'bate'),u0:8.62,u1:9.52,m:'K'},{t0:W(7,'bate'),t1:Ts(8)-.45,u0:9.52,u1:11.4,m:'K'},
  {t0:Ts(8)-.45,t1:Ts(10),u0:5.4,u1:6.5},{t0:Ts(10),t1:W(10,'și'),u0:8.45,u1:9.25},{t0:W(10,'și'),t1:Te(10)+.15,u0:9.25,u1:9.95},{t0:Te(10)+.15,t1:Ts(12)-.45,u0:9.95,u1:14.4},
  {t0:Ts(12)-.45,t1:Ts(14)-.05,crank:[560,95]},
  {t0:Ts(14)-.05,t1:W(14,'pulverizează'),u0:13.2,u1:14.66,m:'R'},{t0:W(14,'pulverizează'),t1:Te(14)+.2,u0:14.66,u1:15.02,m:'R'},{t0:Te(14)+.2,t1:Te(15)+.15,u0:15.02,u1:15.3,m:'R'},
  {t0:Te(15)+.15,t1:W(16,'și'),u0:15.3,u1:16.95,m:'R'},{t0:W(16,'și'),t1:Ts(19)-.5,crank:[700,110],m:'R'},
  {t0:Ts(19)-.5,t1:Ts(20)-.05,crank:[200,100]},
  {t0:Ts(20)-.05,t1:W(20,'bate'),u0:8.7,u1:9.52,m:'K'},{t0:W(20,'bate'),t1:Ts(21)-.05,u0:9.52,u1:11.3,m:'K'},
  {t0:Ts(21)-.05,t1:END+2,crank:[120,100]}
];
const DIPS=[HK,Ts(7)-.05,Ts(8)-.45,Ts(12)-.45,Ts(14)-.05,Ts(19)-.5,Ts(20)-.05,Ts(21)-.05];
const TH_N=3440,thLut=new Float32Array(TH_N+1);for(let i=0;i<=TH_N;i++)thLut[i]=thetaOf(i/200);
function uOfTheta(th){th=((th%720)+720)%720;let lo=0,hi=TH_N;while(hi-lo>1){const m=(lo+hi)>>1;if(thLut[m]<=th)lo=m;else hi=m;}return (lo+(th-thLut[lo])/Math.max(1e-6,thLut[hi]-thLut[lo]))/200;}
function stateAt(t){
  let s=SEG[SEG.length-1];for(const x of SEG){if(t<x.t1){s=x;break;}}
  const u=s.crank?uOfTheta(s.crank[0]+s.crank[1]*(t-s.t0)):lerp(s.u0,s.u1,clamp((t-s.t0)/(s.t1-s.t0),0,1));
  return {u:clamp(u,0,TOTAL-0.001),regen:s.m==='R',knock:s.m==='K'};
}
function track(tr,t){let i=0;while(i<tr.length-2&&t>tr[i+1][0])i++;const a=tr[i],b=tr[i+1];return lerp(a[1],b[1],sst(a[0],b[0],t));}
const TR={
  soot:[[0,.5],[Ts(13),.86],[Ts(14),.95],[W(17,'iar'),.95],[Te(17)+.2,.42],[Ts(19)-.6,.06],[Ts(21),.3],[END,1.0],[END+2,1.0]],
  burn:[[0,0],[W(17,'iar')-.2,0],[W(17,'funinginea')+.7,1],[Te(18),.95],[Ts(19)-.45,0],[END+2,0]],
  doc:[[0,0],[W(16,'și'),0],[Te(16)+.25,1],[Te(18),1],[Ts(19)-.4,0],[END+2,0]],
  temp:[[0,240],[W(16,'și'),250],[Ts(17),300],[W(17,'600')+.5,615],[W(17,'iar'),640],[Te(18),655],[Ts(19)-.45,655],[Ts(19)-.4,300],[END+2,280]],
  vapor:[[0,0],[Ts(16)+.4,0],[Ts(16)+.9,1],[Te(18),1],[Ts(19)-.45,0],[END+2,0]],
  vfront:[[0,0],[Ts(16)+.4,0],[Te(16)+.5,1.3],[END+2,1.3]],
  flowv:[[0,1],[Ts(21),1],[END,.22],[END+2,.2]],
  strip:[[0,0],[HK+.9,0],[HK+1.5,1],[W(16,'și')-.15,1],[W(16,'și')+.2,0],[Ts(19)-.56,0],[Ts(19)-.46,1],[TDASH-.3,1],[TDASH,0],[END+2,0]],
  top:[[0,720],[HK-.3,720],[HK+.9,470],[END+2,470]],
  tempVis:[[0,0],[W(16,'și')-.1,0],[W(16,'și')+.4,1],[Ts(19)-.75,1],[Ts(19)-.5,0],[END+2,0]],
  clog:[[0,0],[END+2,0]]
};
/* phase of the gas stream = integral of its speed, so a clogging filter visibly slows the flow */
const PH_N=Math.ceil((END+2)*60),phLut=new Float32Array(PH_N+1);for(let i=1;i<=PH_N;i++)phLut[i]=phLut[i-1]+0.2*track(TR.flowv,i/60)/60;
const phaseAt=t=>{const x=clamp(t,0,END+2)*60,i=Math.min(PH_N-1,Math.floor(x));return phLut[i]+(phLut[i+1]-phLut[i])*(x-i);};

/* ---------- labels ---------- */
const labelDefs=[],svg=$('leaders'),labBox=$('labels');
function addLabel(text,sub,anchor,side,dx,dy,vis,cls){
  const el=document.createElement('div');el.className='lb'+(side<0?' l':'')+(cls?' '+cls:'');el.textContent=text;
  if(sub){const s=document.createElement('small');s.textContent=sub;el.appendChild(s);}
  labBox.appendChild(el);
  const ln=document.createElementNS('http://www.w3.org/2000/svg','line'),dot=document.createElementNS('http://www.w3.org/2000/svg','circle');
  dot.setAttribute('r','5');svg.appendChild(ln);svg.appendChild(dot);
  const L={el,ln,dot,anchor,side,dx,dy,vis,w:0,h:0};labelDefs.push(L);return L;
}
const win=(a,b,fi,fo)=>t=>pulse(t,a,a+(fi||.35),b-(fo||.3),b);
addLabel('Aer comprimat','se încinge la peste 500 °C',()=>[-16,crownNow+ -2,0],-1,26,-16,win(HK+2.4,W(3,'injectorul')+.3));
addLabel('Preinjecție','cantitate foarte mică',()=>[9,-5,0],1,13,-7,win(W(3,'trimite'),Ts(4)+.45));
addLabel('Acul se ridică o clipă',null,()=>[-1.9,13,0],-1,12,0,win(W(3,'trimite')-.3,Te(3)+.4));
addLabel('Flacăra preinjecției','încălzește camera de ardere',()=>[-9,-7.5,0],-1,9,-9,win(Ts(4)+.5,Te(4)+.2));
addLabel('Injecția principală','arde progresiv',()=>[10,-5,0],1,12,-8,win(Ts(5)+.9,Te(5)+.1));
addLabel('Înaltă presiune','de la rampă',()=>[29.5,93.4,0],1,7,-9,win(Ts(8)+.9,Ts(10)+.6));
addLabel('Bobină',null,()=>[-8.8,105,0],-1,20,0,win(Ts(8)+1.0,Ts(10)+.4));
addLabel('Ac',null,()=>[-1.8,13,0],-1,24,0,win(Ts(8)+1.1,Ts(10)+.4));
addLabel('Duză',null,()=>[3.6,10,0],1,22,-4,win(Ts(8)+1.2,Ts(10)+.4));
addLabel('~2.000 bar',null,()=>[4.75,30.5,0],1,9,2,win(W(10,'aproape'),W(10,'și')+.2),'num');
addLabel('Orificii de ~0,1 mm',null,()=>[2.5,-1.9,0],-1,7,-5.5,win(W(10,'sparge'),Te(10)+.1));
addLabel('Picături de câțiva microni',null,()=>[15,-6.3,0],1,3,5.5,win(W(10,'picături')-.1,Te(10)+.2));
addLabel('Catalizator','de oxidare',()=>[EX0+118,EY+BR+7,0],-1,4,15,win(Ts(13)+1.2,Ts(14)-.2));
addLabel('Filtru de particule','DPF',()=>[EX0+300,EY+BR+7,0],1,4,15,win(Ts(13)+1.3,Ts(14)-.2));
addLabel('Funingine',null,()=>[EX0+296,EY-BR+PITCH*0.5,0],1,2,-16,win(Ts(13)+1.8,Ts(14)-.2));
addLabel('Postinjecție','târzie, fără flacără',()=>[20,-8,0],1,14,-12,win(W(14,'pulverizează')+.2,Te(15)+.1));
addLabel('Piston jos',null,()=>[39,crownNow-5,0],1,4,-6,win(W(14,'târziu'),Te(15)));
addLabel('Vapori de motorină',null,()=>[EX0+22,EY,0],1,6,-20,win(Ts(16)+.5,Te(16)-.2));
addLabel('Motorina arde aici',null,()=>[EX0+126,EY+BR+7,0],1,-22,13,win(W(16,'și')+.5,W(17,'iar')+.2));
addLabel('Funinginea arde',null,()=>[EX0+280,EY+BR+7,0],1,-16,11,win(W(17,'funinginea')-.1,W(18,'regenerarea')));
addLabel('Injector uzat?',null,()=>[11.5,74,0],1,18,6,win(Ts(19)+.3,Ts(20)-.3));
addLabel('Funinginea se adună',null,()=>[EX0+280,EY+BR+7,0],1,-16,11,win(Ts(21)+1.0,END+.6));
const tempEl=$('temp'),tempVal=$('tempV'),tempBar=$('tempBar'),clogEl=$('clog');

/* ---------- camera ---------- */
const SHOTS={
  wide:{c:[5,-24],w:156,h:236,az:22,el:8},inj:{c:[4,64],w:74,h:156,az:-14,el:4,pb:640},noz:{c:[0,3],w:64,h:50,az:14,el:13},macro:{c:[9,-5.5],w:38,h:26,az:10,el:12},
  mid:{c:[5,-44],w:172,h:206,az:26,el:11},cyl:{c:[4,-48],w:150,h:156,az:20,el:10},cylh:{c:[2,-36],w:112,h:104,az:18,el:9},port:{c:[74,16],w:130,h:100,az:6,el:9},
  dpf:{c:[EX0+214,EY],w:282,h:150,az:5,el:9},dpfc:{c:[EX0+252,EY],w:206,h:150,az:5,el:10}
};
const CAM=[
  [0,'noz'],[fr(0,HK,.58),'noz'],[fr(0,HK,.73),'cylh'],[HK-.001,'cylh'],
  [HK,'wide'],[W(3,'injectorul')-1.3,'wide'],[W(3,'injectorul')+.5,'noz'],[Ts(6)+.2,'noz'],[Ts(6)+1.5,'mid'],[Ts(7)-.051,'mid'],
  [Ts(7)-.05,'noz'],[Ts(8)-.451,'noz'],
  [Ts(8)-.45,'inj'],[Ts(10)+.25,'inj'],[W(10,'bari'),'noz'],[W(10,'și')+.05,'noz'],[W(10,'picături'),'macro'],[Te(10)+.2,'macro'],[Ts(11)+.7,'noz'],[Ts(11)+1.8,'mid'],[Ts(12)-.451,'mid'],
  [Ts(12)-.45,'wide'],[Ts(13)-.1,'wide'],[Ts(13)+1.3,'dpf'],[Ts(14)-.051,'dpf'],
  [Ts(14)-.05,'cyl'],[Te(15)+.15,'cyl'],[Ts(16)+1.0,'port'],[W(16,'și')+.2,'port'],[Te(16)+.25,'dpf'],[W(17,'iar')-.1,'dpf'],[W(17,'funinginea')+.6,'dpfc'],[Ts(19)-.501,'dpfc'],
  [Ts(19)-.5,'inj'],[Ts(20)-.051,'inj'],
  [Ts(20)-.05,'noz'],[Ts(21)-.051,'noz'],
  [Ts(21)-.05,'dpf'],[END+2,'dpfc']
];
const VW=1080,VH=1920,PADBOT=VH-1500,LABBOT=1250;let padTop=470,pxPerMm=1;
const camTarget=new T.Vector3(),tmpV=new T.Vector3();
function shotAt(t){
  let i=0;while(i<CAM.length-2&&t>CAM[i+1][0])i++;
  const a=SHOTS[CAM[i][1]],b=SHOTS[CAM[i+1][1]],k=sst(CAM[i][0],CAM[i+1][0],t);
  return {cx:lerp(a.c[0],b.c[0],k),cy:lerp(a.c[1],b.c[1],k),w:lerp(a.w,b.w,k),h:lerp(a.h,b.h,k),az:lerp(a.az,b.az,k),el:lerp(a.el,b.el,k),pb:lerp(a.pb||PADBOT,b.pb||PADBOT,k)};
}
function placeCamera(t){
  const s=shotAt(t),tf=Math.tan(FOV*DEG/2),aspect=VW/VH,safeH=VH-padTop-s.pb,safeW=VW-64;
  const d=Math.max((s.h/2)/tf*(VH/safeH),(s.w/2)/(tf*aspect)*(VW/safeW)),az=s.az*DEG,el=s.el*DEG;
  camTarget.set(s.cx,s.cy,0);
  camera.position.set(camTarget.x+d*Math.sin(az)*Math.cos(el),camTarget.y+d*Math.sin(el),d*Math.cos(az)*Math.cos(el));
  camera.lookAt(camTarget);
  camera.updateMatrixWorld();tmpV.setFromMatrixColumn(camera.matrixWorld,1);
  camera.position.addScaledVector(tmpV,((padTop-s.pb)/2)/VH*(2*d*tf));
  for(const k of KNOCKS){const q=t-k;if(q>=0&&q<0.7){const a=d*0.011*Math.exp(-q*6.5);camera.position.x+=a*Math.sin(q*96);camera.position.y+=a*Math.cos(q*77);}}
  camera.updateMatrixWorld();
  pxPerMm=VH/(2*d*tf);shared.uScale.value=VH*DPR/(2*tf);
}
function placeLabels(t){
  for(const L of labelDefs){
    let o=L.vis(t);
    if(o>=0.02){const a=L.anchor();tmpV.set(a[0],a[1],a[2]).project(camera);L.sx=(tmpV.x*0.5+0.5)*VW;L.sy=(-tmpV.y*0.5+0.5)*VH;o*=sst(padTop-30,padTop+20,L.sy)*(1-sst(LABBOT+10,LABBOT+60,L.sy));}
    if(o<0.02){L.el.style.opacity=0;L.ln.style.opacity=0;L.dot.style.opacity=0;continue;}
    const x=L.sx,y=L.sy;if(!L.w){L.w=L.el.offsetWidth;L.h=L.el.offsetHeight;}
    const dx=clamp(L.dx*pxPerMm,30,260),ty=clamp(y-L.dy*pxPerMm,padTop+L.h/2+8,LABBOT-L.h/2);let ex,lx;
    if(L.side>0){lx=Math.min(x+dx,VW-L.w-(ty>800?112:34));ex=lx;}else{ex=Math.max(x-dx,L.w+34);lx=ex-L.w;}
    L.el.style.transform='translate('+lx.toFixed(1)+'px,'+(ty-L.h/2).toFixed(1)+'px)';
    L.el.style.opacity=o;L.ln.style.opacity=o;L.dot.style.opacity=o;
    L.ln.setAttribute('x1',x.toFixed(1));L.ln.setAttribute('y1',y.toFixed(1));L.ln.setAttribute('x2',ex.toFixed(1));L.ln.setAttribute('y2',ty.toFixed(1));
    L.dot.setAttribute('cx',x.toFixed(1));L.dot.setAttribute('cy',y.toFixed(1));
  }
}

/* ---------- injection timing strip (crank angle around firing TDC) ---------- */
const strip=$('strip'),SW=940;
const sx=a=>a<=40?(a+40)/80*0.5*SW:0.5*SW+(a-40)/165*0.5*SW;
const EVS=[['pre',-14,-10,38,'PRE'],['main',-4,9,84,'PRINCIPALĂ'],['post',150,168,44,'POST']],evEl={};
EVS.forEach(e=>{const d=document.createElement('div');d.className='ev '+e[0];d.style.left=sx(e[1])+'px';d.style.width=Math.max(12,sx(e[2])-sx(e[1]))+'px';d.style.height=e[3]+'px';strip.appendChild(d);
  const l=document.createElement('span');l.className='evl '+e[0];l.textContent=e[4];l.style.left=(e[0]==='pre'?sx(e[2])+3:(e[0]==='main'?sx(e[1]):sx(e[1])+Math.max(12,sx(e[2])-sx(e[1]))/2))+'px';strip.appendChild(l);evEl[e[0]]=[d,l];});
[[0,'PMI'],[180,'PME']].forEach(k=>{const d=document.createElement('i');d.className='tick';d.style.left=sx(k[0])+'px';d.dataset.l=k[1];strip.appendChild(d);});
const head=document.createElement('b');head.className='head';strip.appendChild(head);
function updateStrip(u,t,s){
  const pMiss=t>=Ts(21)-.05;
  strip.parentNode.style.opacity=track(TR.strip,t);
  const a=thetaOf(u)-360;head.style.opacity=(a>-40&&a<205)?1:0;head.style.transform='translateX('+sx(clamp(a,-40,205)).toFixed(1)+'px)';
  const act={pre:!MODE.nopilot&&u>6.85&&u<7.5,main:u>8.66&&u<10.9,post:MODE.regen&&u>PO0-0.02&&u<PO1+0.06};
  EVS.forEach(e=>{const on=act[e[0]];evEl[e[0]][0].classList.toggle('on',on);evEl[e[0]][1].classList.toggle('on',on);});
  evEl.post[0].classList.toggle('ghost',!MODE.regen&&!pMiss);evEl.post[0].classList.toggle('miss',pMiss);evEl.post[1].classList.toggle('miss',pMiss);evEl.pre[0].classList.toggle('miss',!!MODE.nopilot);evEl.pre[1].classList.toggle('miss',!!MODE.nopilot);
}

/* ---------- per-frame state ---------- */
const AIR_COLD=new T.Color(0.49,0.80,1.0),AIR_HOT=new T.Color(1.0,0.45,0.36),GAS_HOT=new T.Color(1.0,0.55,0.2),GAS_COLD=new T.Color(0.62,0.6,0.58);
for(let i=1;i<=240;i++)cumPost+=0; // (post flow phase is short; computed inline below)
function apply(u){
  const th=thetaOf(u),crown=-CLEAR-pistonDrop(th);crownNow=crown;
  piston.position.y=crown;rod.position.y=crown-COMP_H;rod.rotation.z=Math.asin(CRK*Math.sin(th*DEG)/ROD);
  const li=vLift(th,712,222),le=vLift(th,498,8);
  vIn.g.position.y=-li;vEx.g.position.y=-le;
  setHelix(vIn.sp.geometry,HEAD_H+1.3,22.4-li);setHelix(vEx.sp.geometry,HEAD_H+1.3,22.4-le);
  const s=sig(u),nl=s.needle*NEEDLE_LIFT,bl=s.ball*BALL_LIFT;
  needle.position.y=nl;setHelix(needleSpring,49.35+nl,8.2-nl);
  ball.position.y=83.76+bl;arm.position.y=bl;armNow=bl;setHelix(solSpring,101.4+bl,11-bl);
  coilGlow.opacity=s.sol*0.2;
  fill.ctl.material.color.copy(FUEL_RET).lerp(FUEL_HP,clamp((s.pc-0.2)/0.8,0,1));
  fill.sac.material.color.copy(FUEL_DIM).lerp(FUEL_HP,clamp(s.needle,0,1));
  const post=MODE.regen?sst(PO0,PO1+0.03,u)*3.2:0;
  const fm=clamp(s.needle,0,1),fc=clamp(s.ball+0.6*s.refill,0,1),pm=lut(cumMain,u)*9.0+post,pcx=lut(cumCtl,u)*7.0+post*0.8;
  ribbons.supply.uFlow.value=Math.max(fm,0.45*fc);ribbons.supply.uPhase.value=pm+0.4*pcx;
  ['annR','annL'].forEach(k=>{ribbons[k].uFlow.value=fm;ribbons[k].uPhase.value=pm;});
  ['seatR','seatL','holeR','holeL'].forEach(k=>{ribbons[k].uFlow.value=fm;ribbons[k].uPhase.value=pm;ribbons[k].uAlpha.value=fm;});
  ['zThr','aThr'].forEach(k=>{ribbons[k].uFlow.value=fc;ribbons[k].uPhase.value=pcx;});
  ribbons.aThr.uAlpha.value=clamp(s.ball*1.5,0,1);
  ['ret0','ret1'].forEach(k=>{ribbons[k].uFlow.value=clamp(s.ball,0,1);ribbons[k].uPhase.value=pcx*0.8;ribbons[k].uAlpha.value=clamp(s.ball*1.4,0,1);});
  coreMat.opacity=fm*0.8;cores.forEach(c=>c.scale.set(1,0.25+0.75*fm,1));
  shared.uT.value=u;shared.uCrown.value=crown;shared.uSwirl.value=u*(4*Math.PI/TOTAL);shared.uSquish.value=1-sst(1.6,17,-crown);
  dropMat.uniforms.uTd.value=u;dropMat.uniforms.uWin.value.x=MODE.nopilot?-100:WIN.pilotDrop[0];dropMat.uniforms.uLife.value.x=MODE.harsh?1.0:0.36;
  postMat.uniforms.uTd.value=MODE.regen?(u-PO0)*9.0:-50;
  flameMat.uniforms.uFw.value.set(MODE.nopilot?-100:WIN.pilotFlame[0],WIN.pilotFlame[1],MODE.harsh?9.5:WIN.mainFlame[0],MODE.harsh?0.45:WIN.mainFlame[1]);
  flameMat.uniforms.uGain.value=(0.085+0.075*sst(11.7,12.9,u))*(MODE.harsh?1.9:1);
  const tm=thermo(Math.min(th,352)),heat=th>180&&th<=540?sst(360,880,tm.Tk):0;
  airMat.uniforms.uP.value=th<360?th/172:3;
  airMat.uniforms.uAlpha.value=(0.62-0.3*heat)*(1-sst(MODE.harsh?9.45:8.95,MODE.harsh?9.7:10.7,u));
  airMat.uniforms.uColor.value.copy(AIR_COLD).lerp(AIR_HOT,heat);
  airMat.uniforms.uValve.value.set(-XV,-li-0.5,0);
  const ue=u>=14.65?(u-14.65)/2.45:(u<1.3?(u+TOTAL-14.65)/2.45:-1);
  burntMat.uniforms.uP.value=ue;
  burntMat.uniforms.uAlpha.value=0.2*(u<1.3?1:sst(11.2,13.4,u));
  burntMat.uniforms.uColor.value.copy(GAS_HOT).lerp(GAS_COLD,u<1.3?1:sst(12.9,14.6,u));
  burntMat.uniforms.uValve.value.set(XV,-le-0.5,0);
  vaporMat.uniforms.uP.value=ue;vaporMat.uniforms.uValve.value.set(XV,-le-0.5,0);
  vaporMat.uniforms.uAlpha.value=MODE.regen?0.4*(u<1.3?1:sst(PO0+0.05,PO1+0.22,u)):0;
  const b=burnOf(u),cy=Math.max(crown*0.5-3,-34);
  fire.intensity=1.5*b;fire.position.set(0,cy,8);
  glow.material.opacity=0.17*b;glow.position.set(0,cy-2,-8);const gs=46+26*b+Math.min(-crown,60)*0.9;glow.scale.set(gs,gs*0.72,1);
}

/* ---------- frame API ---------- */
const dipEl=$('dip');
function frame(t){
  tNow=t;const st=stateAt(t);MODE.regen=st.regen?1:0;MODE.nopilot=st.knock?1:0;MODE.harsh=st.knock?1:0;
  padTop=track(TR.top,t);
  apply(st.u);
  updateExhaust(t,{phase:phaseAt(t),soot:track(TR.soot,t),burn:track(TR.burn,t),doc:track(TR.doc,t),vapor:track(TR.vapor,t),vfront:track(TR.vfront,t),sootFlow:lerp(1,0.55,track(TR.doc,t))});
  placeCamera(t);placeLabels(t);updateStrip(st.u,t,st);
  /* temperature read-out and clog warning, anchored on the filter */
  const tv=track(TR.tempVis,t);tempEl.style.opacity=tv;
  if(tv>0.01){const Tc=track(TR.temp,t),T_=Math.round(Tc/5)*5;tempVal.textContent=T_+' °C';tempEl.classList.toggle('hot',T_>=600);tempBar.style.width=(clamp((Tc-200)/500,0,1)*100).toFixed(1)+'%';}
  const cg=track(TR.clog,t);clogEl.style.opacity=cg;
  if(cg>0.01){tmpV.set(EX0+259,EY-BR-6,0).project(camera);clogEl.style.transform='translate('+((tmpV.x*0.5+0.5)*VW-190).toFixed(1)+'px,'+((-tmpV.y*0.5+0.5)*VH+30).toFixed(1)+'px)';}
  let dp=0;for(const c of DIPS)dp=Math.max(dp,1-Math.abs(t-c)/0.2);dipEl.style.opacity=clamp(dp,0,1);
  renderer.render(scene,camera);
}
renderer.setSize(VW,VH,false);camera.aspect=VW/VH;camera.updateProjectionMatrix();svg.setAttribute('viewBox','0 0 '+VW+' '+VH);
window.__frame=frame;window.__end=END;
window.__probe=t=>{const st=stateAt(t);MODE.regen=st.regen?1:0;MODE.nopilot=st.knock?1:0;MODE.harsh=st.knock?1:0;const s=sig(st.u),th=thetaOf(st.u);
  return [s.needle,burnOf(st.u),st.knock?1:0,track(TR.doc,t),track(TR.burn,t),th,(MODE.regen&&st.u>PO0-0.05&&st.u<PO1+0.1)?1:0,vLift(th,498,8),vLift(th,712,222)];};
if(QS.get('guides')){const g=document.createElement('div');g.style.cssText='position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none';
  g.innerHTML='<div style="position:absolute;left:80px;top:1290px;width:860px;height:240px;border:3px dashed #0f0;color:#0f0;font:700 26px JB">SUBTITRARI</div><div style="position:absolute;left:150px;top:197px;width:780px;height:50px;border:3px dashed #0ff"></div><div style="position:absolute;left:950px;top:820px;width:130px;height:680px;border:3px dashed #f0f"></div><div style="position:absolute;left:0;top:1560px;width:1080px;height:360px;border:3px dashed #f0f"></div><div id="gHook" style="position:absolute;left:40px;top:150px;width:1000px;height:560px;border:3px dashed #ff0"></div>';document.body.appendChild(g);}
window.__info={HK,end:END,hook:{pilot:fr(0,HK,.07),main:fr(0,HK,.34),post:fr(0,HK,.75)},knock1:W(7,'bate'),knock2:W(20,'bate'),dips:DIPS};
frame(0);
const boot=()=>{frame(0);window.__ready=true;};
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(boot);else boot();
})();
