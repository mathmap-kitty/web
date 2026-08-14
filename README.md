# mathmap 數學教材網（mathmap-kitty/web）

線上網址：**https://mathmap-kitty.github.io/web/index.html**

## 站台結構（2026-07 重整後）

```
web/
├── index.html        # 總入口 portal：列出所有教材的入口卡
├── og-cover.png      # portal 的社群分享卡封面
├── concept-map/      # ① 學測數學重點整理（11 單元核心概念地圖＋互動練習）
│   └── README.md     #    子站說明與建置管線（content/*.py → build/ → dist/）
├── exam/             # ② 歷屆試題練習（111–115 學測數學A 逐題互動詳解）
├── guide/            # ③ 學測數學A 複習講義（11 章＋附錄）
└── diagnostic/       # ④ 複習後診斷系統（⚠ 尚未對外公開，見下）
```

- **concept-map/**：正式頁面直接放在該資料夾內；重建流程見 `concept-map/README.md`
  （在 `concept-map/` 下跑 `python build/build.py`，輸出在 `dist/`，確認後覆蓋 `concept-map/` 內正式檔）。
- **exam/**：源頭在本機 `D:\大考複習\歷屆試題詳解\互動網頁版\`，更新＝整包覆蓋 `exam/` 再 push。
  exam 內的核心概念連結一律用相對路徑 `../concept-map/…`。
- **diagnostic/**：源頭在本機 `D:\gmail\ChatGPT_複習\診斷系統\`（見下節）。
- **新增教材**：在根目錄開新資料夾（自成一包、內部用相對連結），再到 `index.html` 加一張入口卡。

## diagnostic/（複習後診斷系統，尚未公開）

11 單元、540 題、58 核心概念的五階段診斷工具；作答紀錄只存在使用者瀏覽器（IndexedDB），無任何外部請求。

**目前狀態：檔案在 repo 內、隨 Pages 一起發布，但刻意沒有任何對外入口**——
`index.html` 沒有入口卡、`sitemap.xml` 不收錄、四張頁面都掛 `noindex,nofollow`。
原因：技術驗收全項通過，但驗收報告載明 Gate 5「真實學生實證」尚未補齊，故先自用試跑。

- 學生端：`/web/diagnostic/app/`（本機預覽 `http://localhost:8765/diagnostic/app/`）
- **教師端班級彙整：`/web/diagnostic/teacher/`**
- 驗收報告：`/web/diagnostic/review/final/system-final-acceptance-review.html`

```
diagnostic/
├── app/        # 學生端（index.html + main.mjs + repository.mjs + styles.css + vendor/katex）
├── teacher/    # 教師端班級彙整（index.html + app.js，純前端，不上傳檔案）
├── content/    # 題庫與知識結構 JSON（questions/<unit>/questions.json 等）
├── engine/     # diagnose.mjs 判讀引擎（無外部相依）
└── review/     # 驗收報告（內部文件，非學生教材）
```

### teacher/ 怎麼用

診斷系統**沒有後端**，老師看不到學生資料。要彙整全班：

1. 學生在「資料」頁按**匯出資料**，得到一個 JSON（含 SHA-256 完整性雜湊，
   且刻意**不含**姓名／學號／班級／Email——匯入時有正則主動擋掉這些欄位）
2. 學生把檔案存成 `座號01.json` 之類再交出來（Google Classroom 或 LINE）
   ——**檔名才是身分**，資料本身永遠匿名
3. 老師把整包檔案拖進 `teacher/`，得到：班級統計、**高信心答錯名單**、
   各核心概念分布、學生×核心概念矩陣；可匯出 CSV（含 BOM，Excel 直接開）或列印 PDF

檔名會自動剝掉 Google Classroom 的「姓名 - 檔名」前綴。被改過的檔案會標 ⚠ 並在 CSV 留備註。

⚠️ `teacher/app.js` 裡的 `UNITS` 表是從 `app/main.mjs` 的 `units` 複製過來的
（核心概念名稱），**兩邊改動要同步**。

**更新方式**：從 `D:\gmail\ChatGPT_複習\診斷系統\` 整包覆蓋 `app/ content/ engine/`。
資料夾結構刻意與源頭一致，所以子站內所有相對連結（`../engine/`、`../content/`、
`../app/vendor/katex/`）都能原樣沿用。覆蓋後只有兩處要補回：

1. `app/main.mjs` 的 `mathMapRoot`：需認得 `/diagnostic/app/` 並回傳 `'../../'`，
   否則「開啟概念圖／歷屆試題／MathMap 首頁」會指錯層。
2. `app/index.html` 的 `<meta name="robots" content="noindex,nofollow">`（公開前都要保留）。

**要正式上線時**：拿掉四張頁面的 `noindex`、在 `index.html` 把「🚧 更多教材籌備中」那張卡
換成診斷系統入口卡，並在 `concept-map/build/gen_sitemap.py` 加上 `diagnostic/` 後重跑。

## 網址慣例

- 重點整理單元頁＋核心概念錨點：`/web/concept-map/115學測數學_<單元名>.html#kp<N>`
- 2026-07 重整說明：重點整理原本放在 `/web/` 根目錄，已整包搬入 `concept-map/`；
  對外僅發布過首頁網址（原首頁位置由 portal 接手），且已發布 PPT 內的核心概念超連結已同步改為新路徑，故未留轉址頁。
