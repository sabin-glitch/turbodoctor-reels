/* ================= HUD 2D: titlu, etichete, legendă, tester, texte ================= */
const C={bg:'#111417',panel:'#1b1f24',panel2:'#22272e',line:'#2c333b',fg:'#e8ecef',muted:'#8b96a2',dim:'#5d6772',
  tur:'#4aa3ff',hp:'#ff6a3d',ret:'#f2c94c',air:'#ffffff',metal:'#c9d0d8',ok:'#5fe0a0',warn:'#ff4a3d'};
const FD='"Barlow Condensed","Arial Narrow",Arial,sans-serif',FB='Barlow,Arial,sans-serif';
function font(w,s,f){g.font=`${w} ${s}px ${f}`}
function txt(s,x,y,col,al='left',bl='alphabetic'){g.fillStyle=col;g.textAlign=al;g.textBaseline=bl;g.fillText(s,x,y)}
function rr(x,y,w,h,r){g.beginPath();g.roundRect(x,y,w,h,r)}
function wrap(s,maxW){const out=[];for(const para of s.split('\n')){let line='';for(const w of para.split(' ')){const tl=line?line+' '+w:w;if(g.measureText(tl).width>maxW&&line){out.push(line);line=w}else line=tl}out.push(line)}return out}
function shadowTxt(fn){g.save();g.shadowColor='rgba(8,10,12,.95)';g.shadowBlur=12;fn();fn();g.restore()}
// etichetă cu linie de ghidaj: punct 3D → text decalat cu (dx,dy) pe ecran
function label(s,p3,dx,dy,a,col,sub){
  if(a<=0)return;const p=proj(p3);if(p[2]>1)return;
  const lines=s.split('\n');font(600,34,FD);let tw=0;for(const ln of lines)tw=Math.max(tw,g.measureText(ln).width);
  if(sub){font(500,24,FB);tw=Math.max(tw,g.measureText(sub).width);}
  const side=dx<0?-1:1;
  let tx=p[0]+dx;tx=side<0?clamp(tx,tw+50,1040):clamp(tx,40,1030-tw);const ty=clamp(p[1]+dy,window.__VOM?560:300,window.__VOM?1190:1420);
  g.save();g.globalAlpha=a;g.strokeStyle=col;g.lineWidth=2.5;g.beginPath();g.moveTo(p[0],p[1]);
  g.lineTo(tx-side*24,ty);g.lineTo(tx,ty);g.stroke();
  g.fillStyle=col;g.beginPath();g.arc(p[0],p[1],6,0,7);g.fill();
  const al=side<0?'right':'left',x=tx+side*10;
  {const bh=lines.length*36+(sub?30:0)+14,by=ty-(lines.length-1)*18-18-7,bx=side<0?x-tw-12:x-12;g.fillStyle='rgba(13,16,19,.62)';rr(bx,by,tw+24,bh,8);g.fill();}   // fond discret sub text, ca eticheta să se citească și peste metal
  shadowTxt(()=>{font(600,34,FD);lines.forEach((ln,j)=>txt(ln,x,ty+j*36-(lines.length-1)*18,C.fg,al,'middle'));
    if(sub){font(500,24,FB);txt(sub,x,ty+lines.length*18+18,col===C.tur?'#b4d8ff':col,al,'middle');}});
  g.restore();
}
const PIc=(n,u)=>()=>SYS.PIPES[n].curve.getPointAt(u);
const LBL=[
  // [text, punct, dx, dy, t0, t1, culoare, sub]
  ['Rezervor',()=>V([-800,492,-250]),170,-150,6.2,9.8,C.fg],
  ['Filtru de motorină',()=>V([FP[0],FP[1]+170,FP[2]]),90,-190,6.6,9.8,C.fg],
  ['Pompă de înaltă presiune',()=>V([PP[0],PP[1]+60,PP[2]]),-60,150,7.0,9.8,C.hp],
  ['Rampă comună\nși injectoare',()=>V([1700,720,-110]),190,60,7.4,9.8,C.hp],
  ['Rezervor',()=>V([TMp[0]-190,TMp[1]-8,TMp[2]-140]),-40,-230,11.2,15.2,C.fg],
  ['Pompă electrică\nauxiliară',()=>V([TMp[0]+14,TMp[1]-170,TMp[2]+14]),250,90,11.6,15.2,C.tur,'la majoritatea mașinilor'],
  ['Sită',()=>V([TMp[0]+30,TMp[1]-240,TMp[2]+8]),230,150,12.2,15.2,C.fg],
  ['Tur spre motor',PIc('feedA',0.05),120,190,12.6,15.2,C.tur,'joasă presiune'],
  ['Retur',PIc('retMain',0.972),230,-150,13.0,15.2,C.ret,'înapoi în rezervor'],
  ['Filtru de motorină',()=>V([FP[0]+40,FP[1]+40,FP[2]+26]),170,150,16.8,20.8,C.fg,'între rezervor și pompă'],
  ['Cartuș din hârtie plisată',()=>V([FP[0]+1,FP[1]+60,FP[2]+32]),-190,170,17.4,20.8,C.fg],
  ['Intrare din rezervor',()=>V([FP[0]-44,FP[1]+167,FP[2]-18]),-150,-130,17.9,20.8,C.tur],
  ['Ieșire spre pompa de\nînaltă presiune',()=>V([FP[0]-6,FP[1]+167,FP[2]-52]),170,-150,18.4,20.8,C.tur],
  ['Pompă de înaltă\npresiune Bosch CP4',()=>V([PP[0]+20,PP[1]+40,PP[2]+40]),-150,190,22.4,26.3,C.hp],
  ['Rampă comună',()=>V([1700,712,-150]),150,-190,22.9,26.3,C.hp,'common rail'],
  ['Injectoare',()=>V([1548,POS.injY+172,132]),-190,-150,23.4,26.3,C.fg],
  ['Retur injectoare',PIc('leak',0.6),30,190,23.9,26.3,C.ret],
  ['Retur spre rezervor',PIc('retMain',0.55),-200,-60,28.0,31.2,C.ret],
  ['Tur spre motor',PIc('feedA',0.5),210,60,28.4,31.2,C.tur],
  ['Filtru vechi, îmbâcsit',()=>V([FP[0],FP[1]+70+SYS.cartOld.position.y,FP[2]+30+SYS.cartOld.position.z]),-170,120,32.6,35.4,C.fg],
  ['Filtru nou, gol',()=>V([FP[0]+SYS.cartNew.position.x,FP[1]+70+SYS.cartNew.position.y,FP[2]+30]),-170,150,36.6,39.8,C.fg,'plin cu aer'],
  ['Aer în conductă',PIc('feedB',0.18),190,-150,37.4,39.8,'#ffffff'],
  ['Motorina umple filtrul',()=>V([FP[0]+2,FP[1]+40,FP[2]+44]),-170,170,41.2,45.0,C.tur],
  ['Aerul iese pe retur',PIc('retMain',0.5),-190,-70,46.8,51.2,'#ffffff'],
  ['Pompa din rezervor\nlucrează în cicluri',()=>V([TMp[0],TMp[1]+20,TMp[2]]),200,-90,46.6,51.2,C.tur],
  ['Aer spre pompă',PIc('feedB',0.3),170,-170,55.6,57.5,'#ffffff'],
  ['Pompa CP4\naspiră aer',()=>V([PP[0]+10,PP[1]+40,PP[2]+40]),-170,200,58.8,60.2,C.warn],
  ['Pompa CP4',()=>V([PP[0],PP[1]+60,PP[2]]),-150,170,79.4,84.6,C.warn,'pilitură'],
  ['Rampă și injectoare',()=>V([1700,712,-60]),170,-170,80.6,84.6,C.warn,'contaminate'],
  ['Retur',PIc('retMain',0.5),-190,-70,85.4,89.8,C.warn,'pilitura ajunge înapoi'],
  ['Rezervor',()=>V([-800,492,-250]),170,-150,86.6,89.8,C.warn,'contaminat'],
];
const cpP=(x,y,z)=>V([PP[0]+x,PP[1]+y,PP[2]+z]);
const LBL_CP=[
  ['Arbore cu camă dublă',()=>cpP(6,-12,14),-200,200,61.2,64.8,C.fg],
  ['Rolă',()=>cpP(4,CP.S.h-2,7),230,60,61.6,64.8,C.fg],
  ['Tachet',()=>cpP(0.5,CP.S.h+14,12),-230,-75,62.0,64.8,C.fg],
  ['Arc',()=>cpP(9,CP.S.h+24,0.5),250,-50,62.4,64.8,C.fg],
  ['Piston',()=>cpP(2.5,CP.S.h+40,2.5),-230,-110,62.8,64.8,C.fg],
  ['Spre rampă',()=>cpP(40,81.6,0.5),150,-170,63.2,64.8,C.hp],
  ['Motorina unge totul',()=>cpP(22,-10,0.5),190,190,61.6,64.8,C.tur],
  ['Fără film de ungere',()=>cpP(3,CP.S.h-5.5,6),230,90,65.4,69.0,C.warn],
  ['Rola se blochează\nși alunecă pe camă',()=>cpP(0.5,CP.S.h,8),-230,60,66.6,69.0,C.warn],
  ['Tachetul se rotește\nîn alezaj',()=>cpP(0.5,CP.S.h+14,12),-230,-60,69.6,73.6,C.warn],
  ['Rola taie cama',()=>cpP(3,CP.S.h-6,3),230,110,71.0,73.6,C.warn],
  ['Pilitură metalică',()=>cpP(22,-12,0.5),170,200,74.0,78.6,C.metal],
];
function labels(t,list){for(const [s,pf,dx,dy,t0,t1,col,sub] of list){const a=fade(t,t0,t1,0.4);if(a>0)label(s,pf(),dx,dy,a,col,sub);}}
function header(t){
  const g2=g.createLinearGradient(0,0,0,330);g2.addColorStop(0,'rgba(17,20,23,.97)');g2.addColorStop(.62,'rgba(17,20,23,.9)');g2.addColorStop(1,'rgba(17,20,23,0)');g.fillStyle=g2;g.fillRect(0,0,W,330);
  font(700,26,FD);g.letterSpacing='4px';txt('TURBO DOCTOR',60,82,C.muted);g.letterSpacing='0px';
  const sc=SC.find(s=>t>=s.a&&t<s.b)||SC[SC.length-1];
  font(600,24,FD);txt(sc.n.toUpperCase(),1020,82,C.dim,'right');
  font(700,60,FD);txt('Schimbi filtrul de motorină?',60,150,C.fg);
  txt('Fă ',60,212,C.fg);const w=g.measureText('Fă ').width;txt('amorsarea corect.',60+w,212,C.tur);
}
function titleCard(t){
  const k=fade(t,0.2,TT.zoom,0.6);if(k<=0)return;
  g.globalAlpha=k;font(500,36,FB);
  shadowTxt(()=>wrap('Filtrul de motorină stă între rezervor și pompa de înaltă presiune. Ce faci după ce îl schimbi contează enorm.',940).forEach((ln,i)=>txt(ln,540,1430+i*48,'#c9d1d9','center')));
  g.globalAlpha=1;
}
const CAP=[
  [5.2,10.0,'Intrăm în mașină: sistemul de alimentare cu motorină, cu circuitul de tur și cel de retur.'],
  [10.4,15.2,'La majoritatea mașinilor, în rezervor există o pompă electrică auxiliară. Ea trimite motorina pe tur, spre motor.'],
  [15.8,20.8,'Pe drum, motorina trece prin filtrul de motorină, montat între rezervor și pompa de înaltă presiune.'],
  [21.3,26.2,'Pompa de înaltă presiune ridică presiunea până la circa 2.000 de bar și împinge motorina în rampa comună, apoi la injectoare.'],
  [26.8,31.2,'Ce nu se injectează se întoarce pe retur, de la injectoare și de la pompă, înapoi în rezervor.'],
  [31.7,35.6,'La service se schimbă filtrul de motorină.'],
  [35.8,39.8,'Filtrul nou vine gol. În el și în conducta spre pompă a intrat aer.'],
  [40.2,45.6,'Corect: amorsarea din diagnoză. Testerul pornește pompa din rezervor în cicluri și umple filtrul cu motorină.'],
  [45.8,51.3,'Aerul e împins prin pompă și iese pe retur, înapoi în rezervor. Procedura exactă depinde de sistemul de injecție și de mașină.'],
  [51.6,54.4,'Circuitul e plin, fără aer. Abia acum pornești motorul.'],
  [54.7,60.2,'Dar dacă sari peste amorsare și dai direct la cheie? Aerul ajunge primul în pompa de înaltă presiune.'],
  [60.8,64.8,'Pompa Bosch CP4 în secțiune. Cama împinge tachetul cu rolă, tachetul împinge pistonul. Totul e uns doar de motorină.'],
  [65.0,69.0,'Cu aer în loc de motorină, filmul de ungere dispare. Rola nu se mai rostogolește: se blochează și freacă pe camă.'],
  [69.2,73.6,'Tachetul se rotește în alezaj. Rola ajunge de-a curmezișul camei și începe să o taie.'],
  [73.8,78.6,'Rezultă pilitură metalică. Pompa practic se autodistruge.'],
  [79.2,84.6,'Pilitura pleacă din pompă în rampa comună și în injectoare, iar pe retur ajunge înapoi în rezervor.'],
  [84.8,89.8,'Tot sistemul e contaminat. Nu mai schimbi doar pompa: injectoare, rampă, conducte și curățarea rezervorului.'],
];
function caption(t){
  for(const [a,b,s] of CAP){const k=fade(t,a,b,0.4);if(k<=0)continue;
    g.globalAlpha=k;font(500,36,FB);const lines=wrap(s,960);
    const bleed=t>=TT.bleed&&t<TT.ok+3;const y0=bleed?1640:1560;
    shadowTxt(()=>lines.forEach((ln,i)=>txt(ln,60,y0+i*48,C.fg)));g.globalAlpha=1;}
}
function legend(t){
  const k=fade(t,5.6,TT.cp-0.3,0.5)+fade(t,TT.cont+0.2,TT.end+0.6,0.5);if(k<=0)return;
  const items=[[C.tur,'Tur'],[C.hp,'Înaltă presiune'],[C.ret,'Retur']];
  if(t>=TT.chg+4&&t<TT.cp)items.push(['#ffffff','Aer']);if(t>=TT.cont)items.push([C.metal,'Pilitură']);
  const bleed=t>=TT.bleed+0.3&&t<TT.ok+3;
  g.globalAlpha=k;font(600,28,FD);let x=60;const y=bleed?1120:1488;
  for(const [c,s] of items){g.fillStyle=c;g.beginPath();g.arc(x+9,y,9,0,7);g.fill();txt(s,x+26,y,C.muted,'left','middle');x+=g.measureText(s).width+66;}
  g.globalAlpha=1;
}
function tester(t){
  const k=fade(t,TT.bleed+0.3,TT.ok+3,0.5);if(k<=0)return;
  const x=60,y=1170,w=960,h=390;
  g.save();g.globalAlpha=k;g.translate(0,(1-ease((t-TT.bleed-0.3)/0.5))*30);
  g.fillStyle='rgba(27,31,36,.96)';rr(x,y,w,h,18);g.fill();g.strokeStyle=C.line;g.lineWidth=2;g.stroke();
  font(600,24,FD);g.letterSpacing='3px';txt('DIAGNOZĂ › FUNCȚII SPECIALE › SISTEM DE ALIMENTARE',x+34,y+50,C.muted);g.letterSpacing='0px';
  font(700,46,FD);txt('Amorsare circuit de joasă presiune',x+34,y+108,C.fg);
  const q=t>=TT.ok?1:clamp((LIFTc(t)-LIFTc(Bq))/LIFT_TOT);const fin=t>=Bq+10.7;
  const cyc=clamp(Math.floor((t-Bq-0.9)/3.5)+1,1,3);const on=liftOn(t);
  font(500,30,FB);
  const row=(i,l,v,c)=>{txt(l,x+34,y+170+i*52,C.muted,'left','middle');txt(v,x+w-34,y+170+i*52,c,'right','middle');};
  row(0,'Pompă electrică din rezervor',on?'ACTIVĂ':'pauză',on?C.tur:C.dim);
  row(1,'Ciclu de amorsare',cyc+' / 3',C.fg);
  const airPct=Math.round(100*(1-ease(clamp(q/0.96))));
  row(2,'Aer în circuit',airPct+' %',airPct>0?'#ffffff':C.ok);
  const by=y+h-74;g.fillStyle=C.panel2;rr(x+34,by,w-68,18,9);g.fill();g.fillStyle=fin?C.ok:C.tur;rr(x+34,by,Math.max(18,(w-68)*q),18,9);g.fill();
  const done=ease((t-(Bq+10.8))/0.4);
  if(done>0){g.globalAlpha=k*done;font(700,34,FD);txt('✓ FINALIZAT · sistem amorsat',x+34,by+52,C.ok,'left','middle');}
  else{font(600,28,FD);txt('În lucru… nu porni motorul',x+34,by+52,C.ret,'left','middle');}
  g.restore();
}
function warnBanner(t){
  const k=fade(t,TT.wrong+0.2,TT.cp-0.3,0.4);if(k<=0)return;
  g.save();g.globalAlpha=k;g.fillStyle='rgba(40,18,18,.88)';rr(60,1296,960,140,16);g.fill();g.strokeStyle=C.warn;g.lineWidth=2.5;g.stroke();
  font(700,52,FD);txt('FĂRĂ AMORSARE',100,1356,C.warn,'left','middle');
  font(500,30,FB);txt('Filtrul nou, gol, și motorul pornit direct la cheie',100,1406,C.fg,'left','middle');
  const cr=t>TT.wrong+1.6&&t<TT.cp;if(cr){const s=Math.sin(t*40)>0;font(700,34,FD);txt(s?'DEMAROR ◉':'DEMAROR ○',980,1356,C.ret,'right','middle');}
  g.restore();
}
function cpOverlay(t){
  const k=fade(t,TT.cp,TT.cont-0.3,0.3);if(k<=0)return;const u=t-TT.cp;
  g.globalAlpha=k;
  font(700,40,FD);txt('Bosch CP4 · secțiune',60,1340,C.fg);
  font(500,26,FB);txt('pompă de înaltă presiune unsă cu motorină',60,1378,C.muted);
  const dry=ease((u-4.4)/2.2);const x=60,y=1460,w=960;
  font(600,28,FD);txt('Ungere cu motorină',x,y,C.muted,'left','middle');txt(dry>0.5?'LIPSĂ · merge cu aer':'OK',x+w,y,dry>0.5?C.warn:C.tur,'right','middle');
  g.fillStyle=C.panel2;rr(x,y+22,w,16,8);g.fill();g.fillStyle=dry>0.5?C.warn:C.tur;rr(x,y+22,Math.max(16,w*(1-dry)),16,8);g.fill();
  const kr=fade(t,69.2,73.6,0.4);
  if(kr>0){const p=proj(cpP(0,CP.S.h+26,0));g.globalAlpha=k*kr;g.strokeStyle=C.warn;g.lineWidth=5;g.beginPath();
    const turn=ease((u-8.8)/2.6);const rx=150,ry=42;g.ellipse(p[0],p[1],rx,ry,0,Math.PI*0.15,Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn));g.stroke();
    const ang=Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn);const ex=p[0]+rx*Math.cos(ang),ey=p[1]+ry*Math.sin(ang);
    g.fillStyle=C.warn;g.beginPath();g.moveTo(ex,ey);g.lineTo(ex+16,ey-6);g.lineTo(ex+4,ey+14);g.closePath();g.fill();
    font(700,48,FD);shadowTxt(()=>txt(Math.round(turn*90)+'°',p[0]+rx+24,p[1]-34,C.warn,'left','middle'));}
  g.globalAlpha=1;
}
function okBadge(t){
  const k=fade(t,TT.ok-0.6,TT.wrong-0.1,0.4);if(k<=0)return;
  g.save();g.globalAlpha=k;const p=proj(V([FP[0],FP[1]+200,FP[2]]));
  g.fillStyle=C.ok;g.beginPath();g.arc(p[0],p[1]-40,34,0,7);g.fill();g.strokeStyle='#0f2a1c';g.lineWidth=7;g.beginPath();g.moveTo(p[0]-15,p[1]-40);g.lineTo(p[0]-4,p[1]-28);g.lineTo(p[0]+16,p[1]-54);g.stroke();
  g.restore();
}
function fadeBlack(t){
  let k=0;for(const tc of [60.2,78.7])k=Math.max(k,1-ease(Math.abs(t-tc)/0.35));
  k=Math.max(k,(1-ease(Math.abs(t-TT.wrong)/0.3))*0.85);
  if(k>0){g.fillStyle=`rgba(17,20,23,${k})`;g.fillRect(0,0,W,H);}
}
function endCard(t){
  const k=ease((t-TT.end)/0.6);if(k<=0)return;
  g.globalAlpha=k;
  g.fillStyle='rgba(27,31,36,.97)';rr(60,1080,960,700,18);g.fill();g.strokeStyle=C.line;g.lineWidth=1.5;g.stroke();
  font(700,64,FD);txt('După schimbarea filtrului:',540,1190,C.fg,'center');txt('amorsare, apoi pornire.',540,1262,C.tur,'center');
  font(500,33,FB);wrap('Fă amorsarea din diagnoză, după procedura sistemului de injecție al mașinii. O pompă CP4 care a mers cu aer poate contamina tot sistemul.',860).forEach((ln,j)=>txt(ln,540,1340+j*46,'#c9d1d9','center'));
  font(700,46,FD);g.letterSpacing='5px';txt('TURBO DOCTOR',540,1640,C.fg,'center');g.letterSpacing='0px';
  font(500,27,FB);txt('Galați · București · Iași · Piatra Neamț',540,1692,C.muted,'center');
  g.globalAlpha=1;
}
function progress(t){
  const x=60,w=960,y=1858;
  g.fillStyle=C.line;rr(x,y,w,6,3);g.fill();g.fillStyle=C.fg;rr(x,y,w*clamp(t/TOTAL),6,3);g.fill();
  for(const s of SC){const xx=x+w*s.a/TOTAL;g.fillStyle=C.bg;g.fillRect(xx-1,y,3,6);}
}
/* ---- mod „vo” (reel cu voce): fără titlu, legendă jos, texte și final; tester / banner / secțiune sus, scena mutată ca să lase loc subtitrărilor ---- */
const VO_TOP=250;
function voDy(t,shot){if(shot.cp)return -10;const tw=fade(t,TT.bleed+0.3,TT.ok+3,0.6);return lerp(110,VO.dyT,tw);}
const VO={dyT:-250};
function testerVO(t){
  const k=fade(t,TT.bleed+0.3,TT.ok+3,0.5);if(k<=0)return;
  const x=60,y=VO_TOP,w=960,h=290;
  g.save();g.globalAlpha=k;g.translate(0,-(1-ease((t-TT.bleed-0.3)/0.5))*30);
  g.fillStyle='rgba(27,31,36,.96)';rr(x,y,w,h,18);g.fill();g.strokeStyle=C.line;g.lineWidth=2;g.stroke();
  font(600,22,FD);g.letterSpacing='3px';txt('DIAGNOZĂ › FUNCȚII SPECIALE',x+30,y+42,C.muted);g.letterSpacing='0px';
  font(700,42,FD);txt('Amorsare circuit joasă presiune',x+30,y+92,C.fg);
  const q=t>=TT.ok?1:clamp((LIFTc(t)-LIFTc(Bq))/LIFT_TOT);const fin=t>=Bq+10.7;
  const cyc=clamp(Math.floor((t-Bq-0.9)/3.5)+1,1,3);const on=liftOn(t);
  const airPct=Math.round(100*(1-ease(clamp(q/0.96))));
  font(500,28,FB);
  const cell=(cx,l,v,c)=>{txt(l,cx,y+140,C.muted,'left','middle');font(700,38,FD);txt(v,cx,y+182,c,'left','middle');font(500,28,FB);};
  cell(x+30,'Pompă din rezervor',on?'ACTIVĂ':'pauză',on?C.tur:C.dim);
  cell(x+390,'Ciclu',cyc+' / 3',C.fg);
  cell(x+620,'Aer în circuit',airPct+' %',airPct>0?'#ffffff':C.ok);
  const by=y+h-62;g.fillStyle=C.panel2;rr(x+30,by,w-60,16,8);g.fill();g.fillStyle=fin?C.ok:C.tur;rr(x+30,by,Math.max(16,(w-60)*q),16,8);g.fill();
  const done=ease((t-(Bq+10.8))/0.4);
  if(done>0){g.globalAlpha=k*done;font(700,30,FD);txt('✓ FINALIZAT · sistem amorsat',x+30,by+40,C.ok,'left','middle');}
  else{font(600,26,FD);txt('În lucru… nu porni motorul',x+30,by+40,C.ret,'left','middle');}
  g.restore();
}
function warnVO(t){
  const k=fade(t,TT.wrong+0.2,TT.cp-0.3,0.4);if(k<=0)return;
  g.save();g.globalAlpha=k;g.fillStyle='rgba(40,18,18,.9)';rr(60,VO_TOP,960,130,16);g.fill();g.strokeStyle=C.warn;g.lineWidth=2.5;g.stroke();
  font(700,50,FD);txt('FĂRĂ AMORSARE',100,VO_TOP+52,C.warn,'left','middle');
  font(500,28,FB);txt('Filtrul nou, gol, și motorul pornit direct la cheie',100,VO_TOP+98,C.fg,'left','middle');
  const cr=t>TT.wrong+1.6&&t<TT.cp;if(cr){const s=Math.sin(t*40)>0;font(700,32,FD);txt(s?'DEMAROR ◉':'DEMAROR ○',980,VO_TOP+52,C.ret,'right','middle');}
  g.restore();
}
function cpVO(t){
  const k=fade(t,TT.cp,TT.cont-0.3,0.3);if(k<=0)return;const u=t-TT.cp;
  g.save();g.globalAlpha=window.__VOHOOK?0:k;
  g.fillStyle='rgba(27,31,36,.9)';rr(60,VO_TOP,960,150,16);g.fill();
  font(700,40,FD);txt('Bosch CP4 · secțiune',90,VO_TOP+48,C.fg,'left','middle');
  const dry=ease((u-4.4)/2.2);const x=90,y=VO_TOP+98,w=900;
  font(600,28,FD);txt('Ungere cu motorină',x,y,C.muted,'left','middle');txt(dry>0.5?'LIPSĂ · merge cu aer':'OK',x+w,y,dry>0.5?C.warn:C.tur,'right','middle');
  g.fillStyle=C.panel2;rr(x,y+22,w,14,7);g.fill();g.fillStyle=dry>0.5?C.warn:C.tur;rr(x,y+22,Math.max(14,w*(1-dry)),14,7);g.fill();
  g.restore();
  // săgeata de rotație a tachetului rămâne din cpOverlay
  const kr=fade(t,69.2,73.6,0.4);
  if(kr>0){const p=proj(cpP(0,CP.S.h+26,0));g.save();g.globalAlpha=k*kr;g.strokeStyle=C.warn;g.lineWidth=5;g.beginPath();
    const turn=ease((u-8.8)/2.6);const rx=150,ry=42;g.ellipse(p[0],p[1],rx,ry,0,Math.PI*0.15,Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn));g.stroke();
    const ang=Math.PI*0.15+Math.PI*1.4*Math.max(0.05,turn);const ex=p[0]+rx*Math.cos(ang),ey=p[1]+ry*Math.sin(ang);
    g.fillStyle=C.warn;g.beginPath();g.moveTo(ex,ey);g.lineTo(ex+16,ey-6);g.lineTo(ex+4,ey+14);g.closePath();g.fill();
    font(700,48,FD);shadowTxt(()=>txt(Math.round(turn*90)+'°',p[0]+rx+24,p[1]-34,C.warn,'left','middle'));g.restore();}
}
function legendVO(t){
  const k=fade(t,5.6,TT.cp-0.3,0.5)+fade(t,TT.cont+0.2,TOTAL+1,0.5);if(k<=0)return;
  const items=[[C.tur,'Tur'],[C.hp,'Înaltă presiune'],[C.ret,'Retur']];
  if(t>=TT.chg+4&&t<TT.cp)items.push(['#ffffff','Aer']);if(t>=TT.cont)items.push([C.metal,'Pilitură']);
  g.globalAlpha=Math.min(1,k);font(600,28,FD);let tw=0;for(const [,s] of items)tw+=g.measureText(s).width+66;
  let x=540-(tw-40)/2;const y=1262;
  for(const [c,s] of items){g.fillStyle=c;g.beginPath();g.arc(x+9,y,9,0,7);g.fill();shadowTxt(()=>txt(s,x+26,y,'#c4ccd4','left','middle'));x+=g.measureText(s).width+66;}
  g.globalAlpha=1;
}
window.__vo=on=>{window.__VOM=on!==false;};
function draw(t){
  t=clamp(t,0,TOTAL);const vo=!!window.__VOM;
  const shot=shotAt(t);placeCam(shot.c,shot.az,shot.el,shot.d,shot.oy+(vo?voDy(t,shot):0));update3D(t,shot);renderer.render(scene,cam);
  g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,W,H);
  if(vo){
    const gr=g.createLinearGradient(0,1150,0,1330);gr.addColorStop(0,'rgba(17,20,23,0)');gr.addColorStop(1,'rgba(17,20,23,.9)');g.fillStyle=gr;g.fillRect(0,1150,W,H-1150);
    const gt=g.createLinearGradient(0,0,0,240);gt.addColorStop(0,'rgba(17,20,23,.85)');gt.addColorStop(1,'rgba(17,20,23,0)');g.fillStyle=gt;g.fillRect(0,0,W,240);
    if(shot.cp)labels(t,LBL_CP);else labels(t,LBL);
    okBadge(t);legendVO(t);testerVO(t);warnVO(t);cpVO(t);fadeBlack(t);return;
  }
  const gy=shot.cp?1200:1300;const gr=g.createLinearGradient(0,gy,0,1460);gr.addColorStop(0,'rgba(17,20,23,0)');gr.addColorStop(shot.cp?0.45:1,shot.cp?'rgba(17,20,23,.86)':'rgba(17,20,23,.92)');gr.addColorStop(1,'rgba(17,20,23,.94)');g.fillStyle=gr;g.fillRect(0,gy,W,H-gy);
  if(window.__NOHUD)return;
  if(shot.cp)labels(t,LBL_CP);else labels(t,LBL);
  okBadge(t);
  header(t);titleCard(t);legend(t);tester(t);warnBanner(t);cpOverlay(t);caption(t);endCard(t);progress(t);fadeBlack(t);
}
