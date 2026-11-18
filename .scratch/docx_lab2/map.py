import sys, json
from docx import Document
from docx.oxml.ns import qn

path = sys.argv[1]
doc = Document(path)

body = doc.element.body
kids = list(body.iterchildren())
idx_p = 0
idx_t = 0
out = []
for i, el in enumerate(kids):
    tag = el.tag.split('}')[1]
    if tag == 'p':
        p = el
        text = ''.join(t.text or '' for t in p.iter(qn('w:t')))
        style = ''
        pPr = p.find(qn('w:pPr'))
        if pPr is not None:
            st = pPr.find(qn('w:pStyle'))
            if st is not None:
                style = st.get(qn('w:val'))
            num = pPr.find(qn('w:numPr'))
            if num is not None:
                ilvl = num.find(qn('w:ilvl'))
                nid = num.find(qn('w:numId'))
                style += f" num(ilvl={ilvl.get(qn('w:val')) if ilvl is not None else ''},id={nid.get(qn('w:val')) if nid is not None else ''})"
        n_img = len(p.findall('.//' + qn('w:drawing'))) + len(p.findall('.//' + qn('w:pict')))
        has_obj = len(p.findall('.//' + qn('w:object')))
        out.append({'i': i, 'p': idx_p, 'style': style, 'img': n_img, 'obj': has_obj, 'text': text})
        idx_p += 1
    elif tag == 'tbl':
        rows = el.findall(qn('w:tr'))
        cols = len(rows[0].findall(qn('w:tc'))) if rows else 0
        tblPr = el.find(qn('w:tblPr'))
        st = ''
        if tblPr is not None:
            ts = tblPr.find(qn('w:tblStyle'))
            if ts is not None:
                st = ts.get(qn('w:val'))
        out.append({'i': i, 'tbl': idx_t, 'style': st, 'rows': len(rows), 'cols': cols, 'text': ''})
        idx_t += 1
    elif tag == 'sectPr':
        out.append({'i': i, 'sectPr': True})

with open(sys.argv[2], 'w', encoding='utf-8') as f:
    for r in out:
        if 'tbl' in r:
            f.write(f"[{r['i']}] TABLE#{r['tbl']} style={r['style']} rows={r['rows']} cols={r['cols']}\n")
        elif r.get('sectPr'):
            f.write(f"[{r['i']}] SECTPR\n")
        else:
            mark = ''
            if r['img']:
                mark += f" IMG{r['img']}"
            if r['obj']:
                mark += " OBJ"
            f.write(f"[{r['i']}] P#{r['p']} <{r['style']}>{mark} {r['text'][:80]}\n")

print('paras', idx_p, 'tables', idx_t)
