# -*- coding: utf-8 -*-
"""脈絡複習講義 → 網頁版（13 章 + 目錄頁），視覺與 concept-map 站一致。

單一來源：content/guide_data.json（由 build/docx2guide.py 從教師版 .docx 產生）。
圖片來源：guide-img/（docx 內嵌圖 + build/pdf_figs.py 從 PDF 裁的手繪圖）。

輸出：guide/index.html、guide/第01章_數與式.html …、guide/img/*
      CSS／JS／頁尾／分享卡／流量統計全部沿用 build_html.py 與 build/assets/。

學生版的每個填空 → 一顆「？」按鈕，點一下顯示答案（教師版的玫瑰色答案）；
頂欄可「全部顯示答案／全部隱藏」，等於一頁同時是學用與教用。

用法（在 concept-map/ 下）：
  python build/build_guide.py
"""
import html as _html
import json
import os
import re
import shutil
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from build_html import (ANALYTICS, PRIVACY_HTML, LIGHTBOX_HTML,  # noqa: E402
                        FAVICON_HTML, OG_SITE_NAME, SITE_BASE, _asset, _esc_attr)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = os.path.dirname(ROOT)                       # 站台根（GitHub Pages 的 /web/）
DATA = os.path.join(ROOT, "content", "guide_data.json")
OUT = os.path.join(REPO, "guide")                  # 發布位置：/web/guide/（與 exam/ 同層）
IMG = os.path.join(OUT, "img")                     # 圖片（docx 內嵌 + PDF 裁圖）
KATEX_SRC = os.path.join(ROOT, "katex")            # 自帶一份 KaTeX（同 exam/ 的作法）
SITE_ROOT = SITE_BASE.replace("concept-map/", "")  # https://…/web/
OG_IMG = SITE_ROOT + "og-cover.png"

CN = ["", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三"]


def is_ap(c):
    return c.get("kind") == "appendix"


def label(c):
    """頁面／選單上的名稱：章 → 「第一章」，章末補充 → 「附錄」。"""
    return "附錄" if is_ap(c) else f"第{CN[c['n']]}章"


def badge(c):
    return "附" if is_ap(c) else CN[c["n"]]

TITLE = "學測數學A 複習講義"        # 主標題（目錄頁 h1／各頁副標／分享卡）
TB_TITLE = "複習講義"                # 頂欄短標題

SEC_ICON = {"flow": "🧭", "link": "🔗", "drill": "📝", "mark": "◆", "star": "★"}
SEC_CLASS = {"flow": "c-flow", "link": "c-link", "drill": "c-drill",
             "mark": "c-mark", "star": "c-star"}
NOTE_LAB = {"lead": "脈絡導讀", "trap": "易錯", "mind": "考場心法",
            "tip": "遷移提示", "howto": "怎麼讀這本"}

# ---------------------------------------------------------------- 講義專屬樣式
GUIDE_CSS = """
  /* ===== 脈絡複習講義（沿用站台色系，只加本頁需要的元件） ===== */
  .g-lead{background:var(--callout); border-left:5px solid #d9a13b; border-radius:0 12px 12px 0;
    padding:14px 18px; margin:16px 0 26px; font-size:15.5px; color:#5c4438}
  .g-lead .nlab{display:inline-block; background:#8c2740; color:#fff; font-weight:800;
    font-size:13px; border-radius:6px; padding:1px 10px; margin-right:8px; vertical-align:1px}
  .g-lead p{margin:.4em 0}
  .g-lead p:first-of-type{display:inline}
  .card.sec-card{padding:18px 22px 22px}
  .card .sec-h{color:var(--maroon); font-size:19.5px; font-weight:800; margin:0 0 10px;
    display:flex; align-items:baseline; gap:9px; scroll-margin-top:70px}
  .card .sec-h .num{flex:0 0 auto; background:var(--maroon); color:#fff; border-radius:8px;
    padding:1px 9px; font-size:15px; font-weight:800}
  .sub-h{display:block; width:fit-content; margin:22px 0 8px; padding:3px 12px; border-radius:6px;
    background:#f3e3e8; color:var(--maroon-d); font-weight:800; font-size:15.5px}
  .sub-h:first-child{margin-top:4px}
  .gp{margin:.55em 0; font-size:16px}
  .gp.ind{margin-left:1.6em}
  .dm{margin:.6em 0; text-align:center; overflow-x:auto}
  /* 條列重點 */
  ul.glist{margin:.4em 0 .6em; padding-left:2px; list-style:none}
  ul.glist>li{position:relative; padding:6px 2px 6px 20px}
  ul.glist>li::before{content:"▪"; position:absolute; left:2px; top:5px; color:var(--rose);
    font-weight:800}
  ul.glist>li>.n{position:absolute; left:-2px; top:6px; color:var(--maroon-d); font-weight:700;
    font-size:14.5px}
  ul.glist>li.numbered{padding-left:34px}
  ul.glist>li.numbered::before{content:none}
  ul.glist ul.glist{margin:2px 0 0}
  ul.glist ul.glist>li{padding:4px 2px 4px 18px; font-size:15.5px}
  ul.glist ul.glist>li::before{content:"–"; color:#b98aa0}
  ul.glist ul.glist>li.numbered::before{content:none}
  ul.glist ul.glist ul.glist>li::before{content:"·"}
  ul.glist>li.figli, ul.glist ul.glist>li.figli{padding:2px 0; text-align:center}
  ul.glist>li.figli::before, ul.glist ul.glist>li.figli::before{content:none}
  /* 原稿用「下一行對齊」的註記（截距式的 (a,0)／(0,b)）：掛在該詞下方 */
  .ann{display:inline-block; text-align:center; vertical-align:top; margin:0 1px}
  .ann>.ann-t{display:block; border-bottom:1px solid #cbb7ae; padding:0 2px}
  .ann>.ann-b{display:block; font-size:.95em; line-height:1.6; margin-top:3px}
  /* 原稿就留白的填空（連教師版都沒答案）＝畫一條底線，讓人知道這裡要自己寫 */
  .ublank{display:inline-block; min-width:4.5em; border-bottom:1.5px dashed #c4aeb6;
    margin:0 .3em; vertical-align:-2px}
  /* 重點框（原 Word 的粉底方塊：公式主結果） */
  .hl{background:#fbeef2; border-left:4px solid var(--rose); border-radius:0 10px 10px 0;
    padding:9px 16px; margin:12px 0; font-size:16.5px}
  /* 提示框 */
  .nbox{border-radius:0 10px 10px 0; padding:10px 16px; margin:14px 0; font-size:15px}
  .nbox p{margin:.35em 0}
  .nbox p:first-of-type{display:inline}
  .nbox .nlab{display:inline-block; font-weight:800; font-size:12.5px; border-radius:6px;
    padding:1px 9px; margin-right:8px; vertical-align:1px; white-space:nowrap}
  .n-trap{background:#fdf1f4; border-left:4px solid #b03a5b; color:#6b4049}
  .n-trap .nlab{background:#b03a5b; color:#fff}
  .n-mind{background:#eef6f1; border-left:4px solid var(--btn); color:#3f5a53}
  .n-mind .nlab{background:var(--btn); color:#fff}
  .n-tip{background:#fff7ef; border-left:4px solid #d9a13b; color:#5c4438}
  .n-tip .nlab{background:#c07d18; color:#fff}
  .n-plain{background:#faf7f4; border-left:4px solid var(--line); color:#5a4a44}
  /* 範例／解 */
  .bdg{display:inline-block; color:#fff; font-size:12.5px; font-weight:800; border-radius:6px;
    padding:1px 9px; margin-right:6px; vertical-align:2px; white-space:nowrap}
  .bg-ex{background:#2e7d5b}
  .bg-trap{background:#b03a5b}
  .exbox{background:#f6faf7; border:1px solid #d7e8de; border-left:4px solid #2e7d5b;
    border-radius:0 10px 10px 0; padding:10px 16px; margin:14px 0}
  .exbox .gp{margin:.4em 0}
  .exbox ul.glist{margin:.2em 0}
  /* 圖 */
  figure.gfig{margin:14px auto; text-align:center; background:#fbfafc; border:1px solid var(--line);
    border-radius:12px; padding:10px 12px 8px; max-width:100%; width:fit-content}
  figure.gfig img{display:block; max-width:100%; height:auto; margin:0 auto; cursor:zoom-in}
  figure.gfig figcaption{font-size:13px; color:#5a4a52; margin-top:6px; font-weight:600}
  figure.gfig.gfig-float{float:right; margin:4px 0 10px 18px; max-width:min(46%,300px)}
  @media(max-width:600px){figure.gfig.gfig-float{float:none; margin:12px auto; max-width:100%}}
  img.cfig{max-width:100%; height:auto; vertical-align:middle; cursor:zoom-in}
  .lb-scroll img{width:min(960px,96vw) !important; max-width:none !important; height:auto;
    background:#fff; border-radius:12px; box-shadow:0 8px 40px rgba(0,0,0,.5); vertical-align:top}
  /* 表格 */
  .tw{overflow-x:auto; margin:14px 0}
  table.gt{border-collapse:collapse; width:100%; font-size:15px; background:#fff}
  table.gt th{background:#f3e3e8; color:var(--maroon-d); padding:8px 12px; border:1px solid #dcc7cf;
    font-weight:800; text-align:center}
  table.gt td{padding:8px 12px; border:1px solid var(--line); vertical-align:middle}
  table.gt tbody td:first-child{background:#faf2f5; font-weight:700; color:var(--maroon-d)}
  table.gt td.mid{text-align:center}
  /* 章末三張卡 */
  .card.c-flow{border-left-color:#b45309}
  .card.c-flow .sec-h{color:#b45309}
  .card.c-flow .sec-h .num{background:#b45309}
  .card.c-link{border-left-color:var(--btn); background:#f7fbfa}
  .card.c-link .sec-h{color:#17595f}
  .card.c-link .sec-h .num{background:var(--btn)}
  .card.c-drill{border-left-color:#2e7d5b; background:#f8fbf9}
  .card.c-drill .sec-h{color:#256c4d}
  .card.c-drill .sec-h .num{background:#2e7d5b}
  .card.c-star{border-left-color:#7a5ea8}
  .card.c-star .sec-h{color:#5e4487; font-size:18px}
  .card.c-star .sec-h .num{background:#7a5ea8}
  /* 上一章／下一章 */
  .chnav{display:flex; gap:12px; margin:26px 0 6px; flex-wrap:wrap}
  .chnav a{flex:1 1 200px; background:#fff; border:1px solid var(--line); border-left:4px solid var(--maroon);
    border-radius:10px; padding:10px 16px; text-decoration:none; color:var(--maroon-d);
    font-weight:700; font-size:15px; box-shadow:0 2px 8px rgba(80,40,30,.06)}
  .chnav a:hover{background:#faf2f5}
  .chnav a small{display:block; font-weight:600; color:#9a857c; font-size:12.5px}
  .chnav a.next{text-align:right}
  /* 目錄頁 */
  .g-toc{display:flex; flex-direction:column; gap:14px; margin-top:6px}
  .g-ch{background:#fff; border-radius:14px; border-left:5px solid var(--maroon);
    box-shadow:0 2px 10px rgba(80,40,30,.07); overflow:hidden}
  .g-ch-h{display:flex; align-items:center; gap:10px; padding:13px 18px; text-decoration:none;
    color:var(--maroon); font-size:19px; font-weight:800}
  .g-ch-h:hover{background:#faf2f5}
  .g-ch-h .num{flex:0 0 auto; background:var(--maroon); color:#fff; border-radius:8px;
    padding:1px 10px; font-size:14.5px}
  .g-ch-h .cnt{margin-left:auto; font-size:14px; font-weight:700; color:var(--blue,#1f6f78);
    white-space:nowrap}
  .g-secs{display:grid; grid-template-columns:repeat(auto-fill,minmax(215px,1fr)); gap:7px;
    padding:0 18px 15px}
  .g-secs a{display:block; padding:8px 12px; background:#faf6f2; border:1px solid var(--line);
    border-radius:9px; color:#4a3a34; text-decoration:none; font-size:14.5px}
  .g-secs a:hover{background:#f3e3e8; color:var(--maroon-d); border-color:#d9c2c9}
  .g-stat{display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin:10px 0 2px}
  .g-stat span{background:#fff; border:1px solid var(--line); border-radius:20px;
    padding:4px 14px; font-size:13.5px; color:#6b5249}
  .g-stat b{color:var(--maroon)}
"""

GUIDE_JS = """
  // 圖片燈箱：點圖放大（沿用站台 .lightbox 樣式）
  (function(){
    var lb=document.getElementById('lightbox'); if(!lb) return;
    var sc=document.getElementById('lb-scroll');
    function op(img){ var c=img.cloneNode(true); c.removeAttribute('style'); c.className='';
      sc.innerHTML=''; sc.appendChild(c); lb.classList.add('open');
      document.documentElement.style.overflow='hidden'; sc.scrollTop=0; sc.scrollLeft=0; }
    function cl(){ lb.classList.remove('open'); sc.innerHTML='';
      document.documentElement.style.overflow=''; }
    document.querySelectorAll('figure.gfig img, img.cfig').forEach(function(im){
      im.addEventListener('click', function(e){ e.stopPropagation(); op(im); });
    });
    lb.addEventListener('click', function(e){
      if(e.target===lb||e.target.classList.contains('lb-close')||
         e.target.classList.contains('lb-scroll')) cl(); });
    document.addEventListener('keydown', function(e){ if(e.key==='Escape') cl(); });
  })();
"""


# ------------------------------------------------------------------- 小工具
def esc(s):
    return _html.escape(s or "", quote=False)


def sec_anchor(i):
    return f"s{i}"


def _split_num(html):
    """「一、數系：…」→ ('一', '數系：…')；沒有編號就回 ('', 原文)。"""
    m = re.match(r"^\s*([一二三四五六七八九十]+)\s*、\s*、?\s*(.*)$", html)
    return (m.group(1), m.group(2)) if m else ("", html.strip())


# --------------------------------------------------------------- 區塊 → HTML
def render_ul(items):
    """扁平的 lvl 清單 → 巢狀 <ul>。"""
    out, stack = [], [0]

    def li(it):
        cls, pre = "", ""
        if it.get("num"):
            cls, pre = ' class="numbered"', f'<span class="n">{esc(it["num"])}</span>'
        if it.get("fig"):        # 只有圖的項目：不出現項目符號
            return ('<li class="figli">'
                    + fig_html({"src": it["fig"], "w": it.get("w", 0),
                                "alt": it.get("alt", ""), "cap": ""}) + "</li>")
        return f"<li{cls}>{pre}{it['html']}</li>"

    out.append('<ul class="glist">')
    cur = 0
    for it in items:
        lvl = it.get("lvl", 0)
        while lvl > cur:
            out.append('<ul class="glist">')
            cur += 1
        while lvl < cur:
            out.append("</ul>")
            cur -= 1
        out.append(li(it))
    while cur > 0:
        out.append("</ul>")
        cur -= 1
    out.append("</ul>")
    return "".join(out)


def fig_html(b):
    cls = "gfig gfig-float" if b.get("float") else "gfig"
    # 用 min(100%,…) 而不是固定 px：手機窄螢幕才不會被圖撐出橫向捲動
    w = f' style="max-width:min(100%,{b["w"]}px)"' if b.get("w") else ""
    alt = _html.escape(b.get("alt", "") or "", quote=True)
    cap = f'<figcaption>{b["cap"]}</figcaption>' if b.get("cap") else ""
    return (f'<figure class="{cls}"{w}><img src="img/{b["src"]}" alt="{alt}" '
            f'loading="lazy">{cap}</figure>')


def table_html(b):
    def cells(row, tag):
        out = []
        for c in row:
            sp = ""
            if c.get("cs"):
                sp += f' colspan="{c["cs"]}"'
            if c.get("rs"):
                sp += f' rowspan="{c["rs"]}"'
            inner = c["html"] or "&nbsp;"
            mid = " class=\"mid\"" if tag == "td" and (
                len(_plain_len(inner)) <= 14 or "<img" in inner) else ""
            out.append(f"<{tag}{sp}{mid}>{inner}</{tag}>")
        return "".join(out)

    head = "".join(f"<tr>{cells(r, 'th')}</tr>" for r in b.get("head") or [])
    body = "".join(f"<tr>{cells(r, 'td')}</tr>" for r in b.get("rows") or [])
    thead = f"<thead>{head}</thead>" if head else ""
    return f'<div class="tw"><table class="gt">{thead}<tbody>{body}</tbody></table></div>'


def _plain_len(h):
    return re.sub(r"<[^>]+>|\\[a-zA-Z]+|[\\(){}$]", "", h).strip()


def _unblank(h):
    """把挖空按鈕還原成純文字（說明性文字不需要挖空）。"""
    return re.sub(r'<span class="blank"[^>]*><span class="q">？</span>'
                  r'<span class="a">(.*?)</span></span>', r"\1", h, flags=re.S)


def note_html(b, lead=False):
    lab = b.get("label") or NOTE_LAB.get(b.get("kind"), "")
    kind = b.get("kind", "plain")
    lab_html = f'<span class="nlab">{esc(lab)}</span>' if lab else ""
    paras = "".join(f"<p>{p}</p>" for p in b["paras"])
    cls = "g-lead" if lead else f"nbox n-{kind}"
    return f'<div class="{cls}">{lab_html}{paras}</div>'


def block_html(b):
    t = b["t"]
    if t == "p":
        cls = "gp ind" if b.get("indent") else "gp"
        return f'<p class="{cls}">{b["html"]}</p>'
    if t == "ul":
        return render_ul(b["items"])
    if t == "hl":
        return f'<div class="hl">{b["html"]}</div>'
    if t == "note":
        return note_html(b)
    if t == "sub":
        return f'<h3 class="sub-h">{b["html"]}</h3>'
    if t == "fig":
        return fig_html(b)
    if t == "cap":
        return f'<p class="gp" style="text-align:center;font-size:13.5px;color:#5a4a52">{b["html"]}</p>'
    if t == "dmath":
        return f'<div class="dm">{b["html"]}</div>'
    if t == "table":
        return table_html(b)
    if t == "ex":
        return f'<div class="exbox">{"".join(block_html(x) for x in b["blocks"])}</div>'
    if t == "hr":
        return "<hr>"
    return ""


def chapter_body(ch):
    """章內容 → HTML（每節一張卡；章末 ◆ 三段各自成卡）。"""
    out, open_card, si = [], False, 0
    for b in ch["blocks"]:
        if b["t"] == "sec":
            if open_card:
                out.append("</section>")
            si += 1
            kind = b.get("kind", "sec")
            num, title = _split_num(b["html"])
            if kind == "sec":
                cls, badge = "card sec-card", num or str(si)
            else:
                cls, badge = f"card sec-card {SEC_CLASS.get(kind,'')}", SEC_ICON.get(kind, "◆")
            out.append(f'<section class="{cls}">'
                       f'<h2 class="sec-h" id="{sec_anchor(si)}">'
                       f'<span class="num">{esc(badge)}</span>'
                       f'<span>{title}</span></h2>')
            open_card = True
            continue
        if b["t"] == "note" and b.get("kind") == "lead" and not open_card:
            out.append(note_html(b, lead=True))
            continue
        out.append(block_html(b))
    if open_card:
        out.append("</section>")
    return "".join(out)


# 小節標題進下拉選單／目錄連結時只能是純文字，常用符號改成看得懂的字
TEX_TXT = {
    r"\neq": "≠", r"\leq": "≤", r"\geq": "≥", r"\Leftrightarrow": "⇔",
    r"\Rightarrow": "⇒", r"\rightarrow": "→", r"\to": "→", r"\times": "×",
    r"\cdot": "·", r"\pm": "±", r"\infty": "∞", r"\sqrt": "√", r"\theta": "θ",
    r"\pi": "π", r"\alpha": "α", r"\beta": "β", r"\mu": "μ", r"\sigma": "σ",
    r"\Delta": "Δ", r"\in": "∈", r"\cap": "∩", r"\cup": "∪", r"\bot": "⊥",
}


def _tex_txt(h):
    """含 LaTeX 的標題 → 純文字（給 <option> 與目錄連結用）。"""
    t = re.sub(r"<[^>]+>", "", h)
    for d in ("\\(", "\\)", "\\[", "\\]"):      # 先拆掉數學界定符，免得留下括號
        t = t.replace(d, "")
    t = re.sub(r"\\(?:mathbf|mathrm|mathbb|text|boldsymbol)\{([^{}]*)\}", r"\1", t)
    for k, v in TEX_TXT.items():
        t = t.replace(k, v)
    t = re.sub(r"[_^]\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = re.sub(r"[\\{}$]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def sec_list(ch):
    """章內小節（給頂欄選單與目錄頁）：[(anchor, 顯示文字, kind)]"""
    out, si = [], 0
    for b in ch["blocks"]:
        if b["t"] == "sec":
            si += 1
            num, title = _split_num(b["html"])
            out.append((sec_anchor(si), (f"{num}、" if num else "") + _tex_txt(title),
                        b.get("kind", "sec")))
    return out


# ------------------------------------------------------------------- 頁面外框
def toolbar(data, cur=None):
    chs = data["chapters"]
    opts = ['<option value="">— 跳到章 —</option>',
            '<option value="index.html">📖 講義目錄</option>']
    for c in chs:
        sel = " selected" if cur and c["n"] == cur["n"] else ""
        opts.append(f'<option value="{_html.escape(c["file"], quote=True)}"{sel}>'
                    f'{label(c)}　{esc(c["title"])}</option>')
    sec_opts = ""
    if cur and len(sec_list(cur)) > 1:
        so = ['<option value="">— 跳到節 —</option>']
        for anchor, txt, kind in sec_list(cur):
            ic = SEC_ICON.get(kind, "")
            so.append(f'<option value="#{anchor}">{ic}{esc(txt)}</option>')
        sec_opts = ('<select class="nav-select" onchange="if(this.value)'
                    '{location.hash=this.value;this.selectedIndex=0;}">'
                    + "".join(so) + "</select>")
    home = ('<a class="tb-home" href="../" style="background:rgba(255,255,255,.15);'
            'color:#fff;border:1px solid rgba(255,255,255,.5);border-radius:18px;'
            'padding:4px 12px;font-size:13px;font-weight:700;text-decoration:none;'
            'white-space:nowrap">🏠 網站首頁</a>')
    back = ('<a class="tb-home" href="../concept-map/" style="background:rgba(255,255,255,.15);'
            'color:#fff;border:1px solid rgba(255,255,255,.5);border-radius:18px;'
            'padding:4px 12px;font-size:13px;font-weight:700;text-decoration:none;'
            'white-space:nowrap">📘 重點整理</a>')
    return ('<div class="toolbar">'
            f'<span class="t-title">{esc(TB_TITLE)}</span>'
            '<span class="tb-caret">▾ 展開選單</span>'
            f'{home}{back}'
            '<select class="nav-select" onchange="if(this.value){location.href=this.value;}">'
            + "".join(opts) + "</select>"
            + sec_opts
            + '<button onclick="revealAll()">全部顯示答案</button>'
              '<button onclick="hideAll()">全部隱藏</button></div>')


def og_meta(title, desc, page_file=""):
    """分享卡 meta：講義發布在站台根的 guide/，網址前綴與 concept-map 不同，故自己組。"""
    url = SITE_ROOT + "guide/" + quote(page_file)
    t, d = _esc_attr(title), _esc_attr(desc)
    tags = [
        f'<meta name="description" content="{d}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{_esc_attr(OG_SITE_NAME)}">',
        '<meta property="og:locale" content="zh_TW">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{OG_IMG}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
        f'<meta name="twitter:image" content="{OG_IMG}">',
        FAVICON_HTML,
    ]
    return "\n".join(tags)


def page(title, desc, file, body, data, cur=None):
    css = _asset("style.css") + GUIDE_CSS
    js = _asset("app.js") + GUIDE_JS
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ANALYTICS}<title>{esc(title)}</title>
{og_meta(title, desc, file)}
<link rel="stylesheet" href="katex/katex.min.css">
<style>
{css}</style>
</head>
<body>
{toolbar(data, cur)}
<div class="wrap">
{body}
{PRIVACY_HTML}
</div>
{LIGHTBOX_HTML}
<script src="katex/katex.min.js"></script>
<script src="katex/contrib/auto-render.min.js"></script>
<script>
{js}</script>
</body>
</html>
"""


LEGEND = ('<div class="legend">使用方式：內容中的 '
          '<span class="blank" style="cursor:default"><span class="q">？</span></span>'
          ' 就是講義的填空——<b>點一下顯示答案</b>，再點一下收回；'
          '也可用上方 <b>「全部顯示答案」</b> 一次切換整章（＝教師版）。'
          '圖可點擊放大。</div>')


def build_chapter(data, i):
    chs = data["chapters"]
    ch = chs[i]
    title = f'{label(ch)}　{ch["title"]}'
    prev_ = chs[i - 1] if i > 0 else None
    next_ = chs[i + 1] if i < len(chs) - 1 else None
    nav = ['<div class="chnav">']
    if prev_:
        nav.append(f'<a href="{_html.escape(prev_["file"], quote=True)}">'
                   f'<small>← {"上一章" if not is_ap(prev_) else "附錄"}</small>'
                   f'{label(prev_)}　{esc(prev_["title"])}</a>')
    nav.append('<a href="index.html" style="flex:0 1 150px;text-align:center;'
               'border-left-color:#1f6f78;color:#17595f"><small>目錄</small>📖 全部章節</a>')
    if next_:
        nav.append(f'<a class="next" href="{_html.escape(next_["file"], quote=True)}">'
                   f'<small>{"下一章" if not is_ap(next_) else "附錄"} →</small>'
                   f'{label(next_)}　{esc(next_["title"])}</a>')
    nav.append("</div>")
    sub = (f'{TITLE}　·　第 {ch.get("from_ch","")} 章補充' if is_ap(ch)
           else f'{TITLE}　·　{len(ch["secs"])} 節')
    body = (f'<div class="hero"><h1>{esc(title)}</h1>'
            f'<p>{sub}</p></div>'
            + LEGEND
            + chapter_body(ch)
            + "".join(nav))
    desc = (f'學測數A「{ch["title"]}」脈絡複習：條列重點填空自測、易錯提醒、'
            f'判斷流程（看到 X 用 Y）、跨章鏈結與歷屆題號。')
    return page(f"{title}｜{TITLE}", desc, ch["file"], body, data, ch)


def build_index(data):
    chs = data["chapters"]
    cards = []
    for c in chs:
        secs = "".join(
            f'<a href="{_html.escape(c["file"], quote=True)}#{a}">{SEC_ICON.get(k,"")}{esc(t)}</a>'
            for a, t, k in sec_list(c))
        cards.append(
            f'<div class="g-ch{" g-ap" if is_ap(c) else ""}">'
            f'<a class="g-ch-h" href="{_html.escape(c["file"], quote=True)}">'
            f'<span class="num">{badge(c)}</span><span>{esc(c["title"])}</span>'
            f'<span class="cnt">前往 →</span></a>'
            + (f'<div class="g-secs">{secs}</div>' if len(sec_list(c)) > 1 else "")
            + '</div>')
    howto = ""
    if data.get("howto"):
        # 目錄頁的「怎麼讀這本」是說明文字：裡面的挖空還原成文字，
        # 並把紙本說法（玫瑰色為答案）換成網頁的操作方式
        hb = dict(data["howto"])
        hb["paras"] = [_unblank(p).replace(
            "（玫瑰色為答案）", "（網頁版：點空格按鈕看答案）") for p in hb["paras"]]
        howto = note_html(hb, lead=True)
    body = (f'<div class="hero"><h1>{esc(TITLE)}</h1>'
            f'<p>{esc(data["subtitle"])}</p>'
            '<p style="font-size:13px;color:#9a857c;margin-top:2px">'
            '涵蓋 106–115 學測數A 歷屆題號　·　mathmap · 游心怡</p></div>'
            f'<div class="g-stat"><span>📚 <b>{sum(1 for c in chs if not is_ap(c))}</b> 章'
            f'{"＋附錄" if any(is_ap(c) for c in chs) else ""}</span>'
            f'<span>🧭 每章附「看到 X → 用 Y」判斷流程</span></div>'
            + howto + LEGEND
            + f'<div class="g-toc">{"".join(cards)}</div>')
    desc = (f"{TITLE}網頁版：13 章條列重點，填空點一下就顯示答案，"
            "附易錯提醒、判斷流程、跨章鏈結與 106–115 歷屆題號。")
    return page(f"{TITLE}｜13 章條列重點 × 挖空自測", desc,
                "index.html", body, data)


def main():
    data = json.load(open(DATA, encoding="utf-8"))
    os.makedirs(IMG, exist_ok=True)
    # KaTeX 自帶一份（與 exam/ 相同作法，講義不依賴 concept-map 的檔案）
    dst = os.path.join(OUT, "katex")
    if not os.path.isdir(dst):
        shutil.copytree(KATEX_SRC, dst)
        print("[guide] 複製 KaTeX → guide/katex/")
    n = len([f for f in os.listdir(IMG) if f.lower().endswith(".png")])
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_index(data))
    print(f"[guide] index.html　（圖片 {n} 張在 guide/img/）")
    for i, ch in enumerate(data["chapters"]):
        html = build_chapter(data, i)
        with open(os.path.join(OUT, ch["file"]), "w", encoding="utf-8") as fh:
            fh.write(html)
        print(f"[guide] {ch['file']}　{len(html)//1024} KB　填空 {ch['blanks']}")


if __name__ == "__main__":
    main()
