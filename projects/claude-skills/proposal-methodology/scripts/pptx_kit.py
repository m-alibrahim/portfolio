#!/usr/bin/env python3
"""مكتبة بناء شرائح عربية داخل قالب pptx قائم.

المبدأ: لا تبنِ عرضا من الصفر. فك ضغط القالب، احقن الأشكال في الشرائح
الفارغة، أعد الحزم. هذه المكتبة تولّد XML جاهز الاتجاه والهوية.

الاستخدام:
    from pptx_kit import Deck
    d = Deck("u", font="A Jannat LT", primary="18274B",
             accent="C89D67", light="F1E7E2")

    sh  = d.title("نطاق عمل المشروع", "سطر تمهيدي اختياري")
    cw, xs = d.cols(3)                      # xs[0] هو أقصى اليمين
    for i,(t,body) in enumerate(items):
        sh.append(d.box(xs[i], 1600000, cw, 1200000,
                  [d.par([d.run(t,1300,1,d.A)]),
                   d.par([d.run(body,1100)],space=200)],
                  fill="FFFFFF", line=d.A))
    sh.append(d.tbl(d.L, 3200000, d.W, [4,4,2],
              [["الشعار","الفئات","العدد"], ["أ","ب","1"]]))
    d.write(9, sh)

قواعد مضمّنة:
- xs[0] دائما أقصى اليمين، فالتدرج يبدأ من اليمين كما تقرأ العربية.
- الجداول تعكس أعمدتها تلقائيا، ولا تستخدم tblPr rtl لأنه غير موثوق.
- العمود الأول في headers هو العمود اليمين.
"""
import re

SLIDE_W, SLIDE_H = 12192000, 6858000


class Deck:
    def __init__(self, unpacked_dir, font="Arial", primary="18274B",
                 accent="C89D67", light="F1E7E2", body="333333",
                 left=700000, width=10800000):
        self.d, self.f = unpacked_dir, font
        self.P, self.A, self.Lt, self.B = primary, accent, light, body
        self.L, self.W = left, width
        self.R = left + width
        self._id = 600

    # ---------- تخطيط ----------
    def cols(self, n, gap=140000, total=None):
        """يعيد (عرض العمود، قائمة إحداثيات) والإحداثي رقم 0 هو أقصى اليمين."""
        total = total or self.W
        cw = (total - gap * (n - 1)) / n
        return cw, [self.L + (n - 1 - i) * (cw + gap) for i in range(n)]

    def grid(self, cols, rows, y0, h, gap=140000, vgap=110000):
        """إحداثيات شبكة، الفهرس 0 أعلى اليمين ثم يسارا ثم أسفل."""
        cw, xs = self.cols(cols, gap)
        return cw, [(xs[i % cols], y0 + (i // cols) * (h + vgap))
                    for i in range(cols * rows)]

    # ---------- نص ----------
    @staticmethod
    def esc(t):
        return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def run(self, t, sz=1200, b=0, col=None):
        col = col or self.B
        return (f'<a:r><a:rPr lang="ar-SA" sz="{sz}" b="{b}" dirty="0">'
                f'<a:solidFill><a:srgbClr val="{col}"/></a:solidFill>'
                f'<a:latin typeface="{self.f}"/><a:cs typeface="{self.f}"/></a:rPr>'
                f'<a:t>{self.esc(t)}</a:t></a:r>')

    def par(self, runs, algn='r', space=0, line=125000):
        return (f'<a:p><a:pPr algn="{algn}" rtl="1">'
                f'<a:lnSpc><a:spcPct val="{line}"/></a:lnSpc>'
                f'<a:spcBef><a:spcPts val="{space}"/></a:spcBef>'
                f'<a:buNone/></a:pPr>{"".join(runs)}</a:p>')

    # ---------- أشكال ----------
    def box(self, x, y, w, h, paras, fill=None, line=None, anchor='t', radius=5000):
        self._id += 1
        fx = (f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
              if fill else '<a:noFill/>')
        lx = (f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
              if line else '<a:ln><a:noFill/></a:ln>')
        return (f'<p:sp><p:nvSpPr><p:cNvPr id="{self._id}" name="ص{self._id}"/>'
                f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
                f'<p:spPr><a:xfrm><a:off x="{int(x)}" y="{int(y)}"/>'
                f'<a:ext cx="{int(w)}" cy="{int(h)}"/></a:xfrm>'
                f'<a:prstGeom prst="roundRect"><a:avLst>'
                f'<a:gd name="adj" fmla="val {radius}"/></a:avLst></a:prstGeom>{fx}{lx}</p:spPr>'
                f'<p:txBody><a:bodyPr rtlCol="1" wrap="square" lIns="128000" rIns="128000" '
                f'tIns="82000" bIns="82000" anchor="{anchor}"/><a:lstStyle/>'
                f'{"".join(paras)}</p:txBody></p:sp>')

    def title(self, text, sub=None, y=380000, size=2400):
        sh = [self.box(self.L, y, self.W, 600000,
                       [self.par([self.run(text, size, 1, self.P)])])]
        if sub:
            sh.append(self.box(self.L, y + 620000, self.W, 420000,
                               [self.par([self.run(sub, 1200, 0, "6B6B6B")])]))
        return sh

    def tbl(self, x, y, w, colw, rows, header=True, sz=1050, rowh=340000):
        """colw و rows بترتيب منطقي: العنصر 0 هو العمود اليمين.
        العكس يتم داخليا لأن tblPr rtl غير موثوق عبر المحركات."""
        self._id += 1
        colw = list(colw)[::-1]
        rows = [list(r)[::-1] for r in rows]
        tot = sum(colw)
        colw = [int(c * w / tot) for c in colw]
        out = [f'<p:graphicFrame><p:nvGraphicFramePr>'
               f'<p:cNvPr id="{self._id}" name="جدول{self._id}"/>'
               f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr>'
               f'<p:nvPr/></p:nvGraphicFramePr>'
               f'<p:xfrm><a:off x="{int(x)}" y="{int(y)}"/>'
               f'<a:ext cx="{int(w)}" cy="{int(rowh * len(rows))}"/></p:xfrm>'
               f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/'
               f'drawingml/2006/table"><a:tbl><a:tblPr/><a:tblGrid>']
        out += [f'<a:gridCol w="{c}"/>' for c in colw]
        out.append('</a:tblGrid>')
        for ri, row in enumerate(rows):
            head = header and ri == 0
            out.append(f'<a:tr h="{int(rowh)}">')
            for cell in row:
                txt, algn = cell if isinstance(cell, tuple) else \
                    (cell, 'r' if len(str(cell)) > 22 else 'ctr')
                fill = self.P if head else (self.Lt if ri % 2 == 0 else "FFFFFF")
                col = "FFFFFF" if head else self.B
                ln = ''.join(
                    f'<a:ln{s} w="6350"><a:solidFill><a:srgbClr val="D9D2CC"/>'
                    f'</a:solidFill></a:ln{s}>' for s in ('L', 'R', 'T', 'B'))
                out.append(
                    f'<a:tc><a:txBody><a:bodyPr rtlCol="1" anchor="ctr" lIns="82000" '
                    f'rIns="82000" tIns="36000" bIns="36000"/><a:lstStyle/>'
                    f'{self.par([self.run(txt, sz, 1 if head else 0, col)], algn, 0, 110000)}'
                    f'</a:txBody><a:tcPr marL="0" marR="0">{ln}'
                    f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill></a:tcPr></a:tc>')
            out.append('</a:tr>')
        out.append('</a:tbl></a:graphicData></a:graphic></p:graphicFrame>')
        return ''.join(out)

    # ---------- كتابة ----------
    def path(self, n):
        return f'{self.d}/ppt/slides/slide{n}.xml'

    def read(self, n):
        return open(self.path(n), encoding='utf-8').read()

    def write(self, n, shapes):
        s = self.read(n)
        s = s.replace('</p:spTree>', ''.join(shapes) + '</p:spTree>')
        open(self.path(n), 'w', encoding='utf-8').write(s)

    def blank(self, n):
        """يفرّغ شريحة مكررة من كل الأشكال ويبقي الخلفية."""
        s = re.sub(r'<p:sp>(?:(?!</p:sp>).)*?</p:sp>', '', self.read(n), flags=re.S)
        open(self.path(n), 'w', encoding='utf-8').write(s)

    # ---------- تعبئة جدول قائم في القالب ----------
    def fill_existing(self, n, table_index, data):
        """data: {(row, col): (text, size, bold, color, align)}
        تحذير: افحص أي فهرس عمود هو اليمين قبل الاعتماد. القوالب تختلف.
        عبّئ بقيم اختبار وحوّل إلى صورة أولا."""
        s = self.read(n)
        t = list(re.finditer(r'<a:tbl>.*?</a:tbl>', s, re.S))[table_index]
        tx = t.group(0)
        rows = list(re.finditer(r'<a:tr .*?</a:tr>', tx, re.S))
        new = tx
        for ri in range(len(rows) - 1, -1, -1):
            rt = rows[ri].group(0); nr = rt
            cs = list(re.finditer(r'<a:tc[ >].*?</a:tc>', rt, re.S))
            for ci in range(len(cs) - 1, -1, -1):
                if (ri, ci) not in data:
                    continue
                txt, sz, b, col, algn = data[(ri, ci)]
                body = (f'<a:txBody><a:bodyPr rtlCol="1" anchor="ctr"/><a:lstStyle/>'
                        f'{self.par([self.run(txt, sz, b, col)], algn)}</a:txBody>')
                nc = re.sub(r'<a:txBody>.*?</a:txBody>', body, cs[ci].group(0), flags=re.S)
                nr = nr[:cs[ci].start()] + nc + nr[cs[ci].end():]
            new = new[:rows[ri].start()] + nr + new[rows[ri].end():]
        s = s[:t.start()] + new + s[t.end():]
        open(self.path(n), 'w', encoding='utf-8').write(s)

    def trim_rows(self, n, table_index, keep):
        """يحذف الصفوف الزائدة في جدول القالب بدل تركها فارغة."""
        s = self.read(n)
        t = list(re.finditer(r'<a:tbl>.*?</a:tbl>', s, re.S))[table_index]
        tx = t.group(0)
        trs = list(re.finditer(r'<a:tr .*?</a:tr>', tx, re.S))
        for i in range(len(trs) - 1, keep - 1, -1):
            tx = tx[:trs[i].start()] + tx[trs[i].end():]
        open(self.path(n), 'w', encoding='utf-8').write(s[:t.start()] + tx + s[t.end():])

    # ---------- ترتيب الشرائح ----------
    def reorder(self, keep_rids):
        p = f'{self.d}/ppt/presentation.xml'
        s = open(p, encoding='utf-8').read()
        new = ''.join(f'<p:sldId id="{300+i}" r:id="{r}"/>'
                      for i, r in enumerate(keep_rids))
        s = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>',
                   '<p:sldIdLst>' + new + '</p:sldIdLst>', s, flags=re.S)
        open(p, 'w', encoding='utf-8').write(s)

    def slide_order(self):
        """يعيد [(الترتيب، rId، اسم الملف)] لمعرفة ما يحذف أو يعاد ترتيبه."""
        s = open(f'{self.d}/ppt/presentation.xml', encoding='utf-8').read()
        rels = open(f'{self.d}/ppt/_rels/presentation.xml.rels', encoding='utf-8').read()
        m = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="slides/(slide\d+\.xml)"', rels))
        lst = re.search(r'<p:sldIdLst>(.*?)</p:sldIdLst>', s, re.S).group(1)
        rids = re.findall(r'r:id="(rId\d+)"', lst)
        return [(i + 1, r, m.get(r)) for i, r in enumerate(rids)]

    # ---------- مخططات زمنية ----------
    @staticmethod
    def gantt_geom(right_edge, unit, start, end):
        """إحداثيات شريط في مخطط من اليمين لليسار."""
        return int(right_edge - end * unit), int((end - start) * unit)
