---
name: app-ux-review
description: "Review the implemented UI against its UX spec, the design language and usability heuristics, from screenshots and observed behavior rather than from code. Use when the user asks for a UX review, design review, visual QA, usability check of a built screen or flow, or wants to know whether the UI matches the spec."
argument-hint: "[app] [screen | flow | all] [--review solo|lean|full]"
user-invocable: true
---

# App UX review

Reviews what a user would see and do in the built app. Evidence comes first: screenshots of each state, captured without stealing focus, and recorded interaction steps. Every finding cites an image or a step and the spec requirement, design-language rule or heuristic it breaks. Opinions without evidence are labelled as such.

Writes: `docs/design/reviews/<date>-<scope>.md`. Evidence in `docs/qa/evidence/ux-<date>-<scope>/`. Per-reviewer notes in `docs/design/reviews/<date>-<scope>/<agent>.md`.
Next: `/app-team-ui` or `/app-dev-story` for fixes, `/app-ux` if the spec itself is wrong, `/app-design-language` if a token or component rule is missing, `/app-a11y-audit` for conformance, `/app-gate` reads the result.

## When to use and when not to

Use after a screen or flow is implemented, before sign-off of a UI or Visual story, and before hardening. Not for: reviewing a UX spec document before build (`/app-spec-review` or `/app-ux`), a conformance audit (`/app-a11y-audit`), measuring speed (`/app-perf`), or a code review (`/app-code-review`).

## Inputs

- `studio.yaml` (required): `platforms`, `stack`, `commands` (`run`, `screenshot`, `e2e`). Stop and offer `/app-adopt` or `/app-start` if absent.
- Scope: a screen, a flow, or `all`. No argument: ask which.
- The standards the review compares against, each recorded FOUND or ABSENT:
  - the UX spec: `docs/design/ux/<flow>.md`
  - the design language: `docs/design/design-language.md`
  - the feature specs and acceptance criteria that cover the scope: `docs/product/specs/`
  - platform conventions for each platform in `platforms` (Apple Human Interface Guidelines, Fluent 2 for Windows, Material 3 for Android, GNOME or KDE human interface guidelines for Linux, web patterns), checked from current vendor guidance, not memory
- A runnable app, or captured screenshots the user supplies. With neither, the verdict is NOT ASSESSED.

An absent UX spec or design language does not stop the review but makes the dimension that needs it NOT ASSESSED (below). Offer `/app-ux` or `/app-design-language` as the producing skill.

## Phase 1: Scope and plan

Main session. List the screens, states and variants in scope from the UX spec or, if absent, from running the app. States to cover for each screen where they exist: default, empty, loading, error, partial or long content, disabled, success; window sizes or viewports and form factors the platform supports; light and dark; text scaling; at least one non-English or long-string case when localization exists.

Announce the plan per `orchestration.md` section 2. Agents: `ux-researcher` (heuristic evaluation and task walk-throughs), `design-director` (design-language and visual quality), `accessibility-specialist` (a quick accessibility glance, not an audit), `content-designer` (copy, tone, error and empty states). Platform-specific specialists are not needed for the review itself.

Gates: `DD-VISUAL` runs at `full` only (`gates/README.md` lean mode does not include it); `solo` prints `DD-VISUAL skipped: solo mode` and `lean` prints `DD-VISUAL skipped: lean mode`. A user who wants the gate at lean reruns with `--review full`.

Check: a screen-state matrix is written to the working notes with every cell marked TO CAPTURE.

## Phase 2: Capture evidence

Main session, or `test-automation-engineer` when the app needs scripted navigation to reach states (name the screens and the driver, the agent writes only under the evidence folder). Run and observe per `orchestration.md` section 10, without stealing focus: headless browser for web and extension, offscreen window capture for desktop, simulator or emulator screenshot for mobile, rendered output for CLI. Use `commands.screenshot` when set. Do not close or interfere with the user's running copy of the app; use a separate build or instance.

For each cell in the matrix save a small PNG (a few hundred KB) named `<screen>-<state>-<variant>.png` and record a one-line step list for flows (what was clicked or typed, what appeared). Navigation is driven only through a headless browser, simulator, emulator or offscreen harness; never inject keyboard or mouse input into the user's real desktop. Then view the images; capturing is not looking.

A cell that could not be captured stays NOT CAPTURED with the reason (state cannot be reached, device unavailable). It is never filled by imagining it. The report ends with `Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why> | N/A - <why>` per section 10.

Check: evidence files exist and open; the matrix shows captured, not captured, and the denominator ("27 of 31 cells captured").

## Phase 3: Review in parallel

Spawn the reviewers in one message per orchestration section 4, each writing its own file under `docs/design/reviews/<date>-<scope>/`. Brief per section 3 with the matrix and evidence paths, the quoted spec requirements and design-language rules that apply, and the lens:

| Agent | Lens | Compares against |
|---|---|---|
| `ux-researcher` | Nielsen's ten usability heuristics (visibility of system status, match with the real world, user control and freedom, consistency and standards, error prevention, recognition over recall, flexibility and efficiency, aesthetic and minimalist design, error recovery, help), task walk-throughs for the top user goals, cognitive load, platform convention fit | heuristics, the UX spec's flows, platform guidelines |
| `design-director` | token use (color, type, spacing, radius, elevation), component fidelity, hierarchy and alignment, theme and density consistency, motion, per-platform adaptation, overall quality bar | the design language and UX spec |
| `accessibility-specialist` | quick glance: visible focus, contrast spot checks, target sizes, text scaling behavior, color-only meaning, motion; points to `/app-a11y-audit` for conformance | design language accessibility rules, platform norms |
| `content-designer` | clarity and tone of labels, errors, empty states and confirmations, terminology consistency, truncation and expansion risks | the UX spec copy, voice and tone guidance |

Rules for every reviewer: cite the evidence file (and region) or step for each finding; separate OBSERVED (what the image shows) from INTERPRETATION (why it matters); cite the spec requirement ID or design rule, or the heuristic, being violated; propose a specific fix; rate CRITICAL, HIGH, MEDIUM or LOW per `standards/severity.md` (CRITICAL: a core task cannot be completed or the screen contradicts the spec's core intent; HIGH: a significant usability or fidelity defect on a common path; MEDIUM: noticeable but workable; LOW: polish). Do not review what was NOT CAPTURED. A dimension with nothing to compare against is reported as NOT ASSESSED, not as a pass.

Return contract appended verbatim. Check: each reviewer file exists, cites evidence, and states what it could not assess.

## Phase 4: Verify and consolidate

Main session. Look at the evidence for every CRITICAL and HIGH finding yourself and confirm the claim. Check each cited spec requirement exists in the quoted file. Merge duplicates across reviewers, keeping the clearest evidence. Where a reviewer finds a defect that the spec itself requires, mark it SPEC ISSUE and route to `/app-ux` rather than the builder. Where reviewers disagree (design-director wants density, accessibility wants larger targets), present both and let the user decide; do not choose silently.

Run `DD-VISUAL` when the mode includes it: spawn `design-director` with the gate ID, the finding summary and evidence paths; the agent reads `gates/dd-visual.md` itself. Record the outcome as the first line under the report's title (`> **Design Director review (DD-VISUAL)**: <VERDICT> <date>`).

Write `docs/design/reviews/<date>-<scope>.md`: scope, standards used (FOUND/ABSENT), matrix with captured counts, findings table (ID `UX-NNN`, severity, screen and state, evidence, rule violated, fix, owner), dimensions NOT ASSESSED, and the verdict. Ask the user which findings to fix now, defer, or reject; record rejected ones with their reason. Do not edit the UI here.

Check: the report file exists, every finding has evidence and a cited rule, and rejected findings carry a reason.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Evidence | default state and top error or empty state per screen, primary platform | all states, light and dark, primary breakpoints or sizes | all states, all variants and devices, scaling and long-string cases |
| Lenses | `ux-researcher` and `design-director` | all four | all four, plus task walk-throughs with timing notes |

Rigor changes how much is looked at, not whether a seen defect counts. `DD-VISUAL` runs per Phase 1; it is not run at solo.

## Verdicts

First match wins:

1. **MAJOR REVISION**: any open CRITICAL finding, or `DD-VISUAL` returned REJECT.
2. **NEEDS REVISION**: any open HIGH or MEDIUM finding, or `DD-VISUAL` returned CONCERNS.
3. **NOT ASSESSED**: no failures (a `DD-VISUAL` NOT ASSESSED lands here too), but the app could not be run and no screenshots exist, the capture matrix is incomplete for cells the scope requires, or a dimension has no standard to compare against (UX spec absent, design language absent). Name each and the skill or input that closes it.
4. **APPROVED**: evidence captured for the whole scope, every dimension assessed, only LOW findings (listed) remain.

An absent standard never defaults to a pass: "matches the design language" cannot be said when there is none.

## Report

```
UX review: <app> (<scope>)   Date: <date>
Standards: UX spec <path|ABSENT>  Design language <path|ABSENT>  Specs <paths|ABSENT>  Platform guidance <named>
Evidence: <captured>/<total> cells   Run result: OBSERVED - ... | NOT VERIFIED - ... 
Findings: CRITICAL <n>  HIGH <n>  MEDIUM <n>  LOW <n>  (spec issues <n>)
Dimensions not assessed: <list with reason> | none
Top findings: UX-NNN <title> (<severity>, <screen/state>) x up to 5
Decisions for you: <fix/defer/reject; spec conflicts> | none
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Never review from code or the spec alone; a finding about appearance or behavior needs captured evidence or a recorded step.
- Never fill an uncaptured state with an assumption; it stays NOT CAPTURED.
- Never capture in a way that steals focus or touches the user's own running instance.
- Never report "matches the design language" without the design language, or "matches the spec" without the spec.
- Never edit UI code, the spec or the design language here; findings route to their owners.
- Never choose between conflicting reviewer recommendations on the user's behalf.
- Keep screenshots small and never include real personal data; use test data.
