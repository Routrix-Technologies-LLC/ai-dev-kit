---
name: app-retro
description: "Runs a retrospective for a sprint, a milestone, a release or an incident: what was planned versus what happened, why, what to keep or change, and a few actions with owners and dates. Use when a sprint or release ends, after an incident, at a milestone, or when the user asks what went well, what went wrong or how to improve the process."
argument-hint: "[app] [sprint <id> | milestone <name> | release <version> | incident <slug>] [--review solo|lean|full]"
user-invocable: true
---

# App Retro

A retrospective turns what happened into a few changes that actually get made. It is built from evidence (plans, story files, git history, bugs, release and incident records) and from the people's own account, never from invention. Blameless: causes are systems, habits and information, not individuals.

Writes: `planning/retros/<date>.md` (template `retrospective.md`; a `-2` suffix if another retro exists for that date).
Next: `/app-plan` or `/app-sprint plan` with the actions loaded; `/app-tech-debt add` for debt the retro found; `/app-incident` if an incident has no postmortem yet.

## When to use and when not to

- Use at the end of a sprint, a kanban review period, a milestone, a release, or after an incident has been resolved.
- Not for the incident itself (`/app-incident` runs it and writes the blameless postmortem; an incident retro reads that postmortem and looks at the process around it), not for a mid-sprint health check (`/app-sprint status`), not for a gate decision (`/app-gate`).

## Inputs

Resolve the app per orchestration.md section 1 and announce per section 2. Scope comes from the argument; with none, ask which of the four and which one. Inventory every input as FOUND or ABSENT before writing anything, and print the inventory.

| Scope | Reads |
|---|---|
| sprint | `planning/sprints/<id>.md`, the stories it committed (Status, Estimate, Completion notes), git log for the sprint dates, `docs/qa/bugs/` (or the issue tracker the app uses), `planning/tech-debt.md`, the previous retro in `planning/retros/` |
| kanban period | the period dates (ask), `planning/sprints/kanban.md`, stories that moved in the period, git log |
| milestone | the sprint plans and stories in it (the user names the sprints or the date range; no milestone file is assumed), `planning/risks.md`, the brief or vision for the milestone's goal, previous retros |
| release | `docs/release/<version>.md`, `CHANGELOG.md`, the release checklist results, bugs and hotfixes logged after the release, store review outcomes if any |
| incident | `docs/ops/incidents/<date>-<slug>.md` (the postmortem), the actions it lists, `docs/ops/runbooks/` entries involved, the release or change that preceded it |

A section whose input is ABSENT is `NOT ASSESSED - NO DATA`: not estimated, not inferred from an adjacent artifact. If every input for the scope is absent, stop with verdict NOT ASSESSED, name what is missing and the skill that produces it (`/app-sprint plan`, `/app-plan`, `/app-incident`). Zero commits in a period is reported as "0 commits in the period (denominator: the dates used)", not as a statement about effort. Absence of evidence is never evidence of absence: say which of the two happened.

An existing retro for the same scope: ask once to update it in place or start fresh (the old file is renamed with an `-archived-<date>` suffix in the same approved write, never deleted).

## Phase 1: Collect the facts (main session)

Read, once, and distil into a fact pack kept in `.studio/drafts/retro-<scope>-facts.md`:

- Planned versus actual: committed stories and weights (S 1, M 3, L 5) against stories Complete; stories carried over; stories added mid-period; stories descoped. Source of truth for "done" is the story file's Status (Complete is written only by `/app-story-done`); In Review is not done.
- Time and flow: dates, the days stories spent In Progress where evidence exists (story dates, commit dates on its Files), blocked stories and blockers recorded, review pile-ups.
- Quality: bugs opened and fixed in the period by severity (S1 to S4), hotfixes, regressions that a Complete story later produced, evidence gaps found at close (NOT VERIFIED run results).
- Debt: `TD-NNN` rows added and resolved in the period, with denominators; marker counts only if `/app-tech-debt scan` data exists for both ends (else NOT ASSESSED).
- Estimation: estimate (S, M, L) against what happened. Actual effort is recorded only if stories carry it (Completion notes) or the user states it; with no actuals, numeric accuracy is `NOT ASSESSED - NO DATA`, and the retro asks the user to name the two or three stories that felt most mis-sized instead.
- Previous retro: its actions and whether each was done (checked against evidence, for example a changed process file, a created story, a closed TD row), not self-reported.
- Velocity: the last three periods' committed and completed weight, if at least two exist; with one period, the trend is NOT ASSESSED.

Check: the fact pack exists and every figure in it names its source file or command.

## Phase 2: Analyse (sequence)

Agent: `program-director`. Brief per orchestration.md section 3 with the fact pack path and the key figures quoted, the goal of the period (from the sprint file or brief), and the rules: blameless, every statement tied to a figure or a file, causes over symptoms (ask "why" until a system or habit is reached), no more than five actions. Output: `.studio/drafts/retro-<scope>-analysis.md` containing: what went well (with evidence), what went poorly (with measurable impact), blockers and their causes, patterns across periods (recurring unaddressed items are a process smell and are named), a ranked list of candidate actions, and a list of what it could not judge. For an incident scope the brief also says: do not redo the postmortem; assess the surrounding process (detection time, change process, runbook quality, release gates) and how the postmortem's actions are progressing. When a release or incident touches a specialty, the main session may add one consulted agent (`release-manager` for release process, `site-reliability-engineer` for operations), each with its own named draft file and the same return contract.

Verify before using: spot-check at least two claims by re-reading the cited file or command output. Claims that do not check are removed; unchecked ones stay marked `UNVERIFIED`.

## Phase 3: The people's account (decision point)

Show the analysis summary in plain text, then ask the user, in plain text and one question, for their own view: what felt good, what felt bad, anything the data missed. For a team, say whose input is missing (this skill cannot ask other people). Record their words as stated. Where the user's account and the data disagree, show both and ask which stands; never silently pick. The user decides the final actions: keep at most five, each with one owner (the user if solo) and a deadline, a priority (High, Med, Low), and the evidence that will show it was done. An action with no owner or no deadline is not accepted. A skipped or empty answer is not an answer: ask again, or record "no account given" and say so in the file.

## Phase 4: Write

Draft the file from `retrospective.md`, keeping its header (Period, Date held, Participants, Type) and its sections in its order, each present even when NOT ASSESSED: What we set out to do; What happened (metrics, with denominators; put the inputs inventory FOUND and ABSENT, velocity trend, estimation accuracy, carryover and debt status here as rows or notes); What went well; What did not go well (include blockers and prevention); Root causes; Surprises and lessons; Follow-up on the last retrospective's actions (done, in progress, not started, with evidence); Actions (#, action, owner, due, how we will know it worked; add priority High, Med or Low in the action text). At full rigor add trend lines across retros and a short Process changes section (two or three, with expected benefit), and a two or three sentence summary naming the single most important change. One ask: "Write `planning/retros/<date>.md`?" (naming any rename of an older retro in the same ask). On yes, write it, then re-read to confirm every section is present and every action has an owner and a deadline. Overwrite the checkpoint (section 9).

## Phase 5: Hand-off

Offer, without doing: turn actions that are work into stories (`/app-plan`) or debt rows (`/app-tech-debt add`); start the next sprint with the retro's actions and velocity (`/app-sprint plan`); for a milestone, `/app-gate` when a stage change is in question; for an incident with no postmortem, `/app-incident`. Never start any of them.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Depth | one page: figures, three keep/change points, up to three actions | all sections | all sections plus pattern analysis over the last three periods and a follow-up of every earlier action |
| Agents | none beyond `program-director`; solo work may skip Phase 2's agent and use the main session (printed as a skipped step) | `program-director` | `program-director` plus consulted specialists for release and incident scopes |

No gates run in this skill at any review mode (print `none run (<mode>)`). Rigor changes depth, never honesty: figures still name their sources and gaps are still named.

## Verdicts

First match wins:

1. BLOCKED: the user declined the write, or the analysis artifact is missing after one re-brief.
2. NOT ASSESSED: every input for the scope was absent, or no usable period could be identified.
3. COMPLETE: the file is written and verified. Sections that were `NOT ASSESSED - NO DATA` are listed on the verdict line, for example `COMPLETE - 3 of 11 sections NOT ASSESSED (no estimate actuals, one period of history)`.

## Report

```
App: <name>   Scope: <sprint|kanban|milestone|release|incident> <id>   Rigor: <r>   Review: <m>
Inputs: FOUND <list>; ABSENT <list>
Planned <n> (weight <w>), completed <n> (weight <w>), carried <n>, added <n>, descoped <n>
Top findings: <up to 5 bullets, each with its evidence>
Actions: <n> (<owner and deadline each>)   Previous actions done: <x> of <y>
Not spawned: <agent> (<why>)   Skipped: <step> (<why>)
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <path, or none>
Next: </app-sprint plan | /app-plan | /app-tech-debt add ...> (<why>)
```

## Rules for this skill

- Blameless: name causes in systems, habits and information, not people. Never rank individuals.
- Evidence first: every finding cites a file, a command output or the user's own words; unsourced claims are removed.
- Never fill a section with an estimate when the data is absent: it reads `NOT ASSESSED - NO DATA`.
- At most five actions, each with an owner and a deadline; an action no one owns is not an action.
- Previous actions are checked against evidence, not memory.
- Never redo an incident postmortem; read it and assess the process around it.
- Never delete an older retro; archive it by rename inside the approved write.
- Recommend the next skill; never start it.
