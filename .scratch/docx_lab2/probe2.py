import sys
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

doc = Document(sys.argv[1])
body = doc.element.body

# styles font sizes
for sid in ('a', 'a9', '1', '2', '3', 'a8', 'a5'):
    try:
        st = doc.styles.element.find(f".//{qn('w:style')}[@{qn('w:styleId')}='{sid}']")
        sz = st.find(f".//{qn('w:sz')}")
        nsz = st.find(f".//{qn('w:name')}")
        ind = st.find(f".//{qn('w:ind')}")
        print(sid, nsz.get(qn('w:val')) if nsz is not None else '',
              ('sz=' + sz.get(qn('w:val'))) if sz is not None else '',
              ('ind=' + str(ind.attrib) if ind is not None else ''))
    except Exception as e:
        print(sid, 'err', e)

tables = doc.tables
print('\ntable count', len(tables))
for ti in (2, 5, 6):
    t = tables[ti]
    row = t.rows[0]
    for ci, c in enumerate(row.cells[:3]):
        p = c.paragraphs[0]
        st = p.style.name if p.style is not None else ''
        r = p.runs[0] if p.runs else None
        sz = r.font.size.pt if (r is not None and r.font.size) else None
        print(f't{ti} c{ci} style={st!r} sz={sz} bold={r.bold if r is not None else None} text={p.text[:20]!r}')

# body paragraph indents for a9
for idx in (145, 172, 190):
    p = Paragraph(list(body.iterchildren())[idx], doc)
    pf = p.paragraph_format
    print('P', idx, 'style', p.style.name, 'first_line', pf.first_line_indent, 'left', pf.left_indent,
          'space_before', pf.space_before, 'space_after', pf.space_after, 'line', pf.line_spacing)
