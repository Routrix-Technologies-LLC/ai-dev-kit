# Testing and evidence

Every change is proven before it is called done. This file says what proof each kind of change needs, how to produce it, and what not to automate. Rigor (`rigor.md`) never relaxes it.

## Evidence by change type

Classify the change by what it touches. A change with several types needs the evidence of each. Evidence is retained: it is still on disk when the story closes. A screenshot taken and discarded is an assertion, not evidence.

| Type | What it covers | Required evidence | Location | Gate |
|---|---|---|---|---|
| Logic | Calculations, rules, state machines, parsing, validation | Automated unit tests that pass, including edge cases and the failure paths | The app's test folder, next to the code or in its test tree | BLOCKING |
| Integration | Two or more components, a service boundary, a database, an IPC or API contract | Integration test, or a recorded manual run of the real path with output | Test tree; notes in `docs/qa/evidence/<story-or-change>/` | BLOCKING |
| UI | Screens, dialogs, views, forms, navigation, any user-visible text or layout | Run and observe: a retained screenshot of each screen or state touched, light and dark if themed, plus a keyboard-only pass noted | `docs/qa/evidence/<story-or-change>/` | BLOCKING |
| Visual | Look and feel: spacing, type, color, icons, theming, animation | Retained screenshots at the target sizes and themes; sign-off by `design-director` or `ui-designer` on a design-system change | `docs/qa/evidence/<story-or-change>/` | BLOCKING |
| Data | Schemas, migrations, save and file formats, seed data, stored settings | Migration run on a copy of realistic data, forward and (where promised) back; old data opens in the new build; row or record counts before and after | `docs/qa/evidence/<story-or-change>/` | BLOCKING |
| Config | Build files, feature flags, tuning values, environment settings | Smoke check: the app builds, starts and does its main path with the new config | Note in evidence folder | ADVISORY |
| Infra | Containers, deployment, CI, hosting, networking | The pipeline or deployment run (log excerpt), a health check after, a rollback or restore noted for risky changes | `docs/qa/evidence/<story-or-change>/` | BLOCKING |
| Security | Auth, authorization, crypto, secrets, input from outside, IPC, updates, permissions | Tests for the abuse cases (not only the happy path), a `security-engineer` review, dependency audit output where dependencies changed | Test tree; review in `docs/security/audits/` | BLOCKING |
| Performance | Anything with a budget: startup, latency, memory, bundle size, frame time, battery | A before and after measurement against the budget in `perf-budget.md`, with method, device and build type | `docs/qa/evidence/<story-or-change>/` | BLOCKING if a budget exists, else ADVISORY |
| Docs | Documentation, comments, README, CHANGELOG | Commands and paths in it were run or checked; links resolve; `documentation.md` checklist | Note in the change | ADVISORY |

A gate level may be tightened by the app's `studio.yaml` `rules:`. It is not loosened to get past a failure. NOT VERIFIED on a UI or Visual change blocks closing the story.

## Test rules

- **Deterministic.** Same result every run. No wall-clock time, random values without a fixed seed, network, locale or timezone dependence unless that is the thing under test; inject clocks and random sources.
- **Isolated.** Each test builds and tears down its own state. No test depends on order or on another test's leftovers. No shared mutable fixtures. Integration tests clean up after themselves, and never touch real user data.
- **No network in unit tests.** Unit tests do not call real APIs, databases or the file system outside a temp directory. Mock or fake external dependencies behind an interface. A test that needs the network is an integration test and is labelled and run separately.
- **Name the scenario and the expectation.** `rejects_expired_token`, `it('shows an error when the file is empty')`. Arrange, act, assert, in that order, one behavior per test. Use the app's language conventions.
- **Regression tests are seen failing first.** Every bug fix has a test that would have caught the bug. Run it against the unfixed code and watch it fail, then apply the fix and watch it pass. A regression test only ever seen passing is not known to test anything; a fixture that cannot trigger the bug looks authoritative and proves nothing.
- **Never disable a failing test to go green.** Not by skipping, deleting, loosening an assertion, or retrying until it passes. Fix the cause, or report the failure and let the user decide.
- **A compile check is not a run.** A passing build proves the code loads. Tests prove the logic. Neither proves the screen looks right or the feature works. Run the thing.
- **Performance tests state thresholds** and fail when exceeded.
- **Test data is explicit:** defined in the test or in a fixture or factory, not inline magic numbers (boundary values excepted, where the number is the point).
- **A count has a denominator.** "42 passed" is incomplete; "42 of 42 run, 3 skipped" is a report. Zero tests run is NOT ASSESSED, not a pass.

## Run and observe

A change a user can see is launched and looked at before it is called done. Compile, then run. The agent can look at images: the Read tool renders a PNG.

1. **Use `commands.run` and `commands.screenshot` from `studio.yaml`.** If they are empty, work out the way below and propose filling them in.
2. **Launch straight to the surface under test** (a route, deep link, screen argument, or a debug flag that sets state). A feature reachable only by five clicks will not be reached by an unattended run.
3. **Do not steal focus and do not inject input.** No SendInput, pyautogui, AutoHotkey, xdotool, AppleScript keystrokes or UI automation that types or clicks on the real desktop, unless the brief says the user is away. Prefer offscreen capture, headless browsers, simulators and the app's own screenshot flag.
4. **Look at the capture,** compare it with the acceptance criteria, and keep it. Clipped text, overflow, wrong color, missing element and wrong state are defects.
5. **Report one line:** `Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why> | N/A - <why nothing is observable>`. "It is a logic change" is not an N/A when what the user sees changes.

| Platform | How to run and capture without focus or input |
|---|---|
| Web | A headless browser (Playwright or similar) at a fixed viewport, screenshot of the route; also at a narrow phone width and in dark theme if supported. Check the console for errors |
| Windows | The app's own screenshot or offscreen render flag; else window capture of the app's window handle (for example PrintWindow) while it stays in the background. Use `timeout`; mind Git Bash rewriting leading-slash arguments (set `MSYS_NO_PATHCONV=1`) |
| macOS | The app's screenshot flag; else `screencapture` of a window id. Do not use scripted keystrokes |
| Linux | A virtual display (`xvfb-run`) or the toolkit's offscreen platform; screenshot from there |
| iOS | Simulator: `xcrun simctl io booted screenshot <path>`; deep links via `xcrun simctl openurl` |
| Android | Emulator: `adb exec-out screencap -p > <path>`; deep links via `adb shell am start` |
| Backend | Start the service, call it with real requests, capture request and response and the relevant log lines. Check status codes, error shapes and a failure path |
| CLI | Run it with real arguments, capture stdout, stderr and exit code, including a bad-argument case and `--help` |

Heavy runs (release builds, emulators, full suites) follow the machine rules in `shared/rules-full.md`: one at a time, through the lock helper where it exists. Scratch captures go in `~/AgentScratch/<task>/`; only the retained evidence goes to the repo, small (PNG, a few hundred KB each).

A still shows layout, clipping, presence, alignment, color and legibility. It does not show timing, responsiveness, animation feel or audio. Say which half the capture covered.

## What not to automate

- Judgment of visual quality and brand fit: a human or `design-director` looks at it.
- Feel: responsiveness, weight, animation curves, perceived performance.
- Real-device behavior that emulators misrepresent: push delivery, sensors, background limits, thermal and battery. Test on a device.
- Platform dialogs and permission prompts that cannot be driven without input injection.
- One-time exploratory testing of a new flow: do it by hand first; automate once the flow is stable and worth guarding.
- Anything whose automation would cost more to maintain than the manual check costs to repeat.

## Flaky tests

A flaky test is a bug in the test or in the code. Do not hide it.

1. Reproduce: run it in a loop (for example 50 times) and on the CI machine's conditions. Record the failure rate.
2. Find the cause: shared state, ordering, real time, real network, race on async work, resource leaks.
3. Fix the cause. Replace sleeps with waits on a condition; inject clocks; isolate state.
4. If it cannot be fixed now, quarantine it: move it to a named quarantine suite that still runs and reports, file a bug (`bug-report.md`) with the failure rate and an owner, and tell the user. A quarantined test that stops running is a deleted test.
5. Never mask flakiness with blanket retries. A bounded retry for a known-unreliable external dependency is allowed only for integration tests, reported as such.

## CI rules

- The full automated suite, lint and build run on every pull request and on every push to the main branch.
- A failing test, lint error or broken build blocks the merge. CI is a blocking gate, not a report.
- CI runs the same commands as `studio.yaml` `commands`, so a green local run means a green CI run.
- Never disable, skip or delete a failing test or check to pass CI.
- CI is reproducible: pinned toolchain versions, lockfiles committed, no dependence on a developer's machine. Secrets come from the CI secret store, never from files.
- Evidence that CI ran (a link or log excerpt) counts for Logic and Integration changes; UI, Visual and Data evidence is produced separately and retained.
- A check that cannot run reports that it did not run. Silence is never a pass.
