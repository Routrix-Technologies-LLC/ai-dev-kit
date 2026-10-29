---
name: app-incident
description: "Run an incident on a live app and write the blameless postmortem: declare severity, keep a timeline, triage in parallel, rank mitigation options, draft (never send) status and user communications, confirm recovery with evidence, and turn the lessons into owned actions. Use when the user says incident, outage, production is down, users are affected, data was exposed, we need a postmortem, or write up what happened."
argument-hint: "[app] [declare | update | resolve | postmortem] [incident slug or description]"
user-invocable: true
---

# App Incident

Two jobs. While something is live and hurting users: keep a calm, honest record, parallelize the diagnosis, rank the ways to stop the damage, and draft the words. Afterwards: write the blameless postmortem so the same thing is harder to repeat. The user is the incident commander and the only one who acts on production or sends anything.

Writes: `docs/ops/incidents/<date>-<slug>.md` (template `incident-postmortem.md`). Agent parts in `.studio/drafts/incident-<slug>-<agent>.md` (local, gitignored).
Next: `/app-hotfix` (code fix on the released version), `/app-release` (rollback or redeploy through a release), `/app-observability` (detection gaps), `/app-retro` (process lessons), `/app-bugfix`, `/app-tech-debt`.

## When to use and when not to

- Use for any event where users or data were harmed or at real risk in a deployed or distributed app, and for a postmortem after one (including a bad release or hotfix).
- Not for an ordinary bug (`/app-bugfix`), a planning retrospective (`/app-retro`), or the code fix itself (`/app-hotfix`).
- Mode: `declare` starts a live incident (default when nothing exists for the slug); `update` appends facts and re-checks severity; `resolve` closes with evidence; `postmortem` writes the analysis (default when the incident is already over).

## Inputs

- `studio.yaml` (`platforms`, `hosting`, `infra_record`, `rules`); the architecture doc and `docs/ops/observability.md` and runbooks if they exist; the release records and tags; `standards/severity.md`.
- Whatever the user can paste or describe: alerts, logs, dashboards, support messages, store reviews. Facts you cannot see are asked for. A fact has a source (log line, commit, user-stated); an unsourced item is written `UNCONFIRMED`.
- Times are recorded in UTC with the zone stated; get the clock with `date -u` (POSIX shell) or `(Get-Date).ToUniversalTime()` (PowerShell). A time given by the user is marked user-stated.

## Phase 1: Declare

1. Follow `orchestration.md` section 1 and print the plan block (section 2). Gates: none are defined for this skill.
2. Ask what is known: what users see, since when, how it was noticed, who or how many are affected, what changed recently. Rate severity on `standards/severity.md` by user impact (S1 outage, data loss or exposure, security; S2 major degradation; S3 minor or workaround; S4 cosmetic), stating the reason. If data loss, exposure or a security compromise is possible, say at once that this may carry legal or contractual notification duties that need a human decision, and that the clock may already be running.
3. Create `docs/ops/incidents/<date>-<slug>.md` immediately from `incident-postmortem.md` with: severity, status ONGOING, detection time, the commander (the user), scribe (this session), and the first timeline rows. Read it back. Overwrite the checkpoint in `.studio/state.md`.

## Phase 2: Triage in parallel (read-only)

Spawn in one message, each told to change nothing in production and to write a short findings file:

| Agent | Question | Output |
|---|---|---|
| `site-reliability-engineer` | What do the signals show (errors, latency, saturation, crash rate, dependency health)? Is there a runbook? What is the blast radius and who is affected? | `.studio/drafts/incident-<slug>-site-reliability-engineer.md` |
| `escalation-engineer` | What are the ranked hypotheses for the cause, what evidence supports or refutes each, and the fastest way to test them? Is there a reproduction? | `.studio/drafts/incident-<slug>-escalation-engineer.md` |
| `release-manager` | What changed (deploys, tags, flags, config, dependencies, migrations, store rollouts) in the window before onset, and what rollback or fix-forward options exist per channel with their time and risk? | `.studio/drafts/incident-<slug>-release-manager.md` |

Brief per `orchestration.md` section 3 with the facts so far quoted, severity, and the return contract. Check each file exists; merge the findings into the record's timeline and hypotheses. Label an agent's inference `HYPOTHESIS` until a tool or the user confirms it; verify one claim the plan turns on.

## Phase 3: Mitigation options

Stop the damage before finding the cause. Present options ranked by speed to relief and by reversibility, each with its risk and who must do it:

- Rollback to the previous version, or halt a staged rollout.
- Turn a feature flag off, revert a config, block bad input, rate-limit, fail over, scale.
- Disable a dependency path or integration; serve a degraded mode.
- A status notice and workaround while a fix is built (`/app-hotfix`).

State the tradeoffs plainly; the user decides. This skill does not change production. Actions run by the user, or through `/app-release` and `/app-hotfix` with their own asks, are logged in the timeline when the user reports them. Never recommend an action that destroys data without saying so and getting an explicit yes. If compromise or exposure is suspected, advise preserving evidence first (copy logs and snapshots read-only before rolling back, redeploying or rotating anything) and rotating credentials as a user action, never by pasting secrets into the record.

## Phase 4: Communications (drafts only)

`release-manager` drafts, the main session reviews; nothing is sent. Draft for each audience the user names (internal team, users, store or support, partners), in `docs/ops/incidents/<date>-<slug>.md` under Communications, each with a placeholder for the time it is sent and its channel:

1. Acknowledgement: what users experience, that it is being worked, when the next update comes.
2. Updates: only what is confirmed; times in UTC and the user's local zone; the next update time.
3. Resolution: what was wrong in plain words, what users should do if anything, apology without excuses.

Rules for every draft: facts only; no speculation about cause or blame; no promise of compensation or a fix date (list those as decisions for the user); no personal data or internal hostnames; consistent with the status of the record. If personal data may be involved, `privacy-specialist` reviews the user-facing text and the notification question before the user sends anything. Mark each draft `DRAFT - not sent`.

## Phase 5: Update and resolve

On `update`: append timeline rows (source for each), refresh severity and hypotheses, redraft comms if facts changed. On `resolve`: confirm recovery from evidence, not from relief. Evidence is a signal back to baseline over a stated window, a successful reproduction attempt that now passes, and a smoke of the critical path; ask the user for dashboards or queries the repo cannot show. Status words:

- **ONGOING:** users are still affected, or recovery is unconfirmed.
- **MITIGATED:** user impact has stopped by a workaround, rollback or flag, but the root cause is not fixed or not verified fixed.
- **RESOLVED:** the cause is fixed and verified in production, signals are normal over the window, and any needed fix is shipped.

## Phase 6: Postmortem (blameless)

Blameless means asking how the system allowed a reasonable person to cause or miss this, not who. Write into the same file, from the template:

1. Impact: who, how many, how long, what data, quantified or marked `UNKNOWN`. Do not estimate without a stated method.
2. Timeline with sources: detection, acknowledgement, diagnosis, mitigation, recovery.
3. Root cause and contributing factors, each traced to evidence. Distinguish trigger (what set it off) from cause (why it was possible) and from missing safeguards (why it was not caught: tests, review, alerts, rollout, runbooks).
4. Detection and response: time to detect, time to mitigate, what slowed them, who knew what.
5. What went well, what went badly, where we got lucky.
6. Actions: each with an owner, a due date, a priority (P0 to P3), a type (prevent, detect, mitigate, process), and a place it is tracked (story, tech-debt row, runbook update). Prefer fewer, sharper actions. Actions that are stories are proposed for `/app-plan`; none are created silently.

Agent split (parallel, each writing its own part under `.studio/drafts/` as `incident-<slug>-<agent>-postmortem.md`): `escalation-engineer` the technical root cause and regression test proposal; `site-reliability-engineer` detection, response, runbooks and alerts; `release-manager` change and rollout factors and comms review. The main session merges the parts into the one record and checks that every timeline claim has a source, every action has an owner and date, and no sentence assigns blame to a person.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Record | severity, timeline, cause, one action list | plus comms drafts, detection analysis, tracked actions | plus review by the directors who own the affected areas (`technical-director` for cause and actions) |

No gates are defined for this skill; review mode does not change it. Rigor never relaxes sourcing or the rule that comms are drafts.

## Verdicts

First match wins.

1. **ONGOING:** impact continues, recovery is unconfirmed, or the user has not confirmed a status.
2. **MITIGATED:** impact stopped, root cause not fixed or not verified in production.
3. **RESOLVED:** cause fixed and verified, signals normal over the stated window, postmortem written (or scheduled with a date if the user chose to defer it).

Unknown facts stay `UNKNOWN` or `UNCONFIRMED` and never raise the status.

## Report

```
Incident: <app> <slug>  Severity: <S1-S4>  Mode: <declare|update|resolve|postmortem>
Impact: <who, how many, how long, or UNKNOWN>   Cause: <confirmed | HYPOTHESIS: ...>
Mitigation: <what the user did, when>   Recovery evidence: <signal and window, or none yet>
Comms: <n drafts, none sent>   Actions: <n, each with owner and date>
Verdict: <WORD> - <one line why>
Gates: none run (no gate defined for this skill)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Drafts comms only. Never send, post or publish anything; never change production. The user is the incident commander.
- Blameless: describe systems, decisions and conditions, never individuals' failings.
- Every timeline entry and root-cause statement has a source or is marked UNCONFIRMED or HYPOTHESIS. Impact numbers have a method or are UNKNOWN.
- Do not promise compensation, dates or outcomes in any draft; surface them as the user's decisions.
- A possible data exposure is flagged to the user at once as needing a human decision on notification; do not state legal conclusions.
- No credentials, tokens, personal data or internal hostnames in the record or the drafts.
- Recommend the next skill; never start it.
