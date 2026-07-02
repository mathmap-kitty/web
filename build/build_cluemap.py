# -*- coding: utf-8 -*-
"""解題線索地圖：看到題目線索／關鍵字 → 想到該用的知識點（跨單元、觸類旁通）。
資料單一來源 content/cues.py（同時餵各考點的「🔑 解題線索」標籤）。
"""
import os
import io
import sys
import importlib
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
from build_html import ANALYTICS, PRIVACY_HTML, _report_btn, og_meta  # noqa: E402
from render import html_rich  # noqa: E402
from units import UNITS  # noqa: E402
from cues import CATS, CUES  # noqa: E402

KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"
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
    return (f'<div class="cue-row"><div class="cue-main">'
            f'<span class="cue-see">看到</span> <b class="cue-k">{html_rich(c["kw"])}</b>'
            f'<div class="cue-h">→ {html_rich(c["hint"])}</div></div>'
            f'<a class="cue-link" href="{link}">{label} ↗</a></div>')


def build():
    by_cat = collections.OrderedDict((cid, []) for cid, _ in CATS)
    for c in CUES:
        by_cat.setdefault(c["cat"], []).append(c)
    cards = ""
    for cid, label in CATS:
        rows = "".join(_cue_row(c) for c in by_cat.get(cid, []))
        cards += f'<div class="cm-cat"><div class="cm-cat-h">{label}</div>{rows}</div>'

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
"""
    nav = ('<a href="index.html">📚 首頁</a>'
           '<a href="115學測數學_概念地圖.html">🗺️ 概念地圖</a>'
           '<a href="115學測數學_跨單元整合_脈絡地圖.html">🧩 脈絡地圖</a>')
    body = f"""<div class="cl-topbar"><span class="t-title">學測數A · 解題線索地圖</span>{nav}</div>
<div class="clue-wrap">
<div class="clue-hero"><h1>🧭 解題線索地圖</h1>
<p>考試時不知道怎麼下手？別急著找公式——先想「<b>我要求什麼</b>」「<b>題目給了什麼線索</b>」，順著線索就能想到該用的知識點。</p></div>
<div class="clue-note"><b>怎麼用：</b>從下面找到你題目的「線索關鍵字」→ 看它指向哪個知識點與怎麼用 → 點右邊連結直達該考點複習。同一個線索常串起<b>好幾個單元</b>的工具，多看幾次就會「觸類旁通」。</div>
<div class="cm-cols">
{cards}
</div>
<div class="clue-foot">解題線索為教學整理，幫助「把題目線索連到知識點」；實際題目仍以大考中心原卷為準。</div>
</div>"""

    og = og_meta("解題線索地圖 · 看到關鍵字就想到知識點",
                 "考試不知如何下手？從『你要求什麼』出發，順著線索找到該用的知識點——跨單元、觸類旁通。",
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
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[cluemap] -> {os.path.basename(OUT)}  ({len(CUES)} 條線索 / {len(CATS)} 類)")


if __name__ == "__main__":
    build()
