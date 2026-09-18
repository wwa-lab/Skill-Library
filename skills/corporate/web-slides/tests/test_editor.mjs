/** Deterministic canvas and rich-text model checks; uses Node built-ins only. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const json=name=>JSON.parse(readFileSync(new URL('../assets/'+name,import.meta.url),'utf8'));
const config={contracts:json('contracts.json'),brand:json('brands/hsbc/brand.json'),themes:['light','executive','dark'].map(name=>json(`themes/hsbc-${name}.json`)),layouts:json('layouts.json')};
const context=vm.createContext({CorporateConfig:config});
for(const name of ['theme','model','editor'])vm.runInContext(readFileSync(new URL(`../assets/${name}.js`,import.meta.url),'utf8'),context);
const E=context.CorporateEdit,M=context.CorporateModel;
const deck=()=>{
  const html=readFileSync(new URL('../examples/six-slides.html',import.meta.url),'utf8');
  return JSON.parse(html.match(/<script type="application\/json" id="deck-data">([\s\S]*?)<\/script>/)[1]);
};
const slide=()=>({id:'canvas',title:'标题',notes:'',layout:'content',elements:[
  {id:'a',type:'text',x:96,y:100,w:100,h:80,text:'A'},
  {id:'b',type:'shape',shape:'rect',x:300,y:100,w:120,h:80,text:'B'},
  {id:'c',type:'text',x:540,y:100,w:80,h:80,text:'C'}
]});

test('move keeps the selected group inside the 16:9 canvas and snaps to shared guides',()=>{
  const source=slide(),before=JSON.stringify(source);
  const snapped=E.move(source,['a'],2,0,{snap:true});
  assert.equal(snapped.slide.elements[0].x,100);assert.deepEqual(JSON.parse(JSON.stringify(snapped.guides)),[{axis:'x',value:100},{axis:'y',value:100}]);
  const moved=E.move(source,['a','b'],2000,0);
  assert.equal(moved.slide.elements[0].x,1276);assert.equal(moved.slide.elements[1].x,1480);
  assert.ok(moved.slide.elements.every(item=>item.x+item.w<=1600));assert.equal(JSON.stringify(source),before);
});

test('resize scales a multi-selection from its bottom-right corner and remains in bounds',()=>{
  const source=slide(),resized=E.resize(source,['a','b'],80,40);
  assert.equal(resized.elements[0].w,124.691);assert.equal(resized.elements[1].x,350.37);
  const clamped=E.resize(source,['a','b'],5000,5000);assert.ok(clamped.elements.every(item=>item.x+item.w<=1600&&item.y+item.h<=900));
  assert.equal(E.resize(source,['a'],-1000,-1000).elements[0].w,8);
});

test('align and distribute create stable positions without mutating source',()=>{
  const source=slide(),aligned=E.align(source,['a','b','c'],'middle');
  assert.equal(aligned.elements[0].y,100);assert.equal(aligned.elements[1].y,100);assert.equal(aligned.elements[2].y,100);
  const spread=E.align(source,['a','b','c'],'horizontal');
  assert.equal(spread.elements[0].x,96);assert.ok(spread.elements[1].x>spread.elements[0].x);assert.ok(spread.elements[2].x>spread.elements[1].x);
  assert.throws(()=>E.align(source,['a'],'unknown'));
});

test('title geometry uses the same canvas operations as content objects',()=>{
  const source=slide(),moved=E.move(source,['__title__'],30,20).slide;
  assert.equal(moved.titleBox.x,130);assert.equal(moved.titleBox.y,112);assert.equal(moved.layoutOverride,true);
  const model=deck();model.slides[0]=moved;assert.doesNotThrow(()=>M.validate(model));
});

test('rich paragraphs retain a plain-text fallback and native-safe formatting',()=>{
  const source=slide().elements[0],paragraphs=E.fromText('第一行\n第二行');
  assert.deepEqual(JSON.parse(JSON.stringify(paragraphs)),[
    {align:'left',list:'none',indent:0,runs:[{text:'第一行'}]},
    {align:'left',list:'none',indent:0,runs:[{text:'第二行'}]}
  ]);
  paragraphs[0].list='bullet';paragraphs[0].runs[0]={text:'重点',bold:true,fontSize:36,color:'C8102E',hyperlink:'https://example.com'};
  const rich=E.rich(source,paragraphs);assert.equal(rich.text,'重点\n第二行');
  const model=deck(),target=model.slides.find(s=>s.id==='text').elements.find(e=>e.id==='text-body');
  Object.assign(target,rich);assert.doesNotThrow(()=>M.validate(model));
  target.text='不一致';assert.throws(()=>M.validate(model));
  target.text=rich.text;target.paragraphs[0].runs[0].hyperlink='javascript:alert(1)';assert.throws(()=>M.validate(model));
});

test('rich-text schema bounds nested data and rejects markup handlers',()=>{
  const malformed=[
    [{runs:[]}],
    [{list:'number',onclick:'alert(1)',runs:[{text:'x'}]}],
    [{runs:[{text:'x',style:'color:red'}]}],
    [{runs:[{text:'x'.repeat(20001)}]}]
  ];
  for(const value of malformed)assert.throws(()=>context.CorporateTheme.rich(value));
});
