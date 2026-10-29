---
name: app-a11y-audit
description: "Accessibility audit of an app against WCAG 2.2 AA and the platform's accessibility API, combining automated tools with a manual checklist per platform and stating plainly what an agent cannot test. Use when the user asks for an accessibility audit, a11y check, screen reader or keyboard review, WCAG conformance, contrast or text scaling checks, or before a release."
argument-hint: "[app] [full | <flow or screen> | <platform>] [--review solo|lean|full]"
user-invocable: true
---

# App accessibility audit

Audits the implemented app, not the spec. Automated tools find a minority of problems; the manual checklist finds the rest; and some checks need a person using real assistive technology, which an agent cannot do. The report keeps those three apart so a green automated scan is never read as conformance.

Writes: `docs/qa/a11y-<date>.md` from template `accessibility-audit.md`. Evidence in `docs/qa/evidence/a11y-<date>/`.
Next: `/app-bugfix` or `/app-plan` for failures; `/app-ux` if a failure needs a design change; a human screen reader pass (below); `/app-gate` or `/app-release` consume the result.

## When to use and when not to

Use on built UI, before hardening or release, after a UI change that touches navigation, forms, color or motion, or when a user reports a barrier. Not for: reviewing a UX spec before build (`/app-ux` and its accessibility notes), a look-and-feel review (`/app-ux-review`, which includes a light accessibility glance only), or a CLI or API with no UI beyond text (still in scope, see the CLI row; a pure backend with no user-facing surface is N/A and the report says so).

## Inputs

- `studio.yaml` (required): `platforms`, `stack`, `commands` (`run`, `screenshot`, `e2e`). Stop and offer `/app-adopt` or `/app-start` if absent.
- A runnable app. If it cannot be launched, the automated and manual-by-agent layers are NOT ASSESSED, and the report is only a static review of markup or code, labelled as such.
- Optional: `docs/design/ux/<flow>.md` (accessibility notes, expected focus order and announcements), `docs/design/design-language.md` (contrast and scaling rules), a prior `docs/qa/a11y-*.md`.
- The target conformance level. Default WCAG 2.2 level AA plus the platform's own accessibility guidance. If the app or the user states a different commitment (a stricter level, a procurement standard), use that and record it. If nothing is stated and the user cannot say, audit to AA and say it was assumed.

## Phase 1: Scope and plan

Main session. List the screens and flows in scope: the core journeys from the brief and specs, plus sign-in, settings, error and empty states, onboarding, dialogs and notifications. For each platform in `platforms`, choose the tools and checklist rows from the routing table. Announce the plan per `orchestration.md` section 2. Agents: `accessibility-specialist` (the audit), `ux-designer` (consulted on findings that need a flow or layout change, and on expected focus order). A platform specialist from `studio.yaml` may be spawned to run the app or tool correctly when the accessibility-specialist cannot.

| Platform | Automated layer | Manual layer (agent can do) | Needs a person |
|---|---|---|---|
| web | axe-class rule engine and Lighthouse-class audit through a headless browser on each route and state; HTML validity and landmark checks | keyboard-only walk with Tab, Shift+Tab, Enter, Space, arrows, Esc; focus visibility and order; accessibility tree dump for names, roles, states; 200% zoom and 400% reflow at 320 CSS px; text spacing override; forced-colors and dark mode; reduced-motion emulation; contrast computed from rendered colors | screen reader use (NVDA or JAWS on Windows, VoiceOver on Mac and iOS, Orca on Linux) on the real flows; voice control; switch access |
| windows | Accessibility Insights-class scan; UI Automation tree dump of every screen | keyboard-only walk; focus order; name, role, value and states from the UIA tree; 200% scale and larger text setting; high contrast themes; reduced animation setting; Narrator-readable names inferred from the tree | Narrator or NVDA on real flows; voice access; switch |
| macos | Accessibility Inspector audit; AX tree dump | keyboard-only including Full Keyboard Access; focus ring; labels from AX attributes; increased contrast, reduce motion, reduce transparency settings; larger text where supported | VoiceOver on real flows; voice control |
| linux | AT-SPI tree dump (Accerciser-class); toolkit inspector | keyboard-only; focus order; names and roles from AT-SPI; high contrast and scale settings | Orca on real flows |
| ios | Accessibility Inspector audit on the simulator; XCUITest accessibility audit if present | traits, labels, hints, and order from the hierarchy; Dynamic Type at the largest sizes including accessibility sizes; Bold Text; Reduce Motion; Increase Contrast; touch target sizes; orientation | VoiceOver, Voice Control and Switch Control on a real device |
| android | Accessibility Scanner-class checks; Espresso accessibility checks if present; layout inspector | content descriptions, roles and state from the hierarchy; font and display size at largest; touch target sizes; reduce animations; high contrast text; focus order with a keyboard | TalkBack, Voice Access and Switch Access on a real device |
| cli | output review | no color-only meaning; honors `NO_COLOR` and non-TTY; no spinner or progress spam in plain output; errors say what to do; usable in a screen reader terminal because output is linear text | a screen reader user's terminal session |
| extension | as web, on popup, options and injected UI | as web, plus the extension does not break the page's own accessibility | as web |

**Input rule.** Keyboard and pointer walks run only where the tool drives its own input: a headless or automated browser, a simulator or emulator, or an offscreen test harness. On the real desktop, never run UI automation that injects keyboard or mouse input (it has typed into the user's own windows): read the accessibility tree and focus order from the tree or the code instead, mark the walk-through criteria NOT TESTED, and put the walk in the human test script, unless the brief says the user is away from the computer.

The criteria spine is WCAG 2.2 (A and AA), applied through the platform's guidance rather than only the web wording: name, role, value; keyboard operable and no trap; visible and non-obscured focus; target size; consistent help and no redundant entry; accessible authentication; contrast for text and non-text; text resize and reflow; motion and flashing; error identification and suggestion; status messages announced; orientation and input purpose. Tell the agent to cite the criterion it fails and to check the current guidance rather than quote clause numbers from memory.

Check: a screen/flow list and a per-platform tool list are written to the working notes before spawning.

## Phase 2: Run the layers

Spawn `accessibility-specialist` (one per platform when the app ships on several unrelated UI stacks; they run in parallel, each writing its own file) per orchestration sections 3 and 4:

- Output: `docs/qa/evidence/a11y-<date>/<platform>-notes.md` plus raw tool output and screenshots.
- Brief with: the screens and flows, the target level, the routing row, and the expected focus order and announcements from the UX specs.
- Rules: capture without stealing focus (section 10); record each automated tool's name, version and rule set in the notes; mark each criterion PASS, FAIL (with evidence and location), NOT TESTED (with reason) or N/A (with reason). A criterion that no automated rule covers and the agent did not check manually is NOT TESTED. Zero violations from a scan of zero screens is NOT TESTED.
- The agent must not mark any criterion that depends on how a screen reader actually speaks and behaves as PASS from the tree alone. It may record "tree exposes name X, role Y; real screen reader behavior not tested".

Return contract appended verbatim. Check: each notes file exists, names the tools, and lists criterion results per screen; a notes file with only a summary is a failed phase (re-brief once, then BLOCKED for that platform).

## Phase 3: What an agent cannot test

Main session. State this explicitly in the report, as its own section, and ask the user once:

- Real screen reader use by a person on the core flows, on each platform in scope.
- Voice control, switch access, and magnification use.
- Cognitive and comprehension factors (plain language, consistent patterns, timing) beyond what the checklist detects.
- Testing with disabled users, which no tool replaces.

Ask: has a person already done a screen reader pass on these flows, or will someone do one? Offer to write a short script for it (steps per flow, expected announcements, what to record) as a section of the report. Record the answer. "Not yet" or no answer means the real screen reader criteria stay NOT TESTED and the verdict cannot be CONFORMS. Never infer a screen reader result from the accessibility tree.

## Phase 4: Verify and consolidate

Main session. For every FAIL that blocks a core flow, reproduce it or re-read the evidence yourself (a screenshot, tree dump line or recorded step). Mark VERIFIED or UNVERIFIED. Spot-check one PASS per platform against the live app. Consult `ux-designer` for failures whose fix changes layout or flow, and attach their note.

Classify each failure: BLOCKER (a user of assistive technology or keyboard cannot complete a core flow, or a Level A criterion fails on a core flow), MAJOR (AA failure, flow completable with difficulty), MINOR (best-practice or polish). Map to finding severity words HIGH, MEDIUM, LOW in the report with BLOCKER shown as CRITICAL.

Write `docs/qa/a11y-<date>.md` from `accessibility-audit.md`: summary, scope, per-platform tables (criterion, screens, result, evidence), the not-testable section, failures ranked with fixes, and the human test script. New studio documents are written directly per section 3.

Check: the report file exists, every in-scope criterion row has a result, and the not-testable section is present.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Screens | the core flows | all flows and states | all flows, states and each theme and scale setting |
| Layers | automated plus keyboard walk and contrast | plus full manual checklist for the platform | plus a written human test script and a re-test of previous failures |
| Platforms | primary | all shipped | all shipped plus lowest supported OS |

Rigor sets how much is checked, never whether a failure counts. No gate runs in this skill; `/app-gate` and `/app-release` read the report. `solo`, `lean` and `full` do not change the audit.

## Verdicts

First match wins:

1. **FAILS**: any open BLOCKER, or a failed Level A criterion on a core flow.
2. **PARTIAL**: no BLOCKER, but open MAJOR failures. The report lists the exceptions to conformance.
3. **NOT ASSESSED**: no failures, but any applicable criterion is NOT TESTED, including real screen reader use, a platform that could not be run, or a scan of zero screens. Name each and what closes it.
4. **CONFORMS**: every applicable criterion on every in-scope platform tested and passing, including a recorded human screen reader pass, and only MINOR issues remain, listed.

A claim of "conforms" is a statement about the tested scope only. The report says which screens, platforms and settings it covers.

## Report

```
Accessibility: <app>   Date: <date>   Target: <WCAG 2.2 AA + platform guidance | other>   Platforms: <tested> / <not tested>
Tools: <name version> per platform
Criteria: <passed> pass, <failed> fail, <not tested> not tested, <n/a> n/a, of <total applicable>
Failures: BLOCKER <n>  MAJOR <n>  MINOR <n>  (verified <n>)
Cannot be tested by an agent: <list>   Human pass: done | planned | not done
Decisions for you: <who runs the human pass; fix order> | none
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Never report CONFORMS from automated results alone, or without a recorded human screen reader pass.
- Never mark a criterion PASS that was not checked; NOT TESTED is a result.
- Never infer real screen reader output from the accessibility tree.
- Never claim a count without its denominator (screens, criteria).
- Never fix code here; route fixes to `/app-bugfix` or `/app-plan`, and design changes to `/app-ux`.
- Never run captures that steal the user's focus, or interfere with the user's running copy of the app.
- Always name the tool and its version used for each automated result.
