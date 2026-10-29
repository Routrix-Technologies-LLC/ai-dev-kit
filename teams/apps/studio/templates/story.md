<!--
Template: story. Written by: product-manager with principal-engineer (design notes) and qa-lead (test cases). Skill: /app-plan writes it (Ready only when its readiness checks ran and passed, otherwise Draft or Blocked); /app-dev-story sets In Progress then In Review and updates Files and Run result; /app-story-done is the only route to Complete.
Field names are read by /app-plan, /app-story-ready, /app-dev-story and /app-story-done: keep them exactly.
Lives at: planning/epics/<epic>/story-NNN-<slug>.md (override: paths.epics).
Rigor: minimal = header, acceptance criteria, Files, test cases, Run result. standard = adds spec and REQ IDs, ADR with summary and version stamp, implementation notes, out of scope, evidence required. full = adds dependency detail, platform-by-platform criteria, review notes.
Delete this comment when the story is created. Never renumber stories. Keep the section headings.
-->

# Story [NNN]: [title]

> **Epic**: [epic name]
> **Status**: [Draft | Ready | In Progress | In Review | Complete | Blocked]
> **Blocked reason**: [only when Status is Blocked, as `BLOCKED: <what must clear>`, naming any ADR by ID, for example `BLOCKED: ADR-0005 is Proposed`; otherwise delete this line]
> **Change type**: [Logic | Integration | UI | Visual | Data | Config | Infra | Security | Performance | Docs]
> **Estimate**: [S | M | L]
> **Rank**: [position in the epic's build order, 1 is first]
> **Platforms**: [web, windows, macos, linux, ios, android, backend, cli, extension, library]
> **Requirement IDs**: [REQ-feature-NNN, REQ-feature-NNN]
> **Governing decision**: [ADR-NNNN, or `N/A: <reason no architectural decision applies>`; never blank]
> **Last updated**: [YYYY-MM-DD, changed on every status change]

Status words are fixed across the studio. Draft: written but not yet shown ready (gaps listed in Context). Ready: passed the readiness checks (`/app-story-ready` checklist, `QL-STORY-READY` at full review mode). In Progress: a builder has it (`/app-dev-story`). In Review: implemented, awaiting `/app-story-done` (set by `/app-dev-story`). Complete: set only by `/app-story-done`. Blocked: a governing ADR is not Accepted or a dependency is not Ready or Complete; the Blocked reason line says what must clear (`/app-adr accept` moves it to Ready when that is the only blocker). Status lives only here; sprint files hold commitments, not status.

## Context

**Spec**: `docs/product/specs/[feature].md`
**UX spec and design language section** (UI and Visual stories): [`docs/design/ux/[flow].md`, section]
**Contract, migration or threat entry** (Integration, Data, Security stories): [`docs/architecture/api/...`, `planning/migrations/MIG-NNNN-...`, threat-model entry ID]
**Budget** (Performance stories): [`docs/qa/perf-budget.md` row]
*(Requirement text lives in the spec. Read it fresh at review time; do not copy it here. If the story cites a rule, quote the specific rule, not only the file.)*

**Governing ADR**: [ADR-NNNN: title, or `N/A: <reason>`]
**ADR decision summary**: [one or two sentences on what the ADR decided]
**ADR version stamp**: [the ADR's last verified date, else its date, else `unversioned`]

If the ADR changes after this stamp, the story is stale: re-check before implementing.

## Acceptance Criteria

Each criterion is binary (it passes or it does not) and scoped to this story.

- [ ] [AC-1: observable behavior, with the exact value, state or message] (REQ-feature-NNN)
- [ ] [AC-2] (REQ-feature-NNN)
- [ ] [AC-3: failure path or empty state] (REQ-feature-NNN)
- [ ] [Performance, accessibility or platform criterion if the spec sets one] (REQ-feature-NNN)

Every criterion ends with its requirement ID. A story needs at least two criteria for Logic, Integration, UI and Visual changes. Aim for no more than eight; split the story beyond that. For UI and Visual stories, state keyboard, screen reader and text-scaling expectations, or `covered by <UX spec section>`.

## Implementation Notes

[Specific, actionable guidance from the ADR and architecture: patterns to use, forbidden patterns, interfaces to honor, data shapes, error handling expectations. This is what the builder reads instead of the whole ADR. Do not paraphrase in ways that change meaning.]

## Out of Scope

Handled elsewhere. Do not implement here:
- [Story NNN: what it handles]
- [Deferred item and where it is tracked]

## Files

The code and test files this story creates or changes. /app-story-done compares the real diff to this list and flags anything outside it.

| Path | Create / Modify | Purpose |
|---|---|---|
| `[src/...]` | [Create] | [what it holds] |
| `[tests/...]` | [Create] | [what it covers] |

Never blank: write `none yet: <reason>` if the files are not known. /app-dev-story replaces the planned list with the files actually changed.

## QA Test Cases

Written by qa-lead before implementation. Pick the style by change type: Given/When/Then for automatable types (Logic, Integration, Data, Config, Security, Performance), Setup/Verify/Pass for manual types (UI, Visual, and anything a person must judge).

### Automatable (Given / When / Then)

**TC-1 [AC-1]: [short name]**
- Given: [state and inputs]
- When: [action]
- Then: [exact expected result]
- Test file: `[path]`   Command: `[from studio.yaml commands.test]`

**TC-2 [AC-3]: [failure path]**
- Given: [...]
- When: [...]
- Then: [...]

### Manual (Setup / Verify / Pass)

**TC-M1 [AC-2]: [short name]**
- Setup: [build, device or browser, data, account, how to reach the screen]
- Verify: [what to look at or do, step by step]
- Pass: [what the tester must see; a screenshot name if evidence is required]

## Test Evidence

Evidence by change type (standards/testing.md). The story is not Complete without it. Name where the proof will live: a test path, or the evidence folder.

| Change type | Required evidence | Path |
|---|---|---|
| Logic, Data | Passing unit tests; for a fix, a regression test seen failing before the fix | test files above |
| Integration | Integration test run output | `docs/qa/evidence/[story]/test-run.md` |
| UI, Visual | Screenshots of each changed state on each affected platform, plus a short note | `docs/qa/evidence/[story]/` |
| Config, Infra | Before and after output, or a dry-run log | `docs/qa/evidence/[story]/` |
| Security | Test or scan output showing the control works; reviewer sign-off | `docs/qa/evidence/[story]/` |
| Performance | Measurements against the budget, before and after | `docs/qa/evidence/[story]/` |
| Docs | Link check or rendered preview | `docs/qa/evidence/[story]/` |

Evidence path for this story: `docs/qa/evidence/[story-slug]/`

## Run result

Exactly one line, filled by /app-dev-story and re-checked by /app-story-done (orchestration.md section 10). NOT VERIFIED blocks closing a UI or Visual story.

Run result: [OBSERVED - what was seen, evidence path | NOT VERIFIED - why it could not be run | N/A - why nothing is observable]

## Dependencies

- **Depends on**: [story IDs (none may be Draft), ADRs that must be Accepted, external services, access needed; write `None` only after checking]
- **Unlocks**: [story IDs]
- **External blockers**: [none, or what and who]

## Completion Notes

[Filled at close: deviations from the spec, tech-debt rows added (TD-NNN), follow-up stories, reviewer verdict.]
