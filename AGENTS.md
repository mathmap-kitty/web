# AGENTS.md — 給接手 AI 的專案指南

> **這份是「怎麼做」的常駐規範**；「現在做到哪」看同層的 `handoff.md`。
> 兩份都在 repo 根目錄 `D:\web`。開工前兩份都讀。

---

## 0. 專案是什麼

高中數學教師游心怡（Kitty）的**學測數學 A 自學教材網**，已上線 GitHub Pages。
- Repo：`D:\web` → `https://github.com/mathmap-kitty/web`
- 網址：`https://mathmap-kitty.github.io/web/`（根目錄是**總入口 portal**）
- 一切工作以「**可發布、可累積的作品**」為終點；教學內容的最終判斷權在老師。

## 1. 三個子站（各自獨立、來源不同）

| 子站 | 網址 | 內容 | 來源與更新方式 |
|---|---|---|---|
| `concept-map/` | `/web/concept-map/` | **學測數學重點整理**：11 單元 × 58 考點，含互動練習、三張地圖 | **本 repo 內**：`content/*.py` → `python build/build.py` → `dist/` → 覆蓋正式 `.html` |
| `exam/` | `/web/exam/` | 111–115 學測數A・數B 逐題互動詳解（200 題） | **本機外部**：`D:\大考複習\歷屆試題詳解\互動網頁版\` → 整包覆蓋 `exam/` |
| `guide/` | `/web/guide/` | 《學測數學A 複習講義》網頁版（13 章＋附錄） | `content/guide_data.json` ＋ `build/build_guide.py`（另一 session 建置，本 agent 未親自驗證） |

> **本 repo 的 build 只管 `concept-map/` 與 `guide/`；`exam/` 不要在這裡改。**

## 2. 資料夾結構

```
D:\web\
├── index.html              # 總入口 portal（手寫維護，非 build 產生）
├── AGENTS.md               # 本檔：常駐規範
├── handoff.md              # 目前進度與下一步
├── README.md               # 站台結構說明
├── sitemap.xml             # 由 concept-map/build/gen_sitemap.py 產生
├── 404.html / favicon.svg / apple-touch-icon.png / og-cover.png
├── 任務書_SOIL認知優化_2026-07-10.md   # ⚠️ 已 gitignore（內部文件，本機保留不發布）
│
├── concept-map/            # ① 重點整理子站
│   ├── 115學測數學_<單元>.html      # 11 個單元頁（正式檔，由 build 產生後覆蓋）
│   ├── 115學測數學_概念地圖.html      # 三視圖地圖（依賴鏈／熱度／概念網）
│   ├── 115學測數學_解題線索地圖.html   # 關鍵字 → 知識點
│   ├── 115學測數學_跨單元整合_脈絡地圖.html  # 25 題跨單元題卡
│   ├── 115學測數學_待複習與錯題.html   # 全站彙整頁
│   ├── index.html                  # 子站目錄首頁（手寫維護）
│   ├── content-overview.html / exam-trend-analysis.html  # 兩張獨立分析頁（不連進導覽）
│   ├── katex/                      # KaTeX 0.16.11 本地包（2026-07 起不走 CDN）
│   ├── content/                    # ★ 內容單一來源
│   │   ├── <slug>.py × 11          # 各單元（trig/prob/space/poly/linecir/
│   │   │                           #   explog/pvec/data/seq/matrix/numexpr）
│   │   ├── units.py                # 單元註冊表＋四大主題分組 SECTIONS
│   │   ├── checks.py               # 「確認理解」題庫（每考點 2 題微集）
│   │   ├── part2_kp.py             # Part2 各題對應考點（★位置制，見雷區）
│   │   ├── cues.py                 # 解題線索（線索地圖＋考點🔑標籤）
│   │   ├── soil_maps.py            # 各單元知識地圖 SVG（含「帶走一句話」）
│   │   ├── openers.py / corr_figs.py     # Part0 開場圖／相關係數教學圖
│   │   └── guide_data.json         # guide/ 子站內容來源
│   ├── build/
│   │   ├── build.py                # ★ 主建置（先跑 validate 再產單元頁＋docx）
│   │   ├── build_html.py           # 單元頁版型（最核心）
│   │   ├── build_docx.py / render.py / tex2omml.py   # Word 產出與富文字引擎
│   │   ├── build_conceptmap.py / build_cluemap.py / build_cross.py
│   │   ├── build_review.py / build_overview.py / build_trend108.py
│   │   ├── build_guide.py / docx2guide.py            # guide/ 子站
│   │   ├── gen_sitemap.py / pdf_figs.py / validate.py
│   │   └── assets/{style.css, app.js, guide-figs/}   # 單元頁共用 CSS/JS
│   ├── dist/                       # 建置產物（gitignore）
│   └── 參考文件/                    # 官方試卷 PDF 等（gitignore，超大檔）
│
├── exam/                   # ② 歷屆試題子站（源頭在本機外部，勿在此改）
└── guide/                  # ③ 複習講義子站（13 章＋附錄＋katex/＋img/）
```

## 3. 建置與發布流程

```bash
cd D:/web/concept-map
PYTHONUTF8=1 python build/build.py            # 全部 11 單元（含 validate 守門）
PYTHONUTF8=1 python build/build.py <slug>     # 單一單元
PYTHONUTF8=1 python build/build_conceptmap.py # 三視圖地圖（改地圖才要跑）
```
然後**逐檔列名**把 `dist/` 的產物複製到 `concept-map/` 正式位置 → 預覽驗證 → commit。

- **絕不直接改** `concept-map/` 根目錄的正式 `.html`：改 `content/*.py` 或 `build/*.py`，用 build 產出。
- **push 前先 `git fetch`**：這個 repo 常有多個 session 平行工作，rebase 後再 push。
- commit 訊息結尾：`Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

## 4. 開發鐵則（踩過的坑，別再踩）

### 4.1 KaTeX（最大雷）
- **不可用後代選擇器碰含數學容器內的 span**（如 `.opts span`）——KaTeX 會產生大量內部 `<span>`，排版會整個散掉。一律用**子選擇器** `.opts > span` 或 **class 專屬** `.blank .a`。
- **任何 CSS 改動後，必用「矩陣」單元頁目視／DOM 驗證數學式沒散**（矩陣式最容易看出來：檢查 `.katex .mtable` 數量與 vlist 列數，別只量高度——高度會有假象）。
- 互動元件慣例：`<button class="sol-btn" onclick="ts(this)">` **後面必須緊接它的 `.sol`**；`ts()` 用 `nextElementSibling` 找。
- 數學式轉義：矩陣欄分隔 `&` 寫 `&amp;`；不等號用 `\lt \gt \le \ge \neq`。

### 4.2 資料耦合
- `content/part2_kp.py` 是**位置制**：Part2 第 n 題對應第 n 個考點。**改題序必須同步改這張表**，否則「解題核心回考點」全部錯位。`build/validate.py` 會擋長度不符，但擋不了「順序錯但長度對」——改動後務必逐題驗證 tag→kp 配對。
- `checks.py` 的 `answer` 是 **1-based list**；Part0 直覺挑戰 `challenge.answer` 是 **0-based index**。兩者別搞混。

### 4.3 建置與環境
- `cp dist/115學測數學_*.html .` 會把 dist 裡的**舊地圖頁**一起蓋掉 → **逐檔列名複製**。
- `build_conceptmap.py` 裡 JS 是寫在 Python 字串內：**註解要用 Python 的 `#`，不是 `//`**。
- dist 子資料夾內的樣張要預覽，KaTeX 路徑得改成 `../katex/` 才會渲染。
- `requestIdleCallback`／`rAF` 在**離屏 iframe 與背景分頁會被餓死** → 排程一律加 `setTimeout` 後備。
- 一次驗證 4 頁以上容易讓預覽逾時，分批 2–3 頁。

## 5. 內容品質規範（老師定調，不可自行放寬）

1. **不憑記憶生成官方題目**。歷屆題一律對官方原卷校正：
   - 數A：`concept-map/參考文件/106~115學測數學試卷.pdf`
   - 數B：`concept-map/參考文件/111~115數學b試卷含解答.pdf`
   - PDF 文字層抽取會吃掉負號／上下標 → 有疑慮就用 `fitz` 渲染該頁成 PNG 目檢。
   - **選項文字也要對**（曾發現占位文字「a值符合某條件」混進正式檔）。
2. **只用 108 課綱數A 範圍的解法**：不得出現微積分（`f'`、`∫`）、托勒密、arcsin、核空間等課綱外工具；環狀排列、重複組合 `H` 不在數A。
3. **命題原則（2026-07-10 老師定調）**：情境**只用在數學原生處**（統計／機率／位數／半衰期／折扣／座位／星期）；其餘一律用「**換敘述**」做近遷移（反向問、求未知、換面貌）——**不要硬套生活情境**，會牽強。
4. 教學內容（題目文字、解析）**須經老師審核才算完成**，AI 只負責起草。
5. 用語：用「排容原理」不用「容斥原理」；公式挖空要挖「等號後整個右式」。

## 6. 路線圖 checklist

### 已完成
- [x] 11 單元 × 58 考點內容建置、全部上線
- [x] 三張地圖（概念地圖三視圖／解題線索／跨單元脈絡）
- [x] 互動系統：填空、顯示解答、練習即時批改、錯題記錄、進度追蹤、匯出學習紀錄、站內搜尋、待複習彙整
- [x] 考點×考題對應體檢 **A/B/C 包全修**（164 題反向檢核；去課綱外工具、補教學缺口、詳解補推導、跨單元先備標註）
- [x] **全站選項對卷複查 91 題**（修 4 處與官方原卷不符）
- [x] SOIL 認知優化 **A1**（解題核心預設收合，先判斷再對照）
- [x] SOIL **A2**（Part3「帶走一句話」回想，與知識地圖同源）
- [x] SOIL **B1**（Part0 直覺挑戰元件＋機率／三角／直線與圓 3 單元）
- [x] SOIL **B2**（header 捲動收合 ≤60px、錨點不遮字、概念地圖觸控與遮擋修正）
- [x] SOIL **C1**（確認理解升級 2 題微集：**11 單元 58 考點 116 題**，全數老師審核）
- [x] SOIL **D2**（強調色統一：琥珀橘 `--accent:#b45309` 只給判斷關鍵）
- [x] SOIL **D3**（概念地圖加「建議看法」一句）
- [x] SOIL **D4**（Part2 題序打散、交錯練習）
- [x] SOIL **D5**（KaTeX 漸進渲染＋全頁切換分段：revealAll 1034ms→4ms）
      ⚠️ 初版的「首屏 833ms→0」是**延到 DOMContentLoaded 後才渲染**換來的，不是分塊——
      當時 `_mmChunks()` 只掃 body 層找 `.card`，整個 `.wrap` 是單一分塊，分塊從沒生效。
      已於 `1d96bf5` 修好（下探 `.wrap`／`.card`）：矩陣頁 11→137 塊、最長單次凍結 106ms→21ms。
- [x] KaTeX 本地化、sitemap、favicon、自訂 404、行動版 sticky 壓縮（**其他 session**）
- [x] `guide/` 複習講義子站 13 章（**其他 session**，在 `feat/guide-web-version` 分支）

### 待辦
- [ ] **`feat/guide-web-version` 合併回 `main`**，並決定 guide 是否連進總入口導覽
- [ ] SOIL **D1**：知識地圖上方加一行使用指引（老師說「先不做」，隨時可撿）
- [ ] **B1 直覺挑戰擴充**到其餘 8 單元（現只有 3 個高頻單元有）
- [ ] **借鏡 ChatGPT 試作版 docx 的 B 方案**（老師尚未定案）：①「式／根／圖」表示選擇框架 ②錯誤代碼 → 回補考點閉環，接上現有待複習頁
- [ ] `exam/` 數B 空間向量考點待補（該子站源頭在本機外部）
- [ ] 好好學《焦點》精修 Word：單元 3~15（另一條產線，與本 repo 無關）

### 已知不修
- D4 題序打散後，學生**舊**錯題紀錄的 `p2qN` 錨點會指到新位置的題（一次性、影響面小，新紀錄正常）。
