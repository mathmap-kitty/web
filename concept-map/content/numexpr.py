# -*- coding: utf-8 -*-
r"""數與式單元 · 單一來源內容（升級版）。

挖空原則：只挖「公式與概念關鍵」（自行判斷），不沿用教師 docx 的粉色標點標記。
例題以官方原卷（106~115學測數學試卷.pdf）為準；數 B 題不採用（不在官方卷、無法核對）。

"""

# 數線圖：絕對值不等式 |x-3|<2 ⟺ 1<x<5（距離意義）
SVG_NUMLINE = r'''<svg viewBox="0 0 330 86" width="330" height="86" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect x="80" y="43" width="160" height="9" fill="#f1d6df"/>
  <line x1="22" y1="47.5" x2="298" y2="47.5" stroke="#2c3e50" stroke-width="2"/>
  <polygon points="306,47.5 296,42.5 296,52.5" fill="#2c3e50"/>
  <g stroke="#2c3e50" stroke-width="1.5">
    <line x1="40" y1="43" x2="40" y2="52"/><line x1="80" y1="43" x2="80" y2="52"/>
    <line x1="120" y1="43" x2="120" y2="52"/><line x1="160" y1="40" x2="160" y2="55"/>
    <line x1="200" y1="43" x2="200" y2="52"/><line x1="240" y1="43" x2="240" y2="52"/>
    <line x1="280" y1="43" x2="280" y2="52"/>
  </g>
  <g fill="#22433c" font-size="12" font-family="serif" text-anchor="middle">
    <text x="40" y="69">0</text><text x="80" y="69">1</text><text x="120" y="69">2</text>
    <text x="160" y="69">3</text><text x="200" y="69">4</text><text x="240" y="69">5</text><text x="280" y="69">6</text>
  </g>
  <circle cx="80" cy="47.5" r="5" fill="#fff" stroke="#b03a5b" stroke-width="2"/>
  <circle cx="240" cy="47.5" r="5" fill="#fff" stroke="#b03a5b" stroke-width="2"/>
  <circle cx="160" cy="47.5" r="3.5" fill="#2c3e50"/>
  <text x="160" y="18" fill="#8c2740" font-size="13" text-anchor="middle" font-weight="bold">|x&#8722;3| &lt; 2 &#8660; 1 &lt; x &lt; 5</text>
</svg>'''

# 實數系概念圖（依老師手繪版重製）：填色圓角節點 + 藍色註解
_RT_DARK = "#5d2640"; _RT_MID = "#8a4f66"; _RT_MAUVE = "#a87d8e"  # 階層色：L0深→L1中→L2淺；同層同色
_RT_LEAF = "#f4e6ec"; _RT_LEDGE = "#d9b8c4"; _RT_LINE = "#b08699"
_RT_BLUE = "#3a5a9a"; _RT_RED = "#c0392b"; _RT_INKL = "#4a2230"; _RT_SUB = "#a06a7e"
_RT_SERIF = "font-family=\"'Noto Serif CJK TC','Microsoft JhengHei',serif\""
_RT_SANS = "font-family=\"'Microsoft JhengHei',system-ui,sans-serif\""

def _rt_box(cx, cy, w, h, fill, text, fs, tcol, rx=11, edge=None):
    st = f' stroke="{edge}" stroke-width="1.2"' if edge else ''
    return (f'<rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>'
            f'<text x="{cx}" y="{cy+fs*0.35:.1f}" font-size="{fs}" fill="{tcol}" font-weight="bold" text-anchor="middle">{text}</text>')

def _realsys_fig():
    N = dict(R=(92,273,128,54,21), Q=(300,216,148,54,20), IR=(300,330,148,50,19),
             Z=(500,132,150,50,18), F=(500,300,150,48,15.5),
             nN=(648,80,118,42,15), n0=(648,132,118,42,15), nNEG=(648,184,118,42,15),
             fFIN=(648,270,118,42,15), fCYC=(648,340,118,42,15))
    L = [f'<svg viewBox="0 0 734 392" width="734" height="392" xmlns="http://www.w3.org/2000/svg" role="img" {_RT_SANS}>']
    L.append(f'<g stroke="{_RT_LINE}" stroke-width="2.5" fill="none" stroke-linecap="round">')
    for x1,y1,x2,y2 in [(156,273,226,216),(156,273,226,330),(374,216,425,132),(374,216,425,300),
                        (575,132,589,80),(575,132,589,132),(575,132,589,184),(575,300,589,270),(575,300,589,340)]:
        L.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    L.append('</g>')
    L.append(f'<text x="36" y="58" font-size="30" fill="{_RT_DARK}" font-weight="bold" {_RT_SERIF}>實數系</text>')
    L.append(f'<text x="38" y="80" font-size="13.5" fill="{_RT_SUB}" font-style="italic">Real Number System</text>')
    L.append(_rt_box(*N['R'][:4], _RT_DARK, '實數 R', N['R'][4], 'white'))
    L.append(_rt_box(*N['Q'][:4], _RT_MID, '有理數 Q', N['Q'][4], 'white'))
    L.append(_rt_box(*N['IR'][:4], _RT_MID, '無理數', N['IR'][4], 'white'))
    L.append(_rt_box(*N['Z'][:4], _RT_MAUVE, '整數 Z', N['Z'][4], 'white'))
    L.append(_rt_box(*N['F'][:4], _RT_MAUVE, '不為整數的分數', N['F'][4], 'white'))
    for k, t in [('nN','正整數 N'),('n0','0'),('nNEG','負整數'),('fFIN','有限小數'),('fCYC','循環小數')]:
        b = N[k]; L.append(_rt_box(b[0], b[1], b[2], b[3], _RT_LEAF, t, b[4], _RT_INKL, rx=9, edge=_RT_LEDGE))
    L.append(f'<text x="92" y="312" font-size="11.5" fill="{_RT_BLUE}" text-anchor="middle">數線上所有的點</text>')
    L.append(f'<g font-size="11.5" fill="{_RT_BLUE}" text-anchor="start">')
    L.append(f'<text x="228" y="258">(1) 形式：n/m<tspan fill="{_RT_RED}">（m≠0）</tspan></text>')
    L.append(f'<text x="228" y="276">(2) 性質：稠密性、封閉性</text>')
    L.append(f'<text x="228" y="294">(3) 可尺規作圖</text></g>')
    L.append(f'<text x="300" y="372" font-size="11.5" fill="{_RT_BLUE}" text-anchor="middle">不循環無限小數</text>')
    L.append(f'<text x="648" y="308" font-size="11" fill="{_RT_BLUE}" text-anchor="middle">Note：分母質因數僅 2、5</text>')
    L.append(f'<text x="648" y="378" font-size="11" fill="{_RT_BLUE}" text-anchor="middle">Note：0.999… ＝ 1</text>')
    L.append('</svg>')
    return "".join(L)

SVG_REALTREE = _realsys_fig()

# 算幾不等式幾何意義：半圓中半弦 √(ab) ≤ 半徑 (a+b)/2
SVG_AMGM = r'''<svg viewBox="0 0 230 150" width="230" height="150" xmlns="http://www.w3.org/2000/svg" role="img" font-family="'Microsoft JhengHei',system-ui,sans-serif">
  <path d="M22 116 A93 93 0 0 1 208 116" fill="#eef4f8" stroke="#2c3e50" stroke-width="1.6"/>
  <line x1="22" y1="116" x2="208" y2="116" stroke="#2c3e50" stroke-width="1.6"/>
  <line x1="78" y1="116" x2="78" y2="31" stroke="#1f8a5b" stroke-width="2"/>
  <line x1="115" y1="116" x2="115" y2="23" stroke="#b03a5b" stroke-width="2"/>
  <rect x="78" y="106" width="10" height="10" fill="none" stroke="#1f8a5b" stroke-width="1"/>
  <g fill="#2c3e50"><circle cx="22" cy="116" r="2.6"/><circle cx="208" cy="116" r="2.6"/><circle cx="78" cy="116" r="2.6"/><circle cx="115" cy="116" r="2.6"/></g>
  <g font-size="12" text-anchor="middle">
    <text x="49" y="133" fill="#2c3e50">a</text>
    <text x="145" y="133" fill="#2c3e50">b</text>
    <text x="60" y="80" fill="#1f8a5b" font-weight="bold">√(ab)</text>
    <text x="150" y="62" fill="#b03a5b" font-weight="bold">(a+b)/2</text>
  </g>
</svg>'''

# 分點公式：P 在 A(a)、B(b) 之間且 PA:PB = m:n
SVG_DIVPT = r'''<svg viewBox="0 0 300 104" width="300" height="104" xmlns="http://www.w3.org/2000/svg" role="img" font-family="'Microsoft JhengHei',system-ui,sans-serif">
  <line x1="20" y1="54" x2="288" y2="54" stroke="#2c3e50" stroke-width="2"/>
  <polygon points="296,54 286,49 286,59" fill="#2c3e50"/>
  <g stroke="#2c3e50" stroke-width="1.6"><line x1="60" y1="48" x2="60" y2="60"/><line x1="170" y1="48" x2="170" y2="60"/><line x1="250" y1="48" x2="250" y2="60"/></g>
  <g fill="#2c3e50"><circle cx="60" cy="54" r="3"/><circle cx="170" cy="54" r="3.5"/><circle cx="250" cy="54" r="3"/></g>
  <g font-size="12.5" text-anchor="middle" font-weight="bold">
    <text x="60" y="36" fill="#2c3e50">A</text><text x="170" y="36" fill="#b03a5b">P</text><text x="250" y="36" fill="#2c3e50">B</text>
  </g>
  <g font-size="12" text-anchor="middle" fill="#22433c">
    <text x="60" y="78">a</text><text x="250" y="78">b</text>
  </g>
  <g font-size="11" text-anchor="middle" fill="#8a6d3b">
    <text x="115" y="48">m</text><text x="210" y="48">n</text>
  </g>
</svg>'''

# 絕對值不等式三型：|x|<a / |x|≤a / |x|≥a 在數線上的解
SVG_ABSCASES = r'''<svg viewBox="0 0 330 198" width="330" height="198" xmlns="http://www.w3.org/2000/svg" role="img" font-family="'Microsoft JhengHei',system-ui,sans-serif">
  <g stroke="#2c3e50" stroke-width="1.8">
    <line x1="120" y1="40" x2="300" y2="40"/><line x1="120" y1="105" x2="300" y2="105"/><line x1="120" y1="170" x2="300" y2="170"/>
  </g>
  <rect x="160" y="36" width="100" height="8" fill="#f1d6df"/>
  <rect x="160" y="101" width="100" height="8" fill="#f1d6df"/>
  <rect x="124" y="166" width="36" height="8" fill="#f1d6df"/><rect x="260" y="166" width="36" height="8" fill="#f1d6df"/>
  <g stroke="#2c3e50" stroke-width="1.3">
    <line x1="160" y1="34" x2="160" y2="46"/><line x1="210" y1="34" x2="210" y2="46"/><line x1="260" y1="34" x2="260" y2="46"/>
    <line x1="160" y1="99" x2="160" y2="111"/><line x1="210" y1="99" x2="210" y2="111"/><line x1="260" y1="99" x2="260" y2="111"/>
    <line x1="160" y1="164" x2="160" y2="176"/><line x1="210" y1="164" x2="210" y2="176"/><line x1="260" y1="164" x2="260" y2="176"/>
  </g>
  <polygon points="296,170 306,165 306,175" fill="#2c3e50"/><polygon points="124,170 114,165 114,175" fill="#2c3e50"/>
  <g fill="#fff" stroke="#b03a5b" stroke-width="2"><circle cx="160" cy="40" r="5"/><circle cx="260" cy="40" r="5"/></g>
  <g fill="#b03a5b"><circle cx="160" cy="105" r="5"/><circle cx="260" cy="105" r="5"/><circle cx="160" cy="170" r="5"/><circle cx="260" cy="170" r="5"/></g>
  <g font-size="11.5" text-anchor="middle" fill="#22433c">
    <text x="160" y="62">−a</text><text x="210" y="62">0</text><text x="260" y="62">a</text>
    <text x="160" y="127">−a</text><text x="210" y="127">0</text><text x="260" y="127">a</text>
    <text x="160" y="192">−a</text><text x="210" y="192">0</text><text x="260" y="192">a</text>
  </g>
  <g font-size="12.5" text-anchor="start" font-weight="bold" fill="#8c2740">
    <text x="14" y="38">|x| &lt; a</text><text x="14" y="103">|x| ≤ a</text><text x="14" y="168">|x| ≥ a</text>
  </g>
  <g font-size="10.5" text-anchor="start" fill="#6b5b73">
    <text x="14" y="52">−a&lt;x&lt;a</text><text x="14" y="117">−a≤x≤a</text><text x="14" y="182">x≤−a或x≥a</text>
  </g>
</svg>'''

import soil_maps  # Part 0 單元知識地圖（SOIL 章節圖）

UNIT = {
    "slug": "numexpr",
    "file": "115學測數學_數與式.html",
    "page_title": "115 學測數學 · 數與式",
    "emoji": "🔢",
    "title": "數與式",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 六大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "六大考點",
    "foot": "115 學測數學 · 數與式 · 學測數學重點整理",

    "part0": {
        "opener": {"svg": soil_maps.SLIDES["numexpr"], "hero": True,
                   "caption": r"**單元知識地圖**：先備 → 各考點（★越多＝越常考） → 跨單元最愛綁考 → 帶走一句話"},
        "heading": "為什麼數與式是穩拿分的入門單元",
        "trend_table": {
            "years": [106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            "counts": ["1.0", "1.0", "0", "1.0", "1.0", "0", "0", "0", "0", "1.0"],
            "total": "5.0",
        },
        "notes": [
            r"**數 A 單獨命題變少**：舊制（\(106\)–\(110\)）幾乎年年 1 題；但數 A（\(111\)–\(115\)）只有 \(115\) 年考 1 題（高斯函數），單獨出題大幅減少。",
            r"**但它是其他單元的「基礎工具」**：絕對值與一次不等式常以「限制條件」融入向量、機率；算幾不等式常在幾何（切線、面積）求極值時登場——**看到就要想到**。",
            r"**觀念陷阱多於計算**：有理／無理判定、\(\sqrt{a^2}=|a|\)、距離和最小值是失分熱區，重點在「分辨」而非硬算。",
            r"**生活應用題**：比例、百分率、加權平均（漲跌幅、得票率）是舊制熱門題型，仍可能以情境題形式回鍋。",
        ],
        "map": r"命題重心六主軸：① 有理／無理與循環小數 ② 絕對值的「距離」意義與分段討論 ③ 數線距離、分點與根號估算 ④ 乘法公式、對稱式與算幾不等式 ⑤ 比例、百分率與加權平均 ⑥ 高斯（最大整數）函數。",
        "fig": {"svg": SVG_REALTREE, "full": True, "caption": r"實數系概念圖：循著分支判定一個數的歸類，藍字為各層的關鍵性質與提醒（進考點前先建立全貌）"},
    },

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "實數系與有理／無理",
            "title": r"實數系、數的分類與循環小數",
            "intro": r"把「數」分門別類——哪些是有理數、哪些是無理數，以及循環小數怎麼化成分數。重點在 **有理／無理的判定** 與運算後「還是不是有理數」。",
            "prereq": [
                r"**整數、分數、小數**的概念",
                r"**根號** \(\sqrt2,\sqrt4\) 的意義",
                r"集合「包含 \(\subset\)」「聯集 \(\cup\)」",
                r"**絕對值＝距離**（考點 2）、**根號估算與平方比大小**（考點 3）——\(112\) 數B多9 的 (3)(4)(5) 會用",
            ],
            "points": [
                {"label": r"實數系包含關係", "lines": [
                    r"正整數 \(\subset\) 整數 \(\subset\) 有理數 \(\subset\) 實數；",
                    r"實數 ＝ 有理數 【\(\cup\)】 無理數（兩者不相交、合起來是全體實數）。"]},
                {"label": r"有理數", "lines": [
                    r"可寫成 【\(\dfrac{m}{n}\)】（\(m,n\) 為整數，\(n\neq0\)）的數；",
                    r"小數表現為 【有限小數】 或 【循環小數】。"]},
                {"label": r"無理數", "lines": [
                    r"不循環的 【無限小數】（如 \(\sqrt2,\,\pi\)）；不能寫成兩整數之比。"]},
                {"label": r"運算後的判定", "lines": [
                    r"有理數對加、減、乘、除（除數 \(\neq0\)）【封閉】（結果仍是有理數）；",
                    r"有理 ＋ 無理 ＝ 【無理】、非零有理 × 無理 ＝ 【無理】；",
                    r"無理 ± 無理、無理 × 無理 【不一定】（要找反例，如 \(\sqrt2\cdot\sqrt2=2\) 為有理數）。"]},
                {"label": r"循環小數化分數", "lines": [
                    r"純循環：\(0.\overline{ab}=\) 【\(\dfrac{ab}{99}\)】、\(0.\overline{abc}=\) 【\(\dfrac{abc}{999}\)】；",
                    r"混循環（前面有不循環位）：\(0.a\overline{bc}=\) 【\(\dfrac{abc-a}{990}\)】（[[分母怎麼來||循環節 \(bc\) 有 2 位 → 2 個 \(9\)；不循環的 \(a\) 有 1 位 → 後面接 1 個 \(0\)，得 \(990\)。分子 ＝（整段數字 \(abc\)）－（不循環部分 \(a\)）。如 \(0.1\overline{23}=\dfrac{123-1}{990}=\dfrac{122}{990}\)。]]）；",
                    r"一般用 [[錯位相減法||設 \(x=0.\overline{ab}\)，乘 \(100\) 得 \(100x=ab.\overline{ab}\)，兩式相減消去循環尾巴：\(99x=ab\Rightarrow x=\dfrac{ab}{99}\)。]]（小數點後幾位循環就乘 \(10\) 的幾次方）。"]},
            ],
            "misconceptions": [
                {"wrong": r"無理 ＋ 無理 ＝ 無理", "right": r"不一定，如 \(\sqrt2+(-\sqrt2)=0\) 為有理數"},
                {"wrong": r"循環小數不是有理數", "right": r"循環小數是有理數（一定可化成分數）"},
                {"wrong": r"\(0.\overline{9}\) 接近 1 但不等於 1", "right": r"\(0.\overline{9}=1\)（化分數即 \(\dfrac{9}{9}=1\)）"},
                {"wrong": r"\(\sqrt2\cdot\sqrt2\) 仍是無理數", "right": r"\(\sqrt2\cdot\sqrt2=2\) 為有理數"},
            ],
            "worked": {
                "q": r"把循環小數 \(0.\overline{6}\) 化成分數。",
                "steps": [
                    {"do": r"設 \(x=0.\overline{6}=0.666\dots\)，乘 \(10\)：\(10x=6.666\dots\)。",
                     "why": r"「錯位相減法」：乘 \(10\) 的次方，讓兩個數的小數部分對齊。"},
                    {"do": r"兩式相減消掉循環尾巴：\(10x-x=6\Rightarrow9x=6\Rightarrow x=\dfrac23\)。",
                     "why": r"能化成分數，就證明「循環小數一定是有理數」。"},
                ],
            },
            "questions": [
                {"tag": "112 數B · 多選 9", "level": "★★☆（中）", "core": "有理／無理判定 · 絕對值（距離）· 數線",
                 "body": r"已知 \(a=6\)、\(b=\dfrac{20}{3}\)、\(c=2\sqrt{10}\) 和 \(d\)（\(d\) 為有理數），將這四數標在數線上，即 \(A(a)、B(b)、C(c)、D(d)\)。試選出正確的選項。",
                 "options": [
                     r"\(a+b+c+d\) 必為有理數",
                     r"\(abcd\) 必為無理數",
                     r"點 \(D\) 有可能與點 \(C\) 的距離等於 \(2\sqrt{10}+6\)",
                     r"點 \(A\) 和點 \(B\) 的中點位在點 \(C\) 的右邊",
                     r"數線上與點 \(B\) 距離小於 \(8\) 的所有點中，正整數有 \(14\) 個、負整數有 \(1\) 個"],
                 "solution": {"brief": r"(3)(4)(5)",
                              "steps": [
                                  r"\(a=6、b=\dfrac{20}{3}、d\) 為有理數；\(c=2\sqrt{10}=\sqrt{40}\)（\(40\) 非完全平方）為無理數。",
                                  r"(1)✗ 四數只有 \(c\) 無理：有理 \(+\) 無理 \(=\) 無理，故和為無理數。",
                                  r"(2)✗ 取 \(d=0\) 則 \(abcd=0\)（有理），不必為無理數。",
                                  r"(3)○ 令 \(|d-2\sqrt{10}|=2\sqrt{10}+6\)：取 \(d=-6\)（有理），距離 \(=2\sqrt{10}-(-6)=2\sqrt{10}+6\)，可行。",
                                  r"(4)○ 中點 \(=\dfrac{6+\frac{20}{3}}{2}=\dfrac{19}{3}\)。比 \(\dfrac{19}{3}\) 與 \(c=2\sqrt{10}\) 大小 → 平方：\(\left(\dfrac{19}{3}\right)^2=\dfrac{361}{9}\)、\((2\sqrt{10})^2=40=\dfrac{360}{9}\)，因 \(\dfrac{361}{9}>\dfrac{360}{9}\)，中點在 \(C\) 右邊。",
                                  r"(5)○ \(\left|x-\dfrac{20}{3}\right|<8\Rightarrow-\dfrac43<x<\dfrac{44}{3}\)（約 \(-1.33<x<14.67\)）：正整數 \(1\sim14\)（\(14\) 個）、負整數 \(-1\)（\(1\) 個）。故選 (3)(4)(5)。"]}},
                {"tag": "觀念範例（多選）", "level": "★★☆（中）", "core": "有理數、無理數的運算判定",
                 "body": r"設 \(a\) 為有理數、\(b\) 為無理數，下列敘述何者 **恆成立**？",
                 "options": [r"\(a+b\) 為無理數", r"\(ab\) 為無理數", r"\(b^2\) 為有理數", r"若 \(a\neq0\)，則 \(\dfrac{b}{a}\) 為無理數", r"\(b-\lfloor b\rfloor\)（\(\lfloor\cdot\rfloor\) 為高斯符號）為無理數"],
                 "solution": {"brief": r"(1)(4)(5)",
                              "steps": [r"(1)○：有理 ＋ 無理 ＝ 無理。(2)✗：\(a=0\) 時 \(ab=0\) 為有理數。",
                                        r"(3)✗：取 \(b=\sqrt[4]{2}\) 則 \(b^2=\sqrt2\) 仍為無理數，不恆成立。",
                                        r"(4)○：無理數除以非零有理數仍為無理數。(5)○：\(\lfloor b\rfloor\) 為整數，無理數減整數仍為無理數。"]}},
            ],
            "strategy": [
                r"判定「運算後是不是有理數」記三句：**有理對四則封閉**；**有理＋無理、非零有理×無理＝無理**；**無理±無理、無理×無理「不一定」**（要找反例）。",
                r"循環小數一律可化分數 → 是有理數；特例 \(0.\overline{9}=1\)。",
                r"看到根號別急著當無理數：\(\sqrt4=2\)、\(\sqrt2\cdot\sqrt2=2\) 都是有理數，**先化簡再判定**。",
            ],
            "selfcheck": {
                "q": r"下列何者為有理數？(1) \(0.\overline{6}\)　(2) \(\sqrt{12}\)　(3) \(\sqrt2\cdot\sqrt8\)　(4) \(\sqrt3+(-\sqrt3)\)",
                "a": r"**(1)(3)(4)**。循環小數是有理數；\(\sqrt2\cdot\sqrt8=\sqrt{16}=4\)、\(\sqrt3-\sqrt3=0\) 也是；只有 \(\sqrt{12}=2\sqrt3\) 為無理數。"},
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "絕對值",
            "title": r"絕對值的意義、方程式與不等式",
            "intro": r"把絕對值看成「**距離**」——這是數與式最高頻的工具。重點在用幾何意義或分段討論去絕對值，並熟記三角不等式。",
            "prereq": [
                r"**數線**、正負數",
                r"「**距離**」的概念",
                r"解一次方程／不等式",
                r"**二次不等式**「兩根內／外」（多項式單元 考點 2）——平方去絕對值後會解到二次（\(111\) 多7）",
            ],
            "points": [
                {"label": r"定義與幾何意義", "lines": [
                    r"\(|a|=\begin{cases}a,&a\ge0\\-a,&a\lt0\end{cases}\)，即 \(a\lt0\) 時 \(|a|=\) 【\(-a\)】；",
                    r"\(|a|\) 表示 \(a\) 到 【原點】 的距離。"]},
                {"label": r"距離意義", "lines": [
                    r"\(|a-b|\) 表示數線上 \(a\)、\(b\) 兩點的 【距離】。"]},
                {"svg": SVG_NUMLINE, "caption": r"絕對值不等式 ＝ 數線上的「距離範圍」"},
                {"label": r"看圖解題（絕對值不等式）", "lines": [
                    r"**① 翻譯**：\(|x-3|<2\) 讀成「\(x\) 到 \(3\) 的距離小於 \(2\)」。",
                    r"**② 讀數線**：以 \(3\) 為中心、左右各 \(2\)，落在 \(1\) 與 \(5\) 之間。",
                    r"**③ 寫答**：\(1<x<5\)。（反過來 \(|x-3|>2\) 就取兩側：\(x<1\) 或 \(x>5\)。）"]},
                {"label": r"絕對值方程式", "lines": [
                    r"\(|x|=k\;(k\gt0)\Rightarrow x=\) 【\(\pm k\)】；",
                    r"\(|x-a|=k\Rightarrow x=\) 【\(a\pm k\)】。"]},
                {"label": r"絕對值不等式", "lines": [
                    r"\(|x|\lt k\Leftrightarrow\) 【\(-k\lt x\lt k\)】；",
                    r"\(|x|\gt k\;(k\gt0)\Leftrightarrow\) 【\(x\lt-k\) 或 \(x\gt k\)】。"]},
                {"svg": SVG_ABSCASES, "wide": True, "caption": r"三型對照：\(\lt\) 取「中間」（空心點）、\(\le\) 含端點（實心點）、\(\ge\) 取「兩側」"},
                {"label": r"重要性質", "lines": [
                    r"\(|ab|=\) 【\(|a||b|\)】、\(\sqrt{a^2}=\) 【\(|a|\)】、\(|-a|=|a|\)；",
                    r"兩邊非負時可 [[平方去絕對值||\(|A|\ge|B|\Leftrightarrow A^2\ge B^2\)，因兩邊都 \(\ge0\)。這招把絕對值不等式變成二次不等式，是 \(111\) 多7 的關鍵。]]：\(|A|\ge|B|\Leftrightarrow\) 【\(A^2\ge B^2\)】。"]},
                {"label": r"三角不等式", "lines": [
                    r"【\(|a-b|\le|a\pm b|\le|a|+|b|\)】；",
                    r"\(|x-a|+|x-b|\) 的最小值為 【\(|a-b|\)】（於 \(a\)、\(b\) 之間取得）。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(|a+b|=|a|+|b|\)", "right": r"一般只有 \(\le\)；同號（含 0）才相等"},
                {"wrong": r"\(\sqrt{a^2}=a\)", "right": r"\(\sqrt{a^2}=|a|\)（\(a\) 可能為負）"},
                {"wrong": r"\(|x|\gt k\) 解為 \(-k\lt x\lt k\)", "right": r"反了：是 \(x\lt-k\) 或 \(x\gt k\)"},
                {"wrong": r"\(|x-a|+|x-b|\) 最小值是 0", "right": r"最小值是 \(|a-b|\)，不是 0"},
            ],
            "worked": {
                "q": r"解 \(|x-2|>3\)。",
                "steps": [
                    {"do": r"把 \(|x-2|>3\) 讀成「\(x\) 到 \(2\) 的距離大於 \(3\)」。",
                     "why": r"絕對值就是距離：\(|x-a|\) 是 \(x\) 到 \(a\) 的距離。"},
                    {"do": r"以 \(2\) 為中心、距離超過 \(3\) → 取**兩側**：\(x<2-3\) 或 \(x>2+3\)，即 \(x<-1\) 或 \(x>5\)。",
                     "why": r"「\(>\)」是離得遠 → 取兩側；「\(<\)」才是取中間那一段。"},
                ],
            },
            "questions": [
                {"tag": "111 數A · 多選 7（改寫為計數）", "level": "★★★（難）", "core": "絕對值不等式：兩邊非負平方化成二次",
                 "body": r"設整數 \(n\) 滿足 \(|5n-21|\ge7|n|\)。試問有多少個整數 \(n\) 滿足此不等式？",
                 "options": [r"6 個", r"10 個", r"12 個", r"14 個", r"無窮多個"],
                 "solution": {"brief": r"(3)，12 個（\(n=-10,-9,\dots,1\)）",
                              "steps": [r"兩邊皆 \(\ge0\)，可平方去絕對值：\(|5n-21|\ge7|n|\Leftrightarrow(5n-21)^2\ge49n^2\)。",
                                        r"展開 \(25n^2-210n+441\ge49n^2\Rightarrow 24n^2+210n-441\le0\Rightarrow 8n^2+70n-147\le0\)。",
                                        r"解得 \(-10.5\le n\le1.75\)，整數 \(n=-10,-9,\dots,1\) 共 **12 個**。（原題為多選，官方答案 (2)(4)，核心即此「平方化二次」技巧。）"]}},
            ],
            "strategy": [
                r"去絕對值兩條路：**幾何意義**（\(|x-a|\) 是到 \(a\) 的距離，畫數線最快）或 **分段討論**（依絕對值內部變號點分段，逐段解再合併）。",
                r"看到「到兩定點的距離和」直接想「最小值 ＝ 兩點距離」。",
                r"\(|A|\ge|B|\)（或 \(\le\)）兩邊非負時，**平方化成二次不等式** 最省事（\(111\) 多7）。",
            ],
            "selfcheck": {
                "q": r"解 \(|x-3|<2\)，並說出它在數線上的意義。",
                "a": r"**\(1<x<5\)**。意義：數線上「到 \(3\) 的距離小於 \(2\)」的所有點（見上面數線圖）。"},
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "數線、距離與根號估算",
            "title": r"數線上的點、距離、分點與根號估算",
            "intro": r"把數線上的「距離、中點、分點、根號落點」算清楚——幾乎都是送分題，重點在 **根號夾在相鄰平方數之間** 與 **不等式取交集**。",
            "prereq": [
                r"**絕對值 ＝ 距離**（考點 2）",
                r"**完全平方數** \(1,4,9,16,25,\dots\)",
                r"**不等式**與取交集",
            ],
            "points": [
                {"label": r"距離與中點", "lines": [
                    r"\(a\)、\(b\) 兩點距離 ＝ 【\(|a-b|\)】，中點坐標 ＝ 【\(\dfrac{a+b}{2}\)】。"]},
                {"label": r"分點公式", "lines": [
                    r"\(P\) 在 \(A_a\)、\(B_b\) 之間且 \(PA:PB=m:n\)，則 \(P\) 坐標 ＝ 【\(\dfrac{na+mb}{m+n}\)】（中點是 \(m:n=1:1\) 的特例）。"]},
                {"svg": SVG_DIVPT, "med": True, "caption": r"分點 \(P\) 把 \(\overline{AB}\) 分成 \(m:n\)；係數要「交叉」：靠 \(A\) 的權重給 \(b\)、靠 \(B\) 的給 \(a\)"},
                {"label": r"根號估算", "lines": [
                    r"\(\sqrt N\) 夾在 [[相鄰兩完全平方根之間||例：\(9\lt10\lt16\Rightarrow 3\lt\sqrt{10}\lt4\)。先框出整數範圍，再決定整數落點。]]；例 \(10\lt\sqrt{101}\lt11\)、\(6\lt\sqrt{38}\lt7\)；",
                    r"框整數不夠精細時，**兩非負數比大小可平方**：如比 \(\dfrac{19}{3}\) 與 \(2\sqrt{10}\)（都在 \(6\) 與 \(7\) 之間）→ 平方比 \(\dfrac{361}{9}\) 與 \(\dfrac{360}{9}\)，立分高下（\(112\) 數B多9(4)）。"]},
                {"label": r"雙重根號化簡", "lines": [
                    r"\(\sqrt{a+b\pm2\sqrt{ab}}=\) 【\(\sqrt a\pm\sqrt b\)】（\(a\gt b\ge0\)）。"]},
                {"label": r"不等式取交集", "lines": [
                    r"兩條件分別解出範圍後 【取交集】（畫數線輔助），不是取聯集。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(\sqrt{a+b}=\sqrt a+\sqrt b\)", "right": r"根號對加法不可拆；正確為 \(\sqrt{a+b\pm2\sqrt{ab}}=\sqrt a\pm\sqrt b\)"},
                {"wrong": r"「同時滿足」兩條件取聯集", "right": r"要取 **交集**（兩範圍重疊處）"},
                {"wrong": r"中點公式與分點公式混用", "right": r"中點是 \(m:n=1:1\) 的特例，分點公式更一般"},
                {"wrong": r"隨手估 \(\sqrt N\) 的近似值", "right": r"先用相鄰平方框出整數範圍再細估"},
            ],
            "worked": {
                "q": r"\(\sqrt{50}\) 落在哪兩個連續整數之間？",
                "steps": [
                    {"do": r"找最接近的兩個完全平方數：\(49=7^2\)、\(64=8^2\)，而 \(49<50<64\)。",
                     "why": r"根號估算先「框整數」——看 \(N\) 落在哪兩個相鄰完全平方數之間。"},
                    {"do": r"開根號（遞增、不變號）：\(7<\sqrt{50}<8\)，故落在 \(7\) 與 \(8\) 之間。",
                     "why": r"開根號不改變大小關係，框好平方數就框好了根號。"},
                ],
            },
            "questions": [
                {"tag": "109 舊制 · 單選 5", "level": "★☆☆（易）", "core": "根號的估算與不等式交集",
                 "body": r"試問數線上有多少個整數點，與點 \(\sqrt{101}\) 的距離小於 \(5\)，但與點 \(\sqrt{38}\) 的距離大於 \(3\)？",
                 "options": [r"1 個", r"4 個", r"6 個", r"8 個", r"10 個"],
                 "solution": {"brief": r"(3)，6 個",
                              "steps": [r"\(\sqrt{101}\approx10.05\)、\(\sqrt{38}\approx6.16\)。",
                                        r"條件一：\(|n-\sqrt{101}|\lt5\Rightarrow5.05\lt n\lt15.05\)；條件二：\(|n-\sqrt{38}|\gt3\Rightarrow n\lt3.16\) 或 \(n\gt9.16\)。",
                                        r"取交集得 \(9.16\lt n\lt15.05\)，整數 \(n=10,11,12,13,14,15\) 共 **6 個**。"]}},
            ],
            "strategy": [
                r"根號估算先「框整數」：找 \(\sqrt N\) 落在哪兩個相鄰平方數之間，再決定整數落點。",
                r"多條件題分別解範圍後 **畫數線取交集**；「同時滿足」是交集不是聯集。",
            ],
            "selfcheck": {
                "q": r"\(\sqrt{40}\) 落在哪兩個連續整數之間？",
                "a": r"**\(6\) 與 \(7\)**（因 \(6^2=36<40<49=7^2\)）。"},
        },
        {
            "num": "考點 4", "id": "kp4", "nav": "乘法公式與算幾不等式",
            "title": r"乘法公式、對稱式求值與算幾不等式",
            "intro": r"把「展開、對稱式求值、用算幾求極值」三件代數工具練熟——這是數與式裡計算量最大、也最常和幾何結合的考點。",
            "prereq": [
                r"**乘法分配律、展開**",
                r"**完全平方** \((a+b)^2\) 的概念",
                r"**根號** \(\sqrt{ab}\)（算幾不等式用）",
            ],
            "points": [
                {"label": r"乘法公式", "lines": [
                    r"\((a\pm b)^2=\) 【\(a^2\pm2ab+b^2\)】、\((a+b)(a-b)=\) 【\(a^2-b^2\)】；",
                    r"\((a\pm b)^3=\) 【\(a^3\pm3a^2b+3ab^2\pm b^3\)】；",
                    r"\((a+b+c)^2=\) 【\(a^2+b^2+c^2+2ab+2bc+2ca\)】。"]},
                {"label": r"對稱式求值（已知 \(a+b\)、\(ab\)）", "lines": [
                    r"\(a^2+b^2=\) 【\((a+b)^2-2ab\)】、\((a-b)^2=\) 【\((a+b)^2-4ab\)】；",
                    r"\(a^3+b^3=\) 【\((a+b)^3-3ab(a+b)\)】。"]},
                {"label": r"算幾不等式", "lines": [
                    r"**限 \(a,b\ge0\)（正數／非負）** 才有 \(\dfrac{a+b}{2}\ge\) 【\(\sqrt{ab}\)】，等號於 【\(a=b\)】 成立（[[少了「正數」就會出錯||算幾不等式只對非負數成立。若變數可能為負，直接套用會算出錯誤的極值——看到「求極值」先確認變數是否 \(\ge0\)，這是最常被扣分的地方。]]）；",
                    r"常配倒數：\(x\gt0\) 時 \(x+\dfrac kx\ge\) 【\(2\sqrt k\)】（[[等號於 \(x=\sqrt k\) 成立||由 \(\dfrac{a+b}{2}\ge\sqrt{ab}\) 取 \(a=x,\,b=\dfrac kx\)，乘積 \(ab=k\) 固定，故和有最小值；等號要 \(a=b\) 即 \(x=\dfrac kx\Rightarrow x=\sqrt k\)。]]）。"]},
                {"svg": SVG_AMGM, "med": True, "caption": r"算幾的幾何意義：半徑 \(\dfrac{a+b}{2}\) 永遠 \(\ge\) 半弦 \(\sqrt{ab}\)，\(a=b\)（\(F\) 落在圓心）時相等"},
            ],
            "misconceptions": [
                {"wrong": r"\((a+b)^2=a^2+b^2\)", "right": r"漏了 \(2ab\)：正確為 \(a^2+2ab+b^2\)"},
                {"wrong": r"\(a^2+b^2=(a+b)^2\)", "right": r"應為 \((a+b)^2-2ab\)"},
                {"wrong": r"算幾不等式不看 \(a,b\) 正負", "right": r"須 \(a,b\ge0\) 才能用算幾"},
                {"wrong": r"算幾等號隨便成立", "right": r"等號只在 \(a=b\) 時，且須驗證可達"},
            ],
            "worked": {
                "q": r"已知 \(a+b=5\)、\(ab=6\)，求 \(a^2+b^2\)。",
                "steps": [
                    {"do": r"用恆等式 \(a^2+b^2=(a+b)^2-2ab\)。",
                     "why": r"對稱式求值的關鍵——把 \(a^2+b^2\) 用「和、積」表示，就不必真的解出 \(a,b\)。"},
                    {"do": r"\(=5^2-2\times6=25-12=13\)。",
                     "why": r"代入 \(a+b=5\)、\(ab=6\) 即得。"},
                ],
            },
            "questions": [
                {"tag": "107 舊制 · 選填 C", "level": "★★☆（中）", "core": "圓切線性質、算幾不等式求面積最大值",
                 "body": r"平面上兩點 \(A\)、\(B\) 距離為 \(5\)。以 \(A\) 為圓心作半徑 \(r\)（\(0\lt r\lt5\)）的圓 \(\Gamma\)，過 \(B\) 作 \(\Gamma\) 的切線，切點之一為 \(P\)。當 \(r\) 變動時，\(\triangle PAB\) 的面積最大可能值為 ？（化為最簡分數）",
                 "solution": {"brief": r"\(\dfrac{25}{4}\)",
                              "steps": [r"設 \(BP=x\)。切線垂直半徑，故 \(\angle APB=90^\circ\)，\(\triangle PAB\) 面積 \(=\dfrac12 rx\)，且 \(r^2+x^2=AB^2=25\)。",
                                        r"由算幾不等式 \(r^2+x^2\ge2rx\Rightarrow rx\le\dfrac{25}{2}\)，故面積 \(=\dfrac{rx}{2}\le\dfrac{25}{4}\)（於 \(r=x=\dfrac{5}{\sqrt2}\) 時最大）。"]}},
                {"tag": "觀念範例（算幾配倒數）", "level": "★☆☆（暖身）", "core": "算幾不等式配倒數求極值",
                 "body": r"設 \(x\gt1\)，求 \(x+\dfrac{4}{x-1}\) 的最小值。",
                 "solution": {"brief": r"最小值 \(=5\)（於 \(x=3\)）",
                              "steps": [r"令 \(t=x-1\gt0\)：\(x+\dfrac{4}{x-1}=(t+1)+\dfrac4t=t+\dfrac4t+1\ge2\sqrt{t\cdot\frac4t}+1=4+1=5\)（\(t=2\)，即 \(x=3\) 時等號）。"]}},
            ],
            "strategy": [
                r"對稱式求值別硬解 \(a,b\)：湊出 \(a+b\) 與 \(ab\)，再套 \(a^2+b^2=(a+b)^2-2ab\) 之類公式。",
                r"求極值看到「和定／積定」就用算幾；務必檢查 \(a,b\ge0\) 與「\(a=b\) 的等號可達」。",
                r"配倒數時先「湊出固定乘積」（如 \(t\cdot\dfrac kt=k\)），再用算幾。",
            ],
            "selfcheck": {
                "q": r"設 \(x>0\)，求 \(x+\dfrac{9}{x}\) 的最小值，並說出在何處取得。",
                "a": r"**最小值 \(6\)**：算幾 \(x+\dfrac9x\ge2\sqrt{x\cdot\frac9x}=2\sqrt9=6\)，於 \(x=3\) 時取等號。"},
        },
        {
            "num": "考點 5", "id": "kp5", "nav": "比例、百分率與加權平均",
            "title": r"比例、百分率與加權平均（生活應用）",
            "intro": r"比例、百分率、加權平均是「生活應用」的核心，舊制熱門、數 A 仍可能以情境題回鍋。重點在 **設未知數列式** 與 **看清「是對誰的比率」**。",
            "prereq": [
                r"**分數、比例**的基本運算",
                r"**百分率** \(p\%=\dfrac{p}{100}\)",
                r"**加權平均**（與數據分析呼應）",
            ],
            "points": [
                {"label": r"比與比例", "lines": [
                    r"\(a:b=c:d\Leftrightarrow\) 【\(ad=bc\)】（內項積 ＝ 外項積）。"]},
                {"label": r"百分率漲跌", "lines": [
                    r"漲跌幅 ＝ 【\(\dfrac{當期-前期}{前期}\)】；連續漲跌要 **連乘**（不是相加）。",
                    r"上漲 \(p\%\) 後再下跌 \(p\%\) 回不到原點：\((1+p\%)(1-p\%)=1-(p\%)^2\lt1\)。"]},
                {"label": r"加權平均", "lines": [
                    r"加權平均 ＝ 【\(\dfrac{加權總和}{總權重}\)】；",
                    r"\(a\) 人平均 \(x\)、\(b\) 人平均 \(y\)，合併平均 ＝ \(\dfrac{ax+by}{a+b}\)（**不是** \(\dfrac{x+y}{2}\)）。"]},
            ],
            "misconceptions": [
                {"wrong": r"連續漲跌幅可直接相加", "right": r"要連乘，如 \((1+p\%)(1+q\%)\)"},
                {"wrong": r"兩組合併平均 ＝ 兩平均的平均", "right": r"要 **加權**：\(\dfrac{ax+by}{a+b}\)"},
                {"wrong": r"漲 \(p\%\) 再跌 \(p\%\) 回到原價", "right": r"\(\times(1-(p\%)^2)\lt1\)，比原價低"},
            ],
            "worked": {
                "q": r"某商品連續兩次漲價，第一次漲 \(10\%\)、第二次漲 \(20\%\)。總共漲了百分之幾？",
                "steps": [
                    {"do": r"兩次漲價要**連乘**：\((1+10\%)(1+20\%)=1.1\times1.2=1.32\)。",
                     "why": r"第二次的 \(20\%\) 是對「已經漲過的價格」算的，所以要乘、不是加。"},
                    {"do": r"\(1.32\) ＝ 原價的 \(132\%\)，所以共漲 \(32\%\)（不是 \(10\%+20\%=30\%\)）。",
                     "why": r"連續漲跌一律連乘——這就是為什麼不能把百分比直接相加。"},
                ],
            },
            "questions": [
                {"tag": "106 舊制 · 單選 1", "level": "★★☆（中）", "core": "用符號代表數、比率的定義",
                 "body": r"已知某校老師玩過某遊戲的比率為 \(r_1\)、學生玩過的比率為 \(r_2\)，其中 \(r_1\gt r_2\)。由下列哪一項資訊，可判定「全校師生玩過該遊戲的比率」？",
                 "options": [r"全校老師與學生的比率", r"全校老師人數", r"全校學生人數", r"全校師生人數", r"全校師生玩過該遊戲的人數"],
                 "solution": {"brief": r"(1)",
                              "steps": [r"設老師 \(t\) 人、學生 \(s\) 人，全校比率 \(=\dfrac{r_1 t+r_2 s}{t+s}\)。",
                                        r"分子分母同除以 \(s\)：\(=\dfrac{r_1\frac ts+r_2}{\frac ts+1}\)，只與 **\(t:s\)（老師與學生的比率）** 有關，故知道比率即可，選 (1)。"]}},
                {"tag": "107 舊制 · 單選 6", "level": "★★☆（中）", "core": "百分率的連乘（漲跌幅）",
                 "body": r"某貨品「當週售價相對前週的漲跌幅」定為「當週成本相對前週成本漲跌幅」的 **一半**。下表為成本與售價（元）：第一週 成本 \(50\)、售價 \(120\)；第二週 成本 \(100\)、售價 \(180\)；第三週 成本 \(50\)、售價 \(x\)；第四週 成本 \(90\)、售價 \(y\)。試選出正確的選項。",
                 "options": [r"\(x\lt120\)", r"\(120\lt x\lt180\) 且 \(y\lt180\)", r"\(x\gt180\)", r"\(120\lt y\lt180\lt x\)", r"\(120\lt x\lt180\lt y\)"],
                 "solution": {"brief": r"(5)，\(x=135,\;y=189\)",
                              "steps": [r"第三週成本 \(100\to50\)，跌 \(50\%\Rightarrow\) 售價跌 \(25\%\)：\(x=180\times(1-25\%)=135\)。",
                                        r"第四週成本 \(50\to90\)，漲 \(80\%\Rightarrow\) 售價漲 \(40\%\)：\(y=135\times(1+40\%)=189\)。",
                                        r"故 \(120\lt x(=135)\lt180\lt y(=189)\)，選 (5)。"]}},
                {"tag": "110 舊制 · 多選 9", "level": "★★★（難）", "core": "比率合成與當選判定",
                 "body": r"某村村長選舉設兩個投票所，兩候選人在各所得票比例如下：第一投票所 甲 \(40\%\)、乙 \(60\%\)；第二投票所 甲 \(55\%\)、乙 \(45\%\)。設兩所有效票數為 \(x,y\;(x,y\gt0)\)，總得票較高者當選。試選出正確的選項。",
                 "options": [r"當 \(x+y\) 已知時，就可決定當選人", r"當 \(x:y\) 的比值小於 \(\tfrac12\) 時，就可決定當選人", r"當 \(x\gt y\) 時，就可決定當選人", r"當甲在第一所的票數比在第二所多時，就可決定當選人", r"當乙在第二所的票數比在第一所多時，就可決定當選人"],
                 "solution": {"brief": r"(2)(3)(4)",
                              "steps": [r"甲得票 \(=0.4x+0.55y\)、乙得票 \(=0.6x+0.45y\)。甲勝 \(\Leftrightarrow 0.4x+0.55y\gt0.6x+0.45y\Leftrightarrow y\gt2x\Leftrightarrow \tfrac xy\lt\tfrac12\)。",
                                        r"(1)✗：只知 \(x+y\) 無法定比值。(2)○：\(\tfrac xy\lt\tfrac12\Rightarrow\) 甲勝。(3)○：\(x\gt y\Rightarrow\tfrac xy\gt1\Rightarrow\) 乙勝。",
                                        r"(4)○：\(0.4x\gt0.55y\Rightarrow\tfrac xy\gt1.375\Rightarrow\) 乙勝。(5)✗：\(0.45y\gt0.6x\Rightarrow\tfrac xy\lt0.75\)，仍可能跨 \(\tfrac12\) 兩側，無法決定。"]}},
            ],
            "strategy": [
                r"比率題先 **設人數／票數為未知數**，把「比率」寫成 \(\dfrac{部分}{全體}\)，再化簡看「只跟什麼有關」。",
                r"連續漲跌一律 **連乘**（\(\times(1+p\%)\)），絕不可把百分率相加。",
                r"合併平均要 **加權**，先分清每組的「人數（權重）」。",
            ],
            "selfcheck": {
                "q": r"某商品先漲 \(20\%\)、再跌 \(20\%\)，最後價格是原價的百分之幾？",
                "a": r"**\(96\%\)**：\(1.2\times0.8=0.96\)。漲跌幅要 **連乘**，不會相抵回 \(100\%\)。"},
        },
        {
            "num": "考點 6", "id": "kp6", "nav": "高斯（最大整數）函數",
            "title": r"高斯函數（最大整數函數）",
            "intro": r"高斯函數 \([x]\) 取「不超過 \(x\) 的最大整數」。重點在 **\([x]\le x\lt[x]+1\)** 的定義、整數可進出、以及負數要往更小取。",
            "prereq": [
                r"**整數、小數**、數線",
                r"「不超過、向下取整」的概念",
                r"**根號估算**（考點 3，算 \([\sqrt N]\) 用）",
            ],
            "points": [
                {"label": r"定義", "lines": [
                    r"\([x]=\) 滿足 【\([x]\le x\lt[x]+1\)】 的整數（不超過 \(x\) 的最大整數）；",
                    r"例 \([3]=3\)、\([3.1]=3\)、\([-3.1]=\) 【\(-4\)】（[[負數要往更小取||\(-3.1\) 介於 \(-4\) 與 \(-3\) 之間，「不超過 \(-3.1\) 的最大整數」是 \(-4\)，不是 \(-3\)。負數最容易錯。]]）。"]},
                {"label": r"重要性質", "lines": [
                    r"\(x\) 為整數時 \([x]=x\)；一般 \(x-1\lt[x]\le x\)；",
                    r"\([x+n]=\) 【\([x]+n\)】（\(n\) 為整數，整數可自由進出）。"]},
                {"label": r"小數部分", "lines": [
                    r"\(\{x\}=x-[x]\)，恆有 \(0\le\{x\}\lt1\)。"]},
            ],
            "misconceptions": [
                {"wrong": r"\([-3.1]=-3\)", "right": r"\([-3.1]=-4\)（負數往更小的整數取）"},
                {"wrong": r"\([x]\) 是四捨五入", "right": r"是「無條件捨去到整數」（向下取整）"},
                {"wrong": r"\([x+y]=[x]+[y]\)", "right": r"不一定，如 \([0.5+0.5]=1\neq[0.5]+[0.5]=0\)"},
            ],
            "worked": {
                "q": r"求 \([\sqrt{99}]\)（高斯函數）。",
                "steps": [
                    {"do": r"先把 \(\sqrt{99}\) 夾在相鄰平方數之間：\(81=9^2<99<100=10^2\Rightarrow9<\sqrt{99}<10\)。",
                     "why": r"算 \([\sqrt N]\) 先用根號估算「框整數」（考點 3 的技巧）。"},
                    {"do": r"\([\sqrt{99}]\) ＝ 不超過 \(\sqrt{99}\) 的最大整數 ＝ \(9\)。",
                     "why": r"\(\sqrt{99}\) 落在 \(9\) 與 \(10\) 之間，向下取整就是 \(9\)。"},
                ],
            },
            "questions": [
                {"tag": "115 數A · 單選 2", "level": "★★☆（中）", "core": "高斯函數與根號估算",
                 "body": r"令 \([a]\) 為滿足 \([a]\le a\lt[a]+1\) 的整數（例 \([3]=3,\,[3.1]=3,\,[-3.1]=-4\)）。關於函數 \(f(x)=[\sqrt{99-x}]+[\sqrt{99+x}]\)（\(-99\le x\le99\)），試選出正確的選項。",
                 "options": [r"\(f(-20)\le f(0)\le f(1)\)", r"\(f(-20)\le f(1)\le f(0)\)", r"\(f(1)\le f(-20)\le f(0)\)", r"\(f(0)\le f(-20)\le f(1)\)", r"\(f(0)\le f(1)\le f(-20)\)"],
                 "solution": {"brief": r"(1)，且 \(f(-20)=f(0)=18\lt f(1)=19\)",
                              "steps": [r"\(f(0)=[\sqrt{99}]+[\sqrt{99}]=9+9=18\)；\(f(1)=[\sqrt{98}]+[\sqrt{100}]=9+10=19\)。",
                                        r"\(f(-20)=[\sqrt{119}]+[\sqrt{79}]=10+8=18\)。故 \(f(-20)=f(0)=18\lt f(1)=19\)，選 (1)。",
                                        r"**關鍵**：先把根號夾在相鄰平方數之間定出 \([\,\cdot\,]\)（如 \(81\lt99\lt100\Rightarrow[\sqrt{99}]=9\)）。"]}},
            ],
            "strategy": [
                r"算 \([\sqrt N]\) 先把 \(\sqrt N\) **夾在相鄰平方數之間**（考點 3 的技巧），再取整數部分。",
                r"負數的高斯值 **往更小的整數取**（\([-3.1]=-4\)），是最常見的陷阱。",
                r"\(x\) 為整數時 \([x\pm 整數]\) 可直接進出，先把整數抽出來。",
            ],
            "selfcheck": {
                "q": r"求 \([-3.1]+[3.1]\)。",
                "a": r"**\(-1\)**：\([-3.1]=-4\)（負數向下取整）、\([3.1]=3\)，相加 \(-4+3=-1\)。"},
        },
    ],

    "part2": {
        "count": "12", "note": "難度貼近學測，著重觀念辨別 · 建議自行限時 40 分鐘作答後再對照詳解",
        "groups": [
            {"title": "一、單選題", "questions": [
                {"tag": "練習 1", "level": "★☆☆", "core": "絕對值不等式",
                 "body": r"滿足 \(|2x-3|\lt5\) 的整數 \(x\) 共有幾個？",
                 "options": ["3", "4", "5", "6", "7"],
                 "solution": {"brief": "(2) 4 個", "brief_label": "答",
                              "steps": [r"\(-5\lt2x-3\lt5\Rightarrow-1\lt x\lt4\)，整數 \(x=0,1,2,3\) 共 4 個。"]}},
                {"tag": "練習 2", "level": "★☆☆", "core": "根號估算",
                 "body": r"設 \(n\) 為整數且 \(n\lt\sqrt{50}\lt n+1\)，則 \(n=\) ？",
                 "options": ["5", "6", "7", "8", "9"],
                 "solution": {"brief": "(3) 7", "brief_label": "答",
                              "steps": [r"\(49\lt50\lt64\Rightarrow7\lt\sqrt{50}\lt8\)，故 \(n=7\)。"]}},
                {"tag": "練習 3", "level": "★★☆", "core": "絕對值的幾何意義（最小值）",
                 "body": r"\(|x-2|+|x+1|\) 的最小值為？",
                 "options": ["1", "2", "3", "4", "0"],
                 "solution": {"brief": "(3) 3", "brief_label": "答",
                              "steps": [r"表 \(x\) 到 \(2\) 與到 \(-1\) 的距離和，最小值為兩點距離 \(|2-(-1)|=3\)（於 \(-1\le x\le2\) 取得）。"]}},
                {"tag": "練習 4", "level": "★★☆", "core": "算幾不等式",
                 "body": r"設 \(x\gt0\)，則 \(x+\dfrac4x\) 的最小值為？",
                 "options": ["2", "3", "4", "5", "8"],
                 "solution": {"brief": "(3) 4", "brief_label": "答",
                              "steps": [r"由算幾 \(x+\dfrac4x\ge2\sqrt{x\cdot\frac4x}=2\sqrt4=4\)（\(x=2\) 時等號）。"]}},
                {"tag": "練習 5", "level": "★★☆", "core": "數線距離（中點）",
                 "body": r"數線上滿足 \(|x-1|=|x-5|\) 的 \(x\) 值為？",
                 "options": ["2", "3", "4", r"\(-3\)", "6"],
                 "solution": {"brief": "(2) 3", "brief_label": "答",
                              "steps": [r"表 \(x\) 到 \(1\)、\(5\) 等距，即中點 \(x=\dfrac{1+5}{2}=3\)。"]}},
            ]},
            {"title": "二、多選題", "questions": [
                {"tag": "練習 6", "level": "★★★", "core": "絕對值的性質",
                 "body": r"設 \(a,b\) 為實數，下列敘述何者 **恆成立**？",
                 "options": [r"\(|-a|=|a|\)", r"\(|ab|=|a||b|\)", r"\(|a+b|=|a|+|b|\)", r"\(\sqrt{a^2}=|a|\)", r"若 \(|a|\lt2\)，則 \(-2\lt a\lt2\)"],
                 "solution": {"brief": "(1)(2)(4)(5)", "brief_label": "答",
                              "steps": [r"(3)✗：一般只有 \(|a+b|\le|a|+|b|\)，等號僅在 \(a,b\) 同號（含 0）時成立。其餘恆成立。"]}},
            ]},
            {"title": "三、選填題", "questions": [
                {"tag": "練習 7", "level": "★★☆", "core": "絕對值不等式的交集",
                 "body": r"同時滿足 \(|x-3|\le2\) 與 \(|x+1|\gt1\) 的整數 \(x\) 共有 ？ 個。",
                 "solution": {"brief": "5 個", "brief_label": "答",
                              "steps": [r"\(|x-3|\le2\Rightarrow1\le x\le5\)；\(|x+1|\gt1\Rightarrow x\gt0\) 或 \(x\lt-2\)。交集 \(1\le x\le5\)，整數 \(x=1,2,3,4,5\) 共 **5 個**。"]}},
                {"tag": "練習 8", "level": "★★☆", "core": "算幾不等式應用",
                 "body": r"設 \(x\gt1\)，則 \(x+\dfrac{9}{x-1}\) 的最小值為 ？",
                 "solution": {"brief": "7", "brief_label": "答",
                              "steps": [r"令 \(t=x-1\gt0\)：\((t+1)+\dfrac9t=t+\dfrac9t+1\ge2\sqrt9+1=7\)（\(t=3\)，即 \(x=4\) 時）。"]}},
                {"tag": "練習 9", "level": "★★☆", "core": "根號估算與整數點",
                 "body": r"數線上與點 \(\sqrt{72}\) 的距離小於 \(2\) 的整數點共有 ？ 個。",
                 "solution": {"brief": "4 個", "brief_label": "答",
                              "steps": [r"\(\sqrt{72}=6\sqrt2\approx8.49\)，故 \(6.49\lt x\lt10.49\)，整數 \(x=7,8,9,10\) 共 **4 個**。"]}},
            ]},
            {"title": "四、非選擇題（須寫出計算過程）", "questions": [
                {"tag": "練習 10", "level": "★★★", "core": "分段討論解絕對值方程式",
                 "body": r"試解方程式 \(|x-1|+|x-3|=6\)，並求所有解之和。",
                 "solution": {"brief": r"兩解 \(x=5,\,-1\)，和 \(=4\)", "brief_label": "答",
                              "steps": [r"\(x\ge3\)：\((x-1)+(x-3)=6\Rightarrow x=5\) ✓；\(1\le x\lt3\)：恆為 \(2\neq6\)，無解。",
                                        r"\(x\lt1\)：\((1-x)+(3-x)=6\Rightarrow x=-1\) ✓。兩解之和 \(=5+(-1)=4\)。"]}},
                {"tag": "練習 11", "level": "★★★", "core": "算幾不等式（切線情境）",
                 "body": r"平面上兩點 \(A\)、\(B\) 距離為 \(6\)，以 \(A\) 為圓心作半徑 \(r\)（\(0\lt r\lt6\)）的圓，過 \(B\) 作切線、切點為 \(P\)。(1) 以 \(r\) 表示 \(\triangle PAB\) 面積。(2) 求面積最大值。",
                 "solution": {"brief": r"最大值 \(=9\)", "brief_label": "答",
                              "steps": [r"(1) 設 \(BP=x\)，切線垂直半徑故 \(r^2+x^2=36\)，面積 \(=\dfrac12rx=\dfrac{r\sqrt{36-r^2}}{2}\)。",
                                        r"(2) 由算幾 \(r^2+(36-r^2)\ge2r\sqrt{36-r^2}\Rightarrow r\sqrt{36-r^2}\le18\)，故面積 \(\le9\)（\(r=3\sqrt2\) 時）。"]}},
                {"tag": "練習 12", "level": "★★★", "core": "加權平均列式",
                 "body": r"某班男生 \(20\) 人、女生 \(a\) 人。男生平均體重 \(60\) 公斤、女生平均 \(50\) 公斤，全班平均 \(55\) 公斤。(1) 以 \(a\) 列出全班平均式。(2) 求 \(a\)。",
                 "solution": {"brief": r"\(a=20\)", "brief_label": "答",
                              "steps": [r"(1) 全班平均 \(=\dfrac{20\times60+a\times50}{20+a}=55\)。",
                                        r"(2) \(1200+50a=1100+55a\Rightarrow100=5a\Rightarrow a=20\)。"]}},
            ]},
        ],
    },

    "part3": {
        "ref_table": [
            {"k": "實數系", "v": r"正整數 \(\subset\) 整數 \(\subset\) 有理 \(\subset\) 實數；實數 ＝ 有理 \(\cup\) 無理"},
            {"k": "有理 / 無理", "v": r"有理＝可化分數（有限或循環小數）；無理＝不循環無限小數"},
            {"k": "運算判定", "v": r"有理＋無理＝無理；無理±無理、無理×無理不一定"},
            {"k": "循環小數", "v": r"\(0.\overline{ab}=\dfrac{ab}{99}\)、\(0.\overline{abc}=\dfrac{abc}{999}\)"},
            {"k": "絕對值意義", "v": r"\(|a|\)＝到原點距離；\(|a-b|\)＝兩點距離"},
            {"k": "絕對值不等式", "v": r"\(|x|\lt k\Leftrightarrow-k\lt x\lt k\)；\(|x|\gt k\Leftrightarrow x\lt-k\) 或 \(x\gt k\)"},
            {"k": "三角不等式", "v": r"\(|a-b|\le|a\pm b|\le|a|+|b|\)；\(|x-a|+|x-b|\) 最小 \(=|a-b|\)"},
            {"k": "去絕對值技巧", "v": r"幾何意義／分段討論；兩邊非負時 \(|A|\ge|B|\Leftrightarrow A^2\ge B^2\)"},
            {"k": "距離 / 中點 / 分點", "v": r"\(|a-b|\)、\(\dfrac{a+b}{2}\)、\(\dfrac{na+mb}{m+n}\)"},
            {"k": "根號估算", "v": r"\(\sqrt N\) 夾相鄰平方根；\(\sqrt{a+b\pm2\sqrt{ab}}=\sqrt a\pm\sqrt b\)"},
            {"k": "乘法 / 對稱式", "v": r"\((a\pm b)^2=a^2\pm2ab+b^2\)；\(a^2+b^2=(a+b)^2-2ab\)"},
            {"k": "算幾不等式", "v": r"\(\dfrac{a+b}{2}\ge\sqrt{ab}\)（\(a,b\ge0\)，\(a=b\) 等號）；\(x+\dfrac kx\ge2\sqrt k\)"},
            {"k": "百分率 / 加權", "v": r"連續漲跌連乘；合併平均 \(=\dfrac{ax+by}{a+b}\)（加權）"},
            {"k": "高斯函數", "v": r"\([x]\le x\lt[x]+1\)；\([x+n]=[x]+n\)；負數往更小取（\([-3.1]=-4\)）"},
        ],
        "checklist": [
            r"\(\sqrt{a^2}=|a|\)，不是 \(a\)（\(a\) 可能為負）。",
            r"\(|a+b|\le|a|+|b|\)，等號只在同號（含 0）時。",
            r"\(|x-a|+|x-b|\) 最小值是 \(|a-b|\)，不是 0。",
            r"循環小數是有理數（可化分數）；\(0.\overline{9}=1\)。",
            r"無理±無理、無理×無理不一定是無理（需找反例）。",
            r"「同時滿足」兩條件取 **交集**，不是聯集。",
            r"\(\sqrt{a+b}\neq\sqrt a+\sqrt b\)；根號對加法不可拆。",
            r"算幾不等式須 \(a,b\ge0\)，等號須驗證 \(a=b\) 可達。",
            r"連續漲跌幅要 **連乘**，不可相加。",
            r"兩組合併平均要 **加權**，不是兩平均再平均。",
            r"\([-3.1]=-4\)（負數往更小取），不是 \(-3\)。",
            r"\([x]\) 是向下取整，不是四捨五入。",
        ],
    },
}
