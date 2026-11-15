/* ================= EPISODE 7: temperatura prea mare a gazelor de evacuare ================= */
const EP_N=7,EP_NAME='Temperatura prea mare a gazelor';
const HOOK_END=Ts(2)-0.3;
const Q={over:W(3,'depășesc')-.2,crk:W(3,'carcasa')-.1,whl:W(3,'roata')-.1,oil:W(3,'uleiul')-.2,snap:W(5,'secunde')+.1,src:Ts(6)-.28,soft:W(6,'soft')-.2,stop:Ts(7)+.2,fix:Ts(8)-.28,out:Ts(9)-.45};
const DIPS=[HOOK_END,Q.src,Q.fix,Q.out],SNAPS=[[Q.snap,Q.src]],FLASHES=[Q.snap];
const GV=[[0,.55],[Q.over,.55],[W(3,'plajă')+.3,1.18],[Q.src-.02,1.18],[Q.src,.6],[Q.soft,.6],[W(6,'putere')+.3,1.18],[Q.fix-.02,1.18],[Q.fix,.55],[END+3,.55]];
window.GAUGE={title:'TEMPERATURA GAZELOR DE EVACUARE',sub:'în plaja de lucru a turbinei',over:'peste plaja de lucru a turbinei',okTxt:'NORMAL',hotTxt:'PREA MARE',
  vis:t=>Math.max(win(HOOK_END+.3,Q.stop+.4)(t),win(W(8,'fără'),Q.out-.05)(t)),val:t=>track(GV,t)+0.012*Math.sin(t*7)};
const TR={
  gasHot:[[0,.2],[2.2,1],[HOOK_END-.02,1],[HOOK_END,0],[Q.over,0],[W(3,'plajă')+.3,1],...cutAt(Q.src,1,0),[Q.soft,0],[W(6,'putere')+.2,1],[Q.stop+.3,1],[Q.stop+1.2,.3],...cutAt(Q.fix,.3,0),[END+3,0]],
  hotT:[[0,.1],[3,1],...cutAt(HOOK_END,1,0),[Q.over+.2,0],[Q.crk+.1,1],...cutAt(Q.src,1,0),[W(6,'putere'),0],[W(6,'ardere')+.6,.85],...cutAt(Q.fix,.85,0),[END+3,0]],
  crack:[[0,0],[W(0,'cauza')-.2,0],[W(0,'temperatura')+.7,1],...cutAt(HOOK_END,1,0),[Q.crk,0],[W(3,'crapă')+.5,1],...cutAt(Q.src,1,0),[END+3,0]],
  crackW:[[0,0],[Q.whl,0],[W(3,'obosește')+.4,1],...cutAt(Q.src,1,0),[END+3,0]],
  soak:[[0,0],[W(1,'Vezi'),0],[HOOK_END-.02,.8],[HOOK_END,0],[Q.oil,0],[Te(3)+.4,.9],...cutAt(Q.src,.9,0),[Q.stop+.4,0],[Te(7)+.3,.9],...cutAt(Q.fix,.9,0),[END+3,0]],
  coke:[[0,0],[W(1,'toate'),0],[HOOK_END-.02,.7],[HOOK_END,0],[W(3,'coace')-.2,0],[Te(3)+.5,.8],[Q.src-.02,1],[Q.src,0],[W(7,'cald')-.2,0],[Q.fix-.02,.7],[Q.fix,0],[END+3,0]],
  smoke:[[0,0],[W(1,'toate'),0],[HOOK_END-.02,.6],[HOOK_END,0],[W(3,'coace'),0],[Te(3),.6],[Ts(4)+.5,.6],[Ts(4)+1.2,0],[W(7,'cald'),0],[Q.fix-.02,.6],[Q.fix,0],[END+3,0]],
  clog:[[0,0],[Ts(4)-.1,0],[W(4,'ulei')+.3,1],...cutAt(Q.src,1,0),[END+3,0]],
  starve:[[0,0],[W(4,'iar'),0],[W(4,'ungerii')+.4,.9],[Q.src-.02,1],[Q.src,0],[END+3,0]],
  heat:[[0,0],[W(4,'lipsa'),0],[Te(4)+.3,.7],[Q.snap,1],...cutAt(Q.src,1,0),[END+3,0]],
  sparks:[[0,0],[W(4,'ungerii'),0],[Te(4)+.3,.6],[Q.snap,1],...cutAt(Q.src,1,0),[END+3,0]],
  wobble:[[0,0],[Ts(5),0],[Q.snap,1],...cutAt(Q.src,1,0),[END+3,0]],
  eng:[[0,1.4],...cutAt(HOOK_END,1.4,1),[Q.soft,1],[W(6,'putere'),1.7],[Q.stop,1.7],[Q.stop+.8,0],[Q.fix-.02,0],[Q.fix,1],[END+3,1]],
  spn:[[0,1.4],...cutAt(HOOK_END,1.4,1),[Q.soft,1],[W(6,'putere'),1.5],[Q.stop,1.5],[Q.stop+1.8,.15],[Q.fix-.02,.05],[Q.fix,1],[END+3,1]]
};
const inT=[66,TY-45,0],crkP=[64,TY+48,0],injP=[EX,30,0],hotP=[28,TY+10,0],manP=[-40,38,-10];
/* hook */
addLabel('Gaze prea fierbinți',null,inT,1,16,-30,win(.5,W(0,'cauza')+.4),'fire');
addLabel('Carcasa crapă',null,crkP,1,14,34,win(W(0,'temperatura'),HOOK_END-.05),'bad');
addLabel('Uleiul se coace',null,hotP,1,18,-44,win(W(1,'toate')+.6,HOOK_END-.05),'bad');
/* the working range */
addLabel('Plaja de temperaturi','pentru care este făcută turbina',[66,TY+30,0],1,14,40,win(W(2,'plajă')-.5,Te(2)+.3),'fire');
addLabel('Peste plajă',null,inT,1,16,-30,win(Q.over+.2,Q.crk),'bad');
addLabel('Carcasa turbinei crapă',null,crkP,1,14,34,win(Q.crk+.1,Q.whl),'bad');
addLabel('Roata obosește',null,[72,TY+12,0],1,14,-44,win(Q.whl+.1,W(3,'iar')+.2),'bad');
addLabel('Uleiul se coace','în lagăre și în conducte',hotP,1,18,30,win(Q.oil+.3,Te(3)+.3),'bad');
addLabel('Calamină în conducta de ulei',null,feedPt(0.9),1,22,0,win(Ts(4),W(4,'iar')),'bad');
addLabel('Lipsa ungerii','cauza 1',[-3,TY+10,0],1,22,34,win(W(4,'lipsa')-.1,Ts(5)+.3),'bad');
addLabel('Poate ceda în câteva secunde',null,[10,TY+5,0],1,18,44,win(W(5,'turbina'),Q.src-.05),'bad');
/* where the heat comes from */
addLabel('Soft modificat','pentru mai multă putere',injP,1,30,30,win(Q.soft,W(6,'dintr-o')-.1),'bad');
addLabel('Ardere defectuoasă',null,()=>[EX,Math.min(-12,crownNow*0.5),0],1,30,-30,win(W(6,'ardere')-.2,W(6,'sau')+.1),'bad');
addLabel('Injecție dereglată','injectoare ori pompă',injP,1,30,30,win(W(6,'injecție')-.2,W(6,'injectoare')+.5),'bad');
addLabel('Gaze prea fierbinți','spre turbină',manP,1,10,44,win(W(6,'injectoare')+.7,Q.stop+.3),'bad');
addLabel('Oprirea motorului la cald','cauza 3',hotP,1,18,34,win(W(7,'oprirea')+.4,Q.fix-.05),'bad');
/* how to avoid */
addLabel('Injecția în parametri',null,injP,1,30,30,win(W(8,'Injecția')-.1,W(8,'injectoarele')-.1),'good');
addLabel('Injectoare și pompă','verificate la timp',injP,1,30,30,win(W(8,'injectoarele'),W(8,'și',2)+.1),'good');
addLabel('Fără soft care o scoate','din plaja ei',[66,TY+30,0],1,14,40,win(W(8,'fără')+.2,Q.out-.05),'good');
addLabel('Gaze în plaja de lucru',null,[56,TY+27,0],1,10,40,win(Q.out+.3,END+3),'fire');
Object.assign(SHOTS,{turbH:{c:[72,TY-4],w:200,h:160,az:14,el:5},turbK7:{c:[70,TY+8],w:124,h:150,az:14,el:5},cylTop:{c:[EX+24,-6],w:200,h:170,az:6,el:4},manT:{c:[-10,112],w:300,h:232,az:14,el:6}});
const CAM=[
  [0,'turbH'],[W(0,'cauza'),'turbH'],[W(0,'temperatura')+.3,'turbK7'],[Te(0),'turbK7'],[W(1,'toate')+.5,'shaft2'],[HOOK_END-.001,'shaft2'],
  [HOOK_END,'turbH'],[Q.crk-.2,'turbH'],[Q.crk+.5,'turbK7'],[W(3,'iar'),'turbK7'],[Q.oil+.7,'hot'],[Te(3)+.1,'hot'],
  [Ts(4)+.5,'feedTop'],[W(4,'iar'),'feedTop'],[W(4,'lipsa'),'chra'],[Te(4),'chra'],[Ts(5)+.5,'shaft2'],[Q.src-.001,'shaft2'],
  [Q.src,'cylTop'],[W(6,'injectoare')-.2,'cylTop'],[W(6,'injectoare')+.7,'manT'],[Te(6)+.1,'manT'],
  [Q.stop+.5,'hot'],[Q.fix-.001,'hot'],
  [Q.fix,'cylTop'],[W(8,'și',2)-.3,'cylTop'],[W(8,'fără')+.3,'turbH'],[Q.out-.001,'turbH'],
  [Q.out,'chra'],[Te(10),'shaft'],[END+3,'wide']
];
