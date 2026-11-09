# Contact Search Query Patterns

Proven Exa query patterns for finding decision-maker LinkedIn URLs. Use `Exa:web_search_exa` (load via `tool_search` if needed) — Exa is better for LinkedIn discovery than plain web_search because it indexes professional content semantically.

---

## Core query patterns

For each company + target title, run one of these:

```
[Company Name] [Title] linkedin
[Company Name] [Title]
site:linkedin.com/in [Company Name] [Title]
```

The third pattern (`site:linkedin.com/in`) often returns the cleanest LinkedIn-only results.

---

## Title-specific query examples

### Founder/CEO at startups
```
[Company] founder linkedin
[Company] CEO linkedin
[Company] co-founder linkedin
```

### Head of Talent / TA Lead
```
[Company] Head of Talent linkedin
[Company] "Talent Acquisition" linkedin
[Company] TA lead linkedin
```

### HR / People
```
[Company] HR Director linkedin
[Company] "People Operations" linkedin
[Company] "Head of People" linkedin
[Company] CPO linkedin   (chief people officer)
```

### Functional VPs (tech recruiter examples)
```
[Company] "VP Engineering" linkedin
[Company] "Head of Engineering" linkedin
[Company] CTO linkedin
```

### Functional VPs (finance recruiter examples)
```
[Company] "VP Finance" linkedin
[Company] CFO linkedin
[Company] "Finance Director" linkedin
```

### Director-level (for enterprise companies)
```
[Company] "Director of [function]" linkedin
[Company] "Senior Director" [function] linkedin
```

---

## Reading Exa results

Exa returns snippets that look like:
```
Title: Sarah Chen - VP of Engineering at Acme Inc | LinkedIn
URL: https://linkedin.com/in/sarah-chen-eng
Snippet: VP of Engineering at Acme Inc. Previously Senior Eng Manager at...
```

Extract:
- **firstName + lastName** from the title or snippet — split carefully (handle middle initials, hyphens, particles like "van", "de")
- **jobTitle** — exact title as shown (including the company qualifier)
- **linkedinUrl** — the URL from the result; must contain `linkedin.com/in/`
- **companyName** — verify the snippet confirms they currently work at the target company

---

## Verification before adding to the list

Reject the result if any of these are true:

❌ URL is `linkedin.com/company/...` (that's a company page, not a person)
❌ URL is a Google search results page or LinkedIn search page
❌ Snippet says "Former [Company]" or "ex-[Company]" — they've left
❌ Snippet says "Founder at [Different Company]" — wrong person
❌ Title is "Intern", "Associate", "Analyst", "Trainee" — too junior
❌ Title is "Office Manager", "EA", "Receptionist" — wrong function

Accept if:
✅ URL is `linkedin.com/in/[anything]`
✅ Snippet confirms current employment at target company
✅ Title matches a decision-maker role per `dm-title-selection.md`

---

## Handling ambiguous results

**Problem 1: Two people with the same title at the company**
Pick the more senior or longer-tenured one based on the snippet. If still tied, include both — agency can choose.

**Problem 2: Result mentions company in their past, not current role**
Skip. Look for "currently at" / "VP of X at Y" present-tense.

**Problem 3: Title format varies (e.g. "Senior VP Engineering" vs "VP, Engineering" vs "VP Engineering")**
All acceptable. Capture the exact phrasing from LinkedIn.

**Problem 4: Person works at parent company, not the target subsidiary**
Note in the row — they may still be the right contact, but flag it.

---

## When searches dry up for a company

If after 3-4 query variations you can't find 3 DMs, fall back in this order:

1. Try the company's LinkedIn company page → "People" section (via search: `[Company] people linkedin`)
2. Search for "Head of [function]" or "Director of [function]" instead of VP-level
3. Try the parent company if the target is a subsidiary
4. Accept 2 DMs and note the gap in the row's `notes` column

**Do not invent.** A blank cell with a "Only 2 DMs found" note is far more valuable than fabricated names that bounce or embarrass the agency.

---

## Batching efficiency

Process companies in batches of 20:

1. Batch 1 (companies 1-20): Run all searches, build all rows
2. Save partial xlsx to a working file
3. Batch 2 (companies 21-40): Repeat
4. ...etc.

If a batch hits unexpected issues (slow searches, ambiguous results), pause and update the user — don't grind silently.

---

## Time and search budget

For 100 companies × 3 DMs = 300 contacts, expect:
- ~3-5 Exa searches per company on average (some need more)
- 300-500 total Exa calls
- Process in 5 batches of 20

If you hit token/context limits mid-run, **deliver what you have with the coverage stats** rather than failing silently. The user can re-run for the remaining companies in a new chat.
