---
name: app-scope
description: "Check planned work against capacity and the product brief: estimate it with ranges and confidence, find scope creep, and propose cuts ordered by distance from the product pillars. Use when the user asks if a plan is realistic, whether there is scope creep, how long something will take, what to cut, or before committing a sprint, milestone or release scope."
argument-hint: "[app] [sprint <id> | milestone <name> | epic <name> | feature <name> | estimate <task>] [--review solo|lean|full]"
user-invocable: true
---

# App Scope

Compares what is planned with what the team can deliver and with what the product is for. It produces an honest estimate (ranges, never single numbers), measures drift from the baseline plan, and proposes cuts ordered by pillar proximity: work furthest from the pillars goes first, work that defines the product goes last. It reports and recommends; it does not edit plans or stories.

Writes: a report, shown in the session and, after one ask, saved to `planning/scope-checks/<date>-<scope>.md` (the `layout.md` path for scope checks; saved only with the user's yes).
Next: `/app-sprint` (re-plan), `/app-plan` (resize stories), `/app-prototype` (to resolve a Low confidence), `/app-brief` (if the pillars themselves are unclear).

## When to use and when not to

- Use before committing a sprint or milestone, when scope seems to grow, or to size a task or feature.
- Reporting progress on a running sprint is `/app-sprint` status. Judging whether a feature spec is complete is `/app-spec-review`. Deciding the product's identity is `/app-brief`.

## Inputs

- Required: `studio.yaml`, and the baseline plan for the argument: the epic and stories (`planning/epics/`), the sprint plan (`planning/sprints/<id>.md`), the spec (`docs/product/specs/`), or for `estimate` the task description.
- Needed for the brief comparison: `docs/product/brief.md` (minimal) or `docs/product/vision.md` with pillars (standard, full). Missing: the proximity ranking is NOT ASSESSED; offer `/app-brief`, and still report the numeric comparison.
- Needed for capacity: team size and availability for the period, and past throughput (completed stories per period from `planning/sprints/` and story files). None found: say "no history; estimates are not calibrated to this team" and ask the user for capacity. Never invent a velocity.
- Baseline that exists but lists no items, or a current state that cannot be read, is handled in Phase 5, not by computing a percentage.

## Phase 1: Resolve and announce

Per `orchestration.md` sections 1 and 2. Agents: `program-director` (capacity, sequencing, risk, owns PG-SCOPE), `product-director` (pillar judgment and cuts affecting identity). Add `principal-engineer` for estimate accuracy when more than a few stories are touched, and `qa-lead` when test effort is large or evidence types are heavy (migrations, device matrices). The platform lead for the affected platforms reviews feasibility only when a single item looks over 10 working days.

Check: announce block printed.

## Phase 2: Establish the baseline

Main session, by reading.

1. Locate the baseline for the argument (table below). If it does not exist, report the missing file and stop; do not guess a baseline.

| Argument | Baseline | Current state |
|---|---|---|
| `sprint <id>` | the sprint plan's committed stories | story files' status and Files lists, git log since the sprint start |
| `milestone <name>` or `epic <name>` | epic file and the stories created from it at that date (git history of the epic shows the original list) | stories now in the epic, their status |
| `feature <name>` | the spec's requirement IDs and acceptance criteria | stories linked to those IDs, code and commits touching the feature |
| `estimate <task>` | none; this mode estimates only | the code and plans around the task |

2. Enumerate baseline items as a numbered list with ids (story numbers, requirement IDs). Count them. This count is the denominator for every percentage.
3. Enumerate current items the same way, marking each as: in baseline, added after baseline, removed from baseline, or split from a baseline item. Find additions with `git log` on the plan files and by comparing the story list to the baseline. TODO and FIXME markers that signal unplanned work are listed with file and line.
4. For each addition, find its source (a commit, a person, a request, a discovered requirement) and whether the baseline was formally changed (a plan edit, a decision-log entry) or the work simply appeared.

Check: both lists exist with counts, each addition has a source or "source unknown".

## Phase 3: Estimate

For every item not done (a story whose status is anything but Complete; In Review counts as open work, estimated as the review and fix remainder), produce an estimate in working days as three numbers.

1. **Measure before guessing.** For the files each story lists, count with Grep: non-blank lines and branch-keyword lines, labelled as approximations of size and complexity, not measurements of either. Count dependents (files referencing the file). Count tests present in the area. Name any file that could not be counted.
2. **Complexity factors:** systems and layers touched, new code versus change to existing, integration points and external services, data or migration work (`/app-data-migration`), contract changes (`/app-api`), UI states and platforms to verify (each target platform multiplies verification), accessibility and localization work, security-sensitive paths, unfamiliar technology, unclear requirements, dependence on unfinished work.
3. **Ranges:** optimistic (nothing surprising), expected (normal friction, one review round), pessimistic (one significant unknown surfaces). Budget the expected, round to half days. Items over 10 days are split before they are accepted into a sprint.
4. **Confidence** per item: High (pattern exists, requirements settled, history to compare), Medium, Low (approach undecided, requirements open, new technology). Low confidence is the signal to recommend a time-boxed spike (`/app-prototype`) before committing; a range built on an undecided approach is a guess.
5. For multi-story scope, `principal-engineer` reviews the estimates for the five biggest items (spawn once with the measurements and the story files; output `~/AgentScratch/app-scope/<run>/principal-engineer.md`). Disagreements are shown, not averaged.

Estimate mode ends here with the estimate table, the biggest risk, and the next-step advice; it still ends with the closing block and a verdict (REALISTIC applies only against a stated capacity, otherwise NOT ASSESSED for the fit question and the estimate is reported as such).

Check: every open item has three numbers and a confidence, and the measurement counts are present or named as unavailable.

## Phase 4: Capacity and fit

Spawn `program-director` with the estimate table, capacity figures and the dependency order (brief per `orchestration.md` section 3; output `~/AgentScratch/app-scope/<run>/program-director.md`). It returns:

- Capacity for the period: people times available days, minus fixed overhead (reviews, releases, meetings, on-call), stated as a formula with the inputs. Past throughput as a cross-check, with the sample size.
- Sum of expected and pessimistic estimates against capacity, as ratios (for example "expected 38 of 30 days, 127%").
- The critical path, the items that block others, and the risks (external dependencies, review or store lag, single-person knowledge).
- Whether the plan holds if the pessimistic estimate lands on the two largest items.

Check: capacity inputs are stated with their source (the user, history, or "assumed, confirm"). An assumed capacity is confirmed with the user before the verdict (AskUserQuestion), never adopted silently.

## Phase 5: Creep measurement

1. Compute the numbers only if both sides are readable: items in baseline (N), items added (+N, percent of baseline), items removed, net change. Show the denominator in every percentage.
2. **Not computable.** If the baseline file exists but enumerates no items, or the current state cannot be read (no stories, no commits, no linked work), or the denominator is zero for any reason, do not print counts or percentages. Print `Baseline unusable` or `Current state unreadable` with the reason. A rendered "0 added, 0%" next to a missing baseline reads as on track and is false.
3. Classify each addition: discovered requirement (necessary), requested change (needs a decision), gold-plating (unrequested polish), refactor or debt (listed in `planning/tech-debt.md`?), or unclear. An addition not accounted for by a cut or a schedule change is creep.

## Phase 6: Propose cuts by pillar proximity

Needs the pillars. Spawn `product-director` with the pillars, the target users and the item list (each with its estimate and, for additions, its source). Output `~/AgentScratch/app-scope/<run>/product-director.md`: for every item, a pillar-proximity grade and a one-line reason.

| Grade | Meaning | Cut order |
|---|---|---|
| Core | Defines the product or is required for a pillar to work | Never first; cut last, and only with the user's explicit word |
| Supporting | Makes a pillar work better or removes friction on the core path | Defer before cutting |
| Adjacent | Useful but a user would still recognize the product without it | Cut or defer early |
| Distant | Does not serve a pillar or the target user | Cut first |

Combine with cost: within a grade, cut the highest expected days first (best cut ratio). Dependencies override: never propose cutting an item something kept depends on without listing the dependent.

The cut list is built to bring expected scope within capacity, stated as "cuts A, B, C free N days; expected load becomes X of Y (Z%)". Always also give the alternative levers: extend the period, add capacity, reduce quality bars (named, never silently), or split the scope across releases. Quality bars (tests, accessibility, security) are not offered as a default cut; if the user asks, name what risk it takes on.

If the brief or vision has no pillars, grades are NOT ASSESSED; use cost and dependency order only and say proximity was not available.

Decision point: present the analysis and cut proposals, then ask which path to take (AskUserQuestion: apply cuts, extend, re-baseline, or keep and accept the risk; `(Recommended)` on one). Cuts touching Core items go to `product-director` for a decision before they are even proposed as options. The skill does not edit plans.

## Phase 7: Gate and report

`PG-SCOPE` (owner `program-director`) is this skill's own single-purpose gate, so it runs in `lean` and `full` and is skipped in `solo` (`gates/README.md`). Spawn it with the planned scope and estimates, the capacity inputs with their source, the creep numbers, the brief or vision path, the cut proposal and `planning/risks.md` if it exists; it reads its own gate file and answers REALISTIC, OPTIMISTIC, UNREALISTIC or NOT ASSESSED. Combine it with the skill's own verdict by the ranking in `gates/README.md` (the stricter of the two stands; the gate never raises the verdict). Where the scope document is saved, record the gate directly under its title as `> **Program Director review (PG-SCOPE)**: <VERDICT> <date>`; a skipped gate prints `PG-SCOPE skipped: solo mode`. Present the report, then ask once whether to save it to `planning/scope-checks/<date>-<scope>.md`. Overwrite the checkpoint.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Estimates | per story, ranges | plus Grep measurements and confidence | plus `principal-engineer` review and pessimistic fit |
| Pillar proximity | against the brief's one-line purpose | against vision pillars | plus `product-director` grading every item |
| Baseline | the brief's build order if no sprint plan | the sprint, epic or spec | plus history of plan edits |

| Review mode | Gates |
|---|---|
| solo | `PG-SCOPE skipped: solo mode` |
| lean | PG-SCOPE runs (the own gate of a single-purpose review skill, always-on in lean) |
| full | PG-SCOPE runs |

## Verdicts

First match wins. Ratios use the expected estimate against stated capacity, unless noted.

1. `UNREALISTIC`: expected load is over 125% of capacity, or the pessimistic load is over 150%, or net creep over 50% of baseline items with no cuts or extension accounted for, or a critical path item has no feasible owner.
2. `OPTIMISTIC`: expected load is over 100% up to 125% of capacity, or the plan fits only if nothing goes wrong (expected within capacity but pessimistic over 125%), or net creep is over 10% up to 50% unaccounted for, or more than a third of the load (by days) is Low confidence.
3. `NOT ASSESSED`: capacity could not be established or confirmed, the baseline is empty or missing, the current state is unreadable, history is absent and the user gave no capacity, or an estimate could not be produced for items carrying more than a quarter of the load. State which, and what input would settle it. (Not ranked as a pass: nothing was compared.)
4. `REALISTIC`: expected load within 100% of confirmed capacity, pessimistic within 125%, creep 10% or less or fully accounted for, and no more than a third of the load Low confidence.

If the pillar grading was NOT ASSESSED but the numeric verdict is otherwise REALISTIC, the verdict is REALISTIC and the report states that cut order lacked pillar proximity. The gate and this verdict combine as described in Phase 7.

## Report

```
Scope: <argument>   Baseline: <path>   Current: <source>
Baseline items: <N>   Added: <N> (<X>% of <N>)   Removed: <N>   Net: <+/-N> (<X>%)   [or: Baseline unusable / Current state unreadable: reason]
Load: expected <X> d, pessimistic <Y> d vs capacity <Z> d (<source of capacity>) = <A>% / <B>%
Confidence: High <N>, Medium <N>, Low <N> (Low = <C>% of load)
Critical path: <items>   Biggest risk: <one line>
Additions: <item: source, class, accounted for yes/no> ...
Proposed cuts (by pillar proximity): <item: grade, days> ... frees <N> d, load becomes <X>%
Alternatives: <extend, add capacity, split release>
Skipped: <agent or step and why>
Decisions for the user: <labelled options>
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Always ranges, never a single number; budget the expected, not the optimistic.
- Never invent capacity or velocity; absent history is stated and the user is asked.
- Never print a percentage whose denominator is zero or unread.
- Never cut Core items by default, never cut quality bars silently, and never propose a cut without its dependents.
- Never edit plans, stories or specs; recommend `/app-sprint` or `/app-plan`.
- Additions are not bad by themselves; they are creep when nothing accounts for them. Say which.
- Guesses are labelled assumptions; every number has a stated source.
