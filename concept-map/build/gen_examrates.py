# -*- coding: utf-8 -*-
r"""從 exam/ 子站的題庫導出「考點 × 官方答對率」，產生 content/exam_rates.py。

資料流：
  ../exam/data.js（window.EXAM_DATA，200 題，每題有 rate 與 kaodian 考點連結）
      → 只取數 A（concept-map 是 108 課綱數 A）
      → 依 kaodian[].url 的 <檔名>#kpN 反查 units.py 的 slug
      → 同一 (slug, kp) 的題目取平均答對率
      → 只保留 n >= MIN_N 的組（樣本太小不足以代表考點難度）

為什麼要落成快照檔：`exam/` 的源頭在本機外部（`D:\大考複習\歷屆試題詳解\互動網頁版\`），
AGENTS.md 明令不在本 repo 內改 exam/。所以這裡「只讀不改」，把導出結果存成
content/exam_rates.py 進版控；exam/ 日後更新時重跑本腳本即可刷新。

用法：
    cd D:/gmail/Mathmap_workspace/concept-map
    PYTHONUTF8=1 python build/gen_examrates.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # concept-map/
REPO = os.path.dirname(ROOT)                 # web/
DATA = os.path.join(REPO, "exam", "data.js")
OUT = os.path.join(ROOT, "content", "exam_rates.py")

sys.path.insert(0, os.path.join(ROOT, "content"))
import units as units_mod  # noqa: E402

# 樣本門檻：少於 3 題的考點不標數字。
# 單一題的難易受該題包裝影響極大，不等於整個考點的難易，標出來會誤導。
MIN_N = 3

# 多選題該採哪個數字？大考中心對多選同時公布「得分率」（部分給分）與「全對率」。
#   "full"  → 用全對率：與單選答對率同構念（完全答對的比例），可直接平均。
#   "score" → 用得分率：與 exam/ 子站標題顯示的數字一致，但語意與單選不同，會偏高。
MULTI_METRIC = "full"

FILE2SLUG = {u["file"]: u["slug"] for u in units_mod.UNITS}

# "29%"  或  "57%（全對率 37%）"
RE_PLAIN = re.compile(r"^(\d+(?:\.\d+)?)%$")
RE_MULTI = re.compile(r"^(\d+(?:\.\d+)?)%（全對率\s*(\d+(?:\.\d+)?)%）$")


def load_questions():
    with open(DATA, encoding="utf-8") as fh:
        s = fh.read()
    return json.loads(s[s.index("["):].rstrip().rstrip(";"))


def parse_rate(raw):
    """把 rate 欄位解析成 (得分率, 全對率, 是否多選)。無數字則回 None。

    單選／選填／混合題只有一個數字，得分率＝全對率＝該數字（全有全無計分）。
    非選擇題大考中心未列答對率，回 None。
    """
    raw = (raw or "").strip()
    m = RE_MULTI.match(raw)
    if m:
        return float(m.group(1)), float(m.group(2)), True
    m = RE_PLAIN.match(raw)
    if m:
        v = float(m.group(1))
        return v, v, False
    return None


def collect(questions, metric):
    """回傳 ({(slug, kpid): [rate, ...]}, {(slug, kpid): 多選題數}, 無法解析清單)。"""
    agg, multi_n, skipped = {}, {}, []
    for q in questions:
        if q.get("subject") != "A":
            continue
        parsed = parse_rate(q.get("rate"))
        if parsed is None:
            if q.get("rate"):
                skipped.append((q.get("year"), q.get("num"), q.get("rate")))
            continue
        score, full, is_multi = parsed
        rate = full if metric == "full" else score
        for k in q.get("kaodian", []):
            um = re.search(r"([^/]+\.html)#(kp\d+)", k.get("url", ""))
            if not um:
                continue
            slug = FILE2SLUG.get(um.group(1))
            if not slug:
                skipped.append((q.get("year"), q.get("num"), um.group(1)))
                continue
            key = (slug, um.group(2))
            agg.setdefault(key, []).append(rate)
            if is_multi:
                multi_n[key] = multi_n.get(key, 0) + 1
    return agg, multi_n, skipped


def main():
    questions = load_questions()
    n_a = sum(1 for q in questions if q.get("subject") == "A")

    agg, multi_n, skipped = collect(questions, MULTI_METRIC)
    kept = {k: v for k, v in agg.items() if len(v) >= MIN_N}
    dropped = {k: v for k, v in agg.items() if len(v) < MIN_N}

    metric_label = "全對率" if MULTI_METRIC == "full" else "得分率"
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""考點 × 官方答對率（大考中心）——由 build/gen_examrates.py 自動產生，請勿手改。',
        "",
        f"來源：exam/ 子站題庫（數 A {n_a} 題；非選擇題大考中心未列答對率，不計）。",
        f"多選題採「{metric_label}」（見 gen_examrates.MULTI_METRIC）。",
        f"只收錄樣本 >= {MIN_N} 題的考點：樣本太小時，單一題的包裝難易不等於考點難易。",
        "",
        "RATES[(slug, kpid)] = (平均答對率%, 題數, 其中多選題數)",
        '"""',
        "",
        "RATES = {",
    ]
    for (slug, kp), vals in sorted(kept.items()):
        avg = sum(vals) / len(vals)
        lines.append(f'    ("{slug}", "{kp}"): ({avg:.1f}, {len(vals)}, {multi_n.get((slug, kp), 0)}),')
    lines.append("}")
    lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"[exam_rates] 寫出 {os.path.relpath(OUT, REPO)}　多選採「{metric_label}」")
    print(f"  數 A {n_a} 題　有考點對應的組數：{len(agg)}"
          f"　→ 收錄 {len(kept)} 組（n>={MIN_N}）、捨去 {len(dropped)} 組（樣本不足）")

    # 兩種口徑並列，讓老師看得出差多少
    other = "score" if MULTI_METRIC == "full" else "full"
    agg2, _, _ = collect(questions, other)
    print(f"\n  {'考點':16s} {'n':>3s} {'多選':>4s} {'全對率':>7s} {'得分率':>7s}  差")
    rows = sorted(kept.items(), key=lambda x: sum(x[1]) / len(x[1]))
    for (slug, kp), vals in rows:
        a = sum(vals) / len(vals)
        b = sum(agg2[(slug, kp)]) / len(agg2[(slug, kp)])
        full_v, score_v = (a, b) if MULTI_METRIC == "full" else (b, a)
        mn = multi_n.get((slug, kp), 0)
        flag = "  ←差很多" if abs(full_v - score_v) >= 10 else ""
        print(f"  {slug + ' ' + kp:16s} {len(vals):3d} {mn:4d} {full_v:6.1f}% {score_v:6.1f}%{flag}")
    if skipped:
        print(f"\n  ⚠ 無法解析 {len(skipped)} 筆（前 3）：{skipped[:3]}")


if __name__ == "__main__":
    main()
