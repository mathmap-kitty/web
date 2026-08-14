# -*- coding: utf-8 -*-
"""全站「待複習與錯題」彙整頁（獨立頁，純 localStorage）。
一頁看完 11 單元裡所有標記『待複習』的核心概念＋答錯過的題目，可一鍵去複習／重測。
資料在瀏覽器本機（mm-kp-mastery 的 review／mm-wrong），本頁只是把它們讀出來彙整。
"""
import os
import io
import sys
import json
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
from build_html import ANALYTICS, PRIVACY_HTML, _report_btn, og_meta, HOME_LINK  # noqa: E402
from units import UNITS  # noqa: E402

KATEX = "katex"  # 本地離線包，見 build_html.py 同名常數
OUT = os.path.join(ROOT, "dist", "115學測數學_待複習與錯題.html")

BY_SLUG = {u["slug"]: u for u in UNITS}
KP_NAV = {}
UNITS_META = []
for _u in UNITS:
    if not os.path.exists(os.path.join(ROOT, "content", _u["slug"] + ".py")):
        continue
    _U = importlib.import_module(_u["slug"]).UNIT
    KP_NAV[_u["slug"]] = {k["id"]: k.get("nav", k.get("title", "")) for k in _U["kps"]}
    UNITS_META.append({"slug": _u["slug"], "e": _u.get("emoji", ""), "t": _u["title"], "f": _u["file"]})


def _asset(name):
    return io.open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


def build():
    css = _asset("style.css")
    extra = """
  .rv-topbar{position:sticky;top:0;z-index:50;background:rgba(140,39,64,.97);color:#fff;display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 18px;box-shadow:0 2px 10px rgba(0,0,0,.15)}
  .rv-topbar .t-title{font-weight:800;margin-right:auto;font-size:16px;letter-spacing:.5px}
  .rv-topbar a{background:#fff;color:var(--maroon-d);border-radius:20px;padding:5px 13px;font-weight:700;font-size:13.5px;text-decoration:none}
  .rv-wrap{max-width:860px;margin:0 auto;padding:0 16px 70px}
  .rv-hero{text-align:center;padding:22px 0 4px}
  .rv-hero h1{color:var(--maroon);font-size:25px;margin:.1em 0;letter-spacing:.5px}
  .rv-hero p{color:#6b5249;font-size:15px;max-width:680px;margin:.4em auto}
  .rv-sec{margin:22px 0 8px}
  .rv-sec-h{font-weight:800;color:var(--maroon-d);font-size:18px;display:flex;align-items:center;gap:8px;border-left:5px solid var(--maroon);padding-left:10px;margin-bottom:10px}
  .rv-sec-h .cnt{font-size:14px;color:#fff;background:var(--maroon);border-radius:14px;padding:1px 11px;font-weight:800}
  .rv-empty{background:#f1f8f4;border:1px solid #cfe6d8;border-radius:12px;padding:14px 18px;color:#2e6b46;font-size:14.5px;text-align:center}
  .rv-uh{font-weight:800;color:#6f1f33;font-size:14.5px;margin:12px 0 6px}
  .rv-item{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:#fff;border:1px solid var(--line);border-radius:12px;padding:9px 14px;margin:6px 0}
  .rv-item .rv-t{flex:1 1 200px;min-width:0;color:#3a3a3a;font-size:14.5px}
  .rv-item .rv-tag{font-size:12px;color:#8c2740;background:#f6e7ec;border-radius:10px;padding:1px 8px;font-weight:700;margin-right:6px;white-space:nowrap}
  .rv-go{font-size:13px;color:#fff;background:var(--maroon);border-radius:16px;padding:4px 13px;text-decoration:none;font-weight:700;white-space:nowrap}
  .rv-go.retest{background:#2e7d46}
  .rv-x{border:1px solid #d9c2c9;background:#fff;color:#9a6b7a;border-radius:16px;padding:4px 11px;font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;white-space:nowrap}
  .rv-x:hover{background:#faf2f5}
  .rv-tools{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;margin-top:6px}
  .rv-note{background:#eef4fb;border:1px dashed #b7cef0;border-radius:12px;padding:10px 16px;font-size:13.5px;color:#3a4a63;margin:8px 0 4px;line-height:1.8}
  .rv-foot{text-align:center;color:#9a8a82;font-size:12.5px;margin-top:26px}
"""
    nav = (HOME_LINK
           + '<a href="index.html">📚 目錄首頁</a>'
           '<a href="115學測數學_概念地圖.html">🗺️ 概念地圖</a>'
           '<a href="115學測數學_解題線索地圖.html">🧭 線索地圖</a>')
    body = f"""<div class="rv-topbar"><span class="t-title">學測數A · 待複習與錯題</span>{nav}</div>
<div class="rv-wrap">
<div class="rv-hero"><h1>📌 待複習與錯題（考前衝刺）</h1>
<p>一頁看完 <b>11 單元裡所有標記「待複習」的核心概念</b> 與 <b>你答錯過的題目</b>。點「去複習／重測」直達；重測答對後會自動從清單消失。</p></div>
<div class="rv-note"><b>資料來源：</b>你在各單元按的「⚠ 待複習」與答錯的練習題，全部存在<b>這台裝置的瀏覽器</b>裡（換裝置或清除瀏覽資料會歸零）。本頁只是把它們彙整出來。</div>

<div class="rv-sec"><div class="rv-sec-h">⚠ 待複習核心概念 <span class="cnt" id="rev-cnt">0</span></div>
<div id="sec-review"></div></div>

<div class="rv-sec"><div class="rv-sec-h">✗ 答錯過的題目 <span class="cnt" id="wrong-cnt">0</span></div>
<div id="sec-wrong"></div></div>

<div class="rv-foot">複習清單為本機學習輔助；題目全文以大考中心原卷為準。</div>
</div>"""

    js = ("var UM=" + json.dumps(UNITS_META, ensure_ascii=False) + ";"
          "var KN=" + json.dumps(KP_NAV, ensure_ascii=False) + ";"
          "function meta(s){for(var i=0;i<UM.length;i++)if(UM[i].slug===s)return UM[i];return{e:'',t:s,f:'#'};}"
          "function esc(x){return (x||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}"
          "function render(){"
          "var mast,wrong;try{mast=JSON.parse(localStorage.getItem('mm-kp-mastery')||'{}')}catch(e){mast={}}"
          "try{wrong=JSON.parse(localStorage.getItem('mm-wrong')||'{}')}catch(e){wrong={}}"
          # 待複習核心概念：依單元分組
          "var rev={},rc=0;for(var k in mast){if(mast[k]==='review'){var p=k.split(':');"
          "(rev[p[0]]=rev[p[0]]||[]).push(p[1]);rc++;}}"
          "var rh='';UM.forEach(function(m){var ks=rev[m.slug];if(!ks||!ks.length)return;"
          "rh+='<div class=\"rv-uh\">'+m.e+' '+esc(m.t)+'</div>';"
          "ks.forEach(function(kp){var nav=(KN[m.slug]||{})[kp]||kp;"
          "rh+='<div class=\"rv-item\"><span class=\"rv-t\">'+esc(nav)+'</span>"
          "<a class=\"rv-go\" href=\"'+m.f+'#'+kp+'\">去複習 →</a>"
          "<button class=\"rv-x\" onclick=\"unrev(\\''+m.slug+'\\',\\''+kp+'\\')\">✓ 已複習</button></div>';});});"
          "document.getElementById('rev-cnt').textContent=rc;"
          "document.getElementById('sec-review').innerHTML=rc?rh:'<div class=\"rv-empty\">🎉 目前沒有待複習的核心概念！在各單元按「⚠ 待複習」或答錯概念小測時，會出現在這裡。</div>';"
          # 錯題：依單元分組
          "var wg={},wc=0;for(var wk in wrong){var w=wrong[wk];(wg[w.s]=wg[w.s]||[]).push({key:wk,t:w.t,f:w.f,a:w.a});wc++;}"
          "var wh='';UM.forEach(function(m){var arr=wg[m.slug];if(!arr||!arr.length)return;"
          "wh+='<div class=\"rv-uh\">'+m.e+' '+esc(m.t)+'</div>';"
          "arr.forEach(function(w){var href=w.f+(w.a?'#'+w.a:'');"
          "wh+='<div class=\"rv-item\"><span class=\"rv-t\"><span class=\"rv-tag\">'+esc(w.t)+'</span></span>"
          "<a class=\"rv-go retest\" href=\"'+href+'\">重測 →</a>"
          "<button class=\"rv-x\" onclick=\"delw(\\''+w.key+'\\')\">移除</button></div>';});});"
          "document.getElementById('wrong-cnt').textContent=wc;"
          "document.getElementById('sec-wrong').innerHTML=wc?wh:'<div class=\"rv-empty\">🎉 目前沒有答錯的題目！答錯練習題（歷屆／模擬）時，會出現在這裡；重測答對後自動移除。</div>';"
          "}"
          "function unrev(s,kp){try{var m=JSON.parse(localStorage.getItem('mm-kp-mastery')||'{}');delete m[s+':'+kp];"
          "localStorage.setItem('mm-kp-mastery',JSON.stringify(m));}catch(e){}render();}"
          "function delw(key){try{var w=JSON.parse(localStorage.getItem('mm-wrong')||'{}');delete w[key];"
          "localStorage.setItem('mm-wrong',JSON.stringify(w));}catch(e){}render();}"
          "render();")

    og = og_meta("待複習與錯題 · 考前衝刺一頁看完",
                 "一頁彙整 11 單元裡所有待複習核心概念與答錯過的題目，可一鍵去複習／重測。純本機紀錄。",
                 "115學測數學_待複習與錯題.html")
    report_btn = _report_btn({"title": "待複習與錯題"})
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ANALYTICS}<title>學測數A · 待複習與錯題</title>
{og}
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<style>
{css}
{extra}</style>
</head>
<body>
{body}
{PRIVACY_HTML}
{report_btn}
<script src="{KATEX}/katex.min.js"></script>
<script src="{KATEX}/contrib/auto-render.min.js"></script>
<script>{js}</script>
<script>
renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}},{{left:'\\\\[',right:'\\\\]',display:true}}]}});
</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[review] -> {os.path.basename(OUT)}  ({len(UNITS_META)} 單元 nav 已嵌入)")


if __name__ == "__main__":
    build()
