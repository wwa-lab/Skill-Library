/** Optional developer acceptance. No runtime Node dependency and no automatic installs.
 * node tests/test_editor_browser.mjs /existing/playwright/index.mjs [output-directory] [--deliver]
 * CORPORATE_TEST_BROWSER may point to an existing Chrome/Edge executable.
 */
import { readFile, writeFile, mkdir, mkdtemp } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
const base=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const modulePath=process.argv[2];
if(!modulePath) throw new Error('Pass an existing Playwright module path; no dependencies are installed.');
const out=process.argv[3] && !process.argv[3].startsWith('--') ? resolve(process.argv[3]) : await mkdtemp(resolve(tmpdir(),'公司 演示 测试 '));
await mkdir(out,{recursive:true});
const {chromium}=await import(pathToFileURL(resolve(modulePath)).href);
const browser=await chromium.launch({headless:true,...(process.env.CORPORATE_TEST_BROWSER?{executablePath:process.env.CORPORATE_TEST_BROWSER}:{})});
const errors=[],network=[];
const context=await browser.newContext({offline:true,acceptDownloads:true,viewport:{width:1366,height:768}});
await context.route('**/*',route=>{
  if(/^https?:/.test(route.request().url())) {network.push(route.request().url());return route.abort();}
  return route.continue();
});
const page=await context.newPage();
page.on('pageerror',error=>errors.push(error.message));
page.on('dialog',dialog=>dialog.dismiss());
const snapshot=()=>page.evaluate(()=>CorporateApp.getDeck());
const settle=()=>page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
async function open(file) {
  await page.goto(pathToFileURL(file).href);
  await page.waitForFunction(()=>!!globalThis.CorporateApp);
  await settle();
  assert.equal(await page.locator('#message').evaluate(el=>el.open),false,'no initial model errors');
}
async function download(button,file) {
  const result=page.waitForEvent('download',{timeout:30000});
  await page.locator(button).click();
  const dl=await result;await dl.saveAs(file);
  assert.equal(await dl.failure(),null);
  return file;
}
async function change(selector,value) {
  await page.locator(selector).fill(value);
  await page.locator(selector).press('Tab');
  await settle();
}
async function chooseSlide(id) {await page.locator(`#slide-list li[data-slide-id="${id}"]`).click();await settle();}
function inspect(file,model,crops) {
  const cmd=process.env.CORPORATE_TEST_PYTHON || (process.platform==='win32'?'py':'python3');
  const args=[...(process.platform==='win32'&&!process.env.CORPORATE_TEST_PYTHON?['-3']:[]),resolve(base,'tests/inspect_pptx.py'),file,'--model',model,...(crops?['--crops',crops]:[])];
  const result=spawnSync(cmd,args,{encoding:'utf8'});
  assert.equal(result.status,0,result.stderr||result.error?.message||result.stdout);
  return JSON.parse(result.stdout);
}
const report={environment:{platform:process.platform,browser:await browser.version(),headless:true,offline:true,node:'developer test harness only',windows11:'not verified',managedBrowser:'not verified',powerPointUI:'not verified'},screenshots:[],checks:[],output:out};
try {
  await open(resolve(base,'examples/six-slides.html'));
  const initial=await snapshot();assert.equal(initial.slides.length,6);
  assert.deepEqual(initial.slides.flatMap(s=>s.elements.map(e=>e.type)).filter((v,i,a)=>a.indexOf(v)===i).sort(),['chart','image','shape','table','text']);
  assert.ok(initial.slides.every(s=>s.notes.length>0));
  // Desktop/projection canvases use exactly the same authored geometry.
  for(const [width,height] of [[1280,720],[1366,768],[1920,1080],[1024,768]]) {
    await page.setViewportSize({width,height});await settle();
    assert.deepEqual(await page.evaluate(()=>CorporateApp.overflow()),[],`overflow at ${width}x${height}`);
    const bounds=await page.locator('#stage .slide.active').boundingBox();
    assert.ok(bounds.x>=-1&&bounds.y>=-1&&bounds.x+bounds.width<=width+1&&bounds.y+bounds.height<=height+1,'slide inside viewport');
    const file=resolve(out,`展示-${width}x${height}.png`);await page.screenshot({path:file});report.screenshots.push(file);
  }
  await page.setViewportSize({width:1366,height:768});
  await page.keyboard.press('ArrowRight');assert.equal(await page.evaluate(()=>CorporateApp.getIndex()),1);
  await page.keyboard.press('End');assert.equal(await page.evaluate(()=>CorporateApp.getIndex()),5);
  await page.keyboard.press('Home');assert.equal(await page.evaluate(()=>CorporateApp.getIndex()),0);
  await page.keyboard.press('n');assert.equal(await page.locator('#notes-panel').isVisible(),true);
  await page.keyboard.press('n');assert.equal(await page.locator('#notes-panel').isVisible(),false);
  await page.locator('#reduced').check();assert.ok(await page.locator('body').evaluate(el=>el.classList.contains('reduced')));
  await page.locator('#fullscreen').click();await page.waitForFunction(()=>!!document.fullscreenElement);
  await page.evaluate(()=>document.exitFullscreen());await settle();
  report.checks.push('six-page model, notes, keyboard navigation, reduced motion, headless fullscreen, 4 viewport sizes');
  if(process.argv.includes('--deliver')) {
    const baseline=resolve(out,'baseline-model.json');await writeFile(baseline,JSON.stringify(initial,null,2));
    const pptx=resolve(base,'examples/six-slides.pptx'),potx=resolve(base,'examples/six-slides.potx');
    await download('#export',pptx);await download('#template',potx);
    report.baselinePptx=inspect(pptx,baseline);report.baselinePotx=inspect(potx,baseline);
  }
  await page.locator('#mode').click();assert.equal(await page.locator('#mode-label').innerText(),'编辑模式');
  await change('#edit-title','团队共享知识的可编辑演示');
  await chooseSlide('text');
  await change('#edit-notes','最新讲稿：网页编辑已保存。\n第二行保留中文与 English。');
  await page.locator('#element-select').selectOption('text-body');
  await change('#edit-text','最新正文：明确问题、分享证据、推动行动。\n这段修改必须保留到 HTML 与 PPTX。');
  await page.locator('#font-size').selectOption('28');
  await page.locator('#color').fill('#c8102e');await page.locator('#color').dispatchEvent('change');
  await page.locator('#align').selectOption('center');
  let model=await snapshot();let text=model.slides.find(s=>s.id==='text');
  assert.equal(text.elements.find(e=>e.id==='text-body').fontSize,28);
  assert.equal(text.elements.find(e=>e.id==='text-body').color,'c8102e');
  assert.equal(text.elements.find(e=>e.id==='text-body').align,'center');
  await chooseSlide('table');await page.locator('#element-select').selectOption('formats');
  const tableRows=(await snapshot()).slides.find(s=>s.id==='table').elements.find(e=>e.id==='formats').rows;
  tableRows[1][0]='更新分享';await page.locator('#edit-data').fill(JSON.stringify(tableRows));await page.locator('#apply-data').click();
  await chooseSlide('chart');await page.locator('#element-select').selectOption('reuse-chart');
  const chartData=(await snapshot()).slides.find(s=>s.id==='chart').elements.find(e=>e.id==='reuse-chart');
  chartData.series[0].values=chartData.series[0].values.map((value,index)=>value+index+1);
  await page.locator('#edit-data').fill(JSON.stringify({labels:chartData.labels,series:chartData.series}));await page.locator('#apply-data').click();
  await chooseSlide('image');await page.locator('#element-select').selectOption('office-image');
  const replaced=await page.evaluate(()=>{
    const canvas=document.createElement('canvas');canvas.width=800;canvas.height=200;
    const ctx=canvas.getContext('2d');ctx.fillStyle='#c8102e';ctx.fillRect(0,0,400,200);ctx.fillStyle='#171717';ctx.fillRect(400,0,400,200);return canvas.toDataURL('image/png');
  });
  await page.locator('#image-input').setInputFiles({name:'替换 图片.png',mimeType:'image/png',buffer:Buffer.from(replaced.split(',')[1],'base64')});
  await page.waitForFunction(src=>CorporateApp.getDeck().slides.find(s=>s.id==='image').elements.find(e=>e.id==='office-image').src===src,replaced);
  await page.locator('#image-fit').selectOption('cover');
  for(const [selector,value] of [['#image-x','1'],['#image-y','0']]) {await page.locator(selector).fill(value);await page.locator(selector).dispatchEvent('change');}
  model=await snapshot();const image=model.slides.find(s=>s.id==='image').elements.find(e=>e.id==='office-image');
  assert.equal(image.src,replaced);assert.equal(image.positionX,1);assert.equal(image.positionY,0);assert.equal(image.fit,'cover');
  await page.locator('#slide-list li[data-slide-id="image"]').dragTo(page.locator('#slide-list li[data-slide-id="cover"]'));
  assert.equal((await snapshot()).slides[0].id,'image','drag order changed');
  await page.locator('#move-down').click();assert.equal((await snapshot()).slides[1].id,'image');
  await page.locator('#move-up').click();assert.equal((await snapshot()).slides[0].id,'image');
  await page.locator('#duplicate').click();assert.equal((await snapshot()).slides.length,7);
  await page.locator('#delete').click();assert.equal((await snapshot()).slides.length,6);
  await page.locator('#undo').click();assert.equal((await snapshot()).slides.length,7);
  await page.locator('#redo').click();assert.equal((await snapshot()).slides.length,6);
  await page.locator('#add').click();assert.equal((await snapshot()).slides.length,7);
  await page.locator('#delete').click();assert.equal((await snapshot()).slides.length,6);
  await chooseSlide('text');await page.locator('#element-select').selectOption('text-body');
  await settle();assert.deepEqual(await page.evaluate(()=>CorporateApp.overflow()),[],'edited deck fits');
  const editingScreenshot=resolve(out,'编辑模式.png');await page.screenshot({path:editingScreenshot});report.screenshots.push(editingScreenshot);
  const expected=await snapshot();
  const saved=resolve(out,'第一次 保存 完整演示.html');await download('#save',saved);
  await open(saved);assert.deepEqual(await snapshot(),expected,'first saved HTML exact model');
  assert.equal(await page.locator('#mode-label').innerText(),'展示模式');
  // Repeat save/reopen with another real edit to guard clone/escape degradation.
  await page.locator('#mode').click();await chooseSlide('cover');
  await change('#edit-notes','第二次保存讲稿：<script>是文字，不执行。</script>');
  const latest=await snapshot();
  const savedAgain=resolve(out,'第二次 保存 中文 演示.html');await download('#save',savedAgain);
  await open(savedAgain);assert.deepEqual(await snapshot(),latest,'second saved HTML exact model');
  assert.equal(latest.slides[0].id,'image');
  assert.equal(latest.slides.find(s=>s.id==='text').elements.find(e=>e.id==='text-body').text,'最新正文：明确问题、分享证据、推动行动。\n这段修改必须保留到 HTML 与 PPTX。');
  const serialized=await readFile(savedAgain,'utf8');assert.ok(serialized.includes('\\u003cscript>'),'embedded JSON escapes markup');
  const latestPath=resolve(out,'最新 模型.json');await writeFile(latestPath,JSON.stringify(latest,null,2));
  const crops=await page.evaluate(async()=>{
    const result={};for(const slide of CorporateApp.getDeck().slides)for(const el of slide.elements)if(el.type==='image')result[slide.id+'/'+el.id]=(await CorporateExport.imageOptions(el)).data;return result;
  });
  const cropPath=resolve(out,'图片裁切.json');await writeFile(cropPath,JSON.stringify(crops));
  const editedPptx=resolve(out,'编辑后 演示.pptx');await download('#export',editedPptx);
  report.editedPptx=inspect(editedPptx,latestPath,cropPath);
  const editedPotx=resolve(out,'编辑后 模板.potx');await download('#template',editedPotx);
  report.editedPotx=inspect(editedPotx,latestPath,cropPath);
  assert.equal(network.length,0,'no network requests');assert.deepEqual(errors,[],'no uncaught browser errors');
  report.checks.push('UI title/body/notes/font/color/alignment/image/crop/table/chart edits','drag reorder and button reorder','add/duplicate/delete/undo/redo','two HTML saves and fresh reopen with exact model preservation','UI export latest content, notes, order, native text/shapes/table/chart workbook','independent picture bytes exactly match latest requested crop','POTX theme and native master/layout placeholder package checks','offline context and network denial');
  await writeFile(resolve(out,'browser-test-report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify({status:'PASS',...report},null,2));
} finally {await context.close();await browser.close();}
