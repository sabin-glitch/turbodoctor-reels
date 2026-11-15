/* ================= SERIES DIRECTOR, part 1: helpers shared by all episodes ================= */
const CU=window.CUES||{end:50,lines:[],words:[]};
const nrm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
const Ts=i=>CU.lines[i].start,Te=i=>CU.lines[i].end,END=CU.end,NL=CU.lines.length;
function W(i,word,nth){const ws=CU.words.filter(w=>w.win===i&&nrm(w.text)===nrm(word)),w=ws[(nth||1)-1];if(!w){console.warn('CUE_MISSING '+i+' '+word);return Ts(i);}return w.s;}
function track(tr,t){if(tr.length<2)return tr[0][1];let i=0;while(i<tr.length-2&&t>tr[i+1][0])i++;const a=tr[i],b=tr[i+1];return lerp(a[1],b[1],sst(a[0],b[0],t));}
/* step(T,a,b): value jumps from a to b at T (used at the dips to black) */
const cutAt=(T,a,b)=>[[T-.012,a],[T,b]];
let crownNow=-CLEAR;
const U0=16;
const labelDefs=[],svg=$('leaders'),labBox=$('labels');
function addLabel(text,sub,anchor,side,dx,dy,vis,cls){
  const el=document.createElement('div');el.className='lb'+(side<0?' l':'')+(cls?' '+cls:'');el.textContent=text;
  if(sub){const s=document.createElement('small');s.textContent=sub;el.appendChild(s);}
  labBox.appendChild(el);
  const ln=document.createElementNS('http://www.w3.org/2000/svg','line'),dot=document.createElementNS('http://www.w3.org/2000/svg','circle');
  dot.setAttribute('r','5');svg.appendChild(ln);svg.appendChild(dot);
  const L={el,ln,dot,anchor:typeof anchor==='function'?anchor:()=>anchor,side,dx,dy,vis,w:0,h:0};labelDefs.push(L);return L;
}
const win=(a,b,fi,fo)=>t=>pulse(t,a,a+(fi||.3),b-(fo||.3),b);
const feedPt=f=>()=>{const p=FEED.curve.getPointAt(f);return [p.x,p.y,p.z];};
const drainPt=f=>()=>{const p=DRAIN.curve.getPointAt(f);return [p.x,p.y,p.z];};
const SHOTS={
  hook:{c:[-6,TY+2],w:150,h:118,az:16,el:5},
  brg:{c:[-8,TY+3],w:112,h:84,az:9,el:3},
  shaft:{c:[-6,TY+4],w:210,h:150,az:20,el:6},
  shaft2:{c:[6,TY-6],w:250,h:170,az:10,el:4},
  wide:{c:[-70,70],w:430,h:300,az:16,el:7},
  turb:{c:[60,TY-20],w:230,h:260,az:28,el:9},
  turb2:{c:[62,TY+4],w:120,h:112,az:14,el:5},
  hot:{c:[24,TY+2],w:112,h:90,az:10,el:3},
  comp:{c:[-150,TY-10],w:300,h:230,az:-8,el:6},
  comp2:{c:[-74,TY+10],w:120,h:104,az:4,el:3},
  chraIn:{c:[-10,TY+28],w:130,h:120,az:8,el:3},
  chra:{c:[2,TY-8],w:130,h:128,az:8,el:3},
  drain:{c:[4,TY-62],w:120,h:190,az:8,el:4},
  pump:{c:[EX+20,-170],w:240,h:150,az:10,el:6},
  sump:{c:[EX+6,-176],w:200,h:110,az:6,el:4},
  sumpF:{c:[-108,-160],w:210,h:140,az:6,el:4},
  filt:{c:[-62,-128],w:84,h:74,az:4,el:2},
  cyl:{c:[EX,-36],w:190,h:240,az:6,el:4},
  crank:{c:[EX+34,-120],w:260,h:230,az:8,el:4},
  ic:{c:[-262,150],w:120,h:170,az:-6,el:4},
  out:{c:[112,TY+2],w:160,h:130,az:22,el:6},
  feedTop:{c:[-14,TY+40],w:120,h:110,az:14,el:4},
  feedAll:{c:[-46,96],w:230,h:400,az:12,el:5},
  mid:{c:[-80,-10],w:400,h:300,az:12,el:6},
  cause:{c:[-60,5],w:380,h:375,az:10,el:5}
};
const SERIES_TOTAL=13;
