# -*- coding: utf-8 -*-
r"""三角單元 · 單一來源內容。

歷年題數之冠（106–115 合計 30.6 題），命題主戰場。例題以官方原卷校正。
※ 本檔目前含 Part 0＋考點 1（三角比/弧度）；考點 2–7 與 Part 2/3 待補。
"""

import soil_maps  # Part 0 單元知識地圖（SOIL 章節圖）

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

SVG_GEN_ANGLE = """<svg viewBox="0 0 264 210" width="264" height="210" xmlns="http://www.w3.org/2000/svg" font-family="'Microsoft JhengHei',system-ui,sans-serif">
<line x1="12" y1="122" x2="248" y2="122" stroke="#9aa6b2" stroke-width="1.2"/>
<line x1="100" y1="16" x2="100" y2="202" stroke="#9aa6b2" stroke-width="1.2"/>
<text x="251" y="126" font-size="12" fill="#888">x</text>
<text x="104" y="18" font-size="12" fill="#888">y</text>
<circle cx="100" cy="122" r="80" fill="none" stroke="#c9b3bb" stroke-width="1.6"/>
<line x1="100" y1="122" x2="149.3" y2="122" stroke="#1f6f78" stroke-width="3"/>
<line x1="149.3" y1="122" x2="149.3" y2="59.0" stroke="#1f6f78" stroke-width="1.8" stroke-dasharray="4 3"/>
<polyline points="140.3,122 140.3,113 149.3,113" fill="none" stroke="#1f6f78" stroke-width="1.1"/>
<line x1="100" y1="122" x2="149.3" y2="59.0" stroke="#8c2740" stroke-width="2.3"/>
<path d="M128.0,122.0 A28 28 0 0 0 117.2,99.9" fill="none" stroke="#b03a5b" stroke-width="2"/>
<text x="133" y="113" font-size="14" fill="#b03a5b">θ</text>
<circle cx="149.3" cy="59.0" r="3.6" fill="#8c2740"/>
<text x="156.3" y="56.0" font-size="12.5" fill="#8c2740" font-weight="bold">P (cos θ, sin θ)</text>
<text x="111.6" y="87.5" font-size="12.5" fill="#8c2740" font-style="italic">1</text>
<text x="124.6" y="138" font-size="12.5" fill="#1f6f78" text-anchor="middle">cos θ</text>
<text x="154.3" y="94.5" font-size="12.5" fill="#1f6f78">sin θ</text>
<text x="87" y="137" font-size="11.5" fill="#2b2b2b">O</text>
</svg>"""

# 三個相似直角三角形：基本 → 底邊÷cosθ → 高÷sinθ（呈現 tan 與倒數關係）
_TF = "font-family=\"'Microsoft JhengHei',system-ui,sans-serif\""

def _trirel_fig():
    BLUE = "#34679a"; ROSE = "#b03a5b"; GRN = "#1f6f78"
    L = [f'<svg viewBox="0 0 366 134" width="366" height="134" xmlns="http://www.w3.org/2000/svg" role="img" {_TF}>']
    def tri(p, adj_l, opp_l, hyp_l):
        Ax, Ay = p+14, 100; Bx, By = p+94, 100; Cx, Cy = p+94, 44
        g = [f'<polygon points="{Ax},{Ay} {Bx},{By} {Cx},{Cy}" fill="#eef4f8" stroke="{BLUE}" stroke-width="2"/>']
        g.append(f'<path d="M{Bx},{By-16} L{Bx-16},{By-16} L{Bx-16},{By}" fill="none" stroke="{BLUE}" stroke-width="1.2"/>')
        g.append(f'<path d="M{Ax+22},{Ay} A22 22 0 0 0 {Ax+18},{Ay-11}" fill="none" stroke="{ROSE}" stroke-width="1.6"/>')
        g.append(f'<text x="{Ax+24}" y="{Ay-3}" font-size="11" fill="{ROSE}">θ</text>')
        g.append(f'<text x="{(Ax+Bx)/2}" y="{Ay+15}" font-size="11" fill="{GRN}" text-anchor="middle">{adj_l}</text>')
        g.append(f'<text x="{Bx+4}" y="{(By+Cy)/2+4}" font-size="11" fill="{GRN}">{opp_l}</text>')
        g.append(f'<text x="{(Ax+Cx)/2-16}" y="{(Ay+Cy)/2-2}" font-size="11" fill="{ROSE}" text-anchor="end" font-weight="bold">{hyp_l}</text>')
        return "".join(g)
    L.append(tri(0,   'cos θ', 'sin θ', '1'))
    L.append(tri(122, '1', 'tan θ', '1/cos θ'))
    L.append(tri(244, '1/tan θ', '1', '1/sin θ'))
    L.append('<text x="61" y="128" font-size="9.5" fill="#5a4a52" text-anchor="middle">基本（÷ 1）</text>')
    L.append('<text x="183" y="128" font-size="9.5" fill="#5a4a52" text-anchor="middle">底邊 ÷ cos θ</text>')
    L.append('<text x="305" y="128" font-size="9.5" fill="#5a4a52" text-anchor="middle">高 ÷ sin θ</text>')
    L.append('</svg>')
    return "".join(L)

SVG_TRIREL = _trirel_fig()

def _sinelaw_fig():
    import math
    INK="#2c3e50"; BLUE="#3a6ea5"; ROSE="#b03a5b"; MAROON="#8c2740"
    Ox,Oy,R=112,100,72
    A=(136.6,32.3); B=(41.1,112.5); C=(167.2,146.3)
    D=(2*Ox-B[0], 2*Oy-B[1])   # B 的對徑點（BD 為直徑＝2R）
    def u(p,q):
        dx,dy=q[0]-p[0],q[1]-p[1]; ln=math.hypot(dx,dy); return (dx/ln,dy/ln)
    L=[f'<svg viewBox="0 0 244 200" width="244" height="200" xmlns="http://www.w3.org/2000/svg" role="img" {_TF}>']
    L.append(f'<circle cx="{Ox}" cy="{Oy}" r="{R}" fill="none" stroke="{BLUE}" stroke-width="1.6"/>')
    L.append(f'<polygon points="{A[0]},{A[1]} {B[0]},{B[1]} {C[0]},{C[1]}" fill="#eef4f8" fill-opacity="0.6" stroke="{INK}" stroke-width="1.8"/>')
    L.append(f'<line x1="{B[0]}" y1="{B[1]}" x2="{D[0]:.1f}" y2="{D[1]:.1f}" stroke="{MAROON}" stroke-width="2.2"/>')
    L.append(f'<line x1="{C[0]}" y1="{C[1]}" x2="{D[0]:.1f}" y2="{D[1]:.1f}" stroke="#9aa6b2" stroke-width="1.4" stroke-dasharray="4 3"/>')
    cb=u(C,B); cd=u(C,D); p1=(C[0]+9*cb[0],C[1]+9*cb[1]); cor=(C[0]+9*cb[0]+9*cd[0],C[1]+9*cb[1]+9*cd[1]); p2=(C[0]+9*cd[0],C[1]+9*cd[1])
    L.append(f'<polyline points="{p1[0]:.1f},{p1[1]:.1f} {cor[0]:.1f},{cor[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{INK}" stroke-width="1"/>')
    db=u(D,B); dc=u(D,C); a1=(D[0]+17*db[0],D[1]+17*db[1]); a2=(D[0]+17*dc[0],D[1]+17*dc[1])
    L.append(f'<path d="M{a1[0]:.1f},{a1[1]:.1f} A17 17 0 0 1 {a2[0]:.1f},{a2[1]:.1f}" fill="none" stroke="{ROSE}" stroke-width="1.6"/>')
    L.append(f'<circle cx="{Ox}" cy="{Oy}" r="2.4" fill="{INK}"/>')
    L.append(f'<g font-size="12.5" font-weight="bold" font-style="italic">'
             f'<text x="132" y="28" fill="{INK}" text-anchor="middle">A</text>'
             f'<text x="30" y="116" fill="{INK}" text-anchor="middle">B</text>'
             f'<text x="172" y="158" fill="{INK}" text-anchor="middle">C</text>'
             f'<text x="{D[0]+6:.0f}" y="{D[1]-3:.0f}" fill="{MAROON}" text-anchor="middle">D</text></g>')
    L.append(f'<g font-size="12" font-weight="bold" font-style="italic" fill="{ROSE}">'
             f'<text x="96" y="138" text-anchor="middle">a</text>'
             f'<text x="158" y="86" text-anchor="middle">b</text>'
             f'<text x="78" y="70" text-anchor="middle">c</text></g>')
    L.append(f'<text x="108" y="90" font-size="11.5" font-weight="bold" fill="{MAROON}">2R</text>')
    L.append(f'<text x="166" y="104" font-size="11" fill="{ROSE}">A</text>')
    L.append(f'<text x="120" y="194" font-size="10" fill="#5a4a52" text-anchor="middle">∠D ＝ ∠A ⇒ a ＝ 2R·sinA</text>')
    L.append('</svg>')
    return "".join(L)

SVG_SINELAW = _sinelaw_fig()

UNIT = {
    "slug": "trig",
    "file": "115學測數學_三角.html",
    "page_title": "115 學測數學 · 三角",
    "emoji": "📐",
    "title": "三角",
    "exam_tag": "115 學測",
    "hero_sub": "Part 1 七大考點 ｜ Part 2 模擬實戰 ｜ Part 3 考前速查",
    "hero_sub2": "每個考點皆含：重點與公式 · 常見誤解 · 歷屆試題 · 解題策略",
    "part1_label": "七大考點",
    "foot": "115 學測數學 · 三角 · 學測數學重點整理",

    "part0": {
        "opener": {"svg": soil_maps.SLIDES["trig"], "hero": True,
                   "caption": r"**單元知識地圖**：先備 → 各考點（★越多＝越常考） → 跨單元最愛綁考 → 帶走一句話"},
        # B1 直覺挑戰（老師定案 T2）：波峰不同時發生 → 疊合
        "challenge": {
            "q": r"\(\sin x+\cos x\) 的最大值是多少？",
            "options": [r"\(2\)", r"\(\sqrt2\)（\(\approx1.41\)）", r"\(1.5\)", r"\(1\)"],
            "answer": 1,
            "reveal": r"直覺說 \(1+1=2\)，但兩個波的最高點 **不同時發生**——錯開的兩波合成一個新波，振幅是 \(\sqrt{1^2+1^2}=\sqrt2\)。這就是考點 4 的「疊合」。",
            "kp": "kp4",
        },
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

    "mixed": [
        {
            "src": "111 學測數A · 第 18–20 題組（大考中心原卷 · 官方評分原則）",
            "context": r"坐標平面上有一環狀區域，由圓 \(x^2+y^2=3\) 的外部與圓 \(x^2+y^2=4\) 的內部交集而成。某甲用一支長 \(1\) 的掃描棒掃描此環狀區域在 \(x\) 軸上方的區域 \(R\)：棒的黑、白兩端分別在半圓 \(C_1:x^2+y^2=3\ (y\ge0)\)、\(C_2:x^2+y^2=4\ (y\ge0)\) 上移動。開始時黑端在 \(A(\sqrt3,0)\)、白端在 \(C_2\) 上的點 \(B\)；接著兩端各沿 \(C_1,C_2\) 逆時針移動，直到白端碰到 \(C_2\) 的點 \(B'(-2,0)\) 停止（此時黑端在 \(A'\)）。",
            "items": [
                {"tag": "第 18 題 · 單選 · 3 分",
                 "q": r"試問點 \(B\) 的坐標為下列哪一選項？",
                 "options": [r"\((0,2)\)", r"\((1,\sqrt3)\)", r"\((\sqrt2,\sqrt2)\)", r"\((\sqrt3,1)\)", r"\((2,0)\)"],
                 "answer": r"**(4) \((\sqrt3,1)\)**。\(B\) 在 \(C_2\)（\(x^2+y^2=4\)）且 \(\overline{AB}=1\)、\(A=(\sqrt3,0)\)。由 \((x-\sqrt3)^2+y^2=1\) 與 \(x^2+y^2=4\) 相減得 \(x=\sqrt3\)，代回得 \(y=1\)，故 \(B=(\sqrt3,1)\)。"},
                {"tag": "第 19 題 · 非選 · 6 分",
                 "q": r"令 \(O\) 為原點。試在圖上標示掃描棒掃過的區域 \(R\)，並求 \(\cos\angle OA'B'\) 及點 \(A'\) 的極坐標。",
                 "answer": r"\(A'\) 在 \(C_1\)（\(x^2+y^2=3\)）且 \(\overline{A'B'}=1\)、\(B'=(-2,0)\)：由 \((x+2)^2+y^2=1\) 與 \(x^2+y^2=3\) 相減得 \(x=-\dfrac32,\ y=\dfrac{\sqrt3}{2}\)，故 \(A'=\left(-\dfrac32,\dfrac{\sqrt3}{2}\right)\)。\(\overrightarrow{A'O}\cdot\overrightarrow{A'B'}=\left(\dfrac32,-\dfrac{\sqrt3}{2}\right)\cdot\left(-\dfrac12,-\dfrac{\sqrt3}{2}\right)=-\dfrac34+\dfrac34=0\)，故 \(\cos\angle OA'B'=0\)（\(\angle OA'B'\) 為直角）。又 \(\overline{OA'}=\sqrt3\)、\(\angle AOA'=150^\circ\)，故 \(A'\) 的極坐標為 \((\sqrt3,\,150^\circ)\)（即 \(\left(\sqrt3,\dfrac{5\pi}{6}\right)\)）。",
                 "rubric": {"full": [r"求得 \(\cos\angle OA'B'=0\)（\(\angle OA'B'\) 為直角）。",
                                     r"求得 \(A'\) 的極坐標 \((\sqrt3,150^\circ)\)（即 \(\left(\sqrt3,\tfrac{5\pi}{6}\right)\)）。"],
                            "partial": r"畫出區域 \(R\)，但 \(\cos\angle OA'B'\) 或 \(A'\) 極坐標僅部分正確。",
                            "zero": r"未作答，或未符合部分給分原則。"}},
                {"tag": "第 20 題 · 非選 · 6 分",
                 "q": r"令 \(\Omega\) 表示掃描棒在第一象限所掃過的區域。試分別求 \(\Omega\) 與 \(R\) 的面積。",
                 "answer": r"\(\Omega\) 面積 ＝ 扇形 \(OBE\) ＋ \(\triangle OAB\) － 扇形 \(OAD\) ＝ \(\dfrac12\cdot\dfrac\pi3\cdot2^2+\dfrac12\cdot\sqrt3\cdot1-\dfrac12\cdot\dfrac\pi2\cdot(\sqrt3)^2=\dfrac{2\pi}{3}+\dfrac{\sqrt3}{2}-\dfrac{3\pi}{4}=\dfrac{\sqrt3}{2}-\dfrac{\pi}{12}\)。整個掃過區域 \(R\) 的面積 \(=\dfrac{5\pi}{12}\)。",
                 "rubric": {"full": [r"求得 \(\Omega\) 的面積 \(=\dfrac{\sqrt3}{2}-\dfrac{\pi}{12}\)。",
                                     r"求得 \(R\) 的面積 \(=\dfrac{5\pi}{12}\)。"],
                            "partial": r"\(\Omega\) 或 \(R\) 其中之一的面積正確、或過程部分正確。",
                            "zero": r"未作答，或未符合部分給分原則。"}},
            ],
        },
        {
            "src": "112 學測數A · 第 18–20 題組（大考中心原卷 · 官方評分原則）",
            "context": r"坐標平面上 \(O\) 為原點，給定 \(A(1,0)\)、\(B(-2,0)\)。另有兩點 \(P,Q\) 在上半平面，且滿足 \(\overline{AP}=\overline{OA}\)、\(\overline{BQ}=\overline{OB}\)、\(\angle POQ\) 為直角。令 \(\angle AOP=\theta\)。",
            "items": [
                {"tag": "第 18 題 · 單選 · 3 分",
                 "q": r"線段 \(\overline{OP}\) 長為下列哪一選項？",
                 "options": [r"\(\sin\theta\)", r"\(\cos\theta\)", r"\(2\sin\theta\)", r"\(2\cos\theta\)", r"\(\cos2\theta\)"],
                 "answer": r"**(4) \(2\cos\theta\)**。因 \(\overline{AP}=\overline{OA}=1\)，\(\triangle OAP\) 為等腰三角形，底角 \(\angle AOP=\angle APO=\theta\)、頂角 \(\angle OAP=\pi-2\theta\)。由正弦定理 \(\overline{OP}=\dfrac{\overline{OA}\cdot\sin(\pi-2\theta)}{\sin\theta}=\dfrac{\sin2\theta}{\sin\theta}=2\cos\theta\)。"},
                {"tag": "第 19 題 · 非選 · 6 分",
                 "q": r"若 \(\sin\theta=\dfrac35\)，試求點 \(Q\) 的坐標，並說明 \(\overline{BQ}=2\,\overline{AP}\)。",
                 "answer": r"由等腰關係 \(\overline{OA}=\overline{AP}\)、\(\overline{OB}=\overline{BQ}\) 可推得 \(\overrightarrow{AP}\parallel\overrightarrow{BQ}\)（同向），且 \(\overline{BQ}=\overline{OB}=2=2\,\overline{OA}=2\,\overline{AP}\)。又 \(\overrightarrow{BQ}\) 與 \(x\) 軸正向夾角為 \(2\theta\)、\(\overline{BQ}=2\)：由 \(\sin\theta=\tfrac35,\cos\theta=\tfrac45\) 得 \(\cos2\theta=\tfrac{7}{25},\ \sin2\theta=\tfrac{24}{25}\)，故 \(\overrightarrow{BQ}=2(\cos2\theta,\sin2\theta)=\left(\tfrac{14}{25},\tfrac{48}{25}\right)\)。因 \(B=(-2,0)\)，得 \(Q=\left(-\dfrac{36}{25},\,\dfrac{48}{25}\right)\)。",
                 "rubric": {"full": [r"正確推證 \(\overline{BQ}=2\,\overline{AP}\)，理由完整。",
                                     r"正確求得 \(Q=\left(-\dfrac{36}{25},\dfrac{48}{25}\right)\)。"],
                            "partial": r"上述兩項的解題過程部分正確。",
                            "zero": r"未作答，或未符合部分給分原則。"}},
                {"tag": "第 20 題 · 非選 · 6 分",
                 "q": r"承上，試求點 \(A\) 到直線 \(BQ\) 的距離，並求四邊形 \(PABQ\) 的面積。",
                 "answer": r"\(\overrightarrow{BQ}\) 與 \(x\) 軸夾角為 \(2\theta\)、\(\overline{AB}=3\)，故 \(A\) 到直線 \(BQ\) 的距離 \(=\overline{AB}\sin2\theta=3\cdot\dfrac{24}{25}=\dfrac{72}{25}\)。四邊形 \(PABQ\) 是以 \(\overline{AP}=1\)、\(\overline{BQ}=2\) 為兩平行邊的梯形，面積 \(=\dfrac12(\overline{AP}+\overline{BQ})\times\dfrac{72}{25}=\dfrac12(1+2)\cdot\dfrac{72}{25}=\dfrac{108}{25}\)。",
                 "rubric": {"full": [r"求得 \(A\) 到直線 \(BQ\) 的距離 \(=\dfrac{72}{25}\)。",
                                     r"求得四邊形 \(PABQ\) 的面積 \(=\dfrac{108}{25}\)。"],
                            "partial": r"距離或面積其中之一正確、或過程部分正確。",
                            "zero": r"未作答，或未符合部分給分原則。"}},
            ],
        },
    ],

    "kps": [
        {
            "num": "考點 1", "id": "kp1", "nav": "三角比、弧度與廣義角",
            "title": r"三角比、弧度與廣義角",
            "intro": r"**三角比就是直角三角形『邊的比例』**：角度固定，三角形放大縮小比值都一樣——對邊÷斜邊這個比值就叫 \(\sin\theta\)。\(\sin=\dfrac{對邊}{斜邊}\)、\(\cos=\dfrac{鄰邊}{斜邊}\)、\(\tan=\dfrac{對邊}{鄰邊}\)。把它從銳角推廣到任意角（廣義角：**值看與 \(x\) 軸的夾角、正負看象限**），再把角度量改用弧度，就是本考點。",
            "prereq": [
                r"**直角三角形**與**畢氏定理** \(a^2+b^2=c^2\)",
                r"**相似三角形**：對應邊成比例（三角比能成立的根本）",
                r"**坐標象限**：知道四象限裡 \(x\)、\(y\) 的正負",
            ],
            "points": [
                {"svg": SVG_RIGHT_TRI, "caption": r"直角三角形：\(\theta\) 的對邊、鄰邊與斜邊"},
                {"label": r"直角三角形定義", "lines": [
                    r"\(\sin\theta=\) 【\(\dfrac{對邊}{斜邊}\)】、\(\cos\theta=\) 【\(\dfrac{鄰邊}{斜邊}\)】、\(\tan\theta=\) 【\(\dfrac{對邊}{鄰邊}\)】。"]},
                {"label": r"平方與商數關係", "lines": [
                    r"**平方關係**：\(\sin^2\theta+\cos^2\theta=\) 【\(1\)】；",
                    r"**商數關係**：\(\tan\theta=\) 【\(\dfrac{\sin\theta}{\cos\theta}\)】。"]},
                {"svg": SVG_TRIREL, "wide": True, "caption": r"同一個角的相似直角三角形：底邊 \(\div\cos\theta\) 得 \(\tan\theta\)（商數關係）；斜邊隨之變 \(\tfrac1{\cos\theta}\)、\(\tfrac1{\sin\theta}\)"},
                {"label": r"特殊角與餘角", "lines": [
                    r"\(\sin30°=\) 【\(\dfrac12\)】、\(\sin45°=\) 【\(\dfrac{\sqrt2}{2}\)】、\(\sin60°=\) 【\(\dfrac{\sqrt3}{2}\)】；",
                    r"餘角關係：\(\cos\theta=\) 【\(\sin(90°-\theta)\)】（\(\cos\) 是「餘」弦）。"]},
                {"label": r"弧度與角度換算", "lines": [
                    r"\(180°=\) 【\(\pi\)】 弧度；角度 \(\times\dfrac{\pi}{180}=\) 弧度；",
                    r"[[小心 \(x°\) 與 \(x\)||\(\cos x°\) 是「\(x\) 度」（要先乘 \(\pi/180\) 化弧度）；\(\cos x\) 是「\(x\) 弧度」。例如 \(x=2\) 時，\(\cos2°\approx0.999\) 但 \(\cos2\,(弧度)\approx-0.416\)，差很多！]]：\(\cos x°\) 與 \(\cos x\) 是 **兩回事**。"]},
                {"svg": SVG_GEN_ANGLE, "caption": r"**廣義角的單位圓定義**：任一角 \(\theta\) 的終邊與單位圓（半徑 \(=1\)）交於 \(P\)，\(P\) 的坐標即 \((\cos\theta,\sin\theta)\)——\(\cos\theta\) 是橫坐標、\(\sin\theta\) 是縱坐標；正負看象限（ASTC）"},
                {"label": r"廣義角", "lines": [
                    r"終邊上取點 \((x,y)\)、到原點距離 \(r\)：\(\sin\theta=\dfrac yr\)、\(\cos\theta=\dfrac xr\)、\(\tan\theta=\dfrac yx\)；",
                    r"**值看與 \(x\) 軸的夾角**（參考角）、**正負看象限**（[[ASTC||第一象限 **A**ll 全正；第二象限只有 **S**in 正；第三象限只有 **T**an 正；第四象限只有 **C**os 正。]]）；",
                    r"補角：\(\sin(180°-\theta)=\) 【\(\sin\theta\)】、\(\cos(180°-\theta)=\) 【\(-\cos\theta\)】。"]},
                {"label": r"弧長與扇形面積", "lines": [
                    r"半徑 \(r\)、圓心角 \(\theta\)（**弧度**）：弧長 \(=\) 【\(r\theta\)】、扇形面積 \(=\) 【\(\dfrac12 r^2\theta\)】。"]},
            ],
            "tables": [
                {"title": r"特殊角三角函數值（必背 ★）",
                 "head": [r"\(\theta\)", r"\(0^\circ\)", r"\(30^\circ\)", r"\(45^\circ\)", r"\(60^\circ\)", r"\(90^\circ\)"],
                 "rows": [
                     [r"\(\sin\theta\)", r"\(0\)", r"\(\dfrac12\)", r"\(\dfrac{\sqrt2}{2}\)", r"\(\dfrac{\sqrt3}{2}\)", r"\(1\)"],
                     [r"\(\cos\theta\)", r"\(1\)", r"\(\dfrac{\sqrt3}{2}\)", r"\(\dfrac{\sqrt2}{2}\)", r"\(\dfrac12\)", r"\(0\)"],
                     [r"\(\tan\theta\)", r"\(0\)", r"\(\dfrac{\sqrt3}{3}\)", r"\(1\)", r"\(\sqrt3\)", r"不存在"],
                 ]},
            ],
            "misconceptions": [
                {"wrong": r"\(\cos x°\) 和 \(\cos x\)（弧度）一樣", "right": r"\(x°\) 要先乘 \(\pi/180\) 化弧度，兩者不同"},
                {"wrong": r"\(\sin(180°-\theta)=-\sin\theta\)", "right": r"\(=\sin\theta\)（補角的 sin 不變號）"},
                {"wrong": r"弧長 ＝ \(r\theta\) 的 \(\theta\) 用角度代入", "right": r"\(\theta\) 必須用 **弧度**"},
            ],
            "worked": {
                "q": r"直角三角形 \(\triangle ABC\)，\(\angle C=90°\)，三邊 \(BC=4\)、\(AC=3\)、\(AB=5\)。求 \(\angle B\) 的 \(\sin\)、\(\cos\)、\(\tan\)。",
                "steps": [
                    {"do": r"先認邊：對 \(\angle B\) 來說，對邊是 \(AC=3\)、鄰邊是 \(BC=4\)、斜邊是 \(AB=5\)。",
                     "why": r"「對邊」是角正前方那條、「斜邊」是直角對面最長那條、剩下一條是「鄰邊」。"},
                    {"do": r"\(\sin B=\dfrac{對邊}{斜邊}=\dfrac35\)、\(\cos B=\dfrac{鄰邊}{斜邊}=\dfrac45\)、\(\tan B=\dfrac{對邊}{鄰邊}=\dfrac34\)。",
                     "why": r"三個比值直接套定義即得。"},
                ],
            },
            "questions": [
                {"tag": "109 舊制 · 單選 1", "level": "★☆☆（易）", "core": "三角比的定義與比大小",
                 "body": r"已知兩個直角三角形三邊長分別為 \(3,4,5\) 與 \(5,12,13\)，\(\alpha\)、\(\beta\) 分別為它們的一角，其中 \(\alpha\) 的對邊為 \(3\)、\(\beta\) 的對邊為 \(5\)。試比較 \(\sin\alpha\)、\(\sin30°\)、\(\sin\beta\) 的大小。",
                 "options": [r"\(\sin\alpha\gt\sin\beta\gt\sin30°\)", r"\(\sin\alpha\gt\sin30°\gt\sin\beta\)", r"\(\sin\beta\gt\sin\alpha\gt\sin30°\)", r"\(\sin\beta\gt\sin30°\gt\sin\alpha\)", r"\(\sin30°\gt\sin\alpha\gt\sin\beta\)"],
                 "solution": {"brief": r"(2)",
                              "steps": [r"\(\sin\alpha=\dfrac35=0.6\)、\(\sin\beta=\dfrac{5}{13}\approx0.385\)、\(\sin30°=0.5\)。",
                                        r"故 \(\sin\alpha\,(0.6)\gt\sin30°\,(0.5)\gt\sin\beta\,(0.385)\)，選 (2)。"]}},
                {"tag": "112 數A · 單選 2", "level": "★★☆（中）", "core": "單位圓切線：用直角三角形讀 tan",
                 "body": r"以原點 \(O\) 為圓心、\(1\) 為半徑作圓，分別交坐標軸正向於 \(A、B\)。在第一象限的圓弧上取一點 \(C\) 作圓的切線，分別交兩軸於 \(D\)（\(x\) 軸）、\(E\)（\(y\) 軸）。令 \(\angle OEC=\theta\)，試選出等於 \(\tan\theta\) 的選項。",
                 "options": [r"\(\overline{OE}\)", r"\(\overline{OC}\)", r"\(\overline{OD}\)", r"\(\overline{CE}\)", r"\(\overline{CD}\)"],
                 "solution": {"brief": r"(5) \(\overline{CD}\)",
                              "steps": [
                                  r"切線在切點 \(C\) 與半徑 \(\overline{OC}\) 垂直，故 \(\triangle OCE\) 在 \(C\) 為直角，\(\overline{OC}=1\)。",
                                  r"\(\angle OEC=\theta\)：\(\tan\theta=\dfrac{\overline{OC}}{\overline{CE}}=\dfrac{1}{\overline{CE}}\)。設 \(C=(\cos\alpha,\sin\alpha)\)，可算 \(\overline{CE}=\dfrac{\cos\alpha}{\sin\alpha}=\cot\alpha\)、\(\overline{CD}=\dfrac{\sin\alpha}{\cos\alpha}=\tan\alpha\)。",
                                  r"故 \(\tan\theta=\dfrac{1}{\cot\alpha}=\tan\alpha=\overline{CD}\)，選 (5)。"]}},
            ],
            "selfcheck": {
                "q": r"\(\sin30^\circ+\cos60^\circ+\tan45^\circ\) 之值為何？",
                "a": r"**\(2\)**：\(\dfrac12+\dfrac12+1=2\)。"},
            "strategy": [
                r"特殊角 \(30°/45°/60°\) 的值要背熟；比大小時化成小數最直覺。",
                r"遇到 \(x°\) 與 \(x\) 弧度，**先統一單位** 再比較或計算。",
                r"廣義角先用 ASTC 判象限定正負，再用補角／餘角化簡到銳角。",
            ],
        },
        {
            "num": "考點 2", "id": "kp2", "nav": "正弦定理、餘弦定理",
            "title": r"正弦定理與餘弦定理",
            "intro": r"**餘弦定理其實是畢氏定理的『加強版』**：直角三角形 \(c^2=a^2+b^2\)；當夾角 \(C\) 不是直角，就多補一項 \(c^2=a^2+b^2-2ab\cos C\)（\(C=90°\) 時 \(\cos C=0\)，正好退回畢氏定理！）。正弦定理則把「邊」與「對角的 \(\sin\)」綁在一起。**看給什麼選工具**——把「已知＋要求的未知」一起數：**二邊二角**用正弦定理、**三邊一角**用餘弦定理。三角 **★★★ 必考核心**。",
            "prereq": [
                r"**畢氏定理** \(a^2+b^2=c^2\)（餘弦定理的根）",
                r"**特殊角的 \(\sin\)、\(\cos\) 值**（考點 1 的表）",
                r"**邊角記法**：邊 \(a\) 對角 \(A\)、\(b\) 對 \(B\)、\(c\) 對 \(C\)",
            ],
            "points": [
                {"label": r"正弦定理", "lines": [
                    r"\(\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=\) 【\(2R\)】（\(R\) 為外接圓半徑）；",
                    r"適用：已知 **兩角一邊**，或 **兩邊一對角**（SSA，注意可能兩解）。"]},
                {"svg": SVG_SINELAW, "wide": True, "caption": r"**正弦定理的靈魂＝直徑**：從 \(B\) 拉直徑 \(BD=2R\)，則 \(\angle BCD=90^\circ\)（半圓上圓周角）、\(\angle D=\angle A\)（同弧 \(BC\)），故 \(a=2R\sin A\)，即 \(\dfrac{a}{\sin A}=2R\)"},
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
            "worked": {
                "q": r"\(\triangle ABC\) 中 \(\angle A=30°\)、\(\angle B=45°\)、\(a=10\)（\(a\) 是 \(A\) 的對邊）。求 \(b\)。",
                "steps": [
                    {"do": r"已知 \(A\)、\(B\)、\(a\)，要求 \(b\)——數一數是「二邊二角」，用正弦定理 \(\dfrac{a}{\sin A}=\dfrac{b}{\sin B}\)。",
                     "why": r"把「已知＋未知」一起數＝二邊二角，正合正弦定理（它的式子剛好牽涉兩邊與兩角）。"},
                    {"do": r"\(\dfrac{10}{\sin30°}=\dfrac{b}{\sin45°}\)。",
                     "why": r"代入：\(a\) 對 \(A\)、\(b\) 對 \(B\)。"},
                    {"do": r"\(\dfrac{10}{1/2}=20=\dfrac{b}{\sqrt2/2}\Rightarrow b=20\times\dfrac{\sqrt2}{2}=10\sqrt2\)。",
                     "why": r"代特殊角 \(\sin30°=\dfrac12\)、\(\sin45°=\dfrac{\sqrt2}{2}\)，再解出 \(b\)。"},
                ],
            },
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
                {"tag": "111 數A · 多選 8", "level": "★★★（難）", "core": "坐標求邊長 → 正弦／餘弦定理、外接圓半徑",
                 "body": r"坐標平面上，\(\triangle ABC\) 三頂點為 \(A(0,2)、B(1,0)、C(4,1)\)。試選出正確的選項。",
                 "options": [
                     r"\(\triangle ABC\) 三邊中 \(\overline{AC}\) 最長",
                     r"\(\sin A<\sin C\)",
                     r"\(\triangle ABC\) 為銳角三角形",
                     r"\(\sin B=\dfrac{7\sqrt2}{10}\)",
                     r"\(\triangle ABC\) 的外接圓半徑比 \(2\) 小"],
                 "solution": {"brief": r"(1)(4)",
                              "steps": [
                                  r"三邊：\(\overline{AB}=\sqrt5\)、\(\overline{BC}=\sqrt{10}\)、\(\overline{AC}=\sqrt{17}\)。(1)○ \(\overline{AC}=\sqrt{17}\) 最長。",
                                  r"(2)✗ 正弦定理 \(\dfrac{\sin A}{\overline{BC}}=\dfrac{\sin C}{\overline{AB}}\Rightarrow\dfrac{\sin A}{\sin C}=\dfrac{\sqrt{10}}{\sqrt5}=\sqrt2>1\)，故 \(\sin A>\sin C\)。",
                                  r"(3)✗ 最長邊 \(\overline{AC}\) 對角 \(B\)：\(\cos B=\dfrac{5+10-17}{2\sqrt5\sqrt{10}}=\dfrac{-2}{2\sqrt{50}}<0\)，\(B\) 為鈍角。",
                                  r"(4)○ \(\cos B=-\dfrac{1}{\sqrt{50}}=-\dfrac{\sqrt2}{10}\Rightarrow\sin B=\sqrt{1-\dfrac{2}{100}}=\dfrac{\sqrt{98}}{10}=\dfrac{7\sqrt2}{10}\)。",
                                  r"(5)✗ \(2R=\dfrac{\overline{AC}}{\sin B}=\dfrac{\sqrt{17}}{7\sqrt2/10}=\dfrac{10\sqrt{17}}{7\sqrt2}\Rightarrow R=\dfrac{5\sqrt{34}}{14}\approx2.08>2\)。故選 (1)(4)。"]}},
            ],
            "selfcheck": {
                "q": r"三角形中 \(a=7,\,b=5\)，夾角 \(C=60^\circ\)，求 \(c\)。",
                "a": r"**\(\sqrt{39}\)**：餘弦定理 \(c^2=49+25-2\cdot7\cdot5\cdot\frac12=39\)。"},
            "strategy": [
                r"先看 **給了什麼**：兩角一邊 → 正弦定理；兩邊夾角或三邊 → 餘弦定理。",
                r"SSA（兩邊一對角）務必判 **對邊 vs 鄰邊** 大小，小心兩解。",
                r"求面積優先用 \(\dfrac12 ab\sin C\)（兩邊夾角）；給三邊（好算的數）才用海龍。",
            ],
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "三角測量與幾何應用",
            "title": r"三角測量與平面幾何應用",
            "intro": r"**測量的精神：把『量不到的高與距離』換成『量得到的角度＋一段水平距離』**。看到塔頂仰角 \(30°\)、你離塔 \(100\) 公尺，塔高就是 \(100\tan30°\)——因為 \(\tan(仰角)=\dfrac{高}{水平距離}\)。再難的題也一樣：先**畫圖、標角度**，再用正弦／餘弦定理把缺的邊角補出來。另一招「大角對大邊」幫你比邊長。",
            "prereq": [
                r"**三角比** \(\tan=\dfrac{對邊}{鄰邊}\)（考點 1）",
                r"**正弦／餘弦定理**（考點 2）",
                r"**把文字情境畫成示意圖**的習慣",
            ],
            "points": [
                {"label": r"仰角與俯角", "lines": [
                    r"**仰角**：視線在水平線 **上方** 的夾角；**俯角**：視線在水平線 **下方** 的夾角；",
                    r"測高常用 \(\tan(仰角)=\) 【\(\dfrac{高}{水平距離}\)】。"]},
                {"label": r"方位角", "lines": [
                    r"從 **正北** 起順時針量；如 N30°E ＝ 北偏東 \(30°\)；",
                    r"測量題先 **畫圖標角度**，再用正弦／餘弦定理求邊或角。"]},
                {"label": r"大角對大邊", "lines": [
                    r"同一三角形中，大角對大邊、大邊對大角：\(\angle A\gt\angle B\Leftrightarrow\) 【\(a\gt b\)】；",
                    r"配合 \(\sin\) 在 \([0°,90°]\) **遞增**、\(\cos\) **遞減** 來比大小（鈍角另論）。"]},
                {"label": r"正射影（投影定理）", "lines": [
                    r"邊 \(b\) 在邊 \(c\) 上的正射影長 ＝ \(b\cos A\)；",
                    r"投影定理：\(a=\) 【\(b\cos C+c\cos B\)】。"]},
            ],
            "misconceptions": [
                {"wrong": r"仰角、俯角從鉛直線量起", "right": r"從 **水平線** 量起"},
                {"wrong": r"三角形中大角對小邊", "right": r"**大角對大邊**（大邊對大角）"},
                {"wrong": r"\(\sin\) 在 \(0°\)–\(180°\) 都遞增", "right": r"\(0°\)–\(90°\) 遞增、\(90°\)–\(180°\) 遞減（鈍角要小心）"},
            ],
            "worked": {
                "q": r"站在 \(60\) 公尺高的樓頂，看地面一輛車的**俯角**為 \(30°\)。車離大樓底部多遠？",
                "steps": [
                    {"do": r"畫圖：樓高 \(60\)（鉛直）、水平距離 \(d\)、視線俯角 \(30°\)，圍成直角三角形。",
                     "why": r"俯角從水平線往下量；先把情境畫成三角形再算。"},
                    {"do": r"\(\tan30°=\dfrac{高}{水平距離}=\dfrac{60}{d}\)。",
                     "why": r"仰角、俯角都滿足 \(\tan=\dfrac{高}{水平距離}\)。"},
                    {"do": r"\(d=\dfrac{60}{\tan30°}=\dfrac{60}{1/\sqrt3}=60\sqrt3\approx103.9\) 公尺。",
                     "why": r"\(\tan30°=\dfrac{1}{\sqrt3}\)，移項解出 \(d\)。"},
                ],
            },
            "questions": [
                {"tag": "108 舊制 · 多選 10", "level": "★★☆（中）", "core": "大角對大邊、sin／cos 的單調性",
                 "body": r"在 \(\triangle ABC\) 中，已知 \(50°\le\angle A\lt\angle B\le60°\)。試選出正確的選項。",
                 "options": [r"\(\sin A\lt\sin B\)", r"\(\sin B\lt\sin C\)", r"\(\cos A\lt\cos B\)", r"\(\sin C\lt\cos C\)", r"\(\overline{AB}\lt\overline{BC}\)"],
                 "solution": {"brief": r"(1)(2)",
                              "steps": [r"由 \(50°\le A\lt B\le60°\) 得 \(C=180°-A-B\in(60°,80°)\)，且 \(A\lt B\lt C\)（三角皆銳角）。",
                                        r"(1)○、(2)○：\(\sin\) 在 \([0°,90°]\) 遞增，\(A\lt B\lt C\Rightarrow\sin A\lt\sin B\lt\sin C\)。",
                                        r"(3)✗：\(\cos\) 遞減，\(A\lt B\Rightarrow\cos A\gt\cos B\)。(4)✗：\(C\gt45°\Rightarrow\sin C\gt\cos C\)。",
                                        r"(5)✗：\(A\) 最小 \(\Rightarrow\) 對邊 \(\overline{BC}=a\) 最短，\(C\) 最大 \(\Rightarrow\) 對邊 \(\overline{AB}=c\) 最長，故 \(\overline{AB}\gt\overline{BC}\)。"]}},
                {"tag": "觀念範例（三角測量）", "level": "★★☆（中）", "core": "仰角與正弦定理測高",
                 "body": r"在水平地面上 \(A\)、\(B\) 兩點相距 \(100\) 公尺，由 \(A\)、\(B\) 測得正前方塔頂的仰角分別為 \(30°\)、\(45°\)（塔在 \(B\) 的正前方、\(A\) 在 \(B\) 後方同一直線）。求塔高。",
                 "solution": {"brief": r"塔高 \(=50(\sqrt3+1)\) 公尺",
                              "steps": [r"設塔高 \(h\)、塔底到 \(B\) 的水平距離 \(d\)。由 \(B\)：\(\tan45°=\dfrac hd\Rightarrow d=h\)；由 \(A\)：\(\tan30°=\dfrac{h}{d+100}\)。",
                                        r"代入 \(\dfrac1{\sqrt3}=\dfrac{h}{h+100}\Rightarrow h+100=\sqrt3\,h\Rightarrow h=\dfrac{100}{\sqrt3-1}=50(\sqrt3+1)\approx136.6\) 公尺。"]}},
                {"tag": "113 數A · 單選 6", "level": "★★★（難）", "core": "三角測量：餘弦定理 ＋ 半角公式",
                 "body": r"同一平面上，相距 \(7\) 公里的砲台 \(A、B\)，\(A\) 在 \(B\) 正東方。\(A\) 向西偏北 \(\theta\)、\(B\) 向東偏北 \(\theta\) 發射（\(\theta\) 為銳角），兩砲彈皆命中 \(9\) 公里外的同一目標 \(P\)。接著 \(A\) 改向西偏北 \(\dfrac\theta2\) 發射，彈著點為 \(9\) 公里外的 \(Q\)。求砲台 \(B\) 與彈著點 \(Q\) 的距離 \(\overline{BQ}\)。",
                 "options": [r"\(4\) 公里", r"\(4.5\) 公里", r"\(5\) 公里", r"\(5.5\) 公里", r"\(6\) 公里"],
                 "solution": {"brief": r"(3) \(5\) 公里",
                              "steps": [
                                  r"由對稱，\(\overline{AP}=\overline{BP}=9\)，\(P\) 在 \(\overline{AB}\) 中垂線上，底角 \(\angle PAB=\theta\)，\(\cos\theta=\dfrac{\overline{AB}/2}{\overline{AP}}=\dfrac{7/2}{9}=\dfrac{7}{18}\)。",
                                  r"半角：\(\cos\dfrac\theta2=\sqrt{\dfrac{1+\cos\theta}{2}}=\sqrt{\dfrac{1+7/18}{2}}=\sqrt{\dfrac{25}{36}}=\dfrac56\)。",
                                  r"\(\triangle ABQ\)：\(\overline{AB}=7,\overline{AQ}=9,\angle QAB=\dfrac\theta2\)。餘弦定理 \(\overline{BQ}^2=49+81-2\cdot7\cdot9\cdot\dfrac56=130-105=25\)，故 \(\overline{BQ}=5\)，選 (3)。"]}},
            ],
            "selfcheck": {
                "q": r"從地面看塔頂仰角 \(30^\circ\)、水平距離 \(100\) 公尺，求塔高。",
                "a": r"**\(\dfrac{100\sqrt3}{3}\) 公尺**：\(100\tan30^\circ=\dfrac{100}{\sqrt3}\)。"},
            "strategy": [
                r"測量題先 **畫示意圖**、標出仰角／俯角／方位角，再選正弦或餘弦定理。",
                r"比較邊長用「**大角對大邊**」；比較 \(\sin/\cos\) 注意單調性（\(\sin\) 在 \(0°\)–\(90°\) 增、\(\cos\) 減）。",
                r"鈍角三角形特別小心：鈍角的 \(\cos\) 為負、\(\sin\) 仍正。",
            ],
        },
        {
            "num": "考點 4", "id": "kp4", "nav": "三角函數圖形（疊合、對稱）",
            "title": r"三角函數圖形：週期、對稱與疊合",
            "intro": r"**疊合＝把兩個波合成一個波**：\(a\sin x+b\cos x\) 看似兩條，其實能併成**一條**正弦波 \(\sqrt{a^2+b^2}\sin(x+\varphi)\)。為什麼振幅是 \(\sqrt{a^2+b^2}\)？把係數 \((a,b)\) 想成坐標，這正是它到原點的長度（畢氏！）。一旦併成一條，**最大值就是 \(\sqrt{a^2+b^2}\)**、週期與對稱軸也都看得出來。這是本考點的王牌。",
            "prereq": [
                r"**和角公式** \(\sin(x+\varphi)=\sin x\cos\varphi+\cos x\sin\varphi\)（考點 5，疊合的原理）",
                r"**\(y=\sin x\) 基本圖形**：過原點、振幅 \(1\)、週期 \(2\pi\)",
                r"**畢氏定理**（理解振幅 \(\sqrt{a^2+b^2}\) 的來源）",
            ],
            "points": [
                {"label": r"基本圖形與週期", "lines": [
                    r"\(y=\sin x\)、\(y=\cos x\) 週期 \(=\) 【\(2\pi\)】、振幅 \(1\)；\(y=\tan x\) 週期 \(=\) 【\(\pi\)】；",
                    r"\(y=a\sin(bx+c)+d\)：振幅 \(=\) 【\(|a|\)】、週期 \(=\) 【\(\dfrac{2\pi}{|b|}\)】、左右平移 \(=\) 【\(-\dfrac cb\)】、上下平移 \(=\) 【\(d\)】。"]},
                {"label": r"對稱", "lines": [
                    r"\(y=\sin x\)：對稱中心 【\((k\pi,\,0)\)】、對稱軸 【\(x=\dfrac\pi2+k\pi\)】（過最高／最低點）；",
                    r"\(y=\cos x\)：對稱中心 【\(\left(\dfrac\pi2+k\pi,\,0\right)\)】、對稱軸 【\(x=k\pi\)】。"]},
                {"label": r"疊合（最重要）", "lines": [
                    r"\(a\sin x+b\cos x=\) 【\(\sqrt{a^2+b^2}\,\sin(x+\varphi)\)】，其中 \(\tan\varphi=\dfrac ba\)；",
                    r"用途：\(a\sin x+b\cos x\) 的 **最大值 ＝ \(\sqrt{a^2+b^2}\)、最小值 ＝ \(-\sqrt{a^2+b^2}\)**；",
                    r"例：\(\sin x+\sqrt3\cos x=\) 【\(2\sin\left(x+\dfrac\pi3\right)\)】（最大值 \(2\)）。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(y=\sin 2x\) 的週期是 \(2\pi\)", "right": r"週期 ＝ \(\dfrac{2\pi}{2}=\pi\)"},
                {"wrong": r"\(a\sin x+b\cos x\) 的最大值是 \(a+b\)", "right": r"是 \(\sqrt{a^2+b^2}\)"},
                {"wrong": r"\(\sin x\) 的對稱軸是 \(x=k\pi\)", "right": r"對稱軸過最高／最低點 \(x=\dfrac\pi2+k\pi\)；\(x=k\pi\) 是對稱中心"},
            ],
            "worked": {
                "q": r"求 \(y=\sqrt3\sin x+\cos x\) 的最大值，並把它寫成單一正弦波。",
                "steps": [
                    {"do": r"振幅 \(=\sqrt{(\sqrt3)^2+1^2}=\sqrt{3+1}=2\)。",
                     "why": r"把係數 \((\sqrt3,\,1)\) 當坐標，它到原點的距離（畢氏）就是振幅。"},
                    {"do": r"\(\sqrt3\sin x+\cos x=2\sin(x+\varphi)\)，其中 \(\tan\varphi=\dfrac{1}{\sqrt3}\Rightarrow\varphi=\dfrac\pi6\)。",
                     "why": r"併成一條後，相位 \(\varphi\) 由 \(\tan\varphi=\dfrac ba\) 決定。"},
                    {"do": r"\(y=2\sin\left(x+\dfrac\pi6\right)\)，最大值 \(=2\)。",
                     "why": r"正弦波的最大值就是它的振幅。"},
                ],
            },
            "questions": [
                {"tag": "112 數A · 多選 12", "level": "★★★（難）", "core": "疊合、對稱軸、解的個數、圖形平移",
                 "body": r"令 \(f(x)=\sin x+\sqrt3\cos x\)，試選出正確的選項。",
                 "options": [r"鉛直線 \(x=\dfrac\pi6\) 為 \(y=f(x)\) 圖形的對稱軸",
                             r"若鉛直線 \(x=a\) 和 \(x=b\) 均為 \(y=f(x)\) 圖形的對稱軸，則 \(f(a)=f(b)\)",
                             r"在 \([0,2\pi)\) 中僅有一個實數 \(x\) 滿足 \(f(x)=\sqrt3\)",
                             r"在 \([0,2\pi)\) 中滿足 \(f(x)=\dfrac12\) 的所有實數 \(x\) 之和不超過 \(2\pi\)",
                             r"\(y=f(x)\) 的圖形可由 \(y=4\sin^2\dfrac x2\) 的圖形經適當（左右、上下）平移得到"],
                 "solution": {"brief": r"(1)(5)",
                              "steps": [r"先疊合：\(f(x)=\sin x+\sqrt3\cos x=2\sin\left(x+\dfrac\pi3\right)\)（振幅 2、週期 \(2\pi\)）。",
                                        r"(1)○：對稱軸過最高／最低點，\(x+\dfrac\pi3=\dfrac\pi2+k\pi\Rightarrow x=\dfrac\pi6+k\pi\)，含 \(x=\dfrac\pi6\)。",
                                        r"(2)✗：對稱軸交替過最高點（\(f=2\)）與最低點（\(f=-2\)），\(f(a)\)、\(f(b)\) 不一定相等。",
                                        r"(3)✗：\(\sin\left(x+\frac\pi3\right)=\frac{\sqrt3}2\) 在 \([0,2\pi)\) 有 \(x=0,\frac\pi3\) **兩解**。",
                                        r"(4)✗：\(f(x)=\frac12\) 兩解之和 \(=3\pi-\frac{2\pi}3=\frac{7\pi}3\gt2\pi\)。",
                                        r"(5)○：\(y=4\sin^2\frac x2=2-2\cos x\)，下移 \(2\) 得 \(-2\cos x=2\sin\left(x-\frac\pi2\right)\)，再左右平移即得 \(f(x)\)。"]}},
                {"tag": "觀念範例（疊合求極值）", "level": "★★☆（中）", "core": "疊合求最大值與週期",
                 "body": r"設 \(g(x)=3\sin x+4\cos x\)。求 \(g(x)\) 的最大值與最小正週期。",
                 "solution": {"brief": r"最大值 \(=5\)、最小正週期 \(=2\pi\)",
                              "steps": [r"疊合：\(g(x)=\sqrt{3^2+4^2}\,\sin(x+\varphi)=5\sin(x+\varphi)\)。",
                                        r"故最大值 \(=5\)、最小值 \(=-5\)；週期與 \(\sin x\) 同，為 \(2\pi\)。"]}},
                {"tag": "114 數A · 多選 10", "level": "★★★（難）", "core": "y=sin(πx) 與水平線的交點：對稱、距離、坐標和",
                 "body": r"令 \(\Gamma\) 為 \(y=\sin(\pi x)\) 在 \(0\le x\le3\) 的圖形。水平線 \(L:y=k\) 與 \(\Gamma\) 相交，其中三交點 \(P(x_1,k)、Q(x_2,k)、R(x_3,k)\) 滿足 \(x_1<x_2<1<x_3\)。試選出正確的選項。",
                 "options": [
                     r"\(k>0\)",
                     r"\(L\) 與 \(\Gamma\) 恰有 \(3\) 個交點",
                     r"\(x_1+x_2<1\)",
                     r"若 \(2\,\overline{PQ}=\overline{QR}\)，則 \(k=\dfrac12\)",
                     r"\(L\) 與 \(\Gamma\) 所有交點的 \(x\) 坐標之和大於 \(5\)"],
                 "solution": {"brief": r"(1)(4)(5)",
                              "steps": [
                                  r"\(y=\sin(\pi x)\) 週期 \(2\)，在 \([0,3]\) 為「上凸峰 \([0,1]\)、下凹谷 \([1,2]\)、上凸峰 \([2,3]\)」。\(P,Q\) 在第一峰（\(x<1\)）故 \(k>0\)（(1)○）。",
                                  r"(2)✗ \(0<k<1\) 時第一、三峰各 \(2\) 交點，共 \(4\) 個（非 \(3\)）。",
                                  r"設第一個交點的 \(x\) 坐標為 \(t\)（\(0<t<\tfrac12\)、\(\sin(\pi t)=k\)）：第一峰對稱於 \(x=\tfrac12\)、第三峰是第一峰右移 \(2\)，故四交點為 \(x_1=t,\ x_2=1-t,\ x_3=2+t,\ x_4=3-t\)。(3)✗ \(x_1+x_2=t+(1-t)=1\)（對稱），非 \(<1\)。",
                                  r"(4)○ \(\overline{PQ}=x_2-x_1=1-2t\)、\(\overline{QR}=x_3-x_2=1+2t\)。\(2(1-2t)=1+2t\Rightarrow t=\dfrac16\Rightarrow k=\sin\dfrac\pi6=\dfrac12\)。",
                                  r"(5)○ 四交點之和 \(=t+(1-t)+(2+t)+(3-t)=6>5\)。故選 (1)(4)(5)。"]}},
                {"tag": "115 數A · 多選 11", "level": "★★★（難）", "core": "y=cos(πx/2) 與過定點直線的交點：對稱與整數判別",
                 "body": r"令 \(\Gamma\) 為 \(y=\cos\!\left(\dfrac\pi2 x\right)\) 的圖形。對任一實數 \(m\neq0\)，\(L_m\) 表示直線 \(y=mx+1\)。試選出正確的選項。",
                 "options": [
                     r"\(m>0\) 時，\(L_m\) 和 \(\Gamma\) 交點的 \(x\) 坐標皆為負",
                     r"若 \((a,b)\) 為 \(L_m\) 和 \(\Gamma\) 的交點，則 \((-a,b)\) 為 \(L_{-m}\) 和 \(\Gamma\) 的交點",
                     r"可以找到 \(m\neq0\) 使 \(L_m\) 和 \(\Gamma\) 交於 \(\left(\dfrac{20}{3},\dfrac12\right)\)",
                     r"若 \(L_m\) 與 \(\Gamma\) 有一交點在直線 \(y=-1\) 上，則 \(\dfrac1m\) 是奇數",
                     r"若 \(L_m\) 與 \(\Gamma\) 有一交點在 \(x\) 軸上，則 \(L_m\) 與 \(\Gamma\) 有偶數個交點"],
                 "solution": {"brief": r"(2)(4)",
                              "steps": [
                                  r"\(\Gamma\) 週期 \(4\)、為偶函數；\(L_m\) 恆過 \((0,1)\) 而 \((0,1)\) 在 \(\Gamma\) 上，故 \((0,1)\) 必為交點。",
                                  r"(1)✗ \(x=0\) 即為交點，不是負的。",
                                  r"(2)○ \(\Gamma\) 偶：\(b=\cos\tfrac\pi2 a=\cos\tfrac\pi2(-a)\)；且 \(b=ma+1=-m(-a)+1\)，故 \((-a,b)\) 在 \(\Gamma\) 與 \(L_{-m}\) 上。",
                                  r"(3)✗ \(\cos\!\left(\dfrac\pi2\cdot\dfrac{20}{3}\right)=\cos\dfrac{10\pi}{3}=\cos\dfrac{4\pi}{3}=-\dfrac12\neq\dfrac12\)，該點不在 \(\Gamma\) 上。",
                                  r"(4)○ 交點在 \(y=-1\)：\(\cos\tfrac\pi2 x_0=-1\Rightarrow x_0=4k+2\)；又 \(mx_0=-2\Rightarrow\dfrac1m=-\dfrac{x_0}{2}=-(2k+1)\) 為奇數。",
                                  r"(5)✗ 反例 \(m=1\)：交點 \((-1,0)\) 在 \(x\) 軸上，但 \(y=x+1\) 與 \(\Gamma\) 交於 \((-2,-1),(-1,0),(0,1)\) 共 \(3\) 個（奇數）。故選 (2)(4)。"]}},
            ],
            "selfcheck": {
                "q": r"\(y=2\sin x+1\) 的最大值、最小值與週期各為何？",
                "a": r"最大 **\(3\)**、最小 **\(-1\)**、週期 **\(2\pi\)**。"},
            "strategy": [
                r"看到 \(a\sin x+b\cos x\) 先 **疊合** 成 \(\sqrt{a^2+b^2}\sin(x+\varphi)\)：振幅、極值、對稱軸全靠它。",
                r"對稱軸過最高／最低點、對稱中心過零點，先疊合再判斷。",
                r"求週期看係數：\(y=\sin(bx)\) 的週期 ＝ \(\dfrac{2\pi}{|b|}\)。",
            ],
        },
        {
            "num": "考點 5", "id": "kp5", "nav": "和差角、倍角",
            "title": r"和差角與倍角（解方程與不等式）",
            "intro": r"**和差角公式讓你『拆開算不出的角』**：\(\sin75°\) 不在特殊角表裡，但 \(75°=45°+30°\)，用 \(\sin(A+B)=\sin A\cos B+\cos A\sin B\) 就能拿特殊角算出來。倍角是和角的特例（\(A=B\)）：\(\sin2\theta=2\sin\theta\cos\theta\)。它們是把複合角**拆開／合併**的工具，解三角方程式、不等式全靠它。**最易錯**：\(\cos(A+B)\) 中間是「\(-\)」，和外面符號相反。",
            "prereq": [
                r"**特殊角三角函數值**（考點 1 的表）",
                r"**會拆角**：把 \(75°\) 看成 \(45°+30°\)、\(15°\) 看成 \(45°-30°\)",
                r"**提公因式／因式分解**（解方程時用）",
            ],
            "points": [
                {"label": r"和差角公式", "lines": [
                    r"\(\sin(A\pm B)=\) 【\(\sin A\cos B\pm\cos A\sin B\)】；",
                    r"\(\cos(A\pm B)=\) 【\(\cos A\cos B\mp\sin A\sin B\)】（[[cos 變號相反||\(\cos(A+B)\) 取「\(-\)」、\(\cos(A-B)\) 取「\(+\)」，和外面的 \(\pm\) **相反**，最容易記錯。]]）；",
                    r"\(\tan(A\pm B)=\) 【\(\dfrac{\tan A\pm\tan B}{1\mp\tan A\tan B}\)】。"]},
                {"label": r"二倍角公式", "lines": [
                    r"\(\sin2\theta=\) 【\(2\sin\theta\cos\theta\)】；",
                    r"\(\cos2\theta=\) 【\(\cos^2\theta-\sin^2\theta\)】 \(=\) 【\(1-2\sin^2\theta\)】 \(=\) 【\(2\cos^2\theta-1\)】；",
                    r"\(\tan2\theta=\) 【\(\dfrac{2\tan\theta}{1-\tan^2\theta}\)】。"]},
                {"label": r"半角與降冪", "lines": [
                    r"降冪：\(\sin^2\theta=\) 【\(\dfrac{1-\cos2\theta}{2}\)】、\(\cos^2\theta=\) 【\(\dfrac{1+\cos2\theta}{2}\)】（積分、求面積常用）。"]},
            ],
            "misconceptions": [
                {"wrong": r"\(\cos(A+B)=\cos A\cos B+\sin A\sin B\)", "right": r"\(=\cos A\cos B-\sin A\sin B\)（cos 的符號與外面相反）"},
                {"wrong": r"\(\sin2\theta=2\sin\theta\)", "right": r"\(=2\sin\theta\cos\theta\)"},
                {"wrong": r"\(\cos2\theta\) 只有一種寫法", "right": r"三種：\(\cos^2-\sin^2\)、\(1-2\sin^2\)、\(2\cos^2-1\)（依已知選用）"},
            ],
            "worked": {
                "q": r"求 \(\sin75°\) 的值。",
                "steps": [
                    {"do": r"\(75°=45°+30°\)，用和角：\(\sin75°=\sin(45°+30°)\)。",
                     "why": r"\(75°\) 不在特殊角表裡，但拆成兩個特殊角的和就能算。"},
                    {"do": r"\(=\sin45°\cos30°+\cos45°\sin30°\)。",
                     "why": r"套和角公式 \(\sin(A+B)=\sin A\cos B+\cos A\sin B\)。"},
                    {"do": r"\(=\dfrac{\sqrt2}{2}\cdot\dfrac{\sqrt3}{2}+\dfrac{\sqrt2}{2}\cdot\dfrac12=\dfrac{\sqrt6+\sqrt2}{4}\)。",
                     "why": r"代入特殊角的值，再通分。"},
                ],
            },
            "questions": [
                {"tag": "113 數A · 單選 4", "level": "★★☆（中）", "core": "和角公式解三角方程式（解的個數）",
                 "body": r"試問有多少個實數 \(x\) 滿足 \(\sin\left(x+\dfrac\pi6\right)=\sin x+\sin\dfrac\pi6\) 且 \(0\le x\lt2\pi\)？",
                 "options": [r"1 個", r"2 個", r"3 個", r"4 個", r"5 個（含）以上"],
                 "solution": {"brief": r"(2)，2 個",
                              "steps": [r"左式用和角：\(\sin\left(x+\frac\pi6\right)=\frac{\sqrt3}2\sin x+\frac12\cos x\)；右式 \(=\sin x+\frac12\)。",
                                        r"整理得 \((\sqrt3-2)\sin x+\cos x-1=0\)。代入 \(\cos x-1=-2\sin^2\frac x2\)、\(\sin x=2\sin\frac x2\cos\frac x2\)：",
                                        r"\(2\sin\dfrac x2\left[(\sqrt3-2)\cos\dfrac x2-\sin\dfrac x2\right]=0\)。得 \(\sin\frac x2=0\Rightarrow x=0\)，或 \(\tan\frac x2=\sqrt3-2\Rightarrow x\approx5.75\)。在 \([0,2\pi)\) 共 **2 個**。"]}},
                {"tag": "114 數A · 單選 5", "level": "★★★（難）", "core": "二倍角解三角不等式（取交集）",
                 "body": r"設 \(0\le\theta\le2\pi\)。若 \(\sin2\theta\gt\sin\theta\) 且 \(\cos2\theta\gt\cos\theta\) 的解可表為 \(a\pi\lt\theta\lt b\pi\)（\(a,b\) 為實數），試問 \(b-a\) 之值為何？",
                 "options": [r"\(\dfrac13\)", r"\(\dfrac12\)", r"\(\dfrac23\)", r"\(1\)", r"\(\dfrac43\)"],
                 "solution": {"brief": r"(1)，\(b-a=\dfrac13\)",
                              "steps": [r"\(\sin2\theta\gt\sin\theta\Rightarrow\sin\theta(2\cos\theta-1)\gt0\Rightarrow\theta\in\left(0,\frac\pi3\right)\cup\left(\pi,\frac{5\pi}3\right)\)。",
                                        r"\(\cos2\theta\gt\cos\theta\Rightarrow2\cos^2\theta-\cos\theta-1\gt0\Rightarrow\cos\theta\lt-\frac12\Rightarrow\theta\in\left(\frac{2\pi}3,\frac{4\pi}3\right)\)。",
                                        r"取交集得 \(\theta\in\left(\pi,\frac{4\pi}3\right)\)，即 \(a=1,\,b=\frac43\)，故 \(b-a=\frac13\)。"]}},
                {"tag": "115 數A · 選填 17", "level": "★★★（難）", "core": "直角三角形內分角（倍角）＋ 正弦定理求分點比",
                 "body": r"直角 \(\triangle ABC\) 中 \(\angle CAB\) 為直角，\(\overline{AB}\) 上一點 \(D\) 滿足 \(\angle BCD=2\angle ACD\)，且 \(\overline{BC}=2\,\overline{BD}\)。若 \(\overrightarrow{AD}=k\,\overrightarrow{AB}\)，求 \(k\)（最簡分數）。",
                 "solution": {"brief": r"\(\dfrac{3}{11}\)",
                              "steps": [
                                  r"令 \(\angle ACD=\theta\)、\(\angle BCD=2\theta\)。直角 \(\triangle ACD\) 中 \(\angle ADC=90^\circ-\theta\)，故 \(\angle BDC=90^\circ+\theta\)。",
                                  r"\(\triangle BCD\) 正弦定理：\(\dfrac{\overline{BD}}{\sin\angle BCD}=\dfrac{\overline{BC}}{\sin\angle BDC}\Rightarrow\dfrac{\overline{BD}}{\overline{BC}}=\dfrac{\sin2\theta}{\sin(90^\circ+\theta)}=\dfrac{2\sin\theta\cos\theta}{\cos\theta}=2\sin\theta\)。",
                                  r"由 \(\overline{BC}=2\,\overline{BD}\Rightarrow\dfrac{\overline{BD}}{\overline{BC}}=\dfrac12=2\sin\theta\Rightarrow\sin\theta=\dfrac14\)，\(\tan\theta=\dfrac{1}{\sqrt{15}}\)。",
                                  r"\(k=\dfrac{\overline{AD}}{\overline{AB}}=\dfrac{\tan\theta}{\tan3\theta}\)（直角邊 \(\overline{AD}=\overline{AC}\tan\theta\)、\(\overline{AB}=\overline{AC}\tan3\theta\)，\(\angle ACB=3\theta\)）。用教過的公式合成 \(3\theta=2\theta+\theta\)：\(\tan2\theta=\dfrac{2\tan\theta}{1-\tan^2\theta}=\dfrac{2/\sqrt{15}}{14/15}=\dfrac{\sqrt{15}}{7}\)，再 \(\tan3\theta=\dfrac{\tan2\theta+\tan\theta}{1-\tan2\theta\tan\theta}=\dfrac{\frac{\sqrt{15}}{7}+\frac{1}{\sqrt{15}}}{1-\frac17}=\dfrac{22/(7\sqrt{15})}{6/7}=\dfrac{11}{3\sqrt{15}}\)。",
                                  r"故 \(k=\dfrac{1/\sqrt{15}}{11/(3\sqrt{15})}=\dfrac{3}{11}\)。"]}},
            ],
            "selfcheck": {
                "q": r"已知 \(\sin\theta=\dfrac35\)（\(\theta\) 為銳角），求 \(\sin2\theta\)。",
                "a": r"**\(\dfrac{24}{25}\)**：\(\cos\theta=\dfrac45\)，\(\sin2\theta=2\cdot\dfrac35\cdot\dfrac45\)。"},
            "strategy": [
                r"和角公式的 \(\cos\) 記「**符號相反**」：\(\cos(A+B)=\cos A\cos B-\sin A\sin B\)。",
                r"解三角方程式：用和差／倍角化成 **同一個角**，或提公因式因式分解（如提出 \(\sin\frac x2\)）。",
                r"解三角不等式：拆成 **乘積 \(\gt0\)**，配單位圓找區間，多條件再 **取交集**。",
            ],
        },
        {
            "num": "考點 6", "id": "kp6", "nav": "角平分線、面積比與相似",
            "title": r"三角形面積比、相似與角平分線",
            "intro": r"**這個考點都在算『比』**。最常考的角平分線定理：\(\angle A\) 的平分線把對邊 \(BC\) 分成的兩段，比例剛好等於**兩條鄰邊之比** \(AB:AC\)（不是切一半！）。面積比的關鍵：**等高的兩個三角形，面積比＝底之比**；夾角相同就用 \(\dfrac12ab\sin C\) 比。相似三角形的**面積比是邊長比的平方**。",
            "prereq": [
                r"**三角形面積** \(\dfrac12\times底\times高\)、\(\dfrac12ab\sin C\)（考點 2）",
                r"**比例與相似**的基本概念",
                r"**內分點**：會把一段長按比例分配",
            ],
            "points": [
                {"label": r"角平分線定理", "lines": [
                    r"\(\angle A\) 的內角平分線交 \(BC\) 於 \(D\)：\(\dfrac{BD}{DC}=\) 【\(\dfrac{AB}{AC}\)】（分對邊成 **兩鄰邊之比**）；",
                    r"外角平分線則為外分點，比值仍為 \(\dfrac{AB}{AC}\)。"]},
                {"label": r"面積比", "lines": [
                    r"**等高** \(\Rightarrow\) 面積比 ＝ 底之比；**夾角相同／互補** \(\Rightarrow\) 用 \(\dfrac12 ab\sin C\) 比；",
                    r"三角形內一點連三頂點分成三塊，面積比可由分點比求出。"]},
                {"label": r"相似", "lines": [
                    r"相似 \(\Rightarrow\) 對應邊成比例、對應角相等；",
                    r"面積比 ＝ 【對應邊長比的平方】（邊長比 \(k\Rightarrow\) 面積比 \(k^2\)）。"]},
            ],
            "misconceptions": [
                {"wrong": r"角平分線把對邊分成相等兩段", "right": r"分成「兩鄰邊之比」\(BD:DC=AB:AC\)"},
                {"wrong": r"相似三角形面積比 ＝ 邊長比", "right": r"＝ 邊長比的 **平方**"},
                {"wrong": r"比面積只能用 底 × 高", "right": r"夾角已知時用 \(\dfrac12 ab\sin C\) 比最快"},
            ],
            "worked": {
                "q": r"\(\triangle ABC\) 中，\(D\) 在 \(BC\) 上且 \(BD:DC=2:3\)。求 \(\triangle ABD\) 與 \(\triangle ABC\) 的面積比。",
                "steps": [
                    {"do": r"\(\triangle ABD\) 與 \(\triangle ABC\) **等高**（都是頂點 \(A\) 到直線 \(BC\) 的高）。",
                     "why": r"兩個三角形共用頂點 \(A\)、底都在直線 \(BC\) 上，所以高相同。"},
                    {"do": r"等高 → 面積比 ＝ 底之比 ＝ \(BD:BC\)。",
                     "why": r"面積 \(=\dfrac12\times底\times高\)，高一樣時就只看底。"},
                    {"do": r"\(BD:BC=2:(2+3)=2:5\)，故 \(\triangle ABD:\triangle ABC=2:5\)。",
                     "why": r"\(BD:DC=2:3\)，所以 \(BD\) 佔 \(BC\) 的 \(\dfrac25\)。"},
                ],
            },
            "questions": [
                {"tag": "觀念範例（角平分線）", "level": "★★☆（中）", "core": "角平分線定理＋分點",
                 "body": r"\(\triangle ABC\) 中 \(AB=6\)、\(AC=4\)，\(\angle A\) 的內角平分線交 \(BC\) 於 \(D\)。若 \(BC=5\)，求 \(BD\)。",
                 "solution": {"brief": r"\(BD=3\)",
                              "steps": [r"角平分線定理 \(\dfrac{BD}{DC}=\dfrac{AB}{AC}=\dfrac64=\dfrac32\)，且 \(BD+DC=BC=5\)，",
                                        r"故 \(BD=5\times\dfrac{3}{3+2}=3\)。"]}},
                {"tag": "111 數A · 選填 15", "level": "★★★（難）", "core": "相似三角形面積比 ＋ 平行線間距（30° 面積）",
                 "body": r"三角形土地 \(ABC\)，\(\overline{BC}=16\) 公尺。原擬徵收以平行線 \(\overline{DE}\parallel\overline{BC}\) 為邊、路寬 \(h\) 的梯形 \(DBCE\)（\(D\) 在 \(\overline{AB}\)、\(E\) 在 \(\overline{AC}\)），使剩下的 \(\triangle ADE\) 只有原面積的 \(\dfrac{9}{16}\)。改協商為：以平行線 \(\overline{BE}\parallel\overline{FC}\) 為邊、路寬不變 \(h\)，只徵收 \(\triangle BCE\)，其中 \(\angle EBC=30^\circ\)。求王家剩餘土地 \(\triangle ABE\) 的面積（平方公尺）。",
                 "solution": {"brief": r"\(192\)",
                              "steps": [
                                  r"**求高 \(H\) 與路寬 \(h\)**：\(\dfrac{[ADE]}{[ABC]}=\dfrac{9}{16}\Rightarrow\dfrac{AD}{AB}=\dfrac34\)，故 \(\overline{DE}\) 距 \(\overline{BC}\) 為 \(H-\tfrac34H=\tfrac14H=h\)。",
                                  r"**由第二方案定 \(h\)**：平行線 \(\overline{BE}、\overline{FC}\)（過 \(B、C\)）間距 \(=\overline{BC}\sin30^\circ=16\cdot\tfrac12=8=h\)，故 \(H=4h=32\)，\([ABC]=\tfrac12\cdot16\cdot32=256\)。",
                                  r"**求 \([BCE]\)**：\(E\) 在 \(\overline{AC}\) 上、與 \(\overline{BC}\) 距 \(h=8\)（同 \(\overline{DE}\) 高度），故 \([BCE]=\tfrac12\cdot\overline{BC}\cdot8=\tfrac12\cdot16\cdot8=64\)。",
                                  r"\([ABE]=[ABC]-[BCE]=256-64=\mathbf{192}\) 平方公尺。"]}},
            ],
            "selfcheck": {
                "q": r"\(\triangle ABC\) 中 \(\overline{AD}\) 為 \(\angle A\) 的平分線，\(AB=6,AC=4\)，求 \(BD:DC\)。",
                "a": r"**\(3:2\)**：角平分線分對邊成兩鄰邊之比 \(AB:AC=6:4\)。"},
            "strategy": [
                r"看到角平分線就用 \(BD:DC=AB:AC\)。",
                r"比面積優先用 \(\dfrac12 ab\sin C\)（夾角已知）或「等高比底」。",
                r"相似的面積比是邊長比的 **平方**。",
            ],
        },
        {
            "num": "考點 7", "id": "kp7", "nav": "圓周角與二面角中的三角",
            "title": r"圓周角與二面角中的三角",
            "intro": r"**同一段弧，站在圓周上看它『永遠是同一個角』，而且剛好是圓心看它的一半**——這就是圓周角定理 \(\angle APB=\dfrac12\angle AOB\)。一個超好用的特例：**直徑所對的圓周角＝\(90°\)**（半圓上的角是直角）。再配上正弦定理 \(\dfrac{a}{\sin A}=2R\)，就能把「角、邊、外接圓」串起來——這正是魔王混合題最愛的接點。",
            "prereq": [
                r"**圓的基本**：圓心、半徑、弦、弧、圓心角",
                r"**正弦定理** \(\dfrac{a}{\sin A}=2R\)（考點 2）",
                r"**餘角** \(\cos(90°-\theta)=\sin\theta\)（考點 1）",
            ],
            "points": [
                {"label": r"圓周角定理", "lines": [
                    r"圓周角 ＝ 同弧所對 **圓心角的** 【一半】：\(\angle APB=\) 【\(\dfrac12\angle AOB\)】（\(O\) 為圓心）；",
                    r"**同弧（或等弧）所對的圓周角相等**；",
                    r"**直徑所對的圓周角 ＝** 【\(90°\)】（半圓上的圓周角是直角）；",
                    r"弦切角（切線與弦的夾角）＝ 該弦所對的 **圓周角**。"]},
                {"label": r"外接圓與正弦定理", "lines": [
                    r"正弦定理 \(\dfrac{a}{\sin A}=\) 【\(2R\)】（\(R\) 為外接圓半徑）；",
                    r"直角三角形：**斜邊 ＝ 外接圓直徑**。"]},
                {"label": r"圓內接四邊形", "lines": [
                    r"圓內接四邊形 **對角互補**：\(\angle A+\angle C=\) 【\(180°\)】。"]},
                {"label": r"二面角", "lines": [
                    r"二面角 ＝ 在稜上取一點、於兩面各作 **垂直稜** 的射線，兩射線的夾角；",
                    r"求值常用餘弦定理，或用法向量（見空間單元）。"]},
            ],
            "misconceptions": [
                {"wrong": r"圓周角 ＝ 圓心角", "right": r"圓周角 ＝ 圓心角的 **一半**"},
                {"wrong": r"圓內接四邊形對角相等", "right": r"對角 **互補**（和為 \(180°\)）"},
                {"wrong": r"任意三角形斜邊 ＝ 外接圓直徑", "right": r"只有 **直角三角形** 才成立"},
            ],
            "worked": {
                "q": r"\(AB\) 是圓 \(O\) 的**直徑**，\(C\) 是圓上另一點，\(AB=10\)、\(AC=6\)。求 \(BC\)。",
                "steps": [
                    {"do": r"\(AB\) 是直徑 \(\Rightarrow\angle ACB=90°\)。",
                     "why": r"直徑所對的圓周角是直角（半圓上的圓周角）。"},
                    {"do": r"\(\triangle ABC\) 直角在 \(C\)，用畢氏：\(BC^2=AB^2-AC^2=100-36=64\)。",
                     "why": r"\(AB\) 是斜邊，兩股平方和等於斜邊平方。"},
                    {"do": r"\(BC=8\)。",
                     "why": r"開根號。"},
                ],
            },
            "questions": [
                {"tag": "110 舊制 · 單選 3", "level": "★★★（難）", "core": "圓周角定理＋切線（cosA=sin(θ/2)）",
                 "body": r"如圖，\(\triangle ABC\) 為銳角三角形，\(P\) 為 \(\triangle ABC\) 外接圓 \(\Gamma\) 外的一點，且 \(PB\)、\(PC\) 都與 \(\Gamma\) 相切。設 \(\angle BPC=\theta\)，則 \(\cos A\) 之值為何？",
                 "options": [r"\(\sin\dfrac\theta2\)", r"\(\sin\theta\)", r"\(\cos\dfrac\theta2\)", r"\(\dfrac{\cos\theta}{2}\)", r"\(\cos\theta\)"],
                 "solution": {"brief": r"(1) \(\sin\dfrac\theta2\)",
                              "steps": [r"切線垂直半徑：設圓心 \(O\)，四邊形 \(PBOC\) 中 \(\angle PBO=\angle PCO=90°\)、\(\angle BPC=\theta\)，故圓心角 \(\angle BOC=360°-90°-90°-\theta=180°-\theta\)。",
                                        r"圓周角 \(\angle A=\dfrac12\angle BOC=90°-\dfrac\theta2\)。",
                                        r"故 \(\cos A=\cos\left(90°-\dfrac\theta2\right)=\sin\dfrac\theta2\)，選 (1)。"]}},
                {"tag": "觀念範例（外接圓＋正弦定理）", "level": "★★☆（中）", "core": "外接圓直徑 ＝ a/sinA",
                 "body": r"\(\triangle ABC\) 內接於半徑 \(R=5\) 的圓，且 \(\angle A=30°\)。求邊 \(BC\)（即 \(a\)）。",
                 "solution": {"brief": r"\(BC=5\)",
                              "steps": [r"正弦定理 \(\dfrac{a}{\sin A}=2R\Rightarrow a=2R\sin A=2\times5\times\sin30°=10\times\dfrac12=5\)。"]}},
                {"tag": "114 數A · 選填 17", "level": "★★★（難）", "core": "外接圓 ＋ 餘弦定理 ＋ 弦↔圓心角求弦長",
                 "body": r"\(\triangle ABC\) 中 \(\overline{AB}=\overline{BC}=3\)、\(\cos\angle ABC=-\dfrac18\)。外接圓上有一點 \(D\) 滿足 \(\overline{BD}=4\) 且 \(\overline{AD}<\overline{CD}\)，求 \(\overline{CD}\)（最簡根式）。",
                 "solution": {"brief": r"\(3+\sqrt2\)",
                              "steps": [
                                  r"餘弦定理：\(\overline{AC}^2=9+9-2\cdot9\cdot(-\tfrac18)=\dfrac{81}{4}\Rightarrow\overline{AC}=\dfrac92\)。\(\sin\angle ABC=\dfrac{3\sqrt7}{8}\)，外接圓 \(2R=\dfrac{\overline{AC}}{\sin B}=\dfrac{12}{\sqrt7}\)。",
                                  r"**弦 ↔ 圓心角**：弦長 \(=2R\sin\)（圓心角的一半）。\(\overline{AB}=\overline{BC}=3\Rightarrow\) 各對半圓心角 \(\gamma\)：\(\sin\gamma=\dfrac{3}{2R}=\dfrac{\sqrt7}{4}\)、\(\cos\gamma=\dfrac34\)；\(\overline{BD}=4\Rightarrow\) 半圓心角 \(\delta\)：\(\sin\delta=\dfrac{4}{2R}=\dfrac{\sqrt7}{3}\)、\(\cos\delta=\dfrac{\sqrt2}{3}\)。",
                                  r"由 \(\overline{AD}<\overline{CD}\) 知 \(D\) 在靠 \(A\) 那側（弦 \(BD\) 的劣弧經過 \(A\)；若在另一側，\(AD,CD\) 恰互換、不合）。故弧 \(AD=2\delta-2\gamma\)：\(\overline{AD}=2R\sin(\delta-\gamma)=\dfrac{12}{\sqrt7}\cdot\left(\dfrac{\sqrt7}{3}\cdot\dfrac34-\dfrac{\sqrt2}{3}\cdot\dfrac{\sqrt7}{4}\right)=\dfrac{12}{\sqrt7}\cdot\dfrac{3\sqrt7-\sqrt{14}}{12}=3-\sqrt2\)。",
                                  r"繞一圈 \(360^\circ\)：弧 \(CD=360^\circ-2\gamma-2\gamma-(2\delta-2\gamma)=360^\circ-(2\gamma+2\delta)\)。由 \(\sin(180^\circ-x)=\sin x\)：\(\overline{CD}=2R\sin(\gamma+\delta)=\dfrac{12}{\sqrt7}\cdot\dfrac{3\sqrt7+\sqrt{14}}{12}=3+\sqrt2\)。",
                                  r"**驗算（補充：托勒密定理）**——圓內接四邊形「對角線乘積 ＝ 兩組對邊乘積之和」：\(\overline{AC}\cdot\overline{BD}=\overline{AB}\cdot\overline{CD}+\overline{BC}\cdot\overline{AD}\)，左式 \(\dfrac92\cdot4=18\)、右式 \(3\big[(3+\sqrt2)+(3-\sqrt2)\big]=18\) ✓。"]}},
            ],
            "selfcheck": {
                "q": r"圓中一弧所對的圓心角為 \(100^\circ\)，則此弧所對的圓周角為何？",
                "a": r"**\(50^\circ\)**：圓周角 ＝ 圓心角的一半。"},
            "strategy": [
                r"圓周角配正弦定理（\(\dfrac{a}{\sin A}=2R\)）連結邊長與外接圓。",
                r"圓內接四邊形 **對角互補**；直徑所對圓周角為直角。",
                r"二面角先找稜、作垂線，再用餘弦定理或法向量。",
            ],
        },
    ],

    "part2": {
        "count": "10", "note": "涵蓋七大考點 · 建議自行限時 40 分鐘作答後再對照詳解",
        "groups": [
            {"title": "一、單選題", "questions": [
                {"tag": "練習 1", "level": "★☆☆", "core": "三角比",
                 "body": r"設 \(\theta\) 為銳角且 \(\sin\theta=\dfrac{5}{13}\)，則 \(\tan\theta=\) ？",
                 "options": [r"\(\dfrac{5}{12}\)", r"\(\dfrac{12}{13}\)", r"\(\dfrac{12}{5}\)", r"\(\dfrac{13}{12}\)", r"\(\dfrac{5}{13}\)"],
                 "solution": {"brief": r"(1) \(\dfrac{5}{12}\)", "brief_label": "答",
                              "steps": [r"\(\cos\theta=\sqrt{1-\frac{25}{169}}=\dfrac{12}{13}\)，故 \(\tan\theta=\dfrac{\sin\theta}{\cos\theta}=\dfrac{5/13}{12/13}=\dfrac{5}{12}\)。"]}},
                {"tag": "練習 2", "level": "★☆☆", "core": "弧度換算",
                 "body": r"將 \(120°\) 化為弧度為？",
                 "options": [r"\(\dfrac{\pi}{3}\)", r"\(\dfrac{2\pi}{3}\)", r"\(\dfrac{3\pi}{4}\)", r"\(\dfrac{5\pi}{6}\)", r"\(\dfrac{4\pi}{3}\)"],
                 "solution": {"brief": r"(2) \(\dfrac{2\pi}{3}\)", "brief_label": "答",
                              "steps": [r"\(120°\times\dfrac{\pi}{180}=\dfrac{2\pi}{3}\)。"]}},
                {"tag": "練習 3", "level": "★★☆", "core": "正弦定理",
                 "body": r"\(\triangle ABC\) 中 \(\angle A=45°\)、\(\angle B=60°\)、\(a=\sqrt2\)，則 \(b=\) ？",
                 "options": [r"\(1\)", r"\(\sqrt2\)", r"\(\sqrt3\)", r"\(2\)", r"\(\sqrt6\)"],
                 "solution": {"brief": r"(3) \(\sqrt3\)", "brief_label": "答",
                              "steps": [r"\(\dfrac{a}{\sin A}=\dfrac{b}{\sin B}\Rightarrow b=\dfrac{a\sin B}{\sin A}=\dfrac{\sqrt2\cdot\frac{\sqrt3}{2}}{\frac{\sqrt2}{2}}=\sqrt3\)。"]}},
                {"tag": "練習 5", "level": "★★☆", "core": "疊合求極值",
                 "body": r"\(\cos x-\sin x\) 的最大值為？",
                 "options": [r"\(1\)", r"\(\sqrt2\)", r"\(\sqrt3\)", r"\(2\)", r"\(0\)"],
                 "solution": {"brief": r"(2) \(\sqrt2\)", "brief_label": "答",
                              "steps": [r"\(\cos x-\sin x=\sqrt{1^2+(-1)^2}\,\sin(x+\varphi)=\sqrt2\sin(x+\varphi)\)，最大值 \(\sqrt2\)。"]}},
                {"tag": "練習 4", "level": "★★☆", "core": "餘弦定理",
                 "body": r"\(\triangle ABC\) 中 \(b=2\)、\(c=3\)、\(\angle A=60°\)，則 \(a=\) ？",
                 "options": [r"\(\sqrt5\)", r"\(\sqrt6\)", r"\(\sqrt7\)", r"\(\sqrt{10}\)", r"\(\sqrt{13}\)"],
                 "solution": {"brief": r"(3) \(\sqrt7\)", "brief_label": "答",
                              "steps": [r"\(a^2=b^2+c^2-2bc\cos A=4+9-2\cdot6\cdot\dfrac12=13-6=7\)，故 \(a=\sqrt7\)。"]}},
            ]},
            {"title": "二、多選題", "questions": [
                {"tag": "練習 6", "level": "★★★", "core": "三角函數圖形性質",
                 "body": r"設 \(f(x)=2\sin 3x\)，下列敘述何者正確？",
                 "options": [r"最小正週期為 \(\dfrac{2\pi}{3}\)", r"振幅為 \(2\)", r"最大值為 \(2\)", r"圖形對稱中心為 \(\left(\dfrac{k\pi}{3},0\right)\)（\(k\) 為整數）", r"\(f\) 為偶函數"],
                 "solution": {"brief": r"(1)(2)(3)(4)", "brief_label": "答",
                              "steps": [r"\(f(x)=2\sin3x\)：週期 \(\frac{2\pi}{3}\)、振幅 \(2\)、最大值 \(2\)（(1)(2)(3)○）；對稱中心過零點 \(3x=k\pi\Rightarrow x=\frac{k\pi}{3}\)（(4)○）；",
                                        r"(5)✗：\(\sin\) 為奇函數，\(f(-x)=-f(x)\)，故 \(f\) 為奇函數。"]}},
            ]},
            {"title": "三、選填題", "questions": [
                {"tag": "練習 8", "level": "★★☆", "core": "角平分線定理",
                 "body": r"\(\triangle ABC\) 中 \(AB=8\)、\(AC=6\)，\(\angle A\) 的內角平分線交 \(BC\) 於 \(D\)。若 \(BC=7\)，則 \(BD=\) ？",
                 "solution": {"brief": r"\(4\)", "brief_label": "答",
                              "steps": [r"\(\dfrac{BD}{DC}=\dfrac{AB}{AC}=\dfrac86=\dfrac43\)，故 \(BD=7\times\dfrac{4}{4+3}=4\)。"]}},
                {"tag": "練習 7", "level": "★★☆", "core": "二倍角",
                 "body": r"設 \(\theta\) 為銳角且 \(\sin\theta=\dfrac45\)，則 \(\sin2\theta=\) ？",
                 "solution": {"brief": r"\(\dfrac{24}{25}\)", "brief_label": "答",
                              "steps": [r"\(\cos\theta=\dfrac35\)，\(\sin2\theta=2\sin\theta\cos\theta=2\cdot\dfrac45\cdot\dfrac35=\dfrac{24}{25}\)。"]}},
            ]},
            {"title": "四、非選擇題（須寫出計算過程）", "questions": [
                {"tag": "練習 9", "level": "★★☆", "core": "圓周角與外接圓（正弦定理）",
                 "body": r"\(\triangle ABC\) 內接於半徑 \(R=4\) 的圓，且 \(\angle A=45°\)。求邊 \(BC\)。",
                 "solution": {"brief": r"\(BC=4\sqrt2\)", "brief_label": "答",
                              "steps": [r"由 \(\dfrac{a}{\sin A}=2R\)：\(BC=a=2R\sin A=2\times4\times\sin45°=8\times\dfrac{\sqrt2}{2}=4\sqrt2\)。"]}},
                {"tag": "練習 10", "level": "★★☆", "core": "仰角三角測量",
                 "body": r"在水平地面上距塔底 \(100\) 公尺處，測得塔頂的仰角為 \(30°\)。求塔高（塔與地面垂直）。",
                 "solution": {"brief": r"塔高 \(=\dfrac{100\sqrt3}{3}\) 公尺", "brief_label": "答",
                              "steps": [r"\(\tan30°=\dfrac{塔高}{100}\Rightarrow 塔高=100\tan30°=\dfrac{100}{\sqrt3}=\dfrac{100\sqrt3}{3}\approx57.7\) 公尺。"]}},
            ]},
        ],
    },

    "part3": {
        "ref_table": [
            {"k": "三角比定義", "v": r"\(\sin=\dfrac{對}{斜}\)、\(\cos=\dfrac{鄰}{斜}\)、\(\tan=\dfrac{對}{鄰}\)"},
            {"k": "三大關係", "v": r"\(\sin^2+\cos^2=1\)；\(\tan=\dfrac{\sin}{\cos}\)；倒數 \(\csc,\sec,\cot\)"},
            {"k": "特殊角 sin", "v": r"\(\sin30°=\frac12\)、\(\sin45°=\frac{\sqrt2}{2}\)、\(\sin60°=\frac{\sqrt3}{2}\)"},
            {"k": "弧度", "v": r"\(180°=\pi\)；弧長 \(=r\theta\)、扇形面積 \(=\frac12 r^2\theta\)（\(\theta\) 用弧度）"},
            {"k": "正弦定理", "v": r"\(\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=2R\)"},
            {"k": "餘弦定理", "v": r"\(c^2=a^2+b^2-2ab\cos C\)；\(\cos C=\dfrac{a^2+b^2-c^2}{2ab}\)"},
            {"k": "面積", "v": r"\(\frac12 ab\sin C=\frac{abc}{4R}=rs=\sqrt{s(s-a)(s-b)(s-c)}\)"},
            {"k": "和差角", "v": r"\(\sin(A\pm B)=\sin A\cos B\pm\cos A\sin B\)；\(\cos(A\pm B)=\cos A\cos B\mp\sin A\sin B\)"},
            {"k": "倍角／降冪", "v": r"\(\sin2\theta=2\sin\theta\cos\theta\)；\(\cos2\theta=1-2\sin^2\theta\)；\(\sin^2\theta=\frac{1-\cos2\theta}{2}\)"},
            {"k": "疊合", "v": r"\(a\sin x+b\cos x=\sqrt{a^2+b^2}\,\sin(x+\varphi)\)，極值 \(\pm\sqrt{a^2+b^2}\)"},
            {"k": "圖形", "v": r"\(y=a\sin(bx+c)+d\)：振幅 \(|a|\)、週期 \(\frac{2\pi}{|b|}\)"},
            {"k": "圓周角", "v": r"＝圓心角一半；直徑所對 \(=90°\)；內接四邊形對角互補"},
            {"k": "角平分線", "v": r"\(\angle A\) 平分線：\(\dfrac{BD}{DC}=\dfrac{AB}{AC}\)"},
        ],
        "checklist": [
            r"\(\cos(A+B)=\cos A\cos B-\sin A\sin B\)（cos 符號相反）。",
            r"\(\sin2\theta=2\sin\theta\cos\theta\)，**不是** \(2\sin\theta\)。",
            r"\(a\sin x+b\cos x\) 的最大值是 \(\sqrt{a^2+b^2}\)，**不是** \(a+b\)。",
            r"同一三角形 **大角對大邊**；\(\sin\) 在 \(0°\)–\(90°\) 增、\(\cos\) 減。",
            r"弧長 \(r\theta\)、扇形面積 \(\frac12 r^2\theta\) 的 \(\theta\) 一定用 **弧度**。",
            r"\(\cos x°\)（度）\(\neq\cos x\)（弧度），先統一單位。",
            r"圓周角 ＝ 圓心角的 **一半**；圓內接四邊形對角 **互補**。",
            r"角平分線分對邊成 **兩鄰邊之比** \(BD:DC=AB:AC\)。",
            r"SSA（兩邊一對角）可能 **兩解**，要判定。",
            r"相似三角形面積比 ＝ 邊長比的 **平方**。",
        ],
    },
}
