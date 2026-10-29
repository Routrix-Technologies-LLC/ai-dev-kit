<!--
Template: sprint-plan. Written by: program-director with product-manager. Skill: /app-sprint (plan mode); status mode updates the sprint Status line and Status history only.
Lives at: planning/sprints/<id>.md (override: paths.sprints). Use the kanban variant at the bottom when the app works in a continuous flow.
Rigor: minimal = goal and story table. standard = adds capacity with buffer, risks, carryover. full = adds milestone link, dependency map, mid-sprint checkpoints, honest status history.
Delete this comment when the plan is created.
-->

# Sprint [ID]: [name or theme]

> **Dates**: [YYYY-MM-DD to YYYY-MM-DD]
> **Status**: [Planned | ON TRACK | AT RISK | OFF TRACK | NOT ASSESSED | Closed]
> **Milestone**: [name or none]
> **Last status update**: [YYYY-MM-DD]

## Goals

1. [The one thing this sprint exists to deliver, stated as an outcome]
2. [Secondary goal]
3. [Stretch goal, clearly labeled stretch]

If the sprint delivers only goal 1 it is a success. Say so explicitly.

## Capacity

| Item | Value |
|---|---|
| Working days | [n] |
| People or agent-sessions available | [n] |
| Gross capacity (points, hours or S/M/L units) | [n] |
| Less: holidays, absences, known interruptions | [n] |
| Less: 20 percent buffer for bugs, reviews and surprises | [20 percent of the net] |
| **Plannable capacity** | [n] |
| Planned load | [n] |

Planned load must not exceed plannable capacity. If it does, cut scope before the sprint starts, not during.
Reference sizes: S = under half a day, M = about one to two days, L = three days or more (split anything larger).

## Stories

| Story | Title | Owner agent | Estimate | Depends on |
|---|---|---|---|---|
| [`story-001`](../epics/[epic]/story-001-[slug].md) | [title] | [agent] | [S/M/L] | [none or IDs] |

This table is the commitment, not the status: each story's status lives only in its story file, and `/app-sprint` status mode reads it from there. Only stories whose status is Ready enter a sprint. Order by dependency, then by risk (unknowns early).

## Must have, should have, nice to have

| Tier | Stories | Why this tier |
|---|---|---|
| Must | [IDs] | [the goal fails without them] |
| Should | [IDs] | [...] |
| Nice | [IDs] | [dropped first] |

## Carryover from the last sprint

| Story | Reason it did not finish | New estimate |
|---|---|---|

## Risks

| Risk | Probability | Impact | Mitigation | Owner | Register ID |
|---|---|---|---|---|---|

## Definition of done for the sprint

- [ ] Every Must story is Complete through /app-story-done
- [ ] Tests, lint and build pass on every target platform
- [ ] No open S1 or S2 bugs introduced
- [ ] Docs and CHANGELOG draft updated
- [ ] Retrospective scheduled (`/app-retro`)

## Status history

Honest, dated lines. Never edit an old line; add a new one.

| Date | Status | Done / total | Note |
|---|---|---|---|

---

## Kanban variant (replace the sections above when working in flow)

**Cadence**: [continuous; review every n days]
**WIP limits**: Ready [n], In Progress [n], In Review [n]

| Column | Stories (ordered, top is next) |
|---|---|
| Ready | |
| In Progress | |
| In Review (awaiting /app-story-done) | |
| Complete (last 14 days) | |
| Blocked | [story: blocker, owner] |

**Pull rule**: take the top Ready story only when In Progress is under its limit. A blocked story leaves the column and gets a named owner for the unblock.
**Metrics**: throughput per week [n], median cycle time [n days], oldest In Progress item [story, age].
