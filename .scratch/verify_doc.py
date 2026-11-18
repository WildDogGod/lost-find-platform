# -*- coding: utf-8 -*-
"""校验生成的 docx：结构、文本、图片、图表序号。"""
import os, re, sys, zipfile
from docx import Document
from docx.oxml.ns import qn

OUT = r"D:\新建文件夹\校园失物招领平台-实验1-可行性和需求分析.docx"
DUMP = r"D:\code\lost-found-platform\.scratch\out_dump.txt"

doc = Document(OUT)
body = doc.element.body
kinds = []
texts = []
img_count = 0
for el in body.iterchildren():
    if el.tag == qn("w:p"):
        from docx.text.paragraph import Paragraph
        p = Paragraph(el, doc)
        style = p.style.name
        t = p.text.strip()
        n_img = len(el.findall(".//" + qn("a:blip")))
        if n_img:
            img_count += n_img
            kinds.append("[IMG x%d]" % n_img)
            continue
        kinds.append("[%s] %s" % (style, t))
        texts.append("%s\t%s" % (style, t))
    elif el.tag == qn("w:tbl"):
        kinds.append("[TABLE]")

with open(DUMP, "w", encoding="utf-8") as f:
    f.write("\n".join(kinds))

print("段落/块数:", len(kinds), " 图片数:", img_count)
print("正文段落数:", len(texts))
print("样式统计:", {k: sum(1 for x in kinds if x.startswith("[%s]" % k)) for k in ["Title", "Heading 1", "Heading 2", "Normal", "我的正文", "Subtitle"]})
with zipfile.ZipFile(OUT) as z:
    media = [n for n in z.namelist() if n.startswith("word/media/")]
    print("media 部件:", media)
    print("zip 条目数:", len(z.namelist()))
print("---- 前 40 行 ----")
for line in kinds[:40]:
    print(line[:110])
print("---- 后 20 行 ----")
for line in kinds[-20:]:
    print(line[:110])
# 图表编号检查
allt = "\n".join(kinds)
for i in range(1, 7):
    print("图%d 题注:" % i, ("图%d" % i) in allt, " 引用:", allt.count("图 %d" % i) + allt.count("图%d" % i))
print("章节标题:")
for k in kinds:
    if k.startswith("[Heading 1]") or k.startswith("[Heading 2]"):
        print("  ", k)