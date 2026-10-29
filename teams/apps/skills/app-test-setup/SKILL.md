---
name: app-test-setup
description: "Set up or repair the app's test runners, test helpers, CI pipeline and headless UI capture for each platform it targets, run every command to prove it works, and record the verified commands in studio.yaml. Use when the user says set up tests, add CI, tests are broken or missing, I need screenshots without a window popping up, or before the foundation stage ends."
argument-hint: "[app] [repair | add-ci | capture] [--review solo|lean|full]"
user-invocable: true
---

# App Test Setup

A test harness that was never run is a rumor. This skill installs or repairs the test runner, shared helpers and CI for the app's stack, sets up capture of the running app without taking over the user's screen, and then runs every command it wrote. Only commands that ran and gave the expected result are recorded in `studio.yaml` `commands:`. Anything it could not run stays empty and is named as a gap.

Writes: test config and a first real test, shared test helpers, CI configuration, `docs/qa/smoke-paths.md` (the critical paths `/app-smoke` observes), capture scripts, and `commands:` in `studio.yaml` (build, build_release, test, lint, format, run, e2e, screenshot).
Next: `/app-smoke` (first real run), `/app-qa-plan`, `/app-plan` or `/app-dev-story`.

## When to use and when not to

Use it at the foundation stage, when adopting an existing app with weak or no tests, when CI is red for harness reasons, or when UI or screenshot evidence is needed and no capture method exists. Not for these:

- Writing tests for a story: `/app-dev-story` (with `test-engineer`).
- A failing test caused by a code bug: `/app-bugfix`.
- Judging whether the tests are enough: `/app-qa-plan` and `/app-story-done`.
- Packaging, signing or deploy pipelines: `/app-release`.

## Inputs

- Required: `studio.yaml` with `platforms` and `stack`. If missing, offer `/app-adopt` or `/app-start` and stop. If `stack` is empty, ask; never guess a stack.
- Optional: existing test directories, CI files, `docs/stack-reference.md` (versions of runners and tools to match), the architecture doc (what must be testable), the QA plan.
- Modes: no argument means detect and do what is missing. `repair` fixes a harness that exists but is broken. `add-ci` only does Phase 4. `capture` only does Phase 5.

## Phase 1: Detect

Who: the main session, with `build-engineer` consulted on CI. Read, do not write.

1. Read `studio.yaml` (`platforms`, `stack`, `commands`, `rules`, `specialists`). Read the manifests and lockfiles to find the real toolchain and versions in use.
2. Find what exists: test directories and runner configuration, test count (Glob for test files by the ecosystem's naming), CI files and which provider (from the git remote and the CI folder), existing screenshot or e2e tooling, lint and format configuration.
3. Probe which tools are installed on this machine (runner, browser, simulators, emulators, display server) with version commands. Record `present`, `missing`, or `not applicable here`. Absence of a tool is a finding, never a reason to assume a pass.
4. Run the commands already in `commands:` once each and record exit code and counts. A command that was never run before is `UNVERIFIED` until it passes here.

Check: a detection table (platform, runner, CI provider, capture method, status of each command) is shown to the user.

## Phase 2: Plan

Who: `build-engineer`, `test-engineer`, `test-automation-engineer` in parallel, each producing a short proposal (returned in the reply, no files yet), briefed per orchestration.md section 3, with the language specialist from `specialists:` consulted for runner choice. Print the announce block first.

Prefer what the repository already uses. Where nothing exists, pick the ecosystem's mainstream default and give one sentence of reason. Do not add a second runner for the same layer.

| Ecosystem | Unit and integration runner (typical) | Notes |
|---|---|---|
| JavaScript, TypeScript | the project's bundler-native runner or the established standalone one; the built-in `node --test` for small libraries | DOM and component tests need a DOM environment; type check as its own command |
| Python | pytest | coverage plugin optional; type check and lint separate |
| .NET | xUnit, NUnit or MSTest, run with `dotnet test` | UI tests need a platform-specific driver |
| Rust | `cargo test`, nextest for large suites | doc tests count; feature matrix for workspaces |
| Go | `go test` with the race detector in CI | table tests; `-count=1` to defeat caching when verifying |
| JVM | JUnit via Gradle or Maven | Android adds instrumented tests |
| C and C++ | CTest with GoogleTest or Catch2 | sanitizer builds as a separate CI job |
| Swift, Apple | XCTest or Swift Testing via `swift test` or `xcodebuild test` | needs a macOS host |
| Android | JUnit local tests plus instrumented tests | managed or CI emulators need hardware acceleration |
| Flutter, React Native, .NET MAUI, Kotlin Multiplatform | the framework's own test command plus a device-level journey tool | one set of journeys, run per OS |

UI and journey layer (`test-automation-engineer` chooses by platform): web uses a browser automation library with a headless browser; desktop uses the platform's accessibility-based automation (UI Automation on Windows, XCUITest or the accessibility API on macOS, AT-SPI or the toolkit's own test driver on Linux) or the shell's WebDriver bridge for webview-based apps (UI-automation drivers that send input run only inside an isolated session such as a virtual display, VM or CI runner, or when the brief says the user is away); mobile uses XCUITest, Espresso or Compose test, or a cross-platform tool such as Maestro, Detox or Appium; backend uses contract and integration tests with a throwaway database or containerized dependencies.

The plan lists: runners and versions to add, files to create, helpers to create, CI jobs (below), capture method per platform (Phase 5 table), and the exact `commands:` values proposed. Present it, with the full list of files the work will create and any existing files it will edit (config, manifests, `studio.yaml`), and ask once for approval (orchestration.md sections 3 and 6). Existing test and config files are never overwritten; edits to them are listed and approved.

## Phase 3: Install the harness

Who: `test-engineer` and `build-engineer`, in sequence (one writes the harness, the other reads it before CI), writing the files named in the approved plan.

1. Add the runner, its config and the scripts or targets that run it. Pin versions in the lockfile.
2. Add shared helpers only for what the app needs now, in the ecosystem's conventional place: fixture and factory builders for domain objects, a temporary directory and temporary database helper, a fake clock and fake network for determinism, a test server or app-launch helper, an accessibility-tree dump helper for UI tests. Helpers are small and documented in a header comment. Do not build a framework.
3. Add one real test per layer that exists in the app (a unit test of real logic, an integration test across a real boundary, and one journey test if a UI exists). A placeholder that asserts true is not a test. Tests must fail when the thing they check is broken: have `test-engineer` demonstrate this by inverting an assertion or feeding the test a deliberately wrong expected value and showing the failure, then restoring it. Only if that cannot reach the logic, break the code under test in a file with no uncommitted user changes, and confirm the restore with `git diff` showing nothing.
4. Add or repair `lint` and `format` commands if the ecosystem has standard tools and the user approved them.

Check: the files exist with real content; the demonstrated failure and restore are reported with the exact output line.

## Phase 4: CI

Who: `build-engineer`. Skipped by `capture` mode; offered, not forced, at minimal rigor.

Write the pipeline for the provider found in Phase 1 (GitHub Actions, Gitea Actions, GitLab CI, Azure Pipelines; if none, ask which and whether CI is wanted at all). Jobs:

| Job | When | Notes |
|---|---|---|
| build | every push and pull request | build per OS in `platforms`; a native Windows or macOS or Linux target builds on that OS; iOS and macOS need a macOS runner |
| lint and type check | every push and pull request | fast feedback first |
| test | every push and pull request | unit and integration; publish the result report and failure logs as artifacts |
| e2e or journey | pull request (standard), nightly plus pull request (full) | browser jobs on Linux runners; emulator jobs need hardware acceleration; simulator jobs need macOS |
| dependency audit | scheduled weekly (standard and above) | ecosystem audit command; failure opens a visible signal, not a silent log |

Rules for every pipeline: pin action or image versions, cache dependencies by lockfile hash, set job timeouts, give least-privilege tokens, never print secrets, keep secrets as repository settings that the user adds (name them in the summary, never put values in files), and make test jobs fail the pipeline on test failure and on zero tests found. Branch protection and runner provisioning are the user's actions; list them as follow-ups, do not attempt them.

A runner type the repository does not have (a macOS or self-hosted runner) means that job is written but marked `NOT VERIFIED - needs <runner>`.

## Phase 5: Headless capture, per platform

Who: `test-automation-engineer`. The goal is one command that launches the app, reaches a named state, captures an image (or request and response transcript), and exits, without moving the user's cursor, pressing keys on the user's desktop or taking focus. Record it as `commands.screenshot`. The state is reached with launch arguments, deep links, URLs, fixture data or app test hooks, not by injecting input into the user's real session. Input automation is acceptable only inside an isolated target: a headless browser, a simulator or emulator, a virtual display.

| Platform | Method | Verify by |
|---|---|---|
| web | headless browser from the automation library, fixed viewport and scale, run against a locally started dev or preview server on a free port, then stopped | image file exists, is not blank, opened and looked at |
| backend | start the service on a free port with a throwaway database and test configuration, send the critical requests with the test client, save request and response pairs and the log tail | transcript exists and shows expected status codes |
| cli | run with fixed arguments in a temporary directory, record stdout, stderr and exit code; for terminal UIs run in a pseudo-terminal and save the rendered screen text | transcript matches expected output |
| windows | launch the app, capture its window by window handle with the OS window capture API, not by copying a region of the screen, so other windows and focus do not matter; add an accessibility-tree dump as non-visual evidence | image is the app window, not the desktop |
| macos | launch in the background without activating it, capture by window id with the system capture tool; needs the Screen Recording permission, which only the user can grant | image is the app window |
| linux | run under a virtual display (or a headless compositor session) and capture from it; the user's display is never touched | image is the app window |
| ios | boot a simulator without its window UI, install, launch with arguments, capture with the simulator control tool; macOS host required | image from the simulator |
| android | emulator with no window and no audio, install, launch, capture through the debug bridge; Linux hosts need hardware acceleration | image from the emulator |
| extension | automation library with the extension loaded into a throwaway profile | popup or page image |
| library | no visual surface: the example or doc build is the observable; capture is N/A | state the reason |
| hybrid desktop (webview shells) | capture the window as for the OS above, or drive the web content through the shell's WebDriver or debugging protocol | image or DOM snapshot |

Capture is audio-off and uses fixed size so images are comparable. Output goes to `docs/qa/evidence/<scope>/`, small PNGs. The script must kill only processes it started, by process id, and never touch a running copy of the app that the user launched.

A platform whose method cannot run on this machine (a macOS or iOS method on another OS, a missing permission, no accelerated emulator) is recorded `NOT VERIFIED - <why>`, with the CI job or machine that could run it. It is not marked working.

## Phase 6: Seed the smoke paths

Who: `test-engineer` with the main session. Write `docs/qa/smoke-paths.md` (new file): the 5 to 10 critical paths `/app-smoke` will launch and observe, each with the platform(s), the way to reach it (launch argument, URL, fixture), what must be seen, and what counts as failure. Always include: launches without crash or error log, first run state, the app's core job end to end, a restart that keeps data, and a clean quit. Derive the core job from the brief or specs; if there is none, ask the user to name it. Never invent product behavior.

## Phase 7: Prove it and record

Who: the main session, running each command itself (orchestration.md section 5).

0. Heavy runs (release builds, full suites, container builds, emulators and simulators, soak runs) go through `~/Tools/agent_locks/run_locked.sh cpu <command>` (`gpu` for anything that opens a window or uses the GPU) when that helper exists, otherwise one at a time; exit code 75 means the user is gaming, so stop, keep what exists and report what is still to run as NOT VERIFIED or NOT ASSESSED.
1. For each of `build`, `build_release`, `test`, `lint`, `format`, `run`, `e2e`, `screenshot`: run it from the repo root and record exit code and the key count (tests run and passed, files written, image produced). `run` is verified by launching and stopping it, not by reading it.
2. A command passes only if it exits as expected and produced the expected result. A test command that ran zero tests is a failure. A screenshot command that produced a blank or missing image is a failure.
3. Show the user the table: command, value, result (VERIFIED with evidence, FAILED, NOT VERIFIED with reason).
4. With the user's approval (existing file edit, listed in the Phase 2 approval), write only the VERIFIED values into `studio.yaml` `commands:`. FAILED and NOT VERIFIED stay empty (never guessed), and each is listed as a gap with the action that would close it.
5. Add `.studio/` to `.gitignore` if it is missing. Record the harness in `docs/stack-reference.md` (runner names and pinned versions) if that file exists.

## Rigor and review mode

Rigor changes how much exists, never what must work. Every command written must have been run.

| | minimal | standard | full |
|---|---|---|---|
| Runner and one real test per layer | required | required | required |
| `build`, `test`, `run` verified | required | required | required |
| Capture for the app's main platform | required | required | required for every platform with a method |
| CI | offered | build, lint, test on push and PR | plus e2e, nightly, audit, coverage report |
| Smoke paths | 3 to 5 | 5 to 10 | 5 to 10 with a per-platform matrix |

Gates: none are defined for this skill. Print `Gates: none run (<mode>)`.

## Verdicts

First match wins. This skill's list has no NOT ASSESSED because it either did the work or reports exactly what it could not do.

1. BLOCKED: the stack is unknown and the user did not supply it, no runner can be installed or run on this machine, or the app does not build so no test can run. Name what blocks and what to do.
2. PARTIAL: harness installed, but at least one of `build`, `test`, `run`, or the main platform's `screenshot` is not VERIFIED, or CI was written but never executed (`NOT VERIFIED`), or a platform in `platforms` has no working capture method. List each gap.
3. COMPLETE: every command written was run and VERIFIED, the real tests fail when broken, capture works for the main platform, and `studio.yaml` `commands:` holds the verified values.

## Report

```
Harness: <runner(s)> for <platforms>   CI: <provider, jobs, verified or not>
Commands: build <ok> | build_release <ok> | test <n run, n passed> | lint <ok> | run <ok> | e2e <ok> | screenshot <ok>
Capture per platform: <platform>: <method> VERIFIED <evidence path> | NOT VERIFIED <why>
Demonstrated failure: <test> failed when broken, passed when restored
Gaps: <list or none>
Follow-ups for the user: <secrets to add, runners to provision, permissions to grant>
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never overwrite an existing test, config or CI file. Edits are listed and approved first.
- Never record a command in `studio.yaml` that has not been run and passed. Unknown stays empty.
- A placeholder test that cannot fail does not count.
- Capture never moves the user's mouse, types on the user's desktop, takes focus, or kills the user's own running copy of the app.
- Never put secrets, tokens or signing material in files or logs. Name what the user must set.
- A tool, permission, runner or platform this machine lacks is a named gap, not a pass.
- Prefer the repository's existing tools to new ones; one runner per layer.
- Never start the next skill automatically.
