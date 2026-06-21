# -*- coding: utf-8 -*-
"""學測數A 概念地圖（從大考反推）。三視圖：② 依賴鏈 ① 熱度地圖 ③ 概念網。
節點顏色＝該單元近十年大考份量（取自各單元 Part 0 趨勢表合計），有數據根據。
視覺重用 build/assets/style.css。本檔先完成「② 依賴鏈」，①③ 之後補。
"""
import os, io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"
OUT = os.path.join(ROOT, "dist", "115學測數學_概念地圖.html")


def _asset(name):
    return io.open(os.path.join(HERE, "assets", name), encoding="utf-8").read()


# 近十年大考份量（各單元 Part 0 trend 合計）
UNIT_W = {"trig": 30.6, "prob": 27.0, "space": 25.0, "poly": 20.5, "linecir": 19.4,
          "explog": 17.8, "pvec": 15.6, "matrix": 12.25, "data": 10.5, "seq": 9.8, "numexpr": 5.0}
UNIT_FILE = {  # 點節點可跳到該單元
    "trig": "115學測數學_三角.html", "prob": "115學測數學_排列組合與機率.html",
    "space": "115學測數學_空間向量.html", "poly": "115學測數學_多項式函數.html",
    "linecir": "115學測數學_直線與圓.html", "explog": "115學測數學_指數與對數.html",
    "pvec": "115學測數學_平面向量.html", "matrix": "115學測數學_矩陣.html",
    "data": "115學測數學_數據分析.html", "seq": "115學測數學_數列與級數.html",
    "numexpr": "115學測數學_數與式.html",
}


def heat(w):
    """大考份量 → (底色, 字色)。越紅＝考越重；藍綠＝份量低。"""
    if w >= 25: return ("#9e1226", "#fff")
    if w >= 20: return ("#c0392b", "#fff")
    if w >= 15: return ("#d2702f", "#fff")
    if w >= 12: return ("#d99a2a", "#3a2a10")
    if w >= 8:  return ("#3f9d8c", "#fff")
    return ("#7aa7bb", "#13303d")


COLX = [95, 330, 585, 855]  # 四層 x 中心：地基 / 工具 / 主力 / 大考高頻

# 節點：(id, 標籤, 層col, y中心, 單元)
NODES = [
    # 代數與函數帶（上）
    ("numexpr", "數與式", 0, 70, "numexpr"),
    ("explaw", "指數律", 0, 140, "explog"),
    ("quad", "二次函數·配方", 1, 80, "poly"),
    ("logop", "對數運算", 1, 150, "explog"),
    ("logfn", "常用對數·指對圖形", 2, 95, "explog"),
    ("polyhi", "多項式不等式·三次圖形", 3, 80, "poly"),
    # 平面幾何帶（中）
    ("trigr", "三角比", 1, 252, "trig"),
    ("vec", "向量運算（坐標化）", 1, 336, "pvec"),
    ("lineq", "直線·斜率(tanθ)", 1, 416, "linecir"),
    ("sincos", "正弦·餘弦定理", 2, 214, "trig"),
    ("trigfn", "三角圖形·和差倍角", 2, 284, "trig"),
    ("dot", "內積·正射影", 2, 354, "pvec"),
    ("det", "行列式·面積", 2, 420, "pvec"),
    ("circle", "圓方程式", 2, 486, "linecir"),
    ("measure", "三角測量·面積", 3, 200, "trig"),
    ("space", "空間向量", 3, 292, "space"),
    ("matrix", "矩陣·線性變換", 3, 372, "matrix"),
    ("lc", "直線與圓·位置弦長", 3, 470, "linecir"),
    # 數列機率統計帶（下）
    ("count", "計數原理", 0, 560, "prob"),
    ("comb", "排列·組合", 1, 545, "prob"),
    ("prob", "古典機率", 2, 560, "prob"),
    ("cond", "條件機率·貝氏·期望", 3, 560, "prob"),
    ("seq", "等差·等比數列", 1, 630, "seq"),
    ("series", "級數·遞迴·應用", 2, 632, "seq"),
    ("data1", "一維數據·標準差", 1, 702, "data"),
    ("corr", "相關係數", 2, 700, "data"),
    ("regr", "迴歸直線", 3, 668, "data"),
]

# 依賴邊：(先備, 進階)
EDGES = [
    ("numexpr", "quad"), ("numexpr", "trigr"), ("numexpr", "vec"), ("numexpr", "circle"),
    ("quad", "polyhi"),
    ("explaw", "logop"), ("logop", "logfn"), ("logop", "seq"),
    ("trigr", "sincos"), ("trigr", "trigfn"), ("trigr", "lineq"),
    ("sincos", "measure"), ("sincos", "space"), ("trigfn", "measure"),
    ("vec", "dot"), ("vec", "det"), ("vec", "matrix"),
    ("dot", "space"), ("det", "space"), ("dot", "matrix"),
    ("lineq", "lc"), ("circle", "lc"),
    ("seq", "series"),
    ("count", "comb"), ("comb", "prob"), ("prob", "cond"),
    ("data1", "corr"), ("corr", "regr"),
]

NW, NH = None, 34  # node height; width computed per-label
POS = {}


def _node_box(n):
    nid, label, col, cy, unit = n
    w = max(86, len(label) * 15 + 20)
    cx = COLX[col]
    return cx - w / 2, cy - NH / 2, w, NH


def _svg_dep():
    # positions
    for n in NODES:
        x, y, w, h = _node_box(n)
        POS[n[0]] = (x, y, w, h, COLX[n[2]], n[3])
    parts = []
    parts.append('<svg viewBox="0 0 1070 745" xmlns="http://www.w3.org/2000/svg" '
                 'font-family="\'Microsoft JhengHei\',system-ui,sans-serif">')
    parts.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                 'markerHeight="7" orient="auto-start-reverse">'
                 '<path d="M0,0 L10,5 L0,10 z" fill="#b9a9b0"/></marker></defs>')
    # 層標題
    layers = ["①地基", "②核心工具", "③主力概念", "④大考高頻 / 反推起點"]
    for i, lab in enumerate(layers):
        parts.append(f'<text x="{COLX[i]}" y="28" text-anchor="middle" font-size="14" '
                     f'font-weight="800" fill="#8c2740">{lab}</text>')
        parts.append(f'<line x1="{COLX[i]}" y1="36" x2="{COLX[i]}" y2="726" stroke="#efe4e8" stroke-width="1"/>')
    # 帶標題（左側）
    for lab, yy, col in [("代數與函數", 110, "#b06a2a"), ("平面幾何", 350, "#1f6f78"), ("數列·機率·統計", 600, "#5a3a8c")]:
        parts.append(f'<text x="8" y="{yy}" font-size="12.5" font-weight="800" fill="{col}" '
                     f'transform="rotate(-90 8 {yy})" text-anchor="middle" opacity="0.55">{lab}</text>')
    # edges
    for a, b in EDGES:
        xa, ya, wa, ha, cxa, _ = POS[a]
        xb, yb, wb, hb, cxb, _ = POS[b]
        x1, y1 = xa + wa, ya + ha / 2
        x2, y2 = xb, yb + hb / 2
        dx = max(40, (x2 - x1) * 0.45)
        parts.append(f'<path d="M{x1:.0f},{y1:.0f} C{x1+dx:.0f},{y1:.0f} {x2-dx:.0f},{y2:.0f} {x2:.0f},{y2:.0f}" '
                     f'fill="none" stroke="#cdbcc4" stroke-width="1.4" marker-end="url(#ar)" opacity="0.85"/>')
    # nodes
    for nid, label, col, cy, unit in NODES:
        x, y, w, h, cx, _ = POS[nid]
        fill, txt = heat(UNIT_W[unit])
        big = ' stroke="#2b2b2b" stroke-width="2"' if col == 3 else ' stroke="rgba(0,0,0,.12)" stroke-width="1"'
        href = UNIT_FILE[unit]
        parts.append(f'<a href="{href}">')
        parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="9" fill="{fill}"{big}/>')
        parts.append(f'<text x="{cx:.0f}" y="{cy+5:.0f}" text-anchor="middle" font-size="13" '
                     f'font-weight="700" fill="{txt}">{label}</text>')
        parts.append('</a>')
    parts.append('</svg>')
    return "".join(parts)


def _legend():
    items = [(">=25 ★最重", "#9e1226"), ("20–25", "#c0392b"), ("15–20", "#d2702f"),
             ("12–15", "#d99a2a"), ("8–12", "#3f9d8c"), ("<8", "#7aa7bb")]
    chips = "".join(f'<span class="cm-chip"><i style="background:{c}"></i>{t}</span>' for t, c in items)
    return f'<div class="cm-legend"><b>顏色＝近十年大考份量（加權題數）：</b>{chips}<span class="cm-note">越紅＝考越重；箭頭＝「先會 → 才好學」；最右欄＝大考高頻、反推起點（粗框，可點進單元）</span></div>'


def build():
    css = _asset("style.css")
    extra = """
  .cm-topbar{position:sticky;top:0;z-index:50;background:rgba(140,39,64,.97);color:#fff;display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 18px;box-shadow:0 2px 10px rgba(0,0,0,.15);margin-bottom:8px}
  .cm-topbar .t-title{font-weight:800;margin-right:auto;font-size:16px;letter-spacing:.5px}
  .cm-topbar a.home{background:#fff;color:var(--maroon-d);border-radius:20px;padding:5px 14px;font-weight:700;font-size:14px;text-decoration:none}
  .cm-wrap{max-width:1120px;margin:0 auto;padding:0 16px 70px}
  .cm-hero{text-align:center;padding:22px 0 4px}
  .cm-hero h1{color:var(--maroon);font-size:25px;margin:.1em 0;letter-spacing:1px}
  .cm-hero p{color:#7a6a63;font-size:14.5px;margin:.3em auto;max-width:760px}
  .cm-tabs{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:14px 0 6px}
  .cm-tabs button{background:#fff;color:var(--maroon-d);border:1.5px solid var(--maroon);border-radius:22px;padding:7px 18px;font-size:14.5px;font-weight:800;cursor:pointer;font-family:inherit;transition:.15s}
  .cm-tabs button.on{background:var(--maroon);color:#fff}
  .cm-view{display:none}
  .cm-view.on{display:block}
  .cm-legend{background:#fff7ef;border:1px dashed #e0b9a6;border-radius:12px;padding:9px 16px;margin:8px 0 12px;font-size:13px;color:#6b5249;line-height:1.9}
  .cm-legend b{color:var(--maroon)}
  .cm-chip{display:inline-flex;align-items:center;gap:4px;margin:0 6px}
  .cm-chip i{width:13px;height:13px;border-radius:3px;display:inline-block}
  .cm-note{display:block;color:#8a7a72;margin-top:2px}
  .cm-board{background:#fffdfb;border:1px solid var(--line);border-radius:14px;padding:8px;overflow-x:auto}
  .cm-board svg{width:100%;min-width:860px;height:auto;display:block}
  .cm-board a{cursor:pointer}.cm-board a:hover rect{filter:brightness(1.08)}
  .cm-stub{padding:40px;text-align:center;color:#9a857c;font-size:15px}
  .cm-foot{text-align:center;color:#9a8a82;font-size:12.5px;margin-top:26px}
"""
    nav = ('<select class="nav-select" onchange="if(this.value)location.href=this.value" '
           'style="background:#fff;color:var(--maroon-d);border:none;border-radius:20px;padding:6px 12px;font-weight:700;font-size:14px">'
           '<option value="">單元 ▾</option><option value="index.html">📚 目錄首頁</option>'
           '<option value="115學測數學_跨單元整合_脈絡地圖.html">🧩 跨單元脈絡地圖</option></select>')
    body = f"""<div class="cm-topbar"><span class="t-title">學測數A · 概念地圖（從大考反推）</span>
<a class="home" href="index.html">📚 首頁</a>{nav}</div>
<div class="cm-wrap">
<div class="cm-hero"><h1>從大考反推的概念地圖</h1>
<p>不照課本目錄，而是讓 <b>近十年大考數據</b> 決定地圖的重點與結構。三種看法：依賴鏈（學習順序）、熱度地圖（份量輕重）、概念網（跨單元連結）。</p></div>
<div class="cm-tabs">
<button class="on" data-v="dep" onclick="cmTab(this,'dep')">② 概念依賴鏈</button>
<button data-v="heat" onclick="cmTab(this,'heat')">① 大考熱度地圖</button>
<button data-v="net" onclick="cmTab(this,'net')">③ 跨單元概念網</button></div>

<div class="cm-view on" id="v-dep">
{_legend()}
<div class="cm-board">{_svg_dep()}</div>
</div>
<div class="cm-view" id="v-heat"><div class="cm-stub">① 大考熱度地圖 — 製作中…</div></div>
<div class="cm-view" id="v-net"><div class="cm-stub">③ 跨單元概念網 — 製作中…</div></div>

<div class="cm-foot">概念份量取自各單元近十年（106–115）出題趨勢加權題數；依賴關係為教學編排。</div>
</div>"""
    js = ("function cmTab(b,v){document.querySelectorAll('.cm-tabs button').forEach(x=>x.classList.remove('on'));"
          "b.classList.add('on');document.querySelectorAll('.cm-view').forEach(x=>x.classList.remove('on'));"
          "document.getElementById('v-'+v).classList.add('on');}")
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>學測數A · 概念地圖（從大考反推）</title>
<style>{css}
{extra}</style></head><body>
{body}
<script>{js}</script>
</body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[conceptmap] -> {os.path.basename(OUT)}  ({len(NODES)} 節點 / {len(EDGES)} 依賴邊)")


if __name__ == "__main__":
    build()
