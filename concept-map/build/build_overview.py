# -*- coding: utf-8 -*-
"""網站內容總覽頁（獨立頁，非單元頁）：章節 → 各考點 → 各考點列的歷屆考題。
資料直接讀 content/*.py 單一來源（數字不手抄）。輸出 dist/content-overview.html。
與「考題變化趨勢」頁互相連結，成一組獨立分析頁；先不接進 mathmap 導覽。
"""
import os
import io
import re
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
from render import html_rich  # noqa: E402
from units import UNITS  # noqa: E402
from build_html import (CONTINUE_BANNER_HTML, CONTINUE_CSS, CONTINUE_JS,  # noqa: E402  繼續上次進度橫幅
                        EXPORT_BUTTON_HTML, EXPORT_MODAL_HTML, EXPORT_CSS, EXPORT_JS,  # 匯出學習紀錄
                        HOME_LINK)  # 「🏠 網站首頁」pill
try:
    from units import SECTIONS
except Exception:
    SECTIONS = None

OUT = os.path.join(ROOT, "dist", "content-overview.html")
TREND_FILE = "exam-trend-analysis.html"

BY_SLUG = {u["slug"]: u for u in UNITS}


def is_exam(tag):
    """歷屆大考題：tag 以 106–115 年份開頭（含舊制／數A／數B）。"""
    return bool(re.match(r"\s*(10[6-9]|11[0-5])", tag or ""))


def collect():
    """回傳每個單元的結構資料：考點、歷屆題、範例、混合題、Part2 題數。"""
    data = []
    tot_kp = tot_exam = tot_ex = tot_mixed = tot_p2 = 0
    for u in UNITS:
        slug = u["slug"]
        if not os.path.exists(os.path.join(ROOT, "content", slug + ".py")):
            continue
        U = importlib.import_module(slug).UNIT
        kps = []
        for kp in U["kps"]:
            exam, ex = [], []
            for q in kp.get("questions", []):
                tag = q.get("tag", "?")
                if "subqs" in q:
                    tag += "（題組）"
                (exam if is_exam(tag) else ex).append(tag)
            kps.append({"id": kp["id"], "num": kp["num"],
                        "nav": kp.get("nav", kp.get("title", "")),
                        "exam": exam, "ex": ex})
            tot_kp += 1
            tot_exam += len(exam)
            tot_ex += len(ex)
        # 混合題
        mixed_groups = []
        mx = U.get("mixed")
        if mx:
            for g in (mx if isinstance(mx, list) else [mx]):
                items = g.get("items", [])
                mixed_groups.append({"src": g.get("src", ""),
                                     "tags": [it.get("tag", "?") for it in items]})
                tot_mixed += len(items)
        # Part2 題數
        p2n = 0
        if U.get("part2"):
            p2n = sum(len(g.get("questions", [])) for g in U["part2"].get("groups", []))
        tot_p2 += p2n
        trend = ""
        if U.get("part0") and U["part0"].get("trend_table"):
            trend = U["part0"]["trend_table"].get("total", "")
        data.append({"slug": slug, "emoji": u.get("emoji", ""), "title": u["title"],
                     "file": u["file"], "trend": trend, "kps": kps,
                     "mixed": mixed_groups, "p2n": p2n})
    stats = {"units": len(data), "kp": tot_kp, "exam": tot_exam, "ex": tot_ex,
             "mixed": tot_mixed, "p2": tot_p2}
    return data, stats


def _qtag(file, kpid, tag, exam):
    if exam:
        return f'<a class="ov-q exam" href="{file}#{kpid}">{html_rich(tag)}</a>'
    return f'<span class="ov-q ex">{html_rich(tag)}</span>'


def _unit_card(d):
    kprows = ""
    for kp in d["kps"]:
        qs = "".join(_qtag(d["file"], kp["id"], t, True) for t in kp["exam"])
        qs += "".join(_qtag(d["file"], kp["id"], t, False) for t in kp["ex"])
        if not qs:
            qs = '<span class="ov-none">（此考點目前無歷屆題）</span>'
        badge = f'<span class="ov-kpn">歷屆 {len(kp["exam"])}</span>' if kp["exam"] else \
                '<span class="ov-kpn zero">歷屆 0</span>'
        kprows += (f'<div class="ov-kp"><div class="ov-kp-h">'
                   f'<a href="{d["file"]}#{kp["id"]}">{kp["num"]} · {html_rich(kp["nav"])}</a>{badge}</div>'
                   f'<div class="ov-qs">{qs}</div></div>')
    mixed = ""
    if d["mixed"]:
        rows = ""
        for g in d["mixed"]:
            tags = "、".join(html_rich(t) for t in g["tags"])
            rows += f'<div class="ov-mx-row"><b>{html_rich(g["src"])}</b><span>{tags}</span></div>'
        mixed = (f'<div class="ov-mixed"><div class="ov-mx-h">🖊 混合題實戰</div>{rows}</div>')
    exam_n = sum(len(k["exam"]) for k in d["kps"])
    return (f'<div class="ov-unit" id="ov-{d["slug"]}">'
            f'<div class="ov-unit-h"><a href="{d["file"]}">{d["emoji"]} {html_rich(d["title"])}</a>'
            f'<small>近十年 {d["trend"]} 題 ｜ {len(d["kps"])} 考點 ｜ 歷屆 {exam_n} 題 ｜ 模擬 {d["p2n"]} 題</small></div>'
            f'{kprows}{mixed}</div>')


def build():
    data, st = collect()

    # 章節分組（首頁四大主題）
    sec_html = ""
    if SECTIONS:
        for label, slugs in SECTIONS:
            chips = "".join(
                f'<a class="sec-chip" href="#ov-{s}">{BY_SLUG[s].get("emoji","")} {BY_SLUG[s]["title"]}</a>'
                for s in slugs if s in BY_SLUG)
            sec_html += f'<div class="sec-row"><b class="sec-name">{label}</b>{chips}</div>'

    cards = "".join(_unit_card(d) for d in data)

    # 無歷屆題的考點（動態列出）
    zero = []
    for d in data:
        for kp in d["kps"]:
            if not kp["exam"]:
                zero.append(f'{d["emoji"]} {d["title"]}「{kp["num"]} · {html_rich(kp["nav"])}」')
    if zero:
        zero_note = (f'<b>無歷屆題的考點（共 {len(zero)} 個）：</b>' + "、".join(zero) +
                     '。多因 111–115 沒有以該主題為主的數A題，故以教學範例呈現；其餘 '
                     f'{st["kp"] - len(zero)} 個考點都有歷屆題支撐。')
    else:
        zero_note = f'{st["kp"]} 個考點都有歷屆題支撐。'

    css = """
:root{--maroon:#8c2740;--maroon-d:#6f1f33;--page:#f7f2ee;--card:#fff;--line:#e7dcd6;
--ink:#2b2b2b;--sub:#6b5249;--blue:#3a5a9a;--teal:#1f6f78}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);line-height:1.85;
font-family:"Microsoft JhengHei","PingFang TC","Noto Sans TC","Segoe UI",system-ui,sans-serif}
.topbar{position:sticky;top:0;z-index:10;background:rgba(140,39,64,.97);color:#fff;
padding:11px 20px;box-shadow:0 2px 10px rgba(0,0,0,.15);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.topbar b{font-size:16px;letter-spacing:.5px;margin-right:auto}
.topbar a{color:#fff;background:rgba(255,255,255,.16);border-radius:18px;padding:5px 13px;
font-size:13.5px;text-decoration:none}
.topbar a:hover{background:rgba(255,255,255,.28)}
.wrap{max-width:960px;margin:0 auto;padding:0 18px 70px}
.hero{text-align:center;padding:26px 0 6px}
.hero h1{color:var(--maroon);font-size:26px;margin:.15em 0;letter-spacing:.5px}
.hero p{color:var(--sub);font-size:15px;margin:.4em auto;max-width:680px}
.src{font-size:12.5px;color:#9a857c;margin-top:6px}
.cards{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:18px 0 6px}
.mc{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 16px;min-width:112px;text-align:center}
.mc .lbl{font-size:12px;color:var(--sub)}
.mc .val{font-size:22px;font-weight:800;color:var(--maroon-d);margin-top:2px}
h2{color:var(--maroon-d);font-size:19px;border-left:5px solid var(--maroon);padding-left:10px;margin:32px 0 10px}
.secbox{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px 16px 8px;margin:10px 0 6px}
.sec-row{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 8px;padding:7px 0;border-top:1px dashed #eee}
.sec-row:first-child{border-top:none}
.sec-name{color:var(--maroon-d);font-weight:800;font-size:14.5px;min-width:150px}
.sec-chip{font-size:13px;color:var(--blue);background:#eef4fb;border:1px solid #cfe0f2;border-radius:14px;padding:2px 11px;text-decoration:none;white-space:nowrap}
.sec-chip:hover{background:#dce8f6}
.pages{background:#eef4fb;border:1px dashed #b7cef0;border-radius:12px;padding:11px 16px;font-size:14px;color:#3a4a63;margin:10px 0;line-height:2}
.pages a{color:var(--blue);font-weight:700;text-decoration:none;border-bottom:1.5px solid #b7cef0}
.ov-unit{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 18px 10px;margin:0 0 16px}
.ov-unit-h{border-bottom:2px solid #f0e6ea;padding-bottom:8px;margin-bottom:8px}
.ov-unit-h a{color:var(--maroon-d);font-size:18px;font-weight:800;text-decoration:none}
.ov-unit-h small{display:block;color:#9a857c;font-size:12.5px;font-weight:600;margin-top:2px}
.ov-kp{padding:8px 0;border-bottom:1px dashed #eee}
.ov-kp:last-of-type{border-bottom:none}
.ov-kp-h{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.ov-kp-h a{color:#22406e;font-weight:800;font-size:15px;text-decoration:none}
.ov-kp-h a:hover{text-decoration:underline}
.ov-kpn{font-size:11.5px;color:#2e6b46;background:#eef7f1;border:1px solid #cfe6d8;border-radius:10px;padding:0 8px;font-weight:700}
.ov-kpn.zero{color:#b06636;background:#fdf1e8;border-color:#e6c6a8}
.ov-qs{margin-top:5px;display:flex;flex-wrap:wrap;gap:6px}
.ov-q{font-size:12.5px;border-radius:12px;padding:2px 10px;white-space:nowrap;line-height:1.7}
.ov-q.exam{color:var(--maroon-d);background:#fbf1f4;border:1px solid #eccdd6;text-decoration:none}
.ov-q.exam:hover{background:#f6e2e9}
.ov-q.ex{color:#7a6a70;background:#f4f0f1;border:1px dashed #ddd0d5}
.ov-none{font-size:12.5px;color:#b06636}
.ov-mixed{margin-top:9px;padding-top:8px;border-top:1px dashed #e6cf94}
.ov-mx-h{font-weight:800;color:#9a6b00;font-size:13.5px;margin-bottom:4px}
.ov-mx-row{font-size:13px;color:#5a4a52;display:flex;flex-wrap:wrap;gap:4px 10px;margin:2px 0}
.ov-mx-row b{color:#22406e}
.note{background:#eef6f4;border:1px solid #cfe6e2;border-radius:12px;padding:11px 16px;font-size:14px;color:#2c5158;margin:14px 0}
.foot{text-align:center;color:#9a8a82;font-size:12.5px;margin-top:30px}
@media(max-width:600px){.ov-q{white-space:normal}}
"""

    body = f"""<div class="topbar"><b>學測數A · 內容總覽</b>
{HOME_LINK}<a href="{TREND_FILE}">📊 考題變化趨勢 →</a>
<span style="font-size:12.5px;opacity:.8">獨立頁 · 教學用</span></div>
<div class="wrap">
<div class="hero">
<h1>這個網站有哪些內容？</h1>
<p>一頁看完全站結構：<b>{st['units']} 個單元 · {st['kp']} 個考點</b>，以及每個考點列了哪些歷屆大考題。點任一項可直達該考點。</p>
<div class="src">資料由 content/*.py 單一來源自動彙整（數字非手抄）· 搭配「考題變化趨勢」頁一起看</div>
</div>

{CONTINUE_BANNER_HTML}
{EXPORT_BUTTON_HTML}

<div class="cards">
<div class="mc"><div class="lbl">單元</div><div class="val">{st['units']}</div></div>
<div class="mc"><div class="lbl">考點</div><div class="val">{st['kp']}</div></div>
<div class="mc"><div class="lbl">歷屆考題</div><div class="val">{st['exam']}</div></div>
<div class="mc"><div class="lbl">混合題（非選）</div><div class="val">{st['mixed']}</div></div>
<div class="mc"><div class="lbl">模擬實戰</div><div class="val">{st['p2']}</div></div>
<div class="mc"><div class="lbl">教學範例</div><div class="val">{st['ex']}</div></div>
</div>

<h2>網站地圖</h2>
<div class="pages"><b>入口與地圖：</b>
<a href="index.html">📚 目錄首頁</a>　·
<a href="115學測數學_待複習與錯題.html">📌 待複習與錯題</a>　·
<a href="115學測數學_概念地圖.html">🗺️ 概念地圖</a>　·
<a href="115學測數學_跨單元整合_脈絡地圖.html">🧩 跨單元脈絡地圖</a>　·
<a href="115學測數學_解題線索地圖.html">🧭 解題線索地圖</a>　·
<a href="{TREND_FILE}">📊 考題變化趨勢</a>
<br><b>單元頁結構：</b>Part 0 出題趨勢 → Part 1 各考點（先備・重點公式・常見誤解・示範例・<b>歷屆試題</b>・確認理解） → 混合題實戰 → Part 2 模擬實戰 → Part 3 考前速查。</div><div style="text-align:center;font-size:12.5px;color:#9a857c;padding:0 14px 30px">mathmap 數學地圖 © Kitty</div>

<h2>四大主題分組</h2>
<div class="secbox">{sec_html}</div>

<h2>各單元 × 考點 × 歷屆考題</h2>
<p style="color:#6b5249;font-size:14px;margin:.2em 0 12px">
<span class="ov-q exam" style="cursor:default">紅底＝歷屆大考題（可點連結）</span>
<span class="ov-q ex" style="cursor:default">灰底＝教學範例</span>
　年份 106–115（111 起為 108 課綱數A，已完整列入；早年以舊制／數B 補足對應主題）。</p>
{cards}

<div class="note">{zero_note}</div>

<div class="foot">內容總覽由單一來源自動生成；題目全文以大考中心原卷為準。</div>
</div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>學測數A · 內容總覽（章節・考點・歷屆考題）</title>
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<link rel="stylesheet" href="katex/katex.min.css">
<style>{css}
{CONTINUE_CSS}
{EXPORT_CSS}</style>
</head>
<body>
{body}
{EXPORT_MODAL_HTML}
<script>{CONTINUE_JS}</script>
<script>{EXPORT_JS}</script>
<script src="katex/katex.min.js"></script>
<script src="katex/contrib/auto-render.min.js"></script>
<script>
renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}},{{left:'\\\\[',right:'\\\\]',display:true}}]}});
</script>
</body>
</html>"""

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[overview] -> {os.path.basename(OUT)}  "
          f"({st['units']} 單元 / {st['kp']} 考點 / 歷屆 {st['exam']} / 混合 {st['mixed']})")


if __name__ == "__main__":
    build()
