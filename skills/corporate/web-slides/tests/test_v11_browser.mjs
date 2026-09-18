/** Existing local developer Playwright + installed Chrome only. Never installs packages. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const base=resolve(dirname(fileURLToPath(import.meta.url)),'..'),out=resolve(process.argv[3]||'/tmp/cws-v11-browser');
await mkdir(out,{recursive:true});
const {chromium}=await import(pathToFileURL(resolve(process.argv[2])).href);
const browser=await chromium.launch({headless:true,...(process.env.CORPORATE_TEST_BROWSER?{executablePath:process.env.CORPORATE_TEST_BROWSER}:{})});
const context=await browser.newContext({offline:true,acceptDownloads:true,viewport:{width:1440,height:900}});
const network=[],errors=[];await context.route('**/*',route=>{if(/^https?:/.test(route.request().url())){network.push(route.request().url());return route.abort();}return route.continue();});
const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));page.on('dialog',d=>d.dismiss());
await page.addInitScript(()=>{globalThis.policyViolations=[];document.addEventListener('securitypolicyviolation',e=>policyViolations.push({directive:e.violatedDirective,uri:e.blockedURI}));});
try{
 await page.goto(pathToFileURL(resolve(base,'examples/six-slides.html')).href);await page.waitForFunction(()=>globalThis.CorporateApp);
 const result=await page.evaluate(async()=>{
  const original=CorporateApp.getDeck(),reports=[];
  for(const theme of CorporateTheme.themes){
   const input=JSON.parse(JSON.stringify(original));input.modelVersion='1.1';input.brand=CorporateTheme.defaultBrand;input.theme=theme;
   // Structured sources keep their original geometry; explicit old colors are user overrides.
   input.slides.forEach(s=>s.elements.forEach(e=>{if(e.type==='text'){delete e.color;e.role='body';}}));
   CorporateApp.commit(input);const brand=CorporateTheme.resolve(input);
   const title=document.querySelector('.slide.active .title-element');
   if(getComputedStyle(title).color!==`rgb(${brand.foreground.match(/../g).map(x=>parseInt(x,16)).join(', ')})`)throw new Error('HTML theme color mismatch');
   const pptx=await CorporateExport.build(input);
   const extra=pptx.addSlide({masterName:'HSBC_TWO_COLUMN'});extra.addText('新增页面主题',{placeholder:'title'});extra.addNotes('新增页面讲稿');
   const zip=await JSZip.loadAsync(await pptx.write({outputType:'uint8array'}));
   const themeXML=await zip.file('ppt/theme/theme1.xml').async('string');
   if(!themeXML.includes('val="DB0011"'))throw new Error('Native theme accent missing');
   const layouts=Object.keys(zip.files).filter(n=>/^ppt\/slideLayouts\/slideLayout\d+\.xml$/.test(n));
   const twocol=await Promise.all(layouts.map(n=>zip.file(n).async('string')));
   if(!twocol.some(x=>x.includes('HSBC_TWO_COLUMN')&&(x.match(/type="body"/g)||[]).length===2))throw new Error('Native two column placeholders missing');
   reports.push({theme:theme.id,layouts:layouts.length,notes:Object.keys(zip.files).filter(n=>/^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(n)).length});
  }
  const evil=JSON.parse(JSON.stringify(original));evil.slides[0].title='<img src=x onerror=alert(1)>';CorporateApp.commit(evil);
  if(document.querySelector('.title-element img')||document.querySelector('.title-element').textContent!==evil.slides[0].title)throw new Error('Unsafe title rendering');
  CorporateApp.commit(original);return reports;
 });
 assert.equal(result.length,3);assert.ok(result.every(r=>r.notes===7));
 // Disk save is verified in a fresh browser context, without the recovery cache.
 const expected=await page.evaluate(()=>CorporateApp.getDeck());const download=page.waitForEvent('download');await page.locator('#save').click();await (await download).saveAs(resolve(out,'saved.html'));
 const fresh=await browser.newContext({offline:true});const reopened=await fresh.newPage();await reopened.goto(pathToFileURL(resolve(out,'saved.html')).href);await reopened.waitForFunction(()=>globalThis.CorporateApp);assert.deepEqual(await reopened.evaluate(()=>CorporateApp.getDeck()),expected);await fresh.close();
 assert.deepEqual(await page.evaluate(()=>policyViolations),[]);assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
 await writeFile(resolve(out,'gate-a-report.json'),JSON.stringify({status:'PASS',browser:await browser.version(),platform:process.platform,themes:result,checks:['literal malicious title','closed schemas','shared HTML/PPTX themes','native layout placeholders','new-slide notes','hash CSP','fresh saved HTML reopen','offline no requests'],office:'NOT VERIFIED'},null,2));
 console.log('PASS Gate A browser: themes, native layouts, malicious title, CSP, offline fresh save/reopen');
}finally{await context.close();await browser.close();}
