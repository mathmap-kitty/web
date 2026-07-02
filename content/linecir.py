# -*- coding: utf-8 -*-
r"""直線與圓單元 · 單一來源內容（單元9：直線與圓，平面坐標系）。

挖空原則：只挖「公式與概念關鍵」（自行判斷）。
例題以官方原卷（106~115學測數學試卷.pdf）為準，答案對官方答案頁校正；數 B 題不採用。

考點對應核心概念分析（單元9）五大主軸：
  ① 直線方程式、斜率與角平分線  ② 兩點距離與三角形  ③ 圓方程式
  ④ 直線與圓的位置（切線、弦長、距離）  ⑤ 平面區域與線性規劃
"""

# 直線與圓相交：圓心到直線距離 d、半徑 r、弦長
SVG_CIRCLINE = r'''<svg viewBox="0 0 200 140" width="200" height="140" xmlns="http://www.w3.org/2000/svg" role="img">
  <circle cx="95" cy="60" r="42" fill="none" stroke="#2c7a6b" stroke-width="2"/>
  <line x1="18" y1="90" x2="178" y2="90" stroke="#8c2740" stroke-width="2"/>
  <line x1="95" y1="60" x2="95" y2="90" stroke="#1f6f78" stroke-width="1.6" stroke-dasharray="4 3"/>
  <line x1="95" y1="60" x2="65.6" y2="90" stroke="#999" stroke-width="1.3"/>
  <circle cx="95" cy="60" r="2.6" fill="#2c3e50"/>
  <circle cx="65.6" cy="90" r="3" fill="#8c2740"/><circle cx="124.4" cy="90" r="3" fill="#8c2740"/>
  <g font-size="12" font-family="serif" font-style="italic">
    <text x="99" y="56" fill="#22433c">O</text>
    <text x="100" y="81" fill="#1f6f78">d</text>
    <text x="73" y="69" fill="#666">r</text>
    <text x="158" y="86" fill="#8c2740">L</text>
  </g>
  <text x="100" y="126" fill="#444" font-size="11" text-anchor="middle">d &lt; r：相交，弦長 ＝ 2&#8730;(r&#178;&#8722;d&#178;)</text>
</svg>'''

# ---- 程式產生的幾何圖（斜率 / 對稱投影 / 半平面 / 點與圓）----
import math as _math
_F = "font-family=\"'Microsoft JhengHei',system-ui,sans-serif\""
_INK = "#2c3e50"; _BLUE = "#34679a"; _ROSE = "#b03a5b"; _GRN = "#1f8a5b"

def _slope_fig():
    L = [f'<svg viewBox="0 0 330 150" width="330" height="150" xmlns="http://www.w3.org/2000/svg" role="img" {_F}>']
    def panel(ox, rising):
        ay, by = (100, 40) if rising else (40, 100)
        ax, bx = ox+30, ox+118; sl = (by-ay)/(bx-ax)
        g = [f'<line x1="{ox+18}" y1="120" x2="{ox+140}" y2="120" stroke="{_INK}" stroke-width="1.1"/>',
             f'<polygon points="{ox+146},120 {ox+138},116.5 {ox+138},123.5" fill="{_INK}"/>',
             f'<line x1="{ox+24}" y1="128" x2="{ox+24}" y2="22" stroke="{_INK}" stroke-width="1.1"/>',
             f'<polygon points="{ox+24},16 {ox+20.5},24 {ox+27.5},24" fill="{_INK}"/>',
             f'<line x1="{ax-18}" y1="{ay-18*sl:.1f}" x2="{bx+18}" y2="{by+18*sl:.1f}" stroke="{_BLUE}" stroke-width="2"/>',
             f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{ay}" stroke="#9aa6b0" stroke-width="1.2" stroke-dasharray="4 3"/>',
             f'<line x1="{bx}" y1="{ay}" x2="{bx}" y2="{by}" stroke="#9aa6b0" stroke-width="1.2" stroke-dasharray="4 3"/>',
             f'<circle cx="{ax}" cy="{ay}" r="3" fill="{_ROSE}"/><circle cx="{bx}" cy="{by}" r="3" fill="{_ROSE}"/>',
             f'<text x="{ax-4}" y="{ay+(16 if rising else -8)}" font-size="11" fill="{_INK}" text-anchor="end">A</text>',
             f'<text x="{bx+5}" y="{by+(0 if rising else 4)}" font-size="11" fill="{_INK}">B</text>',
             f'<text x="{(ax+bx)/2}" y="{ay+(16 if rising else -6)}" font-size="10" fill="#5a4a52" text-anchor="middle">Δx</text>',
             f'<text x="{bx+6}" y="{(ay+by)/2+3}" font-size="10" fill="#5a4a52">Δy</text>',
             f'<text x="{ox+78}" y="18" font-size="11.5" font-weight="bold" fill="{_GRN if rising else _ROSE}" text-anchor="middle">m {"&gt;" if rising else "&lt;"} 0</text>']
        return "".join(g)
    L.append(panel(0, True)); L.append(panel(165, False))
    L.append('<line x1="163" y1="14" x2="163" y2="138" stroke="#e2dde4" stroke-width="1"/></svg>')
    return "".join(L)

def _reflect_fig():
    P0 = (20, 130); d = (180, -90); ln = _math.hypot(*d); u = (d[0]/ln, d[1]/ln)
    P = (70, 40); t = (P[0]-P0[0])*u[0]+(P[1]-P0[1])*u[1]
    Q = (P0[0]+t*u[0], P0[1]+t*u[1]); R = (2*Q[0]-P[0], 2*Q[1]-P[1]); nx, ny = -u[1], u[0]
    L = [f'<svg viewBox="0 0 220 170" width="220" height="170" xmlns="http://www.w3.org/2000/svg" role="img" {_F}>',
         f'<line x1="{P0[0]}" y1="{P0[1]}" x2="{P0[0]+d[0]}" y2="{P0[1]+d[1]}" stroke="{_INK}" stroke-width="1.8"/>',
         f'<text x="{P0[0]+d[0]+4}" y="{P0[1]+d[1]+4}" font-size="12" font-style="italic" fill="{_INK}">L</text>',
         f'<line x1="{P[0]}" y1="{P[1]}" x2="{R[0]:.1f}" y2="{R[1]:.1f}" stroke="{_ROSE}" stroke-width="1.5" stroke-dasharray="5 3"/>',
         f'<polyline points="{Q[0]-u[0]*8:.1f},{Q[1]-u[1]*8:.1f} {Q[0]-u[0]*8+nx*8:.1f},{Q[1]-u[1]*8+ny*8:.1f} {Q[0]+nx*8:.1f},{Q[1]+ny*8:.1f}" fill="none" stroke="{_INK}" stroke-width="1"/>']
    for pt, col in [(P, _ROSE), (Q, _INK), (R, _ROSE)]:
        L.append(f'<circle cx="{pt[0]:.1f}" cy="{pt[1]:.1f}" r="3.2" fill="{col}"/>')
    L += [f'<text x="{P[0]-6}" y="{P[1]-6}" font-size="12" font-weight="bold" fill="{_ROSE}" text-anchor="end">P</text>',
          f'<text x="{Q[0]+6}" y="{Q[1]-6}" font-size="12" font-weight="bold" fill="{_INK}">Q</text>',
          f'<text x="{R[0]+6:.1f}" y="{R[1]+12:.1f}" font-size="12" font-weight="bold" fill="{_ROSE}">R</text>',
          f'<text x="{Q[0]+10}" y="{Q[1]+14}" font-size="9.5" fill="#5a4a52">垂足(投影)</text>',
          f'<text x="{R[0]+6:.1f}" y="{R[1]+24:.1f}" font-size="9.5" fill="#5a4a52">對稱點</text>', '</svg>']
    return "".join(L)

def _halfplane_fig():
    A, B = (30, 145), (205, 28); mid = ((A[0]+B[0])/2, (A[1]+B[1])/2)
    dv = (B[0]-A[0], B[1]-A[1]); n = (-dv[1], dv[0]); nl = _math.hypot(*n); n = (n[0]/nl, n[1]/nl)
    L = [f'<svg viewBox="0 0 232 165" width="232" height="165" xmlns="http://www.w3.org/2000/svg" role="img" {_F}>',
         f'<path d="M{A[0]} {A[1]} L{B[0]} {B[1]} L222 28 L222 155 Z" fill="#e8eef5"/>',
         f'<path d="M{A[0]} {A[1]} L{B[0]} {B[1]} L20 28 L10 145 Z" fill="#fbeef2"/>',
         f'<line x1="{A[0]}" y1="{A[1]}" x2="{B[0]}" y2="{B[1]}" stroke="{_INK}" stroke-width="2"/>',
         f'<line x1="{mid[0]:.0f}" y1="{mid[1]:.0f}" x2="{mid[0]+n[0]*26:.0f}" y2="{mid[1]+n[1]*26:.0f}" stroke="{_GRN}" stroke-width="1.6"/>',
         f'<polygon points="{mid[0]+n[0]*32:.0f},{mid[1]+n[1]*32:.0f} {mid[0]+n[0]*24-n[1]*4:.0f},{mid[1]+n[1]*24+n[0]*4:.0f} {mid[0]+n[0]*24+n[1]*4:.0f},{mid[1]+n[1]*24-n[0]*4:.0f}" fill="{_GRN}"/>',
         f'<text x="150" y="120" font-size="11.5" font-weight="bold" fill="#2c5d8f" text-anchor="middle">ax+by+c &gt; 0</text>',
         f'<text x="74" y="64" font-size="11.5" font-weight="bold" fill="{_ROSE}" text-anchor="middle">ax+by+c &lt; 0</text>',
         f'<text x="{B[0]+2}" y="{B[1]-4}" font-size="10.5" font-style="italic" fill="{_INK}">L</text>', '</svg>']
    return "".join(L)

def _ptcircle_fig():
    O = (118, 92); r = 54; P = (212, 92); A = (O[0]+r, O[1]); Bn = (O[0]-r, O[1])
    L = [f'<svg viewBox="0 0 250 178" width="250" height="178" xmlns="http://www.w3.org/2000/svg" role="img" {_F}>',
         f'<circle cx="{O[0]}" cy="{O[1]}" r="{r}" fill="#eef4f8" stroke="{_INK}" stroke-width="1.6"/>',
         f'<line x1="{Bn[0]}" y1="{O[1]}" x2="{P[0]}" y2="{O[1]}" stroke="#9aa6b0" stroke-width="1" stroke-dasharray="4 3"/>',
         f'<line x1="{O[0]}" y1="{O[1]}" x2="{A[0]}" y2="{O[1]}" stroke="{_ROSE}" stroke-width="1.6"/>']
    for pt, col in [(O, _INK), (P, _ROSE), (A, _GRN), (Bn, _BLUE)]:
        L.append(f'<circle cx="{pt[0]}" cy="{pt[1]}" r="3" fill="{col}"/>')
    L += [f'<text x="{O[0]-4}" y="{O[1]-7}" font-size="11.5" font-weight="bold" fill="{_INK}" text-anchor="end">O</text>',
          f'<text x="{P[0]+4}" y="{O[1]+4}" font-size="11.5" font-weight="bold" fill="{_ROSE}">P</text>',
          f'<text x="{(O[0]+A[0])/2}" y="{O[1]-5}" font-size="10" fill="{_ROSE}" text-anchor="middle">r</text>',
          f'<text x="{A[0]+2}" y="{O[1]+18}" font-size="9.5" fill="{_GRN}" text-anchor="middle">最近</text>',
          f'<text x="{Bn[0]}" y="{O[1]+18}" font-size="9.5" fill="{_BLUE}" text-anchor="middle">最遠</text>',
          f'<text x="125" y="170" font-size="10.5" fill="#5a4a52" text-anchor="middle">最近距離 = d−r、最遠距離 = d+r（d = PO）</text>', '</svg>']
    return "".join(L)

SVG_SLOPE = _slope_fig()
SVG_REFLECT = _reflect_fig()
SVG_HALFPLANE = _halfplane_fig()
SVG_PTCIRCLE = _ptcircle_fig()

import soil_maps  # Part 0 單元知識地圖（SOIL 章節圖）

UNIT = {
    "slug": "linecir",
    "file": "115學測數學_直線與圓.html",
    "page_title": "115 學測數學 · 直線與圓",
    "emoji": "⭕",
    "title": "直線與圓",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 五大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "五大考點",
    "foot": "115 學測數學 · 直線與圓 · 學測數學重點整理",

    "part0": {
        "opener": {"svg": soil_maps.SLIDES["linecir"], "hero": True,
                   "caption": r"**單元知識地圖**：先備 → 各考點（★越多＝越常考） → 跨單元最愛綁考 → 帶走一句話"},
        "heading": "為什麼直線與圓是近年爆發的高頻單元",
        "trend_table": {
            "years": [106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            "counts": ["1.5", "2.5", "2.0", "1.0", "0.75", "2.5", "1.5", "1.3", "3.0", "3.3"],
            "total": "19.4",
        },
        "notes": [
            r"**近年題數明顯上升**：\(114\)、\(115\) 各約 \(3\) 題，合計近 \(19.4\) 題，是必須掌握的高頻單元。",
            r"**兩大 ★★★ 核心**：直線方程式／斜率／角平分線、直線與圓的位置（切線、弦長、點到直線距離）。",
            r"**工具高度重複**：**點到直線距離** 公式幾乎每年用到，務必熟到反射。",
            r"**常跨單元整合**：與三角（角度、正弦定理）、指對數（\(\log\) 三點共線）、平面向量結合。",
        ],
        "map": r"命題主軸五條：① 直線方程式、斜率與角平分線 ② 兩點距離與三角形 ③ 圓方程式 ④ 直線與圓的位置（切線、弦長、距離）⑤ 平面區域與線性規劃。",
    },

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "直線方程式與斜率",
            "title": r"直線方程式、斜率與角平分線",
            "intro": r"直線是平面坐標的基礎。熟練各種 **直線方程式的寫法**、**斜率與平行／垂直** 的關係，以及 **點到直線距離**（本單元最高頻的工具）。",
            "prereq": [
                r"**坐標** \((x,y)\)、會在坐標平面標點",
                r"**斜率** ＝ \(\dfrac{\Delta y}{\Delta x}\)（鉛直變化 ÷ 水平變化）",
                r"**三角的 \(\tan\)**（斜率 \(=\tan\theta\)）",
            ],
            "points": [
                {"label": r"斜率", "lines": [
                    r"過 \((x_1,y_1)\)、\((x_2,y_2)\) 的斜率 \(m=\) 【\(\dfrac{y_2-y_1}{x_2-x_1}\)】（\(x_1\neq x_2\)）；",
                    r"\(m=\tan\theta\)（\(\theta\) 為傾角）；**鉛直線斜率不存在**。"]},
                {"svg": SVG_SLOPE, "wide": True, "caption": r"斜率 ＝ 「鉛直變化 \(\Delta y\) ÷ 水平變化 \(\Delta x\)」：右上走（\(m>0\)）、右下走（\(m<0\)）"},
                {"label": r"跨單元整合（三角 × 直線）", "lines": [
                    r"直線與 \(x\) 軸正向的夾角 \(\theta\)（\(0^\circ\le\theta<180^\circ\)）稱 **傾斜角**，斜率 **\(m=\tan\theta\)**——三角的正切搬到直線上。",
                    r"傾斜角 \(45^\circ\Rightarrow m=\tan45^\circ=1\)；\(60^\circ\Rightarrow m=\sqrt3\)；\(135^\circ\Rightarrow m=-1\)（鈍角 → 負斜率）；",
                    r"\(90^\circ\)（鉛直線）：\(\tan90^\circ\) 無意義 → **斜率不存在**，正好對應特殊角表 \(\tan90^\circ\) 那格。"]},
                {"label": r"直線方程式的寫法", "lines": [
                    r"點斜式：\(y-y_0=\) 【\(m(x-x_0)\)】；",
                    r"斜截式：\(y=mx+k\)（[[\(k\) 為 \(y\) 截距||\(k\) 是直線與 \(y\) 軸交點的 \(y\) 坐標，即令 \(x=0\) 時的 \(y\) 值。]]）；",
                    r"一般式：\(ax+by+c=0\)，斜率 ＝ 【\(-\dfrac{a}{b}\)】（\(b\neq0\)）；",
                    r"截距式：\(\dfrac{x}{a}+\dfrac{y}{b}=1\)（\(a\) 為 \(x\) 截距、\(b\) 為 \(y\) 截距）。"]},
                {"label": r"平行與垂直", "lines": [
                    r"兩直線平行 \(\Leftrightarrow\) 【\(m_1=m_2\)】（且不重合）；",
                    r"垂直 \(\Leftrightarrow\) 【\(m_1m_2=-1\)】（或一鉛直、一水平）。"]},
                {"label": r"點到直線距離", "lines": [
                    r"點 \((x_0,y_0)\) 到直線 \(ax+by+c=0\) 的距離 ＝ 【\(\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}\)】。"]},
                {"svg": SVG_REFLECT, "med": True, "caption": r"投影點 \(Q\)（垂足）＝ \(P\) 沿垂直方向落在 \(L\) 上的點；對稱點 \(R\) 使 \(Q\) 為 \(\overline{PR}\) 中點"},
                {"label": r"角平分線", "lines": [
                    r"兩直線 \(L_1,L_2\) 的角平分線 ＝ 到兩直線 **等距** 的點所成：",
                    r"\(\dfrac{|a_1x+b_1y+c_1|}{\sqrt{a_1^2+b_1^2}}=\dfrac{|a_2x+b_2y+c_2|}{\sqrt{a_2^2+b_2^2}}\)（[[會有兩條||去絕對值時取 \(+\)、\(-\) 各得一條，兩條角平分線 **互相垂直**，分別平分兩組對頂角。要哪條看題目要求的那個角。]]，這兩條互相垂直）。"]},
            ],
            "misconceptions": [
                {"wrong": r"每條直線都有斜率", "right": r"鉛直線 \(x=k\) 的斜率 **不存在**"},
                {"wrong": r"\(m_1=m_2\) 就是平行", "right": r"還要 **不重合**（重合是同一條線）"},
                {"wrong": r"垂直是 \(m_1=m_2\)", "right": r"垂直是 \(m_1m_2=-1\)"},
                {"wrong": r"點到直線距離不必取絕對值", "right": r"分子要 **絕對值**、分母是 \(\sqrt{a^2+b^2}\)"},
            ],
            "worked": {
                "q": r"求過點 \((1,2)\)、斜率 \(3\) 的直線方程式。",
                "steps": [
                    {"do": r"點斜式：\(y-2=3(x-1)\)。",
                     "why": r"已知一點 \((x_0,y_0)\) 與斜率 \(m\)，直接套 \(y-y_0=m(x-x_0)\)。"},
                    {"do": r"展開整理：\(y=3x-1\)（即 \(3x-y-1=0\)）。",
                     "why": r"化成常見的斜截式／一般式。"},
                ],
            },
            "questions": [
                {"tag": "114 數A · 單選 2", "level": "★★☆（中）", "core": "直線與兩軸圍成三角形的面積差",
                 "body": r"坐標平面上，\(P(a,0)\) 為 \(x\) 軸上一點，其中 \(a>0\)。令 \(L_1\)、\(L_2\) 為通過 \(P\) 點、斜率分別為 \(-\dfrac43\)、\(-\dfrac32\) 的直線。已知 \(L_1\)、\(L_2\) 分別與兩坐標軸圍成的兩個直角三角形的面積差為 \(3\)，試問 \(a\) 值為何？",
                 "options": [r"\(3\sqrt2\)", r"\(6\)", r"\(6\sqrt2\)", r"\(9\)", r"\(8\sqrt2\)"],
                 "solution": {"brief": r"(2) \(6\)",
                              "steps": [
                                  r"\(L_1\)：\(y=-\dfrac43(x-a)\)，\(x\) 截距 \(a\)、\(y\) 截距 \(\dfrac{4a}{3}\)；圍成面積 \(=\dfrac12\cdot a\cdot\dfrac{4a}{3}=\dfrac{2a^2}{3}\)。",
                                  r"\(L_2\)：\(y=-\dfrac32(x-a)\)，\(y\) 截距 \(\dfrac{3a}{2}\)；面積 \(=\dfrac12\cdot a\cdot\dfrac{3a}{2}=\dfrac{3a^2}{4}\)。",
                                  r"面積差 \(\left|\dfrac{2a^2}{3}-\dfrac{3a^2}{4}\right|=\dfrac{a^2}{12}=3\Rightarrow a^2=36\Rightarrow a=6\)（\(a>0\)）。選 (2)。"]}},
                {"tag": "直線方程式範例", "level": "★☆☆（基礎）", "core": "點到直線距離 · 平行線 · 垂直線",
                 "body": r"設直線 \(L:3x-4y+5=0\)、點 \(P(2,1)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求 \(P\) 到 \(L\) 的距離。",
                      "solution": {"brief": r"\(\dfrac75\)",
                                   "steps": [r"\(\dfrac{|3(2)-4(1)+5|}{\sqrt{3^2+(-4)^2}}=\dfrac{|7|}{5}=\dfrac75\)。"]}},
                     {"label": "(2)", "body": r"求過 \(P\) 且 **平行** \(L\) 的直線方程式。",
                      "solution": {"brief": r"\(3x-4y-2=0\)",
                                   "steps": [r"平行 → 同斜率，設 \(3x-4y+c=0\)，代 \(P\)：\(6-4+c=0\Rightarrow c=-2\)。得 \(3x-4y-2=0\)。"]}},
                     {"label": "(3)", "body": r"求過 \(P\) 且 **垂直** \(L\) 的直線方程式。",
                      "solution": {"brief": r"\(4x+3y-11=0\)",
                                   "steps": [r"\(L\) 斜率 \(\dfrac34\) → 垂直斜率 \(-\dfrac43\)：\(y-1=-\dfrac43(x-2)\Rightarrow 4x+3y-11=0\)。"]}},
                 ]},
                {"tag": "111 數A · 單選 6", "level": "★★★（難）", "core": "正三角形：角平分線垂直對邊 → 求直線",
                 "body": r"坐標平面上兩直線 \(L_1,L_2\) 斜率皆為正，且 \(L_1,L_2\) 有一夾角的平分線斜率為 \(\dfrac{11}{9}\)。另一直線 \(L\) 通過點 \(\left(2,\dfrac13\right)\)，且與 \(L_1,L_2\) 所圍的有界區域為正三角形。試問 \(L\) 的方程式為下列哪一選項？",
                 "options": [
                     r"\(11x-9y=19\)",
                     r"\(9x+11y=25\)",
                     r"\(11x+9y=25\)",
                     r"\(27x-33y=43\)",
                     r"\(27x+33y=65\)"],
                 "solution": {"brief": r"(5) \(27x+33y=65\)",
                              "steps": [
                                  r"正三角形中，頂角（\(L_1,L_2\) 交角）的 **內角平分線就是對邊的中垂線**，故 \(L\perp\)（該平分線）。",
                                  r"平分線斜率 \(\dfrac{11}{9}\) → \(L\) 斜率為其負倒數 \(-\dfrac{9}{11}\)。",
                                  r"\(L\) 過 \(\left(2,\dfrac13\right)\)：\(y-\dfrac13=-\dfrac{9}{11}(x-2)\)，兩邊 \(\times33\)：\(33y-11=-27(x-2)=-27x+54\)，整理得 \(27x+33y=65\)，選 (5)。"]}},
                {"tag": "112 數A · 多選 10", "level": "★★★（難）", "core": "含參數直線與矩形的交點、斜率與範圍",
                 "body": r"坐標平面上直線 \(L:5y+(2k-4)x-10k=0\)（\(k\) 為實數），長方形 \(OABC\) 頂點為 \(O(0,0)、A(10,0)、B(10,6)、C(0,6)\)。設 \(L\) 分別交直線 \(OC\)、直線 \(AB\) 於點 \(D、E\)。試選出正確的選項。",
                 "options": [
                     r"當 \(k=4\) 時，\(L\) 通過點 \(A\)",
                     r"若 \(L\) 通過點 \(C\)，則 \(L\) 斜率為 \(-\dfrac52\)",
                     r"若點 \(D\) 在線段 \(\overline{OC}\) 上，則 \(0\le k\le3\)",
                     r"若 \(k=\dfrac12\)，則線段 \(\overline{DE}\) 在長方形 \(OABC\) 內部（含邊界）",
                     r"若線段 \(\overline{DE}\) 在長方形內部（含邊界），則 \(L\) 斜率可能為 \(\dfrac{3}{10}\)"],
                 "solution": {"brief": r"(1)(3)(5)",
                              "steps": [
                                  r"由 \(L\) 解 \(y=2k-\dfrac{(2k-4)}{5}x\)：\(x=0\)（直線 \(OC\)）得 \(D=(0,2k)\)；\(x=10\)（直線 \(AB\)）得 \(E=(10,\,8-2k)\)。斜率 \(=-\dfrac{2k-4}{5}\)。",
                                  r"(1)○ \(k=4\)：\(E=(10,0)=A\)。",
                                  r"(2)✗ 過 \(C(0,6)\) 需 \(2k=6\Rightarrow k=3\)，斜率 \(=-\dfrac{2}{5}\)，非 \(-\dfrac52\)。",
                                  r"(3)○ \(D=(0,2k)\) 在 \(\overline{OC}\)（\(0\le y\le6\)）\(\Leftrightarrow0\le2k\le6\Leftrightarrow0\le k\le3\)。",
                                  r"(4)✗ \(k=\dfrac12\)：\(E=(10,7)\)，\(y=7>6\) 超出長方形。",
                                  r"(5)○ \(\overline{DE}\) 在內部需 \(D,E\) 的 \(y\) 皆在 \([0,6]\)：\(0\le2k\le6\) 且 \(0\le8-2k\le6\Rightarrow1\le k\le3\)，斜率 \(-\dfrac{2k-4}{5}\in\left[-\dfrac25,\dfrac25\right]\) 含 \(\dfrac{3}{10}\)（\(k=\dfrac54\)）。故選 (1)(3)(5)。"]}},
            ],
            "selfcheck": {
                "q": r"通過 \((1,2)\)、\((4,11)\) 的直線斜率為何？",
                "a": r"**\(3\)**：\(\dfrac{11-2}{4-1}\)。"},
            "strategy": [
                r"看到「距離」就想 **點到直線距離公式**——本單元最高頻、幾乎每年考。",
                r"平行 → 同斜率（設一般式只改常數項）；垂直 → 斜率相乘 \(-1\)。",
                r"直線與兩軸圍三角形：面積 \(=\dfrac12|x\text{截距}|\cdot|y\text{截距}|\)。",
                r"角平分線 ＝ 到兩直線等距，列 \(\dfrac{|L_1|}{\sqrt{\;}}=\dfrac{|L_2|}{\sqrt{\;}}\)（兩條，取 \(\pm\)）。",
            ],
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "兩點距離與三角形",
            "title": r"兩點距離、中點與三角形",
            "intro": r"把平面上的點「算距離、找中點、求重心與面積」。重點是 **兩點距離**、**中點／分點**、**重心與面積**，以及「等腰／直角」的軌跡判斷。",
            "prereq": [
                r"**兩點距離／中點**的平面公式",
                r"**重心** ＝ 三頂點平均（別跟中點混）",
                r"**行列式／坐標面積**公式",
            ],
            "points": [
                {"label": r"兩點距離", "lines": [
                    r"\(A(x_1,y_1)\)、\(B(x_2,y_2)\)：\(\overline{AB}=\) 【\(\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}\)】。"]},
                {"label": r"中點與分點", "lines": [
                    r"中點 \(M=\) 【\(\left(\dfrac{x_1+x_2}{2},\dfrac{y_1+y_2}{2}\right)\)】；",
                    r"\(\overline{AB}\) 上 \(m:n\) 內分點 ＝ 【\(\left(\dfrac{nx_1+mx_2}{m+n},\dfrac{ny_1+my_2}{m+n}\right)\)】。"]},
                {"label": r"三角形重心", "lines": [
                    r"\(\triangle ABC\) 重心 \(G=\) 【\(\left(\dfrac{x_1+x_2+x_3}{3},\dfrac{y_1+y_2+y_3}{3}\right)\)】。"]},
                {"label": r"三角形面積", "lines": [
                    r"面積 ＝ \(\dfrac12\left|(x_2-x_1)(y_3-y_1)-(x_3-x_1)(y_2-y_1)\right|\)；",
                    r"三點共線 \(\Leftrightarrow\) 面積 ＝ 【\(0\)】。"]},
                {"label": r"等腰三角形的軌跡", "lines": [
                    r"\(C\) 使 \(\triangle ABC\) **等腰** 分三類：\(CA=CB\)（\(C\) 在 \(AB\) 中垂線）、\(AB=AC\)（圓心 \(A\)）、\(AB=BC\)（圓心 \(B\)）；",
                    r"務必 **排除三點共線**（退化、不成三角形）。"]},
            ],
            "misconceptions": [
                {"wrong": r"兩點距離忘了開根號", "right": r"\(\sqrt{(\Delta x)^2+(\Delta y)^2}\)"},
                {"wrong": r"重心是各邊中點", "right": r"重心是三 **頂點** 坐標的平均"},
                {"wrong": r"等腰只算一種情形", "right": r"三類都要算（中垂線 ＋ 兩圓）"},
                {"wrong": r"算出的交點全部算數", "right": r"**三點共線要排除**（不成三角形）"},
            ],
            "worked": {
                "q": r"求頂點 \(A(0,0)\)、\(B(4,0)\)、\(C(1,3)\) 的三角形面積。",
                "steps": [
                    {"do": r"面積 \(=\dfrac12|(x_2-x_1)(y_3-y_1)-(x_3-x_1)(y_2-y_1)|\)，代入三頂點。",
                     "why": r"用坐標算三角形面積的公式（行列式／鞋帶法）。"},
                    {"do": r"\(=\dfrac12|(4-0)(3-0)-(1-0)(0-0)|=\dfrac12|12|=6\)。",
                     "why": r"算出來就是面積；若結果為 \(0\) 代表三點共線。"},
                ],
            },
            "questions": [
                {"tag": "115 數A · 單選 6", "level": "★★★（難）", "core": "等腰三角形的點數（中垂線＋兩圓、排除共線）",
                 "body": r"坐標平面上有 \(A(2,-2)\)、\(B(-1,2)\) 兩點，試問直線 \(y=-6\) 上有多少個點 \(C\) 使得 \(\triangle ABC\) 為 **等腰三角形**？",
                 "options": [r"\(1\)", r"\(2\)", r"\(3\)", r"\(4\)", r"\(5\)"],
                 "solution": {"brief": r"(2) \(2\) 個",
                              "steps": [
                                  r"\(\overline{AB}=\sqrt{(2-(-1))^2+(-2-2)^2}=\sqrt{9+16}=5\)；\(C\) 在直線 \(y=-6\) 上，分三類。",
                                  r"**\(CA=CB\)**：\(C\) 在 \(AB\) 中垂線。中點 \((\tfrac12,0)\)、\(AB\) 斜率 \(-\tfrac43\) → 中垂線斜率 \(\tfrac34\)：代 \(y=-6\) 得 \(C(-7.5,-6)\)（\(1\) 點）。",
                                  r"**\(AB=AC=5\)**：圓 \((x-2)^2+(y+2)^2=25\) 交 \(y=-6\) 得 \(x=5\) 或 \(-1\)；但 \((5,-6)\) 與 \(A,B\) **共線**（退化）排除，只剩 \(C(-1,-6)\)（\(1\) 點）。",
                                  r"**\(AB=BC=5\)**：圓 \((x+1)^2+(y-2)^2=25\) 交 \(y=-6\)：\((x+1)^2=-39<0\) 無解（\(0\) 點）。",
                                  r"合計 \(2\) 個，選 (2)。"]}},
                {"tag": "距離與三角形範例", "level": "★☆☆（基礎）", "core": "重心 · 三角形面積",
                 "body": r"設 \(\triangle ABC\) 頂點為 \(A(1,2)\)、\(B(4,3)\)、\(C(2,7)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求重心 \(G\)。",
                      "solution": {"brief": r"\(\left(\dfrac73,4\right)\)",
                                   "steps": [r"\(G=\left(\dfrac{1+4+2}{3},\dfrac{2+3+7}{3}\right)=\left(\dfrac73,4\right)\)。"]}},
                     {"label": "(2)", "body": r"求 \(\triangle ABC\) 的面積。",
                      "solution": {"brief": r"\(7\)",
                                   "steps": [r"面積 \(=\dfrac12|(4-1)(7-2)-(2-1)(3-2)|=\dfrac12|15-1|=7\)。"]}},
                 ]},
            ],
            "selfcheck": {
                "q": r"\(A(0,0),B(6,0),C(3,4)\) 的重心坐標為何？",
                "a": r"**\(\left(3,\dfrac43\right)\)**：三頂點坐標平均。"},
            "strategy": [
                r"「等腰」分三類：\(CA=CB\)（中垂線）、\(AB=AC\)（圓心 \(A\)）、\(AB=BC\)（圓心 \(B\)），最後 **排除共線**。",
                r"三角形面積用「行列式 / 鞋帶公式」最快；面積 \(=0\) 即三點共線。",
                r"重心 ＝ 三頂點平均；中點 ＝ 兩端點平均，別搞混。",
                r"「直角三角形」的點：以某邊為直徑的圓上（Thales）或斜率乘積 \(-1\)。",
            ],
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "圓方程式",
            "title": r"圓方程式與點的位置",
            "intro": r"圓由「**圓心 ＋ 半徑**」決定。要會在標準式與一般式間轉換、由一般式求圓心半徑，並用「**代入比大小**」判斷點在圓內、圓上或圓外。",
            "prereq": [
                r"**配方**（一般式 ↔ 標準式）",
                r"**兩點距離**（半徑、點到圓心）（考點 2）",
                r"圓「**圓心 ＋ 半徑**」的概念",
            ],
            "points": [
                {"label": r"標準式", "lines": [
                    r"圓心 \((h,k)\)、半徑 \(r\)：\((x-h)^2+(y-k)^2=\) 【\(r^2\)】。"]},
                {"label": r"一般式", "lines": [
                    r"\(x^2+y^2+Dx+Ey+F=0\)，圓心 ＝ 【\(\left(-\dfrac{D}{2},-\dfrac{E}{2}\right)\)】、半徑 \(=\dfrac12\sqrt{D^2+E^2-4F}\)；",
                    r"是圓的條件：\(D^2+E^2-4F\) 【\(>0\)】（\(=0\) 為一點、\(<0\) 不存在）。"]},
                {"label": r"點與圓的位置", "lines": [
                    r"把點代入 \((x-h)^2+(y-k)^2-r^2\)：",
                    r"結果 \(<0\) → 在 【圓內】；",
                    r"結果 \(=0\) → 在 【圓上】；",
                    r"結果 \(>0\) → 在 【圓外】；",
                    r"（等價於比較「點到圓心的距離」與半徑 \(r\)）。"]},
                {"svg": SVG_PTCIRCLE, "med": True, "caption": r"圓外一點 \(P\) 到圓的最近／最遠：沿 \(\overline{PO}\) 連線，最近 \(=d-r\)、最遠 \(=d+r\)"},
                {"label": r"由條件定圓", "lines": [
                    r"已知圓上幾點或圓心在某直線上 → 代入待定係數求 \(D,E,F\)；",
                    r"「\(P\) 在圓內、\(Q\) 在圓外」\(\Rightarrow|CQ|>r>|CP|\)，即圓心 \(C\) 離 \(P\) 比離 \(Q\) **近**。"]},
            ],
            "misconceptions": [
                {"wrong": r"一般式半徑是 \(\sqrt{D^2+E^2-4F}\)", "right": r"要再除 \(2\)：\(\dfrac12\sqrt{D^2+E^2-4F}\)"},
                {"wrong": r"\(x^2+y^2+Dx+Ey+F=0\) 一定是圓", "right": r"須 \(D^2+E^2-4F>0\) 才是圓"},
                {"wrong": r"圓心是 \(\left(\dfrac{D}{2},\dfrac{E}{2}\right)\)", "right": r"圓心是 \(\left(-\dfrac{D}{2},-\dfrac{E}{2}\right)\)（變號）"},
                {"wrong": r"點在圓內代入會 \(>0\)", "right": r"圓內代入 \(<0\)（距離 \(<r\)）"},
            ],
            "worked": {
                "q": r"求圓 \(x^2+y^2-6x+8y=0\) 的圓心與半徑。",
                "steps": [
                    {"do": r"對照 \(x^2+y^2+Dx+Ey+F=0\)：\(D=-6,\,E=8,\,F=0\)，圓心 \(\left(-\dfrac D2,-\dfrac E2\right)=(3,-4)\)。",
                     "why": r"一般式的圓心直接讀 \(\left(-\dfrac D2,-\dfrac E2\right)\)（記得變號）。"},
                    {"do": r"半徑 \(=\dfrac12\sqrt{D^2+E^2-4F}=\dfrac12\sqrt{36+64-0}=\dfrac12\sqrt{100}=5\)。",
                     "why": r"半徑公式 \(\dfrac12\sqrt{D^2+E^2-4F}\)，最容易漏掉的是**除以 \(2\)**。"},
                ],
            },
            "questions": [
                {"tag": "106 · 多選 9", "level": "★★★（難）", "core": "由「一點在內、一點在外」定出圓心可在的區域",
                 "body": r"設 \(\Gamma\) 為坐標平面上的圓，點 \((0,0)\) 在 \(\Gamma\) 的 **外部** 且點 \((2,6)\) 在 \(\Gamma\) 的 **內部**。請選出正確的選項。",
                 "options": [
                     r"\(\Gamma\) 的圓心不可能在第二象限",
                     r"\(\Gamma\) 的圓心可能在第三象限，且此時半徑必定大於 \(10\)",
                     r"\(\Gamma\) 的圓心可能在第一象限，且此時半徑必定小於 \(10\)",
                     r"\(\Gamma\) 的圓心可能在 \(x\) 軸上，且此時圓心的 \(x\) 坐標必定小於 \(10\)",
                     r"\(\Gamma\) 的圓心可能在第四象限，且此時半徑必定大於 \(10\)"],
                 "solution": {"brief": r"(5)",
                              "steps": [
                                  r"關鍵：\((0,0)\) 在外、\((2,6)\) 在內 \(\Rightarrow|CO|>r>|CP|\)（\(C\) 圓心、\(P=(2,6)\)）→ **圓心離 \(P\) 比離 \(O\) 近**。",
                                  r"離 \(P,O\) 等距的點在 \(OP\) 中垂線上：\(x^2+y^2=(x-2)^2+(y-6)^2\Rightarrow x+3y=10\)。圓心須在 \(P\) 側 **\(x+3y>10\)**。",
                                  r"(1)✗ 第二象限可以（如 \((-2,5)\)：\(-2+15=13>10\)）。(2)✗ 第三象限 \(x<0,y<0\) 時 \(x+3y<0\)，不可能。",
                                  r"(3)✗ 第一象限可以，但圓心很遠時 \(r\) 可 \(>10\)，非「必定小於」。(4)✗ 圓心在 \(x\) 軸 \((y=0)\) 時 \(x>10\)，非 \(<10\)。",
                                  r"(5)○ 第四象限 \(y<0\) 時 \(x>10-3y>10\)；圓心離 \(P\) 最近趨近 \((10,0)\)、\(|CP|\to10\)，故 \(r>|CP|>10\) 必成立。選 (5)。"]}},
                {"tag": "圓方程式範例", "level": "★☆☆（基礎）", "core": "一般式求圓心半徑 · 點的位置",
                 "body": r"設圓 \(\Gamma:x^2+y^2-4x+6y-12=0\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求 \(\Gamma\) 的圓心與半徑。",
                      "solution": {"brief": r"圓心 \((2,-3)\)、半徑 \(5\)",
                                   "steps": [r"圓心 \(\left(-\dfrac{-4}{2},-\dfrac{6}{2}\right)=(2,-3)\)；半徑 \(\dfrac12\sqrt{(-4)^2+6^2-4(-12)}=\dfrac12\sqrt{16+36+48}=\dfrac12\sqrt{100}=5\)。"]}},
                     {"label": "(2)", "body": r"判斷點 \((3,0)\) 與 \(\Gamma\) 的位置關係。",
                      "solution": {"brief": r"在圓內",
                                   "steps": [r"\((3-2)^2+(0-(-3))^2=1+9=10<25=r^2\)，故點 \((3,0)\) 在 **圓內**。"]}},
                 ]},
            ],
            "selfcheck": {
                "q": r"圓 \(x^2+y^2-4x=0\) 的圓心與半徑為何？",
                "a": r"圓心 **\((2,0)\)**、半徑 **\(2\)**（配方 \((x-2)^2+y^2=4\)）。"},
            "strategy": [
                r"一般式 → 圓心 \(\left(-\dfrac{D}{2},-\dfrac{E}{2}\right)\)、半徑 \(\dfrac12\sqrt{D^2+E^2-4F}\)（**記得除 2**）。",
                r"點在圓內 / 上 / 外：代入 \((x-h)^2+(y-k)^2\) 與 \(r^2\) 比大小。",
                r"「某點在內、某點在外」→ \(|C\text{外}|>r>|C\text{內}|\)，圓心離「內點」較近（中垂線分區）。",
                r"配方把一般式還原成標準式，最不會出錯。",
            ],
        },
        {
            "num": "考點 4", "id": "kp4", "nav": "直線與圓的位置",
            "title": r"直線與圓的位置：相切、弦長與切線",
            "intro": r"判斷直線與圓「相離、相切、相交」，全看 **圓心到直線的距離 \(d\)** 與 **半徑 \(r\)** 的大小。再延伸到 **弦長**、**切線長**——本單元最會考的 ★★★ 重鎮。",
            "prereq": [
                r"**點到直線距離**（考點 1）",
                r"**圓心、半徑**（考點 3）",
                r"**畢氏定理**（弦長、切線長都靠它）",
            ],
            "points": [
                {"label": r"直線與圓的位置", "lines": [
                    r"比較圓心到直線的距離 \(d\) 與半徑 \(r\)：",
                    r"\(d>r\) → 【相離】（無交點）；",
                    r"\(d=r\) → 【相切】（一個交點）；",
                    r"\(d<r\) → 【相交】（兩個交點）。"]},
                {"svg": SVG_CIRCLINE, "caption": r"\(d<r\) 相交：圓心距 \(d\)、半徑 \(r\) 與弦長"},
                {"label": r"看圖解題（弦長 · 114 選16）", "lines": [
                    r"**① 看圖**：圓心到直線的距離 \(d\)、半徑 \(r\)、半條弦 構成 **直角三角形** → 半弦 \(=\sqrt{r^2-d^2}\)。",
                    r"**② 弦長**：\(=2\sqrt{r^2-d^2}\)。",
                    r"**③ 代值**（\(r=\tfrac{13}{5},\,d=1\)）：\(2\sqrt{\tfrac{169}{25}-1}=2\sqrt{\tfrac{144}{25}}=2\cdot\tfrac{12}{5}=\dfrac{24}{5}\)。"]},
                {"label": r"弦長", "lines": [
                    r"直線與圓交於 \(A,B\)（\(d<r\)）：弦長 \(\overline{AB}=\) 【\(2\sqrt{r^2-d^2}\)】（[[怎麼來||圓心到弦的距離 \(d\)、半弦長、半徑構成直角三角形：\(\left(\tfrac{AB}{2}\right)^2+d^2=r^2\)，故半弦 \(=\sqrt{r^2-d^2}\)、全弦 \(2\sqrt{r^2-d^2}\)。]]）。"]},
                {"label": r"切線長", "lines": [
                    r"圓外一點 \(P\) 到圓的切線長 ＝ 【\(\sqrt{|CP|^2-r^2}\)】（\(C\) 為圓心，畢氏定理）。"]},
                {"label": r"切線方程式", "lines": [
                    r"圓 \(x^2+y^2=r^2\) 上一點 \((x_0,y_0)\) 的切線：\(x_0x+y_0y=\) 【\(r^2\)】；",
                    r"過圓外一點求切線：設斜率、用「圓心到直線距離 ＝ \(r\)」解。"]},
            ],
            "misconceptions": [
                {"wrong": r"弦長是 \(\sqrt{r^2-d^2}\)", "right": r"那是 **半弦**；全弦 \(2\sqrt{r^2-d^2}\)"},
                {"wrong": r"\(d=r\) 是相交", "right": r"\(d=r\) 是 **相切**（恰一個交點）"},
                {"wrong": r"切線長是 \(|CP|-r\)", "right": r"是 \(\sqrt{|CP|^2-r^2}\)（畢氏）"},
                {"wrong": r"直線與圓可有三個以上交點", "right": r"最多 **兩個** 交點"},
            ],
            "worked": {
                "q": r"圓半徑 \(r=5\)、圓心到某直線的距離 \(d=4\)。判斷直線與圓的關係，並求弦長。",
                "steps": [
                    {"do": r"\(d=4<r=5\)，故直線與圓 **相交**（兩交點）。",
                     "why": r"比圓心到直線距離 \(d\) 與半徑 \(r\)：\(d<r\) 就是相交。"},
                    {"do": r"弦長 \(=2\sqrt{r^2-d^2}=2\sqrt{25-16}=2\sqrt9=6\)。",
                     "why": r"圓心到弦的距離 \(d\)、半弦、半徑構成直角三角形，半弦 \(=\sqrt{r^2-d^2}\)（畢氏），全弦再乘 \(2\)。"},
                ],
            },
            "questions": [
                {"tag": "114 數A · 選填 16", "level": "★★★（難）", "core": "點到直線距離 ＋ 相切 ＋ 弦長公式",
                 "body": r"坐標平面上，設 \(L_1\)、\(L_2\) 為通過點 \((3,1)\) 且斜率分別為 \(m\)、\(-m\) 的兩條直線（\(m\) 為實數）。另設 \(\Gamma\) 為圓心在原點的圓，已知 \(\Gamma\) 與 \(L_1\) 交於相異兩點 \(A,B\)、圓心到 \(L_1\) 的距離為 \(1\)，又 \(\Gamma\) 與 \(L_2\) 相切。求弦 \(\overline{AB}\) 的長度（最簡分數）。",
                 "solution": {"brief": r"\(\dfrac{24}{5}\)",
                              "steps": [
                                  r"\(L_1:mx-y+(1-3m)=0\)。圓心 \(O\) 到 \(L_1\) 距離 \(=1\)：\(\dfrac{|1-3m|}{\sqrt{m^2+1}}=1\Rightarrow8m^2-6m=0\Rightarrow m=\dfrac34\)（\(m=0\) 會使 \(L_1\) 相切、不合）。",
                                  r"\(L_2\) 斜率 \(-\dfrac34\)，\(\Gamma\) 與 \(L_2\) 相切 → 半徑 \(r=\dfrac{|1+3m|}{\sqrt{m^2+1}}=\dfrac{13/4}{5/4}=\dfrac{13}{5}\)。",
                                  r"弦長 \(\overline{AB}=2\sqrt{r^2-d^2}=2\sqrt{\left(\dfrac{13}{5}\right)^2-1}=2\sqrt{\dfrac{144}{25}}=\dfrac{24}{5}\)。"]}},
                {"tag": "108 · 單選 1", "level": "★★☆（中）", "core": "圓上到定直線等距的點數",
                 "body": r"點 \(A(1,0)\) 在單位圓 \(\Gamma:x^2+y^2=1\) 上。試問 \(\Gamma\) 上除了 \(A\) 點以外，還有幾個點到直線 \(L:y=x\) 的距離，等於 \(A\) 點到 \(L\) 的距離？",
                 "options": [r"\(1\) 個", r"\(2\) 個", r"\(3\) 個", r"\(4\) 個", r"\(0\) 個"],
                 "solution": {"brief": r"(3) \(3\) 個",
                              "steps": [
                                  r"\(A(1,0)\) 到 \(L:x-y=0\) 距離 \(=\dfrac{|1-0|}{\sqrt2}=\dfrac{1}{\sqrt2}\)。",
                                  r"設圓上點 \((\cos\theta,\sin\theta)\)，到 \(L\) 距離 \(=\dfrac{|\cos\theta-\sin\theta|}{\sqrt2}=\dfrac{1}{\sqrt2}\Rightarrow|\cos\theta-\sin\theta|=1\)。",
                                  r"\(\cos\theta-\sin\theta=\sqrt2\cos(\theta+45^\circ)\Rightarrow|\cos(\theta+45^\circ)|=\dfrac{1}{\sqrt2}\Rightarrow\theta\in\{0^\circ,90^\circ,180^\circ,270^\circ\}\)。",
                                  r"對應 \((1,0),(0,1),(-1,0),(0,-1)\)，扣掉 \(A=(1,0)\) 剩 \(3\) 個，選 (3)。"]}},
                {"tag": "114 數A · 多選 8", "level": "★★☆（中）", "core": "指數方程式化簡成圓 ＋ 圓與直線、參數式極值",
                 "body": r"考慮坐標平面上滿足方程式 \(\dfrac{2^{x^2}}{8}=\dfrac{4^{x}}{2^{y^2}}\) 的點 \(P(x,y)\)。試選出正確的選項。",
                 "options": [
                     r"當 \(x=3\) 時，滿足此方程式的解有相異 \(2\) 個",
                     r"若點 \((a,b)\) 滿足此方程式，則點 \((-a,-b)\) 也滿足",
                     r"所有可能的點 \(P(x,y)\) 構成的圖形為一個圓",
                     r"點 \(P(x,y)\) 可能在直線 \(x+y=4\) 上",
                     r"對於所有可能的點 \(P(x,y)\)，\(x-y\) 的最大值為 \(1+2\sqrt2\)"],
                 "solution": {"brief": r"(3)(5)",
                              "steps": [
                                  r"**先化成圓**：全部化為 \(2\) 的次方——\(2^{x^2-3}=2^{2x-y^2}\Rightarrow x^2-3=2x-y^2\Rightarrow(x-1)^2+y^2=4\)，圓心 \((1,0)\)、半徑 \(2\)。(3)○。",
                                  r"(1)✗ \(x=3\)：\((3-1)^2+y^2=4\Rightarrow y^2=0\)，只有 \(y=0\) 一個解。",
                                  r"(2)✗ 圓心 \((1,0)\) 非原點，不對稱於原點（如 \((3,0)\) 在圓上，\((-3,0)\) 不在）。",
                                  r"(4)✗ 圓心到直線 \(x+y-4=0\) 的距離 \(\dfrac{|1+0-4|}{\sqrt2}=\dfrac{3}{\sqrt2}\approx2.12>2\)，直線與圓不相交。",
                                  r"(5)○ 設 \(x=1+2\cos\theta,\,y=2\sin\theta\)：\(x-y=1+2\cos\theta-2\sin\theta=1+2\sqrt2\cos(\theta+45^\circ)\)，最大值 \(1+2\sqrt2\)。故選 (3)(5)。"]}},
            ],
            "selfcheck": {
                "q": r"圓心到某直線距離 \(d=3\)、半徑 \(r=5\)，直線與圓的關係為何？",
                "a": r"**相交（兩交點）**：\(d<r\)。"},
            "strategy": [
                r"直線與圓的關係：算「**圓心到直線距離 \(d\)**」比半徑 \(r\)，一翻兩瞪眼。",
                r"弦長 \(2\sqrt{r^2-d^2}\)、切線長 \(\sqrt{|CP|^2-r^2}\)——都是 **畢氏定理**。",
                r"求切線：設直線、令「圓心到它的距離 \(=r\)」解斜率。",
                r"「圓上到某直線等距」的點數：化成 \(\cos\theta-\sin\theta\) 形式或畫圖數。",
            ],
        },
        {
            "num": "考點 5", "id": "kp5", "nav": "平面區域與線性規劃",
            "title": r"平面區域與線性規劃",
            "intro": r"二元一次不等式 \(ax+by+c>0\) 代表一個 **半平面**；多個不等式的交集是 **可行域**。線性規劃求 \(f=px+qy\) 的極值，答案必在可行域的 **頂點**。",
            "prereq": [
                r"**畫直線**、判斷不等式在直線哪一側（代測試點）",
                r"**解聯立**求兩直線交點（頂點）",
                r"**代入求值** \(f=px+qy\)",
            ],
            "points": [
                {"label": r"二元一次不等式（半平面）", "lines": [
                    r"\(ax+by+c>0\) 表示直線 \(ax+by+c=0\) 的 **某一側**（半平面）；",
                    r"判斷哪一側：**代一個測試點**（常用原點 \((0,0)\)）看是否滿足。"]},
                {"svg": SVG_HALFPLANE, "med": True, "caption": r"直線把平面切成兩個半平面：一側 \(>0\)、另一側 \(<0\)；代測試點即可定哪側"},
                {"label": r"不等式組與可行域", "lines": [
                    r"多個不等式 **同時成立** → 各半平面的 【交集】（可行域），通常為一塊多邊形區域。"]},
                {"label": r"線性規劃", "lines": [
                    r"在可行域上求 \(f=px+qy\) 的最大／最小值：極值必出現在可行域的 【頂點】（角點）；",
                    r"作法：找出所有頂點坐標 → 各自代入 \(f\) → 比大小。"]},
                {"label": r"區域面積", "lines": [
                    r"可行域為多邊形時，用頂點坐標 ＋ 鞋帶公式（或切成三角形）求面積。"]},
            ],
            "misconceptions": [
                {"wrong": r"不等式邊界一律畫實線", "right": r"\(>/<\) 是 **虛線**（不含邊界）、\(\ge/\le\) 才實線"},
                {"wrong": r"線性規劃極值在區域內部", "right": r"極值出現在可行域的 **頂點**（角點）"},
                {"wrong": r"半平面方向用背的", "right": r"**代測試點**（原點最方便）判斷最保險"},
                {"wrong": r"可行域一定是封閉區域", "right": r"也可能 **無界**（此時某方向的極值可能不存在）"},
            ],
            "worked": {
                "q": r"不等式 \(2x+y<4\) 代表哪一側的半平面？",
                "steps": [
                    {"do": r"看邊界線 \(2x+y=4\)，代測試點原點 \((0,0)\)：\(2(0)+0=0<4\) ✓。",
                     "why": r"判斷半平面最快：代一個不在線上的點（原點最方便）看是否滿足。"},
                    {"do": r"原點滿足 → 不等式就是 **含原點那一側** 的半平面（邊界畫虛線、不含）。",
                     "why": r"測試點滿足就取它所在那側；\(<\) 用虛線（不含邊界）。"},
                ],
            },
            "questions": [
                {"tag": "115 數A · 多選 7", "level": "★★☆（中）", "core": "二元一次不等式組所在的象限",
                 "body": r"坐標平面上同時滿足 \(\begin{cases}2x-y-3>0\\[2pt]x+2y+1<0\end{cases}\) 的點 \(P(x,y)\) 可能位在下列哪些選項？",
                 "options": [r"第一象限", r"第二象限", r"第三象限", r"第四象限", r"\(x\) 軸"],
                 "solution": {"brief": r"(3)(4)",
                              "steps": [
                                  r"區域 ＝ \(y<2x-3\) **且** \(y<-\dfrac{x+1}{2}\)（在兩直線下方），兩界線交於 \((1,-1)\)。",
                                  r"第一、二象限（\(y>0\)）：\(x+2y+1<0\) 會要求 \(y\) 很負，與 \(y>0\) 矛盾 → ✗。",
                                  r"(3)○ 取 \((-0.5,-5)\)：兩式皆滿足，落第三象限。(4)○ 取 \((3,-5)\)：兩式皆滿足，落第四象限。",
                                  r"(5)✗ \(y=0\) 時需 \(x>1.5\) 又 \(x<-1\)，矛盾。故選 (3)(4)。"]}},
                {"tag": "線性規劃範例", "level": "★★☆（中）", "core": "可行域頂點代入目標函數",
                 "body": r"設 \(x,y\) 滿足 \(x\ge0\)、\(y\ge0\)、\(x+y\le4\)、\(x+3y\le6\)。求 \(f=3x+2y\) 的最大值。",
                 "solution": {"brief": r"最大值 \(12\)（在 \((4,0)\)）",
                              "steps": [
                                  r"可行域頂點：\((0,0)\)、\((4,0)\)、\((0,2)\)，以及 \(x+y=4\) 與 \(x+3y=6\) 的交點 \((3,1)\)。",
                                  r"代入 \(f=3x+2y\)：\((0,0)\to0\)、\((4,0)\to12\)、\((3,1)\to11\)、\((0,2)\to4\)。",
                                  r"最大值為 \(12\)，在頂點 \((4,0)\) 取得。"]}},
                {"tag": "113 數A · 選填 17", "level": "★★★（難）", "core": "以不等式描述平面區域 → 求面積",
                 "body": r"坐標平面上，在以 \(O(0,0)、A(0,1)、B(1,1)、C(1,0)\) 為頂點的正方形（含邊界）內，令 \(R\) 為滿足下述條件的點 \(P(x,y)\) 所成的區域：與 \(P(x,y)\) 距離為 \(|x-y|\) 的所有點所成圖形，完全落在正方形 \(OABC\)（含邊界）內。求區域 \(R\) 的面積（最簡分數）。",
                 "solution": {"brief": r"\(\dfrac13\)",
                              "steps": [
                                  r"「與 \(P\) 距離為 \(|x-y|\) 的所有點」＝ **以 \(P\) 為圓心、半徑 \(r=|x-y|\) 的圓**。此圓落在正方形內 \(\Leftrightarrow P\) 到四邊的距離都 \(\ge r\)。",
                                  r"即 \(\min(x,\,1-x,\,y,\,1-y)\ge|x-y|\)。由 \(y=x\) 對稱，只算 \(x\ge y\) 部分再乘 \(2\)。",
                                  r"\(x\ge y\) 時 \(|x-y|=x-y\)，四式化簡後只剩 \(y\ge\dfrac{x}{2}\) 與 \(y\ge2x-1\)（另兩式自動成立），上界 \(y\le x\)。",
                                  r"面積（\(x\ge y\) 部分）\(=\displaystyle\int_0^{2/3}\!\!\left(x-\dfrac x2\right)dx+\int_{2/3}^{1}\!\!\big(x-(2x-1)\big)dx=\dfrac19+\left(\dfrac12-\dfrac49\right)=\dfrac16\)。",
                                  r"故 \(R\) 面積 \(=2\times\dfrac16=\dfrac13\)。"]}},
            ],
            "selfcheck": {
                "q": r"可行域頂點為 \((0,0),(2,0),(0,3)\)，求 \(f=x+y\) 的最大值。",
                "a": r"**\(3\)**：頂點代入取最大，於 \((0,3)\)。"},
            "strategy": [
                r"判斷半平面方向：**代測試點**（原點最方便），滿足就取那一側。",
                r"線性規劃極值在 **頂點**：把頂點全找出來、代入目標函數比大小。",
                r"邊界含不含：\(\ge/\le\) 含（實線）、\(>/<\) 不含（虛線）。",
                r"求可行域面積：頂點坐標 ＋ 鞋帶公式（或切成三角形相加）。",
            ],
        },
    ],

    "part2": {
        "count": "10", "note": "難度貼近學測，涵蓋五大考點 · 建議自行限時 40 分鐘作答後再對照詳解",
        "groups": [
            {"title": "一、單選題", "questions": [
                {"tag": "練習 1", "level": "★☆☆", "core": "兩點求斜率",
                 "body": r"通過 \((1,2)\)、\((3,8)\) 的直線斜率為何？",
                 "options": ["2", "3", "4", r"\(\dfrac12\)", r"\(\dfrac13\)"],
                 "solution": {"brief": "(2) 3", "brief_label": "答",
                              "steps": [r"\(m=\dfrac{8-2}{3-1}=\dfrac63=3\)。"]}},
                {"tag": "練習 2", "level": "★☆☆", "core": "點到直線距離",
                 "body": r"原點到直線 \(3x+4y-10=0\) 的距離為何？",
                 "options": ["1", "2", "3", "4", "5"],
                 "solution": {"brief": "(2) 2", "brief_label": "答",
                              "steps": [r"\(\dfrac{|3(0)+4(0)-10|}{\sqrt{3^2+4^2}}=\dfrac{10}{5}=2\)。"]}},
                {"tag": "練習 3", "level": "★☆☆", "core": "兩點距離",
                 "body": r"\(A(1,2)\)、\(B(4,6)\) 兩點的距離為何？",
                 "options": ["4", "5", r"\(\sqrt{7}\)", r"\(2\sqrt5\)", "7"],
                 "solution": {"brief": "(2) 5", "brief_label": "答",
                              "steps": [r"\(\overline{AB}=\sqrt{(4-1)^2+(6-2)^2}=\sqrt{9+16}=5\)。"]}},
                {"tag": "練習 4", "level": "★★☆", "core": "一般式求圓心半徑",
                 "body": r"圓 \(x^2+y^2-6x+8y=0\) 的圓心與半徑為何？",
                 "options": [r"圓心 \((3,-4)\)、半徑 \(5\)", r"圓心 \((-3,4)\)、半徑 \(5\)", r"圓心 \((3,-4)\)、半徑 \(10\)", r"圓心 \((-3,4)\)、半徑 \(10\)", r"圓心 \((6,-8)\)、半徑 \(5\)"],
                 "solution": {"brief": r"(1) 圓心 \((3,-4)\)、半徑 \(5\)", "brief_label": "答",
                              "steps": [r"圓心 \(\left(-\dfrac{-6}{2},-\dfrac{8}{2}\right)=(3,-4)\)；半徑 \(\dfrac12\sqrt{36+64-0}=\dfrac12\cdot10=5\)。"]}},
                {"tag": "練習 5", "level": "★★☆", "core": "直線與圓的位置",
                 "body": r"直線 \(x+y=1\) 與圓 \(x^2+y^2=4\) 的位置關係為何？",
                 "options": ["相離", "相切", "相交於兩點", "直線在圓內無交點", "無法判斷"],
                 "solution": {"brief": "(3) 相交於兩點", "brief_label": "答",
                              "steps": [r"圓心 \((0,0)\) 到直線 \(x+y-1=0\) 距離 \(d=\dfrac{1}{\sqrt2}\approx0.71\)，半徑 \(r=2\)；\(d<r\) → 相交於兩點。"]}},
            ]},
            {"title": "二、多選題", "questions": [
                {"tag": "練習 6", "level": "★★★", "core": "直線的斜率、截距、平行垂直",
                 "body": r"設直線 \(L:2x-y+3=0\)，下列敘述何者正確？",
                 "options": [
                     r"\(L\) 的斜率為 \(2\)",
                     r"\(L\) 通過點 \((0,3)\)",
                     r"\(L\) 與 \(4x-2y+1=0\) 平行",
                     r"\(L\) 與 \(x+2y=5\) 垂直",
                     r"原點到 \(L\) 的距離為 \(3\)"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"(1)○ 斜率 \(-\dfrac{2}{-1}=2\)。(2)○ \(x=0\Rightarrow y=3\)。(3)○ \(4x-2y+1=0\) 斜率也是 \(2\)。",
                                        r"(4)○ \(x+2y=5\) 斜率 \(-\dfrac12\)，\(2\times(-\dfrac12)=-1\)。(5)✗ 距離 \(\dfrac{|3|}{\sqrt5}=\dfrac{3}{\sqrt5}\neq3\)。"]}},
                {"tag": "練習 7", "level": "★★★", "core": "圓與直線相切",
                 "body": r"設圓 \(C:x^2+y^2=25\)、直線 \(L:3x+4y=25\)，下列敘述何者正確？",
                 "options": [
                     r"\(C\) 的圓心為 \((0,0)\)、半徑 \(5\)",
                     r"圓心到 \(L\) 的距離為 \(5\)",
                     r"\(L\) 與 \(C\) 相切",
                     r"切點為 \((3,4)\)",
                     r"\(L\) 與 \(C\) 交於相異兩點"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"(1)○ 標準式直接讀。(2)○ \(\dfrac{|3(0)+4(0)-25|}{\sqrt{9+16}}=\dfrac{25}{5}=5\)。(3)○ \(d=r=5\) → 相切。",
                                        r"(4)○ \((3,4)\) 同時在 \(C\)（\(9+16=25\)）與 \(L\)（\(9+16=25\)）上。(5)✗ 相切只有 **一個** 交點。"]}},
            ]},
            {"title": "三、選填題", "questions": [
                {"tag": "練習 8", "level": "★★☆", "core": "弦長公式",
                 "body": r"圓 \(x^2+y^2=25\) 被直線 \(y=3\) 所截的弦長為何？",
                 "solution": {"brief": "8", "brief_label": "答",
                              "steps": [r"圓心 \((0,0)\) 到 \(y=3\) 的距離 \(d=3\)、半徑 \(r=5\)。弦長 \(=2\sqrt{r^2-d^2}=2\sqrt{25-9}=2\cdot4=8\)。"]}},
                {"tag": "練習 9", "level": "★★☆", "core": "線性規劃",
                 "body": r"設 \(x\ge0,\ y\ge0,\ 2x+y\le8,\ x+y\le5\)。求 \(f=x+2y\) 的最大值。",
                 "solution": {"brief": "10", "brief_label": "答",
                              "steps": [r"頂點 \((0,0),(4,0),(0,5)\)，及 \(2x+y=8\) 與 \(x+y=5\) 的交點 \((3,2)\)。",
                                        r"代入 \(f=x+2y\)：\(0,\,4,\,10,\,7\)。最大值 \(10\)（在 \((0,5)\)）。"]}},
                {"tag": "練習 10", "level": "★★☆", "core": "圓上一點的切線",
                 "body": r"求過圓 \(x^2+y^2=10\) 上一點 \((1,3)\) 的切線方程式。",
                 "solution": {"brief": r"\(x+3y=10\)", "brief_label": "答",
                              "steps": [r"圓 \(x^2+y^2=r^2\) 上 \((x_0,y_0)\) 的切線 \(x_0x+y_0y=r^2\)：\(1\cdot x+3\cdot y=10\)，即 \(x+3y=10\)。"]}},
            ]},
        ],
    },

    "part3": {
        "ref_table": [
            {"k": "斜率", "v": r"\(m=\dfrac{y_2-y_1}{x_2-x_1}=\tan\theta\)；鉛直線無斜率"},
            {"k": "直線方程式", "v": r"點斜式 \(y-y_0=m(x-x_0)\)；一般式 \(ax+by+c=0\) 斜率 \(-\dfrac{a}{b}\)"},
            {"k": "平行 / 垂直", "v": r"平行 \(m_1=m_2\)（不重合）；垂直 \(m_1m_2=-1\)"},
            {"k": "點到直線距離", "v": r"\(\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}\)（最高頻工具）"},
            {"k": "角平分線", "v": r"到兩直線等距 \(\dfrac{|L_1|}{\sqrt{\,}}=\dfrac{|L_2|}{\sqrt{\,}}\)（兩條、互相垂直）"},
            {"k": "距離 / 中點 / 重心", "v": r"\(\sqrt{(\Delta x)^2+(\Delta y)^2}\)；中點取平均；重心取三頂點平均"},
            {"k": "三角形面積", "v": r"\(\dfrac12|(x_2-x_1)(y_3-y_1)-(x_3-x_1)(y_2-y_1)|\)；\(=0\) 即共線"},
            {"k": "圓（標準 / 一般式）", "v": r"\((x-h)^2+(y-k)^2=r^2\)；圓心 \(\left(-\dfrac{D}{2},-\dfrac{E}{2}\right)\)、\(r=\dfrac12\sqrt{D^2+E^2-4F}\)"},
            {"k": "點與圓", "v": r"代入 \((x-h)^2+(y-k)^2-r^2\)：\(<0\) 內、\(=0\) 上、\(>0\) 外"},
            {"k": "直線與圓", "v": r"圓心到線距 \(d\) 比半徑 \(r\)：\(d>r\) 離、\(d=r\) 切、\(d<r\) 交"},
            {"k": "弦長 / 切線長", "v": r"弦長 \(2\sqrt{r^2-d^2}\)；切線長 \(\sqrt{|CP|^2-r^2}\)"},
            {"k": "圓上切線", "v": r"\(x^2+y^2=r^2\) 上 \((x_0,y_0)\)：\(x_0x+y_0y=r^2\)"},
            {"k": "線性規劃", "v": r"半平面交集為可行域；\(f=px+qy\) 極值在 **頂點**"},
        ],
        "checklist": [
            r"點到直線距離：分子 **絕對值**、分母 \(\sqrt{a^2+b^2}\)——本單元最高頻。",
            r"鉛直線 \(x=k\) 無斜率。",
            r"平行還要 **不重合**；垂直是 \(m_1m_2=-1\)。",
            r"圓一般式：圓心 \(\left(-\dfrac{D}{2},-\dfrac{E}{2}\right)\)、半徑 \(\dfrac12\sqrt{D^2+E^2-4F}\)（**記得除 2**）。",
            r"點在圓內代入 \(<0\)（距離 \(<r\)）。",
            r"直線與圓：\(d>r\) 離、\(d=r\) 切、\(d<r\) 交。",
            r"弦長 \(2\sqrt{r^2-d^2}\) 是 **全弦**；切線長 \(\sqrt{|CP|^2-r^2}\)。",
            r"等腰三角形的點分三類（中垂線＋兩圓），**排除三點共線**。",
            r"線性規劃極值在 **頂點**：頂點都代入比大小。",
            r"不等式邊界：\(\ge/\le\) 實線（含）、\(>/<\) 虛線（不含）。",
            r"「某點在圓內、某點在圓外」→ 圓心離內點較近（中垂線分區）。",
        ],
    },
}
