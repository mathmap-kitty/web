# -*- coding: utf-8 -*-
"""解題線索地圖的單一來源：題目線索／關鍵字 → 該用的核心概念（跨單元）。

同時餵給兩處，改一次兩邊同步：
  ① 獨立「解題線索地圖」頁：build/build_cluemap.py（依 cat 分類彙整）。
  ② 各核心概念旁「🔑 解題線索」標籤：build_html._cues_html（依 unit+kp 反查）。

每條 cue：cat 分類、kw 線索關鍵字、hint 一句怎麼用、unit+kp 連到的核心概念。
kw/hint 可含行內數學 \\( ... \\)（會經 html_rich 渲染）。
"""

# 分類（顯示順序＋圖示）：學生「想求什麼／看到什麼」
CATS = [
    ("max",     "🎯 求最大／最小值"),
    ("dist",    "📏 距離"),
    ("perp",    "⟂ 垂直・平行"),
    ("angle",   "📐 角度"),
    ("area",    "🔺 面積・體積"),
    ("relation", "🔗 數量關係（和・積・比）"),
    ("estimate", "🔢 位數・估計"),
    ("pattern", "🔁 規律・遞迴・週期"),
    ("prob",    "🎲 機率的線索字"),
]

# 「同一招、跨單元」概念群組（觸類旁通）：同一個工具在不同單元／不同題型重複出現。
# cue 標 "g"＝所屬群組；build 依 g 反查同群其他核心概念，做跨單元串連。
GROUPS = {
    "dot":   "內積這一招（\\(\\vec u\\cdot\\vec v\\)：垂直・夾角・正射影）",
    "det":   "行列式這一招（\\(ad-bc\\)：面積・平行・線性變換）",
    "ineq":  "不等式求極值（算幾／柯西）",
    "distf": "距離公式（點到直線／點到平面）",
}

CUES = [
    # 🎯 求最大／最小值
    {"cat": "max", "kw": r"二次式的極值", "hint": r"配方 → 看頂點", "unit": "poly", "kp": "kp2"},
    {"cat": "max", "kw": r"\(a\sin x+b\cos x\) 的最大值", "hint": r"疊合成 \(R\sin(x+\varphi)\)，最大 ＝ \(R=\sqrt{a^2+b^2}\)", "unit": "trig", "kp": "kp4"},
    {"cat": "max", "g": "ineq", "kw": r"（正數）和固定／積固定求極值", "hint": r"**務必是正數 \(a,b>0\)！**算幾不等式 \(\dfrac{a+b}{2}\ge\sqrt{ab}\)：和固定 → 積在 \(a=b\) 時最大；積固定 → 和在 \(a=b\) 時最小", "unit": "numexpr", "kp": "kp4"},
    {"cat": "max", "kw": r"\(px+qy\) 在可行域", "hint": r"線性規劃：只需檢查頂點", "unit": "linecir", "kp": "kp5"},
    {"cat": "max", "g": "ineq", "kw": r"柯西不等式", "hint": r"\((a^2+b^2)(x^2+y^2)\ge(ax+by)^2\)；平方和固定時求 \(ax+by\) 極值（等號在 \((a,b)\parallel(x,y)\)）", "unit": "pvec", "kp": "kp3"},

    # 📏 距離
    {"cat": "dist", "g": "distf", "kw": r"點到直線距離", "hint": r"\(\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}\)", "unit": "linecir", "kp": "kp1"},
    {"cat": "dist", "g": "distf", "kw": r"點到平面距離", "hint": r"\(\dfrac{|ax_0+by_0+cz_0-d|}{\sqrt{a^2+b^2+c^2}}\)", "unit": "space", "kp": "kp4"},
    {"cat": "dist", "kw": r"兩點距離／中點", "hint": r"坐標差平方和開根號", "unit": "linecir", "kp": "kp2"},
    {"cat": "dist", "kw": r"\(|x-a|\) 的意義", "hint": r"\(x\) 到 \(a\) 的距離", "unit": "numexpr", "kp": "kp2"},

    # ⟂ 垂直・平行
    {"cat": "perp", "g": "dot", "kw": r"向量垂直", "hint": r"內積 ＝ 0", "unit": "pvec", "kp": "kp3"},
    {"cat": "perp", "kw": r"兩直線垂直", "hint": r"斜率相乘 ＝ \(-1\)", "unit": "linecir", "kp": "kp1"},
    {"cat": "perp", "g": "det", "kw": r"向量平行（共線）", "hint": r"\(ad-bc=0\)", "unit": "pvec", "kp": "kp1"},
    {"cat": "perp", "kw": r"直線垂直平面", "hint": r"方向向量 ∥ 法向量", "unit": "space", "kp": "kp5"},

    # 📐 角度
    {"cat": "angle", "kw": r"三角形求角", "hint": r"餘弦定理 \(\cos C=\dfrac{a^2+b^2-c^2}{2ab}\)", "unit": "trig", "kp": "kp2"},
    {"cat": "angle", "g": "dot", "kw": r"兩向量夾角", "hint": r"\(\cos\theta=\dfrac{\text{內積}}{\text{兩長度乘積}}\)", "unit": "pvec", "kp": "kp3"},
    {"cat": "angle", "kw": r"直線的傾角", "hint": r"斜率 ＝ \(\tan\theta\)", "unit": "linecir", "kp": "kp1"},
    {"cat": "angle", "kw": r"求非特殊角的 \(\sin/\cos\)", "hint": r"拆成兩特殊角，用和差角公式", "unit": "trig", "kp": "kp5"},
    {"cat": "angle", "g": "dot", "kw": r"二面角", "hint": r"兩平面法向量的夾角", "unit": "space", "kp": "kp6"},

    # 🔺 面積・體積
    {"cat": "area", "g": "det", "kw": r"平行四邊形／三角形面積", "hint": r"\(|\)行列式 \(ad-bc|\)（三角形再 ÷2）", "unit": "pvec", "kp": "kp4"},
    {"cat": "area", "kw": r"三角形面積（有夾角）", "hint": r"\(\dfrac12 ab\sin C\)", "unit": "trig", "kp": "kp2"},
    {"cat": "area", "kw": r"三邊求三角形面積", "hint": r"海龍公式", "unit": "trig", "kp": "kp2"},
    {"cat": "area", "kw": r"空間面積／體積", "hint": r"外積長度／純量三重積 \(|\vec u\cdot(\vec v\times\vec w)|\)", "unit": "space", "kp": "kp3"},
    {"cat": "area", "g": "det", "kw": r"圖形變換後的面積", "hint": r"原面積 \(\times|\det M|\)", "unit": "matrix", "kp": "kp5"},

    # 🔗 數量關係（和・積・比）
    {"cat": "relation", "kw": r"已知 \(a+b,\ ab\) 求 \(a^2+b^2\)", "hint": r"對稱式：用和與積表示", "unit": "numexpr", "kp": "kp4"},
    {"cat": "relation", "kw": r"分點／內分比例", "hint": r"分母比例和、分子交叉乘", "unit": "pvec", "kp": "kp2"},
    {"cat": "relation", "kw": r"三數成等差／等比", "hint": r"等差中項 \(2b=a+c\)；等比中項 \(b^2=ac\)", "unit": "seq", "kp": "kp1"},
    {"cat": "relation", "kw": r"面積比讀成係數", "hint": r"\(\overrightarrow{AP}=\alpha\overrightarrow{AB}+\beta\overrightarrow{AC}\Rightarrow\) 比看係數", "unit": "pvec", "kp": "kp2"},

    # 🔢 位數・估計
    {"cat": "estimate", "kw": r"幾位數／數量級", "hint": r"取常用對數，位數 ＝ \([\log N]+1\)", "unit": "explog", "kp": "kp3"},
    {"cat": "estimate", "kw": r"\(\sqrt N\) 在哪兩整數間", "hint": r"夾在相鄰完全平方數之間", "unit": "numexpr", "kp": "kp3"},
    {"cat": "estimate", "kw": r"高斯符號 \([x]\)", "hint": r"不超過 \(x\) 的最大整數", "unit": "numexpr", "kp": "kp6"},

    # 🔁 規律・遞迴・週期
    {"cat": "pattern", "kw": r"遞迴 \(a_{n+1}=pa_n+q\)", "hint": r"找不動點 → 構造等比", "unit": "seq", "kp": "kp3"},
    {"cat": "pattern", "kw": r"矩陣高次方 \(A^n\)", "hint": r"先算 \(A^2\)，湊 \(kI\) 或凱萊–漢米頓降冪", "unit": "matrix", "kp": "kp2"},
    {"cat": "pattern", "kw": r"循環／週期的第 \(n\) 項", "hint": r"除以週期看餘數定位", "unit": "seq", "kp": "kp4"},
    {"cat": "pattern", "kw": r"證明對所有 \(n\) 成立", "hint": r"數學歸納法", "unit": "seq", "kp": "kp3"},

    # 🎲 機率的線索字
    {"cat": "prob", "kw": r"「至少一個」", "hint": r"算餘事件 \(1-P(\text{都不})\)", "unit": "prob", "kp": "kp5"},
    {"cat": "prob", "kw": r"「已知…求…的機率」", "hint": r"條件機率：分母換成已知範圍", "unit": "prob", "kp": "kp4"},
    {"cat": "prob", "kw": r"「互不影響／獨立」", "hint": r"機率相乘", "unit": "prob", "kp": "kp5"},
    {"cat": "prob", "kw": r"「期望／平均可得」", "hint": r"\(\sum(\text{值}\times\text{機率})\)", "unit": "prob", "kp": "kp6"},
    {"cat": "prob", "kw": r"「恰好 \(k\) 個」", "hint": r"組合 \(C\) 計數", "unit": "prob", "kp": "kp2"},
]
