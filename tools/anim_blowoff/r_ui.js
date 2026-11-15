const STEPS=[[0,TU,'','--accent','','']];
let hudMode='';const hudCache={};
function setText(id,v){if(hudCache[id]!==v){hudCache[id]=v;$(id).textContent=v;}}
const fmtInt=n=>String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g,'.');
const fmtDec=(n,d)=>n.toFixed(d).replace('.',',');
const fmtBar=v=>{const r=Math.round(v*10)/10;return (r<0?'−':'+')+fmtDec(Math.abs(r),1)+' bar';};
function setHud(mode,labels){
  if(hudMode===mode)return;hudMode=mode;
  for(let i=0;i<3;i++){const l=labels[i];$('h'+i).hidden=!l;if(l)$('l'+i).textContent=l;}
  hudBox=document.querySelector('.hud').getBoundingClientRect();
}
function cls(id,c){const e=$(id);if(e.dataset.c!==c){e.dataset.c=c;e.className=c;}}
/* slow-motion pill: the surge pulses are shown slowed down */
/* no pill in the hook: the hook titles sit right under the HUD */
const slowOn=U=>(U>=K.L_LIFT&&U<T_S)||(U>=K.W_LIFT&&U<K.W_ACC);
function updateUI(U,S){
  const sp=$('slowp'),so=S&&slowOn(U);if(sp.dataset.o!==String(so)){sp.dataset.o=String(so);sp.style.opacity=so?1:0;}
  const hud=document.querySelector('.hud');if(hud.dataset.h!==String(!S)){hud.dataset.h=String(!S);hud.style.visibility=S?'visible':'hidden';}
  if(!S){setHud('S',[null,null,null]);return;}
  setHud('A',['Turație turbo','Presiune turbo',null]);
  setText('v0',fmtInt(Math.round(S.rpm/1000)*1000)+' rpm');
  setText('v1',fmtBar(S.p));
  cls('v1',S.p>2.05?'warn':'');cls('v0',S.rpm>178000||(S.surge>0.5&&S.rev>0.25)?'warn':'');
}
