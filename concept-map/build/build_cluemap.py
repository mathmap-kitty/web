# -*- coding: utf-8 -*-
"""解題線索地圖：看到題目線索／關鍵字 → 想到該用的核心概念（跨單元、觸類旁通）。
資料單一來源 content/cues.py（同時餵各核心概念的「🔑 解題線索」標籤）。
"""
import os
import io
import re
import sys
import importlib
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
from build_html import ANALYTICS, PRIVACY_HTML, _report_btn, og_meta, HOME_LINK  # noqa: E402
from render import html_rich  # noqa: E402
from units import UNITS  # noqa: E402
from cues import CATS, CUES, GROUPS  # noqa: E402


def _plain(*parts):
    """把含 LaTeX／markdown 的文字清成可搜尋純文字（保留中文／數字／字母）。"""
    s = " ".join(p for p in parts if p)
    s = re.sub(r"\\[a-zA-Z]+\b", " ", s)      # \dfrac \sqrt ...
    s = re.sub(r"[\\(){}\[\]$*_^|~]", " ", s)  # LaTeX／markdown 符號
    s = re.sub(r"\s+", " ", s)
    return s.strip()

KATEX = "katex"  # 本地離線包，見 build_html.py 同名常數
OUT = os.path.join(ROOT, "dist", "115學測數學_解題線索地圖.html")

BY_SLUG = {u["slug"]: u for u in UNITS}
KP_NAV = {}
for _u in UNITS:
    if os.path.exists(os.path.join(ROOT, "content", _u["slug"] + ".py")):
        try:
            _U = importlib.import_module(_u["slug"]).UNIT
            KP_NAV[_u["slug"]] = {k["id"]: k.get("nav", k.get("title", "")) for k in _U["kps"]}
        except Exception:
            KP_NAV[_u["slug"]] = {}


def _asset(name):
    return io.open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


def _cue_row(c):
    u = BY_SLUG.get(c["unit"], {})
    nav = KP_NAV.get(c["unit"], {}).get(c["kp"], "")
    link = f'{u.get("file", "")}#{c["kp"]}'
    label = f'{u.get("emoji", "")} {u.get("title", "")} · {nav}'
    search = _plain(c["kw"], c["hint"], u.get("title", ""), nav)
    tag = ""  # 「同一招」小標籤（有 g 才顯示）
    if c.get("g"):
        gname = _plain(GROUPS.get(c["g"], c["g"]))
        tag = f'<span class="cue-g" title="{gname}">🔗 {gname}</span>'
    return (f'<div class="cue-row" data-s="{search}"><div class="cue-main">'
            f'<span class="cue-see">看到</span> <b class="cue-k">{html_rich(c["kw"])}</b>{tag}'
            f'<div class="cue-h">→ {html_rich(c["hint"])}</div></div>'
            f'<a class="cue-link" href="{link}">{label} ↗</a></div>')


def _group_section():
    """「同一招、跨單元」總覽（觸類旁通）：每個群組串起它出現的各核心概念。"""
    rows = ""
    for gid, label in GROUPS.items():
        seen, chips = set(), ""
        for c in CUES:
            if c.get("g") != gid:
                continue
            key = (c["unit"], c["kp"])
            if key in seen:
                continue
            seen.add(key)
            u = BY_SLUG.get(c["unit"], {})
            nav = KP_NAV.get(c["unit"], {}).get(c["kp"], "")
            chips += (f'<a class="grp-chip" href="{u.get("file","")}#{c["kp"]}">'
                      f'{u.get("emoji","")} {u.get("title","")}·{nav}</a>')
        rows += (f'<div class="grp-row"><b class="grp-name">{html_rich(label)}</b>'
                 f'<span class="grp-arrow">串起 →</span>{chips}</div>')
    return ('<div class="grp-box"><div class="grp-h">🔗 同一招、跨單元（觸類旁通）'
            '<small>同一個工具在不同單元反覆出現——記一招、通多題</small></div>'
            f'{rows}</div>')


def build():
    by_cat = collections.OrderedDict((cid, []) for cid, _ in CATS)
    for c in CUES:
        by_cat.setdefault(c["cat"], []).append(c)
    cards = ""
    for cid, label in CATS:
        rows = "".join(_cue_row(c) for c in by_cat.get(cid, []))
        cards += (f'<div class="cm-cat"><div class="cm-cat-h">{label}</div>'
                  f'<div class="cm-cat-body">{rows}</div></div>')
    group = _group_section()

    css = _asset("style.css")
    extra = """
  .cl-topbar{position:sticky;top:0;z-index:50;background:rgba(140,39,64,.97);color:#fff;display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 18px;box-shadow:0 2px 10px rgba(0,0,0,.15)}
  .cl-topbar .t-title{font-weight:800;margin-right:auto;font-size:16px;letter-spacing:.5px}
  .cl-topbar a{background:#fff;color:var(--maroon-d);border-radius:20px;padding:5px 13px;font-weight:700;font-size:13.5px;text-decoration:none}
  .clue-wrap{max-width:980px;margin:0 auto;padding:0 16px 70px}
  .clue-hero{text-align:center;padding:24px 0 4px}
  .clue-hero h1{color:var(--maroon);font-size:25px;margin:.1em 0;letter-spacing:.5px}
  .clue-hero p{color:#6b5249;font-size:15px;max-width:700px;margin:.4em auto}
  .clue-note{background:#eef4fb;border:1px dashed #b7cef0;border-radius:12px;padding:10px 16px;font-size:14px;color:#3a4a63;margin:12px 0 16px;line-height:1.85}
  .clue-note b{color:#22406e}
  .cm-cols{column-count:2;column-gap:16px}
  @media(max-width:768px){.cm-cols{column-count:1}}
  .cm-cat{break-inside:avoid;background:#fff;border:1px solid var(--line);border-radius:14px;padding:11px 16px 6px;margin:0 0 16px}
  .cm-cat-h{font-weight:800;color:var(--maroon-d);font-size:16.5px;border-bottom:2px solid #f0e6ea;padding-bottom:7px;margin-bottom:6px}
  .cue-row{display:flex;flex-wrap:wrap;align-items:flex-start;gap:8px;justify-content:space-between;padding:8px 0;border-bottom:1px dashed #eee}
  .cue-row:last-child{border-bottom:none}
  .cue-main{flex:1 1 60%;min-width:0}
  .cue-see{color:#9aa5b0;font-size:12.5px}
  .cue-k{color:#22406e;font-size:15px}
  .cue-h{color:#5a4a52;font-size:13.5px;margin-top:2px;line-height:1.7}
  .cue-link{flex:none;align-self:center;font-size:12.5px;color:#3a5a9a;background:#eef4fb;border:1px solid #cfe0f2;border-radius:16px;padding:3px 11px;text-decoration:none;white-space:nowrap}
  .cue-link:hover{background:#dce8f6}
  .clue-foot{text-align:center;color:#9a8a82;font-size:12.5px;margin-top:26px}
  .cl-search{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:0 0 16px}
  .cl-search input{flex:1;min-width:220px;padding:11px 16px;font-size:15px;font-family:inherit;
    border:1.6px solid #cfe0f2;border-radius:24px;background:#fff;color:#333;outline:none}
  .cl-search input:focus{border-color:#3a5a9a;box-shadow:0 0 0 3px rgba(58,90,154,.12)}
  #clue-count{font-size:13px;color:#3a5a9a;font-weight:700;white-space:nowrap}
  .clue-noresult{background:#fdf1e8;border:1px dashed #e6a76d;border-radius:12px;padding:12px 16px;
    color:#a5642e;font-size:14px;margin:0 0 16px}
  .grp-box{background:#f1f8f4;border:1px solid #cfe6d8;border-radius:14px;padding:12px 16px 8px;margin:0 0 18px}
  .grp-h{font-weight:800;color:#2e6b46;font-size:16px;margin-bottom:8px}
  .grp-h small{display:block;font-weight:600;color:#6a9a7e;font-size:12.5px;margin-top:1px}
  .grp-row{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 8px;padding:7px 0;border-top:1px dashed #d6e8dd}
  .grp-row:first-of-type{border-top:none}
  .grp-name{color:#22406e;font-weight:800;font-size:14.5px}
  .grp-arrow{color:#8aa896;font-size:12.5px}
  .grp-chip{font-size:12.5px;color:#2e6b46;background:#fff;border:1px solid #bfe0cd;border-radius:14px;
    padding:2px 10px;text-decoration:none;white-space:nowrap}
  .grp-chip:hover{background:#eafaf0}
  .cue-g{display:inline-block;margin-left:7px;font-size:11px;color:#2e6b46;background:#eef7f1;
    border:1px solid #cfe6d8;border-radius:10px;padding:0 7px;font-weight:700;vertical-align:1px}
"""
    nav = (HOME_LINK
           + '<a href="index.html">📚 目錄首頁</a>'
           '<a href="115學測數學_待複習與錯題.html">📌 待複習與錯題</a>'
           '<a href="115學測數學_概念地圖.html">🗺️ 概念地圖</a>'
           '<a href="115學測數學_跨單元整合_脈絡地圖.html">🧩 脈絡地圖</a>')
    body = f"""<div class="cl-topbar"><span class="t-title">學測數A · 解題線索地圖</span>{nav}</div>
<div class="clue-wrap">
<div class="clue-hero"><h1>🧭 解題線索地圖</h1>
<p>考試時不知道怎麼下手？別急著找公式——先想「<b>我要求什麼</b>」「<b>題目給了什麼線索</b>」，順著線索就能想到該用的核心概念。</p></div>
<div class="clue-note"><b>怎麼用：</b>卡住不知怎麼下手時，先想「<b>我要求什麼</b>」——在下面搜尋框<b>輸入你在題目看到的字</b>（如「垂直」「極值」「位數」），或往下找分類。點連結直達該核心概念複習。同一招常串起<b>好幾個單元</b>，多看幾次就「觸類旁通」。</div>
<div class="cl-search"><input id="clue-q" type="search" autocomplete="off"
  placeholder="🔍 輸入題目看到的關鍵字，例：垂直、夾角、極值、位數、面積…" oninput="clueFilter()">
<span id="clue-count"></span></div>
{group}
<div id="clue-noresult" class="clue-noresult" style="display:none">找不到相符的線索——換個關鍵字（如「距離」「角度」「機率」），或往下瀏覽分類。</div>
<div class="cm-cols">
{cards}
</div>
<div class="clue-foot">解題線索為教學整理，幫助「把題目線索連到核心概念」；實際題目仍以大考中心原卷為準。</div>
</div>"""

    og = og_meta("解題線索地圖 · 看到關鍵字就想到核心概念",
                 "考試不知如何下手？從『你要求什麼』出發，順著線索找到該用的核心概念——跨單元、觸類旁通。",
                 "115學測數學_解題線索地圖.html")
    report_btn = _report_btn({"title": "解題線索地圖"})
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ANALYTICS}<title>學測數A · 解題線索地圖</title>
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
<script>
renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}},{{left:'\\\\[',right:'\\\\]',display:true}}]}});
</script>
<script>
function clueFilter(){{
 var q=document.getElementById('clue-q').value.trim().toLowerCase();
 var rows=document.querySelectorAll('.cue-row'),n=0;
 rows.forEach(function(r){{var hit=!q||(r.dataset.s||'').toLowerCase().indexOf(q)>=0;
  r.style.display=hit?'':'none';if(hit)n++;}});
 document.querySelectorAll('.cm-cat').forEach(function(cat){{
  var any=[].slice.call(cat.querySelectorAll('.cue-row')).some(function(r){{return r.style.display!=='none';}});
  cat.style.display=any?'':'none';}});
 document.getElementById('clue-count').textContent=q?('找到 '+n+' 條'):'';
 document.getElementById('clue-noresult').style.display=(q&&n===0)?'':'none';
 var gb=document.querySelector('.grp-box');if(gb)gb.style.display=q?'none':'';
}}
</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[cluemap] -> {os.path.basename(OUT)}  ({len(CUES)} 條線索 / {len(CATS)} 類)")


if __name__ == "__main__":
    build()
