#!/usr/bin/env python3
"""استخراج الهوية البصرية والمحتوى من ملف pptx أو docx قائم.
الاستخدام: python3 inspect_brand.py <file> [--texts]
"""
import sys, re, zipfile, collections

def pptx(path, texts):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    fonts = collections.Counter()
    for n in names:
        if re.match(r'ppt/(slides|slideMasters|slideLayouts)/\w+\.xml$', n):
            fonts.update(re.findall(r'typeface="([^"]+)"', z.read(n).decode('utf-8', 'ignore')))
    print("=== الخطوط الأكثر استخداما ===")
    for f, c in fonts.most_common(8):
        if f and f not in ('+mj-lt', '+mn-lt', '+mj-ea', '+mn-ea'):
            print(f"  {c:5d}  {f}")

    th = [n for n in names if n.startswith('ppt/theme/')]
    if th:
        s = z.read(th[0]).decode('utf-8', 'ignore')
        m = re.search(r'<a:clrScheme.*?</a:clrScheme>', s, re.S)
        print("\n=== ألوان السمة ===")
        if m:
            for tag, val in re.findall(r'<a:(\w+)>\s*<a:srgbClr val="([0-9A-Fa-f]{6})"/>', m.group(0)):
                print(f"  {tag:10s} #{val}")
        mj = re.search(r'<a:majorFont><a:latin typeface="([^"]*)"', s)
        mn = re.search(r'<a:minorFont><a:latin typeface="([^"]*)"', s)
        print(f"  خط العناوين: {mj.group(1) if mj else '-'}")
        print(f"  خط المتن:    {mn.group(1) if mn else '-'}")

    slides = sorted([n for n in names if re.match(r'ppt/slides/slide\d+\.xml$', n)],
                    key=lambda x: int(re.search(r'(\d+)', x).group(1)))
    print(f"\n=== الشرائح: {len(slides)} ===")
    for n in slides:
        s = z.read(n).decode('utf-8', 'ignore')
        t = [x for x in re.findall(r'<a:t>(.*?)</a:t>', s, re.S) if x.strip()]
        tb = len(re.findall(r'<a:tbl>', s))
        num = re.search(r'(\d+)', n).group(1)
        head = ' '.join(t[:6])[:80] if t else '(فارغة)'
        print(f"  slide{num:>3}  جداول:{tb}  {head}")
        if texts and t:
            print('        ' + ' | '.join(t)[:600])

def docx(path, texts):
    z = zipfile.ZipFile(path)
    s = z.read('word/document.xml').decode('utf-8', 'ignore')
    fonts = collections.Counter(re.findall(r'w:cs="([^"]+)"', s))
    print("=== الخطوط ===")
    for f, c in fonts.most_common(6):
        print(f"  {c:5d}  {f}")
    print("\n=== الألوان ===")
    for col, c in collections.Counter(re.findall(r'w:val="([0-9A-F]{6})"', s)).most_common(8):
        print(f"  {c:5d}  #{col}")
    print(f"\nالجداول: {len(re.findall(r'<w:tbl>', s))}")
    if texts:
        print('\n'.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', s)))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    p = sys.argv[1]; t = '--texts' in sys.argv
    (pptx if p.endswith(('.pptx', '.potx')) else docx)(p, t)
