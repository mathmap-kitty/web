(function(){
'use strict';
var DATA = window.EXAM_DATA || [];
var YEARS = ['115','114','113','112','111'];
var UNIT_ORDER = ['數與式','多項式函數','指數與對數','數列與級數','排列組合與機率','數據分析','三角','直線與圓','平面向量','空間向量','矩陣'];
/* 58 核心概念總目錄（mathmap 短標題）：供「按核心概念」補列未出題核心概念 */
var KP_ALL = {
 '數與式':[['kp1','實數系與有理／無理'],['kp2','絕對值'],['kp3','數線、距離與根號估算'],['kp4','乘法公式與算幾不等式'],['kp5','比例、百分率與加權平均'],['kp6','高斯（最大整數）函數']],
 '多項式函數':[['kp1','除法、餘式與因式定理'],['kp2','二次函數：判別式與配方'],['kp3','多項式方程式與不等式'],['kp4','高次方程式（有理根、勘根）'],['kp5','三次函數圖形與對稱中心']],
 '指數與對數':[['kp1','指數律與指數方程'],['kp2','對數的定義與運算'],['kp3','常用對數（科學記號、位數）'],['kp4','指數對數函數圖形'],['kp5','應用模型與數列結合']],
 '數列與級數':[['kp1','等差數列'],['kp2','等比數列'],['kp3','遞迴數列'],['kp4','級數求和與規律週期']],
 '排列組合與機率':[['kp1','計數原理與排列'],['kp2','組合與分組分配'],['kp3','古典機率'],['kp4','條件機率與貝氏'],['kp5','獨立事件與餘事件'],['kp6','期望值']],
 '數據分析':[['kp1','一維數據與標準差'],['kp2','相關係數'],['kp3','迴歸直線（最適直線）'],['kp4','加權平均與資料判讀']],
 '三角':[['kp1','三角比、弧度與廣義角'],['kp2','正弦定理、餘弦定理'],['kp3','三角測量與幾何應用'],['kp4','三角函數圖形（疊合、對稱）'],['kp5','和差角、倍角'],['kp6','角平分線、面積比與相似'],['kp7','圓周角與二面角中的三角']],
 '直線與圓':[['kp1','直線方程式與斜率'],['kp2','兩點距離與三角形'],['kp3','圓方程式'],['kp4','直線與圓的位置'],['kp5','平面區域與線性規劃']],
 '平面向量':[['kp1','向量的表示與運算'],['kp2','線性組合、分點與面積比'],['kp3','內積：夾角、垂直、正射影'],['kp4','行列式與平行四邊形面積'],['kp5','向量的旋轉與坐標應用']],
 '空間向量':[['kp1','空間坐標與距離'],['kp2','內積與垂直'],['kp3','外積與體積'],['kp4','平面方程式與距離'],['kp5','空間直線與歪斜線'],['kp6','二面角與立體']],
 '矩陣':[['kp1','意義、相等與乘法'],['kp2','矩陣的高次方'],['kp3','反方陣與解矩陣方程式'],['kp4','一次聯立與高斯消去'],['kp5','平面線性變換']]
};
/* 108 課綱「數B 不含」的核心概念（對照領綱：行列式/空間向量運算僅 11A、線性規劃在 12乙、三元消去法僅 11A） */
var B_EXCLUDED = {'直線與圓':{'kp5':1},'平面向量':{'kp4':1},'空間向量':{'kp2':1,'kp3':1,'kp4':1,'kp5':1,'kp6':1},'矩陣':{'kp4':1}};
var LS_SUBJ = 'exama_subject_v1';
var state = { view:'home', subject:(localStorage.getItem(LS_SUBJ)||'A'), year:'115', unit:'', diff:'', tUnit:'', tKp:'', hardBand:'hard' };
var LS = 'exama_done_v1';
var done = JSON.parse(localStorage.getItem(LS) || '{}');
var LS_STAR = 'exama_star_v1';
var star = JSON.parse(localStorage.getItem(LS_STAR) || '{}');
var LS_TEST = 'exama_testmode_v1';
var testMode = localStorage.getItem(LS_TEST) === '1';
var SUBJ = [];  // 目前科目（A/B）的題目，由 buildIndex() 填
function saveStar(){ localStorage.setItem(LS_STAR, JSON.stringify(star)); }
function saveDone(){ localStorage.setItem(LS, JSON.stringify(done)); }
function starCount(){ return SUBJ.filter(function(q){ return star[qid(q)]; }).length; }

function qid(q){ return (q.subject==='B'?'B':'')+q.year+'-'+q.num; }
function rateNum(r){ var m = String(r).match(/(\d+)\s*%/); return m ? +m[1] : null; }
function diffOf(q){ var n=rateNum(q.rate); if(n===null) return 'none'; if(n<20) return 'hard'; if(n<=50) return 'mid'; return 'easy'; }
function el(tag,cls,html){ var e=document.createElement(tag); if(cls) e.className=cls; if(html!=null) e.innerHTML=html; return e; }

/* ---------- 核心概念 index（依目前科目重建） ---------- */
var byUnit = {};
function buildIndex(){
  SUBJ = DATA.filter(function(q){ return (q.subject||'A')===state.subject; });
  byUnit = {};
  SUBJ.forEach(function(q){
    var seenU={}, seenA={};
    q.kaodian.forEach(function(k){
      var u=byUnit[k.unit] || (byUnit[k.unit]={name:k.unit,qs:[],kps:{},korder:[]});
      if(!seenU[k.unit]){ u.qs.push(q); seenU[k.unit]=1; }
      var a=String(k.url).split('#')[1]||k.title;   // 以 anchor（kp1…）為核心概念身分，避免變體標題重複
      var kp=u.kps[a];
      if(!kp){ kp=u.kps[a]={title:k.title,url:k.url,qs:[]}; u.korder.push(a); }
      else if(String(k.title).length>String(kp.title).length){ kp.title=k.title; kp.url=k.url; } // 取較完整的標題
      if(!seenA[a]){ kp.qs.push(q); seenA[a]=1; }
    });
  });
}
function unitsSorted(){ return Object.keys(byUnit).sort(function(a,b){ return UNIT_ORDER.indexOf(a)-UNIT_ORDER.indexOf(b); }); }
function coveredKp(){ var n=0; for(var u in byUnit){ n+=Object.keys(byUnit[u].kps).length; } return n; }
function anchorNum(url){ var h=String(url).split('#')[1]||''; var m=h.match(/(\d+)/); return m?+m[1]:999; }

/* ---------- lazy KaTeX ---------- */
function texEl(latex, display){
  var e=document.createElement(display?'div':'span');
  e.className = display?'katex-block':'katex-inline';
  e.setAttribute('data-tex', latex); if(display) e.setAttribute('data-disp','1');
  e.textContent = ''; return e;
}
function renderIn(root){
  if(!window.katex) return;
  root.querySelectorAll('[data-tex]:not([data-done])').forEach(function(e){
    try{ katex.render(e.getAttribute('data-tex'), e, {displayMode:e.hasAttribute('data-disp'), throwOnError:false, strict:false}); }
    catch(err){ e.textContent=e.getAttribute('data-tex'); }
    e.setAttribute('data-done','1');
  });
}
function showSec(sec){ sec.classList.add('show'); renderIn(sec); }
function resetAllReveal(){
  document.querySelectorAll('.sec.show').forEach(function(s){ s.classList.remove('show'); });
  document.querySelectorAll('.qcard').forEach(function(c){ c._ri=0; var nb=c.querySelector('.next-btn'); if(nb){ nb.disabled=false; nb.textContent='下一步提示 ▸'; } if(c._setAllOpen) c._setAllOpen(false); });
}

/* ---------- card ---------- */
function sec(cls,label){ var d=document.createElement('div'); d.className='sec '+cls;
  var l=document.createElement('div'); l.className='lab'; l.textContent=label; d.appendChild(l); return d; }

/* ---------- 文字題幹 / 選項 渲染（左欄恆顯示，立即算 KaTeX；行內數學以 $...$ 標記） ---------- */
function texNow(latex, display){
  var e=document.createElement(display?'div':'span');
  e.className=display?'katex-block':'katex-inline';
  if(window.katex){ try{ katex.render(latex, e, {displayMode:display, throwOnError:false, strict:false}); }
    catch(err){ e.textContent=latex; } }
  else { e.textContent=latex; e.setAttribute('data-tex',latex); if(display) e.setAttribute('data-disp','1'); }
  return e;
}
function renderRich(container, str){
  var parts=String(str).split(/\$([^$]*)\$/);   // 偶數段=文字，奇數段=行內數學
  for(var i=0;i<parts.length;i++){
    if(i%2===0){ if(parts[i]!=='') container.appendChild(document.createTextNode(parts[i])); }
    else { container.appendChild(texNow(parts[i], false)); }
  }
}
function renderStem(items, cls){
  var wrap=document.createElement('div'); wrap.className=cls;
  items.forEach(function(it){
    if(it.t==='fig'){ var im=new Image(); im.loading='lazy'; im.src=it.src; im.className='qfig'; im.alt='題目附圖'; wrap.appendChild(im); }
    else { var pp=document.createElement('p'); pp.className='qpara'; renderRich(pp, it.c); wrap.appendChild(pp); }
  });
  return wrap;
}
function renderOpts(opts){
  var box=document.createElement('div'); box.className='qopts';
  opts.forEach(function(o,i){
    var row=document.createElement('div'); row.className='qopt';
    var lab=document.createElement('span'); lab.className='olab'; lab.textContent='('+(i+1)+')';
    var body=document.createElement('span'); body.className='obody'; renderRich(body,o);
    row.appendChild(lab); row.appendChild(body); box.appendChild(row);
  });
  return box;
}

function makeCard(q){
  var card=document.createElement('section'); card.className='qcard'; card.id='q-'+qid(q);
  var grid=document.createElement('div'); grid.className='qcard-grid'; card.appendChild(grid);

  var L=document.createElement('div'); L.className='col q'; grid.appendChild(L);
  var head=document.createElement('div'); head.className='qhead';
  head.innerHTML='<span class="badge">'+q.year+' 第'+q.num+'題</span><span class="badge type">'+q.type+'</span><span class="rate">答對率 '+q.rate+'</span>';
  L.appendChild(head);
  if(q.qtext){
    if(q.gstem){ var gs=renderStem(q.gstem,'qstem gstem'); var gl=document.createElement('div'); gl.className='glab'; gl.textContent='題組共用題幹'; gs.insertBefore(gl,gs.firstChild); L.appendChild(gs); }
    L.appendChild(renderStem(q.qtext,'qstem'));
    if(q.opts && q.opts.length){ L.appendChild(renderOpts(q.opts)); }
  } else {
    if(q.stem){ var si=new Image(); si.loading='lazy'; si.src=q.stem; si.className='qimg'; si.alt='題組共用題幹'; L.appendChild(si); }
    var im=new Image(); im.loading='lazy'; im.src=q.img; im.className='qimg'; im.alt='第'+q.num+'題'; L.appendChild(im);
  }
  var foot=document.createElement('div'); foot.className='qfoot';
  var dt=document.createElement('label'); dt.className='done-toggle';
  var cb=document.createElement('input'); cb.type='checkbox'; cb.checked=!!done[qid(q)];
  cb.onchange=function(){ done[qid(q)]=cb.checked; saveDone(); card.style.opacity=cb.checked?'.55':'1'; };
  dt.appendChild(cb); dt.appendChild(document.createTextNode(' 已複習 / 標記完成')); foot.appendChild(dt);
  var sb=document.createElement('button'); sb.className='star-btn';
  function setStar(){ var on=!!star[qid(q)]; sb.classList.toggle('on',on); sb.textContent=on?'★ 已在複習清單':'☆ 加入複習清單'; }
  setStar();
  sb.onclick=function(){ if(star[qid(q)]) delete star[qid(q)]; else star[qid(q)]=true; saveStar(); setStar(); };
  foot.appendChild(sb); L.appendChild(foot);
  if(cb.checked) card.style.opacity='.55';

  var R=document.createElement('div'); R.className='col s'; grid.appendChild(R);
  R.innerHTML='<h3>解題引導（點按鈕逐步顯示）</h3>';
  var bar=document.createElement('div'); bar.className='reveal-bar'; R.appendChild(bar);

  var secKey=sec('key','💡 解題關鍵'); var kp=document.createElement('div'); renderRich(kp, q.key); secKey.appendChild(kp);
  var secKd=sec('kd','📍 對應 mathmap 核心概念'); var chips=document.createElement('div'); chips.className='kchips';
  q.kaodian.forEach(function(k){ var a=document.createElement('a'); a.className='kchip'; a.href=k.url; a.target='_blank'; a.rel='noopener';
    a.innerHTML='<span class="u">〔'+k.unit+'〕</span>'+k.title; chips.appendChild(a); });
  if(!q.kaodian.length){ var kn=document.createElement('div'); kn.className='kdnote';
    kn.textContent='此題為數學 B 專屬範圍（圓錐截痕／球面經緯度／空間坐標），mathmap 核心概念待補。'; chips.appendChild(kn); }
  secKd.appendChild(chips);

  var order=[secKey, secKd];
  q.steps.forEach(function(st){ var ss=document.createElement('div'); ss.className='sec step-sec';
    if(st.type==='math'){ ss.appendChild(texEl(st.c,true)); }
    else { var tx=document.createElement('div'); tx.className='stext'; renderRich(tx, st.c); ss.appendChild(tx); }
    order.push(ss); });
  if(q.fig){ var fs=document.createElement('div'); fs.className='sec step-sec'; var fi=new Image(); fi.loading='lazy'; fi.src=q.fig; fi.className='sfig'; fi.alt='詳解圖'; fs.appendChild(fi); order.push(fs); }

  var secAns=sec('ans','✅ 答案'); var av=document.createElement('div'); av.className='ans-val';
  q.answer.forEach(function(s){ if(s.m) av.appendChild(texEl(s.m,false)); else renderRich(av, s.t); });
  secAns.appendChild(av);
  if(testMode){
    var g=document.createElement('div'); g.className='grade';
    var gl=document.createElement('span'); gl.className='gl'; gl.textContent='自我評量：'; g.appendChild(gl);
    var ok=document.createElement('button'); ok.className='gbtn ok'; ok.textContent='✔ 我答對了';
    var no=document.createElement('button'); no.className='gbtn no'; no.textContent='✘ 我答錯了 → 加入複習清單';
    var gm=document.createElement('span'); gm.className='gmsg';
    ok.onclick=function(){ done[qid(q)]=true; saveDone(); cb.checked=true; card.style.opacity='.55';
      if(star[qid(q)]){ delete star[qid(q)]; saveStar(); setStar(); }
      gm.style.color='#2e7d46'; gm.textContent='　已標記「已複習」✓'; };
    no.onclick=function(){ star[qid(q)]=true; saveStar(); setStar();
      gm.style.color='#b23b3b'; gm.textContent='　已加入複習清單 ★'; };
    g.appendChild(ok); g.appendChild(no); g.appendChild(gm); secAns.appendChild(g);
  }
  order.push(secAns);

  R.appendChild(secKey); R.appendChild(secKd);
  order.slice(2,-1).forEach(function(s){ R.appendChild(s); });
  R.appendChild(secAns);
  card._order=order; card._ri=0;

  var next=mk('下一步提示 ▸','primary next-btn');
  next.onclick=function(){ if(card._ri<card._order.length){ showSec(card._order[card._ri]); card._ri++; }
    if(card._ri>=card._order.length){ next.disabled=true; next.textContent='已全部顯示 ✓'; }
    else if(card._ri>=2){ next.textContent='下一步 ▸（'+(card._ri-1)+'/'+(card._order.length-2)+'）'; } };
  bar.appendChild(next);
  bar.appendChild(tog('💡 關鍵',secKey)); bar.appendChild(tog('📍 核心概念',secKd));
  var all=mk('📝 展開全部詳解','all-btn');
  function setAllOpen(open){
    if(open){ all.textContent='🔼 收合詳解'; all.dataset.open='1'; }
    else { all.textContent='📝 展開全部詳解'; delete all.dataset.open; }
  }
  card._setAllOpen=setAllOpen;
  all.onclick=function(){
    if(all.dataset.open==='1'){
      card._order.forEach(function(s){ s.classList.remove('show'); });
      card._ri=0; next.disabled=false; next.textContent='下一步提示 ▸'; setAllOpen(false);
    } else {
      card._order.forEach(showSec); card._ri=card._order.length;
      next.disabled=true; next.textContent='已全部顯示 ✓'; setAllOpen(true);
    }
  };
  bar.appendChild(all); bar.appendChild(tog('✅ 答案',secAns));
  return card;

  function mk(t,c){ var b=document.createElement('button'); b.className='rbtn '+(c||''); b.textContent=t; return b; }
  function tog(t,target){ var b=mk(t,''); b.onclick=function(){ if(target.classList.contains('show')) target.classList.remove('show'); else showSec(target); }; return b; }
}

/* ---------- mode nav + contextual toolbar ---------- */
function renderModeNav(){
  var nav=document.getElementById('modeNav'); nav.innerHTML='';
  var home=document.createElement('a'); home.className='sitehome'; home.href='../';
  home.title='回 mathmap 數學教材網總入口'; home.textContent='🏠 網站首頁';
  nav.appendChild(home);
  var subjWrap=document.createElement('div'); subjWrap.className='subjtoggle';
  ['A','B'].forEach(function(s){
    var b=document.createElement('button'); b.textContent='數學'+s; if(state.subject===s) b.className='active';
    b.onclick=function(){ if(state.subject===s) return; state.subject=s; localStorage.setItem(LS_SUBJ,s);
      state.tUnit=''; state.tKp=''; state.unit=''; render(); window.scrollTo(0,0); };
    subjWrap.appendChild(b);
  });
  nav.appendChild(subjWrap);
  var sc=starCount();
  [['home','📋 總覽'],['year','📅 按年度'],['topic','🎯 按核心概念'],['hard','🔥 難題集'],['list','📌 複習清單'+(sc?'（'+sc+'）':'')]].forEach(function(m){
    var b=document.createElement('button'); b.textContent=m[1]; if(state.view===m[0]) b.className='active';
    b.onclick=function(){ state.view=m[0]; render(); window.scrollTo(0,0); };
    nav.appendChild(b);
  });
  var t=document.createElement('button'); t.className='testbtn'+(testMode?' on':'');
  t.textContent=testMode?'✍️ 自我測驗：開':'✍️ 自我測驗：關';
  t.title='開啟後，展開「答案」時會出現自我評量：答對自動標記已複習，答錯自動加入複習清單';
  t.onclick=function(){ testMode=!testMode; localStorage.setItem(LS_TEST, testMode?'1':'0'); render(); };
  nav.appendChild(t);
}
function renderCtx(){
  var bar=document.getElementById('ctxbar'); var tb=document.querySelector('.toolbar'); bar.innerHTML='';
  if(state.view!=='year' && state.view!=='topic'){ tb.style.display='none'; return; }
  tb.style.display='';
  if(state.view==='year'){
    var years=el('div','years');
    YEARS.forEach(function(y){ var b=document.createElement('button'); b.textContent=y+' 年'; if(y===state.year) b.className='active';
      b.onclick=function(){ state.year=y; render(); }; years.appendChild(b); });
    bar.appendChild(years);
    var filters=el('div','filters');
    var ul=el('label',null,'單元'); var usel=document.createElement('select'); usel.innerHTML='<option value="">全部單元</option>';
    unitsSorted().forEach(function(u){ var o=document.createElement('option'); o.value=u; o.textContent=u; if(u===state.unit) o.selected=true; usel.appendChild(o); });
    usel.onchange=function(){ state.unit=usel.value; render(); }; ul.appendChild(usel); filters.appendChild(ul);
    var dl=el('label',null,'難度'); var dsel=document.createElement('select');
    dsel.innerHTML='<option value="">全部難度</option><option value="hard">難（&lt;20%）</option><option value="mid">中（20–50%）</option><option value="easy">易（&gt;50%）</option>';
    dsel.value=state.diff; dsel.onchange=function(){ state.diff=dsel.value; render(); }; dl.appendChild(dsel); filters.appendChild(dl);
    var rb=el('button','ghost-btn','全部收合'); rb.onclick=resetAllReveal; filters.appendChild(rb);
    bar.appendChild(filters);
  } else if(state.view==='topic'){
    var wrap=el('div','topicnav');
    var chips=el('div','unitchips');
    UNIT_ORDER.forEach(function(u){
      var n=byUnit[u]?byUnit[u].qs.length:0;
      var c=el('button','uchip'+(state.tUnit===u?' active':'')+(n?'':' off'));
      c.innerHTML=u+'<span class="c">'+n+'</span>';
      c.onclick=function(){ state.tUnit=u; state.tKp=''; render(); }; chips.appendChild(c);
    });
    wrap.appendChild(chips); bar.appendChild(wrap);
  }
}

/* ---------- views ---------- */
function statCard(n,l,cls){ var s=el('div','stat'+(cls?' '+cls:'')); s.innerHTML='<div class="n">'+n+'</div><div class="l">'+l+'</div>'; return s; }
function bigBtn(t,d,fn){ var b=el('button','bigbtn'); b.innerHTML='<div class="t">'+t+'</div><div class="d">'+d+'</div>'; b.onclick=fn; return b; }

function renderHome(app){
  var dash=el('div','dash');
  dash.appendChild(el('h2',null,'學測數學 '+state.subject+' · 111–115 互動詳解'));
  dash.appendChild(el('p','lead','5 個學年度、'+SUBJ.length+' 題完整詳解，附大考中心答對率與 mathmap 核心概念對應。選擇下面的方式開始複習。'));

  var doneCount=SUBJ.filter(function(q){ return done[qid(q)]; }).length;
  var stats=el('div','statgrid');
  stats.appendChild(statCard(SUBJ.length,'總題數（111–115）'));
  stats.appendChild(statCard(YEARS.length+' 年','涵蓋學年度'));
  stats.appendChild(statCard(coveredKp()+' / 58','已觸及核心概念'));
  stats.appendChild(statCard(doneCount,'已複習題數','progress'));
  dash.appendChild(stats);

  var dc={easy:0,mid:0,hard:0,none:0}; SUBJ.forEach(function(q){ dc[diffOf(q)]++; });
  var p1=el('div','panel'); p1.appendChild(el('h3',null,'難度分布（依大考中心答對率）'));
  var db=el('div','diffbar');
  ['easy','mid','hard','none'].forEach(function(k){ var s=document.createElement('span'); s.className='diff-'+k; s.style.flex=dc[k]||0.0001; s.textContent=dc[k]; db.appendChild(s); });
  p1.appendChild(db);
  var lg=el('div','difflegend');
  lg.innerHTML=[['easy','易（>50%）'],['mid','中（20–50%）'],['hard','難（<20%）'],['none','非選（無答對率）']]
    .map(function(d){ return '<span><i class="diff-'+d[0]+'"></i>'+d[1]+'　'+dc[d[0]]+' 題</span>'; }).join('');
  p1.appendChild(lg); dash.appendChild(p1);

  var p2=el('div','panel'); p2.appendChild(el('h3',null,'單元涵蓋（點單元即可跨年度複習）'));
  var us=unitsSorted(); var max=Math.max.apply(null,us.map(function(u){ return byUnit[u].qs.length; }));
  var heat=el('div','heat');
  us.forEach(function(u){ var n=byUnit[u].qs.length; var row=el('div','heatrow');
    row.innerHTML='<div class="hname">'+u+'</div><div class="hbar"><i style="width:'+(n/max*100).toFixed(1)+'%"></i></div><div class="hn">'+n+' 題</div>';
    row.onclick=function(){ state.view='topic'; state.tUnit=u; state.tKp=''; render(); window.scrollTo(0,0); };
    heat.appendChild(row); });
  p2.appendChild(heat);
  p2.appendChild(el('p','tiny','＊一題可能同時對應多個單元，故各單元題數合計大於 100。','tiny'));
  dash.appendChild(p2);

  dash.appendChild(el('div','sub-h','選擇複習方式'));
  var bb=el('div','bigbtns');
  bb.appendChild(bigBtn('📅 按年度瀏覽','逐年 20 題，像做整份考卷一樣依序複習與檢討。',function(){ state.view='year'; render(); window.scrollTo(0,0); }));
  bb.appendChild(bigBtn('🎯 按核心概念複習','選單元／核心概念，跨 5 年集中攻略同一類題目，並可連到 mathmap 核心概念地圖。',function(){ state.view='topic'; render(); window.scrollTo(0,0); }));
  bb.appendChild(bigBtn('🔥 挑戰難題集','歷屆答對率最低（<20%）的題目，由難到易排序，適合考前衝刺。',function(){ state.view='hard'; state.hardBand='hard'; render(); window.scrollTo(0,0); }));
  bb.appendChild(bigBtn('📌 我的複習清單','收藏想再看的題目與錯題，集中複習'+(starCount()?'（目前 '+starCount()+' 題）':'。'),function(){ state.view='list'; render(); window.scrollTo(0,0); }));
  dash.appendChild(bb);
  dash.appendChild(el('p','tiny','小提醒：右上角可開啟「✍️ 自我測驗模式」——先自己作答，再展開答案自評對錯；答錯的題會自動進入複習清單。'));
  app.appendChild(dash);
}

function renderYear(app){
  var list=SUBJ.filter(function(q){
    if(q.year!==state.year) return false;
    if(state.unit && !q.kaodian.some(function(k){ return k.unit===state.unit; })) return false;
    if(state.diff){ var d=diffOf(q); if(d!==state.diff) return false; }
    return true;
  }).sort(function(a,b){ return a.num-b.num; });
  var note=el('div','count-note');
  note.textContent=state.year+' 學年度 · 共 '+list.length+' 題'+(state.unit?('　·　'+state.unit):'')+(state.diff?'　·　依難度篩選':'');
  app.appendChild(note);
  if(!list.length){ app.appendChild(el('div','empty','此條件下沒有題目')); return; }
  var frag=document.createDocumentFragment();
  list.forEach(function(q){ frag.appendChild(makeCard(q)); });
  app.appendChild(frag);
  if(/open=1/.test(location.search)){ var cs=app.querySelectorAll('.qcard'); for(var i=0;i<2 && i<cs.length;i++){ cs[i]._order.forEach(showSec); cs[i]._ri=cs[i]._order.length; if(cs[i]._setAllOpen) cs[i]._setAllOpen(true); var nb=cs[i].querySelector('.next-btn'); if(nb){ nb.disabled=true; nb.textContent='已全部顯示 ✓'; } } }
}

function renderTopic(app){
  if(!state.tUnit){ app.appendChild(el('div','empty','請從上方選擇一個單元，開始跨年度的核心概念複習。')); return; }
  var u=byUnit[state.tUnit]||{qs:[],kps:{},korder:[]};
  var kwrap=el('div','kpchips2'); kwrap.style.margin='16px 0 4px';
  var allc=el('button','kpc'+(state.tKp===''?' active':'')); allc.innerHTML='全部<span class="c">'+u.qs.length+'</span>';
  allc.onclick=function(){ state.tKp=''; render(); }; kwrap.appendChild(allc);
  u.korder.slice().sort(function(a,b){ return anchorNum(u.kps[a].url)-anchorNum(u.kps[b].url); }).forEach(function(t){
    var kp=u.kps[t]; var c=el('button','kpc'+(state.tKp===t?' active':'')); c.innerHTML=kp.title+'<span class="c">'+kp.qs.length+'</span>';
    c.onclick=function(){ state.tKp=t; render(); }; kwrap.appendChild(c);
  });
  /* 未出題／課綱不含的核心概念：灰色籌碼，點了連到重點整理對應段落 */
  (KP_ALL[state.tUnit]||[]).forEach(function(pair){
    var a=pair[0], t=pair[1];
    if(u.kps[a]) return;
    var ex = state.subject==='B' && B_EXCLUDED[state.tUnit] && B_EXCLUDED[state.tUnit][a];
    var lab = ex ? '數B課綱不含' : '近五年未出題';
    var c=el('a','kpc off'); c.href='../concept-map/115學測數學_'+state.tUnit+'.html#'+a;
    c.target='_blank'; c.rel='noopener';
    c.title = ex ? '108 課綱數B不含此核心概念，可安心跳過' : '課綱範圍內，111–115 未出過題——不代表不會考；點我到重點整理複習';
    c.innerHTML=t+'<span class="c">'+lab+'</span>';
    kwrap.appendChild(c);
  });
  app.appendChild(kwrap);

  var head=el('div','topichead'); var list;
  if(state.tKp){ var kpo=u.kps[state.tKp]; list=kpo.qs.slice();
    head.innerHTML='<span class="th">'+state.tUnit+'　'+kpo.title+'</span> <a class="maplink" href="'+kpo.url+'" target="_blank" rel="noopener">🔗 到 mathmap 核心概念地圖</a><div class="ts">共 '+list.length+' 題（跨 111–115）</div>';
  } else { list=u.qs.slice();
    head.innerHTML='<span class="th">'+state.tUnit+'</span><div class="ts">此單元共 '+list.length+' 題　·　'+u.korder.length+' 個核心概念</div>';
  }
  var rb=el('button','ghost-btn','全部收合'); rb.style.marginLeft='10px'; rb.onclick=resetAllReveal; head.appendChild(rb);
  app.appendChild(head);

  list.sort(function(a,b){ if(a.year!==b.year) return (+b.year)-(+a.year); return a.num-b.num; });
  var frag=document.createDocumentFragment();
  list.forEach(function(q){ frag.appendChild(makeCard(q)); });
  app.appendChild(frag);
}

function renderHard(app){
  var bands=[['hard','難（答對率 &lt;20%）'],['mid','中（20–50%）']];
  var chips=el('div','kpchips2'); chips.style.margin='16px 0 4px';
  bands.forEach(function(b){ var n=SUBJ.filter(function(q){ return diffOf(q)===b[0]; }).length;
    var c=el('button','kpc'+(state.hardBand===b[0]?' active':'')); c.innerHTML=b[1]+'<span class="c">'+n+'</span>';
    c.onclick=function(){ state.hardBand=b[0]; render(); }; chips.appendChild(c); });
  app.appendChild(chips);
  var list=SUBJ.filter(function(q){ return diffOf(q)===state.hardBand; })
    .sort(function(a,b){ var ra=rateNum(a.rate), rb=rateNum(b.rate); if(ra!==rb) return ra-rb; if(a.year!==b.year) return (+b.year)-(+a.year); return a.num-b.num; });
  var head=el('div','topichead');
  head.innerHTML='<span class="th">'+(state.hardBand==='hard'?'🔥 歷屆難題集':'中難度題組')+'</span><div class="ts">'+(state.hardBand==='hard'?'答對率低於 20%':'答對率 20–50%')+'　·　共 '+list.length+' 題，由難到易排序（跨 111–115）</div>';
  var rb=el('button','ghost-btn','全部收合'); rb.style.marginLeft='10px'; rb.onclick=resetAllReveal; head.appendChild(rb);
  app.appendChild(head);
  var frag=document.createDocumentFragment(); list.forEach(function(q){ frag.appendChild(makeCard(q)); }); app.appendChild(frag);
}

function renderList(app){
  var list=SUBJ.filter(function(q){ return star[qid(q)]; }).sort(function(a,b){ if(a.year!==b.year) return (+b.year)-(+a.year); return a.num-b.num; });
  var head=el('div','topichead');
  head.innerHTML='<span class="th">📌 我的複習清單</span><div class="ts">你標記為「要複習／錯題」的題目，共 '+list.length+' 題</div>';
  if(list.length){ var rb=el('button','ghost-btn','全部收合'); rb.style.marginLeft='10px'; rb.onclick=resetAllReveal; head.appendChild(rb); }
  app.appendChild(head);
  if(!list.length){ app.appendChild(el('div','empty','清單是空的。在任何一題按「☆ 加入複習清單」，或開啟自我測驗模式、答錯時按「我答錯了」，題目就會收進這裡。')); return; }
  var frag=document.createDocumentFragment(); list.forEach(function(q){ frag.appendChild(makeCard(q)); }); app.appendChild(frag);
}

/* ---------- dispatch ---------- */
function render(){
  buildIndex();
  renderModeNav(); renderCtx();
  var app=document.getElementById('app'); app.innerHTML='';
  if(state.view==='home') return renderHome(app);
  if(state.view==='topic') return renderTopic(app);
  if(state.view==='hard') return renderHard(app);
  if(state.view==='list') return renderList(app);
  return renderYear(app);
}

/* ---------- 深層連結 ?q=<qid>：從複習講義／重點整理直接跳到某一題 ----------
   qid 格式同 qid()：數A「111-7」、數B「B111-7」（num 是全卷連續編號 1–20）。
   必須在第一次 render 前設好 state，否則預設只顯示 115 年、目標題不會被畫出來。 */
function readDeepLink(){
  var m=/[?&]q=(B?\d{3}-[0-9A-Za-z]+)/.exec(location.search);
  return m ? m[1] : '';
}
function applyDeepLink(t){
  var m=/^(B?)(\d{3})-([0-9A-Za-z]+)$/.exec(t||'');
  if(!m) return '';
  state.subject = m[1] ? 'B' : 'A';
  state.year = m[2];
  state.view = 'year';
  state.unit = ''; state.diff = '';   // 清掉篩選，否則目標題可能被濾掉
  return t;
}
/* 跳到目標題有兩個東西會把它弄丟：
     ① 瀏覽器的捲動位置還原（reload 時會把 scrollY 拉回 0，蓋掉我們的捲動）
     ② 題目截圖是 loading="lazy"，陸續載入時會把下面的內容一路往下推
   所以：先關掉捲動還原，再持續校正到「位置連續兩次不變」為止（上限 2.5 秒）。 */
function focusDeepLink(t){
  if(!t) return;
  var card=document.getElementById('q-'+t);
  if(!card) return;
  card.classList.add('deep-hit');
  function go(){ try{ card.scrollIntoView({block:'start'}); }catch(e){ card.scrollIntoView(); } }

  // 學生一旦自己動了，就別再硬拉回去（校正期間仍可能有人急著往下滑）
  var userMoved=false;
  var EVTS=['wheel','touchstart','keydown','mousedown'];
  function onUser(){ userMoved=true; stop(); }
  function stop(){ EVTS.forEach(function(e){ window.removeEventListener(e, onUser); }); }
  EVTS.forEach(function(e){ window.addEventListener(e, onUser, {passive:true}); });

  var last=-1, stable=0, tries=0;
  (function align(){
    if(userMoved){ setTimeout(fade, 0); return; }
    go();
    var abs=Math.round(card.getBoundingClientRect().top+window.scrollY);
    stable = (abs===last) ? stable+1 : 0;
    last=abs;
    if(stable>=2 || ++tries>16){                 // 穩定了、或 16×150ms 到頂就收手
      stop(); fade(); return;
    }
    setTimeout(align, 150);
  })();
  function fade(){ setTimeout(function(){ card.classList.remove('deep-hit'); }, 3200); }
}

function start(){
  var t=applyDeepLink(readDeepLink());
  if(t && 'scrollRestoration' in history){ try{ history.scrollRestoration='manual'; }catch(e){} }
  render();
  if(t) setTimeout(function(){ focusDeepLink(t); }, 0);
}
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', start);
else start();
})();
