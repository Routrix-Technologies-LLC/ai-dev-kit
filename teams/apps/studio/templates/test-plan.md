<!--
Template: test-plan. Written by: qa-lead with test-engineer. Skill: /app-qa-plan.
Lives at: docs/qa/test-plans/<scope>.md (override: paths.test_plans). Scope is a sprint, feature or release.
Rigor: minimal = summary table and definition of done. standard = adds automated tests required, manual checklist, platform matrix, smoke scope. full = adds device lab detail, soak and edge-case plan, data and account fixtures, exit criteria with numbers.
Delete this comment when the plan is created.
-->

# Test plan: [scope]

> **Scope**: [sprint id | feature | release version]
> **Author**: [agent]   **Date**: [YYYY-MM-DD]
> **Status**: [Draft | Approved | Executed]

## Summary by change type

| Change type | Stories or changes | Evidence required | Automated | Manual |
|---|---|---|---|---|
| Logic | [IDs] | Unit tests passing | [n] | 0 |
| Integration | [IDs] | Integration run output | [n] | [n] |
| UI | [IDs] | Screenshots per state and platform | [n] | [n] |
| Visual | [IDs] | Screenshots compared with the design | [n] | [n] |
| Data | [IDs] | Migration rehearsal and round trip | [n] | [n] |
| Config / Infra | [IDs] | Dry run or before/after output | [n] | [n] |
| Security | [IDs] | Control test or scan output | [n] | [n] |
| Performance | [IDs] | Measurements against perf-budget.md | [n] | [n] |
| Docs | [IDs] | Link check | [n] | [n] |

## Automated tests required

| Test | Level (unit / integration / e2e) | Covers (AC or REQ) | Exists | Command |
|---|---|---|---|---|
| [name or file] | [level] | [IDs] | [yes / to be written in story-NNN] | [from studio.yaml] |

Rules: a regression test for a fix is seen failing before the fix. Tests do not depend on wall-clock time, network or ordering. A skipped test is listed with a reason and a TD row.

## Manual checklist

| # | Area | Setup | Verify | Pass | Platform | Result |
|---|---|---|---|---|---|---|
| M1 | [feature or flow] | [state, data, account] | [steps] | [observable outcome] | [which] | [ ] |

Include: first run, empty state, error and offline states, interruption (call, sleep, resume), upgrade over the previous version, uninstall, and keyboard-only and screen-reader passes for changed UI.

## Platform and device matrix

| Platform | OS / browser versions | Devices or form factors | Build tested | Owner | Automated or manual |
|---|---|---|---|---|---|
| [web] | [oldest supported, current, latest browsers from min_targets] | [desktop, tablet, phone widths] | [build id] | [...] | [...] |
| [windows / macos / linux] | [oldest and newest supported] | [Intel/ARM, display scaling, dark/light] | | | |
| [ios / android] | [oldest supported and current] | [small phone, large phone, tablet, low-end device] | | | |

State what is NOT covered and why (for example no physical device available). That list is part of the plan.

## Smoke scope

The shortest path that proves the build is alive on each target (used by /app-smoke): [launch, sign in, create the core object, save, reopen, quit cleanly].

## Fixtures and environments

[Test accounts (no real credentials in this file), seed data, feature flags, backend environment, how to reset state.]

## Definition of done

- [ ] Every automated test above passes on every target; counts recorded with denominators
- [ ] Every manual item executed and recorded, or listed as NOT ASSESSED with a reason
- [ ] Evidence exists on disk for each UI, Visual, Performance and Security change
- [ ] No open S1 or S2 bugs; S3 and S4 triaged
- [ ] Smoke passes on each target
- [ ] Sign-off by qa-lead: [name, date]
