---
name: app-team-feature
description: "Deliver one feature end to end with the studio team: spec, UX, architecture, stories, build, parallel review, close. Use when the user wants a whole new feature or capability built properly, says 'build this feature', 'take this from idea to done', or names a feature that needs more than one story."
argument-hint: "[app] [feature description or spec path] [--review solo|lean|full]"
user-invocable: true
---

# Team: Feature

Runs one feature through the whole studio pipeline by calling the skills that already own each step and adding the team coordination around them: who is spawned, where each agent writes, where the user decides, and one merged verdict. It is the flagship for new work. It never re-implements `app-spec`, `app-ux`, `app-plan`, `app-dev-story`, `app-story-done` or `app-code-review`; it sequences them.

Writes: `docs/product/specs/<feature>.md` (via `app-spec`, template `feature-spec.md`), `docs/design/ux/<flow>.md` (via `app-ux`, template `ux-spec.md`), `planning/epics/<epic>/` stories (via `app-plan`), code and tests (via `app-dev-story`), `docs/qa/reviews/<date>-<feature>.md` (template `code-review-report.md`), and the run record `planning/features/<feature>/<phase>-<agent>.md`, one file per agent per phase.
Next: `app-team-ui` (polish the screens), `app-team-harden` (before a release), `app-release`.

## When to use and when not to

- Use for a feature that needs a spec and more than one story, or that crosses layers (UI plus service plus data).
- A single small change with a clear story: `app-dev-story`. A bug: `app-bugfix`. Only the screens of a feature: `app-team-ui`. A risky unknown: `app-prototype` first. Planning only, no building: `app-spec` then `app-plan`.

## Inputs

- The app, per orchestration.md section 1 (first argument if it is a folder holding `studio.yaml`, else the current folder). No `studio.yaml`: offer `/app-adopt` or `/app-start` and stop.
- A feature description or an existing spec path. **No description: ask in plain text what the feature is and who it is for, spawn nothing, and wait.**
- Read once and pass distilled: `studio.yaml` (platforms, stack, commands, specialists, rules), the brief or vision, the architecture doc and stack reference if present, the design language if the feature has UI, `planning/tech-debt.md` and `planning/risks.md` for entries touching the same area.
- A missing optional input is named in the announce block and in the brief of every agent that would have used it. A missing command in `commands:` (test, build, run) makes the matching check NOT VERIFIED later, never skipped silently.
- Feature slug: kebab-case from the description; confirm it with the user once. It names every path below.

## Phase 0: Resolve and announce

Main session. Follow orchestration.md sections 1 and 2, then:

1. Resume check: if `.studio/state.md` shows an unfinished run for this slug, offer to resume at its checkpoint.
2. Classify the feature to choose agents: **layers** (UI, service, data, integration, background), **platforms** touched (from `studio.yaml`), **sensitive** (auth, money, personal data, IPC, new network exposure, updates, parsing untrusted input, secrets), **has user-visible surface**, **perf-sensitive**. Show the classification; the user may correct it.
3. Print the announce block, listing builders from the routing table below and every agent not spawned with the reason (for example `ios-engineer: not spawned, app has no iOS target`).
4. Ask once (plain text then AskUserQuestion): run `app-dev-story` and `app-story-done` for each story inside this session by reading their SKILL.md and following them, or will the user type them per story? Those two skills are user-typed by design (they mutate story state), so this run only follows them with this explicit yes. A "no" means Phases 5 and 7 pause at each story and tell the user the exact command.

### Builder routing (select from `studio.yaml`, never hardcode one stack)

| Layer or platform | Design consult | Builders |
|---|---|---|
| web client | `web-lead` | `frontend-engineer`, `ui-engineer`, `web-framework-specialist` (framework-specific), `web-platform-engineer` (PWA, workers, offline, extensions) |
| Windows | `desktop-lead` | `windows-desktop-engineer`; `win32-systems-specialist` below the UI |
| macOS | `desktop-lead` | `macos-engineer` |
| Linux | `desktop-lead` | `linux-desktop-engineer` |
| webview or cross-platform desktop shell | `desktop-lead` | `hybrid-desktop-engineer` |
| iOS or iPadOS | `mobile-lead` | `ios-engineer` |
| Android | `mobile-lead` | `android-engineer` |
| cross-platform mobile | `mobile-lead` | `cross-platform-mobile-engineer` |
| backend service | `backend-lead` | `backend-engineer`; `api-designer` (contract), `database-engineer` (schema), `distributed-systems-engineer` (concurrency, realtime, sync), `integrations-engineer` (third parties), `identity-specialist` (auth), `data-engineer` (pipelines), `ai-features-engineer` (model features) |
| CLI or library | `principal-engineer` | the language specialist, plus `backend-engineer` if it talks to a network |
| browser extension | `web-lead` | `web-platform-engineer` |

Always add the language specialist(s) listed in `studio.yaml` `specialists:` for code-quality review. Add `security-lead` as a consult whenever the feature is sensitive.

## Phase 1: Spec

Run `/app-spec <feature>` (it spawns `product-manager` and `business-analyst` when the feature has complex rules, states or workflows; `ux-designer` and the relevant lead are consulted by it). If a spec already exists at the path, show its requirement count and ask: use as is, retrofit with `app-spec` retrofit mode, or write a new one.

- Check: the spec file exists, has `REQ-<feature>-NNN` IDs, and every requirement has binary acceptance criteria. Count them and show the denominator ("14 requirements, 14 with acceptance criteria").
- Decision point: the user approves the spec (app-spec asks). Gates PD-SPEC-ALIGN and TD-FEASIBILITY run only where app-spec runs them at `full`.
- Cannot be skipped at any rigor. At minimal it is a half page of requirements with acceptance criteria.

## Phase 2: UX

Skip, with a printed note, only when the feature has no user-visible surface (a pure backend or library change: its interface is designed in Phase 3). For a CLI the surface is the command grammar, help text, output, errors and exit codes; `app-ux` handles that.

Run `/app-ux <flow>` (`ux-designer`, `content-designer`, `accessibility-specialist`, `ui-designer`). If the feature has UI and no `docs/design/design-language.md` exists, offer `/app-design-language` first; if declined, the UX spec records the assumption.

- Check: the UX spec exists and names every state (empty, loading, error, partial, offline), every platform variant the feature ships on, the copy, and accessibility notes. Gate DD-UX-SPEC per app-ux at `full`.
- Decision point: user approves. A visual or screen-heavy feature should have `app-team-ui` run after Phase 5.

## Phase 3: Architecture and contracts

Spawn in one message, in parallel, only the agents the classification calls for. Each writes `planning/features/<feature>/3-<agent>.md` (new studio document, allowed directly).

| Agent | Spawn when | Produces |
|---|---|---|
| `principal-engineer` | always (at minimal: alone) | approach, module boundaries, file list, reuse of existing code, test strategy per change type, risks |
| platform lead(s) from the routing table | feature touches that platform at standard and full | placement and feasibility on the platform, conventions to follow |
| `api-designer` | the feature adds or changes an interface another program uses | contract outline; the contract itself is then written with `/app-api` |
| `database-engineer` | the feature stores or changes data | schema change, migration approach; existing data means `/app-data-migration` before the story that changes it |
| `security-lead` | the feature is sensitive | trust boundaries, abuse cases, required mitigations; a new trust boundary means `/app-threat-model` update |
| `identity-specialist`, `privacy-specialist` | auth, or personal data collected or shared | their design constraints |

The main session reconciles the notes. Conflicts between agents are shown with options, never settled silently. A decision that outlives the feature becomes an ADR draft through `/app-adr` (Proposed; only the user accepts). If the feature changes the system structure, offer `/app-architecture` update.

- Check: every spawned agent's file exists with real content; the principal-engineer note lists files and a test approach for each requirement group.
- Decision point: the user approves the approach. Gates: PE-FEASIBILITY at `full`; TD-ADR belongs to `app-adr`.
- Minimal rigor: a change that fits the existing structure and is not sensitive needs only the principal-engineer note (a short approach). A sensitive feature never skips `security-lead`.

## Phase 4: Stories

Run `/app-plan <feature>`. It never renumbers or rewrites existing stories and runs QL-STORY-READY and PG-PLAN per review mode.

- Check: story files exist under `planning/epics/`; each has a change type, estimate, Files list, acceptance criteria traced to REQ IDs, test cases and dependencies. Every REQ ID in the spec appears in at least one story; list any that do not.
- Decision point: the user approves the story set and the build order. A story blocked by a Proposed ADR stays blocked until the user accepts the ADR.

## Phase 5: Build

For each story, in dependency order, follow `app-dev-story` (consent from Phase 0). Route the story to the builders in the routing table by layer; the language specialist advises. Builders return the files they will change; ask once per story for the set, then they write.

- Parallel builders only for stories whose Files lists do not overlap. Two agents never edit the same file at once.
- Every story brings its tests (`test-engineer` for gaps) and, for anything a user can see, a Run result line (orchestration.md section 10) with evidence in `docs/qa/evidence/<story>/`.
- After each story the main session runs `commands.test` (and `lint` if set) and reads the output; a builder's claim that tests pass is UNVERIFIED until then.
- `app-dev-story` never closes a story. BLOCKED stops that story and anything depending on it; others continue.
- Checkpoint after each story (orchestration.md section 9).
- Cannot be skipped. Rigor never relaxes tests-with-the-change or run-and-observe for visible changes.

## Phase 6: Review (parallel)

When all stories are built, run `/app-code-review` on the feature's diff (it is not user-typed; it brings `code-reviewer`, the language and platform specialists and, for sensitive or parsing, auth, IPC or network code, `security-engineer`, verifies its findings and writes `docs/qa/reviews/<date>-<feature>.md` from `code-review-report.md`). Do not re-implement it. In the same message that starts its agents, spawn the lenses it does not cover, each told to review only this feature's diff and to be adversarial ("find where it fails the spec, do not confirm it matches"):

| Agent | Spawn when | Writes |
|---|---|---|
| `accessibility-specialist` | the feature has UI | `planning/features/<feature>/6-accessibility-specialist.md` |
| `performance-engineer` | perf-sensitive, against `perf-budget.md` if present (no budget: NOT ASSESSED for that lens) | `planning/features/<feature>/6-performance-engineer.md` |

Collect all before continuing. Then the main session spot-checks every CRITICAL and HIGH finding from the lenses above (`app-code-review` has already verified its own) by re-reading the cited code (label the rest UNVERIFIED), and presents the verified list. Decision point: fix now, defer to `planning/tech-debt.md`, or reject with a reason, per finding group. Fixes go back to the owning builder (one ask for the file set), then the affected reviewer re-checks the changed hunks. Two rounds at most before the user decides how to proceed.

- Check: the code review report and each spawned lens's file exist. A reviewer that returned nothing is a named gap, and the verdict cannot be COMPLETE.
- Minimal rigor: `app-code-review` (which includes `security-engineer` if sensitive), plus `accessibility-specialist` if new screens were added. The code review never skips.

## Phase 7: Close

For each story run `app-story-done` (consent from Phase 0): acceptance criteria against evidence, scope check, code review, tests. A story whose result is BLOCKED or NOT ASSESSED is closed only after an unconditional ask (orchestration.md section 6).

Then the main session builds the traceability table: each `REQ-<feature>-NNN`, its stories, their closing status, its evidence. A requirement with no closed story is a gap, not a pass. Offer `technical-writer` for user documentation when the feature is user-visible (standard and full), and a CHANGELOG entry under Unreleased.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Spec | half page, REQs with acceptance criteria | full `app-spec` | plus PD-SPEC-ALIGN, TD-FEASIBILITY |
| UX | only if user-visible | `app-ux` | plus DD-UX-SPEC |
| Architecture | principal-engineer note | plus leads and specialists called for | plus ADRs, PE-FEASIBILITY |
| Review | code-reviewer plus what the change touches | all applicable lenses | all applicable lenses, adversarial brief |

Review mode: `solo` skips every gate and prints `<GATE-ID> skipped: solo mode`; `lean` runs only the always-on gates of `gates/README.md` inside the called skills (for example `PE-CODE-REVIEW` at `app-story-done` for non-trivial changes) and prints the rest as `skipped: lean mode`; `full` runs every gate the called skills name. The reviewers in Phase 6 are workflow, not gates, so they run in every mode.

Phases that may be skipped at minimal rigor: 2 (no visible surface), 3 (trivial, non-sensitive change), and the optional lenses of 6. Phases that never skip: 1, 4 (one story is enough), 5, the code-reviewer part of 6, and 7.

## Verdicts

First match wins:

1. `BLOCKED` - an agent or skill returned BLOCKED and the user has not resolved it, or the user stopped before any story was built.
2. `NEEDS WORK` - a verified CRITICAL or HIGH finding is open, a test fails, or a story failed its acceptance criteria.
3. `NOT ASSESSED` - a required piece of evidence is missing: a reviewer returned nothing, a visible change has Run result NOT VERIFIED, a requirement has no closed story because the run was stopped early, or a lens needing a budget or command that is absent. Say which.
4. `COMPLETE WITH NOTES` - everything closed; accepted deviations, deferred findings or tech-debt rows are listed.
5. `COMPLETE` - every requirement traced to a closed story with evidence, all reviewers reported, no open findings above LOW.

## Report

```
Feature: <slug>   App: <name>   Rigor: <r>   Review: <m>
Phases: 1 Spec <path, N REQs> | 2 UX <path or skipped: why> | 3 Architecture <agents, ADR drafts> | 4 Stories <N> | 5 Build <N built, N BLOCKED> | 6 Review <lenses run / not spawned> | 7 Close <N closed of N>
Traceability: <REQ-ID: stories, status> (denominator: N requirements)
Findings: <N verified CRITICAL/HIGH/MEDIUM/LOW>, <N fixed>, <N deferred to tech-debt>, <N UNVERIFIED>
Run results: <one line per visible story>
Gaps: <named gaps, or none>
```

Then the closing block from orchestration.md section 8: `Verdict`, `Gates`, `Wrote`, `Next`.

## Rules for this skill

- Never close a story outside `app-story-done`, never accept an ADR, never advance the stage.
- Never skip a phase silently; every skip is printed with its reason.
- Never run two agents on the same file, and never let an agent pick its own output path.
- Never fill a missing agent's section with your own content; it stays a named gap.
- Commits, merges, tags and pushes are not part of this skill; ask the user separately if wanted.
- Ask at each decision point with AskUserQuestion, question last; a dismissed answer is not an answer.
