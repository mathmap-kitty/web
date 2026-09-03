# 選修數學甲（上）互動教具

九個「拉滑桿看極限」的網頁教具，外觀沿用 mathmap 網頁風格標準 v1
（酒紅頂欄、暖米白底、白卡片、KaTeX 本地包）。**整個資料夾自成一包，
不需要網路**，複製到隨身碟、或整包丟進 `Mathmap_workspace/` 當子站都可以。

| 檔案 | 教什麼 | 對應簡報 |
|---|---|---|
| `index.html` | 目錄（依課本順序分三章） | — |
| `epsilon.html` | ε 帶子與 N、δ：拉 ε 自動找門檻，找不到 = 極限不存在 | 1-1 P20、1-4 P12 |
| `geoseries.html` | 無窮等比級數填正方形：數線走步、Sₙ 圖、\|r\|≥1 發散 | 1-2 P6–P12 |
| `secant.html` | 割線變切線：h → 0、斜率表、跟著 h 放大、尖點無切線 | 2-1 P6–P12 |
| `derivative.html` | 導函數長出來：把每點切線斜率描到下圖 | 2-1 P14–P16 |
| `concavity.html` | 增減與凹凸：f / f′ / f″ 三圖同步，極值與反曲點自動標記 | 2-2 P8–P20 |
| `riemann.html` | 黎曼和逼近：上和下和夾擠、五種取點、夾擠軌跡圖 | 3-1 P6–P14 |
| `ftc.html` | 面積函數長出來：F(x)=∫ₐˣ f(t)dt、F′(x)=f(x) 量給你看 | 3-1 P30–P31 |
| `solid.html` | 旋轉體切圓盤：截面長條 ↔ 圓盤、旋轉角 0°→360°、內接外接 | 3-2 P23–P27 |
| `cavalieri.html` | 祖暅原理：推歪體積不變；半球 = 圓柱 − 圓錐 推球體積 | 3-2 P19、P36 |

共用檔：

- `lab.css` — 色票與元件（頂欄、卡片、膠囊、滑桿、讀數、輸入列）
- `lab.js` — ① 運算式解析器 ② 數值工具 ③ `Lab.Plot` 畫布繪圖 ④ 共用 UI（chips / fnPanel / player）
- `katex/` — 從 `Mathmap_workspace/concept-map/katex/` 複製來的 KaTeX 0.16.11（css + js + fonts，1.5 MB）

## 自訂函數怎麼寫

每頁右欄「自己輸入」都吃同一套語法（`Lab.parseFn`）：

- 四則與次方：`x^2-2x+3`、`x^(1/2)`、`2^x`
- 隱含乘法：`2x`、`x(4-x)`、`(x+1)(x-2)`
- 函數：`sqrt`、`abs`、`sin`、`cos`、`tan`、`exp`、`ln`、`log`；`sinx` 也認得
- 常數：`pi`、`e`；也接受 `π`、`√`、`²`、`³`、全形括號
- 變數 `x` 或 `t` 都行（ftc 頁顯示成 t）
- 區間端點也走同一個解析器，所以可以填 `pi/2`

錯誤訊息會直接顯示在輸入列下方（括號沒配對、區間裡有算不出來的點……）。
自訂函數的「真值」用 Simpson 法數值積分，多項式、三角函數都準到小數第五位。

## 加新教具的做法

1. 複製任一頁當骨架（topbar → hero → `.deck`（stage + rail）→ copyright）。
2. 預設函數寫成 `PRESETS = [{id, src, a, b, note}]`，開頭用 `Lab.parseFn(p.src)` 補上 `f`、`tex`。
3. 畫圖用 `new Lab.Plot(ctx, box, [xlo,xhi], [ylo,yhi])`，有 `grid / axes / curve / rect / fillBetween / line / infLine / dot / text / tick`。
4. 自訂輸入用 `Lab.fnPanel(host, {varName, onApply})`；播放用 `Lab.player(btn, {tick})`。
5. 加進 `index.html` 一張入口卡。

## 已知取捨

- 只做亮色主題（mathmap 全站 `color-scheme:light`）。
- `solid.html` 的立體圖是斜投影（橢圓壓扁 0.30），不是真 3D；用意是看「長條 → 圓盤」，不是精準透視。
- 割線頁的切線是否存在用「h = ±10⁻⁵ 的左右割線斜率是否一致」判斷，所以 |x| 在 0、√x 在 0 都會正確顯示「不存在」。
- 本機預覽：在教材根目錄有 `.claude/launch.json`，或 `python -m http.server 8765 --directory 互動教具`。

## 共用程式補充

- `Lab.d1 / Lab.d2`：數值一、二階導數；`d1` 在左右差商不一致（尖點）時回傳 NaN，畫圖會自動斷開。
- `Lab.Plot.poly(xs, ys, opts, upto)`：畫取樣折線（NaN 斷開、可只畫到某索引）；`band(x0, x1, color, alpha)`：直向色帶。
- 解析器的變數可用 `x`、`t`、`n`（epsilon 頁的數列用 `n`）。
