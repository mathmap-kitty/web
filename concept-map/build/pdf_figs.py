# -*- coding: utf-8 -*-
"""補圖：把 Word 用「繪圖物件」畫的示意圖，從教師版 PDF 裁成 PNG。

為什麼需要：講義裡有 14 張圖是在 Word 裡用線條／圖形直接畫的（不是插入的圖檔），
pandoc 讀 .docx 時完全看不到它們。這些圖有教學價值（指對數圖形、解的三種情形、
點到直線距離示意…），所以改從 PDF 對應位置裁圖，輸出到 guide-img/。

座標由 PDF 的表格框線量出來（見 JOBS），裁完會自動去白邊。

用法（在 concept-map/ 下）：
  python build/pdf_figs.py            # 產生 guide-img/vfig_*.png
  python build/pdf_figs.py --sheet    # 另存一張總覽圖，方便人工確認
"""
import json
import os
import sys

import fitz  # PyMuPDF

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(os.path.dirname(ROOT), "guide", "img")
PDF = r"D:\gmail\115\01_教學\複習講義\學測數A_脈絡複習講義_全教用.pdf"

DPI = 220

# (檔名, PDF 頁(1-based), [x0,y0,x1,y1] 頁面座標, 說明, 網頁顯示寬度 px；0＝不限制)
JOBS = [
    # 第三章：距離公式一節的兩張示意圖
    ("vfig_ch3_proj.png", 14, [368, 212, 487, 292], "對稱點：Q 是 P、R 的中點", 300),
    ("vfig_ch3_half.png", 14, [125, 476, 485, 553], "直線把平面分成兩側：代一點看正負", 430),
    # 第八章「三、圖形」表格的「圖形」列（4 格，格線 x=120/226/333/434/538，y=136~224）
    ("vfig_ch8_exp_gt1.png", 32, [122, 138, 224, 222], "y=a^x（a>1）遞增", 0),
    ("vfig_ch8_exp_lt1.png", 32, [228, 138, 328, 222], "y=a^x（0<a<1）遞減", 0),
    ("vfig_ch8_log_gt1.png", 32, [335, 138, 432, 222], "y=log_a x（a>1）遞增", 0),
    ("vfig_ch8_log_lt1.png", 32, [436, 138, 536, 222], "y=log_a x（0<a<1）遞減", 0),
    # 第九章：三角比一節的兩個直角三角形（合成一張）
    ("vfig_ch9_tri.png", 35, [225, 243, 335, 378], "直角三角形：對邊／鄰邊／斜邊", 165),
    # 第十三章：解的三種情形（格線 x=51/206/359/513，y=577~671 圖列、671~765 向量列）
    ("vfig_ch13_one.png", 58, [53, 579, 204, 669], "恰有一組解：兩線相交", 0),
    ("vfig_ch13_none.png", 58, [208, 579, 357, 669], "無解：兩線平行", 0),
    ("vfig_ch13_many.png", 58, [361, 579, 511, 669], "無限多組解：兩線重合", 0),
    ("vfig_ch13_v_one.png", 58, [53, 673, 204, 763], "恰一解：兩向量不平行", 0),
    ("vfig_ch13_v_none.png", 58, [208, 673, 357, 763], "無解：向量平行、常數不合", 0),
    ("vfig_ch13_v_many.png", 58, [361, 673, 511, 763], "無限多解：向量平行且相合", 0),
]


def trim(pix, pad=8):
    """去白邊：回傳非白像素的外框（像素座標）。"""
    w, h, n = pix.width, pix.height, pix.n
    data = pix.samples
    x0, y0, x1, y1 = w, h, 0, 0
    for y in range(h):
        row = y * pix.stride
        for x in range(w):
            i = row + x * n
            if data[i] < 245 or data[i + 1] < 245 or data[i + 2] < 245:
                if x < x0:
                    x0 = x
                if x > x1:
                    x1 = x
                if y < y0:
                    y0 = y
                if y > y1:
                    y1 = y
    if x1 <= x0 or y1 <= y0:
        return None
    return (max(0, x0 - pad), max(0, y0 - pad),
            min(w, x1 + pad + 1), min(h, y1 + pad + 1))


def main(sheet=False):
    doc = fitz.open(PDF)
    os.makedirs(IMG_DIR, exist_ok=True)
    outs, man = [], {}
    for name, page, box, desc, w in JOBS:
        p = doc[page - 1]
        pix = p.get_pixmap(clip=fitz.Rect(*box), dpi=DPI)
        t = trim(pix)
        if t:
            sc = DPI / 72.0
            box2 = [box[0] + t[0] / sc, box[1] + t[1] / sc,
                    box[0] + t[2] / sc, box[1] + t[3] / sc]
            pix = p.get_pixmap(clip=fitz.Rect(*box2), dpi=DPI)
        path = os.path.join(IMG_DIR, name)
        pix.save(path)
        outs.append((name, pix.width, pix.height, desc))
        man[name] = {"w": w, "cap": desc}
        print(f"  {name:26s} {pix.width:4d}×{pix.height:<4d}  {desc}")
    with open(os.path.join(IMG_DIR, "vfig_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    print(f"共 {len(outs)} 張補圖 → {IMG_DIR}（含 vfig_manifest.json）")

    if sheet:
        # 總覽圖（人工確認裁切是否正確）
        cols, cw, chh = 3, 320, 240
        rows = (len(outs) + cols - 1) // cols
        sh = fitz.open()
        pg = sh.new_page(width=cols * cw, height=rows * chh)
        for i, (name, w, h, desc) in enumerate(outs):
            r, c = divmod(i, cols)
            box = fitz.Rect(c * cw + 10, r * chh + 24, (c + 1) * cw - 10, (r + 1) * chh - 10)
            pg.insert_image(box, filename=os.path.join(IMG_DIR, name), keep_proportion=True)
            pg.insert_text((c * cw + 10, r * chh + 18), f"{i+1}. {name}", fontsize=8)
        out = os.path.join(HERE, "_vfig_sheet.png")
        pg.get_pixmap(dpi=110).save(out)
        print("總覽圖：", out)


if __name__ == "__main__":
    main("--sheet" in sys.argv)
