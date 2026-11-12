/* ================= REEL (video build): regia pentru „Injectorul piezo versus injectorul magnetic” ================= */
const CU=window.CUES;
const nrm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const Ts=i=>CU.lines[i].start,Te=i=>CU.lines[i].end,END=CU.end;
function Wd(i,word,nth){const ws=CU.words.filter(w=>w.win===i&&nrm(w.text)===nrm(word)),w=ws[(nth||1)-1];if(!w){console.warn('CUE_MISSING '+i+' '+word);return Ts(i);}return w.s;}

/* ---------- momente ---------- */
const HK=Ts(2)-0.35;                               // sfârșitul hook-ului
const A2=Wd(2,'supapă')-0.15,A3=Te(3)+0.25;        // amândouă: supapa golește camera de comandă
const M0=Wd(4,'48')-0.2,M1=Te(5)+0.35;             // magnetic: 48 V în bobină
const P0=Wd(6,'150')-0.2,P1=Te(7)+0.35;            // piezo: ~150 V în stivă
const B0=Ts(8)+0.2,B1=Te(8)+0.7;                   // aceeași comandă, acul
const Q=Ts(9)-0.3;                                 // „De ce este superior…”
const RS=[Ts(10)-0.15,Ts(11)-0.15,Ts(12)-0.15,Ts(13)-0.15],R1=Ts(14)-0.35;
const S0=Ts(14)-0.2,MS0=Wd(14,'toarnă')-0.4,MS1=Te(15)+0.3;

/* ---------- starea fiecărui injector ---------- */
const IDLE={pat:'single',ms:0,show:false};
function est(kind,t){
  const pulse=(a,b)=>({pat:'single',ms:clamp((t-a)/(b-a))*2,show:t>=a});
  const loop=(t0,sp)=>({pat:'multi',ms:Math.min(((t-t0)*sp)%4.9,4.2),show:true});
  if(t<HK)return loop(-1.2,0.95);
  if(t<M0-0.6)return pulse(A2,A3);
  if(t<P0-0.6)return kind==='mag'?pulse(M0,M1):IDLE;
  if(t<B0-0.5)return kind==='piezo'?pulse(P0,P1):IDLE;
  if(t<Q)return pulse(B0,B1);
  if(t<S0)return loop(Q,0.55);
  if(t<MS1+0.5)return {pat:'multi',ms:clamp((t-MS0)/(MS1-MS0))*4.2,show:t>=MS0};
  return loop(MS1+0.5,0.7);
}

/* ---------- camera: zona 3D ocupă rândurile pt..pb ale cadrului ---------- */
const FULL={lo:-32,hi:202,x:0},UPB={lo:50,hi:198,x:0};
const SHOTS=[
  {t:0,...FULL,yaw:2.75,pitch:0.10,pt:560,pb:1280},
  {t:HK-0.9,...FULL,yaw:0.30,pitch:0.07,pt:560,pb:1280},
  {t:HK-0.1,...FULL,yaw:0.26,pitch:0.07,pt:560,pb:1280},
  {t:HK+0.8,...FULL,yaw:0.20,pitch:0.06,pt:250,pb:1270},
  {t:A2-0.9,...FULL,yaw:0.14,pitch:0.06,pt:250,pb:1270},
  {t:A2+0.1,...UPB,yaw:0.12,pitch:0.07,pt:250,pb:1270},
  {t:M0-1.0,...UPB,yaw:0.06,pitch:0.07,pt:250,pb:1270},
  {t:M0,lo:99,hi:191,x:MAGX,yaw:0.30,pitch:0.08,pt:250,pb:950},
  {t:M1,lo:99,hi:191,x:MAGX,yaw:0.12,pitch:0.08,pt:250,pb:950},
  {t:P0-0.1,lo:68,hi:190,x:PIEX,yaw:-0.30,pitch:0.07,pt:250,pb:950},
  {t:P1,lo:68,hi:190,x:PIEX,yaw:-0.12,pitch:0.07,pt:250,pb:950},
  {t:B0,lo:-34,hi:100,x:0,yaw:-0.10,pitch:0.10,pt:250,pb:950},
  {t:Q-0.2,lo:-34,hi:100,x:0,yaw:0.05,pitch:0.10,pt:250,pb:950},
  {t:Q+0.9,...FULL,yaw:0.18,pitch:0.06,pt:250,pb:1270},
  {t:RS[0]-0.5,...FULL,yaw:0.10,pitch:0.06,pt:250,pb:1270},
  {t:RS[0]+0.4,lo:20,hi:204,x:0,yaw:0.06,pitch:0.06,pt:250,pb:850},
  {t:R1-0.3,lo:20,hi:204,x:0,yaw:-0.16,pitch:0.06,pt:250,pb:850},
  {t:S0+0.8,...FULL,yaw:-0.08,pitch:0.06,pt:250,pb:950},
  {t:END+2,...FULL,yaw:0.22,pitch:0.06,pt:250,pb:950},
];
function shotAt(t){
  let i=0;while(i<SHOTS.length-2&&t>=SHOTS[i+1].t)i++;
  const a=SHOTS[i],b=SHOTS[i+1],k=ease((t-a.t)/(b.t-a.t));const o={};
  for(const key of ['lo','hi','x','yaw','pitch','pt','pb'])o[key]=lerp(a[key],b[key],k);return o;
}
const camT=new T.Vector3();
function setCamera(t){
  const s=shotAt(t);const span=s.hi-s.lo;const h=span*1920/(s.pb-s.pt);const yc=s.hi-(960-s.pt)/(s.pb-s.pt)*span;
  const d=h/2/Math.tan(FOV*Math.PI/360);
  cam.position.set(s.x+d*Math.sin(s.yaw)*Math.cos(s.pitch),yc+d*Math.sin(s.pitch),d*Math.cos(s.yaw)*Math.cos(s.pitch));
  camT.set(s.x,yc,0);cam.lookAt(camT);cam.updateMatrixWorld();cam.updateProjectionMatrix();
  return s;
}

/* ---------- etichete pe piese: [text, x local, y, parte, moment] ---------- */
function labels(list,ox,t,t1,col){
  font(600,30,FD);
  for(const side of [-1,1]){
    const items=list.filter(l=>l[3]===side).map(l=>({l,p:proj(ox+l[1],l[2],0.4)})).sort((a,b)=>a.p[1]-b.p[1]);
    let prev=-1e9;
    for(const o of items){
      const lines=o.l[0].split('\n');const hh=lines.length*32;
      const ty=Math.max(o.p[1],prev+hh/2+8);prev=ty+hh/2;
      const a=ease((t-o.l[4])/0.35)*(1-ease((t-(t1-0.35))/0.35));if(a<=0)continue;
      const lx=o.p[0]+side*150;
      g.globalAlpha=a;g.strokeStyle=col;g.lineWidth=2.5;g.beginPath();g.moveTo(o.p[0],o.p[1]);g.lineTo(o.p[0]+side*22,ty);g.lineTo(lx,ty);g.stroke();
      g.fillStyle=col;g.beginPath();g.arc(o.p[0],o.p[1],5,0,7);g.fill();
      shadowTxt(()=>lines.forEach((ln,j)=>txt(ln,lx+side*10,ty-(lines.length-1)*16+j*32,C.fg,side<0?'right':'left','middle')));
      g.globalAlpha=1;
    }
  }
}
const LB_BOTH_M=[['Supapă',1.1,123.7,1,A2],['Cameră de comandă',2.4,118,1,Wd(2,'camera')-0.1]];
const LB_BOTH_P=[['Supapă',-2.3,82,-1,A2],['Cameră de comandă',-2.5,72,-1,Wd(2,'camera')-0.1]];
const LB_M=[['Bobină',-7.6,143,-1,Wd(4,'bobină')-0.2],['Armătură de oțel',-7,127.5,-1,Wd(5,'armătură')-0.15],['Bila supapei',1.1,123.7,1,Wd(5,'bila')-0.15],['Cameră de comandă',2.4,118,1,Wd(5,'bila')+0.5]];
const LB_P=[['Stivă piezo\nsute de plăcuțe',-5.2,135,-1,Wd(6,'stivă')-0.2],['Cuplor hidraulic',-4.2,90,-1,Wd(7,'împing')-0.2],['Supapă servo',2.3,82,1,Wd(7,'supapa')-0.2]];

function tags(t,s){
  const wide=clamp(((s.hi-s.lo)-150)/60);
  if(wide>0){
    g.globalAlpha=wide;
    const a=proj(MAGX-17,178),b=proj(PIEX+17,178);
    shadowTxt(()=>{font(700,36,FD);txt('MAGNETIC',a[0],a[1],C.mag,'right');txt('PIEZO',b[0],b[1],C.piezo,'left');});
    if(t>HK+0.6){
      shadowTxt(()=>{font(500,22,FB);txt('Bosch CRI 2 · solenoid',a[0],a[1]+30,C.muted,'right');txt('Bosch CRI 3',b[0],b[1]+30,C.muted,'left');});
      const kv=ease((t-Q)/0.6);
      if(kv>0){g.globalAlpha=wide*kv;shadowTxt(()=>{font(700,32,FD);txt('48 V',a[0],a[1]+70,C.mag,'right');txt('~150 V',b[0],b[1]+70,C.piezo,'left');});g.globalAlpha=wide;}
      const e=proj(0,214,12);shadowTxt(()=>{font(700,27,FD);txt('CALCULATOR INJECȚIE · ECU',e[0],e[1]+4,C.fg,'center','middle');});
      const r=proj(0,RAIL.y,RAIL.z+7);const kr=0.55+0.45*fade(t,Wd(2,'rail')-0.4,A2-0.5,0.3);
      g.globalAlpha=wide*kr;shadowTxt(()=>{font(600,24+8*(kr-0.55)/0.45,FD);txt('RAIL · până la 2.700 bar',r[0],r[1],'#9fd0ff','center','middle');});
    }
    g.globalAlpha=1;
  }
  // tensiunea, mare, în cadrele apropiate
  for(const [a,b,v,sub,col,al,x] of [[M0+0.15,M1-0.2,'48 V','apoi ~12 V ca s-o țină',C.mag,'left',60],[P0+0.15,P1-0.2,'~150 V','stiva se lungește pe loc',C.piezo,'right',1020]]){
    const k=fade(t,a,b,0.35);if(k<=0)continue;g.globalAlpha=k;
    shadowTxt(()=>{font(700,110,FD);txt(v,x,370,col,al);font(600,30,FB);txt(sub,x,416,C.fg,al);});g.globalAlpha=1;}
}

/* ---------- cartonașele Bosch ---------- */
const WHY=[
  {h:'De ~10 ori mai multă forță',b:'Actuatorul piezo față de un solenoid',vis:'force'},
  {h:'100 µs între două injecții',b:'Pauza minimă: o zecime de milisecundă',vis:'gap'},
  {h:'Până la 10 injecții pe ciclu',b:'Preinjecții foarte mici · până la 2.700 bar',vis:'count'},
  {h:'Consum, emisii și zgomot mai mici',b:'Rezultatul după Bosch',vis:'down'},
];
function vis(kind,x,y,w,lt){
  const p=ease(lt/1.2);
  if(kind==='force'){bar(x,y+34,w,30,p*0.1,C.mag,'Solenoid','1×');bar(x,y+112,w,30,p,C.piezo,'Actuator piezo','~10×');}
  if(kind==='gap'){
    g.strokeStyle=C.line;g.lineWidth=2;g.beginPath();g.moveTo(x,y+130);g.lineTo(x+w,y+130);g.stroke();
    const q=(x0,ww,col,k)=>{g.fillStyle=col;g.globalAlpha*=k;rr(x0,y+130-86,ww,86,6);g.fill();g.globalAlpha/=k||1;};
    const k1=ease(lt/0.4),k2=ease((lt-0.6)/0.4);
    g.save();g.globalAlpha*=k1;g.fillStyle=C.piezo;rr(x+w*0.18,y+44,w*0.2,86,6);g.fill();g.restore();
    g.save();g.globalAlpha*=k2;g.fillStyle=C.piezo;rr(x+w*0.50,y+44,w*0.2,86,6);g.fill();
    g.strokeStyle=C.fg;g.lineWidth=3;g.beginPath();g.moveTo(x+w*0.38,y+20);g.lineTo(x+w*0.38,y+34);g.moveTo(x+w*0.38,y+27);g.lineTo(x+w*0.50,y+27);g.moveTo(x+w*0.50,y+20);g.lineTo(x+w*0.50,y+34);g.stroke();
    font(700,30,FD);txt('100 µs',x+w*0.44,y+10,C.fg,'center');g.restore();
    font(600,22,FD);txt('injecția 1',x+w*0.28,y+160,C.muted,'center');txt('injecția 2',x+w*0.60,y+160,C.muted,'center');
  }
  if(kind==='count'){
    for(const [row,n,col,lab] of [[0,3,C.mag,'Magnetic în animație'],[1,10,C.piezo,'Piezo · până la 10']]){
      font(600,24,FD);txt(lab,x,y+24+row*84,C.muted);
      for(let j=0;j<10;j++){const on=j<n&&p*10>j;g.fillStyle=on?col:C.panel2;rr(x+j*(w/10),y+38+row*84,w/10-12,26,6);g.fill();}
    }
  }
  if(kind==='down'){
    ['CONSUM','EMISII','ZGOMOT'].forEach((s,i)=>{const k=ease((lt-i*0.45)/0.4);const cx=x+w*(i+0.5)/3;
      g.save();g.globalAlpha*=k;g.fillStyle=C.panel2;rr(cx-140,y+10,280,150,12);g.fill();
      g.fillStyle='#5fd38a';g.beginPath();const ay=y+30+(1-k)*-20;g.moveTo(cx-16,ay);g.lineTo(cx+16,ay);g.lineTo(cx+16,ay+34);g.lineTo(cx+36,ay+34);g.lineTo(cx,ay+72);g.lineTo(cx-36,ay+34);g.lineTo(cx-16,ay+34);g.closePath();g.fill();
      font(700,34,FD);txt(s,cx,y+142,C.fg,'center');g.restore();});
  }
}
function whyCards(t){
  const kq=fade(t,Q+0.1,RS[0]-0.05,0.35);
  if(kq>0){g.save();g.globalAlpha=kq;g.fillStyle='rgba(13,17,22,.86)';rr(90,1010,900,230,18);g.fill();
    font(700,74,FD);txt('De ce e superior piezo?',540,1105,C.fg,'center');
    const kb=ease((t-(Wd(9,'Bosch')-0.1))/0.3);g.globalAlpha=kq*kb;font(700,54,FD);txt('BOSCH SPUNE AȘA',540,1190,C.piezo,'center');g.restore();}
  let i=-1;for(let k=0;k<RS.length;k++)if(t>=RS[k])i=k;
  if(i<0||t>R1+0.2)return;
  const a=RS[i],b=i+1<RS.length?RS[i+1]:R1+0.2,lt=t-a;const k=ease(lt/0.35)*(1-ease((t-(b-0.3))/0.3));
  const it=WHY[i],x=50,y=870,w=980,h=400;
  g.save();g.globalAlpha=k;g.translate(0,(1-k)*24);
  g.fillStyle=C.panel;rr(x,y,w,h,16);g.fill();g.strokeStyle=C.line;g.lineWidth=1.5;g.stroke();
  font(600,26,FD);g.letterSpacing='3px';txt(`BOSCH · ${i+1} DIN ${WHY.length}`,x+34,y+50,C.piezo);g.letterSpacing='0px';
  font(700,60,FD);txt(it.h,x+34,y+116,C.fg);
  font(500,30,FB);txt(it.b,x+34,y+160,'#c9d1d9');
  vis(it.vis,x+34,y+196,w-68,lt);
  g.restore();
}
function counter(t,em,ep){
  const k=ease((t-(MS0-0.1))/0.4);if(k<=0)return;
  const done=t>=MS1;const cnt=(arr,ms)=>done?arr.length:arr.filter(([s])=>s<ms).length;
  g.globalAlpha=k;
  shadowTxt(()=>{font(700,120,FD);txt(String(cnt(PULSES.multi.mag,em.ms)),118,650,C.mag,'center');txt(String(cnt(PULSES.multi.piezo,ep.ms)),962,650,C.piezo,'center');
    font(600,28,FB);txt('reprize',118,692,C.fg,'center');txt('doze',962,692,C.fg,'center');});
  g.globalAlpha=1;
}

function draw(t){
  const em=est('mag',t),ep=est('piezo',t);const sm=injState('mag',em),sp=injState('piezo',ep);
  const shot=setCamera(t);update3D(t,sm,sp);renderer.render(scene,cam);
  g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);
  // masca: sub zona 3D (grafice, subtitrări) și deasupra ei în hook
  const mb=Math.min(shot.pb,1275);let gr=g.createLinearGradient(0,mb-10,0,mb+30);gr.addColorStop(0,'rgba(13,17,22,0)');gr.addColorStop(1,'rgba(13,17,22,1)');g.fillStyle=gr;g.fillRect(0,mb-10,W,H-mb+10);
  if(shot.pt>260){const mt=shot.pt-70;gr=g.createLinearGradient(0,mt,0,mt+60);gr.addColorStop(0,'rgba(13,17,22,1)');gr.addColorStop(1,'rgba(13,17,22,0)');g.fillStyle=gr;g.fillRect(0,0,W,mt+60);}
  tags(t,shot);
  fieldLines(t,sm.on);
  labels(LB_BOTH_M,MAGX,t,M0-1.0,C.mag);labels(LB_BOTH_P,PIEX,t,M0-1.0,C.piezo);
  labels(LB_M,MAGX,t,M1-0.1,C.mag);labels(LB_P,PIEX,t,P1-0.1,C.piezo);
  const k1=fade(t,M0-0.45,Q-0.05,0.4),k2=ease((t-(S0+0.5))/0.5);
  if(k1>0){scope(30,958,500,320,'mag','single',em.ms,k1,ANN_M);scope(550,958,500,320,'piezo','single',ep.ms,k1,ANN_P);}
  if(k2>0){const full=t>=MS1;scope(30,958,500,320,'mag','multi',full?4.2:em.ms,k2,null);scope(550,958,500,320,'piezo','multi',full?4.2:ep.ms,k2,null);counter(t,em,ep);}
  whyCards(t);
}
window.__frame=t=>draw(t);
const go=()=>{draw(0);window.__ready=true;};
Promise.all(['700 66px "Barlow Condensed"','600 24px "Barlow Condensed"','500 33px Barlow','600 30px Barlow','700 30px Barlow'].map(f=>document.fonts.load(f,'ăîșțâµ'))).then(go,go);
