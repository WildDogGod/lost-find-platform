import sys
from docx import Document
from docx.oxml.ns import qn

doc = Document(sys.argv[1])
print("STYLES:")
for s in doc.styles:
    try:
        el = s.element
        sid = el.get(qn('w:styleId'))
        typ = el.get(qn('w:type'))
        name = s.name
        print(f"  type={typ} id={sid!r} name={name!r}")
    except Exception as e:
        print("  err", e)

print("\nSECTION:")
sec = doc.sections[0]
print(sec.page_width, sec.page_height, sec.left_margin, sec.top_margin)

print("\nSAMPLE PARAGRAPHS XML:")
for i in (145, 149, 172):
    p = doc.paragraphs[0]
print("done")
