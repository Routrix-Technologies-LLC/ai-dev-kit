---
name: app-team-audit
description: "Whole-app health audit for an existing app: independent lenses in parallel (only those relevant to the app's platforms), a verification pass that tries to disprove the top findings, then one prioritized report and a proposed backlog. Use when the user asks for an audit, health check, 'what is wrong with this app', 'where should I invest', a second opinion on an inherited or old codebase, or after app-adopt."
argument-hint: "[app] [--scope all|<path or area>] [--lenses <list>] [--review solo|lean|full]"
user-invocable: true
---

# Team: Audit

The flagship for existing apps. It runs a set of independent expert lenses over the whole app (or a scope), then spends a separate pass trying to prove the biggest findings wrong, then merges what survives into one report ranked by severity, effort and impact, with proposed stories and tech-debt rows. It works for any platform and any language: lenses are chosen from `studio.yaml`, and every lens states what it could not check.

Writes: `docs/qa/audit/<date>/<agent>.md` (one per lens agent), `docs/qa/audit/<date>/00-baseline.md`, `docs/qa/audit/<date>/verify-<n>.md`, and the merged `docs/qa/audit/<date>/report.md`. After the user's yes: rows in `planning/tech-debt.md` (template `tech-debt-register.md`, `TD-NNN` IDs), entries in `planning/risks.md` (`RISK-NNNN`), bug records in `docs/qa/bugs/` (`BUG-NNNN`), and a story list handed to `app-plan` (which assigns the story IDs).
Next: `app-tech-debt`, `app-plan` (stories from the backlog), `app-bugfix`, `app-security-audit` or `app-perf` for a formal deep dive on one lens, `app-team-harden` before a release.

## When to use and when not to

- Use to learn the real state of an app: after `app-adopt`, before a big investment, when inheriting code, or yearly.
- One concern only (security, speed, accessibility): run that skill (`app-security-audit`, `app-perf`, `app-a11y-audit`). A diff or branch: `app-code-review`. Pre-release readiness: `app-team-harden`. Debt register only: `app-tech-debt`.
- This skill is read-only on the app's source. It never fixes anything; fixes are stories the user chooses.

## Inputs

- The app, per orchestration.md section 1. No `studio.yaml`: offer `/app-adopt` and stop; an audit of an app the studio has not mapped has no stack, commands or paths to rely on.
- `--scope`: default the whole repo. A narrower scope is stated in the report header and every denominator.
- `--lenses`: optional comma list to force or drop lenses. Forcing a lens that does not fit the app is allowed and announced.
- Read once and pass distilled: `studio.yaml`, `docs/qa/adoption-report.md`, the architecture doc, stack reference, threat model, privacy record, `planning/tech-debt.md`, `planning/risks.md`, the latest audit under `docs/qa/audit/` (to report what changed since). Each missing input is named; an absent architecture doc means the architecture lens reconstructs it from code and labels it so.
- Commands from `commands:` (build, test, lint, run, screenshot). A missing command makes the dependent check NOT ASSESSED, never skipped silently. Heavy runs go one at a time.
- Formal reports that already exist and are newer than the last source commit (`docs/security/audits/`, `docs/qa/perf-*.md`, `docs/qa/a11y-*.md`, `docs/qa/smoke-*.md`) are given to the matching lens to review and extend, not redone. A deep dive on one lens is the job of `app-security-audit`, `app-perf` or `app-a11y-audit`, recommended in Next, not re-implemented here.

## Phase 0: Resolve and choose lenses

Main session. Follow orchestration.md sections 1 and 2. Then choose lenses from the table using `platforms`, `stack` (including `stack.hosting`) and a quick look at the repo (manifests, whether it stores data, whether it has UI, locales, auth, personal data). Print the announce block with every lens either listed under "Agents this run" or under "Not spawned" with its reason.

| Lens | Agents | Spawn when | Not spawned when |
|---|---|---|---|
| Architecture | `principal-engineer` (plus the platform lead for each platform) | always | never |
| Code quality | `code-reviewer`, plus the language specialist(s) from `studio.yaml` | there is source | no source in scope |
| Security | `security-engineer`; plus `identity-specialist` if the app authenticates; `privacy-specialist` if it handles personal data | always (privacy and identity only on their condition; if unknown, ask) | never |
| Performance | `performance-engineer` | the app can be run or measured; static-only review is allowed and labeled | library with no runnable surface and no benchmarks: say so |
| Accessibility | `accessibility-specialist` | any platform with UI: web, windows, macos, linux, ios, android, extension with UI, CLI with a TUI or colored output | backend, library, plain CLI |
| UX | `ux-researcher` (heuristic evaluation, with `ux-designer` consulted) | there is UI, or a CLI with interaction design | backend, library |
| Tests and CI | `qa-lead`, `build-engineer` | always | never |
| Dependencies and licenses | `compliance-specialist` (licenses, notices) with CVE and supply-chain review owned by the security lens | a dependency manifest exists | none found: say so |
| Docs | `technical-writer` | always | never |
| Operations | `site-reliability-engineer` | the app is deployed (`hosting`, `infra_record`, or platform backend) | client-only app, unless it has crash reporting, telemetry or an update channel, then scoped to those |
| Data (optional) | `database-engineer` | the app stores data (server database, local store, file format) | no persistence |
| Localization (optional) | `localization-specialist` | more than one locale shipped, or user-facing strings exist | none |

Rigor changes the default set (see the rigor table). Ask the user once to confirm the lens list; this is the first decision point.

## Phase 1: Baseline

Main session, before any lens. Run once, from the repo root, read the output yourself, and write `docs/qa/audit/<date>/00-baseline.md`:

- `commands.build`, `commands.test`, `commands.lint` (skip any that is empty and say `not configured`). Never run deploy, migrate, publish or anything that mutates data outside the repo.
- Counts with denominators: source files and lines in scope, number of tests found and run, pass and fail counts, lint warnings, dependency count, languages detected.
- `git` facts: age of the last commit, commits in the last 90 days, number of contributors, large or binary files. Skip if not a git repo.

If the build fails, record it as a finding for the tests and CI lens and continue; lenses that need a build are told so and report NOT ASSESSED for the measured part.

## Phase 2: Lenses in parallel

Spawn every chosen lens in one message. Lenses never share a file, never edit source, and never run the build; they read the baseline file. Agents that need to run the app (performance, accessibility) do it without taking window focus, using `commands.screenshot` or a headless route, and report NOT VERIFIED when there is none.

Each brief contains (orchestration.md section 3): the app and path, `studio.yaml` facts, the lens question, the scope, the baseline file path, the prior audit's findings for that lens (to mark Fixed, Persists, New), and this finding format, required for every finding:

```
ID: <LENS>-NN (security: SEC-NNN)   Title:
Severity: CRITICAL | HIGH | MEDIUM | LOW (standards/severity.md)
Confidence: VERIFIED (ran it, measured it, or reproduced it) | STATIC (read the code) 
Evidence: <file:line, command and output, or measurement>; never paste secrets, cite the location only
Impact: <who or what is harmed, how, and how likely>
Effort: S | M | L | XL (and the area of code it touches)
Fix: <one or two sentences>   Type: <change type from the vocabulary>
```

Also required in each lens file: a Coverage section (what was examined with counts and denominators, what was not and why), a Healthy section (things done well, with evidence), and a lens result of `FINDINGS`, `NO FINDINGS IN <N> items examined`, or `NOT ASSESSED - <why>`. "No findings" from nothing examined is NOT ASSESSED.

IDs: lens IDs (`ARCH-01`, `QUAL-01`, `TEST-01` and so on) are local to this audit. Security findings use the studio scheme `SEC-NNN`, numbered from one above the highest SEC number in any report under `docs/security/audits/` or earlier audits (never reused, never renumbered; a finding that persists keeps its number).

Output paths: `docs/qa/audit/<date>/<agent>.md`. The code-quality lens produces two kinds of file (`code-reviewer.md` and one per language specialist). `code-reviewer` has no Write tool: it returns its findings in the format above and the main session writes `code-reviewer.md` from the reply verbatim.

Lens-specific briefing points:
- Architecture: does the code match the documented architecture, module boundaries, coupling hot spots, layering violations, single points of failure, unclear ownership, budget fit, upgrade paths.
- Code quality: correctness bugs, error handling, resource leaks, concurrency, dead code, duplication, language idioms, fragile areas (large files with high churn from git history).
- Security: verify exposure before rating network-facing findings (public DNS, bind addresses, tunnel or proxy scope, firewall; the infra record if `infra_record` is set); an exposure that cannot be checked is stated as unverified and the finding is capped at HIGH and labeled so. Then authentication, authorization, input handling, secrets in the repo or history, crypto use, platform specifics (web headers and CSP, desktop IPC and update integrity, mobile storage and permissions and transport, backend injection and tenancy, CLI argument and path handling), dependency advisories.
- Tests and CI: coverage by risk (not by percent), tests that cannot fail, flakiness evidence, CI presence, build reproducibility, version stamping, signing in CI, time to feedback.
- Operations: observability, alerting, backups and restore proof, rollback, runbooks, secrets handling, single points of failure.

Check: every spawned lens's file exists with real content and a lens result. A missing one gets one re-brief naming the gap; if it fails again it is a named BLOCKED gap in the report.

Decision point: show a one-screen summary per lens (counts by severity, lens result) and ask: proceed to verification, add a deeper pass on one lens, or drop findings in an area the user knows is out of scope.

## Phase 3: Verification

Findings are claims. This phase tries to break the highest-impact ones before they reach the report.

1. **Select** all CRITICAL, all HIGH (cap at 15, highest impact first, the rest stay unverified and labeled), any finding two lenses contradict, and at `full` every security or data-loss MEDIUM.
2. **Main session first pass:** for each selected finding, open the cited location yourself and check the claim literally (does the line exist, does it do that, is it reachable). A finding whose evidence does not exist is REFUTED at once.
3. **Independent verifiers:** spawn `code-reviewer` instances (read-only, Bash allowed, so they return verdicts and the main session writes the files) in one message, each given about eight findings, none of which came from `code-reviewer` itself. Findings from the code-quality lens are verified by `principal-engineer`. The brief states the claim and evidence only, not the finder's confidence, and the instruction: "Your job is to find why this is wrong: dead code, already mitigated elsewhere, test-only path, misread configuration, wrong severity. Try to reproduce it. Report CONFIRMED, CONFIRMED WITH CHANGES (new severity and why), REFUTED (why), or UNVERIFIABLE (what you could not check)." The main session writes each reply, unedited, to `docs/qa/audit/<date>/verify-<n>.md`.
4. **Apply:** REFUTED findings leave the headline and go to an appendix with the reason. CONFIRMED WITH CHANGES takes the new severity. UNVERIFIABLE findings stay, labeled `UNVERIFIED`, and cannot by themselves set a CRITICAL or HIGH verdict. If the main session and a verifier disagree, show both to the user.
5. **Announce at once** any confirmed CRITICAL (a secret in the repo, a data-loss path, an auth bypass) in plain text before the report is written; do not make the user wait.

Check: a verification file exists for every selected finding that was not refuted in step 2, and the report will state "N findings verified of M total (K CRITICAL/HIGH)".

## Phase 4: Synthesis

The main session merges (it is the only reader of every lens). Write `docs/qa/audit/<date>/report.md`:

- Merge duplicates by root cause, keeping every lens ID. A cause found by two independent lenses gains confidence, not severity.
- Every finding that is recorded gets its studio ID at Phase 5 and the audit finding ID is kept as the trace.
- **Priority** is set from the verified severity and impact, then adjusted by effort: P0 = confirmed CRITICAL, or HIGH with data loss or an exploitable path; P1 = other HIGH; P2 = MEDIUM; P3 = LOW. A finding with effort S and severity MEDIUM or higher is marked QUICK WIN and listed first within its priority. Effort orders work; it never lowers a priority.
- Cross-cutting themes (for example "error handling is absent in three modules"), and what is healthy, with evidence.
- Compare with the prior audit if one exists: Fixed, Persists, New.

Report layout (fixed so a later audit can diff it):

```
# Audit: <app> <date>
Scope | Rigor | Lenses run (N of M relevant) | Not spawned (why) | NOT ASSESSED areas (why)
Baseline: <build, test, lint results with denominators>
Headline: <verdict word and three sentences>
Findings table: ID | Title | Sev | Effort | Impact | Priority | Lenses | Verification
Top findings: P0 and P1, each with evidence, impact, fix, effort
Themes | Healthy areas | Changes since last audit
Refuted findings (appendix) | UNVERIFIED findings | Coverage gaps
Proposed backlog: stories (one line each, type, estimate, traced finding IDs); tech-debt rows; risks; bugs
```

## Phase 5: Backlog (decision point)

Present the proposed backlog grouped as: stories for `app-plan`, tech-debt rows, risk-register entries (things that cannot be fixed now), bug records for S1 and S2 defects. Security vulnerabilities go to stories or bug records traced to their `SEC-NNN`, not into the debt register (`app-tech-debt` leaves them to `app-security-audit`). Ask once for the whole set which to record. After the yes:

- Append the chosen rows to `planning/tech-debt.md` in the ten-column format and ID rule of `app-tech-debt` (read its "The register" section first): `TD-` plus three digits, one above the highest ever used, never reused or renumbered, Source `audit docs/qa/audit/<date>/report.md`. Append risks to `planning/risks.md` as `RISK-NNNN` (template `risk-entry.md`) and write bug records under `docs/qa/bugs/` as `BUG-NNNN-<slug>.md` (template `bug-report.md`). Re-read each file and confirm the row count matches what was approved and no ID repeats.
- Do not write stories here. Run `/app-plan` (not user-typed) for the chosen story list, passing the finding IDs so acceptance criteria trace to evidence; it assigns story IDs and statuses. If the user prefers to run it later, hand them the list in `.studio/drafts/team-audit-stories.md`.
- Update `.studio/state.md` (orchestration.md section 9).

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Default lenses | security, code quality, tests and CI, dependencies, plus any the user names; the rest are announced as not spawned | every relevant lens | every relevant lens, including optional data and localization |
| Verification | all CRITICAL and the top 5 HIGH | all CRITICAL and HIGH (cap 15) | plus security and data-loss MEDIUM |
| Backlog | tech-debt rows and a story list | plus risks and bug records | plus effort ranges and sequencing advice from `program-director` |

Rigor changes how many lenses and how many findings are verified, never what a verdict requires. Phases that may be skipped at minimal: lenses outside the minimal set, Phase 5 beyond tech-debt rows. Phases that never skip: baseline, verification of every CRITICAL, the report with denominators.

No director gate runs in this skill at any review mode; print `Gates: none run (this skill has no gates)`. `--review` only affects whether `program-director` sequences the backlog (full).

## Verdicts

First match wins:

1. `BLOCKED` - no readable source in scope, or the user declined `app-adopt` for an unmapped app.
2. `CRITICAL FINDINGS` - at least one CRITICAL finding is CONFIRMED.
3. `SIGNIFICANT FINDINGS` - no confirmed CRITICAL, at least one confirmed HIGH.
4. `MINOR FINDINGS` - no confirmed CRITICAL or HIGH; MEDIUM and LOW findings remain. Any lens that was NOT ASSESSED is named in the verdict line (`MINOR FINDINGS, with gaps: <lenses>`); a finding keeps its own word even when something else was not assessed.
5. `NOT ASSESSED` - no finding of any rank survived, but a relevant lens returned nothing, the baseline could not run, a lens needing measurement was static-only, or too little was examined for "no findings" to mean anything. Name each reason.
6. `HEALTHY` - every relevant lens ran with real coverage and nothing above LOW survived verification. Rare; state the coverage.

## Report

After the file is written, print in the conversation: the headline, the verdict, the findings count table by severity and verification state, the top five P0/P1 findings in one line each, the lens coverage line (`Lenses: 8 run of 10 relevant; 2 not spawned (reason)`), and the backlog decision. Then the closing block from orchestration.md section 8.

## Rules for this skill

- Read-only on source, config and build files. Agents write only their named audit file.
- Never report a secret's value; cite its location and recommend rotation.
- Never assert what no lens checked; a lens that could not examine something says NOT ASSESSED.
- Never let a finder verify its own finding.
- Never write stories, edit the register, or fix anything without the Phase 5 yes.
- Findings carry evidence or they are not findings. STATIC claims are labeled STATIC.
