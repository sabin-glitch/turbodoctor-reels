/* ================= EPISODE 8: supraturarea ================= */
const EP_N=8,EP_NAME='Supraturarea';
const HOOK_END=Ts(2)-0.3;
const Q={hit0:W(0,'cauza')+.1,over:W(2,'Peste')-.1,hit1:W(3,'rupe')+.15,peel:Ts(4)+.1,sec:Ts(5),src:Ts(6)-.28,soft:W(6,'soft')-.3,vg:W(6,'din')-.2,cmd:W(6,'defect'),
  fat:Ts(7),fix:Ts(8)-.28,vg2:W(8,'cu')-.2,out:Ts(9)-.45};
const DIPS=[HOOK_END,Q.src,Q.fix,Q.out],SNAPS=[],FLASHES=[Q.hit0,Q.hit1];
window.HITC=[Q.hit0,Q.hit1];
const GV=[[0,.6],[Q.over,.6],[W(2,'forța')+.4,1.15],[Q.src-.02,1.15],[Q.src,.6],[Q.soft,.6],[W(6,'modificat')+.5,1.15],[Q.fix-.02,1.15],[Q.fix,.6],[END+3,.6]];
window.GAUGE={title:'TURAȚIA TURBINEI',sub:'sub turația maximă',over:'peste turația maximă',okTxt:'NORMAL',hotTxt:'SUPRATURARE',
  vis:t=>Math.max(win(HOOK_END+.3,Q.peel+.2)(t),win(Q.src+.1,Q.fat+.2)(t),win(Q.fix+.1,Q.out-.05)(t)),val:t=>track(GV,t)+0.012*Math.sin(t*9)};
const TR={
  spn:[[0,1],[.3,1],[4,3],[Q.hit0,3],[Q.hit0+.6,1.2],[HOOK_END-.02,1],[HOOK_END,1],[Q.over,1],[W(2,'forța')+.4,2.6],[Q.hit1,2.8],[Q.hit1+.5,.8],[Q.peel+.5,.15],[Q.sec,.15],[Q.sec+.4,1],
    [Q.soft,1],[W(6,'modificat')+.5,2.5],[Te(6),2.5],[Q.fat+.5,.6],[Q.fix-.02,.6],[Q.fix,1],[END+3,1]],
  eng:[[0,1.5],...cutAt(HOOK_END,1.5,1),[Q.over,1],[W(2,'forța')+.4,1.6],[Q.hit1+.5,1.6],[Q.peel,1],[Q.soft,1],[W(6,'modificat')+.5,1.8],[Te(6),1.8],[Q.fat+.5,1],[END+3,1]],
  grow:[[0,0],[2.5,0],[Q.hit0-.1,1],[Q.hit0+.4,.3],...cutAt(HOOK_END,.3,0),[W(2,'forța'),0],[W(2,'roata')+.6,.5],[Ts(3),.5],[W(3,'diametru')+.5,1],[Q.hit1,1],[Q.hit1+.5,.4],...cutAt(Q.src,.4,0),
    [W(6,'modificat'),0],[W(6,'modificat')+1.5,.5],...cutAt(Q.fix,.5,0),[END+3,0]],
  rubSide:[[0,1],[END+3,1]],
  rub:[[0,0],[3.6,0],[Q.hit0,.9],[HOOK_END-.02,.6],[HOOK_END,0],[W(3,'atinge')-.1,0],[W(3,'atinge')+.3,.9],[Q.peel,.9],[Q.peel+.4,0],[Q.sec,0],[Q.sec+.4,.8],...cutAt(Q.src,.8,0),[END+3,0]],
  chipC:[[0,0],...cutAt(Q.hit0,0,1),...cutAt(HOOK_END,1,0),...cutAt(Q.hit1,0,1),...cutAt(Q.src,1,0),[END+3,0]],
  wobble:[[0,0],[Q.hit0,0],[Q.hit0+.5,.9],[HOOK_END-.02,1],[HOOK_END,0],[Q.hit1,0],[Q.hit1+.4,.6],[Q.peel+.5,.3],[Q.sec,.3],[Q.sec+.5,1],...cutAt(Q.src,1,0),[END+3,0]],
  sparks:[[0,0],[W(1,'toate'),0],[W(1,'pe'),.5],...cutAt(HOOK_END,.5,0),[Q.sec+.3,0],[Te(5),.7],...cutAt(Q.src,.7,0),[END+3,0]],
  inset:[[0,0],[Q.peel,0],[Q.peel+.5,1],[Q.sec-.35,1],[Q.sec-.05,0],[Q.vg,0],[Q.vg+.5,1],[Q.fat-.4,1],[Q.fat-.1,0],[Q.vg2,0],[Q.vg2+.5,1],[Q.out-.02,1],[Q.out,0],[END+3,0]],
  insetKind:[[0,1],...cutAt(Q.src,1,0),[END+3,0]],
  peel:[[0,0],[W(4,'coajă')-.1,0],[W(4,'portocală')+.5,1],[Q.src,1],[END+3,1]],
  vgtPos:[[0,.5],[Q.vg,.5],[W(6,'închis')+.3,0],[Q.fix-.02,0],[Q.fix,.5],[Q.vg2,.5],[Q.vg2+1,.1],[W(8,'curată')+.5,.9],[W(8,'comanda'),.2],[W(8,'verificată')+.3,.9],[W(8,'avarie'),.3],[Q.out,.5],[END+3,.5]],
  vgtSoot:[[0,0],[Q.vg+.2,0],[W(6,'calamină')+.4,1],[W(6,'sau'),1],[Q.cmd,0],[END+3,0]],
  vgtJit:[[0,0],[Q.cmd,0],[W(6,'comanda'),1],[Q.fat-.3,1],[Q.fat,0],[END+3,0]],
  crackW:[[0,0],[Q.fat,0],[W(7,'obosesc')+.5,1],...cutAt(Q.fix,1,0),[END+3,0]],
  hotT:[[0,0],[Q.fat,0],[Te(7),.35],...cutAt(Q.fix,.35,0),[END+3,0]],
  shake:[[0,0],[Q.hit0-.03,0],[Q.hit0+.05,1],[Q.hit0+.7,0],[Q.hit1-.03,0],[Q.hit1+.05,1],[Q.hit1+.7,0],[END+3,0]]
};
const wheelC=[-98,TY+19,0],tipC=[-78,TY+27,0],insP=[INS[0].x+30,INS[0].y+18,2],peelP=[INS[1].x+20,INS[1].y+22,2];
/* hook */
addLabel('Peste turația maximă',null,wheelC,1,18,36,win(.6,Q.hit0-.05),'bad');
addLabel('Roată ruptă',null,wheelC,1,18,36,win(Q.hit0+.3,HOOK_END-.05),'bad');
/* what overspeed does to the wheel */
addLabel('Turația maximă','a turbinei',[-20,TY+5,0],1,18,44,win(W(2,'turație')-.2,Q.over));
addLabel('Forța centrifugă','întinde roata',wheelC,1,18,36,win(W(2,'forța')-.1,W(2,'care')),'bad');
addLabel('Aluminiu',null,[-90,TY-18,0],1,16,-30,win(W(2,'care'),Te(2)+.3),'air');
addLabel('Crește în diametru',null,tipC,1,14,34,win(Ts(3),W(3,'atinge')-.1),'bad');
addLabel('Atinge carcasa',null,tipC,1,14,34,win(W(3,'atinge'),W(3,'și')+.2),'bad');
addLabel('Se poate rupe',null,wheelC,1,18,36,win(Q.hit1-.1,Q.peel),'bad');
addLabel('Spatele roții',null,peelP,1,12,26,win(Q.peel+.5,W(4,'coajă')-.1),'air');
addLabel('Coajă de portocală','semnul clar al supraturării',peelP,1,12,26,win(W(4,'coajă'),Q.sec-.3),'bad');
addLabel('În câteva secunde',null,[10,TY+5,0],1,18,44,win(W(5,'câteva')-.3,Q.src-.05),'bad');
/* where it comes from */
addLabel('Soft modificat',null,[66,TY+30,0],1,14,40,win(Q.soft+.1,Q.vg),'bad');
addLabel('Geometrie variabilă','blocată pe închis, de calamină',insP,1,10,26,win(W(6,'geometria')+.3,W(6,'sau')+.2),'bad');
addLabel('Comanda geometriei','furtunaș fisurat, actuator, membrană',insP,1,10,26,win(Q.cmd,Q.fat-.35),'bad');
addLabel('Roata turbinei','obosită de supraturări repetate',[72,TY+12,0],1,14,-44,win(W(7,'repetate'),Q.fix-.05),'bad');
/* how to avoid */
addLabel('Fără soft peste limita turbinei',null,wheelC,1,18,36,win(W(8,'Fără')-.1,Q.vg2),'good');
addLabel('Geometrie variabilă curată',null,insP,1,10,26,win(W(8,'geometria'),W(8,'și')),'good');
addLabel('Comanda ei verificată','la primul mod de avarie',insP,1,10,26,win(W(8,'și')+.2,Q.out-.05),'good');
addLabel('Turație în limite',null,wheelC,1,20,36,win(Q.out+.3,END+3),'air');
Object.assign(SHOTS,{compS:{c:[-62,TY],w:200,h:130,az:-4,el:4},ind8:{c:[-90,TY+4],w:96,h:104,az:-8,el:4},peelS:{c:[-50,TY+84],w:170,h:230,az:-4,el:3},vgt:{c:[66,TY+100],w:150,h:196,az:6,el:3},
  turbH:{c:[72,TY-4],w:200,h:160,az:14,el:5},turbK7:{c:[70,TY+8],w:124,h:150,az:14,el:5}});
const CAM=[
  [0,'compS'],[Q.hit0-.6,'compS'],[Q.hit0-.1,'ind8'],[W(0,'supraturarea')+.6,'ind8'],[W(1,'toate'),'shaft2'],[HOOK_END-.001,'shaft2'],
  [HOOK_END,'compS'],[Te(2),'compS'],[Ts(3)+.5,'ind8'],[Q.peel-.2,'ind8'],[Q.peel+.6,'peelS'],[Q.sec-.4,'peelS'],[Q.sec+.4,'shaft2'],[Q.src-.001,'shaft2'],
  [Q.src,'turbH'],[Q.vg,'turbH'],[Q.vg+.8,'vgt'],[Q.fat-.4,'vgt'],[Q.fat+.4,'turbK7'],[Q.fix-.001,'turbK7'],
  [Q.fix,'compS'],[Q.vg2-.1,'compS'],[Q.vg2+.7,'vgt'],[Q.out-.001,'vgt'],
  [Q.out,'chra'],[Te(10),'shaft'],[END+3,'wide']
];
