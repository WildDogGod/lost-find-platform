import sys
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

path = r"D:\新建文件夹\七组-实验1-可行性和需求分析.docx"
doc = Document(path)

print("=== SECTIONS ===")
for i, s in enumerate(doc.sections):
    print(i, "page", s.page_width, s.page_height, "margins", s.left_margin, s.right_margin, s.top_margin, s.bottom_margin)

print("=== STYLES USED ===")
used = {}
for p in doc.paragraphs:
    used[p.style.name] = used.get(p.style.name, 0) + 1
print(used)

def iter_block_items(parent):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

print("=== BODY (index, kind, style, text) ===")
for idx, block in enumerate(iter_block_items(doc)):
    if isinstance(block, Paragraph):
        txt = block.text
        pf = block.paragraph_format
        info = f"align={block.alignment} first_line={pf.first_line_indent} space_after={pf.space_after}"
        print(f"[{idx}] P style={block.style.name!r} :: {txt!r}")
    else:
        print(f"[{idx}] TABLE rows={len(block.rows)} cols={len(block.columns)}")
        for r_i, row in enumerate(block.rows):
            cells = [c.text.replace("\n", "\\n") for c in row.cells]
            print(f"      R{r_i}: {cells}")

print("=== HEADERS/FOOTERS ===")
for i, s in enumerate(doc.sections):
    for name, part in (("header", s.header), ("footer", s.footer)):
        texts = [p.text for p in part.paragraphs if p.text.strip()]
        if texts:
            print(i, name, texts)

print("=== IMAGES ===")
for rel in doc.part.rels.values():
    if "image" in rel.reltype:
        print(rel.rId, rel.target_ref)