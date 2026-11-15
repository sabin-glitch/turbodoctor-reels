/* ================= EPISODE 5: corpurile străine din admisie ================= */
const EP_N=5,EP_NAME='Corpurile străine din admisie';
const HOOK_END=Ts(2)-0.3;
const Q={hit0:W(0,'cauza')+.1,sand:W(3,'nisip')-.15,hit1:W(3,'uitată')+.3,hit2:Te(3)+.15,slow:Ts(4)-.1,bal:W(4,'dezechilibrează')-.1,brg:W(4,'lagărele')-.2,
  src:Ts(5)-.28,torn:W(5,'rupt')-.3,clg:W(5,'înfundat')-.1,miss:W(5,'care')-.05,hose:W(5,'De',4)-.2,fis:W(5,'fisurat')-.1,
  left:Ts(6)-.28,nut:W(6,'piulița')-.2,go:W(6,'carcasa')-.1,hit3:Ts(7)+.15,rep:W(7,'turbina')-.1,fix:Ts(8)-.28,out:Ts(9)-.45};
const DIPS=[HOOK_END,Q.src,Q.left,Q.fix,Q.out],SNAPS=[],FLASHES=[Q.hit0,Q.hit3];
window.FODS=[[.25,Q.hit0,0],[Q.hit1-.85,Q.hit1,1],[Q.hit2-.9,Q.hit2,2],[Q.go,Q.hit3,0,Q.nut]];
window.HITC=[Q.hit0,Q.hit1,Q.hit2,Q.hit3];
const TR={
  chipC:[[0,0],...cutAt(Q.hit0,0,1),...cutAt(HOOK_END,1,0),...cutAt(Q.hit1,0,1),...cutAt(Q.src,1,0),...cutAt(Q.hit3,0,1),...cutAt(Q.fix,1,0),[END+3,0]],
  wobble:[[0,0],[Q.hit0,0],[Q.hit0+.5,.8],[HOOK_END-.02,1],[HOOK_END,0],[Q.hit1,0],[Q.hit1+.4,.3],[Q.bal,.3],[Q.bal+.7,1],...cutAt(Q.src,1,0),[Q.hit3,0],[Q.hit3+.6,.6],[Q.rep,.8],[Q.fix-.02,1],[Q.fix,0],[END+3,0]],
  rubSide:[[0,1],[END+3,1]],
  rub:[[0,0],[Q.hit0,0],[Q.hit0+.3,.8],...cutAt(HOOK_END,.8,0),[Q.bal,0],[Q.bal+.6,.8],...cutAt(Q.src,.8,0),[Q.hit3,0],[Q.hit3+.4,.6],[Q.fix-.02,1],[Q.fix,0],[END+3,0]],
  sparks:[[0,0],[W(1,'toate'),0],[W(1,'pe'),.5],...cutAt(HOOK_END,.5,0),[Q.brg,0],[Q.brg+.5,.75],...cutAt(Q.src,.75,0),[Q.rep,0],[Q.rep+.8,.6],...cutAt(Q.fix,.6,0),[END+3,0]],
  heat:[[0,0],[Q.brg,0],[Q.brg+1.2,.5],...cutAt(Q.src,.5,0),[Q.rep,0],[Q.fix-.02,.4],[Q.fix,0],[END+3,0]],
  score:[[0,0],[Q.brg,0],[Q.brg+1.5,.8],...cutAt(Q.src,.8,0),[END+3,0]],
  spn:[[0,1.3],...cutAt(HOOK_END,1.3,1),[W(2,'și'),1],[W(2,'300.000')+.3,1.7],[Te(2)+.4,1.7],[Q.sand,1.3],[Q.slow,1.3],[Q.slow+.6,.1],[Q.bal-.3,.1],[Q.bal+.6,1.3],...cutAt(Q.src,1.3,1),[END+3,1]],
  sand:[[0,0],[Q.sand,0],[Q.sand+.4,1],[Q.hit1-1.0,1],[Q.hit1-.6,0],[Q.torn,0],[Q.torn+.4,.9],[Q.clg,.9],[Q.clg+.3,0],[Q.miss+.1,0],[Q.miss+.45,1],...cutAt(Q.hose,1,0),[END+3,0]],
  afTorn:[[0,0],[Q.torn-.1,0],[Q.torn+.2,1],[Q.clg,1],[Q.clg+.3,0],[END+3,0]],
  afClog:[[0,0],[Q.clg,0],[Q.clg+.6,1],[Q.miss-.1,1],[Q.miss+.15,0],[END+3,0]],
  afHide:[[0,0],...cutAt(Q.miss+.15,0,1),...cutAt(Q.hose,1,0),[END+3,0]],
  sandB:[[0,0],[Q.fis,0],[Q.fis+.5,1],...cutAt(Q.left,1,0),[END+3,0]],
  chips:[[0,0],[W(6,'șurub')-.2,0],[W(6,'șaibă')+.3,1],...cutAt(Q.fix,1,0),[END+3,0]],
  shake:[[0,0],[Q.hit0-.03,0],[Q.hit0+.05,1],[Q.hit0+.7,0],[Q.hit1-.03,0],[Q.hit1+.05,.7],[Q.hit1+.5,0],[Q.hit2-.03,0],[Q.hit2+.05,.7],[Q.hit2+.5,0],[Q.hit3-.03,0],[Q.hit3+.05,1],[Q.hit3+.7,0],[END+3,0]]
};
const fodPos=()=>[fodG.position.x,fodG.position.y,1.5],wheelC=[-98,TY+19,0];
/* hook */
addLabel('Piuliță în admisie',null,fodPos,1,14,30,win(.45,Q.hit0-.02,.25,.1),'bad');
addLabel('Palete rupte',null,wheelC,-1,16,34,win(Q.hit0+.3,HOOK_END-.05),'bad');
addLabel('Rotor dezechilibrat',null,[-20,TY-5,0],1,18,-36,win(W(0,'corpurile')+.9,HOOK_END-.05),'bad');
/* the wheel */
addLabel('Roata compresorului','din aluminiu',[-90,TY+21,0],1,16,30,win(Ts(2),W(2,'și')+.2),'air');
addLabel('300.000 rot/min',null,[-88,TY-19,0],1,16,-28,win(W(2,'300.000')-.1,Te(2)+.3),'num');
addLabel('Orice intră odată cu aerul','lovește paletele',[-138,TY+14,0],1,8,44,win(W(3,'orice')-.1,Q.sand),'bad');
addLabel('Nisip',null,[-150,TY-8,0],1,10,-34,win(Q.sand+.1,Q.hit1-.9),'bad');
addLabel('O șaibă uitată',null,fodPos,1,14,30,win(Q.hit1-.8,Q.hit1-.02,.15,.1),'bad');
addLabel('Gheață',null,fodPos,1,14,30,win(Q.hit2-.85,Q.hit2-.02,.15,.1),'bad');
/* one damaged blade is enough */
addLabel('Paletă ciupită',null,[-99,TY+15,0],1,14,30,win(W(4,'paletă')-.1,Q.bal-.1),'bad');
addLabel('Paletă îndoită',null,[-96,TY-15,0],1,14,-28,win(W(4,'îndoită')-.2,Q.bal-.1),'bad');
addLabel('Rotor dezechilibrat',null,[-20,TY+5,0],1,18,44,win(Q.bal+.1,Q.brg),'bad');
addLabel('Lagărele','nu mai rezistă mult',[-34,TY+8,0],1,18,34,win(Q.brg+.2,Q.src-.05),'bad');
/* where they come from */
addLabel('Filtru de aer rupt',null,[-214,TY+12,30],1,16,48,win(Q.torn,Q.clg),'bad');
addLabel('Filtru de aer înfundat',null,[-214,TY+12,30],1,16,48,win(Q.clg+.05,Q.miss+.1),'bad');
addLabel('Fără filtru de aer',null,[-200,TY+4,0],1,10,48,win(Q.miss+.25,Q.hose-.05),'bad');
addLabel('Furtun fisurat','după filtru',[-150,TY+23,0],1,16,36,win(Q.fis,Q.left-.05),'bad');
addLabel('Aer nefiltrat',null,[-128,TY+8,0],1,14,-40,win(W(5,'aer',2)-.1,Q.left-.05),'bad');
addLabel('Piese uitate după o lucrare',null,[-160,TY-17,0],1,8,-36,win(W(6,'piese')-.1,Q.nut),'bad');
addLabel('Piulița turbinei vechi','rămasă în carcasa filtrului',fodPos,1,14,36,win(Q.nut+.1,Q.hit3-.02,.3,.1),'bad');
addLabel('Cel mai des motiv','al reparațiilor repetate',wheelC,1,18,36,win(W(7,'cel')-.1,Q.rep),'bad');
addLabel('Turbina nouă','cedează după câteva zile',[-20,TY+6,0],1,18,44,win(Q.rep+.05,Q.fix-.05),'bad');
/* how to avoid */
addLabel('Filtru de aer de calitate','schimbat la timp',[-212,TY+12,30],1,16,48,win(W(8,'Filtru')-.1,W(8,'furtunuri')-.1),'good');
addLabel('Furtunuri fără fisuri',null,[-150,TY+23,0],1,16,40,win(W(8,'furtunuri')-.05,W(8,'iar')),'good');
addLabel('Admisia curățată','înainte de turbina nouă',[-140,TY-17,0],1,8,-40,win(W(8,'iar')+.1,Q.out-.05),'good');
addLabel('Aer curat, palete întregi',null,wheelC,1,20,36,win(Q.out+.3,END+3),'air');
Object.assign(SHOTS,{inlet:{c:[-150,TY],w:196,h:112,az:-4,el:3},ind:{c:[-104,TY],w:86,h:90,az:-6,el:3},ind2:{c:[-94,TY],w:84,h:90,az:-12,el:4},
  compS:{c:[-62,TY],w:200,h:130,az:-4,el:4},af:{c:[-196,TY+8],w:150,h:124,az:-4,el:3},af2:{c:[-158,TY+26],w:150,h:150,az:-4,el:3}});
const CAM=[
  [0,'inlet'],[Q.hit0-.3,'inlet'],[Q.hit0+.5,'ind'],[W(0,'corpurile')+.3,'ind'],[W(0,'corpurile')+1.3,'compS'],[HOOK_END-.001,'compS'],
  [HOOK_END,'ind2'],[Te(2)+.1,'ind2'],
  [Ts(3)+.5,'inlet'],[Q.slow-.1,'inlet'],
  [Q.slow+.5,'ind'],[Q.bal-.3,'ind'],[Q.bal+.5,'compS'],[Q.brg-.1,'compS'],[Q.brg+.6,'brg'],[Q.src-.001,'brg'],
  [Q.src,'af'],[Q.hose-.1,'af'],[Q.fis+.2,'af2'],[Q.left-.001,'af2'],
  [Q.left,'inlet'],[Q.hit3-.2,'inlet'],[Q.hit3+.5,'ind'],[W(7,'spune'),'ind'],[W(7,'acesta')+.6,'compS'],[Q.fix-.001,'compS'],
  [Q.fix,'af'],[W(8,'furtunuri')-.3,'af'],[W(8,'furtunuri')+.4,'af2'],[W(8,'iar'),'af2'],[W(8,'înainte')+.5,'inlet'],[Q.out-.001,'inlet'],
  [Q.out,'compS'],[Te(10),'shaft'],[END+3,'wide']
];
