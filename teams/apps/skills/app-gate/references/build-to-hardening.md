# Checklist: build to hardening

Question: is the first version feature-complete and honestly working, so the remaining work is hardening rather than building?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (listed, never counted as passed). Tests are waived at minimal only where none exist; a screenshot of what the user sees is never waived. **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | Feature-complete against the MVP | specs or brief; `planning/epics/` | Every MVP requirement (or brief item) maps to a story whose status is Complete, closed through `/app-story-done` (only that skill sets Complete). Report "N of N requirements have a Complete story". A Complete status with no evidence note is a finding | R | R | R |
| 2 | Evidence per change type is on disk | `docs/qa/evidence/`, test tree | Open three Complete stories at random; the evidence the change type needs (`standards/testing.md`) exists and is newer than the story's code. minimal: UI and Visual screenshots only | R | R | R |
| 3 | Tests pass | run `commands.test` | "N of N run, M skipped, 0 failed". If `commands.test` is empty and no tests exist, minimal reports "tests not required at minimal" and relies on item 5; standard and full: NOT ASSESSED until a harness exists | R if tests exist | R | R |
| 4 | Release build and lint pass | run `commands.build_release`, `commands.lint` | Exit codes | R if set | R | R |
| 5 | Smoke check passes on each target | newest `docs/qa/smoke-<date>.md` | PASS or PASS WITH WARNINGS, dated after the latest source commit (`git log -1`), every target in `platforms` present. A report whose counts disagree with the repo is a finding. No smoke report, or a stale one: run `/app-smoke` or NOT ASSESSED | R | R | R |
| 6 | Bug bar | `docs/qa/bugs/` or the issue tracker | No open S1. standard and full: no open S2 either; an S2 the user accepts in writing makes it CONCERNS. Report open counts by severity | S1 R, S2 rec | R | R |
| 7 | Stories were reviewed | `docs/qa/reviews/` or the story's review note | A review record for each non-trivial merged change at standard; every merge at full (`standards/rigor.md`). Report "N of N" | - | R | R |
| 8 | Specs match what was built | specs, `docs/decisions.md` | Deviations are logged or the spec was updated. Sample two specs against the code | rec | rec | R |
| 9 | Tech debt triaged | `planning/tech-debt.md` | No row marked blocking without an owner and a plan | - | rec | R |
| 10 | Risks reviewed | `planning/risks.md` | No High risk without mitigation or an accepted decision | - | R | R |
| 11 | Per-story and UI gate outcomes recorded | story files, `docs/design/reviews/` | `PM-ACCEPTANCE`, `PE-CODE-REVIEW` and `QL-TEST-COVERAGE` on each Complete story ("N of N"); `DD-VISUAL` on UI and Visual work. None REJECTED, REJECT, INADEQUATE or NOT ASSESSED. `PG-MILESTONE` and `TD-CHANGE-IMPACT` are optional | - | R* | R* |

## Quality checks

Run (not read): `commands.test`, `commands.build_release`, `commands.lint`. Run and observe the app's main path once on each target if the smoke report is missing or stale. `qa-lead` spot-checks items 2 and 5 against the repo (standard and full, unless review mode is solo).

## Manual checks

- Is there any feature you know is half-done but marked Complete?
- Is there a known data-loss or crash path that is not in the bug list?

## Panel focus

All four phase gates are required at this transition at standard and full rigor (`gates/README.md`; at minimal only `TD-PHASE-GATE` and `PG-PHASE-GATE`, and only if the user asks). `PD-PHASE-GATE`: is the product the one defined. `TD-PHASE-GATE`: technical health and debt. `PG-PHASE-GATE`: what remains and in what order. `DD-PHASE-GATE`: the built experience against the design language (N/A for an app with no UI platform).

## On PASS

Stage becomes `hardening`. Next: `/app-team-harden`, `/app-security-audit`, `/app-perf`, `/app-a11y-audit`, `/app-privacy-review`, `/app-i18n` as the checklist of the next gate requires.
