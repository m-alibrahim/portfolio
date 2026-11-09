# Research Playbook

Specific search strategies for finding Dream 100 candidates. Run these in parallel.

## Step 1 — Lock the agency profile

Fetch the agency's site. Look for:
- Homepage hero + "About" page → niche & positioning
- "Sectors" / "Industries" / "Specialisms" page → exact verticals
- "Roles" / "Jobs" page → titles they fill
- Case studies / clients page → existing client patterns (mimic these)
- Footer / contact page → geography
- Team page → size of agency (informs how ambitious to be with prospect size)

If website is sparse, also fetch their LinkedIn company page.

## Step 2 — Source company candidates

Use both `web_search` and `Exa:web_search_exa` (call `tool_search` first to load Exa). Each is better at different things:

- **`web_search`** — recent news, specific facts, dated information, fast-changing data
- **`Exa:web_search_exa`** — semantic queries, "find me companies like X", curated lists, longer-tail discovery

Run searches in parallel where possible. Tailor every query to the agency's niche + geography.

### Funding / growth lists
- `"Series A" [niche] [geography] 2025` (and 2026)
- `"Series B" [niche] [geography] 2026`
- `[geography] [niche] startups raised 2026`
- `fastest growing [niche] companies [geography] 2026`

### Industry rankings
- `top [niche] companies [geography] 2026`
- `[geography] "hot 100" [niche]`
- `Deloitte Fast 50 [geography]`
- `Inc 5000 [niche]` (US)
- `FT 1000 fastest growing [Europe/UK]`
- `[Local business journal] best places to work [year]`

### Hiring signal
- `[niche] companies hiring [role] [geography]`
- `[geography] tech companies expanding 2026`
- LinkedIn search: companies in [industry] in [location] with 50-500 employees

### Geographic / sector publications
For UK tech: TechRound, UKTN, Tech.eu, Sifted
For US tech: TechCrunch, Crunchbase News, regional business journals
For finance: eFinancialCareers, Financial News
For healthcare: Fierce Healthcare, regional health publications

Substitute the equivalent publications for the agency's niche.

## Step 3 — Verify each candidate

For each promising company, fetch or search:
1. Homepage — confirm what they do
2. Careers page — confirm open roles match agency's niche
3. LinkedIn company page — headcount, growth, recent posts
4. Recent news — funding, expansion, M&A, leadership changes

## Step 4 — Capture leadTitle per company

For each verified company, fetch the careers page (`/careers`, `/jobs`, `/work-with-us`, etc.) using `web_fetch` and identify ONE specific currently-open role that matches the agency's niche.

This becomes the `leadTitle` for the company. The downstream `dream-100-outreach` skill plugs it into messages ("Saw your [leadTitle] advertised").

If a company has no matching open role on the careers page, mark `leadTitle` as the closest equivalent role they have hired for historically (visible on LinkedIn) or leave blank with a note. A blank leadTitle weakens outreach — consider dropping the company if the niche match is otherwise borderline.

**Decision-makers are NOT found in this skill.** That's the `dream-100-contact-finder` skill, run in a fresh chat using the Companies xlsx as input.

## Step 5 — Cross-check before adding to list

Before a company makes the final list:
- It must have a real, verifiable Hiring Signal (link or source noted)
- It must pass the size/geography/exclude filters
- Score it against `dream-100-criteria.md` — drop anything below the threshold

## Tips

- **Start with funding databases for "hot" lists** — Crunchbase / TechCrunch announcements give you growing companies with budget by default
- **LinkedIn "People also viewed"** — for any prospect, similar companies often appear; check their pages too
- **The agency's existing clients are the template** — look at their case studies and find lookalike companies. If they placed for a 40-person fintech, find more 40-person fintechs.
- **Local matters** — recruitment is often regional. Don't suggest a New York company to a Manchester agency unless the agency does remote / international placement.

## Time-box research

Don't spiral. For a 100-company list, budget rough effort like this:
- Phase 1 (auto-profile): fast — fetch site + LinkedIn
- Phase 2 (interview): 4 questions max
- Phase 3a (source ~150 candidates): the bulk of the work — parallel searches
- Phase 3b-c (verify + find DMs): batch through systematically
- Phase 3d (score, drop to top 100): quick pass with the rubric
- Phase 4 (Clay enrichment + xlsx + brief): batched Clay calls + assembly

If you're hitting dead ends in a niche and can't find 100 qualified companies, deliver what you have (e.g. 70) and explain why — don't pad with bad fits.
