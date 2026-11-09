#!/usr/bin/env python3
"""مكتبة بناء ملف وورد عربي بالاتجاه الصحيح وهوية محددة.

الاستخدام:
    from docx_builder import Doc
    d = Doc(font="A Jannat LT", primary="18274B", accent="C89D67", light="F1E7E2")
    d.cover("العرض الفني والمالي", "اسم المشروع", "اسم الجهة",
            [("مقدم العرض","..."),("رقم الترخيص","...")], brand="اسم الشركة")
    d.h1("1. الملخص التنفيذي")
    d.p("نص الفقرة ...")
    d.h2("1.1 عنوان فرعي")
    d.bullet("نقطة")
    d.label("أولا، العنوان.", "شرح النقطة ...")
    d.table(["العمود الأول من اليمين","الثاني","الثالث"],
            [["أ","ب","ج"], ["**الإجمالي","**","**10"]], widths=[7,5,3])
    d.page_break()
    d.save("out.docx")

ملاحظات:
- العمود الأول في headers هو العمود اليمين. bidiVisual يتكفل بالباقي.
- ابدأ خلية بـ ** لجعلها صف مجموع بخلفية فاتحة ونص غامق.
- الأرقام تكتب لاتينية 123.
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ALIGN = {'right': WD_ALIGN_PARAGRAPH.RIGHT,
         'center': WD_ALIGN_PARAGRAPH.CENTER,
         'just': WD_ALIGN_PARAGRAPH.JUSTIFY}


class Doc:
    def __init__(self, font="Arial", primary="18274B", accent="C89D67",
                 light="F1E7E2", body="1A1A1A", margins=(2.2, 2.0)):
        self.f, self.P, self.A, self.L, self.B = font, primary, accent, light, body
        self.doc = Document()
        s = self.doc.sections[0]
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(margins[0])
        s.top_margin = s.bottom_margin = Cm(margins[1])
        s._sectPr.append(OxmlElement('w:bidi'))          # اتجاه القسم

    # ---------- أساسيات الاتجاه ----------
    def _run(self, r, size=11, bold=False, color=None, font=None):
        font = font or self.f
        r.font.name, r.font.size, r.bold = font, Pt(size), bold
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        rpr = r._element.get_or_add_rPr()
        rf = rpr.find(qn('w:rFonts'))
        if rf is None:
            rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
        for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):   # الأربعة معا إلزامي
            rf.set(qn(a), font)
        rtl = OxmlElement('w:rtl'); rtl.set(qn('w:val'), '1'); rpr.append(rtl)
        sz = OxmlElement('w:szCs'); sz.set(qn('w:val'), str(int(size * 2)))
        rpr.append(sz)                                            # وإلا بقي الحجم افتراضيا
        if bold:
            rpr.append(OxmlElement('w:bCs'))
        return r

    def _par(self, align='just', after=8, before=0, line=1.35):
        p = self.doc.add_paragraph()
        p._p.get_or_add_pPr().append(OxmlElement('w:bidi'))
        p.alignment = ALIGN[align]
        pf = p.paragraph_format
        pf.space_after, pf.space_before, pf.line_spacing = Pt(after), Pt(before), line
        return p

    @staticmethod
    def _shade(tcPr, color):
        sh = OxmlElement('w:shd')
        sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), color)
        tcPr.append(sh)

    # ---------- عناصر المحتوى ----------
    def p(self, text, size=11, bold=False, color=None, align='just', after=8, before=0):
        self._run(self._par(align, after, before).add_run(text), size, bold, color or self.B)

    def h1(self, text, size=16):
        p = self._par('right', 10, 20)
        pbdr = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
        for k, v in (('w:val', 'single'), ('w:sz', '12'), ('w:space', '4'), ('w:color', self.A)):
            bt.set(qn(k), v)
        pbdr.append(bt); p._p.get_or_add_pPr().append(pbdr)
        self._run(p.add_run(text), size, True, self.P)

    def h2(self, text, size=12.5):
        self._run(self._par('right', 6, 14).add_run(text), size, True, self.A)

    def bullet(self, text, size=11):
        p = self._par('just', 5, 0, 1.3)
        p.paragraph_format.right_indent = Cm(0.6)
        self._run(p.add_run("◂  "), 9, False, self.A)
        self._run(p.add_run(text), size, False, self.B)

    def label(self, label, text, size=11):
        p = self._par('just', 5, 0, 1.3)
        self._run(p.add_run(label + " "), size, True, self.P)
        self._run(p.add_run(text), size, False, self.B)

    def table(self, headers, rows, widths=None, size=10):
        t = self.doc.add_table(rows=1, cols=len(headers))
        t.style, t.alignment = 'Table Grid', WD_TABLE_ALIGNMENT.CENTER
        t._tbl.tblPr.append(OxmlElement('w:bidiVisual'))   # العمود الأول من اليمين
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]; c.text = ''
            p = c.paragraphs[0]
            p._p.get_or_add_pPr().append(OxmlElement('w:bidi'))
            p.alignment = ALIGN['center']
            p.paragraph_format.space_after = p.paragraph_format.space_before = Pt(2)
            self._run(p.add_run(h), size, True, "FFFFFF")
            self._shade(c._tc.get_or_add_tcPr(), self.P)
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                c = cells[i]; c.text = ''
                p = c.paragraphs[0]
                p._p.get_or_add_pPr().append(OxmlElement('w:bidi'))
                p.alignment = ALIGN['right' if len(str(val)) > 12 else 'center']
                p.paragraph_format.space_after = p.paragraph_format.space_before = Pt(2)
                bold = str(val).startswith('**')
                self._run(p.add_run(str(val).replace('**', '')), size, bold,
                          self.P if bold else self.B)
                if bold:
                    self._shade(c._tc.get_or_add_tcPr(), self.L)
        if widths:
            for r in t.rows:
                for i, w in enumerate(widths):
                    r.cells[i].width = Cm(w)
        self._par('right', 4)
        return t

    def cover(self, title, subtitle, client, meta, brand=None, license_no=None):
        for _ in range(4):
            self.doc.add_paragraph()
        if brand:
            self._run(self._par('center', 4).add_run(brand), 13, True, self.A)
        if license_no:
            self._run(self._par('center', 30).add_run(f"ترخيص رقم {license_no}"), 10, False, "6B6B6B")
        self._run(self._par('center', 14).add_run(title), 30, True, self.P)
        for line in (subtitle if isinstance(subtitle, list) else [subtitle]):
            self._run(self._par('center', 6).add_run(line), 15, False, self.P)
        self._run(self._par('center', 36).add_run(client), 17, True, self.A)
        for _ in range(3):
            self.doc.add_paragraph()
        t = self.doc.add_table(rows=0, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t._tbl.tblPr.append(OxmlElement('w:bidiVisual'))
        for k, v in meta:
            cells = t.add_row().cells
            for i, (txt, b, col) in enumerate([(k, True, self.P), (v, False, self.B)]):
                cells[i].text = ''
                p = cells[i].paragraphs[0]
                p._p.get_or_add_pPr().append(OxmlElement('w:bidi'))
                p.alignment = ALIGN['right']; p.paragraph_format.space_after = Pt(3)
                self._run(p.add_run(txt), 10.5, b, col)
            cells[0].width, cells[1].width = Cm(4.5), Cm(8)
        self.page_break()

    def page_break(self):
        self.doc.add_page_break()

    def save(self, path):
        self.doc.save(path)
        return path
