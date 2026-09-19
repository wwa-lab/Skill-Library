/* Pure model QA. Geometry/text estimates are advisory; DOM/Office checks remain separate. */
(function(root){
 'use strict';
 function inspect(deck,{requireNotes=true}={}){
  const issues=[],add=(severity,code,slide,element,message)=>issues.push({severity,code,slideId:slide?.id||null,elementId:element?.id||null,message});
  try{root.CorporateModel.validate(deck);}catch(e){add('ERROR','invalid-model',null,null,e.message);}
  if(!deck||!Array.isArray(deck.slides))return issues;
  const titles=new Set(),ids=deck.slides.map(s=>s?.id),brand=deck.brand||{};
  const allowed=new Set([...(brand.allowedColors||[]),...['accent','foreground','background','muted'].map(k=>brand[k]),...Object.values(deck.theme?.colors||{}),...(deck.theme?.chartPalette||[])].filter(Boolean).map(s=>s.toUpperCase()));
  if(brand.logo&&!/^data:image\/(png|jpeg);base64,/.test(brand.logo))add('ERROR','unsafe-external-reference',null,null,'Logo must be embedded raster data');
  for(const s of deck.slides){
   if(!s)continue;
   const title=(typeof s.title==='string'?s.title:'').trim();
   if(!title)add('WARN','missing-title',s,null,'Missing slide title');
   else if(titles.has(title))add('WARN','duplicate-title',s,null,'Duplicate slide title');titles.add(title);
   if(requireNotes&&!s.notes?.trim())add('WARN','missing-notes',s,null,'Missing speaker notes');
   const elements=Array.isArray(s.elements)?s.elements:[];
   let chars=0;
   for(const e of elements){
    if(!e)continue;
    if(!['text','shape','image','table','chart'].includes(e.type))add('ERROR','unsupported-pptx-object',s,e,'Unsupported PowerPoint object');
    if(e.hyperlink!==undefined){try{root.CorporateModel.validateLink(e.hyperlink,ids);}catch(_){add('ERROR','invalid-hyperlink',s,e,'Invalid link protocol or target');}}
    if(e.type==='image'){
     if(!(e.altText||e.alt||'').trim())add('WARN','missing-alt-text',s,e,'Image missing alt text');
     if(!/^data:image\/(png|jpeg);base64,/.test(e.src||''))add('ERROR','unsafe-external-reference',s,e,'Image is not an embedded PNG/JPEG');
     if(e.x<60||e.y<40||e.x+e.w>1540||e.y+e.h>820)add('WARN','image-outside-safe-area',s,e,'Image outside recommended safe area (may be intentional)');
    }
    if(['image','chart','table'].includes(e.type)&&!e.source)add('INFO','missing-source',s,e,'Add an asset or data source');
    for(const key of ['color','fill','accent'])if(typeof e[key]==='string'&&!allowed.has(e[key].toUpperCase()))add('INFO','non-brand-color',s,e,'Custom colour outside brand palette: '+e[key]);
    const text=e.paragraphs?e.paragraphs.map(p=>p.runs.map(r=>r.text).join('')).join('\n'):e.text;
    if(typeof text==='string'){
     chars+=text.length;const size=e.fontSize||deck.theme?.typography[e.role||'body']?.size||32;
     const units=t=>Array.from(t).reduce((n,c)=>n+(/[\x00-\x7f]/.test(c)?.55:1),0);
     const lines=text.split('\n').reduce((n,line)=>n+Math.max(1,Math.ceil(units(line)*size/Math.max(1,e.w))),0);
     if(lines*size*1.28>e.h+2)add('WARN','text-overflow-estimate',s,e,'Estimated text overflow; verify browser and Office layout');
    }
   }
   if(chars>1100||elements.length>30)add('WARN','dense-slide',s,null,'Dense slide; consider splitting it');
  }
  for(const warning of deck.warnings||[])add('WARN','conversion-warning',null,null,warning);
  return issues;
 }
 root.CorporateQA=Object.freeze({inspect});
})(globalThis);
