/* ================= EPISODE 2: uleiul murdar ================= */
const EP_N=2,EP_NAME='Uleiul murdar';
const HOOK_END=Ts(2)-0.3;
const NEW2=Ts(6)-0.3,CLEAN=Ts(8)-0.28,OUT=Ts(9)-0.45,RUB1=W(0,'uleiul')+.1,RUB2=W(5,'ating'),DEAD=W(5,'distrusă.');
const DIPS=[HOOK_END,NEW2,CLEAN,OUT],SNAPS=[],FLASHES=[RUB1,DEAD];
const TR={
  showFilt:[[0,1],[END+3,1]],
  dirty:[[0,1],...cutAt(HOOK_END,1,0),[Ts(3),0],[W(3,'murdar,')+.5,1],...cutAt(NEW2,1,.15),[W(6,'schimbul'),.15],[W(6,'amânat.')+.5,1],...cutAt(CLEAN,1,0),[END+3,0]],
  dirt:[[0,1],...cutAt(HOOK_END,1,0),[W(3,'particulele')-.3,0],[W(3,'intră'),1],...cutAt(NEW2,1,0),[W(6,'uleiul')-.2,0],[W(6,'nefiltrat.'),1],...cutAt(CLEAN,1,0),[END+3,0]],
  score:[[0,.8],[HOOK_END-.02,1],[HOOK_END,0],[W(4,'Zgârie')-.1,0],[W(4,'lagărele.')+.3,1],...cutAt(NEW2,1,0),[END+3,0]],
  sparks:[[0,.5],[RUB1,.8],...cutAt(HOOK_END,.8,0),[W(3,'lucrează'),0],[W(3,'șmirghel.'),.35],[W(4,'lagărele.'),.5],[W(5,'bată,'),.8],...cutAt(NEW2,.8,0),[END+3,0]],
  wobble:[[0,.45],[RUB1,1],...cutAt(HOOK_END,1,0),[W(4,'Jocul')-.1,0],[W(4,'crește,')+.4,.5],[W(5,'începe'),.55],[W(5,'bată,')+.2,1],...cutAt(NEW2,1,0),[END+3,0]],
  rub:[[0,0],[RUB1-.1,0],[RUB1+.15,1],...cutAt(HOOK_END,1,0),[RUB2-.15,0],[RUB2+.2,1],...cutAt(NEW2,1,0),[END+3,0]],
  heat:[[0,.3],[HOOK_END-.02,.5],[HOOK_END,0],[W(4,'Zgârie'),0],[W(5,'bată,'),.45],...cutAt(NEW2,.5,0),[END+3,0]],
  air:[[0,1],[RUB1,1],[HOOK_END-.02,.5],[HOOK_END,1],[RUB2,1],[DEAD+.5,.3],...cutAt(NEW2,.3,1),[END+3,1]],
  spn:[[0,1],[RUB1,1],[HOOK_END-.02,.55],[HOOK_END,1],[RUB2,1],[DEAD+.8,.3],...cutAt(NEW2,.3,1),[END+3,1]],
  filt:[[0,0],[W(6,'Filtrul')-.1,0],[W(6,'înfundă,')+.4,1],...cutAt(CLEAN,1,0),[END+3,0]],
  bypass:[[0,0],[W(6,'supapa')+.2,0],[W(6,'deschide,')+.4,1],...cutAt(CLEAN,1,0),[END+3,0]]
};
const brgL=[-34,TY+6.2,0],brgR=[28,TY+8.8,0],tipC=[-78,TY+27.5,0];
/* hook */
addLabel('Ulei murdar',null,[OIL_A+12,TY+18,0],1,22,26,win(.3,RUB1-.2),'bad');
addLabel('Ax zgâriat',null,[-33,TY+5,3],-1,24,-26,win(1.2,RUB1-.2),'bad');
addLabel('Paletele ating carcasa',null,tipC,-1,10,26,win(RUB1+.25,HOOK_END-.05),'bad');
/* how it works */
addLabel('Film de ulei','axul plutește',[28,TY+5.6,0],1,24,22,win(W(2,'Plutește')-.1,Te(2)+.3),'oil');
addLabel('Lagăr',null,[-34,TY-7.6,0],-1,22,-22,win(W(2,'lagărele.')-.1,Te(2)+.3),'oil');
/* dirt */
addLabel('Ulei murdar',null,[OIL_A,TY+40,0],1,22,10,win(W(3,'murdar,')-.1,W(3,'intră')),'bad');
addLabel('Particule în filmul de ulei',null,brgL,-1,26,26,win(W(3,'intră'),W(3,'lucrează')+.1),'bad');
addLabel('Ca un șmirghel',null,brgR,1,24,22,win(W(3,'lucrează')+.2,Te(3)+.3),'bad');
addLabel('Ax zgâriat',null,[-33,TY+5,3],-1,24,-26,win(W(4,'Zgârie')+.1,W(4,'Jocul')),'bad');
addLabel('Lagăr uzat',null,brgR,1,24,22,win(W(4,'lagărele.')-.1,W(4,'Jocul')),'bad');
addLabel('Joc mărit','axul nu mai stă pe centru',[28,TY+5.6,0],1,24,22,win(W(4,'Jocul'),Te(4)+.3),'bad');
addLabel('Axul bate',null,()=>[-14,TY+5,5],-1,20,-30,win(W(5,'bată,')-.1,RUB2-.1),'bad');
addLabel('Paletele ating carcasa',null,tipC,-1,10,26,win(RUB2,W(5,'turbina')+.2),'bad');
addLabel('Turbină distrusă',null,[0,TY+34,0],1,22,30,win(DEAD-.2,NEW2-.05),'bad');
/* where the dirt comes from */
addLabel('Schimb de ulei amânat',null,[EX-20,-196,0],1,30,-30,win(W(6,'schimbul')-.1,W(6,'Filtrul')-.1),'bad');
addLabel('Filtru de ulei',null,[FLT.x0+20,FLT.yc+FLT.ro+3,0],-1,10,14,win(W(6,'Filtrul')-.3,W(6,'înfundă,')),'oil');
addLabel('Filtru înfundat',null,[FLT.x0+22,FLT.yc+14,0],-1,10,22,win(W(6,'înfundă,'),W(6,'supapa')+.2),'bad');
addLabel('Supapa de ocolire','deschisă',[FLT.x1-8,FLT.yc,0],-1,12,-24,win(W(6,'supapa')+.3,Te(6)+.3),'bad');
addLabel('Ulei nefiltrat','spre turbină',[FLT.x0+2,FLT.yc,0],-1,6,24,win(W(6,'trece'),Te(6)+.35),'bad');
addLabel('Funingine de la ardere',null,()=>[EX,Math.min(-10,crownNow*0.5),0],1,30,-30,win(W(7,'funinginea')-.1,W(7,'din',2)),'bad');
addLabel('Motorină în ulei',null,[EX-20,-196,0],1,30,-30,win(W(7,'motorina')-.1,W(7,'și')),'bad');
addLabel('Șpan','după o reparație de motor',[EX+60.6,-120,0],1,20,10,win(W(7,'șpanul')-.1,CLEAN-.05),'bad');
/* how to avoid */
addLabel('Ulei schimbat la timp',null,[EX-20,-194,0],1,30,-30,win(W(8,'Schimbi'),W(8,'cu')),'good');
addLabel('Filtru schimbat la timp',null,[FLT.x0+20,FLT.yc+FLT.ro+3,0],-1,10,14,win(W(8,'filtrul')-.1,W(8,'Iar')-.1),'good');
addLabel('Turbină nouă','ulei și filtru noi',[0,TY+34,0],1,22,30,win(W(8,'turbină')-.1,OUT-.05),'good');
addLabel('Ulei curat în lagăre',null,[28,TY+5.6,0],1,24,22,win(OUT+.3,END+3),'oil');
Object.assign(SHOTS,{hk2:{c:[-36,TY+6],w:170,h:124,az:6,el:4},sumpF:{c:[-104,-166],w:190,h:130,az:5,el:3}});
const CAM=[
  [0,'brg'],[W(0,'cauza')-.3,'brg'],[RUB1,'hk2'],[RUB1+2,'hk2'],[HOOK_END-.001,'comp2'],
  [HOOK_END,'shaft'],[W(2,'nu'),'shaft'],[W(2,'lagărele.'),'brg'],[Te(2),'brg'],
  [Ts(3)+.1,'chraIn'],[W(3,'particulele'),'chraIn'],[W(3,'intră')+.3,'brg'],[W(4,'Jocul'),'brg'],[W(5,'începe'),'hook'],[W(5,'bată,')+.3,'hook'],[RUB2-.1,'comp2'],[W(5,'iar'),'comp2'],[DEAD,'shaft'],[NEW2-.001,'shaft'],
  [NEW2,'cause'],[W(6,'Din')-.2,'cause'],[W(6,'schimbul')+.3,'sumpF'],[W(6,'Filtrul')-.4,'sumpF'],[W(6,'Filtrul')+.3,'filt'],[Te(6)+.2,'filt'],
  [Ts(7)+.5,'cyl'],[W(7,'din',2)-.2,'cyl'],[W(7,'motorina')+.4,'sump'],[W(7,'și')-.1,'sump'],[W(7,'șpanul')+.3,'crank'],[CLEAN-.001,'cause'],
  [CLEAN,'sumpF'],[W(8,'filtrul')-.3,'sumpF'],[W(8,'filtrul')+.4,'filt'],[W(8,'Iar')-.2,'filt'],[W(8,'turbină'),'shaft'],[OUT-.001,'shaft'],
  [OUT,'brg'],[Te(9),'shaft'],[END+3,'wide']
];
