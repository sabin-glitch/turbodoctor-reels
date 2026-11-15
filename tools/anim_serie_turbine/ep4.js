/* ================= EPISODE 4: uleiul care nu se mai poate scurge ================= */
const EP_N=4,EP_NAME='Uleiul care nu se mai poate scurge';
const HOOK_END=Ts(2)-0.3;
const CLOG=W(3,'înfundat')-.1,CRKT=Ts(4)+.1,PUSH=W(5,'împins'),RUNA=W(7,'supraturări')-.3;
const NEWT=Ts(8)-0.28,CLEAN=Ts(9)-0.28,OUT=Ts(10)-0.45;
const DIPS=[HOOK_END,NEWT,CLEAN,OUT],SNAPS=[],FLASHES=[];
const TR={
  dclog:[[0,1],...cutAt(HOOK_END,1,0),[CLOG,0],[W(3,'calamină')+.4,1],[CRKT-.3,1],[CRKT+.5,0],...cutAt(NEWT,0,1),...cutAt(CLEAN,1,0),[END+3,0]],
  flood:[[0,.25],[W(0,'cauza'),.7],[W(0,'uleiul'),1],...cutAt(HOOK_END,1,0),[W(3,'calamină'),0],[Te(3)+.2,.5],[W(5,'Uleiul'),.5],[W(5,'turbină')+.4,1],[NEWT-.02,1],[NEWT,0],[NEWT+.5,0],[Te(8),.95],...cutAt(CLEAN,.95,0),[END+3,0]],
  leak:[[0,.3],[W(0,'cauza'),1],...cutAt(HOOK_END,1,0),[PUSH-.2,0],[W(5,'etanșări,'),1],[NEWT-.02,1],[NEWT,0],[W(8,'turbina,'),0],[Te(8),1],...cutAt(CLEAN,1,0),[END+3,0]],
  blue:[[0,.2],[W(0,'cauza'),1],...cutAt(HOOK_END,1,0),[W(5,'etanșări,'),0],[W(5,'evacuare.'),1],[NEWT-.02,1],[NEWT,0],[W(8,'problema'),0],[Te(8)+.3,.9],...cutAt(CLEAN,.9,0),[END+3,0]],
  oilAir:[[0,.2],[W(0,'cauza'),1],...cutAt(HOOK_END,1,0),[W(5,'etanșări,'),0],[W(5,'admisie')+.3,1],[NEWT-.02,1],[NEWT,0],[W(8,'problema'),0],[Te(8)+.3,.9],...cutAt(CLEAN,.9,0),[END+3,0]],
  pool:[[0,0],[W(6,'ulei')-.2,0],[W(6,'intercooler')+.6,.8],[NEWT,1],...cutAt(CLEAN,1,0),[END+3,0]],
  low:[[0,0],[W(6,'consum')-.2,0],[W(6,'ulei.',1)+.4,.55],...cutAt(CLEAN,.55,0),[END+3,0]],
  blowby:[[0,0],[CRKT,0],[W(4,'presiune:')+.2,1],[W(5,'Uleiul'),1],[W(5,'turbină'),.5],[NEWT-.02,.5],[NEWT,0],[END+3,0]],
  vcrust:[[0,0],[W(7,'ars'),0],[W(7,'variabilă,')+.3,1],...cutAt(NEWT,1,0),[END+3,0]],
  eng:[[0,1],[RUNA,1],[RUNA+1.2,2.0],...cutAt(NEWT,2.0,1),[END+3,1]],
  spn:[[0,1],[RUNA,1],[RUNA+1.2,1.5],...cutAt(NEWT,1.5,1),[END+3,1]],
  shake:[[0,0],[RUNA,0],[RUNA+1,.7],...cutAt(NEWT,.7,0),[END+3,0]]
};
const sealC=[-65.5,TY+7.4,0],sealT=[45,TY+7.3,0],dTop=()=>[OIL_A,TY-42,0],crank=[EX+34,-168,0];
/* hook */
addLabel('Ulei în admisie',null,[-71,TY+22,0],-1,16,28,win(W(0,'cauza')-.2,HOOK_END-.05),'bad');
addLabel('Fum albastru',null,[124,TY+6,-6],1,10,30,win(W(0,'din'),HOOK_END-.05),'bad');
addLabel('Retur blocat',null,drainPt(0.11),1,20,-6,win(.3,HOOK_END-.05),'bad');
/* how it works */
addLabel('Intră sub presiune',null,[OIL_A,TY+46,0],1,22,10,win(W(2,'intră')-.1,W(2,'dar')),'oil');
addLabel('Iese singur','prin cădere liberă',dTop,1,22,0,win(W(2,'iese')-.1,W(2,'înapoi')),'oil');
addLabel('Conducta de retur',null,drainPt(0.16),-1,22,0,win(W(2,'conducta')-.1,W(2,'înapoi')),'oil');
addLabel('Baia de ulei',null,[EX-20,-194,0],1,30,-30,win(W(2,'baia')-.2,Te(2)+.3),'oil');
/* blocked return */
addLabel('Retur înfundat','calamină sau furtun îndoit',drainPt(0.11),1,22,-4,win(CLOG+.1,W(3,'uleiul')),'bad');
addLabel('Uleiul nu mai are pe unde ieși',null,[-3,TY-24,0],-1,26,4,win(W(3,'uleiul'),Te(3)+.3),'bad');
/* crankcase pressure */
addLabel('Presiune în carter',null,crank,1,30,-20,win(W(4,'carter')-.1,W(4,'Sunt')),'bad');
addLabel('Ventilația carterului','înfundată',[EX-50,-150,0],1,20,40,win(W(4,'ventilația')-.1,W(4,'sau')+.2),'bad');
addLabel('Segmenți uzați',null,()=>[EX+R,crownNow-12,0],1,34,10,win(W(4,'segmenți')-.1,W(4,'Sunt')),'bad');
addLabel('Câțiva milibari','sunt de ajuns',drainPt(0.5),1,24,0,win(W(4,'Sunt'),Te(4)+.3),'num');
/* oil pushed out */
addLabel('Uleiul se adună',null,[-3,TY-22,0],-1,26,-30,win(W(5,'adună')-.1,PUSH),'bad');
addLabel('Spre admisie',null,[-71,TY+22,0],-1,16,28,win(W(5,'admisie')-.5,Te(5)+.3),'bad');
addLabel('Spre evacuare',null,[58,TY+25,0],1,14,30,win(W(5,'evacuare.')-.4,Te(5)+.3),'bad');
addLabel('Pe lângă etanșări',null,sealT,1,22,-30,win(PUSH+.2,W(5,'admisie')-.3),'bad');
addLabel('Fum albastru',null,[124,TY+6,-6],1,10,30,win(W(6,'fum')-.1,W(6,'ulei')),'bad');
addLabel('Ulei în intercooler',null,[-266,112,0],1,26,-20,win(W(6,'intercooler')-.3,W(6,'consum')+.1),'bad');
addLabel('Consum de ulei',null,[EX-20,-198,0],1,30,-30,win(W(6,'consum')+.2,W(6,'Pare')+.2),'bad');
addLabel('Turbina: bună',null,[0,TY+34,0],1,22,30,win(W(6,'turbina')-.1,Te(6)+.3),'good');
addLabel('Cauza','returul sau presiunea din carter',drainPt(0.45),1,24,0,win(W(6,'cauza')-.1,Te(6)+.3),'bad');
addLabel('Geometrie variabilă','încleiată de uleiul ars',[62,TY+31,0],1,10,34,win(W(7,'încleiază')-.1,W(7,'iar')+.2),'bad');
addLabel('Motorul arde ulei',null,()=>[EX,Math.min(-12,crownNow*0.5),0],1,30,-30,win(W(7,'admisie')-.2,RUNA+.3),'bad');
addLabel('Supraturare','necontrolată',()=>[EX,Math.min(-12,crownNow*0.5),0],1,30,-30,win(RUNA+.3,NEWT-.05),'bad');
addLabel('Turbină nouă',null,[0,TY+34,0],1,22,30,win(NEWT+.1,W(8,'problema')-.2),'good');
addLabel('Aceeași problemă',null,[-3,TY-22,0],-1,26,-30,win(W(8,'problema'),CLEAN-.05),'bad');
/* how to avoid */
addLabel('Retur curat','montat corect, fără silicon',drainPt(0.11),1,22,-4,win(W(9,'Retur')-.1,W(9,'ventilația')-.1),'good');
addLabel('Ventilația carterului','verificată',[EX-50,-150,0],1,20,40,win(W(9,'ventilația')-.1,W(9,'ulei')-.1),'good');
addLabel('Ulei doar până la maxim',null,[EX-20,-190,0],1,30,-30,win(W(9,'ulei')-.1,OUT-.05),'good');
addLabel('Uleiul iese liber prin retur',null,dTop,1,22,0,win(OUT+.3,END+3),'oil');
Object.assign(SHOTS,{crank:{c:[EX+50,-110],w:290,h:240,az:8,el:4},drainUp:{c:[-40,30],w:300,h:420,az:10,el:5}});
const CAM=[
  [0,'chra'],[W(0,'cauza')-.5,'chra'],[W(0,'din')+.2,'shaft2'],[HOOK_END-.001,'shaft2'],
  [HOOK_END,'chraIn'],[W(2,'dar'),'chraIn'],[W(2,'iese')+.4,'drain'],[W(2,'înapoi')-.2,'drain'],[W(2,'baia'),'sump'],[Te(2)+.1,'sump'],
  [CLOG,'drain'],[Te(3)+.2,'drain'],
  [CRKT+.6,'crank'],[W(4,'Sunt')-.2,'crank'],[W(4,'Sunt')+.6,'drainUp'],[Te(4)+.2,'drainUp'],
  [W(5,'adună'),'chra'],[PUSH-.1,'chra'],[W(5,'etanșări,'),'shaft2'],[Te(5)+.2,'shaft2'],
  [W(6,'fum')+.3,'out'],[W(6,'ulei')-.2,'out'],[W(6,'intercooler'),'ic'],[W(6,'consum')-.1,'ic'],[W(6,'consum')+.5,'sump'],[W(6,'Pare'),'sump'],[W(6,'turbina')-.1,'cause'],[Te(6)+.2,'cause'],
  [W(7,'încleiază')-.2,'turb2'],[W(7,'iar'),'turb2'],[W(7,'admisie'),'cyl'],[NEWT-.001,'cyl'],
  [NEWT,'shaft2'],[CLEAN-.001,'shaft2'],
  [CLEAN,'drain'],[W(9,'ventilația')-.4,'drain'],[W(9,'ventilația')+.3,'crank'],[W(9,'ulei')-.2,'crank'],[W(9,'ulei')+.4,'sump'],[OUT-.001,'sump'],
  [OUT,'chra'],[Te(10),'shaft'],[END+3,'wide']
];
