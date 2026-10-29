---
name: app-bugfix
description: "Fix a bug properly: reproduce it first, state the root cause, write a regression test and watch it fail, fix, watch it pass, run the rest, review. Uses escalation-engineer for hard or intermittent bugs. Use when the user reports a bug, crash, wrong behavior or regression, pastes a stack trace or error, or says fix this bug. Not for an emergency on the released version (app-hotfix)."
argument-hint: "[app] [BUG-NNNN | description | stack trace] [--review solo|lean|full]"
user-invocable: true
---

# App Bugfix

Fixes one bug in a way that proves the fix. The order is fixed: reproduce, find the root cause, write a test that fails because of the bug, see it fail, fix, see it pass, run everything else, have the change reviewed. Skipping the "see it fail" step is how a regression test ends up testing nothing, so it is not skippable.

Writes: a bug record `docs/qa/bugs/BUG-NNNN-<slug>.md` (`templates/bug-report.md`), the fix and the regression test, evidence under `docs/qa/evidence/BUG-NNNN/`, the `CHECKPOINT` block in `.studio/state.md`.
Next: `/app-story-done` if the fix belongs to an open story, otherwise the user's own check on a build, then release planning.

## When to use and when not to

- Use for a defect in code in the repo: wrong behavior, crash, regression, failing test caused by a real bug.
- Not for an emergency on a released version that needs a branch from the release tag and a rollback plan: `/app-hotfix`. If the bug is S1 and live, say so and offer it; the user decides.
- Not for new behavior (`/app-spec`, `/app-plan`), for an upgrade that broke things (`/app-upgrade`), or for tuning speed (`/app-perf`).
- Triaging a backlog of bugs (ordering many) is `qa-lead`'s job; this skill fixes one.

## Inputs

- `studio.yaml`: platforms, stack, `commands:`, `rules:`. None: offer `/app-adopt` or `/app-start` and stop.
- The bug: an ID (`docs/qa/bugs/BUG-NNNN-*.md`, or the app's tracker if `paths.bugs` maps one), or a description, or a stack trace or log excerpt. Nothing given: ask for the symptom, the steps, and the expected result.
- `commands.test` and `commands.build` are needed to prove anything. If `commands.test` is empty, offer `/app-test-setup` first; without a runnable test command the verdict cannot be FIXED.

## Checklist (copy and tick)

```
- [ ] Phase 1: app, bug record, severity and priority
- [ ] Phase 2: reproduced (exact steps, failing output kept)
- [ ] Phase 3: root cause stated and evidenced
- [ ] Phase 4: regression test written and seen failing for the right reason
- [ ] Phase 5: fix applied (files asked once)
- [ ] Phase 6: new test passes, whole suite and build run, bug re-observed gone
- [ ] Phase 7: sibling search and code review
- [ ] Phase 8: bug record, checkpoint, closing block
```

## Phase 1: Intake and bug record

Follow `orchestration.md` sections 1 to 3. Read an existing record in full. For a new bug, allocate the ID (highest `BUG-NNNN` in the bugs folder plus one, zero-padded to four digits; `BUG-0001` when none) and write the record directly (a new studio document) from `templates/bug-report.md`: title, environment (version or commit, platform and OS, device or browser, data state), steps, expected, actual, frequency (Always, Often with n of n tries, Sometimes, Once; with how you know), regression (was it working in an earlier version; if so, when), evidence so far.

Rate **severity** S1 to S4 from impact using the table in `standards/severity.md` (S1 is data loss that is not recoverable, a security breach, an unusable app or no acceptable workaround on a core promise; unrecoverable data loss is S1 and any other data loss is at least S2), and propose **priority** P0 to P3 from urgency. Severity is a fact about impact; priority is the user's call: ask when it is S1, S2 or P0/P1. An S1 is written as `proposed S1` until `qa-lead` or the user confirms it; the agent who fixes a bug never downgrades it. A security vulnerability is not discussed in a public tracker or commit message; note it for `security-lead` and use `/app-security-audit` on it.

Print the plan block. Choose the owner by the routing used in `app-dev-story` (the builder for the layer and platform where the symptom appears, plus the language specialist from `studio.yaml`; never an agent for a platform the app lacks). Spawn `escalation-engineer` instead of, or beside, the builder when any of these hold: the bug is intermittent or timing dependent, involves concurrency, memory growth or corruption, a crash needing a dump or native debugger, could not be reproduced by the first attempt, was already attempted by someone and failed, or only occurs on one OS, device or build type.

## Phase 2: Reproduce first

Nothing is fixed before it is reproduced. The owner (or `escalation-engineer`) reproduces it in the real project using the steps in the record: run the app or the failing command (headless, offscreen or through a test seam: never take focus or inject keyboard or mouse input on the user's desktop; a reproduction that needs real input is NOT VERIFIED unless the user says they are away), then capture the actual result verbatim (error text, stack trace, exit code, response body, screenshot per `app-dev-story/references/run-and-observe.md`). Write the evidence under `docs/qa/evidence/BUG-NNNN/` and add a "Reproduced" line to the record naming the exact commands and the output.

- A crash report or stack trace with no steps: find the code path from the trace, then construct the smallest input or sequence that triggers it.
- Intermittent: measure the rate (N failures in M runs, with the loop command), vary one condition at a time (timing, data, order, environment), and look for what the failing runs share. A long stress loop is a heavy run: use the lock (below). The reproduction may be a stress loop or a deterministic seam (inject a delay, a fake clock, a forced ordering). A bug whose reproduction is "1 in 20" is not yet reproduced deterministically; keep going to a reliable trigger before Phase 4 or label the test probabilistic and say so.
- Cannot reproduce after three distinct, recorded attempts (including the reporter's environment and data where you can match them): stop. Do not fix blind. Update the record with what was tried and the information that would help (version, OS, steps, logs, data), and finish with CANNOT REPRODUCE.

Check: the record holds a reproduction with real output, or the attempts list for CANNOT REPRODUCE.

## Phase 3: Root cause

State the cause in the record, in a paragraph that names: the file and function (`file:line`), the condition under which it goes wrong, why that produces the symptom, and why the existing tests and reviews missed it. Distinguish cause from symptom ("the list is empty" is a symptom; "the cache key ignores the locale so a stale entry is returned" is a cause). Back it with evidence you produced: a debugger or log observation, a bisect result (`git bisect` with the reproduction as the test, for regressions; run it in a separate `git worktree` so the user's working tree and uncommitted changes are never touched), or a minimal failing case.

If the cause is still a hypothesis, label it `HYPOTHESIS` with the observation that would confirm it, and note that the verdict cannot be FIXED without it being confirmed or the fix being proven by Phase 4 and 6. A fix that works for reasons nobody can explain is FIXED WITH NOTES at best.

## Phase 4: Regression test, seen failing

`test-engineer` (or the layer's builder for a small bug; `test-automation-engineer` for a UI journey) writes the smallest test that encodes the correct behavior and fails because of this bug. Name the scenario and the expected result; arrange, act, assert; no real network, clock or randomness in a unit-level test; fixtures inside the test. Put it where the app keeps tests for that layer.

Then the main session runs it **against the unfixed code** and reads the output:

1. It must fail.
2. It must fail for the right reason: the failure message is the symptom from the record, not a typo, import error or setup problem.
3. If it passes before the fix, the fixture does not reach the bug (a common cause: data that never triggers the ordering, the cache or the boundary). The test is worthless; rework the fixture and run again. Never proceed with a test that has only ever been seen passing.

Record the failing command and output in the record. For a bug no automated test can reach (pure visual rendering, an OS-integration behavior with no test seam), the equivalent is a written manual reproduction plus a before capture, and the verdict cannot be better than FIXED WITH NOTES; say why a test was not possible and name the closest automated check added (for example a unit test of the extracted logic).

## Phase 5: Fix

List the files the fix will edit (existing source) and ask once, with the root cause quoted: "May the owner edit these files?" Options: approve as listed / change the list / stop. The question is last in the reply. The owner makes the **smallest change that removes the cause**: no refactor, no drive-by cleanup, no unrelated fixes, no special-casing the test's input. If the correct fix is larger than a bug fix (a design change, a migration, a contract change), stop and propose a story (`/app-plan`) or `/app-data-migration` and `/app-api` as fits; the verdict is BLOCKED with that reason, with the regression test left in place and marked as a known failing test only if the user agrees.

The language specialist reviews the diff read-only if the fix is non-trivial (rigor standard and full). Data repair for already-corrupted data is separate: a script that modifies user data is a destructive data operation, designed with `database-engineer`, rehearsed on a copy, and run only after the user's explicit yes.

## Phase 6: Prove it

Run the commands yourself and read the output; take no one's word. Heavy runs (a full suite, a release build, a long stress loop, an emulator) go through `~/Tools/agent_locks/run_locked.sh cpu <command>` (`gpu` for anything that opens a window) when that helper exists, otherwise one at a time; exit code 75 means the user is gaming, so stop and report what is still to run as NOT VERIFIED.

1. The regression test: it must now pass (record command and output).
2. The whole suite, `commands.test`, plus `commands.e2e` for a UI bug when set. Before the fix you recorded which tests were already failing (run the suite once on the unfixed code at the start of Phase 4 when it is affordable); a failure that is new after the fix is yours to resolve, a pre-existing failure is listed by name and not blamed or hidden.
3. `commands.build` and `commands.lint`.
4. Re-run the Phase 2 reproduction by hand and confirm the symptom is gone. For anything a user sees, run and observe per `app-dev-story/references/run-and-observe.md` and keep an after capture beside the before capture. One line:

```
Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why> | N/A - <why nothing is observable>
```

For an intermittent bug, repeat the stress loop at least as many times as made the bug appear before (N runs with zero failures, stated with the denominator and the earlier failure rate); absence in a few runs is not proof.

An empty or failing command is reported as it is: failing is BLOCKED, empty is `NOT VERIFIED: commands.<key> is not set`.

## Phase 7: Siblings and review

**Siblings.** Search the code base for the same pattern that caused the bug (same API misuse, same unchecked condition, same cache key shape). List every hit with `file:line` and the denominator ("4 similar sites in 212 files"). Do not fix them in this change unless they are the same bug in the same function; report the rest in the record and offer stories or tech-debt rows.

**Review.** Review mode solo: skipped, announced (`code review skipped: solo mode`). Lean and full: spawn `code-reviewer` (read-only: it returns findings and the main session writes anything that goes in the record) on the diff (read-only, in one message with `security-engineer` when the code is on a sensitive path as `app-code-review` lists them), briefed with the root cause, the test and the files. Verify each finding as `app-code-review` Phase 4 does before acting; a VERIFIED CRITICAL or HIGH goes back to the owner once. For a larger diff or a wider look, recommend `/app-code-review`.

## Phase 8: Record and close the run

1. Update the bug record: status Confirmed once reproduced, In progress during the fix, then Fixed (never Verified or Closed on your own word: those wait for the user's own confirmation on a build, which they say and you then record), root cause, the fix summary, files changed, regression test path, the before and after evidence, siblings found, the review result, and `Verified by: <commands run and results>`.
2. If the fix belongs to an open story, say so and recommend `/app-story-done`; do not touch the story.
3. Overwrite the `CHECKPOINT` block in `.studio/state.md`.
4. Print a suggested commit message (cause and fix, bug ID). Never commit, push or deploy.

## Rigor and review mode

| Setting | Effect |
|---|---|
| Rigor (any) | Reproduction, root cause, a regression test seen failing, and a passing run of the suite are required at every rigor: they are what must work |
| minimal | Bug record may be a short section; code review and sibling search are brief |
| standard, full | Full bug record; siblings listed; language specialist reviews non-trivial fixes; at full an intermittent bug needs the repeated-run proof written down |
| Review solo | Skip `code-reviewer`; announce it |
| Review lean, full | `code-reviewer` runs (plus `security-engineer` on sensitive paths) |

This skill runs no gate. `Gates: none run (<mode>)`.

## Verdicts

First match wins. This skill has no NOT ASSESSED value; a fix that could not be proven is not FIXED.

1. **BLOCKED**: the user declined the file ask; the fix is larger than a bug fix; the regression test could not be made to fail or the suite or build fails after the fix; the test or build command cannot be run so nothing was proven; a VERIFIED CRITICAL or HIGH review finding stands; the owner stopped early.
2. **CANNOT REPRODUCE**: three recorded attempts did not reproduce it. No fix was made. The record lists what is needed from the reporter.
3. **FIXED WITH NOTES**: the fix is in and the regression test failed before and passes after, with something to disclose: root cause still a hypothesis, no automated test possible (manual evidence instead), intermittent bug proven only by a bounded repeat run, Run result NOT VERIFIED for a visible bug, pre-existing failing tests, siblings found, unverified review findings.
4. **FIXED**: reproduced, root cause stated and evidenced, test seen failing for the right reason and passing after, whole suite, build and lint pass, symptom re-observed gone, review clean or skipped by mode with that announced.

## Report

```
## Bugfix: BUG-NNNN <title>   Severity: S<n>   Priority: P<n>
Owner: <agent(s)>   Escalation: <escalation-engineer | not needed: why>
Reproduced: <command or steps> -> <actual output, one line>
Root cause: <file:line, condition, why it was missed> (CONFIRMED | HYPOTHESIS)
Regression test: <path::name>   Before fix: FAILED (<message, one line>)   After fix: PASSED
Fix: <files changed, one line>
Suite: <command>: <counts>; new failures: <none | list>; pre-existing: <none | list>
Build: <exit>   Lint: <exit>   Run result: <the one line>
Siblings: <N similar sites in M files | none found>
Review: <code-reviewer result | skipped: solo mode>
Notes: <list | none>
```

End with the closing block (`orchestration.md` section 8):

```
Verdict: <FIXED | FIXED WITH NOTES | CANNOT REPRODUCE | BLOCKED> - <one line why>
Gates: none run (<mode>)
Wrote: <bug record, fix, test, evidence, checkpoint paths>
Next: </app-story-done <story> | ask the reporter for <info> | /app-plan for the larger fix | the user confirms on a build> (<why>)
```

## Rules for this skill

- Never fix a bug that was not reproduced, and never fix blind.
- Never take focus or inject input on the live desktop to reproduce or to observe.
- Never trust a regression test that has not been seen failing against the unfixed code, for the right reason.
- Never edit existing source before the Phase 5 ask, and never outside the approved list.
- Never weaken, skip or delete an existing test to get green.
- Never include unrelated cleanup, refactoring or sibling fixes in the change.
- Never run a data repair on real user data without a rehearsal on a copy and the user's explicit yes.
- Never commit, push, tag or deploy. Never mark the bug Verified or Closed on your own word.
- Do not start the next skill. Recommend it.
