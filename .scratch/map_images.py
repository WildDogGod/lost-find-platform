import zipfile, re, json
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

src = r"D:\新建文件夹\七组-实验1-可行性和需求分析.docx"

# rels: rId -> media target
with zipfile.ZipFile(src) as z:
    rels_xml = z.read("word/_rels/document.xml.rels").decode("utf-8")
    medias = [n for n in z.namelist() if n.startswith("word/media/")]
    sizes = {n: z.getinfo(n).file_size for n in medias}

rel_map = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels_xml))

doc = Document(src)

def iter_blocks(parent):
    for child in parent.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

out = []
for idx, block in enumerate(iter_blocks(doc)):
    if not isinstance(block, Paragraph):
        continue
    blips = block._p.findall('.//' + qn('a:blip'))
    if not blips:
        continue
    for b in blips:
        rid = b.get(qn('r:embed'))
        target = rel_map.get(rid, '?')
        ext = block._p.findall('.//' + qn('wp:extent'))
        cx = cy = None
        if ext:
            cx = int(ext[0].get('cx')); cy = int(ext[0].get('cy'))
        out.append({"idx": idx, "rid": rid, "target": target,
                    "cx_emu": cx, "cy_emu": cy,
                    "w_in": round(cx/914400, 2) if cx else None,
                    "h_in": round(cy/914400, 2) if cy else None,
                    "bytes": sizes.get('word/' + target.replace('media/', 'media/')) if target != '?' else None})

with open(r"D:\code\lost-found-platform\.scratch\image_map.json", "w", encoding="utf-8") as f:
    json.dump({"images": out, "all_media": {n: sizes[n] for n in medias}}, f, ensure_ascii=False, indent=1)
print("ok", len(out))