---
name: app-qa-plan
description: "Write the test plan for a sprint, feature or release: evidence required per change type, the platform matrix, automated and manual checks, regression selection, non-functional checks and exit criteria. Use when the user says QA plan, test plan, how will we test this, what do we need to verify before release, or before a sprint, feature or release starts."
argument-hint: "[sprint <id> | feature <name> | story <path> | release <version>] [--review solo|lean|full]"
user-invocable: true
---

# App QA Plan

A test plan written after the build is a post-mortem. This skill reads the stories, specs and release scope, assigns each change its evidence by change type, maps the platforms the app must be proven on, picks the regression checks, and lists the manual checks a human must do. The plan is what `/app-smoke`, `/app-story-done` and `/app-gate` later measure against.

Writes: `docs/qa/test-plans/<scope>.md` (template `test-plan.md`) and `docs/qa/test-plans/<scope>-cases.md` (the written cases).
Next: `/app-dev-story` (build to the plan), `/app-smoke` (run the smoke scope), `/app-story-done`, `/app-release`.

## When to use and when not to

Use it before a sprint or batch starts, before a feature is built, and before a release or hardening pass. Not for these:

- Checking one story is ready to build: `/app-story-ready`.
- Running the build and observing it: `/app-smoke`.
- Setting up the test runner or CI: `/app-test-setup`.
- Judging the quality of the tests that exist: `/app-story-done` and `/app-code-review`.
- Measuring performance, accessibility or security: `/app-perf`, `/app-a11y-audit`, `/app-security-audit`. This plan schedules them and says what each must show.

## Inputs

- Required: `studio.yaml` (platforms, `stack.min_targets`, commands, rigor).
- Required, by scope: `sprint` reads `planning/sprints/<id>.md` and its stories; `feature` reads the spec and its stories in `planning/epics/`; `story` reads one story file; `release` reads the release scope (`docs/release/<version>.md` or the changelog's unreleased section), the stories closed since the last release and the open bugs.
- Read when present: UX specs, `perf-budget.md`, the threat model, `docs/qa/bugs/`, `docs/qa/smoke-paths.md`, previous plans (to reuse, not copy).
- `standards/testing.md` defines the evidence required for each change type. Read it; do not invent evidence rules. If it is missing, report BLOCKED for this input and offer to continue with the evidence defaults stated in the story files, labelled `UNVERIFIED STANDARD`.

## Phase 1: Resolve scope and count

Who: the main session. Announce the plan (orchestration.md section 2).

1. Resolve the scope from the argument. No argument: ask which of sprint, feature, story or release, listing the candidates found on disk.
2. Count the in-scope stories (or, for a release, closed stories plus open bugs): **N**. State it: "N stories in scope, from <paths>".
3. **If N is 0, stop.** Do not write a plan. A plan for zero stories looks exactly like a finished plan. Report BLOCKED with which scope was searched and which path was empty, and route: no sprint file means `/app-sprint`; stories missing means `/app-plan`; a release with no closed stories means there is nothing to release.
4. A story file that is referenced but missing is listed as MISSING and the plan continues with the rest. All missing is N=0.

Check: N and the story list are printed before anything else happens.

## Phase 2: Load and classify

Who: the main session. Read targeted sections (acceptance criteria, change type, files, dependencies), not whole stories, unless a story has no acceptance criteria, in which case read it fully; a story without testable criteria is itself a finding (`QL-STORY-READY` territory; recommend `/app-story-ready`).

For each story, record the change types from the story header (Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance, Docs). Use the declared type as given. If undeclared, infer it from the acceptance criteria, mark it `INFERRED`, and list it as a gap to fix before the story is built. A story may carry a primary and a secondary type; both get their evidence.

Print the classification table (story, types, source of type) and move on.

## Phase 3: Draft the plan

Who: `qa-lead` writes the plan; `test-engineer` writes the cases; they run in sequence (the cases follow the strategy), each into its own file. Brief both per orchestration.md section 3, passing the distilled story table, the platform list, the evidence rules from `standards/testing.md`, and the rigor.

`qa-lead` writes `docs/qa/test-plans/<scope>.md` from `templates/test-plan.md`, keeping the template's section names (Summary by change type, Automated tests required, Manual checklist, Platform and device matrix, Smoke scope, Fixtures and environments, Definition of done). Place the contents below as follows: scope and risk and open questions in the summary and Fixtures and environments; evidence by story in Summary by change type; regression selection in Automated tests required; scheduled non-functional checks in the Manual checklist; entry and exit criteria in Definition of done; the matrix and smoke scope in their own sections. Contents:

1. **Scope and risk.** What is in, what is out, the riskiest changes first (data loss, money, auth, migrations, anything hard to roll back).
2. **Evidence by story.** One row per story: types, the automated tests required (layer and location), the retained evidence required (screenshots per screen and state, request and response captures, migration dry-run output, measurements), and the manual checks. The row follows the evidence rules for each change type in `standards/testing.md`; UI and Visual evidence is a retained screenshot per screen and state per platform and form factor (light and dark if themed), a keyboard-only pass noted, and the Run result line (`orchestration.md` section 10); it is never waived by rigor.
3. **Platform matrix.** Derived from `platforms` and `stack.min_targets`, one row per target the scope touches:

| Platform | Matrix rows | How each is proven |
|---|---|---|
| web | supported browser families, small and large viewport, light and dark, one slow-network run | headless browser in CI; real-browser spot check where engines differ |
| windows, macos, linux | oldest and newest supported OS version, display scale factors, high contrast on Windows, installed and portable run if both ship | CI job per OS; window capture; manual pass on a real machine for installers and OS integration |
| ios, android | oldest and newest supported OS, smallest and largest screen class, one low-memory device class, accessibility text sizes | simulator and emulator in CI or locally; a real device for push, camera, biometrics, background behavior |
| backend | supported runtime version, database engine version, empty and migrated database, one dependency-down scenario | integration tests against throwaway dependencies |
| cli | each OS and shell the app supports, a non-interactive run, piped input and output | CI job per OS |
| extension, library | host browser versions, or supported language and runtime versions | CI matrix |

Each row says `automated`, `simulated`, `real device or machine`, or `manual`, and which of these are not possible with the team's current setup (those rows are marked `GAP`, with the closing action).
4. **Smoke scope.** The critical paths `/app-smoke` must observe for this scope: start from `docs/qa/smoke-paths.md` and add the paths that this scope's changes make newly critical. If `smoke-paths.md` does not exist, say so and recommend `/app-test-setup`.
5. **Regression selection.** The tests that must run and pass because of what changed: tests of every module the scope touches (use the Files lists), the critical-path journeys, and a regression test for each bug fixed in scope (list the bug IDs; a fixed bug without a test is a gap). Name quarantined (flaky) tests and their owners. A quarantined test is excluded from the pass count but listed, with a rule: quarantined more than one sprint becomes a story to fix or delete.
6. **Non-functional checks scheduled.** Only those that apply, each with the skill that produces its evidence and the budget or standard it is held to: performance against budgets (`/app-perf`), accessibility (`/app-a11y-audit`), security (`/app-security-audit`), privacy (`/app-privacy-review`), localization (`/app-i18n`), and for long-running targets (services, desktop apps, mobile apps with background work) a soak run: duration, the metrics watched (memory growth, handles or descriptors, connection count, battery, error rate) and the limit that fails it.
7. **Entry and exit criteria.** Entry: build green, smoke PASS on the candidate. Exit: every story's evidence present, no open S1 or S2 in scope, regression selection passed, matrix rows either proven or accepted as GAP by the user in writing, non-functional checks run or explicitly deferred.
8. **Open questions and gaps.** Everything unknown, each with an owner. Nothing is filled with a guess.

`test-engineer` writes `docs/qa/test-plans/<scope>-cases.md`: for Logic and Integration changes, cases as Given, When, Then with data and expected results including edge cases from the spec (empty, boundary, maximum, malformed, concurrent, offline, interrupted); for UI and Visual changes, the setup, the exact state to reach, what to verify against the UX spec, and the pass condition; for Data changes, the dry-run and rollback cases and an old-data-still-loads case. Each case carries the requirement ID or acceptance criterion it proves. Cases that a human must run are marked MANUAL with the platform.

Check, by the main session: both files exist with real content; every story appears in the evidence table; every acceptance criterion in scope appears in at least one case (report any that do not as uncovered); the platform matrix has one row per platform in `platforms` that the scope touches.

## Phase 4: Review and agree

Who: the main session. Show the user the summary: stories by type, matrix rows with GAPs, manual check count, scheduled non-functional checks, uncovered criteria, open questions. Ask once (orchestration.md section 6) whether to accept the plan, revise it, or accept with the GAPs recorded as risks (they go to `planning/risks.md` through the user's approval). Checkpoint.

At `standard` and `full`, offer to back-fill missing test cases into the story files' QA sections; edits to existing stories are listed and asked once, and existing stories are never renumbered or rewritten.

## Rigor and review mode

Rigor changes how much the plan contains, never whether UI and Visual changes get their screenshots.

| | minimal | standard | full |
|---|---|---|---|
| Evidence table and smoke scope | required | required | required |
| Cases file | acceptance criteria only | Given, When, Then for Logic and Integration; setup and pass condition for UI | plus edge-case matrix per spec and coverage targets per module |
| Platform matrix | main platform | every platform in `platforms` | oldest and newest targets, device classes |
| Regression selection and non-functional schedule | fixed-bug tests only | plus touched modules and critical journeys | plus soak and budgets per target |

Gates: none are defined for this skill. Recommend `/app-story-ready` for stories whose criteria were flagged (its checklist runs at every mode; the `QL-STORY-READY` gate itself is full only). Print `Gates: none run (<mode>)`.

## Verdicts

1. BLOCKED: N is 0, the scope cannot be resolved, or `standards/testing.md` is missing and the user declined to continue with labelled defaults.
2. COMPLETE: the plan and cases files exist and meet the checks above. A COMPLETE plan may still list GAPs and uncovered criteria; the report counts them.

## Report

```
Scope: <scope>  Stories: <N> (<n> missing)  Types: <counts by type>
Matrix: <rows> rows (<n> automated, <n> simulated, <n> real device, <n> manual, <n> GAP)
Smoke scope: <n> paths (<source>)   Regression: <n> tests + <n> bug regressions   Quarantined: <n>
Non-functional scheduled: <list or none>
Uncovered criteria: <n of total>   Open questions: <n>
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never write a plan for zero stories.
- Never invent evidence rules; they come from `standards/testing.md`.
- Never waive the screenshot for a UI or Visual change at any rigor.
- A matrix row the team cannot prove today is a visible GAP with a closing action, never silently dropped.
- Never rewrite or renumber existing stories. Back-fill edits are listed and approved first.
- A fixed bug without a regression test is listed as a gap.
- Soak runs, emulator matrices and full suites named in the plan are marked as lock-run heavy jobs (`shared/rules-full.md`).
- Never start the next skill automatically.
