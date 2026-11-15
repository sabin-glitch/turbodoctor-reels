// node shot.cjs t1,t2,... [dpr] [outdir] -> <outdir>/s_<t>.png (stills of the reel animation at voice time t)
const fs=require('fs');const ts=process.argv[2].split(',').map(Number),dpr=+(process.argv[3]||1),od=process.argv[4]||(__dirname+'/stills');
fs.mkdirSync(od,{recursive:true});
require('./rlib.cjs')({dpr},async p=>{for(const t of ts){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:`${od}/s_${t}.png`});}});
