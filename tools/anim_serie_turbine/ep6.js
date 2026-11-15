/* ================= EPISODE 6: corpurile străine din evacuare ================= */
const EP_N=6,EP_NAME='Corpurile străine din evacuare';
const HOOK_END=Ts(2)-0.3;
const Q={hit0:W(0,'cauza')+.1,hit1:W(3,'paletele')+.2,hit2:W(7,'distrug')+.1,slow:Ts(4)-.1,ins:W(4,'iar')-.1,bal:W(5,'rotorul')-.1,brg:W(5,'turbina')-.1,
  newT:Ts(7)-.28,rest:W(7,'fără',2)-.1,fix:Ts(8)-.28,out:Ts(9)-.45};
const DIPS=[HOOK_END,Q.newT,Q.fix,Q.out],SNAPS=[],FLASHES=[Q.hit0,Q.hit2];
window.FODT=[[.3,Q.hit0],[W(3,'bucata')-.15,Q.hit1],[W(7,'resturile'),Q.hit2,Q.rest,0.3]];
window.HITT=[Q.hit0,Q.hit1,Q.hit2];
const TR={
  chipT:[[0,0],...cutAt(Q.hit0,0,1),...cutAt(HOOK_END,1,0),...cutAt(Q.hit1,0,1),...cutAt(Q.newT,1,0),...cutAt(Q.hit2,0,1),...cutAt(Q.fix,1,0),[END+3,0]],
  wobble:[[0,0],[Q.hit0,0],[Q.hit0+.5,.8],[HOOK_END-.02,1],[HOOK_END,0],[Q.hit1,0],[Q.hit1+.5,.4],[Q.bal,.4],[Q.bal+.6,1],...cutAt(Q.newT,1,0),[Q.hit2,0],[Q.hit2+.5,.9],...cutAt(Q.fix,.9,0),[END+3,0]],
  rubSide:[[0,2],[END+3,2]],
  rub:[[0,0],[Q.hit0,0],[Q.hit0+.3,.9],...cutAt(HOOK_END,.9,0),[Q.bal,0],[Q.bal+.6,.9],...cutAt(Q.newT,.9,0),[Q.hit2,0],[Q.hit2+.3,.9],...cutAt(Q.fix,.9,0),[END+3,0]],
  sparks:[[0,0],[W(1,'toate'),0],[W(1,'pe'),.5],...cutAt(HOOK_END,.5,0),[Q.brg,0],[Q.brg+.6,.7],...cutAt(Q.newT,.7,0),[END+3,0]],
  heat:[[0,0],[Q.brg,0],[Q.brg+1.2,.45],...cutAt(Q.newT,.45,0),[END+3,0]],
  spn:[[0,1.3],...cutAt(HOOK_END,1.3,1),[Q.slow,1],[Q.slow+.6,.1],[Ts(5)-.3,.1],[Ts(5)+.5,1.2],...cutAt(Q.newT,1.2,1),[END+3,1]],
  inset:[[0,0],[Q.ins,0],[Q.ins+.5,1],[Ts(5)-.4,1],[Ts(5)-.1,0],[END+3,0]],
  vgtBent:[[0,0],[W(4,'variabile'),0],[W(4,'îndoaie')+.3,1],[Ts(5),1],[Ts(5)+.2,0],[END+3,0]],
  shake:[[0,0],[Q.hit0-.03,0],[Q.hit0+.05,1],[Q.hit0+.7,0],[Q.hit1-.03,0],[Q.hit1+.05,1],[Q.hit1+.6,0],[Q.hit2-.03,0],[Q.hit2+.05,1],[Q.hit2+.7,0],[END+3,0]]
};
const fodTPos=()=>[fodTG.position.x,fodTG.position.y,fodTG.position.z],wheelT=[60,TY+28,0],cylP=[EX,-30,0],manP=[-40,38,-10];
/* hook */
addLabel('Bucată ruptă din motor',null,fodTPos,1,14,34,win(.5,Q.hit0-.02,.3,.1),'bad');
addLabel('Palete rupte',null,wheelT,1,16,40,win(Q.hit0+.3,HOOK_END-.05),'bad');
/* the path of the gas */
addLabel('Cilindru',null,cylP,-1,30,0,win(W(2,'cilindru')-.3,W(2,'trece')+.3),'fire');
addLabel('Galeria de evacuare',null,manP,1,10,44,win(W(2,'galeria')-.2,W(2,'direct')+.3),'fire');
addLabel('Roata turbinei',null,[70,TY+20,0],1,12,44,win(W(2,'roata')-.2,Te(2)+.5),'fire');
addLabel('Supapă ruptă',null,[EX+XV,-10,0],1,24,30,win(W(3,'supapă')-.3,W(3,'un')+.1),'bad');
addLabel('Segment rupt',null,()=>[EX+R,crownNow-10,0],1,24,-10,win(W(3,'segment')-.2,W(3,'sau')+.2),'bad');
addLabel('Bucată din galerie',null,[-56,36,-4],1,10,44,win(W(3,'bucată')-.2,W(3,'bucata')),'bad');
addLabel('Direct în turbină',null,fodTPos,1,14,34,win(W(3,'bucata')+.1,Q.hit1-.02,.25,.1),'bad');
addLabel('Muchii de intrare rupte',null,wheelT,1,16,40,win(Q.hit1+.4,Q.ins+.2),'bad');
addLabel('Geometrie variabilă','palete îndoite',[INS[0].x+30,INS[0].y+18,2],1,10,26,win(W(4,'paletele')+.3,Ts(5)-.35),'bad');
addLabel('Rotor dezechilibrat',null,[10,TY+5,0],1,18,44,win(Q.bal,W(5,'iar')+.2),'bad');
addLabel('Turbina nu mai are mult',null,[28,TY+8,0],1,18,40,win(Q.brg,Ts(6)+.3),'bad');
addLabel('Turbina: victima',null,[60,TY+34,0],1,14,30,win(W(6,'turbina')-.1,Q.newT-.05),'bad');
addLabel('Defectul a pornit din motor',null,cylP,1,30,10,win(W(6,'Defectul')-.1,Q.newT-.05),'bad');
addLabel('Turbină nouă',null,[60,TY+34,0],1,14,34,win(Q.newT+.1,W(7,'fără')),'good');
addLabel('Motor nereparat',null,cylP,1,30,10,win(W(7,'fără')-.1,Q.rest),'bad');
addLabel('Resturi rămase în galerie',null,fodTPos,1,10,40,win(Q.rest+.1,Q.hit2-.02,.3,.1),'bad');
addLabel('Distrusă și cea nouă',null,wheelT,1,16,40,win(Q.hit2+.25,Q.fix-.05),'bad');
/* how to avoid */
addLabel('De unde a venit bucata?',null,[EX+XV,-10,0],1,24,34,win(W(8,'găsești')-.1,W(8,'repari')-.1),'good');
addLabel('Repari motorul',null,[EX,-40,0],1,30,0,win(W(8,'repari')-.05,W(8,'și')+.1),'good');
addLabel('Cureți galeria de evacuare',null,manP,1,10,44,win(W(8,'cureți')-.1,Q.out-.05),'good');
addLabel('Gaze curate, palete întregi',null,[56,TY+27,0],1,10,40,win(Q.out+.3,END+3),'fire');
Object.assign(SHOTS,{man:{c:[-28,100],w:300,h:232,az:14,el:6},cylEx:{c:[-116,4],w:150,h:150,az:6,el:4},vgt:{c:[66,TY+100],w:150,h:196,az:6,el:3},turbK:{c:[66,TY+2],w:130,h:120,az:14,el:5},
  manMid:{c:[-36,52],w:210,h:170,az:12,el:5},turbIn:{c:[48,132],w:200,h:170,az:14,el:5},cause2:{c:[-45,92],w:330,h:300,az:10,el:5}});
const follow=(t0,t1)=>[[t0,'cylEx'],[t0+.5*(t1-t0),'manMid'],[t0+.85*(t1-t0),'turbIn'],[t1+.2,'turbK']];
const CAM=[
  [0,'cylEx'],...follow(.3,Q.hit0),[W(0,'corpurile')+.5,'turbK'],[W(1,'toate'),'shaft2'],[HOOK_END-.001,'shaft2'],
  [HOOK_END,'cylEx'],[W(2,'trece'),'cylEx'],[W(2,'evacuare'),'man'],[W(2,'direct')+.1,'man'],[Te(2)+.2,'turb2'],
  [Ts(3)+.9,'cylEx'],...follow(W(3,'bucata')-.15,Q.hit1),[Q.ins-.1,'turbK'],
  [Q.ins+.7,'vgt'],[Ts(5)-.4,'vgt'],[Ts(5)+.4,'shaft2'],[Te(5)+.1,'shaft2'],
  [Ts(6)+.6,'cause2'],[Q.newT-.001,'cause2'],
  [Q.newT,'cause2'],[Q.rest-.3,'cause2'],[Q.rest+.5,'manMid'],[W(7,'resturile'),'manMid'],[Q.hit2-.25,'turbIn'],[Q.hit2+.3,'turbK'],[Q.fix-.001,'turbK'],
  [Q.fix,'cause2'],[W(8,'găsești')-.2,'cause2'],[W(8,'găsești')+.5,'cylEx'],[W(8,'și')-.1,'cylEx'],[W(8,'cureți')+.3,'man'],[Q.out-.001,'man'],
  [Q.out,'chra'],[Te(10),'shaft'],[END+3,'wide']
];
