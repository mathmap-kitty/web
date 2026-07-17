// 填空切換（D5：漸進渲染期間，展開前先補渲染所在區塊）
  function tb(el){
    if (typeof ensureMath === 'function') ensureMath(el);
    el.classList.toggle('on');
  }
  // 解答區塊切換
  function ts(btn){
    var sol = btn.nextElementSibling;
    if (typeof ensureMath === 'function') ensureMath(sol);
    var open = sol.classList.toggle('open');
    btn.classList.toggle('active', open);
    btn.textContent = open ? (btn.dataset.h || '隱藏') : (btn.dataset.s || '顯示解答');
  }
  // D5-D 全部顯示／隱藏：分段切換（每批 120 個、間隔 30ms），
  // 避免一次觸發全頁（2～5 萬節點）的樣式重排造成長時間凍結；新操作會取代進行中的舊操作。
  var _mmStageTok = 0;
  function _stageToggle(on){
    var tok = ++_mmStageTok;
    document.querySelectorAll('.sol-btn').forEach(function(b){
      b.classList.toggle('active', on);
      b.textContent = on ? (b.dataset.h || '隱藏') : (b.dataset.s || '顯示解答');
    });
    var els = Array.prototype.slice.call(document.querySelectorAll('.blank, .sol'));
    var i = 0, B = 120;
    (function step(){
      if (tok !== _mmStageTok) return;
      var end = Math.min(i + B, els.length);
      for (; i < end; i++){
        var el = els[i];
        if (on && typeof ensureMath === 'function' && el.classList.contains('sol')) ensureMath(el);
        if (el.classList.contains('blank')) el.classList.toggle('on', on);
        else el.classList.toggle('open', on);
      }
      if (i < els.length) setTimeout(step, 30);
    })();
  }
  function revealAll(){ _stageToggle(true); }
  function hideAll(){ _stageToggle(false); }
  // B2 置頂工具列瘦身：下捲收合成單排、上捲或點擊展開；
  // 錨點跳轉一律先收合再 scrollIntoView 重新定位，讓 scroll-margin-top:64px 兩態都不遮字
  (function(){
    var tb = document.querySelector('.toolbar');
    if (!tb) return;
    var lastY = window.pageYOffset, lock = 0;
    function setMin(on){ tb.classList.toggle('min', on); }
    window.addEventListener('scroll', function(){
      var y = window.pageYOffset;
      if (Date.now() < lock) { lastY = y; return; }  // 程式跳轉中：維持收合
      if (y < 40) setMin(false);
      else if (y > lastY + 6) setMin(true);
      else if (y < lastY - 6) setMin(false);
      lastY = y;
    }, {passive: true});
    tb.addEventListener('click', function(){
      if (tb.classList.contains('min')) setMin(false);
    });
    function jumpFix(){
      var id = location.hash.slice(1);
      var el = id && document.getElementById(id);
      if (!el) return;
      setMin(true); lock = Date.now() + 900;
      requestAnimationFrame(function(){ el.scrollIntoView(); });
    }
    window.addEventListener('hashchange', jumpFix);
    if (location.hash) {
      if (document.readyState === 'loading')
        document.addEventListener('DOMContentLoaded', jumpFix);
      else jumpFix();
    }
  })();
  // Part 0 直覺挑戰：點選直覺答案 → 標示正解／誤答 → 展開「為什麼」說明（只作答一次）
  function chal(btn){
    var box = btn.closest('.chal');
    if (!box || box.classList.contains('done')) return;
    if (typeof ensureMath === 'function') ensureMath(box);
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
  // D5-A KaTeX 分塊漸進渲染：不再一次鎖住主執行緒渲染整頁；
  // 由上而下分塊、用閒置時間逐塊完成——最終仍「全頁渲染完」，維持既有
  // 「隱藏內容先渲染、之後只切換顯示」的慣例（blank/sol/練習模式零改動）。
  var _mmOpts = {delimiters: [
      {left:'\\(', right:'\\)', display:false},
      {left:'\\[', right:'\\]', display:true}], throwOnError:false};
  var _mmPend = [];  // 尚未渲染的分塊（DOM 順序）
  function _mmChunks(){
    // 分塊單位：各 .card 的直接子元素（教學內容都在卡片裡）＋其餘 body 頂層元素
    var list = [];
    Array.prototype.forEach.call(document.body.children, function(top){
      if (top.classList && top.classList.contains('card') && top.children.length)
        Array.prototype.push.apply(list, top.children);
      else list.push(top);
    });
    return list;
  }
  function ensureMath(root){
    // 立刻補渲染與 root 相關（包含或被包含）的待渲染分塊——互動永遠看得到成品
    if (!window.renderMathInElement || !_mmPend.length || !root) return;
    for (var i = _mmPend.length - 1; i >= 0; i--){
      var el = _mmPend[i];
      if (el === root || (root.contains && root.contains(el)) || (el.contains && el.contains(root))){
        _mmPend.splice(i, 1);
        try{ renderMathInElement(el, _mmOpts); }catch(e){}
      }
    }
  }
  function renderMath(){
    if (!window.renderMathInElement) return;
    _mmPend = _mmChunks();
    // 帶錨點進頁：先渲染目標區塊，跳過去不會看到未渲染的原始碼
    if (location.hash){
      var t = document.getElementById(location.hash.slice(1));
      if (t) ensureMath(t);
    }
    // 排程雙保險：優先用閒置時間（rIC），但背景分頁／省電模式會餓死 rIC，
    // 故同時掛 setTimeout 賽跑（先到先跑、只跑一次）——保證最慢每 250ms 前進一批
    function schedule(fn){
      var done = false;
      function run(){ if (done) return; done = true; fn(); }
      if (window.requestIdleCallback) requestIdleCallback(run, {timeout: 250});
      setTimeout(run, 250);
    }
    (function pump(){
      if (!_mmPend.length) return;
      schedule(function(){
        var t0 = performance.now();
        while (_mmPend.length && performance.now() - t0 < 12){
          var el = _mmPend.shift();
          try{ renderMathInElement(el, _mmOpts); }catch(e){}
        }
        pump();
      });
    })();
  }
  if (document.readyState !== 'loading') renderMath();
  else document.addEventListener('DOMContentLoaded', renderMath);
