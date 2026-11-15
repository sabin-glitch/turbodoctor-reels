/* ================= EPISODE 13: uzura motorului ================= */
const EP_N=13,EP_NAME='Uzura motorului';
const HOOK_END=Ts(2)-0.3;
const Q={soot:Ts(4)-.28,sign:Ts(5)-.28,wit:Ts(6)-.28,new:W(6,'Dacă')-.2,say:Ts(7)-.28,fix:Ts(8)-.28,out:Ts(9)-.45,
  c0:W(4,'iar')-.1,c1:W(5,'consum')-.12,c2:W(5,'și')-.1,f1:W(8,'verifici')-.12};
Q.e3=Math.min(Te(3),Q.soot-.1);Q.e4=Math.min(Te(4),Q.sign-.1);Q.e6=Math.min(Te(6),Q.say-.1);Q.e7=Math.min(Te(7),Q.fix-.1);
const DIPS=[HOOK_END,Q.soot,Q.sign,Q.wit,Q.new,Q.say,Q.fix,Q.out],SNAPS=[],FLASHES=[];
const GV=[[0,.4],[Ts(3),.5],[W(3,'presiunea')+.5,1.2],[Q.say-.02,1.2],[Q.say,.4],[END+3,.4]];
window.GAUGE={title:'PRESIUNEA DIN CARTER',sub:'gazele ies prin ventilație',over:'gaze scăpate pe lângă piston',okTxt:'NORMALĂ',hotTxt:'PREA MARE',
  vis:t=>Math.max(win(Ts(3)-.1,Q.soot-.1)(t),win(Q.new+.1,Q.say-.05)(t),win(Q.f1+.05,Q.out-.05)(t)),val:t=>track(GV,t)+0.012*Math.sin(t*8)};
const TR={
  blowby:[[0,0],[.4,0],[2,1],...cutAt(HOOK_END,1,0),[W(2,'o')-.2,0],[W(2,'scapă')+.5,1],...cutAt(Q.say,1,0),[END+3,0]],
  flood:[[0,0],[2,0],[W(0,'cauza')+.5,.9],...cutAt(HOOK_END,.9,0),[W(3,'Uleiul')-.1,0],[W(3,'scurge')+.5,.8],[W(3,'împins'),1],...cutAt(Q.new,1,0),[W(6,'cea')-.1,0],[Q.e6,.95],...cutAt(Q.say,.95,0),[END+3,0]],
  leak:[[0,0],[3,0],[W(0,'cauza')+.8,1],...cutAt(HOOK_END,1,0),[W(3,'împins')-.2,0],[W(3,'etanșări')+.3,1],...cutAt(Q.new,1,0),[W(6,'nouă'),0],[Q.e6,1],...cutAt(Q.say,1,0),[END+3,0]],
  blue:[[0,0],[3.5,0],[W(0,'uzura'),1],...cutAt(HOOK_END,1,0),[W(3,'etanșări'),0],[Q.e3,.8],...cutAt(Q.sign,.8,1),...cutAt(Q.new,1,0),[W(6,'pățește')-.1,0],[Q.e6,.9],...cutAt(Q.say,.9,0),[END+3,0]],
  oilAir:[[0,0],[3.5,0],[W(0,'uzura'),1],...cutAt(HOOK_END,1,0),[W(3,'etanșări'),0],[Q.e3,.8],...cutAt(Q.sign,.8,1),...cutAt(Q.new,1,0),[W(6,'pățește')-.1,0],[Q.e6,.9],...cutAt(Q.say,.9,0),[END+3,0]],
  dirty:[[0,0],[W(4,'aduc')-.1,0],[W(4,'ulei')+.4,1],...cutAt(Q.say,1,0),[END+3,0]],
  dirt:[[0,0],[W(4,'uleiul')-.1,0],[W(4,'murdar')+.4,.9],...cutAt(Q.say,.9,0),[END+3,0]],
  score:[[0,0],[W(4,'zgârie')-.1,0],[Q.e4,.9],...cutAt(Q.new,.9,0),[END+3,0]],
  wobble:[[0,0],[W(4,'zgârie'),0],[Q.e4,.5],...cutAt(Q.sign,.5,.3),...cutAt(Q.new,.3,0),[END+3,0]],
  low:[[0,0],...cutAt(Q.c1,0,.2),[W(5,'ulei')+.5,.55],...cutAt(Q.say,.55,0),[END+3,0]],
  eng:[[0,1.3],...cutAt(HOOK_END,1.3,1),[END+3,1]]
};
const sealT=[45,TY+7.3,0],dTop=()=>[OIL_A,TY-42,0],crank=[EX+34,-168,0],ringP=()=>[EX+R,crownNow-12,0],newP=[0,TY+34,0],brgR=[28,TY+8.8,0],engP=[EX+41,-60,0],smokeP=[124,TY+6,-6],pushP=[-3,TY-22,0];
/* hook */
addLabel('Motor uzat','gaze scăpate pe lângă piston',ringP,1,34,10,win(.5,W(0,'cauza')-.3),'bad');
addLabel('Ulei pe lângă etanșări',null,sealT,1,22,-30,win(W(0,'cauza')+.6,W(1,'Vezi')),'bad');
addLabel('Fum albastru',null,smokeP,1,10,30,win(W(0,'uzura'),W(1,'Vezi')),'bad');
addLabel('Turbina: bună',null,newP,1,22,30,win(W(1,'Vezi')+.2,HOOK_END-.05),'good');
addLabel('Cauza: motorul',null,pushP,-1,26,-30,win(W(1,'pe')+.1,HOOK_END-.05),'bad');
/* blow-by */
addLabel('Segmenți și cilindri uzați',null,ringP,1,34,10,win(HOOK_END+.3,W(2,'o')),'bad');
addLabel('Gaze de ardere scăpate','pe lângă piston',ringP,1,34,10,win(W(2,'o')+.1,W(2,'în')),'bad');
addLabel('În carter',null,crank,1,30,-20,win(W(2,'în'),Ts(3)),'bad');
/* crankcase pressure */
addLabel('Presiune în carter',null,crank,1,30,-20,win(Ts(3)+.1,W(3,'Uleiul')),'bad');
addLabel('Uleiul nu se mai poate scurge',null,dTop,1,22,0,win(W(3,'nu')-.1,W(3,'și')),'bad');
addLabel('Împins afară','pe lângă etanșări',sealT,1,22,-30,win(W(3,'împins'),Q.soot-.05),'bad');
/* soot in the oil */
addLabel('Funingine în ulei',null,[EX-20,-192,0],1,30,-34,win(W(4,'funingine')-.2,Q.c0,.3,.12),'bad');
addLabel('Uleiul murdar','zgârie lagărele',brgR,1,24,22,win(Q.c0+.05,Q.sign-.05,.15,.3),'bad');
/* signs */
addLabel('Fum albastru',null,smokeP,1,10,30,win(W(5,'fum')-.2,Q.c1,.2,.12),'bad');
addLabel('Consum de ulei',null,[EX-20,-198,0],1,30,-30,win(Q.c1+.05,Q.c2,.15,.12),'bad');
addLabel('Ulei la compresor',null,[-71,TY+22,0],-1,16,28,win(Q.c2+.05,Q.wit-.05,.15,.3),'bad');
addLabel('Ulei la turbină',null,[58,TY+25,0],1,14,30,win(Q.c2+.3,Q.wit-.05,.15,.3),'bad');
/* the witness */
addLabel('Turbina: martorul',null,newP,1,22,30,win(W(6,'turbina')-.1,Q.new-.05),'good');
addLabel('Motorul: bolnavul',null,engP,1,30,10,win(W(6,'nu')-.1,Q.new-.05),'bad');
addLabel('Turbină nouă',null,newP,1,22,30,win(Q.new+.2,W(6,'cea')),'good');
addLabel('Pățește la fel',null,pushP,-1,26,-30,win(W(6,'pățește')-.2,Q.say-.05),'bad');
addLabel('O turbină ține cât motorul','spune un mare producător',newP,1,22,30,win(W(7,'o')-.1,W(7,'dacă')),'num');
addLabel('Dacă motorul este sănătos',null,engP,1,30,10,win(W(7,'dacă'),Q.fix-.05),'good');
/* how to avoid */
addLabel('Înainte de a schimba turbina',null,newP,1,22,30,win(W(8,'Înainte')-.1,Q.f1,.3,.12));
addLabel('Verifici presiunea din carter',null,crank,1,30,-20,win(Q.f1+.05,W(8,'și')+.1,.15,.3),'good');
addLabel('Și starea motorului','segmenți și cilindri',ringP,1,34,10,win(W(8,'starea')-.1,Q.out-.05),'good');
addLabel('Motor sănătos, turbină sănătoasă',null,newP,1,22,30,win(Q.out+.3,END+3),'good');
Object.assign(SHOTS,{cylR:{c:[EX+12,-44],w:176,h:184,az:6,el:4},crank9:{c:[EX+40,-104],w:250,h:214,az:8,el:4},ringS:{c:[EX+18,-40],w:128,h:116,az:6,el:4}});
const CAM=[
  [0,'ringS'],[W(0,'Astăzi')+.3,'ringS'],[W(0,'cauza')+.4,'shaft2'],[HOOK_END-.001,'shaft2'],
  [HOOK_END,'cylR'],[W(2,'o')-.1,'cylR'],[W(2,'scapă')+.5,'crank9'],[W(3,'Uleiul')-.2,'crank9'],[W(3,'turbină')+.4,'drain'],[W(3,'și')-.1,'drain'],[W(3,'împins')+.3,'shaft2'],[Q.soot-.001,'shaft2'],
  [Q.soot,'sump'],[Q.c0-.001,'sump'],[Q.c0,'chra'],[W(4,'zgârie'),'brg'],[Q.sign-.001,'brg'],
  [Q.sign,'out'],[Q.c1-.001,'out'],[Q.c1,'sump'],[Q.c2-.001,'sump'],[Q.c2,'shaft2'],[Q.wit-.001,'shaft2'],
  [Q.wit,'wide'],[Q.new-.001,'wide'],[Q.new,'shaft2'],[Q.say-.001,'shaft2'],
  [Q.say,'wide'],[W(7,'dacă'),'wide'],[Q.e7,'mid'],[Q.fix-.001,'mid'],
  [Q.fix,'shaft'],[Q.f1-.001,'shaft'],[Q.f1,'crank9'],[W(8,'și')-.1,'crank9'],[W(8,'starea')+.4,'cylR'],[Q.out-.001,'cylR'],
  [Q.out,'chra'],[Te(10),'shaft'],[END+3,'wide']
];
