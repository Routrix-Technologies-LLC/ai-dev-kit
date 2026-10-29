---
name: app-story-done
description: "Close one finished story: check every acceptance criterion against evidence, compare changed files with the story's Files list, report deviations, run the code review gate, actually run the tests, check evidence per change type, then change the story's status. The only way a story closes. Use when the user says a story is done, finished, ready to close, or asks to verify or sign off a story."
argument-hint: "[app] [story-path] [--review solo|lean|full]"
user-invocable: true
disable-model-invocation: true
---

# App Story Done

The only skill that closes a story. It never trusts the builder's summary: it runs the tests itself, checks each acceptance criterion against something it can point to, compares what changed on disk with what the story said would change, reports every deviation as a fact, runs the review gate for the app's review mode, checks that the evidence the change type needs exists and is fresh, and only then changes the story's status.

Writes (after the close decision): the story's `Status` and `Last updated` header fields and its `Completion Notes` section, evidence notes in `docs/qa/evidence/<story>/` (`test-evidence.md` template), tech-debt rows in `planning/tech-debt.md` (`tech-debt-register.md` template) when chosen, the `CHECKPOINT` block in `.studio/state.md`. It never writes to a sprint file: sprint files hold commitments, not status.
Next: the next story (`/app-dev-story`), `/app-qa-plan` or `/app-smoke` when the batch is done.

## When to use and when not to

- Use after `/app-dev-story` (and `/app-code-review` at standard and full rigor), for one story.
- Not to implement or fix anything: this skill reports failures and never repairs them. Not for a readiness check before work (`/app-story-ready`). Not to close a bug (`/app-bugfix` records its own result).

## Inputs

- `studio.yaml`: `commands:`, `platforms`, `modes`, `rules:`. None: offer `/app-adopt` or `/app-start` and stop.
- The story: the argument; else the checkpoint's current task if it names a story; else the stories whose status is In Review or In Progress (ask which if several); else ask for the path. No story files at all: offer `/app-plan`.
- The `.studio/state.md` checkpoint (baseline dirty files, last Run result), the story's `Files` list, `docs/qa/evidence/<story>/`, any `docs/qa/reviews/*.md` naming this story or its files.
- Spec, ADR and contract text by section, only what the criteria and deviations need.

A story already Complete: say so and stop. A story still Draft, Ready or Blocked with no implementation: say `/app-dev-story` has not run (or the story is Blocked, and why) and give verdict NOT ASSESSED with that reason (no evidence exists to assess). Status owners: `/app-plan` writes Draft, Ready or Blocked at creation, `/app-dev-story` sets In Progress and In Review, and this skill alone sets Complete. This skill never moves a story back to In Progress; `/app-dev-story` does that when it reworks an In Review story.

## Checklist (copy and tick)

```
- [ ] Phase 1: app, story, rigor and review mode; plan announced
- [ ] Phase 2: what the story is checked against
- [ ] Phase 3: tests, build and lint run now
- [ ] Phase 4: each criterion against evidence
- [ ] Phase 5: evidence per change type
- [ ] Phase 6: deviations and scope
- [ ] Phase 7: review gates
- [ ] Phase 8: report, verdict, close decision, writes
- [ ] Phase 9: next story, checkpoint, closing block
```

## Phase 1: Resolve and announce

`orchestration.md` sections 1 and 2. Read the story in full: `Change type` (one or several), acceptance criteria (IDs), QA test cases, `Files`, Out of Scope, dependencies, Completion Notes if any. Note the rigor and review mode. Print the plan block with the agents this run may use (`code-reviewer`, `principal-engineer`, `qa-lead`, `product-manager` per the review mode in Phase 7) and which gates run.

## Phase 2: What the story is checked against

Read by section, never whole documents.

- **minimal:** the story's own criteria are the spec.
- **standard:** the feature spec requirements the story cites (`REQ-` IDs) and the API contract fragment or UX spec states if the story touches them.
- **full:** as standard, plus each cited ADR's decision and consequences sections and the architecture sections on trust boundaries and budgets the change touches.

A cited document that does not exist is recorded as a gap: any deviation that would be judged against it is NOT ASSESSED, not clean.

## Phase 3: Run the checks now

Run, from the repo root, and report command, exit code and counts. Reading a prior run output or the builder's summary does not count.

1. `commands.build` (`build_release` when `rules:` names the build the user tests from).
2. `commands.lint`.
3. `commands.test`, and `commands.e2e` when the story is UI or Integration and the command is set.

Heavy runs (a release build, a full suite, an emulator) go through `~/Tools/agent_locks/run_locked.sh cpu <command>` (`gpu` for anything that opens a window or uses the GPU) when that helper exists, otherwise one at a time; exit code 75 means the user is gaming, so stop and report those checks NOT ASSESSED. Never run anything that takes focus or injects input on the live desktop: a `commands.e2e` that needs a visible window or real keystrokes is not run, and that check is NOT ASSESSED unless the user says they are away.

A command that fails: BLOCKING, quote the first failing lines. A command that is empty, or a tool that is not installed: that check is NOT ASSESSED with the reason; it is never a pass. A failing test that also fails on the baseline (you may check with `git stash` only if the user agrees; otherwise report that you could not tell) is reported as pre-existing only with that proof. Confirm the story's new tests are in the run output by name.

## Phase 4: Each criterion against evidence

Build one row per acceptance criterion. The kinds of evidence, in order of strength:

| Evidence | Counts as | Rules |
|---|---|---|
| A test that ran in Phase 3 and names the criterion | COVERED | Read the test: it must assert the criterion's outcome. A test that cannot fail (no assertion, mocks the thing under test, asserts a constant) is not coverage; say so |
| A retained capture or output you opened, in `docs/qa/evidence/<story>/` | COVERED (look) | Never describe an image you have not opened. The Run result line from the checkpoint is `app-dev-story`'s description, quoted as such |
| The user's recorded answer (asked in plain words: "Does <criterion> hold on a build with the change?") | COVERED (user-asserted) | Allowed for behaviour that has no automated check and nothing visible; recorded as `user, <date>, build <x>`. Not accepted alone for a criterion about something on screen |
| Reading the code | nothing | Code says what should happen, not what the app does. Never COVERED |
| Needs a long-running or live-traffic observation (soak, rollout, real device matrix) | DEFERRED | Name the owner and the check (`/app-smoke`, `/app-perf`, `/app-team-harden`); does not block |

```
| Criterion | Covered by | Status |
|---|---|---|
| AC-1: <text> | <test path::name (ran, passed)> | COVERED |
| AC-2: <text> | docs/qa/evidence/<story>/01-<what>.png (opened) | COVERED |
| AC-3: <text> | none | UNTESTED |
| AC-4: <text> | user, <date>, build <x> | COVERED (user-asserted) |
| AC-5: <text> | cannot be evaluated: names no observable outcome | NOT ASSESSED |
```

A criterion that names no observable outcome ("works well") is NOT ASSESSED and a finding against the story. A failing criterion is FAILS with the reason. UNTESTED means nothing in the evidence would fail if the criterion broke. For Logic, Integration, Data and Security criteria it is BLOCKING at standard and full, and at minimal whenever a test harness exists (`standards/testing.md`: evidence is not relaxed by rigor); at minimal with no harness it is a note plus the recommendation `/app-test-setup`. A UI or Visual criterion with no retained capture is UNTESTED and BLOCKING at every rigor.

## Phase 5: Evidence per change type

Take the story's change types (`standards/testing.md` is the authority; the table is the working summary, and where the two differ the standard wins). Each missing item is BLOCKING unless marked advisory.

| Change type | Evidence required |
|---|---|
| Logic | Unit tests that ran and passed (Phase 3) |
| Integration or API | An integration or contract test run, or a recorded manual run of the real path with its output (`docs/qa/evidence/<story>/test-run.md`); for an API change, the contract file updated and consumers checked |
| UI | Retained capture of each screen and state touched, per platform and form factor the story names, light and dark if the app themes, and a keyboard-only pass noted in the evidence note (or listed as NOT VERIFIED with the reason), plus any accessibility scan output the story asks for |
| Visual | Retained captures at the target sizes and themes, plus the `design-director` or `ui-designer` sign-off line in the evidence note for a design-system change (`DD-VISUAL` is not run here) |
| Data (schema or format) | Migration run on a copy of realistic data, forward and (where the story promises it) back, row or record counts before and after, old data still opens in the new build (`/app-data-migration` record) |
| Config | A smoke check: the app builds, starts and does its main path with the new config. ADVISORY per `standards/testing.md`, blocking only if the app's `rules:` say so |
| Infra | The pipeline or deployment run (log excerpt) or plan, dry-run or validate output, a health check after, and a rollback or restore noted for risky changes |
| Security | Tests of the abuse cases (the attack is refused, not only the happy path), dependency audit output where dependencies changed, and a `security-engineer` review (Phase 7) |
| Performance | Before and after measurement against the committed budget (`perf-budget.md`), with method, device and build type; BLOCKING if a budget exists, else ADVISORY |
| Docs | ADVISORY: the doc exists, links resolve, commands and paths in it were run or checked |

Rigor effect: rigor never relaxes a row. It changes which documents the criteria are checked against (Phase 2) and how much is written down, not what must work. Where a type has no test harness at minimal rigor, say so, and the run-and-observe evidence stands in for the missing tests only for UI and Visual changes.

**Run result.** Find the `Run result:` line in the story file (filled by `/app-dev-story`), cross-checked against the checkpoint if its current task names this story and the evidence note. `OBSERVED` with a path: confirm the file exists, open it, and check the evidence is not older than the changed files (compare the evidence note's recorded commit and file list, and file modified times, with the changed files; report `evidence older than <file>`, advisory). `N/A`: accept only if the reason says why nothing is observable; "it is a logic change" is not one when the change alters what a user sees or receives. `NOT VERIFIED` on a UI or Visual story: BLOCKING. No line at all: advisory ("confirm the app was launched and looked at"), blocking for UI and Visual. A story with no change type declared: advisory, state it.

## Phase 6: Deviations and scope

Facts, not judgments. Each deviation is **BLOCKING** (contradicts the spec, an ADR, a contract, or a standing `rules:` entry), **ADVISORY** (drifts but works the same; the user decides), or **OUT OF SCOPE** (for awareness).

1. **Scope:** list changed files (`git status --porcelain`, and `git diff --name-only <base>` when the work is committed) minus the baseline dirty files from the checkpoint, against the story's `Files` list. A changed file the list does not name is OUT OF SCOPE; a listed file with no change is noted. A file under the story's Out of Scope section is BLOCKING. A story with no `Files` list: use the checkpoint's files in progress; if neither exists, `Scope: NOT ASSESSED - the story lists no files`. A clean working tree: `Scope: not checked - no uncommitted changes to compare` (say how you looked for committed changes).
2. **Spec and contract:** search the changed files for the names, fields, routes or messages the cited requirements and contract use; a mismatch is BLOCKING.
3. **ADR and architecture:** search for patterns the cited ADR rejects (full rigor; standard for a foundation-level ADR).
4. **Hardcoded values:** secrets, URLs, keys, magic limits that belong in configuration; a committed secret is BLOCKING and is also reported to the user at once.
5. **New dependencies:** any addition to a manifest or lock file not named in the story or `docs/stack-reference.md` is ADVISORY (BLOCKING at full) and routed to `compliance-specialist` in review.
6. **Unfinished work:** `TODO`, `FIXME`, commented-out code and debug output added by the change (count with the denominator: "3 in 14 changed files").
7. **Strings and accessibility:** new user-facing strings not externalized when the app localizes, and UI without the accessibility notes the UX spec requires: ADVISORY.

## Phase 7: Review gates

Apply the review mode (`orchestration.md` section 7). Print each gate that runs or `<GATE-ID> skipped: <mode> mode`. Agents read `gates/<id>.md` themselves; give them the gate ID and the context fields.

| Gate | Owner | solo | lean | full |
|---|---|---|---|---|
| `PE-CODE-REVIEW` | `principal-engineer` | skipped | **runs for a non-trivial change** (more than a few lines, or any change an agent wrote; always-on at lean per `gates/README.md`) | runs |
| `QL-TEST-COVERAGE` | `qa-lead` | skipped | skipped | runs (not for Config, Docs) |
| `PM-ACCEPTANCE` | `product-manager` | skipped | skipped | runs |

- **PE-CODE-REVIEW:** at lean, a trivial change (a few lines written by the user) prints `PE-CODE-REVIEW skipped: lean mode, trivial change`; anything an agent wrote is non-trivial. Verdicts: APPROVE passes, CONCERNS is ADVISORY (listed), REJECT is BLOCKING. First look for a code review report in `docs/qa/reviews/` that covers this story's files and is not older than the last change to them (compare the files it lists and modified times). Pass that report path in the brief; `principal-engineer` judges the report and the diff. No fresh report: say so and give the diff and the file list directly, and recommend `/app-code-review` before closing. A report verdict of CHANGES REQUIRED is BLOCKING; NOT ASSESSED carries through. If the change touches sensitive paths (authentication, authorization, cryptography, payments, personal data, IPC, updaters, network exposure, file parsing) and no review in the report involved `security-engineer`: ADVISORY at solo and lean, BLOCKING at full.
- **QL-TEST-COVERAGE:** `qa-lead` gets the story, the test paths found in Phase 3 and 4, the QA test cases and the criteria; judges whether the tests cover what was specified, not just that files exist. ADEQUATE passes, GAPS is ADVISORY, INADEQUATE is BLOCKING.
- **PM-ACCEPTANCE:** `product-manager` gets the criteria table, the spec requirements and the evidence; returns ACCEPTED, CONCERNS or REJECTED (or NOT ASSESSED naming the missing input). ACCEPTED passes, CONCERNS is ADVISORY, REJECTED is BLOCKING.

Combine gate results by the strictest rule (section 7). Spawn the gates that run in one message, in parallel. A gate that returned NOT ASSESSED is never a pass; supply its input and rerun, or carry it to the verdict.

**Reviewed by** is never blank: `principal-engineer (PE-CODE-REVIEW)`, or `/app-code-review report <path>`, or `self, no independent review` (solo mode, or no implementation files).

## Phase 8: Report, verdict, close decision

```
## Story Done: <title>
Story: <path>   Types: <types>   Date: <today>   Rigor: <r>   Review: <mode>

### Checks run now
Build: <command> exit <n> | NOT ASSESSED: <why>
Lint: <command> exit <n> | NOT ASSESSED: <why>
Tests: <command>: <passed/failed/skipped>; story tests in run: <yes|no> | NOT ASSESSED: <why>

### Acceptance criteria: <X of Y covered>
<Phase 4 table>

### Evidence
Required for <types>: <list>   Found: <list>   Missing: <BLOCKING/ADVISORY each>
Run result: <the line> (evidence fresh | older than <file> | no stamp)

### Deviations
<NONE, or each: BLOCKING | ADVISORY | OUT OF SCOPE - description - reference>
Scope: <N changed files, M outside the Files list> | NOT ASSESSED: <why>

### Review
Gates: <GATE-ID: VERDICT, ... | skipped lines>   Reviewed by: <value>

### Verdict: <COMPLETE | COMPLETE WITH NOTES | NOT ASSESSED | BLOCKED> - <why>
```

**Verdicts, first match wins:**

1. **BLOCKED**: a criterion fails; build, lint or tests fail; a BLOCKING evidence gap or deviation stands; a gate returned a blocking verdict.
2. **NOT ASSESSED**: a required check could not run (empty or uninstalled command), a criterion cannot be evaluated, a gate returned NOT ASSESSED and its input was not supplied, the scope check had nothing to compare while the story was supposed to have one, or a document a deviation would be judged against is missing. Name each and what would settle it. It never hides a failure and is never a pass.
3. **COMPLETE WITH NOTES**: everything passes or is DEFERRED, with advisory items, accepted risks or user-asserted evidence listed. Information lines (an absent sprint plan, stale-evidence timestamps) do not by themselves downgrade.
4. **COMPLETE**: every criterion covered, every check ran and passed, nothing advisory.

**The close decision.**

- **COMPLETE:** announce the status change and make it. Invoking this skill by name is the request to close a clean story.
- **COMPLETE WITH NOTES:** ask once, last in the reply: close and keep the notes in Completion Notes (Recommended) / close and log the advisory items as tech debt / do not close yet. 
- **BLOCKED or NOT ASSESSED:** recommend not closing, list exactly what must change, and ask: do not close yet (Recommended) / close anyway accepting the listed gaps. This ask is mandatory in every mode (`orchestration.md` section 6). Closing anyway writes the accepted gaps and "closed over <verdict> by the user on <date>" into Completion Notes.

A skipped, dismissed or empty answer is not an answer: ask again in plain text. Never repair a failing criterion yourself; report it and ask what to do.

**On close, in order:**

1. Set the story `Status` to Complete and `Last updated` to today (the header field names in `templates/story.md`).
2. Fill the story's `Completion Notes` section: completed date, criteria count with deferred items, deviations, evidence paths, test command and result, Reviewed by, and any closed-over gaps.
3. Write or update `docs/qa/evidence/<story>/evidence.md` from `templates/test-evidence.md` with the Phase 3 and 4 results (commands, counts, criteria table). Keep images small.
4. "Log as tech debt": one row per advisory deviation in `planning/tech-debt.md` (`templates/tech-debt-register.md`; ID one above the highest existing, today's date; create the file from the template when absent).
5. Print a suggested commit (`git add <the changed files and the story path>` and a message naming the story). Never run it.

**On "do not close yet":** change no story file. List what the user flagged.

## Phase 9: Next story, checkpoint, close

**Next story.** Read the story files in the same epic and the sprint plan if present (the plan gives the commitment and order; the story files give the status). In order: a story In Review, then In Progress, then the first Ready by the plan's order (or the epic's number order at kanban). Print `Next up: <story> - <one line> - /app-dev-story <path>` (or `/app-story-done <path>` for In Review). If nothing remains in the epic: say the epic's stories are all Complete and recommend `/app-qa-plan` or `/app-smoke`; if stories remain only as Blocked or Draft, name each with its blocker and do not claim the work is done.

**Checkpoint.** Overwrite the `CHECKPOINT` block in `.studio/state.md`: current task `app-story-done <path>: <verdict>, closed|left open`, next step, blocked on, files in progress (none when closed), open questions (tech debt logged: N, or none).

End with the closing block (`orchestration.md` section 8):

```
Verdict: <COMPLETE | COMPLETE WITH NOTES | NOT ASSESSED | BLOCKED> - <story path>: <one line why>
Gates: <PE-CODE-REVIEW: V, QL-TEST-COVERAGE: V, PM-ACCEPTANCE: V | none run (solo)>
Wrote: <story, evidence, tech-debt and checkpoint paths | none>
Next: </app-dev-story <path> | /app-story-done <path> | the fix | /app-smoke> (<why>)
```

## Review mode and rigor

| Setting | What changes |
|---|---|
| Rigor minimal | Story criteria are the spec; evidence rows are not relaxed; UNTESTED blocks wherever a harness exists; look never waived |
| Rigor standard | Spec and contract checks; all evidence rows; any UNTESTED automatable criterion blocks |
| Rigor full | ADR and architecture checks on top of standard; the gates below run if review mode is full |
| Review solo | No gates; Reviewed by is `self, no independent review` unless a fresh `/app-code-review` report exists |
| Review lean | `PE-CODE-REVIEW` runs for a non-trivial change |
| Review full | `PE-CODE-REVIEW`, `QL-TEST-COVERAGE`, `PM-ACCEPTANCE` run |

## Rules for this skill

- Never close a story on a builder's summary, a described check, or code reading alone.
- Never repair code, tests or evidence. Report, and recommend `/app-dev-story` or `/app-bugfix`.
- Never close a BLOCKED or NOT ASSESSED story without the user's explicit yes, in every mode.
- Never take focus or inject input on the live desktop to gather evidence.
- Never pass an empty command, an unopened image, an unreadable evidence file or a skipped gate as a pass.
- Every count states its denominator.
- Never commit, tag, push or deploy. Print the suggested commit only.
- Never start the next skill.
