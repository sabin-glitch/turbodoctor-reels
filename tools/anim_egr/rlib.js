const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const SP=__dirname;const F=SP+'/fonts';
function css(){let s='';for(const [fam,dir,ws] of [['Barlow','fontsource-barlow-5.3.0',[400,500]],['Barlow Condensed','fontsource-barlow-condensed-5.3.0',[500,600,700]]])for(const w of ws)for(const sub of ['latin','latin-ext']){const pre=fam==='Barlow'?'barlow':'barlow-condensed';s+=`@font-face{font-family:"${fam}";font-weight:${w};src:url(https://fonts.gstatic.com/x/${dir}/${pre}-${sub}-${w}-normal.woff2) format("woff2");unicode-range:${sub==='latin'?'U+0000-00FF,U+2000-206F,U+2190-21FF,U+2212':'U+0100-02AF,U+0218-021B'};}\n`;}return s}
module.exports=async function(opts,cb){
  const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:540,height:960},deviceScaleFactor:opts.dpr||2});
  await p.route('https://fonts.googleapis.com/**',r=>r.fulfill({contentType:'text/css',body:css()}));
  await p.route('https://fonts.gstatic.com/x/**',r=>{const u=new URL(r.request().url());const parts=u.pathname.split('/');r.fulfill({contentType:'font/woff2',body:fs.readFileSync(path.join(F,parts[2],'package/files',parts[3]))})});
  await p.route('https://cdnjs.cloudflare.com/**',r=>r.fulfill({contentType:'application/javascript',body:fs.readFileSync(SP+'/three/package/build/three.min.js')}));
  p.on('pageerror',e=>console.log('PAGEERR',e.message));p.on('console',m=>{if(m.type()==='error'||m.type()==='warning')console.log('CONSOLE',m.text().slice(0,300))});
  const html=fs.readFileSync(SP+'/'+(process.env.HTML||'egr-admisie.html'),'utf8');
  await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+html+'</body></html>',{waitUntil:'load'});
  await p.waitForFunction(()=>window.__ready,null,{timeout:400000});
  await p.evaluate(vo=>{window.__pause();window.__reel(true);if(vo&&window.__vo)window.__vo(true);},!!process.env.HTML);
  await p.evaluate(()=>document.fonts.ready);
  await cb(p);await b.close();
}
