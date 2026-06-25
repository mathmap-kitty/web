# -*- coding: utf-8 -*-
"""單一來源 (YAML) -> 互動學習網頁（單一 HTML，內嵌 CSS/JS，KaTeX 由 CDN 載入）。

視覺與既有矩陣頁一致：CSS/JS 直接重用 build/assets/。
"""
import os
import io
from render import html_rich

HERE = os.path.dirname(os.path.abspath(__file__))
KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"

# 已讀進度（考點層，localStorage 鍵 mm-read-kps，格式 "slug:kpN"，與概念地圖共用）
PROGRESS_JS = (
    "var RK='mm-read-kps';"
    "function gR(){try{return new Set(JSON.parse(localStorage.getItem(RK)||'[]'))}catch(e){return new Set()}}"
    "function kpToggle(b){var k=MMSLUG+':'+b.dataset.kp;var s=gR();var on=!s.has(k);on?s.add(k):s.delete(k);"
    "localStorage.setItem(RK,JSON.stringify([...s]));upUnit();}"
    "function upUnit(){var s=gR();var done=MMKPS.filter(k=>s.has(MMSLUG+':'+k)).length,t=MMKPS.length;"
    "document.querySelectorAll('.kpchk').forEach(b=>b.classList.toggle('on',s.has(MMSLUG+':'+b.dataset.kp)));"
    "var tx=document.getElementById('up-txt');if(tx)tx.textContent=done+' / '+t;"
    "var bar=document.getElementById('up-bar');if(bar)bar.style.width=(t?done/t*100:0)+'%';}"
    "function markAllKp(){var s=gR();var all=MMKPS.every(k=>s.has(MMSLUG+':'+k));"
    "MMKPS.forEach(k=>{var key=MMSLUG+':'+k;all?s.delete(key):s.add(key);});"
    "localStorage.setItem(RK,JSON.stringify([...s]));upUnit();}"
    "upUnit();")


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

# 頁尾隱私說明（GA／Clarity 流量統計告知），全站一致；要改文案：這裡＋三個靜態檔（index、概念地圖、脈絡地圖）。
PRIVACY_HTML = ('<div style="text-align:center;font-size:12px;color:#9a857c;'
                'padding:16px 14px 28px;line-height:1.7">本站使用 Google Analytics 與 '
                'Microsoft Clarity 統計匿名流量，藉以了解使用情況、持續改善內容。</div>')


def _asset(name):
    return io.open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


def _opts_html(options):
    if not options:
        return ""
    spans = "".join(f"<span>({i}) {html_rich(o)}</span>" for i, o in enumerate(options, 1))
    return f'<div class="opts">{spans}</div>'


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


def _question_html(q, first=False):
    meta_style = ' style="margin-top:0"' if first else ""
    core = f'<span class="core">解題核心：{html_rich(q["core"])}</span>' if q.get("core") else ""
    meta = (f'<div class="q-meta"{meta_style}>'
            f'<span class="tag">{html_rich(q["tag"])}</span>'
            f'<span class="lv">{q["level"]}</span>{core}</div>')
    body = f'<div class="q-body">{html_rich(q["body"])}{_table_html(q.get("table"))}{_opts_html(q.get("options"))}</div>'
    btn = ('<button class="sol-btn" data-s="顯示解答" data-h="隱藏解答" '
           'onclick="ts(this)">顯示解答</button>')
    sol = f'<div class="sol">{_solution_html(q.get("solution"))}</div>'
    return meta + body + btn + sol


def _subq_html(sq):
    """混合題組的子題。"""
    body = f'<div class="q-body subq"><b>{html_rich(sq["label"])}</b>{html_rich(sq.get("body",""))}</div>'
    btn = ('<button class="sol-btn" data-s="顯示解答" data-h="隱藏解答" '
           'onclick="ts(this)">顯示解答</button>')
    sol = f'<div class="sol">{_solution_html(sq.get("solution"))}</div>'
    return body + btn + sol


def _point_html(p):
    if isinstance(p, dict) and "svg" in p:
        cap = f'<figcaption>{html_rich(p["caption"])}</figcaption>' if p.get("caption") else ""
        # 圖寬四段：預設 155px（小圖）／med 250px／wide 362px／full 560px（大型概念圖）
        style = ' style="max-width:560px"' if p.get("full") else (
            ' style="max-width:362px"' if p.get("wide") else (
            ' style="max-width:250px"' if p.get("med") else ""))
        return f'<li class="figli"><figure class="tfig"{style}>{p["svg"]}{cap}</figure></li>'
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


def _kp_html(kp):
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
            qs += _question_html(q, first=(i == 0 and False))
    strategy = ""
    if kp.get("strategy"):
        s = kp["strategy"]
        if isinstance(s, (list, tuple)):
            inner = "".join(f'<div class="sln">{html_rich(x)}</div>' for x in s)
        else:
            inner = html_rich(s)
        strategy = f'<span class="label">解題策略</span><div class="callout">{inner}</div>'
    selfcheck = ""
    sc = kp.get("selfcheck")
    if sc:
        ans = "".join(f'<p>{html_rich(x)}</p>' for x in sc["a"]) if isinstance(sc["a"], (list, tuple)) \
            else f'<p>{html_rich(sc["a"])}</p>'
        selfcheck = ('<div class="selfcheck">'
                     '<div class="sc-head">⏱ 1 分鐘自我檢查</div>'
                     f'<div class="sc-q">{html_rich(sc["q"])}</div>'
                     '<button class="sol-btn" data-s="看答案" data-h="收起答案" '
                     'onclick="ts(this)">看答案</button>'
                     f'<div class="sol">{ans}</div></div>')
    return (f'<div class="card" id="{kp["id"]}">'
            f'<p class="kp"><button class="kpchk" data-kp="{kp["id"]}" onclick="kpToggle(this)" '
            f'title="標記此考點已讀" aria-label="標記已讀"></button>'
            f'<span class="num">{kp["num"]}</span>{html_rich(kp["title"])}</p>'
            f'<div class="callout"><b>◆ 這個考點在學什麼：</b>{html_rich(kp["intro"])}</div>'
            f'<span class="label">重點與公式</span><ul class="points">{points}</ul>'
            f'{tables}'
            f'{mis}'
            f'<span class="label">歷屆試題</span>{qs}'
            f"{strategy}{selfcheck}</div>")


def _question_intro_html(q):
    """題組的共同題幹。"""
    core = f'<span class="core">解題核心：{html_rich(q["core"])}</span>' if q.get("core") else ""
    meta = (f'<div class="q-meta"><span class="tag">{html_rich(q["tag"])}</span>'
            f'<span class="lv">{q["level"]}</span>{core}</div>')
    body = f'<div class="q-body">{html_rich(q["body"])}</div>'
    return meta + body


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
            '<div class="card">'
            '<span class="label">近十年出題趨勢（106–115）</span>'
            f"{table}"
            f'<span class="label">趨勢解讀</span><ul class="points">{notes}</ul>'
            f"{mp}{fig}</div>")


def _part2_html(p2):
    if not p2:
        return ""
    groups = ""
    for g in p2["groups"]:
        items = ""
        for j, q in enumerate(g["questions"]):
            items += _question_html(q, first=(j == 0))
        groups += f'<span class="label">{g["title"]}</span>{items}'
    return (f'<div class="part" id="part2">Part 2　喚起行動：模擬實戰（{p2.get("count","")}題）'
            f'<small>{p2.get("note","")}</small></div><div class="card">{groups}</div>')


def _part3_html(p3):
    if not p3:
        return ""
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
            f'<div class="card">{ref}{chk}</div>')


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
                 '<option value="115學測數學_概念地圖.html">🗺️ 概念地圖</option>',
                 '<option value="115學測數學_跨單元整合_脈絡地圖.html">🧩 跨單元脈絡地圖</option>']
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
    kp_opts.append('<option value="part2">Part 2 · 模擬實戰</option>')
    kp_opts.append('<option value="part3">Part 3 · 考前速查</option>')
    return (f'<div class="toolbar"><span class="t-title">{unit["title"]}</span>'
            f'<select class="nav-select" onchange="if(this.value){{location.href=this.value;}}">'
            f'{"".join(unit_opts)}</select>'
            f'<select class="nav-select" onchange="if(this.value){{location.hash=this.value;this.selectedIndex=0;}}">'
            f'{"".join(kp_opts)}</select>'
            '<button onclick="revealAll()">全部顯示解答</button>'
            '<button onclick="hideAll()">全部隱藏</button></div>')


def build_html(unit, units):
    css = _asset("style.css")
    js = _asset("app.js")
    kps_html = "".join(_kp_html(kp) for kp in unit["kps"])
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
            f'{_part0_html(unit.get("part0"))}'
            '<div class="part">Part 1　建構概念：'
            f'{unit.get("part1_label","五大考點")} <small>先把觀念與公式打穩，再上戰場</small></div>'
            f'{kps_html}'
            f'{_part2_html(unit.get("part2"))}'
            f'{_part3_html(unit.get("part3"))}'
            f'<div class="foot">{unit.get("foot","")}</div>')
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ANALYTICS}<title>{unit.get("page_title", unit["title"])}</title>
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
<script src="{KATEX}/katex.min.js"></script>
<script src="{KATEX}/contrib/auto-render.min.js"></script>
<script>
{js}</script>
<script>
window.MMSLUG="{unit["slug"]}";window.MMKPS={[k["id"] for k in unit["kps"]]};
{PROGRESS_JS}</script>
</body>
</html>
"""
