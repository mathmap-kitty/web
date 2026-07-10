// 填空切換
  function tb(el){ el.classList.toggle('on'); }
  // 解答區塊切換
  function ts(btn){
    var sol = btn.nextElementSibling;
    var open = sol.classList.toggle('open');
    btn.classList.toggle('active', open);
    btn.textContent = open ? (btn.dataset.h || '隱藏') : (btn.dataset.s || '顯示解答');
  }
  // 全部顯示 / 隱藏
  function revealAll(){
    document.querySelectorAll('.blank').forEach(function(b){ b.classList.add('on'); });
    document.querySelectorAll('.sol').forEach(function(s){ s.classList.add('open'); });
    document.querySelectorAll('.sol-btn').forEach(function(b){ b.classList.add('active'); b.textContent=b.dataset.h||'隱藏'; });
  }
  function hideAll(){
    document.querySelectorAll('.blank').forEach(function(b){ b.classList.remove('on'); });
    document.querySelectorAll('.sol').forEach(function(s){ s.classList.remove('open'); });
    document.querySelectorAll('.sol-btn').forEach(function(b){ b.classList.remove('active'); b.textContent=b.dataset.s||'顯示解答'; });
  }
  // Part 0 直覺挑戰：點選直覺答案 → 標示正解／誤答 → 展開「為什麼」說明（只作答一次）
  function chal(btn){
    var box = btn.closest('.chal');
    if (!box || box.classList.contains('done')) return;
    box.classList.add('done');
    box.querySelectorAll('.chal-opt').forEach(function(o){
      o.disabled = true;
      if (o.dataset.ok === '1') o.classList.add('right');
    });
    if (btn.dataset.ok !== '1') btn.classList.add('wrong');
    var rv = box.querySelector('.chal-reveal');
    if (rv) rv.classList.add('open');
  }
  // 附註浮動說明：點按開關，一次只開一個，點別處關閉；並自動避免超出畫面被切到
  function tn(ev, el){
    ev.stopPropagation();
    var open = el.classList.contains('on');
    document.querySelectorAll('.note.on').forEach(function(n){
      n.classList.remove('on');
      var p = n.querySelector('.np'); if(p){ p.style.left=''; }
    });
    if(!open){
      el.classList.add('on');
      var np = el.querySelector('.np');
      if(np){
        np.style.left = '0px';
        var m = 8, r = np.getBoundingClientRect();
        if(r.right > window.innerWidth - m){ np.style.left = (-(r.right - (window.innerWidth - m))) + 'px'; }
        r = np.getBoundingClientRect();
        if(r.left < m){ np.style.left = ((parseFloat(np.style.left)||0) + (m - r.left)) + 'px'; }
      }
    }
  }
  // 點在附註以外的地方才關閉（避免和開啟的點擊互相打架）
  document.addEventListener('click', function(e){
    if (e.target.closest && e.target.closest('.note')) return;
    document.querySelectorAll('.note.on').forEach(function(n){ n.classList.remove('on'); });
  });
  // KaTeX 渲染（含隱藏內容；失敗也不影響頁面）
  function renderMath(){
    try{
      if (window.renderMathInElement){
        renderMathInElement(document.body, {
          delimiters: [
            {left:'\\(', right:'\\)', display:false},
            {left:'\\[', right:'\\]', display:true}
          ],
          throwOnError:false
        });
      }
    }catch(e){}
  }
  if (document.readyState !== 'loading') renderMath();
  else document.addEventListener('DOMContentLoaded', renderMath);
