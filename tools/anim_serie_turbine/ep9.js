/* ================= EPISODE 9: geometria variabilă blocată ================= */
const EP_N=9,EP_NAME='Geometria variabilă blocată';
const HOOK_END=Ts(2)-0.3;
const Q={stuck:W(0,'cauza'),ring:W(2,'inel')-.1,soot:Ts(3),seize:W(3,'înțepenesc')-.1,open:Ts(4)-.28,weak:W(4,'motorul')-.2,shut:Ts(5)-.28,ovr:W(5,'Urmează')-.1,
  src:Ts(6)-.28,cc:W(6,'din',2)-.2,trip:W(6,'din',4)-.2,fix:Ts(7)-.28,pcv:W(7,'ventilația')-.2,trip2:W(7,'din')-.2,out:Ts(8)-.45};
const DIPS=[HOOK_END,Q.open,Q.shut,Q.src,Q.fix,Q.out],SNAPS=[],FLASHES=[];
const osc=(t0,t1,p,lo,hi)=>{const k=[];let v=0;for(let t=t0;t<t1;t+=p/2){k.push([t,v%2?hi:lo]);v++;}return k;};
const GV=[[0,.7],[Q.open,.7],[W(4,'turbina'),.7],[W(4,'presiune')+.3,.15],[Q.shut-.02,.15],[Q.shut,.7],[W(5,'împinsă')-.2,.7],[W(5,'maximă')+.3,1.18],[Q.src-.02,1.18],[Q.src,.7],[END+3,.7]];
window.GAUGE={title:'PRESIUNEA DE SUPRAALIMENTARE',
  state:v=>v<0.4?{hot:true,sub:'prea mică: motorul nu mai trage',txt:'PREA MICĂ'}:(v>1?{hot:true,sub:'peste limită: supraturare',txt:'PREA MARE'}:{hot:false,sub:'cât cere motorul',txt:'POTRIVITĂ'}),
  vis:t=>Math.max(win(W(2,'ca')-.2,Q.src-.05)(t),win(Q.trip2+.5,Q.out-.05)(t)),val:t=>track(GV,t)+0.012*Math.sin(t*8)};
const TR={
  inset:[[0,1],[W(1,'Vezi')+.6,1],[W(1,'pe')-.1,0],[HOOK_END,0],[Q.ring,0],[Q.ring+.5,1],[Q.weak+.1,1],[Q.weak+.5,0],[Q.shut-.02,0],[Q.shut,1],[Q.ovr+.1,1],[Q.ovr+.5,0],[Q.src,0],[Q.trip,0],[Q.trip+.5,1],[Q.fix-.02,1],[Q.fix,0],[Q.trip2,0],[Q.trip2+.5,1],[Q.out-.02,1],[Q.out,0],[END+3,0]],
  vgtPos:[...osc(0,3.7,1.2,.1,.9),[Q.stuck,.12],[HOOK_END-.02,.12],[HOOK_END,.5],[W(2,'Ele'),.5],[W(2,'închid')+.4,.08],[W(2,'și'),.08],[W(2,'deschid')+.4,.95],[W(2,'ca'),.95],[W(2,'ca')+.8,.5],[Q.soot,.5],
    [Q.soot+.8,.75],[Q.soot+1.8,.35],[Q.seize,.6],[Q.open-.02,.6],[Q.open,.95],[Q.shut-.02,.95],[Q.shut,.05],[Q.src-.02,.05],[Q.src,.5],[Q.trip2,.5],...osc(Q.trip2+.3,Q.out,1.4,.15,.9),[END+3,.5]],
  vgtSoot:[[0,0],[1.2,0],[4,1],[HOOK_END-.02,1],[HOOK_END,0],[Q.soot,0],[W(3,'ele')+.3,1],[Q.src-.02,1],[Q.src,0],[Q.trip+.2,0],[Te(6)+.2,1],[Q.fix-.02,1],[Q.fix,0],[END+3,0]],
  vgtJit:[[0,0],[Q.stuck-.1,0],[Q.stuck+.25,1],[HOOK_END-.02,1],[HOOK_END,0],[Q.seize,0],[Q.seize+.4,1],[Q.src-.02,1],[Q.src,0],[END+3,0]],
  spn:[[0,1],[Q.stuck,1],[W(0,'geometria'),2.6],[HOOK_END-.02,2.6],[HOOK_END,1],[W(2,'închid'),1],[W(2,'închid')+.5,.7],[W(2,'deschid'),.7],[W(2,'deschid')+.6,1.5],[Q.soot,1],[Q.open,1],
    [W(4,'turbina')+.5,.45],[Q.shut-.02,.45],[Q.shut,1],[W(5,'împinsă'),1],[W(5,'maximă')+.3,2.8],[Q.src-.02,2.8],[Q.src,1],[END+3,1]],
  eng:[[0,1.5],...cutAt(HOOK_END,1.5,1),[W(2,'închid'),1],[W(2,'închid')+.5,.6],[W(2,'deschid'),.6],[W(2,'deschid')+.6,1.7],[Q.soot,1],[Q.shut,1],[W(5,'turbina'),1.7],[Q.src-.02,1.7],[Q.src,1],[END+3,1]],
  airK:[[0,1],[W(4,'turbina'),1],[W(4,'presiune')+.3,.3],[Q.shut-.02,.3],[Q.shut,1],[END+3,1]],
  grow:[[0,0],[W(1,'Vezi'),0],[W(1,'pe'),.8],...cutAt(HOOK_END,.8,0),[Q.ovr,0],[W(5,'supraturarea')+.5,.9],...cutAt(Q.src,.9,0),[END+3,0]],
  rubSide:[[0,1],[END+3,1]],
  rub:[[0,0],[W(1,'pe'),0],[W(1,'pe')+.5,.8],...cutAt(HOOK_END,.8,0),[W(5,'supraturarea'),0],[W(5,'supraturarea')+.4,.9],...cutAt(Q.src,.9,0),[END+3,0]],
  wobble:[[0,0],[W(1,'pe'),0],[HOOK_END-.02,.6],[HOOK_END,0],[W(5,'supraturarea')+.3,0],[Q.src-.02,.7],[Q.src,0],[END+3,0]],
  sootGas:[[0,0],[W(6,'multă')-.2,0],[W(6,'funingine')+.5,1],[Q.cc,1],[Q.cc+.8,.4],[Q.fix-.02,.4],[Q.fix,0],[END+3,0]],
  blowby:[[0,0],[Q.cc,0],[W(6,'suflat')+.4,.9],[Q.trip,.9],[Q.trip+.6,.3],...cutAt(Q.fix,.3,0),[END+3,0]],
  oilAir:[[0,0],[W(6,'suflat'),0],[W(6,'carter')+.3,.9],...cutAt(Q.fix,.9,0),[END+3,0]],
  gasHot:[[0,0],[Q.trip2,0],[W(7,'drum')+.3,.6],[Q.out,.6],[Q.out+.5,0],[END+3,0]]
};
const wheelC=[-98,TY+19,0],insP=[INS[0].x+30,INS[0].y+18,2],manP=[-40,38,-10],burnP=()=>[EX,Math.min(-12,crownNow*0.5),0];
/* hook */
addLabel('Palete mobile',null,insP,1,10,26,win(.5,Q.stuck-.1));
addLabel('Blocate de funingine',null,insP,1,10,26,win(Q.stuck+.1,W(1,'pe')-.1),'bad');
addLabel('Supraturare',null,wheelC,1,18,36,win(W(1,'pe')+.3,HOOK_END-.05),'bad');
/* how it works */
addLabel('Inel de palete mobile','în jurul roții turbinei',[59,TY+33,0],1,14,40,win(Ts(2)+.3,Q.ring+.3),'fire');
addLabel('Închise','la turații mici',insP,1,10,26,win(W(2,'închid')-.1,W(2,'și')+.1),'fire');
addLabel('Deschise','la turații mari',insP,1,10,26,win(W(2,'deschid')-.1,W(2,'ca')+.1),'fire');
addLabel('Presiunea potrivită',null,insP,1,10,26,win(W(2,'presiunea')-.3,Te(2)+.3),'good');
addLabel('Funingine și ulei ars',null,insP,1,10,26,win(Q.soot+.1,W(3,'și',2)),'bad');
addLabel('Palete înțepenite',null,insP,1,10,26,win(W(3,'și',2)+.1,Q.open-.05),'bad');
addLabel('Blocate pe deschis',null,insP,1,10,26,win(Q.open+.1,Q.weak),'bad');
addLabel('Motorul nu mai trage','intră în avarie',wheelC,1,18,36,win(Q.weak+.5,Q.shut-.05),'bad');
addLabel('Blocate pe închis',null,insP,1,10,26,win(Q.shut+.1,Q.ovr),'bad');
addLabel('Supraturare','cauza 8',wheelC,1,18,36,win(Q.ovr+.6,Q.src-.05),'bad');
/* where the deposits come from */
addLabel('Multă funingine',null,[-70,34,0],1,14,44,win(W(6,'multă')-.1,W(6,'de',2)),'bad');
addLabel('Recircularea gazelor',null,manP,1,10,44,win(W(6,'recircularea')-.2,W(6,'și')+.1),'bad');
addLabel('Ardere proastă',null,burnP,1,30,-30,win(W(6,'ardere')-.2,Q.cc),'bad');
addLabel('Ulei suflat din carter',null,[EX+34,-168,0],1,30,-20,win(W(6,'uleiul')-.1,Q.trip),'bad');
addLabel('Multe drumuri scurte',null,insP,1,10,26,win(W(6,'multe')+.2,Q.fix-.05),'bad');
/* how to avoid */
addLabel('Motor care arde curat',null,burnP,1,30,-30,win(W(7,'Motor')-.1,Q.pcv),'good');
addLabel('Ventilația carterului','în stare bună',[EX-50,-150,0],1,20,40,win(Q.pcv+.3,W(7,'și')+.1),'good');
addLabel('Din când în când','un drum mai lung',insP,1,10,26,win(Q.trip2+.5,Q.out-.05),'good');
addLabel('Palete libere, presiune potrivită',null,[56,TY+27,0],1,10,40,win(Q.out+.3,END+3),'fire');
Object.assign(SHOTS,{compS:{c:[-62,TY],w:200,h:130,az:-4,el:4},vgt:{c:[66,TY+100],w:150,h:196,az:6,el:3},turbK7:{c:[70,TY+8],w:124,h:150,az:14,el:5},
  cylTop:{c:[EX+24,-6],w:200,h:170,az:6,el:4},crank9:{c:[EX+40,-104],w:250,h:214,az:8,el:4}});
const CAM=[
  [0,'vgt'],[W(1,'Vezi'),'vgt'],[W(1,'pe'),'shaft'],[HOOK_END-.001,'shaft'],
  [HOOK_END,'turbK7'],[Q.ring,'turbK7'],[Q.ring+.8,'vgt'],[Q.open-.001,'vgt'],
  [Q.open,'vgt'],[Q.weak,'vgt'],[Q.weak+.8,'compS'],[Q.shut-.001,'compS'],
  [Q.shut,'vgt'],[Q.ovr,'vgt'],[Q.ovr+.8,'compS'],[Q.src-.001,'compS'],
  [Q.src,'cylTop'],[Q.cc-.1,'cylTop'],[Q.cc+.7,'crank9'],[Q.trip-.1,'crank9'],[Q.trip+.7,'vgt'],[Q.fix-.001,'vgt'],
  [Q.fix,'cylTop'],[Q.pcv-.1,'cylTop'],[Q.pcv+.6,'crank9'],[W(7,'și')-.1,'crank9'],[Q.trip2+.5,'vgt'],[Q.out-.001,'vgt'],
  [Q.out,'chra'],[Te(9),'shaft'],[END+3,'wide']
];
