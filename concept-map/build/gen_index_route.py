# -*- coding: utf-8 -*-
r"""把「今天走哪條路」路線列注入子站首頁 concept-map/index.html。

為什麼要一支腳本：`index.html` 是**手寫維護**的（AGENTS.md），不由 build 產生。
但路線篩選需要 58 個考點的星等，手改 58 個連結太容易出錯。
折衷做法：內容仍手寫，只有 `<!-- ROUTE-START -->` 與 `<!-- ROUTE-END -->`
之間這一段由本腳本維護——星等資料從 content/*.py 讀，改考點後重跑即可。

用法：
    cd D:/web/concept-map
    PYTHONUTF8=1 python build/gen_index_route.py
"""
import importlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, "index.html")
sys.path.insert(0, os.path.join(ROOT, "content"))

import units as units_mod  # noqa: E402

START = "<!-- ROUTE-START 由 build/gen_index_route.py 產生，勿手改；改動請跑該腳本 -->"
END = "<!-- ROUTE-END -->"


def collect():
    """{檔名: {"slug": slug, "kp": {kpid: 星數}}}"""
    out = {}
    for u in units_mod.UNITS:
        mod = importlib.import_module(u["slug"])
        importlib.reload(mod)
        kps = {k["id"]: (k.get("freq") or "").count("★") for k in mod.UNIT["kps"]}
        out[u["file"]] = {"slug": u["slug"], "kp": kps}
    return out


CSS = """<style>
  .idx-route{display:flex;align-items:center;flex-wrap:wrap;gap:8px 10px;background:#fbf7f4;
    border:1px solid var(--line,#e7dcd6);border-radius:12px;padding:10px 14px;margin:16px 0 4px}
  .idx-route .rb-lbl{font-weight:800;color:#6f1f33;font-size:14.5px;white-space:nowrap}
  .idx-route .rb-btns{display:flex;gap:6px;flex-wrap:wrap}
  .idx-route .rb-btn{display:inline-flex;align-items:center;min-height:34px;background:#fff;color:#6b5249;
    border:1.5px solid var(--line,#e7dcd6);border-radius:20px;padding:5px 14px;font-size:13.5px;
    font-weight:700;font-family:inherit;cursor:pointer;transition:.15s}
  .idx-route .rb-btn:hover{border-color:#8c2740;color:#8c2740}
  .idx-route .rb-btn.on{background:#8c2740;border-color:#8c2740;color:#fff}
  .idx-route .rb-note{flex:1 1 100%;font-size:13px;color:#7a6a63;line-height:1.6}
  .idx-route .rb-note:empty{display:none}
  .unit.rt-empty{opacity:.5}
  @media(max-width:560px){
    .idx-route .rb-lbl{flex:1 1 100%}
    .idx-route .rb-btn{min-height:40px;padding:4px 12px;font-size:13px}
  }
</style>"""

BAR = """<div class="idx-route" id="idx-route">
  <span class="rb-lbl">\U0001f9ed 今天走哪條路？</span>
  <span class="rb-btns">
    <button class="rb-btn on" data-r="all" onclick="idxRoute('all')">完整複習</button>
    <button class="rb-btn" data-r="basic" onclick="idxRoute('basic')">先拿基本分</button>
    <button class="rb-btn" data-r="review" onclick="idxRoute('review')">錯題回補</button>
  </span>
  <span class="rb-note" id="idx-rb-note"></span>
</div>"""

# 與單元頁共用 localStorage 的 mm-route / mm-kp-mastery，選一次全站通用。
# 找不到星等資料的連結一律「顯示」——資料萬一過期，寧可多顯示也不要把考點藏起來。
JS = """<script>
(function(){
  var D=window.MMROUTE||{f:{},s:{}};
  function meta(a){
    var h=a.getAttribute('href')||'', i=h.indexOf('#');
    if(i<0) return null;
    var file=h.slice(0,i), kp=h.slice(i+1);
    var u=D.f[file]; if(!u||!(kp in u.kp)) return null;
    return {file:file,kp:kp,freq:u.kp[kp],slug:u.slug};
  }
  function mastery(){ try{ return JSON.parse(localStorage.getItem('mm-kp-mastery')||'{}'); }catch(e){ return {}; } }
  window.idxRoute=function(r,quiet){
    var m=mastery(), shown=0, total=0, units=0;
    document.querySelectorAll('.unit').forEach(function(card){
      var vis=0, any=0;
      card.querySelectorAll('.sub a[href*="#kp"]').forEach(function(a){
        var d=meta(a); any++;
        var show=true;
        if(d){
          total++;
          if(r==='basic') show = d.freq>=3;
          else if(r==='review') show = m[d.slug+':'+d.kp]==='review';
        }
        a.style.display = show ? '' : 'none';
        if(show){ vis++; shown++; }
      });
      var empty = any>0 && vis===0;
      card.classList.toggle('rt-empty', empty && r!=='all');
      if(!empty) units++;
    });
    document.querySelectorAll('.idx-route .rb-btn').forEach(function(b){ b.classList.toggle('on', b.dataset.r===r); });
    var n=document.getElementById('idx-rb-note');
    if(n){
      if(r==='basic') n.textContent='只列 '+shown+' 個必考核心考點（共 '+total+' 個），涵蓋 '+units+' 個單元。點進單元後也是同一條路線。';
      else if(r==='review') n.textContent = shown ? ('只列你標記待複習的 '+shown+' 個考點。') : '目前沒有標記待複習的考點——先到各考點末「確認理解」作答，答錯會自動標記。';
      else n.textContent='';
    }
    if(!quiet){ try{ localStorage.setItem('mm-route', r); }catch(e){} }
  };
  var r='all'; try{ r=localStorage.getItem('mm-route')||'all'; }catch(e){}
  idxRoute(r,1);
})();
</script>"""


def main():
    data = collect()
    pairs = []
    for f, d in data.items():
        kp = ",".join(f'{k}:{v}' for k, v in d["kp"].items())
        pairs.append(f'"{f}":{{s:"{d["slug"]}",kp:{{{kp}}}}}')
    blob = ("<script>window.MMROUTE={f:{"
            + ",".join(f'"{f}":{{kp:{{' + ",".join(f'{k}:{v}' for k, v in d["kp"].items())
                       + f'}},slug:"{d["slug"]}"}}' for f, d in data.items())
            + "}};</script>")

    block = "\n".join([START, CSS, BAR, blob, JS, END])

    src = open(INDEX, encoding="utf-8").read()
    if START not in src or END not in src:
        sys.exit(f"✗ index.html 找不到 {START} / {END} 標記，請先加上")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, src, flags=re.S)
    if new == src:
        print("[index-route] 內容未變")
    else:
        open(INDEX, "w", encoding="utf-8").write(new)
        print("[index-route] 已更新 concept-map/index.html")

    n_kp = sum(len(d["kp"]) for d in data.values())
    n3 = sum(1 for d in data.values() for v in d["kp"].values() if v >= 3)
    print(f"  單元 {len(data)} 個、考點 {n_kp} 個，其中 3★ {n3} 個（＝「先拿基本分」會顯示的數量）")


if __name__ == "__main__":
    main()
