---
name: app-help
description: "Read-only and fast: say where an app is (stage, artifacts present, checkpoint, open stories) and name the one or two best next skills. Use when the user asks what to do next, where things stand, is stuck, returns after a break, or says 'help'."
argument-hint: "[app] [optional: what you just finished or are stuck on]"
user-invocable: true
---

# App Help

A quick orientation, not an audit. It reads the app's `studio.yaml`, the session checkpoint and the artifacts that exist, then answers three questions: where is this app, what is missing for the stage it is in, and what should the user type next. It writes nothing, spawns no agents, and runs no builds or tests. For a deep gap analysis of an existing codebase use `/app-adopt` (first time) or `/app-team-audit` (health).

Writes: nothing.
Next: whatever it recommends; it never starts it.

## When to use and when not to

- Use whenever the user is unsure what comes next, returns to an app after time away, or wants the status in one screen.
- Not for judging quality: this skill sees what exists, not whether it is good or whether tests pass. Use `/app-story-ready`, `/app-smoke`, `/app-gate` or `/app-team-audit` for that.
- No `studio.yaml` anywhere: say so and offer `/app-start` (new app) or `/app-adopt` (existing code), then stop.

## Inputs

- The app: the argument, else the current folder if it holds `studio.yaml`, else ask which app. Orchestration section 1 applies except that this skill never offers to resume work (it is not a work skill).
- Optional free text ("finished the architecture", "stuck on stories"): use it to personalize the answer, never to override what is on disk. If it contradicts the files, say what the files show.
- Optional: `.studio/state.md`. Absent is fine; say "no checkpoint".

## Phase 1: Read (main session, at most about a dozen tool calls)

Use Read, Glob and Grep only. Never recurse over `node_modules`, `target`, `build`, `.git` or similar. Check paths named in `studio.yaml` `paths:` first, then the defaults in `layout.md`.

1. Read `studio.yaml`: name, `stage`, `platforms`, `modes.rigor`, `modes.review`, `commands`, `specialists`. Note any empty `commands:` entries by name and an unset `stage` or `rigor`.
2. Read only the `CHECKPOINT` block of `.studio/state.md` (Grep for its markers, then Read that range). Pull: current task, next step, blocked on, last run result, open questions. Ignore the narrative below it.
3. Check artifacts by existence with Glob, one call per folder, not per file: the brief or vision, specs, UX specs, design language, architecture, ADRs, stack reference, threat model, privacy, epics and stories, sprint plans, test plans, evidence, release docs, runbooks, the latest `docs/gates/` report and the latest `docs/qa/smoke-*` report.
4. For a file the stage turns on, test whether it has real content: Grep for placeholder markers (`TBD`, `To be designed`, `TODO`, empty template headings) with a count and Read nothing else. A file that exists but is placeholder-only is `EMPTY`, not present.
5. If `planning/epics/` has stories, Grep their `Status` lines (one call over that folder) and count by value. The fixed words are Draft, Ready, In Progress, In Review, Complete and Blocked (a `Blocked: <reason>` line counts as Blocked). Any other value, including the older `Implemented`, counts as `OTHER`; report the count and say so.
6. Never run git commands that touch the working tree. `git -C <app> log -1 --format=%cr` and `git -C <app> status --short` (read-only) are allowed for "last commit" and "uncommitted changes" lines.

Anything that could not be read is reported as `NOT CHECKED - <why>`, never as absent.

## Phase 2: Judge the stage

Take `stage` from `studio.yaml`. If it is unset, say "stage not recorded" and use the table below only to say what the files suggest; do not write it. Compare the recorded stage with the evidence in one line:

| Recorded stage | Looks stale when |
|---|---|
| `discovery` or `definition` | source files exist but no brief or spec |
| `architecture` | no architecture doc and no ADRs |
| `foundation` | `commands.build` and `commands.test` both empty |
| `build` | no stories and no feature specs |
| `hardening` or `release` | no passing smoke report on record |
| `operate` | no release doc, changelog entry or tag |

A mismatch is a notice ("Recorded stage is `build`, but no stories exist; the stage may be stale, or planning lives elsewhere"), never a correction. Only `/app-gate` changes the stage, and `/app-adopt` records an existing app's first one.

Expected artifacts per stage (what `/app-gate` will look for next). Rigor decides which rows are required: `minimal` needs the first column only, `standard` adds the second, `full` adds the third. Anything not listed for a rigor is optional and is shown as `optional`, never as a gap.

| Stage | minimal | standard adds | full adds |
|---|---|---|---|
| discovery | brief | vision | first entries in `planning/risks.md` |
| definition | one spec per MVP feature | cross-spec review, UX specs for key flows | design language, usability plan |
| architecture | decision log (`docs/decisions.md`), stack choice | architecture doc, ADRs for foundation decisions, stack reference | threat model, performance budget |
| foundation | `commands.build` and `commands.test` filled and passing, one path running | CI green, test harness | evidence capture working per platform |
| build | stories with evidence per story | reviews per story | story-level security and accessibility checks |
| hardening | smoke pass, no open S1 | security audit, performance check | accessibility audit, privacy review, localization pass |
| release | checklist, release notes, rollback note | signed packages or store drafts | go/no-go record, staged rollout plan |
| operate | changelog kept, known issues | runbooks, monitoring | incident process, retrospective cadence |

## Phase 3: Choose the next skills

Pick the first applicable rule; add a second suggestion only when it is independent of the first. Use rows from this table in order.

| Situation | Recommend |
|---|---|
| No `studio.yaml` | `/app-start` (new) or `/app-adopt` (existing code) |
| Checkpoint lists a BLOCKED item | resolve it first; name the skill that produces what it waits for |
| Checkpoint has a concrete next step | that step, quoted |
| Adopted recently, no `docs/qa/adoption-report.md` follow-up done | `/app-team-audit` |
| `discovery`, no brief | `/app-brief` (or `/app-start` if there is no `studio.yaml` content) |
| `definition`, MVP features without specs | `/app-spec <feature>` |
| `definition`, specs but no review | `/app-spec-review` |
| `architecture`, no stack or empty stack fields | `/app-stack` |
| `architecture`, no architecture doc | `/app-architecture` |
| `foundation`, `commands` empty | `/app-test-setup` |
| `build`, specs without stories | `/app-plan` |
| `build`, stories `Draft` | `/app-story-ready` (checks them, then they can become Ready) |
| `build`, stories `Ready` | `/app-dev-story` (or `/app-sprint` first to order them) |
| `build`, a story `In Review` | `/app-story-done` for that story |
| `build`, a story `In Progress` and none In Review | continue `/app-dev-story` |
| `build`, all stories Complete | `/app-sprint` or `/app-gate` |
| All required artifacts for the stage present | `/app-gate` |
| `hardening` | `/app-team-harden` or the missing audit by name |
| `release` | `/app-team-release` or `/app-release` |
| `operate` | `/app-incident`, `/app-observability`, or `/app-retro` as the situation fits |
| The user said they are stuck on a named topic | the skill that owns that topic, with one sentence on why |

Never recommend more than two. If nothing fits, say so and ask what the user is trying to do.

## Phase 4: Report

Keep it under about thirty lines. Use this shape:

```
App: <name> (<path>)   Stage: <stage or "not recorded">   Rigor: <rigor>   Review: <mode>
Platforms: <list>   Last commit: <relative time or NOT CHECKED>   Uncommitted: <yes/no/NOT CHECKED>

Checkpoint: <task> | next: <step> | blocked on: <item or none>   (or: no checkpoint)

Artifacts for this stage (<rigor>):
  present   <name> (<path>)
  EMPTY     <name> (<path>): placeholder only
  missing   <name> (expected at <path>)
  optional  <name>
  NOT CHECKED  <name>: <why>

Stories: <n> draft, <n> ready, <n> in progress, <n> in review, <n> complete, <n> blocked, <n> other of <total>   (or: no stories yet)
Commands: build <filled|empty>, test <filled|empty>, lint <filled|empty>, run <filled|empty>
Notice: <stage mismatch or other oddity, or omit>

What existence cannot tell me: <one line, e.g. whether tests pass or the code is good>

Best next: </app-skill ...> - <why>
Also: </app-skill ...> - <why>   (omit if none)
```

Counts always show their denominator ("3 of 5 expected artifacts present"). A stage with nothing checkable says "nothing here can be checked by existence", never "complete".

## Verdict and closing block

This skill is informational. Its verdict is always `INFORMATIONAL`; the report above is the content. End with the closing block from orchestration section 8:

```
Verdict: INFORMATIONAL - <one line: stage and the top gap>
Gates: none run (read-only)
Wrote: none
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Read-only: no Write or Edit, no builds, no tests, no network, no agents.
- Never claim a stage is done because its files exist, or an app is healthy because nothing was found. Existence is not adequacy.
- Never report an unreadable path as missing; use `NOT CHECKED`.
- Never write or "fix" the stage or any setting. Name the skill that does.
- Be fast: do not read whole documents; counts, markers and the checkpoint block are enough.
- No em dashes or en dashes in the output.
