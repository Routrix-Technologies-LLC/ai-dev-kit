---
name: app-team-harden
description: "Hardening pass before a release: parallel security, performance, accessibility, localization, edge-and-soak and failure-mode lenses, fixes routed to their owners, re-verification, and a sign-off. Use when the user says 'harden', 'get this ready to ship', 'final quality pass', the app is feature complete, or the stage is moving from build to hardening or release."
argument-hint: "[app] [release or milestone label] [--review solo|lean|full]"
user-invocable: true
---

# Team: Harden

The stabilizing pass between feature work and release. A smoke baseline first, then the lenses that find what feature testing misses (security, speed, accessibility, locale, edge cases and endurance, failure behavior) in parallel, then fixes routed to the right owners, then a re-check of what changed, then a sign-off that cannot pass on unchecked ground. It uses the methods of `app-security-audit`, `app-perf`, `app-a11y-audit` and `app-i18n` and calls `app-smoke`, `app-bugfix`, `app-code-review` and `app-story-done` instead of reinventing them.

Writes: `docs/qa/harden/<date>/<agent>.md` (one per agent), `docs/qa/harden/<date>/signoff.md`; the lens reports whose downstream readers expect a fixed home go there instead: `docs/security/audits/<date>.md` (security, read by `app-release` and SL-SECURITY-REVIEW), `docs/qa/a11y-<date>.md`, `docs/qa/perf-<date>.md`, `docs/qa/smoke-<date>.md`. Bug records in `docs/qa/bugs/`, deferred items as rows in `planning/tech-debt.md`.
Next: `app-gate` (hardening to release), `app-team-release`, `app-release`.

## When to use and when not to

- Use once features are done and before the release stage, and again after a risky fix round.
- Whole-app health with no release in mind: `app-team-audit`. A single lens: its own skill. The release itself: `app-team-release`. A change under review: `app-code-review`. An emergency on the shipped version: `app-hotfix`.
- It fixes defects found, not features missing. A finding that needs new design becomes a story or an ADR via the user, not a quiet change.

## Inputs

- The app per orchestration.md section 1. Normal stage is `build` ending or `hardening`; any other stage is announced and the user confirms. This skill never changes the stage.
- Read once and pass distilled: `studio.yaml` (platforms, `min_targets`, commands, hosting), open bugs in `docs/qa/bugs/` or the tracker (count S1 and S2 in scope), the latest audit or harden run (to mark fixed and persisting), `perf-budget.md`, the threat model, the privacy record, the previous release's checklist.
- Decisions asked in Phase 0, because unset must never mean permissive: whether personal data handling changed (privacy lens), the soak duration the user will allow (see Phase 2), whether more than one locale ships.
- Missing `perf-budget.md` means the performance lens reports NO BUDGET and the run cannot end as READY. Missing `commands.test` or `commands.run` makes the matching checks NOT VERIFIED.

## Phase 0: Resolve and announce

Main session: orchestration.md sections 1 and 2. Choose lenses from this table by platform and answers, then print the announce block with every lens either spawned or listed under Not spawned with its reason.

| Lens | Agent | Spawn when | Report path |
|---|---|---|---|
| Security | `security-engineer` (method of `app-security-audit`, including its exposure check before rating); `identity-specialist` if the app authenticates | always | `docs/security/audits/<date>.md`; identity: `docs/qa/harden/<date>/identity-specialist.md` |
| Privacy | `privacy-specialist` (method of `app-privacy-review`) | personal data collected, stored or shared, or changed since the last release; unknown means ask | `docs/qa/harden/<date>/privacy-specialist.md` |
| Performance | `performance-engineer` (method of `app-perf`) | always: a measurable target exists for every app type (startup, latency, memory, bundle, battery) | `docs/qa/perf-<date>.md` |
| Accessibility | `accessibility-specialist` (method of `app-a11y-audit`) | any UI: web, windows, macos, linux, ios, android, extension, TUI | `docs/qa/a11y-<date>.md` |
| Localization | `localization-specialist` (method of `app-i18n`) | more than one locale ships or is planned, or strings are user-facing and not yet externalized | `docs/qa/harden/<date>/localization-specialist.md` |
| Edge and soak | `test-engineer` (with `test-automation-engineer` for UI journeys and minimum-target runs) | always | `docs/qa/harden/<date>/test-engineer.md` |
| Failure modes | `site-reliability-engineer` | deployed services; for client apps scoped to crash reporting, update failure, and offline or interrupted-operation recovery | `docs/qa/harden/<date>/site-reliability-engineer.md` |
| Sign-off draft | `qa-lead` | Phase 6 | `docs/qa/harden/<date>/signoff.md` |

Ask the three decisions above in one AskUserQuestion round before spawning.

## Phase 1: Baseline

Run `/app-smoke` (build, tests, launch-and-observe the critical paths on each target). Record its verdict and report path.

- `FAIL`: stop. Hardening a build that does not work finds noise. Surface the failures, recommend `app-bugfix`, and end with verdict `NOT READY` (reason: smoke FAIL).
- `NOT ASSESSED`: continue only if the user says so after seeing what did not run; the sign-off cannot be READY.
- `PASS` or `PASS WITH WARNINGS`: continue; warnings go to every lens brief.

Also count open S1 and S2 bugs in scope. Open S1 or S2 are known failures; they appear in the sign-off whatever the lenses find.

## Phase 2: Lenses in parallel

Spawn every chosen lens in one message. Each brief (orchestration.md section 3) contains: the app and path, the release label, the scope and build under test (the release build, `commands.build_release`, not a debug build, when the platform differs), the smoke report path, the lens method (point at the named skill's SKILL.md: "follow its method, template and ID scheme (SEC-NNN for security) and its verdict rules, skip its orchestration"; the lenses run as parallel agents because a skill itself runs sequentially in the main session), the exact output path above, the finding format with severity words from `standards/severity.md`, a Coverage section with denominators, and the instruction that nothing is edited: lenses find, they do not fix.

Lens specifics:

- **Edge and soak** (`test-engineer`): boundary and malformed inputs, empty and huge data, rapid repeated actions, interruption and resume (app switch, sleep, rotation, network loss, permission revoked), concurrent use, clock and locale changes, low disk and memory, first run and upgrade-from-previous-version with real old data, minimum supported OS or browser from `min_targets` if a target is available. **Soak:** run for the duration the user chose in Phase 0, scripted and bounded, watching memory, handles, disk growth and error rate. A longer soak than the session allows is delivered as an exact command for the user to run; until its results are supplied, that part is NOT ASSESSED.
- **Failure modes** (`site-reliability-engineer`): for each dependency (database, network, third party, disk) what happens when it is slow, down or wrong; timeouts, retries with backoff, idempotency, graceful degradation; crash recovery and data integrity after a kill; backups and a proven restore; rollback path; crash reporting and logs sufficient to diagnose; no secrets in logs. Reports what it verified by fault injection and what it only read.
- **Security** also runs a delta check: everything that changed since the last audit gets looked at first, then threat-model areas.
- **Accessibility** states plainly what an agent cannot test (live screen reader behavior, switch control, voice control) and lists it as manual checks for the user; those items are NOT ASSESSED until answered.
- **Performance** compares each metric to its budget with method and variance. A metric with no budget is NO BUDGET, not a pass.

Check: each spawned lens's file exists with real content, a Coverage section and a lens result (`CLEAR`, `FINDINGS`, `NOT ASSESSED - why`). Re-brief once for a gap; a second failure is a named BLOCKED gap.

## Phase 3: Consolidate and decide

The main session merges all reports into one table (ID, lens, severity, evidence state, owner, proposed fix). Then:

1. Spot-check every CRITICAL and HIGH finding by re-reading the cited code or output; relabel anything unchecked `UNVERIFIED`. A confirmed CRITICAL is announced to the user immediately.
2. Remove duplicates by root cause, keeping all IDs.
3. Release bar (state it in the table header): no open CRITICAL or S1; no open HIGH or S2 unless the user accepts the risk in writing here; MEDIUM and LOW may be deferred as tech-debt rows.
4. Decision point: for each finding group choose fix now, defer (tech-debt row), or accept the risk. Accepted risks are recorded verbatim with the user's reason in `signoff.md`. A dismissed answer is not acceptance.

Run the formal gates here per review mode (orchestration.md section 7). This skill is not a single-purpose review skill, so its gates are not always-on: at `full`, `SL-SECURITY-REVIEW` (spawn `security-lead` with the gate ID, the audit path and the open findings) and, when the privacy lens ran, `SL-PRIVACY`; at `lean` and `solo` print each as `skipped: <mode> mode` (they run at `/app-release`, or when the user runs `/app-security-audit` or `/app-privacy-review`). Combine verdicts strictest first.

## Phase 4: Fix

Route each "fix now" item to its owner:

| Finding type | Owner | Procedure |
|---|---|---|
| defect, crash, wrong behavior (S1 to S3) | the owning builder from `app-team-feature`'s routing logic for that platform and layer, `escalation-engineer` if intermittent or hard | `app-bugfix` (reproduce, root cause, regression test seen failing then passing) |
| security | `security-engineer` | fix with a test or a reproducer showing the exploit closed |
| performance | `performance-engineer` with the builder | before and after measurement against the budget |
| accessibility | the UI builder for the platform with `accessibility-specialist` | recaptured evidence |
| localization | `localization-specialist` with the UI builder | pseudo-localization or locale run |
| resilience | `site-reliability-engineer` with the backend or platform builder | fault injection repeated |

Builders return the files they will change; the main session asks once for the whole set; then they write. No new features, no refactors outside the finding. Anything that needs a design change is stopped and put to the user as a story or ADR. `code-reviewer` reviews every hardening diff (run `/app-code-review` on it); security-sensitive diffs also go to `security-engineer`.

## Phase 5: Re-verify

Rerun only what the fixes touch, plus the baseline: the affected lens narrowly (the original reproducer, measurement or scan, with the result), the full test suite, `/app-smoke` again on the release build. UI changes get run-and-observe evidence in `docs/qa/evidence/` (orchestration.md section 10). A fix that was not re-verified is still open.

## Phase 6: Sign-off

Spawn `qa-lead` to draft `docs/qa/harden/<date>/signoff.md`. Brief it with the evidence (smoke result, each lens result and path, the merged table with decisions, open bugs, accepted risks) and the verdict rules below verbatim. Do not name a verdict or say which fact decides it. The main session then checks the draft against the same rules; if they disagree, show both and ask, never silently substitute. Gates do not run on the sign-off itself: `QL-RELEASE-QUALITY` belongs to `/app-release`.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Lenses | security, edge and soak (short soak), accessibility (automated scan and keyboard path), performance against whatever budget exists; others announced as not spawned | every relevant lens | every relevant lens, adversarial brief ("find how it breaks"), longer soak |
| Re-verify | affected lenses | affected lenses plus full suite | plus a second smoke on a clean build |
| Gates (by review mode) | solo and lean: none run here | the same | full: `SL-SECURITY-REVIEW`, plus `SL-PRIVACY` when the privacy lens ran |

Phases that may be skipped at minimal: localization (single locale), privacy (confirmed no personal data), failure-mode depth for client apps. Never skipped: Phases 1, 3, 5, 6, the security lens, and edge cases. Rigor changes how deep, never what a sign-off requires.

## Verdicts

First match wins:

1. `NOT READY` - smoke FAIL, an open CRITICAL or S1, an open HIGH or S2 without a recorded user acceptance, a blocking gate verdict, or a failed re-verification.
2. `NOT ASSESSED` - a relevant lens returned nothing, a lens result is NOT ASSESSED (no budget, no way to run, soak or manual accessibility results outstanding), smoke was NOT ASSESSED, or a fix was not re-verified. Name each.
3. `READY WITH NOTES` - bar met; accepted risks, deferred MEDIUM and LOW items, or agent-untestable checks the user confirmed are listed.
4. `READY` - every relevant lens ran with real coverage, nothing above LOW open, no accepted risks.

## Report

```
Hardening: <label>   App: <name>   Stage: <stage>   Rigor: <r>   Review: <m>
Baseline: smoke <verdict> (<path>)   Open S1/S2 before: <n>
Lenses: <run of relevant> ; not spawned: <list with reasons> ; NOT ASSESSED: <list with reasons>
Findings: <n CRITICAL / HIGH / MEDIUM / LOW>   Fixed and re-verified: <n>   Deferred: <n>   Accepted risks: <n>
Re-verification: <what was rerun, results>   Manual checks outstanding for the user: <list>
Sign-off: <path>
```

Then the closing block from orchestration.md section 8.

## Rules for this skill

- Lenses find; only Phase 4 fixes, and only after the user's yes for the file set.
- Never test the debug build and call it the release build.
- Never close a finding without a re-verification; never accept a risk on the user's behalf.
- Never print secrets; cite locations.
- Never advance the stage or tag anything. Recommend `app-gate`.
- Never run destructive data operations against real data; use a copy.
