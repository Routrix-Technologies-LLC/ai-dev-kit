---
name: app-plan
description: "Turns feature specs into epics and implementable stories, each with a change type, an S/M/L estimate, a planned Files list, binary acceptance criteria traced to requirement IDs, QA test cases and dependencies. Use when the user wants to break specs into epics and stories, plan the work before building, or add stories for a new feature."
argument-hint: "[app] [feature | epic-slug | all] [--review solo|lean|full]"
user-invocable: true
---

# App Plan

Turns approved specs (the brief at minimal rigor) into epics and stories a builder can pick up cold. A story is one implementable behaviour: small enough to finish and prove in one sitting, self-contained, traced to a requirement and to the decision that governs it. This skill plans; it never writes code and never starts a story.

Writes: `planning/epics/<epic>/epic.md` (template `epic.md`) and `planning/epics/<epic>/story-NNN-<slug>.md` (template `story.md`), all subject to the app's `paths:` overrides.
Next: `/app-story-ready <epic>` (check the stories), then `/app-sprint plan` (sprints or kanban order) or `/app-dev-story <story>`.

## When to use and when not to

- Use after specs exist (`/app-spec`) and, at standard and full rigor, after the architecture and its foundation decisions exist (`/app-architecture`, `/app-adr`).
- Not for one-line fixes (a bug goes to `/app-bugfix`) and not for choosing what to build (`/app-spec`, `/app-scope`). Not for debt paydown stories (`/app-tech-debt plan`).
- Run it per feature or per layer as the work approaches. Stories for work months away describe a design that will have changed.

## Inputs

Resolve the app per orchestration.md section 1 and announce per section 2. Read once, by section, never whole files you do not need:

| Input | Needed at | If missing |
|---|---|---|
| `docs/product/specs/<feature>.md` with `REQ-<feature>-NNN` IDs and acceptance criteria | standard, full | Stop. Offer `/app-spec` (or `/app-spec` retrofit mode for an existing spec). Never invent requirements. |
| `docs/product/brief.md` (MVP list and build order) | minimal (stands in for specs) | Stop. Offer `/app-brief`. |
| `docs/architecture/architecture.md` (components, boundaries) | standard, full | Stop. Offer `/app-architecture`. At minimal, ask the user for the module boundaries in plain text and record them in the epic. |
| ADRs (`docs/architecture/adr/`) or `docs/decisions.md` | standard, full / minimal | Statuses are read, never assumed. A story whose governing ADR is not Accepted is written Blocked, with the `Blocked reason` line `BLOCKED: <ADR-ID> is <status>`. |
| `docs/design/ux/<flow>.md`, `docs/design/design-language.md` | UI and Visual stories | Not a stop. The story's Out of Scope or Dependencies names the missing UX spec, and the story is written Draft. |
| `docs/architecture/api/`, `planning/migrations/`, `docs/security/threat-model.md` | Integration, Data, Security stories | Same: name the gap, write the story Draft or Blocked. |
| `docs/stack-reference.md`, `studio.yaml` | all | `studio.yaml` is required. Missing stack reference: framework-version risk is `NOT ASSESSED` in the story, never guessed. |
| Existing `planning/epics/**` | all | Absent is normal on a first run. |

The scope argument is a feature (all of its requirements), an existing epic slug (more stories for it), or `all` (every approved spec, one epic at a time). With no argument, list the specs and existing epics and ask which.

## Phase 1: Inventory what exists

The main session lists `planning/epics/*/epic.md` and every `story-*.md` with its Status. Record the highest story number per epic folder. Build a coverage map from every requirement ID in scope to the stories that already cite it.

Hard rules that start here:

- Story numbers are per epic folder, three digits, never reused and never renumbered, even for a Complete or abandoned story.
- An existing story file is never rewritten, reordered or renamed. A defect found in one (wrong estimate, stale ADR, missing criterion) goes in the report as a proposed edit with the exact text, for the user to apply.
- Requirements already covered by a story are not planned again.

Check: print `Specs: <n> in scope, <r> requirements; existing: <e> epics, <s> stories; uncovered requirements: <u>`. Zero requirements in scope is BLOCKED, not an empty plan.

## Phase 2: Decompose (sequence)

Agent: `principal-engineer`, with the platform leads and specialists the scope touches, chosen from `studio.yaml` `platforms` and `stack` (see the routing table below). Brief per orchestration.md section 3 with: the uncovered requirements (ID and text quoted), the architecture components they land in, the ADR statuses, the coverage map, the rigor, and the rules below. Output: `.studio/drafts/plan-<scope>-principal-engineer.md`, one file only.

The decomposition proposes, for each epic and story:

- **Epics:** one per architectural module or user-facing capability, not one per layer of tech. Name the slug, the requirement IDs it owns, its governing decisions and its Definition of Done (every story closed by `/app-story-done`, every criterion of the spec verified, evidence present per change type).
- **Stories:** a title, the requirement IDs covered, the **change type**, the **estimate**, the **planned Files list**, the platform(s), the governing ADR (or `N/A: <reason>`), the **dependencies** by path or by planned story name, and the **rank** (position in the epic's build order, 1 is first; the epic's Stories table lists the stories in the same order).

| Change type | Use when the story is mostly |
|---|---|
| Logic | rules, calculations, state transitions, validation, parsing |
| Integration | two or more components, an external service, an API or IPC contract, a persistence boundary |
| UI | screens, components, navigation, copy, accessibility behaviour (structure and function) |
| Visual | how it looks or feels: layout fidelity, motion, theming, polish |
| Data | schema, migration, storage or file-format change, backfill |
| Config | settings, flags, constants, build or manifest values with no new logic |
| Infra | hosting, CI/CD, environments, packaging, signing, observability plumbing |
| Security | a mitigation from the threat model, auth, secrets, permissions, hardening |
| Performance | meeting a budget: startup, latency, memory, size, battery |
| Docs | user or developer documentation |

A mixed story takes the type with the highest implementation risk and names the secondary in its title or notes. The type decides the evidence `/app-story-done` demands (`standards/testing.md`).

| Estimate | Meaning |
|---|---|
| S | a few hours; one component; no unknowns |
| M | about a day; two components or one unknown |
| L | several days; if it is more than about a week or touches more than three components, split it |

Decomposition rules: foundation behaviour first, edge cases after, UI last; a story that cannot be finished and observed on its own is split; a story with more than 8 acceptance criteria is split unless rigor is minimal (then up to 10); a threat-model mitigation or a Data change becomes its own story, never a line inside a feature story; dependencies form no cycle (check by listing each story's dependencies and walking them).

Routing for the platform lead and builders consulted on feasibility and the Files list (consult, do not delegate the whole plan):

| App platform | Consult |
|---|---|
| web | `web-lead`, `frontend-engineer` |
| windows, macos, linux | `desktop-lead`, and the OS engineer for each target (`windows-desktop-engineer`, `macos-engineer`, `linux-desktop-engineer`, or `hybrid-desktop-engineer` for webview or cross-platform shells) |
| ios, android | `mobile-lead`, `ios-engineer` and/or `android-engineer`, or `cross-platform-mobile-engineer` |
| backend | `backend-lead`, `backend-engineer`, `database-engineer` if Data stories exist, `api-designer` if contracts change |
| cli, library | `principal-engineer` alone, plus the language specialist from `studio.yaml` `specialists` |

Spawn the consulted leads in parallel with one brief each and one output file each (`.studio/drafts/plan-<scope>-<agent>.md`, one per lead), then give `principal-engineer` their notes. Check: the principal-engineer's decomposition file exists and has a row per story with every field above; any blank field sends the file back once with the gap named.

## Phase 3: Acceptance criteria and trace (sequence)

Agent: `product-manager`. Brief with the decomposition and the spec sections for the stories' requirement IDs. Output: `.studio/drafts/plan-<scope>-product-manager.md`.

For each story it writes the acceptance criteria as binary checkboxes, copied or tightened from the spec, each ending with the requirement ID it proves, for example `- [ ] Given an expired session, the API returns 401 and the client shows the sign-in screen (REQ-auth-004)`. A criterion is binary when two people given the finished work would agree on pass or fail without discussion. These fail: "works well", "is fast", "looks right", "is intuitive". For Visual stories a judgement criterion is allowed only when it names the evidence file and who signs it off. It also returns a **coverage table**: every requirement in scope, the stories that cover it, and `UNCOVERED` for any with none. An uncovered requirement is reported, never silently dropped. At minimal rigor the trace is `Brief MVP feature N`, never a fabricated REQ ID.

Check: every story has at least the minimum criteria (below) and every requirement in scope appears in the coverage table.

## Phase 4: QA test cases and testability (sequence)

Agent: `qa-lead`. Brief with the stories, their types and criteria. Output: `.studio/drafts/plan-<scope>-qa-lead.md`.

Per story: QA test cases by change type, written so `test-engineer` can implement them without asking. Logic and Integration use Given/When/Then with concrete values. UI and Visual use Setup/Verify/Pass condition per screen and state, per platform in scope. Data names the dry-run and rollback check. Security names the abuse case from the threat model. Performance names the budget and the measurement. Config and Infra name the smoke check. It also returns the story's evidence plan: the rows of `standards/testing.md` that apply to its change type and where the proof will live (a test path, or `docs/qa/evidence/<story>/`). A UI or Visual story's plan names how the change will be launched and looked at on each affected platform without taking focus or injecting input. It lists any criterion it judges untestable, with a rewrite. Check: every story has cases and an evidence line; untestable criteria were rewritten or the story is marked Draft with the reason.

## Phase 5: Assemble and self-check

The main session merges the drafts into complete stories using the exact `templates/story.md` layout. Header fields, in the template's exact names: `Epic`, `Status`, `Blocked reason` (only when Blocked, as `BLOCKED: <what must clear>`; otherwise delete the line), `Change type`, `Estimate`, `Rank`, `Platforms`, `Requirement IDs`, `Governing decision` (an ADR ID or `N/A: <reason>`, never blank), `Last updated` (the creation date; every status change refreshes it). The ADR decision summary and version stamp, the spec path and the UX, contract, migration, threat or budget references go in Context. Sections, in order, with the template's headings: Context, Acceptance Criteria (each ending with its requirement ID), Implementation Notes, Out of Scope, Files (never blank), QA Test Cases, Test Evidence, Run result (left as the template's placeholder: `/app-dev-story` fills it), Dependencies, Completion Notes (left empty). Each story is then run through the checklist in `.claude/skills/app-story-ready/SKILL.md` (Phase 3, the six groups), inline, without spawning; this self-check runs in every review mode. Status is assigned by that result, and `Ready` means the story passed that checklist in this run:

| Result of the self-check | Status written |
|---|---|
| Every blocking item passes | `Ready` |
| A governing ADR is not Accepted, or a dependency is missing, Draft or Blocked | `Blocked`, with the `Blocked reason` line `BLOCKED: <what must clear>` |
| Anything else fails or could not be checked (missing UX spec, open question, untestable criterion, input NOT ASSESSED) | `Draft`, with the gaps listed in the story's Context |

Never write `Ready` for a story that was not checked. Print the planned work as one table: epic, story, type, estimate, status, requirement IDs, dependencies, rank.

## Phase 6: Gates

Per orchestration.md section 7. Apply the review mode first.

- `QL-STORY-READY` (owner `qa-lead`): full only. Pass the story paths (drafts), each type, each criterion verbatim, the requirement text, and dependencies with state. One spawn for the whole set.
- `PG-PLAN` (owner `program-director`): full only. Pass the epics, stories with estimates, dependencies, the rank order, and the uncovered requirements. Spawn both in one message.
- Solo and lean print `QL-STORY-READY skipped: <mode> mode` and `PG-PLAN skipped: <mode> mode`. The inline self-check above still ran, so a story can be Ready without the gates.

Handle results: a blocking verdict stops the write and the plan is revised (or the user overrides, recorded in the report as `proceeding despite <GATE>: <verdict> (user override)`); CONCERNS go to the user in the Phase 7 decision; NOT ASSESSED keeps every story that depended on the missing input at Draft. Record each gate outcome in the epic.md header per `gates/README.md` ("Recording a gate outcome").

## Phase 7: One ask, then write

Present the plan table, the coverage table (with any UNCOVERED rows), the gate results and any proposed edits to existing stories. Ask once, covering the whole set, with the exact list of files to be created and the epic.md files to be created or updated: "Write these <n> files?" Options: write all, revise first, write only the Ready and Blocked stories (keeps Drafts as notes in the report). Per orchestration.md section 6 a skipped answer is not a yes.

On yes the main session writes each file at its path. An existing `epic.md` is updated only in the sections this skill owns (Specs and decisions, Stories, Definition of done for the epic) and by appending rows to its Stories table; its other content is untouched. The Stories table's Status column is the status at creation and is not maintained afterwards: the story file is the only authority. Check: re-read the directory and confirm each file exists, has the sections, and that story numbers continue each epic's sequence without gaps or reuse. Then overwrite the checkpoint (section 9).

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Input | brief (MVP list, build order); one epic per group of features that ship together | specs with REQ IDs, architecture, ADR statuses | same, plus threat model, UX specs, API contracts, migrations required for the types that need them |
| Story sections that must be filled | header, Acceptance Criteria, Files, QA Test Cases, Run result | adds Context with spec and REQ IDs, ADR summary and version stamp, Implementation Notes, Out of Scope, Test Evidence | adds Dependencies detail, platform-by-platform criteria |
| Trace | `Brief MVP feature N` | `REQ-<feature>-NNN` | `REQ-<feature>-NNN`, coverage table must show zero UNCOVERED or a user-accepted list |
| QA cases | per story, short | per story | per criterion |
| Gates | none at solo or lean | none at solo or lean | `PG-PLAN`, `QL-STORY-READY` when review mode is full |

Rigor changes what must exist, never what must work: every criterion is binary at every level, and a UI or Visual story always plans observed evidence.

Review mode: solo and lean skip both gates (`PG-PLAN` and `QL-STORY-READY` are full only per `gates/README.md`); full runs both. The inline readiness self-check runs in every mode.

## Delivery shape: sprints or kanban

Stories carry a Rank (build order from dependencies and value), not a sprint. A solo or small team can work straight down the rank (kanban) with `/app-sprint plan` in kanban mode, or group stories into sprints. This skill does not choose; it prints `Suggested order` in the report.

## Verdicts

First match wins. The catalog's verdict words are COMPLETE and BLOCKED; a story whose check or gate could not run is written Draft, never Ready, and the verdict line says so.

1. BLOCKED: required inputs missing (no specs or brief, no requirements in scope, no architecture at standard or full), the user declined the write, or a blocking gate verdict stands.
2. COMPLETE: files written and verified. The line carries the counts, for example `COMPLETE - 14 stories (9 Ready, 3 Blocked, 2 Draft; QL-STORY-READY NOT ASSESSED for 2)`.

## Report

```
App: <name>   Scope: <scope>   Rigor: <r>   Review: <m>
Epics: <n> (<new>, <updated>)   Stories written: <n> (Ready <a>, Blocked <b>, Draft <c>)
Requirement coverage: <covered>/<total> covered; UNCOVERED: <ids or none>
Existing stories: <n> untouched; proposed edits: <list with exact text, or none>
Suggested order: <rank list, dependency-respecting>
Not spawned: <agent> (<why>)   Skipped: <step> (<why>)
Run result: N/A - planning only, nothing observable
Verdict: <WORD> - <one line why>
Gates: <GATE-ID: VERDICT, ...> | none run (<mode>)
Wrote: <paths, or none>
Next: </app-story-ready ...> (<why>)
```

## Rules for this skill

- Never renumber, rewrite, reorder or delete an existing story or epic; propose edits instead.
- Never invent a requirement, a requirement ID or an ADR; an untraceable story is reported, not written as traced.
- Never write `Ready` unless the story passed the readiness checklist in this run.
- Never write source code, and never change a story's status after creation. Status owners: this skill writes Draft, Ready or Blocked once, at creation; `/app-dev-story` sets In Progress and In Review; only `/app-story-done` sets Complete; a Draft story becomes Ready when `/app-story-ready` returns READY and the user says yes to its single status write; a Blocked story becomes Ready only by the user's own edit. In lean and solo this skill runs its own readiness checklist inline and does not spawn the full-only `QL-STORY-READY` gate.
- Ask once for the whole file set; never one ask per story.
- Agent drafts live in `.studio/drafts/`; nothing there counts as a plan until written to `planning/`.
- Recommend the next skill; never start it.
