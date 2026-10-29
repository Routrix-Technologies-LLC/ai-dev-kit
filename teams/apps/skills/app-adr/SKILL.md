---
name: app-adr
description: "Record an architecture decision as an ADR (new), turn an existing undocumented decision into one (retrofit), or move a Proposed ADR to Accepted (accept, the only route, after the user's explicit yes). Use when the user makes or has made a technical decision worth recording, says 'write an ADR', 'document why we chose X', 'accept ADR-0007', or a story is blocked waiting on a decision."
argument-hint: "[app] <title> | retrofit <path-or-topic> | accept <ADR-id> [--review solo|lean|full]"
user-invocable: true
---

# App ADR

Writes and manages Architecture Decision Records in three modes. **new** guides a decision and writes an ADR with status `Proposed`. **retrofit** brings a decision that already exists in code, a document or someone's head into the ADR format without rewriting what is there. **accept** is the only route in the studio that sets `Accepted`; it needs the user's explicit yes, shows the stories it unblocks before asking, and refuses if a dependency ADR is not Accepted.

Writes: `docs/architecture/adr/ADR-NNNN-<slug>.md` (template `templates/adr.md`), story status lines in accept mode, `.studio/state.md` checkpoint. At minimal rigor, decisions go to `docs/decisions.md` instead (see Rigor).
Next: `/app-adr accept` when settled, then `/app-plan` (stories read Accepted ADRs), `/app-architecture` (required-ADR list), `/app-gate`.

## When to use and when not to

- Use for a decision that is costly to reverse, crosses components, constrains later work or will be asked about in a year: framework, data store, sync strategy, auth model, module boundary, hosting, distribution path.
- Not for choosing or pinning the whole stack or adopting a dependency (`/app-stack`, which hands an ADR draft here), not for the system overview (`/app-architecture`), not for contract design (`/app-api`), not for small reversible choices (a line in `docs/decisions.md`).

## Mode detection

| Argument | Mode | Detail |
|---|---|---|
| `<title>` | new | Phases N1 to N6 below |
| `retrofit <path>` or `retrofit <topic>` | retrofit | Read `references/retrofit.md` now and follow it. Read it again if the conversation was compacted |
| `accept <ADR-id>` | accept | Read `references/accept.md` now and follow it. Read it again if the conversation was compacted |
| nothing | ask | "What decision are you documenting?" Use the answer as the title |

Resolve the app and print the plan block first (`orchestration.md` sections 1 and 2). If `modes.rigor` is minimal and the user did not insist on an ADR, offer a `docs/decisions.md` entry (date, decision, why, alternatives in a line each, revisit trigger) and write that instead; the ADR path stays available on request.

## Inputs

| Input | If missing |
|---|---|
| `studio.yaml` | Stop; offer `/app-adopt` or `/app-start`. |
| `docs/architecture/architecture.md` | Not blocking; the ADR's context is gathered from the user and specs. Recommend `/app-architecture` afterward. |
| `docs/stack-reference.md` | The platform and version risk section is filled only from sources checked this run (WebSearch or WebFetch on official documentation, lock files, manifests); otherwise it says `UNVERIFIED` and names what to verify. Never filled from memory. |
| Existing ADRs | Needed for numbering, conflicts and dependencies. None existing is fine; the first number is 0001. |

## New mode

### Phase N1: Number and conflicts

1. List `docs/architecture/adr/` (or `paths.adr` if the app maps it elsewhere; an adopted app may use a different pattern, in which case follow the app's pattern and say so). Next number is the highest existing plus one, four digits. Numbers are never reused or renumbered, even for withdrawn ADRs. If two files share a number, stop and report it.
2. Read the Status and Summary of every existing ADR (Grep for `^## Status` and the line after it, and the Summary section) to find ADRs in the same area. If a **Accepted** ADR already decides this, the new ADR is either a supersession (the old one will be marked `Superseded by ADR-NNNN` only when this one is accepted) or an exception with a stated scope. Ask which. A silent conflict is not allowed: the decision cannot proceed until the user resolves it.

Check: the next number is printed with the count of ADRs scanned; any conflicts are listed or "0 conflicts in N ADRs".

### Phase N2: Context

Main session reads: the architecture document sections relevant to the decision, the specs and requirement IDs that motivate it, the threat model if the decision touches trust, `docs/stack-reference.md`, and `docs/decisions.md` for earlier related choices.

### Phase N3: Assumptions and analysis

1. Derive and show, then ask to confirm or change (one ask): the problem in one sentence; the decision drivers (requirements, budgets, constraints); two to four real alternatives plus "do nothing or defer" where that is viable; dependencies on other ADRs; requirements addressed; status `Proposed` (never asked).
   - **Dependencies the scan cannot establish are shown as `UNKNOWN - please confirm`, never as `None`.** `None` asserts that nothing upstream constrains this decision; an unexamined list must not look like an examined one. UNKNOWN is resolved in this prompt and is never written to the file.
2. Spawn the owning lead for the analysis (one call, or several in parallel when the decision spans areas):

| Decision area | Agent |
|---|---|
| Browser client | `web-lead` |
| Desktop app | `desktop-lead` |
| Phone or tablet app | `mobile-lead` |
| Services, APIs, data | `backend-lead` |
| Build, hosting, environments, observability | `platform-lead` |
| Trust, auth, secrets, privacy impact | `security-lead` |
| Module structure, code-level pattern, language | `principal-engineer` |

   Brief per `orchestration.md` section 3 with the confirmed assumptions. Output `~/AgentScratch/app-adr-<slug>/<agent>.md`: for each alternative, how it satisfies each driver, cost and risk, reversibility, and the platform and version facts it rests on **with a source for each** (official doc URL, lock file, manifest) or marked UNVERIFIED. The main session spot-checks any version or API claim the recommendation turns on (open the source or search the official documentation) and labels the rest `UNVERIFIED`.

Check: the analysis file exists and covers every alternative.

### Phase N4: Decide

Write the analysis in plain text and ask (`orchestration.md` section 6): the options with a recommendation. If the decision involves schema or data-shape choices, ask those separately after the approach is chosen. A skipped answer is not an answer; ask again. The user decides; `technical-director` advises when the user asks or at the gate.

### Phase N5: Draft and gate

Draft from `templates/adr.md`, keeping its headings character for character, because later skills parse them (case matters): `## Status`, `## Date`, `## Last Verified`, `## Decision Makers`, `## Summary`, `## Platform and Version Risk` (a field table), `## ADR Dependencies` (a table with Depends on, Enables, Blocks, Ordering note), `## Context` (with `### Problem statement`, `### Current state`, `### Constraints`, `### Requirements`), `## Decision` (with `### Diagram` and `### Implementation Guidelines`: concrete Must and Must never rules builders follow), `## Options Considered` (`### Alternative 1: <name>`, `### Alternative 2: <name>`, and so on), `## Consequences` (`### Positive`, `### Negative`, `### Neutral`, `### Risks`), `## Requirements Addressed`, `## Performance implications`, `## Security and privacy implications`, `## Migration and Rollout` (with the **Rollback plan:** line), `## Validation Criteria` (how we will know it was right, and the signal that reopens it), `## Related`. Never rename, merge or reorder them. Status is `Proposed`. Date is today. A section that does not apply (or is full-rigor only at a lower rigor) says so in one line with a reason; it is not removed.

Gate `TD-ADR`, owner `technical-director`. It runs in `full` review mode only (`gates/README.md`: it is neither a phase gate nor an always-on gate); in `lean` and `solo` print `TD-ADR skipped: lean mode` or `TD-ADR skipped: solo mode`. When it runs, spawn it before writing, passing the draft path in scratch, the ADR path it will have, the architecture document path, the stack reference path and the constraints; it reads its own gate file. Its verdict words are APPROVE, CONCERNS, REJECT or NOT ASSESSED. CONCERNS: ask to revise, accept the concerns (recorded under Consequences, Risks) or discuss. REJECT: revise and re-run, do not write. NOT ASSESSED: record it as such with the missing input (the ADR draft or the architecture document); it is never recorded as an approval.

### Phase N6: Write and close

Ask once to write `docs/architecture/adr/ADR-NNNN-<slug>.md` (name the path and number; use `paths.adr` if mapped), then write it. When the gate ran, add its record line directly under the title in the form `gates/README.md` fixes: `> **Technical Director review (TD-ADR)**: <VERDICT> <date>` (APPROVE, CONCERNS or NOT ASSESSED). When it did not run, add no line. Re-read the file: the sections above exist and are non-empty.

**Do not unblock any story here.** The ADR is `Proposed`; a story blocked on it is still waiting. Instead list the waiting stories by path (see `references/accept.md` for how they are found) so the cost of leaving it Proposed is visible, read the required-ADR list in `architecture.md` and name the remaining ones, and recommend a review of the ADR by someone who did not write it (a fresh session, or `/app-architecture adr-audit`) before `accept`.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Where decisions live | `docs/decisions.md` entry (ADR only on request) | ADRs for foundation decisions; entries for the rest | ADRs for every significant decision |
| ADR depth | Not applicable | Status, Date, Summary, Context, Decision, Options Considered (at least two real ones), Consequences, Requirements Addressed, Validation Criteria, Rollback plan | Every section, including the version risk table, performance and security implications, migration plan and a Last Verified date |
| TD-ADR | skipped (solo) | skipped (lean) | runs (full mode only) |
| Accept | Always asks, in every mode | Always asks | Always asks |

Review mode never changes the accept rules: acceptance asks the user in `solo`, `lean` and `full` alike.

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

- BLOCKED (new): an unresolved conflict with an Accepted ADR, no decision after two asks, a required analysis artifact missing after one re-brief, or `TD-ADR` returned REJECT.
- BLOCKED (accept): any refusal (see `references/accept.md`); the verdict line names the exact refusal and what to do next.
- COMPLETE (new): the ADR is written as `Proposed`, re-read, and the waiting stories listed. COMPLETE (retrofit): sections appended per the user's yes, nothing existing modified. COMPLETE (accept): the ADR is `Accepted` and the stories unblocked are listed, or the user answered "not yet" and the ADR stays `Proposed`; the verdict line says which (`COMPLETE - ADR-0005 left Proposed at the user's choice, 0 stories unblocked`).
- NOT ASSESSED (new or retrofit): `TD-ADR` ran and returned NOT ASSESSED and the missing input was not supplied, or the decision rests on version or platform facts that could not be checked at all and the user chose to write the ADR anyway. The ADR is still written as `Proposed` with the gap named. Smaller unchecked facts are marked UNVERIFIED in the ADR and noted on the verdict line without changing the verdict.

## Report

```
ADR: ADR-NNNN <title>   Mode: <new | retrofit | accept>   Status now: <Proposed | Accepted | unchanged>
Path: <path>
Alternatives considered: <n>   Dependencies: <list | none confirmed>   Requirements addressed: <ids>
Platform/version facts: <n sourced, n UNVERIFIED>
Stories waiting on this ADR: <n> (<paths>)   Stories unblocked (accept only): <n>
Required ADRs still unwritten: <list>

Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: <TD-ADR: VERDICT> | none run (<mode> mode)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- `Accepted` is written only by accept mode, after the user's explicit yes in this conversation, and never by new or retrofit mode. `technical-director` may advise but never accepts.
- A new ADR is always `Proposed`. A retrofit answer of "Accepted" is written as `Proposed` and handed to accept mode.
- Never write `None` for dependencies that were not examined; `UNKNOWN` is resolved before writing.
- Never reuse or renumber an ADR number; never edit an existing ADR's decision text; supersession is a new ADR plus a status change made at its acceptance.
- Never state a version, API or platform behavior that was not checked from a source this run.
- Never unblock a story from new or retrofit mode, and never set a story to In Progress, In Review or Complete.
- Never invent rationale for a retrofitted decision.
