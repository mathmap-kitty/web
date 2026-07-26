# 學測數學重點整理 — 交接文件（給 Claude Code）

> 用途：把這份連同檔案一起交給 Claude Code，讓它接手「數學單元 → 互動學習網頁」這個專案。
> **2026-07 註記**：本專案已整包搬入 repo 的 `concept-map/` 子資料夾（網址 `…/web/concept-map/`），
> repo 根目錄改為全站總入口。文中提到的「同一資料夾／根目錄」皆指 `concept-map/` 這一層。

---

## 一、專案目標
把老師的數學教材（Word／PDF）轉成**學生用的互動式學習網頁**。每個單元一頁，含「填空點按顯示」「按鈕顯示解答」等互動；多個單元用一個**目錄首頁**串起來，最後部署成網址發給學生。

---

## 二、目前已產出的檔案
（目前都在同一個資料夾；建議整包複製到一個新資料夾並 `git init`）

| 檔案 | 說明 |
|------|------|
| `index.html` | **目錄首頁／網站入口**，列出所有單元 → 考點的樹狀連結 |
| `115學測數學_矩陣.html` | 第一個單元頁（矩陣），同時是**樣板範例**，新單元照它的結構做 |
| `單元資料範本.docx` | 給老師填「單元內容」的範本（= 內容輸入格式） |
| `make_template.py` | 產生上面那份 .docx 的腳本（python-docx） |
| 原始教材 | 矩陣這份的來源是老師的 Word／PDF／截圖；其他單元請向老師索取原始檔 |

---

## 三、技術棧與重要慣例
- 純前端、單一 HTML 檔，CSS + 原生 JS，**無框架**。
- 數學排版：**KaTeX 0.16.9（cdnjs）+ auto-render**；行內用 `\(...\)`、獨立行用 `\[...\]`。

### ⚠️ 最重要的雷（務必遵守）
**不要用「後代選擇器」去設定含數學的容器內的 span**，例如 `.opts span { ... }`。
KaTeX 會在數學式內部產生**大量 `<span>`**，這種選擇器會套到那些內部 span，把矩陣／上下標的排版整個打散（曾經來回除錯很多次才找到）。
→ 一律改用**子選擇器** `.opts > span`，或 **class 專屬選擇器** 如 `.blank .a`。

### 互動元件（JS 函式都放在單元頁底部）
- 填空：`<span class="blank" onclick="tb(this)"><span class="q">？</span><span class="a">答案</span></span>`；`tb()` 切換 `.on`。
- 顯示解答：`<button class="sol-btn" data-s="顯示解答" data-h="隱藏解答" onclick="ts(this)">…</button><div class="sol">…</div>`；`ts()` 切換**緊鄰的下一個** `.sol`。**所以按鈕後面必須緊接它的 `.sol`**。
- 全頁切換：`revealAll()` / `hideAll()`。
- KaTeX 渲染包在 try/catch、於 DOMContentLoaded 觸發；**隱藏（display:none）的內容也會先被渲染**，所以「先渲染、之後再用 CSS 切換顯示」不會出問題。

### 在 HTML 裡寫 KaTeX 的轉義
- 矩陣欄分隔 `&` 要寫成 `&amp;`；列分隔用 `\\`（兩個反斜線）。
- 不等號用 `\lt` `\gt` `\le` `\ge` `\neq`，**不要**在數學裡直接打 `<`、`>`（會被 HTML 當標籤）。

### 導覽與錨點
- 置頂工具列（`position:sticky; top:0`）：標題、`單元 ▾`（跨單元，用 `location.href`）、`跳至考點 ▾`（同頁，用 `location.hash`，跳完 reset `selectedIndex`）、全部顯示／隱藏。
- 每個考點卡片 `id="kp1"…"kp5"`；Part 2／3 `id="part2"`／`"part3"`；以 `scroll-margin-top:64px` 處理 sticky 遮擋。
- `index.html` 用相對路徑 + `#錨點` 連到單元頁。

### 視覺
- 主色酒紅 `#8c2740`、答案紅 `#c0392b`、按鈕青 `#1f6f78`、底色 `#f7f2ee`；卡片式版面；支援 RWD（手機）。
- 中文字型：`Microsoft JhengHei` / `PingFang TC` / `Noto Sans TC`。

---

## 四、每個單元的內容結構（＝ .docx 範本欄位）
- **Part 1 各考點**：① 考點標題 ② 這個考點在學什麼 ③ 重點與公式 ④ 常見誤解 ×→○（表） ⑤ 歷屆試題（題目＋簡答＋解題關鍵） ⑥ 解題策略
- **Part 2 模擬實戰**：每題＝題目＋選項＋答案＋詳解
- **Part 3 考前速查**：公式速查表 ＋ 常見誤解清單

**內容轉換約定**：範本中用 **【 】** 框起來的＝要做成「填空」；常見誤解的「正解」、歷屆／練習的「簡答、詳解」→ 自動做成「顯示解答」按鈕。

---

## 五、新增一個單元的步驟（目前是手工，可改善）
1. 拿老師填好的 .docx／文字。
2. 複製 `115學測數學_矩陣.html`，替換內容（沿用所有 class 與 JS）。
3. 在 `index.html` 加一張單元卡片（含考點子連結）。
4. 在**每個**單元頁的「單元 ▾」下拉，加上新單元的選項。← 目前各頁各自硬寫，有重複維護成本。

---

## 六、建議 Code 接手後做的優化
- **資料與樣板分離**：把每個單元寫成資料檔（JSON 或 Markdown），用一支 Node 建置腳本、或 SSG（Astro／Eleventy）由樣板自動生出各單元頁與 `index.html`，並**集中管理單元清單**（解決第五點的重複維護）。
- **KaTeX 改為本地打包**，支援完全離線（學校網路較保險）。
- 加值功能：作答進度記錄（localStorage）、站內搜尋、深色模式。
- 用 **git** 版本控管；部署到 **GitHub Pages / Netlify / Cloudflare Pages**（整個資料夾上傳，`index.html` 當入口，把它的網址發給學生）。
- 檔名建議改 **ASCII**（如 `matrix.html`）以避免中文檔名在某些主機的編碼問題；**若改名，務必同步更新** `index.html` 與各頁「單元 ▾」下拉的連結。

---

## 七、交接時你（使用者）要做的事
1. 把目前資料夾的檔案複製到一個新資料夾，最好先 `git init`。
2. 用 Claude Code 打開該資料夾，把**這份 `交接文件_給Claude_Code.md`** 一起給它。
3. 附上各單元的**原始教材**（老師的 Word／PDF／截圖）。
4. 告訴它下一步目標（例：先做「資料／樣板分離」，再新增「三角函數」單元）。

---

## 八、環境備註
- 這些檔案是在 Cowork 環境產生的；`.docx` 用 `python-docx` 製作（`make_template.py`）。Claude Code 在一般開發環境，工具更自由，可自行選用 Node／Python／SSG。
- KaTeX 目前走 CDN，開啟需連網；要離線發佈再改本地打包即可。

---

## 九、《學測數學A 複習講義》網頁版（2026-07 新增；站台根的 `guide/`）

老師另有一份上課用的 Word 講義（全教用＝答案玫瑰色、全學用＝底線挖空），已轉成網頁版。
**它是獨立子站，不屬於 concept-map**（老師的定位：那是重點整理、這是上課講義）：

```
/web/guide/              ← 發布位置，與 exam/ 同層；網址 …/web/guide/
    index.html           ← 目錄頁
    第01章_…html ～ 第13章_…html、附錄_解二元一次聯立方程組.html
    img/                 ← 45 張圖（docx 內嵌 32 ＋ 從 PDF 裁的手繪圖 13）
    katex/               ← 自帶一份（與 exam/ 相同作法，不依賴 concept-map）
```
產線腳本仍放在 `concept-map/build/`（要共用 `build_html.py` 的分享卡／流量統計／頁尾與
`build/assets/` 的 CSS/JS），資料檔在 `concept-map/content/guide_data.json`。

### 產線（三支腳本，都在 `concept-map/` 下執行）
```
python build/pdf_figs.py --sheet   # ① 從教師版 PDF 裁 13 張 Word 手繪圖 → guide/img/（--sheet 出總覽圖供人工確認）
python build/docx2guide.py         # ② 教師版 .docx → content/guide_data.json（＋內嵌圖 32 張 → guide/img/）
python build/build_guide.py        # ③ JSON → /web/guide/*.html（第一次會複製 KaTeX）
python build/gen_sitemap.py        # ④ 頁面增減後重跑，更新 sitemap.xml
```
來源檔（不在 repo 內）：`D:\gmail\115\01_教學\複習講義\學測數A_脈絡複習講義_全教用.docx / .pdf`

### 原理與雷
- **答案怎麼認出來的**：`docx2guide.py` 先在 docx 裡把「玫瑰色 9C5A6E」的 run 用 `⟦…⟧` 包起來
  （OMML 數學式內的 `m:r` 也包），再交給 `pandoc -f docx+styles -t json`。
  段落樣式（SecHead／SubHead／NoteBox／HL）保留成 `custom-style`，數學式自動變 LaTeX。
- **數學式挖空的切法**：一條式子裡的標記會先合併成一段；切不出合法 LaTeX 時
  退回「整條式子當答案」，寧可整條變按鈕也不要讓 KaTeX 壞掉（`split_math`）。
- **KaTeX 0.16 不支援 `\mspace`**（會印出紅字原文）→ `_fix_tex()` 換成 `\,`。
- **Word 手繪圖（`w:pict` VML）pandoc 完全看不到**：指對數圖形、解的三種情形、
  點到直線示意圖等 13 張，改用 `pdf_figs.py` 從 PDF 座標裁圖；安插位置寫在
  `docx2guide.py` 的 `TABLE_FIGS` / `EMPTY_ROW_FIGS` / `AFTER_FIGS`。
- **`.wmf` 舊式方程式物件**瀏覽器不能顯示 → `WMF_TEX` 直接改寫成 LaTeX。
- 圖片寬度一律 `max-width:min(100%,Npx)`，寫死 px 會讓手機出現橫向捲動。
- 講義頁沿用 `build/assets/style.css` 與 `app.js`（`tb()`／`revealAll()`／漸進渲染都直接重用），
  講義專屬樣式集中在 `build_guide.py` 的 `GUIDE_CSS`；分享卡網址前綴不同，
  `build_guide.py` 自己有一份 `og_meta()`（指向 `…/web/guide/`）。
- **原稿一對一對不上的地方**，都集中成表格，改了原稿要回來看：
  `TYPO_FIXES`（錯字，如「空間中個元素」→「各元素」）、`fix_intercept_annot()`
  （截距式 (a,0)/(0,b) 掛回對應詞下方）、`split_off_appendix()`（第13章章末補充獨立成頁）。
  對不上會在建置時印警告。
- 章末「考場心法」在 Word 是 HL 樣式、後面可能還接幾句同框的句子 → `_tidy()` 會併回心法框，
  否則會被誤判成章末補充。
