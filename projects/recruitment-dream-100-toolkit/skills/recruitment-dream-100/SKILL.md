---
name: recruitment-dream-100
description: Build a Dream 100 target client list for a recruitment agency, with decision-maker LinkedIn URLs ready for Lemlist import. Use this skill whenever the user provides a recruitment agency's domain, LinkedIn, or website copy and asks to find ideal target clients, prospects, dream clients, target companies, or build a Dream 100 / D100 / target list. Also use when the user asks "who should we recruit for," "find me companies hiring in X," or wants a prospecting list for a recruitment / staffing / executive search / talent agency. The skill conducts a short interview to lock the ideal client profile, then uses web search + Exa to source 100 target companies with ~300 decision-makers (3 per company) including LinkedIn URLs. Output is a Lemlist-ready xlsx — emails and phones are enriched downstream in Lemlist. This skill is specific to RECRUITMENT agencies — do not use for other agency types.
---

# Recruitment Dream 100 Builder

Builds a 100-company Dream 100 target client list for a recruitment agency, with ~300 decision-maker contacts (3 per company) and LinkedIn URLs. Output is formatted for direct import into Lemlist, which handles email/phone enrichment downstream.

Based on Chet Holmes' Dream 100 framework adapted for recruitment. Win 10-20 of these and the agency hits seven figures.

## Workflow

```
Phase 1: AUTO-PROFILE   → Fetch site/LinkedIn, extract what you can
Phase 2: INTERVIEW      → Confirm findings + ask thoughtful gap questions
Phase 3: RESEARCH       → Source 100 companies (web_search + Exa)
Phase 4: CONTACTS       → Find 3 decision-makers per company, get LinkedIn URLs via Exa
Phase 5: DELIVER        → Build Lemlist-ready xlsx + brief
```

Do not skip the interview — the user's input drives list quality more than any clever search.

---

## Phase 1 — Auto-profile

Accept any of these inputs:
- Domain (e.g. `ronaldjames.co.uk`)
- LinkedIn company page URL
- Website copy or "About" text
- Short user description

Use `web_fetch` on the homepage, `/about`, `/sectors` (or `/industries`), and `/jobs`. Extract:

1. **Niche / sector** — tech, finance, healthcare, legal, etc.
2. **Roles they fill** — exact job titles
3. **Seniority** — exec, mid, junior, mixed
4. **Geography** — city / region / country
5. **Existing clients** — from case studies, logos, testimonials
6. **Fee model** (if visible) — perm, contract, retained, contingent
7. **Agency size** — informs realistic target size

---

## Phase 2 — Interview

Present what you found in 3-5 lines. Then ask gap questions. **Use the `ask_user_input_v0` tool for multiple-choice questions** — buttons beat typing.

Ask these (skip any already answered by Phase 1):

**Q1 (single_select) — Ideal client size:**
- Startup (<50 employees)
- Scale-up (50-200)
- Mid-market (200-1000)
- Enterprise (1000+)
- Mix

Drives DM title selection. <50 = founder/CEO. 50-500 = HR/Talent lead. 500+ = functional VP.

**Q2 (multi_select) — Sub-sectors to target.** Build 4-6 options from Phase 1 niche (e.g. for tech: SaaS, Fintech, AI/ML, eCom, Cybersecurity, HealthTech).

**Q3 (free text in chat) — Three of your best clients:**
"Name 2-3 of your best current or recent clients (any size, just names). I'll find lookalikes."

Lookalike sourcing is often the highest-signal way to find Dream 100 candidates.

**Q4 (free text in chat, optional) — Exclude list:**
"Any companies or sectors to AVOID? (e.g. a competitor's exclusive accounts, sectors you've had bad experiences with, geographies outside your service area.)"

Max 4 questions. If user gives partial answers, proceed and note assumptions in the brief.

---

## Phase 3 — Research companies

Read `references/research-playbook.md` for specific queries. Run searches in parallel.

### 3a — Source ~150 candidate companies

Use a mix of `web_search` and `Exa:web_search_exa` (Exa is semantic — better for "fastest growing fintech in London 2026" type queries; web_search is better for specific facts and recent news).

To use Exa, first call `tool_search` with query "exa web search" to load the tool, then call `Exa:web_search_exa`.

Sources:
- **Lookalikes of best clients** (from Q3) — same size, sector, geography
- **Funding announcements** in the niche + geography (Series A/B/C/D in last 18 months)
- **Industry "top 100" / "hot 100" / "fastest growing" lists**
- **Local business journals + trade publications**
- **LinkedIn company search** (via Google site:linkedin.com/company queries)

### 3b — Verify each candidate

Confirm:
- Public hiring signal (open roles, headcount growth, recent funding)
- Right size (matches Q1)
- Right geography
- Not on the exclude list (Q4)
- Real company (use `Exa:web_fetch_exa` on the homepage to confirm)

### 3c — Score and rank

Use the rubric in `references/dream-100-criteria.md` (0-10). Keep top 100 by score. Drop anything below 6/10 — replace with next-best.

If the niche genuinely doesn't support 100 strong candidates, deliver what you have honestly (e.g. 70) and flag it in the brief. Don't pad.

---

## Phase 4 — Find decision-makers

For each of the 100 companies, find **3 decision-makers**. Target ~300 total contacts.

### 4a — Title selection by company size

- **<50 employees** — Founder, CEO, MD, Head of People (if any)
- **50-500** — Head of Talent, Talent Acquisition Lead, HR Director, CPO, plus the relevant functional VP (e.g. VP Engineering for tech recruiters)
- **500+** — Functional VP for the agency's niche, Head of Talent for that function, Talent Acquisition Partner

### 4b — Find LinkedIn URLs via Exa

For each contact, run `Exa:web_search_exa` with queries like:

```
"site:linkedin.com/in [Company Name] [Title]"
"[Company Name] Head of Talent linkedin"
"[Company Name] CEO founder linkedin"
```

Exa returns LinkedIn profile URLs with name + title context. Verify the result actually works at the company before adding to the list.

For each contact, capture:
- First name (split from full name)
- Last name
- Job title (exact, from LinkedIn)
- LinkedIn URL
- Company name (matches Sheet 1)

**Do not invent names.** If you can't find 3 real decision-makers for a company, find 2. If you can only find 1, the company score should reflect that — consider replacing it.

### 4c — Quality check

Before adding a contact:
- LinkedIn URL must be `linkedin.com/in/...` format (not `/company/`, not search results)
- Name must be a real person, not a placeholder
- Title must match a decision-maker role (not "Intern", not "Analyst")

---

## Phase 5 — Build Lemlist-ready output

### 5a — Build the xlsx

Use the xlsx skill at `/mnt/skills/public/xlsx/SKILL.md`. Read that SKILL.md first.

**Two sheets:**

#### Sheet 1: "Companies" (100 rows)

| Column | Content |
|---|---|
| Rank | 1-100, by fit score |
| Company | Name |
| Website | Homepage URL |
| Vacancies Page | Careers/jobs URL |
| LinkedIn | Company LinkedIn URL |
| Industry | Sub-sector |
| HQ Location | City, country |
| Headcount | Approx, with growth note (e.g. "120 (+40% in 18mo)") |
| Hiring Signal | Specific evidence + source |
| Why They Fit | 1-2 sentences, agency-specific |
| Fit Score | 1-10 |
| Category | "Exclusive-prone" / "Multi-agency" / "Doesn't use agencies" |
| Notes | Watch-outs, competitor info |
| Status | Blank — agency fills in during outreach |

#### Sheet 2: "Contacts" (~300 rows, Lemlist-ready)

Use these **exact column names** (camelCase, no spaces) — they match Lemlist import conventions and become available as `{{variables}}` in Lemlist templates:

| Column | Content |
|---|---|
| firstName | First name |
| lastName | Last name |
| jobTitle | Exact title from LinkedIn |
| linkedinUrl | Full LinkedIn profile URL |
| companyName | Must match Sheet 1 exactly |
| companyDomain | Just the domain, e.g. `ronaldjames.co.uk` (no https://) |
| companyHiringSignal | The specific growth/hiring signal — usable in cold email openers |
| whyTheyFit | The agency-specific reason — usable for personalization |
| vacanciesPage | URL — useful reference for the SDR |
| dmPriority | 1 = primary target, 2 = backup, 3 = alt |

Leave `email` and `phone` columns OUT — Lemlist will enrich those at import.

**Formatting:**
- Header row bold, frozen pane on row 1
- Auto-width columns
- Hyperlinks live
- Sort Companies by Rank ascending
- Sort Contacts by companyName alphabetical, then dmPriority
- Keep column names camelCase exactly — Lemlist matching is case-sensitive

### 5b — Brief (markdown, in chat)

Under 250 words:

```
Dream 100 list built for [Agency Name] — [N] companies, [M] contacts.

Profile locked: [niche, roles, seniority, geography, ideal client size]

Top 5 picks and why:
1. [Company] — [one-line specific reason]
2. ...

Patterns: [e.g. "Heavy concentration in post-Series B fintech in London"]
Lookalikes from your best clients ([client names from Q3]): [N] companies

Watch-outs: [e.g. "3 companies had recent layoffs — verify before outreach"]

Lemlist import: Sheet 2 ("Contacts") is formatted for direct CSV/XLSX import. Lemlist will enrich emails and phones. The camelCase column names map to {{firstName}}, {{companyHiringSignal}}, etc. in your templates.

Next steps:
1. Review the spreadsheet, mark priorities in the Status column
2. Import Sheet 2 into Lemlist for email/phone enrichment
3. Run lumpy-letter campaign on Rank 1-20 in parallel
4. Use the Dream 100 cadence: letter → call → loom → LinkedIn → value brochure
```

---

## Quality bar before delivering

- [ ] 100 companies (or fewer with honest explanation)
- [ ] ~300 contacts (3 per company where possible, never fewer than 2 per company)
- [ ] Every row has real URLs — Website, LinkedIn, vacancies page
- [ ] Every contact LinkedIn URL is `linkedin.com/in/...` format
- [ ] Contacts sheet uses Lemlist column names (camelCase, exact)
- [ ] No duplicates
- [ ] No invented people, companies, or URLs
- [ ] Sorted by fit score
- [ ] Brief flags watch-outs honestly

---

## What NOT to do

- **Don't invent contacts.** Every name + LinkedIn URL must be verifiable.
- **Don't enrich emails/phones.** Lemlist does that downstream. Leave those columns out.
- **Don't skip the interview.** A 60-second interview saves a bad list.
- **Don't pad** to hit 100. Honest 70 beats sloppy 100.
- **Don't use camelCase wrong.** Lemlist column names are case-sensitive. `firstName` not `FirstName` or `first_name`.
- **Don't use this skill for non-recruitment agencies.**
