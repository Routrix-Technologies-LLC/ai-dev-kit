---
name: app-perf
description: "Measure an app's performance against its committed budgets on each target, with method, variance and before/after evidence. Use when the user asks about performance, speed, startup time, memory, jank, bundle size, battery, load, or whether the app is within budget, or after a change that could affect any of those."
argument-hint: "[app] [scope: full | startup | memory | render | network | size | load | <flow>] [--baseline <git ref or report>] [--review solo|lean|full]"
user-invocable: true
---

# App performance profile

Measures the app on each target it supports and compares the numbers to the budgets the team committed to. Measurement is the point: reading code produces candidates, not results. A report with no measurements, or measurements against a budget nobody set, is not a pass.

Writes: `docs/qa/perf-<date>.md` (the profile), and `docs/qa/perf-budget.md` from template `perf-budget.md` only when no budget exists and the user agrees to set one. Evidence (profiler exports, traces, screenshots) in `docs/qa/evidence/perf-<date>/`.
Next: `/app-plan` or `/app-bugfix` for over-budget items, `/app-adr` if the fix is architectural, `/app-gate` or `/app-release` read the result.

## When to use and when not to

Use to establish a baseline, to check a change, before hardening or release, or when something feels slow. Not for: a failing test (`/app-bugfix`), a hard intermittent leak or hang that needs root cause (`/app-bugfix`, which routes to `escalation-engineer`), or a production incident (`/app-incident`). Load testing a deployed service is in scope only for environments the user names.

## Inputs

- `studio.yaml` (required): `platforms`, `stack`, `commands` (`build_release`, `run`, `screenshot`), `min_targets`. Stop and offer `/app-adopt` or `/app-start` if absent.
- Budgets (required for a verdict): `docs/qa/perf-budget.md`, else budget sections in `docs/architecture/architecture.md` or the brief. Record each as FOUND or ABSENT, never assumed.
- A release-mode build. Profiling a debug build is only valid for a metric that is build-independent (a query plan, an algorithmic count); everything else needs `commands.build_release`.
- Optional: a previous `docs/qa/perf-*.md` or `--baseline` ref for before/after.

## Phase 1: Budgets

Main session. Read the budget file and list every metric with its number, unit, the target (device class, OS, browser, network profile) it applies to, and who set it. A budget with no number, no target or a placeholder value counts as absent.

If no budget exists for any metric:

1. State that the verdict will be NO BUDGET.
2. Offer to create one now from template `perf-budget.md`. Spawn `performance-engineer` to draft a proposal from the platforms and the metric table below, with each number marked PROPOSED and its rationale (platform guidance, comparable apps, user-perceptible thresholds). The user chooses every number; ask once for the set. Budgets are owned by `qa-lead` with `technical-director`, so mention that the user may want a `technical-director` review of the numbers.
3. Never fill a budget with a number nobody chose. If the user declines, continue to measure and report values, and the verdict is NO BUDGET.

Metrics by platform (pick what applies; each needs a budget to be judged):

| Platform | Metrics |
|---|---|
| web | LCP, INP, CLS, TTFB, JS and CSS transfer size by route, total requests, long tasks, memory growth over a session, API p95 as seen by the client |
| desktop | cold start to first interactive window, warm start, idle and working-set memory, CPU at idle and under a standard flow, frame time and jank in heavy views, disk and installer size, energy impact where the OS reports it |
| mobile | cold and warm start, frame drops (jank) per flow, memory peak and leaks across navigation, binary and download size, battery and wakeups in background, network bytes per flow, behavior on the lowest supported device class |
| backend | latency p50/p95/p99 per endpoint at a stated load, throughput, error rate under load, saturation (CPU, memory, connections), cold start for serverless, query time for the worst queries, queue lag |
| cli | startup time, time and peak memory on a standard input size, behavior on a large input, binary size |
| library | benchmark per public hot path, allocation count, size added to a consumer |

Check: a Budget table with FOUND or ABSENT per metric is written into the working notes, or the NO BUDGET path was taken and announced.

## Phase 2: Plan the run

Main session. Announce per `orchestration.md` section 2. Select agents: `performance-engineer` always; the platform specialist(s) from `studio.yaml` `specialists` and `platforms` to run the app and its profiler correctly (for example `windows-desktop-engineer`, `macos-engineer`, `ios-engineer`, `android-engineer`, `web-framework-specialist`, `backend-engineer`, `hybrid-desktop-engineer`, `cross-platform-mobile-engineer`); `test-automation-engineer` when a repeatable scripted flow is needed.

Decide per metric and target: how it is measured, on what device or environment, with what data size, how many runs. Define the standard flows from the brief or specs (the three to five journeys users do most). If target hardware is not available (no real low-end device), say so: results from a faster machine or an emulator are labelled as such and a budget for the slow class stays NOT ASSESSED.

Ask the user before: running load against any shared or deployed environment, anything that costs money or calls a paid service the app does not already use, and anything that could disturb the user's own running copy of the app. Never close or interfere with a user's running instance.

Check: a run plan lists metric, target, method, tool, run count. Nothing is measured without an entry.

## Phase 3: Measure

Spawn `performance-engineer` (and platform specialists) in parallel per orchestration section 4, one output file each under `docs/qa/evidence/perf-<date>/`. Brief per section 3 with the budget table, the run plan, and these method rules:

- Use the release configuration the user ships, from `commands.build_release`.
- Cold versus warm is stated for every start-up number. Caches, data size and network profile are stated.
- At least a stated number of runs per measurement (default 5 for fast metrics, fewer for slow ones with the reason given); report the median and the spread (min and max, or p95). One run is an anecdote.
- A comparison to a budget uses the unfavorable end of the spread. If the spread straddles the budget, the status is INCONCLUSIVE, which counts as NOT ASSESSED, and the fix is more runs or a quieter machine.
- Record the environment: OS and version, hardware class, build id or commit, other load on the machine.
- Capture without stealing focus (section 10): headless browser, offscreen capture, simulator or emulator, request capture for services.
- Lab measurements (a Lighthouse-class run, a simulator, a laptop) are labeled lab data and are not field data; a field-data budget (for example Core Web Vitals at the 75th percentile) without field data is NOT ASSESSED.
- Heavy runs (release builds, load, emulators) go one at a time.
- Static findings (hot loops, N+1 queries, large bundles, main-thread work) are listed separately as CANDIDATES. They are never reported as measured results and never change a metric status.
- Never optimize in this skill. Measure and report.

Return contract appended verbatim. Check: each named evidence file exists and holds raw numbers with run counts; a file without numbers is a failed phase (re-brief once, then BLOCKED for that metric).

## Phase 4: Before and after

If the run follows a change, or a baseline exists (`--baseline` ref, or the newest earlier `docs/qa/perf-*.md`), the same method must be run on the baseline: check out the ref in a separate worktree or build directory, never in the user's working tree, and measure with the same plan. Table each metric: before (median, spread), after (median, spread), delta, and whether the delta exceeds the combined spread. A delta inside the noise is reported as "no measurable change", not as an improvement or regression.

If no baseline can be built or found, say `before: not measured` and the verdict is not affected, but no improvement or regression claim may be made. When the user is about to optimize something, run this skill first so the baseline exists.

Check: either the before/after table exists with both sides measured, or the report states "no baseline" in the summary line.

## Phase 5: Report and decisions

Main session. Spot-check the claims the verdict turns on: re-run one measurement yourself or read the raw trace for the worst metric. Label unchecked specialist claims `UNVERIFIED`.

Write `docs/qa/perf-<date>.md`: budget table with status per metric (WITHIN, OVER, NOT ASSESSED, INCONCLUSIVE), method and environment, before/after, candidates, ranked recommendations (each with expected gain, risk, effort and the location). Keep NOT ASSESSED rows in the file.

For each OVER BUDGET item with M or L effort, ask once: fix now (route to `/app-plan` or `/app-bugfix`), cut scope, accept and record in `planning/tech-debt.md` or `docs/decisions.md`, or escalate to `technical-director` (`/app-adr`). A skipped answer is not an answer.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Metrics | startup and one memory number per platform | all budgeted metrics on primary target | all metrics on every target and the lowest supported device class |
| Runs | fewer, spread still reported | default | default plus soak (long session memory growth) |
| Baseline | optional | when a prior report exists | required for any change-driven run |

No gate runs in this skill; `/app-gate` and `/app-release` consume the report. At every mode, an OVER BUDGET result stands.

## Verdicts

First match wins:

1. **OVER BUDGET**: any measured metric exceeds its budget at the unfavorable end of its spread on a target the app supports.
2. **NO BUDGET**: no metric has a usable budget and the user did not set one in Phase 1. Values are still reported, with no judgement.
3. **NOT ASSESSED**: some budgeted metric or target could not be measured (no device, no release build, INCONCLUSIVE, tool unavailable, load test not approved), or a profile ran over zero flows. Name each and what closes it.
4. **WITHIN BUDGET**: every budgeted metric measured on every supported target class, inside budget with spread considered.

## Report

```
Performance: <app>   Date: <date>   Build: <commit/version, release|debug>   Targets measured: <list>   Not measured: <list>
Budget source: <path> | none (user declined)
Metric: <name> | budget <v> | median <v> (min-max or p95) over <n> runs | <WITHIN|OVER|INCONCLUSIVE|NOT ASSESSED|no budget>
...
Before/after: <table summary> | no baseline
Top candidates (static, unmeasured): <up to 3>
Decisions for you: <options> | none
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Never report headroom against a budget nobody set, or a placeholder budget.
- Never present a static finding or an estimate as a measurement.
- Never report a single run without saying so, and never hide the spread.
- Never judge a comparison that sits inside the noise.
- Never profile on a debug build and call it the shipped behavior.
- Never touch the user's running instance, shared environments or paid services without asking.
- Never change production code here; optimization is a separate, planned change.
