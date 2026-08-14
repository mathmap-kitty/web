# -*- coding: utf-8 -*-
r"""從 exam/ 子站的題庫導出「核心概念 × 歷屆題清單」，產生 content/exam_qs.py。

這是 gen_examrates.py 的姊妹產線：同一份 kaodian 對應表，那支取「平均答對率」，
這支取「題目清單」，用來在核心概念卡上掛回 exam 的深連結。

資料流：
  ../exam/data.js（window.EXAM_DATA，200 題，每題有 kaodian 核心概念連結）
      → 依 kaodian[].url 的 <檔名>#kpN 反查 units.py 的 slug
      → 同一 (slug, kp) 收集所有題，依 年份↓ → 數A先於數B → 題號↑ 排序
      → 落成 content/exam_qs.py

與 gen_examrates.py 的差別：
  - **不篩科目**：數 A 100 題 ＋ 數 B 100 題全收。數 B 對數 A 考生是額外練習題材，
    版型上會分開顯示（數 A 先、數 B 後）。
  - **不設樣本門檻**：那個門檻是為了「不要用 1 題去論斷核心概念難易」；
    這裡只是列出題目，1 題也是有用的連結。

深連結格式：exam/app.js 的 readDeepLink() 認 `?q=<B?><年份>-<題號>`
（見該檔 `/[?&]q=(B?\d{3}-[0-9A-Za-z]+)/`，數 B 的 B 在年份**前面**）。

為什麼要落成快照檔：`exam/` 的源頭在本機外部（`D:\大考複習\歷屆試題詳解\互動網頁版\`），
AGENTS.md 明令不在本 repo 內改 exam/。所以這裡「只讀不改」，把導出結果存成
content/exam_qs.py 進版控；exam/ 日後更新時重跑本腳本即可刷新。

用法：
    cd D:/gmail/Mathmap_workspace/concept-map
    PYTHONUTF8=1 python build/gen_exam_index.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # concept-map/
REPO = os.path.dirname(ROOT)                 # web/
DATA = os.path.join(REPO, "exam", "data.js")
OUT = os.path.join(ROOT, "content", "exam_qs.py")

sys.path.insert(0, os.path.join(ROOT, "content"))
import units as units_mod  # noqa: E402

FILE2SLUG = {u["file"]: u["slug"] for u in units_mod.UNITS}

# 題型縮寫：核心概念卡上空間有限，用兩個字就好
TYPE_SHORT = [
    ("非選", "非選"),
    ("混合", "混合"),
    ("單選", "單選"),
    ("多選", "多選"),
    ("選填", "選填"),
]


def load_questions():
    with open(DATA, encoding="utf-8") as fh:
        s = fh.read()
    return json.loads(s[s.index("["):].rstrip().rstrip(";"))


def short_type(raw):
    for key, short in TYPE_SHORT:
        if key in (raw or ""):
            return short
    return (raw or "")[:2]


def rate_num(raw):
    """取答對率數字給版型排序／顯示用。

    多選是 "57%（全對率 37%）"——這裡取**前面的得分率**，因為它就是 exam/ 子站
    卡片上顯示的那個數字，兩邊要一致（核心概念徽章的平均值才用全對率，見 gen_examrates）。
    非選擇題未列答對率 → None。
    """
    m = re.match(r"^(\d+(?:\.\d+)?)%", (raw or "").strip())
    return float(m.group(1)) if m else None


def collect(questions):
    """回傳 {(slug, kpid): [(year, subj, num, type_short, rate or None), ...]}。"""
    out = {}
    unmapped = []
    for q in questions:
        subj = q.get("subject", "A")
        year = int(q.get("year"))
        num = q.get("num")
        item = (year, subj, num, short_type(q.get("type")), rate_num(q.get("rate")))
        for k in q.get("kaodian", []):
            um = re.search(r"([^/]+\.html)#(kp\d+)", k.get("url", ""))
            if not um:
                unmapped.append((year, subj, num, k.get("url", "")[:40]))
                continue
            slug = FILE2SLUG.get(um.group(1))
            if not slug:
                unmapped.append((year, subj, num, um.group(1)))
                continue
            out.setdefault((slug, um.group(2)), []).append(item)
    # 年份新→舊、數A先於數B、題號小→大（學生最想先看今年的）
    for key in out:
        seen, uniq = set(), []
        for it in sorted(out[key], key=lambda x: (-x[0], x[1], x[2])):
            if it[:3] in seen:      # 同一題被同一核心概念掛兩次（理論上不會，防呆）
                continue
            seen.add(it[:3])
            uniq.append(it)
        out[key] = uniq
    return out, unmapped


def main():
    questions = load_questions()
    data, unmapped = collect(questions)

    n_a = sum(1 for q in questions if q.get("subject") == "A")
    n_b = sum(1 for q in questions if q.get("subject") == "B")
    total_links = sum(len(v) for v in data.values())
    years = sorted({int(q["year"]) for q in questions})

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""核心概念 × 歷屆題清單——由 build/gen_exam_index.py 自動產生，請勿手改。',
        "",
        f"來源：exam/ 子站題庫（{years[0]}–{years[-1]}，數A {n_a} 題 ＋ 數B {n_b} 題）。",
        "用途：核心概念卡「這個核心概念的歷屆全題」可收合區塊，連回 exam/?q=<B?><年>-<題號>。",
        "",
        "EXAM_QS[(slug, kpid)] = [(年份, 科目, 題號, 題型, 答對率 or None), ...]",
        "  排序：年份新→舊、數A 先於數B、題號小→大",
        "  答對率：多選取「得分率」（與 exam/ 卡片顯示一致；核心概念徽章的平均值另採全對率）",
        '"""',
        "",
        "EXAM_QS = {",
    ]
    for (slug, kp), items in sorted(data.items()):
        body = ", ".join(
            f"({y}, {s!r}, {n}, {t!r}, {r if r is not None else 'None'})"
            for y, s, n, t, r in items)
        lines.append(f'    ("{slug}", "{kp}"): [{body}],')
    lines.append("}")
    lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"[exam_qs] 寫出 {os.path.relpath(OUT, REPO)}")
    print(f"  {years[0]}–{years[-1]}　數A {n_a} ＋ 數B {n_b} 題"
          f"　→ {len(data)} 個核心概念、{total_links} 條連結")

    # 覆蓋率報表：哪些核心概念掛不到題，一眼看得出來
    all_kps = []
    for u in units_mod.UNITS:
        mod = __import__(u["slug"])
        for k in mod.UNIT["kps"]:
            all_kps.append((u["slug"], k["id"], u["title"], k["nav"]))
    miss = [x for x in all_kps if (x[0], x[1]) not in data]
    print(f"  覆蓋 {len(all_kps) - len(miss)}/{len(all_kps)} 個核心概念")
    if miss:
        print("  ⚠ 掛不到題的核心概念（exam 題庫中沒有對應）：")
        for slug, kp, title, nav in miss:
            print(f"      {title} {kp} {nav}")
    if unmapped:
        print(f"  ⚠ 無法反查 slug 的連結 {len(unmapped)} 筆（前 3）：{unmapped[:3]}")

    top = sorted(data.items(), key=lambda x: -len(x[1]))[:5]
    print("  題數最多的核心概念：" + "、".join(f"{s} {k}（{len(v)}）" for (s, k), v in top))


if __name__ == "__main__":
    main()
