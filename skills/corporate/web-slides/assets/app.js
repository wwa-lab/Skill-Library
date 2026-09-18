/* Browser application: explicit modes, immutable history, portable save. */
(function () {
  'use strict';
  const $=id=>document.getElementById(id), M=globalThis.CorporateModel, R=globalThis.CorporateRender, E=globalThis.CorporateEdit;
  let history, current=0, selected='__title__', selectedIds=['__title__'], editing=false, saved='', dragged=null;
  let richParagraph=0, richRun=0, gesture=null;
  let cached=null, latestProblems=[], imageBusy=false, presenting=false;
  let timerStart=performance.now(),timerElapsed=0,timerRunning=true;
  const tell=text=>{$('status').textContent=text;};
  function message(title,body) { $('message-title').textContent=title;$('message-body').textContent=body;if(!$('message').open)$('message').showModal(); }
  function safe(action) { return async (...args)=>{try{return await action(...args);}catch(error){tell(error.message);message('操作未完成',error.message);}}; }
  const deck=()=>history.get();
  const page=()=>deck().slides[current];
  const cacheKey=()=>`corporate-web-slides:${deck().id}`;
  function snapshotCache() {
    try {localStorage.setItem(cacheKey(),JSON.stringify({savedAt:new Date().toISOString(),deck:deck()}));}
    catch(_error) {tell('本次无法写入恢复缓存，请下载 HTML 保存');}
  }
  function commit(next,notice='已修改，请保存 HTML') {
    if(history.commit(next)){tell(notice);snapshotCache();}
    render();
  }
  function sizeStage() {
    const box=$('viewport').getBoundingClientRect();
    const scale=Math.min(box.width/1600,box.height/900);
    $('stage').style.transform=`translate(${(box.width-1600*scale)/2}px,${(box.height-900*scale)/2}px) scale(${scale})`;
  }
  function renderList(data) {
    $('slide-list').replaceChildren();
    let section=null;
    data.slides.forEach((s,i)=>{
      if(s.section&&s.section!==section){const head=document.createElement('li');head.className='section-heading';head.textContent=s.section;head.setAttribute('role','presentation');$('slide-list').append(head);}section=s.section;
      const item=document.createElement('li');item.textContent=`${i+1}. ${s.title||'导入页面'}`;item.tabIndex=0;item.draggable=editing;item.dataset.slideId=s.id;item.setAttribute('aria-current',String(i===current));
      item.addEventListener('click', ()=>go(i));item.addEventListener('keydown', e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go(i);}});
      item.addEventListener('dragstart', e=>{dragged=s.id;e.dataTransfer.setData('text/plain',s.id);});
      item.addEventListener('dragover', e=>{if(editing)e.preventDefault();});
      item.addEventListener('drop', safe(e=>{e.preventDefault();if(!editing)return;const d=deck(),from=d.slides.findIndex(v=>v.id===dragged),to=d.slides.findIndex(v=>v.id===s.id);if(from<0||to<0)return;const active=page().id;const next=M.move(d,from,to);current=next.slides.findIndex(v=>v.id===active);commit(next,'页面顺序已更新');dragged=null;}));
      $('slide-list').append(item);
    });
  }
  function option(value,text) {const n=document.createElement('option');n.value=value;n.textContent=text;return n;}
  function selectedObject(slide=page()) {return selected==='__title__'?{type:'text',text:slide.title,fontSize:slide.layout==='cover'?82:58,...slide.titleStyle}:slide.elements.find(e=>e.id===selected);}
  function fillRichEditor(obj) {
    const paragraphs=obj.paragraphs;
    $('rich-controls').hidden=selected==='__title__'||obj.type!=='text';
    $('rich-enable').hidden=Boolean(paragraphs);$('rich-disable').hidden=!paragraphs;$('rich-editor').hidden=!paragraphs;
    $('text-label').hidden=!['text','shape'].includes(obj.type)||Boolean(paragraphs);
    $('edit-text').value=obj.text||'';
    if(!paragraphs)return;
    richParagraph=Math.max(0,Math.min(richParagraph,paragraphs.length-1));
    $('rich-paragraph').replaceChildren(...paragraphs.map((_,i)=>option(String(i),`段落 ${i+1}`)));
    $('rich-paragraph').value=String(richParagraph);
    const paragraph=paragraphs[richParagraph];
    $('rich-align').value=paragraph.align||obj.align||'left';$('rich-list').value=paragraph.list||'none';$('rich-indent').value=String(paragraph.indent||0);
    richRun=Math.max(0,Math.min(richRun,paragraph.runs.length-1));
    $('rich-run').replaceChildren(...paragraph.runs.map((_,i)=>option(String(i),`片段 ${i+1}`)));
    $('rich-run').value=String(richRun);
    const run=paragraph.runs[richRun];
    $('rich-run-text').value=run.text;$('rich-bold').checked=Boolean(run.bold);$('rich-italic').checked=Boolean(run.italic);
    $('rich-size').value=run.fontSize??'';$('rich-color').value='#'+(run.color||obj.color||deck().brand.foreground);$('rich-link').value=run.hyperlink||'';
    $('rich-remove-paragraph').disabled=paragraphs.length<=1;$('rich-remove-run').disabled=paragraph.runs.length<=1;
  }
  function fillEditor() {
    const s=page(),data=deck();$('edit-section').value=s.section||'';$('layout-select').value=s.layout;$('edit-title').value=s.title;$('edit-notes').value=s.notes;
    $('element-select').replaceChildren(option('__title__','页面标题'));
    s.elements.forEach((e,i)=>$('element-select').append(option(e.id,`${i+1}. ${e.type} ${(e.text||e.alt||'').slice(0,22)}`)));
    const valid=new Set(['__title__',...s.elements.map(e=>e.id)]);selectedIds=selectedIds.filter(id=>valid.has(id));if(!selectedIds.length)selectedIds=['__title__'];selected=selectedIds[0];
    $('element-select').value=selected;
    const obj=selectedObject(s);$('object-fields').hidden=selectedIds.length>1;$('selection-hint').textContent=selectedIds.length>1?`已选择 ${selectedIds.length} 个对象。可一起移动、缩放、对齐或等距分布。`:'拖动对象移动；拖动角点调整大小；按住 Shift 多选，方向键以 1 / 10 单位微调。表格首行为表头；修改后请保存 HTML。';
    $('edit-hyperlink').disabled=selected==='__title__';$('edit-hyperlink').value=obj.hyperlink||'';
    $('edit-alt').disabled=selected==='__title__';$('edit-alt').value=obj.altText||obj.alt||'';
    $('edit-source').disabled=selected==='__title__';$('edit-source').value=typeof obj.source==='string'?obj.source:'';
    fillRichEditor(obj);
    $('image-fields').hidden=obj.type!=='image';$('data-fields').hidden=!['table','chart'].includes(obj.type);
    const fs=obj.fontSize||(obj.type==='table'?28:32);if(![...$('font-size').options].some(o=>+o.value===fs))$('font-size').append(option(String(fs),`当前 ${fs}`));$('font-size').value=String(fs);
    $('color').value=`#${obj.color||data.brand.foreground}`;$('align').value=obj.align||'left';
    if(obj.type==='image'){$('image-fit').value=obj.fit||'contain';$('image-x').value=obj.positionX??.5;$('image-y').value=obj.positionY??.5;$('image-input').value='';}
    if(obj.type==='table')$('edit-data').value=JSON.stringify(obj.rows,null,2);
    if(obj.type==='chart')$('edit-data').value=JSON.stringify({labels:obj.labels,series:obj.series},null,2);
    $('undo').disabled=!history.canUndo();$('redo').disabled=!history.canRedo();
    document.querySelectorAll('[data-align="horizontal"],[data-align="vertical"]').forEach(b=>b.disabled=selectedIds.length<3);
    $('delete').disabled=data.slides.length<=1;$('move-up').disabled=current===0;$('move-down').disabled=current===data.slides.length-1;
  }
  function renderOverlay(slideModel=page(),guides=[]) {
    const active=$('stage').querySelector('.slide.active');if(!active)return;
    active.querySelector('.canvas-overlay')?.remove();if(!editing)return;
    const overlay=document.createElement('div');overlay.className='canvas-overlay';
    const all=E.items(slideModel),chosen=all.filter(item=>selectedIds.includes(item.id)),bounds=E.bounds(chosen);
    for(const item of chosen){const frame=document.createElement('div');frame.className='canvas-frame';Object.assign(frame.style,{left:item.x+'px',top:item.y+'px',width:item.w+'px',height:item.h+'px'});overlay.append(frame);}
    if(bounds){
      if(chosen.length>1){const group=document.createElement('div');group.className='canvas-frame group';Object.assign(group.style,{left:bounds.x+'px',top:bounds.y+'px',width:bounds.w+'px',height:bounds.h+'px'});overlay.append(group);}
      const handle=document.createElement('button');handle.className='selection-handle';handle.type='button';handle.title='拖动以调整大小';handle.setAttribute('aria-label','调整所选对象大小');handle.dataset.canvasAction='resize';
      Object.assign(handle.style,{left:(bounds.x+bounds.w-8)+'px',top:(bounds.y+bounds.h-8)+'px'});overlay.append(handle);
    }
    for(const guide of guides){const line=document.createElement('div');line.className='snap-guide '+guide.axis;if(guide.axis==='x')line.style.left=guide.value+'px';else line.style.top=guide.value+'px';overlay.append(line);}
    active.append(overlay);
  }
  function selectObjects(id,toggle=false) {
    if(toggle){
      if(selectedIds.includes(id)){if(selectedIds.length>1)selectedIds=selectedIds.filter(value=>value!==id);else selectedIds=[id];}
      else selectedIds=[...selectedIds,id];
    }else if(!selectedIds.includes(id))selectedIds=[id];
    selected=selectedIds[0]||'__title__';fillEditor();
    $('stage').querySelectorAll('.element').forEach(el=>el.classList.toggle('selected',selectedIds.includes(el.dataset.elementId)&&el.closest('.slide').classList.contains('active')));
    renderOverlay();
  }
  function previewGesture() {
    if(!gesture?.slide)return;
    const boxes=new Map(E.items(gesture.slide).map(item=>[item.id,item]));
    const active=$('stage').querySelector('.slide.active');
    for(const id of gesture.ids){const item=boxes.get(id),element=[...active.querySelectorAll('.element')].find(node=>node.dataset.elementId===id);if(item&&element)Object.assign(element.style,{left:item.x+'px',top:item.y+'px',width:item.w+'px',height:item.h+'px'});}
    renderOverlay(gesture.slide,gesture.guides||[]);
  }
  function canvasPointerDown(event) {
    if(!editing||event.button!==0)return;
    const action=event.target.closest('[data-canvas-action]')?.dataset.canvasAction;
    const element=event.target.closest('.element');if(action!=='resize'&&!element)return;
    if(!event.target.closest('.slide.active'))return;
    if(!action){const id=element.dataset.elementId;const removing=event.shiftKey&&selectedIds.includes(id)&&selectedIds.length>1;selectObjects(id,event.shiftKey);if(removing)return;}
    event.preventDefault();
    const stageRect=$('stage').getBoundingClientRect(),scale=stageRect.width/1600||1;
    gesture={pointerId:event.pointerId,action:action||'move',ids:[...selectedIds],slideId:page().id,original:M.clone(page()),startX:event.clientX,startY:event.clientY,scale,moved:false,slide:null,guides:[]};
    try{$('stage').setPointerCapture(event.pointerId);}catch(_error){}
  }
  function canvasPointerMove(event) {
    if(!gesture||gesture.pointerId!==event.pointerId)return;
    const dx=(event.clientX-gesture.startX)/gesture.scale,dy=(event.clientY-gesture.startY)/gesture.scale;
    if(Math.hypot(event.clientX-gesture.startX,event.clientY-gesture.startY)<2)return;
    const result=gesture.action==='resize'?{slide:E.resize(gesture.original,gesture.ids,dx,dy),guides:[]}:E.move(gesture.original,gesture.ids,dx,dy,{snap:true});
    gesture.moved=true;gesture.slide=result.slide;gesture.guides=result.guides;previewGesture();
  }
  function commitCanvasSlide(slideModel,notice='画布位置已更新，可撤销') {
    const data=deck(),next=M.changeSlide(data,page().id,slideModel);commit(next,notice);
  }
  function activateLink(link) {
    if(!link)return;if(link.startsWith('#'))go(deck().slides.findIndex(s=>s.id===link.slice(1)));
    else message('外部链接（不会自动打开）',link+'\n此链接同时保留在导出的 PowerPoint 对象中。');
  }
  function canvasPointerUp(event) {
    if(!gesture||gesture.pointerId!==event.pointerId)return;
    const finished=gesture;gesture=null;
    if(finished.moved&&finished.slide)commitCanvasSlide(finished.slide,finished.action==='resize'?'对象大小已更新，可撤销':'对象位置已更新，可撤销');
    else renderOverlay();
  }
  function canvasPointerCancel(event) {
    if(!gesture||gesture.pointerId!==event.pointerId)return;gesture=null;render();
  }
  function render() {
    const data=deck();current=Math.max(0,Math.min(current,data.slides.length-1));
    document.title=data.title;$('deck-name').textContent=data.title;$('stage').replaceChildren();
    data.slides.forEach((s,i)=>{const el=R.slide(s,CorporateTheme.resolve(data),i,data.slides.length);el.classList.toggle('active',i===current);el.setAttribute('aria-hidden',String(i!==current));$('stage').append(el);});
    $('stage').querySelectorAll('.element').forEach(el=>{
      el.classList.toggle('selected',editing&&selectedIds.includes(el.dataset.elementId)&&el.closest('.slide').classList.contains('active'));
      el.addEventListener('click', event=>{if(editing)return;activateLink(event.target.closest('[data-hyperlink]')?.dataset.hyperlink);});
    });
    $('page-number').textContent=`${current+1} / ${data.slides.length}`;$('notes-content').textContent=data.slides[current].notes||'本页暂无讲稿';
    $('prev').disabled=current===0;$('next').disabled=current===data.slides.length-1;
    $('theme-select').value=data.theme?.id||'';
    renderList(data);if(editing)fillEditor();renderOverlay();renderPresenter(data);sizeStage();
    requestAnimationFrame(()=>{latestProblems=R.overflow($('stage'));if(latestProblems.length)tell(`发现 ${latestProblems.length} 处溢出，橙色虚线标记；请调整后导出`);});
  }
  function go(index){current=Math.max(0,Math.min(index,deck().slides.length-1));selected='__title__';selectedIds=['__title__'];richParagraph=0;richRun=0;render();}
  function editObject(patch) {
    const s=page();if(selected==='__title__')commit(M.changeSlide(deck(),s.id,{titleStyle:{...s.titleStyle,...patch}}));
    else commit(M.changeElement(deck(),s.id,selected,patch));
  }
  function updateText() {
    if(selected==='__title__')commit(M.changeSlide(deck(),page().id,{title:$('edit-text').value}));
    else editObject({text:$('edit-text').value});
  }
  function richParagraphs(){return selectedObject()?.paragraphs||[];}
  function commitRich(paragraphs){const obj=selectedObject(),value=E.rich(obj,paragraphs);editObject({paragraphs:value.paragraphs,text:value.text});}
  function patchRichRun(patch={},remove=[]) {
    const paragraphs=M.clone(richParagraphs()),run=paragraphs[richParagraph].runs[richRun];Object.assign(run,patch);remove.forEach(key=>delete run[key]);commitRich(paragraphs);
  }
  function patchRichParagraph(patch) {const paragraphs=M.clone(richParagraphs());Object.assign(paragraphs[richParagraph],patch);commitRich(paragraphs);}
  function editObjectFields(patch,remove=[]) {
    const data=M.clone(deck()),slide=data.slides[current],obj=slide.elements.find(e=>e.id===selected);Object.assign(obj,patch);remove.forEach(key=>delete obj[key]);commit(data);
  }
  function addRichParagraph(){const paragraphs=M.clone(richParagraphs());richParagraph+=1;paragraphs.splice(richParagraph,0,{align:'left',list:'none',indent:0,runs:[{text:''}]});richRun=0;commitRich(paragraphs);}
  function removeRichParagraph(){const paragraphs=M.clone(richParagraphs());if(paragraphs.length<=1)return;paragraphs.splice(richParagraph,1);richParagraph=Math.max(0,richParagraph-1);richRun=0;commitRich(paragraphs);}
  function addRichRun(){const paragraphs=M.clone(richParagraphs());richRun+=1;paragraphs[richParagraph].runs.splice(richRun,0,{text:''});commitRich(paragraphs);}
  function removeRichRun(){const paragraphs=M.clone(richParagraphs()),runs=paragraphs[richParagraph].runs;if(runs.length<=1)return;runs.splice(richRun,1);richRun=Math.max(0,richRun-1);commitRich(paragraphs);}
  function setMode(value){if(value&&presenting)setPresenter(false);editing=value;document.body.classList.toggle('editing',editing);$('editor').hidden=!editing;if(editing)$('toc').hidden=false;$('mode').textContent=editing?'完成编辑':'编辑';$('mode-label').textContent=editing?'编辑模式':'展示模式';render();}
  function moveCurrent(delta){const next=current+delta;if(next<0||next>=deck().slides.length)return;const d=M.move(deck(),current,next);current=next;commit(d,'页面顺序已更新');}
  function addSlide(duplicate){
    if(deck().slides.length>=200)throw new Error('最多支持 200 页，请拆分演示');
    const d=deck(),s=duplicate?{...M.clone(page()),id:M.uid('slide'),elements:page().elements.map(e=>({...M.clone(e),id:M.uid('el')}))}:{id:M.uid('slide'),title:'新页面',notes:'',layout:'content',elements:[{id:M.uid('text'),type:'text',x:100,y:290,w:1400,h:410,text:'在编辑模式下输入本页内容',fontSize:40}]};
    const slides=[...d.slides.slice(0,current+1),s,...d.slides.slice(current+1)];current+=1;selected='__title__';selectedIds=['__title__'];richParagraph=0;richRun=0;commit({...d,slides});
  }
  function htmlText() {
    const copy=document.documentElement.cloneNode(true);
    copy.querySelector('#deck-data').textContent=JSON.stringify(deck()).replace(/</g,'\\u003c');
    copy.querySelector('#stage').replaceChildren();copy.querySelector('#slide-list').replaceChildren();
    copy.querySelector('#notes-content').replaceChildren();copy.querySelector('#next-stage').replaceChildren();copy.querySelector('#presenter-notes').replaceChildren();copy.querySelector('#presenter').textContent='演讲者';copy.querySelector('#black-screen').textContent='黑屏';
    copy.querySelector('body').className='';
    ['toc','editor','notes-panel','recover','presenter-panel'].forEach(id=>copy.querySelector(`#${id}`).hidden=true);
    copy.querySelector('#message').removeAttribute('open');copy.querySelector('#message-title').textContent='';copy.querySelector('#message-body').textContent='';
    copy.querySelector('#mode').textContent='编辑';copy.querySelector('#mode-label').textContent='展示模式';
    return '<!doctype html>\n'+copy.outerHTML;
  }
  function downloadBlob(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);}
  const fileName=()=>deck().title.replace(/[<>:"/\\|?*\x00-\x1F]/g,'_').slice(0,80)||'presentation';
  function flushActive(){const active=document.activeElement;if(active&&active.closest('#editor'))active.blur();}
  function saveHTML(){if(imageBusy)throw new Error('图片正在读取，请稍后保存');flushActive();M.validate(deck());downloadBlob(new Blob([htmlText()],{type:'text/html;charset=utf-8'}),`${fileName()}.html`);saved=JSON.stringify(deck());tell('已发起 HTML 下载，请保留下载的文件');}
  async function exportDeck(template){
    if(imageBusy)throw new Error('图片正在读取，请稍后导出');
    flushActive();latestProblems=R.overflow($('stage'));if(latestProblems.length)throw new Error(latestProblems.join('\n'));
    const button=template?$('template'):$('export');button.disabled=true;tell('正在生成可编辑文件，动画采用静态终态…');
    try {await CorporateExport.download(deck(),{template});tell('已发起下载；请在 PowerPoint 中复核字体和版式');} finally{button.disabled=false;}
  }
  async function readImageInput(){
    const file=$('image-input').files[0];if(!file)return;
    if(!['image/png','image/jpeg'].includes(file.type)||file.size>20000000)throw new Error('请选择不超过 20 MB 的 PNG 或 JPEG 图片');
    const targetSlide=page().id,targetElement=selected;
    const src=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.addEventListener('load', ()=>resolve(reader.result));reader.addEventListener('error', ()=>reject(new Error('无法读取图片')));reader.readAsDataURL(file);});
    await new Promise((resolve,reject)=>{const image=new Image();image.addEventListener('load', ()=>image.width*image.height<=40000000?resolve():reject(new Error('图片像素超过 4000 万，请先缩小')));image.addEventListener('error', ()=>reject(new Error('图片内容无效')));image.src=src;});
    commit(M.changeElement(deck(),targetSlide,targetElement,{src,alt:file.name}),'图片已替换，请保存 HTML');
  }
  async function imageInput(){
    imageBusy=true;['save','export','template'].forEach(id=>$(id).disabled=true);tell('正在读取图片…');
    try{await readImageInput();}finally{imageBusy=false;['save','export','template'].forEach(id=>$(id).disabled=false);}
  }
  function tick(){
    const seconds=Math.floor((timerElapsed+(timerRunning?performance.now()-timerStart:0))/1000);
    $('timer').textContent=String(Math.floor(seconds/60)).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0');
    $('clock').textContent=new Date().toLocaleTimeString('zh-CN',{hour12:false});
  }
  function renderPresenter(data){
    if(!presenting)return;
    $('presenter-notes').textContent=data.slides[current].notes||'本页暂无讲稿';$('next-stage').replaceChildren();
    if(current+1<data.slides.length){const next=R.slide(data.slides[current+1],CorporateTheme.resolve(data),current+1,data.slides.length);next.classList.add('active');$('next-stage').append(next);}
    else $('next-stage').textContent='演示结束';
    const w=$('next-viewport').clientWidth;$('next-stage').style.transform='scale('+(w/1600)+')';$('next-viewport').style.height=(w*9/16)+'px';tick();
  }
  function setPresenter(value){
    if(value&&editing)setMode(false);presenting=value;document.body.classList.toggle('presenting',value);$('presenter-panel').hidden=!value;$('presenter').textContent=value?'退出演讲者':'演讲者';
    document.body.classList.remove('blackout');$('black-screen').textContent='黑屏';if(value)$('toc').hidden=false;render();
  }
  function themeSwitch(){const next=CorporateTheme.themes.find(t=>t.id===$('theme-select').value);if(next){flushActive();commit(CorporateTheme.change(deck(),next),'主题已更新，坐标保持不变');}}
  function bind() {
    $('theme-select').replaceChildren(option('','原有样式'),...CorporateTheme.themes.filter(t=>!deck().brand.id||t.brand===deck().brand.id).map(t=>option(t.id,t.id)));
    $('layout-select').replaceChildren(...CorporateTheme.layouts.map(l=>option(l.id,l.id)));
    $('theme-select').addEventListener('change',safe(themeSwitch));
    $('edit-section').addEventListener('change',safe(()=>commit(M.changeSlide(deck(),page().id,{section:$('edit-section').value}))));
    $('reapply-layout').addEventListener('click',safe(()=>commit(M.changeSlide(deck(),page().id,CorporateTheme.reapply(page(),$('layout-select').value)),'已重新应用布局，可撤销')));
    $('edit-hyperlink').addEventListener('change',safe(()=>editObject({hyperlink:$('edit-hyperlink').value||undefined})));
    $('edit-alt').addEventListener('change',safe(()=>editObject({altText:$('edit-alt').value})));
    $('edit-source').addEventListener('change',safe(()=>editObject({source:$('edit-source').value})));
    $('presenter').addEventListener('click',()=>setPresenter(!presenting));
    $('timer-toggle').addEventListener('click',()=>{if(timerRunning)timerElapsed+=performance.now()-timerStart;else timerStart=performance.now();timerRunning=!timerRunning;$('timer-toggle').textContent=timerRunning?'暂停计时':'继续计时';tick();});
    $('timer-reset').addEventListener('click',()=>{timerElapsed=0;timerStart=performance.now();tick();});
    $('black-screen').addEventListener('click',()=>{$('black-screen').textContent=document.body.classList.toggle('blackout')?'恢复画面':'黑屏';});
    $('qa').addEventListener('click',()=>{flushActive();const issues=CorporateQA.inspect(deck());message('质量检查（模型估算，不自动修改）',issues.length?issues.map(i=>i.severity+' · '+i.code+' · '+(i.slideId||'全局')+(i.elementId?' / '+i.elementId:'')+'\n'+i.message).join('\n\n'):'未发现模型问题；仍需浏览器及 PowerPoint 排版验收。');});
    setInterval(()=>{if(presenting)tick();},1000);

    $('mode').addEventListener('click', ()=>setMode(!editing));$('prev').addEventListener('click', ()=>go(current-1));$('next').addEventListener('click', ()=>go(current+1));
    $('toc-toggle').addEventListener('click', ()=>{$('toc').hidden=!$('toc').hidden;sizeStage();});$('notes-toggle').addEventListener('click', ()=>{$('notes-panel').hidden=!$('notes-panel').hidden;});
    $('fullscreen').addEventListener('click', safe(async()=>{if(document.fullscreenElement)await document.exitFullscreen();else if($('viewport').requestFullscreen)await $('viewport').requestFullscreen();else throw new Error('此浏览器未允许网页全屏，可尝试浏览器 F11');}));
    $('reduced').addEventListener('change', ()=>document.body.classList.toggle('reduced',$('reduced').checked));
    $('save').addEventListener('click', safe(saveHTML));$('export').addEventListener('click', safe(()=>exportDeck(false)));$('template').addEventListener('click', safe(()=>exportDeck(true)));
    $('add').addEventListener('click', safe(()=>addSlide(false)));$('duplicate').addEventListener('click', safe(()=>addSlide(true)));
    $('delete').addEventListener('click', safe(()=>{const d=deck();if(d.slides.length>1){selected='__title__';selectedIds=['__title__'];commit({...d,slides:d.slides.filter((_,i)=>i!==current)},'已删除，可撤销');}}));
    $('move-up').addEventListener('click', safe(()=>moveCurrent(-1)));$('move-down').addEventListener('click', safe(()=>moveCurrent(1)));
    $('undo').addEventListener('click', ()=>{history.undo();snapshotCache();render();tell('已撤销');});$('redo').addEventListener('click', ()=>{history.redo();snapshotCache();render();tell('已重做');});
    $('element-select').addEventListener('change', ()=>{selected=$('element-select').value;selectedIds=[selected];richParagraph=0;richRun=0;render();});
    $('edit-title').addEventListener('change', safe(()=>commit(M.changeSlide(deck(),page().id,{title:$('edit-title').value}))));
    $('edit-notes').addEventListener('change', safe(()=>commit(M.changeSlide(deck(),page().id,{notes:$('edit-notes').value}))));
    $('edit-text').addEventListener('change', safe(updateText));$('font-size').addEventListener('change', safe(()=>editObject({fontSize:+$('font-size').value})));
    $('color').addEventListener('change', safe(()=>editObject({color:$('color').value.slice(1)})));$('align').addEventListener('change', safe(()=>editObject({align:$('align').value})));
    $('rich-enable').addEventListener('click',safe(()=>{richParagraph=0;richRun=0;commitRich(E.fromText(selectedObject().text||''));}));
    $('rich-disable').addEventListener('click',safe(()=>editObjectFields({text:selectedObject().text},['paragraphs'])));
    $('rich-paragraph').addEventListener('change',()=>{richParagraph=+$('rich-paragraph').value;richRun=0;fillEditor();});
    $('rich-run').addEventListener('change',()=>{richRun=+$('rich-run').value;fillEditor();});
    $('rich-add-paragraph').addEventListener('click',safe(addRichParagraph));$('rich-remove-paragraph').addEventListener('click',safe(removeRichParagraph));
    $('rich-add-run').addEventListener('click',safe(addRichRun));$('rich-remove-run').addEventListener('click',safe(removeRichRun));
    $('rich-align').addEventListener('change',safe(()=>patchRichParagraph({align:$('rich-align').value})));
    $('rich-list').addEventListener('change',safe(()=>patchRichParagraph({list:$('rich-list').value})));
    $('rich-indent').addEventListener('change',safe(()=>patchRichParagraph({indent:+$('rich-indent').value})));
    $('rich-run-text').addEventListener('change',safe(()=>patchRichRun({text:$('rich-run-text').value})));
    $('rich-bold').addEventListener('change',safe(()=>patchRichRun({bold:$('rich-bold').checked})));
    $('rich-italic').addEventListener('change',safe(()=>patchRichRun({italic:$('rich-italic').checked})));
    $('rich-size').addEventListener('change',safe(()=>{const value=$('rich-size').value;patchRichRun(value?{fontSize:+value}:{},value?[]:['fontSize']);}));
    $('rich-color').addEventListener('change',safe(()=>patchRichRun({color:$('rich-color').value.slice(1)})));
    $('rich-link').addEventListener('change',safe(()=>{const value=$('rich-link').value;patchRichRun(value?{hyperlink:value}:{},value?[]:['hyperlink']);}));
    document.querySelectorAll('[data-align]').forEach(button=>button.addEventListener('click',safe(()=>{const next=E.align(page(),selectedIds,button.dataset.align);commitCanvasSlide(next,'对象已对齐，可撤销');})));
    $('stage').addEventListener('pointerdown',canvasPointerDown);$('stage').addEventListener('pointermove',canvasPointerMove);$('stage').addEventListener('pointerup',canvasPointerUp);$('stage').addEventListener('pointercancel',canvasPointerCancel);
    $('image-input').addEventListener('change', safe(imageInput));$('image-fit').addEventListener('change', safe(()=>editObject({fit:$('image-fit').value})));
    $('image-x').addEventListener('change', safe(()=>editObject({positionX:+$('image-x').value})));$('image-y').addEventListener('change', safe(()=>editObject({positionY:+$('image-y').value})));
    $('apply-data').addEventListener('click', safe(()=>{const data=JSON.parse($('edit-data').value),obj=page().elements.find(e=>e.id===selected);editObject(obj.type==='table'?{rows:data}:{labels:data.labels,series:data.series});}));
    $('recover').addEventListener('click', safe(()=>{if(cached){commit(cached.deck,'已恢复缓存副本，请保存 HTML');$('recover').hidden=true;}}));
    $('help').addEventListener('click', ()=>message('使用与转换说明',`展示：← →、空格、PageUp/PageDown 翻页；Home/End 首尾页；N 讲稿；F 全屏；E 编辑。\n编辑：拖动对象移动、拖动角点缩放；Shift+单击多选；方向键每次移动 1 单位，Shift+方向键移动 10；画布工具可对齐/等距。文本可拆为结构化段落并设置列表、字重、斜体、局部字号/颜色和安全链接。修改后离开输入框生效；也可拖动左侧目录或用按钮排序；最多撤销 30 次。Ctrl/Cmd+S 保存。\n保存：下载完整 HTML，重新打开可继续编辑。恢复缓存是辅助，不代替文件保存。\n导出：文字、图片、形状、矩形表格及基础图表为独立原生对象；富文本列表、格式和安全链接保留为原生文本。网页动画导出为完全可见的静态终态。图片裁切可能在独立图片内烘焙像素，不栅格化整页。导出 POTX 可复用母版。PowerPoint 的修改不自动回写 HTML。\n隐私：展示、编辑、导出无需联网。生成新内容需要用户批准的 Agent/模型。浏览器策略限制时请使用本机预览服务。\n字体：优先 Microsoft YaHei，未嵌入字体，换设备后请复核。\n转换记录：\n${(deck().warnings||[]).join('\n')||'无已知输入转换警告'}`));
  }
  function keyboard(event) {
    const typing=/INPUT|TEXTAREA|SELECT/.test(event.target.tagName)||event.target.isContentEditable;
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='s'){event.preventDefault();safe(saveHTML)();return;}
    if(typing||$('message').open)return;
    if(!editing&&event.key==='Enter'){const link=event.target.closest('[data-hyperlink]')?.dataset.hyperlink;if(link){event.preventDefault();activateLink(link);return;}}
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'){event.preventDefault();if(event.shiftKey)history.redo();else history.undo();snapshotCache();render();return;}
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='y'){event.preventDefault();history.redo();snapshotCache();render();return;}
    const key=event.key.toLowerCase();
    if(editing&&['arrowleft','arrowright','arrowup','arrowdown'].includes(key)){
      event.preventDefault();const amount=event.shiftKey?10:1,dx=key==='arrowleft'?-amount:key==='arrowright'?amount:0,dy=key==='arrowup'?-amount:key==='arrowdown'?amount:0;
      commitCanvasSlide(E.move(page(),selectedIds,dx,dy,{snap:false}).slide,'对象位置已微调，可撤销');return;
    }
    if(['arrowright','pagedown',' '].includes(key)){event.preventDefault();go(current+1);}else if(['arrowleft','pageup'].includes(key)){event.preventDefault();go(current-1);}else if(key==='home')go(0);else if(key==='end')go(deck().slides.length-1);else if(key==='e')setMode(!editing);else if(key==='n')$('notes-toggle').click();else if(key==='f')$('fullscreen').click();else if(key==='p')setPresenter(!presenting);else if(key==='b'&&presenting)$('black-screen').click();else if(key==='escape'&&presenting)setPresenter(false);
  }
  try {
    history=M.history(JSON.parse($('deck-data').textContent));saved=JSON.stringify(deck());
    bind();render();document.addEventListener('keydown',keyboard);window.addEventListener('resize',()=>{sizeStage();renderPresenter(deck());});document.addEventListener('fullscreenchange',sizeStage);
    if(window.ResizeObserver)new ResizeObserver(sizeStage).observe($('viewport'));
    window.addEventListener('beforeunload',e=>{if(JSON.stringify(deck())!==saved){e.preventDefault();e.returnValue='';}});
    try{cached=JSON.parse(localStorage.getItem(cacheKey()));if(cached?.deck&&JSON.stringify(cached.deck)!==saved){M.validate(cached.deck);$('recover').hidden=false;}}catch(_error){cached=null;}
    if(deck().warnings?.length)message('导入转换记录',deck().warnings.join('\n'));
    /* Public inspection API supports repeatable offline acceptance checks. */
    globalThis.CorporateApp={getDeck:deck,serialize:htmlText,go,setMode,commit,overflow:()=>R.overflow($('stage')),getIndex:()=>current,setPresenter};
  } catch(error) {tell('模型加载失败');message('无法打开演示',error.message);}
})();
