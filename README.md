# mathmap 數學教材網（mathmap-kitty/web）

線上網址：**https://mathmap-kitty.github.io/web/index.html

## 站台結構（2026-07 重整後）

```
web/
├── index.html        # 總入口 portal：列出所有教材的入口卡
├── og-cover.png      # portal 的社群分享卡封面
├── concept-map/      # ① 學測數學重點整理（11 單元考點地圖＋互動練習）
│   └── README.md     #    子站說明與建置管線（content/*.py → build/ → dist/）
└── exam/             # ② 歷屆試題練習（111–115 學測數學A 逐題互動詳解）
```

- **concept-map/**：正式頁面直接放在該資料夾內；重建流程見 `concept-map/README.md`
  （在 `concept-map/` 下跑 `python build/build.py`，輸出在 `dist/`，確認後覆蓋 `concept-map/` 內正式檔）。
- **exam/**：源頭在本機 `D:\大考複習\歷屆試題詳解\互動網頁版\`，更新＝整包覆蓋 `exam/` 再 push。
  exam 內的考點連結一律用相對路徑 `../concept-map/…`。
- **新增教材**：在根目錄開新資料夾（自成一包、內部用相對連結），再到 `index.html` 加一張入口卡。

## 網址慣例

- 重點整理單元頁＋考點錨點：`/web/concept-map/115學測數學_<單元名>.html#kp<N>`
- 2026-07 重整說明：重點整理原本放在 `/web/` 根目錄，已整包搬入 `concept-map/`；
  對外僅發布過首頁網址（原首頁位置由 portal 接手），且已發布 PPT 內的考點超連結已同步改為新路徑，故未留轉址頁。
