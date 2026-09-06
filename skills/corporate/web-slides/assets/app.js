/* Browser application: explicit modes, immutable history, portable save. */
(function () {
  'use strict';
  const $=id=>document.getElementById(id), M=globalThis.CorporateModel, R=globalThis.CorporateRender;
  let history, current=0, selected='__title__', editing=false, saved='', dragged=null;
  let cached=null, latestProblems=[], imageBusy=false;
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
    data.slides.forEach((s,i)=>{
      const item=document.createElement('li');item.textContent=`${i+1}. ${s.title||'导入页面'}`;item.tabIndex=0;item.draggable=editing;item.dataset.slideId=s.id;item.setAttribute('aria-current',String(i===current));
      item.onclick=()=>go(i);item.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go(i);}};
      item.ondragstart=e=>{dragged=s.id;e.dataTransfer.setData('text/plain',s.id);};
      item.ondragover=e=>{if(editing)e.preventDefault();};
      item.ondrop=safe(e=>{e.preventDefault();if(!editing)return;const d=deck(),from=d.slides.findIndex(v=>v.id===dragged),to=d.slides.findIndex(v=>v.id===s.id);if(from<0||to<0)return;const active=page().id;const next=M.move(d,from,to);current=next.slides.findIndex(v=>v.id===active);commit(next,'页面顺序已更新');dragged=null;});
      $('slide-list').append(item);
    });
  }
  function option(value,text) {const n=document.createElement('option');n.value=value;n.textContent=text;return n;}
  function fillEditor() {
    const s=page(),data=deck();$('edit-title').value=s.title;$('edit-notes').value=s.notes;
    $('element-select').replaceChildren(option('__title__','页面标题'));
    s.elements.forEach((e,i)=>$('element-select').append(option(e.id,`${i+1}. ${e.type} ${(e.text||e.alt||'').slice(0,22)}`)));
    if(selected!=='__title__'&&!s.elements.some(e=>e.id===selected))selected='__title__';
    $('element-select').value=selected;
    const obj=selected==='__title__'?{type:'text',text:s.title,fontSize:s.layout==='cover'?82:58,...s.titleStyle}:s.elements.find(e=>e.id===selected);
    const isText=['text','shape'].includes(obj.type);
    $('text-label').hidden=!isText;$('edit-text').value=obj.text||'';
    $('image-fields').hidden=obj.type!=='image';$('data-fields').hidden=!['table','chart'].includes(obj.type);
    const fs=obj.fontSize||(obj.type==='table'?28:32);if(![...$('font-size').options].some(o=>+o.value===fs))$('font-size').append(option(String(fs),`当前 ${fs}`));$('font-size').value=String(fs);
    $('color').value=`#${obj.color||data.brand.foreground}`;$('align').value=obj.align||'left';
    if(obj.type==='image'){$('image-fit').value=obj.fit||'contain';$('image-x').value=obj.positionX??.5;$('image-y').value=obj.positionY??.5;$('image-input').value='';}
    if(obj.type==='table')$('edit-data').value=JSON.stringify(obj.rows,null,2);
    if(obj.type==='chart')$('edit-data').value=JSON.stringify({labels:obj.labels,series:obj.series},null,2);
    $('undo').disabled=!history.canUndo();$('redo').disabled=!history.canRedo();
    $('delete').disabled=data.slides.length<=1;$('move-up').disabled=current===0;$('move-down').disabled=current===data.slides.length-1;
  }
  function render() {
    const data=deck();current=Math.max(0,Math.min(current,data.slides.length-1));
    document.title=data.title;$('deck-name').textContent=data.title;$('stage').replaceChildren();
    data.slides.forEach((s,i)=>{const el=R.slide(s,data.brand,i,data.slides.length);el.classList.toggle('active',i===current);el.setAttribute('aria-hidden',String(i!==current));$('stage').append(el);});
    $('stage').querySelectorAll('.element').forEach(el=>{
      el.classList.toggle('selected',editing&&el.dataset.elementId===selected&&el.closest('.slide').classList.contains('active'));
      el.onclick=()=>{if(editing){selected=el.dataset.elementId;fillEditor();$('stage').querySelectorAll('.selected').forEach(n=>n.classList.remove('selected'));el.classList.add('selected');}};
    });
    $('page-number').textContent=`${current+1} / ${data.slides.length}`;$('notes-content').textContent=data.slides[current].notes||'本页暂无讲稿';
    $('prev').disabled=current===0;$('next').disabled=current===data.slides.length-1;
    renderList(data);if(editing)fillEditor();sizeStage();
    requestAnimationFrame(()=>{latestProblems=R.overflow($('stage'));if(latestProblems.length)tell(`发现 ${latestProblems.length} 处溢出，橙色虚线标记；请调整后导出`);});
  }
  function go(index){current=Math.max(0,Math.min(index,deck().slides.length-1));selected='__title__';render();}
  function editObject(patch) {
    const s=page();if(selected==='__title__')commit(M.changeSlide(deck(),s.id,{titleStyle:{...s.titleStyle,...patch}}));
    else commit(M.changeElement(deck(),s.id,selected,patch));
  }
  function updateText() {
    if(selected==='__title__')commit(M.changeSlide(deck(),page().id,{title:$('edit-text').value}));
    else editObject({text:$('edit-text').value});
  }
  function setMode(value){editing=value;document.body.classList.toggle('editing',editing);$('editor').hidden=!editing;if(editing)$('toc').hidden=false;$('mode').textContent=editing?'完成编辑':'编辑';$('mode-label').textContent=editing?'编辑模式':'展示模式';render();}
  function moveCurrent(delta){const next=current+delta;if(next<0||next>=deck().slides.length)return;const d=M.move(deck(),current,next);current=next;commit(d,'页面顺序已更新');}
  function addSlide(duplicate){
    if(deck().slides.length>=200)throw new Error('最多支持 200 页，请拆分演示');
    const d=deck(),s=duplicate?{...M.clone(page()),id:M.uid('slide'),elements:page().elements.map(e=>({...M.clone(e),id:M.uid('el')}))}:{id:M.uid('slide'),title:'新页面',notes:'',layout:'content',elements:[{id:M.uid('text'),type:'text',x:100,y:290,w:1400,h:410,text:'在编辑模式下输入本页内容',fontSize:40}]};
    const slides=[...d.slides.slice(0,current+1),s,...d.slides.slice(current+1)];current+=1;selected='__title__';commit({...d,slides});
  }
  function htmlText() {
    const copy=document.documentElement.cloneNode(true);
    copy.querySelector('#deck-data').textContent=JSON.stringify(deck()).replace(/</g,'\\u003c');
    copy.querySelector('#stage').replaceChildren();copy.querySelector('#slide-list').replaceChildren();
    copy.querySelector('#notes-content').replaceChildren();
    copy.querySelector('body').className='';
    ['toc','editor','notes-panel','recover'].forEach(id=>copy.querySelector(`#${id}`).hidden=true);
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
    const src=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=()=>reject(new Error('无法读取图片'));reader.readAsDataURL(file);});
    await new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>image.width*image.height<=40000000?resolve():reject(new Error('图片像素超过 4000 万，请先缩小'));image.onerror=()=>reject(new Error('图片内容无效'));image.src=src;});
    commit(M.changeElement(deck(),targetSlide,targetElement,{src,alt:file.name}),'图片已替换，请保存 HTML');
  }
  async function imageInput(){
    imageBusy=true;['save','export','template'].forEach(id=>$(id).disabled=true);tell('正在读取图片…');
    try{await readImageInput();}finally{imageBusy=false;['save','export','template'].forEach(id=>$(id).disabled=false);}
  }
  function bind() {
    $('mode').onclick=()=>setMode(!editing);$('prev').onclick=()=>go(current-1);$('next').onclick=()=>go(current+1);
    $('toc-toggle').onclick=()=>{$('toc').hidden=!$('toc').hidden;sizeStage();};$('notes-toggle').onclick=()=>{$('notes-panel').hidden=!$('notes-panel').hidden;};
    $('fullscreen').onclick=safe(async()=>{if(document.fullscreenElement)await document.exitFullscreen();else if($('viewport').requestFullscreen)await $('viewport').requestFullscreen();else throw new Error('此浏览器未允许网页全屏，可尝试浏览器 F11');});
    $('reduced').onchange=()=>document.body.classList.toggle('reduced',$('reduced').checked);
    $('save').onclick=safe(saveHTML);$('export').onclick=safe(()=>exportDeck(false));$('template').onclick=safe(()=>exportDeck(true));
    $('add').onclick=safe(()=>addSlide(false));$('duplicate').onclick=safe(()=>addSlide(true));
    $('delete').onclick=safe(()=>{const d=deck();if(d.slides.length>1)commit({...d,slides:d.slides.filter((_,i)=>i!==current)},'已删除，可撤销');});
    $('move-up').onclick=safe(()=>moveCurrent(-1));$('move-down').onclick=safe(()=>moveCurrent(1));
    $('undo').onclick=()=>{history.undo();snapshotCache();render();tell('已撤销');};$('redo').onclick=()=>{history.redo();snapshotCache();render();tell('已重做');};
    $('element-select').onchange=()=>{selected=$('element-select').value;render();};
    $('edit-title').onchange=safe(()=>commit(M.changeSlide(deck(),page().id,{title:$('edit-title').value})));
    $('edit-notes').onchange=safe(()=>commit(M.changeSlide(deck(),page().id,{notes:$('edit-notes').value})));
    $('edit-text').onchange=safe(updateText);$('font-size').onchange=safe(()=>editObject({fontSize:+$('font-size').value}));
    $('color').onchange=safe(()=>editObject({color:$('color').value.slice(1)}));$('align').onchange=safe(()=>editObject({align:$('align').value}));
    $('image-input').onchange=safe(imageInput);$('image-fit').onchange=safe(()=>editObject({fit:$('image-fit').value}));
    $('image-x').onchange=safe(()=>editObject({positionX:+$('image-x').value}));$('image-y').onchange=safe(()=>editObject({positionY:+$('image-y').value}));
    $('apply-data').onclick=safe(()=>{const data=JSON.parse($('edit-data').value),obj=page().elements.find(e=>e.id===selected);editObject(obj.type==='table'?{rows:data}:{labels:data.labels,series:data.series});});
    $('recover').onclick=safe(()=>{if(cached){commit(cached.deck,'已恢复缓存副本，请保存 HTML');$('recover').hidden=true;}});
    $('help').onclick=()=>message('使用与转换说明',`展示：← →、空格、PageUp/PageDown 翻页；Home/End 首尾页；N 讲稿；F 全屏；E 编辑。\n编辑：选择对象，修改后离开输入框生效；可拖动左侧目录排序，也可上移/下移；最多撤销 30 次。Ctrl/Cmd+S 保存。\n保存：下载完整 HTML，重新打开可继续编辑。恢复缓存是辅助，不代替文件保存。\n导出：文字、图片、形状、矩形表格及基础图表为独立原生对象。网页动画导出为完全可见的静态终态。图片裁切可能在独立图片内烘焙像素，不栅格化整页。导出 POTX 可复用母版。PowerPoint 的修改不自动回写 HTML。\n隐私：展示、编辑、导出无需联网。生成新内容需要用户批准的 Agent/模型。浏览器策略限制时请使用本机预览服务。\n字体：优先 Microsoft YaHei，未嵌入字体，换设备后请复核。\n转换记录：\n${(deck().warnings||[]).join('\n')||'无已知输入转换警告'}`);
  }
  function keyboard(event) {
    const typing=/INPUT|TEXTAREA|SELECT/.test(event.target.tagName)||event.target.isContentEditable;
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='s'){event.preventDefault();safe(saveHTML)();return;}
    if(typing||$('message').open)return;
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'){event.preventDefault();if(event.shiftKey)history.redo();else history.undo();snapshotCache();render();return;}
    if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='y'){event.preventDefault();history.redo();snapshotCache();render();return;}
    const key=event.key.toLowerCase();
    if(['arrowright','pagedown',' '].includes(key)){event.preventDefault();go(current+1);}else if(['arrowleft','pageup'].includes(key)){event.preventDefault();go(current-1);}else if(key==='home')go(0);else if(key==='end')go(deck().slides.length-1);else if(key==='e')setMode(!editing);else if(key==='n')$('notes-toggle').click();else if(key==='f')$('fullscreen').click();
  }
  try {
    history=M.history(JSON.parse($('deck-data').textContent));saved=JSON.stringify(deck());
    bind();render();document.addEventListener('keydown',keyboard);window.addEventListener('resize',sizeStage);document.addEventListener('fullscreenchange',sizeStage);
    if(window.ResizeObserver)new ResizeObserver(sizeStage).observe($('viewport'));
    window.addEventListener('beforeunload',e=>{if(JSON.stringify(deck())!==saved){e.preventDefault();e.returnValue='';}});
    try{cached=JSON.parse(localStorage.getItem(cacheKey()));if(cached?.deck&&JSON.stringify(cached.deck)!==saved){M.validate(cached.deck);$('recover').hidden=false;}}catch(_error){cached=null;}
    if(deck().warnings?.length)message('导入转换记录',deck().warnings.join('\n'));
    /* Public inspection API supports repeatable offline acceptance checks. */
    globalThis.CorporateApp={getDeck:deck,serialize:htmlText,go,setMode,commit,overflow:()=>R.overflow($('stage')),getIndex:()=>current};
  } catch(error) {tell('模型加载失败');message('无法打开演示',error.message);}
})();
