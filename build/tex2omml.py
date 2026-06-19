"""LaTeX -> OMML（Word 原生方程式）轉換。

路徑：LaTeX --latex2mathml--> (Presentation) MathML --MML2OMML.XSL--> OMML
OMML 元素可直接插入 python-docx 的段落，成為 Word 可編輯的真方程式（非圖片）。
"""
import os
import functools
from lxml import etree
import latex2mathml.converter
from docx.oxml import parse_xml

# 官方 MathML -> OMML 樣式表（隨 MS Office 一起安裝）
_XSL_CANDIDATES = [
    r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
    r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
]


@functools.lru_cache(maxsize=1)
def _transform():
    for p in _XSL_CANDIDATES:
        if os.path.exists(p):
            return etree.XSLT(etree.parse(p))
    raise FileNotFoundError(
        "找不到 MML2OMML.XSL；請確認已安裝 MS Office，或改用圖片渲染路徑。"
    )


@functools.lru_cache(maxsize=4096)
def tex_to_omml_xml(tex: str) -> str:
    """回傳 OMML 的 XML 字串（<m:oMath ...>...</m:oMath>）。"""
    mathml = latex2mathml.converter.convert(tex)
    mml_tree = etree.fromstring(mathml.encode("utf-8"))
    omml_tree = _transform()(mml_tree)
    root = omml_tree.getroot()  # m:oMath
    return etree.tostring(root, encoding="unicode")


def omml_element(tex: str):
    """回傳可插入 python-docx 的 oMath 元素（已在 python-docx 的解析器下）。"""
    return parse_xml(tex_to_omml_xml(tex))


if __name__ == "__main__":
    # 自我測試：印出一段 OMML 開頭，確認轉換可用
    samples = [r"\det(A)=ad-bc", r"\begin{bmatrix}a&b\\c&d\end{bmatrix}"]
    for s in samples:
        xml = tex_to_omml_xml(s)
        print(s, "->", xml[:80].replace("\n", " "), "...")
