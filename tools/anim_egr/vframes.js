// node vframes.js a b  -> renders frames a..b-1 of the voice-synced reel into $OUT/NNNNN.jpg (U per frame from uframes.json)
const fs=require('fs');const U=JSON.parse(fs.readFileSync(__dirname+'/uframes.json'));const OUT=process.env.OUT;
const [a,b]=process.argv.slice(2).map(Number);
require('./rlib.js')({dpr:2},async p=>{const t0=Date.now();let d=0;for(let i=a;i<Math.min(b,U.length);i++){const f=`${OUT}/${String(i).padStart(5,'0')}.jpg`;if(fs.existsSync(f))continue;
 await p.evaluate(t=>window.__seek(t),U[i]);const buf=await p.screenshot({type:'jpeg',quality:92,timeout:180000});fs.writeFileSync(f+'.tmp',buf);fs.renameSync(f+'.tmp',f);d++;
 if(d%50==0)console.log('f',i,((Date.now()-t0)/d/1000).toFixed(2),'s/f');}console.log('DONE',a,b);});
