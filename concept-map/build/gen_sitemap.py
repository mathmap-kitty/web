# -*- coding: utf-8 -*-
"""產生全站 sitemap.xml（寫到 repo 根，隨 Pages 發布）。

用法：python build/gen_sitemap.py   （在 concept-map/ 下執行；頁面增減後重跑再 push）
- 收錄：總入口、concept-map 全部 HTML、guide/（複習講義）、exam/
- lastmod 取各檔最後一次 git commit 日期；中文檔名自動 percent-encode
"""
import os
import sys
import subprocess
from urllib.parse import quote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
CM = os.path.dirname(HERE)              # concept-map/
REPO = os.path.dirname(CM)              # repo 根
SITE = "https://mathmap-kitty.github.io/web/"


def git_lastmod(relpath):
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", relpath],
            cwd=REPO, stderr=subprocess.DEVNULL)
        d = out.decode().strip()
        if d:
            return d
    except Exception:
        pass
    return None


entries = []  # (loc, git 查詢路徑)
entries.append((SITE, "index.html"))
for f in sorted(os.listdir(CM)):
    if not f.endswith(".html"):
        continue
    loc = SITE + "concept-map/" + ("" if f == "index.html" else quote(f))
    entries.append((loc, "concept-map/" + f))
GUIDE = os.path.join(REPO, "guide")     # 複習講義子站（站台根，13 章 + 附錄 + 目錄頁）
if os.path.isdir(GUIDE):
    for f in sorted(os.listdir(GUIDE)):
        if not f.endswith(".html"):
            continue
        loc = SITE + "guide/" + ("" if f == "index.html" else quote(f))
        entries.append((loc, "guide/" + f))
entries.append((SITE + "exam/", "exam/index.html"))

rows = []
for loc, gp in entries:
    lastmod = git_lastmod(gp)
    lm = f"<lastmod>{lastmod}</lastmod>" if lastmod else ""
    rows.append(f"  <url><loc>{loc}</loc>{lm}</url>")

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")
out = os.path.join(REPO, "sitemap.xml")
with open(out, "w", encoding="utf-8") as f:
    f.write(xml)
print(f"sitemap.xml：{len(entries)} 個網址 -> {out}")
