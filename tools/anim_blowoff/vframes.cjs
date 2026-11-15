// node vframes.cjs k n -> cadrele i (t = i/30) cu i%n==k, în $OUT/NNNNN.jpg (1080x1920, JPEG q92); sare peste cele deja randate
const fs=require('fs');const OUT=process.env.OUT;const NF=+process.env.NF;
const [k,n]=process.argv.slice(2).map(Number);
require('./rlib.cjs')({dpr:2},async p=>{const t0=Date.now();let d=0;
 for(let i=0;i<NF;i++){if(i%n!==k)continue;const f=`${OUT}/${String(i).padStart(5,'0')}.jpg`;if(fs.existsSync(f))continue;
  await p.evaluate(t=>window.__seek(t),i/30);const buf=await p.screenshot({type:'jpeg',quality:92});fs.writeFileSync(f+'.tmp',buf);fs.renameSync(f+'.tmp',f);d++;
  if(d%100==0)console.log('f',i,((Date.now()-t0)/d/1000).toFixed(2),'s/f');}console.log('DONE',k);});
