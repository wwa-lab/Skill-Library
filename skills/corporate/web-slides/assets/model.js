/* Corporate Web Slides — authoritative JSON model, no DOM dependence. */
(function (root) {
  'use strict';
  const T = root.CorporateTheme;
  const layouts = ['cover','content','data','imported','section','title-body','two-column','image-text','kpi','comparison','timeline','process','closing','freeform'];
  const roles = ['coverTitle','slideTitle','body','subtitle','caption','kpi','label'];
  const clone = value => JSON.parse(JSON.stringify(value));
  const fail = (condition, message) => { if (!condition) throw new Error(message); };
  const hex = value => typeof value === 'string' && /^[0-9a-f]{6}$/i.test(value);
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  const raster = value => typeof value === 'string' && /^data:image\/(png|jpeg);base64,[A-Za-z0-9+/=\r\n]+$/.test(value) && value.length <= 40000000;
  function style(value, label) {
    ['color', 'fill', 'accent', 'background'].forEach(key => {
      if (value[key] !== undefined) fail(hex(value[key]), `${label}: ${key} must be a six-digit hex colour`);
    });
    if (value.fontSize !== undefined) fail(finite(value.fontSize) && value.fontSize >= 12 && value.fontSize <= 160, `${label}: font size must be 12–160`);
    if (value.role !== undefined) fail(roles.includes(value.role), label+': semantic role');
    if (value.layoutOverride !== undefined) fail(typeof value.layoutOverride === 'boolean', label+': layoutOverride');
    if (value.bold !== undefined) fail(typeof value.bold === 'boolean', label+': bold');
    if (value.align !== undefined) fail(['left', 'center', 'right'].includes(value.align), `${label}: invalid alignment`);
  }
  function validateElement(el, label) {
    fail(el && typeof el === 'object', `${label}: invalid object`);
    fail(typeof el.id === 'string' && el.id.length > 0, `${label}: missing id`);
    fail(['text', 'image', 'shape', 'table', 'chart'].includes(el.type), `${label}: unsupported object ${el.type}`);
    ['x', 'y', 'w', 'h'].forEach(key => fail(finite(el[key]), `${label}: ${key} must be finite`));
    fail(el.x >= 0 && el.y >= 0 && el.w > 0 && el.h > 0 && el.x + el.w <= 1600.1 && el.y + el.h <= 900.1, `${label}: object exceeds the 1600×900 canvas`);
    style(el, label);
    if (el.type === 'text' || (el.type === 'shape' && el.text !== undefined)) fail(typeof el.text === 'string' && el.text.length <= 20000, `${label}: invalid or oversized text`);
    if (el.paragraphs!==undefined){fail(el.type==='text'&&T,'Rich text requires text type and contracts');T.rich(el.paragraphs);fail(el.text===el.paragraphs.map(p=>p.runs.map(r=>r.text).join('')).join('\n'),'Rich text fallback must match paragraphs');}
    if (el.type === 'image') {
      fail(raster(el.src), `${label}: image must be embedded PNG/JPEG, up to approximately 30 MB`);
      if (el.fit !== undefined) fail(['contain', 'cover'].includes(el.fit), `${label}: invalid image fit`);
      ['positionX', 'positionY'].forEach(key => { if (el[key] !== undefined) fail(finite(el[key]) && el[key] >= 0 && el[key] <= 1, `${label}: crop position must be 0–1`); });
    }
    if (el.type === 'shape') fail(['rect', 'roundRect', 'ellipse', 'arrow', 'line'].includes(el.shape), `${label}: unsupported shape ${el.shape}`);
    if (el.type === 'table') {
      fail(Array.isArray(el.rows) && el.rows.length > 0 && el.rows.length <= 12, `${label}: table requires 1–12 rows`);
      const count = Array.isArray(el.rows[0]) ? el.rows[0].length : 0;
      fail(count > 0 && count <= 8 && el.rows.every(row => Array.isArray(row) && row.length === count && row.every(cell => typeof cell === 'string' && cell.length <= 2000)), `${label}: table requires rectangular plain text, 1–8 columns`);
    }
    if (el.type === 'chart') {
      fail(['bar', 'line', 'pie'].includes(el.chartType), `${label}: only bar, line and pie charts are supported`);
      fail(Array.isArray(el.labels) && el.labels.length > 0 && el.labels.length <= 12 && el.labels.every(x => typeof x === 'string' && x.length <= 60), `${label}: chart requires 1–12 categories`);
      fail(Array.isArray(el.series) && el.series.length > 0 && el.series.length <= 4, `${label}: requires 1–4 series`);
      el.series.forEach(s => fail(typeof s.name === 'string' && Array.isArray(s.values) && s.values.length === el.labels.length && s.values.every(v => finite(v) && (el.chartType === 'line' || v >= 0)), `${label}: invalid series length or values`));
      if (el.chartType === 'pie') fail(el.series.length === 1 && el.series[0].values.some(v => v > 0), `${label}: pie chart requires one series with a positive total`);
      if (el.colors !== undefined) fail(Array.isArray(el.colors) && el.colors.every(hex), `${label}: invalid chart colours`);
    }
  }
  function validate(deck) {
    fail(deck && deck.version === 1, 'unsupported deck model; version: 1 required');
    fail(typeof deck.id === 'string' && deck.id.length > 0, 'deck missing id');
    fail(typeof deck.title === 'string' && deck.title.length <= 300, 'invalid deck title');
    if (deck.modelVersion !== undefined) fail(deck.modelVersion === '1.1', 'Unsupported modelVersion');
    if (deck.theme) {fail(T,'Theme module required');T.validate(deck.theme);fail(!deck.brand.id || deck.theme.brand==='universal' || deck.theme.brand===deck.brand.id,'Theme brand mismatch');}
    const brand = deck.brand;
    if (brand?.schemaVersion !== undefined) {fail(T,'Brand module required');T.brand(brand);}
    fail(brand && typeof brand === 'object', 'missing brand configuration');
    ['accent', 'background', 'foreground', 'muted'].forEach(k => fail(hex(brand[k]), `Brand ${k}: invalid colour`));
    ['name', 'fontFace', 'titleFontFace'].forEach(k => fail(typeof brand[k] === 'string' && brand[k].length <= 200, `Brand ${k}: invalid value`));
    if (brand.logo) fail(raster(brand.logo), 'Logo must be an embedded PNG/JPEG');
    fail(Array.isArray(deck.slides) && deck.slides.length > 0 && deck.slides.length <= 200, 'deck requires 1–200 slides');
    const ids = new Set();
    deck.slides.forEach((slide, i) => {
      const label = `Slide ${i + 1}`;
      fail(typeof slide.id === 'string' && slide.id && !ids.has(slide.id), `${label}: missing or duplicate slide id`); ids.add(slide.id);
      fail(typeof slide.title === 'string' && slide.title.length <= 52 && typeof slide.notes === 'string' && slide.notes.length <= 100000, `${label}: invalid title or notes`);
      fail(layouts.includes(slide.layout), `${label}: invalid layout`);
      if(slide.section!==undefined)fail(typeof slide.section==='string'&&slide.section.length<=100,'Invalid section');
      if(slide.titleBox){const b=slide.titleBox;['x','y','w','h'].forEach(k=>fail(finite(b[k]),'Title coordinates'));fail(b.x>=0&&b.y>=0&&b.w>0&&b.h>0&&b.x+b.w<=1600.1&&b.y+b.h<=900.1,'Title outside canvas');}
      style(slide, label); if (slide.titleStyle) style(slide.titleStyle, label);
      fail(Array.isArray(slide.elements) && slide.elements.length <= 100, `${label}: maximum 100 objects`);
      const elementIds = new Set();
      slide.elements.forEach(el => {
        validateElement(el, label);
        for(const p of el.paragraphs||[])for(const run of p.runs)if(run.hyperlink!==undefined)validateLink(run.hyperlink,deck.slides.map(s=>s.id));
        if(el.hyperlink!==undefined)validateLink(el.hyperlink,deck.slides.map(s=>s.id));
        if(el.altText!==undefined)fail(typeof el.altText==='string'&&el.altText.length<=2000,'Invalid alt text');
        fail(!elementIds.has(el.id) && el.id !== '__title__', `${label}: duplicate or reserved object id`); elementIds.add(el.id);
      });
    });
    if (deck.warnings !== undefined) fail(Array.isArray(deck.warnings) && deck.warnings.every(w => typeof w === 'string'), 'conversion warnings must be a string array');
    return deck;
  }
  function validateLink(value,ids=[]) {
    fail(typeof value==='string'&&value.length<=2048&&!/[\x00-\x20<>"\\]/.test(value),'Invalid hyperlink');
    if(value.startsWith('#'))fail(ids.includes(value.slice(1)),'Missing hyperlink slide');
    else fail(/^https:\/\/[^/\s?#]+(?:[/?#][^\s]*)?$|^mailto:[^\s@]+@[^\s@]+$/i.test(value),'Only https, mailto or #slide-id hyperlinks are allowed');
    return value;
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
  root.CorporateModel = {validate, validateElement, validateLink, layouts, clone, history, uid, changeSlide, changeElement, move};
})(globalThis);
