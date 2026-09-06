/** Optional developer verification only. End users never need Node or Playwright.
 * node tests/test_export_browser.mjs /absolute/path/to/playwright/index.mjs [output-dir]
 */
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
const base = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const packagePath = process.argv[2];
if (!packagePath) throw new Error('Pass an existing Playwright module path; no dependency is installed automatically.');
const { chromium } = await import(pathToFileURL(resolve(packagePath)).href);
const browser = await chromium.launch({ headless: true, ...(process.env.CORPORATE_TEST_BROWSER ? { executablePath: process.env.CORPORATE_TEST_BROWSER } : {}) });
try {
  const page = await browser.newPage();
  await page.route('**/*', route => route.abort()); // No CDN/network fallback can hide omissions.
  await page.setContent('<!doctype html><meta charset="UTF-8"><title>Exporter verification</title>');
  await page.addScriptTag({ content: await readFile(resolve(base, 'assets/vendor/pptxgenjs-4.0.1.bundle.js'), 'utf8') });
  await page.addScriptTag({ content: await readFile(resolve(base, 'assets/export.js'), 'utf8') });
  const results = await page.evaluate(async () => {
    const image = document.createElement('canvas'); image.width = 200; image.height = 100;
    const ctx = image.getContext('2d'); ctx.fillStyle = '#c8102e'; ctx.fillRect(0, 0, 100, 100); ctx.fillStyle = '#171717'; ctx.fillRect(100, 0, 100, 100);
    const src = image.toDataURL();
    const deck = { version: 1, id: 'test', title: '中文 企业演示验证', brand: { name: '验证公司', accent: 'C8102E', background: 'FFFFFF', foreground: '171717', muted: '666666', fontFace: 'Microsoft YaHei', titleFontFace: 'Microsoft YaHei' }, slides: [
      { id: 'text', title: '修改后的中文标题', layout: 'cover', notes: '讲稿一：已修改；完整保存。', elements: [{ id: 'text-1', type: 'text', x: 100, y: 280, w: 1000, h: 200, text: '修改后的正文\n中文与 English', fontSize: 42 }] },
      { id: 'image', title: '独立图片', layout: 'content', notes: '讲稿二：裁切图片。', elements: [{ id: 'image-1', type: 'image', x: 100, y: 280, w: 300, h: 300, src, fit: 'cover', positionX: 1, positionY: 0.5 }] },
      { id: 'shape', title: '流程图', layout: 'content', notes: '讲稿三：原生形状。', elements: ['rect', 'arrow', 'roundRect'].map((shape, i) => ({ id: 'shape-' + i, type: 'shape', shape, x: 100 + i * 430, y: 300, w: 300, h: 160, fill: 'C8102E', color: 'FFFFFF', text: ['输入', '', '交付'][i] })) },
      { id: 'table', title: '原生表格', layout: 'data', notes: '讲稿四：表格。', elements: [{ id: 'table-1', type: 'table', x: 100, y: 280, w: 1300, h: 360, rows: [['部门', '人数'], ['研发', '30'], ['设计', '10']] }] },
      { id: 'chart', title: '原生图表', layout: 'data', notes: '讲稿五：图表工作簿。', elements: [{ id: 'chart-1', type: 'chart', chartType: 'bar', x: 100, y: 280, w: 1300, h: 450, labels: ['一月', '二月'], series: [{ name: '产出', values: [20, 35] }] }] },
      { id: 'notes', title: '讲稿与主题', layout: 'content', notes: '讲稿六：第一行\n第二行\n第三行', elements: [] }
    ] };
    const before = JSON.stringify(deck);
    const pptx = await CorporateExport.build(deck);
    // Equivalent OOXML operation to adding a slide from a named branded layout.
    const extra = pptx.addSlide({ masterName: 'CORPORATE_CONTENT' });
    extra.addText('新增页面继承主题', { placeholder: 'title' }); extra.addNotes('新增页讲稿');
    const bytes = await pptx.write({ outputType: 'uint8array' });
    const zip = await JSZip.loadAsync(bytes);
    const xml = {};
    for (const name of Object.keys(zip.files).filter(n => /\.xml$/.test(n))) xml[name] = await zip.file(name).async('string');
    const template = await CorporateExport.toBlob(deck, { template: true });
    const potx = await JSZip.loadAsync(await template.arrayBuffer());
    const crop = await CorporateExport.imageOptions(deck.slides[1].elements[0]);
    const cropped = new Image(); cropped.src = crop.data; await cropped.decode();
    const sample = document.createElement('canvas'); sample.width = 1; sample.height = 1;
    sample.getContext('2d').drawImage(cropped, 0, 0, 1, 1);
    const pixel = [...sample.getContext('2d').getImageData(0, 0, 1, 1).data];
    const rejected = [];
    for (const el of [{ type: 'unsupported', x: 0, y: 0, w: 1, h: 1 }, { type: 'image', src: 'https://example.com/x.png', x: 0, y: 0, w: 1, h: 1 }]) {
      try { await CorporateExport.build({ ...deck, slides: [{ ...deck.slides[0], elements: [el] }] }); } catch (e) { rejected.push(e.message); }
    }
    const imported = await CorporateExport.build({ ...deck, slides: [{ id: 'imported', layout: 'imported', title: '导入页标题仍保留', notes: '', elements: [{ id: 'line', type: 'shape', shape: 'line', x: 100, y: 300, w: 600, h: 60 }] }] });
    const importedZip = await JSZip.loadAsync(await imported.write({ outputType: 'uint8array' }));
    const importedXml = await importedZip.file('ppt/slides/slide1.xml').async('string');
    const blank = await CorporateExport.build({ ...deck, slides: [{ id: 'blank', layout: 'content', title: '', notes: '', elements: [] }] });
    const blankZip = await JSZip.loadAsync(await blank.write({ outputType: 'uint8array' }));
    const blankXml = await blankZip.file('ppt/slides/slide1.xml').async('string');
    const dark = await CorporateExport.build({ ...deck, brand: { ...deck.brand, background: '171717', foreground: 'FFFFFF' }, slides: [deck.slides[3], { ...deck.slides[3], id: 'explicit-color', elements: [{ ...deck.slides[3].elements[0], color: 'F2D56B' }] }] });
    const darkZip = await JSZip.loadAsync(await dark.write({ outputType: 'uint8array' }));
    const inspectCells = xml => [...new DOMParser().parseFromString(xml, 'application/xml').getElementsByTagName('a:tc')].map(cell => ({
      text: [...cell.getElementsByTagName('a:t')].map(n => n.textContent).join(''),
      color: cell.getElementsByTagName('a:rPr')[0]?.getElementsByTagName('a:srgbClr')[0]?.getAttribute('val'),
      fill: [...(cell.getElementsByTagName('a:tcPr')[0]?.children || [])].find(n => n.localName === 'solidFill')?.getElementsByTagName('a:srgbClr')[0]?.getAttribute('val')
    }));
    const darkCells = inspectCells(await darkZip.file('ppt/slides/slide1.xml').async('string'));
    const explicitCells = inspectCells(await darkZip.file('ppt/slides/slide2.xml').async('string'));
    return { darkCells, explicitCells, importedXml, blankXml, xml, names: Object.keys(zip.files), templateTypes: await potx.file('[Content_Types].xml').async('string'), unchanged: JSON.stringify(deck) === before, pixel, rejected, base64: await zip.generateAsync({ type: 'base64' }), potxBase64: await potx.generateAsync({ type: 'base64' }) };
  });
  assert.deepEqual(results.darkCells.slice(2).map(c => [c.color, c.fill]), [['FFFFFF', '252525'], ['FFFFFF', '252525'], ['FFFFFF', '171717'], ['FFFFFF', '171717']]);
  assert.ok(results.explicitCells.slice(2).every(c => c.color === 'F2D56B'), 'explicit table text color preserved');
  assert.match(results.importedXml, /导入页标题仍保留/);
  assert.match(results.importedXml, /cy="0"/);
  assert.doesNotMatch(results.blankXml, /单击此处添加标题/);
  assert.equal(results.unchanged, true, 'export must not mutate authoritative model');
  assert.equal(results.rejected.length, 2, 'unsupported objects and external images must fail');
  assert.deepEqual(results.pixel, [23, 23, 23, 255], 'right-position image crop must use requested area');
  const slides = results.names.filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n));
  const notes = results.names.filter(n => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(n));
  assert.equal(slides.length, 7); assert.equal(notes.length, 7);
  assert.match(results.xml['ppt/slides/slide1.xml'], /修改后的中文标题/);
  assert.match(results.xml['ppt/slides/slide1.xml'], /修改后的正文/);
  assert.match(results.xml['ppt/slides/slide2.xml'], /<p:pic>/);
  assert.match(results.xml['ppt/slides/slide3.xml'], /prst="rightArrow"/);
  assert.match(results.xml['ppt/slides/slide4.xml'], /<a:tbl>/);
  assert.match(results.xml['ppt/slides/slide5.xml'], /<c:chart /);
  assert.ok(results.names.some(n => /^ppt\/embeddings\/.*\.xlsx$/.test(n)), 'native chart workbook');
  assert.match(results.xml['ppt/notesSlides/notesSlide6.xml'], /第一行/);
  assert.match(results.xml['ppt/notesSlides/notesSlide6.xml'], /第三行/);
  assert.match(results.xml['ppt/theme/theme1.xml'], /<a:accent1><a:srgbClr val="C8102E"/);
  assert.match(results.xml['ppt/theme/theme1.xml'], /<a:ea typeface="Microsoft YaHei"/);
  const layouts = Object.entries(results.xml).filter(([n]) => /^ppt\/slideLayouts\/slideLayout\d+\.xml$/.test(n));
  assert.equal(layouts.length, 5); // PptxGenJS base + four explicit layouts.
  assert.ok(layouts.some(([, xml]) => /type="title"/.test(xml) && /type="body"/.test(xml) && /C8102E/.test(xml)), 'branded native placeholders in reusable layout');
  assert.match(results.templateTypes, /presentationml\.template\.main\+xml/);
  if (process.argv[3]) {
    const out = resolve(process.argv[3]); await mkdir(out, { recursive: true });
    await writeFile(resolve(out, 'export-objects-test.pptx'), Buffer.from(results.base64, 'base64'));
    await writeFile(resolve(out, 'export-objects-test.potx'), Buffer.from(results.potxBase64, 'base64'));
  }
  console.log('PASS: offline browser export, 7 slides/notes, native text/image/shapes/table/chart + workbook, corporate theme/East Asian fonts, named layouts/placeholders, image crop, POTX, immutability and rejection checks. PowerPoint UI and Windows not verified.');
} finally { await browser.close(); }
