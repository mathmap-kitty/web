# -*- coding: utf-8 -*-
r"""指數與對數單元 · 單一來源內容（單元3：指數與對數）。

挖空原則：只挖「公式與概念關鍵」（自行判斷）。
例題以官方原卷（106~115學測數學試卷.pdf）為準，答案對官方答案頁校正；數 B 題不採用。

考點對應核心概念分析（單元3）五大主軸：
  ① 指數律與指數方程  ② 對數的定義與運算  ③ 常用對數（科學記號、位數）
  ④ 指數對數函數圖形  ⑤ 應用模型與數列結合
※ 本檔逐考點建置中；先 Part 0＋考點 1。
"""

# 指數 y=2^x 與對數 y=log₂x 圖形：互為反函數，對 y=x 鏡射對稱
SVG_EXPLOG = r'''<svg viewBox="0 0 170 168" width="170" height="168" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,'Segoe UI',sans-serif">
  <line x1="4" y1="128" x2="128" y2="128" stroke="#9aa6b2" stroke-width="1.3"/>
  <line x1="38" y1="164" x2="38" y2="40" stroke="#9aa6b2" stroke-width="1.3"/>
  <polygon points="133,128 125,124 125,132" fill="#9aa6b2"/>
  <polygon points="38,35 34,43 42,43" fill="#9aa6b2"/>
  <polyline points="12,154 124,42" fill="none" stroke="#b0b8c0" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="4,117 12,115 20,112 28,108 35,104 43,98 51,91 59,83 67,72 74,59 82,44" fill="none" stroke="#1f6f78" stroke-width="2.2"/>
  <polyline points="51,154 54,147 56,141 60,134 64,128 69,121 74,115 82,108 90,102 103,94 116,87 129,81" fill="none" stroke="#c0392b" stroke-width="2.2"/>
  <circle cx="38" cy="102" r="2.5" fill="#1f6f78"/><circle cx="64" cy="128" r="2.5" fill="#c0392b"/>
  <g fill="#555" font-size="8"><text x="58" y="140">1</text><text x="27" y="106">1</text><text x="27" y="140">O</text></g>
  <g font-size="10.5" font-weight="bold">
    <text x="50" y="44" fill="#1f6f78">y=2&#739;</text>
    <text x="92" y="108" fill="#c0392b">y=log&#8322;x</text>
    <text x="106" y="52" fill="#8a93a0">y=x</text>
  </g>
</svg>'''

# 指數／對數函數圖形四型（a>1 / 0<a<1）— 程式產生
import math as _math
_EF = "font-family=\"'Microsoft JhengHei',system-ui,sans-serif\""

def _el_axes(ox, oy, x0, x1, ytop):
    AX = "#9aa6b2"
    return (f'<line x1="{x0}" y1="{oy}" x2="{x1}" y2="{oy}" stroke="{AX}" stroke-width="1.1"/>'
            f'<polygon points="{x1+6},{oy} {x1-2},{oy-3} {x1-2},{oy+3}" fill="{AX}"/>'
            f'<line x1="{ox}" y1="{oy+8}" x2="{ox}" y2="{ytop}" stroke="{AX}" stroke-width="1.1"/>'
            f'<polygon points="{ox},{ytop-6} {ox-3},{ytop+2} {ox+3},{ytop+2}" fill="{AX}"/>')

def _explog4_fig():
    INK = "#2c3e50"; CURVE = "#34679a"; KEY = "#c0392b"; ROSE = "#b03a5b"
    cxs = [47, 141, 235, 329]
    L = [f'<svg viewBox="0 0 376 150" width="376" height="150" xmlns="http://www.w3.org/2000/svg" role="img" {_EF}>']
    L.append('<g stroke="#e6e0e8" stroke-width="1">')
    for x in [94, 188, 282]:
        L.append(f'<line x1="{x}" y1="6" x2="{x}" y2="144"/>')
    L.append('</g>')
    def cell(cx, kind, agt1):
        g = []; a = 2.4 if agt1 else 1/2.4
        if kind == 'exp':
            Ox, Oy, sX, sY = cx-12, 100, 15, 11
            g.append(_el_axes(Ox, Oy, cx-42, cx+40, 32))
            pts = []; x = -2.2
            while x <= 2.3:
                y = a**x
                if 0 <= y <= 6.2: pts.append(f"{Ox+x*sX:.1f},{Oy-y*sY:.1f}")
                x += 0.12
            g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CURVE}" stroke-width="2.2"/>')
            g.append(f'<circle cx="{Ox}" cy="{Oy-sY}" r="2.6" fill="{KEY}"/>')
            g.append(f'<text x="{Ox-4}" y="{Oy-sY+3}" font-size="8" fill="{INK}" text-anchor="end">1</text>')
        else:
            Ox, Oy, sX, sY = cx-30, 66, 17, 16
            g.append(_el_axes(Ox, Oy, cx-40, cx+42, 26))
            pts = []; x = 0.14
            while x <= 4.0:
                y = _math.log(x, a)
                if -2.4 <= y <= 2.4: pts.append(f"{Ox+x*sX:.1f},{Oy-y*sY:.1f}")
                x += 0.08
            g.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CURVE}" stroke-width="2.2"/>')
            g.append(f'<circle cx="{Ox+sX}" cy="{Oy}" r="2.6" fill="{KEY}"/>')
            g.append(f'<text x="{Ox+sX}" y="{Oy+13}" font-size="8" fill="{INK}" text-anchor="middle">1</text>')
        return "".join(g)
    specs = [('exp', True, 'y = aˣ', 'a &gt; 1'), ('exp', False, 'y = aˣ', '0 &lt; a &lt; 1'),
             ('log', True, 'y = logₐx', 'a &gt; 1'), ('log', False, 'y = logₐx', '0 &lt; a &lt; 1')]
    for cx, (kind, agt1, f1, f2) in zip(cxs, specs):
        L.append(cell(cx, kind, agt1))
        L.append(f'<text x="{cx}" y="18" font-size="11" fill="{ROSE}" text-anchor="middle" font-weight="bold">{f1}</text>')
        L.append(f'<text x="{cx}" y="32" font-size="9.5" fill="{INK}" text-anchor="middle">{f2}</text>')
        L.append(f'<text x="{cx}" y="140" font-size="9.5" fill="#5a4a52" text-anchor="middle">{"遞增" if agt1 else "遞減"}</text>')
    L.append('</svg>')
    return "".join(L)

SVG_EXPLOG4 = _explog4_fig()

import soil_maps  # Part 0 單元知識地圖（SOIL 章節圖）

UNIT = {
    "slug": "explog",
    "file": "115學測數學_指數與對數.html",
    "page_title": "115 學測數學 · 指數與對數",
    "emoji": "📉",
    "title": "指數與對數",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 五大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "五大考點",
    "foot": "115 學測數學 · 指數與對數 · 學測數學重點整理",

    "part0": {
        "opener": {"svg": soil_maps.SLIDES["explog"], "hero": True,
                   "caption": r"**單元知識地圖**：先備 → 各考點（★越多＝越常考） → 跨單元最愛綁考 → 帶走一句話"},
        "heading": "為什麼指數與對數是計算題的得分關鍵",
        "trend_table": {
            "years": [106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            "counts": ["2.0", "2.0", "2.0", "1.5", "2.5", "1.5", "2.0", "2.0", "1.5", "0.8"],
            "total": "17.8",
        },
        "notes": [
            r"**題數穩定（近十年約 \(17.8\) 題）**：數 A 幾乎年年 \(1.5\)–\(2.5\) 題，是計算題的得分關鍵。",
            r"**兩大 ★★★ 核心**：指數／對數函數圖形與模型、與數列／數據的結合。",
            r"**工具固定**：指數律、\(\log\) 性質、換底、科學記號——熟練就能又快又準。",
            r"**常跨單元整合**：與數列（等差等比取 \(\log\)）、數據分析（取 \(\log\) 迴歸）、直線與圓（\(\log\) 共線）結合。",
        ],
        "map": r"命題主軸五條：① 指數律與指數方程 ② 對數的定義與運算 ③ 常用對數（科學記號、位數）④ 指數對數函數圖形 ⑤ 應用模型與數列結合。",
    },

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "指數律與指數方程",
            "title": r"指數律與指數方程",
            "intro": r"**指數就是「連乘」的簡記**：\(2^3\) 就是 \(2\) 連乘 \(3\) 次。抓住這一點，指數律全都能「**數出來**」——\(2^3\times2^2=(2\cdot2\cdot2)\times(2\cdot2)=2^5\)，數一數 \(2\) 的個數，就知道同底相乘指數要**相加**；\((2^3)^2=2^3\times2^3=2^6\)，所以「次方再次方」是**相乘**。本考點就是把這些規則練熟，再用「**化成同底**」來解指數方程。",
            "prereq": [
                r"**次方的意思**：\(a^n\) 是 \(a\) 連乘 \(n\) 次（\(2^3=2\cdot2\cdot2=8\)）",
                r"**平方根**：\(\sqrt a\) 是「平方後會變回 \(a\)」的正數（\(\sqrt9=3\)）",
                r"**一次方程移項**求未知數（會解 \(x+1=3\) 得 \(x=2\)）",
            ],
            "points": [
                {"label": r"指數律", "lines": [
                    r"\(a^m\cdot a^n=\) 【\(a^{m+n}\)】（同底相乘、指數相加）；",
                    r"\(\dfrac{a^m}{a^n}=\) 【\(a^{m-n}\)】（同底相除、指數相減）；",
                    r"\((a^m)^n=\) 【\(a^{mn}\)】（次方再次方、指數相乘）；",
                    r"\((ab)^n=\) 【\(a^nb^n\)】（積的次方）。"]},
                {"label": r"零與負指數", "lines": [
                    r"\(a^0=\) 【\(1\)】（\(a\neq0\)）、\(a^{-n}=\) 【\(\dfrac{1}{a^n}\)】。"]},
                {"label": r"分數指數（根式）", "lines": [
                    r"\(a^{1/n}=\sqrt[n]{a}\)、\(a^{m/n}=\) 【\(\sqrt[n]{a^m}\)】（\(a>0\)）；",
                    r"**連續開 \(n\) 次平方根**（開完的結果再開、共開 \(n\) 次）＝ 取 \(\left(\dfrac12\right)^n=\dfrac{1}{2^n}\) 次方（[[舉例||一次平方根是 \(a^{1/2}\)；連開 \(3\) 次：\(\sqrt{\sqrt{\sqrt a}}=a^{1/2}\to a^{1/4}\to a^{1/8}=a^{1/2^3}\)。這正是 \(112\) 單1 的考點。]]）。"]},
                {"label": r"解指數方程", "lines": [
                    r"**化成同底**：\(a^{f(x)}=a^{g(x)}\Rightarrow f(x)=\) 【\(g(x)\)】（\(a>0,a\neq1\)）；",
                    r"無法化同底時，**兩邊取對數**。"]},
            ],
            "misconceptions": [
                {"wrong": r"\((a^m)^n=a^{m+n}\)", "right": r"\((a^m)^n=a^{mn}\)；\(a^m\cdot a^n\) 才是指數相加"},
                {"wrong": r"\(a^{m/n}=\dfrac{a^m}{n}\)", "right": r"\(a^{m/n}=\sqrt[n]{a^m}\)（分母是 **根次**）"},
                {"wrong": r"\((a+b)^n=a^n+b^n\)", "right": r"指數律只對 **乘法** 成立，對加法不可拆"},
                {"wrong": r"\(a^0=0\)", "right": r"\(a^0=1\)（\(a\neq0\)）"},
            ],
            "worked": {
                "q": r"解指數方程 \(2^{x+1}=8\)。",
                "steps": [
                    {"do": r"\(8=2^3\)，原式變成 \(2^{x+1}=2^3\)。",
                     "why": r"指數律只能在「**同底**」時用，所以先把右邊的 \(8\) 也湊成 \(2\) 的次方。"},
                    {"do": r"\(x+1=3\)。",
                     "why": r"底數相同（且底 \(\neq1\)）時，**兩邊的指數一定相等**——這就是「化成同底」的用處。"},
                    {"do": r"\(x=2\)。",
                     "why": r"剩下就是移項解一次方程。"},
                ],
            },
            "questions": [
                {"tag": "108 · 單選 3", "level": "★★☆（中）", "core": "指數方程化同底 → 一次方程的正整數解",
                 "body": r"試問共有多少組正整數 \((k,m,n)\) 滿足 \(2^k\cdot4^m\cdot8^n=512\)？",
                 "options": [r"\(1\) 組", r"\(2\) 組", r"\(3\) 組", r"\(4\) 組", r"\(0\) 組"],
                 "solution": {"brief": r"(3) \(3\) 組",
                              "steps": [
                                  r"化同底 \(2\)：\(2^k\cdot2^{2m}\cdot2^{3n}=2^{k+2m+3n}=2^9\Rightarrow k+2m+3n=9\)。",
                                  r"求正整數解（\(k,m,n\ge1\)）：\(k=9-2m-3n\ge1\Rightarrow2m+3n\le8\)。",
                                  r"\(n=1\)：\(2m\le5\Rightarrow m=1,2\)；\(n=2\)：\(2m\le2\Rightarrow m=1\)；\(n\ge3\) 不合。共 \((m,n)=(1,1),(2,1),(1,2)\)，**3 組**，選 (3)。"]}},
                {"tag": "112 數A · 單選 1", "level": "★☆☆（基礎）", "core": "連續開平方根（分數指數）",
                 "body": r"在計算器中鍵入某正整數 \(N\)，接著連按「\(\sqrt{\;\;}\)」鍵（取正平方根）\(3\) 次，視窗顯示得到答案為 \(2\)，則 \(N\) 等於下列哪一個選項？",
                 "options": [r"\(2^3\)", r"\(2^4\)", r"\(2^6\)", r"\(2^8\)", r"\(2^{12}\)"],
                 "solution": {"brief": r"(4) \(2^8\)",
                              "steps": [
                                  r"連按 \(\sqrt{\;}\) 三次 ＝ 取 \(\left(\dfrac12\right)^3=\dfrac18\) 次方：\(N^{1/8}=2\)。",
                                  r"兩邊 \(8\) 次方：\(N=2^8\)，選 (4)。"]}},
            ],
            "selfcheck": {
                "q": r"\(8^{2/3}\) 之值為何？",
                "a": r"**\(4\)**：\((2^3)^{2/3}=2^2\)。"},
            "strategy": [
                r"看到指數方程先想 **化成同底**，再讓指數相等。",
                r"根式 ↔ 分數指數：\(\sqrt[n]{a^m}=a^{m/n}\)；連開 \(k\) 次平方根 ＝ 乘 \(\dfrac{1}{2^k}\) 次方。",
                r"次方再次方 **相乘**（\((a^m)^n=a^{mn}\)）、同底相乘 **相加**，別記反。",
                r"指數律只對「乘除、次方」成立，對「加減」不可拆。",
            ],
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "對數的定義與運算",
            "title": r"對數的定義、運算法則與換底",
            "intro": r"**對數就是『反過來問指數』**：\(\log_2 8\) 是在問「\(2\) 要幾次方才會變成 \(8\)？」——答案 \(3\)，所以 \(\log_2 8=3\)。一句話，\(\log_a N=x\) 和 \(a^x=N\) 在說同一件事。看懂這層，運算法則（積化加、商化減、次方化乘）和換底都只是它的延伸。",
            "prereq": [
                r"**指數會算**：\(2^3=8\)、\(10^2=100\)（考點 1）",
                r"**反過來想指數**：看到 \(2^?=8\) 要能答 \(3\)",
                r"**分數約分／通分**（換底公式會用到）",
            ],
            "points": [
                {"label": r"定義", "lines": [
                    r"\(\log_a N=x\Leftrightarrow\) 【\(a^x=N\)】（\(a>0,a\neq1,N>0\)）；",
                    r"\(\log_a1=0\)、\(\log_a a=1\)、\(a^{\log_a N}=N\)。"]},
                {"label": r"對數運算法則", "lines": [
                    r"\(\log_a(MN)=\) 【\(\log_a M+\log_a N\)】（積化加）；",
                    r"\(\log_a\dfrac{M}{N}=\) 【\(\log_a M-\log_a N\)】（商化減）；",
                    r"\(\log_a M^k=\) 【\(k\log_a M\)】（次方化乘）。"]},
                {"label": r"換底公式", "lines": [
                    r"\(\log_a b=\) 【\(\dfrac{\log_c b}{\log_c a}\)】（換成任意底 \(c\)）；",
                    r"特例 \(\log_a b=\dfrac{1}{\log_b a}\)（[[倒數關係||換底取 \(c=b\)：\(\log_a b=\dfrac{\log_b b}{\log_b a}=\dfrac{1}{\log_b a}\)。所以 \(\log_a b\) 與 \(\log_b a\) **互為倒數**——\(111\) 單2 就用這個。]]）。"]},
                {"label": r"常用對數", "lines": [
                    r"\(\log\) 不寫底 ＝ 以 \(10\) 為底；\(\log10^k=\) 【\(k\)】。"]},
            ],
            "tables": [
                {"title": r"指數律 ↔ 對數律 對照（互為反運算，一一對應）",
                 "head": [r"指數律", r"對應的對數律"],
                 "rows": [
                     [r"\(a^m\cdot a^n=a^{m+n}\)（乘 → 指數相加）", r"\(\log_a(MN)=\log_a M+\log_a N\)（乘 → 對數相加）"],
                     [r"\(\dfrac{a^m}{a^n}=a^{m-n}\)（除 → 指數相減）", r"\(\log_a\dfrac{M}{N}=\log_a M-\log_a N\)（除 → 對數相減）"],
                     [r"\((a^m)^n=a^{mn}\)（次方 → 指數相乘）", r"\(\log_a M^k=k\log_a M\)（次方 → 提到前面乘）"],
                     [r"\(a^0=1\)", r"\(\log_a 1=0\)"],
                     [r"\(a^1=a\)", r"\(\log_a a=1\)"],
                 ]},
            ],
            "misconceptions": [
                {"wrong": r"\(\log(M+N)=\log M+\log N\)", "right": r"是 \(\log(MN)=\log M+\log N\)；**和不可拆**"},
                {"wrong": r"\(\dfrac{\log M}{\log N}=\log\dfrac{M}{N}\)", "right": r"商化減是 \(\log\dfrac{M}{N}=\log M-\log N\)；左式是 **換底**"},
                {"wrong": r"\(\log_a b=\log_b a\)", "right": r"兩者 **互為倒數**，一般不相等"},
                {"wrong": r"\(\log\) 負數也有值", "right": r"真數必須 \(>0\)"},
            ],
            "worked": {
                "q": r"求 \(\log 4+\log 25\) 的值（\(\log\) 為常用對數，底 \(10\)）。",
                "steps": [
                    {"do": r"\(\log 4+\log 25=\log(4\times25)\)。",
                     "why": r"對數法則「積化加」反過來用：兩個 \(\log\) 相加，可併成「相乘」的一個 \(\log\)。"},
                    {"do": r"\(=\log 100\)。",
                     "why": r"先把好算的乘起來：\(4\times25=100\)。"},
                    {"do": r"\(=2\)。",
                     "why": r"回到定義問「\(10\) 的幾次方是 \(100\)」——是 \(2\)。"},
                ],
            },
            "questions": [
                {"tag": "108 · 單選 5", "level": "★★☆（中）", "core": "對數方程：湊因式分解 (u+1)(v+1)",
                 "body": r"設正實數 \(b\) 滿足 \((\log100)(\log b)+\log100+\log b=7\)。試問 \(b\) 落在下列哪一範圍？",
                 "options": [r"\(1\le b\le\sqrt{10}\)", r"\(\sqrt{10}\le b\le10\)", r"\(10\le b\le10\sqrt{10}\)", r"\(10\sqrt{10}\le b\le100\)", r"\(100\le b\le100\sqrt{10}\)"],
                 "solution": {"brief": r"(4) \(10\sqrt{10}\le b\le100\)",
                              "steps": [
                                  r"令 \(u=\log100=2\)、\(v=\log b\)，原式 \(uv+u+v=7\)，加 \(1\) 湊因式：\((u+1)(v+1)=8\)。",
                                  r"\((2+1)(v+1)=8\Rightarrow v+1=\dfrac83\Rightarrow v=\log b=\dfrac53\)。",
                                  r"\(\log b=\dfrac53\approx1.67\in[1.5,2]\)，即 \(10\sqrt{10}\le b\le100\)（\(b=10^{5/3}\approx46.4\)）。選 (4)。"]}},
                {"tag": "111 數A · 單選 2", "level": "★★☆（中）", "core": "換底公式（log_a b 與 log_b a 互為倒數）",
                 "body": r"某計算機算 \(\log_a b\) 需按 \(\log(a,b)\)。某生在計算 \(\log_a b\) 時（\(a>1\) 且 \(b>1\)）順序弄錯、誤按 \(\log(b,a)\)，所得為正確值的 \(\dfrac94\) 倍。試選出 \(a,b\) 間的關係式。",
                 "options": [r"\(a^2=b^3\)", r"\(a^3=b^2\)", r"\(a^4=b^9\)", r"\(2a=3b\)", r"\(3a=2b\)"],
                 "solution": {"brief": r"(1) \(a^2=b^3\)",
                              "steps": [
                                  r"正確值 \(\log_a b\)、誤按得 \(\log_b a\)，已知 \(\log_b a=\dfrac94\log_a b\)。",
                                  r"設 \(t=\log_a b>0\)，由倒數關係 \(\log_b a=\dfrac1t\)：\(\dfrac1t=\dfrac94t\Rightarrow t^2=\dfrac49\Rightarrow t=\dfrac23\)。",
                                  r"\(\log_a b=\dfrac23\Rightarrow b=a^{2/3}\Rightarrow b^3=a^2\)，即 \(a^2=b^3\)。選 (1)。"]}},
            ],
            "selfcheck": {
                "q": r"\(\log_2 8+\log_2\dfrac14\) 之值為何？",
                "a": r"**\(1\)**：\(3+(-2)\)。"},
            "strategy": [
                r"對數三法則：**積化加、商化減、次方化乘**。",
                r"換底公式把不同底統一；\(\log_a b\) 與 \(\log_b a\) **互為倒數**。",
                r"「\(uv+u+v\)」型湊 \((u+1)(v+1)\) 因式分解最快。",
                r"先檢查定義域：真數 \(>0\)、底 \(>0\) 且 \(\neq1\)。",
            ],
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "常用對數（科學記號、位數）",
            "title": r"常用對數：科學記號、位數與首位",
            "intro": r"**位數其實藏在 \(\log\) 裡**：一個數有幾位，看它「比 \(10\) 的幾次方大」就知道——\(100=10^2\) 是 \(3\) 位、\(1000=10^3\) 是 \(4\) 位，發現了嗎？**位數 ＝ \(\log\) 的整數部分 \(+1\)**。所以把大數取 \(\log\)，整數部分管位數、小數部分管首位，再大的數都不必真的乘出來。",
            "prereq": [
                r"**常用對數**：\(\log\) 不寫底 ＝ 底 \(10\)（考點 2）",
                r"**次方化乘** \(\log N^k=k\log N\)（考點 2）",
                r"**高斯符號** \([x]\)：不超過 \(x\) 的最大整數（\([3.7]=3\)）",
            ],
            "points": [
                {"label": r"科學記號", "lines": [
                    r"任何正數 \(N=a\times10^n\)（\(1\le a<10\)、\(n\) 整數）；\(\log N=n+\log a\)，其中 \(0\le\log a<1\)。"]},
                {"label": r"位數", "lines": [
                    r"正整數 \(N\) 的位數 ＝ 【\([\log N]+1\)】（\([\,\cdot\,]\) 為高斯符號，取整數部分）。"]},
                {"label": r"首位數字", "lines": [
                    r"由 \(\log N\) 的 **小數部分** \(f\)（\(0\le f<1\)）決定：首位看 \(10^f\) 的整數部分；",
                    r"即科學記號 \(N=a\times10^n\) 中 \(a=\) 【\(10^f\)】，\(a\) 的整數部分即首位。"]},
                {"label": r"常用估計值", "lines": [
                    r"\(\log2\approx0.301\)、\(\log3\approx0.477\)、\(\log7\approx0.845\)；\(\log5=\) 【\(1-\log2\)】。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(N\) 的位數 \(=[\log N]\)", "right": r"要 **\(+1\)**：位數 \(=[\log N]+1\)"},
                {"wrong": r"首位看 \(\log N\) 的整數部分", "right": r"首位看 **小數部分** 對應的 \(10^f\)"},
                {"wrong": r"\(\log5\) 要另外查表", "right": r"\(\log5=\log\dfrac{10}{2}=1-\log2\)"},
                {"wrong": r"取 \(\log\) 會改變大小關係", "right": r"\(\log\) 遞增，取 \(\log\) 前後 **大小不變**"},
            ],
            "worked": {
                "q": r"\(3^{20}\) 是幾位數？（\(\log 3\approx0.477\)）",
                "steps": [
                    {"do": r"任何正數都能寫成「\(10\) 的某次方」：\(3\approx10^{0.477}\)。",
                     "why": r"這正是常用對數的意思——\(\log 3\approx0.477\) 就是說 \(3\approx10^{0.477}\)。"},
                    {"do": r"\(3^{20}\approx(10^{0.477})^{20}=10^{0.477\times20}=10^{9.54}\)。",
                     "why": r"次方再次方、指數相乘（考點 1 的指數律）。"},
                    {"do": r"\(10^{9.54}=10^{0.54}\times10^{9}\)，而 \(1\le10^{0.54}<10\)。",
                     "why": r"把指數拆成「小數 ＋ 整數」：小數那塊 \(10^{0.54}\) 必定落在 \(1\) 到 \(10\) 之間，這就是科學記號 \(a\times10^{9}\) 的 \(a\)。"},
                    {"do": r"所以 \(3^{20}=a\times10^{9}\)（\(1\le a<10\)），是 **\(10\) 位數**。",
                     "why": r"\(10^{9}\) 是 \(1\) 後面 \(9\) 個 \(0\)（共 \(10\) 位）；再乘 \(1\)～\(10\) 之間的 \(a\) 不會多進一位。這就是「位數 ＝ \(\log\) 整數部分 \(+1\)」的道理。"},
                ],
            },
            "questions": [
                {"tag": "107 · 單選 4", "level": "★★☆（中）", "core": "取 log 把指數不等式化為一次不等式",
                 "body": r"試問有多少個整數 \(x\) 滿足 \(10^9<2^x<9^{10}\)？（\(\log2\approx0.301\)、\(\log3\approx0.477\)）",
                 "options": [r"\(1\) 個", r"\(2\) 個", r"\(3\) 個", r"\(4\) 個", r"\(0\) 個"],
                 "solution": {"brief": r"(2) \(2\) 個",
                              "steps": [
                                  r"取 \(\log\)（遞增、不等號不變）：\(10^9<2^x\Rightarrow9<x\log2\Rightarrow x>\dfrac{9}{0.301}\approx29.9\)。",
                                  r"\(2^x<9^{10}\Rightarrow x\log2<10\log9=20\log3\Rightarrow x<\dfrac{20\times0.477}{0.301}\approx31.7\)。",
                                  r"\(29.9<x<31.7\)，整數 \(x=30,31\)，共 **2 個**，選 (2)。"]}},
                {"tag": "110 · 選填 E", "level": "★★★（難）", "core": "科學記號：位數 n 與首位 m",
                 "body": r"將 \(\left(\sqrt[3]{49}\right)^{100}\) 寫成科學記號 \(a\times10^n\)（\(1\le a<10\)、\(n\) 為正整數）。若 \(a\) 的整數部分為 \(m\)，求數對 \((m,n)\)。（\(\log7\approx0.845\)）",
                 "solution": {"brief": r"\((m,n)=(2,56)\)",
                              "steps": [
                                  r"\(X=\left(\sqrt[3]{49}\right)^{100}=49^{100/3}=7^{200/3}\)。取 \(\log\)：\(\log X=\dfrac{200}{3}\log7\approx\dfrac{200}{3}\times0.845\approx56.34\)。",
                                  r"\(\log X=56+0.34\Rightarrow X=10^{0.34}\times10^{56}\)，故 \(n=56\)、\(a=10^{0.34}\)。",
                                  r"\(\log2=0.301<0.34<\log3=0.477\Rightarrow 2<10^{0.34}<3\)，整數部分 \(m=2\)。故 \((m,n)=(2,56)\)。"]}},
            ],
            "selfcheck": {
                "q": r"\(2^{10}\) 是幾位數？（\(\log2\approx0.301\)）",
                "a": r"**\(4\) 位**：\(10\log2\approx3.01\)，位數 \([3.01]+1\)。"},
            "strategy": [
                r"求位數 \([\log N]+1\)；求首位看 \(\log N\) 的 **小數部分** 對應的 \(10^{小數}\)。",
                r"「\(2^x\) 介於兩數」的整數解：**取 \(\log\)** 變成 \(x\) 的一次不等式。",
                r"善用 \(\log2\approx0.301,\ \log3\approx0.477,\ \log7\approx0.845\)，\(\log5=1-\log2\)。",
                r"取 \(\log\) 不改變大小（遞增函數），不等號方向不變。",
            ],
        },
        {
            "num": "考點 4", "id": "kp4", "nav": "指數對數函數圖形",
            "title": r"指數與對數函數的圖形",
            "intro": r"**指數和對數是同一條曲線的『正反面』**：\(2^3=8\) 與 \(\log_2 8=3\) 不過是把點 \((3,8)\) 和 \((8,3)\) 對調——所以兩個函數的圖形會沿 \(y=x\) **鏡射對稱**。記牢兩個錨點：指數必過 \((0,1)\)、對數必過 \((1,0)\)；\(a>1\) 遞增、\(0<a<1\) 遞減。再小心 \(\log\) 的「定義域（真數 \(>0\)）陷阱」。",
            "prereq": [
                r"**指對互換**：\(a^x=N\Leftrightarrow\log_a N=x\)（考點 2）",
                r"**對稱 \(y=x\)**：點 \((a,b)\) 的鏡射點是 \((b,a)\)",
                r"**函數圖形**：會看遞增／遞減與定義域",
            ],
            "points": [
                {"label": r"指數函數圖形", "lines": [
                    r"\(y=a^x\)（\(a>0,a\neq1\)）：恆過 \((0,1)\)、漸近線 \(y=0\)、值域 \(y>0\)；",
                    r"\(a>1\) → 【遞增】；",
                    r"\(0<a<1\) → 【遞減】。"]},
                {"label": r"對數函數圖形", "lines": [
                    r"\(y=\log_a x\)：恆過 \((1,0)\)、漸近線 \(x=0\)（\(y\) 軸）、定義域 \(x>0\)；",
                    r"\(a>1\) → 【遞增】；",
                    r"\(0<a<1\) → 【遞減】。"]},
                {"svg": SVG_EXPLOG4, "wide": True, "caption": r"四型對照：指數恆過 \((0,1)\)（漸近線 \(x\) 軸）、對數恆過 \((1,0)\)（漸近線 \(y\) 軸）；\(a>1\) 遞增、\(0<a<1\) 遞減"},
                {"label": r"互為反函數", "lines": [
                    r"\(y=a^x\) 與 \(y=\log_a x\) 互為反函數，圖形對稱於 【\(y=x\)】（\(x\leftrightarrow y\) 對調）。"]},
                {"svg": SVG_EXPLOG,
                 "caption": r"**互為反函數**：\(y=2^x\)（過 \((0,1)\)）與 \(y=\log_2 x\)（過 \((1,0)\)）的圖形對虛線 \(y=x\) **鏡射對稱**——把其中一條沿 \(y=x\) 翻摺即得另一條。"},
                {"label": r"定義域陷阱", "lines": [
                    r"\(\log(x^2)\) 定義域 \(x\neq0\)（含 \(x<0\)）、\(\log(x^3)\) 定義域 \(x>0\)——化簡前先看 **定義域**，否則圖形會多／少一截。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(y=a^x\) 通過原點", "right": r"過 \((0,1)\)，**不過原點**"},
                {"wrong": r"\(\log_a x\) 定義域為全體實數", "right": r"只有 \(x>0\)"},
                {"wrong": r"\(\log(x^2)=2\log x\)", "right": r"是 \(2\log|x|\)（\(x\) 可負）；\(\log(x^3)=3\log x\) 才需 \(x>0\)"},
                {"wrong": r"指數與對數圖形對稱 \(y\) 軸", "right": r"對稱於 \(y=x\)（互為反函數）"},
            ],
            "worked": {
                "q": r"已知 \(y=2^x\) 通過 \((3,8)\)，則 \(y=\log_2 x\) 一定通過哪一點？",
                "steps": [
                    {"do": r"把坐標對調：\((3,8)\to(8,3)\)。",
                     "why": r"兩函數互為反函數、圖形對稱於 \(y=x\)；對稱就是把 \(x\)、\(y\) 互換。"},
                    {"do": r"驗證 \(\log_2 8=3\) ✓。",
                     "why": r"用定義確認：\(2^3=8\)，沒錯。"},
                ],
            },
            "questions": [
                {"tag": "114 數A · 單選 4", "level": "★★★（難）", "core": "對數曲線圍成區域內的格子點數",
                 "body": r"坐標平面上 \(x\)、\(y\) 坐標均為整數的點稱為格子點。試問在函數圖形 \(y=\log_2 x\)、\(x\) 軸與直線 \(x=\dfrac{61}{2}\) 所圍 **有界區域的內部（不含邊界）** 共有多少個格子點？",
                 "options": [r"\(88\)", r"\(89\)", r"\(90\)", r"\(91\)", r"\(92\)"],
                 "solution": {"brief": r"(3) \(90\) 個",
                              "steps": [
                                  r"區域由 \(y=\log_2 x\)（上）、\(x\) 軸（下）、\(x=30.5\)（右）所圍；內部即 \(1<x<30.5\) 且 \(0<y<\log_2 x\)。",
                                  r"**按 \(y\) 分層數**：對整數 \(y=k\ge1\)，需 \(\log_2 x>k\) 即 \(x>2^k\)，且 \(x\le30\)。",
                                  r"\(y=1\)：\(x=3\sim30\)（\(28\) 個）；\(y=2\)：\(x=5\sim30\)（\(26\)）；\(y=3\)：\(x=9\sim30\)（\(22\)）；\(y=4\)：\(x=17\sim30\)（\(14\)）；\(y\ge5\)：無。",
                                  r"共 \(28+26+22+14=90\)，選 (3)。"]}},
                {"tag": "113 數A · 多選 7", "level": "★★★（難）", "core": "與 y=log x 完全相同的圖形（含定義域）",
                 "body": r"令坐標平面上滿足 \(y=\log x\) 的點 \((x,y)\) 所成圖形為 \(\Gamma\)。試問滿足下列哪些關係式的 \((x,y)\) 所成圖形與 \(\Gamma\) **完全相同**？",
                 "options": [
                     r"\(y+\dfrac12=\log(5x)\)",
                     r"\(2y=\log(x^2)\)",
                     r"\(3y=\log(x^3)\)",
                     r"\(x=10^y\)",
                     r"\(x^3=10^{(y^3)}\)"],
                 "solution": {"brief": r"(3)(4)",
                              "steps": [
                                  r"\(\Gamma:y=\log x\)，定義域 \(x>0\)；要「**圖形完全相同**」須連定義域都一致。",
                                  r"(1)✗ \(y+\dfrac12=\log5+\log x\Rightarrow y=\log x+(\log5-\tfrac12)\)，整條上下平移（\(\log5-\tfrac12\neq0\)）。",
                                  r"(2)✗ \(2y=\log(x^2)=2\log|x|\Rightarrow y=\log|x|\)，定義域 \(x\neq0\)，**多出 \(x<0\) 的一支**。",
                                  r"(3)○ \(\log(x^3)\) 需 \(x>0\)，且 \(=3\log x\Rightarrow y=\log x\)，與 \(\Gamma\) 相同。",
                                  r"(4)○ \(x=10^y\Leftrightarrow y=\log x\)（\(x>0\)），同一圖形。(5)✗ \(y^3=3\log x\neq\log x\)，非同一曲線。故選 (3)(4)。"]}},
            ],
            "selfcheck": {
                "q": r"\(y=\log_2 x\) 通過哪一點？定義域為何？",
                "a": r"過 **\((1,0)\)**、定義域 **\(x>0\)**。"},
            "strategy": [
                r"指數過 \((0,1)\)、對數過 \((1,0)\)；兩者互為反函數、對稱 \(y=x\)。",
                r"化簡 \(\log\) 前先看 **定義域**：\(\log(x^2)\) 含 \(x<0\)、\(\log(x^3)\) 只 \(x>0\)。",
                r"圍成區域數格子點：**按 \(x\) 或按 \(y\) 分層** 數，注意「不含邊界」用嚴格不等式。",
                r"比較兩圖是否相同：除了式子，**定義域也要一致**。",
            ],
        },
        {
            "num": "考點 5", "id": "kp5", "nav": "應用模型與數列結合",
            "title": r"指對數的應用：成長衰退模型與數列",
            "intro": r"**衰退是「每隔一段時間乘一個固定比例」，不是減固定的量**：半衰期 \(2\) 小時，代表每過 \(2\) 小時就剩一半——\(4\) 小時是 \(2\) 個半衰期，剩 \(\dfrac12\times\dfrac12=\dfrac14\)（不是剩 \(0\)！）。寫成式子就是 \(Q_0\left(\dfrac12\right)^{t/T}\)。另一個關鍵口訣：**等比數列取 \(\log\) 會變等差**，這是指對數與數列互通的橋。",
            "prereq": [
                r"**指數律** \(\left(\dfrac12\right)^{t/T}\) 的計算（考點 1）",
                r"**等比／等差數列**的公比、公差（數列單元）",
                r"**取 \(\log\)**：\(\log y=\log k+x\log a\)（考點 2）",
            ],
            "points": [
                {"label": r"指數成長衰退模型", "lines": [
                    r"量 \(Q(t)=Q_0\cdot r^{\,t/T}\)：每隔 \(T\) 變為 \(r\) 倍；**半衰期** 即每隔 \(T\) 剩一半（\(r=\dfrac12\)）。"]},
                {"label": r"取對數的威力", "lines": [
                    r"指數關係 \(y=k\cdot a^x\) 兩邊取 \(\log\)：\(\log y=\) 【\(\log k+x\log a\)】（變成 \(x\) 的 **一次** 關係）。"]},
                {"label": r"等比 ↔ 等差", "lines": [
                    r"\(a_1,a_2,\dots\) 成 **等比** \(\Leftrightarrow\log a_1,\log a_2,\dots\) 成 【等差】（公比 \(r\) → 公差 \(\log r\)）；",
                    r"這是「指對數 ↔ 數列」互通的橋梁。"]},
                {"label": r"複利模型", "lines": [
                    r"本金 \(P\)、利率 \(i\)、\(n\) 期複利：本利和 \(=P(1+i)^n\)；求期數時 **兩邊取 \(\log\)** 解。"]},
            ],
            "misconceptions": [
                {"wrong": r"半衰期 \(2\) 小時，\(4\) 小時就剩 \(0\)", "right": r"\(4\) 小時 ＝ \(2\) 個半衰期 → 剩 \(\left(\dfrac12\right)^2=\dfrac14\)"},
                {"wrong": r"等比數列取 \(\log\) 還是等比", "right": r"等比取 \(\log\) 變 **等差**"},
                {"wrong": r"指數衰退是「等量遞減」", "right": r"是「每段乘固定比例」，非等量減少"},
                {"wrong": r"半衰期問題用線性內插", "right": r"用 \(\left(\dfrac12\right)^{t/T}\) 指數式"},
            ],
            "worked": {
                "q": r"某物質半衰期為 \(3\) 小時，\(9\) 小時後剩原來的幾分之幾？",
                "steps": [
                    {"do": r"\(9\div3=3\)，共 \(3\) 個半衰期。",
                     "why": r"每 \(3\) 小時算一個半衰期，先看經過了幾個。"},
                    {"do": r"剩 \(\left(\dfrac12\right)^3\)。",
                     "why": r"每過一個半衰期就乘 \(\dfrac12\)，過 \(3\) 個就乘 \(3\) 次。"},
                    {"do": r"\(=\dfrac18\)。",
                     "why": r"算出比例。"},
                ],
            },
            "questions": [
                {"tag": "113 數A · 單選 1", "level": "★☆☆（基礎）", "core": "半衰期（指數衰退模型）",
                 "body": r"某藥物在使用者體內的殘留量隨時間呈指數型衰退。已知服用 \(2\) 小時後體內仍殘留一半劑量，試問下列哪一選項正確？",
                 "options": [
                     r"\(3\) 小時後殘留 \(\dfrac13\) 劑量",
                     r"\(4\) 小時後殘留 \(\dfrac14\) 劑量",
                     r"\(6\) 小時後殘留 \(\dfrac16\) 劑量",
                     r"\(8\) 小時後殘留 \(\dfrac18\) 劑量",
                     r"\(10\) 小時後殘留 \(\dfrac{1}{10}\) 劑量"],
                 "solution": {"brief": r"(2)",
                              "steps": [
                                  r"半衰期 \(2\) 小時 → 殘留比例 \(=\left(\dfrac12\right)^{t/2}\)。",
                                  r"(2) \(t=4\)：\(\left(\dfrac12\right)^{2}=\dfrac14\) ○。(1) \(t=3\)：\(\left(\dfrac12\right)^{1.5}\approx0.354\neq\dfrac13\)。",
                                  r"(3)(4)(5) \(t=6,8,10\)：分別為 \(\dfrac18,\dfrac1{16},\dfrac1{32}\)，皆不符。故選 (2)。"]}},
                {"tag": "109 · 多選 11", "level": "★★☆（中）", "core": "log 值成等差 ⟺ 原數成等比 ＋ 科學記號估計",
                 "body": r"設 \(a,b,c\) 為實數且滿足 \(\log a=1.1\)、\(\log b=2.2\)、\(\log c=3.3\)。試選出正確的選項。",
                 "options": [
                     r"\(a+c=2b\)",
                     r"\(1<a<10\)",
                     r"\(1000<c<2000\)",
                     r"\(b=2a\)",
                     r"\(a,b,c\) 成等比數列"],
                 "solution": {"brief": r"(3)(5)",
                              "steps": [
                                  r"\(a=10^{1.1},\ b=10^{2.2},\ c=10^{3.3}\)。",
                                  r"(5)○ \(\log a,\log b,\log c=1.1,2.2,3.3\) 成等差（公差 \(1.1\)）→ \(a,b,c\) 成 **等比**（公比 \(10^{1.1}\)）。",
                                  r"(3)○ \(c=10^{3.3}=10^3\cdot10^{0.3}\approx1000\times1.995=1995\)，故 \(1000<c<2000\)。",
                                  r"(1)✗ 等比非等差，\(a+c\neq2b\)。(2)✗ \(a=10^{1.1}\approx12.6>10\)。(4)✗ \(b=10^{2.2}=a^2\neq2a\)。故選 (3)(5)。"]}},
            ],
            "selfcheck": {
                "q": r"某物質半衰期為 \(4\) 小時，\(8\) 小時後殘留為原來的幾分之幾？",
                "a": r"**\(\dfrac14\)**：\(\left(\dfrac12\right)^{8/4}=\left(\dfrac12\right)^2\)。"},
            "strategy": [
                r"指數成長／衰退：寫成 \(Q_0\cdot r^{\,t/T}\)，半衰期就是 \(r=\dfrac12\)。",
                r"「等比 ↔ 取 \(\log\) ↔ 等差」是指對數與數列的橋梁。",
                r"求「幾年／幾次」達某量：列指數式、**兩邊取 \(\log\)** 解。",
                r"衰退是「每段乘固定比例」，不是等量遞減；別用線性內插。",
            ],
        },
    ],

    "part2": {
        "count": "10", "note": "難度貼近學測，涵蓋五大考點 · 建議自行限時 40 分鐘作答後再對照詳解",
        "groups": [
            {"title": "一、單選題", "questions": [
                {"tag": "練習 1", "level": "★☆☆", "core": "分數指數",
                 "body": r"\(8^{2/3}\) 之值為何？",
                 "options": ["2", "3", "4", "6", "16"],
                 "solution": {"brief": "(3) 4", "brief_label": "答",
                              "steps": [r"\(8^{2/3}=(2^3)^{2/3}=2^2=4\)。"]}},
                {"tag": "練習 2", "level": "★☆☆", "core": "對數運算",
                 "body": r"\(\log_2 8+\log_2\dfrac14\) 之值為何？",
                 "options": ["0", "1", "2", "3", r"\(-1\)"],
                 "solution": {"brief": "(2) 1", "brief_label": "答",
                              "steps": [r"\(\log_2 8=3\)、\(\log_2\dfrac14=-2\)，相加 \(=1\)。"]}},
                {"tag": "練習 3", "level": "★★☆", "core": "換底公式",
                 "body": r"\(\log_4 8\) 之值為何？",
                 "options": [r"\(\dfrac32\)", r"\(\dfrac23\)", "2", r"\(\dfrac12\)", "3"],
                 "solution": {"brief": r"(1) \(\dfrac32\)", "brief_label": "答",
                              "steps": [r"\(\log_4 8=\dfrac{\log 8}{\log 4}=\dfrac{3\log2}{2\log2}=\dfrac32\)。"]}},
                {"tag": "練習 4", "level": "★★☆", "core": "位數",
                 "body": r"\(2^{30}\) 是幾位數？（\(\log2\approx0.301\)）",
                 "options": ["9 位", "10 位", "11 位", "30 位", "31 位"],
                 "solution": {"brief": "(2) 10 位", "brief_label": "答",
                              "steps": [r"\(\log(2^{30})=30\log2\approx9.03\)，位數 \(=[9.03]+1=10\)。"]}},
                {"tag": "練習 5（106 學測 · 單選 2）", "level": "★★☆", "core": "連續平方（指數律）",
                 "body": r"某程式每次點擊把螢幕上的數 \(a\) 變成 \(a^2\)。一開始螢幕上的正數為 \(b\)，連續點擊三次後，螢幕上的數接近 \(81^3\)。試問 \(b\) 最接近下列哪一個選項？",
                 "options": ["1.7", "3", "5.2", "9", "81"],
                 "solution": {"brief": "(3) 5.2", "brief_label": "答",
                              "steps": [r"三次平方：\(b\to b^2\to b^4\to b^8\)，故 \(b^8=81^3=(3^4)^3=3^{12}\)。",
                                        r"\(b=3^{12/8}=3^{3/2}=3\sqrt3\approx5.2\)。選 (3)。"]}},
            ]},
            {"title": "二、多選題", "questions": [
                {"tag": "練習 6", "level": "★★★", "core": "常用對數的估計",
                 "body": r"已知 \(\log2\approx0.301\)、\(\log3\approx0.477\)，下列敘述何者正確？",
                 "options": [
                     r"\(\log6\approx0.778\)",
                     r"\(\log5\approx0.699\)",
                     r"\(\log9\approx0.954\)",
                     r"\(\log8\approx0.903\)",
                     r"\(\log12\approx1.176\)"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"(1)○ \(\log6=\log2+\log3=0.778\)。(2)○ \(\log5=1-\log2=0.699\)。(3)○ \(\log9=2\log3=0.954\)。(4)○ \(\log8=3\log2=0.903\)。",
                                        r"(5)✗ \(\log12=2\log2+\log3=0.602+0.477=1.079\neq1.176\)。"]}},
                {"tag": "練習 7", "level": "★★★", "core": "指數與對數函數圖形",
                 "body": r"關於函數 \(y=\log_2 x\) 與 \(y=2^x\)，下列敘述何者正確？",
                 "options": [
                     r"兩函數互為反函數",
                     r"兩圖形對稱於直線 \(y=x\)",
                     r"\(y=2^x\) 的圖形通過 \((0,1)\)",
                     r"\(y=\log_2 x\) 的圖形通過 \((1,0)\)",
                     r"兩圖形都通過第三象限"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"(1)(2)○ 互為反函數、對稱 \(y=x\)。(3)○ \(2^0=1\)。(4)○ \(\log_2 1=0\)。",
                                        r"(5)✗ \(y=2^x>0\) 不入第三象限；\(y=\log_2 x\) 定義域 \(x>0\) 也不入第三象限。"]}},
            ]},
            {"title": "三、選填題", "questions": [
                {"tag": "練習 8", "level": "★★☆", "core": "指數方程",
                 "body": r"解方程式 \(3^{2x-1}=27\)。",
                 "solution": {"brief": r"\(x=2\)", "brief_label": "答",
                              "steps": [r"\(27=3^3\)，化同底：\(2x-1=3\Rightarrow x=2\)。"]}},
                {"tag": "練習 9", "level": "★★☆", "core": "對數方程（注意定義域）",
                 "body": r"解方程式 \(\log_2(x-1)+\log_2(x+1)=3\)。",
                 "solution": {"brief": r"\(x=3\)", "brief_label": "答",
                              "steps": [r"\(\log_2[(x-1)(x+1)]=3\Rightarrow x^2-1=8\Rightarrow x^2=9\Rightarrow x=\pm3\)。",
                                        r"定義域須 \(x>1\)，故 \(x=3\)（\(x=-3\) 不合）。"]}},
                {"tag": "練習 10", "level": "★★☆", "core": "半衰期模型",
                 "body": r"某放射性物質的半衰期為 \(5\) 天。經過 \(15\) 天後，殘留量為原來的幾分之幾？",
                 "solution": {"brief": r"\(\dfrac18\)", "brief_label": "答",
                              "steps": [r"\(\left(\dfrac12\right)^{15/5}=\left(\dfrac12\right)^3=\dfrac18\)。"]}},
            ]},
        ],
    },

    "part3": {
        "ref_table": [
            {"k": "指數律", "v": r"\(a^m a^n=a^{m+n}\)、\((a^m)^n=a^{mn}\)、\(a^0=1\)、\(a^{-n}=\dfrac{1}{a^n}\)"},
            {"k": "分數指數", "v": r"\(a^{m/n}=\sqrt[n]{a^m}\)；連開 \(k\) 次平方根 ＝ 乘 \(\dfrac{1}{2^k}\) 次方"},
            {"k": "對數定義", "v": r"\(\log_a N=x\Leftrightarrow a^x=N\)（\(a>0,a\neq1,N>0\)）"},
            {"k": "對數法則", "v": r"\(\log(MN)=\log M+\log N\)；\(\log\dfrac{M}{N}=\log M-\log N\)；\(\log M^k=k\log M\)"},
            {"k": "換底公式", "v": r"\(\log_a b=\dfrac{\log_c b}{\log_c a}\)；\(\log_a b=\dfrac{1}{\log_b a}\)（互為倒數）"},
            {"k": "位數 / 首位", "v": r"位數 \(=[\log N]+1\)；首位看 \(\log N\) 小數部分的 \(10^{小數}\)"},
            {"k": "常用估計值", "v": r"\(\log2\approx0.301\)、\(\log3\approx0.477\)、\(\log7\approx0.845\)、\(\log5=1-\log2\)"},
            {"k": "指數函數", "v": r"\(y=a^x\) 過 \((0,1)\)、漸近 \(y=0\)、值域 \(y>0\)"},
            {"k": "對數函數", "v": r"\(y=\log_a x\) 過 \((1,0)\)、漸近 \(x=0\)、定義域 \(x>0\)"},
            {"k": "互為反函數", "v": r"\(y=a^x\) 與 \(y=\log_a x\) 對稱於 \(y=x\)"},
            {"k": "等比 ↔ 等差", "v": r"等比數列取 \(\log\) 變等差（公比 \(r\) → 公差 \(\log r\)）"},
            {"k": "成長衰退模型", "v": r"\(Q(t)=Q_0\,r^{\,t/T}\)；半衰期 \(r=\dfrac12\)；複利 \(P(1+i)^n\)"},
        ],
        "checklist": [
            r"\((a^m)^n=a^{mn}\)（相乘）；\(a^m\cdot a^n\) 才相加。",
            r"\(\log(MN)=\log M+\log N\)（積化加）；和 **不可拆**。",
            r"\(\log_a b\) 與 \(\log_b a\) **互為倒數**。",
            r"位數 \(=[\log N]+1\)（**記得 \(+1\)**）。",
            r"\(\log2\approx0.301,\ \log3\approx0.477\)，\(\log5=1-\log2\)。",
            r"\(\log(x^2)\) 含 \(x<0\)、\(\log(x^3)\) 只 \(x>0\)。",
            r"指數過 \((0,1)\)、對數過 \((1,0)\)。",
            r"指數與對數 **互為反函數**，對稱 \(y=x\)。",
            r"**等比取 \(\log\) 變等差**——指對數與數列的橋梁。",
            r"半衰期：經過 \(t\) 時間剩 \(\left(\dfrac12\right)^{t/T}\)。",
            r"解對數方程記得檢查 **真數 \(>0\)** 的定義域。",
        ],
    },
}
