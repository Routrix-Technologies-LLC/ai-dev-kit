---
name: app-smoke
description: "Build the app, run its tests, and launch and observe its critical paths on each target it supports, without stealing focus or injecting input into the user's session, and return PASS, PASS WITH WARNINGS, NOT ASSESSED or FAIL. Use when the user says smoke test, does it still work, is this build healthy, sanity check, before QA hand-off, before a gate or release, or after a risky merge or upgrade."
argument-hint: "[quick | full] [--target <platform>] [--review solo|lean|full]"
user-invocable: true
---

# App Smoke

The smoke check answers one question: is this build healthy enough to be worth anyone else's time. It builds the app, runs the test suite, then launches the app on each target it supports and looks at the critical paths with its own eyes (captured images, transcripts, logs). It reports exactly what ran and what did not. A target it could not run is NOT ASSESSED, never PASS.

Writes: `docs/qa/smoke-<date>.md` (a second run on the same date adds a time suffix) and evidence in `docs/qa/evidence/smoke-<date>/` (template `test-evidence.md` for evidence notes).
Next: `/app-story-done`, `/app-gate`, `/app-bugfix` (on FAIL), `/app-test-setup` (on missing commands), `/app-qa-plan`.

## When to use and when not to

Use it before QA hand-off, at a sprint close, after merging or upgrading, and before `/app-gate` or `/app-release`. Not for these:

- Proving one story's acceptance criteria: `/app-story-done`.
- Deep checks (performance, accessibility, security): `/app-perf`, `/app-a11y-audit`, `/app-security-audit`.
- Setting up the harness: `/app-test-setup`.
- Fixing what fails: `/app-bugfix`. This skill never edits code or tests.

## Inputs

- Required: `studio.yaml` with `platforms` and `commands:`. Without `studio.yaml`, offer `/app-adopt` or `/app-start` and stop.
- `commands.build` and `commands.test` are needed for the build and test parts; `commands.run` and `commands.screenshot` (or another capture method) for the observe part. Each missing command is NOT ASSESSED for its part, with `/app-test-setup` offered. Never invent a command and never run an unverified guess.
- The critical paths, in priority order, naming the source in the report: the smoke scope of the current QA plan in `docs/qa/test-plans/`, then `docs/qa/smoke-paths.md`, then the fallback list below (used only when neither exists, and said so).
- `studio.yaml` `rules:` are obeyed (for example a rule to build the release binary after UI changes).
- Modes: `quick` skips the test-coverage cross-check and the optional paths; a quick run is labelled so in the verdict and can pass but never reads as a full run. `full` is the default. `--target` limits the run to one platform; the report then says the other targets were not run (NOT ASSESSED for them).

## Phase 1: Resolve targets and capabilities

Who: the main session. Print the announce block (orchestration.md section 2) with `test-automation-engineer` and `test-engineer`. Gates: none.

1. List every target from `platforms`, with the oldest and newest OS or browser from `stack.min_targets` where it matters to launch behavior.
2. For each target decide `can run here` or `cannot run here`, by probing the machine (tool present, version command works, display or simulator available). Examples of cannot-run: an iOS or macOS target on a non-Apple host, a Linux desktop target without a virtual display tool, an Android target without an emulator image or hardware acceleration, a mobile real-device path, a Windows-only target on another OS. A target that cannot run is NOT ASSESSED in the verdict from this point; it is still listed.
3. Record the capture method per target (the `commands.screenshot` or the method documented by `/app-test-setup`).
4. Note any running copy of the app the user started. Never close, restart or capture the user's copy. If the build output is locked by it, follow `studio.yaml` `rules:`; with no rule, stop that target and ask.

Check: a target table (target, can run here, build, test, observe, status) is printed before running anything.

## Phase 2: Build

Who: `test-automation-engineer` runs; the main session reads the output.

Heavy builds, suites and emulators run one at a time; if the user needs the machine back, stop and mark what is left NOT ASSESSED. Run `commands.build` for every target that can run here (and `commands.build_release` when a rule requires it, or at `full`). Build per platform as the project does (for a multi-platform app: each platform's build command or CI job). Record exit code, duration and the warning count. A build that exits non-zero, times out, or produces no artifact is FAIL for that target. Do not fix anything.

Check: each build has a recorded exit code and, for targets that produce an artifact, the artifact path exists.

## Phase 3: Run the tests

Who: `test-engineer` runs; the main session verifies the result itself (orchestration.md section 5).

Run `commands.test` (and `commands.e2e` at `full` when set). Record tests run, passed, failed, skipped, with the denominator. Rules:

- Failures: FAIL, with the failing test names and the first useful output line each.
- The runner could not run, a compile error, a timeout, or no result file: FAIL if the cause is the code, NOT ASSESSED if the cause is the environment (tool missing). Say which.
- Zero tests executed: NOT ASSESSED ("0 tests run"), never a pass.
- Passed with skips or runner warnings: PASS WITH WARNINGS, listing skips and warnings.
- A test command that runs only on another OS or in CI: NOT ASSESSED here, and check the latest CI result if the provider's tooling is available; record it as `CI result, not run here` with the run link, never as a local pass.

Unless `quick`, cross-check coverage: for each story closed in the scope (from the QA plan or sprint), is there test evidence for its change type? Count covered, manual, missing and unknown; a story that cannot be read is UNKNOWN. Missing evidence for a Logic or Integration story is a warning. A story whose file is unreadable is NOT ASSESSED.

## Phase 4: Launch and observe the critical paths

Who: `test-automation-engineer`, briefed per orchestration.md section 3 with the path list, the capture method per target, the evidence folder, and these constraints, appended verbatim to the brief:

```
Do not take focus, do not move the user's pointer, do not type or click in the user's session, and do not close or capture any app copy you did not start. Reach states with launch arguments, deep links, URLs, fixture data or the app's own test hooks. Input automation is allowed only inside an isolated target: a headless browser, a simulator or emulator, a virtual display. Start audio muted or off where the platform allows. Use a throwaway profile, database and data directory. Kill only the processes you started, by process id. A path you could not reach is NOT RUN with the reason; do not describe a path you did not observe.
```

Observe each path as a transcript, an image or a log, and record per path: how it was reached, what was observed (quoted), the evidence file, and PASS, FAIL, or NOT RUN with the reason.

Critical paths when no list exists (fallback, say so in the report): the app starts and reaches its first usable state with no error in the log; a first run with empty data; the core job from the brief completes end to end; data survives a restart; the app quits cleanly; and, if the app has them, sign-in and the main settings screen. Per platform:

| Target | Observed how |
|---|---|
| web | serve the build locally, load each critical route in a headless browser at a small and a large viewport, count console errors and failed network requests, capture an image per route |
| backend | start on a free port against a throwaway database with migrations applied, wait for the health endpoint, send the critical requests, save request and response pairs, scan the log for errors and stack traces, stop cleanly |
| cli | run `--help`, `--version`, and the core command on a fixture in a temporary directory; record stdout, stderr, exit codes; check a failing input returns a non-zero code and a readable error |
| windows, macos, linux desktop | launch the built app non-activating, wait for the main window, capture by window (not by screen region), check the process is alive after a settle period, scan logs and crash reports, relaunch to check persisted state, quit cleanly |
| ios, android | boot a simulator or emulator without its window, install the build, launch with arguments, capture, scan system log for crashes, relaunch for persistence; lifecycle (background and foreground, rotation) may use the emulator's own controls since it is isolated |
| extension | load into a throwaway browser profile, open the popup or the page it changes, capture |
| library | build the examples and run them; the public API surface check is part of the tests; capture is N/A with the reason |

Compose the run result per target as exactly one line (orchestration.md section 10): `Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why> | N/A - <why nothing is observable>`. A UI-bearing target is never N/A.

The main session opens at least one captured image per target (Read renders images) and one log or transcript, and confirms the claim in the report matches. An image that is blank, shows the wrong screen, or shows an error dialog is FAIL. Label specialist claims it did not check `UNVERIFIED`.

If paths remain NOT RUN because they need human input (for example a hardware prompt or an OS permission dialog), list them. Ask the user once, with AskUserQuestion batched to at most three calls, whether they ran those paths and what they saw. Their answers are recorded as `user-reported` beside the path. They do not change the target's status: a target that this skill could not run stays NOT ASSESSED.

## Phase 5: Verdict and report

Who: the main session. Compute the per-target status and the overall verdict by the rules below, then write `docs/qa/smoke-<date>.md` (new file, so no ask is needed; an existing report is never overwritten) with the fixed shape under Report. Evidence files are small PNGs and text, saved in the evidence folder and referenced from the report.

Do not fix, retry silently to hide flakiness, or edit tests. A failure that passes on rerun is reported as `FLAKY`, with both results, and counts as a warning at minimum.

Offer next steps by result: FAIL means `/app-bugfix` for each failure (with the evidence path); NOT ASSESSED means the closing action per item (`/app-test-setup`, run on the missing platform, CI); PASS means the next planned skill.

## Rigor and review mode

Rigor changes how much is observed, never whether it must work.

| | minimal | standard | full |
|---|---|---|---|
| Build and launch of the main target | required | required | required |
| Test suite | required if `commands.test` is set; unset is NOT ASSESSED | required | required plus e2e |
| Paths observed | the core job and launch | all listed critical paths | all, plus restart persistence, log scan and clean quit on every target, release build |
| Targets | main platform | every platform in `platforms` | every platform, oldest and newest OS where available |

Gates: none run. Smoke feeds `QL-TEST-COVERAGE` and the gate skills as evidence. Print `Gates: none run (<mode>)`.

## Verdicts

Per target and overall. First match wins. Overall is the worst target. NOT ASSESSED ranks below FAIL and above PASS WITH WARNINGS.

1. FAIL: any build error or missing artifact; any test failure; the suite did not complete because of a code problem; any critical path observed failing (crash, hang, wrong screen, error dialog, error in the log at startup, data lost on restart); a captured image that is blank or wrong.
2. NOT ASSESSED: any target in `platforms` that was not run (cannot run here, `--target` excluded it, a missing command or tool); zero tests executed or the runner could not run for environmental reasons; any critical path NOT RUN; a Run result of NOT VERIFIED; the critical-path list had to fall back and the user did not accept the fallback; any story whose coverage is UNKNOWN. Name each.
3. PASS WITH WARNINGS: everything ran and passed, with at least one warning: skipped or flaky tests, runner or build warnings above the baseline, Logic or Integration stories lacking test evidence, a slow startup against a budget, or log warnings.
4. PASS: every target ran build, tests and every critical path with OBSERVED evidence, no skips, no warnings, no missing evidence. A `quick` PASS carries the label `PASS (quick: coverage and optional paths not checked)`.

With `--target`, the best possible overall verdict is NOT ASSESSED when other platforms exist, and the report says `<n> of <m> targets run`.

## Report

The report file and the final reply use this shape:

```
Smoke check <date>   App: <name>   Build: <commit or version>   Mode: <full|quick>   Checklist source: <path or fallback>
Targets: <n run> of <m>
| Target | Build | Tests (passed/run, skipped) | Paths (observed/total) | Run result | Status |
Failures: <test or path, evidence path, first useful output line>
NOT ASSESSED items: <item: reason, closing action>
Warnings: <list>
User-reported (unverified): <list or none>
Coverage cross-check: <covered> covered, <manual> manual, <missing> missing, <unknown> unknown of <total> stories (or "not checked (quick)")
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never mark a target PASS that was not run on that target. Not run means NOT ASSESSED.
- Never take focus, move the pointer, type into the user's session, or touch an app copy the user started. Never audible: audio muted or off.
- Never edit source, tests or config. Never auto-fix a failure.
- Counts always carry a denominator ("38 of 38 tests", "5 of 6 paths"). Zero tests or zero paths is NOT ASSESSED.
- Describing a path is not observing it. Every PASS path has an evidence file or transcript the main session looked at.
- A user-reported result is recorded as such and never raises a verdict.
- A rerun that changes the result is reported as FLAKY, not as a clean pass.
- Never start the next skill automatically.
