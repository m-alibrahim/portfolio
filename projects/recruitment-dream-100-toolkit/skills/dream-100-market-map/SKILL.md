---
name: dream-100-market-map
description: Build a Dream 100 market map for a recruitment agency — a target client list of 100 companies (the "who" of the Dream 100, no contacts yet). Use this skill whenever the user provides a recruitment agency's domain, LinkedIn, or website copy and asks to find ideal target clients, prospects, dream clients, target companies, or build a Dream 100 / D100 / target list. Also use when the user asks "who should we recruit for," "find me companies hiring in X," or wants a prospecting list for a recruitment / staffing / executive search / talent agency. The skill conducts a short interview to lock the ideal client profile, then uses web search + Exa to source 100 target companies with hiring signals and a specific live role (leadTitle) per company. Output is a Companies-only xlsx — decision-makers + LinkedIn URLs are found in a SEPARATE chat using the dream-100-contact-finder skill (this two-step split avoids context exhaustion). This skill is specific to RECRUITMENT agencies — do not use for other agency types.
---

# Dream 100 Market Map

Builds a 100-company Dream 100 market map for a recruitment agency — the strategic identification phase. Produces 100 target companies with hiring signals and one specific live role (`leadTitle`) per company.

**Two-skill chain:**
- **`dream-100-market-map` (this skill)** = WHO to target (the 100 companies)
- **`dream-100-contact-finder` (next, fresh chat)** = decision-makers per company with LinkedIn URLs
- **`dream-100-outreach`** = HOW to reach each prospect (11 assets per DM)

Run this skill, deliver the xlsx, then start a NEW chat with the xlsx as input to run `dream-100-contact-finder`. The split keeps each chat well within context limits.

Based on Chet Holmes' Dream 100 framework adapted for recruitment. Win 10-20 of these and the agency hits seven figures.

## Workflow

```
Phase 1: AUTO-PROFILE   → Fetch site/LinkedIn, extract what you can
Phase 2: INTERVIEW      → Confirm findings + ask thoughtful gap questions
Phase 3: RESEARCH       → Source 100 companies (web_search + Exa)
Phase 4: DELIVER        → Build Companies xlsx + brief, hand off to contact-finder
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

### 3c — Capture leadTitle per company

For each company that passes verification, fetch the careers page (`/careers`, `/jobs`, `/work-with-us`, etc.) and identify ONE specific currently-open role that matches the agency's niche.

This becomes the `leadTitle` for the company — every contact at that company shares the same `leadTitle`. The outreach skill uses it to drop a specific live job into the message ("Saw your [leadTitle] advertised").

If a company has no matching open role on the careers page, mark `leadTitle` as the closest equivalent role they have hired for historically (visible from LinkedIn) or leave blank and note in the Notes column. A blank leadTitle weakens outreach — consider dropping the company if the niche match is otherwise borderline.

### 3d — Score and rank

Use the rubric in `references/dream-100-criteria.md` (0-10). Keep top 100 by score. Drop anything below 6/10 — replace with next-best.

If the niche genuinely doesn't support 100 strong candidates, deliver what you have honestly (e.g. 70) and flag it in the brief. Don't pad.

---

## Phase 4 — Deliver

### 4a — Build the xlsx (Companies sheet only)

Use the xlsx skill at `/mnt/skills/public/xlsx/SKILL.md`. Read that SKILL.md first.

**One sheet: "Companies"** (100 rows)

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
| leadTitle | A specific currently-open role at this company that matches the agency's niche (e.g. "Senior Backend Engineer"). Fetched from the careers page. Used downstream by `dream-100-outreach`. |
| Notes | Watch-outs, competitor info |
| Status | Blank — agency fills in during outreach |

**Formatting:**
- Header row bold, frozen pane on row 1
- Auto-width columns
- Hyperlinks live
- Sort by Rank ascending

### 4b — Save the agency profile

In a second sheet called "AgencyProfile", save the key facts captured in Phases 1-2 so the next skill can read them without re-interviewing:

| Field | Value |
|---|---|
| agencyName | |
| agencyDomain | |
| niche | |
| rolesFilled | |
| seniority | |
| geography | |
| idealClientSize | (Startup / Scale-up / Mid-market / Enterprise / Mix) |
| feeModel | (perm / contract / retained / contingent) |
| recentPlacements | 2-3 named clients + role titles, if known |
| excludeList | from Q4 |

This sheet is small but invaluable — the contact-finder reads it to pick the right decision-maker titles and avoid re-asking the user.

### 4c — Brief (markdown, in chat)

Under 200 words:

```
Dream 100 market map built for [Agency Name] — [N] companies.

Profile locked: [niche, roles, seniority, geography, ideal client size]

Top 5 picks and why:
1. [Company] — [one-line specific reason]
2. ...

Patterns: [e.g. "Heavy concentration in post-Series B fintech in London"]
Lookalikes from your best clients ([client names from Q3]): [N] companies

Watch-outs: [e.g. "3 companies had recent layoffs — verify before outreach"]

Next step — find the contacts:
Start a NEW chat and run the `dream-100-contact-finder` skill with this xlsx as input. It will find 3 decision-makers per company and produce the Lemlist-ready Contacts sheet. Running it in a fresh chat keeps context clean.

Or do it in this chat if you prefer (heavier on context).
```

---

## Quality bar before delivering

- [ ] 100 companies (or fewer with honest explanation)
- [ ] Every row has real URLs — Website, LinkedIn, vacancies page
- [ ] Every row has a `leadTitle` (the specific live role) or a clear blank with a note
- [ ] No duplicates
- [ ] No invented companies
- [ ] Sorted by fit score
- [ ] AgencyProfile sheet populated for handoff
- [ ] Brief flags watch-outs honestly and points to the next skill


---

## What NOT to do

- **Don't try to find decision-makers in this skill.** That's the `dream-100-contact-finder` skill, run in a fresh chat. Adding 300 LinkedIn searches here blows the context budget.
- **Don't invent companies.** Every entry must trace to a real source.
- **Don't skip the interview.** A 60-second interview saves a bad list.
- **Don't pad** to hit 100. Honest 70 beats sloppy 100.
- **Don't skip the AgencyProfile sheet.** The next skill needs it.
- **Don't use this skill for non-recruitment agencies.**
