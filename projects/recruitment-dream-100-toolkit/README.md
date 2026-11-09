# Recruitment Dream 100 Toolkit

An open-source, AI-assisted prospecting system for recruitment and staffing agencies. It turns an agency's website into a list of 100 target client companies, finds three decision-makers at each one, and produces personalized multichannel outreach for every prospect.

It is based on Chet Holmes' Dream 100 framework, adapted for recruitment and run as a chain of Claude skills.

> All examples are generic. No client data, names, or results from real engagements are included.

---

## What it produces

| Stage | Skill | Output |
|---|---|---|
| 1. Who to target | `dream-100-market-map` | 100 companies with hiring signals and one live role per company (xlsx) |
| 2. Who to contact | `dream-100-contact-finder` | ~300 decision-makers (3 per company) with LinkedIn URLs, Lemlist-ready (xlsx) |
| 3. How to reach them | `dream-100-outreach` | 11 assets per prospect: lumpy letter, call script, Loom email and script, LinkedIn note and message, video and voice-note scripts, value brochure concept, candidate spec-in, social comments |
| All-in-one (smaller runs) | `recruitment-dream-100` | Stages 1 and 2 in a single run |

## Workflow

```
Agency website / LinkedIn
        │
        ▼
[1] Interview: lock the ideal client profile (sectors, roles, size, region)
        │
        ▼
[2] Market map: source 100 companies with live hiring signals  ──► Companies.xlsx
        │   (new chat, to keep context clean)
        ▼
[3] Contact finder: 3 decision-makers per company + LinkedIn URLs ──► Contacts.xlsx
        │
        ▼
[4] Import to Lemlist: enrich emails and phones, build the sequence
        │
        ▼
[5] Outreach: run per prospect, generate the 11-asset stack, launch
```

Splitting stages 2 and 3 into separate chats is deliberate: each stage is research-heavy, and the split keeps every run within context limits.

## Tools to connect

| Tool | Used for | Required? |
|---|---|---|
| Claude (claude.ai or Claude Code) with skills enabled | Running the skills | Yes |
| Web search | Company discovery, hiring signals | Yes |
| [Exa](https://exa.ai) connector | Semantic company search and LinkedIn profile discovery | Strongly recommended |
| [Lemlist](https://lemlist.com) | Email/phone enrichment and sequencing | Recommended |
| Clay connector | Optional extra enrichment | Optional |
| Spreadsheet skill (xlsx) | Building the output files | Yes (built into Claude) |

## Installation

1. Download the `skills/` folder.
2. In Claude, go to **Settings → Capabilities → Skills** and upload each skill folder (zip each one), or place them in `~/.claude/skills/` for Claude Code.
3. Connect Exa (and optionally Lemlist and Clay) from the connectors menu.

## Ready-to-use prompts

**Stage 1: market map**
```
Use the dream-100-market-map skill. Our agency is <agency website>.
We place <roles> in <sectors> across <region>. Build our Dream 100.
```

**Stage 2: contact finder** (new chat, attach the Companies.xlsx from stage 1)
```
Use the dream-100-contact-finder skill on the attached Dream 100 companies file.
Find 3 decision-makers per company and make the file Lemlist-ready.
```

**Stage 3: outreach** (one prospect at a time)
```
Use the dream-100-outreach skill for <decision-maker name>, <title> at <company>.
Our agency: <agency website>. The live role we can fill: <role>.
```

## Guardrails built in

- No fabricated emails or phone numbers. Enrichment happens downstream in Lemlist.
- Contacts are verified against the company before they are added.
- Only public professional information is captured.
- Column names follow Lemlist's case-sensitive import conventions (`firstName`, `companyName`, ...).

## Folder structure

```
skills/
├── dream-100-market-map/       # Stage 1
├── dream-100-contact-finder/   # Stage 2
├── dream-100-outreach/         # Stage 3
└── recruitment-dream-100/      # Stages 1 and 2 combined
```

## License

MIT. Use it, adapt it, and build on it.

---

Built by [Mohammed Alibrahim](https://www.linkedin.com/in/mohammed-al-ibrahim-0b7192275/), Business Development.
