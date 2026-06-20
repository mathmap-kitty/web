# -*- coding: utf-8 -*-
"""跨單元整合題 · 脈絡地圖。

資料來源：參考文件/學測數學考題分析_106-115_更正版.xlsx 的「跨單元清單」分頁。
題目資料（年度/題號/單元配對/核心概念/難易）逐筆取自 Excel；
分組主題與「脈絡」敘述為教學編排。視覺重用 build/assets/style.css。
"""
import os, io, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"
XLSX = os.path.join(ROOT, "參考文件", "學測數學考題分析_106-115_更正版.xlsx")
OUT = os.path.join(ROOT, "dist", "115學測數學_跨單元整合_脈絡地圖.html")

sys.path.insert(0, os.path.join(ROOT, "content"))


def _asset(name):
    return io.open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


# 單元名稱 → 對應單元頁（可點按跳轉）
UNIT_FILE = {
    "數與式": "115學測數學_數與式_互動學習.html",
    "多項式函數": "115學測數學_多項式函數_互動學習.html",
    "指數與對數": "115學測數學_指數與對數_互動學習.html",
    "數列級數": "115學測數學_數列與級數_互動學習.html",
    "排列組合": "115學測數學_排列組合與機率_互動學習.html",
    "機率期望值": "115學測數學_排列組合與機率_互動學習.html",
    "數據分析": "115學測數學_數據分析_互動學習.html",
    "三角比": "115學測數學_三角_互動學習.html",
    "三角函數": "115學測數學_三角_互動學習.html",
    "平面向量": "115學測數學_平面向量_互動學習.html",
    "空間向量": "115學測數學_空間向量_互動學習.html",
    "空間的平面與直線": "115學測數學_空間向量_互動學習.html",
    "矩陣": "115學測數學_矩陣_互動學習.html",
}

# 主題（脈絡）→ 成員題目 key（"學年度|卷別|題號"），各主題內依年度排序
THEMES = [
    ("① 向量：跨單元之王",
     "向量最會「串門子」——它把長度、角度、面積全化成坐標與內積運算，於是能和三角、多項式、數與式、指對數通通結合。看到向量題，先想「能不能坐標化」。",
     ["107|數A|10", "107|數A|G", "108|數A|G", "111|數B|14",
      "111|數B|4", "113|數B|4", "115|數A|14"]),
    ("② 三角：比與函數的縫合",
     "「三角比」管直角三角形與測量、「三角函數」管廣義角與恆等式。學測常把兩者縫在一起：先用正/餘弦定理算邊角，再用倍角、和角化簡——多項式的對稱性也常來軋一腳。",
     ["109|數A|G", "113|數A|6", "115|數A|17", "109|數A|7"]),
    ("③ 數列：規律與成長的離散版",
     "數列是「離散的函數」。它的規律常藏在二次函數、指數成長（指對數）裡；一旦要求和，又會碰上計數原理——所以數列題天生愛跨界。",
     ["106|數A|A", "107|數A|5", "110|數A|2", "113|數A|8",
      "113|數B|17", "115|數A|3"]),
    ("④ 機率：計數與資料的十字路口",
     "機率的分母來自排列組合的計數，分子常牽涉矩陣（解聯立）、指對數（估量級）或數據（列聯表）。它正站在「計數 × 資料」的交會點。",
     ["109|數A|6", "113|數A|11", "114|數B|4", "114|數B|13", "115|數B|15"]),
    ("⑤ 空間：把平面升一個維度",
     "空間題把平面的畢氏、餘弦定理、向量「升一維」，再加上點到平面距離、外積、二面角——常是壓軸難題，務必先畫圖、建坐標。",
     ["107|數A|H", "111|數A|17", "111|數B|6"]),
]

DIFF_CLASS = {"易": "easy", "中": "mid", "難": "hard"}


def _load_rows():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["跨單元清單"]
    rows = {}
    for r in range(2, ws.max_row + 1):
        v = [ws.cell(r, c).value for c in range(1, 9)]
        if not any(x is not None for x in v):
            continue
        yr, juan, num, typ, main, cross, concept, diff = v
        key = f"{yr}|{juan}|{str(num)}"
        rows[key] = dict(yr=yr, juan=juan, num=str(num), typ=typ or "",
                         main=main or "", cross=cross or "",
                         concept=concept or "", diff=(diff or "").strip())
    return rows


def _utag(name):
    f = UNIT_FILE.get(name)
    if f:
        return f'<a class="utag" href="{f}">{name}</a>'
    return f'<span class="utag dead">{name}</span>'


def _card(row):
    d = DIFF_CLASS.get(row["diff"], "mid")
    juan = row["juan"]
    return (
        f'<div class="xq" data-juan="{juan}">'
        f'<div class="xq-head">'
        f'<span class="yr">{row["yr"]} {juan}</span>'
        f'<span class="qn">{row["typ"]} {row["num"]}</span>'
        f'<span class="lv {d}">{row["diff"]}</span>'
        f'</div>'
        f'<div class="xq-units">{_utag(row["main"])}<span class="x">×</span>{_utag(row["cross"])}</div>'
        f'<div class="xq-concept">{row["concept"]}</div>'
        f'</div>'
    )


def build():
    rows = _load_rows()
    used = set()
    sections = []
    for title, ctx, keys in THEMES:
        cards = []
        for k in keys:
            if k not in rows:
                raise SystemExit(f"Excel 找不到題目 key：{k}")
            used.add(k)
            cards.append(_card(rows[k]))
        sections.append(
            f'<div class="part">{title}<small>{len(keys)} 題</small></div>'
            f'<div class="callout ctx">{ctx}</div>'
            f'<div class="xq-grid">{"".join(cards)}</div>'
        )
    # 確認沒有漏掉 Excel 裡的題目
    missing = [k for k in rows if k not in used]
    if missing:
        raise SystemExit(f"有 {len(missing)} 題未編入主題：{missing}")

    nA = sum(1 for r in rows.values() if r["juan"] == "數A")
    nB = len(rows) - nA
    css = _asset("style.css")
    extra = """
  .x-intro{background:#fff7ef;border:1px dashed #e0b9a6;border-radius:12px;padding:12px 18px;margin:14px 0 8px;font-size:14.5px;color:#6b5249}
  .x-intro b{color:var(--maroon)}
  .filterbar{display:flex;gap:8px;align-items:center;margin:14px 0 4px;flex-wrap:wrap}
  .filterbar .fb-label{font-weight:700;color:var(--maroon-d);font-size:14px}
  .filterbar button{background:#fff;color:var(--maroon-d);border:1.5px solid var(--maroon);border-radius:20px;padding:5px 16px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;transition:.15s}
  .filterbar button.on{background:var(--maroon);color:#fff}
  .callout.ctx{font-size:14.5px;line-height:1.8}
  .xq-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:12px;margin:8px 0 6px}
  .xq{background:#fff;border-radius:12px;padding:12px 14px;box-shadow:0 2px 8px rgba(80,40,30,.07);border-left:4px solid var(--btn)}
  .xq[data-juan="數B"]{border-left-color:#b0853a;background:#fffdf7}
  .xq-head{display:flex;align-items:center;gap:8px;margin-bottom:7px}
  .xq-head .yr{font-weight:800;color:var(--maroon);font-size:14.5px}
  .xq-head .qn{font-size:12.5px;color:#6b5249;background:#f3e3e8;border-radius:6px;padding:1px 8px}
  .xq-head .lv{margin-left:auto;font-size:12px;font-weight:700;border-radius:6px;padding:1px 9px;color:#fff}
  .lv.easy{background:#3a9d6b}.lv.mid{background:#d39a2a}.lv.hard{background:#c0392b}
  .xq-units{margin:2px 0 6px;font-size:15px;font-weight:700}
  .xq-units .x{color:#b08;margin:0 6px;font-weight:800}
  .utag{color:var(--btn);text-decoration:none;border-bottom:1.5px solid #bfe0dd}
  .utag:hover{background:var(--btn-bg)}
  .utag.dead{color:#999;border:none;font-weight:600}
  .xq-concept{font-size:13.5px;color:#5a4a52;line-height:1.7}
  .xstat{display:flex;gap:18px;flex-wrap:wrap;font-size:13.5px;color:#6b5249;margin:6px 0 2px}
  .xstat b{color:var(--maroon);font-size:18px}
"""
    body = f"""<div class="hero"><h1>跨單元整合 · 脈絡地圖</h1>
<p>學測數學 106–115　共 {len(rows)} 道「跨單元」考題，依<b>結合的概念主軸</b>分成五大脈絡</p></div>
<div class="x-intro">
<b>為什麼要看跨單元題？</b>　近年學測越來越愛把兩個單元縫在一起——會單一公式不夠，要看出「這題其實是 A × B」。
這頁把 106–115 的跨單元題依<b>「誰跟誰結合、為什麼結合」</b>排成五條脈絡；每張卡片可點<b>單元名稱</b>直接跳到該單元複習。
<div class="xstat"><span>總題數 <b>{len(rows)}</b></span><span>數A <b>{nA}</b></span><span>數B <b>{nB}</b></span><span>五大脈絡主軸</span></div>
</div>
<div class="filterbar"><span class="fb-label">篩選卷別：</span>
<button data-f="all" class="on" onclick="flt(this,'all')">全部</button>
<button data-f="數A" onclick="flt(this,'數A')">只看數A</button>
<button data-f="數B" onclick="flt(this,'數B')">只看數B</button></div>
{''.join(sections)}
<div class="foot">資料整理自《學測數學考題分析 106–115》；分組與脈絡敘述為教學編排，題幹與官方答案以原卷為準。</div>"""

    # 上方導覽：回首頁 + 四大主題單元下拉
    try:
        from units import SECTIONS, UNITS
        by = {u["slug"]: u for u in UNITS}
        opts = ['<option value="">單元 ▾</option>', '<option value="index.html">📚 目錄首頁</option>']
        for label, slugs in SECTIONS:
            grp = "".join(f'<option value="{by[s]["file"]}">{by[s]["emoji"]} {by[s]["title"]}</option>'
                          for s in slugs if s in by and not by[s].get("draft"))
            if grp:
                opts.append(f'<optgroup label="{label}">{grp}</optgroup>')
        navsel = ('<select class="nav-select" onchange="if(this.value){location.href=this.value;}">'
                  + "".join(opts) + '</select>')
    except Exception:
        navsel = '<a class="nav-select" href="index.html">📚 目錄首頁</a>'

    toolbar = (f'<div class="toolbar"><span class="t-title">跨單元整合 · 脈絡地圖</span>{navsel}</div>')
    js = ("function flt(btn,f){document.querySelectorAll('.filterbar button').forEach(b=>b.classList.remove('on'));"
          "btn.classList.add('on');"
          "document.querySelectorAll('.xq').forEach(c=>{c.style.display=(f==='all'||c.dataset.juan===f)?'':'none';});"
          "document.querySelectorAll('.part').forEach(p=>{let g=p.nextElementSibling;"
          "while(g&&!g.classList.contains('xq-grid'))g=g.nextElementSibling;"
          "if(g){let vis=[...g.children].some(c=>c.style.display!=='none');"
          "p.style.display=vis?'':'none';p.nextElementSibling.style.display=vis?'':'none';}});}")

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>學測數學 · 跨單元整合脈絡地圖（106–115）</title>
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<style>
{css}
{extra}</style>
</head>
<body>
{toolbar}
<div class="wrap">
{body}
</div>
<script src="{KATEX}/katex.min.js"></script>
<script src="{KATEX}/contrib/auto-render.min.js"></script>
<script>
renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}},{{left:'\\\\[',right:'\\\\]',display:true}}]}});
{js}
</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[cross] -> {os.path.basename(OUT)}  （{len(rows)} 題 / 數A {nA} · 數B {nB} / 5 主軸）")


if __name__ == "__main__":
    build()
