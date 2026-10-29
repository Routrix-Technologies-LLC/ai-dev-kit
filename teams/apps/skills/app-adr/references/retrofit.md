# app-adr: retrofit mode

Loaded when the argument is `retrofit <path-or-topic>`. Retrofit brings a decision that already exists into the ADR format without altering anything that is already there. It covers three starting points.

| Starting point | Example | Handling |
|---|---|---|
| An ADR file missing template sections | An ADR with no Status or no dependencies | Append only the absent sections to that file |
| A decision recorded elsewhere | A README paragraph, a `docs/decisions.md` entry, a design doc, a wiki page | Create a new ADR from it; leave the source untouched and link it in Related |
| A decision visible only in code or config | "We use a local SQLite file", "the app talks to the API through a message bus" | Create a new ADR from code evidence and the user's account; mark what is reconstructed |

## Steps

1. **Resolve and read.** For a path, read the whole file in ranges by heading (Grep `^#` first) if it is large. For a topic, find the evidence (Grep, manifests, config, existing docs) and list it with paths. Never proceed on a topic with no evidence and no user account.

2. **Present present and missing** before changing anything:

```
Retrofit: <title>   Source: <path or evidence list>
Will not be touched (already present):
  Status: <current value or MISSING>
  <section>: present
Missing, to be added:
  Status                     BLOCKING   later skills cannot tell if it is accepted
  ADR Dependencies           HIGH       dependency order and acceptance checks break
  Platform and Version Risk  HIGH       version risk unknown
  Requirements Addressed     MEDIUM     traceability lost
  Date (and no Last Verified) MEDIUM    stories cannot detect change
```

3. **Ask once**: "Add the N missing sections? I will not modify any existing content." If no, write nothing and list the gaps by name. For a decision recorded elsewhere or in code, the ask names the new file and its number (numbering as in new mode: scan, next number, never reuse).

4. **Fill each missing section from the right source**, asking only what the evidence cannot answer:
   - Status: ask "What is the status of this decision?" Options: Proposed, Accepted, Deprecated, Superseded by ADR-NNNN. An answer of Accepted (a decision already in force) is **written as Proposed**; after the sections are added, run accept mode (`references/accept.md`) on this ADR. Its dependency check, completeness check, story list and explicit yes all apply; retrofit never sets `Accepted` itself.
   - ADR Dependencies: ask which ADRs it depends on, enables and blocks. Accept "None" only as the user's explicit statement; if the user is unsure, the section is written as `UNKNOWN - not established at retrofit` and accept mode will refuse until it is resolved.
   - Platform and Version Risk: read the pinned versions from manifests, lock files and `docs/stack-reference.md`; verify claims from official documentation; anything unchecked is `UNVERIFIED`.
   - Requirements Addressed: ask which specs or requirement IDs motivated the decision; "unknown" is a legal answer and is written as such.
   - Decision, Options Considered, Consequences, Context for a decision found only in code or elsewhere: draft from the evidence and the user's account. Where the reasoning was never recorded, write `RATIONALE UNKNOWN - original reasoning not recorded` and ask the user whether they remember it. Never invent alternatives that were not actually considered; list alternatives the user names as "considered (reported by <user>, not documented)" or leave the section noting none were recorded.
   - Date: append `## Date` with today's date and say it records the retrofit, not when the decision was made. Add the original decision date as a separate line only if the user or the sources supply it.

5. **Mark provenance.** For decisions reconstructed from code or documents, add a line at the top of Context: `Retrofitted on <date> from <sources>. Reasoning marked UNKNOWN was not recorded.`

6. **Append with Edit** (include the new section heading in the matched text). Do not reorder, reword or delete existing sections. A heading that exists but is empty counts as present and is reported as empty, not filled silently; ask the user whether to fill it.

7. **Gate and close.** `TD-ADR` follows the same rules as new mode (full review mode only; otherwise print `TD-ADR skipped: <mode> mode`) and is passed the retrofit evidence. Re-read the file; confirm each added section is non-empty. Suggest `/app-adr accept <id>` when the decision is settled, `/app-architecture adr-audit` to re-check coverage.

Verdict: COMPLETE when the agreed sections were appended and verified; NOT ASSESSED when `TD-ADR` could not assess and the input was not supplied; BLOCKED when the evidence is missing, the number is ambiguous or the user declined to say anything about a BLOCKING section.
