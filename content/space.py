# -*- coding: utf-8 -*-
r"""空間向量單元 · 單一來源內容（單元10：空間向量與空間中的平面與直線）。

挖空原則：只挖「公式與概念關鍵」（自行判斷）。
例題以官方原卷（106~115學測數學試卷.pdf）為準，答案對官方答案頁校正；數 B 題不採用。

考點對應核心概念分析（單元10）六大主軸：
  ① 空間坐標與距離  ② 內積與垂直  ③ 外積與體積
  ④ 平面方程式、投影與點到平面距離  ⑤ 空間直線與歪斜線  ⑥ 二面角與立體
※ 本檔逐考點建置中；先 Part 0＋考點 1。
"""

# 正立方體（斜投影）— 隱藏頂點 H 相關邊以虛線表示
SVG_CUBE = r'''<svg viewBox="0 0 200 175" width="200" height="175" xmlns="http://www.w3.org/2000/svg" role="img">
  <g fill="none" stroke="#2c7a6b" stroke-width="2" stroke-linejoin="round">
    <!-- 前面 ABCD -->
    <path d="M35 58 L125 58 L125 148 L35 148 Z"/>
    <!-- 後面上、右、連接邊（可見） -->
    <path d="M75 23 L165 23 L165 113"/>
    <path d="M35 58 L75 23"/>
    <path d="M125 58 L165 23"/>
    <path d="M125 148 L165 113"/>
    <!-- 隱藏邊（虛線）：經由後下左頂點 H -->
    <path d="M75 23 L75 113 M75 113 L165 113 M35 148 L75 113" stroke-dasharray="4 4" stroke-width="1.4"/>
  </g>
  <g fill="#22433c" font-size="12" font-family="serif" font-style="italic">
    <text x="26" y="55">A</text><text x="128" y="55">B</text>
    <text x="128" y="161">C</text><text x="24" y="160">D</text>
    <text x="70" y="20">E</text><text x="168" y="20">F</text>
    <text x="169" y="125">G</text><text x="62" y="118">H</text>
  </g>
</svg>'''

# 外積 u×v：同時垂直 u、v；長度 = u,v 張成的平行四邊形面積
SVG_CROSS = r'''<svg viewBox="0 0 256 200" width="256" height="200" xmlns="http://www.w3.org/2000/svg" role="img" font-family="'Microsoft JhengHei',system-ui,sans-serif"><polygon points="92,150 182,134 248,168 158,184" fill="#eef0f5" stroke="#9aa6b2" stroke-width="1" stroke-dasharray="4 3"/><line x1="92" y1="150" x2="182" y2="134" stroke="#1f3a93" stroke-width="2.2"/><polygon points="182,134 173.7,139.6 172.3,131.6" fill="#1f3a93"/><line x1="92" y1="150" x2="158" y2="184" stroke="#1f3a93" stroke-width="2.2"/><polygon points="158,184 148.0,183.4 151.8,176.2" fill="#1f3a93"/><line x1="92" y1="150" x2="92" y2="52" stroke="#c0392b" stroke-width="2.6"/><polygon points="92,52 96.1,61.1 87.9,61.1" fill="#c0392b"/><path d="M92,137 L103,137 L103,148" fill="none" stroke="#9aa6b2" stroke-width="1"/><circle cx="92" cy="150" r="2.6" fill="#2c3e50"/><text x="196" y="130" font-size="13" font-weight="bold" font-style="italic" fill="#1f3a93" text-anchor="middle">v</text><line x1="190" y1="119.3" x2="200" y2="119.3" stroke="#1f3a93" stroke-width="1.1"/><polygon points="203,119.3 199,117.1 199,121.5" fill="#1f3a93"/><text x="150" y="200" font-size="13" font-weight="bold" font-style="italic" fill="#1f3a93" text-anchor="middle">u</text><line x1="144" y1="189.3" x2="154" y2="189.3" stroke="#1f3a93" stroke-width="1.1"/><polygon points="157,189.3 153,187.1 153,191.5" fill="#1f3a93"/><text x="48" y="40" font-size="13" font-weight="bold" font-style="italic" fill="#c0392b" text-anchor="middle">u</text><line x1="42" y1="29.3" x2="52" y2="29.3" stroke="#c0392b" stroke-width="1.1"/><polygon points="55,29.3 51,27.1 51,31.5" fill="#c0392b"/><text x="62" y="40" font-size="13" font-weight="bold" fill="#c0392b" text-anchor="middle">×</text><text x="76" y="40" font-size="13" font-weight="bold" font-style="italic" fill="#c0392b" text-anchor="middle">v</text><line x1="70" y1="29.3" x2="80" y2="29.3" stroke="#c0392b" stroke-width="1.1"/><polygon points="83,29.3 79,27.1 79,31.5" fill="#c0392b"/><text x="180" y="158" font-size="9.5" fill="#5a4a52" text-anchor="middle">面積 = |u×v|</text></svg>'''

import openers  # Part 0 開場「闖關知識地圖」

UNIT = {
    "slug": "space",
    "file": "115學測數學_空間向量.html",
    "page_title": "115 學測數學 · 空間向量",
    "emoji": "🧊",
    "title": "空間向量",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 六大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "六大考點",
    "foot": "115 學測數學 · 空間向量 · 學測數學重點整理",

    "part0": {
        "opener": {"svg": openers.OPENERS["space"], "full": True,
                   "caption": r"**必考重點地圖**：①坐標·距離 → ②內積·夾角·垂直（核心）→ ③外積·體積（行列式）→ ④平面與點到平面距離"},
        "heading": "為什麼空間向量是高 CP 值的拉分單元",
        "trend_table": {
            "years": [106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            "counts": ["2.5", "3.0", "2.0", "1.5", "2.0", "2.5", "3.5", "3.0", "1.5", "3.5"],
            "total": "25.0",
        },
        "notes": [
            r"**題數第三高（近十年約 \(25\) 題）**：數 A 年年 \(1.5\)–\(3.5\) 題，\(112\)、\(115\) 各 \(3.5\) 題，是高報酬單元。",
            r"**兩大 ★★★ 核心**：外積與體積、平面方程式與點到平面距離——最常考、也最會拉開差距。",
            r"**武器很集中**：幾乎每題都化成 **內積、外積、行列式** 三件工具，學會就能通殺一整個單元。",
            r"**常跨單元整合**：與矩陣（行列式、線性方程組）、平面向量、三角（夾角、二面角）緊密結合。",
        ],
        "map": r"命題主軸六條：① 空間坐標與距離 ② 向量內積與垂直 ③ 外積與體積 ④ 平面方程式、投影與點到平面距離 ⑤ 空間直線與歪斜線 ⑥ 二面角與立體。",
    },

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "空間坐標與距離",
            "title": r"空間坐標、距離與正立方體",
            "intro": r"把空間中的點、線、面通通「**坐標化**」——這是整個單元的總策略。先掌握 **兩點距離**、**中點**，以及正立方體三種長度。",
            "points": [
                {"label": r"空間坐標", "lines": [
                    r"空間中一點以 \(P(x,y,z)\) 表示；三坐標平面為 \(xy\)（\(z=0\)）、\(yz\)（\(x=0\)）、\(zx\)（\(y=0\)）。",
                    r"點 \(P(x,y,z)\) 到 \(xy\) 平面的距離 ＝ 【\(|z|\)】（到 \(yz\)、\(zx\) 平面同理為 \(|x|\)、\(|y|\)）。"]},
                {"label": r"兩點距離", "lines": [
                    r"\(A(x_1,y_1,z_1)\)、\(B(x_2,y_2,z_2)\)：",
                    r"\(\overline{AB}=\) 【\(\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}\)】。"]},
                {"label": r"中點", "lines": [
                    r"\(\overline{AB}\) 中點 \(M=\) 【\(\left(\dfrac{x_1+x_2}{2},\,\dfrac{y_1+y_2}{2},\,\dfrac{z_1+z_2}{2}\right)\)】。"]},
                {"label": r"正立方體三長度", "lines": [
                    r"邊長 \(a\) 的正立方體：邊 ＝ \(a\)、面對角線 ＝ 【\(\sqrt2\,a\)】、體對角線 ＝ 【\(\sqrt3\,a\)】（[[怎麼來||面對角線 ＝ 邊長 \(a\) 正方形的對角線 \(\sqrt{a^2+a^2}=\sqrt2a\)；體對角線連接相對兩頂點 \(\sqrt{a^2+a^2+a^2}=\sqrt3a\)。空間題把每個頂點的坐標都取 \(0\) 或 \(a\) 最快。]]）。"]},
                {"svg": SVG_CUBE, "caption": r"空間題萬用第一步：把正立方體頂點坐標化"},
            ],
            "misconceptions": [
                {"wrong": r"兩點距離只算 \(x,y\) 兩項", "right": r"空間距離有三項：\(\sqrt{\Delta x^2+\Delta y^2+\Delta z^2}\)"},
                {"wrong": r"體對角線 \(=\sqrt2\,a\)", "right": r"面對角線才 \(\sqrt2a\)；體對角線 \(=\sqrt3a\)"},
                {"wrong": r"點到坐標平面要套點到平面公式", "right": r"到 \(xy\) 平面就是 \(|z|\)，直接讀坐標"},
                {"wrong": r"中點公式用兩端點相減", "right": r"中點是兩端點坐標 **相加除以 \(2\)**"},
            ],
            "questions": [
                {"tag": "108 · 選填 F", "level": "★★☆（中）", "core": "空間距離：用體對角線鉛直擺放求最小邊長",
                 "body": r"坐標空間中，考慮有一個頂點在平面 \(z=0\) 上、且另一個頂點在平面 \(z=6\) 上的正立方體。試求滿足前述條件的正立方體之 **邊長最小可能值**（化成最簡根式）。",
                 "solution": {"brief": r"\(2\sqrt3\)",
                              "steps": [
                                  r"正立方體兩頂點間距離只有三種：邊長 \(a\)、面對角線 \(\sqrt2a\)、**體對角線 \(\sqrt3a\)**（最長）。",
                                  r"要讓一頂點落在 \(z=0\)、另一頂點落在 \(z=6\)，兩頂點的 **鉛直高度差需達 \(6\)**。而長度 \(L\) 的線段，鉛直高度差最大為 \(L\)（線段鉛直時）。",
                                  r"想邊長最小 → 用最長的對角線去「頂」這個高度：把 **體對角線 \(\sqrt3a\) 鉛直** 擺放，\(\sqrt3a=6\)。",
                                  r"\(a=\dfrac{6}{\sqrt3}=\dfrac{6\sqrt3}{3}=2\sqrt3\)。故最小邊長 \(=\mathbf{2\sqrt3}\)。"]}},
                {"tag": "空間距離範例", "level": "★☆☆（基礎）", "core": "兩點距離 · 中點",
                 "body": r"坐標空間中有兩點 \(A(1,2,2)\)、\(B(3,-2,4)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求 \(\overline{AB}\)。",
                      "solution": {"brief": r"\(2\sqrt6\)",
                                   "steps": [r"\(\overline{AB}=\sqrt{(3-1)^2+(-2-2)^2+(4-2)^2}=\sqrt{4+16+4}=\sqrt{24}=2\sqrt6\)。"]}},
                     {"label": "(2)", "body": r"求 \(\overline{AB}\) 的中點 \(M\)。",
                      "solution": {"brief": r"\(M=(2,0,3)\)",
                                   "steps": [
                                       r"\(M=\left(\dfrac{1+3}{2},\dfrac{2+(-2)}{2},\dfrac{2+4}{2}\right)=(2,0,3)\)。"]}},
                 ]},
            ],
            "selfcheck": {
                "q": r"\(A(1,2,2)\)、\(B(3,2,4)\) 的距離為何？",
                "a": r"**\(2\sqrt2\)**：\(\sqrt{4+0+4}\)。"},
            "strategy": [
                r"空間題第一步幾乎都是 **建坐標**：把立方體、長方體頂點的坐標都取 \(0\) 或 \(a\)（例如 \((0,0,0),(a,a,0),(a,a,a)\)），距離、向量全用算的。",
                r"立方體三長度要分清：邊 \(a\)、面對角線 \(\sqrt2a\)、體對角線 \(\sqrt3a\)。",
                r"求「最小邊長／最短距離」常是：固定一個幾何限制，再用最長對角線或鉛直擺放去逼近。",
            ],
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "內積與垂直",
            "title": r"空間向量的內積、夾角與垂直",
            "intro": r"內積是空間向量的「**萬用尺**」——一個式子同時量長度、夾角、垂直。記住兩種算法（坐標 vs 長度×cos）與最常用的判別：**垂直 ⇔ 內積為 \(0\)**。",
            "points": [
                {"label": r"向量與長度", "lines": [
                    r"\(\vec v=(a,b,c)\)，長度 \(|\vec v|=\) 【\(\sqrt{a^2+b^2+c^2}\)】；",
                    r"\(\overrightarrow{AB}=B-A=\) 【\((x_2-x_1,\,y_2-y_1,\,z_2-z_1)\)】。"]},
                {"label": r"內積（兩種算法）", "lines": [
                    r"坐標式：\(\vec u\cdot\vec v=\) 【\(u_1v_1+u_2v_2+u_3v_3\)】；",
                    r"幾何式：\(\vec u\cdot\vec v=\) 【\(|\vec u|\,|\vec v|\cos\theta\)】（\(\theta\) 為兩向量夾角）。"]},
                {"label": r"夾角", "lines": [
                    r"\(\cos\theta=\) 【\(\dfrac{\vec u\cdot\vec v}{|\vec u|\,|\vec v|}\)】；內積 **正 → 銳角、負 → 鈍角、零 → 直角**。"]},
                {"label": r"垂直判別", "lines": [
                    r"兩非零向量 \(\vec u\perp\vec v\Leftrightarrow\vec u\cdot\vec v=\) 【\(0\)】。"]},
                {"label": r"正射影（投影向量）", "lines": [
                    r"\(\vec u\) 在 \(\vec v\) 上的正射影（投影向量）＝ 【\(\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\,\vec v\)】（[[幾何意義||把 \(\vec u\) 投影到 \(\vec v\) 方向所得的 **向量**：方向沿 \(\vec v\)、長度為 \(\dfrac{|\vec u\cdot\vec v|}{|\vec v|}\)。這是點到直線、點到平面距離的基礎。]]）。"]},
            ],
            "misconceptions": [
                {"wrong": r"內積的結果是向量", "right": r"內積是 **純量**（一個數）；外積才是向量"},
                {"wrong": r"要兩向量等長才會垂直", "right": r"垂直只看 **內積為 \(0\)**，與長度無關"},
                {"wrong": r"\(\cos\theta\) 等於內積本身", "right": r"要除長度：\(\cos\theta=\dfrac{\vec u\cdot\vec v}{|\vec u||\vec v|}\)"},
                {"wrong": r"內積為負代表兩向量反向", "right": r"內積 \(<0\) 只代表 **鈍角**；恰反向才是 \(\cos\theta=-1\)"},
            ],
            "questions": [
                {"tag": "112 數A · 單選 6", "level": "★★★（難）", "core": "內積 ＋ 期望值（立方體頂點兩兩內積）",
                 "body": r"坐標空間中，考慮邊長為 \(1\) 的正立方體，固定一頂點 \(O\)。從 \(O\) 以外的七個頂點隨機選取相異兩點 \(P\)、\(Q\)，試問內積 \(\overrightarrow{OP}\cdot\overrightarrow{OQ}\) 的期望值為何？",
                 "options": [r"\(\dfrac47\)", r"\(\dfrac57\)", r"\(\dfrac67\)", r"\(1\)", r"\(\dfrac87\)"],
                 "solution": {"brief": r"(3) \(\dfrac67\)",
                              "steps": [
                                  r"設 \(O\) 為原點，立方體頂點為各坐標取 \(0\) 或 \(1\)。\(O\) 以外七頂點：\(3\) 個相鄰（\(|OP|^2=1\)）、\(3\) 個面對角（\(|OP|^2=2\)）、\(1\) 個體對角（\(|OP|^2=3\)）。",
                                  r"取兩點共 \(C^7_2=21\) 對，用恆等式 \(\displaystyle\sum_{i<j}\vec{u_i}\cdot\vec{u_j}=\frac12\!\left(\Big|\sum\vec{u_i}\Big|^2-\sum|\vec{u_i}|^2\right)\)。",
                                  r"\(\sum\vec{OP_i}=(4,4,4)\)（八頂點和 \((4,4,4)\) 減去 \(O\)）→ \(\big|\sum\big|^2=48\)；\(\sum|\vec{OP_i}|^2=3(1)+3(2)+1(3)=12\)。",
                                  r"\(\displaystyle\sum_{i<j}\vec{OP_i}\cdot\vec{OP_j}=\frac12(48-12)=18\)；期望值 \(=\dfrac{18}{21}=\dfrac67\)，選 (3)。"]}},
                {"tag": "內積觀念範例", "level": "★☆☆（基礎）", "core": "長度 · 內積 · 夾角 · 垂直求參數",
                 "body": r"設空間向量 \(\vec a=(1,2,2)\)、\(\vec b=(2,-1,2)\)、\(\vec c=(t,1,-1)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求 \(|\vec a|\) 與 \(\vec a\cdot\vec b\)。",
                      "solution": {"brief": r"\(|\vec a|=3\)，\(\vec a\cdot\vec b=4\)",
                                   "steps": [r"\(|\vec a|=\sqrt{1+4+4}=3\)；\(\vec a\cdot\vec b=1\cdot2+2\cdot(-1)+2\cdot2=2-2+4=4\)。"]}},
                     {"label": "(2)", "body": r"求 \(\vec a\) 與 \(\vec b\) 夾角的 \(\cos\theta\)。",
                      "solution": {"brief": r"\(\dfrac49\)",
                                   "steps": [r"\(|\vec b|=\sqrt{4+1+4}=3\)；\(\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}=\dfrac{4}{3\times3}=\dfrac49\)。"]}},
                     {"label": "(3)", "body": r"若 \(\vec a\perp\vec c\)，求 \(t\)。",
                      "solution": {"brief": r"\(t=0\)",
                                   "steps": [r"\(\vec a\perp\vec c\Rightarrow\vec a\cdot\vec c=0\)：\(1\cdot t+2\cdot1+2\cdot(-1)=t+2-2=t=0\)。"]}},
                 ]},
            ],
            "selfcheck": {
                "q": r"\((1,2,2)\) 與 \((2,-1,0)\) 是否垂直？",
                "a": r"**垂直**：內積 \(2-2+0=0\)。"},
            "strategy": [
                r"看到「**垂直**」立刻寫「內積 ＝ \(0\)」列方程式求參數。",
                r"求夾角 ＝ 內積 ÷（兩長度）；只問銳／鈍／直角時，**看內積正負** 即可，不必算到底。",
                r"立方體、長方體的內積題，先把頂點坐標化，內積就是「對應坐標相乘再相加」。",
                r"「對一堆頂點兩兩取內積再平均」型期望值（如本考點 \(112\) 單6），善用 \(\sum_{i<j}\vec{u_i}\cdot\vec{u_j}=\frac12\big(|\sum\vec{u_i}|^2-\sum|\vec{u_i}|^2\big)\)。",
            ],
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "外積與體積",
            "title": r"外積、面積與體積（行列式）",
            "intro": r"外積把「兩向量」變出一個 **同時垂直兩者** 的新向量，長度剛好是平行四邊形面積。再配上行列式，**法向量、面積、體積** 一次搞定——這是本單元最會拉分的 ★★★ 核心。",
            "points": [
                {"label": r"外積的坐標", "lines": [
                    r"\(\vec u\times\vec v=\) 【\((u_2v_3-u_3v_2,\;u_3v_1-u_1v_3,\;u_1v_2-u_2v_1)\)】；",
                    r"可用行列式 \(\begin{vmatrix}\vec i&\vec j&\vec k\\u_1&u_2&u_3\\v_1&v_2&v_3\end{vmatrix}\) 展開記憶。"]},
                {"label": r"外積的方向與長度", "lines": [
                    r"方向：\(\vec u\times\vec v\) 【同時垂直】 \(\vec u\) 與 \(\vec v\)（右手定則）；",
                    r"長度：\(|\vec u\times\vec v|=\) 【\(|\vec u|\,|\vec v|\sin\theta\)】 ＝ 以 \(\vec u,\vec v\) 為鄰邊的 **平行四邊形面積**。"]},
                {"svg": SVG_CROSS, "med": True, "caption": r"外積 \(\vec u\times\vec v\)（紅）同時垂直 \(\vec u,\vec v\)（右手定則）；其長度 ＝ \(\vec u,\vec v\) 張成的平行四邊形面積"},
                {"label": r"三角形面積", "lines": [
                    r"\(\triangle ABC\) 面積 ＝ 【\(\dfrac12\left|\overrightarrow{AB}\times\overrightarrow{AC}\right|\)】。"]},
                {"label": r"純量三重積與體積", "lines": [
                    r"平行六面體體積 ＝ 【\(\left|\vec u\cdot(\vec v\times\vec w)\right|\)】（[[亦＝行列式絕對值||把 \(\vec u,\vec v,\vec w\) 的坐標排成 \(3\times3\) 行列式、取絕對值即得：\(\left|\det\begin{pmatrix}u_1&u_2&u_3\\v_1&v_2&v_3\\w_1&w_2&w_3\end{pmatrix}\right|\)。]]）；",
                    r"四面體體積 ＝ 【\(\dfrac16\left|\vec u\cdot(\vec v\times\vec w)\right|\)】。"]},
                {"label": r"兩兩垂直的特例", "lines": [
                    r"若 \(\vec u,\vec v,\vec w\) **兩兩垂直**：平行六面體即長方體，體積 ＝ 【\(|\vec u|\,|\vec v|\,|\vec w|\)】。"]},
            ],
            "misconceptions": [
                {"wrong": r"外積的結果是純量", "right": r"外積是 **向量**（內積才是純量）"},
                {"wrong": r"\(\vec u\times\vec v=\vec v\times\vec u\)", "right": r"反交換：\(\vec v\times\vec u=-\vec u\times\vec v\)（方向相反）"},
                {"wrong": r"平行四邊形面積要除 \(2\)", "right": r"平行四邊形 ＝ \(|\vec u\times\vec v|\)；**三角形** 才除 \(2\)"},
                {"wrong": r"三重積算出負值就是體積", "right": r"體積要取 **絕對值**（三重積可正可負）"},
            ],
            "questions": [
                {"tag": "113 數A · 單選 2", "level": "★★☆（中）", "core": "外積方向：與平面法向量平行",
                 "body": r"正方體 \(OABC\)–\(DEFG\) 中，\(OABC\)、\(DEFG\) 分別為下、上底面，且 \(D\)、\(E\)、\(F\)、\(G\) 分別在頂點 \(O\)、\(A\)、\(B\)、\(C\) 的正上方。試問向量外積 \(\overrightarrow{AD}\times\overrightarrow{AG}\) 與下列哪一個向量平行？",
                 "options": [r"\(\overrightarrow{AE}\)", r"\(\overrightarrow{BE}\)", r"\(\overrightarrow{CE}\)", r"\(\overrightarrow{DE}\)", r"\(\overrightarrow{OE}\)"],
                 "solution": {"brief": r"(5) \(\overrightarrow{OE}\)",
                              "steps": [
                                  r"取邊長 \(1\)、\(O\) 為原點：\(A(1,0,0),\,D(0,0,1),\,E(1,0,1),\,G(0,1,1)\)。",
                                  r"\(\overrightarrow{AD}=D-A=(-1,0,1)\)、\(\overrightarrow{AG}=G-A=(-1,1,1)\)。",
                                  r"\(\overrightarrow{AD}\times\overrightarrow{AG}=(0\cdot1-1\cdot1,\;1\cdot(-1)-(-1)\cdot1,\;(-1)\cdot1-0\cdot(-1))=(-1,0,-1)\)。",
                                  r"而 \(\overrightarrow{OE}=E-O=(1,0,1)\)，恰 \((-1,0,-1)=-\overrightarrow{OE}\) → 兩者平行（外積垂直於平面 \(ADG\)，\(OE\) 正是該面法線）。選 (5)。"]}},
                {"tag": "114 數A · 單選 6", "level": "★★★（難）", "core": "兩兩垂直向量張出的平行六面體體積",
                 "body": r"坐標空間中有三個 **彼此互相垂直** 的向量 \(\vec u,\vec v,\vec w\)。已知 \(\vec u-\vec v=(2,-1,0)\)，且 \(\vec v-\vec w=(-1,2,3)\)。試問由 \(\vec u,\vec v,\vec w\) 所張出的平行六面體之體積為何？",
                 "options": [r"\(2\sqrt5\)", r"\(5\sqrt2\)", r"\(2\sqrt{10}\)", r"\(4\sqrt5\)", r"\(4\sqrt{10}\)"],
                 "solution": {"brief": r"(3) \(2\sqrt{10}\)",
                              "steps": [
                                  r"三向量兩兩垂直 → 平行六面體即長方體，體積 ＝ \(|\vec u|\,|\vec v|\,|\vec w|\)。",
                                  r"因 \(\vec u\cdot\vec v=0\)，\(|\vec u-\vec v|^2=|\vec u|^2+|\vec v|^2=2^2+1^2+0^2=5\)；同理 \(|\vec v-\vec w|^2=|\vec v|^2+|\vec w|^2=1+4+9=14\)。",
                                  r"\(\vec u-\vec w=(\vec u-\vec v)+(\vec v-\vec w)=(1,1,3)\)，\(|\vec u-\vec w|^2=|\vec u|^2+|\vec w|^2=11\)。",
                                  r"三式相加得 \(|\vec u|^2+|\vec v|^2+|\vec w|^2=15\)，解出 \(|\vec u|^2=1,\;|\vec v|^2=4,\;|\vec w|^2=10\)。",
                                  r"體積 ＝ \(1\cdot2\cdot\sqrt{10}=2\sqrt{10}\)，選 (3)。"]}},
            ],
            "selfcheck": {
                "q": r"\(\vec u=(2,0,0),\vec v=(0,3,0),\vec w=(0,0,4)\) 張成的平行六面體體積為何？",
                "a": r"**\(24\)**：兩兩垂直 → \(|\vec u||\vec v||\vec w|=2\cdot3\cdot4\)。"},
            "strategy": [
                r"外積算坐標記「行列式第一列放 \(\vec i,\vec j,\vec k\)」；方向同時垂直兩向量，是求 **法向量** 的利器。",
                r"**空間中** 要「平行四邊形／三角形面積」「同時垂直兩向量的方向」→ 一律想外積。",
                r"體積：平行六面體 ＝ 三重積絕對值；四面體再 \(\times\dfrac16\)。",
                r"向量兩兩垂直時別硬算外積，直接 \(|\vec u||\vec v||\vec w|\)；常配合 \(|\vec u-\vec v|^2=|\vec u|^2+|\vec v|^2\) 求各長度。",
            ],
        },
        {
            "num": "考點 4", "id": "kp4", "nav": "平面方程式與距離",
            "title": r"平面方程式、投影與點到平面距離",
            "intro": r"平面用「**法向量 ＋ 一點**」就能決定。本考點是 ★★★ 最大重鎮：求平面方程式、點到平面距離、投影點。武器仍是 **外積**（求法向量）＋ **內積**（判平面上、求夾角）。",
            "points": [
                {"label": r"平面方程式", "lines": [
                    r"法向量 \(\vec n=(a,b,c)\)、過 \((x_0,y_0,z_0)\)：\(a(x-x_0)+b(y-y_0)+c(z-z_0)=0\)，即 \(ax+by+cz=\) 【\(d\)】（\(d=ax_0+by_0+cz_0\)）；",
                    r"平面 \(ax+by+cz=d\) 的法向量 ＝ 【\((a,b,c)\)】（直接讀係數）。"]},
                {"label": r"由三點求平面", "lines": [
                    r"三點 \(A,B,C\)：法向量 \(\vec n=\) 【\(\overrightarrow{AB}\times\overrightarrow{AC}\)】，再代任一點求 \(d\)。"]},
                {"label": r"點到平面距離", "lines": [
                    r"點 \((x_0,y_0,z_0)\) 到平面 \(ax+by+cz=d\) 的距離 ＝",
                    r"【\(\dfrac{|ax_0+by_0+cz_0-d|}{\sqrt{a^2+b^2+c^2}}\)】。"]},
                {"label": r"兩平面的關係", "lines": [
                    r"夾角 ＝ 兩 **法向量** 的夾角（用 \(\cos\) 算、有兩個互補的角）；",
                    r"平行 \(\Leftrightarrow\) 法向量平行（【成比例】）；",
                    r"垂直 \(\Leftrightarrow\) 法向量垂直（【內積為 \(0\)】）。"]},
                {"label": r"投影點與對稱點", "lines": [
                    r"點 \(P\) 到平面 \(E\) 的投影 \(P'\)：沿法向量移動 \(P'=P+t\vec n\)、代入 \(E\) 解 \(t\)；",
                    r"\(P\) 到 \(E\) 的距離 ＝ \(|PP'|=\) 【\(|t|\,|\vec n|\)】。"]},
            ],
            "misconceptions": [
                {"wrong": r"平面方程式右邊一定是 \(0\)", "right": r"一般是 \(ax+by+cz=d\)；過原點時 \(d\) 才為 \(0\)"},
                {"wrong": r"點到平面距離不必取絕對值", "right": r"分子要 **絕對值**、分母是法向量長度 \(\sqrt{a^2+b^2+c^2}\)"},
                {"wrong": r"兩平面夾角用平面內的向量算", "right": r"用 **法向量** 夾角（用 \(\cos\) 算、有兩個互補角）"},
                {"wrong": r"法向量要解聯立才看得出", "right": r"\(ax+by+cz=d\) 的法向量直接讀 \((a,b,c)\)"},
            ],
            "questions": [
                {"tag": "108 · 多選 13", "level": "★★★（難）", "core": "三點求平面、含坐標軸、點到平面距離",
                 "body": r"坐標空間中有一平面 \(P\) 過 \((0,0,0)\)、\((1,2,3)\)、\((-1,2,3)\) 三點。試選出正確的選項。",
                 "options": [
                     r"向量 \((0,3,2)\) 與平面 \(P\) 垂直",
                     r"平面 \(P\) 與 \(xy\) 平面垂直",
                     r"點 \((0,4,6)\) 在平面 \(P\) 上",
                     r"平面 \(P\) 包含 \(x\) 軸",
                     r"點 \((1,1,1)\) 到平面 \(P\) 的距離是 \(1\)"],
                 "solution": {"brief": r"(3)(4)",
                              "steps": [
                                  r"法向量 \(\vec n=(1,2,3)\times(-1,2,3)=(0,-6,4)\parallel(0,3,-2)\)；\(P\) 過原點 → \(P:3y-2z=0\)。",
                                  r"(1)✗ \((0,3,2)\) 不平行於法向量 \((0,3,-2)\)，故不垂直於 \(P\)。",
                                  r"(2)✗ \(xy\) 平面法向量 \((0,0,1)\)，\((0,3,-2)\cdot(0,0,1)=-2\neq0\)，兩平面不垂直。",
                                  r"(3)○ \((0,4,6)\)：\(3(4)-2(6)=0\)，在 \(P\) 上。(4)○ \(x\) 軸點 \((t,0,0)\)：\(3(0)-2(0)=0\) 恆成立，\(P\) 含 \(x\) 軸。",
                                  r"(5)✗ 距離 \(=\dfrac{|3(1)-2(1)|}{\sqrt{3^2+2^2}}=\dfrac{1}{\sqrt{13}}\neq1\)。故選 (3)(4)。"]}},
                {"tag": "112 數A · 選填 16", "level": "★★★（難）", "core": "投影點為外心、點到平面距離",
                 "body": r"令 \(E:x+z=2\) 為坐標空間中過三點 \(A(2,-1,0)\)、\(B(0,1,2)\)、\(C(-2,1,4)\) 的平面。另有一點 \(P\) 在平面 \(z=1\) 上，且其在 \(E\) 的投影點與 \(A\)、\(B\)、\(C\) 三點 **等距離**。試求點 \(P\) 與平面 \(E\) 的距離（最簡根式）。",
                 "solution": {"brief": r"\(2\sqrt2\)",
                              "steps": [
                                  r"\(E:x+z=2\)，法向量 \(\vec n=(1,0,1)\)。投影點 \(P'\) 在 \(E\) 上且與 \(A,B,C\) 等距 → \(P'\) 是 \(\triangle ABC\) 的 **外心**。",
                                  r"設 \(P'=(x,y,z)\)，由 \(|P'A|^2=|P'B|^2=|P'C|^2\) 配合 \(x+z=2\)，解得 \(P'=(-1,-4,3)\)（驗證三距離平方皆 \(=27\)）。",
                                  r"\(P\) 在平面 \(z=1\)、且沿法向量投影到 \(P'\)：\(P=P'+t\vec n=(-1+t,\,-4,\,3+t)\)，由 \(z=3+t=1\Rightarrow t=-2\)，得 \(P=(-3,-4,1)\)。",
                                  r"距離 \(=\dfrac{|(-3)+1-2|}{\sqrt{1^2+1^2}}=\dfrac{4}{\sqrt2}=2\sqrt2\)。"]}},
            ],
            "selfcheck": {
                "q": r"點 \((1,1,1)\) 到平面 \(x+y+z=6\) 的距離為何？",
                "a": r"**\(\sqrt3\)**：\(\dfrac{|1+1+1-6|}{\sqrt3}=\dfrac{3}{\sqrt3}\)。"},
            "strategy": [
                r"求平面先找 **法向量**：三點 → 兩向量外積；已知垂直某向量 → 那向量就是法向量；再代一點定 \(d\)。",
                r"點到平面距離直接套公式：分子代入 **取絕對值**、分母是法向量長度。",
                r"兩平面的夾角、平行、垂直 → 一律看 **法向量**。",
                r"投影點／對稱點：沿法向量參數化 \(P+t\vec n\)、代條件解 \(t\)；距離 ＝ \(|t|\,|\vec n|\)。",
            ],
        },
        {
            "num": "考點 5", "id": "kp5", "nav": "空間直線與歪斜線",
            "title": r"空間中的直線、軌跡與歪斜線",
            "intro": r"空間直線用「**一點 ＋ 方向向量**」描述。重點在判斷兩直線是平行、相交還是 **歪斜**（不平行又不相交），以及點到直線、歪斜線間的距離。",
            "points": [
                {"label": r"直線參數式", "lines": [
                    r"過點 \((x_0,y_0,z_0)\)、方向向量 \(\vec d=(a,b,c)\)：",
                    r"\((x,y,z)=\) 【\((x_0+at,\;y_0+bt,\;z_0+ct)\)】，\(t\in\mathbb{R}\)。"]},
                {"label": r"兩直線的關係", "lines": [
                    r"方向向量 **平行** → 兩直線平行或重合；",
                    r"方向向量 **不平行** → 相交或 **歪斜**（[[怎麼分||方向不平行時，把兩直線參數式設相等解聯立：**有解 → 相交**（共平面）；**無解 → 歪斜**（不共平面、也不相交）。]]）。"]},
                {"label": r"直線與平面", "lines": [
                    r"直線方向 \(\vec d\)、平面法向量 \(\vec n\)：",
                    r"直線 \(/\!/\) 平面 \(\Leftrightarrow\) 【\(\vec d\cdot\vec n=0\)】；",
                    r"直線 \(\perp\) 平面 \(\Leftrightarrow\) 【\(\vec d\,/\!/\,\vec n\)】。"]},
                {"label": r"點到直線距離", "lines": [
                    r"點 \(P\) 到「過 \(A\)、方向 \(\vec d\)」的直線：距離 ＝ 【\(\dfrac{|\overrightarrow{AP}\times\vec d|}{|\vec d|}\)】。"]},
                {"label": r"兩歪斜線距離", "lines": [
                    r"\(L_1\)（過 \(P_1\)、方向 \(\vec{d_1}\)）、\(L_2\)（過 \(P_2\)、方向 \(\vec{d_2}\)）：",
                    r"距離 ＝ 【\(\dfrac{|\overrightarrow{P_1P_2}\cdot(\vec{d_1}\times\vec{d_2})|}{|\vec{d_1}\times\vec{d_2}|}\)】（[[幾何意義||分子 ＝ 以 \(\overrightarrow{P_1P_2},\vec{d_1},\vec{d_2}\) 為邊的平行六面體體積；分母 ＝ 底面積 \(|\vec{d_1}\times\vec{d_2}|\)。體積 ÷ 底面積 ＝ 高，正是兩歪斜線的最短距離。]]）。"]},
            ],
            "misconceptions": [
                {"wrong": r"兩直線不平行就一定相交", "right": r"空間中還可能 **歪斜**（不平行也不相交）"},
                {"wrong": r"直線平行平面要 \(\vec d\,/\!/\,\vec n\)", "right": r"平行是 \(\vec d\cdot\vec n=0\)；\(\vec d\,/\!/\,\vec n\) 是 **垂直**"},
                {"wrong": r"點到直線套點到平面公式", "right": r"點到直線用 \(\dfrac{|\overrightarrow{AP}\times\vec d|}{|\vec d|}\)（外積）"},
                {"wrong": r"歪斜線距離取兩點直接連", "right": r"要沿 **公垂線**（\(\vec{d_1}\times\vec{d_2}\) 方向）量才是最短"},
            ],
            "questions": [
                {"tag": "107 · 單選 1", "level": "★★☆（中）", "core": "空間軌跡：平面截球面得一圓",
                 "body": r"給定相異兩點 \(A\)、\(B\)，試問空間中能使 \(\triangle PAB\) 成一 **正三角形** 的所有點 \(P\) 所成集合為下列哪一選項？",
                 "options": [r"兩個點", r"一線段", r"一直線", r"一圓", r"一平面"],
                 "solution": {"brief": r"(4) 一圓",
                              "steps": [
                                  r"\(\triangle PAB\) 為正三角形 \(\Leftrightarrow|PA|=|PB|=|AB|\)。",
                                  r"\(|PA|=|PB|\)：\(P\) 落在 \(\overline{AB}\) 的 **垂直平分面**（一個平面）上。",
                                  r"\(|PA|=|AB|\)（定值）：\(P\) 落在以 \(A\) 為球心、半徑 \(|AB|\) 的 **球面** 上。",
                                  r"平面 \(\cap\) 球面 ＝ **一圓**（平面截球）。選 (4)。"]}},
                {"tag": "歪斜線範例", "level": "★★☆（中）", "core": "歪斜判定與兩歪斜線距離",
                 "body": r"設直線 \(L_1\) 過 \((0,0,0)\)、方向向量 \((1,0,0)\)；\(L_2\) 過 \((0,0,1)\)、方向向量 \((0,1,0)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"判斷 \(L_1\)、\(L_2\) 為平行、相交還是歪斜。",
                      "solution": {"brief": r"歪斜",
                                   "steps": [r"方向 \((1,0,0)\)、\((0,1,0)\) 不平行。設兩參數式相等：\((t,0,0)=(0,s,1)\)，第三式 \(0=1\) 矛盾、無解 → **歪斜**。"]}},
                     {"label": "(2)", "body": r"求 \(L_1\)、\(L_2\) 之間的距離。",
                      "solution": {"brief": r"\(1\)",
                                   "steps": [
                                       r"\(\vec{d_1}\times\vec{d_2}=(1,0,0)\times(0,1,0)=(0,0,1)\)；\(\overrightarrow{P_1P_2}=(0,0,1)\)。",
                                       r"距離 \(=\dfrac{|(0,0,1)\cdot(0,0,1)|}{|(0,0,1)|}=\dfrac{1}{1}=1\)。"]}},
                 ]},
            ],
            "selfcheck": {
                "q": r"兩直線方向 \((1,0,0)\)、\((0,1,0)\) 且不相交，是平行還是歪斜？",
                "a": r"**歪斜**：方向不平行、又不相交。"},
            "strategy": [
                r"兩直線先比 **方向向量**：平行就是平行／重合；不平行再解聯立判 **相交 vs 歪斜**。",
                r"點到直線用外積 \(\dfrac{|\overrightarrow{AP}\times\vec d|}{|\vec d|}\)；別跟點到平面公式搞混。",
                r"歪斜線距離 ＝ 三重積絕對值 ÷ \(|\vec{d_1}\times\vec{d_2}|\)（體積 ÷ 底面積 ＝ 高）。",
                r"「使三角形為正三角形／等腰」的 **點軌跡**（對應本考點 \(107\) 單1）：拆成「到兩點等距 → 中垂面」「到一點等距 → 球面」，再求兩者交集。",
            ],
        },
        {
            "num": "考點 6", "id": "kp6", "nav": "二面角與立體",
            "title": r"二面角與立體（摺疊問題）",
            "intro": r"立體題（摺疊、角錐）的關鍵是 **二面角**——兩個半平面沿一條稜的夾角。處理摺疊題的標準動作：**沿稜建坐標**，把垂直關係化成坐標，再用距離公式算。",
            "points": [
                {"label": r"二面角的量法", "lines": [
                    r"沿稜 \(\ell\) 的二面角：在兩半平面內各作 **垂直於稜** 的射線，這兩射線的夾角即二面角；",
                    r"亦可由兩面的 **法向量** 夾角求得（再取所需的銳角或鈍角）。"]},
                {"label": r"平面垂直", "lines": [
                    r"兩平面垂直 \(\Leftrightarrow\) 二面角 \(=90^\circ\Leftrightarrow\) 兩法向量 【內積為 \(0\)】。"]},
                {"label": r"三垂線定理", "lines": [
                    r"自平面外一點 \(P\) 向平面作垂足 \(H\)、再自 \(H\) 向面內直線 \(\ell\) 作垂足 \(F\)：則 【\(PF\perp\ell\)】；",
                    r"常用來「定出二面角」或「算點到直線距離」。"]},
                {"label": r"摺疊問題標準解法", "lines": [
                    r"沿摺線（稜）建坐標：摺線當一軸；摺後若兩平面垂直，兩半平面分別落在 **互相垂直的兩坐標平面**；",
                    r"各點以「到摺線的垂足 ＋ 垂直距離」定坐標，再用 【兩點距離公式】 求空間距離。"]},
            ],
            "misconceptions": [
                {"wrong": r"二面角 ＝ 兩平面內任兩線的夾角", "right": r"兩射線都要 **垂直於稜** 才是二面角"},
                {"wrong": r"摺疊後邊長會改變", "right": r"摺疊只改變空間相對位置，**各三角形內部邊長、角度不變**"},
                {"wrong": r"兩平面垂直 → 面內所有線都互相垂直", "right": r"只有特定（垂直於稜）的方向才垂直"},
            ],
            "questions": [
                {"tag": "107 · 選填 H", "level": "★★★（難）", "core": "摺疊成直二面角、沿稜建坐標求空間距離",
                 "body": r"將一塊邊長 \(AB=15\) 公分、\(BC=20\) 公分的長方形鐵片 \(ABCD\) 沿對角線 \(BD\) 對摺後豎立，使得平面 \(ABD\) 與平面 \(CBD\) **垂直**。試求 \(A\)、\(C\) 兩點（在空間中）的距離 \(\overline{AC}\)（最簡根式）。",
                 "solution": {"brief": r"\(\sqrt{337}\) 公分",
                              "steps": [
                                  r"對角線 \(BD=\sqrt{15^2+20^2}=25\)，摺線為 \(BD\)。",
                                  r"\(\triangle ABD\) 直角在 \(A\)：\(A\) 到 \(BD\) 的垂足 \(P\)，垂距 \(AP=\dfrac{15\times20}{25}=12\)，\(BP=\dfrac{15^2}{25}=9\)。",
                                  r"\(\triangle CBD\) 直角在 \(C\)：\(C\) 到 \(BD\) 的垂足 \(Q\)，垂距 \(CQ=12\)，\(BQ=\dfrac{20^2}{25}=16\)。",
                                  r"沿 \(BD\) 建坐標 \(B(0,0,0),D(25,0,0)\)，\(P(9,0,0),Q(16,0,0)\)。取平面 \(CBD\) 為 \(xy\) 面 → \(C=(16,12,0)\)；平面 \(ABD\perp CBD\) 取 \(xz\) 面 → \(A=(9,0,12)\)。",
                                  r"\(\overline{AC}=\sqrt{(16-9)^2+12^2+12^2}=\sqrt{49+144+144}=\sqrt{337}\)。"]}},
                {"tag": "二面角範例", "level": "★★☆（中）", "core": "正四面體相鄰兩面的二面角",
                 "body": r"設 \(ABCD\) 為邊長 \(a\) 的 **正四面體**。試求相鄰兩面（面 \(ABC\) 與面 \(ABD\)）所夾二面角 \(\theta\) 的 \(\cos\theta\)。",
                 "solution": {"brief": r"\(\cos\theta=\dfrac13\)",
                              "steps": [
                                  r"取公共稜 \(AB\) 的中點 \(M\)。正三角形中，\(CM\perp AB\)、\(DM\perp AB\)，故 \(\angle CMD\) 就是二面角 \(\theta\)。",
                                  r"\(CM=DM=\) 正三角形的高 \(=\dfrac{\sqrt3}{2}a\)，而 \(CD=a\)。",
                                  r"餘弦定理：\(\cos\theta=\dfrac{CM^2+DM^2-CD^2}{2\cdot CM\cdot DM}=\dfrac{\frac34a^2+\frac34a^2-a^2}{2\cdot\frac34a^2}=\dfrac{\frac12a^2}{\frac32a^2}=\dfrac13\)。"]}},
            ],
            "selfcheck": {
                "q": r"兩平面的法向量為 \((1,0,0)\)、\((0,1,0)\)，二面角為何？",
                "a": r"**\(90^\circ\)**：法向量互相垂直。"},
            "strategy": [
                r"摺疊題標準三步：① 找摺線、② 沿摺線建坐標（兩半平面落在垂直的坐標平面）、③ 兩點距離公式。",
                r"各點坐標 ＝（沿摺線的垂足位置、垂距、另一軸）；謹記摺疊 **不改各三角形內部長度**。",
                r"求二面角：兩半平面內各作 **垂直於稜** 的線量夾角（餘弦定理），或用兩面法向量。",
                r"看到「平面 A 與平面 B 垂直」就轉成「兩半平面落在垂直坐標面」或「法向量內積 \(=0\)」。",
            ],
        },
    ],

    "part2": {
        "count": "10", "note": "難度貼近學測，涵蓋六大考點 · 建議自行限時 40 分鐘作答後再對照詳解",
        "groups": [
            {"title": "一、單選題", "questions": [
                {"tag": "練習 1", "level": "★☆☆", "core": "兩點距離",
                 "body": r"坐標空間中 \(A(1,0,2)\)、\(B(3,2,2)\)，求 \(\overline{AB}\)。",
                 "options": [r"\(2\sqrt2\)", "4", r"\(2\sqrt3\)", r"\(\sqrt{10}\)", "6"],
                 "solution": {"brief": r"(1) \(2\sqrt2\)", "brief_label": "答",
                              "steps": [r"\(\overline{AB}=\sqrt{(3-1)^2+(2-0)^2+(2-2)^2}=\sqrt{4+4+0}=2\sqrt2\)。"]}},
                {"tag": "練習 2", "level": "★☆☆", "core": "垂直求參數",
                 "body": r"設 \(\vec a=(1,-2,1)\)、\(\vec b=(2,1,k)\)，且 \(\vec a\perp\vec b\)，求 \(k\)。",
                 "options": [r"\(-2\)", r"\(-1\)", "0", "1", "2"],
                 "solution": {"brief": "(3) 0", "brief_label": "答",
                              "steps": [r"\(\vec a\cdot\vec b=1\cdot2+(-2)\cdot1+1\cdot k=2-2+k=k=0\)。"]}},
                {"tag": "練習 3", "level": "★★☆", "core": "外積求三角形面積",
                 "body": r"\(\triangle OAB\) 中 \(O\) 為原點、\(A(1,1,0)\)、\(B(0,1,1)\)，求其面積。",
                 "options": [r"\(\dfrac{\sqrt3}{2}\)", r"\(\sqrt3\)", r"\(\dfrac12\)", r"\(\dfrac32\)", r"\(\dfrac{\sqrt2}{2}\)"],
                 "solution": {"brief": r"(1) \(\dfrac{\sqrt3}{2}\)", "brief_label": "答",
                              "steps": [r"\(\overrightarrow{OA}\times\overrightarrow{OB}=(1,1,0)\times(0,1,1)=(1,-1,1)\)，\(|\cdot|=\sqrt3\)。面積 \(=\dfrac12\sqrt3\)。"]}},
                {"tag": "練習 4", "level": "★★☆", "core": "點到平面距離",
                 "body": r"求點 \((1,2,3)\) 到平面 \(2x-y+2z=5\) 的距離。",
                 "options": [r"\(\dfrac13\)", r"\(\dfrac23\)", "1", r"\(\dfrac{1}{\sqrt3}\)", r"\(\dfrac53\)"],
                 "solution": {"brief": r"(1) \(\dfrac13\)", "brief_label": "答",
                              "steps": [r"\(\dfrac{|2(1)-2+2(3)-5|}{\sqrt{2^2+(-1)^2+2^2}}=\dfrac{|1|}{3}=\dfrac13\)。"]}},
                {"tag": "練習 5", "level": "★★☆", "core": "平行六面體體積（行列式）",
                 "body": r"由 \(\vec u=(2,0,0)\)、\(\vec v=(0,3,0)\)、\(\vec w=(1,1,4)\) 所張出的平行六面體體積為何？",
                 "options": ["12", "24", "6", "8", "18"],
                 "solution": {"brief": "(2) 24", "brief_label": "答",
                              "steps": [r"體積 \(=\left|\det\begin{pmatrix}2&0&0\\0&3&0\\1&1&4\end{pmatrix}\right|=|2(3\cdot4-0)|=24\)。"]}},
            ]},
            {"title": "二、多選題", "questions": [
                {"tag": "練習 6", "level": "★★★", "core": "內積、外積、垂直綜合",
                 "body": r"設 \(\vec a=(1,2,2)\)、\(\vec b=(2,-2,1)\)，下列敘述何者正確？",
                 "options": [
                     r"\(|\vec a|=3\)",
                     r"\(\vec a\perp\vec b\)",
                     r"\(|\vec b|=3\)",
                     r"\(|\vec a\times\vec b|=9\)",
                     r"\(\vec a\times\vec b=(6,3,6)\)"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"(1)○ \(\sqrt{1+4+4}=3\)。(2)○ \(\vec a\cdot\vec b=2-4+2=0\)。(3)○ \(\sqrt{4+4+1}=3\)。",
                                        r"(4)○ \(\vec a\perp\vec b\Rightarrow|\vec a\times\vec b|=|\vec a||\vec b|=9\)。(5)✗ 實際 \(\vec a\times\vec b=(6,3,-6)\)，非 \((6,3,6)\)。"]}},
                {"tag": "練習 7", "level": "★★★", "core": "平面方程式與直線關係",
                 "body": r"平面 \(E:x+2y+2z=6\)，下列敘述何者正確？",
                 "options": [
                     r"\(E\) 的一個法向量為 \((1,2,2)\)",
                     r"原點到 \(E\) 的距離為 \(2\)",
                     r"點 \((2,1,1)\) 在 \(E\) 上",
                     r"方向向量 \((1,1,1)\) 的直線與 \(E\) 垂直",
                     r"\(E\) 與平面 \(2x+4y+4z=1\) 平行"],
                 "solution": {"brief": "(1)(2)(3)(5)", "brief_label": "答",
                              "steps": [r"(1)○ 讀係數。(2)○ \(\dfrac{|0-6|}{\sqrt{1+4+4}}=\dfrac63=2\)。(3)○ \(2+2+2=6\)。",
                                        r"(4)✗ 垂直需 \((1,1,1)\parallel(1,2,2)\)，不成立。(5)○ \((2,4,4)=2(1,2,2)\)，法向量平行。"]}},
            ]},
            {"title": "三、選填題", "questions": [
                {"tag": "練習 8", "level": "★★☆", "core": "外積求空間三角形面積",
                 "body": r"設 \(\triangle ABC\) 頂點為 \(A(1,0,0)\)、\(B(0,2,0)\)、\(C(0,0,3)\)，求其面積。",
                 "solution": {"brief": r"\(\dfrac72\)", "brief_label": "答",
                              "steps": [r"\(\overrightarrow{AB}=(-1,2,0)\)、\(\overrightarrow{AC}=(-1,0,3)\)，\(\overrightarrow{AB}\times\overrightarrow{AC}=(6,3,2)\)。",
                                        r"面積 \(=\dfrac12|\overrightarrow{AB}\times\overrightarrow{AC}|=\dfrac12\sqrt{36+9+4}=\dfrac12\sqrt{49}=\dfrac72\)。"]}},
                {"tag": "練習 9", "level": "★★★", "core": "兩歪斜線距離",
                 "body": r"直線 \(L_1\) 過 \((0,0,0)\)、方向 \((1,1,0)\)；\(L_2\) 過 \((0,0,2)\)、方向 \((1,-1,0)\)。求 \(L_1\)、\(L_2\) 之間的距離。",
                 "solution": {"brief": "2", "brief_label": "答",
                              "steps": [r"\(\vec{d_1}\times\vec{d_2}=(1,1,0)\times(1,-1,0)=(0,0,-2)\)，\(\overrightarrow{P_1P_2}=(0,0,2)\)。",
                                        r"距離 \(=\dfrac{|(0,0,2)\cdot(0,0,-2)|}{|(0,0,-2)|}=\dfrac{4}{2}=2\)。"]}},
                {"tag": "練習 10", "level": "★★☆", "core": "向量夾角",
                 "body": r"求 \(\vec a=(1,1,0)\) 與 \(\vec b=(0,1,1)\) 的夾角（度數）。",
                 "solution": {"brief": r"\(60^\circ\)", "brief_label": "答",
                              "steps": [r"\(\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}=\dfrac{0+1+0}{\sqrt2\cdot\sqrt2}=\dfrac12\)，故 \(\theta=60^\circ\)。"]}},
            ]},
        ],
    },

    "part3": {
        "ref_table": [
            {"k": "兩點距離 / 中點", "v": r"\(\sqrt{\Delta x^2+\Delta y^2+\Delta z^2}\)；中點取坐標平均"},
            {"k": "正立方體三長度", "v": r"邊 \(a\)、面對角線 \(\sqrt2a\)、體對角線 \(\sqrt3a\)"},
            {"k": "內積", "v": r"\(\vec u\cdot\vec v=u_1v_1+u_2v_2+u_3v_3=|\vec u||\vec v|\cos\theta\)"},
            {"k": "夾角 / 垂直", "v": r"\(\cos\theta=\dfrac{\vec u\cdot\vec v}{|\vec u||\vec v|}\)；垂直 \(\Leftrightarrow\vec u\cdot\vec v=0\)"},
            {"k": "外積", "v": r"\((u_2v_3-u_3v_2,\,u_3v_1-u_1v_3,\,u_1v_2-u_2v_1)\)；同時垂直 \(\vec u,\vec v\)，\(|\vec u\times\vec v|=|\vec u||\vec v|\sin\theta\)"},
            {"k": "面積 / 體積", "v": r"\(\triangle=\frac12|\vec u\times\vec v|\)；平行六面體 \(=|\vec u\cdot(\vec v\times\vec w)|\)；四面體 \(=\frac16|\cdot|\)"},
            {"k": "平面方程式", "v": r"\(ax+by+cz=d\)，法向量 \((a,b,c)\)；三點求平面用 \(\overrightarrow{AB}\times\overrightarrow{AC}\)"},
            {"k": "點到平面距離", "v": r"\(\dfrac{|ax_0+by_0+cz_0-d|}{\sqrt{a^2+b^2+c^2}}\)"},
            {"k": "兩平面關係", "v": r"夾角、平行、垂直全看法向量（垂直 \(\Leftrightarrow\vec{n_1}\cdot\vec{n_2}=0\)）"},
            {"k": "直線參數式", "v": r"\((x_0+at,\,y_0+bt,\,z_0+ct)\)，方向向量 \((a,b,c)\)"},
            {"k": "直線與平面", "v": r"平行 \(\Leftrightarrow\vec d\cdot\vec n=0\)；垂直 \(\Leftrightarrow\vec d\,/\!/\,\vec n\)"},
            {"k": "兩直線關係", "v": r"方向平行 → 平行；不平行解聯立：有解相交、無解歪斜"},
            {"k": "點到直線 / 歪斜線距離", "v": r"\(\dfrac{|\overrightarrow{AP}\times\vec d|}{|\vec d|}\)；歪斜 \(\dfrac{|\overrightarrow{P_1P_2}\cdot(\vec{d_1}\times\vec{d_2})|}{|\vec{d_1}\times\vec{d_2}|}\)"},
            {"k": "二面角 / 摺疊", "v": r"兩半平面內各作垂直稜的線量夾角；摺疊沿稜建坐標、不改內部長度"},
        ],
        "checklist": [
            r"體對角線 \(\sqrt3a\)、面對角線 \(\sqrt2a\)，別搞混。",
            r"內積是 **純量**、外積是 **向量**。",
            r"垂直 \(\Leftrightarrow\) 內積 \(0\)；直線 \(\parallel\) 平面 \(\Leftrightarrow\vec d\cdot\vec n=0\)、直線 \(\perp\) 平面 \(\Leftrightarrow\vec d\parallel\vec n\)。",
            r"點到平面距離分子 **取絕對值**、分母是法向量長度。",
            r"平面 \(ax+by+cz=d\) 法向量直接讀 \((a,b,c)\)。",
            r"兩平面的夾角／平行／垂直 一律看法向量。",
            r"兩直線不平行 **還可能歪斜**（不相交）。",
            r"點到直線、兩歪斜線距離都用 **外積**。",
            r"平行六面體體積 ＝ 三重積絕對值；四面體再 \(\times\dfrac16\)。",
            r"向量兩兩垂直 → 體積 \(=|\vec u||\vec v||\vec w|\)。",
            r"摺疊題沿摺線建坐標，**各三角形內部邊長不變**。",
            r"二面角要用「**垂直於稜**」的兩線去量，不是隨便兩線。",
        ],
    },
}
