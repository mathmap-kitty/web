# 數學 互動學習講義

把老師的數學教材轉成**學生用的互動式網頁**：每個單元一頁，含「填空點按顯示答案」「按鈕展開解答」等互動；多個單元由一個目錄首頁串起，部署成網址供學生自行點閱。

---

## 檔案結構

```
.
├── index.html                         # 目錄首頁／網站入口（列出所有單元）
├── 115學測數學_矩陣_互動學習.html      # 單元頁：矩陣（也是新單元的樣板範例）
├── 單元資料範本.docx                   # 給老師填單元內容的範本（內容輸入格式）
├── make_template.py                   # 產生上述 .docx 的腳本（python-docx）
├── 交接文件_給Claude_Code.md           # 交接／開發細節（含完整慣例）
└── README.md                          # 本檔
```

> 部署時：所有 `.html` 要放在**同一層**（彼此用相對路徑＋`#錨點`連結）。`.docx`、`.py`、`.md` 是編輯／文件用，不需上傳。

---

## 本機預覽
直接用瀏覽器打開 `index.html` 即可（數學由 KaTeX 線上載入，開啟需連網）。

---

## 如何新增一個單元
1. 請老師用 `單元資料範本.docx` 填內容（或直接給文字）。
2. 複製 `115學測數學_矩陣_互動學習.html`，替換成新單元內容（沿用所有 class 與 JS）。
3. 在 `index.html` 新增一張單元卡片（含各考點子連結）。
4. 在**每個**單元頁的「單元 ▾」下拉，加入新單元選項。

**內容轉換約定**：範本中用 **【 】** 框的＝做成「填空」；「常見誤解的正解」「歷屆／練習的簡答、詳解」＝自動做成「顯示解答」按鈕。

每個單元的結構：Part 1 各考點（這個考點在學什麼／重點與公式／常見誤解 ×→○／歷屆試題／解題策略）、Part 2 模擬實戰、Part 3 考前速查。

---

## 開發慣例（重要）

- 純前端、單一 HTML 檔，CSS + 原生 JS，無框架。
- 數學：**KaTeX 0.16.9（cdnjs）+ auto-render**；行內 `\(...\)`、獨立行 `\[...\]`。

### ⚠️ 最大的雷：別讓 CSS 誤傷 KaTeX
**不要用後代選擇器**（如 `.opts span { ... }`）去設定含數學的容器內的 span —— KaTeX 會在數學式內部產生大量 `<span>`，這種選擇器會把它們一起套到，導致矩陣／上下標排版整個散掉。
→ 一律用**子選擇器** `.opts > span` 或 **class 專屬選擇器** `.blank .a`。

### 互動元件（JS 函式在單元頁底部）
- 填空：`<span class="blank" onclick="tb(this)"><span class="q">？</span><span class="a">答案</span></span>`
- 顯示解答：`<button class="sol-btn" data-s="顯示解答" data-h="隱藏解答" onclick="ts(this)">…</button><div class="sol">…</div>`（按鈕後**必須緊接**它的 `.sol`）
- 全頁切換：`revealAll()` / `hideAll()`
- KaTeX 在 DOMContentLoaded 渲染，且會渲染隱藏內容，故「先渲染再切換顯示」OK。

### HTML 裡寫 KaTeX 的轉義
- 矩陣欄分隔 `&` → 寫 `&amp;`；列分隔用 `\\`。
- 不等號用 `\lt` `\gt` `\le` `\ge` `\neq`，勿在數學中直接打 `<`、`>`。

### 導覽與配色
- 置頂工具列（sticky）：標題、單元 ▾、跳至考點 ▾、全部顯示／隱藏。
- 考點卡片 `id="kp1"…"kp5"`，Part 2/3 `id="part2"/"part3"`，`scroll-margin-top:64px` 處理遮擋。
- 主色酒紅 `#8c2740`、答案紅 `#c0392b`、按鈕青 `#1f6f78`、底色 `#f7f2ee`；字型 `Microsoft JhengHei / PingFang TC / Noto Sans TC`；支援 RWD。

---

## 部署
把整包（所有 `.html`）上傳：
- **Netlify Drop**（拖資料夾即得網址，最快）
- **GitHub Pages** / **Cloudflare Pages**（適合長期維護）

取得網址後，把 **`index.html` 的網址**發給學生當總入口。

---

## 未來優化（建議交給 Claude Code）
- **資料／樣板分離**：每單元寫成資料檔（JSON/Markdown）+ 樣板 + 建置腳本（或用 Astro／Eleventy），集中管理單元清單，免去各頁「單元 ▾」重複維護。
- KaTeX 改**本地打包**以支援完全離線。
- 進度記錄（localStorage）、站內搜尋、深色模式。
- 檔名改 ASCII（如 `matrix.html`）以利主機相容（改名須同步更新所有連結）。
- 詳細慣例與交接細節見 `交接文件_給Claude_Code.md`。
