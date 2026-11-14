// node vframes.cjs k n -> cadrele i cu i%n==k din uframes.json, în $OUT/NNNNN.jpg (mod vo; hook fără panoul CP)
const fs=require('fs');const U=JSON.parse(fs.readFileSync(process.env.UF));const OUT=process.env.OUT;const HK=+process.env.HOOK_F;
const [k,n]=process.argv.slice(2).map(Number);
require('./rlib.cjs')({dpr:2,file:'out/amorsare.html'},async p=>{await p.evaluate(()=>window.__vo(true));const t0=Date.now();let d=0;
 for(let i=0;i<U.length;i++){if(i%n!==k)continue;const f=`${OUT}/${String(i).padStart(5,'0')}.jpg`;if(fs.existsSync(f))continue;
  await p.evaluate(([t,h])=>{window.__VOHOOK=h;window.__seek(t);},[U[i],i<HK]);const buf=await p.screenshot({type:'jpeg',quality:92});fs.writeFileSync(f+'.tmp',buf);fs.renameSync(f+'.tmp',f);d++;
  if(d%100==0)console.log('f',i,((Date.now()-t0)/d/1000).toFixed(2),'s/f');}console.log('DONE',k);});
