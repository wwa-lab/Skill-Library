/* Declarative contracts shared by HTML and native PPTX. No code/CSS in theme data. */
(function(root){
  'use strict';
  const C=root.CorporateConfig || JSON.parse(document.getElementById('corporate-config').textContent);
  const clone=v=>JSON.parse(JSON.stringify(v));
  const fail=(ok,msg)=>{if(!ok)throw new Error(msg);};
  function check(value,schema,path='config'){
    if(schema.enum){fail(schema.enum.includes(value),path+': invalid enum');return;}
    const kind=value===null?'null':Array.isArray(value)?'array':typeof value;
    fail([].concat(schema.type).includes(kind),path+': invalid type');
    if(kind==='object'){
      for(const k of Object.keys(value))fail(Object.hasOwn(schema.properties,k),path+': unknown field '+k);
      for(const k of schema.required)fail(Object.hasOwn(value,k),path+': missing '+k);
      for(const k of Object.keys(value))check(value[k],schema.properties[k],path+'.'+k);
    }else if(kind==='array'){
      fail(value.length>=schema.minItems&&value.length<=schema.maxItems,path+': array length');value.forEach((v,i)=>check(v,schema.items,path+'['+i+']'));
    }else if(kind==='number')fail(Number.isFinite(value)&&value>=schema.minimum&&value<=schema.maximum,path+': number range');
    else if(kind==='string'){
      fail(value.length<=schema.maxLength,path+': text too long');
      if(schema.pattern)fail(new RegExp(schema.pattern,'u').test(value),path+': invalid value');
    }
    return value;
  }
  const theme=t=>check(t,C.contracts.theme,'theme');
  function brand(b){if(b.schemaVersion!==undefined)check(b,C.contracts.brand,'brand');return b;}
  C.themes.forEach(theme);C.layouts.forEach(v=>check(v,C.contracts.layout,'layout'));brand(C.brand);
  function resolve(deck){
    const b=clone(deck.brand),t=deck.theme;
    if(!t)return b;
    theme(t);brand(b);fail(!b.id||t.brand===b.id,'Theme brand does not match deck brand');
    return {...b,accent:t.colors.accent,background:t.colors.canvas,foreground:t.colors.text,muted:t.colors.textMuted,fontFace:t.fonts.body,titleFontFace:t.fonts.title,chartPalette:t.chartPalette,theme:t};
  }
  function element(el,b){
    if(!b.theme)return el;
    const t=b.theme,role=el.role||'body',ty=t.typography[role]||t.typography.body;
    return {fontSize:el.type==='table'?t.typography.label.size:el.type==='chart'?t.typography.caption.size:ty.size,color:role==='caption'?t.colors.textMuted:t.colors.text,bold:ty.weight===700,...(el.type==='shape'?{fill:t.cards.fill,color:t.cards.text}:{}),...(el.type==='chart'?{colors:t.chartPalette}:{}),...el};
  }
  function title(s,b){
    const role=s.layout==='cover'?'coverTitle':'slideTitle';
    return {fontSize:b.theme?b.theme.typography[role].size:(s.layout==='cover'?82:58),color:b.foreground,align:'left',...s.titleStyle};
  }
  function change(deck,next){
    theme(next);fail(!deck.brand.id||next.brand===deck.brand.id,'Theme brand mismatch');
    const result=clone(deck),old=resolve(deck),fresh=resolve({...deck,theme:next});
    const map=new Map(['accent','background','foreground','muted'].map(k=>[old[k].toUpperCase(),fresh[k]]));
    for(const s of result.slides){
      for(const obj of [s,s.titleStyle||{},...s.elements])for(const k of ['color','fill','accent','background'])if(typeof obj[k]==='string'&&map.has(obj[k].toUpperCase()))obj[k]=map.get(obj[k].toUpperCase());
    }
    result.modelVersion='1.1';result.theme=clone(next);return result;
  }
  function reapply(slide,layout){
    const l=C.layouts.find(v=>v.id===layout);fail(l,'Unknown layout');const s=clone(slide);s.layout=layout;s.titleBox=clone(l.title);s.layoutOverride=false;
    // Preserve every object. For a slot containing multiple objects, partition vertically.
    s.elements.forEach((e,i)=>{if(!l.slots.length)return;const slot=l.slots[i%l.slots.length],count=Math.ceil((s.elements.length-(i%l.slots.length))/l.slots.length),row=Math.floor(i/l.slots.length),gap=20,h=(slot.h-gap*(count-1))/count;fail(h>=12,'Layout too dense; split the slide');Object.assign(e,{x:slot.x,y:slot.y+row*(h+gap),w:slot.w,h,layoutOverride:false});});
    return s;
  }
  root.CorporateTheme=Object.freeze({rich:paragraphs=>check(paragraphs,C.contracts.paragraphs,'paragraphs'),check,validate:theme,brand,resolve,element,title,change,reapply,layouts:C.layouts,themes:C.themes,defaultBrand:clone(C.brand)});
})(globalThis);
