<!--
Template: test-evidence. Written by: test-engineer or the builder who ran the checks; qa-lead signs off. Skill: /app-dev-story writes it, /app-story-done verifies it.
Lives at: docs/qa/evidence/<story-or-change>/evidence.md with the screenshots beside it (override: paths.evidence). Keep images small (PNG, a few hundred KB).
Rigor: minimal = AC results and Run result line. standard = adds screenshots table, test conditions, observations. full = adds both light and dark / all locales / all supported platforms and a named sign-off.
Delete this comment when the file is created. Every file named in the screenshots table must exist on disk.
-->

# Test evidence: [story or change]

> **Story / change**: [path or ID]
> **Change type**: [Logic | Integration | UI | Visual | Data | Config | Infra | Security | Performance | Docs]
> **Date**: [YYYY-MM-DD]   **Tester**: [agent or person]

## Acceptance criteria results

| AC | Criterion (short) | Result | Evidence |
|---|---|---|---|
| AC-1 | [text] | [PASS / FAIL / NOT ASSESSED] | [test name, screenshot file, or log path] |

A criterion without evidence is NOT ASSESSED, not a pass.

## Automated test results

| Suite | Command | Passed / total | Failed | Skipped (why) |
|---|---|---|---|---|
| [unit] | `[command]` | [n / n] | [n] | [n] |

## Screenshots

| File | What it shows | State and platform | Verified present |
|---|---|---|---|
| `[01-empty-state.png]` | [description] | [empty, light, windows] | [yes] |

Capture without taking focus: headless browser, offscreen window capture, simulator or emulator screenshot. Cover each changed state: default, empty, loading, error, long text, disabled, focus, dark mode, and the narrowest and widest layouts.

## Test conditions

| Item | Value |
|---|---|
| OS and version | [...] |
| Browser and version, or device and model | [...] |
| App build (version, commit, debug or release) | [...] |
| Locale, language, text scale, theme | [...] |
| Data and account used | [fixture names only, no credentials] |
| Network | [online / offline / throttled] |

## Run result

Run result: [OBSERVED - what was seen, evidence path | NOT VERIFIED - why it could not be run | N/A - why nothing is observable]

## Observations

[Anything surprising, even if it passed: flicker, slow frame, odd copy, behavior that differs by platform. File bugs for real defects and link them.]

## Sign-off

- Tester: [name, date]
- qa-lead review: [name, date, or pending]
