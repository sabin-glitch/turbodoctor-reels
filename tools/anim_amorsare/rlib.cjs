const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const SP=__dirname;const F=SP+'/fonts';
function css(){let s='';for(const [fam,dir,ws] of [['Barlow','fontsource-barlow-5.3.0',[500,600,700]],['Barlow Condensed','fontsource-barlow-condensed-5.3.0',[500,600,700]]])for(const w of ws)for(const sub of ['latin','latin-ext']){const pre=fam==='Barlow'?'barlow':'barlow-condensed';s+=`@font-face{font-family:"${fam}";font-weight:${w};src:url(https://fonts.gstatic.com/x/${dir}/${pre}-${sub}-${w}-normal.woff2) format("woff2");unicode-range:${sub==='latin'?'U+0000-00FF,U+2000-206F,U+2190-21FF,U+2212,U+2713,U+25C9,U+25CB':'U+0100-02AF,U+0218-021B'};}\n`;}return s}
module.exports=async function(opts,cb){
  const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:opts.dpr||2});
  p.setDefaultTimeout(600000);
  await p.route('https://fonts.googleapis.com/**',r=>r.fulfill({contentType:'text/css',body:css()}));
  await p.route('https://fonts.gstatic.com/x/**',r=>{const u=new URL(r.request().url());const parts=u.pathname.split('/');r.fulfill({contentType:'font/woff2',body:fs.readFileSync(path.join(F,parts[2],'package/files',parts[3]))})});
  await p.route('https://cdnjs.cloudflare.com/**',r=>r.fulfill({contentType:'application/javascript',body:fs.readFileSync(SP+'/three/package/build/three.min.js')}));
  p.on('pageerror',e=>console.log('PAGEERR',e.message));p.on('console',m=>{const t=m.text();if((m.type()==='error'||m.type()==='warning'||m.type()==='log')&&!t.includes('parser-blocking'))console.log('CONSOLE',t.slice(0,600))});
  const html=fs.readFileSync(SP+'/'+(opts.file||'out/amorsare.html'),'utf8');
  if(opts.init)await p.addInitScript(opts.init);
  await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load'});
  await p.evaluate(()=>document.body.classList.add('reel'));
  await p.waitForFunction(()=>window.__ready,null,{timeout:400000});
  await p.evaluate(()=>document.fonts.ready);
  await cb(p);await b.close();
}
