import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const read=n=>JSON.parse(readFileSync(new URL('../assets/'+n,import.meta.url),'utf8'));
const config={contracts:read('contracts.json'),brand:read('brands/hsbc/brand.json'),themes:['light','executive','dark'].map(n=>read('themes/hsbc-'+n+'.json')),layouts:read('layouts.json')};
const ctx=vm.createContext({CorporateConfig:config});
for(const name of ['theme','model'])vm.runInContext(readFileSync(new URL('../assets/'+name+'.js',import.meta.url),'utf8'),ctx);
const T=ctx.CorporateTheme,M=ctx.CorporateModel,copy=v=>JSON.parse(JSON.stringify(v));
const deck=()=>({...read('deck-template.json'),modelVersion:'1.1',brand:copy(config.brand),theme:copy(config.themes[0])});
test('v1 model remains valid and unchanged',()=>{const d=read('deck-template.json'),s=JSON.stringify(d);M.validate(d);assert.equal(JSON.stringify(d),s);});
test('three closed theme schemas and Brand v2 validate',()=>{for(const t of config.themes)T.validate(t);T.brand(config.brand);});
test('theme rejects colors, ranges, unknown data/code/CSS/URL/handlers',()=>{
 for(const patch of [t=>t.colors.text='red',t=>t.typography.body.size=999,t=>t.typography.body.weight=500,t=>t.onclick='alert(1)',t=>t.colors.background='FFFFFF',t=>t.fonts.body='url(https://evil.invalid)',t=>t.fonts.body='Arial; color:red',t=>t.chartPalette=[],t=>t.chartPalette=Array(13).fill('FFFFFF'),t=>t.script='alert(1)',t=>t.schemaVersion=2]){const t=copy(config.themes[0]);patch(t);assert.throws(()=>T.validate(t));}
});
test('theme switches preserve IDs, notes, content and all geometry including overrides',()=>{
 const d=deck();d.slides[0].elements[0].layoutOverride=true;const next=T.change(d,config.themes[2]);M.validate(next);
 for(let i=0;i<d.slides.length;i++){assert.equal(next.slides[i].id,d.slides[i].id);assert.equal(next.slides[i].notes,d.slides[i].notes);d.slides[i].elements.forEach((e,j)=>{for(const k of ['id','text','x','y','w','h','layoutOverride'])assert.deepEqual(next.slides[i].elements[j][k],e[k]);});}
 assert.equal(next.theme.id,'hsbc-dark');assert.equal(d.theme.id,'hsbc-light');
});
test('semantic roles resolve shared visual tokens, explicit overrides survive',()=>{
 const b=T.resolve(deck());assert.equal(T.element({type:'text',role:'kpi'},b).fontSize,80);assert.equal(T.element({type:'text',role:'kpi',fontSize:44},b).fontSize,44);
 const d=deck();d.slides[0].elements[0].role='execute';assert.throws(()=>M.validate(d));
});
test('reapply layout is explicit and preserves every object',()=>{
 const d=deck(),s=d.slides[0];s.elements.push({...s.elements[0],id:'extra'});const next=T.reapply(s,'two-column');assert.equal(next.elements.length,2);assert.equal(next.elements[1].x,830);assert.notEqual(s.elements[1].x,830);
});
test('hyperlink protocol whitelist and existing slide targets',()=>{
 const d=deck(),e=d.slides[0].elements[0];
 for(const v of ['javascript:alert(1)','data:text/html,x','file:///x','http://example.com','#missing','https://bad\n.invalid']){e.hyperlink=v;assert.throws(()=>M.validate(d));}
 for(const v of ['https://example.com','mailto:user@example.com','#content']){e.hyperlink=v;M.validate(d);}
});
