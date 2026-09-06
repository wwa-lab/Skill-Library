/* Corporate Web Slides — browser-only native Office Open XML export. */
(function (root) {
  'use strict';
  const SCALE = 120;
  const DEFAULT_BRAND = { name: 'Corporate', accent: 'C8102E', background: 'FFFFFF', foreground: '171717', muted: '666666', fontFace: 'Microsoft YaHei', titleFontFace: 'Microsoft YaHei' };
  const LAYOUTS = ['cover', 'content', 'data', 'imported'];
  const PPTX_MIME = 'application/vnd.openxmlformats-officedocument.presentationml.presentation';
  const POTX_MIME = 'application/vnd.openxmlformats-officedocument.presentationml.template';
  const fail = message => { throw new Error('PPTX 导出：' + message); };
  const hex = (value, fallback) => /^[0-9a-f]{6}$/i.test(value || '') ? value.toUpperCase() : fallback;
  const esc = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]));
  const box = el => ({ x: el.x / SCALE, y: el.y / SCALE, w: el.w / SCALE, h: el.h / SCALE });
  const pt = (value, fallback = 32) => (Number.isFinite(value) ? value : fallback) * 0.6;

  function validate(deck) {
    if (!deck || deck.version !== 1 || !Array.isArray(deck.slides) || !deck.slides.length) fail('需要非空的 v1 演示模型。');
    if (deck.slides.length > 200) fail('第一版每次最多导出 200 页。');
    const ids = new Set();
    deck.slides.forEach((slide, index) => {
      if (ids.has(slide.id)) fail('页面 id 重复。');
      ids.add(slide.id);
      if (!LAYOUTS.includes(slide.layout) || typeof slide.title !== 'string' || !Array.isArray(slide.elements)) fail(`第 ${index + 1} 页格式不正确。`);
      if (slide.title.length > 52) fail(`第 ${index + 1} 页标题超过 52 字，请缩短。`);
      slide.elements.forEach(el => {
        if (!['text', 'image', 'shape', 'table', 'chart'].includes(el.type)) fail(`不支持对象类型 ${el.type}，已停止以避免内容丢失。`);
        if (!['x', 'y', 'w', 'h'].every(k => Number.isFinite(el[k]) && el[k] >= 0) || el.x + el.w > 1600.1 || el.y + el.h > 900.1) fail(`对象 ${el.id} 超出画布或坐标无效。`);
        if (el.type === 'image' && !/^data:image\/(png|jpeg);base64,[a-z0-9+/=\s]+$/i.test(el.src || '')) fail('图片必须是内嵌 PNG/JPEG。');
        if (el.type === 'shape' && !['rect', 'roundRect', 'ellipse', 'arrow', 'line'].includes(el.shape)) fail(`不支持形状 ${el.shape}。`);
        if (el.type === 'table' && (!Array.isArray(el.rows) || !el.rows.length || el.rows.length > 12 || !el.rows[0].length || el.rows[0].length > 8 || !el.rows.every(r => Array.isArray(r) && r.length === el.rows[0].length && r.every(v => typeof v === 'string')))) fail('表格必须为最多 12 行、8 列的矩形字符串数组。');
        if (el.type === 'chart') validateChart(el);
      });
    });
  }

  function validateChart(el) {
    if (!['bar', 'line', 'pie'].includes(el.chartType) || !Array.isArray(el.labels) || !el.labels.length || el.labels.length > 12 || !Array.isArray(el.series) || !el.series.length || el.series.length > 4) fail('图表类型或数据范围不支持。');
    if (el.chartType === 'pie' && el.series.length !== 1) fail('饼图只能有一个系列。');
    if (!el.series.every(s => Array.isArray(s.values) && s.values.length === el.labels.length && s.values.every(v => Number.isFinite(v) && (el.chartType === 'line' || v >= 0)))) fail('图表标签、数值不匹配或含无效数值。');
  }

  function textOptions(el, brand, extra = {}) {
    return { ...box(el), fontFace: brand.fontFace, fontSize: pt(el.fontSize), color: hex(el.color, brand.foreground), bold: Boolean(el.bold), align: el.align || 'left', valign: 'top', margin: 0, breakLine: false, paraSpaceAfterPt: 0, lineSpacingMultiple: 1.28, lang: 'zh-CN', ...extra };
  }

  function imageLoad(src) {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = () => reject(new Error('图片无法解码，请换用有效的 PNG/JPEG。'));
      image.src = src;
    });
  }

  async function imageOptions(el) {
    const image = await imageLoad(el.src);
    const px = Number.isFinite(el.positionX) ? Math.max(0, Math.min(1, el.positionX)) : 0.5;
    const py = Number.isFinite(el.positionY) ? Math.max(0, Math.min(1, el.positionY)) : 0.5;
    const factor = (el.fit === 'cover' ? Math.max : Math.min)(el.w / image.naturalWidth, el.h / image.naturalHeight);
    const width = image.naturalWidth * factor;
    const height = image.naturalHeight * factor;
    if (el.fit !== 'cover') return { data: el.src, x: (el.x + (el.w - width) * px) / SCALE, y: (el.y + (el.h - height) * py) / SCALE, w: width / SCALE, h: height / SCALE, altText: el.alt || '' };
    // Bake only the requested image crop; the picture remains a separate editable object.
    const canvas = document.createElement('canvas');
    const quality = Math.min(2, 4096 / Math.max(el.w, el.h));
    canvas.width = Math.max(1, Math.round(el.w * quality));
    canvas.height = Math.max(1, Math.round(el.h * quality));
    const context = canvas.getContext('2d');
    if (!context) fail('浏览器不支持图片裁切。');
    context.drawImage(image, (image.naturalWidth - el.w / factor) * px, (image.naturalHeight - el.h / factor) * py, el.w / factor, el.h / factor, 0, 0, canvas.width, canvas.height);
    return { data: canvas.toDataURL('image/png'), ...box(el), altText: el.alt || '' };
  }

  async function defineMasters(pptx, brand) {
    const logo = brand.logo ? await imageOptions({ src: brand.logo, x: 1340, y: 28, w: 160, h: 48, fit: 'contain' }) : null;
    LAYOUTS.forEach(layout => {
      const titleFontSize = layout === 'cover' ? 82 : 58;
      const objects = layout === 'imported' ? [] : [
        { rect: { x: 0, y: 0, w: 13.333333, h: 0.1, fill: { color: brand.accent }, line: { color: brand.accent, transparency: 100 } } },
        { text: { text: brand.name, options: { x: 100 / SCALE, y: 838 / SCALE, w: 9, h: 0.22, margin: 0, fontFace: brand.fontFace, fontSize: 12, color: brand.muted } } },
        { placeholder: { options: { name: 'title', type: 'title', x: 100 / SCALE, y: 92 / SCALE, w: 1400 / SCALE, h: 125 / SCALE, fontFace: brand.titleFontFace, fontSize: pt(titleFontSize), color: brand.foreground, bold: true, margin: 0, valign: 'top' }, text: '单击此处添加标题' } },
        { placeholder: { options: { name: 'body', type: 'body', x: 100 / SCALE, y: 260 / SCALE, w: 1400 / SCALE, h: 540 / SCALE, fontFace: brand.fontFace, fontSize: pt(32), color: brand.foreground, margin: 0, valign: 'top' }, text: '' } }
      ];
      if (logo && layout !== 'imported') objects.push({ image: logo });
      pptx.defineSlideMaster({ title: 'CORPORATE_' + layout.toUpperCase(), background: { color: brand.background }, objects, ...(layout !== 'imported' ? { slideNumber: { x: 11.7, y: 836 / SCALE, w: 0.8, h: 0.3, fontFace: brand.fontFace, fontSize: 14.4, color: brand.foreground, margin: 0, align: 'right' } } : {}) });
    });
  }

  function addShape(pptx, slide, el, brand) {
    const type = el.shape === 'arrow' ? pptx.ShapeType.rightArrow : pptx.ShapeType[el.shape];
    slide.addShape(type, { ...box(el), ...(el.shape === 'line' ? { h: 0 } : {}), fill: { color: hex(el.fill, brand.accent), transparency: el.shape === 'line' ? 100 : 0 }, line: { color: hex(el.fill, brand.accent), width: el.shape === 'line' ? 2 : 0 }, radius: el.shape === 'roundRect' ? 0.12 : undefined, objectName: el.id });
    if (el.text) slide.addText(el.text, textOptions(el, brand, { align: el.align || 'center', valign: 'mid', color: hex(el.color, brand.foreground), margin: 5 }));
  }

  function addTable(slide, el, brand) {
    const rgb = brand.background.match(/../g).map(channel => parseInt(channel, 16));
    const dark = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2] < 128;
    const stripe = dark ? '252525' : 'F4F4F4';
    const rows = el.rows.map((row, index) => row.map(value => ({ text: value, options: { bold: index === 0, color: index === 0 ? 'FFFFFF' : hex(el.color, brand.foreground), fill: { color: index === 0 ? hex(el.accent, brand.accent) : (index % 2 ? stripe : brand.background) } } })));
    slide.addTable(rows, { ...box(el), colW: Array(el.rows[0].length).fill(el.w / SCALE / el.rows[0].length), rowH: el.h / SCALE / el.rows.length, autoPage: false, fontFace: brand.fontFace, fontSize: pt(el.fontSize, 28), margin: [4.8, 8.4, 4.8, 8.4], border: { type: 'solid', color: 'DDDDDD', pt: 0.5 }, valign: 'mid', align: el.align || 'left', objectName: el.id });
  }

  function addChart(pptx, slide, el, brand) {
    slide.addChart(pptx.ChartType[el.chartType], el.series.map(series => ({ name: series.name, labels: [...el.labels], values: [...series.values] })), {
      ...box(el), catAxisLabelFontFace: brand.fontFace, valAxisLabelFontFace: brand.fontFace,
      catAxisLabelFontSize: pt(el.fontSize, 24), valAxisLabelFontSize: pt(el.fontSize, 24), legendFontFace: brand.fontFace, legendFontSize: pt(el.fontSize, 24),
      chartColors: (el.colors || [brand.accent, '171717', '999999', 'E6ABB6']).map(c => hex(c, brand.accent)),
      showLegend: el.series.length > 1 || el.chartType === 'pie', legendPos: 'b', showTitle: false,
      showValue: false, showBorder: false, showMarker: el.chartType === 'line', showLine: true,
      showSerName: false, catAxisLineColor: 'AAAAAA', valAxisLineColor: 'AAAAAA',
      showPercent: el.chartType === 'pie', showCatName: el.chartType === 'pie',
      ...(el.chartType === 'bar' ? { catAxisLabelRotate: 0, barDir: 'col' } : {})
    });
  }

  async function build(deck) {
    if (!(root.PptxGenJS || root.pptxgen) || !root.JSZip) fail('离线导出库缺失，请重新生成完整 HTML。');
    if (root.CorporateModel) root.CorporateModel.validate(deck);
    validate(deck);
    const snapshot = JSON.parse(JSON.stringify(deck));
    const brand = { ...DEFAULT_BRAND, ...snapshot.brand };
    ['accent', 'background', 'foreground', 'muted'].forEach(key => { brand[key] = hex(brand[key], DEFAULT_BRAND[key]); });
    const pptx = new (root.PptxGenJS || root.pptxgen)();
    pptx.defineLayout({ name: 'CORPORATE_WIDE', width: 13.333333, height: 7.5 });
    pptx.layout = 'CORPORATE_WIDE';
    pptx.author = 'Corporate Web Slides';
    pptx.company = brand.name;
    pptx.subject = 'Native editable slides; web animations export as visible final state.';
    pptx.title = snapshot.title || '公司演示';
    pptx.lang = 'zh-CN';
    pptx.theme = { headFontFace: brand.titleFontFace, bodyFontFace: brand.fontFace };
    await defineMasters(pptx, brand);
    for (const page of snapshot.slides) {
      const slide = pptx.addSlide({ masterName: 'CORPORATE_' + page.layout.toUpperCase() });
      slide.background = { color: hex(page.background, brand.background) };
      if (page.layout !== 'imported') slide.addText(page.title, { placeholder: 'title', fontFace: brand.titleFontFace, fontSize: pt(page.titleStyle?.fontSize, page.layout === 'cover' ? 82 : 58), color: hex(page.titleStyle?.color, brand.foreground), align: page.titleStyle?.align || 'left', bold: true, margin: 0, valign: 'top', lineSpacingMultiple: 1.2, charSpacing: -0.84 });
      else if (page.title) slide.addText(page.title, textOptions({ x: 100, y: 92, w: 1400, h: 125, fontSize: 58, ...page.titleStyle }, brand, { bold: true, fontFace: brand.titleFontFace, lineSpacingMultiple: 1.2, charSpacing: -0.84 }));
      for (const el of page.elements) {
        if (el.type === 'text') slide.addText(el.text || '', textOptions(el, brand, { objectName: el.id }));
        else if (el.type === 'image') slide.addImage({ ...await imageOptions(el), objectName: el.id });
        else if (el.type === 'shape') addShape(pptx, slide, el, brand);
        else if (el.type === 'table') addTable(slide, el, brand);
        else if (el.type === 'chart') addChart(pptx, slide, el, brand);
      }
      slide.addNotes(page.notes || '');
    }
    // Wrap public write so API callers and downloads receive the same normalized theme.
    const originalWrite = pptx.write.bind(pptx);
    pptx.write = async (options = {}) => {
      const zip = await root.JSZip.loadAsync(await originalWrite({ outputType: 'uint8array', compression: true }));
      await normalizeTheme(zip, brand);
      return zip.generateAsync({ type: options.outputType || 'blob', compression: 'DEFLATE', mimeType: PPTX_MIME });
    };
    return pptx;
  }

  async function normalizeTheme(zip, brand) {
    const palette = { dk1: brand.foreground, lt1: brand.background, dk2: '444444', lt2: 'F4F4F4', accent1: brand.accent, accent2: brand.foreground, accent3: '999999', accent4: 'E8A2AF', accent5: '666666', accent6: 'DDDDDD', hlink: brand.accent, folHlink: '8D0B20' };
    const scheme = '<a:clrScheme name="Corporate">' + Object.entries(palette).map(([key, color]) => `<a:${key}><a:srgbClr val="${color}"/></a:${key}>`).join('') + '</a:clrScheme>';
    for (const name of Object.keys(zip.files).filter(n => /^ppt\/theme\/theme\d+\.xml$/.test(n))) {
      let xml = await zip.file(name).async('string');
      xml = xml.replace(/<a:clrScheme\b[^>]*>[\s\S]*?<\/a:clrScheme>/, scheme);
      xml = xml.replace(/(<a:majorFont>[\s\S]*?<a:ea) typeface="[^"]*"/, '$1 typeface="' + esc(brand.titleFontFace) + '"');
      xml = xml.replace(/(<a:minorFont>[\s\S]*?<a:ea) typeface="[^"]*"/, '$1 typeface="' + esc(brand.fontFace) + '"');
      xml = xml.replace(/(<a:font script="Hans" typeface=")[^"]*"/g, '$1' + esc(brand.fontFace) + '"');
      zip.file(name, xml);
    }
    // The base master also carries the brand background; generated named layouts add chrome.
    for (const name of Object.keys(zip.files).filter(n => /^ppt\/slideMasters\/slideMaster\d+\.xml$/.test(n))) {
      let xml = await zip.file(name).async('string');
      const bg = `<p:bg><p:bgPr><a:solidFill><a:srgbClr val="${brand.background}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>`;
      xml = /<p:bg>/.test(xml) ? xml.replace(/<p:bg>[\s\S]*?<\/p:bg>/, bg) : xml.replace(/(<p:cSld[^>]*>)/, '$1' + bg);
      zip.file(name, xml);
    }
  }

  async function toBlob(deck, options = {}) {
    const pptx = await build(deck);
    const bytes = await pptx.write({ outputType: 'uint8array', compression: true });
    if (!options.template) return new Blob([bytes], { type: PPTX_MIME });
    const zip = await root.JSZip.loadAsync(bytes);
    const name = '[Content_Types].xml';
    zip.file(name, (await zip.file(name).async('string')).replace('application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml', 'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml'));
    return zip.generateAsync({ type: 'blob', compression: 'DEFLATE', mimeType: POTX_MIME });
  }

  async function download(deck, options = {}) {
    const blob = await toBlob(deck, options);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = (deck.title || '公司演示').replace(/[<>:"/\\|?*\x00-\x1F]/g, '_').slice(0, 100) + (options.template ? '.potx' : '.pptx');
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
    return blob;
  }
  root.CorporateExport = Object.freeze({ build, toBlob, download, validate, imageOptions });
})(globalThis);
