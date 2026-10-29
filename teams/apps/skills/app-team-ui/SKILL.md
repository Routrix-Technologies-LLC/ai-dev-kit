---
name: app-team-ui
description: "Take a screen or UI area from spec to polished, accessible, observed implementation: UX spec, visual spec, platform build, parallel design, accessibility and copy review, polish. Use when the user wants a screen or UI area designed and built well, says 'build this screen', 'polish this UI', 'make this look right on every platform', or UI work keeps coming out inconsistent or inaccessible."
argument-hint: "[app] [screen or UI area] [--review solo|lean|full]"
user-invocable: true
---

# Team: UI

Coordinates the people who make a screen good: UX design, visual design, the platform's UI builders, and a parallel review by design, accessibility and content. It calls `app-ux`, `app-plan`, `app-dev-story`, `app-story-done` and `app-design-language` rather than redoing them, and adds what a single skill does not: the visual spec, evidence captured per state, theme and form factor, and a joint review.

Writes: `docs/design/ux/<flow>.md` (via `app-ux`, template `ux-spec.md`), `docs/design/ui/<area>/visual-spec.md`, code and tests (via `app-dev-story`), evidence in `docs/qa/evidence/<area>/`, review notes `docs/design/ui/<area>/review-<agent>.md`, a review summary `docs/design/reviews/<date>-<area>.md`.
Next: `app-ux-review` (formal review against the spec), `app-a11y-audit` (full audit), `app-team-harden`, `app-release`.

## When to use and when not to

- Use for one screen, a flow, or an area of the UI that needs design and build together.
- A UX spec only: `app-ux`. A tokens or theme definition: `app-design-language`. A whole feature that includes UI plus services: `app-team-feature` (run this afterwards for the screens). A review of UI that already exists: `app-ux-review`. A single small UI bug: `app-bugfix`.
- App with no UI (backend, library, plain CLI): stop and say so. A CLI with a TUI or interactive prompts counts as UI here; its "screens" are its interactive views and its builder is the language specialist.

## Inputs

- The app, per orchestration.md section 1. No `studio.yaml`: offer `/app-adopt` or `/app-start` and stop.
- **No screen or area given: print usage and the platforms this app has, spawn nothing, and ask in plain text what to build.**
- Phase 1 reads and reports each of these as `present` or `ABSENT`: the feature spec for the area, an existing UX spec, `docs/design/design-language.md`, existing implemented screens that set the pattern, the accessibility commitment (usually inside the design language), the `platforms` and `min_targets` in `studio.yaml`, `commands.screenshot`. Absence is never silent.

## Phase 0: Resolve and announce

Main session: orchestration.md sections 1 and 2. Resume from `.studio/state.md` if an earlier run of this area exists. Pick the UI builder(s) from the table and print the announce block with every agent not spawned and why.

| Platform in `studio.yaml` | UI builder | Also |
|---|---|---|
| web | `ui-engineer` (components, CSS, layout, theming) with `frontend-engineer` (views, state, forms) | `web-framework-specialist` for framework-specific problems; `web-lead` consulted |
| windows | `windows-desktop-engineer` | `win32-systems-specialist` only for below-UI problems |
| macos | `macos-engineer` | |
| linux | `linux-desktop-engineer` | |
| webview or cross-platform desktop | `hybrid-desktop-engineer` | the web or toolkit specialists for the UI layer |
| ios | `ios-engineer` | |
| android | `android-engineer` | |
| cross-platform mobile | `cross-platform-mobile-engineer` | |
| extension | `web-platform-engineer` with `ui-engineer` | |
| cli with TUI | the language specialist from `studio.yaml` | |

An app on several platforms gets one builder per platform for the platform-specific parts; shared UI code is built by the builder of the shared layer. Always add the language specialist(s) for review.

## Phase 1: Context

Main session reads the inputs above and reports each as present or ABSENT.

- **No design language** (`docs/design/design-language.md`): ask whether to run `/app-design-language` first (recommended for a first screen) or proceed. If proceeding, `ui-designer` states the tokens the screen assumes in the visual spec and those are flagged as proposed additions; they are not silently invented.
- **No accessibility commitment**: the target is WCAG 2.2 AA plus the platform's accessibility API, recorded as an assumption in the brief of every agent. If the standard is neither committed nor assumed, the review is NOT ASSESSED for accessibility.
- **No existing screens** to match: say so; the first screen becomes the pattern and must be flagged as such for the design language.
- **No `commands.screenshot`**: evidence in Phase 4 will be NOT VERIFIED unless the user supplies a capture route; offer `/app-test-setup` for headless capture.

Distill a context brief: user goal on this screen, constraints, patterns to reuse, platform and form factors, themes, locales in use.

## Phase 2: UX spec

Run `/app-ux <flow>` unless a current, approved spec for this area exists (show its date and states; ask whether to reuse, revise or replace). `app-ux` spawns `ux-designer`, `content-designer`, `accessibility-specialist` and `ui-designer` as it defines.

- Check: the spec exists and covers purpose, navigation, layout, every state (loading, empty, error, partial, offline, long content), every platform variant and input mode, copy, accessibility, events and acceptance criteria.
- Gate: DD-UX-SPEC as app-ux runs it at `full`. REJECT blocks Phase 3. CONCERNS: show them, ask revise or accept; an accepted concern is recorded in the report. A skipped or dismissed answer is not acceptance.

## Phase 3: Visual spec

Spawn `ui-designer` alone (it needs the approved UX spec). It writes `docs/design/ui/<area>/visual-spec.md`:

- tokens used (by name from the design language) and any proposed new token with its reason;
- component specs for every state and size class, spacing, type, iconography, imagery, motion with a reduced-motion alternative;
- light, dark and high-contrast treatment, with measured contrast ratios for every text and control pair (not asserted);
- per-platform adaptation (density, platform conventions, safe areas, window resizing, text scaling, touch target or pointer sizes);
- an asset manifest with sizes and formats.

Decision point: the user approves or revises. New design-language tokens go through `/app-design-language`, not into the spec as facts. Check: the file exists and lists contrast pairs with numbers.

## Phase 4: Implementation

Stories first: if no stories cover this UX spec, run `/app-plan` scoped to it and ask the user to approve the set. Then build each story with `app-dev-story`'s procedure. The skill is user-typed by design; ask once whether to follow it here or have the user type it per story, and honor the answer.

The builder's brief carries these requirements, none optional:

- Follow the UX spec and visual spec; use existing components and tokens before making new ones; flag every deviation for `ux-designer`.
- Every state in the spec is implemented and reachable, including loading, empty, error and long content.
- User-facing strings externalized, no hardcoded copy; no layout that breaks at 200 percent text size or in a longer language.
- Keyboard and focus order complete; every control has an accessible name, role and state through the platform's accessibility API; touch or pointer targets meet the platform minimum; reduced motion respected.
- Presentation holds no business logic; user actions emit events or calls to the layer that owns the behavior.
- Light, dark and high-contrast themes work; window or device resizing works across the supported sizes.

The builder returns the files it will change; ask once per story for the set; then it writes. The main session runs `commands.test` and lint and reads the output.

**Run and observe** (orchestration.md section 10): capture each screen in each state, in each supported theme and at least the smallest and largest form factor, into `docs/qa/evidence/<area>/`, without taking window focus. Look at the images yourself. Report the single `Run result:` line per story. NOT VERIFIED blocks closing a UI story and caps this skill's verdict at NOT ASSESSED.

## Phase 5: Review (parallel)

Spawn in one message, each told "your job is not to confirm this matches the spec, find where it fails it", each reading the spec, the visual spec and the evidence, and each writing `docs/design/ui/<area>/review-<agent>.md`:

| Agent | Checks |
|---|---|
| `design-director` | consistency with the design language and sibling screens, visual quality, hierarchy, polish; at `full` also issues the DD-VISUAL verdict (told to read `gates/dd-visual.md`) |
| `accessibility-specialist` | keyboard-only path, focus order and visibility, names and roles, contrast of what was captured, text scaling, reduced motion, screen reader announcements where testable; states plainly what an agent cannot test (live screen reader, switch control) |
| `content-designer` | labels, messages, empty and error states, terminology, tone, truncation and length |
| `ux-researcher` | `full` only: heuristic evaluation against the heuristics in `app-ux-review` |

Collect all reviews before continuing. The main session spot-checks every blocking finding against the evidence or code (orchestration.md section 5) and merges them into `docs/design/reviews/<date>-<area>.md` (verdict words per `app-ux-review`: APPROVED, NEEDS REVISION, MAJOR REVISION, NOT ASSESSED). For a formal evidence-led review of the finished flow, recommend `/app-ux-review`; at `full`, run `/app-a11y-audit` scoped to the area instead of relying on the specialist's note alone.

## Phase 6: Polish and fix loop

Route each accepted finding to its owner: layout and visuals to the UI builder, copy to the builder with the `content-designer`'s text, spec gaps to `ux-designer` for a spec update, new tokens or components to `app-design-language`. One ask for the file set, fix, recapture evidence for every changed screen, and have the reviewer who raised a blocking finding re-check it. Two rounds at most, then the user decides: accept the remainder as notes, defer to tech debt, or continue.

Polish checklist the main session verifies from evidence: all states captured, themes captured, motion skippable, long text and small window checked, new patterns added to the design language or logged as a proposal, UX spec still matches what was built.

## Phase 7: Close

Run `app-story-done` per story (same consent as Phase 4). Record the area's review summary and open items. Update `.studio/state.md`.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| UX spec | short, states and copy listed | `app-ux` | plus DD-UX-SPEC |
| Visual spec | only new tokens and states, contrast measured | complete | complete, per-platform adaptation reviewed |
| Evidence | each state once in the default theme | each state, light and dark, two sizes | plus high contrast, text scaling, every supported form factor |
| Review | `accessibility-specialist` plus `design-director` | plus `content-designer` | plus `ux-researcher`, DD-VISUAL, `app-a11y-audit` |

Gates by mode: `solo` skips all gates (printed); `lean` runs only the always-on gates inside the called skills (for example `PE-CODE-REVIEW` at `app-story-done`) and prints `DD-UX-SPEC` and `DD-VISUAL` as `skipped: lean mode`; `full` runs `DD-UX-SPEC` and `DD-VISUAL`. The reviewers themselves run at every mode.

Phases that may be skipped at minimal: 3 for a change that adds no new look (reuse, state the reuse), and `content-designer` when the screen adds no copy. Never skipped: 1, the accessibility review, Phase 4 evidence, Phase 7.

## Verdicts

First match wins:

1. `BLOCKED` - UX spec rejected, an agent BLOCKED unresolved, or the app has no UI.
2. `NEEDS WORK` - a verified blocking finding is open (contrast failure, unreachable state, broken keyboard path, wrong behavior against the spec) or a story failed.
3. `NOT ASSESSED` - Run result NOT VERIFIED, a review agent returned nothing, accessibility has no standard or could not be examined, or a state or theme in the spec has no evidence. Name each.
4. `COMPLETE WITH NOTES` - done; accepted concerns, deferred items and untestable-by-agent accessibility checks are listed.
5. `COMPLETE` - every state and theme in the spec has evidence, all reviewers reported, nothing blocking open.

## Report

```
Area: <area>   App: <name>   Platforms: <list>   Rigor: <r>   Review: <m>
UX spec: <path, states N, platform variants N> | Visual spec: <path, contrast pairs N, failing N>
Build: <stories closed of N, builders used>   Run results: <lines>
Evidence: <N images across N states x N themes x N sizes; denominator stated>
Reviews: design <verdict> | accessibility <verdict, not agent-testable list> | content <verdict>
Open: <findings by severity>   Accepted concerns: <list>   Gaps: <named>
```

Then the closing block from orchestration.md section 8.

## Rules for this skill

- Never invent tokens, patterns or copy silently; proposals are labeled.
- Never call accessibility passed on assertion; cite what was measured or exercised, and name what was not.
- Never close a UI story without retained evidence of the screens it touched.
- Never write to the design language or UX spec outside their skills.
- Capture without stealing focus; never type into or click in the user's open windows, and never run UI automation that injects keyboard or mouse input into the real desktop (headless browsers, simulators and offscreen captures drive their own input and are fine).
- Two agents never edit the same file; each review agent writes only its own file.
