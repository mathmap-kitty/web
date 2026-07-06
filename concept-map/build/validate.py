# -*- coding: utf-8 -*-
"""資料鏈結守門：build 前檢查考點／題目相關的耦合是否一致，避免「默默錯位」。
檢查項：
  ① part2_kp 清單長度 == 各單元 Part2 題數（位置對應，最易錯）→ 錯誤
  ② part2_kp／checks／cues 參照的考點 kp 是否存在 → 錯誤
  ③ 有 Part2 卻無 part2_kp、考點無概念小測、cue 群組未定義 → 提醒
可獨立跑：python build/validate.py（回傳碼 1＝有錯誤）。build.py 也會在建置前呼叫。
"""
import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, os.path.join(ROOT, "content")):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load():
    from units import UNITS
    try:
        from part2_kp import PART2_KP
    except Exception:
        PART2_KP = {}
    try:
        from checks import CHECKS
    except Exception:
        CHECKS = {}
    try:
        from cues import CUES, GROUPS
    except Exception:
        CUES, GROUPS = [], {}
    return UNITS, PART2_KP, CHECKS, CUES, GROUPS


def validate():
    UNITS, PART2_KP, CHECKS, CUES, GROUPS = _load()
    errors, warns = [], []

    unit_kps = {}   # slug -> [kp ids]（依序）
    part2_n = {}    # slug -> Part2 題數
    for u in UNITS:
        slug = u["slug"]
        if not os.path.exists(os.path.join(ROOT, "content", slug + ".py")):
            continue
        U = importlib.import_module(slug).UNIT
        unit_kps[slug] = [k["id"] for k in U.get("kps", [])]
        p2 = U.get("part2")
        part2_n[slug] = sum(len(g.get("questions", [])) for g in p2.get("groups", [])) if p2 else 0

    # ① + ② part2_kp：長度對齊 ＋ kp 存在
    for slug, lst in PART2_KP.items():
        if slug not in unit_kps:
            warns.append(f"[part2_kp] 未知單元「{slug}」（units.py 沒有或無內容檔）")
            continue
        n = part2_n.get(slug, 0)
        if len(lst) != n:
            errors.append(f"[part2_kp] {slug}：清單 {len(lst)} 筆 ≠ Part2 題數 {n} —— 位置會錯位！"
                          f"（增刪/搬動 Part2 題目後，要同步 content/part2_kp.py）")
        for i, kp in enumerate(lst):
            if kp not in unit_kps[slug]:
                errors.append(f"[part2_kp] {slug} 第 {i+1} 筆指向不存在的考點「{kp}」")
    for slug, n in part2_n.items():
        if n > 0 and slug not in PART2_KP:
            warns.append(f"[part2_kp] {slug} 有 {n} 題 Part2，但無對應清單（那些題的『解題核心』不會連回考點）")

    # ② checks：kp 存在
    for (slug, kp) in CHECKS:
        if slug not in unit_kps:
            warns.append(f"[checks] 未知單元「{slug}」")
        elif kp not in unit_kps[slug]:
            errors.append(f"[checks] {slug}:{kp} 指向不存在的考點")
    # ③ checks 覆蓋率（缺＝退回自我檢查，提醒即可）
    miss = [f"{s}:{k}" for s, kps in unit_kps.items() for k in kps if (s, k) not in CHECKS]
    if miss:
        warns.append(f"[checks] {len(miss)} 個考點無概念小測（會退回『看答案』自我檢查）："
                     f"{'、'.join(miss[:8])}{'…' if len(miss) > 8 else ''}")

    # ② cues：unit/kp 存在 ＋ 群組已定義
    for c in CUES:
        slug, kp = c.get("unit"), c.get("kp")
        kw = str(c.get("kw", ""))[:18]
        if slug not in unit_kps:
            errors.append(f"[cues] 未知單元「{slug}」（線索：{kw}）")
        elif kp not in unit_kps[slug]:
            errors.append(f"[cues] {slug}:{kp} 指向不存在的考點（線索：{kw}）")
        g = c.get("g")
        if g and g not in GROUPS:
            warns.append(f"[cues] 群組「{g}」未定義於 GROUPS（線索：{kw}）")

    for w in warns:
        print("  ⚠ " + w)
    for e in errors:
        print("  ✗ " + e)
    if errors:
        print(f"\n✗ 資料鏈結驗證失敗：{len(errors)} 個錯誤（見上）。請修正後再 build。")
        return False
    print(f"✓ 資料鏈結驗證通過（{len(warns)} 個提醒）")
    return True


if __name__ == "__main__":
    sys.exit(0 if validate() else 1)
