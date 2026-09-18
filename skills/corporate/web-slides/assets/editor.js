/* Pure geometry and structured text operations. Browser events commit one history entry. */
(function(root){
 'use strict';
 const clone=v=>JSON.parse(JSON.stringify(v)),fail=(v,m)=>{if(!v)throw new Error(m);};
 function items(slide){return [...(slide.title?[{id:'__title__',type:'text',x:100,y:92,w:1400,h:125,...slide.titleBox}]:[]),...slide.elements];}
 function bounds(objects){if(!objects.length)return null;const x=Math.min(...objects.map(e=>e.x)),y=Math.min(...objects.map(e=>e.y));return{x,y,w:Math.max(...objects.map(e=>e.x+e.w))-x,h:Math.max(...objects.map(e=>e.y+e.h))-y};}
 function setBoxes(slide,boxes){
  const s=clone(slide);
  for(const [id,b] of Object.entries(boxes)){
   for(const k of ['x','y','w','h'])fail(Number.isFinite(b[k]),'Invalid canvas coordinates');
   fail(b.x>=0&&b.y>=0&&b.w>0&&b.h>0&&b.x+b.w<=1600.1&&b.y+b.h<=900.1,'Object must fit in canvas');
   const geometry=Object.fromEntries(['x','y','w','h'].map(k=>[k,Math.round(b[k]*1000)/1000]));
   if(id==='__title__'){s.titleBox=geometry;s.layoutOverride=true;}
   else {const e=s.elements.find(e=>e.id===id);fail(e,'Missing selected object');Object.assign(e,geometry,{layoutOverride:true});}
  }
  return s;
 }
 function move(slide,ids,dx,dy,{snap=false}={}){
  const all=items(slide),chosen=all.filter(e=>ids.includes(e.id)),b=bounds(chosen);if(!b)return{slide:clone(slide),guides:[]};
  const guides=[];dx=Math.max(-b.x,Math.min(1600-b.x-b.w,dx));dy=Math.max(-b.y,Math.min(900-b.y-b.h,dy));
  if(snap){
   const others=all.filter(e=>!ids.includes(e.id));
   for(const axis of ['x','y']){
    const size=axis==='x'?'w':'h',limit=axis==='x'?1600:900,delta=axis==='x'?dx:dy;
    const targets=axis==='x'?[100,800,1500]:[92,450,800];for(const e of others)targets.push(e[axis],e[axis]+e[size]/2,e[axis]+e[size]);
    let best=null;
    for(const anchor of [b[axis],b[axis]+b[size]/2,b[axis]+b[size]])for(const t of targets){const gap=t-anchor-delta;if(Math.abs(gap)<=8&&(!best||Math.abs(gap)<Math.abs(best.gap))&&b[axis]+delta+gap>=0&&b[axis]+b[size]+delta+gap<=limit)best={gap,t};}
    if(best){if(axis==='x')dx+=best.gap;else dy+=best.gap;guides.push({axis,value:best.t});}
   }
  }
  return{slide:setBoxes(slide,Object.fromEntries(chosen.map(e=>[e.id,{x:e.x+dx,y:e.y+dy,w:e.w,h:e.h}]))),guides};
 }
 function resize(slide,ids,dw,dh){
  const chosen=items(slide).filter(e=>ids.includes(e.id)),b=bounds(chosen);if(!b)return clone(slide);
  const sx=Math.max(Math.min(1,Math.max(...chosen.map(e=>8/e.w))),Math.min((1600-b.x)/b.w,(b.w+dw)/b.w));
  const sy=Math.max(Math.min(1,Math.max(...chosen.map(e=>8/e.h))),Math.min((900-b.y)/b.h,(b.h+dh)/b.h));
  return setBoxes(slide,Object.fromEntries(chosen.map(e=>[e.id,{x:b.x+(e.x-b.x)*sx,y:b.y+(e.y-b.y)*sy,w:e.w*sx,h:e.h*sy}])));
 }
 function align(slide,ids,mode){
  const chosen=items(slide).filter(e=>ids.includes(e.id)),b=bounds(chosen);if(!b)return clone(slide);const boxes={};
  fail(['left','center','right','top','middle','bottom','horizontal','vertical'].includes(mode),'Unknown alignment');
  if(['horizontal','vertical'].includes(mode)){
   if(chosen.length<3)return clone(slide);
   const axis=mode==='horizontal'?'x':'y',size=axis==='x'?'w':'h',sorted=[...chosen].sort((a,b)=>a[axis]-b[axis]);
   const gap=(b[size]-sorted.reduce((n,e)=>n+e[size],0))/(sorted.length-1);let at=b[axis];
   for(const e of sorted){boxes[e.id]={x:e.x,y:e.y,w:e.w,h:e.h,[axis]:at};at+=e[size]+gap;}
  }else for(const e of chosen){const g={x:e.x,y:e.y,w:e.w,h:e.h};if(mode==='left')g.x=b.x;if(mode==='center')g.x=b.x+(b.w-e.w)/2;if(mode==='right')g.x=b.x+b.w-e.w;if(mode==='top')g.y=b.y;if(mode==='middle')g.y=b.y+(b.h-e.h)/2;if(mode==='bottom')g.y=b.y+b.h-e.h;boxes[e.id]=g;}
  return setBoxes(slide,boxes);
 }
 const plain=paragraphs=>paragraphs.map(p=>p.runs.map(r=>r.text).join('')).join('\n');
 function rich(element,paragraphs){fail(element.type==='text','Rich text is supported on text objects');return{...clone(element),paragraphs:clone(paragraphs),text:plain(paragraphs)};}
 const fromText=text=>text.split('\n').map(text=>({align:'left',list:'none',indent:0,runs:[{text}]}));
 root.CorporateEdit=Object.freeze({items,bounds,setBoxes,move,resize,align,plain,rich,fromText});
})(globalThis);
