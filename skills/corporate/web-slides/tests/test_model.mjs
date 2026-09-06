/** Optional Node built-in tests. End-user workflows do not need Node. */
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const context=vm.createContext({});
vm.runInContext(readFileSync(new URL('../assets/model.js',import.meta.url),'utf8'),context);
const M=context.CorporateModel;
const template=()=>JSON.parse(readFileSync(new URL('../assets/deck-template.json',import.meta.url),'utf8'));
const same=(a,b)=>assert.equal(JSON.stringify(a),JSON.stringify(b));
test('history restores the entire deck without mutation',()=>{
 const d=template(),before=JSON.stringify(d),h=M.history(d),id=d.slides[0].id;
 h.commit(M.changeSlide(d,id,{title:'修改的标题',notes:'讲稿\n第二行'}));
 assert.equal(JSON.stringify(d),before);assert.equal(h.get().slides[0].notes,'讲稿\n第二行');
 same(h.undo(),d);assert.equal(h.redo().slides[0].title,'修改的标题');
 const copy=h.get();copy.slides[0].title='外部污染';assert.notEqual(h.get().slides[0].title,copy.slides[0].title);
});
test('reorder keeps all content and a new edit invalidates redo',()=>{
 const d=template(),h=M.history(d);h.commit(M.move(d,0,2));
 same(h.get().slides.map(s=>s.id),['content','data','title']);same(h.get().slides[2],d.slides[0]);
 h.undo();h.commit(M.changeSlide(h.get(),'content',{notes:'新的分支'}));assert.equal(h.canRedo(),false);
});
test('unknown objects and unsafe remote data fail',()=>{
 for(const patch of [{type:'smartArt'},{type:'image',src:'https://example.invalid/private.jpg'},{w:1700},{fontSize:NaN}]){
  const d=template();d.slides[0].elements[0]={...d.slides[0].elements[0],...patch};assert.throws(()=>M.validate(d));
 }
});
test('table and chart constraints reject data loss',()=>{
 const d=template();d.slides[2].elements[0].rows=[['指标','值'],['不等宽']];assert.throws(()=>M.validate(d));
 const chart={id:'c',type:'chart',x:100,y:280,w:1300,h:400,chartType:'pie',labels:['A','B'],series:[{name:'例',values:[0,0]}]};
 d.slides[2].elements=[chart];assert.throws(()=>M.validate(d));chart.series[0].values=[1,2];assert.doesNotThrow(()=>M.validate(d));
 chart.series[0].values=[1];assert.throws(()=>M.validate(d));
});
test('failed validation leaves current and history intact',()=>{
 const h=M.history(template()),before=h.get(),bad=h.get();bad.slides=[];
 assert.throws(()=>h.commit(bad));same(h.get(),before);assert.equal(h.canUndo(),false);
});
test('HTML-like strings and multiline notes are plain model data',()=>{
 const d=template();d.slides[0].notes='</script><script>danger()</script>\n中文 & English';
 d.slides[0].elements[0].text='<img src=x onerror=alert(1)>';
 same(M.history(d).get(),d);
});
