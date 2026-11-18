import json
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

path = r"D:\新建文件夹\七组-实验1-可行性和需求分析.docx"
doc = Document(path)

out = []
def iter_block_items(parent):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

for idx, block in enumerate(iter_block_items(doc)):
    if isinstance(block, Paragraph):
        has_img = bool(block._p.findall('.//' + qn('a:blip')))
        out.append({"i": idx, "kind": "p", "style": block.style.name, "text": block.text, "img": has_img})
    else:
        out.append({"i": idx, "kind": "t", "rows": [[c.text for c in r.cells] for r in block.rows]})

with open(r"D:\code\lost-found-platform\.scratch\docx_dump.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("dumped", len(out))