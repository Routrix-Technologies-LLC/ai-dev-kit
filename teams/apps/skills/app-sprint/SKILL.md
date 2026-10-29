---
name: app-sprint
description: "Plans a sprint or a kanban batch from Ready stories against real capacity, or reports honestly how the current sprint or flow is going and surfaces risk early. Use when the user wants to plan the next sprint, pick what to work on next, set up kanban order for solo work, replan mid-sprint, or asks how the sprint is going."
argument-hint: "[app] [plan | status | update] [sprint-id | kanban] [--review solo|lean|full]"
user-invocable: true
---

# App Sprint

Two modes. `plan` commits a set of Ready stories to a sprint (time-boxed) or to a kanban queue (no sprints, ordered, with a work-in-progress limit), checked against real capacity. `status` reads the stories and reports how it is going, and it is built to tell the truth early: it can say AT RISK on day three.

Writes: `planning/sprints/<id>.md` (template `sprint-plan.md`), in plan and update mode only. Status mode writes nothing.
Next: plan mode, `/app-story-ready sprint`, then `/app-dev-story`; status mode, one recommended action; at the end of a sprint, `/app-retro`.

## When to use and when not to

- Use after `/app-plan` has produced Ready stories, at a sprint boundary, mid-sprint to replan, or any time for status.
- Not for creating stories (`/app-plan`), checking whether the plan is too big for the product (`/app-scope`), or a retrospective (`/app-retro`).
- Kanban is the right shape for one person or a very small team: no sprint dates, no capacity maths, a ranked queue, a WIP limit, and health judged by age and flow.

## Inputs

Resolve the app per orchestration.md section 1 and announce per section 2. Mode comes from the argument; with none, ask (plan, status, update). Shape comes from the argument (`kanban` or a sprint id), else from what exists: `planning/sprints/kanban.md` means kanban, sprint files mean sprints, neither means ask which shape, once, and note the answer in the checkpoint (the file itself is written in Phase 6, after the user's yes).

| Input | Used for | If missing |
|---|---|---|
| `planning/epics/*/story-*.md` (header: Status, Change type, Estimate, Rank, Last updated; Dependencies section) | the backlog and, in status, the truth about progress | Plan: stop, offer `/app-plan`. Status: NOT ASSESSED. |
| Previous `planning/sprints/*.md` | velocity, carryover | Absent on a first sprint: say so, velocity is NOT ASSESSED, plan on the user's stated capacity. |
| `planning/risks.md` | sprint risks | Say "no risk register" once and assess from the contents only. |
| `planning/tech-debt.md` | scheduled debt items (`TD-NNN` with a story) | Optional. |
| `docs/qa/test-plans/<scope>.md` | QA readiness | Absent is a warning with the offer `/app-qa-plan`, not a stop. |
| `studio.yaml` | platforms, rigor, review mode | Required. |

Story status lives in the story files only. Sprint files hold commitments, never copies of status, so the two cannot drift (`orchestration.md` section 3). Story statuses are Draft, Ready, In Progress, In Review, Complete, Blocked; only `/app-story-done` produces Complete, and this skill never sets any status.

## Plan mode

### Phase 1: Gather (main session)

List every story with Status, Change type, Estimate, Rank and dependencies. Partition: Ready (plannable), Blocked, Draft, In Progress or In Review (already in flight), Complete. Find the previous sprint (highest id) and its carryover: every story in it that is not Complete goes in the Carryover table with a reason and a new estimate, and appears nowhere else. Read open TD items marked for scheduling. Print the partition counts with the denominator. Zero Ready stories and nothing in flight is BLOCKED with the route `/app-plan` (new stories) or `/app-story-ready` (check the Drafts; it marks the READY ones Ready after the user's yes).

### Phase 2: Capacity (decision point, never assumed)

Sprint shape: ask for the start and end dates, who is working and the real available days (leave, other duties, support load). Propose a buffer of 20 percent for unplanned work and bug fixes and let the user change it. Capacity is the user's number; do not guess it from calendar length. If the user cannot say, record capacity as `NOT ASSESSED` and the sprint plan cannot reach a clean pass at the gate.

Estimate weights for the maths: S is 1, M is 3, L is 5. If previous sprints exist, compare the sum of Complete weights to its capacity to suggest a points-per-day rate, and label it as a suggestion drawn from N sprints. With no history there is no rate: ask the user to commit a number of stories or days.

Kanban shape: no dates or capacity. Ask for the WIP limit (a recommended default for one person is 2, for a team the number of people plus one) and an optional review cadence. An unset WIP limit is recorded as `none set`, and status will say so.

### Phase 3: Draft the plan (sequence)

Agent: `program-director` drafts, `product-manager` validates the goal and the priority order against the brief and the specs. Brief per orchestration.md section 3: the partition, capacity, carryover, dependencies, risks, TD items, the rigor. Outputs: `.studio/drafts/sprint-<id>-plan.md` (program-director), `.studio/drafts/sprint-<id>-priority.md` (product-manager, spawned after, in sequence, with the draft). Selection rules:

- Only `Ready` stories are committed. A Blocked or Draft story is listed under Not committed with its blocker, never silently included.
- Respect dependencies: a story is not committed unless everything it depends on is Complete, in the sprint ahead of it, or in flight.
- Order by dependency first, then Rank, then value. Group into **Must** (the sprint goal fails without it), **Should**, **Could**. Total Must weight must fit inside available capacity after the buffer; Should and Could may exceed it only as stretch, labelled as such.
- A planned-whole backlog smaller than capacity is planned whole; never pad with invented work.
- Debt: include scheduled TD stories as ordinary stories; a sprint with zero debt for three sprints running is flagged in the risks.
- Kanban: no tiers. Output an ordered queue (top is next), the WIP limit, and which stories are in flight now.

**Goal prerequisites.** State the goal in one sentence (from the brief or specs, validated by `product-manager`). List what must exist to demonstrate it: a runnable build on each target in scope, environments, accounts or test data, third-party sandbox access, an API or stub, assets, a signed build for device testing. Each need is `exists`, `built by <story>` or **missing**. Missing items are copied into Risks and reported with three options (pull in the story that builds it, write one with `/app-plan`, or reword the goal). Report the gap; do not solve it by widening a story.

### Phase 4: QA readiness

Check for a test plan covering the sprint's stories in `docs/qa/test-plans/`. Found: link it. Not found: say so plainly, add the line `No QA plan: run /app-qa-plan before the last story is built` to the plan's Risks, and recommend `/app-qa-plan sprint`. Ask only once, in the Phase 6 decision.

### Phase 5: Gate

`PG-PLAN` (owner `program-director`), per orchestration.md section 7: full only (`gates/README.md` lists it nowhere in the always-on set); solo and lean print `PG-PLAN skipped: <mode> mode` and the plan header says `PG-PLAN: skipped (<mode> mode)`, so a reduced run is never mistaken for a reviewed one. Pass: the goal, committed stories with weights, capacity and buffer, carryover, dependency order, missing prerequisites, risks. Results: a blocking verdict sends the user back to revise the scope; CONCERNS go to the user in Phase 6; NOT ASSESSED (for example capacity unknown) is shown in the plan header as `PG-PLAN: NOT ASSESSED - <missing input>` and never read as a pass.

### Phase 6: Decide and write

Present the plan: goal, prerequisites, capacity maths, committed stories by tier with weights, Not committed list, carryover, risks, gate result. The decision is the user's: commit as drafted, move stories between tiers or out, or change capacity. Re-run the checks after any change. Then one ask naming the file: "Write `planning/sprints/<id>.md`?" Sprint ids are `sprint-NNN` (highest existing plus one, zero padded) or `kanban`. A skipped answer is not a yes.

On yes, write the file from `sprint-plan.md`, leaving out its Stories table `Status` column and, in the kanban variant, the In Progress, Implemented and Complete columns: those would be copies of story status (keep Ready queue and Blocked list with owners). Check: re-read it; it has the goal, capacity (or `none set` for kanban), a row for every committed story that points at a real story path, carryover and risks. Overwrite the checkpoint (section 9).

## Update mode (replan an active sprint)

Read the current sprint file and the stories' live Status. Ask what to change: add, remove, reorder or re-estimate. Allowed freely: Ready stories not yet started. Never removed or reordered silently: anything In Progress, In Review or Complete (those can only be descoped by the user's explicit decision, recorded with a reason in the sprint file's Changes section). Mid-sprint additions are recorded in Changes with the date and why; a sprint whose added weight exceeds 20 percent of its original committed weight is flagged as scope growth. Re-run Phases 3 to 6 on the revised plan.

## Status mode (read-only, honest)

Writes nothing, asks nothing except which sprint if ambiguous, and ends in one recommendation.

### Step 1: Find the sprint
The argument id, else the newest file in `planning/sprints/`. No sprint files and no `kanban.md`: if stories exist, report their flow counts only and say `no sprint plan: status of the plan is NOT ASSESSED`; if no stories either, `NOT ASSESSED - nothing to report on`, route to `/app-plan`.

### Step 2: Read the truth
For each committed story read its file's Status and Last Updated. `Complete` counts as done only when the story file says so; `In Review` is not done; "almost done" does not exist. For staleness use the story's Last Updated and, when git is available, the date of the latest commit touching the story's Files list; the later of the two is the last activity. Missing dates mean "never stamped", reported as such, never as fresh. A committed story file that is missing is reported by name.

### Step 3: Measure (sprint shape)
Days elapsed and remaining from the sprint dates (none: skip the burn comparison and say so). Completion percent is Complete weight over committed weight (S 1, M 3, L 5); time percent is elapsed over total days.

### Step 3b: Measure (kanban shape)
Count by Status; In Progress and In Review against the WIP limit (`none set` is reported as a risk in itself); age of each in-flight story (days since it moved to In Progress, from the earliest evidence available, else its Last updated); the median cycle time of Complete stories if at least three exist (else `NOT ASSESSED - fewer than 3 completed`); the lowest-Rank Ready story and whether it is being worked.

### Step 4: Risk flags (surface them early)
Evaluate every flag, every time, and list each that fires with its evidence:

| Flag | Fires when |
|---|---|
| Must blocked | any Must (or first in the queue, for kanban) story is Blocked |
| Late start | a Must story is Ready but not started and more than 40 percent of the time is gone |
| Stale | an In Progress story has had no activity for 4 calendar days (weekends count; say so in the evidence) |
| Review pile-up | stories sit In Review for more than 2 days: finishing beats starting. Close them with `/app-story-done` |
| Big rock | an L story is not started after 40 percent of time, or not In Review by 70 percent |
| Dependency inversion | a story is In Progress while something it depends on is not Complete |
| Scope growth | weight added since the plan exceeds 20 percent of the original |
| No owner or estimate | a committed story has none |
| WIP over limit (kanban) | in-flight stories exceed the limit |
| Aging (kanban) | a story's age exceeds twice the median cycle time, or 7 days when there is no median |
| Missing prerequisite | a goal prerequisite recorded as missing in the plan is still missing |
| No QA plan | the plan recorded none and it still does not exist |

### Step 5: Verdict
First match wins. Dates, WIP limits and cycle times that do not exist are never invented.

1. OFF TRACK: completion is more than 25 points behind time; or a Must story is Blocked with under 40 percent of the time left; or the sprint end has passed with a Must story not Complete; (kanban) the first story in the queue is Blocked and nothing else of value can proceed, or aging plus WIP over limit both fire.
2. AT RISK: completion is 10 to 25 points behind time; or any risk flag fires.
3. NOT ASSESSED: the sprint file or the committed stories could not be read, no dates exist for a sprint, or more than a third of committed stories have no readable Status. Name what is missing.
4. ON TRACK: completion within 10 points of time or ahead, and no flag fired.

ON TRACK is unreachable while any flag fires: early risk is the point.

### Step 6: Output (under about 40 lines)

```
## Sprint <id> status: <date>   (or: Kanban status: <date>)
Goal: <goal>   Time: <elapsed>/<total> days (<t>%)   Done: <weight done>/<weight committed> (<c>%), <n> of <total> stories
Verdict: <ON TRACK | AT RISK | OFF TRACK | NOT ASSESSED> - <one line why>

| Story | Tier | Status | Owner | Last activity | Note |
|---|---|---|---|---|---|

Risk flags: <each flag that fired with its evidence, or "none fired of 12 checked">
Missing or unreadable: <items, or none>
Recommendation: <one concrete action, or "none needed">
```

If all Must stories are Complete, say so and name the next Should or Could (or the next Ready story). At the sprint end recommend `/app-retro`. Offer `/app-sprint update` when the verdict is AT RISK or OFF TRACK.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Shape | kanban recommended; no sprint file needed to start | sprint or kanban | sprint or kanban |
| Capacity maths | optional for kanban | required for sprints | required, with velocity from history |
| QA plan check | warning | warning | warning, and a missing plan is a `PG-PLAN` concern when that gate runs |
| Gate | none | `PG-PLAN` at full review mode only | `PG-PLAN` at full review mode only |

Review mode: `PG-PLAN` runs at full only; solo and lean skip it. Status mode runs `PG-MILESTONE` (owner `program-director`, read-only, answers inline) at full review mode only, and only when the sprint file names a milestone; solo and lean print `PG-MILESTONE skipped: <mode> mode`. A `PG-MILESTONE` verdict stricter than the Step 5 verdict raises it (OFF TRACK over AT RISK over ON TRACK); NOT ASSESSED keeps ON TRACK from standing. The status block is still printed in every mode and the skill writes nothing.

## Verdicts

- Plan mode: COMPLETE (file written and verified; `PG-PLAN` result shown). BLOCKED (no Ready stories, the user declined the write, or a blocking `PG-PLAN` verdict stands). A plan written with capacity or a gate NOT ASSESSED is COMPLETE with that stated on the verdict line.
- Status mode: ON TRACK, AT RISK, OFF TRACK, NOT ASSESSED, in the Step 5 order.

## Report

```
App: <name>   Mode: <plan|update|status>   Shape: <sprint|kanban>   Rigor: <r>   Review: <m>
<plan: committed N stories (weight W) against capacity C after buffer B; not committed: <n with reasons>; carryover: <n>>
<status: the Step 6 block>
Not spawned: <agent> (<why>)   Skipped: <step> (<why>)
Verdict: <WORD> - <one line why>
Gates: <PG-PLAN: VERDICT | PG-MILESTONE: VERDICT> | none run (<mode>)
Wrote: <path, or none>
Next: </app-story-ready sprint | /app-dev-story ... | /app-retro> (<why>)
```

## Rules for this skill

- Capacity and WIP limits are the user's numbers; never assume them and never derive them from calendar length alone.
- Commit only `Ready` stories; never include a Blocked or Draft story and never invent work to fill capacity.
- Never change a story file, its status or its order. Sprint files hold commitments, not status; do not copy story status into them.
- Status mode is read-only and honest: it counts only Complete as done, reports unread data as unread, and never reports ON TRACK while a risk flag fires.
- Every count carries its denominator.
- Recommend the next skill; never start it.
