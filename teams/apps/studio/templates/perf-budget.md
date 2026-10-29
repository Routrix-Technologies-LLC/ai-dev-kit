<!--
Template: perf-budget. Written by: performance-engineer with the platform specialists; technical-director approves budgets. Skill: /app-perf (creates it if absent; measurements update the current-value columns).
Lives at: docs/qa/perf-budget.md (a studio.yaml `paths:` note if kept elsewhere). Dated measurements per run go in docs/qa/perf-<date>.md.
Rigor: minimal = three to five budgets that matter for this app. standard = a row for every metric below that applies, with method and current value. full = adds percentiles, device tiers, trend history and regression thresholds in CI.
Delete this comment when the budget is created. Delete rows that do not apply and say why in Notes. A budget with no measurement is "unmeasured", never "met".
-->

# Performance budget

> **Last measured**: [YYYY-MM-DD]   **Build**: [version, commit, release configuration]
> **Reference hardware**: [lowest supported device or machine per platform; budgets are set against the slow end, not the developer's machine]

## Budgets

Measure release builds, not debug. Repeat each measurement at least [5] times and report the median and the spread.

| Platform | Metric | Budget | Measurement method | Current value | Date | Status |
|---|---|---|---|---|---|---|
| [all desktop and mobile] | Startup, cold (process start to interactive) | [n ms] | [tool and procedure, cold means after reboot or cache purge] | [..] | | [Within / Over / Unmeasured] |
| | Startup, warm | [n ms] | | | | |
| | Memory, steady state (resident set) | [n MB] | [profiler, after 10 minutes of the core scenario] | | | |
| | Memory growth over a long session | [n MB per hour, or "no growth"] | [soak run] | | | |
| | CPU while idle | [n percent] | | | | |
| | CPU in the core scenario | [n percent] | | | | |
| | Frame time and jank (UI) | [p95 under 16.7 ms at 60 Hz; under n percent dropped frames] | [platform profiler] | | | |
| | Input latency | [n ms] | | | | |
| [web] | Largest Contentful Paint | [under 2.5 s at p75] | [lab: Lighthouse on throttled profile; field: RUM] | | | |
| [web] | Interaction to Next Paint | [under 200 ms at p75] | | | | |
| [web] | Cumulative Layout Shift | [under 0.1 at p75] | | | | |
| [web] | JavaScript shipped per route (compressed) | [n KB] | [bundle analyzer] | | | |
| [all] | Bundle, binary or installer size | [n MB] | [built artifact on disk] | | | |
| [backend] | API latency p50 / p95 / p99 | [n / n / n ms] | [load test at stated concurrency] | | | |
| [backend] | Throughput at target latency | [n req/s] | | | | |
| [backend] | Error rate under load | [under n percent] | | | | |
| [mobile] | Battery drain in the core scenario | [n percent per hour] | [platform energy tools, device unplugged] | | | |
| [all] | Network use per core action | [n KB] | | | | |
| [all] | Disk writes / storage growth | [n] | | | | |

## Regression rule

A change that pushes any metric more than [10 percent] over its last value, or past its budget, needs a note in the story and a Performance evidence file. CI thresholds: [which metrics are automated and where].

## Method notes

[Tools, device state (battery saver off, thermal state, plugged in), network profile, data set size, how variance was handled, anything that makes numbers incomparable across runs.]

## History

| Date | Build | Metric | Value | Note |
|---|---|---|---|---|
