# Run and observe: how to look at a change

Used by `app-dev-story` (Phase 6), `app-bugfix` (Phase 6) and read by `app-story-done` to judge evidence. Principle: `orchestration.md` section 10. A build that compiles and tests that pass do not show that the text fits, the screen appeared, the request returns the right body or the command prints the right thing. Someone (you) must look at the running app and keep what was seen.

## The rules

1. **Never steal focus or drive the user's desktop.** No keystrokes or clicks sent to the shared desktop session, no window forced to the front. Use headless or background modes, the app's own automation interface, or test hooks. If the only route is one that would take over the screen or needs injected input, the result is NOT VERIFIED with that reason. It runs only when the brief says the user is away from the computer, for that run; permission to do it once does not carry over.
2. **Prefer the app's own command.** If `commands.screenshot` or `commands.e2e` in `studio.yaml` covers the case, use it. Otherwise use the table below.
3. **Reach the state the change touches.** A screenshot of the home screen proves nothing about the third step of a flow. Use a launch argument, deep link, route, seeded test data or fixture to land on the surface. If the state cannot be reached, say so: that is NOT VERIFIED, and a finding for the story ("surface not reachable without N manual steps").
4. **Run the build the user will run.** If `studio.yaml` `rules:` names a build the user tests from (for example a release build), build and run that one.
5. **Retain the evidence.** Capture straight into `docs/qa/evidence/<story-or-change>/` (the `paths.evidence` override applies), named `NN-what-it-shows.png`. Keep images small (a few hundred KB; scale or crop). A screenshot taken and discarded is an assertion, not evidence.
6. **Open and look.** Use the Read tool on each image (it renders PNG and JPG). Compare with each acceptance criterion: clipped or overflowing text, missing element, wrong state, wrong theme, unreadable contrast, layout broken at the narrow width. Never describe an image you have not opened.
7. **Redact.** No secrets, tokens or real personal data in a retained capture or log excerpt. Use test accounts and seeded data.
8. **Heavy runs use the lock.** Emulators, simulators, release builds and full end-to-end suites run through `~/Tools/agent_locks/run_locked.sh cpu <command>` (`gpu` for anything that opens a window or uses the GPU) when it exists, otherwise one at a time. Exit code 75 means the user is gaming: stop, keep what exists, report NOT VERIFIED for what did not run. Scratch captures go in `~/AgentScratch/<task>/`; only the retained, small evidence is copied into the repo.
9. **Stamp it.** Write `docs/qa/evidence/<story-or-change>/evidence.md` from `templates/test-evidence.md`: date, `git rev-parse HEAD`, the changed files, the command or steps used, each capture and what it shows, and which half it covers (look or behaviour). `app-story-done` compares the evidence's age with the changed files; a later edit to a changed file makes the evidence stale.

## By platform

| Surface | Launch | Capture | Cover at least |
|---|---|---|---|
| Web app | Start the dev or preview server from `commands.run`, wait for the URL to answer, drive a headless browser (Playwright or the app's e2e tool) | Page or element screenshot, plus the browser console and failed network requests | A narrow phone width and a desktop width; light and dark when the app themes; the empty, loading and error states the story names |
| Browser extension | Load the unpacked build in a headless-capable browser through the e2e tool | Screenshot of the popup, options page or injected UI | Each surface the story touches |
| Windows desktop | Launch the built app (hybrid shells: the shell, not the dev server alone). Under Git Bash set `MSYS_NO_PATHCONV=1` for arguments that start with `/`, and wrap the launch in `timeout` | The app's own screenshot flag or test hook; else a window capture of that one window that does not need it in front (PrintWindow or Windows Graphics Capture from a small script); else UI Automation to read the control tree (reading only, never invoking controls) | Default DPI and a scaled DPI when layout changed; light, dark and high contrast when theming changed |
| macOS desktop | `open -g` or launch in the background | `screencapture -l <window id>` captures one window without focus (needs the Screen Recording permission, which the user grants once); else the app's own hook | Light and dark; a Retina scale |
| Linux desktop | Run under a virtual display (`xvfb-run`) so nothing appears on the user's screen | Capture the virtual display or window; on Wayland-only toolkits use the compositor's or portal's capture tool | The toolkit's light and dark themes |
| iOS or iPadOS | Boot a simulator, install, launch (`xcrun simctl boot`, `install`, `launch`) | `xcrun simctl io booted screenshot <path>`; appearance via `simctl ui` | Smallest and largest supported device class; light and dark; large text when layout changed |
| Android | Start an emulator (a no-window mode still renders), `adb install`, `adb shell am start` | `adb exec-out screencap -p > <path>` | Smallest and largest supported screen class; light and dark; large font when layout changed |
| Cross-platform mobile | Both targets the story touches | As above, one per platform | A change that affects both platforms needs both; one unobserved platform is NOT VERIFIED for that platform |
| Backend service | Start with the test or local config from `commands.run`; seed data through the app's own fixtures | The request and response (status, headers that matter, body) from `curl` or the tests' client, redacted; the relevant log lines; for data changes a read-only query showing the row | Success path, one validation failure, one auth failure when auth is involved |
| CLI | Run the built binary or `commands.run` with the story's arguments | stdout, stderr and the exit code, pasted into `evidence.md`; for help or output format changes, the exact text | Success, a bad argument, and output piped (non-terminal) when formatting changed |
| Library or SDK | Run the smallest consumer or example that uses the changed API | Its output | The public call the story changed |
| Infra or Config | Plan, dry run or validate command for the tool | Its output; for a deployed change a health check | See `standards/testing.md` |

**Keyboard-only pass (UI stories).** Drive it with the browser's own automation (Playwright keyboard events inside the page are fine), or the toolkit's accessibility tree, and note in `evidence.md` the tab order and that each control activates. Where that needs OS-level keystrokes on the real desktop, record `keyboard-only pass NOT VERIFIED: needs input injection` and list it as a manual check for the user.

## What a still can and cannot show

A still shows layout, clipping, presence, alignment, colour, legibility and that the right screen appeared. It does not show timing, responsiveness, animation, scrolling feel or sound. Say which half the evidence covers. A criterion about the second half is verified by a test that measures it, a screen recording where the platform allows one, or the user's own check recorded as such.

## The result line

Exactly one line, plain text, no bold (the next skill reads it as written):

```
Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why it could not be run> | N/A - <why nothing is observable>
```

- `OBSERVED` needs a retained file and the fact that you opened it.
- `NOT VERIFIED` is a blocker for closing a UI or Visual story. Reasons are concrete: "no simulator available", "`commands.run` unset", "launch crashed (log excerpt)", "surface unreachable without manual login".
- `N/A` is only for a change with nothing observable at all (a build-file change that alters no output, an internal rename with no behaviour change). "It is a logic change" is not a reason when the change alters anything a user sees, receives or reads. A backend change is observable: the response.
