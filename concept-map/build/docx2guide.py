# -*- coding: utf-8 -*-
"""把「學測數A 脈絡複習講義（全教用）.docx」轉成單一來源 JSON：content/guide_data.json。

為什麼這樣做：講義的原稿是 Word（教師版答案＝玫瑰色 9C5A6E，學生版＝底線挖空），
網頁要的是「同一份內容 + 答案可點按顯示」。所以：

  教師版 .docx
    → 注入標記：把每個玫瑰色 run 用 ⟦…⟧ 包起來（含 OMML 數學式內的 m:r）
    → pandoc -f docx+styles -t json：段落樣式（SecHead/SubHead/NoteBox/HL…）保留成
      custom-style，OMML 數學式自動轉成 LaTeX
    → 走訪 AST，正規化成自家區塊格式，⟦…⟧ 變成挖空（HTML 端＝可點按按鈕）
    → 寫出 content/guide_data.json + 圖片到 guide-img/

之後 build_guide.py 只吃 JSON，不需要 docx，也不需要 pandoc。

用法（在 concept-map/ 下執行；需 pandoc 3.x 與 lxml）：
  python build/docx2guide.py                      # 用預設的 DOCX 路徑
  python build/docx2guide.py 路徑\\全教用.docx      # 指定來源
"""
import html as _html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from lxml import etree

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # concept-map/
OUT_JSON = os.path.join(ROOT, "content", "guide_data.json")
IMG_DIR = os.path.join(os.path.dirname(ROOT), "guide", "img")   # 圖片直接產到發布位置

DEFAULT_DOCX = r"D:\gmail\115\01_教學\複習講義\學測數A_脈絡複習講義_全教用.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
XML = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W, "m": M}

ANS_COLORS = {"9C5A6E"}       # 玫瑰色＝答案（教師版）
OPEN, CLOSE = "\u27e6", "\u27e7"     # ⟦ ⟧ 答案標記（挑不會出現在數學內容的字元）
UMARK = "⸫"            # ⸫ 標記：原稿留白（連教師版都沒填答案）的長底線填空
UND = "⸨⸩"        # 舊版底線標記字元，讀到就丟掉
# 原稿留白的填空（教師版也沒填答案）→ 網頁留一條底線，讓人知道這裡要填
UBLANK = '<span class="ublank"></span>'


# ---------------------------------------------------------------- 1. 注入標記
def inject_markers(src, dst):
    """複製一份 docx，把玫瑰色 run 的文字用 ⟦…⟧ 包住（w:t 與 m:t 都要）。"""
    zin = zipfile.ZipFile(src)
    root = etree.fromstring(zin.read("word/document.xml"))
    n = nu = 0
    for r in root.iter(f"{{{W}}}r", f"{{{M}}}r"):
        rpr = r.find("w:rPr", NS)
        col, und = "", False
        if rpr is not None:
            c = rpr.find("w:color", NS)
            if c is not None:
                col = (c.get(f"{{{W}}}val") or "").upper()
            u = rpr.find("w:u", NS)
            if u is not None:
                und = (u.get(f"{{{W}}}val") or "none") != "none"
        rose = col in ANS_COLORS
        if not rose and not und:
            continue
        ts = list(r.iter(f"{{{W}}}t", f"{{{M}}}t"))
        if not ts:
            continue
        txt = "".join(t.text or "" for t in ts)
        # 底線＋整段空白（>=4 格）＝原稿刻意留白的填空：pandoc 會把連續空白壓成一格，
        # 所以在這裡就換成一個標記字元，之後直接畫成一條底線
        if und and txt.strip() == "" and len(txt) >= 4:
            for t in ts:
                t.text = ""
            ts[0].text = UMARK
            nu += 1
            continue
        if not rose:
            continue
        ts[0].text = OPEN + (ts[0].text or "")
        ts[-1].text = (ts[-1].text or "") + CLOSE
        for t in (ts[0], ts[-1]):
            t.set(f"{{{XML}}}space", "preserve")
        n += 1
    doc = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, doc if item.filename == "word/document.xml"
                          else zin.read(item.filename))
    zin.close()
    print(f"  注入答案標記：{n} 個玫瑰色 run；原稿留白填空 {nu} 處")


# ------------------------------------------------------- 2. LaTeX 挖空切割工具
CMD_NEEDS_ARG = {
    "frac", "dfrac", "tfrac", "sqrt", "overline", "underline", "text", "textbf",
    "mathbf", "mathrm", "mathbb", "binom", "vec", "overrightarrow", "widehat",
    "hat", "bar", "operatorname", "begin", "end", "left", "right", "color",
    "substack", "mspace", "overset", "underset", "stackrel", "boxed",
}
# 可當「題目 = 答案」切點的關係符號（只在最外層生效）
RELS = ["\\Leftrightarrow", "\\Longleftrightarrow", "\\Rightarrow", "\\Longrightarrow",
        "\\leq", "\\geq", "\\neq", "\\approx", "\\equiv", "\\sim", "\\in",
        "=", "<", ">"]


def _strip_markers(tex, ans_in):
    """回傳 (乾淨 LaTeX, 每字元是否屬於答案, 結束時是否還在答案中)。"""
    out, mask, ans = [], [], ans_in
    for ch in tex:
        if ch == OPEN:
            ans = True
        elif ch == CLOSE:
            ans = False
        elif ch in UND:
            continue
        else:
            out.append(ch)
            mask.append(ans)
    return "".join(out), mask, ans


def _tex_ok(s):
    """粗略檢查一段 LaTeX 是否自成完整片段（大括號／\\left\\right／begin\\end 成對，
    結尾沒有懸空的 ^ _ 或需要參數的指令）。切割挖空時用來擋掉會讓 KaTeX 爆掉的切法。"""
    s = s.strip()
    if not s:
        return False
    depth, i = 0, 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            j = i + 1
            if j < len(s) and s[j].isalpha():
                while j < len(s) and s[j].isalpha():
                    j += 1
                i = j
            else:
                i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    if depth != 0:
        return False
    if s.count("\\left") != s.count("\\right"):
        return False
    if s.count("\\begin") != s.count("\\end"):
        return False
    if re.search(r"(\^|_|&)\s*$", s):
        return False
    m = re.search(r"\\([a-zA-Z]+)\s*$", s)
    if m and m.group(1) in CMD_NEEDS_ARG:
        return False
    if re.match(r"^\s*[}\^_&]", s):
        return False
    return True


def _structural(s):
    """只有括號／空白／指令外殼（沒有實質內容）→ 這段前綴／後綴可以併進答案。"""
    t = re.sub(r"\\[a-zA-Z]+|\\.|[\s{}()\[\]|]", "", s)
    return t == ""


def _top_level_rel_ends(s):
    """所有「最外層」關係符號的結束位置（不在大括號／環境內）。"""
    ends, depth, env, i = [], 0, 0, 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            for r in RELS:
                if r.startswith("\\") and s.startswith(r, i):
                    if depth == 0 and env == 0:
                        ends.append(i + len(r))
                    i += len(r)
                    break
            else:
                if s.startswith("\\begin", i):
                    env += 1
                    i += 6
                    continue
                if s.startswith("\\end", i):
                    env -= 1
                    i += 4
                    continue
                j = i + 1
                if j < len(s) and s[j].isalpha():
                    while j < len(s) and s[j].isalpha():
                        j += 1
                    i = j
                else:
                    i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c in "=<>" and depth == 0 and env == 0:
            ends.append(i + 1)
        i += 1
    return ends


def _runs(mask):
    """mask 中連續為 True 的區間 [[lo,hi), …]。"""
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]:
                j += 1
            out.append([i, j])
            i = j
        else:
            i += 1
    return out


def _groups(s, mask):
    """答案區間分組：中間只隔括號／運算符外殼的相鄰區間併成一組
    （像 {a}^{2} \\pm 2ab 是同一個答案）；中間夾了實質內容的不併
    （像「abc/999，0.abc̄ = (abc-a)/990」是一條式子裡的兩題）。
    再各自往外吃掉純結構字元，讓每組自成一段合法 LaTeX。"""
    gs = []
    for lo, hi in _runs(mask):
        if gs and _structural(s[gs[-1][1]:lo]):
            gs[-1][1] = hi
        else:
            gs.append([lo, hi])
    orig = [tuple(g) for g in gs]
    out = []
    for i, (lo, hi) in enumerate(orig):
        lmin = orig[i - 1][1] if i else 0             # 不越過前一組
        rmax = orig[i + 1][0] if i + 1 < len(orig) else len(s)
        l, r = lo, hi
        while l > lmin and _structural(s[l - 1:lo]):
            l -= 1
        # 左邊若留下懸空的 \frac、\sqrt… 這類「要吃參數」的指令，連指令一起併進來，
        # 否則黑字那段會以 \frac 結尾（不合法），整段只能退回當答案
        while True:
            m = re.search(r"\\([a-zA-Z]+)\s*$", s[:l])
            if m and m.group(1) in CMD_NEEDS_ARG and m.start() >= lmin:
                l = m.start()
                continue
            break
        while r < rmax and _structural(s[hi:r + 1]):
            r += 1
        out.append([l, r])
    return out


def _pieces(s, gs):
    """依分組把字串切成 [(片段, 是否答案), …]（含中間的黑字）。"""
    out, pos = [], 0
    for lo, hi in gs:
        if lo > pos:
            out.append([s[pos:lo], False])
        out.append([s[lo:hi], True])
        pos = hi
    if pos < len(s):
        out.append([s[pos:], False])
    return [p for p in out if p[0]]


def _ok_pieces(pieces):
    return all(_tex_ok(t) or not t.strip() for t, _ in pieces)


def split_math(tex, ans_in):
    """把（含標記的）LaTeX 切成 [(片段, 是否答案), …]；回傳 (片段串, 結束時的答案狀態)。

    一條式子可能同時有題目與答案、甚至兩題（Word 常把好幾題放進同一個方程式物件），
    所以按「答案區間分組」切，切不成合法 LaTeX 時逐步併回去；最後才退回「整式當答案」
    ——寧可整條變按鈕，也不要讓 KaTeX 壞掉。
    """
    s, mask, ans_out = _strip_markers(tex, ans_in)
    if not s.strip():
        return [], ans_out
    if not any(mask):
        return [(s, False)], ans_out
    gs = _groups(s, mask)
    pieces = _pieces(s, gs)
    if _ok_pieces(pieces):
        return [tuple(p) for p in pieces], ans_out
    # 退路一：只有一個答案區間 → 在答案前最靠右的關係符號（= ⇔ ≤ …）切開，題目留著當提示
    if len(gs) == 1:
        for p in reversed([e for e in _top_level_rel_ends(s) if e <= gs[0][0]]):
            if _tex_ok(s[:p]) and _tex_ok(s[p:]):
                return [(s[:p], False), (s[p:], True)], ans_out
    # 退路二：把切壞的片段和鄰居併回去，直到每段都合法
    while len(pieces) > 1 and not _ok_pieces(pieces):
        i = next(k for k, (t, _) in enumerate(pieces) if t.strip() and not _tex_ok(t))
        j = i + 1 if i + 1 < len(pieces) else i - 1
        a, b = sorted((i, j))
        pieces[a] = [pieces[a][0] + pieces[b][0], pieces[a][1] or pieces[b][1]]
        del pieces[b]
    if _ok_pieces(pieces):
        return [tuple(p) for p in pieces], ans_out
    return [(s, True)], ans_out


# ---------------------------------------------------------- 3. inline → HTML
def esc(t):
    return _html.escape(t, quote=False)


def _fix_tex(t):
    """KaTeX 0.16 不支援 Word 轉出來的 \\mspace（會印成紅字原文）→ 換成等效寫法。"""
    t = t.replace("\\sqrt{\\mspace{6mu}}", "\\sqrt{\\phantom{x}}")
    return re.sub(r"\\mspace\{[^}]*\}", "\\\\,", t)


def math_html(tex, display=False):
    # KaTeX 讀 textContent，故 & < > 必須先轉成實體（矩陣的欄分隔 & 尤其重要）
    t = _html.escape(_fix_tex(tex), quote=False)
    return ("\\[" + t + "\\]") if display else ("\\(" + t + "\\)")


def _style(attr):
    """pandoc attr → custom-style 名稱。"""
    for k, v in (attr[2] or []):
        if k == "custom-style":
            return v
    return ""


BADGE_CLASS = {"BadgeBasic": "bg-ex", "BadgeTrap": "bg-trap"}

# Word 舊式方程式（OLE→.wmf，瀏覽器不能顯示）：直接改寫成 LaTeX
WMF_TEX = {"image17.wmf": "y = a^{x}", "image18.wmf": "y = \\log_{a}x"}

def _vfig_meta():
    """pdf_figs.py 產生的補圖清單（顯示寬度、圖說）。"""
    p = os.path.join(IMG_DIR, "vfig_manifest.json")
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}


VFIG = _vfig_meta()

# ---- 補圖（pdf_figs.py 從 PDF 裁出來的 Word 手繪圖）安插位置 ----
# 表格內：(章, 該列首格文字, 從第幾格開始填, [檔名…])
TABLE_FIGS = [
    (8, "圖形", 1, ["vfig_ch8_exp_gt1.png", "vfig_ch8_exp_lt1.png",
                    "vfig_ch8_log_gt1.png", "vfig_ch8_log_lt1.png"]),
]
# 表格內：(章, 第幾個「整列全空」的列(0-based), [檔名…])
EMPTY_ROW_FIGS = [
    (13, 0, ["vfig_ch13_one.png", "vfig_ch13_none.png", "vfig_ch13_many.png"]),
    (13, 1, ["vfig_ch13_v_one.png", "vfig_ch13_v_none.png", "vfig_ch13_v_many.png"]),
]
# 一般段落後面：(章, 錨點文字（出現在某區塊內即接在其後）, 檔名, 圖說, 是否靠右浮動)
AFTER_FIGS = [
    (3, "對稱點", "vfig_ch3_proj.png", "對稱點：Q 是 P、R 的中點", True),
    (3, "半平面", "vfig_ch3_half.png", "直線把平面分成兩側：代一點看正負", False),
    (9, "定義（直角三角形）", "vfig_ch9_tri.png", "直角三角形：對邊／鄰邊／斜邊", True),
]


class Ctx:
    """走訪過程中共用的狀態：答案標記是否開著、蒐集到的圖片。"""

    def __init__(self):
        self.ans = False        # 目前是否在「答案」標記內
        self.und = None         # 目前是否在「底線」標記內（收集其中文字）
        self.images = []


def _emit(toks, ctx, s):
    if not s:
        return
    if toks and toks[-1][1] == ctx.ans:
        toks[-1][0] += esc(s)
    else:
        toks.append([esc(s), ctx.ans])


def push_text(toks, ctx, s):
    for ch in s:
        if ch == OPEN:
            ctx.ans = True
        elif ch == CLOSE:
            ctx.ans = False
        elif ch == UMARK:
            toks.append([UBLANK, False])
        elif ch in UND:
            pass
        else:
            _emit(toks, ctx, ch)


def walk_inlines(inls, ctx):
    """→ [[html, is_ans], …]（圖片會另外記到 ctx.images 並回傳 'IMG' 佔位）"""
    toks = []
    for n in inls or []:
        t = n["t"]
        if t == "Str":
            push_text(toks, ctx, n["c"])
        elif t == "Space":
            push_text(toks, ctx, " ")
        elif t in ("SoftBreak",):
            push_text(toks, ctx, " ")
        elif t == "LineBreak":
            toks.append(["<br>", ctx.ans])
        elif t == "Math":
            display = n["c"][0]["t"] == "DisplayMath"
            parts, ctx.ans = split_math(n["c"][1], ctx.ans)
            # 顯示數學被切成「題目＋答案」時，改用行內＋\displaystyle：
            # 否則 \[…\] 各自佔一行，答案按鈕會掉到下一行去
            split_disp = display and len([p for p in parts if p[0].strip()]) > 1
            for tex, is_ans in parts:
                if split_disp:
                    toks.append([math_html("\\displaystyle " + tex, False), is_ans])
                else:
                    toks.append([math_html(tex, display), is_ans])
        elif t in ("Emph", "Strong", "Subscript", "Superscript", "Strikeout",
                   "Underline", "SmallCaps"):
            tag = {"Emph": "em", "Strong": "b", "Subscript": "sub",
                   "Superscript": "sup", "Strikeout": "s"}.get(t)
            sub = walk_inlines(n["c"], ctx)
            for h, a in sub:
                toks.append([f"<{tag}>{h}</{tag}>" if tag else h, a])
        elif t == "Span":
            st = _style(n["c"][0])
            sub = walk_inlines(n["c"][1], ctx)
            if st in BADGE_CLASS:
                inner = "".join(h for h, _ in sub)
                if inner.strip():
                    toks.append([f'<b class="bdg {BADGE_CLASS[st]}">{inner}</b>', False])
            else:
                toks.extend(sub)
        elif t == "Link":
            sub = walk_inlines(n["c"][1], ctx)
            url = n["c"][2][0]
            if url.startswith("#"):        # Word 內部連結（目錄）→ 只留文字
                toks.extend(sub)
            else:
                inner = "".join(h for h, _ in sub)
                toks.append([f'<a href="{_html.escape(url)}">{inner}</a>', False])
        elif t == "Image":
            attr, alt, tgt = n["c"]
            src = os.path.basename(tgt[0]).replace("\\", "/")
            if src in WMF_TEX:      # Word 舊式方程式物件（.wmf 瀏覽器不支援）→ 直接寫成數學式
                toks.append([math_html(WMF_TEX[src]), False])
                continue
            ctx.images.append({
                "src": src,
                "w": _inch_px(dict(attr[2] or {}).get("width")),
                "alt": "".join(h for h, _ in walk_inlines(alt, ctx)),
            })
            toks.append(["\x00IMG\x00", False])
        elif t == "Quoted":
            q = "「" if n["c"][0]["t"] == "SingleQuote" else "「"
            push_text(toks, ctx, q)
            toks.extend(walk_inlines(n["c"][1], ctx))
            push_text(toks, ctx, "」")
        elif t in ("Cite",):
            toks.extend(walk_inlines(n["c"][1], ctx))
        elif t in ("Code",):
            toks.append([f"<code>{esc(n['c'][1])}</code>", ctx.ans])
        # Note / RawInline 等忽略
    return toks


def _inch_px(v):
    if not v:
        return 0
    m = re.match(r"([\d.]+)in", str(v))
    return int(round(float(m.group(1)) * 96)) if m else 0


def _drop_stray_ublanks(toks):
    """緊貼在答案旁邊的底線空白＝答案本來寫在底線上，不是另一個空格 → 拿掉。"""
    out = []
    for i, tk in enumerate(toks):
        if tk[0] == UBLANK and not tk[1]:
            def near(rng):
                for j in rng:
                    if toks[j][0].strip() == "":
                        continue
                    return toks[j][1]
                return False
            if near(range(i - 1, -1, -1)) or near(range(i + 1, len(toks))):
                continue
        out.append(tk)
    return out


def _merge(toks):
    toks = _drop_stray_ublanks(toks)
    out = []
    for h, a in toks:
        if out and out[-1][1] == a:
            out[-1][0] += h
        else:
            out.append([h, a])
    i = 1
    while i < len(out) - 1:      # 兩段答案之間只隔空白 → 併成一個挖空
        if (not out[i][1] and out[i][0].strip() == ""
                and out[i - 1][1] and out[i + 1][1]):
            out[i - 1][0] += out[i][0] + out[i + 1][0]
            del out[i:i + 2]
        else:
            i += 1
    return out


BLANK = ('<span class="blank" onclick="tb(this)"><span class="q">？</span>'
         '<span class="a">{}</span></span>')


def toks_html(toks):
    parts = []
    for h, a in _merge(toks):
        if a and h.strip():
            parts.append(BLANK.format(h))
        else:
            parts.append(h)
    return "".join(parts).strip()


def inl_html(inls, ctx):
    return toks_html(walk_inlines(inls, ctx))


def n_blanks(h):
    return h.count('class="blank"')


# --------------------------------------------------------------- 4. 區塊走訪
NOTE_KINDS = {"易錯": "trap", "脈絡導讀": "lead", "考場心法": "mind",
              "遷移提示": "tip", "怎麼讀這本": "howto"}
P_STYLES = {"Body Text", "First Paragraph", "Compact", "", "Normal"}


def _plain(h):
    """HTML → 純文字（做標題、選單、比對用）。"""
    t = re.sub(r"<[^>]+>", "", h)
    t = t.replace("\\(", "").replace("\\)", "").replace("\\[", "").replace("\\]", "")
    t = _html.unescape(t)
    t = re.sub(r"\\[a-zA-Z]+", " ", t)
    t = re.sub(r"[{}\\$]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def blocks_of(blks, ctx, indent=0):
    out = []
    for b in blks or []:
        out.extend(one_block(b, ctx, indent))
    return out


def one_block(b, ctx, indent=0):
    t = b["t"]
    if t == "Div":
        st = _style(b["c"][0])
        inner = b["c"][1]
        if st.startswith("toc") or st == "TOC-Heading":
            return []
        if st == "SecHead":
            h, figs = _para_html(inner, ctx, extract=True)
            p = _plain(h)
            kind = "sec"
            if p.startswith("◆"):
                kind = ("flow" if "判斷流程" in p else
                        "link" if "跨章鏈結" in p else
                        "drill" if "練習指引" in p else "mark")
            out = [{"t": "sec", "html": h.lstrip("◆ "), "plain": p.lstrip("◆ ").strip(),
                    "kind": kind}]
            out += [_fig_block(im, float_=True) for im in figs]
            return out
        if st == "SubHead":
            h, figs = _para_html(inner, ctx, extract=True)
            return ([{"t": "sub", "html": h}]
                    + [_fig_block(im, float_=True) for im in figs])
        if st == "NoteBox":
            return [_note_block(inner, ctx)]
        if st == "HL":
            # 「考場心法」在 Word 是 HL 樣式（藍色左邊條），語意上是提示框 → 轉成 note
            h = _para_html(inner, ctx)[0]
            m = re.match(r"^(?:<b>)?(" + "|".join(NOTE_KINDS) + r")(?:</b>)?[　 ]*",
                         h)
            if m:
                return [{"t": "note", "kind": NOTE_KINDS[m.group(1)],
                         "label": m.group(1), "paras": [h[m.end():]]}]
            return [{"t": "hl", "html": h}]
        if st == "Image Caption":
            return [{"t": "cap", "html": _para_html(inner, ctx)[0]}]
        if st in ("Captioned Figure", "Figure"):
            return blocks_of(inner, ctx, indent)
        if st == "List Paragraph":
            return _para_blocks(inner, ctx, max(indent, 1))
        return _para_blocks(inner, ctx, indent)
    if t in ("Para", "Plain"):
        return _para_blocks([b], ctx, indent)
    if t == "BlockQuote":
        return blocks_of(b["c"], ctx, indent + 1)
    if t == "BulletList":
        items = []
        for it in b["c"]:
            items.extend(_li(it, ctx, 0))
        return [{"t": "ul", "items": items}] if items else []
    if t == "OrderedList":
        items = []
        for i, it in enumerate(b["c"][1]):
            items.extend(_li(it, ctx, 0, _num(b["c"][0], i)))
        return [{"t": "ul", "items": items}] if items else []
    if t == "Table":
        return [_table_block(b, ctx)]
    if t == "Figure":
        attr, cap, body = b["c"]
        blocks = blocks_of(body, ctx, indent)
        cap_html = ""
        for cb in blocks_of(cap[1] if isinstance(cap, list) else [], ctx):
            cap_html += cb.get("html", "")
        for blk in blocks:
            if blk["t"] == "fig" and cap_html and not blk.get("cap"):
                blk["cap"] = cap_html
        return blocks
    if t == "Header":       # 章標題由外層處理；其餘層級當小節標題
        lvl, attr, inls = b["c"]
        h = inl_html(inls, ctx)
        return [{"t": "sec", "html": h, "plain": _plain(h), "kind": "sec"}] if h else []
    if t in ("HorizontalRule",):
        return [{"t": "hr"}]
    if t in ("CodeBlock", "RawBlock", "Null"):
        return []
    if t == "LineBlock":
        return [{"t": "p", "html": toks_html(walk_inlines(
            [i for ln in b["c"] for i in ln + [{"t": "LineBreak"}]], ctx)), "indent": indent}]
    if t == "DefinitionList":
        return []
    return []


def _img_tag(im, cls="cfig"):
    w = (f' style="max-width:min(100%,{im["w"]}px)"' if im.get("w") else "")
    alt = _html.escape(_plain(im.get("alt", "")), quote=True)
    return (f'<img class="{cls}" src="img/{im["src"]}" alt="{alt}" '
            f'loading="lazy"{w}>')


def _fig_block(im, float_=False, cap=""):
    b = {"t": "fig", "src": im["src"], "w": im.get("w", 0),
         "alt": _plain(im.get("alt", "")), "cap": cap}
    if float_:
        b["float"] = True
    return b


def _para_html(blks, ctx, extract=False):
    """把 Div 內的段落串接成一段 HTML。回傳 (html, 圖片清單)。

    extract=True：圖片抽出來給呼叫者（標題列的浮動小圖）；
    extract=False：圖片就地變成 <img>（表格格子、圖說）。
    """
    parts, figs = [], []
    for b in blks or []:
        if b["t"] in ("Para", "Plain"):
            before = len(ctx.images)
            h = inl_html(b["c"], ctx)
            imgs = ctx.images[before:]
            segs = h.split("\x00IMG\x00")
            buf = ""
            for i, seg in enumerate(segs):
                buf += seg
                if i < len(imgs):
                    if extract:
                        figs.append(imgs[i])
                    else:
                        buf += _img_tag(imgs[i])
            parts.append(buf)
        else:
            for blk in one_block(b, ctx):
                if blk.get("html"):
                    parts.append(blk["html"])
                elif blk["t"] == "fig":
                    if extract:
                        figs.append(blk)
                    else:
                        parts.append(_img_tag(blk))
    return " ".join(p for p in parts if p.strip()), figs


def _para_blocks(blks, ctx, indent):
    """段落 → p / dmath / fig（圖片自成一塊）。"""
    out = []
    for b in blks or []:
        if b["t"] not in ("Para", "Plain"):
            out.extend(one_block(b, ctx, indent))
            continue
        before = len(ctx.images)
        toks = walk_inlines(b["c"], ctx)
        imgs = ctx.images[before:]
        html = toks_html(toks)
        segs = html.split("\x00IMG\x00")
        for i, seg in enumerate(segs):
            if seg.strip() and seg.strip() != "&nbsp;":
                # 整段就是一條顯示數學 → 自成一塊，置中呈現
                if re.fullmatch(r"\\\[.*\\\]", seg.strip(), re.S):
                    out.append({"t": "dmath", "html": seg.strip()})
                elif re.fullmatch(
                        r'<span class="blank"[^>]*><span class="q">？</span>'
                        r'<span class="a">\\\[.*\\\]</span></span>', seg.strip(), re.S):
                    out.append({"t": "dmath", "html": seg.strip()})
                # 被切開的顯示數學（題目＋答案按鈕）：整段置中，維持同一行
                elif "\\(\\displaystyle" in seg:
                    out.append({"t": "dmath", "html": seg.strip()})
                else:
                    out.append({"t": "p", "html": seg.strip(), "indent": indent})
            if i < len(imgs):
                out.append({"t": "fig", "src": imgs[i]["src"], "w": imgs[i]["w"],
                            "alt": _plain(imgs[i]["alt"]), "cap": ""})
    return out


def _note_block(inner, ctx):
    """NoteBox：抓開頭的徽章／粗體標籤決定樣式（易錯／脈絡導讀／考場心法／遷移提示）。"""
    label, kind = "", "plain"
    first = None
    for b in inner:
        if b["t"] in ("Para", "Plain") and b["c"]:
            first = b["c"]
            break
    if first:
        f = first[0]
        cand = ""
        if f["t"] == "Span" and _style(f["c"][0]) in BADGE_CLASS:
            cand = _plain(inl_html(f["c"][1], Ctx()))
        elif f["t"] == "Strong":
            cand = _plain(inl_html(f["c"], Ctx()))
        if cand in NOTE_KINDS:
            label, kind = cand, NOTE_KINDS[cand]
            del first[0]
            while first and first[0]["t"] in ("Space", "SoftBreak"):
                del first[0]
            if first and first[0]["t"] == "Str":
                first[0]["c"] = first[0]["c"].lstrip("\u3000 ")
    paras = []
    for b in inner:
        if b["t"] in ("Para", "Plain"):
            h = inl_html(b["c"], ctx)
            if h.strip():
                paras.append(h)
        else:
            for blk in one_block(b, ctx):
                if blk.get("html"):
                    paras.append(blk["html"])
    return {"t": "note", "kind": kind, "label": label, "paras": paras}


def _num(attrs, i):
    """OrderedList 的編號文字（Word 的「(1)(2)」在 pandoc 是 TwoParens）。"""
    start, _sty, delim = attrs
    n = start + i
    d = delim["t"] if isinstance(delim, dict) else str(delim)
    return f"({n})" if d == "TwoParens" else (f"{n})" if d == "OneParen" else f"{n}.")


def _li(item, ctx, lvl, num=None):
    """清單項目（可含巢狀清單）→ 扁平化成帶 lvl 的項目串。num＝編號文字（有序清單）。"""
    out = []
    head = []
    for b in item:
        if b["t"] in ("Para", "Plain"):
            before = len(ctx.images)
            h = toks_html(walk_inlines(b["c"], ctx))
            imgs = ctx.images[before:]
            segs = h.split("\x00IMG\x00")
            for i, seg in enumerate(segs):
                if seg.strip():
                    it = {"lvl": lvl, "html": seg.strip()}
                    if num and not head:
                        it["num"] = num
                    head.append(it)
                if i < len(imgs):
                    head.append({"lvl": lvl, "fig": imgs[i]["src"], "w": imgs[i]["w"],
                                 "alt": _plain(imgs[i]["alt"]), "html": ""})
        elif b["t"] in ("BulletList", "OrderedList"):
            ordered = b["t"] == "OrderedList"
            subs = b["c"][1] if ordered else b["c"]
            for k, s in enumerate(subs):
                head.extend(_li(s, ctx, lvl + 1,
                                _num(b["c"][0], k) if ordered else None))
        elif b["t"] == "BlockQuote":
            for blk in blocks_of(b["c"], ctx):
                if blk.get("html"):
                    head.append({"lvl": lvl + 1, "html": blk["html"]})
                elif blk["t"] == "note":
                    head.append({"lvl": lvl + 1, "html": " ".join(blk["paras"])})
        else:
            for blk in one_block(b, ctx):
                if blk.get("html"):
                    head.append({"lvl": lvl, "html": blk["html"]})
    out.extend(head)
    return out


def _cells(row, ctx):
    """一列 → [{html, rs, cs}]（保留 Word 的跨欄／跨列）。"""
    out = []
    for c in row[1]:
        h, _figs = _para_html(c[4], ctx)
        cell = {"html": h}
        if c[2] > 1:
            cell["rs"] = c[2]
        if c[3] > 1:
            cell["cs"] = c[3]
        out.append(cell)
    return out


def _table_block(b, ctx):
    _, cap, specs, head, bodies, foot = b["c"]
    hd = [_cells(row, ctx) for row in head[1]]
    rows = []
    for body in bodies:
        for row in body[3]:
            rows.append(_cells(row, ctx))
    if not hd and rows:
        hd, rows = [rows[0]], rows[1:]
    return {"t": "table", "head": hd, "rows": rows, "cols": len(specs)}


# ------------------------------------------------------------------ 5. 主流程
CH_RE = re.compile(r"^第(.+?)章[\s\u3000]*(.*)$")
NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8,
       "九": 9, "十": 10, "十一": 11, "十二": 12, "十三": 13}


def mark_appendix(blocks):
    """章末「考場心法」之後若還有內容（如第 13 章的解二元一次聯立），補一個小節標題，
    否則它會被塞進「練習指引」那張卡裡。"""
    last = -1
    for i, b in enumerate(blocks):
        if b["t"] == "note" and b.get("kind") == "mind":
            last = i
    if last < 0 or last == len(blocks) - 1:
        return blocks
    rest = blocks[last + 1:]
    if not any(b["t"] in ("p", "ul", "table", "hl", "fig", "ex") for b in rest):
        return blocks
    head = rest[0]
    if head["t"] == "ul" and len(head["items"]) == 1:
        h = head["items"][0]["html"]
        sec = {"t": "sec", "html": h, "plain": _plain(h), "kind": "star"}
        return blocks[:last + 1] + [sec] + rest[1:]
    sec = {"t": "sec", "html": "補充", "plain": "補充", "kind": "star"}
    return blocks[:last + 1] + [sec] + rest


def group_examples(blocks):
    """把「範例 → 解 → 說明」連續段落收成一個 ex 區塊（視覺上成為一個示範例卡）。"""
    out, cur = [], None
    STOP = {"sec", "sub", "note", "hl", "table"}
    for b in blocks:
        is_ex_head = (b["t"] == "p" and 'bdg bg-ex">範例' in b.get("html", ""))
        if is_ex_head:
            cur = {"t": "ex", "blocks": [b]}
            out.append(cur)
            continue
        if cur is not None:
            if b["t"] in STOP:
                cur = None
            else:
                cur["blocks"].append(b)
                continue
        out.append(b)
    return out


def fix_intercept_annot(ch):
    """第 3 章「截距式」：原稿用定位點把 (a,0)／(0,b) 排在上一行「x軸截距為a」「y軸截距為b」
    的正下方，轉檔後會掉成獨立一行、失去對應關係。這裡把兩個註記掛回各自的詞下面。

    找不到預期的原文就回 False（原稿改過 → 建置時會印警告，提醒回來看這段）。
    """
    if ch["n"] != 3:
        return None
    OLD = "<em>x</em>軸截距為<em>a，y</em>軸截距為<em>b</em>"
    for bi, b in enumerate(ch["blocks"]):
        if b["t"] != "ul":
            continue
        for it in b["items"]:
            if "截距式" not in it["html"]:
                continue
            if OLD not in it["html"]:
                return False
            nxt = ch["blocks"][bi + 1] if bi + 1 < len(ch["blocks"]) else None
            if not nxt or nxt["t"] != "p" or "blank" not in nxt.get("html", ""):
                return False
            m = re.search(r'<span class="a">(.*?)</span></span>', nxt["html"], re.S)
            if not m:
                return False
            # 「( a , 0 ) ( 0 , b )」→ 依括號切成兩段註記，依序對應 x／y 截距
            ps = [p.strip() for p in re.findall(r"[^()]*\([^()]*\)", m.group(1))]
            if len(ps) != 2:
                return False

            def ann(word, note):
                return ('<span class="ann"><span class="ann-t">' + word + "</span>"
                        + '<span class="ann-b">' + BLANK.format(note) + "</span></span>")

            it["html"] = it["html"].replace(
                OLD, ann("<em>x</em> 軸截距為 <em>a</em>", ps[0]) + "，"
                + ann("<em>y</em> 軸截距為 <em>b</em>", ps[1]))
            del ch["blocks"][bi + 1]
            return True
    return False


# 原稿錯字：網頁版直接改掉（Word 原稿要不要跟著改由老師決定）
TYPO_FIXES = [
    ("空間中個元素的關係", "空間中各元素的關係"),   # 第12章 三、
]

# 原稿解析度太低、放大就糊的圖 → 換成重畫的 SVG（放在 build/assets/guide-figs/）
# {原檔名: (替換檔名, 顯示寬度 px)}
IMG_SWAP = {
    "image31.png": ("fig_ch12_skew.svg", 320),   # 第12章 三、兩直線的 u、v（原檔只有 92×69）
}


def apply_img_swap(x):
    if isinstance(x, list):
        return [apply_img_swap(v) for v in x]
    if isinstance(x, dict):
        for key in ("src", "fig"):
            if x.get(key) in IMG_SWAP:
                new, w = IMG_SWAP[x[key]]
                x[key], x["w"] = new, w
        return {k: apply_img_swap(v) for k, v in x.items()}
    return x


def apply_typo_fixes(x):
    """把 TYPO_FIXES 套到所有文字欄位（含清單項目、表格格子）。"""
    if isinstance(x, list):
        return [apply_typo_fixes(v) for v in x]
    if isinstance(x, dict):
        return {k: apply_typo_fixes(v) for k, v in x.items()}
    if isinstance(x, str):
        for old, new in TYPO_FIXES:
            x = x.replace(old, new)
    return x


def split_off_appendix(ch):
    """章末 ★ 補充段（第 13 章的「解二元一次聯立方程組」）→ 切出來自成一頁。

    老師要求不要併在矩陣章裡。回傳新的一頁（dict）或 None；
    小節標題只留下聯立方程式本體，章名交給頁面標題。
    """
    for i, b in enumerate(ch["blocks"]):
        if b["t"] == "sec" and b.get("kind") == "star":
            rest = ch["blocks"][i:]
            ch["blocks"] = ch["blocks"][:i]
            m = re.search(r"\\\(", b["html"])
            title = _plain(b["html"][:m.start()] if m else b["html"]) or "補充"
            if m:
                rest[0] = dict(b, html=b["html"][m.start():], plain=title)
            return {"n": 90 + ch["n"], "cn": "附錄", "kind": "appendix",
                    "title": title, "from_ch": ch["n"], "blocks": rest}
    return None


def _iter_blocks(blocks):
    for b in blocks:
        yield b
        if b["t"] == "ex":
            for s in b["blocks"]:
                yield s


def _block_text(b):
    """區塊（含清單項目）的純文字，供錨點比對。"""
    s = []
    for k, v in b.items():
        if k in ("html", "plain", "label"):
            s.append(v)
        elif k == "paras":
            s.extend(v)
        elif k in ("items", "blocks"):
            for it in v:
                s.append(_block_text(it))
        elif k in ("head", "rows"):
            for row in v:
                for c in row:
                    s.append(c.get("html", "") if isinstance(c, dict) else str(c))
    return _plain(" ".join(x for x in s if x))


def _cell_blank(c):
    """格子是不是空的（只有底線留白也算空，補圖要蓋上去）。"""
    h = re.sub(r'<span class="ublank"></span>', "", c["html"])
    return not h.strip() and "<img" not in c["html"]


def inject_figs(ch):
    """把 pdf_figs.py 裁出的 Word 手繪圖安插回內容（表格格子／指定段落後）。"""
    n, hit = ch["n"], []
    for cn, label, start, files in TABLE_FIGS:
        if cn != n:
            continue
        for b in _iter_blocks(ch["blocks"]):
            if b["t"] != "table":
                continue
            for row in b["rows"]:
                if row and _plain(row[0]["html"]) == label:
                    for i, f in enumerate(files):
                        j = start + i
                        if j < len(row) and _cell_blank(row[j]):
                            row[j]["html"] = _img_tag(
                                {"src": f, "w": VFIG.get(f, {}).get("w", 0)},
                                "cfig tfig-in")
                            hit.append(f)
    empt = [x for x in EMPTY_ROW_FIGS if x[0] == n]
    if empt:
        idx = 0
        for b in _iter_blocks(ch["blocks"]):
            if b["t"] != "table":
                continue
            for row in b["rows"]:
                if row and all(_cell_blank(c) for c in row):
                    for _cn, ri, files in empt:
                        if ri == idx:
                            for k, c in enumerate(row):
                                if k < len(files):
                                    c["html"] = _img_tag(
                                        {"src": files[k],
                                         "w": VFIG.get(files[k], {}).get("w", 0)},
                                        "cfig tfig-in")
                                    hit.append(files[k])
                    idx += 1
    for cn, anchor, f, cap, fl in AFTER_FIGS:
        if cn != n:
            continue
        for i, b in enumerate(ch["blocks"]):
            if anchor in _block_text(b):
                fig = {"t": "fig", "src": f, "w": VFIG.get(f, {}).get("w", 0),
                       "alt": cap, "cap": cap}
                if fl:
                    fig["float"] = True
                ch["blocks"].insert(i + 1, fig)
                hit.append(f)
                break
    return hit


def build(docx_path):
    tmp = tempfile.mkdtemp(prefix="guide_")
    marked = os.path.join(tmp, "marked.docx")
    print(f"讀取：{docx_path}")
    inject_markers(docx_path, marked)
    media = os.path.join(tmp, "media")
    js = os.path.join(tmp, "ast.json")
    subprocess.run(["pandoc", "-f", "docx+styles", "-t", "json",
                    f"--extract-media={media}", marked, "-o", js], check=True)
    ast = json.load(open(js, encoding="utf-8"))

    ctx = Ctx()
    chapters, intro, cur = [], [], None
    for b in ast["blocks"]:
        if b["t"] == "Header" and b["c"][0] == 1:
            title = _plain(inl_html(b["c"][2], Ctx()))
            m = CH_RE.match(title)
            if m:
                n = NUM.get(m.group(1), len(chapters) + 1)
                cur = {"n": n, "cn": m.group(1), "title": m.group(2).strip(),
                       "blocks": []}
                chapters.append(cur)
                continue
        blks = one_block(b, ctx)
        (cur["blocks"] if cur else intro).extend(blks)

    # 前言：只留「怎麼讀這本」那段（首頁用）
    howto = next((b for b in intro if b["t"] == "note" and b["kind"] == "howto"), None)

    vfigs = 0
    for ch in chapters:
        ch["blocks"] = mark_appendix(group_examples(_tidy(ch["blocks"])))
        vfigs += len(inject_figs(ch))
        if fix_intercept_annot(ch) is False:
            print("  ⚠ 第3章「截距式」的 (a,0)／(0,b) 註記沒對上原文，"
                  "請看 fix_intercept_annot()")

    # 章末 ★ 補充段獨立成頁（附錄），排在所有章之後
    for ch in list(chapters):
        ap = split_off_appendix(ch)
        if ap:
            chapters.append(ap)
            print(f"  附錄獨立成頁：{ap['title']}（原在第 {ap['from_ch']} 章章末）")

    chapters = apply_img_swap(apply_typo_fixes(chapters))
    for ch in chapters:
        ch["file"] = (f"附錄_{ch['title']}.html" if ch.get("kind") == "appendix"
                      else f"第{ch['n']:02d}章_{ch['title']}.html")
        ch["blanks"] = _count_blanks(ch["blocks"])
        ch["secs"] = [b["plain"] for b in ch["blocks"]
                      if b["t"] == "sec" and b["kind"] == "sec"]

    # 圖片：docx 內嵌圖（pandoc 抽出）複製到 guide-img/；補圖由 pdf_figs.py 產生，不動
    used = {im["src"] for im in ctx.images}
    os.makedirs(IMG_DIR, exist_ok=True)
    found = 0
    for root, _dirs, files in os.walk(media):
        for f in files:
            if f in used:
                shutil.copy(os.path.join(root, f), os.path.join(IMG_DIR, f))
                found += 1
    miss = sorted(used - set(os.listdir(IMG_DIR)))
    print(f"  內嵌圖：{found}/{len(used)} → guide-img/"
          + (f"（缺 {miss}）" if miss else "") + f"；補圖插入 {vfigs} 處")

    data = {"title": "學測數學A 複習講義",
            "subtitle": "11 章脈絡複習 · 條列重點 × 跨章連結",
            "source": os.path.basename(docx_path),
            "howto": howto,
            "chapters": chapters}
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    tot = sum(c["blanks"] for c in chapters)
    print(f"寫出：{OUT_JSON}")
    print(f"  {len(chapters)} 章、挖空 {tot} 個")
    for ch in chapters:
        _lab = "附錄  " if ch.get("kind") == "appendix" else f"第{ch['n']:2d}章"
        print(f"   {_lab} {ch['title']:<12} 區塊 {len(ch['blocks']):3d}　"
              f"挖空 {ch['blanks']:3d}　節 {len(ch['secs'])}")
    shutil.rmtree(tmp, ignore_errors=True)


def _tidy(blocks):
    """收尾：連續的無標籤 NoteBox 併進前一個（Word 裡導讀被拆成好幾段）、丟掉空塊。"""
    out = []
    for b in blocks:
        if b["t"] == "note":
            if (b["kind"] == "plain" and out and out[-1]["t"] == "note"):
                out[-1]["paras"].extend(b["paras"])
                continue
            if not b["paras"]:
                continue
        # 「考場心法」後面緊接的粉底方塊是心法的後續句子（原稿同一個框）→ 併進去，
        # 否則會被當成章末補充、甚至被切成獨立一頁
        if (b["t"] == "hl" and out and out[-1]["t"] == "note"
                and out[-1].get("kind") == "mind"):
            out[-1]["paras"].append(b["html"])
            continue
        if b["t"] == "p" and not _plain(b["html"]) and "\\(" not in b["html"]:
            continue
        # Word 圖形上的文字框（P、Q、R…）會落成單獨一段；圖本身已含標籤 → 丟掉
        if b["t"] == "p" and re.fullmatch(r"[A-Za-z0-9]", b["html"].strip()):
            continue
        out.append(b)
    return out


def _count_blanks(blocks):
    return json.dumps(blocks, ensure_ascii=False).count("tb(this)")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOCX)
