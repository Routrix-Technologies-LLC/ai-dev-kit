---
name: app-brief
description: "Write the product brief (one page, minimal rigor) or the product vision with pillars, personas and positioning (standard and full rigor), through a short conversation and sourced research. Use when the user wants to define what the app is for, says 'brief', 'vision', 'pillars', 'who is this for', 'what are we building', or an app has an idea but no written product definition."
argument-hint: "[app] [idea hint or 'open'] [--review solo|lean|full]"
user-invocable: true
---

# App Brief

Turns an idea, a rough pitch or an existing brief into the written product definition every later skill builds from. At `minimal` rigor that is a one-page brief. At `standard` and `full` it is a vision document: problem, users and personas, jobs to be done, pillars (with what each rules out), positioning against real alternatives, scope, success measures and risks. It records the user's decisions; it does not make them.

Writes: `docs/product/brief.md` (template `product-brief.md`) at minimal rigor, or `docs/product/vision.md` (template `product-vision.md`) at standard and full. Paths follow `paths.brief` and `paths.vision` in `studio.yaml` when set.
Next: `/app-stack` (stack undecided), `/app-spec` per MVP feature, `/app-prototype` for the riskiest unknown, then `/app-gate` to leave `discovery`.

## When to use and when not to

- Use after `/app-start` (which writes a first, thin brief), or on any app whose product definition is missing, stale or never written down.
- A specific feature's behavior belongs in `/app-spec`, not here. How a flow looks belongs in `/app-ux`.
- An existing app with no brief: run this in refine mode; the vision describes what the app is meant to be, and anything inferred from the code is labelled as such.

## Inputs

- `studio.yaml` (required, per orchestration section 1; none: offer `/app-start` or `/app-adopt` and stop). Read `app`, `platforms`, `modes.rigor`, `modes.review`.
- An existing brief or vision at the mapped or default path: read it. Mode follows:

| Found | Mode |
|---|---|
| nothing | **new**: write from scratch |
| a brief, rigor is minimal | **refine**: change only the fields the user names, show before and after |
| a brief, rigor is standard or full | **upgrade**: keep every brief field as input, build the vision around it, leave the brief file untouched |
| a vision | **refine**, section by section; never rewrite an approved section without asking |

- Optional: notes, competitor links, user interviews, analytics. Anything the user supplies is read first and quoted in the draft with its source. If there is no evidence for a claim about users, the text says so.
- A missing rigor in `studio.yaml` is asked for, never defaulted.

## Phase 1: Announce and set up

Print the plan block (orchestration section 2). Agents by rigor:

| Agent | Job | minimal | standard | full |
|---|---|---|---|---|
| `product-director` | Pressure-tests pillars, scope and "what it is not" | no | at the pillar step | yes |
| `product-manager` | MVP list, success measures, riskiest assumption | no | yes | yes |
| `domain-researcher` | Sourced facts on comparable products, standards, regulations | only if the user asks | yes | yes |
| `ux-researcher` | Evidence-based personas, jobs to be done, journeys | no | yes | yes |

Gate: `PD-VISION` runs at review mode `full` only (print `PD-VISION skipped: solo mode` or `skipped: lean mode` otherwise). Checkpoint (orchestration section 9) at each phase boundary.

## Phase 2: Understand the idea (main session, plain-text questions)

Ask only what is not already answered; a few at a time.

1. One sentence: what is it, and who is it for? If the user has no idea, offer two or three one-line directions (a different user and problem each) and let them choose, combine or discard.
2. The problem: what do those people do today, what does it cost them, how do you know?
3. The single most important thing a user does repeatedly (the core job).
4. What the first version must do (three to seven items). More than seven: push back, propose cuts, move cuts to out of scope.
5. What is deliberately not being built.
6. How will you know it worked (a measurable outcome, even a small one)?
7. The riskiest assumption: what, if false, kills the idea?
8. Constraints: time, money, data sensitivity, legal or store rules, people, and the platforms from `studio.yaml` (ask whether the platform list is still right).

Restate the answers in a short summary and ask whether it is right before research starts.

## Phase 3: Research (standard and full; skipped, announced, at minimal)

Spawn in parallel, per orchestration sections 3 and 4. Each writes one file in `~/AgentScratch/app-brief-<app>/` (scratch, not the repo; the main session carries what survives into the document with its sources).

- `domain-researcher`: three to six comparable or competing products and the manual or workaround alternatives people use now (what each does, who it serves, pricing model, platform support, evidence of weaknesses), the standards or regulations that touch this kind of app, and what real users complain about. Every fact carries a source and an access date. Facts it cannot source are listed as "not found", never filled in.
- `ux-researcher`: provisional personas and jobs to be done derived from the user's answers and any supplied evidence. Without real user data, personas are marked `Hypothesis, not validated` and the file proposes the cheapest way to validate each (interview questions, a survey, a prototype test). It never invents quotes, statistics or interview results.
- At `full`, also `product-manager`: a first success-metric set (outcome, leading indicator, guardrail) and a scope sanity check against the stated time and people.

Check: each file exists with sourced content. If an agent returned without its file, re-brief once; a second failure leaves that section marked `NOT RESEARCHED` and the final verdict reflects it (see Verdicts).

Optional at `full`: if the idea depends on a capability that may not be buildable (a device sensor, a model's accuracy, a platform API), ask whether to run `TD-FEASIBILITY` (`technical-director`, full mode only) on the brief before drafting the scope; the gate reads its own file.

## Phase 4: Draft section by section

Create the skeleton file after one ask ("May I create `<path>` with section headings?"), then write each section as soon as the user approves it, using Edit with the heading in `old_string` so a crash or compaction loses nothing. For each section: question, 2 to 3 options where there is a real choice, draft, approval. A section is not written without a yes. Agents return proposals in their reply; they do not write the document.

**minimal: the brief.** Use the template's fields: working name, one-line pitch, problem and who has it, primary user, core job, MVP (7 or fewer, each later becomes a story), out of scope, success measure, riskiest assumption, build order (riskiest first), platforms and constraints, closest comparable and what the MVP keeps from it. Fill several fields per exchange. Show the whole brief once, then ask to write.

**standard and full: the vision.** Sections, in order:

1. Vision statement: one or two sentences someone outside could repeat.
2. Problem and evidence: the problem, who has it, what they do today, evidence with sources or `no evidence yet`.
3. Users and personas: one primary persona, at most two others, each with context, goals, frustrations and a validation status.
4. Jobs to be done: the jobs the product is hired for, in "When ... I want to ... so I can ..." form.
5. Pillars: three to five. Each has a name, a one-sentence meaning, and **what it rules out** ("we will not ..."). A pillar that rules nothing out is not a pillar. `product-director` pressure-tests them at `standard` and `full`.
6. Positioning: against the researched alternatives (a small table: alternative, what it does well, where this app is different, and why that matters to the primary persona). No unsourced claims.
7. Core experience: the loop or flow the user repeats, in four to six steps.
8. Scope: MVP list (7 or fewer), later, and never (the anti-goals). Cut items move to later or never, visibly.
9. Success measures: outcome, leading indicators, guardrails (what must not get worse), and how each is measured. `analytics-specialist` is not spawned here; instrumentation is designed later.
10. Platforms and constraints: from `studio.yaml`, plus distribution (stores, installers, hosting), regulations, data sensitivity.
11. Risks and assumptions: ranked; the riskiest first with a cheap test (often `/app-prototype`). Optionally seed `planning/risks.md`; ask first.
12. Open questions, with an owner each. Never bury a question in prose.

In upgrade mode, the brief's wording is reused where the user still agrees; changed fields are shown before and after.

Check after each write: the section is present in the file with real content and the file still parses as markdown with its headings in order.

## Phase 5: Gate and finish

1. Self-check by the main session: every MVP item traces to the core job or a pillar; nothing in out-of-scope also appears in the MVP; every persona claim has a source or the `Hypothesis` label; platforms match `studio.yaml`; no section is placeholder text; scan for U+2014 and U+2013.
2. `PD-VISION` (full review mode only): spawn `product-director` with the gate ID and the document path, the pitch, the primary persona, the pillars with what each rules out, the MVP and out-of-scope lists, and the platforms. Tell it to read `gates/pd-vision.md` first. Apply orchestration section 7. Handle the result:

| Gate verdict | Action |
|---|---|
| APPROVE | record directly under the title: `> **Product Director review (PD-VISION)**: APPROVE <date>` |
| CONCERNS | ask: revise flagged items / accept and proceed / discuss; record `CONCERNS <date>` in the same line form and list accepted concerns under Open questions |
| REJECT | show the blockers; do not mark the document ready; verdict BLOCKED |
| NOT ASSESSED | record `> **Product Director review (PD-VISION)**: NOT ASSESSED <date>` and name the missing input beside it; never treat it as approval |

3. If `app.summary` in `studio.yaml` is empty or older than the pitch, offer to update it as part of one grouped ask; edit only that line.
4. Update the checkpoint. Tell the user the document is a draft until they say it is accepted; `/app-gate` checks `discovery` exit later.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Document | one-page brief | vision | vision plus validation plan for each persona and the riskiest assumption |
| Research | none (optional on request) | comparables and personas | adds regulations, standards and success metrics review |
| Pillars | not required | 3 to 5 with exclusions | same, pressure-tested by `product-director` |
| Gate PD-VISION (set by review mode, not rigor) | solo: skipped | lean: skipped | full: runs |

Rigor changes what must exist, never what must work: at every rigor the MVP list is 7 or fewer and every item is something a user can do.

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

- **BLOCKED:** the user cannot or will not name who the app is for and what problem it solves after two rounds of questions (the brief would be fiction); no `studio.yaml` and the user declines `/app-start`; the file cannot be written; `PD-VISION` returned REJECT.
- **NOT ASSESSED:** the document is written, but `PD-VISION` returned NOT ASSESSED and the missing input was not supplied, or a section the document relies on is marked `NOT RESEARCHED` after the retry and the user did not accept that. The line names which.
- **COMPLETE:** the document is written and read back and no NOT ASSESSED remains. The closing line still names every section marked `NOT RESEARCHED` that the user accepted and every persona marked `Hypothesis`.

## Report

```
App: <name> (<path>)   Stage: <stage>   Rigor: <rigor>   Review: <mode>
Mode: <new | refine | upgrade>   Document: <path>
Pitch: <one line>
Pillars: <list or n/a>   MVP items: <n>   Out of scope: <n>
Research: <done | partial | not run (<why>)>   Personas: <n validated, n hypothesis>
Open questions: <n> (listed in the document)
```

```
Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: PD-VISION: <verdict> | none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never invent users, quotes, statistics, market sizes or competitor facts. Unsourced means labelled as such or left out.
- Never write a section without the user's approval of it; never present a full draft as a finished decision.
- Never edit an approved section silently on a later run; show before and after.
- Never exceed seven MVP items without the user explicitly choosing to, and then record that choice.
- Never advance the stage; `/app-gate` does that after the user's yes.
- Stay platform-neutral: the brief says what and for whom, not which framework.
