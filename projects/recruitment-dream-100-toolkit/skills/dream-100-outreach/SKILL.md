---
name: dream-100-outreach
description: Generate the full Dream 100 outreach asset stack for a single recruitment-agency prospect — lumpy letter, follow-up call script, Loom email + video script, LinkedIn connection note + opening message, LinkedIn selfie video script, voice note script, value brochure concept, candidate spec-in message, and social engagement comments. Use this skill whenever a recruitment agency wants to reach out to a Dream 100 prospect, when the user mentions "Dream 100 outreach", "lumpy letter", "Loom for a prospect", "LinkedIn message for a client", or asks for personalized multi-channel cold outreach for a specific company/decision-maker. Pairs with the dream-100-market-map skill — runs AFTER the market map is built, on one prospect at a time for deep personalization. Output is a markdown file of copy-ready assets. Recruitment agencies only — not general B2B sales outreach.
---

# Dream 100 Outreach Generator

Produces the full Dream 100 multi-channel outreach asset stack for a single prospect, deeply personalized. The user copies each asset and sends it via the right channel on the Dream 100 calendar cadence.

Pairs with `dream-100-market-map`:
- **Market Map** = WHO to target (the 100 companies + contacts)
- **Outreach** = HOW to reach them (the 11 assets per prospect, this skill)

Based on Chet Holmes' Dream 100 framework adapted for recruitment.

## Workflow

```
Phase 1: INPUT          → Capture prospect + DM + agency context
Phase 2: RESEARCH       → Find personalization hooks (company + DM)
Phase 3: HOOK           → Synthesize ONE core angle to anchor every asset
Phase 4: GENERATE       → Produce 11 assets, all using the hook
Phase 5: DELIVER        → Single markdown file, copy-ready
```

---

## Phase 1 — Input

Accept any of these:

**Prospect side (required):**
- Company name + domain
- Decision-maker: full name, title, LinkedIn URL
- `leadTitle` — a specific role currently open at the prospect's company that matches the agency's niche (from the Market Map's Contacts sheet, or fetch from their careers page)

**Agency side (required — drives the proven copy patterns):**
- Agency name
- **Niche** — the role types they fill (e.g. "senior backend engineers", "CFOs", "registered nurses")
- **Location** — geography they serve (e.g. "London", "the Northeast UK", "Texas")
- **Recent placements** — 2-3 specific named clients they've recently placed with (drops social proof in every asset)
- **Recent role titles placed** — e.g. "Senior Rust Engineers", "Head of Finance, FP&A Director"

**Per-campaign (optional but recommended — unlocks the strongest hook):**
- `leadCandidate` — one-line USP of a candidate the agency is currently shopping. Example: "ex-Stripe Senior Engineer with 7 years Rust experience" or "FP&A Director who scaled finance teams 3 → 15 at two Series B SaaS companies"

If `leadCandidate` is provided, the candidate spec-in becomes the central angle across all assets. If not provided, the skill defaults to a value-asset angle (salary guide, market report) instead.

If the user just pastes a row from the Market Map xlsx, parse the columns: `companyName`, `firstName`, `lastName`, `jobTitle`, `linkedinUrl`, `companyDomain`, `companyHiringSignal`, `whyTheyFit`, `leadTitle`.

If agency context is missing, ask **one** consolidated question covering all 5 agency fields above. Don't pepper the user with separate questions.

If the prospect is missing critical fields (no name, no DM, no LinkedIn URL), stop and ask for them.

---

## Phase 2 — Research personalization hooks

This phase is the highest-leverage step. Generic outreach fails. Specific outreach books meetings.

Read `references/personalization-research.md` for queries. Run searches in parallel using `web_search` and `Exa:web_search_exa` (load Exa via `tool_search` if needed).

Find:

### Company hooks
- Recent funding rounds, M&A, expansion announcements
- New office openings
- Recent leadership hires
- Headcount growth signal
- Open roles matching the agency's niche (visit careers page via `web_fetch`)
- Recent press coverage
- Awards / industry list inclusions

### Decision-maker hooks
- Recent LinkedIn posts (search `[Name] linkedin post` via Exa)
- Articles they've authored or commented on
- Recent job change (joined the company in last 12 months?)
- Public talks, podcasts, panels
- Previous company connections
- Shared connections / alumni networks

### Triangulation
- Is the DM hiring NOW? (cross-check open roles + their team area)
- Is the company in a "they need to hire fast" moment? (post-funding, post-expansion)
- Is there a candidate angle? (e.g. "we placed a Senior Engineer at [similar company] last month")

Capture 3-5 specific facts. Cite the source URL for each so the user can verify.

---

## Phase 3 — Synthesize the hook

Pick ONE core angle that anchors every asset. The hook should answer:

> Why am I reaching out to THIS person at THIS company RIGHT NOW?

A strong hook combines:
- **A specific trigger** (they just raised £20M / they opened a Berlin office / they're hiring 15 engineers)
- **A specific value** (we placed 3 senior Rust engineers at similar-stage fintechs in Q1)
- **A specific ask** (a 10-min call, look at a candidate, accept a salary guide)

**Weak hook:** "We help SaaS companies hire."
**Strong hook:** "I saw you just opened your Berlin office and are hiring 4 senior backend engineers — we placed 3 senior Rust engineers at Series B fintechs in Berlin last quarter. Would you take 10 mins to see two of them?"

Lock the hook before generating assets. Every asset re-frames the same hook in different formats. Consistency across channels makes the outreach feel intentional, not spammy.

---

## Phase 4 — Generate the 11 assets

Read `references/touchpoint-templates.md` for proven templates and length limits for each asset.

Produce these in order. Each gets its own clear section in the output file.

**Sequence on the Dream 100 calendar (FYI for the user, not for asset generation):**

| Week | Touchpoint |
|---|---|
| 1 (Mon) | Lumpy letter posted |
| 1 (Thu) | Follow-up call |
| 2 | Loom email |
| 3 | LinkedIn connection request |
| 4 | LinkedIn opening message |
| 5 | LinkedIn selfie video |
| 6 | Voice note DM |
| 8 | Value brochure sent |
| 10 | Candidate spec-in |
| Ongoing | Social engagement (weekly) |

### The 11 assets

1. **Lumpy letter** — physical mail, ~150-200 words, references the gift book, sets up the Thursday call
2. **Follow-up call script** — ~100 words of bullet points / talking flow for a 2-3 min call
3. **Loom email** — subject line + ~50-80 word email pitching the Loom
4. **Loom video script (90 sec)** — bullet-point talking script: hook, body, CTA
5. **LinkedIn connection note** — under 300 characters (LinkedIn's hard limit)
6. **LinkedIn opening message** — first message after they connect, ~75 words
7. **LinkedIn selfie video script (60 sec)** — bullet points for a vertical selfie video
8. **Voice note script (60-90 sec)** — bullet points for a voice note DM
9. **Value brochure concept** — topic + 5-7 section bullet outline (the agency turns this into a PDF in Canva later)
10. **Candidate spec-in message** — "I have a candidate" angle for when the agency has a real candidate
11. **Social engagement starter pack** — 3 sample comments to leave on the DM's recent LinkedIn posts

Each asset must:
- Use the hook from Phase 3
- Name the DM by first name
- Reference a specific company fact (no "I love what you're doing")
- Have a single clear CTA
- Pass the "would I find this annoying as the recipient" test

---

## Phase 5 — Deliver

Output as a single markdown file: `dream-100-outreach-[FirstName]-[Company].md`

### File structure

```markdown
# Dream 100 Outreach Pack — [DM First Name] [Last Name] @ [Company]

**Prospect:** [Name], [Title]
**Company:** [Company] ([domain])
**LinkedIn:** [URL]
**Date prepared:** [today]

## The Hook
[The single anchor angle, 2-3 sentences]

## Research notes (sources for personalization)
- [Fact 1] — source: [URL]
- [Fact 2] — source: [URL]
- [Fact 3] — source: [URL]

---

## 1. Lumpy Letter
**When:** Post on Monday. Handwrite the envelope. Include a book (e.g. The Ultimate Sales Machine, Shoe Dog, Built to Sell).
**Marking:** "Private and Confidential" on envelope.

```
[Full letter text here, ready to copy]
```

---

## 2. Follow-up Call Script
**When:** Thursday or Friday of the same week the letter arrives.
**Format:** Casual phone call, 2-3 mins max.

[Bullet talking points]

---

[... and so on for all 11 assets ...]

---

## Cadence reminder
[Insert the 10-week cadence table from Phase 4]

## Notes for the agency
[Anything specific — e.g. "Sarah just joined 3 months ago, lead with congrats" or "Company had layoffs in May — avoid headcount-growth angles"]
```

Save the file to the outputs folder, then call `present_files` so the user can download it.

After delivery, in chat, give a 3-line summary:
- The hook in one sentence
- The top 2-3 facts found
- Which asset to send first (usually the lumpy letter)

Keep the chat reply under 100 words. The file is the deliverable.

---

## Quality bar before delivering

- [ ] Every asset uses the hook
- [ ] No generic language ("I came across your profile", "I love what you're doing", "synergies", "circle back")
- [ ] DM's first name used in every asset
- [ ] Each asset has a specific, single CTA
- [ ] All factual claims are sourced (in the Research notes section)
- [ ] Length limits respected (LinkedIn connection note <300 chars; lumpy letter ~150-200 words; videos 60-90 sec talking points)
- [ ] The voice matches the agency's tone (warm-professional for most recruiters; adjust if agency is more casual)

---

## What NOT to do

- **Don't invent facts.** If you can't find a specific hook, ask the user if they have inside info before falling back to generic.
- **Don't write all 11 the same.** Each channel has its own format and brevity rules.
- **Don't apologize or hedge** ("Sorry to bother you", "I know you're busy"). Cold outreach with hedging looks weak. Be direct and respectful.
- **Don't pitch a meeting in every asset.** The Dream 100 goal is to get the prospect to RAISE THEIR HAND — sometimes that's "accept a free salary guide", sometimes that's "look at a candidate's profile". Vary the asks.
- **Don't use this skill for non-recruitment outreach.** Templates and angles are recruitment-specific.
