# -*- coding: utf-8 -*-
"""一鍵建置：單一來源 -> 互動網頁 + Word（教師版／學生版）。

用法：
  python build/build.py            # 建置所有已登錄單元到 dist/
  python build/build.py matrix     # 只建置某單元
輸出在 dist/（確認無誤後再覆蓋根目錄的正式檔）。
"""
import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))

from build_html import build_html        # noqa: E402
from build_docx import build_docx        # noqa: E402
from units import UNITS                   # noqa: E402
from validate import validate            # noqa: E402  資料鏈結守門（考點/題目/part2_kp/checks/cues 一致性）

DIST = os.path.join(ROOT, "dist")


def build_unit(slug):
    mod = importlib.import_module(slug)
    unit = mod.UNIT
    os.makedirs(DIST, exist_ok=True)
    html = build_html(unit, UNITS)
    html_path = os.path.join(DIST, unit["file"])
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    t_path = os.path.join(DIST, f"{slug}_教師完整版.docx")
    s_path = os.path.join(DIST, f"{slug}_學生挖空版.docx")
    build_docx(unit, "teacher", t_path)
    build_docx(unit, "student", s_path)
    print(f"[{slug}] -> {os.path.basename(html_path)}, "
          f"{os.path.basename(t_path)}, {os.path.basename(s_path)}")


def main():
    if not validate():   # 資料鏈結不一致（如 part2_kp 錯位）→ 直接擋下，不產出錯誤的頁
        sys.exit(1)
    slugs = sys.argv[1:] or [u["slug"] for u in UNITS if os.path.exists(
        os.path.join(ROOT, "content", u["slug"] + ".py"))]
    for slug in slugs:
        build_unit(slug)


if __name__ == "__main__":
    main()
