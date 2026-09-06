/* Corporate Web Slides — authoritative JSON model, no DOM dependence. */
(function (root) {
  'use strict';
  const clone = value => JSON.parse(JSON.stringify(value));
  const fail = (condition, message) => { if (!condition) throw new Error(message); };
  const hex = value => typeof value === 'string' && /^[0-9a-f]{6}$/i.test(value);
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  const raster = value => typeof value === 'string' && /^data:image\/(png|jpeg);base64,[A-Za-z0-9+/=\r\n]+$/.test(value) && value.length <= 40000000;
  function style(value, label) {
    ['color', 'fill', 'accent', 'background'].forEach(key => {
      if (value[key] !== undefined) fail(hex(value[key]), `${label}: ${key} 必须为六位十六进制颜色`);
    });
    if (value.fontSize !== undefined) fail(finite(value.fontSize) && value.fontSize >= 12 && value.fontSize <= 160, `${label}: 字号需为 12–160`);
    if (value.align !== undefined) fail(['left', 'center', 'right'].includes(value.align), `${label}: 对齐方式无效`);
  }
  function validateElement(el, label) {
    fail(el && typeof el === 'object', `${label}: 对象无效`);
    fail(typeof el.id === 'string' && el.id.length > 0, `${label}: 缺少 id`);
    fail(['text', 'image', 'shape', 'table', 'chart'].includes(el.type), `${label}: 不支持的对象 ${el.type}`);
    ['x', 'y', 'w', 'h'].forEach(key => fail(finite(el[key]), `${label}: ${key} 必须是有限数字`));
    fail(el.x >= 0 && el.y >= 0 && el.w > 0 && el.h > 0 && el.x + el.w <= 1600.1 && el.y + el.h <= 900.1, `${label}: 对象超出 1600×900 画布`);
    style(el, label);
    if (el.type === 'text' || (el.type === 'shape' && el.text !== undefined)) fail(typeof el.text === 'string' && el.text.length <= 20000, `${label}: 文字无效或过长`);
    if (el.type === 'image') {
      fail(raster(el.src), `${label}: 图片必须为嵌入的 PNG/JPEG，最大约 30 MB`);
      if (el.fit !== undefined) fail(['contain', 'cover'].includes(el.fit), `${label}: 图片显示方式无效`);
      ['positionX', 'positionY'].forEach(key => { if (el[key] !== undefined) fail(finite(el[key]) && el[key] >= 0 && el[key] <= 1, `${label}: 裁切位置必须在 0–1`); });
    }
    if (el.type === 'shape') fail(['rect', 'roundRect', 'ellipse', 'arrow', 'line'].includes(el.shape), `${label}: 不支持的形状 ${el.shape}`);
    if (el.type === 'table') {
      fail(Array.isArray(el.rows) && el.rows.length > 0 && el.rows.length <= 12, `${label}: 表格须为 1–12 行`);
      const count = Array.isArray(el.rows[0]) ? el.rows[0].length : 0;
      fail(count > 0 && count <= 8 && el.rows.every(row => Array.isArray(row) && row.length === count && row.every(cell => typeof cell === 'string' && cell.length <= 2000)), `${label}: 表格须为矩形、1–8 列纯文字`);
    }
    if (el.type === 'chart') {
      fail(['bar', 'line', 'pie'].includes(el.chartType), `${label}: 仅支持柱状、折线和饼图`);
      fail(Array.isArray(el.labels) && el.labels.length > 0 && el.labels.length <= 12 && el.labels.every(x => typeof x === 'string' && x.length <= 60), `${label}: 图表需要 1–12 个分类`);
      fail(Array.isArray(el.series) && el.series.length > 0 && el.series.length <= 4, `${label}: 需要 1–4 个系列`);
      el.series.forEach(s => fail(typeof s.name === 'string' && Array.isArray(s.values) && s.values.length === el.labels.length && s.values.every(v => finite(v) && (el.chartType === 'line' || v >= 0)), `${label}: 系列长度或数值无效`));
      if (el.chartType === 'pie') fail(el.series.length === 1 && el.series[0].values.some(v => v > 0), `${label}: 饼图需一个系列且总和大于零`);
      if (el.colors !== undefined) fail(Array.isArray(el.colors) && el.colors.every(hex), `${label}: 图表颜色无效`);
    }
  }
  function validate(deck) {
    fail(deck && deck.version === 1, '不支持的演示模型版本，需要 version: 1');
    fail(typeof deck.id === 'string' && deck.id.length > 0, '演示缺少 id');
    fail(typeof deck.title === 'string' && deck.title.length <= 300, '演示名称无效');
    const brand = deck.brand;
    fail(brand && typeof brand === 'object', '缺少品牌配置');
    ['accent', 'background', 'foreground', 'muted'].forEach(k => fail(hex(brand[k]), `品牌 ${k} 颜色无效`));
    ['name', 'fontFace', 'titleFontFace'].forEach(k => fail(typeof brand[k] === 'string' && brand[k].length <= 200, `品牌 ${k} 无效`));
    if (brand.logo) fail(raster(brand.logo), 'Logo 必须为嵌入的 PNG/JPEG');
    fail(Array.isArray(deck.slides) && deck.slides.length > 0 && deck.slides.length <= 200, '演示须有 1–200 页');
    const ids = new Set();
    deck.slides.forEach((slide, i) => {
      const label = `第 ${i + 1} 页`;
      fail(typeof slide.id === 'string' && slide.id && !ids.has(slide.id), `${label}: 页面 id 缺少或重复`); ids.add(slide.id);
      fail(typeof slide.title === 'string' && slide.title.length <= 52 && typeof slide.notes === 'string' && slide.notes.length <= 100000, `${label}: 标题或讲稿无效`);
      fail(['cover', 'content', 'data', 'imported'].includes(slide.layout), `${label}: 版式无效`);
      style(slide, label); if (slide.titleStyle) style(slide.titleStyle, label);
      fail(Array.isArray(slide.elements) && slide.elements.length <= 100, `${label}: 最多 100 个对象`);
      const elementIds = new Set();
      slide.elements.forEach(el => {
        validateElement(el, label);
        fail(!elementIds.has(el.id) && el.id !== '__title__', `${label}: 对象 id 重复或保留`); elementIds.add(el.id);
      });
    });
    if (deck.warnings !== undefined) fail(Array.isArray(deck.warnings) && deck.warnings.every(w => typeof w === 'string'), '转换警告必须为文字数组');
    return deck;
  }
  function history(initial) {
    let current = clone(validate(initial)), past = [], future = [];
    return {
      get: () => clone(current),
      canUndo: () => past.length > 0, canRedo: () => future.length > 0,
      commit(next) {
        validate(next);
        if (JSON.stringify(next) === JSON.stringify(current)) return false;
        past = [...past.slice(-29), current]; current = clone(next); future = []; return true;
      },
      undo() { if (past.length) { future = [current, ...future]; current = past[past.length - 1]; past = past.slice(0, -1); } return clone(current); },
      redo() { if (future.length) { past = [...past, current]; current = future[0]; future = future.slice(1); } return clone(current); }
    };
  }
  const uid = prefix => `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
  function changeSlide(deck, id, patch) { return {...deck, slides: deck.slides.map(s => s.id === id ? {...s, ...patch} : s)}; }
  function changeElement(deck, slideId, id, patch) {
    return {...deck, slides: deck.slides.map(s => s.id === slideId ? {...s, elements: s.elements.map(e => e.id === id ? {...e, ...patch} : e)} : s)};
  }
  function move(deck, from, to) {
    if (from < 0 || to < 0 || from >= deck.slides.length || to >= deck.slides.length) return deck;
    const rest = deck.slides.filter((_, i) => i !== from);
    return {...deck, slides: [...rest.slice(0, to), deck.slides[from], ...rest.slice(to)]};
  }
  root.CorporateModel = {validate, validateElement, clone, history, uid, changeSlide, changeElement, move};
})(globalThis);
