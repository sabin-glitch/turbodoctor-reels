/* ================= EPISODE 3: oprirea motorului la cald ================= */
const EP_N=3,EP_NAME='Oprirea motorului la cald';
const HOOK_END=Ts(2)-0.3;
const STOP0=W(0,'oprirea')-.1,STOP=W(4,'oprești')+.35,RST=W(6,'La')-.1,FAILT=Ts(7);
const CLEAN=Ts(8)-0.28,OUT=Ts(10)-0.45;
const DIPS=[HOOK_END,CLEAN,OUT],SNAPS=[],FLASHES=[];
const TR={
  eng:[[0,1],[STOP0,1],[STOP0+.5,0],...cutAt(HOOK_END,0,1),[STOP,1],[STOP+.5,0],[RST,0],[RST+.6,.8],...cutAt(CLEAN,.8,.9),[W(8,'lași'),.9],[W(8,'ralanti.'),.22],[Ts(9),.22],[Ts(9)+.8,.5],[END+3,.5]],
  spn:[[0,1],[STOP0,1],[STOP0+3.2,0],...cutAt(HOOK_END,0,1),[STOP,1],[STOP+3.6,0],[RST,0],[RST+1.2,.9],...cutAt(CLEAN,.9,1),[W(8,'lași'),1],[W(8,'ralanti.')+.5,.2],[Ts(9),.2],[Ts(9)+.8,.5],[END+3,.5]],
  gas:[[0,1],[STOP0+.2,1],[STOP0+1.6,0],...cutAt(HOOK_END,0,1),[STOP+.2,1],[STOP+1.6,0],[RST,0],[RST+.8,1],[END+3,1]],
  airK:[[0,1],[STOP0+.2,1],[STOP0+2.4,0],...cutAt(HOOK_END,0,1),[STOP+.2,1],[STOP+2.4,0],[RST,0],[RST+1.2,1],[END+3,1]],
  hotT:[[0,1],[HOOK_END-.02,.9],[HOOK_END,.35],[W(2,'turbina'),.5],[W(2,'fierbinte.')+.3,1],[W(5,'Se'),1],[RST,.7],[RST+1,.6],...cutAt(CLEAN,.6,1),[W(8,'lași'),1],[Te(8),.3],[Te(9),.12],[END+3,.1]],
  soak:[[0,0],[STOP0+.3,0],[STOP0+3.4,1],...cutAt(HOOK_END,1,0),[W(5,'Căldura'),0],[W(5,'lagăre')+.6,1],[RST,1],[RST+1.5,.35],[FAILT,.35],...cutAt(CLEAN,.5,0),[END+3,0]],
  smoke:[[0,0],[STOP0+1.4,0],[STOP0+3,1],...cutAt(HOOK_END,1,0),[W(5,'coace')-.2,0],[W(5,'uleiul.'),1],[W(6,'returul.'),.8],[RST+.5,.25],...cutAt(CLEAN,.25,0),[END+3,0]],
  coke:[[0,0],[STOP0+1.6,0],[HOOK_END-.02,.8],[HOOK_END,0],[W(5,'coace'),0],[W(5,'calamină.')+.4,.5],[W(6,'înfundă'),.55],[W(6,'returul.')+.5,1],...cutAt(CLEAN,1,0),[END+3,0]],
  starve:[[0,0],[RST,0],[RST+.01,.5],[FAILT,.6],[Te(7),.8],...cutAt(CLEAN,.8,0),[END+3,0]],
  only:[[0,1],[END+3,1]],
  leakSide:[[0,1],[END+3,1]],
  sparks:[[0,0],[W(7,'cedează')-.2,0],[W(7,'lagărul')+.2,.9],...cutAt(CLEAN,.9,0),[END+3,0]],
  heat:[[0,0],[W(7,'cedează')-.2,0],[W(7,'evacuare')+.2,.9],...cutAt(CLEAN,.9,0),[END+3,0]],
  wobble:[[0,0],[W(7,'lagărul'),0],[W(7,'evacuare'),.4],...cutAt(CLEAN,.4,0),[END+3,0]],
  leak:[[0,0],[W(7,'segmentul')-.1,0],[W(7,'etanșare')+.3,.9],...cutAt(CLEAN,.9,0),[END+3,0]],
  blue:[[0,0],[W(7,'etanșare'),0],[Te(7),.7],...cutAt(CLEAN,.7,0),[END+3,0]]
};
const brgR=[28,TY+8.8,0],thz=[66,TY+34,-6];
/* hook */
addLabel('Turbină fierbinte',null,thz,1,14,26,win(.3,STOP0+.6),'fire');
addLabel('Motor oprit','uleiul nu mai curge',[OIL_A,TY+40,0],-1,24,6,win(STOP0+.5,HOOK_END-.05),'bad');
addLabel('Uleiul se coace',null,brgR,1,24,-26,win(STOP0+2.2,HOOK_END-.05),'bad');
/* story */
addLabel('Gaze de evacuare','foarte fierbinți',()=>[30,62,-44],1,30,-10,win(W(2,'drum'),W(2,'turbina')),'fire');
addLabel('Turbină fierbinte',null,thz,1,14,26,win(W(2,'turbina')+.1,Te(2)+.3),'fire');
addLabel('Uleiul unge',null,[28,TY+5.6,0],1,24,22,win(W(3,'uleiul')-.1,Te(3)+.3),'oil');
addLabel('Și duce căldura',null,()=>[OIL_A,TY-42,0],-1,22,0,win(W(3,'duce')-.1,Te(3)+.3),'oil');
addLabel('Motor oprit',null,()=>[EX,Math.min(-12,crownNow*0.5),0],1,30,-30,win(STOP+.1,W(4,'pompa')),'bad');
addLabel('Pompa de ulei oprită',null,[EX+40,-186,0],1,30,24,win(W(4,'pompa')-.1,W(4,'Uleiul')),'bad');
addLabel('Uleiul rămâne pe loc',null,[OIL_A+14,TY+18,0],1,22,26,win(W(4,'Uleiul'),Te(4)+.3),'bad');
addLabel('Căldură din evacuare',null,[52,TY+22,0],1,14,30,win(W(5,'Căldura'),W(5,'coace')),'fire');
addLabel('Uleiul se coace',null,brgR,1,24,-26,win(W(5,'coace'),W(5,'Se')),'bad');
addLabel('Calamină',null,[34,TY-9.6,0],1,24,-26,win(W(5,'formează'),Te(5)+.3),'bad');
addLabel('Canal de ulei înfundat',null,[16,TY+18,0],1,22,26,win(W(6,'înfundă'),W(6,'și')+.1),'bad');
addLabel('Retur înfundat',null,[OIL_A,TY-40,0],-1,24,0,win(W(6,'returul.')-.1,RST+.2),'bad');
addLabel('Tot mai puțin ulei','la fiecare pornire',[-34,TY+6.2,0],-1,26,26,win(W(6,'lagărele'),Te(6)+.3),'bad');
addLabel('Lagărul dinspre evacuare',null,brgR,1,20,30,win(W(7,'lagărul')-.1,W(7,'și')+.1),'bad');
addLabel('Segmentul de etanșare',null,[45,TY-7.4,0],1,22,-26,win(W(7,'segmentul')-.1,CLEAN-.05),'bad');
/* how to avoid */
addLabel('Ralanti','între 1 și 3 minute',()=>[-14,TY+5,5],-1,20,-30,win(W(8,'ralanti.')-.2,Te(8)+.3),'num');
addLabel('Uleiul scoate căldura',null,()=>[OIL_A,TY-42,0],1,22,0,win(W(8,'Producătorii'),Te(8)+.3),'oil');
addLabel('Ultimii kilometri','mergi liniștit',thz,1,14,26,win(W(9,'liniștit')-.1,OUT-.05),'good');
addLabel('Turbină răcită înainte de oprire',null,[28,TY+5.6,0],1,24,22,win(OUT+.3,END+3),'good');
const CAM=[
  [0,'shaft'],[STOP0-.2,'shaft'],[STOP0+2.6,'hot'],[HOOK_END-.001,'hot'],
  [HOOK_END,'wide'],[W(2,'drum'),'wide'],[W(2,'turbina'),'turb'],[Te(2),'turb'],
  [Ts(3)+.3,'chraIn'],[W(3,'duce')-.2,'chraIn'],[W(3,'duce')+.5,'chra'],[Te(3)+.1,'chra'],
  [STOP-.2,'mid'],[W(4,'se')-.1,'mid'],[W(4,'pompa')+.2,'pump'],[W(4,'Uleiul')-.3,'pump'],[W(4,'Uleiul')+.5,'chraIn'],[Te(4),'chraIn'],
  [W(5,'Căldura')+.3,'shaft'],[W(5,'trece'),'shaft'],[W(5,'lagăre')+.3,'hot'],[Te(5),'hot'],
  [W(6,'înfundă')+.2,'chra'],[RST-.2,'chra'],[RST+.8,'shaft'],[W(6,'lagărele'),'brg'],[Te(6),'brg'],
  [W(7,'lagărul'),'hot'],[CLEAN-.001,'hot'],
  [CLEAN,'shaft'],[W(8,'lași'),'shaft'],[W(8,'ralanti.')+.5,'brg'],[W(8,'Producătorii'),'chra'],[Te(8),'chra'],[Ts(9)+.6,'turb'],[OUT-.001,'turb'],
  [OUT,'brg'],[Te(10),'shaft'],[END+3,'wide']
];
