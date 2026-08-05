# -*- coding: utf-8 -*-
"""單一來源 (YAML) -> 互動學習網頁（單一 HTML，內嵌 CSS/JS，KaTeX 由 CDN 載入）。

視覺與既有矩陣頁一致：CSS/JS 直接重用 build/assets/。
"""
import os
import io
import re
import sys
import json
from urllib.parse import quote
# 確保 content/ 在 path 上（讓 units／cues／checks 可匯入），不論由哪個生成器匯入本模組
_CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")
if _CONTENT_DIR not in sys.path:
    sys.path.insert(0, _CONTENT_DIR)
from render import html_rich
try:
    from cues import CUES, GROUPS  # 解題線索＋「同一招」群組（單一來源；同餵地圖頁與各考點標籤）
except Exception:
    CUES, GROUPS = [], {}
try:
    from checks import CHECKS  # 考點「確認理解」概念小測（單一來源）
except Exception:
    CHECKS = {}
try:
    from part2_kp import PART2_KP  # Part2 各題→對應考點（錯題導回考點複習）
except Exception:
    PART2_KP = {}
try:
    from exam_rates import RATES as EXAM_RATES  # 考點×大考中心答對率（build/gen_examrates.py 產生）
except Exception:
    EXAM_RATES = {}
try:
    from units import UNITS as _UNITS  # 單元中繼資料（檔名／emoji／title），供跨單元連結
    _BY_SLUG = {u["slug"]: u for u in _UNITS}
except Exception:
    _BY_SLUG = {}
_CUES_BY_KP = {}
for _c in CUES:
    _CUES_BY_KP.setdefault((_c["unit"], _c["kp"]), []).append(_c)
CLUEMAP_FILE = "115學測數學_解題線索地圖.html"

_KP_NAV_CACHE = {}


def _kp_nav(slug, kpid):
    """惰性查某單元某考點的 nav 名稱（供觸類旁通跨單元連結顯示）。"""
    if slug not in _KP_NAV_CACHE:
        try:
            _u = __import__(slug).UNIT
            _KP_NAV_CACHE[slug] = {k["id"]: k.get("nav", k.get("title", "")) for k in _u["kps"]}
        except Exception:
            _KP_NAV_CACHE[slug] = {}
    return _KP_NAV_CACHE[slug].get(kpid, "")

HERE = os.path.dirname(os.path.abspath(__file__))
KATEX = "katex"  # 本地離線包（0.16.11，與 exam 同源；含 contrib/auto-render），不再走 CDN

# 已讀進度（考點層，localStorage 鍵 mm-read-kps，格式 "slug:kpN"，與概念地圖共用）
# 掌握度（理解確認，localStorage 鍵 mm-kp-mastery，值 "ok"／"review"）：每考點的「確認理解」互動。
PROGRESS_JS = (
    "var RK='mm-read-kps',MK='mm-kp-mastery';"
    "function gR(){try{return new Set(JSON.parse(localStorage.getItem(RK)||'[]'))}catch(e){return new Set()}}"
    "function gM(){try{return JSON.parse(localStorage.getItem(MK)||'{}')}catch(e){return {}}}"
    # 記錄「上次讀到哪」：首頁『繼續上次進度』用（鍵 mm-last＝{slug,file,title,kp}）
    "function setLast(kp){try{var h=document.querySelector('.hero h1');"
    "localStorage.setItem('mm-last',JSON.stringify({slug:MMSLUG,"
    "file:decodeURIComponent(location.pathname.split('/').pop()),"
    "title:h?h.textContent:document.title,kp:kp||''}));}catch(e){}}"
    "function kpToggle(b){var k=MMSLUG+':'+b.dataset.kp;var s=gR();var on=!s.has(k);on?s.add(k):s.delete(k);"
    "localStorage.setItem(RK,JSON.stringify([...s]));setLast(b.dataset.kp);upUnit();}"
    "function upUnit(){var s=gR();var done=MMKPS.filter(k=>s.has(MMSLUG+':'+k)).length,t=MMKPS.length;"
    "document.querySelectorAll('.kpchk').forEach(b=>b.classList.toggle('on',s.has(MMSLUG+':'+b.dataset.kp)));"
    "var tx=document.getElementById('up-txt');if(tx)tx.textContent=done+' / '+t;"
    "var bar=document.getElementById('up-bar');if(bar)bar.style.width=(t?done/t*100:0)+'%';}"
    "function markAllKp(){var s=gR();var all=MMKPS.every(k=>s.has(MMSLUG+':'+k));"
    "MMKPS.forEach(k=>{var key=MMSLUG+':'+k;all?s.delete(key):s.add(key);});"
    "localStorage.setItem(RK,JSON.stringify([...s]));upUnit();}"
    # 設定某考點掌握度：'ok'＝我懂了（同步標已讀）、'review'＝待複習；再點同一鈕可取消。
    "function kpMastery(kp,st,force){var o=gM(),key=MMSLUG+':'+kp;"
    "if(o[key]===st&&!force){delete o[key];}else{o[key]=st;}"
    "localStorage.setItem(MK,JSON.stringify(o));"
    "if(o[key]==='ok'){var s=gR();s.add(MMSLUG+':'+kp);localStorage.setItem(RK,JSON.stringify([...s]));}"
    "setLast(kp);upMastery();upUnit();}"
    "function upMastery(){var o=gM(),ok=0,rv=0;MMKPS.forEach(function(k){var v=o[MMSLUG+':'+k];"
    "if(v==='ok')ok++;else if(v==='review')rv++;});"
    "document.querySelectorAll('.kpcheck').forEach(function(b){var v=o[MMSLUG+':'+b.dataset.kp]||'';"
    "b.classList.toggle('is-ok',v==='ok');b.classList.toggle('is-rv',v==='review');"
    "var ok0=b.querySelector('.kc-ok'),rv0=b.querySelector('.kc-rv');"
    "if(ok0)ok0.classList.toggle('on',v==='ok');if(rv0)rv0.classList.toggle('on',v==='review');});"
    "document.querySelectorAll('.kp-mastery').forEach(function(e){var v=o[MMSLUG+':'+e.dataset.kp]||'';"
    "e.textContent=v==='ok'?'✓ 已理解':(v==='review'?'⚠ 待複習':'');e.className='kp-mastery '+v;});"
    "var mt=document.getElementById('mst-txt');if(mt)mt.textContent=ok;"
    "var rv2=document.getElementById('mst-rv');if(rv2)rv2.textContent=rv;"
    "var mb=document.getElementById('mst-bar');if(mb)mb.style.width=(MMKPS.length?ok/MMKPS.length*100:0)+'%';"
    "var jp=document.getElementById('mst-jump');if(jp)jp.style.display=rv?'':'none';}"
    "function jumpReview(){var o=gM();for(var i=0;i<MMKPS.length;i++){"
    "if(o[MMSLUG+':'+MMKPS[i]]==='review'){location.hash=MMKPS[i];return;}}}"
    # 一進單元頁就記錄為「上次位置」（若網址帶 #kpN 則連考點一起記）
    "setLast((location.hash||'').replace('#',''));"
    "upUnit();upMastery();")


# 入口診斷（方案 B）：只判斷「第一步從哪個抽屜切入」，不要求算答案。
# 互動慣例與 B1 直覺挑戰一致：點選 → 即時對錯 → 展開一句話說明 → 錨點回考點。
# 作答後鎖定該題（避免亂點湊對），答對數即時累計。
ENTRYDIAG_JS = (
    "function edPick(b){var c=b.closest('.edcard');if(!c||c.classList.contains('done'))return;"
    "c.classList.add('done');"
    "var ok=b.dataset.ok==='1';b.classList.add(ok?'right':'wrong');"
    "if(!ok){var t=c.querySelector('.ed-opt[data-ok=\"1\"]');if(t)t.classList.add('right');}"
    "c.classList.add(ok?'is-ok':'is-no');"
    "c.querySelectorAll('.ed-opt').forEach(function(x){x.disabled=true;});"
    "var n=document.getElementById('ed-ok');"
    "if(n)n.textContent=document.querySelectorAll('.edcard.is-ok').length;"
    "var fb=c.querySelector('.ed-fb');"
    "if(fb&&typeof ensureMath==='function')ensureMath(fb);}")


# 路線選擇器（方案 A）：把 Part 1 的考點卡依路線篩選／重排。
#   完整複習  ＝ 全部顯示、恢復原順序
#   先拿基本分＝ 只留 3★ 高頻考點，並依官方答對率由高到低排（難的排後面）
#   錯題回補  ＝ 只留自評／小測判定為「待複習」的考點
# 選擇存 localStorage（鍵 mm-route），跨單元沿用——學生選一次就好。
# 不另外包容器：考點卡是 .wrap 的連續兄弟節點，直接在原位重排，
# 避免動到 app.js 依 DOM 層級做的分塊渲染。
ROUTE_JS = (
    "var RTK='mm-route',_rtCards=null,_rtAnchor=null,_rtParent=null;"
    "function _rtInit(){var c=[].slice.call(document.querySelectorAll('.card[data-freq]'));"
    "if(!c.length)return false;_rtCards=c;_rtParent=c[0].parentNode;"
    "_rtAnchor=c[c.length-1].nextSibling;return true;}"
    "function _rtRate(el){var v=el.getAttribute('data-rate');return v===null?-1:+v;}"
    "function setRoute(r,quiet){"
    "if(!_rtCards&&!_rtInit())return;"
    "var m=gM(),show=[],hidden=0;"
    "if(r==='basic'){"
    "show=_rtCards.filter(function(e){return +e.dataset.freq>=3;});"
    # 難的排後面：有答對率的由高到低；沒有官方資料的排最後（不臆測它的難易）
    "show.sort(function(a,b){return _rtRate(b)-_rtRate(a);});"
    "}else if(r==='review'){"
    "show=_rtCards.filter(function(e){return m[MMSLUG+':'+e.id]==='review';});"
    "}else{r='all';show=_rtCards.slice();}"
    "hidden=_rtCards.length-show.length;"
    "_rtCards.forEach(function(e){e.style.display='none';});"
    "show.forEach(function(e){e.style.display='';_rtParent.insertBefore(e,_rtAnchor);});"
    "document.querySelectorAll('.rb-btn').forEach(function(b){b.classList.toggle('on',b.dataset.r===r);});"
    # 篩不到東西時一律退回全部顯示並說明——不能讓學生翻到下一個單元看到空白的 Part 1
    "if(!show.length&&r!=='all'){_rtCards.forEach(function(e){e.style.display='';"
    "_rtParent.insertBefore(e,_rtAnchor);});"
    "document.querySelectorAll('.rb-btn').forEach(function(b){b.classList.toggle('on',b.dataset.r===r);});"
    "var n0=document.getElementById('rb-note');"
    "if(n0)n0.textContent=(r==='basic')?'這個單元沒有 ★★★ 考點，已顯示全部'"
    ":'這個單元目前沒有待複習的考點，已顯示全部——在各考點末「確認理解」作答，答錯會自動標記';"
    "if(!quiet){try{localStorage.setItem(RTK,r);}catch(e){}}return;}"
    "var n=document.getElementById('rb-note');"
    "if(n){if(r==='basic'){n.textContent='只顯示 '+show.length+' 個必考核心，答對率高的排前面（其餘 '+hidden+' 個先收起來）';}"
    "else if(r==='review'){n.textContent='只顯示你標記待複習的 '+show.length+' 個考點';}"
    "else{n.textContent='';}}"
    "if(!quiet){try{localStorage.setItem(RTK,r);}catch(e){}}"
    # 篩選後版面位移，帶錨點進來的要重新對位；數學式也可能還沒渲染到
    "if(typeof ensureMath==='function')show.forEach(function(e){ensureMath(e);});"
    "}"
    "(function(){if(!_rtInit())return;var r='all';try{r=localStorage.getItem(RTK)||'all';}catch(e){}"
    # 帶 #kpN 進頁時一律走完整模式，否則目標考點可能剛好被篩掉、跳過去是空的
    "if(location.hash&&document.querySelector(location.hash+'.card'))r='all';"
    "setRoute(r,1);})();")


# ===「繼續上次進度」橫幅（首頁 index.html 內嵌一份；概念地圖／內容總覽引用下列共用常數）===
# 讀 localStorage 的 mm-last（單元頁 setLast 寫入）。放一個 id="continue-bar" 的 <a> 即可自動生效。
_F2S_JS = "{" + ",".join(f'"{u["file"]}":"{u["slug"]}"' for u in _BY_SLUG.values()) + "}"

CONTINUE_BANNER_HTML = (
    '<a id="continue-bar" class="continue" href="#" style="display:none">'
    '<span class="cont-ico">⏯</span>'
    '<span class="cont-main"><b>繼續上次進度</b><span class="cont-sub" id="cont-sub"></span></span>'
    '<span class="cont-go">前往 →</span></a>')

CONTINUE_CSS = (
    ".continue{display:flex;align-items:center;gap:12px;max-width:600px;margin:16px auto;"
    "background:linear-gradient(90deg,#8c2740,#ac4159);color:#fff;border-radius:14px;padding:12px 18px;"
    "text-decoration:none;box-shadow:0 4px 16px rgba(140,39,64,.3)}"
    ".continue:hover{filter:brightness(1.07)}"
    ".continue .cont-ico{font-size:24px;line-height:1}"
    ".continue .cont-main{display:flex;flex-direction:column;line-height:1.35;margin-right:auto;min-width:0}"
    ".continue .cont-main b{font-size:16px}"
    ".continue .cont-sub{font-size:13px;opacity:.92;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"
    ".continue .cont-go{font-weight:800;white-space:nowrap;font-size:14px}")

CONTINUE_JS = (
    "(function(){var F2S=" + _F2S_JS + ";var last;"
    "try{last=JSON.parse(localStorage.getItem('mm-last')||'null')}catch(e){last=null}"
    "var bar=document.getElementById('continue-bar');"
    "if(!bar||!last||!last.file||!F2S[last.file])return;"
    "var kp=last.kp&&/^kp\\d+$/.test(last.kp);"
    "bar.setAttribute('href',last.file+(kp?'#'+last.kp:''));"
    "var s=document.getElementById('cont-sub');"
    "if(s)s.textContent=(last.title||'')+(kp?' · 考點 '+last.kp.slice(2):'');"
    "bar.style.display='';})();")


# ===「匯出學習紀錄」摘要卡（首頁、概念地圖、內容總覽共用）===
# 讀 localStorage（mm-read-kps 已讀／mm-kp-mastery 理解確認／mm-quiz 練習成績），彙整成一張可截圖繳交的卡。
_UNITS_META = []
for _u in _BY_SLUG.values():
    try:
        _n = len(__import__(_u["slug"]).UNIT["kps"])
    except Exception:
        _n = 0
    _UNITS_META.append({"slug": _u["slug"], "e": _u.get("emoji", ""), "t": _u["title"], "n": _n})
_UNITS_META_JS = json.dumps(_UNITS_META, ensure_ascii=False)


def _plain_txt(s):
    """把含 LaTeX／markdown 的字串清成純文字（供搜尋比對／顯示）。"""
    s = re.sub(r"\\[a-zA-Z]+\b", " ", s or "")
    s = re.sub(r"[\\(){}\[\]$*_^|~]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# 站內搜尋索引：各單元「考點 nav」＋「Part3 速查表」→ 可查考點／公式關鍵字。
_SEARCH = []
for _u in _BY_SLUG.values():
    try:
        _U = __import__(_u["slug"]).UNIT
    except Exception:
        continue
    _e, _t, _f = _u.get("emoji", ""), _u["title"], _u["file"]
    for _k in _U.get("kps", []):
        _lab = _plain_txt(_k.get("nav", _k.get("title", "")))
        _SEARCH.append({"l": _lab, "u": _t, "e": _e, "f": _f, "a": _k["id"], "k": "考點",
                        "s": (_lab + " " + _t).lower()})
    for _r in (_U.get("part3") or {}).get("ref_table", []):
        _lab = _plain_txt(_r.get("k", ""))
        _det = _plain_txt(_r.get("v", ""))
        _SEARCH.append({"l": _lab, "d": _det[:44], "u": _t, "e": _e, "f": _f, "a": "part3", "k": "速查",
                        "s": (_lab + " " + _det + " " + _t).lower()})
_SEARCH_JS = json.dumps(_SEARCH, ensure_ascii=False)

EXPORT_BUTTON_HTML = ('<div class="export-wrap">'
                      '<button class="export-btn" onclick="openExport()">📤 匯出學習紀錄</button></div>')

EXPORT_MODAL_HTML = (
    '<div id="export-modal" class="ex-modal">'
    '<div class="ex-card" id="ex-card">'
    '<div class="ex-head">📊 我的學習紀錄<span class="ex-brand">學測數學重點整理</span></div>'
    '<div class="ex-meta"><label>姓名／班級：<input id="ex-name" placeholder="繳交必填"></label>'
    '<span class="ex-namehint" id="ex-namehint">← 先填寫再截圖</span>'
    '<span class="ex-date" id="ex-date"></span></div>'
    '<div class="ex-sec-t">單元完成度（已讀考點）</div>'
    '<div class="ex-rows" id="ex-rows"></div>'
    '<div class="ex-total" id="ex-total"></div>'
    '<div class="ex-stats">'
    '<div class="ex-stat"><div class="ex-k">✅ 確認理解</div><div class="ex-v" id="ex-mastery"></div></div>'
    '<div class="ex-stat"><div class="ex-k">✏️ 練習作答</div><div class="ex-v" id="ex-quiz"></div></div></div>'
    '<div class="ex-foot">自主學習佐證 · 紀錄存於本機瀏覽器 · 換裝置／清除瀏覽資料會歸零</div></div>'
    '<div class="ex-controls"><span class="ex-tip">📸 截圖上方卡片即可繳交</span>'
    '<button onclick="closeExport()">關閉</button></div></div>')

EXPORT_CSS = (
    ".export-wrap{text-align:center;margin:10px 0 4px}"
    ".export-btn{background:#fff;color:#8c2740;border:1.6px solid #8c2740;border-radius:22px;padding:8px 20px;"
    "font:inherit;font-weight:800;font-size:14.5px;cursor:pointer}"
    ".export-btn:hover{background:#8c2740;color:#fff}"
    # 頂部對齊＋可捲動（避免內容比視窗高時，垂直置中把標題推到視窗上緣又捲不上去）
    ".ex-modal{display:none;position:fixed;inset:0;z-index:4000;background:rgba(30,12,18,.74);"
    "flex-direction:column;align-items:center;justify-content:flex-start;padding:20px 16px 28px;overflow:auto;"
    "font-family:'Microsoft JhengHei','PingFang TC','Noto Sans TC','Segoe UI',system-ui,sans-serif}"
    ".ex-card{background:#fff;border-radius:18px;max-width:410px;width:100%;padding:20px 22px;flex-shrink:0;"
    "box-shadow:0 12px 48px rgba(0,0,0,.45);color:#2b2b2b;line-height:1.7}"
    ".ex-head{font-size:19px;font-weight:800;color:#8c2740;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}"
    ".ex-brand{font-size:12px;color:#9a857c;font-weight:600;margin-left:auto}"
    ".ex-meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:10px 0 14px;font-size:14px;color:#5a4a52}"
    ".ex-meta input{border:1px solid #e0cdd5;border-radius:8px;padding:4px 10px;font:inherit;font-size:14px;max-width:150px}"
    ".ex-namehint{color:#c0392b;font-size:12px;font-weight:700}"
    ".ex-namehint.hide{display:none}"
    ".ex-date{margin-left:auto;color:#8a7a72;font-size:13px}"
    ".ex-sec-t{font-weight:800;color:#6f1f33;font-size:14px;margin:4px 0 7px}"
    ".ex-rows{display:flex;flex-direction:column;gap:5px}"
    ".ex-row{display:flex;align-items:center;gap:8px;font-size:13px}"
    ".ex-u{flex:0 0 112px;color:#3a3a3a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
    ".ex-bar{flex:1;height:8px;background:#f0e0e6;border-radius:5px;overflow:hidden}"
    ".ex-bar i{display:block;height:100%;background:linear-gradient(90deg,#8c2740,#c96f88)}"
    ".ex-bar.f i{background:linear-gradient(90deg,#2e9e5b,#57c483)}"
    ".ex-n{flex:0 0 42px;text-align:right;font-weight:700;color:#8c2740}"
    ".ex-total{margin:11px 0;padding:8px 12px;background:#faf2f5;border-radius:10px;font-weight:800;"
    "color:#6f1f33;text-align:center;font-size:14px}"
    ".ex-stats{display:flex;gap:10px;flex-wrap:wrap}"
    ".ex-stat{flex:1;min-width:135px;background:#f4f9f6;border:1px solid #d6e8de;border-radius:10px;padding:8px 12px}"
    ".ex-stat .ex-k{font-size:12.5px;color:#2e6b46;font-weight:800}"
    ".ex-stat .ex-v{font-size:13.5px;color:#3a3a3a;margin-top:2px}"
    ".ex-foot{margin-top:12px;text-align:center;font-size:11px;color:#9a857c;line-height:1.5}"
    ".ex-controls{display:flex;align-items:center;gap:14px;margin-top:14px}"
    ".ex-controls button{background:#fff;color:#8c2740;border:none;border-radius:20px;padding:7px 22px;"
    "font:inherit;font-weight:800;cursor:pointer}"
    ".ex-tip{color:#fff;font-size:13px}")

EXPORT_JS = (
    "var UNITS_META=" + _UNITS_META_JS + ";"
    "function openExport(){var read,mast,quiz;"
    "try{read=new Set(JSON.parse(localStorage.getItem('mm-read-kps')||'[]'))}catch(e){read=new Set()}"
    "try{mast=JSON.parse(localStorage.getItem('mm-kp-mastery')||'{}')}catch(e){mast={}}"
    "try{quiz=JSON.parse(localStorage.getItem('mm-quiz')||'{}')}catch(e){quiz={}}"
    "var tot=0,dn=0,rows='';UNITS_META.forEach(function(m){var d=0;"
    "read.forEach(function(k){if(k.indexOf(m.slug+':kp')===0)d++;});if(d>m.n)d=m.n;tot+=m.n;dn+=d;"
    "var p=m.n?Math.round(d/m.n*100):0,full=(d>=m.n&&m.n>0);"
    "rows+='<div class=\"ex-row\"><span class=\"ex-u\">'+m.e+' '+m.t+'</span>"
    "<span class=\"ex-bar'+(full?' f':'')+'\"><i style=\"width:'+p+'%\"></i></span>"
    "<span class=\"ex-n\">'+d+'/'+m.n+'</span></div>';});"
    "var ok=0,rv=0;for(var k in mast){if(mast[k]==='ok')ok++;else if(mast[k]==='review')rv++;}"
    "var qa=0,qc=0;for(var s in quiz){qa+=quiz[s].a||0;qc+=quiz[s].c||0;}"
    "document.getElementById('ex-date').textContent=new Date().toLocaleDateString('zh-TW');"
    "document.getElementById('ex-rows').innerHTML=rows;"
    "document.getElementById('ex-total').textContent='總計 已讀 '+dn+' / '+tot+' 考點（'+(tot?Math.round(dn/tot*100):0)+'%）';"
    "document.getElementById('ex-mastery').textContent='已理解 '+ok+' 考點 · 待複習 '+rv+' 考點';"
    "document.getElementById('ex-quiz').textContent=qa?('作答 '+qa+' 題 · 答對 '+qc+' 題（正確率 '+Math.round(qc/qa*100)+'%）'):'尚未作答';"
    "document.getElementById('export-modal').style.display='flex';"
    # 防呆：姓名沒填就提示＋聚焦，填了就把提示藏起來（避免匿名繳交）
    "var nm=document.getElementById('ex-name'),nh=document.getElementById('ex-namehint');"
    "function chkNm(){if(nh)nh.classList.toggle('hide',!!(nm&&nm.value.trim()));}"
    "if(nm&&!nm._b){nm._b=1;nm.addEventListener('input',chkNm);}chkNm();"
    "if(nm&&!nm.value.trim())setTimeout(function(){try{nm.focus();}catch(e){}},120);}"
    "function closeExport(){document.getElementById('export-modal').style.display='none';}")


# === 站內搜尋框（首頁）：輸入考點名或公式關鍵字 → 即時列出結果、直達考點／速查表 ===
SEARCH_BOX_HTML = (
    '<div class="site-search">'
    '<input id="ss-q" type="search" autocomplete="off" oninput="ssSearch()" '
    'placeholder="🔍 搜尋考點或公式，例：分點公式、內積、位數、餘弦定理…">'
    '<div id="ss-results" class="ss-results"></div></div>')

SEARCH_CSS = (
    ".site-search{position:relative;max-width:600px;margin:16px auto 0}"
    ".site-search input{width:100%;padding:11px 16px;font-size:15px;font-family:inherit;"
    "border:1.6px solid #cfe0f2;border-radius:24px;background:#fff;color:#333;outline:none}"
    ".site-search input:focus{border-color:#3a5a9a;box-shadow:0 0 0 3px rgba(58,90,154,.12)}"
    ".ss-results{display:none;position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:60;"
    "background:#fff;border:1px solid #dcd0d5;border-radius:14px;box-shadow:0 8px 30px rgba(80,40,30,.18);"
    "max-height:60vh;overflow:auto;padding:5px}"
    ".ss-results.open{display:block}"
    ".ss-item{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:8px 12px;border-radius:10px;"
    "text-decoration:none;color:#333;border-bottom:1px solid #f2eaee}"
    ".ss-item:last-child{border-bottom:none}.ss-item:hover{background:#faf2f5}"
    ".ss-u{font-size:12px;color:#8c2740;background:#f6e7ec;border-radius:10px;padding:1px 8px;font-weight:700;white-space:nowrap}"
    ".ss-l{flex:1;min-width:0;font-size:14.5px;color:#3a3a3a}"
    ".ss-d{color:#9a857c;font-size:12.5px}"
    ".ss-k{font-size:11.5px;color:#3a5a9a;background:#eef4fb;border-radius:9px;padding:1px 8px;font-weight:700;white-space:nowrap}"
    ".ss-none{padding:12px 14px;color:#b06636;font-size:14px}")

SEARCH_JS = (
    "var SS=" + _SEARCH_JS + ";"
    "function ssEsc(x){return (x||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}"
    "function ssSearch(){var q=document.getElementById('ss-q').value.trim().toLowerCase(),"
    "box=document.getElementById('ss-results');"
    "if(!q){box.innerHTML='';box.classList.remove('open');return;}"
    "var hits=SS.filter(function(e){return e.s.indexOf(q)>=0;}).slice(0,20);"
    "if(!hits.length){box.innerHTML='<div class=\"ss-none\">找不到「'+ssEsc(q)+'」——換個關鍵字試試（如：距離、面積、機率）</div>';"
    "box.classList.add('open');return;}"
    "box.innerHTML=hits.map(function(e){return '<a class=\"ss-item\" href=\"'+e.f+'#'+e.a+'\">'"
    "+'<span class=\"ss-u\">'+e.e+' '+ssEsc(e.u)+'</span>'"
    "+'<span class=\"ss-l\">'+ssEsc(e.l)+(e.d?' <span class=\"ss-d\">'+ssEsc(e.d)+'</span>':'')+'</span>'"
    "+'<span class=\"ss-k\">'+e.k+'</span></a>';}).join('');box.classList.add('open');}"
    # 點結果外的地方關閉下拉
    "document.addEventListener('click',function(ev){var s=document.querySelector('.site-search');"
    "if(s&&!s.contains(ev.target)){var b=document.getElementById('ss-results');if(b)b.classList.remove('open');}});")


# 流量分析：GA4 + Microsoft Clarity，統一插在每頁 <head>，11 個單元頁全部生效。
# 之後要換或停用，只改下面兩個 ID 即可（空字串＝該段不輸出）。
GA4_ID = "G-KQVPGYJ1FK"
CLARITY_ID = "xcgidr4emy"  # Microsoft Clarity Project ID


def _analytics():
    out = []
    if GA4_ID:
        s = ('<!-- Google Analytics (GA4) -->\n'
             '<script async src="https://www.googletagmanager.com/gtag/js?id=GA4ID"></script>\n'
             '<script>window.dataLayer=window.dataLayer||[];'
             'function gtag(){dataLayer.push(arguments);}'
             "gtag('js',new Date());gtag('config','GA4ID');</script>")
        out.append(s.replace("GA4ID", GA4_ID))
    if CLARITY_ID:
        s = ('<!-- Microsoft Clarity -->\n'
             '<script type="text/javascript">'
             '(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
             't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
             'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})'
             '(window,document,"clarity","script","CLARITYID");</script>')
        out.append(s.replace("CLARITYID", CLARITY_ID))
    return ("\n".join(out) + "\n") if out else ""


ANALYTICS = _analytics()


# 社群分享卡（Open Graph + Twitter Card）：貼連結到 LINE／FB／IG 會顯示標題＋說明＋封面。
# 全站共用一張封面 og-cover.png（1200×630，放本子站 concept-map/ 根）。換網域或封面只動這三個常數。
SITE_BASE = "https://mathmap-kitty.github.io/web/concept-map/"
OG_IMAGE = SITE_BASE + "og-cover.png"
OG_SITE_NAME = "115 學測數學重點整理"

# 全站 favicon（放 repo 根；concept-map 頁面在一層深，故用 ../）。隨 og_meta() 一起輸出。
FAVICON_HTML = ('<link rel="icon" type="image/svg+xml" href="../favicon.svg">\n'
                '<link rel="apple-touch-icon" href="../apple-touch-icon.png">')

# 「🏠 網站首頁」pill：連回 repo 根的總入口 portal（../）。全站每頁頂欄共用；
# 內聯樣式蓋過各頁 topbar 的白底連結樣式，讓「離開子站」的連結有視覺區隔。
HOME_LINK = ('<a class="tb-home" href="../" style="background:rgba(255,255,255,.15);'
             'color:#fff;border:1px solid rgba(255,255,255,.5);border-radius:18px;'
             'padding:4px 12px;font-size:13px;font-weight:700;text-decoration:none;'
             'white-space:nowrap">🏠 網站首頁</a>')


def _esc_attr(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def og_meta(title, desc, page_file=""):
    """產生 Open Graph／Twitter 分享卡 meta。page_file＝該頁檔名（相對站台根），空字串＝首頁。"""
    url = SITE_BASE + quote(page_file)
    t, d = _esc_attr(title), _esc_attr(desc)
    return (f'<meta name="description" content="{d}">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="{_esc_attr(OG_SITE_NAME)}">\n'
            f'<meta property="og:locale" content="zh_TW">\n'
            f'<meta property="og:title" content="{t}">\n'
            f'<meta property="og:description" content="{d}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{OG_IMAGE}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{t}">\n'
            f'<meta name="twitter:description" content="{d}">\n'
            f'<meta name="twitter:image" content="{OG_IMAGE}">\n'
            f'{FAVICON_HTML}')

# 頁尾隱私說明（GA／Clarity 流量統計告知）＋版權列，全站一致；要改文案：這裡＋靜態檔（兩個 index、exam、404）。
PRIVACY_HTML = ('<div style="text-align:center;font-size:12px;color:#9a857c;'
                'padding:16px 14px 8px;line-height:1.7">本站使用 Google Analytics 與 '
                'Microsoft Clarity 統計匿名流量，藉以了解使用情況、持續改善內容。</div>'
                '<div style="text-align:center;font-size:12.5px;color:#9a857c;'
                'padding:0 14px 30px">mathmap 數學地圖 © Kitty</div>')


def _asset(name):
    return io.open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


def _parse_answer(sol):
    """從 solution.brief 開頭的「(N)」或「(N)(M)…」解析正解選項（1-based list）；解析不到回 None。"""
    if not sol or not sol.get("brief"):
        return None
    m = re.match(r"\s*((?:[(（]\d+[)）])+)", sol["brief"])
    if not m:
        return None
    return [int(n) for n in re.findall(r"[(（](\d+)[)）]", m.group(1))]


def _opts_html(options, answer=None):
    if not options:
        return ""
    if not answer or any(a < 1 or a > len(options) for a in answer):
        # 無可靠正解 → 維持非互動（純列出），絕不亂標
        spans = "".join(f"<span>({i}) {html_rich(o)}</span>" for i, o in enumerate(options, 1))
        return f'<div class="opts">{spans}</div>'
    multi = len(answer) > 1
    btns = "".join(
        f'<button type="button" class="opt" data-i="{i}">'
        f'<span class="opt-n">({i})</span>{html_rich(o)}</button>'
        for i, o in enumerate(options, 1))
    ck = '<button type="button" class="opt-check">對答案</button>' if multi else ""
    hint = "（多選；選好後按「對答案」）" if multi else "（點選你的答案）"
    return (f'<div class="opts quiz" data-ans="{",".join(map(str, answer))}" data-multi="{1 if multi else 0}">'
            f'<div class="opt-hint">{hint}</div>{btns}{ck}<div class="opt-fb"></div></div>')


def _table_html(tbl):
    """題目內嵌表格：{head:[...], rows:[[...],...]}。"""
    if not tbl:
        return ""
    th = "".join(f'<th style="width:auto">{html_rich(c)}</th>' for c in tbl["head"])
    trs = ""
    for r in tbl["rows"]:
        tds = "".join(f'<td class="cor">{html_rich(c)}</td>' for c in r)
        trs += f"<tr>{tds}</tr>"
    return (f'<div class="tbl-wrap"><table class="mis" style="min-width:420px">'
            f"<tr>{th}</tr>{trs}</table></div>")


def _solution_html(sol):
    if not sol:
        return ""
    parts = []
    if sol.get("brief"):
        label = sol.get("brief_label", "簡答：")
        parts.append(f'<p><span class="k">{label}</span>'
                     f'<span class="ad">{html_rich(sol["brief"])}</span></p>')
    steps = sol.get("steps", [])
    for i, st in enumerate(steps):
        if i == 0 and sol.get("steps_label", "解題關鍵："):
            parts.append(f'<p><span class="k">{sol.get("steps_label","解題關鍵：")}</span>'
                         f'{html_rich(st)}</p>')
        else:
            parts.append(f"<p>{html_rich(st)}</p>")
    return "".join(parts)


def _core_block(q, kp=""):
    """解題核心：預設收合（SOIL：先讓學生判斷題型，再點按對照）。
    沿用 sol-btn/ts() 機制（按鈕後緊接其 .sol），revealAll/hideAll 自動連動。"""
    if not q.get("core"):
        return ""
    if kp:  # 解題核心＝超連結，回上方對應考點複習
        core = (f'<a class="core corelink" href="#{kp}" title="回上方複習這個考點">'
                f'解題核心：{html_rich(q["core"])} <span class="core-go">↑ 複習考點</span></a>')
    else:
        core = f'<span class="core">解題核心：{html_rich(q["core"])}</span>'
    return ('<button class="sol-btn core-btn" data-s="🔍 先判斷：這題是哪一類？（點我對照）" '
            'data-h="收合對照" onclick="ts(this)">🔍 先判斷：這題是哪一類？（點我對照）</button>'
            f'<div class="sol core-sol">{core}</div>')


def _question_html(q, first=False, qid="", kp=""):
    meta_style = ' style="margin-top:0"' if first else ""
    meta = (f'<div class="q-meta"{meta_style}>'
            f'<span class="tag">{html_rich(q["tag"])}</span>'
            f'<span class="lv">{q["level"]}</span>{_hard_badge(q["level"])}</div>')
    body = f'<div class="q-body">{html_rich(q["body"])}{_table_html(q.get("table"))}{_opts_html(q.get("options"), _parse_answer(q.get("solution")))}</div>'
    btn = ('<button class="sol-btn" data-s="顯示解答" data-h="隱藏解答" '
           'onclick="ts(this)">顯示解答</button>')
    sol = f'<div class="sol">{_solution_html(q.get("solution"))}</div>'
    inner = meta + body + _core_block(q, kp) + btn + sol
    # 每題包一層有 id 的外框（供錯題「重測」直達原題）＋ data-kp（對應考點）
    return f'<div class="qwrap" id="{qid}" data-kp="{kp}">{inner}</div>' if qid else inner


def _subq_html(sq):
    """混合題組的子題。"""
    body = f'<div class="q-body subq"><b>{html_rich(sq["label"])}</b>{html_rich(sq.get("body",""))}</div>'
    btn = ('<button class="sol-btn" data-s="顯示解答" data-h="隱藏解答" '
           'onclick="ts(this)">顯示解答</button>')
    sol = f'<div class="sol">{_solution_html(sq.get("solution"))}</div>'
    return body + btn + sol


# 圖片放大燈箱（手機點圖看細節）：每頁一個 overlay ＋ 點任何 figure.tfig 開啟
LIGHTBOX_HTML = ('<div id="lightbox" class="lightbox" role="dialog" aria-modal="true">'
                 '<button class="lb-close" aria-label="關閉">×</button>'
                 '<div class="lb-scroll" id="lb-scroll"></div>'
                 '<div class="lb-tip">雙指可再放大 · 點背景或 × 關閉</div></div>')
LIGHTBOX_JS = (
    "(function(){var lb=document.getElementById('lightbox');if(!lb)return;"
    "var sc=document.getElementById('lb-scroll');"
    "function op(svg){sc.innerHTML='';sc.appendChild(svg.cloneNode(true));lb.classList.add('open');"
    "document.documentElement.style.overflow='hidden';sc.scrollTop=0;sc.scrollLeft=0;}"
    "function cl(){lb.classList.remove('open');sc.innerHTML='';document.documentElement.style.overflow='';}"
    "document.querySelectorAll('figure.tfig').forEach(function(f){var s=f.querySelector('svg');if(!s)return;"
    "f.addEventListener('click',function(e){e.stopPropagation();op(s);});});"
    "lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-close')||e.target.classList.contains('lb-scroll'))cl();});"
    "document.addEventListener('keydown',function(e){if(e.key==='Escape')cl();});})();")

# 練習模式：選擇題可點作答、即時批改，右下角顯示分數
QUIZ_BADGE_HTML = ('<div id="quizscore" class="quizscore" hidden>✏️ 練習　答對 '
                   '<b id="qs-c">0</b> / 作答 <b id="qs-a">0</b></div>')
QUIZ_JS = (
    "(function(){var box=document.getElementById('quizscore'),"
    "ce=document.getElementById('qs-c'),ae=document.getElementById('qs-a');var C=0,A=0;"
    "function bump(ok){A++;if(ok)C++;if(box){box.hidden=false;ce.textContent=C;ae.textContent=A;}}"
    "function num(s){return parseInt(s,10);}"
    # 練習成績持久化（供首頁『匯出學習紀錄』）：mm-quiz={slug:{a,c}}；用題序去重，重整不灌水。
    "function persistQuiz(qi,ok){if(typeof MMSLUG==='undefined')return;try{"
    "var key=MMSLUG+':q'+qi,D=JSON.parse(localStorage.getItem('mm-quiz-done')||'[]');"
    "if(D.indexOf(key)>=0)return;D.push(key);localStorage.setItem('mm-quiz-done',JSON.stringify(D));"
    "var Q=JSON.parse(localStorage.getItem('mm-quiz')||'{}'),u=Q[MMSLUG]||{a:0,c:0};u.a++;if(ok)u.c++;"
    "Q[MMSLUG]=u;localStorage.setItem('mm-quiz',JSON.stringify(Q));}catch(e){}}"
    # 錯題清單（供全站『待複習與錯題』頁）：mm-wrong={題鍵:{s單元,f檔,t題tag,a錨點}}；答對移除、答錯加入。
    "function logWrong(qi,ok,q){if(typeof MMSLUG==='undefined')return;try{"
    "var key=MMSLUG+':q'+qi,W=JSON.parse(localStorage.getItem('mm-wrong')||'{}');"
    "if(ok){delete W[key];}else{var qb=q.closest('.q-body'),m=qb?qb.previousElementSibling:null,"
    "tg=m&&m.querySelector?m.querySelector('.tag'):null,ii=q.closest('[id]');"  # 題目外框 id＝重測直達原題
    "W[key]={s:MMSLUG,f:decodeURIComponent(location.pathname.split('/').pop()),"
    "t:tg?tg.textContent:'練習題',a:ii?ii.id:''};}"
    "localStorage.setItem('mm-wrong',JSON.stringify(W));}catch(e){}}"
    "document.querySelectorAll('.opts.quiz').forEach(function(q,qi){"
    "var ans=q.dataset.ans.split(',').map(num),multi=q.dataset.multi==='1';"
    "var opts=[].slice.call(q.querySelectorAll('.opt')),fb=q.querySelector('.opt-fb');var done=false,sel=[];"
    "function grade(p){if(done)return;done=true;opts.forEach(function(b){var i=num(b.dataset.i),c=ans.indexOf(i)>=0;"
    "if(c)b.classList.add('correct');if(p.indexOf(i)>=0&&!c)b.classList.add('wrong');b.disabled=true;});"
    "var ok=p.length===ans.length&&p.every(function(i){return ans.indexOf(i)>=0;});"
    "fb.textContent=ok?'✓ 答對了！':'✗ 答錯了，正解見綠色選項';fb.className='opt-fb '+(ok?'ok':'no');bump(ok);"
    # 概念小測（.kpcheck）：答對自動標『我懂了』、答錯『待複習』（走理解確認，不計入練習成績）；
    # 其餘（歷屆題＋模擬實戰）計入練習成績 persistQuiz。
    "var kc=q.closest('.kpcheck');if(kc){q.dataset.done='1';q.dataset.ok=ok?'1':'0';"
    "var kqs=[].slice.call(kc.querySelectorAll('.opts.quiz'));"
    "if(kqs.every(function(x){return x.dataset.done==='1';})&&typeof kpMastery==='function'){"
    "kpMastery(kc.dataset.kp,kqs.every(function(x){return x.dataset.ok==='1';})?'ok':'review',true);}}"
    "else{persistQuiz(qi,ok);logWrong(qi,ok,q);}}"
    "if(multi){var ck=q.querySelector('.opt-check');"
    "opts.forEach(function(b){b.addEventListener('click',function(){if(done)return;var i=num(b.dataset.i),k=sel.indexOf(i);"
    "if(k>=0){sel.splice(k,1);b.classList.remove('sel');}else{sel.push(i);b.classList.add('sel');}});});"
    "if(ck)ck.addEventListener('click',function(){if(done||!sel.length)return;ck.style.display='none';grade(sel.slice());});}"
    "else{opts.forEach(function(b){b.addEventListener('click',function(){grade([num(b.dataset.i)]);});});}});})();")

# 錯誤回報 Google 表單（空字串＝不顯示按鈕）。REPORT_UNIT_ENTRY＝表單「單元」題的 entry 號，
# 設了就把當頁單元名自動預填進表單（學生免選單元）。按鈕逐頁產生（_report_btn）。
REPORT_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSf7rBJ0OnAQTiZjUbq3gn6CKFgvz9wir8FzEUccXzTfl54DDw/viewform"
REPORT_UNIT_ENTRY = "120093039"


def _report_btn(unit):
    if not REPORT_FORM_URL:
        return ""
    url = REPORT_FORM_URL
    if REPORT_UNIT_ENTRY:
        url += "?usp=pp_url&entry." + REPORT_UNIT_ENTRY + "=" + quote(unit["title"])
    return (f'<a class="report-btn" href="{url}" target="_blank" rel="noopener" '
            f'title="發現內容有誤？點此回報">🚩 回報錯誤</a>')


def _point_html(p):
    if isinstance(p, dict) and "svg" in p:
        cap = f'<figcaption>{html_rich(p["caption"])}</figcaption>' if p.get("caption") else ""
        # 圖寬四段：預設 155px（小圖）／med 250px／wide 362px／full 560px（大型概念圖）
        style = ' style="max-width:960px"' if p.get("hero") else (
            ' style="max-width:560px"' if p.get("full") else (
            ' style="max-width:362px"' if p.get("wide") else (
            ' style="max-width:250px"' if p.get("med") else "")))
        cls = "tfig hero" if p.get("hero") else "tfig"
        hint = '<div class="zoomhint">🔍 點圖可放大看細節</div>' if p.get("hero") else ""
        return f'<li class="figli"><figure class="{cls}"{style}>{p["svg"]}{cap}{hint}</figure></li>'
    if isinstance(p, dict):
        lab = html_rich(p["label"]) + "："
        lines = "".join(f'<span class="ln">{html_rich(l)}</span>' for l in p["lines"])
        return f'<li class="pt2"><span class="lab">{lab}</span><span class="body">{lines}</span></li>'
    if isinstance(p, (list, tuple)):
        main = html_rich(p[0])
        subs = "".join(f'<span class="sub">{html_rich(s)}</span>' for s in p[1:])
        return f"<li>{main}{subs}</li>"
    return f"<li>{html_rich(p)}</li>"


def _geo_table_html(tb):
    head = "".join(f"<th>{html_rich(c)}</th>" for c in tb["head"])
    rows = ""
    for r in tb["rows"]:
        rows += "<tr>" + "".join(f"<td>{html_rich(c)}</td>" for c in r) + "</tr>"
    title = f'<span class="label">{html_rich(tb["title"])}</span>' if tb.get("title") else ""
    return (f'{title}<div class="tbl-wrap"><table class="ref">'
            f"<tr>{head}</tr>{rows}</table></div>")


def _kpcheck_html(kp, slug=""):
    """考點「確認理解」互動區塊：概念小測（check，即時批改）或退回自我檢查（selfcheck，看答案），
    末尾加『我懂了／待複習』自評（掌握度進度追蹤，PROGRESS_JS 的 kpMastery）。
    concept 小測來源：kp 內嵌 "check" 優先，否則查 checks.py 的 CHECKS[(slug,kpid)]。"""
    sc = kp.get("selfcheck")
    chk = kp.get("check") or CHECKS.get((slug, kp.get("id")))
    if not sc and not chk:
        return ""
    body = ""
    if chk:  # 概念選擇題 → 即時批改（正解須存在才互動；answer 為 1-based list）
        # C1 微集：可為 2 題 list（辨析＋變情境）；全部作答完且全對才自動標「我懂了」（QUIZ_JS）
        for c in (chk if isinstance(chk, list) else [chk]):
            ans = c.get("answer")
            why = f'<div class="kc-why">{html_rich(c["why"])}</div>' if c.get("why") else ""
            why_btn = ('<button class="sol-btn mini" data-s="為什麼" data-h="收合" onclick="ts(this)">為什麼</button>'
                       f'<div class="sol">{why}</div>') if why else ""
            tag = f'<div class="kc-tag">{html_rich(c["tag"])}</div>' if c.get("tag") else ""
            body += (f'{tag}<div class="kc-q">{html_rich(c["q"])}</div>'
                     f'{_opts_html(c["options"], ans)}{why_btn}')
    elif sc:  # 退回：原 1 分鐘自我檢查（看答案揭曉）
        ans = "".join(f'<p>{html_rich(x)}</p>' for x in sc["a"]) if isinstance(sc["a"], (list, tuple)) \
            else f'<p>{html_rich(sc["a"])}</p>'
        body = (f'<div class="kc-q">{html_rich(sc["q"])}</div>'
                '<button class="sol-btn" data-s="看答案" data-h="收起答案" onclick="ts(this)">看答案</button>'
                f'<div class="sol">{ans}</div>')
    rate = ('<div class="kc-rate"><span class="kc-rate-l">讀完覺得懂了嗎？</span>'
            f'<button class="kc-ok" onclick="kpMastery(\'{kp["id"]}\',\'ok\')">✓ 我懂了</button>'
            f'<button class="kc-rv" onclick="kpMastery(\'{kp["id"]}\',\'review\')">✗ 待複習</button></div>')
    return (f'<div class="kpcheck" data-kp="{kp["id"]}">'
            '<div class="kc-head">✅ 確認理解 <small>先自己作答／回想，再自評掌握度</small></div>'
            f'{body}{rate}</div>')


def _kp_html(kp, slug=""):
    points = "".join(_point_html(p) for p in kp["points"])
    tables = "".join(_geo_table_html(tb) for tb in kp.get("tables", []))
    mis = ""
    if kp.get("misconceptions"):
        rows = ""
        for m in kp["misconceptions"]:
            rows += (f'<tr><td class="err">{html_rich(m["wrong"])}</td>'
                     f'<td class="cor"><button class="sol-btn mini" data-s="顯示正解" '
                     f'data-h="隱藏正解" onclick="ts(this)">顯示正解</button>'
                     f'<div class="sol inline">{html_rich(m["right"])}</div></td></tr>')
        mis = ('<span class="label">常見誤解 × → 正解 ○</span>'
               '<div class="tbl-wrap"><table class="mis">'
               '<tr><th>常見誤解 <span class="x">×</span></th>'
               '<th>正確理解 <span class="o">○</span></th></tr>'
               f"{rows}</table></div>")
    qs = ""
    qlist = kp.get("questions", [])
    for i, q in enumerate(qlist):
        if "subqs" in q:  # 題組
            qs += _question_intro_html(q)
            for sq in q["subqs"]:
                qs += _subq_html(sq)
        else:
            qs += _question_html(q, first=(i == 0 and False),
                                 qid=f'{kp["id"]}-q{i}', kp=kp["id"])
    strategy = ""
    if kp.get("strategy"):
        s = kp["strategy"]
        if isinstance(s, (list, tuple)):
            inner = "".join(f'<div class="sln">{html_rich(x)}</div>' for x in s)
        else:
            inner = html_rich(s)
        strategy = f'<span class="label">解題策略</span><div class="callout">{inner}</div>'
    selfcheck = _kpcheck_html(kp, slug)
    prereq = ""
    pr = kp.get("prereq")
    if pr:
        items = "".join(f"<li>{html_rich(x)}</li>" for x in pr) if isinstance(pr, (list, tuple)) \
            else f"<li>{html_rich(pr)}</li>"
        prereq = ('<div class="prereq"><span class="pr-tag">🔑 先備</span>'
                  f'<ul class="pr-list">{items}</ul>'
                  '<span class="pr-note">這幾項看不懂，先回去補再往下會更省力</span></div>')
    worked = ""
    w = kp.get("worked")
    if w:
        steps = "".join(
            f'<li><span class="wk-do">{html_rich(st["do"])}</span>'
            f'<span class="wk-why">{html_rich(st["why"])}</span></li>' for st in w["steps"])
        wans = f'<div class="wk-ans">答：{html_rich(w["ans"])}</div>' if w.get("ans") else ""
        worked = ('<div class="worked"><div class="wk-head">👉 示範一題 — 先自己想想，再點開解法對照</div>'
                  f'<div class="wk-q">{html_rich(w["q"])}</div>'
                  '<button class="sol-btn wk-btn" data-s="💡 看詳解（每步都說明為什麼）" '
                  'data-h="收合詳解" onclick="ts(this)">💡 看詳解（每步都說明為什麼）</button>'
                  f'<div class="sol wk-reveal"><ol class="wk-steps">{steps}</ol>{wans}</div></div>')
    # 路線選擇器要用的兩個訊號：考頻星數、官方答對率（沒有資料就不寫這個屬性）
    _fr = (kp.get("freq") or "").count("★")
    _rt = EXAM_RATES.get((slug, kp["id"]))
    _data = f' data-freq="{_fr}"' + (f' data-rate="{_rt[0]:.0f}"' if _rt else "")
    return (f'<div class="card" id="{kp["id"]}"{_data}>'
            f'<p class="kp"><button class="kpchk" data-kp="{kp["id"]}" onclick="kpToggle(this)" '
            f'title="標記此考點已讀" aria-label="標記已讀"></button>'
            f'<span class="num">{kp["num"]}</span>{html_rich(kp["title"])}{_freq_badge(kp.get("freq"))}'
            f'{_axis_badge(kp)}{_rate_badge(slug, kp["id"])}'
            f'<span class="kp-mastery" data-kp="{kp["id"]}"></span></p>'
            f'{prereq}'
            f'<div class="callout"><b>◆ 這個考點在學什麼：</b>{html_rich(kp["intro"])}</div>'
            f'{_cues_html(slug, kp["id"])}'
            f'<span class="label">重點與公式</span><ul class="points">{points}</ul>'
            f'{tables}'
            f'{mis}'
            f'{worked}'
            f'<span class="label">歷屆試題</span>{qs}'
            f"{strategy}{selfcheck}</div>")


def _freq_badge(freq):
    """考點旁的考頻徽章（★ 越多越常考）。"""
    return f'<span class="kp-freq" title="近十年考頻">{html_rich(freq)}</span>' if freq else ""


def _axis_badge(kp):
    """考點標題旁的入口組合。

    老師的觀察（2026-08-05）：**實際考題多半是「主＋次」兩格的組合，不是單一格**。
    所以標成有方向的組合「式 ▸ 根」＝從式切入、接著處理根，而不是主／次分列——
    後者會讓學生以為次要那格可以不管。
    """
    ax = kp.get("axis")
    if not ax:
        return ""
    if len(ax) >= 2:
        tip = f"常見組合：從「{ax[0]}」切入，接著會用到「{ax[1]}」"
    else:
        tip = f"建議從「{ax[0]}」切入"
    parts = [f'<span class="ax-tag{" main" if i == 0 else ""}">'
             f'{AXIS_ICON.get(k, "◆")}{html_rich(k)}</span>' for i, k in enumerate(ax)]
    inner = '<span class="ax-arrow">▸</span>'.join(parts)
    return f'<span class="ax-tags" title="{_esc_attr(tip)}">{inner}</span>'


def _rate_badge(slug, kpid):
    """考點旁的官方答對率徽章：這個考點對應的歷屆數 A 題目，全國平均多少人答對。

    來源 content/exam_rates.py（由 build/gen_examrates.py 從 exam/ 題庫導出）。
    只有樣本 >= 3 題的考點才有資料——樣本再少就只是「那一題難」，不是「這個考點難」。
    多選題採全對率，與單選答對率同構念（完全答對的比例）才能一起平均。
    """
    hit = EXAM_RATES.get((slug, kpid))
    if not hit:
        return ""
    rate, n, n_multi = hit
    tip = f"111–115 學測數 A 對應此考點 {n} 題的平均"
    if n_multi:
        tip += f"（其中 {n_multi} 題多選，採全對率）"
    return (f'<span class="kp-rate" title="{_esc_attr(tip)}">'
            f'全國答對率 {rate:.0f}%<i>{n} 題</i></span>')


def _hard_badge(level):
    """★★★ 題目標「學測難題」徽章。"""
    return ' <span class="hard-badge">🔥 學測難題</span>' if level and "★★★" in level else ""


def _touch_html(cs, cur_slug, cur_kp):
    """觸類旁通：這個考點的線索若屬於某「同一招」群組（cues 的 g），
    就列出同群、其他單元／考點的連結，串成小型聯想圖。"""
    groups = []
    for c in cs:
        g = c.get("g")
        if g and g not in groups:
            groups.append(g)
    rows = ""
    for g in groups:
        seen, links = set(), []
        for c2 in CUES:
            if c2.get("g") != g:
                continue
            key = (c2["unit"], c2["kp"])
            if key == (cur_slug, cur_kp) or key in seen:
                continue
            seen.add(key)
            u = _BY_SLUG.get(c2["unit"], {})
            nav = _kp_nav(c2["unit"], c2["kp"])
            links.append(f'<a class="ct-link" href="{u.get("file","")}#{c2["kp"]}">'
                         f'{u.get("emoji","")} {u.get("title","")}·{nav} ↗</a>')
        if links:
            rows += (f'<div class="ct-row"><b class="ct-g">{html_rich(GROUPS.get(g, g))}</b>'
                     f'<span class="ct-also">也用在</span>{"".join(links)}</div>')
    if not rows:
        return ""
    return ('<div class="cue-touch"><span class="ct-lbl">🔗 觸類旁通 · 同一招多處用</span>'
            f'{rows}</div>')


def _cues_html(slug, kpid):
    """考點旁「🔑 解題線索」：看到哪些關鍵字就想到這個考點（反查 cues.py），
    並附「觸類旁通」跨單元同招串連。"""
    cs = _CUES_BY_KP.get((slug, kpid))
    if not cs:
        return ""
    kws = "、".join(f'<b class="cue-kw">{html_rich(c["kw"])}</b>' for c in cs)
    return (f'<div class="cues"><span class="cue-lbl">🔑 解題線索</span>'
            f'看到 {kws} → 想到這個考點。'
            f'<a class="cue-more" href="{CLUEMAP_FILE}">全部線索地圖 →</a>'
            f'{_touch_html(cs, slug, kpid)}</div>')


def _mixed_html(mixed):
    """混合題實戰：真學測非選題＋官方評分原則。可放多題組（list）或單一題組（dict）。"""
    if not mixed:
        return ""
    groups = mixed if isinstance(mixed, list) else [mixed]
    blocks = ""
    for g in groups:
        items = ""
        for it in g["items"]:
            opts = _opts_html(it.get("options"), None) if it.get("options") else ""
            rub = ""
            r = it.get("rubric")
            if r:
                full = "".join(f"<li>{html_rich(x)}</li>" for x in r["full"])
                rub = ('<div class="mx-rub"><div class="mx-rub-h">✎ 官方評分原則</div>'
                       f'<div class="mx-rub-row"><span class="mx-lvl mx-full">滿分</span>'
                       f'<div>下列均須正確、且過程完整：<ol>{full}</ol></div></div>'
                       f'<div class="mx-rub-row"><span class="mx-lvl mx-mid">部分</span><div>{html_rich(r["partial"])}</div></div>'
                       f'<div class="mx-rub-row"><span class="mx-lvl mx-zero">零分</span><div>{html_rich(r["zero"])}</div></div></div>')
            items += (f'<div class="mx-item"><div class="mx-q"><span class="mx-tag">{html_rich(it["tag"])}</span>'
                      f'{html_rich(it["q"])}{opts}</div>'
                      '<button class="sol-btn mini" data-s="看官方解答＋評分原則" data-h="收合" '
                      'onclick="ts(this)">看官方解答＋評分原則</button>'
                      f'<div class="sol"><div class="mx-ans"><b>滿分參考答案：</b>{html_rich(it["answer"])}</div>{rub}</div></div>')
        src = f'<span class="mx-src">{html_rich(g["src"])}</span>' if g.get("src") else ""
        blocks += (f'<div class="mx-group"><div class="mx-ctx"><b>題組情境</b>{src}<br>{html_rich(g["context"])}</div>{items}</div>')
    return ('<div class="part" id="mixed">混合題實戰 <small>108 課綱新增 · 練「寫出過程」拿分（附官方評分原則）</small></div>'
            f'<section class="mixed">{blocks}</section>')


def _question_intro_html(q):
    """題組的共同題幹。"""
    meta = (f'<div class="q-meta"><span class="tag">{html_rich(q["tag"])}</span>'
            f'<span class="lv">{q["level"]}</span>{_hard_badge(q["level"])}</div>')
    body = f'<div class="q-body">{html_rich(q["body"])}</div>'
    return meta + body + _core_block(q)


def _challenge_html(ch):
    """B1 直覺挑戰（SOIL：製造認知落差）。content 的 part0 提供 challenge 資料才渲染。
    三步固定：點直覺答案 → 揭示正解 → 一句話說明＋錨點連到考點。"""
    if not ch:
        return ""
    kpid = ch.get("kp", "")
    kpnum = re.sub(r"\D", "", kpid)
    opts = "".join(
        f'<button class="chal-opt" data-ok="{1 if i == ch["answer"] else 0}" '
        f'onclick="chal(this)">{html_rich(o)}</button>'
        for i, o in enumerate(ch["options"]))
    link = (f'<a class="chal-go" href="#{kpid}">→ 前往考點 {kpnum} 看懂為什麼</a>'
            if kpid else "")
    return ('<div class="card chal">'
            '<span class="label">🎯 直覺挑戰：先猜猜看</span>'
            f'<p class="chal-q">{html_rich(ch["q"])}</p>'
            f'<div class="chal-opts">{opts}</div>'
            '<div class="chal-reveal">'
            f'<p><b>正解：{html_rich(ch["options"][ch["answer"]])}</b>　{html_rich(ch["reveal"])}</p>'
            f'{link}</div></div>')


AXIS_ICON = {"式": "＝", "根": "◉", "圖": "📈",
             "方向": "↗", "方程": "＝", "距離": "📏", "區域": "▨",
             "項": "①", "遞迴": "↻", "和": "∑", "函數模型": "📈"}


def _axes_html(ax):
    """入口 N 格（方案 B）：把題目先分進 3–4 個抽屜，再挑公式。

    content 的 part0 有 axes 才渲染；沒有的單元完全不受影響。
    """
    if not ax:
        return ""
    cells = ""
    for it in ax["items"]:
        k = it["key"]
        cells += (f'<div class="axcell" data-ax="{_esc_attr(k)}">'
                  f'<span class="ax-k"><i>{AXIS_ICON.get(k, "◆")}</i>{html_rich(k)}</span>'
                  f'<span class="ax-d">{html_rich(it["desc"])}</span>'
                  f'<span class="ax-h">{html_rich(it["hint"])}</span></div>')
    return ('<div class="card axes"><span class="label">🗂️ 先分抽屜：這題在講什麼</span>'
            f'<div class="callout">{html_rich(ax["intro"])}</div>'
            f'<div class="axgrid">{cells}</div></div>')


def _entrydiag_html(ed, axes):
    """入口診斷：只判斷「第一步從哪個抽屜切入」，不要求算出答案。

    與 B1 直覺挑戰同一套互動慣例（點選 → 即時對錯 → 一句話說明 → 錨點回考點），
    但選項固定是那幾個入口表示，練的是「辨識」而不是「計算」。
    """
    if not ed or not axes:
        return ""
    keys = [it["key"] for it in axes["items"]]
    cards = ""
    for i, c in enumerate(ed["cards"]):
        opts = "".join(
            f'<button class="ed-opt" data-ok="{1 if k == c["a"] else 0}" '
            f'onclick="edPick(this)">{html_rich(k)}</button>' for k in keys)
        kpid = c.get("kp", "")
        link = (f'<a class="ed-go" href="#{kpid}">→ 考點 {re.sub(r"[^0-9]", "", kpid)}</a>'
                if kpid else "")
        cards += (f'<div class="edcard" data-i="{i}">'
                  f'<div class="ed-q"><span class="ed-n">{i + 1}</span>{html_rich(c["q"])}</div>'
                  f'<div class="ed-opts">{opts}</div>'
                  f'<div class="ed-fb"><b class="ed-ans">入口：{html_rich(c["a"])}</b>'
                  f'<span class="ed-why">{html_rich(c["why"])}</span>{link}</div></div>')
    return ('<div class="card entrydiag">'
            f'<span class="label">🧭 {html_rich(ed.get("heading", "入口診斷"))}</span>'
            f'<div class="callout">{html_rich(ed.get("note", ""))}</div>'
            f'<div class="ed-prog">答對 <b id="ed-ok">0</b> / {len(ed["cards"])}'
            '<span class="ed-hint">（只選抽屜，先不要算）</span></div>'
            f'{cards}</div>')


def _part0_html(p0):
    if not p0:
        return ""
    yrs = "".join(f"<th>{y}</th>" for y in p0["trend_table"]["years"])
    cnts = "".join(f"<td>{c}</td>" for c in p0["trend_table"]["counts"])
    table = ('<div class="tbl-wrap"><table class="ref" style="min-width:640px">'
             f'<tr><th style="width:14%">年度</th>{yrs}<th>合計</th></tr>'
             f'<tr><td>題數(加權)</td>{cnts}<td><b>{p0["trend_table"]["total"]}</b></td></tr>'
             "</table></div>")
    notes = "".join(f"<li>{html_rich(n)}</li>" for n in p0.get("notes", []))
    mp = (f'<span class="label">考點地圖</span><div class="callout">{html_rich(p0["map"])}</div>'
          if p0.get("map") else "")
    heading = p0.get("heading", "出題趨勢與落點")
    sub = p0.get("sub", "先抓近十年趨勢與落點，再進入觀念")
    fig = f'<ul class="points">{_point_html(p0["fig"])}</ul>' if p0.get("fig") else ""
    opener = f'<ul class="points">{_point_html(p0["opener"])}</ul>' if p0.get("opener") else ""
    return (f'<div class="part" id="part0">Part 0　引起動機：{heading}'
            f'<small>{sub}</small></div>'
            f'{opener}'
            f'{_axes_html(p0.get("axes"))}'
            f'{_entrydiag_html(p0.get("entrydiag"), p0.get("axes"))}'
            f'{_challenge_html(p0.get("challenge"))}'
            '<div class="card">'
            '<span class="label">近十年出題趨勢（106–115）</span>'
            f"{table}"
            f'<span class="label">趨勢解讀</span><ul class="points">{notes}</ul>'
            f"{mp}{fig}</div>")


def _part2_html(p2, slug=""):
    if not p2:
        return ""
    kps = PART2_KP.get(slug, [])
    groups = ""
    gi = 0
    for g in p2["groups"]:
        items = ""
        for j, q in enumerate(g["questions"]):
            kp = q.get("kp") or (kps[gi] if gi < len(kps) else "")  # 對應考點（解題核心連回、複習用）
            items += _question_html(q, first=(j == 0), qid=f'p2q{gi}', kp=kp)
            gi += 1
        groups += f'<span class="label">{g["title"]}</span>{items}'
    return (f'<div class="part" id="part2">Part 2　喚起行動：模擬實戰（{p2.get("count","")}題）'
            f'<small>{p2.get("note","")}</small></div><div class="card">{groups}</div>')


def _takeaway_sentence(slug):
    """從單元知識地圖（soil_maps.SLIDES 的 SVG）抽出「帶走一句話」核心句。
    同源重用：句子只存在地圖 SVG 一份，Part 3 回想區塊直接引用，不另存副本。"""
    try:
        from soil_maps import SLIDES
    except Exception:
        return ""
    svg = SLIDES.get(slug, "")
    # 錨定底部白字標籤「帶走一句話」（副標題那次是灰紫字），取其後第一個深紅粗體字＝核心句
    m = re.search(r'fill="#fff"[^>]*>帶走一句話</text>.*?fill="#6f1f33"[^>]*>([^<]+)</text>', svg)
    if svg and not m:
        print(f"  ⚠ [{slug}] 知識地圖 SVG 找不到「帶走一句話」句（格式變了？），Part 3 回想區塊未渲染")
    return m.group(1) if m else ""


def _part3_html(p3, slug=""):
    if not p3:
        return ""
    # SOIL A2：考前速查開頭先「提取」核心句（回想），而非直接重讀
    recall = ""
    tk = _takeaway_sentence(slug)
    if tk:
        recall = ('<div class="recall">'
                  '<span class="label">先回想：這個單元帶走的一句話是什麼？</span>'
                  '<p class="recall-hint">先在心裡把它說完整，再點開對照——回想一次，勝過重讀十次。</p>'
                  '<button class="sol-btn" data-s="回想好了，點我對照" data-h="收合" '
                  'onclick="ts(this)">回想好了，點我對照</button>'
                  f'<div class="sol"><b>{tk}</b></div></div>')
    rows = ""
    for r in p3["ref_table"]:
        rows += f'<tr><td>{html_rich(r["k"])}</td><td>{html_rich(r["v"])}</td></tr>'
    ref = ('<span class="label">3-1　公式一頁速查</span>'
           '<div class="tbl-wrap"><table class="ref">'
           '<tr><th style="width:30%">主題</th><th>必記公式 / 結論</th></tr>'
           f"{rows}</table></div>")
    checks = "".join(f"<li>{html_rich(c)}</li>" for c in p3.get("checklist", []))
    chk = (f'<span class="label">3-2　常見誤解總清單（考前自我檢查）</span>'
           f'<ol class="checklist">{checks}</ol>')
    return ('<div class="part" id="part3">Part 3　快速複習：考前翻這頁就好</div>'
            f'<div class="card">{recall}{ref}{chk}</div>')


def _toolbar(unit, units):
    try:
        from units import SECTIONS
    except Exception:
        SECTIONS = None
    by_slug = {u["slug"]: u for u in units}

    def _unit_option(u):
        cur = "（目前）" if u["slug"] == unit["slug"] else ""
        return f'<option value="{u["file"]}">{u["emoji"]} {u["title"]}{cur}</option>'

    unit_opts = ['<option value="">單元 ▾</option>',
                 '<option value="index.html">📚 目錄首頁</option>',
                 '<option value="115學測數學_待複習與錯題.html">📌 待複習與錯題</option>',
                 '<option value="115學測數學_概念地圖.html">🗺️ 概念地圖</option>',
                 '<option value="115學測數學_跨單元整合_脈絡地圖.html">🧩 跨單元脈絡地圖</option>',
                 '<option value="115學測數學_解題線索地圖.html">🧭 解題線索地圖</option>']
    if SECTIONS:
        # 依首頁四大主題分組（optgroup），與 index.html 一致。
        for label, slugs in SECTIONS:
            group = [_unit_option(by_slug[s]) for s in slugs
                     if s in by_slug and not (by_slug[s].get("draft") and s != unit["slug"])]
            if group:
                unit_opts.append(f'<optgroup label="{label}">{"".join(group)}</optgroup>')
    else:
        for u in units:
            if u.get("draft") and u["slug"] != unit["slug"]:
                continue
            unit_opts.append(_unit_option(u))
    kp_opts = ['<option value="">跳至考點 ▾</option>']
    if unit.get("part0"):
        kp_opts.append('<option value="part0">Part 0 · 出題趨勢</option>')
    for kp in unit["kps"]:
        kp_opts.append(f'<option value="{kp["id"]}">{kp["num"]} · {kp.get("nav", kp["title"])}</option>')
    if unit.get("mixed"):
        kp_opts.append('<option value="mixed">🖊 混合題實戰</option>')
    kp_opts.append('<option value="part2">Part 2 · 模擬實戰</option>')
    kp_opts.append('<option value="part3">Part 3 · 考前速查</option>')
    return (f'<div class="toolbar"><span class="t-title">{unit["title"]}</span>'
            '<span class="tb-caret">▾ 展開選單</span>'
            f'{HOME_LINK}'
            f'<select class="nav-select" onchange="if(this.value){{location.href=this.value;}}">'
            f'{"".join(unit_opts)}</select>'
            f'<select class="nav-select" onchange="if(this.value){{location.hash=this.value;this.selectedIndex=0;}}">'
            f'{"".join(kp_opts)}</select>'
            '<button onclick="revealAll()">全部顯示解答</button>'
            '<button onclick="hideAll()">全部隱藏</button></div>')


def _routebar_html():
    """Part 1 上方的「今天走哪條路」：一次把 58 個考點縮成看得完的份量。

    只篩 Part 1 的考點卡；Part 0 趨勢、Part 2 實戰、Part 3 速查一律保留。
    """
    return (
        '<div class="routebar" id="routebar">'
        '<span class="rb-lbl">🧭 今天走哪條路？</span>'
        '<span class="rb-btns">'
        '<button class="rb-btn on" data-r="all" onclick="setRoute(\'all\')">完整複習</button>'
        '<button class="rb-btn" data-r="basic" onclick="setRoute(\'basic\')">先拿基本分</button>'
        '<button class="rb-btn" data-r="review" onclick="setRoute(\'review\')">錯題回補</button>'
        '</span>'
        '<span class="rb-note" id="rb-note"></span></div>')


def build_html(unit, units):
    css = _asset("style.css")
    js = _asset("app.js")
    kps_html = "".join(_kp_html(kp, unit["slug"]) for kp in unit["kps"])
    body = (f'<div class="hero"><h1>{unit["title"]}</h1>'
            f'<p>{unit.get("hero_sub","")}</p>'
            f'<p style="font-size:13px;color:#9a857c;margin-top:2px">{unit.get("hero_sub2","")}</p></div>'
            '<div class="legend">使用方式：點選紅色 '
            '<span class="blank on" style="cursor:default"><span class="a">空格</span></span> '
            '可顯示／隱藏填空答案；點 <b>「顯示正解 / 顯示解答」</b> 按鈕可展開答案。'
            '也可用上方 <b>「全部顯示解答」</b> 一次切換整頁。</div>'
            f'<div class="unit-prog">📖 本單元讀過 <b id="up-txt">0 / {len(unit["kps"])}</b> 考點'
            '<span class="upbar"><i id="up-bar"></i></span>'
            '<button class="up-all" onclick="markAllKp()">全部標記／取消</button>'
            '<span class="up-hint">（點各考點前的 ○ 標記；會同步到概念地圖）</span></div>'
            f'<div class="unit-prog mastery-prog">✅ 已確認理解 <b id="mst-txt">0</b> / {len(unit["kps"])} 考點'
            '<span class="upbar mst"><i id="mst-bar"></i></span>'
            '<span class="mst-rvline">⚠ 待複習 <b id="mst-rv">0</b>'
            '<button class="up-all" id="mst-jump" onclick="jumpReview()" style="display:none">跳到待複習 →</button></span>'
            '<a class="up-all mst-all" href="115學測數學_待複習與錯題.html">📌 全站待複習與錯題</a>'
            '<span class="up-hint">（在各考點末「確認理解」作答或自評）</span></div>'
            f'{_part0_html(unit.get("part0"))}'
            '<div class="part">Part 1　建構概念：'
            f'{unit.get("part1_label","五大考點")} <small>先把觀念與公式打穩，再上戰場</small></div>'
            f'{_routebar_html()}'
            f'{kps_html}'
            f'{_mixed_html(unit.get("mixed"))}'
            f'{_part2_html(unit.get("part2"), unit["slug"])}'
            f'{_part3_html(unit.get("part3"), unit["slug"])}'
            f'<div class="foot">{unit.get("foot","")}</div>')
    report_btn = _report_btn(unit)
    og_title = unit.get("page_title", unit["title"])
    og_desc = f'學測數A「{unit["title"]}」重點整理：考點地圖、先備、示範例與即時練習，中等程度也能自學看得懂。'
    og = og_meta(og_title, og_desc, unit["file"])
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ANALYTICS}<title>{og_title}</title>
{og}
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<style>
{css}</style>
</head>
<body>
{_toolbar(unit, units)}
<div class="wrap">
{body}
{PRIVACY_HTML}
</div>
{LIGHTBOX_HTML}
{QUIZ_BADGE_HTML}
{report_btn}
<script src="{KATEX}/katex.min.js"></script>
<script src="{KATEX}/contrib/auto-render.min.js"></script>
<script>
{js}</script>
<script>
window.MMSLUG="{unit["slug"]}";window.MMKPS={[k["id"] for k in unit["kps"]]};
{PROGRESS_JS}
{ENTRYDIAG_JS}
{ROUTE_JS}</script>
<script>
{LIGHTBOX_JS}</script>
<script>
{QUIZ_JS}</script>
</body>
</html>
"""
