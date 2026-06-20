# -*- coding: utf-8 -*-
"""所有單元的註冊表（工具列「單元 ▾」跨頁導覽用）。"""

UNITS = [
    {"slug": "trig", "file": "115學測數學_三角_互動學習.html", "emoji": "📐", "title": "三角"},
    {"slug": "prob", "file": "115學測數學_排列組合與機率_互動學習.html", "emoji": "🎲", "title": "排列組合與機率"},
    {"slug": "space", "file": "115學測數學_空間向量_互動學習.html", "emoji": "🧊", "title": "空間向量"},
    {"slug": "poly", "file": "115學測數學_多項式函數_互動學習.html", "emoji": "📈", "title": "多項式函數"},
    {"slug": "linecir", "file": "115學測數學_直線與圓_互動學習.html", "emoji": "⭕", "title": "直線與圓"},
    {"slug": "explog", "file": "115學測數學_指數與對數_互動學習.html", "emoji": "📉", "title": "指數與對數"},
    {"slug": "pvec", "file": "115學測數學_平面向量_互動學習.html", "emoji": "➡️", "title": "平面向量"},
    {"slug": "data", "file": "115學測數學_數據分析_互動學習.html", "emoji": "📊", "title": "數據分析"},
    {"slug": "seq", "file": "115學測數學_數列與級數_互動學習.html", "emoji": "🪜", "title": "數列與級數"},
    {"slug": "matrix", "file": "115學測數學_矩陣_互動學習.html", "emoji": "🧮", "title": "矩陣"},
    {"slug": "numexpr", "file": "115學測數學_數與式_互動學習.html", "emoji": "🔢", "title": "數與式"},
]

# 首頁與各頁「單元 ▾」下拉的四大主題分區（與 index.html 一致）。
SECTIONS = [
    ("① 代數與函數", ["numexpr", "poly", "explog"]),
    ("② 數列・機率・統計", ["seq", "prob", "data"]),
    ("③ 平面幾何", ["trig", "linecir", "pvec"]),
    ("④ 空間與矩陣", ["space", "matrix"]),
]
