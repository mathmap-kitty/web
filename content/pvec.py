# -*- coding: utf-8 -*-
r"""平面向量單元 · 單一來源內容（單元8：平面向量）。

挖空原則：只挖「公式與概念關鍵」（自行判斷）。
例題以官方原卷（106~115學測數學試卷.pdf）為準，答案對官方答案頁校正；數 B 題不採用。

考點對應核心概念分析（單元8）：
  ① 向量運算與線性組合（分點、面積比）  ② 內積（夾角、垂直、正射影）
  ③ 行列式（面積）  ④ 向量與旋轉、坐標
※ 本檔逐考點建置中；先 Part 0＋考點 1。
"""

# 向量加法：三角形法（首尾相接 u→v）＋平行四邊形法，對角線 = u+v
SVG_VECADD = r'''<svg viewBox="0 0 206 126" width="206" height="126" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,'Segoe UI',sans-serif">
  <line x1="30" y1="112" x2="86" y2="56" stroke="#2e8b57" stroke-width="1.3" stroke-dasharray="4 3"/>
  <line x1="86" y1="56" x2="176" y2="40" stroke="#1f3a93" stroke-width="1.3" stroke-dasharray="4 3"/>
  <line x1="30" y1="112" x2="120" y2="96" stroke="#1f3a93" stroke-width="2.2"/>
  <polygon points="120,96 112,102 110,94" fill="#1f3a93"/>
  <line x1="120" y1="96" x2="176" y2="40" stroke="#2e8b57" stroke-width="2.2"/>
  <polygon points="176,40 172,49 167,44" fill="#2e8b57"/>
  <line x1="30" y1="112" x2="176" y2="40" stroke="#c0392b" stroke-width="2.4"/>
  <polygon points="176,40 170,48 166,40" fill="#c0392b"/>
  <circle cx="30" cy="112" r="2.6" fill="#333"/>
  <g font-size="12" font-weight="bold" font-style="italic">
    <text x="64" y="118" fill="#1f3a93">u</text>
    <text x="150" y="74" fill="#2e8b57">v</text>
    <text x="52" y="100" fill="#c0392b">u+v</text>
  </g>
  <text x="20" y="117" font-size="10" fill="#333">A</text>
</svg>'''

UNIT = {
    "slug": "pvec",
    "file": "115學測數學_平面向量_互動學習.html",
    "page_title": "115 學測數學 · 平面向量 · 互動學習",
    "emoji": "➡️",
    "title": "平面向量",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 五大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "五大考點",
    "foot": "115 學測數學 · 平面向量 · 互動學習講義",

    "part0": {
        "heading": "為什麼平面向量是幾何題的萬用語言",
        "trend_table": {
            "years": [106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            "counts": ["1.0", "1.5", "0.5", "3.0", "1.75", "1.0", "2.5", "1.3", "1.5", "1.5"],
            "total": "15.6",
        },
        "notes": [
            r"**題數中等（近十年約 \(15.6\) 題）**：數 A 年年 \(1\)–\(2.5\) 題，\(109\) 年甚至 \(3\) 題，是幾何題的萬用工具。",
            r"**兩大 ★★★ 核心**：線性組合（分點、面積比）、內積（夾角、垂直、正射影）。",
            r"**一體兩面**：幾何問題可化成向量「**用算的**」（內積、行列式），向量也能畫成幾何圖。",
            r"**常跨單元整合**：與三角（夾角、餘弦定理）、直線與圓、矩陣（旋轉）緊密結合。",
        ],
        "map": r"命題主軸五條：① 向量的表示與運算 ② 線性組合、分點與面積比 ③ 內積（夾角、垂直、正射影）④ 行列式與面積 ⑤ 向量的旋轉與坐標應用。",
    },

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "向量的表示與運算",
            "title": r"向量的表示、運算與平行",
            "intro": r"向量同時帶 **大小** 與 **方向**。先把向量「**坐標化**」，加減、係數積、長度、平行全部變成坐標的計算。",
            "points": [
                {"label": r"向量的表示", "lines": [
                    r"\(\overrightarrow{AB}=B-A=\) 【\((x_B-x_A,\,y_B-y_A)\)】（坐標 ＝ **終點減起點**）；",
                    r"相等向量：**大小、方向皆相同**（與位置無關）。"]},
                {"label": r"加減與係數積", "lines": [
                    r"\(\overrightarrow{AB}+\overrightarrow{BC}=\) 【\(\overrightarrow{AC}\)】（首尾相接）；",
                    r"坐標：\((a,b)\pm(c,d)=(a\pm c,\,b\pm d)\)、\(k(a,b)=(ka,kb)\)。"]},
                {"svg": SVG_VECADD,
                 "caption": r"**向量加法兩種畫法**：① 三角形法——\(\vec u\) 的終點接 \(\vec v\) 的起點（首尾相接），起點到終點即 \(\vec u+\vec v\)；② 平行四邊形法——\(\vec u,\vec v\) 同起點張成平行四邊形，**對角線** 就是 \(\vec u+\vec v\)（紅）。"},
                {"label": r"長度（大小）", "lines": [
                    r"\(\vec v=(a,b)\) 的長度 \(|\vec v|=\) 【\(\sqrt{a^2+b^2}\)】；",
                    r"單位向量（長度 \(1\)、同向）＝ 【\(\dfrac{\vec v}{|\vec v|}\)】。"]},
                {"label": r"平行（共線）", "lines": [
                    r"\(\vec u\,/\!/\,\vec v\Leftrightarrow\vec u=k\vec v\)（\(k\) 為實數）\(\Leftrightarrow\) 坐標 **成比例**；",
                    r"\((a,b)\,/\!/\,(c,d)\Leftrightarrow\) 【\(ad-bc=0\)】。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(\overrightarrow{AB}=A-B\)", "right": r"\(\overrightarrow{AB}=\) **終點 \(-\) 起點** \(=B-A\)"},
                {"wrong": r"向量相等要位置相同", "right": r"只要 **大小、方向** 相同，與位置無關"},
                {"wrong": r"向量平行要長度相等", "right": r"平行只要方向相同／相反（坐標成比例）"},
                {"wrong": r"\(|\vec v|=a+b\)", "right": r"\(|\vec v|=\sqrt{a^2+b^2}\)"},
            ],
            "questions": [
                {"tag": "向量運算範例", "level": "★☆☆（基礎）", "core": "坐標運算 · 長度 · 單位向量",
                 "body": r"設 \(A(1,2)\)、\(B(4,6)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求 \(\overrightarrow{AB}\) 與 \(|\overrightarrow{AB}|\)。",
                      "solution": {"brief": r"\(\overrightarrow{AB}=(3,4)\)、\(|\overrightarrow{AB}|=5\)",
                                   "steps": [r"\(\overrightarrow{AB}=(4-1,\,6-2)=(3,4)\)，\(|\overrightarrow{AB}|=\sqrt{3^2+4^2}=5\)。"]}},
                     {"label": "(2)", "body": r"求與 \(\overrightarrow{AB}\) 同方向的單位向量。",
                      "solution": {"brief": r"\(\left(\dfrac35,\dfrac45\right)\)",
                                   "steps": [r"單位向量 \(=\dfrac{\overrightarrow{AB}}{|\overrightarrow{AB}|}=\dfrac{(3,4)}{5}=\left(\dfrac35,\dfrac45\right)\)。"]}},
                 ]},
                {"tag": "平行求參數範例", "level": "★☆☆（基礎）", "core": "向量平行（成比例）",
                 "body": r"設 \(\vec u=(2,-3)\)、\(\vec v=(k,6)\)。若 \(\vec u\,/\!/\,\vec v\)，求 \(k\)。",
                 "solution": {"brief": r"\(k=-4\)",
                              "steps": [r"\(\vec u\,/\!/\,\vec v\Leftrightarrow ad-bc=0\)：\(2\times6-(-3)\times k=12+3k=0\Rightarrow k=-4\)。"]}},
            ],
            "selfcheck": {
                "q": r"向量 \((-3,4)\) 的長度為何？",
                "a": r"**\(5\)**：\(\sqrt{9+16}\)。"},
            "strategy": [
                r"向量坐標 ＝ **終點減起點**；運算就是「對應坐標加減、乘係數」。",
                r"長度 \(\sqrt{a^2+b^2}\)；單位向量 ＝ 向量 ÷ 長度。",
                r"平行（共線）\(\Leftrightarrow\) 坐標成比例 \(\Leftrightarrow ad-bc=0\)（交叉相乘相等）。",
                r"幾何題先「**設坐標** 或 **設基底向量**」，再全部用算的。",
            ],
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "線性組合、分點與面積比",
            "title": r"線性組合、分點與面積比",
            "intro": r"用兩個不平行向量當 **基底**，把平面上每個向量都「組合」出來。重點是 **分點公式**、**重心**，以及把 **面積比** 直接讀成線性組合的係數。",
            "points": [
                {"label": r"線性組合（基底）", "lines": [
                    r"平面上任一向量都可 **唯一** 寫成 \(\vec w=a\vec u+b\vec v\)（\(\vec u,\vec v\) 不平行，為一組 **基底**）。"]},
                {"label": r"分點公式", "lines": [
                    r"\(P\) 內分 \(\overline{AB}\) 為 \(m:n\)（\(\overline{AP}:\overline{PB}=m:n\)）：",
                    r"\(\overrightarrow{OP}=\) 【\(\dfrac{n\,\overrightarrow{OA}+m\,\overrightarrow{OB}}{m+n}\)】（[[對角交叉||靠近 \(B\)（佔比 \(m\)）的權重給 \(\overrightarrow{OB}\)、靠近 \(A\) 的給 \(\overrightarrow{OA}\)，係數 **對調交叉**。中點即 \(m=n\)：\(\dfrac{\overrightarrow{OA}+\overrightarrow{OB}}{2}\)。]]）。"]},
                {"label": r"中點與重心", "lines": [
                    r"中點 \(\overrightarrow{OM}=\dfrac{\overrightarrow{OA}+\overrightarrow{OB}}{2}\)；",
                    r"\(\triangle ABC\) 重心 \(\overrightarrow{OG}=\) 【\(\dfrac{\overrightarrow{OA}+\overrightarrow{OB}+\overrightarrow{OC}}{3}\)】。"]},
                {"label": r"共線判定", "lines": [
                    r"\(A,B,C\) 三點共線 \(\Leftrightarrow\overrightarrow{AC}=t\,\overrightarrow{AB}\)；",
                    r"\(\overrightarrow{OP}=\alpha\overrightarrow{OA}+\beta\overrightarrow{OB}\) 且 \(P\) 在直線 \(AB\) 上 \(\Leftrightarrow\) 【\(\alpha+\beta=1\)】。"]},
                {"label": r"面積比（關鍵）", "lines": [
                    r"\(P\) 在 \(\triangle ABC\) 內、\(\overrightarrow{AP}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\) 時：",
                    r"\(\triangle ABP=\) 【\(\beta\)】\(\times\triangle ABC\)；\(\triangle ACP=\alpha\times\triangle ABC\)；\(\triangle BCP=(1-\alpha-\beta)\times\triangle ABC\)。"]},
            ],
            "misconceptions": [
                {"wrong": r"分點公式係數照位置擺", "right": r"\(\overrightarrow{OP}=\dfrac{n\overrightarrow{OA}+m\overrightarrow{OB}}{m+n}\)：係數 **對角交叉**（靠 \(B\) 的權重 \(m\)）"},
                {"wrong": r"\(P\) 在直線 \(AB\) 上係數和任意", "right": r"\(\overrightarrow{OP}=\alpha\overrightarrow{OA}+\beta\overrightarrow{OB}\) 在直線 \(AB\) 上 \(\Leftrightarrow\alpha+\beta=1\)"},
                {"wrong": r"\(\overrightarrow{AP}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\) 時 \(\triangle ABP\) 佔 \(\alpha\)", "right": r"\(\triangle ABP\) 佔 **\(\beta\)**（另一邊 \(\overrightarrow{AC}\) 的係數）"},
            ],
            "questions": [
                {"tag": "111 數A · 多選 9", "level": "★★★（難）", "core": "線性組合的係數 ↔ 面積比",
                 "body": r"已知 \(P\) 為 \(\triangle ABC\) 內一點，且 \(\overrightarrow{AP}=a\overrightarrow{AB}+b\overrightarrow{AC}\)（\(a,b\) 為相異實數）。設 \(Q,R\) 在同一平面上，且 \(\overrightarrow{AQ}=b\overrightarrow{AB}+a\overrightarrow{AC}\)、\(\overrightarrow{AR}=a\overrightarrow{AB}+(b-0.05)\overrightarrow{AC}\)。試選出正確的選項。",
                 "options": [
                     r"\(Q,R\) 也都在 \(\triangle ABC\) 內部",
                     r"\(\overrightarrow{AP}=\overrightarrow{AQ}\)",
                     r"\(\triangle ABP\) 面積 \(=\triangle ACQ\) 面積",
                     r"\(\triangle BCP\) 面積 \(=\triangle BCQ\) 面積",
                     r"\(\triangle ABP\) 面積 \(=\triangle ABR\) 面積"],
                 "solution": {"brief": r"(3)(4)",
                              "steps": [
                                  r"關鍵：\(\overrightarrow{AX}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\Rightarrow\triangle ABX=\beta\,[ABC]\)、\(\triangle ACX=\alpha\,[ABC]\)、\(\triangle BCX=(1-\alpha-\beta)[ABC]\)。",
                                  r"(3)○ \(\triangle ABP=b\,[ABC]\)；\(\triangle ACQ=(Q\) 的 \(\overrightarrow{AB}\) 係數\()\,[ABC]=b\,[ABC]\)，相等。",
                                  r"(4)○ \(\triangle BCP=(1-a-b)[ABC]=\triangle BCQ\)（\(P,Q\) 的 \(\overrightarrow{AB}+\overrightarrow{AC}\) 係數和相同）。",
                                  r"(1)✗ \(R\) 的 \(\overrightarrow{AC}\) 係數 \(b-0.05\) 可能 \(<0\)，不一定在內部。(2)✗ \(a\neq b\Rightarrow\overrightarrow{AP}\neq\overrightarrow{AQ}\)。(5)✗ \(\triangle ABR=(b-0.05)[ABC]\neq b[ABC]\)。故選 (3)(4)。"]}},
                {"tag": "分點與重心範例", "level": "★☆☆（基礎）", "core": "中線 · 重心的線性組合",
                 "body": r"設 \(\triangle ABC\)，\(M\) 為 \(\overline{BC}\) 中點、\(G\) 為重心。",
                 "subqs": [
                     {"label": "(1)", "body": r"以 \(\overrightarrow{AB},\overrightarrow{AC}\) 表示 \(\overrightarrow{AM}\)。",
                      "solution": {"brief": r"\(\overrightarrow{AM}=\dfrac{\overrightarrow{AB}+\overrightarrow{AC}}{2}\)",
                                   "steps": [r"\(M\) 為 \(BC\) 中點：\(\overrightarrow{AM}=\dfrac{\overrightarrow{AB}+\overrightarrow{AC}}{2}\)。"]}},
                     {"label": "(2)", "body": r"以 \(\overrightarrow{AB},\overrightarrow{AC}\) 表示 \(\overrightarrow{AG}\)。",
                      "solution": {"brief": r"\(\overrightarrow{AG}=\dfrac{\overrightarrow{AB}+\overrightarrow{AC}}{3}\)",
                                   "steps": [r"重心 \(\overrightarrow{AG}=\dfrac23\overrightarrow{AM}=\dfrac23\cdot\dfrac{\overrightarrow{AB}+\overrightarrow{AC}}{2}=\dfrac{\overrightarrow{AB}+\overrightarrow{AC}}{3}\)。"]}},
                 ]},
            ],
            "selfcheck": {
                "q": r"\(\overrightarrow{AP}=\dfrac14\overrightarrow{AB}+\dfrac12\overrightarrow{AC}\)，則 \(\triangle ABP\) 佔 \(\triangle ABC\) 幾分之幾？",
                "a": r"**\(\dfrac12\)**：佔比 ＝ \(\overrightarrow{AC}\) 的係數 \(\beta\)。"},
            "strategy": [
                r"線性組合先選 **兩個不平行向量** 當基底，所有向量都用它們表示。",
                r"分點記「**對角交叉**」：\(\overrightarrow{AP}:\overrightarrow{PB}=m:n\Rightarrow\overrightarrow{OP}=\dfrac{n\overrightarrow{OA}+m\overrightarrow{OB}}{m+n}\)。",
                r"面積比口訣：\(\overrightarrow{AP}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\Rightarrow\triangle ABP\) 佔 \(\beta\)、\(\triangle ACP\) 佔 \(\alpha\)、\(\triangle BCP\) 佔 \(1-\alpha-\beta\)。",
                r"三點共線 \(\Leftrightarrow\) 係數和為 \(1\)（\(\overrightarrow{OP}=\alpha\overrightarrow{OA}+\beta\overrightarrow{OB}\)、\(\alpha+\beta=1\)）。",
            ],
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "內積：夾角、垂直、正射影",
            "title": r"內積：夾角、垂直與正射影",
            "intro": r"內積是平面向量的「**萬用尺**」——一個式子同時量長度、夾角、垂直，還能求 **正射影**。（與空間向量的內積完全同理。）",
            "points": [
                {"label": r"內積（兩種算法）", "lines": [
                    r"坐標式：\(\vec u\cdot\vec v=\) 【\(u_1v_1+u_2v_2\)】；",
                    r"幾何式：\(\vec u\cdot\vec v=\) 【\(|\vec u|\,|\vec v|\cos\theta\)】；且 \(|\vec u|^2=\vec u\cdot\vec u\)。"]},
                {"label": r"夾角", "lines": [
                    r"\(\cos\theta=\) 【\(\dfrac{\vec u\cdot\vec v}{|\vec u|\,|\vec v|}\)】；內積 **正 → 銳角、負 → 鈍角、零 → 直角**。"]},
                {"label": r"垂直", "lines": [
                    r"兩非零向量 \(\vec u\perp\vec v\Leftrightarrow\vec u\cdot\vec v=\) 【\(0\)】。"]},
                {"label": r"正射影", "lines": [
                    r"\(\vec u\) 在 \(\vec v\) 上的 **正射影向量** ＝ 【\(\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\,\vec v\)】；",
                    r"**正射影長**（在 \(\vec v\) 方向的分量）＝ \(\dfrac{\vec u\cdot\vec v}{|\vec v|}\)（[[帶正負號||正射影長 ＝ \(|\vec u|\cos\theta\)，與 \(\vec v\) 同向為正、反向為負；夾角為銳角時為正。\(113\) 選16 就用這個。]]）。"]},
            ],
            "misconceptions": [
                {"wrong": r"內積的結果是向量", "right": r"內積是 **純量**（一個數）"},
                {"wrong": r"正射影長 ＝ 內積", "right": r"要除以 \(|\vec v|\)：正射影長 \(=\dfrac{\vec u\cdot\vec v}{|\vec v|}\)"},
                {"wrong": r"要兩向量等長才垂直", "right": r"垂直只看 **內積為 \(0\)**，與長度無關"},
                {"wrong": r"\(\cos\theta\) 等於內積本身", "right": r"要除兩長度：\(\cos\theta=\dfrac{\vec u\cdot\vec v}{|\vec u||\vec v|}\)"},
            ],
            "questions": [
                {"tag": "109 數A · 單選 2", "level": "★★☆（中）", "core": "內積移項 → 垂直",
                 "body": r"相異四點 \(A,B,C,D\)，已知內積 \(\overrightarrow{AB}\cdot\overrightarrow{AC}=\overrightarrow{AB}\cdot\overrightarrow{AD}\)。試選出正確的選項。",
                 "options": [
                     r"\(\overrightarrow{AB}\cdot\overrightarrow{CD}=0\)",
                     r"\(\overrightarrow{AC}=\overrightarrow{AD}\)",
                     r"\(\overrightarrow{AB}\) 與 \(\overrightarrow{CD}\) 平行",
                     r"\(\overrightarrow{AD}\cdot\overrightarrow{BC}=0\)",
                     r"\(A,B,C,D\) 四點共平面"],
                 "solution": {"brief": r"(1)",
                              "steps": [
                                  r"移項：\(\overrightarrow{AB}\cdot\overrightarrow{AC}-\overrightarrow{AB}\cdot\overrightarrow{AD}=\overrightarrow{AB}\cdot(\overrightarrow{AC}-\overrightarrow{AD})=0\)。",
                                  r"而 \(\overrightarrow{AC}-\overrightarrow{AD}=\overrightarrow{DC}\)，故 \(\overrightarrow{AB}\cdot\overrightarrow{DC}=0\)，即 \(\overrightarrow{AB}\cdot\overrightarrow{CD}=0\)（\(\overrightarrow{AB}\perp\overrightarrow{CD}\)）。(1) ○。",
                                  r"(2)✗ 投影相等不代表向量相等。(3)✗ 內積 \(0\) 是垂直、非平行。(4)(5)✗ 推不出。故選 (1)。"]}},
                {"tag": "113 數A · 選填 16", "level": "★★★（難）", "core": "正射影長 ＋ 正交基底分解",
                 "body": r"已知向量 \(\vec v\) 在向量 \((2,-3)\) 方向的正射影長比 \(|\vec v|\) 少 \(1\)、在 \((3,2)\) 方向的正射影長比 \(|\vec v|\) 少 \(2\)，且 \(\vec v\) 與 \((2,-3)\)、\((3,2)\) 的夾角皆為銳角。求 \(\vec v\) 在 \((4,7)\) 方向的正射影長（最簡根式）。",
                 "solution": {"brief": r"\(\dfrac{2\sqrt5}{5}\)",
                              "steps": [
                                  r"\((2,-3)\cdot(3,2)=6-6=0\)：兩向量 **互相垂直**、長度皆 \(\sqrt{13}\)，可當正交基底。",
                                  r"設 \(L=|\vec v|\)。兩方向正射影長 \(L-1\)、\(L-2\)，由正交分解 \(L^2=(L-1)^2+(L-2)^2\Rightarrow L^2-6L+5=0\Rightarrow L=1\) 或 \(5\)。",
                                  r"\(L=1\) 使第二個正射影長 \(<0\)（與銳角矛盾），取 \(L=5\)；故 \(\vec v=\dfrac{4(2,-3)+3(3,2)}{\sqrt{13}}=\dfrac{(17,-6)}{\sqrt{13}}\)。",
                                  r"在 \((4,7)\)（長 \(\sqrt{65}\)）的正射影長 \(=\dfrac{\vec v\cdot(4,7)}{\sqrt{65}}=\dfrac{26/\sqrt{13}}{\sqrt{65}}=\dfrac{26}{13\sqrt5}=\dfrac{2\sqrt5}{5}\)。"]}},
            ],
            "selfcheck": {
                "q": r"若 \((2,k)\perp(3,-6)\)，求 \(k\)。",
                "a": r"**\(1\)**：內積 \(6-6k=0\)。"},
            "strategy": [
                r"內積三用途：長度（\(|\vec u|^2=\vec u\cdot\vec u\)）、夾角（\(\cos\theta\)）、垂直（\(=0\)）。",
                r"看到「垂直」立刻寫「內積 \(=0\)」；只問銳／鈍／直角看內積正負。",
                r"正射影長 \(=\dfrac{\vec u\cdot\vec v}{|\vec v|}\)；正射影向量 \(=\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\vec v\)。",
                r"遇到兩個 **互相垂直** 的向量，當「正交基底」用，\(|\vec v|^2=\) 各分量平方和。",
            ],
        },
        {
            "num": "考點 4", "id": "kp4", "nav": "行列式與平行四邊形面積",
            "title": r"行列式與平行四邊形面積",
            "intro": r"兩向量「張成」的平行四邊形面積 ＝ **行列式絕對值**。善用行列式「**對每個向量都是線性**」的性質，許多面積比題不必算坐標就能解。",
            "points": [
                {"label": r"二階行列式", "lines": [
                    r"\(\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=\) 【\(ad-bc\)】。"]},
                {"label": r"平行四邊形與三角形面積", "lines": [
                    r"\(\vec u=(u_1,u_2)\)、\(\vec v=(v_1,v_2)\) 張成的平行四邊形面積 ＝ 【\(|u_1v_2-u_2v_1|\)】（即 \(|\det(\vec u,\vec v)|\)）；",
                    r"三角形面積 ＝ 【\(\dfrac12|\det(\vec u,\vec v)|\)】。"]},
                {"label": r"行列式的線性性質", "lines": [
                    r"\(\det(\vec a,\vec b)=-\det(\vec b,\vec a)\)、\(\det(\vec a,\vec a)=0\)；",
                    r"對每個向量都 **線性**：\(\det(k\vec a+\vec c,\,\vec b)=k\det(\vec a,\vec b)+\det(\vec c,\vec b)\)。"]},
            ],
            "misconceptions": [
                {"wrong": r"行列式 \(=ad+bc\)", "right": r"是 \(ad-bc\)（**相減**）"},
                {"wrong": r"平行四邊形面積要除 \(2\)", "right": r"平行四邊形 ＝ \(|\det|\)；**三角形** 才除 \(2\)"},
                {"wrong": r"\(\det(\vec a,\vec b)=\det(\vec b,\vec a)\)", "right": r"反號：\(\det(\vec b,\vec a)=-\det(\vec a,\vec b)\)"},
            ],
            "questions": [
                {"tag": "110 · 單選 4", "level": "★★☆（中）", "core": "行列式的雙線性 → 面積比",
                 "body": r"設 \(\vec a\) 與 \(\vec b\) 都是平面上不為零的向量。若 \(2\vec a+\vec b\) 與 \(\vec a+2\vec b\) 所張成的 **三角形** 面積為 \(6\)，則 \(3\vec a+\vec b\) 與 \(\vec a+3\vec b\) 所張成的三角形面積為何？",
                 "options": [r"\(8\)", r"\(9\)", r"\(12\)", r"\(13.5\)", r"\(16\)"],
                 "solution": {"brief": r"(5) \(16\)",
                              "steps": [
                                  r"記 \([\vec u,\vec v]=\det(\vec u,\vec v)\)。用線性與 \([\vec a,\vec a]=[\vec b,\vec b]=0\)、\([\vec b,\vec a]=-[\vec a,\vec b]\)：",
                                  r"\([2\vec a+\vec b,\;\vec a+2\vec b]=4[\vec a,\vec b]+[\vec b,\vec a]=3[\vec a,\vec b]\)；三角形面積 \(\dfrac12|3[\vec a,\vec b]|=6\Rightarrow|[\vec a,\vec b]|=4\)。",
                                  r"\([3\vec a+\vec b,\;\vec a+3\vec b]=9[\vec a,\vec b]+[\vec b,\vec a]=8[\vec a,\vec b]\)；三角形面積 \(=\dfrac12\cdot8\cdot4=16\)。選 (5)。"]}},
                {"tag": "行列式面積範例", "level": "★☆☆（基礎）", "core": "坐標求平行四邊形 / 三角形面積",
                 "body": r"求由 \(\vec u=(3,1)\)、\(\vec v=(1,4)\) 所張成的平行四邊形面積與三角形面積。",
                 "solution": {"brief": r"平行四邊形 \(11\)、三角形 \(\dfrac{11}{2}\)",
                              "steps": [r"\(\det(\vec u,\vec v)=3\cdot4-1\cdot1=11\)。平行四邊形面積 \(=|11|=11\)，三角形面積 \(=\dfrac{11}{2}\)。"]}},
            ],
            "selfcheck": {
                "q": r"\(\vec u=(3,1),\vec v=(1,4)\) 張成的平行四邊形面積為何？",
                "a": r"**\(11\)**：\(|3\cdot4-1\cdot1|\)。"},
            "strategy": [
                r"平行四邊形面積 ＝ \(|\)行列式\(|\)；三角形 ＝ 一半。",
                r"面積題若給「基底向量的組合」，用行列式 **線性展開**、不必算坐標（\(110\) 單4）。",
                r"展開關鍵：\(\det(\vec a,\vec a)=0\)、交換變號 \(\det(\vec b,\vec a)=-\det(\vec a,\vec b)\)。",
            ],
        },
        {
            "num": "考點 5", "id": "kp5", "nav": "向量的旋轉與坐標應用",
            "title": r"向量的旋轉與坐標應用",
            "intro": r"把向量「**旋轉**」一個角度，是平面向量與三角、矩陣的交會點。掌握旋轉公式（尤其 \(90^\circ\)）與「用向量解坐標幾何」的手法。",
            "points": [
                {"label": r"旋轉公式", "lines": [
                    r"向量 \((x,y)\) 繞原點 **逆時針** 轉 \(\theta\)：新坐標 ＝ 【\((x\cos\theta-y\sin\theta,\;x\sin\theta+y\cos\theta)\)】；",
                    r"用 **矩陣** 表示：\(\begin{pmatrix}x'\\y'\end{pmatrix}=\) 【\(\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}\)】\(\begin{pmatrix}x\\y\end{pmatrix}\)（即 **旋轉矩陣**，與矩陣單元呼應）。"]},
                {"label": r"90° 旋轉（最常用）", "lines": [
                    r"逆時針 \(90^\circ\)：\((x,y)\to\) 【\((-y,\,x)\)】；",
                    r"順時針 \(90^\circ\)：\((x,y)\to\) 【\((y,\,-x)\)】。"]},
                {"label": r"與垂直方向的關係", "lines": [
                    r"\(\vec u=(a,b)\) 轉 \(90^\circ\) 得 **垂直向量** \((-b,a)\) 或 \((b,-a)\)，與 \(\vec u\) 內積為 \(0\)；",
                    r"旋轉 **不改變長度**（保長）。"]},
                {"label": r"用向量解坐標", "lines": [
                    r"幾何條件（垂直、等長、夾角、面積）→ 翻成 **內積、行列式、旋轉** → 用坐標算。"]},
            ],
            "misconceptions": [
                {"wrong": r"逆時針 \(90^\circ\) 是 \((y,-x)\)", "right": r"逆時針是 \((-y,x)\)；\((y,-x)\) 是 **順時針**"},
                {"wrong": r"旋轉會改變向量長度", "right": r"旋轉 **保長**（長度不變）"},
                {"wrong": r"旋轉公式 \(\sin\cos\) 位置可隨意", "right": r"固定 \((x\cos\theta-y\sin\theta,\;x\sin\theta+y\cos\theta)\)"},
            ],
            "questions": [
                {"tag": "旋轉範例", "level": "★★☆（中）", "core": "90° 與一般角的旋轉",
                 "body": r"設向量 \(\vec u=(3,1)\)。",
                 "subqs": [
                     {"label": "(1)", "body": r"求 \(\vec u\) 逆時針旋轉 \(90^\circ\) 後的向量。",
                      "solution": {"brief": r"\((-1,3)\)",
                                   "steps": [r"逆時針 \(90^\circ\)：\((x,y)\to(-y,x)\)，故 \((3,1)\to(-1,3)\)。"]}},
                     {"label": "(2)", "body": r"求 \(\vec u\) 逆時針旋轉 \(60^\circ\) 後的向量。",
                      "solution": {"brief": r"\(\left(\dfrac{3-\sqrt3}{2},\;\dfrac{3\sqrt3+1}{2}\right)\)",
                                   "steps": [r"\((3\cos60^\circ-1\sin60^\circ,\;3\sin60^\circ+1\cos60^\circ)=\left(\dfrac32-\dfrac{\sqrt3}{2},\;\dfrac{3\sqrt3}{2}+\dfrac12\right)=\left(\dfrac{3-\sqrt3}{2},\dfrac{3\sqrt3+1}{2}\right)\)。"]}},
                 ]},
                {"tag": "坐標應用範例", "level": "★★☆（中）", "core": "用 90° 旋轉求正方形頂點",
                 "body": r"正方形 \(ABCD\)（頂點 **逆時針** 排列）中，\(A(1,1)\)、\(B(4,2)\)。求頂點 \(C\)、\(D\)。",
                 "solution": {"brief": r"\(C(3,5)\)、\(D(0,4)\)",
                              "steps": [
                                  r"\(\overrightarrow{AB}=(3,1)\)。正方形逆時針 → \(\overrightarrow{BC}\) 是 \(\overrightarrow{AB}\) 逆時針轉 \(90^\circ\)：\((3,1)\to(-1,3)\)。",
                                  r"\(C=B+\overrightarrow{BC}=(4,2)+(-1,3)=(3,5)\)；\(\overrightarrow{AD}=\overrightarrow{BC}=(-1,3)\)，\(D=A+\overrightarrow{AD}=(0,4)\)。",
                                  r"驗證 \(\overrightarrow{AB}\cdot\overrightarrow{BC}=(3,1)\cdot(-1,3)=0\)（垂直）、\(|\overrightarrow{AB}|=|\overrightarrow{BC}|=\sqrt{10}\)（等長），確為正方形。"]}},
            ],
            "selfcheck": {
                "q": r"向量 \((2,5)\) 繞原點逆時針旋轉 \(90^\circ\) 後為何？",
                "a": r"**\((-5,2)\)**：\((x,y)\to(-y,x)\)。"},
            "strategy": [
                r"旋轉 \(90^\circ\) 記「逆時針 \((x,y)\to(-y,x)\)」——求正方形頂點、垂直方向最常用。",
                r"一般角用旋轉公式 \((x\cos\theta-y\sin\theta,\;x\sin\theta+y\cos\theta)\)。",
                r"正方形／等腰直角：把一邊 **旋轉 \(90^\circ\)** 得鄰邊。",
                r"幾何條件先翻成向量（內積＝垂直、行列式＝面積、旋轉＝轉角），再算坐標。",
            ],
        },
    ],

    "part2": {
        "count": "10", "note": "難度貼近學測，涵蓋五大考點 · 建議自行限時 40 分鐘作答後再對照詳解",
        "groups": [
            {"title": "一、單選題", "questions": [
                {"tag": "練習 1", "level": "★☆☆", "core": "向量坐標運算",
                 "body": r"設 \(\vec u=(2,-1)\)、\(\vec v=(1,3)\)，求 \(2\vec u-\vec v\)。",
                 "options": [r"\((3,-5)\)", r"\((5,1)\)", r"\((3,1)\)", r"\((1,-5)\)", r"\((4,-2)\)"],
                 "solution": {"brief": r"(1) \((3,-5)\)", "brief_label": "答",
                              "steps": [r"\(2\vec u-\vec v=(4,-2)-(1,3)=(3,-5)\)。"]}},
                {"tag": "練習 2", "level": "★☆☆", "core": "向量長度",
                 "body": r"求 \(\vec v=(-3,4)\) 的長度。",
                 "options": ["5", "7", r"\(\sqrt7\)", "25", "1"],
                 "solution": {"brief": "(1) 5", "brief_label": "答",
                              "steps": [r"\(|\vec v|=\sqrt{(-3)^2+4^2}=\sqrt{25}=5\)。"]}},
                {"tag": "練習 3", "level": "★★☆", "core": "夾角的餘弦",
                 "body": r"設 \(\vec u=(1,2)\)、\(\vec v=(3,-1)\)，求兩向量夾角 \(\theta\) 的 \(\cos\theta\)。",
                 "options": [r"\(\dfrac{\sqrt2}{10}\)", r"\(\dfrac{1}{5}\)", r"\(\dfrac{1}{\sqrt5}\)", r"\(\dfrac{2}{5}\)", r"\(\dfrac{\sqrt2}{2}\)"],
                 "solution": {"brief": r"(1) \(\dfrac{\sqrt2}{10}\)", "brief_label": "答",
                              "steps": [r"\(\vec u\cdot\vec v=3-2=1\)，\(|\vec u|=\sqrt5,|\vec v|=\sqrt{10}\)。\(\cos\theta=\dfrac{1}{\sqrt5\cdot\sqrt{10}}=\dfrac{1}{5\sqrt2}=\dfrac{\sqrt2}{10}\)。"]}},
                {"tag": "練習 4", "level": "★★☆", "core": "垂直求參數",
                 "body": r"若 \((2,k)\perp(3,-6)\)，求 \(k\)。",
                 "options": ["1", "2", r"\(-1\)", "4", "0"],
                 "solution": {"brief": "(1) 1", "brief_label": "答",
                              "steps": [r"垂直 \(\Rightarrow\) 內積 \(=2\cdot3+k\cdot(-6)=6-6k=0\Rightarrow k=1\)。"]}},
                {"tag": "練習 5", "level": "★★☆", "core": "行列式求三角形面積",
                 "body": r"求頂點 \(O(0,0)\)、\(A(3,1)\)、\(B(1,4)\) 的三角形面積。",
                 "options": [r"\(\dfrac{11}{2}\)", "11", r"\(\dfrac{13}{2}\)", "13", "6"],
                 "solution": {"brief": r"(1) \(\dfrac{11}{2}\)", "brief_label": "答",
                              "steps": [r"面積 \(=\dfrac12|\det(\overrightarrow{OA},\overrightarrow{OB})|=\dfrac12|3\cdot4-1\cdot1|=\dfrac{11}{2}\)。"]}},
            ]},
            {"title": "二、多選題", "questions": [
                {"tag": "練習 6", "level": "★★★", "core": "內積、長度、垂直、正射影綜合",
                 "body": r"設 \(\vec u=(3,4)\)、\(\vec v=(4,-3)\)，下列敘述何者正確？",
                 "options": [
                     r"\(|\vec u|=5\)",
                     r"\(|\vec v|=5\)",
                     r"\(\vec u\perp\vec v\)",
                     r"\(\vec u+\vec v=(7,1)\)",
                     r"\(\vec u\) 在 \(\vec v\) 上的正射影長為 \(5\)"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"(1)(2)○ \(\sqrt{9+16}=5\)。(3)○ \(\vec u\cdot\vec v=12-12=0\)。(4)○ \((3+4,4-3)=(7,1)\)。",
                                        r"(5)✗ 正射影長 \(=\dfrac{\vec u\cdot\vec v}{|\vec v|}=\dfrac{0}{5}=0\neq5\)。"]}},
                {"tag": "練習 7", "level": "★★★", "core": "線性組合的係數 ↔ 面積比",
                 "body": r"\(P\) 在 \(\triangle ABC\) 內，\(\overrightarrow{AP}=\dfrac14\overrightarrow{AB}+\dfrac12\overrightarrow{AC}\)，下列敘述何者正確？",
                 "options": [
                     r"\(\triangle ABP=\dfrac12\triangle ABC\)",
                     r"\(\triangle ACP=\dfrac14\triangle ABC\)",
                     r"\(\triangle BCP=\dfrac14\triangle ABC\)",
                     r"\(\triangle ABP:\triangle ACP=2:1\)",
                     r"\(P\) 在 \(\overline{BC}\) 上"],
                 "solution": {"brief": "(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"\(\alpha=\frac14,\beta=\frac12\)：(1)○ \(\triangle ABP=\beta=\frac12\)。(2)○ \(\triangle ACP=\alpha=\frac14\)。(3)○ \(\triangle BCP=1-\frac14-\frac12=\frac14\)。(4)○ \(\frac12:\frac14=2:1\)。",
                                        r"(5)✗ 在 \(BC\) 上須係數和 \(=1\)，但 \(\frac14+\frac12=\frac34\neq1\)。"]}},
            ]},
            {"title": "三、選填題", "questions": [
                {"tag": "練習 8", "level": "★★☆", "core": "分點公式",
                 "body": r"設 \(A(1,2)\)、\(B(7,8)\)，\(P\) 內分 \(\overline{AB}\) 為 \(\overline{AP}:\overline{PB}=1:2\)。求 \(P\) 坐標。",
                 "solution": {"brief": r"\((3,4)\)", "brief_label": "答",
                              "steps": [r"\(\overrightarrow{OP}=\dfrac{2\,\overrightarrow{OA}+1\,\overrightarrow{OB}}{3}=\dfrac{2(1,2)+(7,8)}{3}=\dfrac{(9,12)}{3}=(3,4)\)。"]}},
                {"tag": "練習 9", "level": "★★☆", "core": "90° 旋轉",
                 "body": r"求向量 \((2,5)\) 繞原點逆時針旋轉 \(90^\circ\) 後的向量。",
                 "solution": {"brief": r"\((-5,2)\)", "brief_label": "答",
                              "steps": [r"逆時針 \(90^\circ\)：\((x,y)\to(-y,x)\)，故 \((2,5)\to(-5,2)\)。"]}},
                {"tag": "練習 10", "level": "★★☆", "core": "行列式求平行四邊形面積",
                 "body": r"求由 \(\vec u=(5,2)\)、\(\vec v=(1,3)\) 所張成的平行四邊形面積。",
                 "solution": {"brief": "13", "brief_label": "答",
                              "steps": [r"面積 \(=|\det(\vec u,\vec v)|=|5\cdot3-2\cdot1|=|13|=13\)。"]}},
            ]},
        ],
    },

    "part3": {
        "ref_table": [
            {"k": "向量坐標", "v": r"\(\overrightarrow{AB}=B-A\)；\(|\vec v|=\sqrt{a^2+b^2}\)；單位向量 \(\dfrac{\vec v}{|\vec v|}\)"},
            {"k": "平行（共線）", "v": r"\((a,b)\,/\!/\,(c,d)\Leftrightarrow ad-bc=0\)"},
            {"k": "分點公式", "v": r"\(\overline{AP}:\overline{PB}=m:n\Rightarrow\overrightarrow{OP}=\dfrac{n\overrightarrow{OA}+m\overrightarrow{OB}}{m+n}\)"},
            {"k": "重心 / 共線", "v": r"重心 \(\dfrac{\overrightarrow{OA}+\overrightarrow{OB}+\overrightarrow{OC}}{3}\)；\(P\) 在 \(AB\) 上 \(\Leftrightarrow\) 係數和 \(=1\)"},
            {"k": "面積比", "v": r"\(\overrightarrow{AP}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\Rightarrow\triangle ABP=\beta\,[ABC]\)、\(\triangle ACP=\alpha\,[ABC]\)、\(\triangle BCP=(1-\alpha-\beta)[ABC]\)"},
            {"k": "內積", "v": r"\(\vec u\cdot\vec v=u_1v_1+u_2v_2=|\vec u||\vec v|\cos\theta\)"},
            {"k": "夾角 / 垂直", "v": r"\(\cos\theta=\dfrac{\vec u\cdot\vec v}{|\vec u||\vec v|}\)；垂直 \(\Leftrightarrow\vec u\cdot\vec v=0\)"},
            {"k": "正射影", "v": r"向量 \(\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\vec v\)；長 \(\dfrac{\vec u\cdot\vec v}{|\vec v|}\)"},
            {"k": "行列式 / 面積", "v": r"\(\det=ad-bc\)；平行四邊形 \(|\det|\)、三角形 \(\frac12|\det|\)"},
            {"k": "旋轉", "v": r"逆時針 \(\theta\)：\((x\cos\theta-y\sin\theta,\,x\sin\theta+y\cos\theta)\)；逆 \(90^\circ\)：\((x,y)\to(-y,x)\)"},
        ],
        "checklist": [
            r"\(\overrightarrow{AB}=\) 終點 \(-\) 起點 \(=B-A\)。",
            r"平行（共線）\(\Leftrightarrow ad-bc=0\)。",
            r"分點對角交叉：\(\overline{AP}:\overline{PB}=m:n\Rightarrow\overrightarrow{OP}=\dfrac{n\overrightarrow{OA}+m\overrightarrow{OB}}{m+n}\)。",
            r"三點共線 \(\Leftrightarrow\) 係數和 \(=1\)。",
            r"\(\overrightarrow{AP}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\Rightarrow\triangle ABP\) 佔 **\(\beta\)**（另一邊係數）。",
            r"內積是 **純量**；垂直 \(\Leftrightarrow\) 內積 \(=0\)。",
            r"正射影長 \(=\dfrac{\vec u\cdot\vec v}{|\vec v|}\)（要除長度）。",
            r"平行四邊形面積 \(=|\det|\)；三角形 \(\frac12|\det|\)。",
            r"逆時針 \(90^\circ\)：\((x,y)\to(-y,x)\)（順時針 \((y,-x)\)）。",
            r"旋轉 **保長**（不改變向量長度）。",
        ],
    },
}
