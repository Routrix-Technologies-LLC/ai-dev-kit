---
name: app-spec-review
description: "Independent review of one feature spec or all specs: completeness against the template, testability of every criterion, contradictions across specs, duplicated or missing capabilities and scope against the brief. Use when the user wants a spec reviewed before architecture or planning, says 'review the specs', 'are these specs consistent', 'is this ready to build', or before advancing from definition."
argument-hint: "[app] <spec-path | feature | all> [--review solo|lean|full]"
user-invocable: true
---

# App Spec Review

An independent, read-only review of feature specs. Single mode reviews one spec for completeness, testability, internal consistency and implementability. `all` mode additionally reviews the specs against each other and against the brief: contradictions, overlapping capabilities, dangling references and scope overload. Findings are verified before they are reported, and the review never edits a spec.

Writes: `docs/product/reviews/<date>-<scope>.md` (inline format below).
Next: `/app-spec <feature> retrofit` or edit the specs to fix findings, then `/app-spec-review` again; on APPROVED, `/app-architecture`; at stage exit, `/app-gate`.

## When to use and when not to

- Use after specs are authored and before architecture or story planning, after a spec changed materially, and at the definition gate.
- Not for authoring or changing a spec (`/app-spec`), not for judging stories (`/app-story-ready`), not for UX specs (`/app-ux-review` after build; UX spec completeness is checked inside `/app-ux`), not for the prose quality of documents.
- Independence: if `.studio/state.md` or this conversation shows that `/app-spec` authored the spec in this same session, say so and recommend a fresh session. Ask whether to proceed anyway; if the user proceeds, the report header says `Independence: authored in the same session`.

## Inputs

| Input | If missing |
|---|---|
| `studio.yaml` | Stop; offer `/app-adopt` or `/app-start`. |
| The spec(s): `docs/product/specs/<feature>.md` | If none, verdict is `NOT ASSESSED - no specs found` with the paths searched. Never APPROVED. |
| `templates/feature-spec.md` | Structure check becomes `NOT ASSESSED - template not found`; the other checks still run. |
| Brief or vision | Scope and alignment checks become `NOT ASSESSED - no brief`; say so in the report. |
| UX specs, architecture, ADRs | Optional context; used to detect conflicts where they exist. |

## Phase 1: Resolve, scope, announce

1. Resolve the app and print the plan block (`orchestration.md` sections 1 and 2). Agents: `product-manager`, `business-analyst`, `qa-lead` (testability), and the lead who owns the spec's platforms for implementability (`web-lead`, `desktop-lead`, `mobile-lead`, `backend-lead`, chosen from the spec's platforms and `studio.yaml`; `technical-director` is not used here).
2. Resolve scope. A path or feature name means single mode. `all` means every file in the specs folder. List the in-scope files with their modified dates before starting. **A scope that resolves to zero files is NOT ASSESSED, not a pass.**
3. Prior review: look in `docs/product/reviews/` for a review of the same scope. If every in-scope spec is unchanged since it (compare `git log -1 --format=%cs -- <spec>` to the review date; no git history means treat as changed), offer: reuse the prior verdict, or re-review. Unchanged specs reviewed against newer neighbours still need the cross-spec pass.

Check: the in-scope list is printed with a count.

## Phase 2: Structural pass (main session)

For each in-scope spec, deterministic checks, reported as rows with the denominator:

| Check | Fails when |
|---|---|
| Template sections present | A section of `templates/feature-spec.md` is missing, empty or still a placeholder |
| Requirement IDs | An ID does not match `REQ-<feature>-NNN`, is duplicated within or across specs, or the numbering skips without a note (a dropped one stays as `Withdrawn: <reason>`) |
| Acceptance criteria per requirement | A requirement has no criterion, or a criterion cites no requirement ID (count both directions) |
| Criterion form | A criterion contains unmeasurable words ("fast", "intuitive", "robust", "user-friendly") without a number or observable condition |
| States and edge cases | A requirement implies data, a network call, an input or a permission, and no empty, error or boundary behaviour is specified |
| Dependencies | A referenced spec, API, service or ADR does not exist at the named path |
| Open questions | Unresolved questions exist on a P0 or P1 requirement, or an Open questions section is absent |
| Status header | Missing or not one of the template's values (Draft, In review, Approved, Implemented, Withdrawn) |

Record exact locations (file and heading). Keep the rows; they are observations, and severity is assigned in Phase 5.

## Phase 3: Lens pass (parallel)

Issue every spawn in one message (`orchestration.md` section 4). Each agent reads the in-scope specs itself, writes one file to `~/AgentScratch/app-spec-review-<scope>/<agent>.md`, and receives the structural rows so it does not repeat them. Briefs quote the brief's goals and platforms.

| Agent | Lens | Looks for |
|---|---|---|
| `product-manager` | Value and scope | Requirements with no tie to a goal in the brief; P0 to P3 priorities that contradict the brief's MVP; scope that exceeds the stated MVP; success metrics missing or unmeasurable; out-of-scope list absent |
| `business-analyst` | Rules and completeness | Business rules stated twice differently; unreachable or dead-end states; undefined terms; edge-case matrices with holes; permissions and roles inconsistent with the rest of the spec; data that is read but never defined |
| `qa-lead` | Testability | For each requirement, can a test be written from the text alone? What type of test (Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance)? Criteria that cannot be observed; requirements that need data or environments nobody described; performance and accessibility requirements without thresholds |
| Platform lead (per spec platforms) | Implementability | Requirements the platform cannot do or does only with a heavy cost; hidden dependencies on OS, browser, store or hardware capability; permission and background-execution constraints; offline and sync implications not stated |

In `all` mode the `product-manager` and `business-analyst` briefs also include the Phase 4 cross-spec checklist so they work from the full set.

Gate `PD-SPEC-ALIGN` (`product-director`, review mode `full` only; `gates/pd-spec-align.md` names this skill as a trigger): in the same message, spawn it once per in-scope spec (batch up to five specs per call when there are many, one verdict per spec) with the gate ID, the spec path, the requirement IDs, the brief or vision path with its pillars and out-of-scope list quoted, and the paths of neighboring specs. It reads its own gate file. In `lean` and `solo` print `PD-SPEC-ALIGN skipped: lean mode` or `skipped: solo mode`. Its verdicts go into the review file and never into the spec headers (this skill does not edit specs): MISALIGNED is a BLOCKING scope finding, CONCERNS become REVISE findings, NOT ASSESSED goes under Not assessed with the missing input.

Check: every spawned agent's file exists with content. A missing file is re-briefed once, then reported as `<lens> NOT ASSESSED`; the lens's section stays a named gap.

## Phase 4: Cross-spec pass (all mode)

Main session, grep-first: extract from each spec its defined terms, roles, entities, states, numeric limits with units, event names and the IDs it references; then grep the other specs for the same names instead of re-reading everything. Findings:

- Contradictions: the same entity, limit, role permission, state name or flow defined differently in two specs (quote both with file and heading).
- Overlap: two specs that own the same capability, or a capability that nobody owns.
- Dangling references: a spec points at a feature with no spec file, or at a removed requirement ID.
- Dependency cycles between specs, and an order in which they can be built.
- Scope: count P0 and P1 requirements and features against the brief's MVP statement and any capacity noted in `planning/`; state the totals. Flag features not traceable to the brief.
- Ownership of shared data: which spec defines it, which only reference it.

Report the denominator ("checked 14 shared terms across 6 specs"). With a single spec in scope, this phase prints `Cross-spec pass: skipped, single spec in scope` and, when other specs exist, still greps them for the names the reviewed spec defines.

## Phase 5: Verify and classify

The main session verifies before reporting (agents are reliable when deriving and unreliable when diagnosing):

1. Every BLOCKING candidate and every contradiction: re-read the cited lines in the specs. Label `VERIFIED` or `UNVERIFIED - agent claim`. Drop what the text disproves. Unverified items are reported as such and never drive MAJOR REVISION.
2. Assign severity words from `standards/severity.md` (CRITICAL, HIGH, MEDIUM, LOW) plus the class:

| Class | Meaning |
|---|---|
| BLOCKING | Architecture or planning would be built on a wrong or untestable base |
| REVISE | Real defect, work can start on the rest |
| ADVISORY | Improvement |

3. Do not decide which of two contradicting specs is right. Present both and the options for the user.

## Phase 6: Write and present

Write `docs/product/reviews/<date>-<scope>.md` (scope is the feature name or `all`; if a file with that name exists, add a numeric suffix, never overwrite) in this shape:

```
# Spec review: <scope>   <date>
Independence: <fresh session | authored in same session>
Scope: <N specs> (<names>)   Brief: <path | none>   Template: <path | none>
Verdict: <WORD> - <why>
## Summary table: spec | structure | testability | consistency | scope | verdict
## BLOCKING findings (each: id, spec and heading, quote, why, VERIFIED/UNVERIFIED, options)
## REVISE findings
## ADVISORY findings
## Cross-spec findings (contradictions, overlaps, dangling, cycles, scope totals)
## Not assessed (what, why)
## Recommended order of fixes
```

Present the verdict and top findings in plain text, then ask which to do next (`orchestration.md` section 6): revise specs via `/app-spec`, accept listed items as known risk (recorded in the review, with the date), or discuss. Accepting a BLOCKING item as risk is allowed only on the user's explicit yes and is written in the review.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Specs expected | The brief only: this skill reviews any spec voluntarily | Specs for MVP features | Specs for every feature |
| Structure pass | Core sections only | Template-required sections | All sections |
| Lenses | `qa-lead` only | All four | All four, plus cross-spec pass is mandatory |
| Gate PD-SPEC-ALIGN (set by review mode, not rigor) | solo and lean: skipped | solo and lean: skipped | full mode: runs per spec; `/app-gate` consumes the review |

At minimal rigor with no specs, say "no specs required at minimal rigor" and stop with `NOT ASSESSED - no specs in scope`; that is information, not a pass.

## Verdicts

First match wins:

1. MAJOR REVISION: any VERIFIED BLOCKING finding of class contradiction, untestable P0 or P1 requirement, missing acceptance criteria on a P0 or P1 requirement, `PD-SPEC-ALIGN` MISALIGNED, a dangling dependency on something that does not exist, or scope exceeding the MVP with no cut list.
2. NEEDS REVISION: any verified REVISE finding, or a lens that returned only unverified blocking claims that the user must resolve.
3. NOT ASSESSED: the scope resolved to zero files, a spec is unreadable or placeholder-only, a lens did not return, or the brief and template were absent so a check named in the verdict could not run. The report says which reason applied. Per-check gaps are listed even when another verdict outranks this one.
4. APPROVED: every in-scope spec passed every check that ran, with counts shown, and nothing is NOT ASSESSED.

## Report

```
Spec review: <scope> (<N specs>)   Independence: <...>
Structure: <N of N checks passed>   Testability: <N of N requirements testable>
Cross-spec: <N contradictions, N overlaps, N dangling> (checked <N terms> across <N specs>) | skipped
Findings: BLOCKING <n> (verified <v>), REVISE <n>, ADVISORY <n>
Not assessed: <list or none>

Verdict: <WORD> - <one line why>
Gates: PD-SPEC-ALIGN: <verdict per spec> | none run (<mode> mode)
Wrote: <review path>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Read-only toward specs: it writes only the review file. Fixes are made by `/app-spec` or by the user.
- Never count a missing check as a pass; every zero has its denominator.
- Never decide which of two conflicting specs is right.
- Never report an agent's claim as a finding without re-reading the cited text.
- Never run its own lenses on a spec this session just authored without telling the user.
