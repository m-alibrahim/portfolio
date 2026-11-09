---
name: "redact-sensitive-info"
description: "حجب المعلومات الحساسة — يشطب من ملفات PDF شطبًا حقيقيًا لا يمكن التراجع عنه: أسماء العملاء، الشعارات والعلامات التجارية، السجلات التجارية، التواريخ، الأشخاص، المبالغ، والميتاداتا. استخدم هذه المهارة كلما ذُكر حجب أو شطب أو تعقيم أو إخفاء أو تخفية اسم أو \"redact\"، وكلما أراد المستخدم مشاركة PDF مع طرف ثالث أو استعراض نموذج عمل سابق أو إرساله لعميل محتمل أو للمحكمة أو للنشر، حتى لو لم يقل كلمة \"حجب\" صراحة. Also use for any request to remove, black out, anonymize, or strip identifying data from a PDF before sharing it. تعالج المهارة تحديدًا مشكلة النص العربي المشوّه داخل الـPDF التي تُفشل البحث النصي العادي، والشعارات التي لا يراها استخراج النص."
---

# حجب المعلومات الحساسة من ملفات PDF

Redact sensitive information from PDFs so it is **actually gone** — removed from the content stream, not merely covered by a rectangle.

The failure mode this skill exists to prevent: someone draws black boxes with an annotation tool, ships the file, and the recipient selects the text underneath and copies it out. That has ended careers. Everything below is oriented around making sure that cannot happen, and around proving it didn't.

---

## المبدأ الأساسي

Four things must all be true before delivery:

1. The text is deleted from the PDF content stream — `Ctrl+A, Ctrl+C` on the output yields nothing sensitive.
2. Logos and other raster marks are destroyed at the pixel level, not covered.
3. The metadata is wiped — author fields and creation dates routinely leak more than the body text does.
4. You verified 1–3 by re-extracting from the *output* file and by looking at rendered pages, not by assuming.

Never claim a file is redacted without running the verification step. "It looks black in the preview" is not evidence.

---

## المشكلة التقنية التي تُفشل معظم المحاولات

Arabic PDFs — especially those exported from InDesign, Word, or macOS Quartz — store text as **presentation-form glyphs in visual order**, not as logical Unicode. In one real file the phrase `شركة رموز` was stored as four separate word tokens:

```
'ﺷﺮﻛﺔ'  'ر'  'ﻣﻮ'  'ز'
```

Consequences you must plan around:

- `page.search_for("رموز")` returns **zero hits**. The string is not in the file in that form.
- Word order within a line is often reversed; sometimes letters within a token are reversed too.
- Some glyphs are corrupted outright — a `ب` may be stored as a Latin `H`. This means **long search phrases fail even when short ones succeed.**

The fix is to normalize with `NFKC` (which folds presentation forms back to base letters), strip everything non-alphanumeric, and slide a window across consecutive word tokens comparing the joined result — in both directions.

**Practical rule: search on the shortest distinctive fragment.** For `شركة رموز العربية`, search `رموز`. Searching the full name returns nothing because the corrupted `ب` in `العربية` breaks the match. Redacting the distinctive fragment while leaving the generic word `شركة` visible also reads better — `شركة ███ للتعاقد` flows naturally, whereas blacking out both leaves a jarring gap.

---

## سير العمل

### ١. استخرج وافحص

Read every page and build the list of candidates. Do not skim — identifiers hide in headers, footers, and mid-sentence.

Sweep for:

- اسم الشركة أو الشخص، وكل اختصار أو اشتقاق منه (بالعربي والإنجليزي معًا)
- الشعار والعلامة التجارية — صور لا يراها استخراج النص
- أرقام السجل التجاري والرقم الضريبي والعناوين
- التواريخ الهجرية والميلادية التي تحدد زمن العمل
- أسماء الأشخاص، البريد الإلكتروني، أرقام الجوال
- أسطر التوجيه في الترويسة: "إلى:"، "عناية:"
- أرقام العقود والملفات والمراجع الداخلية
- المبالغ المحددة، أسماء المشاريع، المواقع الجغرافية
- الميتاداتا داخل الملف

**Two sweeps catch what one misses.** Text extraction is blind to rasters, so also enumerate images and render pages:

```python
for pno, page in enumerate(d):
    for x in page.get_images(full=True):
        print(pno + 1, x[0], [list(r) for r in page.get_image_rects(x[0])])
```

A logo repeated on every page is the single most common way a "verified clean" file still leaks — and logos often carry a tagline naming a parent company or fund that appears nowhere in the text.

Read the metadata early, not at the end. `author` frequently holds a real employee's email address.

### ٢. صنّف واعرض قبل التنفيذ

Split the candidates into three buckets and show the user the table before touching the file:

| يُحجب | يبقى | اسأل |
|---|---|---|
| كل ما يدل على الطرف الآخر | ترويسة المكتب وشعاره | أي بند مشكوك فيه |
| الشعار والعلامة التجارية للعميل | السجل التجاري للمكتب | التفاصيل الوقائعية الحدّية |
| التواريخ ومراجع الملف | بيانات التواصل في التذييل | المبالغ والمكافآت |
| | المحتوى الفني والتحليل النظامي بالكامل | |

**First establish whose document it is.** If it carries your own firm's letterhead, that letterhead is normally kept — it identifies the sender, not the counterparty, and its presence is what makes a work sample credible. But if the whole document belongs to the client (their charter, their policy, their template), there is nothing to keep and the header goes too. Getting this backwards in either direction is costly, so confirm rather than assume.

Distinguish **engagement dates** from **legal-reference dates**. The date a consultation was issued identifies the client; the date a statute or regulation was promulgated is part of the analysis and deleting it guts the work. A blanket year search will hit both.

The judgment call worth surfacing every time: **facts can identify a party even after the name is gone.** A rare business activity, a well-known transaction, an unusual deal size — any of these can let a reader in the same market reconstruct who it was. Flag this explicitly and let the user decide; you cannot assess market notoriety on their behalf.

### ٣. نفّذ

Write the script below to `redact_pdf.py`, then:

```bash
pip install pymupdf --break-system-packages -q

python3 redact_pdf.py scan IN.pdf "رموز" "1010653688" "٢٠٢٤"
# → prints hit counts per page and writes redaction_plan.json
```

Review the plan. Hit counts that look wrong are your early warning — zero hits usually means the term is glyph-corrupted, so try a shorter fragment. Then add whole-line removals and logo rectangles, and apply:

```jsonc
// redaction_plan.json — entries you add by hand
"lines":  [ {"page": 1, "y": 157, "x0": 325} ],
// y = vertical centre of the line; x0/x1 optionally widen the box so
// sibling lines end up the same width and the result looks deliberate
"images": [ {"page": 1, "rect": [203, 68, 409, 320]} ]
// take rects from get_image_rects(); these are burned out at pixel level
```

```bash
python3 redact_pdf.py apply IN.pdf OUT.pdf redaction_plan.json
```

### ٤. تحقّق — لا تتخطَّ هذه الخطوة

```bash
python3 redact_pdf.py verify OUT.pdf "رموز" "1010653688" "٢٠٢٤"
```

Exit code 0 means every term is gone from the extracted text and the metadata is clean.

**A FAIL is not automatically a leak — print the surrounding context before reacting.** Because the verifier strips punctuation and spaces to defeat glyph mangling, ordinary prose can produce spurious matches: `all committee` collapses to `allcommittee`, which contains `llc`; `membership if it` contains `pif`. Look at the neighbouring characters and decide. Silencing a real hit and panicking over a false one are both failures.

Then render every page whose layout you touched and actually look. The text check proves deletion; the image check proves you didn't black out something you needed, and catches over-wide boxes.

```python
import fitz; fitz.open("OUT.pdf")[0].get_pixmap(dpi=110).save("check.png")
```

Watch for a box far wider than its neighbours — usually a match that wrapped across a line break. The script below already splits those per line, but verify visually anyway.

### ٥. سلّم

Save under a **new** filename that signals what it is; never overwrite the original — the unredacted version is the firm's record. If the working directory refuses deletes, write to `/tmp` first and copy in. Check the filename itself for identifiers.

Report to the user: عدد مواضع الحجب في كل صفحة، تأكيد نظافة الاستخراج والميتاداتا، والملاحظة الوقائعية إن وُجدت.

---

## السكربت

```python
#!/usr/bin/env python3
"""True redaction for PDFs, built to survive Arabic glyph mangling.

  python redact_pdf.py scan   IN.pdf  "term1" "term2" ...
  python redact_pdf.py apply  IN.pdf OUT.pdf plan.json
  python redact_pdf.py verify OUT.pdf "term1" "term2" ...
"""
import fitz, unicodedata, re, sys, json

_FOLD = str.maketrans({'أ':'ا','إ':'ا','آ':'ا','ٱ':'ا','ة':'ه','ى':'ي'})

def norm(s: str) -> str:
    """Fold a token to a comparable key.

    NFKC turns Arabic presentation forms (ﺷﺮﻛﺔ) back into base letters (شركة).
    Everything non-alphanumeric is dropped so spacing and punctuation never block a match.
    """
    s = unicodedata.normalize('NFKC', s).replace('ـ', '')
    s = re.sub(r'[^\w]', '', s, flags=re.UNICODE)
    return s.translate(_FOLD).lower()

def find_runs(page, term, max_span=8):
    """Rects for every occurrence of `term`, however the PDF split or reversed it."""
    t = norm(term)
    if not t:
        return []
    tr = t[::-1]
    ws = page.get_text("words")
    rects, i = [], 0
    while i < len(ws):
        hit = 0
        for L in range(1, max_span + 1):
            if i + L > len(ws):
                break
            j = ''.join(norm(w[4]) for w in ws[i:i + L])
            if j in (t, tr):
                hit = L
                break
            if len(j) > len(t) + 24:      # window overshot the term; stop growing
                break
        if not hit:                        # fallback: term glued inside one token
            k = norm(ws[i][4])
            if t in k or tr in k:
                hit = 1
        if hit:
            g = ws[i:i + hit]
            # A match can wrap across lines. Union-boxing it would black out the
            # whole gap between them, so emit one rect per line band instead.
            bands = {}
            for w in g:
                bands.setdefault(round((w[1] + w[3]) / 2 / 4), []).append(w)
            for b in bands.values():
                rects.append(fitz.Rect(min(w[0] for w in b) - 1.5, min(w[1] for w in b) - 0.5,
                                       max(w[2] for w in b) + 1.5, max(w[3] for w in b) + 0.5))
            i += hit
        else:
            i += 1
    return rects

def line_rect(page, y_center, pad=1.5):
    """Rect covering the whole text line whose vertical centre is nearest y_center."""
    ws = page.get_text("words")
    sel = [w for w in ws if abs((w[1] + w[3]) / 2 - y_center) < 8]
    if not sel:
        return None
    return fitz.Rect(min(w[0] for w in sel) - pad, min(w[1] for w in sel) - pad,
                     max(w[2] for w in sel) + pad, max(w[3] for w in sel) + pad)

def scan(path, terms):
    d = fitz.open(path)
    plan = {"terms": [], "lines": [], "images": []}
    for term in terms:
        entry = {"term": term, "hits": []}
        for pno, page in enumerate(d):
            for r in find_runs(page, term):
                entry["hits"].append({"page": pno + 1, "rect": [round(v, 1) for v in r]})
        plan["terms"].append(entry)
        wide = [h for h in entry["hits"] if h["rect"][2] - h["rect"][0] > 200]
        print(f'"{term}": {len(entry["hits"])} hit(s) -> '
              f'{sorted({h["page"] for h in entry["hits"]})}'
              + (f'  [{len(wide)} unusually wide — inspect]' if wide else ''))
    print("\nimages (text extraction cannot see these):")
    for pno, page in enumerate(d):
        for x in page.get_images(full=True):
            for r in page.get_image_rects(x[0]):
                print(f'  page {pno+1} xref {x[0]} {[round(v,1) for v in r]}')
    print("\nmetadata:", {k: v for k, v in d.metadata.items() if v})
    return plan

def apply(inp, out, plan):
    d = fitz.open(inp)
    n, has_img = 0, False
    for entry in plan.get("terms", []):
        for h in entry["hits"]:
            d[h["page"] - 1].add_redact_annot(fitz.Rect(*h["rect"]), fill=(0, 0, 0)); n += 1
    for ln in plan.get("lines", []):
        page = d[ln["page"] - 1]
        r = fitz.Rect(*ln["rect"]) if "rect" in ln else line_rect(page, ln["y"])
        if r:
            if "x0" in ln: r.x0 = ln["x0"]
            if "x1" in ln: r.x1 = ln["x1"]
            page.add_redact_annot(r, fill=(0, 0, 0)); n += 1
    for im in plan.get("images", []):
        d[im["page"] - 1].add_redact_annot(fitz.Rect(*im["rect"]), fill=(0, 0, 0))
        n += 1; has_img = True
    mode = fitz.PDF_REDACT_IMAGE_PIXELS if has_img else fitz.PDF_REDACT_IMAGE_NONE
    for page in d:
        page.apply_redactions(images=mode)
    d.set_metadata({}); d.del_xml_metadata()
    d.save(out, garbage=4, deflate=True, clean=True)
    print(f"applied {n} redaction(s) -> {out}")

def verify(path, terms):
    d = fitz.open(path)
    pages = [norm(p.get_text()) for p in d]
    blob = ''.join(pages)
    ok = True
    for term in terms:
        t = norm(term)
        c = blob.count(t) + (blob.count(t[::-1]) if t[::-1] != t else 0)
        print(f'{"FAIL" if c else "PASS"}  "{term}": {c} residual occurrence(s)')
        if c:
            ok = False
            for pno, b in enumerate(pages):          # context so you can judge false positives
                for m in re.finditer(re.escape(t), b):
                    print(f'      p{pno+1}: ...{b[max(0, m.start()-40):m.end()+40]}...')
    meta = {k: v for k, v in d.metadata.items() if v and k != 'format'}
    print(f'{"FAIL" if meta else "PASS"}  metadata: {meta or "clean"}')
    if meta: ok = False
    return ok

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "scan":
        json.dump(scan(sys.argv[2], sys.argv[3:]), open("redaction_plan.json", "w"),
                  ensure_ascii=False, indent=1)
        print("\nplan written to redaction_plan.json — review before apply")
    elif cmd == "apply":
        apply(sys.argv[2], sys.argv[3], json.load(open(sys.argv[4])))
    elif cmd == "verify":
        sys.exit(0 if verify(sys.argv[2], sys.argv[3:]) else 1)
```

---

## حالات خاصة

**الشعار والعلامة التجارية.** Rasters are invisible to `get_text()`. Take rects from `get_image_rects()`, put them in `plan["images"]`, and the script switches to `PDF_REDACT_IMAGE_PIXELS`, which destroys the underlying pixels rather than drawing over them. Inspect the extracted image itself (`fitz.Pixmap(d, xref).save(...)`) before deciding — some xrefs are masks or decorative shapes that carry no identity and need not go.

**PDF ممسوح ضوئيًا (صور فقط).** `get_text()` يرجع فارغًا. There is no text layer to delete, so everything is an image redaction. Tell the user the file was image-based — it changes what "verified" means, since there is no text extraction to check against.

**الملف مقفل بكلمة مرور.** Ask for it; do not attempt to bypass.

**النتيجة صفر مواضع لمصطلح تتوقع وجوده.** Almost always glyph corruption. Shorten the term to its most distinctive three or four letters and rescan before concluding it isn't there.

**المستند ثنائي اللغة.** The same entity appears as an English name and an Arabic name that are not translations of each other in the text layer. Search both independently; finding one does not mean you found the other.

