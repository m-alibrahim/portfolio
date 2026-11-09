---
name: dream-100-contact-finder
description: Find 3 decision-makers per company for a recruitment agency's Dream 100 market map. Takes the Companies xlsx produced by the dream-100-market-map skill as input, then uses Exa to discover decision-maker LinkedIn URLs per company. Use this skill whenever the user has a list of target companies (from dream-100-market-map or any other source) and asks to find contacts, decision-makers, hiring managers, HR leads, or LinkedIn URLs for outreach. Also triggers on "find me the contacts at these companies", "who do I reach out to at X", "find decision-makers for my Dream 100 list", or any request to populate contact information for a list of recruitment-agency target companies. Output is a Lemlist-ready xlsx with both the Companies sheet (passed through) and a new Contacts sheet (~300 rows, 3 per company). Run this in a FRESH chat after dream-100-market-map — the split keeps context budgets clean. This skill is specific to RECRUITMENT agency outreach — do not use for general B2B contact lists.
---

# Dream 100 Contact Finder

Takes the Companies xlsx from `dream-100-market-map` and finds 3 decision-makers per company with LinkedIn URLs. Output is the complete Lemlist-ready xlsx (Companies + Contacts sheets) ready for import.

**Two-skill chain:**
- **`dream-100-market-map`** = WHO to target (the 100 companies)
- **`dream-100-contact-finder` (this skill)** = decision-makers per company
- **`dream-100-outreach`** = HOW to reach each prospect (11 assets per DM)

This skill is designed to run in a **fresh chat** with the Companies xlsx attached as input. Running it in the same chat as the market map risks context exhaustion (~300 LinkedIn searches is heavy).

## Workflow

```
Phase 1: LOAD       → Read Companies xlsx + AgencyProfile sheet
Phase 2: CONFIRM    → Sanity-check agency profile with user (one question)
Phase 3: BATCH FIND → Find 3 DMs per company via Exa, in batches of 20
Phase 4: DELIVER    → Write merged xlsx (Companies + Contacts), present brief
```

---

## Phase 1 — Load the input

Expect a Companies xlsx file from `dream-100-market-map`. It has two sheets:
- **Companies** (100 rows) — passed through unchanged
- **AgencyProfile** (key-value sheet) — agency niche, geography, roles filled, etc.

Read both sheets using the xlsx skill at `/mnt/skills/public/xlsx/SKILL.md`. Read that SKILL.md first.

If the user pastes a list of companies without the xlsx, ask for the file. If they only have company names without the structured data, ask them to run `dream-100-market-map` first.

Extract from AgencyProfile:
- `niche` — drives functional VP title selection
- `rolesFilled` — drives specific hiring-manager title selection
- `idealClientSize` — drives the small/mid/large title selection rule
- `geography` — sanity check for DM location

If AgencyProfile sheet is missing, ask the user one consolidated question to capture: niche, roles filled, ideal client size, geography.

---

## Phase 2 — Confirm agency profile (one question max)

Show the user the agency profile in 3 lines and ask: "Anything to change before I find ~300 contacts?"

If they say "no" or "looks good," proceed. If they want changes, take the updated values and proceed.

Do not interview again — the market-map skill already did that. This is just a sanity check.

---

## Phase 3 — Batch find decision-makers

For each of the 100 companies in the Companies sheet, find **3 decision-makers**. Target ~300 total contacts.

### 3a — Pick the right titles per company

Read `references/dm-title-selection.md` for the full title-priority rules. Quick version:

| Company size | DM titles to prioritize |
|---|---|
| <50 employees | Founder, CEO, MD, Head of People (if any) |
| 50-500 | Head of Talent, Talent Acquisition Lead, HR Director, CPO, plus the relevant functional VP for the niche |
| 500+ | Functional VP for the agency's niche, Head of Talent for that function, Talent Acquisition Partner |

Read the Headcount column in the Companies sheet to determine which bucket each company falls into.

### 3b — Run Exa searches in batches

Read `references/contact-search-queries.md` for proven query patterns.

**Process companies in batches of 20.** This keeps memory clean and lets you save progress mid-run if context gets tight.

For each company, run 3-5 Exa searches (`Exa:web_search_exa`, loaded via `tool_search` if needed). Capture from each result:
- First name (split from full name)
- Last name
- Job title (exact)
- LinkedIn URL (must be `linkedin.com/in/...` format)
- Company name (verify it matches)

**Verification before adding:**
- LinkedIn URL is `linkedin.com/in/...` (not `/company/`, not search result page)
- Title actually matches a decision-maker role for this company's size (not Intern, not Analyst)
- The person currently works at this company (check the Exa snippet; if unclear, skip — don't guess)

**Do not invent names.** If you can only find 2 DMs for a company, write 2. If you can only find 1, flag it in the Notes column for that row.

### 3c — Save progress between batches

After each batch of 20 companies, save what you have so far. If context starts getting tight (you notice slower responses or token warnings), deliver what's done with a clear note: "Batch X of 5 complete — let me know if you want me to continue, or I can deliver what's done now."

---

## Phase 4 — Deliver the merged xlsx

### 4a — Build the xlsx

Use the xlsx skill at `/mnt/skills/public/xlsx/SKILL.md`.

**Three sheets:**

**Sheet 1: "Companies"** — passed through from the input xlsx unchanged.

**Sheet 2: "Contacts"** (~300 rows, Lemlist-ready)

Use these **exact column names** (camelCase, case-sensitive — Lemlist matching depends on it):

| Column | Content |
|---|---|
| firstName | First name |
| lastName | Last name |
| jobTitle | Exact title from LinkedIn |
| linkedinUrl | Full LinkedIn profile URL (linkedin.com/in/...) |
| companyName | Must match the Companies sheet exactly |
| companyDomain | Just the domain, e.g. `ronaldjames.co.uk` (no https://) |
| leadTitle | Copied from the Companies sheet for this company |
| companyHiringSignal | Copied from the Companies sheet (the "Hiring Signal" column) |
| whyTheyFit | Copied from the Companies sheet (the "Why They Fit" column) |
| vacanciesPage | Copied from the Companies sheet |
| dmPriority | 1 = primary target, 2 = backup, 3 = alt — based on title priority |
| notes | Any flags ("Recently joined", "Only DM found for this company", etc.) |

Leave `email` and `phone` columns OUT — Lemlist enriches those at import.
Leave `leadCandidate` OUT — that's filled in per outreach campaign by the agency.

**Sheet 3: "AgencyProfile"** — passed through from the input unchanged (so the outreach skill can read it later).

**Formatting:**
- Header row bold, frozen pane on row 1
- Auto-width columns
- Hyperlinks live
- Sort Companies by Rank ascending
- Sort Contacts by companyName alphabetical, then dmPriority ascending

### 4b — Brief (markdown, in chat, under 200 words)

```
Contacts found for [Agency Name] — [N] companies, [M] decision-makers.

Coverage:
- 3 DMs found: [X] companies
- 2 DMs found: [Y] companies
- 1 DM found: [Z] companies — flagged in notes
- 0 DMs found: [W] companies — consider dropping or asking around

Title mix: [e.g. "Heavy on Head of Talent (45%), VP Engineering (30%), Founder/CEO (25%)"]

Watch-outs: [e.g. "12 contacts joined their company in the last 6 months — great window for outreach"]

Next steps:
1. Import the Contacts sheet into Lemlist — it enriches emails and phones at import
2. Run `dream-100-outreach` (one prospect at a time, deep personalization) for top-priority contacts
3. Variables ready in Lemlist: {{firstName}}, {{companyName}}, {{leadTitle}}, {{companyHiringSignal}}, etc.
```

Save the file to outputs and call `present_files`.

---

## Quality bar before delivering

- [ ] Every contact has a valid `linkedin.com/in/...` URL
- [ ] Every contact's company name matches a row in the Companies sheet exactly
- [ ] No invented people — all names verified from Exa results
- [ ] Coverage stats reported honestly in the brief (don't hide low-coverage companies)
- [ ] camelCase column names exact
- [ ] All three sheets present in output xlsx

---

## What NOT to do

- **Don't invent contacts.** Real LinkedIn URLs only. If you can't find them, leave it blank and note it.
- **Don't enrich emails or phones.** Lemlist does that at import.
- **Don't re-do the market map.** Companies come from the input xlsx — don't go searching for new ones.
- **Don't skip the AgencyProfile read.** It's the only thing that tells you which DM titles to prioritize.
- **Don't process all 100 companies before saving progress.** Batches of 20.
- **Don't use this skill for non-recruitment contact lists.** Title priorities are recruitment-specific.
