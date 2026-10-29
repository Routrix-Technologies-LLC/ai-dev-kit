---
name: app-tech-debt
description: "Finds, registers, prioritizes and plans paydown of technical debt in planning/tech-debt.md, with stable TD-NNN IDs that are never reused. Use when the user asks about tech debt, wants a debt scan, wants to log a shortcut, wants to know what to clean up first, or wants debt turned into stories."
argument-hint: "[app] [scan | add | prioritize | report | plan] [--review solo|lean|full]"
user-invocable: true
---

# App Tech Debt

Debt is a tool, not a sin: the register exists so every shortcut is a recorded, priced decision instead of a surprise. This skill keeps one register, `planning/tech-debt.md`, with stable `TD-NNN` IDs, and works in five modes: `scan` finds debt in the code, `add` records one by hand, `prioritize` scores and orders the register, `report` summarizes it, `plan` turns chosen items into stories.

Writes: `planning/tech-debt.md` (template `tech-debt-register.md`); in `plan` mode also `planning/epics/tech-debt/epic.md` and story files.
Next: `/app-sprint plan` to schedule paydown stories, `/app-dev-story` to start one, `/app-upgrade` for dependency items.

## When to use and when not to

- Use at least once per sprint or milestone (scan, then report), whenever a shortcut is taken on purpose (add), and before planning (prioritize).
- Not for bugs (`/app-bugfix`), vulnerabilities (`/app-security-audit`, which owns SEC-NNN findings; a debt row may cross-reference one), or a whole-app health audit (`/app-team-audit`, which proposes stories and may feed this register).
- Debt rows are not stories. A row becomes work only through `plan` mode or `/app-plan`.

## Inputs

Resolve the app per orchestration.md section 1 and announce per section 2. Read `studio.yaml` for platforms, stack, and the `commands:` that exist. The register may be absent on a first run (create it after the ask). Mode comes from the argument; with none, print the five modes and ask which. The code root is not assumed: find source folders from the stack and the repo layout, and name them in the report; an unresolved code root makes `scan` NOT ASSESSED.

## The register

Template `tech-debt-register.md` (its columns and words are canon). One table, nine columns, in the template's order. Any skill that adds a row (this one, `/app-story-done` when it logs deviations, `/app-code-review` suggestions the user chose to register) writes all nine.

| Column | Value |
|---|---|
| ID | `TD-` and three digits, one above the highest ever used. Never reused, never renumbered, even for a Paid, Dropped or Accepted row. Four digits if the register passes 999. |
| Area | the module or layer, and the platform when it is platform specific (for example `auth module, backend`) |
| Description | what is wrong and what it costs, with `file:line` or path; why it was taken on (deadline, spike, missing information). Mandatory: `unknown` is allowed, blank is not |
| Impact | High (user-visible bugs, security exposure, or blocks work), Medium (slows work or raises defect rates), Low (untidy but harmless); `unset` until judged |
| Cost to fix | S (under a day), M (days), L (a week or more: split into stories before scheduling); `unset` until judged |
| Interest | how fast it gets worse if left alone: High (every new feature on this code makes it worse), Medium (grows with time or dependency drift), Low (static); `unset` until judged |
| Owner | an agent or a person; `unassigned` until someone takes it |
| Status | `Open`; `Planned` with the story path; `In progress`; `Paid` with the date and story; `Accepted` with the date and reason (a conscious decision to live with it); `Dropped` with the reason |
| Source | `scan <date>`, `user <date>`, `story-done <story>`, `review <report path>`, `audit <report path>`, a bug ID or an ADR |

Header lines above the table: Last reviewed, Open rows (n of n total), Paydown budget. Below it: the Paydown plan table (Row, Planned story, Target sprint or release, Notes) and the Review log (Date, Reviewer, Rows added, Rows paid or dropped, Decisions); each approved write adds one Review log line. Security debt is never `Accepted` without `security-lead`: such a row stays Open with the question recorded. Priority is not a column: it is computed (impact times interest, divided by cost) and shown in the `prioritize` and `report` output.

Scan categories (used for denominators and the report; write the category into Area when it helps): Architecture, Code Quality, Test, Documentation, Dependency, Performance, Security, Build and Infra.

At minimal rigor only ID, Area, Description and Status must be filled; the other columns may be `unset`. Do not delete a Paid row.

## Mode: scan

### Phase 1: Establish the denominator (main session)

List the source files the scan will cover by folder and language, and count them. Zero source files, or an unresolved code root, is `NOT ASSESSED - no source files to scan`: stop, write nothing. "No debt found in zero files" must never read as a clean result. Every count in this skill carries its denominator ("3 TODOs in 214 files").

### Phase 2: Find debt (parallel, read-only)

Spawn in parallel in one message, one output file each under `.studio/drafts/` (`<skill>-<scope>-<agent>.md`), with the return contract of orchestration.md section 3 (these agents report; they do not edit the register or source; `code-reviewer` is read-only and returns findings inline):

| Agent | Looks for | Output |
|---|---|---|
| `principal-engineer` | architecture and code-quality debt: module boundary violations, circular dependencies, god objects, duplicated logic, leaky abstractions, layering shortcuts, files and functions far beyond the app's own norms; churn hotspots (files changed most often in the last quarter that are also large or untested) | `.studio/drafts/tech-debt-scan-principal-engineer.md` |
| `modernization-engineer` | dependency and platform debt: outdated or abandoned packages, deprecated APIs in use, runtimes or SDKs approaching end of support, pinned-forever versions, framework patterns the vendor has replaced, dead code and feature flags past their purpose; uses the stack's own read-only tooling for outdated, unused and advisory-flagged dependencies (and says which it ran; never an `audit fix`, `update` or anything that rewrites a manifest or lock file) | `.studio/drafts/tech-debt-scan-modernization-engineer.md` |
| `code-reviewer` | markers and smells: TODO, FIXME, HACK, XXX with age from git blame; lint, type and warning suppressions (the stack's forms: disabled lint rules, ignore comments, `any` or untyped escapes, allow-attributes); skipped, disabled or flaky tests; tests missing near risky code; error handling that swallows failures; hard-coded values that should be config. Read-only: it returns its findings inline and the main session writes them to the draft file | `.studio/drafts/tech-debt-scan-code-reviewer.md` |

Add by platform where it applies: `build-engineer` for build-time and CI debt (slow or flaky pipelines, unreproducible builds, warnings tolerated), `accessibility-specialist` or `localization-specialist` when UI exists and hard-coded strings or inaccessible components are suspected. Name each agent not spawned and why. Each agent states, per category, what it searched, how many files, and what it could not check (for example no network for an advisory lookup). A category with nothing checked is `NOT ASSESSED` in the report, never clean. Check: each draft file exists with real content; re-brief once if not.

### Phase 3: Verify and match (main session)

Spot-check at least one finding per agent by re-reading the code. A finding that fails the check is dropped and noted; an unchecked agent claim is labelled `UNVERIFIED` and not registered unless the user asks. Then match against the register: a finding with the same file and kind of debt as an existing Open or Planned row updates that row (never duplicates); an Open row whose pattern no longer exists in its file is proposed as `Paid <date>` with the evidence.

### Phase 4: One ask, then write

Show new rows (with proposed Area, Impact, Cost to fix, Interest and Owner, `unset` where no one can judge), updated rows, and rows proposed as Paid, plus the per-category denominators. One ask for the whole set: "Write these to `planning/tech-debt.md`?" Options: write all, write new only, not now. A skipped answer is not a yes. On yes, edit the register (create from the template if absent), assigning IDs in order, then re-read it and confirm the row count matches what was approved and that no ID repeated. Overwrite the checkpoint.

## Mode: add

Ask in plain text for the description (including why it was taken on) and affected files, then ask for Area, Impact, Cost to fix and Interest as options (or `unset` if the user cannot judge). If an Open row has the same file and area, show it and ask whether to update it instead. Show the complete row; one ask to append; append with the next ID. Source is `user <date>`.

## Mode: prioritize

Requires the register; if it does not exist the verdict is NOT ASSESSED (run `scan` or `add` first). Score `impact x interest / cost` with Impact and Interest Low 1, Medium 2, High 3, and Cost to fix S 1, M 2, L 4, one decimal. Two adjustments are stated on the row, never hidden: a Security or dependency row tied to an end-of-support date or a published advisory moves up one Impact level (and says why), and a row that blocks a planned story or upgrade is marked `blocking <path>` and sorts above unblocked rows of equal score. A row with Impact, Interest or Cost unset is listed after the scored rows as `not scored: <column> not judged`. Higher score first; ties go to the lower ID. Rows Open for more than three sprints (or 90 days with no sprints) are listed as `stale: fix, plan or Accept with a reason`. Present the ordering and the recommended next set (what fits the next sprint or kanban capacity, if the user gave one). One ask to write the judged Impact, Cost to fix, Interest and Owner values the user approved, the chosen rows into the Paydown plan, and a Review log line.

## Mode: report

Read-only. Print: open count and cost to fix by scan category; added and Paid in the window (the last sprint or the last 30 days, said); trend (growing, stable, shrinking, from added versus Paid); the ten highest-priority Open rows; stale rows; rows Planned whose story is Complete but not marked Paid (propose the fix); Accepted rows with their reasons. Unscored rows are counted, not ignored. Writes nothing.

## Mode: plan (turn debt into stories)

1. Select: the user names TD IDs, or the skill proposes the top Open scored rows that fit a stated budget (days or story count). Rows with Cost to fix L must be split first: propose the split into M or smaller steps with a stated order.
2. Draft: `principal-engineer` (with `modernization-engineer` for dependency and framework rows, and the language or platform specialist from `studio.yaml` for the area) writes `.studio/drafts/debt-plan-stories.md`: per story the title, the TD ID, change type (Logic for refactors, Config, Infra, Performance, Security, Docs; whichever is closest), estimate S, M or L, planned Files, the other `templates/story.md` header fields (`Platforms`, `Rank`, `Requirement IDs`: the TD ID, `Governing decision`: `N/A: <reason>`), dependencies, and acceptance criteria that are binary and measurable: behaviour unchanged (named existing tests pass, and characterization tests added first where coverage is thin), plus the structural claim (for example "no module in X imports Y", "the deprecated call appears 0 times in 214 files", "bundle size at most the recorded value"). Criteria trace to the TD ID (no REQ ID exists; do not invent one) and, where the debt came from a requirement, to it.
3. Check each draft against the readiness groups of `.claude/skills/app-story-ready/SKILL.md` (Phase 3), inline. Pass: `Ready`. Anything failing: `Draft` with the gaps.
4. Numbering: stories go in `planning/epics/tech-debt/` (create `epic.md` if absent, otherwise append rows to its Stories table only), numbered on from the highest existing story number; existing stories are never rewritten.
5. One ask naming every file; on yes write them, set each source row to `Planned <story path>` (and add it to the Paydown plan table), and verify by re-reading. Status owners are the same as in `/app-plan`: this skill writes Ready or Draft once at creation and never changes a story afterwards. Run mode gates: none.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Scan agents | `code-reviewer` only | all three | all three plus build, accessibility, localization where relevant |
| Register columns | ID, Area, Description, Status required; the rest may be `unset` | all nine; Impact, Cost to fix, Interest, Owner and Source judged for new rows | all nine judged, plus the Paydown plan and Review log |
| Paydown stories | Draft or Ready by the readiness check | same | same; no gate runs |

No gates run in this skill at any review mode (print `none run (<mode>)`). Rigor changes how many agents look and how complete each row is, never what a row must say. A solo run skips no check here, because this skill runs no gate.

## Verdicts

The catalog verdict is COMPLETE; this skill adds the two outcomes its honesty requires. First match wins:

1. BLOCKED: the user declined the write, or a required agent output is missing after one re-brief.
2. NOT ASSESSED: scan over zero source files or an unresolved code root; prioritize or report with no register; a scan where every category was unchecked.
3. COMPLETE: the mode's work was done and, where a write was approved, verified on disk. Categories not checked are named on the line: `COMPLETE - 9 rows added; Dependency NOT ASSESSED (no network)`.

## Report

```
App: <name>   Mode: <mode>   Rigor: <r>   Review: <m>
Scanned: <files> files in <folders>; categories checked: <list>; NOT ASSESSED: <list or none>
Rows: <added> new, <updated> updated, <paid> proposed Paid; register total <n> (<open> open)
Top open: TD-NNN <description> (score)   [up to 5]
Not spawned: <agent> (<why>)   Skipped: <step> (<why>)
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <paths, or none>
Next: </app-sprint plan | /app-tech-debt plan | /app-upgrade ...> (<why>)
```

## Rules for this skill

- IDs are stable: never reuse, renumber or delete a TD ID; Paid, Dropped and Accepted rows stay.
- Never register debt without a reason it exists; "unknown" is allowed, blank is not.
- Never report a clean scan without its denominator, and never treat an unchecked category as clean.
- Never edit source code; paydown is done by stories through `/app-dev-story`.
- Match before appending; never duplicate an Open row.
- One ask per artifact set; a skipped answer is not a yes.
- Recommend the next skill; never start it.
