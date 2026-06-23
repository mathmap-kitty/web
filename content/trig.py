# -*- coding: utf-8 -*-
r"""三角單元 · 單一來源內容。

歷年題數之冠（106–115 合計 30.6 題），命題主戰場。例題以官方原卷校正。
※ 本檔目前含 Part 0＋考點 1（三角比/弧度）；考點 2–7 與 Part 2/3 待補。
"""

import openers  # Part 0 開場視覺概念圖（含老師 Q 版角色）

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
        "opener": {"svg": openers.OPENERS["trig"], "full": True,
                   "caption": r"**必考重點地圖**：基礎＝三角比·單位圓；兩大主幹——**解三角形**（正餘弦定理★★ → 測量·面積）、**三角函數**（圖形疊合★★★、和差·倍角★★★）。星越多＝越常考"},
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
                {"svg": SVG_GEN_ANGLE, "caption": r"廣義角：**值** 看與 \(x\) 軸的夾角、**正負** 看象限"},
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
            "questions": [
                {"tag": "109 舊制 · 單選 1", "level": "★☆☆（易）", "core": "三角比的定義與比大小",
                 "body": r"已知兩個直角三角形三邊長分別為 \(3,4,5\) 與 \(5,12,13\)，\(\alpha\)、\(\beta\) 分別為它們的一角，其中 \(\alpha\) 的對邊為 \(3\)、\(\beta\) 的對邊為 \(5\)。試比較 \(\sin\alpha\)、\(\sin30°\)、\(\sin\beta\) 的大小。",
                 "options": [r"\(\sin\alpha\gt\sin\beta\gt\sin30°\)", r"\(\sin\alpha\gt\sin30°\gt\sin\beta\)", r"\(\sin\beta\gt\sin\alpha\gt\sin30°\)", r"\(\sin\beta\gt\sin30°\gt\sin\alpha\)", r"\(\sin30°\gt\sin\alpha\gt\sin\beta\)"],
                 "solution": {"brief": r"(2)",
                              "steps": [r"\(\sin\alpha=\dfrac35=0.6\)、\(\sin\beta=\dfrac{5}{13}\approx0.385\)、\(\sin30°=0.5\)。",
                                        r"故 \(\sin\alpha\,(0.6)\gt\sin30°\,(0.5)\gt\sin\beta\,(0.385)\)，選 (2)。"]}},
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
            "intro": r"已知三角形的部分邊角，求其餘。**看題目給什麼選工具**：給兩角一邊用正弦定理；給兩邊夾角或三邊用餘弦定理。這是三角 **★★★ 必考核心**，幾乎年年出現。",
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
            "selfcheck": {
                "q": r"三角形中 \(a=7,\,b=5\)，夾角 \(C=60^\circ\)，求 \(c\)。",
                "a": r"**\(\sqrt{39}\)**：餘弦定理 \(c^2=49+25-2\cdot7\cdot5\cdot\frac12=39\)。"},
            "strategy": [
                r"先看 **給了什麼**：兩角一邊 → 正弦定理；兩邊夾角或三邊 → 餘弦定理。",
                r"SSA（兩邊一對角）務必判 **對邊 vs 鄰邊** 大小，小心兩解。",
                r"求面積優先用 \(\dfrac12 ab\sin C\)（兩邊夾角）；給三邊才用海龍。",
            ],
        },
        {
            "num": "考點 3", "id": "kp3", "nav": "三角測量與幾何應用",
            "title": r"三角測量與平面幾何應用",
            "intro": r"把三角比、正餘弦定理用到「測量」與平面幾何：**仰角、俯角、方位角** 的實際問題，以及「**大角對大邊**」與射影的判定。",
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
            "intro": r"三角函數的圖形——**週期、振幅、對稱軸／對稱中心**，以及最重要的「**疊合**」：把 \(a\sin x+b\cos x\) 併成單一正弦波。是三角 **★★★ 必考核心**。",
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
            "intro": r"和差角、倍角公式是「把複合角拆開／合併」的工具，常用來 **解三角方程式與不等式**。是三角 **★★★ 必考核心**，魔王題（\(114\) 選17、\(115\) 選17）也靠它。",
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
            "intro": r"三角形裡的各種「比」——角平分線分對邊的比、面積比、相似比。常與正弦面積公式、平面向量整合（\(111\) 選15、\(114\) 多11）。",
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
            "questions": [
                {"tag": "觀念範例（角平分線）", "level": "★★☆（中）", "core": "角平分線定理＋分點",
                 "body": r"\(\triangle ABC\) 中 \(AB=6\)、\(AC=4\)，\(\angle A\) 的內角平分線交 \(BC\) 於 \(D\)。若 \(BC=5\)，求 \(BD\)。",
                 "solution": {"brief": r"\(BD=3\)",
                              "steps": [r"角平分線定理 \(\dfrac{BD}{DC}=\dfrac{AB}{AC}=\dfrac64=\dfrac32\)，且 \(BD+DC=BC=5\)，",
                                        r"故 \(BD=5\times\dfrac{3}{3+2}=3\)。"]}},
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
            "intro": r"圓裡的角與三角結合——圓周角定理、外接圓與正弦定理，以及立體中的二面角。常出魔王／混合題（\(111\) 混18–20、\(114\) 選17）。",
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
                {"tag": "練習 4", "level": "★★☆", "core": "餘弦定理",
                 "body": r"\(\triangle ABC\) 中 \(b=2\)、\(c=3\)、\(\angle A=60°\)，則 \(a=\) ？",
                 "options": [r"\(\sqrt5\)", r"\(\sqrt6\)", r"\(\sqrt7\)", r"\(\sqrt{10}\)", r"\(\sqrt{13}\)"],
                 "solution": {"brief": r"(3) \(\sqrt7\)", "brief_label": "答",
                              "steps": [r"\(a^2=b^2+c^2-2bc\cos A=4+9-2\cdot6\cdot\dfrac12=13-6=7\)，故 \(a=\sqrt7\)。"]}},
                {"tag": "練習 5", "level": "★★☆", "core": "疊合求極值",
                 "body": r"\(\cos x-\sin x\) 的最大值為？",
                 "options": [r"\(1\)", r"\(\sqrt2\)", r"\(\sqrt3\)", r"\(2\)", r"\(0\)"],
                 "solution": {"brief": r"(2) \(\sqrt2\)", "brief_label": "答",
                              "steps": [r"\(\cos x-\sin x=\sqrt{1^2+(-1)^2}\,\sin(x+\varphi)=\sqrt2\sin(x+\varphi)\)，最大值 \(\sqrt2\)。"]}},
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
                {"tag": "練習 7", "level": "★★☆", "core": "二倍角",
                 "body": r"設 \(\theta\) 為銳角且 \(\sin\theta=\dfrac45\)，則 \(\sin2\theta=\) ？",
                 "solution": {"brief": r"\(\dfrac{24}{25}\)", "brief_label": "答",
                              "steps": [r"\(\cos\theta=\dfrac35\)，\(\sin2\theta=2\sin\theta\cos\theta=2\cdot\dfrac45\cdot\dfrac35=\dfrac{24}{25}\)。"]}},
                {"tag": "練習 8", "level": "★★☆", "core": "角平分線定理",
                 "body": r"\(\triangle ABC\) 中 \(AB=8\)、\(AC=6\)，\(\angle A\) 的內角平分線交 \(BC\) 於 \(D\)。若 \(BC=7\)，則 \(BD=\) ？",
                 "solution": {"brief": r"\(4\)", "brief_label": "答",
                              "steps": [r"\(\dfrac{BD}{DC}=\dfrac{AB}{AC}=\dfrac86=\dfrac43\)，故 \(BD=7\times\dfrac{4}{4+3}=4\)。"]}},
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
