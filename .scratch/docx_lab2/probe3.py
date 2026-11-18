import sys
from docx import Document
from docx.oxml.ns import qn

doc = Document(sys.argv[1])
numbering = doc.part.numbering_part.element
for num in numbering.findall(qn('w:num')):
    numId = num.get(qn('w:numId'))
    if numId in ('11', '12', '13', '14', '15'):
        abs_id = num.find(qn('w:abstractNumId')).get(qn('w:val'))
        absn = numbering.find(f".//{qn('w:abstractNum')}[@{qn('w:abstractNumId')}='{abs_id}']")
        print('numId', numId, 'abs', abs_id)
        for lvl in absn.findall(qn('w:lvl'))[:4]:
            ilvl = lvl.get(qn('w:ilvl'))
            fmt = lvl.find(qn('w:numFmt')).get(qn('w:val'))
            txt = lvl.find(qn('w:lvlText')).get(qn('w:val'))
            start = lvl.find(qn('w:start'))
            print('   ilvl', ilvl, 'fmt', fmt, 'text', repr(txt), 'start', start.get(qn('w:val')) if start is not None else None)
