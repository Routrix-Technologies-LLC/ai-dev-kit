---
name: app-ux
description: "Author a UX spec for one flow or screen group: purpose, navigation, layout, every state, every platform variant and input mode, copy, accessibility, events and testable acceptance criteria. Use when the user wants to design how a feature looks and behaves screen by screen, says 'UX spec', 'wireframe this flow', 'what states does this screen have', or a feature spec needs its experience pinned down before architecture or build."
argument-hint: "[app] <flow-or-screen-group> [--review solo|lean|full]"
user-invocable: true
---

# App UX

Produces the UX spec for one flow or screen group, written section by section with the user, covering the happy path and everything around it: every state, every supported platform and window or screen size, every input mode, the words on screen, and the accessibility behaviour. The spec says what the interface must do and what it needs; it does not choose frameworks or data delivery (that is `/app-architecture`).

Writes: `docs/design/ux/<flow>.md` (template `templates/ux-spec.md`), `.studio/state.md` checkpoint.
Next: `/app-ux-review` after build, `/app-ux <next-flow>`, `/app-architecture` (data needs and events feed it), `/app-plan` (acceptance criteria become story criteria).

## When to use and when not to

- Use for a flow (onboarding, checkout, sync conflict) or a group of screens that share navigation (settings, an inspector).
- A look-and-feel question across the whole product is `/app-design-language`. A requirement that is not yet decided is `/app-spec` first. Reviewing UI that is already built against a spec is `/app-ux-review`. A CLI or an API has no screens: for a CLI this skill specs commands, prompts, output and exit codes (see the platform table); for an API use `/app-api`.

## Inputs

| Input | If missing |
|---|---|
| `studio.yaml` | Stop; offer `/app-adopt` or `/app-start` (`orchestration.md` section 1). |
| The feature spec(s) the flow serves (`docs/product/specs/`) | Ask which requirement IDs the flow covers. With none, proceed only if the user states the purpose in their words, and record "no governing spec" in Open Questions. |
| Brief or vision (personas, platforms) | Ask who the user is and in what situation. Record the answer; never invent a persona. |
| Design language (`docs/design/design-language.md`) | Not blocking. Component and token references become `NOT ASSESSED - no design language`; offer `/app-design-language`. |
| Existing UX specs and, for an adopted app, existing UI code | Read the specs for navigation consistency; for code, list the screens that already exist so the spec matches or consciously changes them. |
| Accessibility baseline | If the app has none, the baseline for this spec is WCAG 2.2 AA plus the platform's accessibility API; record that as the assumed baseline. |

## Phase 1: Resolve, announce, gather

Main session. Resolve the app and print the plan block (`orchestration.md` sections 1 and 2). Pick agents from `studio.yaml` `platforms`: `ux-designer` always; `content-designer`, `accessibility-specialist` and `ui-designer` for the specialist pass; the platform lead (`web-lead`, `desktop-lead`, `mobile-lead`) for feasibility questions only.

1. Read the governing specs, brief or vision, existing UX specs, the design language if present, and `studio.yaml`. If `.studio/state.md` shows an unfinished run for this flow, offer to resume (sections with real content are done).
2. If `docs/design/ux/<flow>.md` exists, ask: continue and fill missing sections (retrofit; existing content is never edited), or start a new flow name. Never overwrite.
3. Build the variant plan from `studio.yaml` `platforms`, using the routing table below, and show it to the user before drafting. This table drives sections 4 to 6 of the spec.

Check: the variant plan lists every platform in `studio.yaml` with its variants or an explicit "not applicable: <why>".

### Platform routing

| Platform | Variants the spec must cover | Input modes | Extra sections |
|---|---|---|---|
| web | Breakpoints (name the widths where the layout changes, from the design language or proposed), orientation, zoom to 200 percent and reflow, reduced motion, light and dark | Mouse, keyboard, touch, screen reader | Browser support from `min_targets`, deep links and back button, loading and offline behaviour |
| windows, macos, linux | Minimum, default and maximized window sizes, multi-window and multi-monitor, DPI and scaling, light, dark and high contrast, full screen | Mouse, keyboard with shortcuts, touch or pen where relevant, screen reader | Menu bar or command surface, tray or dock presence, window state restore, drag and drop, OS integration touch points |
| ios, android | Phone and tablet, orientation, safe areas and notches, text scaling, split screen or multitasking, light and dark | Touch gestures, system back, hardware keyboard, switch and voice control, screen reader | Permission prompts and their denied states, interruptions (call, background, low power), notifications entry, platform navigation idioms |
| cli | No layout: commands, arguments, prompts, output, exit codes, color off, narrow terminal | Keyboard, piped input and output | Help text, error text, non-interactive mode, progress for long runs |
| extension | Popup, side panel, options page, content-script UI | Mouse, keyboard | Permission explanation, host page conflicts |
| backend, library | Not a UX spec subject; state "not applicable" and route to `/app-api` | none | none |

Read `references/states-and-variants.md` now for the state catalog and per-platform checklists. Read it again if the conversation was compacted during Phases 2 or 3.

## Phase 2: Skeleton and options draft

1. Spawn `ux-designer` (one call, brief per `orchestration.md` section 3) with the purpose, governing requirement IDs, variant plan, personas and existing navigation. Output: `~/AgentScratch/app-ux-<flow>/ux-designer.md` containing, for sections 2 to 4 of the template, two or three options with the trade-off of each (information hierarchy, zone arrangements, navigation placement). Agents propose; the user decides.
2. Ask once (`orchestration.md` section 6): create the skeleton at `docs/design/ux/<flow>.md` from `templates/ux-spec.md`, every template section present with `[To be designed]`. List the path. Write it.

Check: the file exists and every section heading from the template is present.

## Phase 3: Section by section

Main session, with the user. For each section in order: show the evidence it rests on (requirement IDs, persona, existing screens), present the options, record the decision, draft, get approval, write that section immediately, and update the checkpoint. Ask per section for choices only; do not ask permission to write a section the user just approved.

Use the template's headings exactly (`templates/ux-spec.md`; its header line carries Status `In design`, Author, Last updated, Feature specs, Pillars served, Platforms, Design language path and the accessibility target).

| # | Template section | What it must contain |
|---|---|---|
| 1 | Purpose and user context | User goal, system goal and arrival context: where from, what they were doing, state (calm, rushed, stressed, one-handed, bad connection), first-time or returning; the requirement IDs served; design for the worst plausible arrival |
| 2 | Information architecture and navigation | Where the flow sits; every entry (link, notification, deep link, shortcut, restore after relaunch) and every exit, including one-way exits, back behavior and unsaved-change handling; each screen named once |
| 3 | Flows | One numbered flow per user goal, happy path first, then each alternate, failure and interrupted path as a branch with its own number; each step has user action, system response and resulting screen and state |
| 4 | Screens | One block per screen: purpose, layout and hierarchy by region in priority order, content and data shown, primary and secondary actions, components used (each marked existing pattern or new), and the state table from the catalog with a row per state or `N/A: <why>`, never a blank or an omission |
| 5 | Platform variants and breakpoints | One row per entry of the variant plan: layout, navigation and notable differences at each breakpoint, window size, orientation or text scale, and what is identical |
| 6 | Input methods | Per action and per input mode: pointer or touch, keyboard (shortcuts, tab order, focus start and return), other (voice, switch, gesture alternative), immediate feedback and outcome, hit-target sizes |
| 7 | Copy | Every string with a key, context, text and notes (variables, plurals, length limits); error and empty-state copy; terminology; longest strings and expansion risk (assume 30 to 40 percent), dates, numbers and RTL mirroring points |
| 8 | Accessibility notes | Per screen: focus order, names, roles and states, announcements for async changes, focus management for dialogs and route changes, contrast pairs by token, non-color cues, zoom and text scaling, reduced motion, platform accessibility API notes |
| 9 | Motion and feedback | What moves and why, duration and easing as design-language motion tokens, the reduced-motion version, haptics or sound, and progress feedback with thresholds (feedback under about 100 ms, a spinner after about 1 s, determinate progress for longer waits); loading indicators and optimistic updates; offline behavior |
| 10 | Open questions and risks | Anything unresolved with an owner and a needed-by date. Also here: analytics events or data the flow needs that its feature spec does not list (the feature spec owns events and data; name what `/app-spec` must add), and anything that changes persistent state (flag for `/app-architecture`) |
| Acceptance | Acceptance | The REQ IDs the spec satisfies and at least five binary checks a tester can run without other documents: one for performance or perceived speed, one navigation, one error or empty state, one accessibility, one for the core purpose; each names the platform or size it applies to |

Rules inside this phase:

- A conflict between a requirement and the available space or platform convention is surfaced with options. A requirement is never dropped silently and the layout is never expanded silently.
- Layout and visual taste decisions are the user's; present options, do not pick "the standard one".
- Do not contradict an approved UX spec without flagging the conflict.
- State tables and the variants table are never summarized as "same as default". If a state or variant is identical, say that in a row.

Check: no section still reads `[To be designed]`, and every screen's state table and section 5 have a row for every state in the catalog and every variant in the plan.

## Phase 4: Specialist pass (parallel)

Issue all three in one message (`orchestration.md` section 4), each reading the spec on disk. Each writes one file under `~/AgentScratch/app-ux-<flow>/`.

| Agent | Job | Output |
|---|---|---|
| `content-designer` | Review sections 4 (state copy) and 7: voice and tone, error message quality (what happened, why, what to do), empty states, terminology consistency, string keys, length limits | `content-designer.md`: proposed edits as a table (string key, current, proposed, reason) |
| `accessibility-specialist` | Review sections 2, 3, 5, 6, 8 and 9 against WCAG 2.2 AA and the accessibility API of each platform in the variant plan: focus order, names and roles, targets, contrast, reflow, motion, error identification | `accessibility-specialist.md`: findings with severity (CRITICAL to LOW) and the section they apply to |
| `ui-designer` | Check the component inventory against the design language: tokens for each state, missing components, density at each size, dark and high-contrast treatment. With no design language, list the decisions it will need and report NOT ASSESSED | `ui-designer.md`: gaps and proposed component specs |

The main session reads the three files, verifies any finding the verdict turns on by re-reading the spec section it cites (label unchecked claims `UNVERIFIED`), then presents the edits to the user grouped by section. Approved edits are written to the spec; rejected ones are listed under Open Questions with the reason. A CRITICAL or HIGH accessibility finding the user declines to fix is recorded in the spec as an accepted risk with the date.

Check: all three files exist with content; every CRITICAL and HIGH finding has a recorded outcome.

## Phase 5: Cross-reference check

Main session, no agents. Print the result as a block:

```
Cross-reference: <flow>
Requirements covered: <N of M> (<IDs uncovered>)
New patterns not in the design language: <list or none>
Navigation mismatches with other specs: <list or none>
States without copy: <list or none>
Variants without acceptance criteria: <list or none>
Data written that changes persistent state: <list or none>
```

Counts always show their denominator. A line that could not be computed (no specs to compare, no governing spec) says `NOT ASSESSED - <why>`, never "none". Do not edit other specs; name the ones that should link here.

## Phase 6: Gate

Gate `DD-UX-SPEC`, owner `design-director`. It runs in `full` review mode only (it is not a phase gate or always-on): `solo` prints `DD-UX-SPEC skipped: solo mode` and `lean` prints `DD-UX-SPEC skipped: lean mode`. In `full`, spawn `design-director` with the gate ID, the spec path, the feature spec path, the design language path, the variant plan, the cross-reference block and the accessibility findings with their outcomes; it reads its own gate file. Record the result directly under the title as `> **Design Director review (DD-UX-SPEC)**: <APPROVE | CONCERNS | NOT ASSESSED> <date>` (no line when skipped). CONCERNS: ask to revise, accept (recorded) or discuss. REJECT: do not call the spec complete; revise and re-run. NOT ASSESSED: name the missing input (the UX spec or the feature spec); never treat it as approval.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Spec required | Optional; key flows only if the user wants one | Core flows | Every flow |
| Sections | 1, 3, 4 (every state listed) and Acceptance | All of 1 to 10 and Acceptance | All, plus annotated captures or wireframes per variant, completed motion and input tables, and copy stress-tested with pseudo-localized strings |
| Variants | Primary platform only | Every platform in `studio.yaml` | Every platform, every breakpoint or window size, high contrast |
| Specialist pass | accessibility-specialist only | All three | All three, re-run after edits |
| Gate DD-UX-SPEC (set by review mode, not rigor) | solo and lean: skipped | solo and lean: skipped | full mode: runs |

Rigor changes what must exist, never what must be true: a section that exists must be real.

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

- BLOCKED: no governing purpose can be established, the user declined a required decision twice, a specialist artifact is missing after one re-brief, or `DD-UX-SPEC` returned REJECT.
- NOT ASSESSED: the spec is written, but `DD-UX-SPEC` returned NOT ASSESSED and the input was not supplied, or the spec could not be checked against the governing feature spec (none exists) or the design language (none exists) and the user chose to proceed. The verdict line names what was not assessed; downstream gates that need that item treat it as missing.
- COMPLETE: every section required at this rigor is written and approved, Phase 4 outcomes are recorded and nothing above applied.

## Report

```
UX spec: <flow> (<path>)
Rigor: <rigor>   Sections: <N of M written>   States: <N rows>   Variants: <N of N>
Specialist pass: <accessibility: N findings (CRITICAL a, HIGH b), copy: N edits, ui: N gaps>
Accepted risks: <list or none>
Cross-reference: <summary line>
Open questions: <N>

Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: <DD-UX-SPEC: VERDICT> | none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never write a section the user has not approved; never present a fully generated spec as finished.
- Never leave a state or variant blank; use "N/A: <why>" or a row.
- Never write outside `docs/design/ux/` (and scratch). Never edit another spec or the design language.
- Never invent personas, research or analytics. Mark unsupported statements as assumptions.
- Never pick layout or taste decisions for the user.
- A skipped specialist, gate or comparison is named in the report, not omitted.
