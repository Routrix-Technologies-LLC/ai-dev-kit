<!--
Template: bug-report. Written by: any agent that finds a bug; qa-lead triages; escalation-engineer for hard ones. Skill: /app-bugfix (and /app-smoke, /app-story-done when they find defects).
Lives at: docs/qa/bugs/BUG-NNNN-<slug>.md (override: paths.bugs), or the app's issue tracker if it has one (then paste this structure into the issue).
Rigor: minimal = title, severity, steps, expected, actual. standard = adds priority, frequency, platform and version, evidence, regression test. full = adds root cause, fix notes, affected versions and verification on every platform.
Delete this comment when the report is created.
-->

# BUG-[NNNN]: [short, specific title]

> **Status**: [Open | Confirmed | In progress | Fixed | Verified | Closed | CANNOT REPRODUCE]
> **Reported**: [YYYY-MM-DD by agent or person]
> **System / area**: [module, screen or service]
> **Severity**: [S1 Critical | S2 High | S3 Medium | S4 Low]
> **Priority**: [P0 | P1 | P2 | P3]
> **Frequency**: [Always | Often (n of n tries) | Sometimes | Once]
> **Platform and version**: [OS and version, browser or device, app version and build, backend version]
> **Regression?**: [Yes, since version/commit | No | Unknown]

Severity is impact (S1 data loss, security exposure, crash on launch or no workaround; S2 major function broken; S3 minor function broken with workaround; S4 cosmetic). Priority is urgency (P0 now, P1 this release, P2 soon, P3 backlog). They are separate calls.

## Steps to reproduce

1. [Start state: build, data, account, settings]
2. [Action]
3. [Action]

Reduced to the smallest reliable sequence: [yes / not yet]

## Expected result

[What should happen, citing the spec or REQ ID if there is one.]

## Actual result

[What happens, with the exact error text, code or stack trace excerpt.]

## Evidence

| Kind | Path or link |
|---|---|
| Screenshot or recording | `docs/qa/evidence/BUG-[NNNN]/[file]` |
| Log excerpt (redacted of secrets and personal data) | [...] |
| Crash report or trace | [...] |

## Analysis (fill when known)

- Root cause: [file:line and why]
- Why it was not caught: [missing test, untested platform, ...]
- Workaround: [none | description]

## Regression test

- Test reference: `[path::name]`, seen failing before the fix: [yes / no]; seen passing after: [yes / no]
- If no automated test is possible, the manual case: [Setup / Verify / Pass]

## Fix

- Fix commit or story: [...]
- Verified on: [platforms and builds]
