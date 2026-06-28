# -*- coding: utf-8 -*-
"""學測數A 概念地圖（從大考反推）。三視圖：② 依賴鏈 ① 熱度地圖 ③ 概念網。
節點顏色＝該單元近十年大考份量（取自各單元 Part 0 趨勢表合計），有數據根據。
視覺重用 build/assets/style.css。本檔先完成「② 依賴鏈」，①③ 之後補。
"""
import os, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from build_html import ANALYTICS, PRIVACY_HTML, _report_btn  # noqa: E402  共用 GA4 + Clarity 追蹤碼＋頁尾隱私＋回報鈕
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


UNIT_NAME = {"trig": "三角", "prob": "排列組合與機率", "space": "空間向量", "poly": "多項式函數",
             "linecir": "直線與圓", "explog": "指數與對數", "pvec": "平面向量", "matrix": "矩陣",
             "data": "數據分析", "seq": "數列與級數", "numexpr": "數與式"}
KP_COUNT = {"trig": 7, "prob": 6, "space": 6, "poly": 5, "linecir": 5, "explog": 5,
            "pvec": 5, "matrix": 5, "data": 4, "seq": 4, "numexpr": 6}
THEMES_CM = [("① 代數與函數", ["numexpr", "poly", "explog"]),
             ("② 數列·機率·統計", ["seq", "prob", "data"]),
             ("③ 平面幾何", ["trig", "linecir", "pvec"]),
             ("④ 空間與矩陣", ["space", "matrix"])]

ABBR = {"trig": "三角", "prob": "機率", "space": "空間", "poly": "多項式", "linecir": "直線圓",
        "explog": "指對數", "pvec": "向量", "matrix": "矩陣", "data": "數據", "seq": "數列", "numexpr": "數與式"}
# 跨單元配對與次數（取自 25 題跨單元清單，同單元自配不計）
EDGES_NET = [("pvec", "trig", 4), ("trig", "seq", 2), ("seq", "explog", 2),
             ("seq", "poly", 1), ("explog", "prob", 1), ("poly", "trig", 1),
             ("pvec", "explog", 1), ("space", "trig", 1), ("prob", "matrix", 1),
             ("pvec", "numexpr", 1), ("seq", "prob", 1), ("pvec", "poly", 1), ("prob", "data", 1)]
ORDER_NET = ["numexpr", "poly", "explog", "seq", "prob", "data", "matrix", "space", "linecir", "trig", "pvec"]

# 各單元考點 (id, nav 名稱)，由 content 單一來源取得（供「考點層」下鑽）
import sys as _sys
_sys.path.insert(0, os.path.join(ROOT, "content"))
from units import UNITS as _UNITS
KP_NAV = {_u["slug"]: [(k["id"], k.get("nav", k.get("title", "")))
                       for k in __import__(_u["slug"]).UNIT["kps"]] for _u in _UNITS}


def heat(w):
    """大考份量 → (底色, 字色)。越紅＝考越重；藍綠＝份量低。"""
    if w >= 25: return ("#9e1226", "#fff")
    if w >= 20: return ("#c0392b", "#fff")
    if w >= 15: return ("#d2702f", "#fff")
    if w >= 12: return ("#d99a2a", "#3a2a10")
    if w >= 8:  return ("#3f9d8c", "#fff")
    return ("#7aa7bb", "#13303d")


COLX = [180, 415, 660, 925]  # 四層 x 中心（左側留 gutter 放帶標題）

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

# 依賴邊：(先備, 進階, 為什麼需要)
EDGES = [
    ("numexpr", "quad", "配方、判別式要先會乘法公式與根號"),
    ("numexpr", "trigr", "三角比的值要會根號運算"),
    ("numexpr", "vec", "向量坐標化要先會坐標與距離"),
    ("numexpr", "circle", "圓方程式＝到圓心的距離（數與式）"),
    ("quad", "polyhi", "高次不等式建立在二次函數的根與配方"),
    ("explaw", "logop", "對數是指數的反運算，先會指數律"),
    ("logop", "logfn", "科學記號、位數是常用對數的應用"),
    ("logop", "seq", "等比＝指數成長，求項數要取對數"),
    ("trigr", "sincos", "正餘弦定理把三角比推廣到任意三角形"),
    ("trigr", "trigfn", "三角函數圖形、和差倍角以三角比為底"),
    ("trigr", "lineq", "直線斜率 m=tanθ，要先會三角比"),
    ("sincos", "measure", "三角測量靠正餘弦定理算邊角"),
    ("sincos", "space", "空間夾角／距離用餘弦定理升維"),
    ("trigfn", "measure", "測量化簡常用和差倍角"),
    ("vec", "dot", "內積定義在向量的坐標運算之上"),
    ("vec", "det", "行列式（面積）由向量坐標算出"),
    ("vec", "matrix", "線性變換把向量映成向量"),
    ("dot", "space", "空間夾角、垂直＝內積升維"),
    ("det", "space", "空間體積＝外積／行列式"),
    ("dot", "matrix", "矩陣是否保長度／角度看內積"),
    ("lineq", "lc", "直線與圓的位置要先有直線方程式"),
    ("circle", "lc", "弦長、切線要先有圓方程式"),
    ("seq", "series", "級數＝把數列加起來"),
    ("count", "comb", "組合是計數原理的進階"),
    ("comb", "prob", "古典機率＝有利／全部，靠組合計數"),
    ("prob", "cond", "條件機率、貝氏建立在古典機率"),
    ("data1", "corr", "相關係數要先會標準差"),
    ("corr", "regr", "迴歸斜率＝r×σy/σx，先有相關係數"),
]

NW, NH = None, 34  # node height; width computed per-label
POS = {}


def _node_box(n):
    nid, label, col, cy, unit = n
    w = max(86, len(label) * 15 + 20)
    cx = COLX[col]
    return cx - w / 2, cy - NH / 2, w, NH


def _rdmark(x, y, r=8):
    """已讀 ✓ 戳記（綠圓白勾），預設隱藏、節點 .read 時顯示。"""
    return (f'<g class="rdmark"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#2e9e5b" stroke="#fff" stroke-width="1.4"/>'
            f'<path d="M{x-r*0.5:.1f},{y:.1f} L{x-r*0.08:.1f},{y+r*0.42:.1f} L{x+r*0.55:.1f},{y-r*0.45:.1f}" '
            f'fill="none" stroke="#fff" stroke-width="{r*0.3:.1f}" stroke-linecap="round" stroke-linejoin="round"/></g>')


def _svg_dep():
    # positions
    for n in NODES:
        x, y, w, h = _node_box(n)
        POS[n[0]] = (x, y, w, h, COLX[n[2]], n[3])
    parts = []
    parts.append('<svg viewBox="0 0 1150 745" xmlns="http://www.w3.org/2000/svg" '
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
    # 帶標題（左側 gutter，橫向清楚＋色條）
    for lab, y0, y1, col in [("代數與函數", 48, 172, "#a66526"),
                             ("平面幾何", 184, 508, "#1f6f78"),
                             ("數列機率統計", 524, 722, "#5a3a8c")]:
        cy = (y0 + y1) / 2
        parts.append(f'<rect x="8" y="{y0}" width="6" height="{y1-y0}" rx="3" fill="{col}" opacity="0.5"/>')
        parts.append(f'<text x="20" y="{cy+5:.0f}" font-size="15" font-weight="800" fill="{col}">{lab}</text>')
    # edges（細線＋透明寬線供滑過顯示「為什麼需要」）
    LABEL = {n[0]: n[1] for n in NODES}
    for a, b, why in EDGES:
        xa, ya, wa, ha, cxa, _ = POS[a]
        xb, yb, wb, hb, cxb, _ = POS[b]
        x1, y1 = xa + wa, ya + ha / 2
        x2, y2 = xb, yb + hb / 2
        dx = max(40, (x2 - x1) * 0.45)
        d = f"M{x1:.0f},{y1:.0f} C{x1+dx:.0f},{y1:.0f} {x2-dx:.0f},{y2:.0f} {x2:.0f},{y2:.0f}"
        parts.append(f'<path d="{d}" fill="none" stroke="#cdbcc4" stroke-width="1.4" marker-end="url(#ar)" opacity="0.85"/>')
        parts.append(f'<path d="{d}" fill="none" stroke="transparent" stroke-width="14" style="cursor:help">'
                     f'<title>{LABEL[a]} → {LABEL[b]}：{why}</title></path>')
    # nodes
    for nid, label, col, cy, unit in NODES:
        x, y, w, h, cx, _ = POS[nid]
        fill, txt = heat(UNIT_W[unit])
        big = ' stroke="#2b2b2b" stroke-width="2"' if col == 3 else ' stroke="rgba(0,0,0,.12)" stroke-width="1"'
        href = UNIT_FILE[unit]
        parts.append(f'<g class="mnode" data-u="{unit}" onclick="nodeClick(event,\'{unit}\')">')
        parts.append(f'<a href="{href}">')
        parts.append(f'<rect class="nbg" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="9" fill="{fill}"{big}/>')
        parts.append(f'<text x="{cx:.0f}" y="{cy+5:.0f}" text-anchor="middle" font-size="13" '
                     f'font-weight="700" fill="{txt}">{label}</text>')
        parts.append('</a>')
        parts.append(_rdmark(x + w - 8, y + 7, 7))
        parts.append('</g>')
    parts.append('</svg>')
    return "".join(parts)


def _svg_heat():
    """① 大考熱度地圖：treemap，每單元矩形面積 ∝ 近十年大考份量，依四大主題分欄。"""
    GRAND = sum(UNIT_W.values())
    W, TOP, H = 1000, 54, 548
    parts = ['<svg viewBox="0 0 1000 614" xmlns="http://www.w3.org/2000/svg" '
             'font-family="\'Microsoft JhengHei\',system-ui,sans-serif">']
    x = 0.0
    for tlabel, slugs in THEMES_CM:
        ttot = sum(UNIT_W[s] for s in slugs)
        cw = ttot / GRAND * W
        parts.append(f'<text x="{x+cw/2:.0f}" y="34" text-anchor="middle" font-size="14" font-weight="800" '
                     f'fill="#8c2740">{tlabel} <tspan font-size="11.5" fill="#9a857c">{ttot:.1f}題</tspan></text>')
        y = float(TOP)
        for s in sorted(slugs, key=lambda z: -UNIT_W[z]):
            w = UNIT_W[s]
            uh = w / ttot * H
            fill, txt = heat(w)
            cx, cy = x + cw / 2, y + uh / 2
            namef = min(19, max(12, uh / 3.6))
            numf = min(31, max(15, uh / 3.0))
            parts.append(f'<g class="mnode" data-u="{s}" onclick="nodeClick(event,\'{s}\')">')
            parts.append(f'<a href="{UNIT_FILE[s]}">')
            parts.append(f'<rect class="nbg" x="{x+2:.1f}" y="{y+2:.1f}" width="{cw-4:.1f}" height="{uh-4:.1f}" rx="6" fill="{fill}"/>')
            parts.append(f'<text x="{cx:.0f}" y="{cy-numf*0.32:.0f}" text-anchor="middle" font-size="{namef:.0f}" '
                         f'font-weight="800" fill="{txt}">{UNIT_NAME[s]}</text>')
            parts.append(f'<text x="{cx:.0f}" y="{cy+numf*0.58:.0f}" text-anchor="middle" font-size="{numf:.0f}" '
                         f'font-weight="800" fill="{txt}">{w:g}</text>')
            if uh > 82:
                parts.append(f'<text x="{cx:.0f}" y="{y+uh-10:.0f}" text-anchor="middle" font-size="11" '
                             f'fill="{txt}" opacity="0.85">{KP_COUNT[s]} 考點</text>')
            parts.append('</a>')
            parts.append(_rdmark(x + cw - 18, y + 18, 9))
            parts.append('</g>')
            y += uh
        x += cw
    parts.append('</svg>')
    return "".join(parts)


def _svg_kpgrid():
    """① 考點層下鑽：每單元一列、其考點為小格；讀過的格變綠＋✓，份量用顏色。"""
    CW = 120
    body, y = [], 18
    for tlabel, slugs in THEMES_CM:
        body.append(f'<text x="6" y="{y+12}" font-size="13.5" font-weight="800" fill="#8c2740">{tlabel}</text>')
        y += 24
        for s in slugs:
            w = UNIT_W[s]
            fill, _ = heat(w)
            body.append(f'<a href="{UNIT_FILE[s]}"><text x="8" y="{y+19}" font-size="13" font-weight="800" '
                        f'fill="{fill}">{UNIT_NAME[s]}</text>'
                        f'<text x="8" y="{y+33}" font-size="10" fill="#9a857c">{w:g} 題</text></a>')
            for i, (kid, nav) in enumerate(KP_NAV[s]):
                cx = 116 + i * CW
                cw2 = CW - 7
                kk = f"{s}:{kid}"
                body.append(f'<g class="kpcell" data-kk="{kk}" onclick="cellClick(event,\'{kk}\',\'{UNIT_FILE[s]}#{kid}\')">')
                body.append(f'<rect class="cellbg" x="{cx}" y="{y}" width="{cw2}" height="35" rx="6" fill="{fill}"/>')
                body.append(f'<text x="{cx+cw2/2:.0f}" y="{y+22:.0f}" text-anchor="middle" font-size="12.5" '
                            f'font-weight="700" fill="#fff">考{i+1}</text>')
                body.append(f'<g class="ckm"><circle cx="{cx+cw2-12:.0f}" cy="{y+11}" r="7.5" fill="#fff" stroke="#2e9e5b" stroke-width="1.3"/>'
                            f'<path d="M{cx+cw2-16:.0f},{y+11} L{cx+cw2-13:.0f},{y+14} L{cx+cw2-8:.0f},{y+8}" '
                            f'fill="none" stroke="#2e9e5b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>')
                body.append(f'<title>{UNIT_NAME[s]} · 考{i+1}：{nav}</title>')
                body.append('</g>')
            y += 43
        y += 8
    return (f'<svg viewBox="0 0 1000 {y}" xmlns="http://www.w3.org/2000/svg" '
            "font-family=\"'Microsoft JhengHei',system-ui,sans-serif\">" + "".join(body) + '</svg>')


def _svg_net():
    """③ 跨單元概念網：11 單元排成圓，連線＝大考同題綁定次數，線越粗越常一起考。"""
    import math
    cx, cy, R = 480, 334, 248
    pos = {}
    n = len(ORDER_NET)
    for i, s in enumerate(ORDER_NET):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        pos[s] = (cx + R * math.cos(ang), cy + R * math.sin(ang))
    parts = ['<svg viewBox="0 0 960 690" xmlns="http://www.w3.org/2000/svg" '
             'font-family="\'Microsoft JhengHei\',system-ui,sans-serif">']
    for a, b, c in sorted(EDGES_NET, key=lambda e: e[2]):  # 細線先畫
        x1, y1 = pos[a]; x2, y2 = pos[b]
        col = "#c0392b" if c >= 4 else ("#d2843a" if c >= 2 else "#d2c2ca")
        op = 0.95 if c >= 4 else (0.85 if c >= 2 else 0.6)
        parts.append(f'<line class="netedge" data-a="{a}" data-b="{b}" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                     f'stroke="{col}" stroke-width="{c*1.6+1.4:.1f}" opacity="{op}" stroke-linecap="round"/>')
    # 中央註
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="78" ry="26" fill="#fffaf6" opacity="0.92"/>')
    parts.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="14" font-weight="800" fill="#8c2740">向量 × 三角</text>')
    parts.append(f'<text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="11" fill="#9a857c">最常綁在一起（4 題）</text>')
    for s in ORDER_NET:
        x, y = pos[s]
        w = UNIT_W[s]
        r = 15 + w * 0.55
        fill, txt = heat(w)
        nm = ABBR[s]
        nf = 12.5 if len(nm) <= 2 else 10.5
        parts.append(f'<g class="mnode" data-u="{s}" onclick="nodeClick(event,\'{s}\')" '
                     f'onmouseenter="netHi(\'{s}\')" onmouseleave="netClr()">')
        parts.append(f'<a href="{UNIT_FILE[s]}">')
        parts.append(f'<circle class="nbg" cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{fill}" stroke="#fff" stroke-width="2"/>')
        parts.append(f'<text x="{x:.0f}" y="{y-1:.0f}" text-anchor="middle" font-size="{nf}" font-weight="800" fill="{txt}">{nm}</text>')
        parts.append(f'<text x="{x:.0f}" y="{y+12:.0f}" text-anchor="middle" font-size="9.5" fill="{txt}" opacity="0.85">{w:g}</text>')
        parts.append('</a>')
        parts.append(_rdmark(x + r * 0.66, y - r * 0.66, 8))
        parts.append('</g>')
    parts.append('</svg>')
    return "".join(parts)


def _legend_chips():
    items = [("≥25 ★最重", "#9e1226"), ("20–25", "#c0392b"), ("15–20", "#d2702f"),
             ("12–15", "#d99a2a"), ("8–12", "#3f9d8c"), ("<8", "#7aa7bb")]
    return "".join(f'<span class="cm-chip"><i style="background:{c}"></i>{t}</span>' for t, c in items)


def _legend():
    return f'<div class="cm-legend"><b>顏色＝近十年大考份量（加權題數）：</b>{_legend_chips()}<span class="cm-note">越紅＝考越重；箭頭＝「先會 → 才好學」（<b>滑過箭頭看「為什麼需要」</b>）；最右欄＝大考高頻、反推起點（粗框，可點進單元）</span></div>'


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
  .rdmark{display:none}
  .mnode.read .rdmark{display:block}
  .mnode.read .nbg{stroke:#2e9e5b;stroke-width:2.6}
  .cm-board.marking{outline:2px dashed #2e9e5b;outline-offset:-3px;border-radius:14px}
  .cm-board.marking .mnode{cursor:pointer}
  .cm-board.marking .mnode:hover .nbg{filter:brightness(1.12)}
  .cm-prog{display:flex;align-items:center;gap:11px;justify-content:center;flex-wrap:wrap;margin:12px 0 2px}
  .cm-prog .markbtn{background:#fff;color:#2e7d46;border:1.6px solid #2e9e5b;border-radius:20px;padding:6px 15px;font-weight:800;font-size:13.5px;cursor:pointer;font-family:inherit;transition:.15s}
  .cm-prog .markbtn.on{background:#2e9e5b;color:#fff}
  .cm-prog .ptxt{font-weight:800;color:var(--maroon-d);font-size:14px}
  .cm-prog .bar{width:180px;height:12px;background:#e6ddd4;border-radius:8px;overflow:hidden}
  .cm-prog .bar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#2e9e5b,#52c47e);transition:width .3s}
  .cm-prog .resetbtn{background:none;border:none;color:#b3a3ab;font-size:12px;cursor:pointer;text-decoration:underline;font-family:inherit}
  .cm-subtabs{display:flex;gap:6px;justify-content:center;margin:8px 0 4px}
  .cm-subtabs button{background:#fff;color:#8a6b75;border:1px solid #d9c2c9;border-radius:16px;padding:4px 13px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}
  .cm-subtabs button.on{background:#f0dde3;color:var(--maroon-d);border-color:var(--maroon)}
  .kpcell{cursor:pointer}
  .ckm{display:none}
  .kpcell.kpread .cellbg{fill:#2e9e5b}
  .kpcell.kpread .ckm{display:block}
  .cm-board.marking .kpcell:hover .cellbg{filter:brightness(1.1)}
"""
    nav = ('<select class="nav-select" onchange="if(this.value)location.href=this.value" '
           'style="background:#fff;color:var(--maroon-d);border:none;border-radius:20px;padding:6px 12px;font-weight:700;font-size:14px">'
           '<option value="">單元 ▾</option><option value="index.html">📚 目錄首頁</option>'
           '<option value="115學測數學_跨單元整合_脈絡地圖.html">🧩 跨單元脈絡地圖</option></select>')
    body = f"""<div class="cm-topbar"><span class="t-title">學測數A · 概念地圖（從大考反推）</span>
<a class="home" href="index.html">📚 首頁</a>{nav}</div>
<div class="cm-wrap">
<div class="cm-hero"><h1>從大考反推的概念地圖</h1>
<p>寫給「上課聽得懂、自己做卻卡住」的你——中間缺的是一座 <b>從「點狀題型」到「面狀概念」的橋</b>。這張地圖不照課本目錄，而是讓 <b>近十年大考數據</b> 決定重點與結構：依賴鏈（先學什麼）、熱度地圖（份量輕重）、概念網（跨單元連結）。</p></div>
<div class="cm-prog">
<button class="markbtn" id="markbtn" onclick="toggleMark()">✏️ 標記已讀</button>
<span class="ptxt" id="ptxt">已讀 0 / 58 考點</span>
<div class="bar"><i id="pbar"></i></div>
<button class="resetbtn" onclick="resetRead()">清除</button></div>
<div class="cm-tabs">
<button class="on" data-v="dep" onclick="cmTab(this,'dep')">② 概念依賴鏈</button>
<button data-v="heat" onclick="cmTab(this,'heat')">① 大考熱度地圖</button>
<button data-v="net" onclick="cmTab(this,'net')">③ 跨單元概念網</button></div>

<div class="cm-view on" id="v-dep">
{_legend()}
<div class="cm-board">{_svg_dep()}</div>
</div>
<div class="cm-view" id="v-heat">
<div class="cm-legend"><b>面積／顏色 ＝ 該單元近十年大考份量</b>，依四大主題分欄。{_legend_chips()}<span class="cm-note">「單元層」面積越大＝考越重；「考點層」下鑽到每個考點，讀過的格變綠 ✓（標記模式中可直接點格標記）。</span></div>
<div class="cm-subtabs">
<button class="on" onclick="heatSub(this,'tree')">▦ 單元層（面積＝份量）</button>
<button onclick="heatSub(this,'kp')">▤ 考點層（讀過進度）</button></div>
<div class="cm-board" id="heat-tree">{_svg_heat()}</div>
<div class="cm-board" id="heat-kp" style="display:none">{_svg_kpgrid()}</div>
</div>
<div class="cm-view" id="v-net">
<div class="cm-legend"><b>連線 ＝ 大考把兩單元綁在同一題（取自 25 題跨單元清單）</b>，線越粗＝越常一起考；圓的大小/顏色＝該單元大考份量。{_legend_chips()}<span class="cm-note">向量、三角是「跨單元之王」——連到最多其他單元；圓可點進該單元。</span></div>
<div class="cm-board">{_svg_net()}</div>
</div>

<div class="cm-foot">概念份量取自各單元近十年（106–115）出題趨勢加權題數；依賴關係為教學編排。</div>
</div>"""
    js = ("function cmTab(b,v){document.querySelectorAll('.cm-tabs button').forEach(x=>x.classList.remove('on'));"
          "b.classList.add('on');document.querySelectorAll('.cm-view').forEach(x=>x.classList.remove('on'));"
          "document.getElementById('v-'+v).classList.add('on');}"
          "var RK='mm-read-kps';"
          "var KPN={trig:7,prob:6,space:6,poly:5,linecir:5,explog:5,pvec:5,matrix:5,data:4,seq:4,numexpr:6};"
          "function kk(u){var a=[];for(var i=1;i<=KPN[u];i++)a.push(u+':kp'+i);return a;}"
          "function gR(){try{return new Set(JSON.parse(localStorage.getItem(RK)||'[]'))}catch(e){return new Set()}}"
          "function uf(u,s){return kk(u).every(k=>s.has(k));}"
          "function aR(){var s=gR();document.querySelectorAll('.mnode').forEach(n=>n.classList.toggle('read',uf(n.dataset.u,s)));"
          "document.querySelectorAll('.kpcell').forEach(c=>c.classList.toggle('kpread',s.has(c.dataset.kk)));uP(s);}"
          "function uP(s){s=s||gR();var t=0;for(var u in KPN)t+=KPN[u];var d=s.size;"
          "document.getElementById('ptxt').textContent='已讀 '+d+' / '+t+' 考點';"
          "document.getElementById('pbar').style.width=(t?d/t*100:0)+'%';}"
          "function toggleRead(u){var s=gR();var ks=kk(u);var f=ks.every(k=>s.has(k));"
          "ks.forEach(k=>f?s.delete(k):s.add(k));localStorage.setItem(RK,JSON.stringify([...s]));aR();}"
          "window.markMode=false;"
          "function toggleMark(){window.markMode=!window.markMode;var b=document.getElementById('markbtn');"
          "b.classList.toggle('on',window.markMode);b.textContent=window.markMode?'✓ 標記中（點概念）':'✏️ 標記已讀';"
          "document.querySelectorAll('.cm-board').forEach(x=>x.classList.toggle('marking',window.markMode));}"
          "function nodeClick(e,u){if(window.markMode){e.preventDefault();e.stopPropagation();toggleRead(u);}}"
          "function resetRead(){if(confirm('清除所有已讀標記？')){localStorage.removeItem(RK);aR();}}"
          "function toggleKp(k){var s=gR();s.has(k)?s.delete(k):s.add(k);localStorage.setItem(RK,JSON.stringify([...s]));aR();}"
          "function cellClick(e,k,href){if(window.markMode){e.preventDefault();e.stopPropagation();toggleKp(k);}else{location.href=href;}}"
          "function heatSub(b,w){document.querySelectorAll('.cm-subtabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');"
          "document.getElementById('heat-tree').style.display=(w==='tree')?'':'none';"
          "document.getElementById('heat-kp').style.display=(w==='kp')?'':'none';}"
          "function netHi(u){if(window.markMode)return;var nb=new Set([u]);"
          "document.querySelectorAll('#v-net .netedge').forEach(l=>{var on=(l.dataset.a===u||l.dataset.b===u);"
          "l.style.opacity=on?'1':'0.07';if(on){nb.add(l.dataset.a);nb.add(l.dataset.b);}});"
          "document.querySelectorAll('#v-net .mnode').forEach(n=>{n.style.opacity=nb.has(n.dataset.u)?'1':'0.16';});}"
          "function netClr(){document.querySelectorAll('#v-net .netedge').forEach(l=>l.style.opacity='');"
          "document.querySelectorAll('#v-net .mnode').forEach(n=>n.style.opacity='');}"
          "aR();")
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ANALYTICS}<title>學測數A · 概念地圖（從大考反推）</title>
<style>{css}
{extra}</style></head><body>
{body}
{PRIVACY_HTML}
{_report_btn({"title": "概念地圖"})}
<script>{js}</script>
</body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"[conceptmap] -> {os.path.basename(OUT)}  ({len(NODES)} 節點 / {len(EDGES)} 依賴邊)")


if __name__ == "__main__":
    build()
