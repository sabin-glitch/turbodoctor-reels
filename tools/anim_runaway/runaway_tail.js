/* ================= REEL director: „Ambalarea dieselului” (diesel runaway), 16.11.2026 ================= */
const CU=window.CUES||{end:60,lines:[],words:[]};
const nrm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const Ts=i=>CU.lines[i].start,Te=i=>CU.lines[i].end,END=CU.end;
function W(i,word,nth){const ws=CU.words.filter(w=>w.win===i&&nrm(w.text)===nrm(word)),w=ws[(nth||1)-1];if(!w){console.warn('CUE_MISSING '+i+' '+word);return Ts(i);}return w.s;}
function track(tr,t){if(t<=tr[0][0])return tr[0][1];let i=0;while(i<tr.length-2&&t>tr[i+1][0])i++;const a=tr[i],b=tr[i+1];return lerp(a[1],b[1],sst(a[0],b[0],t));}
let crownNow=-CLEAR;
const E=0.02;

/* ---------- cuts (dip to black) ---------- */
const D1=Ts(2)-0.22, D2=Ts(24)-0.22, D3=Ts(26)-0.22, D4=Te(26)+0.30;
const DIPS=[D1,D2,D3,D4];
const R1=W(27,'nivelul'), R2=W(27,'filtrul'), R3=W(27,'turbina');   // Rețeta vorbită: baia, filtrul de aer, intercoolerul
const T_TAIE=W(19,'taie'), F_CLOSE=W(21,'închide'), F_OPEN=W(22,'stă')+0.15;
const T_LOV=W(23,'lovesc'), T_BIELA=W(23,'bielă'), T_ULEI=W(23,'ulei'), T_GRIP=W(23,'gripează');
const T_BRUSC=W(25,'brusc'), T_AER=W(26,'aerul');
const T_NEUTRU=W(24,'sarcină');

/* ---------- tracks (value keys, smoothstep between keys) ---------- */
const TR={
  /* crank speed, deg/s of the (slow-motion) animation */
  spd:[[0,1700],[2.2,1850],[D1-E,1850],[D1,260],[Te(2)+0.1,260],[Ts(3)+0.4,520],[Ts(5),600],[W(15,'crește'),600],[Te(15)+0.2,1100],[Te(16),1400],[Te(17),1650],[Te(18),1900],
       [F_CLOSE,2000],[F_CLOSE+1.6,1250],[F_OPEN,1250],[F_OPEN+1.8,2000],[T_LOV,2150],[T_GRIP,2300],[T_GRIP+0.55,0],[D2-E,0],[D2,1900],[T_NEUTRU,1900],[Te(24),2250],
       [T_BRUSC-0.05,2250],[T_BRUSC+0.65,0],[D3-E,0],[D3,1900],[T_AER,1950],[T_AER+2.4,0],[D4-E,0],[D4,600],[END+3,600]],
  inj:[[0,0],[D1-E,0],[D1,1],[T_TAIE-0.05,1],[T_TAIE+0.15,0],[D4-E,0],[D4,1],[END+3,1]],
  oilm:[[0,1],[D1-E,1],[D1,0],[W(4,'ajunge')-0.3,0],[W(4,'ajunge')+0.3,0.85],[Te(4)+0.2,0.85],[Te(4)+0.5,0],[W(12,'trage')-0.2,0],[W(12,'trage')+0.3,0.4],[Te(12)+0.1,0.4],[Te(12)+0.4,0],
        [W(14,'scăpat')-0.2,0],[W(14,'scăpat')+0.6,1],[Te(16),1.1],[Te(18),1.3],[D4-E,1.3],[D4,0],[END+3,0]],
  pool:[[0,0.5],[D1-E,0.5],[D1,0],[W(14,'intercooler')-0.2,0],[Te(14)+1.2,0.75],[W(17,'aerul'),0.75],[Te(17)+0.3,0.25],[D4-E,0.25],[D4,0],[END+3,0]],
  airk:[[0,1],[W(12,'îmbâcsit')-0.2,1],[W(12,'îmbâcsit')+0.4,0.45],[Te(12)+0.1,0.45],[Te(12)+0.4,1],[F_CLOSE-0.05,1],[F_CLOSE+0.3,0.28],[F_OPEN,0.28],[F_OPEN+0.4,1],[T_AER-0.05,1],[T_AER+0.6,0],[D4-E,0],[D4,1],[END+3,1]],
  flap:[[0,0],[F_CLOSE-0.05,0],[F_CLOSE+0.3,1],[F_OPEN,1],[F_OPEN+0.45,0],[END+3,0]],
  wobble:[[0,0.5],[D1-E,0.5],[D1,0],[W(10,'bucșele')-0.2,0],[W(10,'joacă')+0.1,1],[Te(10)+0.2,1],[Te(10)+0.6,0],[W(14,'scăpat')-0.2,0],[W(14,'scăpat')+0.6,0.4],[D4-E,0.4],[D4,0],[END+3,0]],
  drainb:[[0,0],[W(11,'returul')-0.2,0],[W(11,'returul')+0.3,1],[Te(11)+0.2,1],[Te(11)+0.5,0],[END+3,0]],
  crankp:[[0,0],[W(11,'presiunea')-0.2,0],[W(11,'presiunea')+0.3,1],[Te(11)+0.2,1],[Te(11)+0.5,0],[Ts(17)-0.2,0],[Ts(17)+0.3,1],[W(17,'aerul'),1],[W(17,'aerul')+0.4,0],[END+3,0]],
  filt:[[0,0],[W(12,'filtrul')-0.2,0],[W(12,'filtrul')+0.4,1],[Te(12)+0.2,1],[Te(12)+0.6,0],[END+3,0]],
  sump:[[0,0],[W(13,'prea')-0.2,0],[W(13,'baie')+0.2,1],[Te(13)+0.2,1],[Te(13)+0.6,0],[T_ULEI-0.1,0],[T_ULEI+0.9,-1],[D2-E,-1],[D2,0],[END+3,0]],
  float:[[0,0],[W(23,'supapele')-0.1,0],[W(23,'supapele')+0.3,1],[D2-E,1],[D2,0],[END+3,0]],
  rodred:[[0,0],[T_BIELA-0.05,0],[T_BIELA+0.2,1],[D2-E,1],[D2,0],[END+3,0]],
  starve:[[0,0],[T_ULEI-0.1,0],[T_ULEI+0.8,1],[D2-E,1],[D2,0],[END+3,0]],
  heat:[[0,0],[T_GRIP-0.6,0],[T_GRIP,1],[D2-E,1],[D2,0],[END+3,0]],
  top:[[0,650],[D1-E,650],[D1,560],[Ts(9)-0.5,560],[Ts(9)+0.2,700],[Te(13)+0.2,700],[Ts(14)+0.4,560],[D2-E,560],[D2,760],[END+3,760]]
};
const SPD=t=>track(TR.spd,t);
const rpmW=w=>Math.max(0,750+(w-260)*2.75);
const revOf=w=>Math.min(1.55,0.25+0.6*w/1000);

/* ---------- integrated motion (crank angle, gas/air travel, rotor spin, oil phases) ---------- */
const DT=1/240,NT=Math.ceil((END+3)/DT)+2;
const A_th=new Float32Array(NT),A_gex=new Float32Array(NT),A_gair=new Float32Array(NT),A_sp=new Float32Array(NT),A_oil=new Float32Array(NT),A_dr=new Float32Array(NT);
(function(){
  let th=200,g=0,ga=0,sp=0,oi=0,od=0;
  for(let i=0;i<NT;i++){
    const t=i*DT;A_th[i]=th;A_gex[i]=g;A_gair[i]=ga;A_sp[i]=sp;A_oil[i]=oi;A_dr[i]=od;
    const w=SPD(t);th+=DT*w;const le=vLift(th,498,8)/LIFT_V;
    g+=DT*(w/720)*300*(0.22+1.5*le);
    ga+=DT*0.21*w*(0.35+0.65*track(TR.airk,t));
    sp+=DT*TAU*revOf(w);
    const ow=0.25+0.3*w/1000;oi+=DT*ow;od+=DT*ow*(1-track(TR.drainb,t));
  }
})();
const AT=(arr,t)=>{const x=clamp(t,0,(NT-2)*DT)/DT,i=Math.floor(x);return arr[i]+(arr[i+1]-arr[i])*(x-i);};

/* ---------- extra scene objects ---------- */
/* intercooler oil pool (front face) */
const poolMat=new T.MeshBasicMaterial({color:col(0xb07812),transparent:true,opacity:0.92,toneMapped:false,side:T.DoubleSide});
const poolMesh=new T.Mesh(new T.PlaneGeometry(44,1),poolMat);poolMesh.position.set(-266,100,0.14);scene.add(poolMesh);
const poolTop=new T.Mesh(new T.PlaneGeometry(44,1.2),new T.MeshBasicMaterial({color:col(0xffd27a),toneMapped:false,side:T.DoubleSide}));poolTop.position.set(-266,100,0.16);scene.add(poolTop);
/* intake throttle flap in the runner, shaft along z (seen edge-on: horizontal = open, vertical = closed) */
const flapG=new T.Group();flapG.position.set(-226,31,0.4);scene.add(flapG);
flapG.add(new T.Mesh(new T.BoxGeometry(3.4,23.5,3),flat(0xf2f5f8)));
const flapAx=new T.Mesh(new T.CircleGeometry(2.4,20),flat(0x15181c));flapAx.position.z=1.8;flapG.add(flapAx);
/* injector spray */
const sprayPts=makePts(260,{max:16,soft:1.1,order:5});
const SPRAY=[];for(let i=0;i<260;i++)SPRAY.push({j:i%4,q:rnd(),r:rnd()});
const FUEL_C=new T.Color(1.0,0.86,0.36);
/* oil mist colour, smoke colour */
const MIST_C=new T.Color(0.96,0.62,0.14),SMOKE_C=new T.Color(0.56,0.62,0.74);
/* sparks where the floating valves touch the piston */
const vSpk=makePts(240,{add:true,max:14,soft:0.8,order:6});
const VSPK=[];for(let i=0;i<240;i++)VSPK.push({ph:rnd(),ang:rnd()*TAU,sp:0.5+rnd(),k:i%2});
/* sump level */
const POOL0={y:oilPool.position.y,by:oilPoolBack.position.y};
/* rod glow */
const rodMats=[];rod.traverse(o=>{if(o.material){(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>rodMats.push(m));}});
const rodCol0=rodMats.map(m=>m.color.clone());
const hoseCol0=M.hose.color.clone(),filtCol0=M.filter.color.clone();

/* ---------- particle draws (time-integrated versions of the source ones) ---------- */
const EXS=EX_SPAN+700,AIS=AIR_SPAN+900;
function drawExhaust2(G,smoke){
  exPts.begin();
  for(const p of exP){
    const d=((G-p.e)%EXS+EXS)%EXS;if(d>p.L4)continue;
    const prog=exPos(p,d,_v);if(_v.z>3)continue;
    let a=0.5*(1-sst(0.5,3,_v.z))*sst(0,8,d)*(1-sst(p.L4-25,p.L4,d));
    if(prog<0.35)_c.copy(GAS_HOT);else if(prog<0.7)_c.copy(GAS_HOT).lerp(GAS_MID,(prog-0.35)/0.35);else _c.copy(GAS_MID).lerp(GAS_OUT,(prog-0.7)/0.3);
    if(smoke>0.01&&prog>0.3){_c.lerp(SMOKE_C,clamp(smoke*(prog-0.2)*1.3,0,0.85));a*=1+0.7*smoke*prog;}
    exPts.push(_v,_c,Math.min(0.85,a),(prog<0.3?3.2:2.6+1.4*smoke*prog)*p.sz);
  }
  exPts.end();
}
function drawAir2(G,airk,mist){
  airPts.begin();
  for(const p of airP){
    const d=((G-p.e)%AIS+AIS)%AIS;if(d>p.L5)continue;
    const prog=airPos(p,d,_v);if(_v.z>3)continue;
    let a=0.42*airk*(1-sst(0.5,3,_v.z))*sst(0,10,d)*(1-sst(p.L5-30,p.L5,d));
    if(prog<0.2)_c.copy(AIR_C);else if(prog<0.4)_c.copy(AIR_C).lerp(AIR_W,(prog-0.2)/0.2);
    else{_c.copy(AIR_W);if(_v.x<-230&&_v.y<232)_c.lerp(AIR_C,clamp((232-_v.y)/110,0,1));else if(_v.x<-230&&_v.y<120)_c.copy(AIR_C);}
    if(prog>0.5&&_v.y<200&&_v.x<-200)_c.copy(AIR_C);
    let sz=2.4*p.sz;
    if(mist>0.01&&prog>0.19&&p.q<0.34*Math.min(1,mist)){_c.copy(MIST_C);a=Math.max(a,0.75*airk*sst(0,10,d)*(1-sst(p.L5-30,p.L5,d)));sz*=1.25;}
    airPts.push(_v,_c,a,sz);
  }
  airPts.end();
}
function drawCyl2(th,crown,fuel,mist,airk){
  const c=((th%720)+720)%720,burn=pulse(c,352,366,400,470)*clamp(fuel,0,1);cylPts.begin();
  let colA,al=0.34;
  const airMix=new T.Color().copy(AIR_C).lerp(MIST_C,0.55*clamp(mist,0,1));
  if(c<180)colA=airMix;
  else if(c<352)colA=new T.Color().copy(airMix).lerp(AIR_W,sst(200,352,c)*0.8);
  else if(c<540){colA=fuel>0.05?new T.Color().copy(AIR_W).lerp(GAS_HOT,clamp(fuel,0,1)).lerp(new T.Color(1,0.85,0.5),burn*0.6):new T.Color().copy(AIR_W);al=0.34+0.08*clamp(fuel,0,1);}
  else{colA=fuel>0.05?new T.Color().copy(AIR_W).lerp(GAS_HOT,clamp(fuel,0,1)):new T.Color().copy(AIR_C);al=0.42*(1-0.55*sst(540,700,c));}
  if(c>=705||c<20)colA=new T.Color().copy(fuel>0.05?GAS_HOT:AIR_W).lerp(airMix,sst(700,740,c<20?c+720:c));
  al*=0.35+0.65*airk;
  for(const q of cyl){_v.set(EX+q[0],lerp(crown+1,-1,q[1]),q[2]);cylPts.push(_v,colA,al,3.4);}
  cylPts.end();
  return {c,burn};
}
function drawSpray(th,inj){
  sprayPts.begin();
  const c=((th%720)+720)%720;
  if(inj>0.02&&c>338&&c<392){
    const k=(c-338)/54,len=6+26*sst(0,0.6,k),fade=1-sst(0.8,1,k);
    const angs=[-68,-34,34,68];
    for(const s of SPRAY){
      const a=angs[s.j]*DEG,dd=len*s.q,spread=(s.r-0.5)*dd*0.18;
      _v.set(EX+Math.sin(a)*dd+Math.cos(a)*spread,-2.2-Math.cos(a)*dd*0.62+Math.sin(a)*spread*0.3,-0.8);
      sprayPts.push(_v,FUEL_C,0.95*inj*fade*(1-0.4*s.q),2.0+1.6*s.q);
    }
  }
  sprayPts.end();
}
function drawDrops2(O,blocked,starve){
  dropPts.begin();
  for(const d of drops){
    if(d.ph<starve)continue;const path=dropPaths[d.k],t=(d.ph+O*0.55)%1,dist=t*path.len;
    path.at(dist,_v);_v.x+=d.j*(dist<40?1.2:2.0);
    let a=0.85*sst(0,4,dist)*(1-sst(path.len-12,path.len,dist));
    if(blocked>0.01){a*=1-blocked*sst(30,60,dist);}
    dropPts.push(_v,OILC,a,1.3*d.sz);
  }
  dropPts.end();
}
function drawVSparks(t,on,crown){
  vSpk.begin();
  if(on>0.02&&crown>-6){
    const k=clamp((crown+6)/6,0,1);
    for(const q of VSPK){const life=0.3,tt=((t*2.2+q.ph)%life)/life,x=EX+(q.k?XV:-XV),r=2+tt*16*q.sp;
      _v.set(x+Math.cos(q.ang)*r,-2+Math.sin(q.ang)*r*0.6-tt*tt*6,-0.5);_c.copy(SP_C).lerp(SP_H,tt);vSpk.push(_v,_c,(1-tt)*0.95*k*on,1.1);}
  }
  vSpk.end();
}

/* ---------- labels ---------- */
const labelDefs=[],svg=$('leaders'),labBox=$('labels');
function addLabel(text,sub,anchor,side,dx,dy,vis,cls){
  const el=document.createElement('div');el.className='lb'+(side<0?' l':'')+(cls?' '+cls:'');el.textContent=text;
  if(sub){const s=document.createElement('small');s.textContent=sub;el.appendChild(s);}
  labBox.appendChild(el);
  const ln=document.createElementNS('http://www.w3.org/2000/svg','line'),dot=document.createElementNS('http://www.w3.org/2000/svg','circle');
  dot.setAttribute('r','5');svg.appendChild(ln);svg.appendChild(dot);
  const L={el,ln,dot,anchor:typeof anchor==='function'?anchor:()=>anchor,side,dx,dy,vis,w:0,h:0};labelDefs.push(L);return L;
}
const win=(a,b,fi,fo)=>t=>pulse(t,a,a+(fi||.3),b-(fo||.3),b);
const feedPt=()=>{const p=FEED.curve.getPointAt(0.72);return [p.x,p.y,p.z];};
const drainPt=f=>()=>{const p=DRAIN.curve.getPointAt(f);return [p.x,p.y,p.z];};
/* L2-L4: why a diesel burns oil */
addLabel('Fără bujie',null,[EX,46,0],-1,26,-18,win(W(2,'scânteie')-0.25,W(2,'pistonul')+0.2));
addLabel('Aer comprimat','700–900 °C',()=>[EX+24,Math.max(crownNow,-60)+6,0],1,30,8,win(W(2,'pistonul'),W(2,'motorina')+0.1),'fire');
addLabel('Se aprinde singură',null,[EX+10,-6,0],1,28,-20,win(W(2,'motorina')-0.05,Te(2)+0.35),'fire');
addLabel('Aer liber','fără clapetă de reglaj',[-244,31,0],-1,22,-26,win(W(3,'aer')-0.2,W(3,'motorina')+0.1),'air');
addLabel('Puterea = motorina injectată',null,[EX,8,0],1,26,-26,win(W(3,'motorina')-0.1,Te(3)+0.35));
addLabel('Ulei de motor','se aprinde mult mai ușor',[-244,31,0],-1,22,-26,win(W(4,'uleiul')-0.2,W(4,'arde',2)),'oil');
addLabel('Arde ca motorina',null,[EX+10,-6,0],1,28,-20,win(W(4,'arde',2)-0.1,Te(4)+0.35),'fire');
/* L5-L8: the turbo's oil seal */
addLabel('Turbina',null,[30,TY+34,0],1,18,26,win(W(5,'turbină')-0.35,Te(5)+0.3));
addLabel('Ulei sub presiune','câțiva litri pe minut',feedPt,-1,18,-6,win(W(6,'ulei')-0.2,W(6,'capete')),'oil');
addLabel('Segmenți metalici','nu simeringuri',[-58,TY+8,0],-1,24,-24,win(W(6,'segmenți')-0.2,W(7,'etanșarea')-0.05));
addLabel('Segmenți',null,[46,TY+9,0],1,24,-24,win(W(6,'segmenți')-0.2,W(7,'etanșarea')-0.05));
addLabel('Nu țin ulei sub presiune',null,[-58,TY+8,0],-1,24,-24,win(W(7,'ei')-0.1,W(7,'etanșarea')-0.05),'bad');
addLabel('Etanșare prin presiune',null,[-8,TY-30,0],1,26,-12,win(W(7,'etanșarea')-0.15,Ts(8)+0.4));
addLabel('Presiune mare',null,[-80,TY+20,0],-1,18,26,win(Ts(8)-0.1,W(8,'uleiul')+0.2),'air');
addLabel('Presiune mare',null,[64,TY+20,0],1,18,26,win(Ts(8)-0.1,W(8,'uleiul')+0.2),'fire');
addLabel('Corp central','presiune mică',[-8,TY-26,0],1,22,-30,win(W(8,'central')-0.2,W(8,'uleiul')+0.2));
addLabel('Uleiul se scurge în baie',null,drainPt(0.18),1,22,0,win(W(8,'uleiul')-0.15,Te(8)+0.4),'oil');
/* L10-L13: the four failures */
addLabel('Bucșe uzate','axul joacă, roade segmenții',[-34,TY+6.2,0],-1,26,26,win(W(10,'bucșele')-0.2,Te(10)+0.35),'bad');
addLabel('Retur înfundat',null,drainPt(0.42),1,22,0,win(W(11,'returul')-0.2,W(11,'presiunea')+0.1),'bad');
addLabel('Presiune mare în carter',null,[EX+40,-120,0],1,26,0,win(W(11,'presiunea')-0.1,W(11,'uleiul')+0.3),'bad');
addLabel('Uleiul nu se mai scurge',null,[OIL_A,TY-30,0],1,26,10,win(W(11,'uleiul')-0.15,Te(11)+0.35),'oil');
addLabel('Filtru de aer îmbâcsit',null,[-214,TY+31,0],-1,18,-30,win(W(12,'filtrul')-0.2,W(12,'trage')),'bad');
addLabel('Depresiune',null,[-150,TY+12,0],1,20,-34,win(W(12,'depresiune')-0.15,W(12,'trage')+0.3),'bad');
addLabel('Uleiul e tras afară',null,[-62,TY+9,0],-1,26,26,win(W(12,'trage')-0.1,Te(12)+0.35),'oil');
addLabel('Prea mult ulei în baie','+ motorină din regenerările DPF',[EX+10,-168,0],1,26,26,win(W(13,'prea')-0.2,Te(13)+0.35),'bad');
/* L14: the path into the engine */
addLabel('Ulei pe partea compresorului',null,[CV.a0,TY+62,-CV.r(TAU)*0.3],1,20,-20,win(W(14,'compresorului')-0.4,W(14,'intercooler')),'oil');
addLabel('Intercooler','se adună ulei',[-266,112,0],1,30,-10,win(W(14,'intercooler')-0.2,W(14,'cilindri')+0.1),'oil');
addLabel('Nivelul uleiului',null,[EX+10,-168,0],1,26,26,win(R1-0.05,R2-0.35),'good');
addLabel('Filtru de aer',null,[-214,TY+31,0],-1,18,-30,win(R2-0.05,R3-0.35),'good');
addLabel('Intercooler',null,[-266,112,0],1,30,-10,win(R3+0.15,END+1),'good');
addLabel('Arde în cilindru',null,[EX-10,-6,0],1,30,-20,win(W(14,'cilindri')-0.2,Te(14)+0.45),'fire');
/* L16-L17: the loop */
addLabel('Pompa de ulei','turație mai mare = mai mult ulei',[EX+40,-186,0],1,30,24,win(W(16,'pompa')-0.2,W(16,'turbina')+0.1),'oil');
addLabel('Turbina stricată',null,[-34,TY+6.2,0],-1,26,26,win(W(16,'turbina')-0.15,Te(16)+0.35),'bad');
addLabel('Presiune în carter',null,[EX+40,-120,0],1,26,0,win(Ts(17)-0.1,W(17,'aerul')+0.1),'bad');
addLabel('Uleiul din intercooler',null,[-266,112,0],1,30,-10,win(W(17,'aerul')-0.1,Te(17)+0.35),'oil');
/* L19-L22: the ECU, the key, the flap */
addLabel('Injecție: zero',null,[EX,10,0],1,26,-26,win(T_TAIE-0.05,W(19,'propriul')),'');
addLabel('Arde propriul ulei',null,[EX+10,-6,0],1,28,-20,win(W(19,'propriul')-0.15,Te(19)+0.35),'oil');
addLabel('Cheia oprește doar injectoarele',null,[EX,10,0],1,26,-26,win(W(20,'cheia')-0.1,W(20,'uleiul')+0.1));
addLabel('Uleiul vine pe admisie',null,[-244,31,0],-1,22,-26,win(W(20,'uleiul')-0.15,Te(20)+0.35),'oil');
addLabel('Clapetă de admisie','se închide la oprire',[-226,40,0],-1,22,-34,win(W(21,'clapetă')-0.2,F_OPEN-0.2),'air');
addLabel('Se redeschide',null,[-226,40,0],-1,22,-34,win(F_OPEN-0.1,W(22,'uleiul')+0.1),'bad');
addLabel('Uleiul din galerie arde',null,[EX-XV,22,0],1,30,-12,win(W(22,'uleiul')-0.15,Te(22)+0.35),'fire');
/* L23: what breaks */
addLabel('Supapele lovesc pistonul',null,[EX-XV,2,0],-1,26,-20,win(W(23,'supapele')-0.1,T_BIELA-0.05),'bad');
addLabel('Biela cedează',null,()=>[EX+6,crownNow-COMP_H-62,0],1,30,0,win(T_BIELA-0.15,T_ULEI-0.05),'bad');
addLabel('Fără ulei: gripare',null,[EX+20,-192,0],1,30,20,win(T_ULEI-0.1,D2-0.05),'bad');
/* L25-L26: stopping it */
addLabel('Motorul se îneacă',null,[EX+10,-40,0],1,30,0,win(T_BRUSC+0.1,D3-0.05),'good');
addLabel('Aer tăiat',null,[-232,TY,0],-1,20,-28,win(T_AER-0.1,D4-0.05),'good');
addLabel('Fără aer, nu mai arde',null,[EX+10,-6,0],1,28,-20,win(T_AER+0.9,D4-0.05),'good');

/* ---------- arrows (pressure / flow), projected from 3D ---------- */
const ARW=[];const ACOL={air:'#7ccaf5',fire:'#ff6a2b',oil:'#f0b43a',bad:'#ff4b4b',good:'#3ddc84'};
(function(){const NS='http://www.w3.org/2000/svg',defs=document.createElementNS(NS,'defs');
  Object.keys(ACOL).forEach(k=>{const m=document.createElementNS(NS,'marker');m.setAttribute('id','ah_'+k);m.setAttribute('viewBox','0 0 10 10');m.setAttribute('refX','6');m.setAttribute('refY','5');
    m.setAttribute('markerWidth','4.2');m.setAttribute('markerHeight','4.2');m.setAttribute('orient','auto');const p=document.createElementNS(NS,'path');p.setAttribute('d','M0,0 L10,5 L0,10 z');p.setAttribute('fill',ACOL[k]);m.appendChild(p);defs.appendChild(m);});
  svg.appendChild(defs);})();
function addArrow(a,b,vis,k){const NS='http://www.w3.org/2000/svg',ln=document.createElementNS(NS,'line');ln.setAttribute('class','arw');ln.style.stroke=ACOL[k];ln.setAttribute('marker-end','url(#ah_'+k+')');svg.appendChild(ln);ARW.push({ln,a,b,vis});}
/* L8: higher pressure in the housings pushes inwards; oil falls to the drain */
const wA8=win(Ts(8)+0.2,W(8,'uleiul')+0.3),wO8=win(W(8,'uleiul')-0.15,Te(8)+0.4);
addArrow([-82,TY+19,0],[-64,TY+10.5,0],wA8,'air');addArrow([-82,TY-19,0],[-64,TY-10.5,0],wA8,'air');
addArrow([66,TY+19,0],[52,TY+11,0],wA8,'fire');addArrow([66,TY-19,0],[52,TY-11,0],wA8,'fire');
addArrow([OIL_A,TY-14,0],[OIL_A,TY-44,0],wO8,'oil');
/* L11: crankcase pressure pushes up the drain */
const wC11=win(W(11,'presiunea')-0.1,Te(11)+0.35);
addArrow([16,-120,0],[16,-60,0],wC11,'bad');addArrow([EX+44,-150,0],[EX+44,-100,0],wC11,'bad');
/* L12: depression pulls the oil out on the compressor side */
const wD12=win(W(12,'trage')-0.1,Te(12)+0.35);
addArrow([-62,TY+9,0],[-82,TY+20,0],wD12,'oil');addArrow([-62,TY-9,0],[-82,TY-20,0],wD12,'oil');
/* L17: crankcase pressure again */
const wC17=win(Ts(17)-0.1,W(17,'aerul')+0.2);
addArrow([EX+44,-150,0],[EX+44,-100,0],wC17,'bad');
function placeArrows(t){
  for(const A of ARW){const o=A.vis(t);if(o<0.02){A.ln.style.opacity=0;continue;}
    tmpV.set(A.a[0],A.a[1],A.a[2]).project(camera);const x1=(tmpV.x*0.5+0.5)*VW,y1=(-tmpV.y*0.5+0.5)*VH;
    tmpV.set(A.b[0],A.b[1],A.b[2]).project(camera);const x2=(tmpV.x*0.5+0.5)*VW,y2=(-tmpV.y*0.5+0.5)*VH;
    A.ln.setAttribute('x1',x1.toFixed(1));A.ln.setAttribute('y1',y1.toFixed(1));A.ln.setAttribute('x2',x2.toFixed(1));A.ln.setAttribute('y2',y2.toFixed(1));
    A.ln.style.opacity=o;A.ln.style.strokeDashoffset=(-t*70).toFixed(1);}
}

/* ---------- camera ---------- */
const SHOTS={
  hook:{c:[-128,12],w:260,h:232,az:18,el:7},
  wide:{c:[-100,40],w:390,h:330,az:16,el:7},
  cyl:{c:[EX,-14],w:170,h:150,az:12,el:5},
  cylTop:{c:[EX,8],w:150,h:118,az:10,el:4},
  intake:{c:[-200,20],w:200,h:150,az:14,el:5},
  turbo:{c:[-20,TY+2],w:300,h:220,az:20,el:6},
  feed:{c:[-14,TY+36],w:130,h:120,az:14,el:4},
  chra:{c:[-6,TY+3],w:150,h:116,az:9,el:3},
  chraDrain:{c:[0,TY-30],w:170,h:180,az:10,el:4},
  drain:{c:[-10,-20],w:220,h:320,az:12,el:5},
  filter:{c:[-170,TY+4],w:200,h:150,az:14,el:5},
  compSeal:{c:[-72,TY+4],w:130,h:110,az:12,el:4},
  sump:{c:[EX,-176],w:240,h:150,az:10,el:6},
  comp:{c:[-110,TY+60],w:220,h:250,az:-6,el:6},
  cooler:{c:[-250,150],w:160,h:230,az:14,el:5},
  pump:{c:[EX+20,-170],w:240,h:150,az:10,el:6},
  mid:{c:[-80,-10],w:400,h:300,az:12,el:6},
  flap:{c:[-218,30],w:96,h:80,az:10,el:4},
  valves:{c:[EX,12],w:150,h:112,az:10,el:4},
  cylFull:{c:[EX,-80],w:200,h:270,az:12,el:5},
  sumpWide:{c:[EX,-140],w:250,h:200,az:10,el:6},
  airCut:{c:[-160,TY-40],w:240,h:260,az:12,el:5}
};
const CAM=[
  [0,'hook'],[D1-E,'hook'],
  [D1,'cyl'],[W(3,'aer')-0.4,'cyl'],[W(3,'aer'),'intake'],[W(3,'motorina')-0.3,'intake'],[W(3,'motorina'),'cylTop'],
  [W(4,'uleiul')-0.4,'cylTop'],[W(4,'uleiul'),'intake'],[W(4,'arde',2)-0.4,'intake'],[W(4,'arde',2),'cyl'],
  [Ts(5)-0.3,'cyl'],[Ts(5)+0.4,'turbo'],[W(6,'ulei')-0.4,'turbo'],[W(6,'ulei'),'feed'],[W(6,'capete')-0.3,'feed'],[W(6,'capete')+0.2,'chra'],
  [W(8,'uleiul')-0.3,'chra'],[W(8,'uleiul')+0.2,'chraDrain'],[Te(8)+0.1,'chraDrain'],[Ts(9)+0.2,'turbo'],[Ts(10)-0.2,'turbo'],[Ts(10)+0.4,'chra'],
  [Te(10)+0.1,'chra'],[W(11,'returul')+0.1,'drain'],[Te(11)+0.1,'drain'],[W(12,'filtrul')+0.1,'filter'],[W(12,'trage')-0.4,'filter'],[W(12,'trage')+0.1,'compSeal'],
  [Te(12)+0.1,'compSeal'],[Ts(13)+0.3,'sump'],[Te(13)+0.1,'sump'],[Ts(14)+0.3,'comp'],[W(14,'intercooler')-0.4,'comp'],[W(14,'intercooler')+0.1,'cooler'],
  [W(14,'cilindri')-0.4,'cooler'],[W(14,'cilindri')+0.1,'cyl'],[Ts(15)-0.2,'cyl'],[Ts(15)+0.6,'wide'],[W(16,'pompa')-0.4,'wide'],[W(16,'pompa')+0.1,'pump'],
  [W(16,'turbina')-0.4,'pump'],[W(16,'turbina')+0.1,'turbo'],[Ts(17)-0.2,'turbo'],[Ts(17)+0.4,'mid'],[W(17,'aerul')-0.4,'mid'],[W(17,'aerul')+0.1,'cooler'],
  [Ts(18)-0.2,'cooler'],[Ts(18)+0.5,'wide'],[Ts(19)-0.2,'wide'],[Ts(19)+0.4,'cylTop'],[W(20,'uleiul')-0.4,'cylTop'],[W(20,'uleiul')+0.1,'intake'],
  [W(21,'clapetă')-0.5,'intake'],[W(21,'clapetă'),'flap'],[W(22,'uleiul')-0.4,'flap'],[W(22,'uleiul')+0.1,'intake'],
  [Ts(23)-0.2,'intake'],[Ts(23)+0.4,'valves'],[T_BIELA-0.4,'valves'],[T_BIELA+0.1,'cylFull'],[T_ULEI-0.4,'cylFull'],[T_ULEI+0.1,'sumpWide'],[D2-E,'sumpWide'],
  [D2,'wide'],[D3-E,'wide'],[D3,'wide'],[T_AER-0.5,'wide'],[T_AER,'airCut'],[D4-E,'airCut'],[D4,'wide'],[R1-0.7,'wide'],[R1+0.1,'sump'],[R2-0.6,'sump'],[R2+0.1,'filter'],[R3-0.6,'filter'],[R3+0.2,'cooler'],[END+3,'cooler']
];
const VW=1080,VH=1920,PADBOT=VH-1280,LABBOT=1250;let padTop=560,pxPerMm=1;
const camTarget=new T.Vector3(),tmpV=new T.Vector3();
function shotAt(t){
  let i=0;while(i<CAM.length-2&&t>CAM[i+1][0])i++;
  const a=SHOTS[CAM[i][1]],b=SHOTS[CAM[i+1][1]],k=sst(CAM[i][0],CAM[i+1][0],t);
  const lw=Math.exp(lerp(Math.log(a.w),Math.log(b.w),k)),lh=Math.exp(lerp(Math.log(a.h),Math.log(b.h),k));
  return {cx:lerp(a.c[0],b.c[0],k),cy:lerp(a.c[1],b.c[1],k),w:lw,h:lh,az:lerp(a.az,b.az,k),el:lerp(a.el,b.el,k)};
}
let shakeK=0;
function placeCamera(t){
  const s=shotAt(t),tf=Math.tan(FOV*DEG/2),aspect=VW/VH,safeH=VH-padTop-PADBOT,safeW=VW-64;
  const d=Math.max((s.h/2)/tf*(VH/safeH),(s.w/2)/(tf*aspect)*(VW/safeW)),az=s.az*DEG,el=s.el*DEG;
  camTarget.set(s.cx,s.cy,0);
  camera.position.set(camTarget.x+d*Math.sin(az)*Math.cos(el),camTarget.y+d*Math.sin(el),d*Math.cos(az)*Math.cos(el));
  camera.lookAt(camTarget);
  camera.updateMatrixWorld();tmpV.setFromMatrixColumn(camera.matrixWorld,1);
  camera.position.addScaledVector(tmpV,((padTop-PADBOT)/2)/VH*(2*d*tf));
  const amp=d*0.0042*shakeK;
  if(amp>0){camera.position.x+=amp*Math.sin(t*97);camera.position.y+=amp*Math.cos(t*83);}
  camera.near=Math.max(1,d*0.05);camera.far=d*8+1500;camera.updateProjectionMatrix();
  camera.updateMatrixWorld();
  pxPerMm=VH/(2*d*tf);shared.uScale.value=VH*DPR/(2*tf);
}
function placeLabels(t){
  for(const L of labelDefs){
    let o=L.vis(t);
    if(o>=0.02){const a=L.anchor();tmpV.set(a[0],a[1],a[2]).project(camera);L.sx=(tmpV.x*0.5+0.5)*VW;L.sy=(-tmpV.y*0.5+0.5)*VH;o*=sst(padTop-140,padTop-80,L.sy)*(1-sst(LABBOT+10,LABBOT+60,L.sy))*sst(-10,30,L.sx)*(1-sst(VW-30,VW+10,L.sx));}
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

/* ---------- RPM read-out ---------- */
const rpmEl=$('rpm'),rpmV=rpmEl.querySelector('.tv'),rpmBar=rpmEl.querySelector('.tb i');
const RPM_MAX=7000,RPM_LIM=4500;rpmEl.querySelector('.tb b').style.left=(RPM_LIM/RPM_MAX*100)+'%';
const rpmVis=t=>Math.max(win(0.15,D1-0.05,0.25,0.15)(t),win(Ts(15)+0.2,D2-0.05,0.4,0.15)(t));
let rpmShown=-1;
function placeRpm(t,w){
  const o=rpmVis(t);rpmEl.style.opacity=o.toFixed(3);if(o<0.01)return;
  rpmEl.style.top=(t<D1?1318:300)+'px';
  const r=Math.round(rpmW(w)/50)*50;if(r!==rpmShown){rpmShown=r;rpmV.textContent=r.toLocaleString('ro-RO');}
  rpmBar.style.width=clamp(r/RPM_MAX*100,0,100).toFixed(1)+'%';rpmEl.classList.toggle('hot',r>RPM_LIM);
}

/* ---------- per-frame state ---------- */
function apply(t){
  const w=SPD(t),th=AT(A_th,t),crown=-CLEAR-pistonDrop(th);crownNow=crown;
  piston.position.y=crown;rod.position.y=crown-COMP_H;rod.rotation.z=Math.asin(CRK*Math.sin(th*DEG)/ROD);
  const fl=track(TR.float,t);
  const li=Math.min(LIFT_V*1.15,vLift(th,712,222)+fl*3.2*(0.6+0.4*Math.sin(th*0.9*DEG))),le=Math.min(LIFT_V*1.15,vLift(th,498,8)+fl*3.2*(0.6+0.4*Math.cos(th*0.8*DEG)));
  vIn.g.position.y=-li;vEx.g.position.y=-le;
  setHelix(vIn.sp.geometry,HEAD_H+1.3,22.4-li);setHelix(vEx.sp.geometry,HEAD_H+1.3,22.4-le);
  const inj=track(TR.inj,t),mist=track(TR.oilm,t),airk=track(TR.airk,t);
  const fuel=clamp(inj+0.9*mist,0,1.1)*(w>30?1:0)*clamp(airk*1.4,0,1);
  const st=drawCyl2(th,crown,fuel,mist,airk);
  drawSpray(th,inj*(w>30?1:0));
  const cy=Math.max(crown*0.5-3,-40);
  fireLight.intensity=1.6*st.burn;fireLight.position.set(EX,cy,10);
  glow.material.opacity=0.2*st.burn;glow.position.set(EX,cy-2,-8);const gs=60+26*st.burn+Math.min(-crown,60)*0.9;glow.scale.set(gs,gs*0.72,1);
  tGlow.material.opacity=0.10*clamp(w/600,0,1.3);
  drawExhaust2(AT(A_gex,t),clamp(mist,0,1)*clamp(w/600,0,1));
  drawAir2(AT(A_gair,t),airk,mist);
  const O=AT(A_oil,t);
  oilMats.forEach(m=>{m.uniforms.uHi.value=0;m.uniforms.uFront.value=1e5;m.uniforms.uPhase.value=O*(m.uniforms.uLen.value>1.5?1.6:1.0);});
  oilNet.blockMat.uniforms.uFront.value=1e5;
  /* failure layer of the source: rotor whirl, heat, starvation */
  FAIL.starve=track(TR.starve,t)*0.9;FAIL.clog=0;FAIL.pump=0;FAIL.heat=track(TR.heat,t);
  FAIL.wobble=track(TR.wobble,t);FAIL.sparks=0;FAIL.snap=-1;FAIL.spinC=null;FAIL.spinT=null;FAIL.air=airk;
  drawDrops2(AT(A_dr,t),track(TR.drainb,t),FAIL.starve);
  applyFail(t,AT(A_sp,t));
  /* drain blocked: hose turns red; filter clogged: filter goes brown */
  const db=track(TR.drainb,t);M.hose.color.copy(hoseCol0).lerp(new T.Color(0.75,0.08,0.06),db*0.85);
  const fc=track(TR.filt,t);M.filter.color.copy(filtCol0).lerp(new T.Color(0.32,0.2,0.08),fc);
  /* sump level: +1 overfilled, -1 empty */
  const sl=track(TR.sump,t),hk=sl>=0?1+2.4*sl:1+sl*0.92;
  oilPool.scale.y=hk;oilPool.position.y=-204*(1-hk);oilPoolBack.position.y=POOL0.by+14*(hk-1);
  /* intercooler pool */
  const pl=track(TR.pool,t),ph=Math.max(0.01,pl*46);poolMesh.scale.y=ph;poolMesh.position.y=100+ph/2;poolTop.position.y=100+ph;poolMesh.visible=poolTop.visible=pl>0.01;
  /* flap: open = horizontal */
  flapG.rotation.z=(1-track(TR.flap,t))*Math.PI/2;
  /* rod glow when it fails */
  const rr=track(TR.rodred,t);rodMats.forEach((m,i)=>{m.color.copy(rodCol0[i]).lerp(new T.Color(1,0.2,0.08),rr*(0.75+0.25*Math.sin(t*20)));});
  drawVSparks(t,fl,crown);
  /* shake: above the limiter, harder when things break */
  shakeK=clamp((w-1200)/900,0,1)*0.8+fl*0.5+track(TR.heat,t)*0.4;
  return {w,th,st};
}

/* ---------- frame API ---------- */
const dipEl=$('dip'),flashEl=$('flash');
const FLASHES=[T_LOV+0.05,T_BIELA+0.05,T_GRIP+0.05];
function frame(t){
  padTop=track(TR.top,t);
  const s=apply(t);placeCamera(t);placeLabels(t);placeArrows(t);placeRpm(t,s.w);
  let dp=0;for(const c of DIPS)dp=Math.max(dp,1-Math.abs(t-c)/0.24);dipEl.style.opacity=clamp(dp,0,1);
  let fl=0;for(const c of FLASHES){const q=t-c;if(q>=-0.03&&q<0.5)fl=Math.max(fl,q<0?1+q/0.03:Math.exp(-q*7));}flashEl.style.opacity=(0.7*fl).toFixed(3);
  renderer.render(scene,camera);
}
renderer.setSize(VW,VH,false);camera.aspect=VW/VH;camera.updateProjectionMatrix();svg.setAttribute('viewBox','0 0 '+VW+' '+VH);
window.__frame=frame;window.__end=END;
/* sound-bed probe: crank speed, oil mist, flashes, flap */
window.__probe=t=>{let fl=0;for(const c of FLASHES){const q=t-c;if(q>=0&&q<0.05)fl=1;}return [SPD(t),track(TR.oilm,t),fl,track(TR.flap,t)];};
window.__info={dips:DIPS,flashes:FLASHES,taie:T_TAIE,flap:[F_CLOSE,F_OPEN],brusc:T_BRUSC,aer:T_AER,end:END};
frame(0);
const boot=()=>{frame(0);window.__ready=true;};
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(boot);else boot();
