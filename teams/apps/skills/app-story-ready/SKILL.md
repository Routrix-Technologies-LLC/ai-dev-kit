---
name: app-story-ready
description: "Read-only readiness check of one story, an epic or a sprint: traced and binary acceptance criteria, valid decisions, clear scope, no open questions, a test and evidence plan. Use when the user asks if a story, an epic or the sprint's stories are ready to build, or before starting work."
argument-hint: "[app] [story-path | epic-slug | sprint | all] [--review solo|lean|full]"
user-invocable: true
---

# App Story Ready

Checks that a story holds everything a builder needs before writing code: no design questions mid-build, no guessing, no vague criteria. It reports and offers to draft fixes in the conversation. It is read-only with one exception: when a story's verdict is READY and its status is Draft, it asks once to mark it Ready (Phase 6). It never writes anything else, never changes any other status and never writes a checkpoint.

Writes: nothing, except the `Status` field of Draft stories that came out READY, after the user's yes. If the user asks for the report saved, the main session saves the printed report to `docs/qa/reviews/<date>-story-ready-<scope>.md`; the check itself touches a story only in that one way.
Next: `/app-dev-story <story>` for READY stories, otherwise fix the gaps and run this again; `/app-sprint plan` once a set is READY.

## When to use and when not to

- Use before building, before committing a story to a sprint, and after editing a Draft or Blocked story.
- Not for judging a finished story (`/app-story-done`), a spec (`/app-spec-review`), or the whole plan's size and order (`/app-scope`, and gate `PG-PLAN` at full review mode in `/app-plan` and `/app-sprint`).

## Inputs

Resolve the app per orchestration.md section 1 and announce per section 2 (this skill announces even though it spawns nothing at lean and solo). Needed: the stories in scope. Optional but checked when a story cites them: the spec (`docs/product/specs/`), ADRs or `docs/decisions.md`, UX specs, API contracts, migration plans, the threat model, the perf budget, `docs/stack-reference.md`. A cited artifact that does not exist is a finding. An input that exists but cannot be read is NOT ASSESSED for that item, never a pass.

## Phase 1: Scope

The scope is the text after the skill name, with any `--review` pair removed:

- a story path: that story;
- an epic slug or folder: every `story-*.md` in `planning/epics/<epic>/`;
- `sprint`: the stories named by the newest file in `planning/sprints/` (a kanban file counts: its queue);
- `all`: every `story-*.md` under `planning/epics/`;
- nothing: ask which of those, as options.

Zero stories in scope is `NOT ASSESSED - no stories in scope`. Name the scope and the empty path and route to `/app-plan`. Never print `Ready: 0, Needs Work: 0` over an empty list. For `sprint`, "no sprint file found" and "the sprint file lists no stories" are different reports; say which. A sprint entry whose story file is missing is reported as a missing story and the rest are still checked. Print `Checking <n> stories.` before going on.

## Phase 2: Read the facts once

The main session reads each story fully, then, once for the run:

1. Every decision a story cites: its status (Accepted, Proposed, Superseded, Deprecated) from the ADR file, or the dated entry in `docs/decisions.md` at minimal rigor. A decision with no readable status is NOT ASSESSED for that item; a missing file is a finding.
2. Each cited requirement ID in the spec (`REQ-<feature>-NNN`). An ID not found in the spec is a finding. A spec that cannot be found is NOT ASSESSED for traceability.
3. Each dependency story's Status.
4. Existence (only existence) of every artifact a story names: UX spec, design language section, API contract, migration plan, threat-model entry, perf budget, copy keys file, asset paths.
5. Rigor from `studio.yaml` `modes.rigor`, which decides which groups block (table in Phase 3).

Rows are observations; the verdict is the main session's.

## Phase 3: The checklist

Check every item for every story, and print all six groups every time. A group with nothing passing prints `none - see Gaps`, so the reader sees it was checked.

| Group | full | standard | minimal |
|---|---|---|---|
| 1 Requirements and Acceptance | blocks | blocks | blocks; `Brief MVP feature N` stands in for a REQ ID |
| 2 Decisions and Contracts | blocks | the decision-status item blocks, the rest advisory | the decision-status item only |
| 3 Scope Clarity | blocks | blocks | blocks except Estimate: advisory |
| 4 Open Questions and Dependencies | blocks | blocks | blocks |
| 5 Referenced Artifacts | blocks | blocks | blocks |
| 6 Test and Evidence Plan | blocks | blocks | blocks; test files may be waived per rigor, observed evidence for UI and Visual never |

An advisory item that fails is listed under Gaps with its Fix and never lowers READY by itself.

### 1 Requirements and Acceptance
- [ ] **Requirement traced:** the story cites at least one requirement ID that exists in the spec and quotes or links the specific rule, not only the file.
- [ ] **Self-contained:** the criteria say what done means without opening the spec.
- [ ] **Binary:** each criterion is a specific, observable condition two people would judge the same way. "Fast", "works well", "intuitive" fail. A criterion a test can set up with chosen inputs counts as testable.
- [ ] **No judgement calls** except Visual stories, where a judgement criterion must name its evidence file and who signs it off.
- [ ] **Coverage:** every criterion ends with its requirement ID, and the number of criteria meets the minimum for the story's type (Logic and Integration 2, UI and Visual 2, others 1; minimal rigor may group but never drops to zero).

### 2 Decisions and Contracts
- [ ] **Decision status** (every rigor): each cited decision is Accepted. Proposed, Superseded or Deprecated is BLOCKED, with the fix text `BLOCKED: <ADR> is <status>; accept it with /app-adr accept, or point the story at its successor`. No file for a cited decision is BLOCKED. `N/A - <reason>` is a pass; a blank field fails.
- [ ] **Contract defined:** an Integration story names the contract (path in `docs/architecture/api/`, or the IPC command list) it implements; one with no contract yet is NEEDS WORK, routed to `/app-api`.
- [ ] **Migration planned:** a Data story names its `planning/migrations/<id>.md`, routed to `/app-data-migration`.
- [ ] **Threat traced:** a Security story names the threat-model entry it mitigates; routed to `/app-threat-model`.
- [ ] **Version risk:** any framework or SDK API the story touches that is newer than the pinned reference has a note or a verification step, or the story states `N/A - no framework API involved`. No stack reference: NOT ASSESSED for this item.

### 3 Scope Clarity
- [ ] **Rank** is a number (advisory). **Change type** is one of Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance, Docs.
- [ ] **Estimate** is S, M or L (a leftover template bracket fails). An L with a Files list of more than about a dozen files or three components: advisory "consider splitting".
- [ ] **Files** lists the planned files or modules, or `none yet - <reason>`. Blank fails.
- [ ] **Out of Scope** states the boundary, or wording makes it unambiguous.
- [ ] **Platforms** named when the app has more than one platform in `studio.yaml`, with per-platform differences in the criteria.

### 4 Open Questions and Dependencies
- [ ] **No open markers:** no TBD, TODO, UNRESOLVED or `???` as whole words. A question mark inside code or a formula is not a marker.
- [ ] **Dependencies listed** (or `None` stated), **exist**, and none is Draft or Blocked. A missing, Draft or Blocked dependency makes the story BLOCKED. A dependency that is Ready, In Progress or In Review is a note, not a block; it orders the work.
- [ ] **No cycle:** following dependencies never returns to the story.

### 5 Referenced Artifacts
- [ ] A UI or Visual story names its UX spec and the design-language section it uses, and both exist.
- [ ] Copy or localization keys, assets, test fixtures and seed data the story reads exist, or the story says it creates them. Existence only. Print `Referenced artifacts verified: <n> found` or `No artifact references`.
- [ ] A Performance story names its budget (`perf-budget.md`); none is NEEDS WORK.

### 6 Test and Evidence Plan
- [ ] **QA test cases** exist for the story's type: Given/When/Then for Logic and Integration; Setup/Verify/Pass per screen and state for UI and Visual; dry-run and rollback for Data; the abuse case for Security; the measurement for Performance; a smoke check for Config and Infra.
- [ ] **Test Evidence** names where proof will live (a test path, or `docs/qa/evidence/<story>/`).
- [ ] **Run and observe planned** for UI, Visual and any story a user can see: it names how the change will be launched and looked at on each platform (orchestration.md section 10). "Logic change" is not an acceptable exemption when what a user sees changes.
- [ ] **Accessibility noted** for UI and Visual: keyboard, screen reader and text scaling expectations, or `covered by <UX spec section>`.

## Phase 4: Verdict per story

First match wins:

1. BLOCKED: a finding the reader can clear by other work: a cited decision missing or not Accepted, a dependency missing or Draft, an open design question with no owner.
2. NEEDS WORK: a blocking checklist item fails and the story can be fixed now.
3. NOT ASSESSED: the story or something its verdict turns on could not be read (unreadable file, decision with no status, spec missing). Name what. It is never READY, because a story nobody could check has not been shown ready. It ranks below the failures because a known blocker is more useful than an unknown.
4. READY: every item passes, is N/A with a stated reason, or is advisory. Advisory gaps are still listed.

A BLOCKED story may also have NEEDS WORK items; list both. Gaps lists failed checklist items only, never a passing item and never an observation from outside the checklist.

## Phase 5: Independent testability review (gate)

Per orchestration.md section 7. `QL-STORY-READY` (owner `qa-lead`) runs at full review mode; lean and solo print `QL-STORY-READY skipped: <mode> mode`. One spawn for the whole scope (split into batches of ten stories). Pass per story: the path, change type, every criterion verbatim, the requirement text, and each dependency with its state. The agent edits nothing and writes no file: tell it to return its answer inline and replace the standard return contract with `Reply with only: the gate verdict per story (the gate's verdict words), the list of gaps per story, one line each, and anything you could not judge.` At full also spawn `product-manager` in parallel to check that each cited requirement says what the story claims and that no requirement in scope is silently dropped; it also returns inline.

Apply the result: ADEQUATE clears; GAPS are added to the story's Gaps and the user decides (draft fixes, accept, discuss); INADEQUATE raises the verdict to at least NEEDS WORK (BLOCKED stays BLOCKED); NOT ASSESSED turns a READY into NOT ASSESSED. If the user goes on regardless, the report says `proceeding despite QL-STORY-READY: <verdict> (user override)`. Never a silent READY. Claims from the agents are labelled `UNVERIFIED` unless the main session re-read the line that supports them.

## Phase 6: Report

One story:

```
## Story Readiness: <title>
File: <path>   Type: <type>   Estimate: <S|M|L>   Status in file: <status>
Verdict: <READY | NEEDS WORK | BLOCKED | NOT ASSESSED>

### Passing checks (<n>/<total>)
Requirements and Acceptance: <items or "none - see Gaps">
Decisions and Contracts: <items, "N/A at minimal (decision status checked)", or "none - see Gaps">
Scope Clarity: <items or "none - see Gaps">
Open Questions and Dependencies: <items or "none - see Gaps">
Referenced Artifacts: <items, "no artifact references", or "none - see Gaps">
Test and Evidence Plan: <items or "none - see Gaps">

### Gaps
- <checklist item>: <what is missing or wrong>
  Fix: <the text that resolves it>

### Blockers (if BLOCKED)
- <what blocks>: <the story, decision or question that must clear first>
```

Several stories: a summary first, then the block for each story that is not READY.

```
## Story Readiness Summary: <scope> (<date>)
Ready <n> | Needs Work <n> | Blocked <n> | Not Assessed <n>   of <total> stories
Ready: <title> (<path>), ...
Needs Work: <title>: <main gap>
Blocked: <title>: blocked by <story, decision or question>
Not Assessed: <title>: <what could not be read>
```

`sprint` scope: when a Must story is not READY, put this first: `WARNING: <n> Must stories are not ready: <each with main gap>. Fix them before the sprint starts or replan with /app-sprint plan.`

For a single story, also list up to three other stories to start (Ready, not waiting on unfinished dependencies, lowest Rank number) with one line and the estimate, or say `Next ready stories: none ready in <scope>`.

Promotion (the one write): when the verdict for a story is READY and its `Status` in the file is Draft, ask once for the whole set, last in the reply: "Mark these N stories Ready?" with the story list. Options: yes / no. A skipped answer is not a yes. On yes, change only the `> **Status**: Draft` line to `> **Status**: Ready` in those files (and nothing else in them), then re-read each to confirm. A READY Blocked story, a story with any other status, and every non-READY story are never changed: tell the user what to do instead. Status owners across the lifecycle: `/app-plan` writes Draft, Ready or Blocked at creation; `/app-dev-story` sets In Progress and In Review; only `/app-story-done` sets Complete. A Blocked story becomes Ready only by the user's own edit once the blocker clears.

Offer help: "Draft the missing parts for any of these?" Options: yes (drafted in the conversation only), no. On yes, draft only the missing text; the user or `/app-plan` writes it.

Redirects: a story file missing, `/app-plan <epic>`; no spec for the work, `/app-spec`; scope grew past its estimate, split it (a new story through `/app-plan`).

## Rigor and review mode

Rigor changes which groups block (Phase 3 table), never what a criterion must be. Review mode: `QL-STORY-READY` is full only per `gates/README.md`; solo and lean skip it and print `QL-STORY-READY skipped: <mode> mode`. The checklist in Phase 3 runs in every mode, because it is this skill's whole job.

## Verdicts

Per story as in Phase 4. The run's verdict is the strictest across stories: BLOCKED, then NEEDS WORK, then NOT ASSESSED, then READY. NOT ASSESSED applies when any story's check could not complete, when the scope was empty, and when a gate that should have run returned NOT ASSESSED.

## Report footer

```
Verdict: <WORD> - <one line why, with counts and denominator>
Gates: <QL-STORY-READY: VERDICT> | none run (<mode>)
Wrote: <the story files marked Ready | none>
Next: </app-dev-story ...> (<why>)
```

## Rules for this skill

- Read-only except the Draft to Ready status line, after the user's yes. Never write, edit or rename anything else, never set any other Status, never write the checkpoint.
- Fail only on checklist items. Observations outside the checklist belong in the user's summary, not in Gaps.
- An absent field never defaults to the permissive answer: unfilled is a failure or NOT ASSESSED, not a pass.
- Every group is printed every time, including groups with nothing passing.
- Counts always carry their denominator ("12 of 14 READY").
- Recommend the next skill; never start it.
