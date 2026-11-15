/* ================= EPISODE 12: greșelile de montaj ================= */
const EP_N=12,EP_NAME='Greșelile de montaj';
const HOOK_END=Ts(2)-0.3;
const Q={snap:W(0,'greșelile')+.15,m1:Ts(3)-.28,m2:Ts(4)-.28,m3:Ts(5)-.28,m4:Ts(6)-.28,rule:Ts(7)-.28,fix:Ts(8)-.28,out:Ts(9)-.45,
  c1:W(6,'uleiul')-.12,c2:W(6,'Resturile')-.3,hitc:W(6,'ajung')+.25,f1:W(8,'ulei')-.15,f2:W(8,'conducte')-.15};
Q.e2=Math.min(Te(2),Q.m1-.1);Q.e3=Math.min(Te(3),Q.m2-.1);Q.e4=Math.min(Te(4),Q.m3-.1);Q.e5=Math.min(Te(5),Q.m4-.1);Q.e6=Math.min(Te(6),Q.rule-.1);
const DIPS=[HOOK_END,Q.m1,Q.m2,Q.m3,Q.m4,Q.rule,Q.fix,Q.out],SNAPS=[[Q.snap,HOOK_END]],FLASHES=[Q.snap,Q.hitc];
window.HITC=[Q.hitc];
const TR={
  sil:[[0,0],[1.2,0],[3.2,1],...cutAt(HOOK_END,1,0),[W(4,'silicon')-.2,0],[W(4,'silicon')+.7,1],...cutAt(Q.m3,1,0),[END+3,0]],
  starve:[[0,0],[2.4,0],[4.2,1],...cutAt(HOOK_END,1,0),[W(2,'cedează')-.1,0],[W(2,'zile')+.3,.8],...cutAt(Q.m1,.8,0),[W(4,'Trecerea')-.1,0],[W(4,'îngustează')+.3,.7],...cutAt(Q.m3,.7,0),
    [W(5,'calamină')-.1,0],[Q.e5,.85],...cutAt(Q.m4,.85,0),[END+3,0]],
  heat:[[0,0],[3,0],[Q.snap,1],...cutAt(HOOK_END,.8,0),[W(2,'cedează'),0],[Q.e2,.7],...cutAt(Q.m1,.7,0),[W(3,'turat'),0],[Q.e3,.8],...cutAt(Q.m2,.8,0),[W(4,'îngustează'),0],[Q.e4,.5],...cutAt(Q.m3,.5,0),
    [W(5,'calamină'),0],[Q.e5,.6],...cutAt(Q.m4,.6,0),[END+3,0]],
  sparks:[[0,0],[3,0],[Q.snap-.05,1],[Q.snap,0],[W(2,'cedează'),0],[W(2,'zile'),.8],...cutAt(Q.m1,.8,0),[W(3,'turat')-.1,0],[W(3,'imediat'),.9],...cutAt(Q.m2,.9,0),[W(4,'îngustează')-.1,0],[Q.e4,.5],...cutAt(Q.m3,.5,0),
    [W(5,'calamină'),0],[Q.e5,.7],...cutAt(Q.m4,.7,0),[END+3,0]],
  wobble:[[0,0],[3,0],[Q.snap-.05,1],[Q.snap,0],[W(2,'cedează'),0],[Q.e2,.6],...cutAt(Q.m1,.6,0),[W(3,'turat'),0],[Q.e3,.5],...cutAt(Q.m2,.5,0),[W(6,'ajung'),0],[Q.e6,.6],...cutAt(Q.rule,.6,0),[END+3,0]],
  prime:[[0,-1],...cutAt(Q.m1,-1,.22),[W(3,'iar'),.5],[Q.e3,.74],...cutAt(Q.m2,.72,-1),...cutAt(Q.fix,-1,.3),[W(8,'amorsată')+.5,.99],...cutAt(Q.f1,.99,-1),[END+3,-1]],
  eng:[[0,1.4],...cutAt(HOOK_END,1.4,1),...cutAt(Q.m1,1,.3),[W(3,'iar'),.3],[W(3,'turat')+.5,1.7],...cutAt(Q.m2,1.7,1),...cutAt(Q.fix,1,.35),[Q.out,.35],[Q.out+.8,1],[END+3,1]],
  spn:[[0,1.2],[Q.snap,1.6],...cutAt(HOOK_END,1.6,1),...cutAt(Q.m1,1,.25),[W(3,'iar'),.25],[W(3,'turat')+.6,1.6],...cutAt(Q.m2,1.6,1),...cutAt(Q.fix,1,.3),[Q.out,.3],[Q.out+.8,1],[END+3,1]],
  clog:[[0,0],[Q.m3-.02,0],[Q.m3,.15],[W(5,'vechi'),.6],[W(5,'calamină')+.3,1],...cutAt(Q.m4,1,0),[END+3,0]],
  chips:[[0,0],...cutAt(Q.m4,0,1),...cutAt(Q.rule,1,0),[END+3,0]],
  pool:[[0,0],...cutAt(Q.m4,0,.5),...cutAt(Q.rule,.5,0),[END+3,0]],
  afClog:[[0,0],...cutAt(Q.m4,0,.9),...cutAt(Q.rule,.9,0),[END+3,0]],
  dirty:[[0,0],...cutAt(Q.m4,0,1),...cutAt(Q.rule,1,0),[END+3,0]],
  dirt:[[0,0],...cutAt(Q.m4,0,.8),...cutAt(Q.rule,.8,0),[END+3,0]],
  sandMetal:[[0,1],[END+3,1]],
  sand:[[0,0],...cutAt(Q.c2,0,1),...cutAt(Q.rule,1,0),[END+3,0]],
  chipC:[[0,0],...cutAt(Q.hitc,0,1),...cutAt(Q.rule,1,0),[END+3,0]],
  score:[[0,0],[W(6,'Resturile'),0],[Q.e6,.6],...cutAt(Q.rule,.6,0),[END+3,0]],
  shake:[[0,0],[Q.snap-.03,0],[Q.snap+.05,1],[Q.snap+.7,0],[Q.hitc-.03,0],[Q.hitc+.05,.7],[Q.hitc+.6,0],[END+3,0]]
};
const brgL=[-34,TY+6.2,0],brgR=[28,TY+8.8,0],inP=[-3,TY+46,0],midP=[-6,TY+20,0],wheelC=[-98,TY+19,0],afP=[-211,TY+28,0],frac=()=>[FRAC_A+2,TY-6,2];
const frontP=()=>{const f=clamp(FX.prime*(FEED.path.len+190)/FEED.path.len,0.02,0.98);const p=FEED.curve.getPointAt(f);return [p.x,p.y,p.z];};
/* hook */
addLabel('Turbină nouă',null,[0,TY+34,0],1,22,30,win(.3,1.9),'good');
addLabel('Silicon pe flanșa de ulei',null,inP,1,18,24,win(2.1,W(0,'cauza')+.4),'bad');
addLabel('Lagăre fără ulei',null,brgL,-1,26,26,win(W(0,'cauza')+.6,Q.snap+.1),'bad');
addLabel('Ax rupt','din montaj, nu din fabricație',frac,1,22,-22,win(Q.snap+.25,HOOK_END-.05),'bad');
/* new turbos fail in the first days */
addLabel('Turbină nouă',null,[0,TY+34,0],1,22,30,win(HOOK_END+.3,W(2,'cedează')),'good');
addLabel('Cedează în primele zile',null,brgR,1,24,22,win(W(2,'cedează')+.1,W(2,'Nu')),'bad');
addLabel('Nu din fabricație',null,midP,1,16,40,win(W(2,'Nu')+.1,W(2,'ci')));
addLabel('Ci din montaj',null,midP,1,16,40,win(W(2,'ci')+.05,Q.m1-.05),'bad');
/* 1: not primed */
addLabel('Greșeala 1','pornită fără amorsare cu ulei',[OIL_A,TY+40,0],1,22,10,win(W(3,'turbina'),W(3,'iar')),'bad');
addLabel('Uleiul încă pe drum',null,frontP,-1,24,0,win(W(3,'fără')+.3,W(3,'iar')+.2),'oil');
addLabel('Motor turat imediat','lagăre încă uscate',brgL,-1,26,26,win(W(3,'turat')-.2,Q.m2-.05),'bad');
/* 2: silicone / gasket */
addLabel('Greșeala 2','silicon pe flanșele de ulei',inP,1,18,24,win(W(4,'silicon')-.2,W(4,'sau')),'bad');
addLabel('Sau o garnitură pusă invers',null,inP,1,18,24,win(W(4,'sau')+.05,W(4,'Trecerea')),'bad');
addLabel('Trecerea uleiului se îngustează',null,[-3,TY+36,0],1,18,24,win(W(4,'Trecerea')+.1,Q.m3-.05),'bad');
/* 3: old oil pipes */
addLabel('Greșeala 3','conducte vechi de ulei, refolosite',feedPt(0.86),-1,22,8,win(W(5,'conductele')-.2,W(5,'cu')),'bad');
addLabel('Calamină în conductă','uleiul nu mai trece',feedPt(0.86),-1,22,8,win(W(5,'cu')+.05,Q.m4-.05),'bad');
/* 4: leftovers of the old turbo */
addLabel('Greșeala 4','intercooler necurățat',[-266,112,0],1,16,40,win(W(6,'intercoolerul')-.3,W(6,'filtrul')-.1),'bad');
addLabel('Filtru de aer vechi',null,afP,1,14,40,win(W(6,'filtrul')+.3,Q.c1,.3,.12),'bad');
addLabel('Ulei neschimbat','după turbina distrusă',[EX-20,-192,0],1,30,-34,win(Q.c1+.05,Q.c2,.15,.12),'bad');
addLabel('Resturile turbinei vechi','ajung în cea nouă',wheelC,1,18,36,win(Q.c2+.05,Q.rule-.05,.15,.3),'bad');
/* the rule */
addLabel('Regula tuturor producătorilor',null,midP,1,16,40,win(Q.rule+.3,W(7,'schimbi')-.1));
addLabel('Întâi găsești și repari cauza','abia apoi schimbi turbina',midP,1,16,40,win(W(7,'schimbi'),Q.fix-.05),'good');
/* how to avoid */
addLabel('Turbină amorsată','ulei în lagăre înainte de pornire',[OIL_A,TY+40,0],1,22,10,win(W(8,'Turbină')-.1,Q.f1,.3,.12),'good');
addLabel('Ulei și filtre noi',null,[EX-20,-192,0],1,30,-34,win(Q.f1+.05,Q.f2,.15,.12),'good');
addLabel('Conducte de ulei','noi sau curățate',feedPt(0.86),-1,22,8,win(Q.f2+.05,W(8,'garnituri')-.1,.15,.3),'good');
addLabel('Garnituri corecte','și fără silicon',inP,1,18,24,win(W(8,'garnituri'),Q.out-.05),'good');
addLabel('Ulei din prima secundă',null,brgR,1,24,22,win(Q.out+.3,END+3),'oil');
Object.assign(SHOTS,{af:{c:[-196,TY+8],w:150,h:124,az:-4,el:3},compS:{c:[-62,TY],w:200,h:130,az:-4,el:4},feedUp:{c:[-34,128],w:210,h:250,az:10,el:4}});
const CAM=[
  [0,'feedTop'],[W(0,'Astăzi'),'feedTop'],[W(0,'cauza')+.5,'hook'],[Q.snap+1.2,'hook'],[HOOK_END-.001,'shaft'],
  [HOOK_END,'shaft'],[W(2,'cedează'),'shaft'],[W(2,'zile')+.4,'hook'],[Q.m1-.001,'hook'],
  [Q.m1,'feedUp'],[W(3,'amorsată'),'feedUp'],[W(3,'iar'),'chraIn'],[W(3,'turat')+.3,'brg'],[Q.m2-.001,'brg'],
  [Q.m2,'feedTop'],[W(4,'Trecerea')-.2,'feedTop'],[W(4,'îngustează'),'chraIn'],[Q.m3-.001,'chraIn'],
  [Q.m3,'feedTop'],[W(5,'cu'),'feedTop'],[Q.e5,'chraIn'],[Q.m4-.001,'chraIn'],
  [Q.m4,'ic'],[W(6,'filtrul')-.2,'ic'],[W(6,'filtrul')+.5,'af'],[Q.c1-.001,'af'],[Q.c1,'sump'],[Q.c2-.001,'sump'],[Q.c2,'compS'],[Q.rule-.001,'compS'],
  [Q.rule,'wide'],[W(7,'schimbi')-.2,'wide'],[W(7,'după')+.5,'shaft'],[Q.fix-.001,'shaft'],
  [Q.fix,'chraIn'],[Q.f1-.001,'chraIn'],[Q.f1,'sump'],[Q.f2-.001,'sump'],[Q.f2,'feedTop'],[Q.out-.001,'feedTop'],
  [Q.out,'brg'],[Te(10),'shaft'],[END+3,'wide']
];
