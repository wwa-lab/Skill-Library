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
   if(!title)add('WARN','missing-title',s,null,'页面缺少标题');
   else if(titles.has(title))add('WARN','duplicate-title',s,null,'页面标题重复');titles.add(title);
   if(requireNotes&&!s.notes?.trim())add('WARN','missing-notes',s,null,'缺少讲稿');
   const elements=Array.isArray(s.elements)?s.elements:[];
   let chars=0;
   for(const e of elements){
    if(!e)continue;
    if(!['text','shape','image','table','chart'].includes(e.type))add('ERROR','unsupported-pptx-object',s,e,'不支持的 PowerPoint 对象');
    if(e.hyperlink!==undefined){try{root.CorporateModel.validateLink(e.hyperlink,ids);}catch(_){add('ERROR','invalid-hyperlink',s,e,'链接协议或目标无效');}}
    if(e.type==='image'){
     if(!(e.altText||e.alt||'').trim())add('WARN','missing-alt-text',s,e,'图片缺少替代文字');
     if(!/^data:image\/(png|jpeg);base64,/.test(e.src||''))add('ERROR','unsafe-external-reference',s,e,'图片不是内嵌 PNG/JPEG');
     if(e.x<60||e.y<40||e.x+e.w>1540||e.y+e.h>820)add('WARN','image-outside-safe-area',s,e,'图片超出建议安全区（可能是有意满版）');
    }
    if(['image','chart','table'].includes(e.type)&&!e.source)add('INFO','missing-source',s,e,'建议补充素材或数据来源');
    for(const key of ['color','fill','accent'])if(typeof e[key]==='string'&&!allowed.has(e[key].toUpperCase()))add('INFO','non-brand-color',s,e,'使用自定义品牌外颜色：'+e[key]);
    const text=e.paragraphs?e.paragraphs.map(p=>p.runs.map(r=>r.text).join('')).join('\n'):e.text;
    if(typeof text==='string'){
     chars+=text.length;const size=e.fontSize||deck.theme?.typography[e.role||'body']?.size||32;
     const units=t=>Array.from(t).reduce((n,c)=>n+(/[\x00-\x7f]/.test(c)?.55:1),0);
     const lines=text.split('\n').reduce((n,line)=>n+Math.max(1,Math.ceil(units(line)*size/Math.max(1,e.w))),0);
     if(lines*size*1.28>e.h+2)add('WARN','text-overflow-estimate',s,e,'文字预计溢出；需以浏览器及 Office 实际排版复核');
    }
   }
   if(chars>1100||elements.length>30)add('WARN','dense-slide',s,null,'本页内容密集，建议拆页');
  }
  for(const warning of deck.warnings||[])add('WARN','conversion-warning',null,null,warning);
  return issues;
 }
 root.CorporateQA=Object.freeze({inspect});
})(globalThis);
