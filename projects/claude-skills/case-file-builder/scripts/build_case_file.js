/**
 * build_case_file.js
 * محرك توليد ملفات القضايا بصيغة وورد عربية (اتجاه من اليمين لليسار).
 *
 * التثبيت:
 *   npm install docx
 *
 * الاستخدام:
 *   node build_case_file.js spec.json "/mnt/user-data/outputs/ملف-القضية.docx"
 *
 * صيغة spec.json موصوفة في references/spec-format.md
 */

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType,
  Footer, PageNumber, LevelFormat,
} = require("docx");

const FONT = "Arial";
const TOTAL = 9000;
const NAVY = "1F3864";
const GREY = "F2F2F2";
const LINE = "BFBFBF";
const MUTED = "595959";

const DOTS = "..........................................................................................................................................";

/* ------------------------- أدوات أساسية ------------------------- */

function run(text, o = {}) {
  return new TextRun({
    text: String(text === undefined || text === null ? "" : text),
    rightToLeft: true,
    font: FONT,
    size: o.size || 22,
    bold: !!o.bold,
    italics: !!o.italics,
    color: o.color,
  });
}

function para(text, o = {}) {
  return new Paragraph({
    bidirectional: true,
    alignment: o.align || AlignmentType.JUSTIFIED,
    spacing: { after: o.after === undefined ? 120 : o.after, line: o.line || 300 },
    border: o.border,
    numbering: o.numbering,
    children: [run(text, o)],
  });
}

function h1(text) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 340, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 4 } },
    children: [run(text, { bold: true, size: 26, color: NAVY })],
  });
}

function h2(text) {
  return new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { before: 220, after: 100 },
    children: [run(text, { bold: true, size: 23, color: NAVY })],
  });
}

function normalize(widths, n) {
  let w = Array.isArray(widths) && widths.length === n
    ? widths.slice()
    : new Array(n).fill(Math.floor(TOTAL / n));
  const sum = w.reduce((a, b) => a + b, 0);
  if (sum !== TOTAL) {
    w = w.map((x) => Math.floor((x * TOTAL) / sum));
    w[w.length - 1] += TOTAL - w.reduce((a, b) => a + b, 0);
  }
  return w;
}

function cell(text, width, o = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: o.head
      ? { type: ShadingType.CLEAR, fill: NAVY, color: "auto" }
      : (o.grey ? { type: ShadingType.CLEAR, fill: GREY, color: "auto" } : undefined),
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    children: [
      new Paragraph({
        bidirectional: true,
        alignment: o.head ? AlignmentType.CENTER : (o.align || AlignmentType.RIGHT),
        spacing: { after: 0, line: 260 },
        children: [run(text, {
          bold: o.head || o.bold,
          color: o.head ? "FFFFFF" : undefined,
          size: o.size || 21,
        })],
      }),
    ],
  });
}

function buildTable(widths, rows) {
  return new Table({
    columnWidths: widths,
    width: { size: TOTAL, type: WidthType.DXA },
    visuallyRightToLeft: true,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      left: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      right: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      insideVertical: { style: BorderStyle.SINGLE, size: 4, color: LINE },
    },
    rows,
  });
}

/* ------------------------- الكتل ------------------------- */

// كل مجموعة مرقمة تأخذ تسلسلا مستقلا يبدأ من 1
const NUM_POOL = 24;
let numIdx = -1;
let lastWasQuestion = false;
function numRef() {
  return "num-" + (numIdx % NUM_POOL);
}

function renderBlock(b) {
  const out = [];
  const t = b.t || b.type;

  if (t === "numbered") {
    numIdx++;
    lastWasQuestion = false;
  } else if (t === "question") {
    if (!lastWasQuestion) numIdx++;
    lastWasQuestion = true;
  } else {
    lastWasQuestion = false;
  }

  switch (t) {
    case "h2":
      out.push(h2(b.text));
      break;

    case "p":
      out.push(para(b.text, { after: b.after }));
      break;

    case "note":
      out.push(new Paragraph({
        bidirectional: true,
        alignment: AlignmentType.JUSTIFIED,
        spacing: { before: 100, after: 160, line: 300 },
        shading: { type: ShadingType.CLEAR, fill: GREY, color: "auto" },
        border: {
          top: { style: BorderStyle.SINGLE, size: 2, color: LINE, space: 6 },
          bottom: { style: BorderStyle.SINGLE, size: 2, color: LINE, space: 6 },
          left: { style: BorderStyle.SINGLE, size: 2, color: LINE, space: 6 },
          right: { style: BorderStyle.SINGLE, size: 2, color: LINE, space: 6 },
        },
        children: [run(b.text, { size: 21 })],
      }));
      break;

    case "bullets":
      (b.items || []).forEach((it) => {
        out.push(new Paragraph({
          bidirectional: true,
          alignment: AlignmentType.JUSTIFIED,
          numbering: { reference: "dash-list", level: 0 },
          spacing: { after: 90, line: 300 },
          children: [run(it)],
        }));
      });
      break;

    case "numbered":
      (b.items || []).forEach((it) => {
        out.push(new Paragraph({
          bidirectional: true,
          alignment: AlignmentType.JUSTIFIED,
          numbering: { reference: numRef(), level: 0 },
          spacing: { after: 90, line: 300 },
          children: [run(it)],
        }));
      });
      break;

    case "fill":
      out.push(new Paragraph({
        bidirectional: true,
        alignment: AlignmentType.RIGHT,
        spacing: { after: 140, line: 320 },
        children: [run(b.label + " " + DOTS.slice(0, Math.max(20, 120 - String(b.label).length)))],
      }));
      break;

    case "lines":
      for (let i = 0; i < (b.n || 5); i++) {
        out.push(new Paragraph({
          bidirectional: true,
          alignment: AlignmentType.RIGHT,
          spacing: { after: 220, line: 320 },
          children: [run(DOTS)],
        }));
      }
      break;

    case "question":
      out.push(new Paragraph({
        bidirectional: true,
        alignment: AlignmentType.JUSTIFIED,
        numbering: { reference: numRef(), level: 0 },
        spacing: { after: 100, line: 300 },
        children: [run(b.text)],
      }));
      for (let i = 0; i < (b.lines || 2); i++) {
        out.push(new Paragraph({
          bidirectional: true,
          alignment: AlignmentType.RIGHT,
          spacing: { after: 180, line: 320 },
          children: [run(DOTS)],
        }));
      }
      break;

    case "kv": {
      const w = normalize(b.widths, 2);
      const rows = (b.rows || []).map((r) =>
        new TableRow({ children: [cell(r[0], w[0], { grey: true, bold: true }), cell(r[1] || "", w[1])] })
      );
      out.push(buildTable(w, rows));
      break;
    }

    case "form": {
      const w = normalize(b.widths, 2);
      const heads = b.headers || ["البيان", "التعبئة"];
      const rows = [new TableRow({
        tableHeader: true,
        children: [cell(heads[0], w[0], { head: true }), cell(heads[1], w[1], { head: true })],
      })];
      (b.items || []).forEach((it) => {
        rows.push(new TableRow({ children: [cell(it, w[0], { grey: true }), cell("", w[1])] }));
      });
      out.push(buildTable(w, rows));
      break;
    }

    case "table": {
      const n = (b.headers || []).length;
      const w = normalize(b.widths, n);
      const rows = [new TableRow({
        tableHeader: true,
        children: b.headers.map((hd, hi) => cell(hd, w[hi], { head: true, size: 20 })),
      })];
      (b.rows || []).forEach((r) => {
        rows.push(new TableRow({
          children: w.map((cw, ci) => cell(
            r[ci] === undefined ? "" : r[ci],
            cw,
            { size: 20, align: ci === 0 && b.numbered ? AlignmentType.CENTER : undefined }
          )),
        }));
      });
      const start = (b.rows || []).length;
      for (let i = 0; i < (b.emptyRows || 0); i++) {
        rows.push(new TableRow({
          children: w.map((cw, ci) => cell(
            ci === 0 && b.numbered ? String(start + i + 1) : "",
            cw,
            { size: 20, align: ci === 0 && b.numbered ? AlignmentType.CENTER : undefined }
          )),
        }));
      }
      if (b.totalRow) {
        rows.push(new TableRow({
          children: w.map((cw, ci) => cell(ci === 1 ? "الإجمالي" : "", cw, { grey: true, bold: ci === 1 })),
        }));
      }
      out.push(buildTable(w, rows));
      break;
    }

    case "signature": {
      const w = normalize(b.widths, 3);
      const labels = b.labels || ["الاسم", "التوقيع", "التاريخ"];
      out.push(buildTable(w, [
        new TableRow({
          children: labels.map((l, i) => cell(l, w[i], { grey: true, bold: true, align: AlignmentType.CENTER })),
        }),
        new TableRow({
          height: { value: 700, rule: "atLeast" },
          children: w.map((cw) => cell("", cw)),
        }),
      ]));
      break;
    }

    case "spacer":
      out.push(para("", { after: b.after || 200 }));
      break;

    default:
      throw new Error("نوع كتلة غير معروف: " + t);
  }
  return out;
}

/* ------------------------- البناء ------------------------- */

function build(spec) {
  numIdx = -1;
  lastWasQuestion = false;
  const children = [];

  children.push(new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [run(spec.org || "شركة المكتب", { bold: true, size: 24, color: NAVY })],
  }));

  children.push(new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.CENTER,
    spacing: { after: spec.subtitle ? 160 : 260 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: NAVY, space: 6 } },
    children: [run(spec.title || "ملف القضية", { bold: true, size: 32 })],
  }));

  if (spec.subtitle) {
    children.push(new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      spacing: { after: 260 },
      children: [run(spec.subtitle, { bold: true, size: 23 })],
    }));
  }

  if (spec.internal) {
    children.push(new Paragraph({
      bidirectional: true,
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
      shading: { type: ShadingType.CLEAR, fill: GREY, color: "auto" },
      children: [run("مذكرة داخلية — لا تُسلّم للعميل بصيغتها هذه", { bold: true, size: 21 })],
    }));
  }

  if (spec.meta && spec.meta.length) {
    renderBlock({ t: "kv", rows: spec.meta, widths: spec.metaWidths || [2600, 6400] }).forEach((x) => children.push(x));
    children.push(para("", { after: 240 }));
  }

  (spec.intro || []).forEach((line) => {
    children.push(para(line, { align: AlignmentType.RIGHT }));
  });
  if (spec.intro && spec.intro.length) children.push(para("", { after: 120 }));

  (spec.sections || []).forEach((sec) => {
    if (sec.h) children.push(h1(sec.h));
    (sec.blocks || []).forEach((b) => {
      renderBlock(b).forEach((x) => children.push(x));
      if (["kv", "form", "table", "signature"].includes(b.t || b.type)) {
        children.push(para("", { after: 140 }));
      }
    });
  });

  return new Document({
    styles: { default: { document: { run: { font: FONT, size: 22 } } } },
    numbering: {
      config: [
        {
          reference: "dash-list",
          levels: [{
            level: 0, format: LevelFormat.BULLET, text: "-", alignment: AlignmentType.RIGHT,
            style: { paragraph: { indent: { start: 360, hanging: 220 } } },
          }],
        },
        ...Array.from({ length: NUM_POOL }, (_, i) => ({
          reference: "num-" + i,
          levels: [{
            level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.RIGHT,
            style: { paragraph: { indent: { start: 400, hanging: 260 } } },
          }],
        })),
      ],
    },
    sections: [{
      properties: { page: { margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } } },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            bidirectional: true,
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({
                text: (spec.footer || spec.title || "ملف القضية") + "   |   صفحة ",
                rightToLeft: true, font: FONT, size: 18, color: MUTED,
              }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: MUTED }),
            ],
          })],
        }),
      },
      children,
    }],
  });
}

/* ------------------------- التشغيل ------------------------- */

const specPath = process.argv[2];
const outPath = process.argv[3];

if (!specPath || !outPath) {
  console.error("الاستخدام: node build_case_file.js spec.json output.docx");
  process.exit(1);
}

const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));

Packer.toBuffer(build(spec)).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log("تم إنشاء: " + outPath);
}).catch((e) => {
  console.error("خطأ: " + e.message);
  process.exit(1);
});
