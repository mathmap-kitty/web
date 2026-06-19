# -*- coding: utf-8 -*-
r"""三角單元 · 單一來源內容。

歷年題數之冠（106–115 合計 30.6 題），命題主戰場。例題以官方原卷校正。
※ 本檔目前含 Part 0＋考點 1（三角比/弧度）；考點 2–7 與 Part 2/3 待補。
"""

SVG_RIGHT_TRI = """<svg viewBox="0 0 250 165" width="250" height="165" xmlns="http://www.w3.org/2000/svg" font-family="'Microsoft JhengHei',system-ui,sans-serif">
<polygon points="35,135 215,135 215,40" fill="#fdeef2" stroke="#8c2740" stroke-width="2.5"/>
<path d="M215,118 L198,118 L198,135" fill="none" stroke="#8c2740" stroke-width="1.6"/>
<path d="M72,135 A37,37 0 0 0 68,118" fill="none" stroke="#b03a5b" stroke-width="2"/>
<text x="79" y="129" fill="#b03a5b" font-size="15">θ</text>
<text x="24" y="152" font-size="13" fill="#2b2b2b">A</text>
<text x="219" y="152" font-size="13" fill="#2b2b2b">C</text>
<text x="221" y="44" font-size="13" fill="#2b2b2b">B</text>
<text x="110" y="153" font-size="13.5" fill="#1f6f78">鄰邊</text>
<text x="223" y="93" font-size="13.5" fill="#1f6f78">對邊</text>
<text x="110" y="80" font-size="13.5" fill="#1f6f78">斜邊</text>
</svg>"""

SVG_GEN_ANGLE = """<svg viewBox="0 0 240 200" width="240" height="200" xmlns="http://www.w3.org/2000/svg" font-family="'Microsoft JhengHei',system-ui,sans-serif">
<line x1="15" y1="108" x2="225" y2="108" stroke="#aaa" stroke-width="1.2"/>
<line x1="115" y1="14" x2="115" y2="196" stroke="#aaa" stroke-width="1.2"/>
<text x="228" y="112" font-size="12" fill="#888">x</text>
<text x="118" y="16" font-size="12" fill="#888">y</text>
<circle cx="115" cy="108" r="76" fill="none" stroke="#c9b3bb" stroke-width="1.5"/>
<line x1="115" y1="108" x2="57" y2="59" stroke="#8c2740" stroke-width="2.3"/>
<line x1="57" y1="59" x2="57" y2="108" stroke="#1f6f78" stroke-width="1.6" stroke-dasharray="4 3"/>
<line x1="115" y1="108" x2="57" y2="108" stroke="#1f6f78" stroke-width="3"/>
<path d="M150,108 A35,35 0 0 0 90,86" fill="none" stroke="#b03a5b" stroke-width="2"/>
<text x="128" y="100" fill="#b03a5b" font-size="14">θ</text>
<circle cx="57" cy="59" r="3.5" fill="#8c2740"/>
<text x="14" y="50" font-size="12.5" fill="#8c2740">P(cos θ, sin θ)</text>
<text x="30" y="88" font-size="12.5" fill="#1f6f78">sin θ</text>
<text x="70" y="124" font-size="12.5" fill="#1f6f78">cos θ</text>
<text x="150" y="44" font-size="11.5" fill="#9a857c">Ⅰ 全＋</text>
<text x="20" y="44" font-size="11.5" fill="#9a857c">Ⅱ sin＋</text>
<text x="20" y="180" font-size="11.5" fill="#9a857c">Ⅲ tan＋</text>
<text x="150" y="180" font-size="11.5" fill="#9a857c">Ⅳ cos＋</text>
</svg>"""

UNIT = {
    "slug": "trig",
    "file": "115學測數學_三角_互動學習.html",
    "page_title": "115 學測數學 · 三角 · 互動學習",
    "emoji": "📐",
    "title": "三角",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 七大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "七大考點",
    "foot": "115 學測數學 · 三角 · 互動學習講義",

    "part0": {
        "heading": "為什麼三角是必爭的命題主戰場",
        "trend_table": {
            "years": [106, 107, 108, 109, 110, 111, 112, 113, 114, 115],
            "counts": ["2.5", "4.0", "2.5", "3.5", "3.25", "4.0", "3.0", "2.8", "3.5", "1.5"],
            "total": "30.6",
        },
        "notes": [
            r"**題數之冠**：\(106\)–\(115\) 合計 \(30.6\) 題，是命題主戰場；幾何群（三角＋向量＋直線圓＋空間）在數 A 各年約佔五成。",
            r"**正弦／餘弦定理幾乎年年考**；三角函數圖形（疊合、對稱）與和差倍角是 **★★★ 必考核心**。",
            r"**魔王題常出在這裡**：\(114\) 選17（餘弦定理＋半角＋外接圓）、\(115\) 選17（角平分線＋倍角）都是壓軸難題。",
            r"**最愛跨單元整合**：常與平面向量、直線與圓、空間幾何合成混合題組（手寫 18–20）。",
        ],
        "map": r"七大考點：① 三角比、弧度與廣義角 ② 正弦／餘弦定理 ③ 三角測量與幾何應用 ④ 三角函數圖形（週期、對稱、疊合）⑤ 和差角／倍角（解方程與不等式）⑥ 三角形面積、相似與角平分線 ⑦ 圓周角與二面角中的三角。",
    },

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "三角比、弧度與廣義角",
            "title": r"三角比、弧度與廣義角",
            "intro": r"從直角三角形的 \(\sin/\cos/\tan\) 出發，推廣到廣義角與弧度。重點在 **特殊角的值**、**弧度↔角度換算**，以及廣義角看象限定正負。",
            "points": [
                {"svg": SVG_RIGHT_TRI, "caption": r"直角三角形：\(\theta\) 的對邊、鄰邊與斜邊"},
                {"label": r"直角三角形定義", "lines": [
                    r"\(\sin\theta=\) 【\(\dfrac{對邊}{斜邊}\)】、\(\cos\theta=\) 【\(\dfrac{鄰邊}{斜邊}\)】、\(\tan\theta=\) 【\(\dfrac{對邊}{鄰邊}\)】。"]},
                {"label": r"三大關係", "lines": [
                    r"**平方關係**：\(\sin^2\theta+\cos^2\theta=\) 【\(1\)】、\(1+\tan^2\theta=\) 【\(\sec^2\theta\)】、\(1+\cot^2\theta=\) 【\(\csc^2\theta\)】；",
                    r"**商數關係**：\(\tan\theta=\) 【\(\dfrac{\sin\theta}{\cos\theta}\)】；",
                    r"**倒數關係**：\(\csc\theta=\dfrac{1}{\sin\theta}\)、\(\sec\theta=\dfrac{1}{\cos\theta}\)、\(\cot\theta=\) 【\(\dfrac{1}{\tan\theta}\)】。"]},
                {"label": r"特殊角與餘角", "lines": [
                    r"\(\sin30°=\) 【\(\dfrac12\)】、\(\sin45°=\) 【\(\dfrac{\sqrt2}{2}\)】、\(\sin60°=\) 【\(\dfrac{\sqrt3}{2}\)】；",
                    r"餘角關係：\(\cos\theta=\) 【\(\sin(90°-\theta)\)】（\(\cos\) 是「餘」弦）。"]},
                {"label": r"弧度與角度換算", "lines": [
                    r"\(180°=\) 【\(\pi\)】 弧度；角度 \(\times\dfrac{\pi}{180}=\) 弧度；",
                    r"[[小心 \(x°\) 與 \(x\)||\(\cos x°\) 是「\(x\) 度」（要先乘 \(\pi/180\) 化弧度）；\(\cos x\) 是「\(x\) 弧度」。例如 \(x=2\) 時，\(\cos2°\approx0.999\) 但 \(\cos2\,(弧度)\approx-0.416\)，差很多！]]：\(\cos x°\) 與 \(\cos x\) 是 **兩回事**。"]},
                {"svg": SVG_GEN_ANGLE, "caption": r"廣義角：**值** 看與 \(x\) 軸的夾角、**正負** 看象限"},
                {"label": r"廣義角", "lines": [
                    r"終邊上取點 \((x,y)\)、到原點距離 \(r\)：\(\sin\theta=\dfrac yr\)、\(\cos\theta=\dfrac xr\)、\(\tan\theta=\dfrac yx\)；",
                    r"**值看與 \(x\) 軸的夾角**（參考角）、**正負看象限**（[[ASTC||第一象限 **A**ll 全正；第二象限只有 **S**in 正；第三象限只有 **T**an 正；第四象限只有 **C**os 正。]]）；",
                    r"補角：\(\sin(180°-\theta)=\) 【\(\sin\theta\)】、\(\cos(180°-\theta)=\) 【\(-\cos\theta\)】。"]},
                {"label": r"弧長與扇形面積", "lines": [
                    r"半徑 \(r\)、圓心角 \(\theta\)（**弧度**）：弧長 \(=\) 【\(r\theta\)】、扇形面積 \(=\) 【\(\dfrac12 r^2\theta\)】。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(\cos x°\) 和 \(\cos x\)（弧度）一樣", "right": r"\(x°\) 要先乘 \(\pi/180\) 化弧度，兩者不同"},
                {"wrong": r"\(\sin(180°-\theta)=-\sin\theta\)", "right": r"\(=\sin\theta\)（補角的 sin 不變號）"},
                {"wrong": r"弧長 ＝ \(r\theta\) 的 \(\theta\) 用角度代入", "right": r"\(\theta\) 必須用 **弧度**"},
            ],
            "questions": [
                {"tag": "109 舊制 · 單選 1", "level": "★☆☆（易）", "core": "三角比的定義與比大小",
                 "body": r"已知兩個直角三角形三邊長分別為 \(3,4,5\) 與 \(5,12,13\)，\(\alpha\)、\(\beta\) 分別為它們的一角，其中 \(\alpha\) 的對邊為 \(3\)、\(\beta\) 的對邊為 \(5\)。試比較 \(\sin\alpha\)、\(\sin30°\)、\(\sin\beta\) 的大小。",
                 "options": [r"\(\sin\alpha\gt\sin\beta\gt\sin30°\)", r"\(\sin\alpha\gt\sin30°\gt\sin\beta\)", r"\(\sin\beta\gt\sin\alpha\gt\sin30°\)", r"\(\sin\beta\gt\sin30°\gt\sin\alpha\)", r"\(\sin30°\gt\sin\alpha\gt\sin\beta\)"],
                 "solution": {"brief": r"(2)",
                              "steps": [r"\(\sin\alpha=\dfrac35=0.6\)、\(\sin\beta=\dfrac{5}{13}\approx0.385\)、\(\sin30°=0.5\)。",
                                        r"故 \(\sin\alpha\,(0.6)\gt\sin30°\,(0.5)\gt\sin\beta\,(0.385)\)，選 (2)。"]}},
            ],
            "strategy": [
                r"特殊角 \(30°/45°/60°\) 的值要背熟；比大小時化成小數最直覺。",
                r"遇到 \(x°\) 與 \(x\) 弧度，**先統一單位** 再比較或計算。",
                r"廣義角先用 ASTC 判象限定正負，再用補角／餘角化簡到銳角。",
            ],
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "正弦定理、餘弦定理",
            "title": r"正弦定理與餘弦定理",
            "intro": r"已知三角形的部分邊角，求其餘。**看題目給什麼選工具**：給兩角一邊用正弦定理；給兩邊夾角或三邊用餘弦定理。這是三角 **★★★ 必考核心**，幾乎年年出現。",
            "points": [
                {"label": r"正弦定理", "lines": [
                    r"\(\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=\) 【\(2R\)】（\(R\) 為外接圓半徑）；",
                    r"適用：已知 **兩角一邊**，或 **兩邊一對角**（SSA，注意可能兩解）。"]},
                {"label": r"餘弦定理", "lines": [
                    r"\(c^2=\) 【\(a^2+b^2-2ab\cos C\)】（\(C\) 是 \(a,b\) 的夾角）；",
                    r"\(\cos C=\) 【\(\dfrac{a^2+b^2-c^2}{2ab}\)】；",
                    r"適用：已知 **兩邊夾角**（SAS 求第三邊）或 **三邊**（SSS 求角）。"]},
                {"label": r"三角形面積（多種寫法）", "lines": [
                    r"\(\triangle=\) 【\(\dfrac12\times底\times高\)】（最基本）；",
                    r"\(\phantom{\triangle}=\) 【\(\dfrac12 ab\sin C\)】（兩邊夾角，**正弦**）；",
                    r"\(\phantom{\triangle}=\) 【\(\dfrac{abc}{4R}\)】（\(R\)＝外接圓半徑）；",
                    r"\(\phantom{\triangle}=\) 【\(rs\)】（\(r\)＝內切圓半徑，\(s=\dfrac{a+b+c}{2}\) 半周長）；",
                    r"\(\phantom{\triangle}=\) 【\(\sqrt{s(s-a)(s-b)(s-c)}\)】（**海龍公式**）；",
                    r"\(\phantom{\triangle}=\) 【\(\dfrac12\sqrt{|\overrightarrow{AB}|^2|\overrightarrow{AC}|^2-(\overrightarrow{AB}\cdot\overrightarrow{AC})^2}\)】（**向量**內積）；",
                    r"\(\phantom{\triangle}=\) 【\(\dfrac12\,|x_1y_2-x_2y_1|\)】（平面，**行列式**）；",
                    r"\(\phantom{\triangle}=\) 【\(\dfrac12|\overrightarrow{AB}\times\overrightarrow{AC}|\)】（空間，**外積**）。"]},
                {"label": r"SSA 的兩解判定", "lines": [
                    r"已知角 \(A\) 與其對邊 \(a\)、另一邊 \(b\)：[[對邊較大則唯一||已知角 \(A\) 的「對邊」\(a\) 與「鄰邊」\(b\)。若 \(a\ge b\)（對邊不小於鄰邊），三角形唯一；若 \(a\lt b\)，視高 \(b\sin A\) 與 \(a\) 的關係可能 0、1 或 2 個三角形。]] \(a\ge b\) 時唯一；\(a\lt b\) 時可能 **兩解**，要小心。"]},
            ],
            "misconceptions": [
                {"wrong": r"已知兩邊一對角一定能唯一決定三角形", "right": r"SSA 可能有兩解（要判定對邊與鄰邊大小）"},
                {"wrong": r"\(c^2=a^2+b^2-2ab\cos C\) 的 \(C\) 可取任一角", "right": r"\(C\) 必須是 \(a,b\) 的 **夾角**（\(c\) 的對角）"},
                {"wrong": r"面積 \(=\dfrac12 ab\sin C\) 的 \(C\) 隨便取一角", "right": r"\(C\) 是 \(a,b\) 兩邊的 **夾角**"},
            ],
            "questions": [
                {"tag": "110 舊制 · 多選 10", "level": "★★★（難）", "core": "SSA 的唯一性、面積、外接圓",
                 "body": r"在 \(\triangle ABC\) 中，已知 \(AB=4\)、\(AC=6\)，此時尚不足以確定 \(\triangle ABC\) 的形狀與大小。但只要再知道某些條件，就可確定唯一的 \(\triangle ABC\)。試選出正確的選項。",
                 "options": [r"再知道 \(\cos A\) 的值", r"再知道 \(\cos B\) 的值", r"再知道 \(\cos C\) 的值", r"再知道 \(\triangle ABC\) 的面積", r"再知道 \(\triangle ABC\) 的外接圓半徑"],
                 "solution": {"brief": r"(1)(2)(5)",
                              "steps": [r"(1)○：\(A\) 是 \(AB,AC\) 的 **夾角**，屬 SAS → 唯一。",
                                        r"(2)○：角 \(B\) 的對邊為 \(AC=6\)、鄰邊 \(AB=4\)，對邊較大（\(6\gt4\)）→ SSA 唯一。",
                                        r"(3)✗：角 \(C\) 的對邊 \(AB=4\) 比鄰邊 \(AC=6\) 小 → SSA 可能 **兩解**，不唯一。",
                                        r"(4)✗：面積 \(=\dfrac12\cdot4\cdot6\sin A=12\sin A\)，知道面積只得 \(\sin A\)，\(A\) 可銳可鈍 → 不唯一。",
                                        r"(5)○：由正弦定理，外接圓半徑 \(R\) 與兩定邊一起可定出各角與第三邊（官方答案 (1)(2)(5)）。"]}},
                {"tag": "觀念範例（餘弦定理）", "level": "★☆☆（暖身）", "core": "兩邊夾角求第三邊",
                 "body": r"\(\triangle ABC\) 中，\(AB=5\)、\(AC=8\)、\(\angle A=60°\)，求 \(BC\)。",
                 "solution": {"brief": r"\(BC=7\)",
                              "steps": [r"由餘弦定理 \(BC^2=AB^2+AC^2-2\cdot AB\cdot AC\cos A=25+64-2\cdot5\cdot8\cdot\dfrac12=89-40=49\)，故 \(BC=7\)。"]}},
            ],
            "strategy": [
                r"先看 **給了什麼**：兩角一邊 → 正弦定理；兩邊夾角或三邊 → 餘弦定理。",
                r"SSA（兩邊一對角）務必判 **對邊 vs 鄰邊** 大小，小心兩解。",
                r"求面積優先用 \(\dfrac12 ab\sin C\)（兩邊夾角）；給三邊才用海龍。",
            ],
        },
    ],
}
