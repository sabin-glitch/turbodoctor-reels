// node amask.cjs <uframes.json> <lista.json> <outdir> <k> <n>  -> masca de acoperire (scena + HUD) pentru cadrele din lista (cele care nu sunt refacute cu Blender),
// la jumatate de rezolutie (540x960, PNG gri): 255 = acoperit, 0 = fundal liber. Din ea se pune marcajul din fundal doar unde nu sunt piese.
const fs=require('fs');const [uf,dj,out,k,n]=process.argv.slice(2);const U=JSON.parse(fs.readFileSync(uf));const K=+k,N=+n;
const want=new Set(JSON.parse(fs.readFileSync(dj)));fs.mkdirSync(out,{recursive:true});
require('./rlib.cjs')({dpr:1,file:'out/amorsare.html',init:'window.__ALPHA=1;'},async p=>{
  await p.evaluate(()=>{window.__vo(true);window.__maskSetup();});const t0=Date.now();let d=0;
  const L=[...want].sort((x,y)=>x-y);for(let i=0;i<L.length;i++){if(i%N!==K)continue;const f=L[i];const fp=`${out}/${String(f).padStart(5,'0')}.png`;if(fs.existsSync(fp))continue;
    const img=await p.evaluate(u=>{window.__OV=null;window.__VOHOOK=false;window.__seek(u);return window.__mask();},U[f]);
    fs.writeFileSync(fp+'.tmp',Buffer.from(img.split(',')[1],'base64'));fs.renameSync(fp+'.tmp',fp);d++;
    if(d%200==0)console.log('f',f,((Date.now()-t0)/d/1000).toFixed(2),'s/f');}
  console.log('DONE',K,d);});
