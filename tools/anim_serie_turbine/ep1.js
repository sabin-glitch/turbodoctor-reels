/* ================= EPISODE 1: lipsa ungerii ================= */
const EP_N=1,EP_NAME='Lipsa ungerii';
const HOOK_END=Ts(2)-0.3;
const SNAP1=W(0,'lipsa')+0.15,SNAP2=W(4,'rupe.')+0.12;
const NEW2=Ts(5)-0.3,NEW3=Ts(6)-0.3,NEW4=Ts(7)-0.28,CLEAN=Ts(8)-0.28,OUT=Ts(9)-0.45;
const DIPS=[HOOK_END,NEW2,NEW3,NEW4,CLEAN,OUT],SNAPS=[[SNAP1,HOOK_END],[SNAP2,NEW2]],FLASHES=[SNAP1,SNAP2];
const DRY7=W(7,'turezi'),WET7=W(7,'turbină.')+0.5;
const TR={
  starve:[[0,1],...cutAt(HOOK_END,1,0),[Ts(3)-.1,0],[W(3,'lagăre,')+.5,1],...cutAt(NEW2,1,0),[W(5,'Nivel')+.3,0],[Te(5),1],...cutAt(NEW3,1,0),[END+3,0]],
  low:[[0,0],[NEW2,0],[W(5,'Nivel')-.1,0],[W(5,'baie,')+.2,1],...cutAt(NEW3,1,0),[END+3,0]],
  pump:[[0,0],[W(5,'pompă')-.2,0],[W(5,'slăbită')+.3,1],...cutAt(NEW3,1,0),[END+3,0]],
  clog:[[0,0],[W(5,'depuneri')-.1,0],[W(5,'alimentare')+.2,1],...cutAt(NEW3,1,0),[END+3,0]],
  heat:[[0,.5],[SNAP1,1],...cutAt(HOOK_END,.8,0),[W(4,'Lagărele')-.1,0],[W(4,'încing,')+.5,.85],[SNAP2,1],...cutAt(NEW2,.75,0),[NEW3,0],[W(6,'fără'),0],[Te(6)+.3,.8],...cutAt(NEW4,.8,0),[DRY7+.4,0],[W(7,'uleiul')+.3,.75],[WET7,.6],...cutAt(CLEAN,.5,0),[END+3,0]],
  wobble:[[0,.5],[SNAP1-.05,1],[SNAP1,0],[W(3,'metalul')-.1,0],[W(3,'metal.'),.35],[W(4,'gripează,')-.2,.4],[W(4,'gripează,')+.3,1],[SNAP2-.05,1],[SNAP2,0],[W(6,'fără'),0],[Te(6),.5],...cutAt(NEW4,.5,0),[DRY7+.3,0],[W(7,'uleiul'),.5],[WET7,.3],...cutAt(CLEAN,.3,0),[END+3,0]],
  sparks:[[0,.6],[SNAP1-.05,1],[SNAP1,0],[W(3,'metalul')-.15,0],[W(3,'freacă')+.2,.8],[SNAP2,1],[SNAP2+.01,0],[W(6,'fără')-.1,0],[W(6,'amorsată'),.9],...cutAt(NEW4,.9,0),[DRY7+.2,0],[W(7,'motorul')+.3,.9],[WET7-.4,.9],[WET7+.2,.2],...cutAt(CLEAN,.2,0),[END+3,0]],
  prime:[[0,-1],...cutAt(NEW3,-1,.52),[Te(6)+.3,.60],...cutAt(NEW4,.6,.10),[WET7,.93],...cutAt(CLEAN,.93,-1),[END+3,-1]],
  cold:[[0,0],...cutAt(NEW4,0,1),...cutAt(CLEAN,1,0),[END+3,0]],
  spn:[[0,1],[NEW4-.01,1],[NEW4,.25],[DRY7,.25],[DRY7+.9,1.15],[CLEAN,1.15],[CLEAN+.01,1],[OUT,1],[OUT+1,.8],[END+3,.8]],
  eng:[[0,1],[NEW4-.01,1],[NEW4,.3],[DRY7,.3],[DRY7+.9,1.2],[CLEAN,1.2],[CLEAN+.01,.9],[END+3,.9]]
};
const brgL=[-34,TY+6.2,0],brgR=[28,TY+8.8,0],frac=()=>[FRAC_A+2,TY-6,2];
/* hook */
addLabel('Lagăre fără ulei',null,brgL,-1,26,26,win(.3,SNAP1+.1),'bad');
addLabel('Ax rupt',null,frac,1,22,-22,win(SNAP1+.25,HOOK_END-.05),'bad');
/* how it works */
addLabel('Până la 300.000','rotații pe minut',()=>[-14,TY+5,5],-1,20,-30,win(W(2,'300.000')-.2,W(2,'Plutește')-.1),'num');
addLabel('Film de ulei','axul plutește',[28,TY+5.6,0],1,24,22,win(W(2,'Plutește'),Te(2)+.3),'oil');
addLabel('Lagăr',null,[-34,TY-7.6,0],-1,22,-22,win(W(2,'Plutește')+.3,Te(2)+.3),'oil');
/* starvation */
addLabel('Uleiul nu mai ajunge',null,[OIL_A,TY+30,0],1,20,10,win(Ts(3)+.2,W(3,'metalul')-.1),'bad');
addLabel('Metal pe metal',null,brgL,-1,26,26,win(W(3,'metalul'),W(4,'încing,')-.1),'bad');
addLabel('Se încing',null,brgR,1,24,22,win(W(4,'încing,')-.05,W(4,'gripează,')-.05),'bad');
addLabel('Se gripează',null,brgR,1,24,22,win(W(4,'gripează,')-.05,SNAP2),'bad');
addLabel('Ax rupt',null,frac,1,22,-22,win(SNAP2+.2,NEW2-.05),'bad');
/* why */
addLabel('Nivel scăzut în baie',null,[EX-20,-196,0],1,30,-34,win(W(5,'Nivel')-.05,W(5,'pompă')-.3),'bad');
addLabel('Pompă de ulei slăbită',null,[EX+40,-186,0],1,30,24,win(W(5,'pompă')-.1,W(5,'depuneri')-.15),'bad');
addLabel('Depuneri pe alimentare',null,feedPt(0.86),-1,22,8,win(W(5,'depuneri')-.05,NEW3-.05),'bad');
addLabel('Lagăre fără ulei',null,brgR,1,24,22,win(W(5,'alimentare')+.3,NEW3-.05),'bad');
/* new turbo, not primed */
addLabel('Turbină nouă',null,[0,TY+34,0],1,22,30,win(NEW3+.1,W(6,'pornită')+.3),'good');
addLabel('Neamorsată','uleiul încă nu a ajuns',[OIL_A,TY+40,0],1,22,10,win(W(6,'fără')-.1,NEW4-.05),'bad');
addLabel('Lagăre uscate',null,brgL,-1,26,26,win(W(6,'amorsată'),NEW4-.05),'bad');
/* cold start */
addLabel('Motor rece','ulei gros, curge greu',feedPt(0.30),-1,24,0,win(NEW4+.15,W(7,'înainte')),'air');
addLabel('Turat imediat',null,()=>[-14,TY+5,5],1,20,-30,win(DRY7,W(7,'înainte')),'bad');
addLabel('Uleiul încă pe drum',null,()=>{const f=clamp(FX.prime*(FEED.path.len+190)/FEED.path.len,0.02,0.98);const p=FEED.curve.getPointAt(f);return [p.x,p.y,p.z];},-1,24,0,win(W(7,'înainte'),WET7-.3),'oil');
addLabel('Lagăre uscate',null,brgR,1,24,22,win(W(7,'înainte')+.2,WET7-.2),'bad');
/* how to avoid */
addLabel('Ulei la nivel','schimbat la timp',[EX-20,-192,0],1,30,-34,win(W(8,'Ulei')-.1,W(8,'conducte')-.1),'good');
addLabel('Conducte de ulei curate',null,feedPt(0.80),-1,22,8,win(W(8,'conducte')-.1,W(8,'fără')+.2),'good');
addLabel('Fără turații mari','în primele secunde',()=>[-14,TY+5,5],-1,20,-30,win(W(8,'fără')+.1,OUT-.05),'good');
/* outro */
addLabel('Axul pe film de ulei',null,[28,TY+5.6,0],1,24,22,win(OUT+.3,END+3),'oil');
const CAM=[
  [0,'brg'],[SNAP1-.3,'hook'],[SNAP1+1.2,'hook'],[HOOK_END-.001,'shaft'],
  [HOOK_END,'wide'],[W(2,'învârte')-.3,'wide'],[W(2,'300.000'),'shaft'],[W(2,'Plutește')-.4,'shaft'],[W(2,'Plutește')+.4,'brg'],[Te(2),'brg'],
  [Ts(3),'chraIn'],[W(3,'lagăre,'),'chraIn'],[W(3,'metalul')+.2,'brg'],[W(4,'gripează,'),'brg'],[SNAP2-.15,'hook'],[SNAP2+1,'hook'],[NEW2-.001,'shaft'],
  [NEW2,'cause'],[W(5,'Nivel')-.4,'cause'],[W(5,'Nivel')+.3,'sump'],[W(5,'pompă')-.2,'sump'],[W(5,'pompă')+.4,'pump'],[W(5,'depuneri')-.3,'pump'],[W(5,'depuneri')+.5,'feedTop'],[W(5,'alimentare')+.2,'feedTop'],[Te(5)+.1,'chraIn'],[NEW3-.001,'chraIn'],
  [NEW3,'shaft'],[W(6,'pornită'),'shaft'],[W(6,'fără')+.3,'chraIn'],[W(6,'amorsată')+.4,'brg'],[NEW4-.001,'brg'],
  [NEW4,'feedAll'],[W(7,'înainte')-.3,'feedAll'],[W(7,'uleiul')+.2,'chraIn'],[CLEAN-.001,'brg'],
  [CLEAN,'sump'],[W(8,'conducte')-.5,'sump'],[W(8,'conducte')+.3,'feedTop'],[W(8,'fără')-.1,'feedTop'],[W(8,'turații'),'shaft'],[OUT-.001,'shaft'],
  [OUT,'brg'],[Te(9),'shaft'],[END+3,'wide']
];
