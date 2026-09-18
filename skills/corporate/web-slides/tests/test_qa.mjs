import test from 'node:test';import assert from 'node:assert/strict';import vm from 'node:vm';import {readFileSync} from 'node:fs';
const ctx=vm.createContext({});for(const n of ['model','qa'])vm.runInContext(readFileSync(new URL('../assets/'+n+'.js',import.meta.url),'utf8'),ctx);
const example=()=>JSON.parse(readFileSync(new URL('../assets/deck-template.json',import.meta.url),'utf8'));
test('QA is pure, configurable and catches missing titles, notes, sources and overflow estimates',()=>{
 const d=example();d.slides[0].title='';d.slides[0].notes='';d.slides[1].title=d.slides[2].title;d.slides[0].elements[0].text='密'.repeat(1400);d.slides[0].elements[0].h=20;
 const before=JSON.stringify(d),issues=ctx.CorporateQA.inspect(d),codes=new Set(issues.map(i=>i.code));
 for(const c of ['missing-title','duplicate-title','missing-notes','missing-source','text-overflow-estimate','dense-slide'])assert.ok(codes.has(c),c);
 assert.equal(JSON.stringify(d),before);assert.ok(!ctx.CorporateQA.inspect(d,{requireNotes:false}).some(i=>i.code==='missing-notes'));
});
test('QA reports unsupported objects, invalid hyperlinks, outside images and unsafe references',()=>{
 const d=example();d.slides[0].elements=[{id:'img',type:'image',src:'https://bad.invalid/x',x:0,y:0,w:1600,h:900,color:'ABCDEF',hyperlink:'javascript:x()'},{id:'ole',type:'ole'}];
 const codes=new Set(ctx.CorporateQA.inspect(d).map(i=>i.code));for(const c of ['unsupported-pptx-object','invalid-hyperlink','image-outside-safe-area','unsafe-external-reference','missing-alt-text','non-brand-color'])assert.ok(codes.has(c),c);
});
