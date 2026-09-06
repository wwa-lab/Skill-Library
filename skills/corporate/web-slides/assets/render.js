/* Fixed-stage rendering shared by presentation, editing and previews. */
(function (root) {
  'use strict';
  const node = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; };
  const svgNode = (tag, attrs, text) => { const n = document.createElementNS('http://www.w3.org/2000/svg', tag); Object.entries(attrs).forEach(([k, v]) => n.setAttribute(k, v)); if (text !== undefined) n.textContent = text; return n; };
  function chart(el, brand) {
    const svg = svgNode('svg', {viewBox:`0 0 ${el.w} ${el.h}`, role:'img', 'aria-label': el.labels.join('、')});
    const colors = el.colors?.length ? el.colors : [brand.accent, brand.foreground, '999999', 'E6ABB6'];
    const textSize = el.fontSize || 24, left = 65, top = 35, width = el.w - 100, height = el.h - 120;
    const label = (x, y, text, anchor='middle') => svg.append(svgNode('text', {x,y,'text-anchor':anchor,'font-size':textSize,fill:`#${el.color || brand.foreground}`},text));
    if (el.chartType === 'pie') {
      const values = el.series[0].values, total = values.reduce((a,b) => a+b,0);
      const radius = Math.min(el.w * .29, el.h * .37), cx=el.w*.36, cy=el.h*.48;
      let angle = -Math.PI / 2;
      values.forEach((value, i) => {
        const end = angle + value / total * Math.PI * 2;
        if (value === total) svg.append(svgNode('circle',{cx,cy,r:radius,fill:`#${colors[i%colors.length]}`}));
        else if(value>0) svg.append(svgNode('path',{d:`M ${cx} ${cy} L ${cx+Math.cos(angle)*radius} ${cy+Math.sin(angle)*radius} A ${radius} ${radius} 0 ${end-angle>Math.PI?1:0} 1 ${cx+Math.cos(end)*radius} ${cy+Math.sin(end)*radius} Z`,fill:`#${colors[i%colors.length]}`}));
        const ly=50+i*(textSize+14);
        svg.append(svgNode('rect',{x:el.w*.71,y:ly-18,width:16,height:16,fill:`#${colors[i%colors.length]}`}));
        label(el.w*.71+25,ly,`${el.labels[i]} ${Math.round(value/total*100)}%`,'start'); angle=end;
      });
      return svg;
    }
    const values = el.series.flatMap(s=>s.values), min = Math.min(0,...values), max = Math.max(1,...values);
    const range=max-min || 1, yy = v => top + height * (max-v) / range;
    for(let t=0;t<=4;t++) {
      const value=min+range*t/4, y=yy(value);
      svg.append(svgNode('line',{x1:left,y1:y,x2:left+width,y2:y,stroke:'#DDDDDD','stroke-width':1}));
      label(left-12,y+8,`${Math.round(value*10)/10}`,'end');
    }
    const slot=width/el.labels.length;
    el.labels.forEach((v,i)=>label(left+slot*(i+.5),top+height+35,v));
    el.series.forEach((series,si)=>{
      const color=`#${colors[si%colors.length]}`;
      if(el.chartType==='bar') series.values.forEach((v,i)=>{
        const bw=slot*.7/el.series.length;
        svg.append(svgNode('rect',{x:left+slot*i+slot*.15+si*bw,y:yy(v),width:Math.max(1,bw-4),height:Math.max(0,yy(0)-yy(v)),fill:color}));
      });
      else {
        const points=series.values.map((v,i)=>`${left+slot*(i+.5)},${yy(v)}`).join(' ');
        svg.append(svgNode('polyline',{points,fill:'none',stroke:color,'stroke-width':4}));
        series.values.forEach((v,i)=>svg.append(svgNode('circle',{cx:left+slot*(i+.5),cy:yy(v),r:5,fill:color})));
      }
      const lx=left+si*width/el.series.length;
      svg.append(svgNode('rect',{x:lx,y:el.h-30,width:16,height:16,fill:color}));
      label(lx+25,el.h-14,series.name,'start');
    });
    return svg;
  }
  function element(el, brand) {
    const box=node('div',`element ${el.type}-element`); box.dataset.elementId=el.id;
    Object.assign(box.style,{left:`${el.x}px`,top:`${el.y}px`,width:`${el.w}px`,height:`${el.h}px`,fontSize:`${el.fontSize || (el.type==='table'?28:32)}px`,color:`#${el.color||brand.foreground}`,textAlign:el.align||'left',fontWeight:el.bold?'700':'400'});
    if (el.type==='text') box.textContent=el.text;
    if (el.type==='shape') { box.classList.add(el.shape); box.style.background=el.shape==='line'?'transparent':`#${el.fill||brand.accent}`; box.style.borderColor=`#${el.fill||brand.accent}`; box.textContent=el.text||''; }
    if (el.type==='image') { const img=node('img'); img.src=el.src;img.alt=el.alt||'';img.draggable=false;img.style.objectFit=el.fit||'contain';img.style.objectPosition=`${(el.positionX??.5)*100}% ${(el.positionY??.5)*100}%`;box.append(img); }
    if (el.type==='table') {
      const table=node('table');const tbody=node('tbody'); table.append(tbody);
      el.rows.forEach((row,i)=>{const tr=node('tr');tr.style.height=`${100/el.rows.length}%`;row.forEach(cell=>{const td=node(i===0?'th':'td',null,cell);if(i>0){const bg=brand.background;const dark=(parseInt(bg.slice(0,2),16)*.299+parseInt(bg.slice(2,4),16)*.587+parseInt(bg.slice(4,6),16)*.114)<128;td.style.background=i%2?(dark?'#252525':'#F4F4F4'):`#${bg}`;}if(i===0){td.style.background=`#${el.accent||brand.accent}`;td.style.color='#fff';}tr.append(td);});tbody.append(tr);});box.append(table);
    }
    if (el.type==='chart') box.append(chart(el,brand));
    return box;
  }
  function slide(slideModel,brand,index,total) {
    const page=node('section','slide'); page.dataset.slideId=slideModel.id;page.setAttribute('aria-label',`${index+1} / ${total} ${slideModel.title}`);
    page.style.background=`#${slideModel.background||brand.background}`;page.style.color=`#${brand.foreground}`;page.style.fontFamily=`"${brand.fontFace.replace(/["\\]/g,'')}","Microsoft YaHei","PingFang SC",sans-serif`;
    if(slideModel.layout!=='imported') {
      const rule=node('div','brand-rule');rule.style.background=`#${brand.accent}`;page.append(rule);
      page.append(node('div','brand-footer',brand.name),node('div','brand-page',`${String(index+1).padStart(2,'0')} / ${String(total).padStart(2,'0')}`));
      if(brand.logo) {const logo=node('img','brand-logo');logo.src=brand.logo;logo.alt=brand.name;page.append(logo);}
    }
    if(slideModel.title) {
      const title=element({id:'__title__',type:'text',text:slideModel.title,x:100,y:92,w:1400,h:125,fontSize:slideModel.layout==='cover'?82:58,bold:true,...slideModel.titleStyle},brand);title.classList.add('title-element');title.style.fontFamily=`"${brand.titleFontFace.replace(/["\\]/g,'')}","Microsoft YaHei","PingFang SC",sans-serif`;page.append(title);
    }
    slideModel.elements.forEach(el=>page.append(element(el,brand)));return page;
  }
  function overflow(stage) {
    const problems=[];
    stage.querySelectorAll('.element').forEach(el=>{
      let bad=el.scrollHeight>el.clientHeight+2||el.scrollWidth>el.clientWidth+2;
      el.querySelectorAll('table').forEach(t=>{if(t.offsetHeight>el.clientHeight+2||t.offsetWidth>el.clientWidth+2)bad=true;});
      el.querySelectorAll('svg').forEach(svg=>{
        const bbox=svg.getBBox(), w=svg.viewBox.baseVal.width,h=svg.viewBox.baseVal.height;
        if(bbox.x < -2 || bbox.y < -2 || bbox.x+bbox.width > w+2 || bbox.y+bbox.height > h+2)bad=true;
        const labels=[...svg.querySelectorAll('text')].map(t=>t.getBBox());
        for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++){
          const a=labels[i],b=labels[j];
          if(a.x < b.x+b.width-2 && a.x+a.width > b.x+2 && a.y < b.y+b.height-2 && a.y+a.height > b.y+2)bad=true;
        }
      });
      el.classList.toggle('overflow',bad);
      if(bad)problems.push(`${el.closest('.slide').getAttribute('aria-label')} / ${el.dataset.elementId} 内容溢出，请减字、减小字号或拆页`);
    });return problems;
  }
  root.CorporateRender={slide,element,overflow};
})(globalThis);
