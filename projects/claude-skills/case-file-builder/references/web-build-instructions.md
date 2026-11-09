# Web app build instructions

Hand this file, plus `ai-system-prompt.md`, `client-file-structure.md`, `documents-menu.md`,
`legal-guidance-saudi.md` and `team-file-structure.md`, to a coding tool (Lovable, Bolt, v0,
Cursor). It is written to be read by a model directly.

---

## 1. What this product is

An internal intake tool for a licensed Saudi law firm (شركة المكتب).

A lawyer finishes a phone call with a prospective client, pastes rough notes, and the app
generates a **pre-filled** case file. The client opens a private link, corrects what is wrong,
tells their story, answers a few questions, and uploads documents. The firm then gets an
internal memo with every fact tagged by source.

**The core insight, do not design it away:** the value is that the client *corrects a draft*
rather than *fills a blank form*. A generic questionnaire is a worse product. Everything the
lawyer already said in the notes must appear pre-filled on the client's screen.

**All client-facing UI is Arabic, RTL, Latin numerals, no diacritics.**

---

## 2. Stack

- React + Vite + TypeScript + Tailwind
- Supabase (Postgres, Auth, Storage)
- One AI provider call per stage (see `ai-system-prompt.md`)
- PDF/Word export of the internal memo and the client file

---

## 3. Screens

1. **Login** — firm staff only (Supabase Auth). No public signup.
2. **Dashboard** — case cards: client name, matter, status (draft / sent / in progress /
   returned / memo ready), days since sent, limitation flag. Counters at top.
3. **New case** — paste notes, optional known fields, "Generate". Shows the AI draft in an
   editable form: summary points, questions, document list. Lawyer edits, then generates the
   client link and the WhatsApp/email message (copy button).
4. **Client route `/f/:token`** — no login. Arabic RTL. Sections in the fixed order from
   `client-file-structure.md`: summary to correct, "قصتي" free text, parties, timeline,
   questions, documents with upload, goals, notes, confidentiality notice, submit.
   Autosave. Mobile first — most clients open this on a phone.
5. **Case detail** — side-by-side: what the lawyer wrote vs what the client corrected, with
   changes highlighted. Uploaded documents list. Button: "Generate team memo".
6. **Team memo** — printable, source tags visible, footer "مذكرة داخلية — لا تُسلّم للعميل".

---

## 4. Data model (minimum)

```
cases            id, client_name, counterparty, matter, status, created_by,
                 created_at, sent_at, returned_at, limitation_warning
case_tokens      token (random, unguessable), case_id, expires_at, used_at, revoked
case_draft       case_id, summary_points jsonb, questions jsonb,
                 documents jsonb, parties_fields jsonb, timeline jsonb
case_response    case_id, corrected_summary jsonb, story text, answers jsonb,
                 timeline jsonb, goals jsonb, notes text, submitted_at
case_files       case_id, storage_path, original_name, uploaded_at, size, mime
case_memo        case_id, memo jsonb, generated_at, approved_by
audit_log        actor, action, case_id, at, ip
```

---

## 5. Security model — this is the part that must not be simplified

The client route is public by token. Treat it as hostile input.

1. **The `anon` role has no direct table access.** Revoke it. All client-route reads and writes
   go through `security definer` Postgres functions that take the token as an argument, resolve
   it to a single case, and return only that case's client-facing fields.
2. **The token never appears in a query string** in a way that gets logged or shared beyond the
   link itself. No token in analytics events.
3. **Tokens expire** (default 30 days) and are revocable from the dashboard. One token per case.
4. **Uploads are private.** Storage bucket is not public. Client uploads go through a signed
   path scoped to the case; downloads are staff-only signed URLs.
5. **Staff tables (memo, notes, characterization) are unreachable from the client route by
   construction, not by a filter.** Separate functions, separate policies.
6. **RLS on every table.** Staff access is scoped to the firm workspace.
7. **File type and size validation** server-side, not just in the browser.
8. **Audit log** every generate, send, view, submit, and memo action.

---

## 6. Legal and compliance requirements

These come from the firm's obligations, not from product preference. Implement all of them.

1. **No legal advice pre-engagement.** The client-facing file collects facts only. No assessment
   of the case, no chance of success, no amounts, no fees, no promised timeline.
2. **No engagement is created by submission.** The confidentiality and pre-engagement notice
   from `client-file-structure.md` section 9 appears above the submit button and in the exported
   file, verbatim, and cannot be removed by the lawyer editing the draft.
3. **Human in the loop.** AI output is always a draft. Nothing is sent to a client and no memo is
   treated as final without an authenticated lawyer approving it. Record who approved and when.
4. **Limitation periods.** The system may flag internally, but the client sees only one generic
   line: "نلفت انتباهكم إلى أن للمطالبات مددا نظامية، ولذلك نرجو موافاتنا بالملف في أقرب وقت ممكن."
   Never display a computed deadline to a client.
5. **Personal data (Saudi PDPL).** Collect the minimum needed for the stated purpose, state the
   purpose on the client screen, set a retention period per case, support deletion on request,
   and keep the data hosted in line with the firm's chosen residency requirements. Special
   categories (health, judicial) get restricted staff visibility.
6. **Professional secrecy** applies from the first contact, including cases the firm declines.
7. **Conflict check** before a link is issued: match client and counterparty names against
   existing cases and warn the lawyer. Do not auto-block, warn and require an explicit override
   that is logged.
8. **The AI must not invent facts.** Highlight any generated name, date, or amount that is
   absent from the source notes so the lawyer can see it before sending.
9. **Article numbers and statutory references** produced by the AI are shown as unverified until
   a lawyer confirms them.

---

## 7. Content generation rules for the app

Read `ai-system-prompt.md` for the exact prompts and JSON schemas, and `legal-guidance-saudi.md`
for the substantive rules that drive question and document selection.

Hard rules to enforce in code, not only in the prompt:

- Maximum 8 questions, 6 documents "نحتاجها الآن", 4 documents "إن تيسر لاحقا".
- Every document row must carry a one-line reason. Empty reason blocks send.
- The "قصتي" section is mandatory and always second. It cannot be removed, shortened, or moved.
- Fixed copy (intro, "قصتي" preamble, filling instructions, confidentiality notice) is stored in
  the app and rendered as-is, never regenerated.

---

## 8. Build order and acceptance tests

1. Auth, schema, RLS, security definer functions. *Test: anonymous client with a valid token can
   read only that case's client fields, and gets nothing from memo or notes tables.*
2. New case + Stage A generation + editable draft. *Test: notes containing no date produce no
   date anywhere in the output.*
3. Client route with autosave and uploads. *Test: submit on a phone at 360px width with three
   files, then reopen the link and see saved answers.*
4. Case detail with diff highlighting. *Test: a corrected summary point renders visibly changed.*
5. Stage B memo generation and print/export. *Test: every fact carries a source tag; the internal
   footer is present.*
6. Conflict check, token expiry and revocation, audit log. *Test: a revoked token returns a
   neutral "الرابط لم يعد صالحا" page and writes an audit entry.*

---

## 9. Out of scope for version one

Billing and fee agreements, e-signature, court filing integrations, client login accounts,
multi-firm tenancy, automatic OCR of uploads, and any automated legal opinion.
