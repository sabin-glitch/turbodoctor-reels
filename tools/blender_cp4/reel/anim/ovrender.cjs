// node ovrender.cjs <ovl|add> <director.json> <outdir> <k> <n>  -> trecerile paginii three.js pentru cadrele i cu i%n==k din regie
//   ovl = bule + pilitura + HUD (etichete, panou, degrade-uri) pe fond transparent, PNG cu alfa
//   add = scantei + stralucirea de la contact pe negru (se aduna peste randarea Blender)
// Camera si starea pompei vin din regie (window.__OV), deci se suprapun exact peste randarea Blender. Sare peste cadrele existente.
const fs=require('fs');const [pass,dj,out,k,n]=process.argv.slice(2);const D=JSON.parse(fs.readFileSync(dj)).frames;const K=+k,N=+n;
fs.mkdirSync(out,{recursive:true});const PP=[1778,468,215];
require('./rlib.cjs')({dpr:2,file:'out/amorsare.html',init:`window.__ALPHA=1;window.__PASS='${pass}';`},async p=>{
  await p.evaluate(()=>window.__vo(true));const t0=Date.now();let d=0;
  for(let i=0;i<D.length;i++){if(i%N!==K)continue;const r=D[i];if(pass==='add'&&!r.add)continue;
    const f=`${out}/${String(r.f).padStart(5,'0')}.png`;if(fs.existsSync(f))continue;
    const s=r.shot;const shot={c:[PP[0]+s.c[0],PP[1]+s.c[1],PP[2]+s.c[2]],az:s.az,el:s.el,d:s.d,oy:s.oy+10};
    const img=await p.evaluate(([shot,st,U,hook,panel])=>{window.__OV={shot,st,panel};window.__VOHOOK=hook;window.__seek(U);return window.__grab('image/png');},[shot,r.st,r.U,r.hook,r.panel==null?1:r.panel]);
    fs.writeFileSync(f+'.tmp',Buffer.from(img.split(',')[1],'base64'));fs.renameSync(f+'.tmp',f);d++;
    if(d%50==0)console.log(pass,'f',r.f,((Date.now()-t0)/d/1000).toFixed(2),'s/f');}
  console.log('DONE',pass,K,d);});
