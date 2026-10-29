<!--
Template: incident-postmortem. Written by: site-reliability-engineer with escalation-engineer and release-manager. Skill: /app-incident (the response and the blameless postmortem).
Lives at: docs/ops/incidents/<date>-<slug>.md (override: paths.incidents).
Rigor: minimal = severity, timeline, root cause, actions. standard = adds user-perspective impact, why it was not caught, contributing factors, went well and badly. full = adds where we got lucky, detection and response metrics, comms record, and action follow-up dates.
Blameless: describe systems, decisions and information available at the time, never individuals' fault. Delete this comment when the document is created.
-->

# Incident: [short description]

> **Date**: [YYYY-MM-DD]   **Duration**: [start to resolution, with time zone]
> **Severity**: [S1 | S2 | S3 | S4]   **Status**: [ONGOING | MITIGATED | RESOLVED]
> **Incident lead**: [role/agent]   **Authors**: [...]
> **Related**: [bug IDs, release version, runbook]

## Summary

[Three sentences: what broke, who it affected, how it was fixed.]

## Impact (from the user's perspective)

- What users experienced: [exact symptoms]
- Who and how many: [platforms, versions, regions, plan; number or percentage with the method of counting]
- Data: [lost / corrupted / exposed / none, and how we know]
- Duration of impact per group: [...]
- Support contacts, store reviews, revenue or trust effects: [...]

## Timeline

All times in [UTC]. Include detection, decisions and the reasoning at the time.

| Time | Event | Source |
|---|---|---|
| [hh:mm] | [change deployed / released] | [log, commit] |
| [hh:mm] | [first user impact] | |
| [hh:mm] | [detected, by what: alert, user report, engineer] | |
| [hh:mm] | [mitigation attempted and result] | |
| [hh:mm] | [resolved] | |

Detection delay: [n min]   Time to mitigate: [n min]   Time to resolve: [n min]

## Root cause

[The technical chain of cause and effect, down to the code, config, process or assumption. Distinguish the trigger from the underlying condition. Evidence: file:line, log excerpts, commit.]

## Why it was not caught

| Layer | Why it did not catch this |
|---|---|
| Design and review | |
| Tests (what test was missing, and why) | |
| Staging and canary | |
| Monitoring and alerts | |
| Release process | |

## Contributing factors

- [Factors that made it more likely or worse: missing runbook, confusing config, unclear ownership, time pressure, platform quirk.]

## What went well

- [...]

## What went poorly

- [...]

## Where we got lucky

- [Things that could have made it worse but did not.]

## Action items

| # | Action | Type (prevent / detect / mitigate / process) | Owner | Due | Tracked as |
|---|---|---|---|---|---|
| 1 | [specific, verifiable change] | | [one owner] | [YYYY-MM-DD] | [story / TD-NNN / RISK-NNNN] |

Every action has one owner and a date. Prefer actions that make the failure impossible or loud over ones that ask people to be careful.

## Communications

| When | Audience | Channel | Message (summary) | Approved by |
|---|---|---|---|---|

Drafts only; the user sends external communications.

## Lessons

[What the studio, the process or the code should do differently. Feed into `/app-retro`.]
