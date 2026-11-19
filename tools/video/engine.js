// Детермінований рушій: setT(t) виставляє стан сцени для моменту t (секунди).
// Сцена задає: window.DUR, window.CUR=[[t,"#sel"|[x,y],click?]], window.CAPS=[[from,to,n,text]]
// Атрибути елементів: data-t="a" або "a-b" (видимість), data-sw='[[t,"текст"],...]' (зміна тексту),
// data-cl='[[t,"клас"],...]' (клас, що вмикається з моменту t, попередній знімається),
// data-press="t" (кнопка «натиснута» 0.25 с), data-type="a,b,текст" (набір тексту).
(function(){
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
  const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
  function pos(tg){
    if(Array.isArray(tg))return tg;
    const r=document.querySelector(tg).getBoundingClientRect();
    return [r.left+r.width*0.5, r.top+r.height*0.55];
  }
  window.setT=function(t){
    document.querySelectorAll('[data-t]').forEach(e=>{
      const p=e.dataset.t.split('-').map(Number), a=p[0], b=p.length>1?p[1]:1e9;
      let o=0;
      if(t>=a&&t<b){o=clamp((t-a)/0.3,0,1);if(b<1e8)o=Math.min(o,clamp((b-t)/0.3,0,1));}
      e.style.opacity=o; e.style.visibility=o>0?'visible':'hidden';
      e.style.transform=o>0&&o<1&&!e.dataset.nomove?'translateY('+((1-o)*8)+'px)':'';
    });
    document.querySelectorAll('[data-sw]').forEach(e=>{
      const l=JSON.parse(e.dataset.sw);let v=l[0][1];l.forEach(x=>{if(t>=x[0])v=x[1]});
      if(e.textContent!==v)e.textContent=v;
    });
    document.querySelectorAll('[data-cl]').forEach(e=>{
      const l=JSON.parse(e.dataset.cl);const base=e.dataset.base||'';
      if(!e.dataset.base)e.dataset.base=e.className;
      let c='';l.forEach(x=>{if(t>=x[0])c=x[1]});
      e.className=(e.dataset.base+' '+c).trim();
    });
    document.querySelectorAll('[data-press]').forEach(e=>{
      const s=parseFloat(e.dataset.press);e.classList.toggle('press',t>=s&&t<s+0.25);
    });
    document.querySelectorAll('[data-type]').forEach(e=>{
      const p=e.dataset.type.split(','),a=+p[0],b=+p[1],tx=p.slice(2).join(',');
      e.textContent=tx.slice(0,Math.round(tx.length*clamp((t-a)/(b-a),0,1)));
    });
    // підписи
    let cap=null;(window.CAPS||[]).forEach(c=>{if(t>=c[0]&&t<c[1])cap=c});
    const pill=document.getElementById('pill');
    if(cap){pill.style.display='flex';pill.querySelector('i').textContent=cap[2];pill.querySelector('span').textContent=cap[3];
      const o=Math.min(clamp((t-cap[0])/0.3,0,1),clamp((cap[1]-t)/0.2,0,1));pill.style.opacity=o;}
    else pill.style.display='none';
    // курсор
    const C=window.CUR||[];const cur=document.getElementById('cur'),ring=document.getElementById('ring');
    if(C.length){
      let i=0;while(i<C.length-1&&C[i+1][0]<=t)i++;
      let p=pos(C[i][1]);
      if(i<C.length-1&&t>=C[i][0]){
        const n=C[i+1],q=pos(n[1]);const k=ease(clamp((t-C[i][0])/(n[0]-C[i][0]-0.0001),0,1));
        // рух відбувається в першій половині інтервалу, далі зупинка
        const k2=ease(clamp((t-C[i][0])/Math.min(0.9,n[0]-C[i][0]),0,1));
        p=[p[0]+(q[0]-p[0])*k2,p[1]+(q[1]-p[1])*k2];
      }
      cur.style.left=p[0]+'px';cur.style.top=p[1]+'px';
      let ro=0;C.forEach(c=>{if(c[2]&&t>=c[0]&&t<c[0]+0.4){ro=1-(t-c[0])/0.4;const pp=pos(c[1]);ring.style.left=(pp[0]-15)+'px';ring.style.top=(pp[1]-15)+'px';ring.style.transform='scale('+(0.6+(t-c[0])*1.5)+')'}});
      ring.style.opacity=ro;
      cur.style.opacity=t>=C[0][0]?1:0;
    }
  };
})();
