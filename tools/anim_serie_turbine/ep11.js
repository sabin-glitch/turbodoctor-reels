/* ================= EPISODE 11: scăpări și înfundări pe traseul de aer și de gaze ================= */
const EP_N=11,EP_NAME='Scăpări și înfundări';
const HOOK_END=Ts(2)-0.3;
const Q={inf:W(0,'înfundările'),af:Ts(3)-.28,hose:Ts(4)-.28,man:Ts(5)-.28,dpf:Ts(6)-.28,sig:Ts(7)-.28,fix:Ts(8)-.28,out:Ts(9)-.45,
  tA:W(7,'fumul')-.15,tB:W(7,'lipsa')-.12,tC:W(7,'uleiul')-.15};
Q.e3=Math.min(Te(3),Q.hose-.1);Q.e6=Math.min(Te(6),Q.sig-.1);
const DIPS=[HOOK_END,Q.af,Q.hose,Q.man,Q.dpf,Q.sig,Q.fix,Q.out],SNAPS=[],FLASHES=[];
const GV=[[0,.7],[W(4,'pierde')-.1,.7],[W(4,'presiune')+.4,.3],[W(4,'învârte'),.3],[W(4,'compenseze')+.4,.62],[Q.man,.62],[Q.man+.1,.7],[Q.tB-.02,.7],[Q.tB,.3],[END+3,.3]];
window.GAUGE={title:'PRESIUNEA DE SUPRAALIMENTARE',
  state:v=>v<0.5?{hot:true,sub:'aerul se pierde pe drum',txt:'PREA MICĂ'}:{hot:false,sub:'cât cere motorul',txt:'POTRIVITĂ'},
  vis:t=>Math.max(win(W(4,'pierde')-.3,Q.man-.1)(t),win(Q.tB+.02,Q.tC,.15,.15)(t)),val:t=>track(GV,t)+0.012*Math.sin(t*8)};
const TR={
  leakSide:[[0,2],[END+3,2]],
  hoseLeak:[[0,0],[.3,0],[.9,1],[Q.inf-.3,1],[Q.inf,0],[W(4,'fisurat')-.2,0],[W(4,'fisurat')+.4,1],...cutAt(Q.man,1,0),...cutAt(Q.sig,0,1),...cutAt(Q.tA,1,0),
    [W(8,'șuierat')-.3,0],[W(8,'șuierat')+.3,.7],...cutAt(Q.out,.7,0),[END+3,0]],
  afClog:[[0,0],[Q.inf-.3,0],[Q.inf+.6,1],...cutAt(HOOK_END,1,0),...cutAt(Q.af,0,.15),[W(3,'înfundat')+.5,1],...cutAt(Q.hose,1,0),...cutAt(Q.fix,0,1),[W(8,'schimbat')-.1,1],[W(8,'schimbat')+.6,0],[END+3,0]],
  airK:[[0,1],[Q.inf,1],[Q.inf+.8,.45],...cutAt(HOOK_END,.45,1),[W(3,'înfundat'),1],[W(3,'forța')+.2,.4],...cutAt(Q.hose,.4,1),[W(4,'pierde'),1],[W(4,'presiune')+.4,.6],...cutAt(Q.man,.6,1),
    [W(5,'scapă'),1],[W(5,'turbină')+.3,.55],...cutAt(Q.dpf,.55,1),...cutAt(Q.tB,1,.4),...cutAt(Q.fix,.4,.5),[W(8,'schimbat')-.1,.5],[W(8,'schimbat')+.6,1],[END+3,1]],
  leak:[[0,0],[W(3,'trage')-.2,0],[W(3,'etanșare')+.3,.9],...cutAt(Q.hose,.9,0),...cutAt(Q.tC,0,.9),...cutAt(Q.fix,.9,0),[END+3,0]],
  oilAir:[[0,0],[W(3,'ulei'),0],[Q.e3,.8],...cutAt(Q.hose,.8,0),...cutAt(Q.tC,0,.8),...cutAt(Q.fix,.8,0),[END+3,0]],
  spn:[[0,1.3],[W(1,'Vezi'),1.3],[W(1,'pe')+.5,2.3],...cutAt(HOOK_END,2.3,1),[W(4,'iar'),1],[W(4,'repede')+.5,2.2],...cutAt(Q.man,2.2,1),[W(5,'fură')-.1,1],[W(5,'turbină')+.3,.5],...cutAt(Q.dpf,.5,1),
    [W(6,'ține'),1],[Q.e6,.75],...cutAt(Q.sig,.75,1),...cutAt(Q.tB,1,.6),...cutAt(Q.fix,.6,1),[END+3,1]],
  eng:[[0,1.4],...cutAt(HOOK_END,1.4,1),[END+3,1]],
  wobble:[[0,0],[W(1,'pe'),0],[HOOK_END-.1,.5],...cutAt(HOOK_END,.5,0),[END+3,0]],
  manLeak:[[0,0],[W(5,'crăpată')-.2,0],[W(5,'crăpată')+.4,1],...cutAt(Q.dpf,1,0),[END+3,0]],
  gas:[[0,1],[W(5,'fură')-.1,1],[W(5,'scapă')+.5,.45],...cutAt(Q.dpf,.45,1),[END+3,1]],
  showDpf:[[0,0],...cutAt(Q.dpf,0,1),...cutAt(Q.sig,1,0),[END+3,0]],
  dpfClog:[[0,.1],[Q.dpf,.1],[W(6,'înfundat')+.3,1],[END+3,1]],
  hotT:[[0,0],[W(6,'ține'),0],[Q.e6,.85],...cutAt(Q.sig,.85,0),[END+3,0]],
  gasHot:[[0,0],[W(6,'înfundat'),0],[W(6,'căldura')+.3,.85],...cutAt(Q.sig,.85,0),[END+3,0]],
  sootGas:[[0,0],...cutAt(Q.tA,0,1),...cutAt(Q.tB,1,0),[END+3,0]],
  sootOut:[[0,0],...cutAt(Q.tA,0,1),...cutAt(Q.tB,1,0),[END+3,0]]
};
const hoseP=[-279,248,0],afP=[-211,TY+28,0],inletP=[-120,TY+14,0],sealC=[-66,TY+9,0],manP=[-84,44,0],brickP=[226,TY+34,0],wheelT=[72,TY+12,0],wheelC=[-98,TY+19,0],midP=[-6,TY+20,0];
/* hook */
addLabel('Scăpare','furtun fisurat',hoseP,1,16,44,win(.8,Q.inf-.3),'bad');
addLabel('Înfundare','filtru de aer plin',afP,1,14,40,win(Q.inf+.3,W(1,'Vezi')),'bad');
addLabel('Turbina le simte pe toate',null,midP,1,16,40,win(W(1,'pe')+.2,HOOK_END-.05),'bad');
/* the whole route */
addLabel('Traseul de aer',null,[-266,170,0],1,16,50,win(W(2,'aer')-.4,W(2,'Orice')),'air');
addLabel('Traseul de gaze',null,[-40,38,-10],1,12,-46,win(W(2,'gaze')-.3,W(2,'Orice')+.3),'fire');
addLabel('Se simte în turbină',null,midP,1,16,40,win(W(2,'simte')-.2,Q.af-.05),'bad');
/* clogged air filter */
addLabel('Filtru de aer înfundat',null,afP,1,14,40,win(W(3,'înfundat')-.2,W(3,'La')),'bad');
addLabel('Vid','la intrarea în compresor',inletP,1,14,40,win(W(3,'vid')-.3,W(3,'trage')+.2),'bad');
addLabel('Ulei tras pe lângă etanșare',null,sealC,1,14,40,win(W(3,'ulei')-.1,Q.hose-.05),'oil');
/* boost leak */
addLabel('Furtun fisurat','sau colier slăbit',hoseP,1,16,44,win(W(4,'fisurat')-.1,W(4,'iar')),'bad');
addLabel('Turbina se învârte mai repede','ca să compenseze',wheelC,1,18,36,win(W(4,'învârte')-.2,Q.man-.05),'bad');
/* exhaust leak before the turbine */
addLabel('Galerie crăpată','sau garnitură lipsă',manP,1,16,-46,win(W(5,'crăpată')-.1,W(5,'gazele')),'bad');
addLabel('Gazele scapă','înainte de turbină',manP,1,16,-46,win(W(5,'gazele')+.1,W(5,'ajungă')),'bad');
addLabel('Mai puțină energie la turbină',null,wheelT,1,16,40,win(W(5,'ajungă')+.2,Q.dpf-.05),'bad');
/* blocked exhaust */
addLabel('Catalizator înfundat','sau eșapament înfundat',brickP,-1,20,56,win(Q.dpf+.3,W(6,'ține')),'bad');
addLabel('Gazele și căldura','rămân în turbină',wheelT,1,16,40,win(W(6,'ține'),Q.sig-.05),'bad');
/* signs */
addLabel('Șuierat',null,hoseP,1,16,44,win(W(7,'șuieratul')-.2,Q.tA,.15,.12),'bad');
addLabel('Fum negru',null,[132,TY+12,0],-1,16,44,win(Q.tA+.05,Q.tB,.15,.12),'bad');
addLabel('Lipsă de putere',null,wheelC,1,18,36,win(Q.tB+.05,Q.tC,.15,.12),'bad');
addLabel('Ulei la compresor',null,sealC,1,14,40,win(Q.tC+.05,Q.fix-.05,.15,.3),'oil');
/* how to avoid */
addLabel('Filtru de aer schimbat la timp',null,afP,1,14,40,win(W(8,'Filtru')-.1,W(8,'furtunuri')-.1),'good');
addLabel('Furtunuri și coliere verificate',null,hoseP,1,16,44,win(W(8,'furtunuri')+.4,W(8,'iar')),'good');
addLabel('Un șuierat nou apărut','nu se ignoră',hoseP,1,16,44,win(W(8,'șuierat')-.1,Q.out-.05),'bad');
addLabel('Traseu etanș și liber',null,midP,1,16,40,win(Q.out+.3,END+3),'air');
Object.assign(SHOTS,{hoseS:{c:[-286,232],w:176,h:136,az:-6,el:3},af:{c:[-196,TY+8],w:150,h:124,az:-4,el:3},compS:{c:[-62,TY],w:200,h:130,az:-4,el:4},manL:{c:[-66,72],w:176,h:150,az:10,el:5},
  dpfS:{c:[186,TY],w:264,h:150,az:6,el:3},dpfT:{c:[138,TY],w:200,h:140,az:8,el:3},turbH:{c:[72,TY-4],w:200,h:160,az:14,el:5},outS:{c:[124,TY+2],w:176,h:130,az:14,el:5}});
const CAM=[
  [0,'hoseS'],[Q.inf-.3,'hoseS'],[Q.inf+.5,'af'],[W(1,'Vezi'),'af'],[W(1,'pe'),'shaft'],[HOOK_END-.001,'shaft'],
  [HOOK_END,'wide'],[W(2,'Orice')-.2,'wide'],[W(2,'simte'),'shaft'],[Q.af-.001,'shaft'],
  [Q.af,'af'],[W(3,'La')-.2,'af'],[W(3,'intrarea')+.5,'compS'],[W(3,'care'),'compS'],[W(3,'ulei'),'comp2'],[Q.hose-.001,'comp2'],
  [Q.hose,'hoseS'],[W(4,'iar')-.2,'hoseS'],[W(4,'turbina')+.4,'compS'],[Q.man-.001,'compS'],
  [Q.man,'manL'],[W(5,'înainte'),'manL'],[W(5,'ajungă')+.4,'turbH'],[Q.dpf-.001,'turbH'],
  [Q.dpf,'dpfS'],[W(6,'ține')-.1,'dpfS'],[W(6,'căldura'),'dpfT'],[Q.sig-.001,'dpfT'],
  [Q.sig,'hoseS'],[Q.tA-.001,'hoseS'],[Q.tA,'outS'],[Q.tB-.001,'outS'],[Q.tB,'compS'],[Q.tC-.001,'compS'],[Q.tC,'comp2'],[Q.fix-.001,'comp2'],
  [Q.fix,'af'],[W(8,'furtunuri')-.3,'af'],[W(8,'furtunuri')+.5,'hoseS'],[Q.out-.001,'hoseS'],
  [Q.out,'chra'],[Te(10),'shaft'],[END+3,'wide']
];
