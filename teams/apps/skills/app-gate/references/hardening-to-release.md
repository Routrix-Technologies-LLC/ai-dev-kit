# Checklist: hardening to release

Question: is this version secure, fast, accessible, private and stable enough to put in front of users?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (listed, never counted as passed). A "UI platform" is any of web, windows, macos, linux, ios, android, extension; other apps read `N/A: no UI platform` for UI items. **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

**Hard rules at every rigor:** an open CRITICAL or HIGH security finding, an open S1 or S2 bug, or a failing release build is FAIL. Rigor changes which audits must exist, not whether a known problem blocks.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | Security audit | newest `docs/security/audits/<date>.md` | Verdict CLEAR, or CONCERNS with every MEDIUM-or-lower finding owned. No open CRITICAL or HIGH. Dated after the last change to security-sensitive code. Absent at minimal is CONCERNS, except that it is required (R) at any rigor when security-sensitive code (auth, money, personal data, IPC, updates, crypto, parsing of untrusted input) changed since the last release, because `standards/rigor.md` never relaxes the security look | rec, R if sensitive | R | R |
| 2 | Dependency and license review | audit output, notices file or SBOM | Dependency audit was run (not just read about); license notices for shipped dependencies exist (`compliance-specialist`) | rec | R | R |
| 3 | Performance against budget | newest `docs/qa/perf-<date>.md`, `perf-budget.md` | WITHIN BUDGET on each target. OVER BUDGET is FAIL unless the user accepted the deviation in writing (then CONCERNS). NO BUDGET at full is NOT ASSESSED. `standards/rigor.md` requires budgets and performance evidence at full; at standard they are recommended (absent is CONCERNS) | - | rec | R |
| 4 | Accessibility audit (UI platforms) | newest `docs/qa/a11y-<date>.md` | CONFORMS passes; PARTIAL is CONCERNS with an owner per gap; FAILS is FAIL. Absent is CONCERNS at minimal and standard. Required at full | rec | rec | R |
| 5 | Privacy review | `docs/security/privacy.md` | CLEAR. Required when the app collects or sends personal data or ships through a store; if unknown, ask. Store declarations agree with the inventory | rec | R if data | R |
| 6 | Localization readiness for each shipped locale | newest i18n report | READY for each shipped locale; a single-locale app records `N/A: one locale` | - | rec | R |
| 7 | Bug bar | bug list | No open S1 or S2; S3 and S4 counts reported | R | R | R |
| 8 | Release candidate is clean | run `commands.build_release` on a clean checkout of the candidate commit | Exit code, artifact path and size; version stamp matches the intended version | R | R | R |
| 9 | Full test suite passes on the candidate | run `commands.test` | "N of N run, 0 failed"; zero run is NOT ASSESSED (minimal with no tests relies on item 10) | R if tests exist | R | R |
| 10 | Smoke on the candidate package, every target | newest `docs/qa/smoke-<date>.md` | The package that will ship (installer, container image, build archive), not a dev build, launched and observed; dated after the candidate commit | R | R | R |
| 11 | Data migration rehearsed | `planning/migrations/<id>.md` | If the schema or a file format changed since the last release: verdict READY, old data opens. Otherwise record "no data change since <tag>" with the diff checked | R if changed | R if changed | R if changed |
| 12 | Stability pass | soak and edge-case results | Long-run and failure-mode tests (`test-engineer`, `site-reliability-engineer`) have results on disk | - | rec | R |
| 13 | Per-artifact gate outcomes recorded | audit, privacy record and release record headers | `SL-SECURITY-REVIEW` on the security audit (it runs after `/app-security-audit` at every mode but solo; at `solo` report `not run: solo mode`); `QL-RELEASE-QUALITY` on the release candidate; `SL-PRIVACY` on the privacy record when personal data is handled. `QL-RELEASE-QUALITY` is normally run by `/app-release` or `/app-team-release`: if it has not run yet, report it as not yet run and name those skills. None may be BLOCK, NOT READY or NOT ASSESSED; a CONCERNS line needs the user's recorded acceptance. `PG-MILESTONE` is optional | - | R* | R* |

## Quality checks

Run, do not read: items 8, 9 and the launch-and-observe of item 10. `qa-lead` re-checks items 1 to 5 against the files and the repo dates (standard and full, unless review mode is solo). Any audit that is older than the code it audits is stale: re-run the skill or report NOT ASSESSED.

## Manual checks

- Is there anything you are shipping that you have not personally used since the last big change?
- Is there a store, platform or legal requirement you know about that is not on this list?

## Panel focus

All four phase gates are required at this transition at standard and full rigor (`gates/README.md`; at minimal `TD-PHASE-GATE` and `PG-PHASE-GATE`). `TD-PHASE-GATE`: reliability, security posture, release risk. `PG-PHASE-GATE`: release plan feasibility. `PD-PHASE-GATE`: the shipped product is the one intended. `DD-PHASE-GATE`: the experience holds on every platform (N/A for an app with no UI platform).

## On PASS

Stage becomes `release`. Next: `/app-release` (and `/app-store-prep` for store channels), `/app-team-release`.
