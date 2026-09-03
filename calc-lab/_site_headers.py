# -*- coding: utf-8 -*-
"""把 calc-lab/ 的 5 個 HTML 補上站台標頭：GA4、Clarity、favicon、回總入口的連結。

源頭資料夾（D:\\gmail\\115\\...\\9教學簡報\\互動教具\\）是離線版，沒有這些；
每次整包覆蓋 calc-lab/ 之後在 repo 根目錄跑：  python calc-lab/_site_headers.py
可重複執行（已補過的檔案會跳過）。
"""
import io
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "<!-- mathmap site headers -->"

HEAD = MARK + """
<!-- Google Analytics (GA4) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KQVPGYJ1FK"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-KQVPGYJ1FK');</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","xcgidr4emy");</script>
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
"""

OG = """<meta property="og:type" content="website">
<meta property="og:site_name" content="mathmap 數學教材網">
<meta property="og:locale" content="zh_TW">
<meta property="og:title" content="微積分互動教具 · 選修數學甲（上）">
<meta property="og:description" content="拉滑桿看極限：割線變切線、黎曼和逼近、面積函數長出來、旋轉體切圓盤。每一頁都能自己輸入函數與區間。">
<meta property="og:url" content="https://mathmap-kitty.github.io/web/calc-lab/">
<meta property="og:image" content="https://mathmap-kitty.github.io/web/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
"""

VIEWPORT = '<meta name="viewport" content="width=device-width,initial-scale=1">'
PORTAL_ABS = '<a class="ghost" href="https://mathmap-kitty.github.io/web/" target="_blank" rel="noopener">⇄ mathmap 總入口</a>'
PORTAL_REL = '<a class="ghost" href="../">← mathmap 總入口</a>'
TOOL_GHOST = '<a class="ghost" href="index.html">← 教具目錄</a>'
TOOL_GHOST2 = '<a class="ghost" href="index.html">← 教具目錄</a>\n  <a class="ghost" href="../">總入口</a>'

n = 0
for f in sorted(os.listdir(HERE)):
    if not f.endswith(".html"):
        continue
    p = os.path.join(HERE, f)
    s = io.open(p, encoding="utf-8").read()
    if MARK in s:
        print("skip (已補過)", f)
        continue
    if VIEWPORT not in s:
        print("!! 找不到 viewport meta：", f)
        continue
    extra = HEAD + (OG if f == "index.html" else "")
    s = s.replace(VIEWPORT, VIEWPORT + "\n" + extra, 1)
    s = s.replace(PORTAL_ABS, PORTAL_REL, 1)
    if f != "index.html":
        s = s.replace(TOOL_GHOST, TOOL_GHOST2, 1)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    n += 1
    print("ok", f)
print("補標頭完成：%d 個檔案" % n)
