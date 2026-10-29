---
name: app-spec
description: "Author a feature spec section by section with requirement IDs and binary acceptance criteria, for a new feature or as a retrofit of an existing spec, PRD, ticket or shipped behavior. Use when the user wants to specify a feature, says 'write a spec', 'PRD', 'requirements for X', 'what exactly should this do', or a feature is about to be planned or built with no written definition."
argument-hint: "<feature name> [new | retrofit <path or 'from code'>] [--review solo|lean|full]"
user-invocable: true
---

# App Spec

Writes one feature's definition so it can be planned, built and tested without guessing: why it exists, what is in and out, every requirement with a stable ID, every state and edge case, how it behaves on each of the app's platforms, and acceptance criteria that anyone can answer pass or fail. It works one section at a time and writes each approved section to the file immediately, so nothing is lost to a crash or a compaction.

Writes: `docs/product/specs/<feature>.md` (template `feature-spec.md`; path from `paths.specs` when mapped). Requirement IDs are `REQ-<feature>-NNN`.
Next: `/app-spec-review` (in a fresh session), `/app-ux` for user-visible features, `/app-architecture` or `/app-adr` when the spec forces a technical decision, then `/app-plan`.

## When to use and when not to

- One feature or capability per run. A tiny change (copy, a tuning value) does not need a spec: put it in the story. A whole product definition is `/app-brief`.
- Screens, layout and copy detail go in `/app-ux`; the spec says what must be true, the UX spec says how it looks and flows.
- The independent review is `/app-spec-review`. Do not review your own spec in the same session as a final check.

## Inputs

- `studio.yaml` (orchestration section 1). Read `platforms`, `modes.rigor`, `modes.review`, `paths`.
- Product intent: the brief or vision. At `minimal` the brief; at `standard` and `full` the vision (or the brief if the vision does not exist yet). If neither exists, ask: write one first with `/app-brief`, or continue with the intent the user states now. Continuing records `Brief alignment: NOT ASSESSED (no brief)` in the spec header and makes `PD-SPEC-ALIGN` NOT ASSESSED.
- Other specs in the specs folder: list their names and requirement ID prefixes now (Glob, then Grep `REQ-` IDs with a count per file). They are used for conflict checks, not read in full unless a topic overlaps.
- Constraints already decided: architecture document, ADRs, stack reference, design language, UX specs. Read the headings and only the parts that touch this feature.
- A missing feature name: list the brief's MVP items that have no spec yet and ask which one. A feature name that matches an existing spec file switches to retrofit mode after confirmation.

## Mode selection

| Situation | Mode |
|---|---|
| No spec file for the feature, no source document | **new** |
| Spec file exists in studio format with missing or placeholder sections | **retrofit, fill**: author only the missing or placeholder sections; existing content is never modified |
| A PRD, ticket, README section, notes or chat history describes the feature in another format | **retrofit, convert**: faithfully map the source into the spec's sections (below) |
| The feature exists in code and has no document | **retrofit, from code**: document what it does today (below) |

Retrofit modes never renumber or reuse an existing requirement ID, never delete text, and say before writing what will be added.

## Phase 1: Announce and choose agents

Print the plan block (orchestration section 2). Select consulted agents from the app's platforms and the feature:

| Agent | Consulted for | When |
|---|---|---|
| `product-manager` | Scope, priorities, acceptance criteria wording | always (standard, full); at minimal the main session does this |
| `business-analyst` | Rules, states, decision tables, edge-case matrices, data dictionary | any feature with rules, workflows or several states; standard and full |
| `ux-designer` | User-visible behavior, states, platform conventions (consulted, proposes only) | the feature has a user interface; standard and full |
| the platform lead(s) for feasibility | `web-lead` (web, extension), `desktop-lead` (windows, macos, linux), `mobile-lead` (ios, android), `backend-lead` (backend, data, API) | the sections that touch their platform; standard and full |
| `technical-director` | gate `TD-FEASIBILITY` | review mode `full` |
| `product-director` | gate `PD-SPEC-ALIGN` | review mode `full` |

Agents return proposals in their reply; they write no files. The only writer of the spec is the main session. This replaces the file-path item of the return contract with "none (proposal text is in your reply)".

Gates: `PD-SPEC-ALIGN` and `TD-FEASIBILITY` both run in review mode `full` only (neither is a phase gate or always-on in `gates/README.md`); print `<GATE-ID> skipped: lean mode` or `skipped: solo mode` otherwise. `TD-FEASIBILITY` is for specs with technical uncertainty.

## Phase 2: Gather context

Read once, then give the user a short context summary (what the brief says this feature is for, adjacent specs, constraints found, platforms in play). For `new` mode ask: "Ready to start, or do you want to add context?" In retrofit modes read the source fully and run the mode-specific steps below before Phase 3.

**Retrofit, fill.** Read the existing spec by section headings (Grep `^#`, then Read ranges). List: sections present (not touched), sections missing, sections that are placeholder-only. Ask: "Shall I author the N missing sections? I will not modify any existing content." Existing requirement IDs are preserved and the next ID continues after the highest one.

**Retrofit, convert.** Read the source. Build a mapping table (source passage, target section, requirement) and show it before writing. Rules:
- Every requirement is traced to the passage it came from (`Source: <path or ticket>, <heading>`).
- Do not add requirements the source does not state. Gaps become Open Questions, not guesses.
- Contradictions inside the source are listed, not resolved.
- Mark the spec header `Converted from <source> on <date>; wording preserved where possible`.

**Retrofit, from code.** `business-analyst` reads the feature's code paths (named by the user or found from the brief) and returns observed behavior: inputs, outputs, states, error cases, permissions, platform differences. The spec states what the code does today, marked `OBSERVED (documented from code, intent unknown where unsure)`. Every requirement cites a file. Anything that looks accidental is an Open Question ("does this behavior need to be kept?"), not a requirement. Acceptance criteria are written against observed behavior and run by `test-engineer` later through `/app-plan`.

## Phase 3: Skeleton

After one ask ("May I create `<path>` with the section headings?"), create the file from `.claude/studio/templates/feature-spec.md` with the template's header line (Status `Draft`, Owner, Last updated, Serves, Related), plus rigor, brief alignment and source documents beneath it and every required heading holding the placeholder `[To be written]`. In retrofit modes skip creation; the file exists (convert mode creates it, with the converted-from header). Never set Status to In review, Approved or Implemented: review and approval belong to `/app-spec-review` and the user.

Check: the file exists and all required headings for the rigor are present.

## Phase 4: Section cycle

Required sections by rigor. Use the template's numbered headings (`templates/feature-spec.md`) exactly; the template's own rigor note is the authority:

| Template section | minimal | standard | full |
|---|---|---|---|
| 1 Overview (summary, scope in and out) | required | required | required |
| 2 User stories or jobs | optional | required | required |
| 3 Detailed behavior (main flow and 3.2 rules, where the `REQ-<feature>-NNN` requirements live) | required | required | required |
| 4 States | required, briefly (the states that matter) | required | required |
| 5 Edge cases and failure behavior | a brief list inside 4 or here | required | required |
| 6 Platform variants (one row per platform in `studio.yaml`) | optional | required | required |
| 7 Data and API needs (what, not design; flag changed stored formats) | optional | required or `N/A: reason` | required or `N/A: reason` |
| 8 Permissions and access | optional | required or `N/A: reason` | required or `N/A: reason` |
| 9 Analytics events | optional | required or `N/A: reason` | required, linked to the success measure |
| 10 Accessibility | optional | required | required |
| 11 Localization | optional | required or `N/A: reason` | required |
| 12 Acceptance criteria | required | required | required |
| 13 Configuration and feature flags | optional | required or `N/A: reason` | required (every flag has an exit plan) |
| 14 Dependencies | optional | required | required |
| 15 Open questions | required | required | required |

Performance, privacy and security needs have no section of their own: write them as requirements in section 3.2 (or 5 for failure limits) and list collected data in sections 7 and 8. At `full`, also state rollout and migration impact in sections 13 and 14, and leave room for the traceability from each REQ to stories and tests that `/app-plan` fills in.

For each required section, run this cycle and write the section as soon as it is approved (Edit with the heading in `old_string`):

1. **Question.** Ask what the section needs; read before asking so the questions are about gaps, not facts already known.
2. **Consult** (standard and full, in parallel when sections are independent): brief the agents for this section with the feature, the quoted brief lines, adjacent requirements and the platforms, and ask for proposals. Show disagreements between agents to the user; do not resolve them silently.
3. **Options** where a real choice exists (2 to 4, one marked `(Recommended)` with a one-sentence trade-off).
4. **Draft** the section in the chat. Ask for approval with AskUserQuestion in the same reply. A skipped or empty answer is not an approval.
5. **Write** the approved section; update the checkpoint (orchestration section 9).

Content rules per section:

- **Requirements (section 3.2).** One testable statement each, with an ID `REQ-<feature>-NNN` (three digits, sequential, never renumbered, never reused; a dropped requirement stays in place as `Withdrawn: <reason>`), a priority P0 to P3, and the user or system it concerns. Use plain behavior ("When the user submits an empty form, the system shows ..."), not implementation. Related rules that vary by condition go in a decision table (`business-analyst`).
- **States and edge cases (sections 4 and 5).** Walk the standard list for each flow and write down what happens: empty, loading, partial, success, validation failure, network failure and offline, permission denied or revoked, first run, interrupted (app killed, connection dropped, device rotated or window resized), concurrent edit, large data, slow device, time zone and locale differences, accessibility input (keyboard only, screen reader, reduced motion). Skip an item only with a stated reason ("not applicable: no network use").
- **Platform variants (section 6).** One row per platform in `studio.yaml`: what is different (navigation model, input, permissions prompts, background rules, file handling, notifications, store or distribution constraints) or `same as <platform>`. A platform with no entry is a gap, not an implied "same".
- **Performance, privacy, security and other quality needs (written as requirements in section 3.2).** Numbers carry units, conditions and a measurement method ("first content visible within 2 s on the oldest supported device class, measured by ...") or are marked `no budget set; see /app-perf`. Data the feature collects or stores is listed, so `/app-privacy-review` has a start.
- **Acceptance criteria.** Binary and observable: a person who did not write the spec can answer pass or fail. Format `Given ..., when ..., then ...`, each covering one or more requirement IDs, plus the evidence type from the change types (Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance) so `/app-plan` can pick tests. Every requirement has at least one criterion; every criterion covers at least one requirement. Forbidden without a measurable definition: fast, slow, easy, intuitive, user-friendly, robust, appropriate, as needed, etc., and so on, should work well, seamless, modern. Ranges and limits are written out.
- **Open questions.** One line each: the question, who can answer, what it blocks. Never leave a question inside prose.

If the context window is near its limit, write the current section, update the checkpoint, and tell the user to continue in a fresh session with the same command; the skill resumes from the first placeholder section.

## Phase 5: Self-check and gates

Mechanical checks by the main session (read the file, search it):

1. No section still holds `[To be written]` for a required section.
2. Requirement IDs are unique, sequential, in the spec's feature prefix, and cover the whole list in the criteria table, both directions ("14 of 14 requirements have a criterion; 21 of 21 criteria cover a requirement").
3. No forbidden vague word remains in a requirement or criterion (search the list above).
4. Where section 6 is required, every platform in `studio.yaml` has a row.
5. Every cross-reference to another spec names a real file and, where used, a real ID.
6. Conflicts with other specs: the same capability described twice, or contradictory rules. Show each to the user and ask which spec owns it; record the decision in both documents' Dependencies or Open questions.
7. Nothing in the spec contradicts the brief's out-of-scope list; items that do are flagged.
8. Scan for U+2014 and U+2013.

Then the gates, per review mode:

- `PD-SPEC-ALIGN` (`full` only): spawn `product-director` with the gate ID, the spec path, the pitch and pillars and out-of-scope list from the brief or vision (or `none` if absent), and the requirement list. Tell it to read `gates/pd-spec-align.md` first.
- `TD-FEASIBILITY` (`full` only, when the spec has technical uncertainty): spawn `technical-director` with the gate ID, the spec path, the platforms, the architecture and stack summary (or `none`), and the platform leads' feasibility notes.
- Run both in one message, apply orchestration section 7 (strictest wins), and handle results by the default actions in `gates/README.md`: record each directly under the title as `> **Product Director review (PD-SPEC-ALIGN)**: <ALIGNED | CONCERNS | MISALIGNED | NOT ASSESSED> <date>` (and `> **Technical Director review (TD-FEASIBILITY)**: <VIABLE | CONCERNS | HIGH RISK | NOT ASSESSED> <date>`), ask on CONCERNS (revise, accept and record, or discuss), stop on MISALIGNED or HIGH RISK, and never treat NOT ASSESSED as approval. When a gate is skipped, add no header line and say so in the report.
- If the spec being extended already has stories or code built on it, `TD-CHANGE-IMPACT` (full mode) reviews the added or changed requirements; owner `technical-director`, which reads its own gate file.

Finally, update the checkpoint and tell the user which section the next skills will read first.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Sections | 1, 3, 4, 12, 15 | all of 1 to 15, each filled or `N/A: reason` where the table allows | all 15, plus feasibility and traceability |
| Agents consulted | none (main session) | `product-manager`, `business-analyst`, `ux-designer` (if UI), platform leads | the same, plus `technical-director` for the gate |
| Acceptance criteria | binary at every rigor | binary and typed by change type | binary, typed, with the evidence each will need |
| Gates (set by review mode, not rigor) | solo and lean: none | solo and lean: none | full mode: `PD-SPEC-ALIGN`, plus `TD-FEASIBILITY` for specs with technical uncertainty |

Rigor changes what must exist, never what must work: a criterion that cannot be answered pass or fail is rewritten at every rigor.

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

- **BLOCKED:** the user cannot say what the feature must do after two rounds; the file cannot be written; a gate returned MISALIGNED or HIGH RISK; the retrofit source cannot be read; a required agent proposal is missing after one re-brief and the section depends on it.
- **NOT ASSESSED:** all required sections were written, but a gate that ran returned NOT ASSESSED, or brief alignment could not be assessed (no brief or vision), and the missing input was not supplied. The spec header records it and the verdict line names the missing input.
- **COMPLETE:** all required sections written and approved, the self-check passed, gates as the review mode requires, no NOT ASSESSED left over.

## Report

```
App: <name> (<path>)   Stage: <stage>   Rigor: <rigor>   Review: <mode>
Feature: <name>   Mode: <new | retrofit fill | retrofit convert | retrofit from code>
Spec: <path>   Requirements: <n> (P0 <n>, P1 <n>, P2 <n>, P3 <n>)   Criteria: <n>
Coverage: <n of n requirements have a criterion>; <n of n criteria cover a requirement>
Platforms covered: <n of n>   Open questions: <n>
Conflicts with other specs: <n resolved, n open>
```

```
Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: PD-SPEC-ALIGN: <verdict or skipped: <mode> mode>, TD-FEASIBILITY: <verdict or skipped: <mode> mode>
Wrote: <paths>
Next: /app-spec-review in a fresh session (<why>), then /app-ux or /app-plan
```

## Rules for this skill

- Never write a section the user did not approve, and never present a whole generated spec as finished.
- Never modify existing spec text in a retrofit; fill gaps only, and never renumber an ID.
- Never invent a requirement in convert or from-code mode; unknowns become open questions.
- Never write implementation (frameworks, class names, table schemas) into requirements; that belongs to architecture and stories.
- Never mark a spec approved or advance the stage; `/app-spec-review` and `/app-gate` do that with the user's yes.
- Agents propose; the main session writes.
