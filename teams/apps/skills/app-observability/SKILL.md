---
name: app-observability
description: "Design or audit how an app is observed once it is in users' hands: logs, metrics, traces, crash reporting with symbolication, product analytics boundaries, SLOs, alerts and runbooks, reviewed for privacy. Use when the user asks about monitoring, logging, crash reports, alerts, SLOs, 'how will we know it is broken', telemetry, analytics events, or before the first release, or after an incident exposed a blind spot."
argument-hint: "[app] [design | audit] [--review solo|lean|full]"
user-invocable: true
---

# App Observability

Answers one question: when this app breaks or degrades for a user, how do we find out, how fast, and with enough detail to fix it, without collecting what we should not. Works for services, web clients, desktop and mobile apps, command-line tools and libraries; what "observing" means differs sharply by platform, so the design is routed by `platforms`.

Writes: `docs/ops/observability.md`, `docs/ops/slo.md` (when SLOs are defined), runbooks `docs/ops/runbooks/<topic>.md` (template `runbook.md`).
Next: `/app-privacy-review` (if data findings), `/app-plan` (stories for the gaps), `/app-test-setup` (CI steps for symbols), `/app-gate` (release to operate), `/app-incident`.

## When to use and when not to

- Mode `design` for an app with no observability record (before or during foundation, and before the first release). Mode `audit` for one that exists, after an incident, or when adopting an app. If unspecified: `audit` if `docs/ops/observability.md` or telemetry code exists, else `design`.
- Not for choosing product metrics and experiments from scratch (the `analytics-specialist` is a participant here, but a full measurement plan is its own product decision), not for an incident in progress (`/app-incident`), not for performance budgets (`/app-perf`).

## Inputs

- `studio.yaml` (`platforms`, `stack`, `hosting`, `infra_record`, `rules`); architecture doc (deployment, trust boundaries, budgets); `docs/security/privacy.md`; the threat model; existing runbooks; `docs/product/` for the user journeys that matter.
- For `audit`: the code and config. Search for logging calls, crash-reporting SDK initialization, metrics and tracing libraries, health endpoints, analytics calls, CI steps that upload symbols or source maps. Each count states its denominator ("14 of 112 log calls include a user identifier").
- Facts about hosting dashboards, alert routing, retention settings or vendor consoles cannot be read from the repo. Ask the user; label answers user-stated; an unknown stays `UNKNOWN` and makes that item NOT ASSESSED.

## Platform routing

| Platform | What to observe | Specific concerns |
|---|---|---|
| backend, services | structured logs with request and correlation ids; RED metrics (rate, errors, duration) and saturation; distributed traces across services and queues; health and readiness endpoints; dependency health; synthetic checks | log volume and cost, sampling, cardinality of metric labels, propagation of trace context through jobs |
| web | real-user performance (Core Web Vitals), JavaScript errors with source maps, failed network calls, CSP and other reports; server side as for services | source maps uploaded per build and not publicly served, consent for analytics, ad blockers hiding data (state the blind spot) |
| desktop (windows, macos, linux) | crash reports with minidumps or equivalent and symbols, local log files with rotation, update success and failure, startup time, opt-in usage telemetry | symbols archived per build (PDB, dSYM, debug files), crash dump contents can include user data, offline queueing, user-controlled opt-out |
| mobile (ios, android) | crash and ANR or hang reporting, store vitals, app start and frame metrics, network errors, release health by version | dSYM and mapping or native-symbol upload per build, breadcrumbs without personal data, OS-level privacy prompts and labels, background limits on uploads |
| cli | exit codes and error classes, a `--verbose` or debug log flag, opt-in anonymous usage if any, a version command | no phone-home by default, never log arguments that may hold secrets, crash output safe to paste into an issue |
| extension | error reports through the extension's own channel, permission-limited | store policy on data collection, no remote code |
| library | none in production by design; diagnostics hooks and clear error types for the host app | do not emit telemetry from a library |

`site-reliability-engineer` owns operational signals, SLOs, alerts and runbooks. `analytics-specialist` owns product events and the line between product analytics and operational telemetry. `privacy-specialist` reviews everything that leaves the device or lands in a log.

## Phase 1: Resolve and scope

Follow `orchestration.md` sections 1 and 2; print the plan block. Gates: none are defined for this skill. The privacy review below is part of its work, not a gate, so it runs at every review mode. Confirm the mode and which user journeys matter most (up to five). Choose the layers from the routing table; list the layers marked "not applicable" with a reason.

## Phase 2: Current state (audit) or inputs (design)

Parallel, read-only, each writing a draft file under `.studio/drafts/`:

- `site-reliability-engineer`: what exists for logs, metrics, traces, crash reporting, alerts, runbooks and symbol handling; where it is configured; what is missing for the platforms; backups and retention if relevant. Output `.studio/drafts/observability-site-reliability-engineer.md`.
- `analytics-specialist`: existing events, naming, properties, consent handling, and what questions the product needs answered. Output `.studio/drafts/observability-analytics-specialist.md`.
- Main session: the Grep counts above; read the CI config for symbol and source map steps.

Verify two claims by opening the cited file. In `design` mode the same agents list what the platforms require instead of what exists.

## Phase 3: Design the layers

`site-reliability-engineer` drafts, `analytics-specialist` drafts the product-event boundary; each writes its part to the same drafts folder (`observability-<agent>-design.md`). The main session assembles `docs/ops/observability.md` with these sections (omit a section only with a stated reason):

1. **Journeys and signals:** per critical journey, the user-visible success definition and the signal that measures it.
2. **Logs:** schema (timestamp, level, message, correlation id, component, version), levels and what each means, what must never be logged (credentials, tokens, full payloads, personal data), redaction, retention, where they go and how a user-submitted log is made safe.
3. **Metrics:** (OpenTelemetry where the stack supports it, so signals are not locked to one vendor) names, types, units, labels with bounded cardinality, who reads them.
4. **Traces:** span boundaries, context propagation, sampling. Not applicable to local-only apps.
5. **Crash and error reporting:** the tool or approach, what each report contains and omits, user consent where the platform or law requires it, release health by version.
6. **Symbolication:** the symbol, mapping or source map artifacts for each platform; they are produced by the release build, uploaded in the release pipeline for every shipped version, kept as long as that version is supported, and access-controlled. Include how to verify: trigger a deliberate crash or error in a release-configured build and confirm the received report shows readable function names and lines. State which team step does this.
7. **Product analytics boundary:** which events are product analytics (consented, minimal) and which are operational (always on, no personal data); event naming convention; the list of events and properties.
8. **SLIs and SLOs** (written to `docs/ops/slo.md` and linked from `docs/ops/observability.md`; the layout's path for SLOs): per journey, an SLI as a ratio of good to total events, an SLO target and window chosen against the architecture's reliability budget, and an error budget policy (what happens when it is spent). Do not invent numbers: derive from the budgets, or mark `PROPOSED - needs the user's decision`.
9. **Alerts:** symptom-based alerts on SLO burn (multiwindow, multi-burn-rate: a fast window for pages and a slow window for tickets, per the Google SRE Workbook) and a small set of cause-based ones for known cliffs (disk, certificate expiry, queue depth). Each alert states severity (matching `standards/severity.md`), who is paged or notified, the runbook, and why a human must act. An alert without an owner or a runbook is a gap. Cap noisy alerts; state the review cadence.
10. **Dashboards and ownership:** the few views that answer "is it healthy", who owns each.
11. **Cost and retention:** volume estimate or "not estimated", retention per signal.

## Phase 4: Privacy review (privacy-specialist, after the drafts)

Spawn `privacy-specialist` with the assembled draft and `docs/security/privacy.md`. It writes `.studio/drafts/observability-privacy-specialist.md` covering: every field that can contain personal data (user ids, emails, IP addresses, device ids, free text, URLs with tokens, crash dump memory, screenshots); the lawful purpose and consent state for each; minimization, redaction and hashing choices; retention and deletion path for a user request; third-party processors and their disclosures; consistency with store privacy declarations; telemetry off by default where required or promised. It returns findings as BLOCK, CONCERN or OK per item. Any BLOCK is applied to the design before the doc is finalized, or recorded as an open gap that makes the verdict GAPS. Update `docs/security/privacy.md` only through `/app-privacy-review`; recommend it if the inventory is out of date.

## Phase 5: Runbooks

For every alert and for the top failure modes (a failed deploy, a bad release, data restore, a certificate expiry, a dependency outage, a crash spike), `site-reliability-engineer` writes `docs/ops/runbooks/<topic>.md` from `runbook.md`: symptoms, first checks, diagnosis steps with real commands or console paths, mitigation options, rollback, escalation, and verification that it worked. One file per agent invocation; check each exists with content. A runbook that has never been read against the real system is marked `UNTESTED`.

## Phase 6: Verify

Checks that prove the phases happened; run them, do not infer:

1. Every layer applicable to `platforms` is designed or has a stated N/A reason: count "n of n layers".
2. Every alert has an owner and an existing runbook file: "n of n".
3. Every SLI names a data source that exists in the design.
4. `audit` mode: the Grep counts for risky log content are recorded with the denominator; the CI config either uploads symbols or the gap is listed.
5. The symbolication check (item 6 above): run the deliberate-crash test where a release-configured build and a reporting backend are available; otherwise the item is NOT ASSESSED and says what is needed.
6. The privacy review returned and every BLOCK is resolved or listed.
7. Read `docs/ops/observability.md` back; no template placeholders remain.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Layers | logs, crash and error reporting with symbols, a health check for deployed apps | plus metrics, SLOs for the top journeys, symptom alerts, runbooks for each alert | plus traces, error budget policy, synthetic checks, dashboards, on-call and review cadence, tested runbooks |
| Always | privacy review; symbols archived per release; nothing sensitive in logs | | |

Review mode does not change this skill; no gates are defined for it. Rigor relaxes which layers must exist, not the privacy review or the "no sensitive data in logs" rule.

## Verdicts

First match wins.

1. **GAPS:** an applicable layer has no design or no implementation (in audit), an alert has no owner or runbook, a privacy BLOCK is open, symbols for shipped versions are not retained, or sensitive data is found in logs or events.
2. **NOT ASSESSED:** something the verdict turns on could not be checked (no access to the console or dashboards, the symbolication test could not run, the privacy review did not return, platform unknown).
3. **COMPLETE:** every applicable layer for the rigor is designed (and, in audit mode, found in place), the checks in Phase 6 hold, and the privacy review has no open BLOCK.

## Report

```
Observability: <app>  Mode: <design|audit>  Platforms: <list>  Rigor: <r>  Review: <mode>
Layers: <n of n designed or present>   Alerts with runbook and owner: <n of n>
Symbolication verified: <yes|NOT ASSESSED - why>   Privacy: <n BLOCK, n CONCERN, n OK>
Verdict: <WORD> - <one line why>
Gates: none run (no gate defined for this skill)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Privacy-specialist reviews every design; nothing that logs or sends personal data is finalized without it.
- Never put credentials, tokens or personal data in a design example, a log schema sample or a runbook.
- No invented targets: SLO numbers come from the app's budgets or are marked PROPOSED for the user.
- Crash reporting without symbolication is not crash reporting; say so when symbols are missing.
- Counts carry denominators; facts about consoles and dashboards are user-stated or UNKNOWN.
- Design only what the platforms need. A cli or library does not get a metrics pipeline.
- Recommend the next skill; never start it.
