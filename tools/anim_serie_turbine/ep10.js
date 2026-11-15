/* ================= EPISODE 10: filtrul de particule înfundat ================= */
const EP_N=10,EP_NAME='Filtrul de particule înfundat';
const HOOK_END=Ts(2)-0.3;
const Q={seal:Ts(4)-.28,oil:Ts(5),fat:Ts(6),new:Ts(7)-.28,fix:Ts(8)-.28,out:Ts(9)-.45,cl:W(8,'curățarea')};
Q.e7=Math.min(Te(7),Q.fix-.15);
const DIPS=[HOOK_END,Q.seal,Q.new,Q.fix,Q.out],SNAPS=[],FLASHES=[];
const GV=[[0,.45],[W(3,'cresc')-.1,.45],[W(3,'presiunea')+.6,1.2],[Q.cl-.3,1.2],[Q.cl+1.0,.45],[END+3,.45]];
window.GAUGE={title:'CONTRAPRESIUNEA DIN EVACUARE',sub:'gazele ies liber',over:'gazele nu mai au pe unde ieși',okTxt:'NORMALĂ',hotTxt:'PREA MARE',
  vis:t=>Math.max(win(W(3,'În')-.2,Q.oil-.1)(t),win(W(7,'filtrul')-.1,Q.out-.05)(t)),val:t=>track(GV,t)+0.012*Math.sin(t*8)};
const TR={
  showDpf:[[0,1],[END+3,1]],
  dpfClog:[[0,.08],[.5,.08],[3.9,1],...cutAt(HOOK_END,1,.12),[W(2,'plin')-.2,.12],[W(2,'dop')+.5,1],[Q.cl-.5,1],[Q.cl+.9,.05],[END+3,.05]],
  gasHot:[[0,0],[2,0],[4.5,.8],...cutAt(HOOK_END,.8,0),[W(3,'ieși')-.2,0],[W(3,'temperatura')+.5,.85],...cutAt(Q.new,.85,0),[W(7,'sunt'),0],[W(7,'mari')+.3,.85],...cutAt(Q.fix,.85,.6),[Q.cl-.3,.6],[Q.cl+1.0,0],[END+3,0]],
  hotT:[[0,0],[2.5,0],[6,.9],...cutAt(HOOK_END,.9,0),[W(3,'și',2)-.2,0],[W(3,'temperatura')+.8,.8],[Q.fat-.3,.8],[Q.fat+.3,.35],[Q.fat+.8,1],[Q.fat+1.3,.4],[W(6,'roata')+.1,1],...cutAt(Q.new,1,0),
    [W(7,'sunt')+.3,0],[Q.e7,.9],...cutAt(Q.fix,.9,.5),[Q.cl-.3,.5],[Q.cl+1.0,0],[END+3,0]],
  gasIn:[[0,0],[W(1,'Vezi'),0],[W(1,'pe')+.5,.9],...cutAt(HOOK_END,.9,0),[W(4,'trec')-.2,0],[W(4,'segmentul')+.4,1],[Q.fat,1],[Q.fat+.5,.6],...cutAt(Q.new,.6,0),[W(7,'șanse'),0],[Q.e7,.9],...cutAt(Q.fix,.9,0),[END+3,0]],
  coke:[[0,0],[W(1,'pe'),0],[HOOK_END-.1,.7],...cutAt(HOOK_END,.7,0),[W(4,'coc')-.1,0],[W(4,'uleiul')+.7,.9],...cutAt(Q.new,.9,0),[W(7,'cedeze')-.2,0],[Q.e7,.7],...cutAt(Q.fix,.7,0),[END+3,0]],
  smoke:[[0,0],[W(1,'pe')+.3,0],[HOOK_END-.1,.6],...cutAt(HOOK_END,.6,0),[W(4,'coc'),0],[W(4,'uleiul')+.8,.6],[Q.oil,.6],[Q.oil+.5,0],[END+3,0]],
  clog:[[0,0],[W(4,'înfundă')-.1,0],[W(4,'alimentarea')+.5,.85],...cutAt(Q.new,.85,0),[END+3,0]],
  starve:[[0,0],[W(4,'alimentarea'),0],[W(4,'uzează')+.3,.8],...cutAt(Q.new,.8,0),[END+3,0]],
  score:[[0,0],[W(4,'uzează')-.1,0],[Te(4),.9],...cutAt(Q.new,.9,0),[END+3,0]],
  sparks:[[0,0],[W(4,'uzează'),0],[W(4,'lagărele')+.2,.6],[Q.oil+.3,.6],[Q.oil+.8,0],[END+3,0]],
  wobble:[[0,0],[W(4,'uzează'),0],[Te(4),.7],[Q.fat,.5],...cutAt(Q.new,.5,0),[END+3,0]],
  leakSide:[[0,2],[END+3,2]],
  leak:[[0,0],[W(5,'împins')-.2,0],[W(5,'compresorului')+.3,.9],...cutAt(Q.new,.9,0),[END+3,0]],
  oilAir:[[0,0],[W(5,'partea'),0],[W(5,'iar'),.8],...cutAt(Q.new,.8,0),[END+3,0]],
  inset:[[0,0],[W(5,'iar')+.1,0],[W(5,'iar')+.6,1],[Q.fat-.4,1],[Q.fat-.1,0],[END+3,0]],
  vgtSoot:[[0,0],[W(5,'geometria'),0],[W(5,'calamină')+.5,1],[Q.fat,1],[Q.fat+.1,0],[END+3,0]],
  vgtPos:[[0,.5],[W(5,'iar'),.5],[W(5,'variabilă'),.8],[W(5,'încarcă'),.3],[W(5,'calamină'),.55],[END+3,.55]],
  vgtJit:[[0,0],[W(5,'încarcă'),0],[W(5,'calamină'),1],[Q.fat,1],[Q.fat+.1,0],[END+3,0]],
  crackW:[[0,0],[W(6,'roata')+.2,0],[W(6,'crăpa')+.7,1],...cutAt(Q.new,1,0),[W(7,'cedeze')-.1,0],[Q.e7+.1,1],...cutAt(Q.fix,1,0),[END+3,0]],
  spn:[[0,1.4],[3.9,.8],...cutAt(HOOK_END,.8,1),[W(2,'dop'),1],[W(3,'ieși')+.3,.75],...cutAt(Q.new,.75,1),[W(7,'sunt'),1],[Q.e7,.7],...cutAt(Q.fix,.7,.8),[Q.cl,.8],[Q.cl+1.8,1.1],[END+3,1]],
  eng:[[0,1.4],...cutAt(HOOK_END,1.4,1),[END+3,1]],
  airK:[[0,1],[2,1],[4,.6],...cutAt(HOOK_END,.6,1),[W(3,'ieși'),1],[W(3,'temperatura'),.6],...cutAt(Q.new,.6,1),[W(7,'sunt'),1],[Q.e7,.6],...cutAt(Q.fix,.6,.7),[Q.cl,.7],[Q.cl+1.8,1],[END+3,1]]
};
const brickP=[226,TY+34,0],wheelT=[72,TY+12,0],insP=[INS[0].x+30,INS[0].y+18,2];
/* hook */
addLabel('Filtru de particule',null,brickP,-1,20,56,win(.4,W(0,'cauza')-.2));
addLabel('Înfundat','gazele nu mai au pe unde ieși',brickP,-1,20,56,win(W(0,'cauza'),W(1,'pe')),'bad');
addLabel('Turbină supraîncălzită',null,wheelT,1,16,40,win(W(1,'pe')+.3,HOOK_END-.05),'bad');
/* the plug on the exhaust */
addLabel('Filtru de particule','gazele trec prin el',brickP,-1,20,56,win(HOOK_END+.3,W(2,'plin')));
addLabel('Plin de funingine',null,brickP,-1,20,56,win(W(2,'plin'),W(2,'ca')),'bad');
addLabel('Ca un dop pe eșapament',null,brickP,-1,20,56,win(W(2,'ca')+.1,Te(2)+.2),'bad');
addLabel('Gazele nu mai au pe unde ieși',null,[170,TY+16,0],-1,20,60,win(Ts(3)+.2,W(3,'În')),'bad');
addLabel('Presiune mare',null,[66,TY+40,0],1,14,40,win(W(3,'presiunea')-.2,W(3,'și',2)),'bad');
addLabel('Temperatură mare',null,[66,TY+40,0],1,14,40,win(W(3,'și',2)+.1,Q.seal-.05),'bad');
/* what the gas does inside the turbo */
addLabel('Segmentul de etanșare','al axului',[45,TY+8.5,0],1,12,40,win(W(4,'segmentul')-.3,W(4,'în')));
addLabel('Gaze fierbinți','în carcasa lagărelor',[26,TY+10.5,0],1,12,40,win(W(4,'în'),W(4,'Acolo')),'fire');
addLabel('Uleiul se coace',null,[18,TY+11,0],1,12,40,win(W(4,'coc')-.1,W(4,'înfundă')),'bad');
addLabel('Alimentare înfundată',null,[-3,TY+44,0],1,14,30,win(W(4,'înfundă'),W(4,'și')),'bad');
addLabel('Lagăre uzate',null,[-34,TY+8,0],1,14,40,win(W(4,'uzează'),Q.oil-.1),'bad');
addLabel('Ulei împins spre compresor',null,[-66,TY+9,0],1,14,40,win(W(5,'împins'),W(5,'iar')),'oil');
addLabel('Calamină','pe geometria variabilă',insP,1,10,26,win(W(5,'geometria')+.3,Q.fat-.3),'bad');
addLabel('Supraîncălziri repetate',null,wheelT,1,16,40,win(Q.fat+.5,W(6,'roata')+.2),'bad');
addLabel('Roată crăpată','prin oboseală',wheelT,1,16,40,win(W(6,'crăpa')-.1,Q.new-.05),'bad');
/* the new turbo */
addLabel('Turbină nouă',null,[-6,TY+20,0],1,16,40,win(Q.new+.3,W(7,'fără')),'good');
addLabel('Filtrul a rămas înfundat',null,brickP,-1,20,56,win(W(7,'filtrul'),W(7,'sunt')+.4),'bad');
addLabel('Cedează la fel',null,wheelT,1,16,40,win(W(7,'cedeze')-.3,Q.fix-.05),'bad');
/* how to avoid */
addLabel('Problemă de turbină?',null,[-6,TY+20,0],1,16,40,win(W(8,'La')+.2,W(8,'verifici')));
addLabel('Verifici și filtrul de particule',null,brickP,-1,20,56,win(W(8,'verifici'),W(8,'iar')),'good');
addLabel('Curățat la timp',null,brickP,-1,20,56,win(Q.cl,Q.out-.05),'good');
addLabel('Evacuare liberă',null,[112,TY+10,0],1,14,40,win(Q.out+.3,END+3),'fire');
Object.assign(SHOTS,{dpfS:{c:[186,TY],w:264,h:150,az:6,el:3},dpfT:{c:[138,TY],w:200,h:140,az:8,el:3},compS:{c:[-62,TY],w:200,h:130,az:-4,el:4},vgt:{c:[66,TY+100],w:150,h:196,az:6,el:3},
  turbH:{c:[72,TY-4],w:200,h:160,az:14,el:5},turbK7:{c:[70,TY+8],w:124,h:150,az:14,el:5},sealS:{c:[34,TY+4],w:104,h:88,az:8,el:3}});
const CAM=[
  [0,'dpfS'],[W(0,'cauza')-.3,'dpfS'],[W(0,'filtrul')+.3,'dpfT'],[W(1,'Vezi'),'dpfT'],[W(1,'pe'),'turbK7'],[HOOK_END-.001,'turbK7'],
  [HOOK_END,'dpfS'],[Te(2),'dpfS'],[W(3,'În')-.1,'dpfT'],[W(3,'cresc'),'turbH'],[Q.seal-.001,'turbH'],
  [Q.seal,'sealS'],[W(4,'Acolo')-.1,'sealS'],[W(4,'coc')+.4,'chra'],[W(4,'înfundă')-.1,'chra'],[W(4,'alimentarea'),'chraIn'],[W(4,'uzează')-.1,'chraIn'],[W(4,'uzează')+.6,'brg'],[Q.oil-.2,'brg'],
  [Q.oil+.6,'compS'],[W(5,'iar')-.1,'compS'],[W(5,'iar')+.7,'vgt'],[Q.fat-.3,'vgt'],[Q.fat+.5,'turbK7'],[Q.new-.001,'turbK7'],
  [Q.new,'shaft'],[W(7,'fără')-.1,'shaft'],[W(7,'filtrul')-.1,'dpfS'],[W(7,'sunt'),'dpfS'],[W(7,'șanse')+.8,'turbH'],[Q.fix-.001,'turbH'],
  [Q.fix,'shaft'],[W(8,'verifici')-.2,'shaft'],[W(8,'filtrul')-.1,'dpfS'],[Q.out-.001,'dpfS'],
  [Q.out,'turbH'],[Te(10),'shaft'],[END+3,'wide']
];
