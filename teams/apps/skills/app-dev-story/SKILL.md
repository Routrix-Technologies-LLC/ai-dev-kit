---
name: app-dev-story
description: "Implement one story: route it by layer and platform to the right builders, write tests with the change, run build, lint and tests, run and observe the result, update the story's Files list. Never closes the story. Use when the user says to build, implement, code or start a story."
argument-hint: "[app] [story-path] [--review solo|lean|full]"
user-invocable: true
disable-model-invocation: true
---

# App Dev Story

Implements one story. The main session checks the story can start, routes it to the builders its layers and platforms need (from the roster and `studio.yaml`), has tests written with the code, runs the app's own build, lint and test commands, launches the result and looks at it, then records what changed in the story and the checkpoint. It stops there: `app-story-done` is the only skill that closes a story.

Writes: source and tests (by the builders), evidence under `docs/qa/evidence/<story>/` (`test-evidence.md` template), the story's `Status` and `Last updated` header fields, its `Files` table and its `Run result` line, the `CHECKPOINT` block in `.studio/state.md`.
Next: `/app-code-review` (recommended at standard and full rigor), then `/app-story-done`.

## When to use and when not to

- Use for one story that is Ready, In Progress (to resume) or In Review (to rework after a review or a blocked `/app-story-done`).
- Not for a story that has not been checked: run `/app-story-ready` first. Not for a defect: `/app-bugfix`. Not for an emergency on the released version: `/app-hotfix`. Not for a throwaway experiment: `/app-prototype`. Not for several stories at once: run this skill per story (`/app-team-feature` does that).

## Inputs

- `studio.yaml` (platforms, stack, `commands:`, `specialists:`, `rules:`, `modes:`). None: offer `/app-adopt` or `/app-start` and stop (`orchestration.md` section 1).
- The story file. The argument; else the story the checkpoint in `.studio/state.md` names (confirm it); else list the stories whose status is Ready or In Progress and ask. No stories exist: offer `/app-plan` and stop.
- Optional but read by section when the story points at them: the feature spec (`REQ-` IDs), the UX spec and design language (UI stories), the API contract, the ADRs it names, `docs/stack-reference.md`.
- The `commands:` it needs: `build`, `test`, `lint`, `run`. An empty command is stated, never skipped silently: see Phase 2.

## Checklist (copy and tick)

```
- [ ] Phase 1: app and story resolved, plan announced
- [ ] Phase 2: can it start (status, dependencies, ADRs, commands, clean baseline)
- [ ] Phase 3: routed, files listed, one ask
- [ ] Phase 4: builders ran with full briefs
- [ ] Phase 5: build, lint, tests run and read
- [ ] Phase 6: run and observe, one Run result line
- [ ] Phase 7: story, evidence and checkpoint updated; closing block
```

## Phase 1: Resolve and announce

Follow `orchestration.md` sections 1 to 3. Read the story in full: type, layers, acceptance criteria, QA test cases, Files (planned), Out of Scope, dependencies, the spec and ADR text it embeds. Take the **change types** from the story (`standards/testing.md`: Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance, Docs). A story with no type is a gap: ask the user which types apply and write them into the story (the one edit allowed before Phase 3's ask), since evidence and closing depend on them.

Print the plan block (section 2) naming the builders chosen in Phase 3 and what is not spawned and why.

## Phase 2: Can it start

Check each, and stop on a failure (no agent runs; go to Phase 7 with BLOCKED):

| Check | Stop when | Otherwise |
|---|---|---|
| Story status | Draft, Blocked, or Complete | Ready, In Progress or In Review continues (In Review goes back to In Progress at the Phase 3 ask). Draft: refuse to start, say the story has not passed a readiness check, and offer `/app-story-ready` (it can mark a READY Draft as Ready after the user's yes). Blocked: quote its `Blocked reason` line. Complete: say it is closed |
| Dependencies | A dependency story is not Complete | Ask: proceed anyway (recorded under notes) / stop / the dependency is actually done (then ask before editing its status) |
| ADRs the story names | Any is Proposed, Deprecated or Superseded (name the ADR and the action: `/app-adr accept`, or point the story at the successor) | Do not read whole ADRs: the story carries the decision summary. If the story records an ADR version or date and the ADR now differs, ask: re-read the ADR section and refresh the story / proceed on the summary and note the drift / stop. An absent stamp means trust the story and note "summary trusted unverified" |
| Spec traceability | The story cites no `REQ-` ID at standard or full rigor | Note it as a gap; continue at minimal |
| Commands | `commands.build` or `commands.test` is empty | An empty build or test command means Phase 5 cannot verify. Ask: continue and end NOT VERIFIED / run `/app-test-setup` first. Never assume the check passed |
| Working tree | Uncommitted changes exist | Record the dirty file list as the **baseline** in the checkpoint, so `app-story-done` can tell what this story changed. Tell the user if the baseline touches files in the story's list |

## Phase 3: Route, list files, ask once

Decide which layers and platforms the story touches from its Files list, type and criteria, and the app's `platforms`. Pick builders from the table. Take the language specialist from `studio.yaml` `specialists:` (or from `stack.languages`: typescript-specialist, python-specialist, dotnet-specialist, rust-specialist, go-specialist, jvm-specialist, cpp-specialist). Never hardcode one stack; never spawn an agent for a platform the app does not have.

| Layer or platform | Builder | Notes |
|---|---|---|
| Web UI: views, state, forms, routing | `frontend-engineer` | `ui-engineer` for components, CSS, theming, responsive layout; `web-framework-specialist` for framework internals (SSR, hydration, build tooling); `web-platform-engineer` for PWA, workers, storage, WebAssembly, extensions |
| Windows desktop UI and OS integration | `windows-desktop-engineer` | `win32-systems-specialist` below the UI layer (services, COM, hooks, IPC) |
| macOS desktop | `macos-engineer` | |
| Linux desktop | `linux-desktop-engineer` | |
| Web-tech or cross-platform desktop shell (Tauri, Electron, Flutter desktop, MAUI, Avalonia, Qt Quick) | `hybrid-desktop-engineer` | Plus `frontend-engineer` or `ui-engineer` for the web layer inside the shell; `rust-specialist` or another language specialist for the native side |
| iOS or iPadOS | `ios-engineer` | |
| Android | `android-engineer` | |
| Cross-platform mobile (React Native, Flutter, KMP, MAUI, Capacitor) | `cross-platform-mobile-engineer` | Native module work on a platform adds that platform's engineer |
| Backend: logic, handlers, jobs | `backend-engineer` | |
| API or IPC contract change | `api-designer` first | Contract before consumers |
| Schema, migration, local storage, file formats | `database-engineer` | A destructive or large migration goes through `/app-data-migration` first |
| Pipelines, ingestion, search indexes | `data-engineer` | |
| Concurrency, queues, realtime, sync, caching | `distributed-systems-engineer` | |
| Third-party APIs, webhooks, SDKs | `integrations-engineer` | |
| Authentication, authorization, accounts | `identity-specialist` | A Security change type also needs `security-engineer` review in `/app-code-review` |
| LLM or ML features | `ai-features-engineer` | |
| CI, build, containers, hosting | `build-engineer` or `infrastructure-engineer` | |
| Logs, metrics, crash reporting | `site-reliability-engineer` | Product event instrumentation: `analytics-specialist` |
| CLI or library | the language specialist builds | `backend-engineer` when it calls services |
| Accessibility or i18n fixes | `accessibility-specialist`, `localization-specialist` | |
| Docs, help text | `technical-writer` | |
| Tests beyond the builder's unit tests | `test-engineer` (unit, integration); `test-automation-engineer` (end-to-end and UI automation) | |
| Config or data values only | the main session, after the ask | No builder needed |

Several layers: order by dependency (contract, then data, then service, then client). Run builders in parallel only when their file sets do not overlap, and give each an explicit list of files it owns.

**One ask for the phase** (`orchestration.md` section 3 write permission). Print the builders, the planned files to **edit** (existing source, config, build files) and the files to **create** (including test files), then ask: "May I mark the story In Progress, record the baseline, and let these builders edit these files?" Options: approve as listed / change the list / stop. The question is the last thing in the reply. On yes, set the story `Status` to In Progress and `Last updated` to today (the header field names are the story template's). A file the builders later need that is not on the list goes back to the user as a new ask; it is never silently added. Declined: change nothing, verdict BLOCKED.

## Phase 4: Implement

Spawn the builders per Phase 3 (parallel for disjoint file sets, in order otherwise). Brief each per `orchestration.md` section 3, with:

- The story's objective, acceptance criteria, Out of Scope, and the exact files the agent owns.
- The key facts quoted: the `REQ-` text, the ADR decision summary and implementation notes, the API contract fragment, the UX spec states and copy for UI, the design tokens it must use (not invented values), accessibility requirements, `docs/stack-reference.md` entries for APIs it uses (do not use an API from memory when the pinned version may differ).
- `studio.yaml` `rules:` and `commands:` (run only these commands to build and test). Machine rules from `shared/rules-full.md`: heavy runs through the lock helper, no focus-taking windows, no input injection, scratch in `~/AgentScratch/<task>/`.
- **Tests with the change**, by rigor (table below). Tests are written with the code, not later. Names say the scenario and the result; arrange, act, assert; no real network, clock, filesystem or random seed in unit tests; fixtures defined in the test.
- Boundaries: no change outside the story's scope; report the need instead. No abstraction for one use, no handling for cases that cannot happen (validate at input boundaries), general logic and never a value special-cased to pass a test. No secrets in code. New dependency: report it, do not add it silently (`compliance-specialist` checks licenses in review).
- Output: the exact paths written, the tests added (names), what it ran and the result, any blocker or question.

Then, once the builders report, the **language specialist** reviews the changed files read-only (idioms, typing, errors, concurrency, tooling) and returns file, line, problem, fix; it edits nothing. A problem that breaks an acceptance criterion goes back to the builder once; the rest go in the notes. Skipped at review mode solo (print `<specialist> not consulted: solo mode`).

**Test-engineer pass** (standard and full rigor, Integration, Data, API and UI-automation work): after the builders, `test-engineer` (and `test-automation-engineer` where `commands.e2e` is set) adds the integration, edge-case and journey tests the story's QA test cases name, working from the criteria rather than from the implementation.

Check each agent's artifacts (`orchestration.md` section 5): every named file exists with real content, and `git status` shows no file outside the approved list. An agent that stopped early or reports BLOCKED makes the story BLOCKED with that reason, never "implemented". Resume it once with the gap named.

## Phase 5: Build, lint, test (run them yourself)

Run, from the repo root, the commands in `studio.yaml`, and read the output. Do not take a builder's word.

1. `commands.build` (use `build_release` if `rules:` says the user tests from it). Report the command and exit code.
2. `commands.lint`, and `commands.format` as a check where it supports one. Failures in changed files are fixed by the builder; a failure in untouched files is noted, not fixed.
3. `commands.test`. Report counts. Confirm the new tests are in the run (their names appear in the output); a suite that passes without running the new tests proves nothing.
4. A failure goes back to the builder once with the output quoted. A second failure: BLOCKED with the failing output in the checkpoint. Never weaken or delete a test to get green, and never mark a flaky failure as passed: rerun once and report both runs.

An empty command: print `<command> NOT VERIFIED: commands.<key> is not set`. Never infer from reading the code that it builds or passes.

**Heavy runs use the run lock.** A release build, a container build, a full test suite, an emulator or a large dependency install runs as `~/Tools/agent_locks/run_locked.sh cpu <command>` (`gpu` for anything that opens a window or uses the GPU) when that helper exists, and one at a time when it does not. Exit code 75 means the user is gaming: stop, keep what exists, record in the checkpoint what is still to run, and report NOT VERIFIED for it. A quick unit-test or incremental build run may go directly.

| Rigor | Tests the story must leave behind | Always, at every rigor |
|---|---|---|
| minimal | Logic and Data changes with a harness available get a test for the main criteria; Integration, UI and Visual rely on the Run result | The build and the existing tests are run; a defect fix gets a regression test; the look is observed (Phase 6) |
| standard | Every automatable acceptance criterion has at least one test | |
| full | As standard, plus edge cases and error paths, plus an end-to-end journey for a UI story when `commands.e2e` is set | |

Rigor changes what must exist, never what must work.

## Phase 6: Run and observe

Read `references/run-and-observe.md` now and follow it. Read it again if the conversation was compacted during this phase. For every change a user can see, receive or read (all UI and Visual stories, and any backend, CLI or data change with a response or output), launch the result, reach the state the story touched, capture without taking focus, open the capture, and compare it with the criteria. Evidence goes in `docs/qa/evidence/<story>/` with an `evidence.md` stamp.

Leave the evidence the change type needs (`standards/testing.md` is the authority; `app-story-done` checks it):

| Change type | Evidence to leave behind |
|---|---|
| Logic | Passing unit tests, including edge cases and failure paths |
| Integration | Integration test output (`docs/qa/evidence/<story>/test-run.md`), or a recorded manual run of the real path |
| UI | A retained capture of each screen and state touched, light and dark if themed, and a keyboard-only pass noted |
| Visual | Retained captures at the target sizes and themes; a design-system change also needs `design-director` or `ui-designer` sign-off in review |
| Data | A migration run on a copy of realistic data, forward and (where promised) back; old data opens in the new build; counts before and after |
| Config | A smoke check: it builds, starts and does its main path with the new config |
| Infra | The pipeline or deployment run (log excerpt), a health check after, a rollback or restore noted for risky changes |
| Security | Tests of the abuse cases, dependency audit output where dependencies changed; the `security-engineer` review happens in `/app-code-review` |
| Performance | A before and after measurement against the budget, with method, device and build type |
| Docs | Commands in it were run, links resolve |

Report one line, exactly (`orchestration.md` section 10):

```
Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why it could not be run> | N/A - <why nothing is observable>
```

"It is a logic change" is not an N/A reason when the change alters what a user sees. NOT VERIFIED on a UI or Visual story blocks closing, and the summary says so.

## Phase 7: Update the story, checkpoint, close the run

1. **Story file.** Replace the rows of its `Files` table with the files actually changed (Path, Create or Modify, Purpose; code and tests), fill its `Run result:` line with the one line from Phase 6, record the test files and evidence folder under the story's `Test Evidence` section, set `Last updated`, and set `Status` to In Review when the verdict is IMPLEMENTED or IMPLEMENTED WITH NOTES (left In Progress when BLOCKED or NOT VERIFIED). Never Complete. The Phase 3 ask covered these edits.
2. **Checkpoint.** Overwrite the `CHECKPOINT` block in `.studio/state.md` (`templates/session-state.md`; create from the template if absent, and add `.studio/` to `.gitignore` if missing): current task, next step, blocked on, files in progress, baseline dirty files, last Run result, open questions. On every outcome.
3. **Summary** (fenced shape below), then the closing block.

```
## Implemented: <story title>   (<path>)
Builders: <agent, agent>   Specialist review: <agent: clean | N findings | not consulted: reason>
Files changed: <path (created|modified: what)>, ...
Tests: <N added, names or file> | none required at <rigor> for <type> | NOT WRITTEN: <why>
Build: <command> exit <n> | NOT VERIFIED: <why>
Lint: <command> exit <n> | NOT VERIFIED: <why>
Test run: <command>: <passed/failed/skipped counts>; new tests in run: <yes|no> | NOT VERIFIED: <why>
Acceptance criteria:
- <criterion> : <test name | file:function | OBSERVED path | NOT YET COVERED>
Notes: <accepted drift, dependency risk, specialist suggestions, baseline overlap | none>
Blockers: <none | each>
Run result: <the one line>
```

## Review mode

| Mode | Effect here |
|---|---|
| solo | No language specialist review, no test-engineer pass unless the story needs integration tests. `Gates: none run (solo)` |
| lean | Language specialist review runs. No gates here: gates run in `app-story-done` (`PE-CODE-REVIEW` at lean for non-trivial changes) |
| full | As lean, plus the test-engineer and test-automation-engineer passes per the rigor table |

This skill runs no gate at any mode.

## Verdicts

First match wins. NOT VERIFIED ranks below BLOCKED and above the passes.

1. **BLOCKED**: a Phase 2 stop; the user declined the Phase 3 ask; a builder stopped early or reports BLOCKED; build or tests still fail after one fix attempt; a needed file lies outside the approved list.
2. **NOT VERIFIED**: the work is written and nothing failed, but the build, lint or test command could not be run (empty command, tool missing), or the Run result is NOT VERIFIED for a UI or Visual story, or the new tests did not appear in the run. Name each check and what would settle it.
3. **IMPLEMENTED WITH NOTES**: everything ran and passed, with advisory items (specialist suggestions, accepted ADR drift, accepted dependency risk, baseline overlap, a criterion with no automated test at this rigor, a Run result of N/A with its reason).
4. **IMPLEMENTED**: everything ran, passed, nothing to note.

## Rules for this skill

- Never set a story Complete or Done. `app-story-done` is the only closer.
- Never edit existing source, config or build files outside the list the user approved in Phase 3.
- Never claim a build, lint, test or run result that was not produced in this run. Missing means NOT VERIFIED.
- Never weaken, skip or delete a failing test to reach green.
- Never take focus or inject keyboard or mouse input on the user's live desktop (`shared/rules-full.md`). The only exception is a brief that says the user is away, for that run. Otherwise the Run result is NOT VERIFIED, with that reason.
- Never edit an ADR, spec or contract: report the conflict and ask.
- Do not start the next skill. Recommend it.

## Report

Print the summary above, then end with the closing block (`orchestration.md` section 8):

```
Verdict: <IMPLEMENTED | IMPLEMENTED WITH NOTES | NOT VERIFIED | BLOCKED> - <one line why>
Gates: none run (dev-story runs no gate)
Wrote: <source, test, evidence, story and checkpoint paths>
Next: </app-code-review <scope> then /app-story-done <story> | /app-dev-story <story> to resume | the action that unblocks it> (<why>)
```
