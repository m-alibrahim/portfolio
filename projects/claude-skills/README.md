# Claude Skills for Legal & BD Work

Three Claude skills I built and use in daily work at a Saudi law firm, shared as open source with all firm and client details removed.

| Skill | What it does |
|---|---|
| `proposal-methodology` | Turns a tender booklet (RFP/RFQ, Etimad or private) into a complete Arabic technical and financial proposal: requirement analysis, compliance matrix, pricing, a Word document, and a presentation in the bidder's brand. Includes Python helpers for branded DOCX/PPTX output. |
| `case-file-builder` | Turns rough notes from a first client call into (1) a client-facing intake file the client completes themselves, (2) a WhatsApp/email message to send it, and (3) an internal memo with an initial Saudi legal assessment for the legal team. Includes a Saudi legal reference (jurisdiction, limitation periods, evidence, data protection). |
| `redact-sensitive-info` | Permanently redacts client names, logos, commercial registration numbers, dates, people, amounts, and metadata from PDFs before sharing. Handles the garbled Arabic text extraction that breaks ordinary search-and-redact. |

## Install

- **Claude (web/desktop):** zip each skill folder and upload it under **Settings → Capabilities → Skills**.
- **Claude Code:** copy the folders into `~/.claude/skills/`.

## Example prompts

```
Use the proposal-methodology skill. Here is the tender booklet (attached).
We are <company name>; build the technical and financial proposal.
```

```
Use the case-file-builder skill. Call notes: <paste notes>.
```

```
Use the redact-sensitive-info skill on the attached PDF. Remove the client
name, logos, CR numbers, and all amounts before I share it.
```

## License

MIT
