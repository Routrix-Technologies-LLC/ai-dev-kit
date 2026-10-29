---
name: app-design-language
description: "Create or update the app's design language: principles, design tokens, type, color, spacing, motion, iconography, components, theming and per-platform adaptation, with contrast measured rather than asserted. Use when the user wants a design system, style guide, tokens, theming or dark mode defined, says 'design language', 'what should this look like across platforms', or UI work keeps drifting because there is no shared visual spec."
argument-hint: "[app] [create | update <section> | from-code] [--review solo|lean|full]"
user-invocable: true
---

# App Design Language

Defines the shared visual and interaction vocabulary every screen is built from: principles, tokens, typography, color roles, spacing, elevation, motion, iconography, a component set with states, theming (light, dark, high contrast), and how the language adapts on each platform the app ships on. It is the one document `/app-ux` specs and UI builders refer to for "how things look".

Writes: `docs/design/design-language.md` (template `templates/design-language.md`), `.studio/state.md` checkpoint.
Next: `/app-ux` (specs use its components and tokens), `/app-a11y-audit` (verifies the contrast and target claims), `/app-architecture` or `/app-plan` (token delivery becomes a foundation story).

## When to use and when not to

- Use at definition stage before UI work, when adopting an app whose UI has grown without a system (`from-code`), or when adding a platform, a theme or a brand change.
- Not for one screen's behaviour (`/app-ux`), not for judging built UI (`/app-ux-review`), not for the product's identity and positioning (`product-director` through `/app-brief`).

## Inputs

| Input | If missing |
|---|---|
| `studio.yaml` (`platforms`, `stack.frameworks`) | Stop; offer `/app-adopt` or `/app-start`. |
| Brief or vision (audience, tone, brand constraints) | Ask for tone words and any fixed brand assets (logo, colors, fonts). Never invent a brand. |
| Existing UI code or style files | `from-code` and `update` read them; `create` on an empty app proceeds without. |
| Accessibility baseline | Assume WCAG 2.2 AA and the platform accessibility API; record the assumption. |
| Licensing constraints for fonts and icons | Ask. Only fonts and icon sets with a license the app can ship are proposed (open licenses by default); the choice is recorded with its license. |

## Mode detection

| Argument | Mode |
|---|---|
| none, `create`, file absent | create: author every section |
| `update <section>` or file present | update: change only the named section(s), keep a change note, flag components and UX specs that now disagree |
| `from-code` | Extract what exists first (Phase 1b), present it as the proposed baseline, then decide what to keep. Output is marked as reconstructed until the user approves each section |

If the file exists and the mode is `create`, ask: update, or replace one section. Never overwrite silently.

## Phase 1: Resolve, announce, ground

Main session. Print the plan block (`orchestration.md` section 2). Agents: `design-director` (direction and gate), `ui-designer` (the language), `accessibility-specialist` (measured checks), `ui-engineer` (consulted on feasibility; for apps with no web or cross-platform UI layer use the platform's UI builder from `studio.yaml` `specialists`, such as `windows-desktop-engineer`, `macos-engineer`, `ios-engineer`, `android-engineer`). Not spawned: builders for platforms the app does not target.

1a. Read the brief, specs' UI-relevant requirements, existing UX specs and `studio.yaml`.

1b. From code (mandatory for `from-code`, and for `update` on an app with UI): spawn `ui-engineer` (or the platform UI builder) with a brief to inventory what is actually implemented: color literals and their frequency, font families and sizes in use, spacing values, radii and shadows, theme mechanisms, component library in use, duplicated one-off components. Output `~/AgentScratch/app-design-language/inventory.md` with file paths and counts. The main session spot-checks three counts with Grep. This inventory is evidence; the language is not obliged to preserve it.

Check: the inventory file exists with counts and paths, or the app has no UI code and the report says so.

## Phase 2: Direction

`design-director` and `ui-designer` in parallel (`orchestration.md` section 4). Each writes one file under `~/AgentScratch/app-design-language/`.

- `design-director.md`: three to five design principles tied to the brief ("calm over clever"), what the product should feel like, what it must never look like, and the platform strategy options below.
- `ui-designer.md`: two or three visual direction options (not just one), each with a sample color set, type pairing, shape language and density, with the trade-offs.

Decision for the user (one ask): the platform strategy. Present the three with consequences and a recommendation fitted to the stack:

| Strategy | Meaning | Cost |
|---|---|---|
| Native idiomatic | Each platform follows its own guidelines (Fluent on Windows, Human Interface Guidelines on Apple platforms, Material on Android, the target desktop environment's conventions on Linux). Brand shows through accent color, icon and content only | Most platform-correct; most design and test work |
| Unified brand, adapted per platform | One visual language; layout, navigation, controls behaviour, text rendering and system integration adapt to each platform | Balanced; the usual choice for cross-platform stacks |
| Single custom system | One look everywhere, platform conventions only where accessibility or the OS forces them | Cheapest to build; feels foreign on some platforms; highest risk for accessibility |

Then the visual direction option. Write principles and the chosen strategy into the document immediately.

## Phase 3: Tokens and foundations

`ui-designer` drafts each foundation; the main session presents it, the user decides, the section is written when approved. Write each section into the matching numbered heading of `templates/design-language.md` (1 Principles, 2 Token architecture, 3 Color, 4 Typography, 5 Spacing, layout and shape, 6 Iconography and imagery, 7 Elevation, surfaces and effects, 8 Theming, 9 Motion (including sound and haptics), 10 Components, 11 Per-platform adaptation, 12 Governance); the header line carries Status `Draft`, Version, Last updated, platforms covered and the token source of truth. Foundations, in order:

1. Token architecture: primitive tokens (raw values), semantic tokens (roles such as surface, on-surface, accent, danger, border, focus), component tokens (only where a component needs its own). Components consume semantic tokens only. Name the source of truth and its format for this stack (W3C design tokens file, CSS custom properties, XAML resource dictionaries, asset catalogs, Android theme resources, Compose or SwiftUI theme objects, a shared package) and how values reach each platform. Ask `ui-engineer` (Phase 6) whether the delivery is practical before locking it.
2. Color: roles, not swatches. Neutral ramp, accent, semantic status colors (success, warning, danger, info), focus color, data-visualization colors if the app has charts (and color-blind-safe pairs).
3. Typography: families (with license), type scale by role (display, heading, body, label, code), weights, line heights, platform text rendering notes, how text scales with the platform's text size setting (dynamic type, font scaling, browser zoom).
4. Spacing, layout and size classes: spacing scale, grid or layout rules, breakpoints for web and size classes or window width classes for desktop and mobile, minimum window size for desktop, density options.
5. Shape and elevation: radii, borders, shadows or tonal elevation, focus ring.
6. Motion: durations and easing by purpose (feedback, transition, emphasis), what must never animate, reduced-motion behaviour for every animation class.
7. Iconography and imagery: icon set (license), sizes, stroke or fill rule, illustration and photo direction, app icon and splash requirements for each platform's shipped sizes and shapes (adaptive and rounded-mask conventions, store asset sizes are filled by `/app-store-prep`).
8. Sound and haptics only if the product uses them (recorded under Motion).
9. Governance (template section 12): who approves a new token or component (`design-director`), how deprecations are announced and removed, how design and code stay in sync (the token source of truth and how drift is detected), where the visual regression baseline lives, and the document's version and change log.

Check after each section: the section is written with concrete values, not adjectives. "Warm gray" is not a token.

## Phase 4: Components

`ui-designer` proposes the component set from the specs and UX specs (do not design components nothing needs). For each component the document records: purpose, anatomy, variants, every state (default, hover, focus, pressed, disabled, loading, error, selected), tokens used, size and density behaviour, content rules, accessibility notes (role, name, keyboard, focus, target size), and the native control it maps to per platform, or "custom, because <reason>". Start with the set the first flows need: button, text input, selection controls, list and table, navigation, dialog and sheet, menu, toast or inline message, empty state, progress, and whatever the app is built around.

Decision point: for each custom component that duplicates a native control, the user confirms the reason. Check: every component lists all states or marks one "not applicable" with a reason.

## Phase 5: Theming and per-platform adaptation

`ui-designer` writes both; `accessibility-specialist` reviews in Phase 6.

- Themes: light, dark, high contrast or increased contrast, and any brand theme. Dark is its own palette, not an inversion. Define how the theme is chosen (follow system, user override) and persisted.
- Per-platform adaptation table, filled for each platform in `studio.yaml`:

| Aspect | web | Windows | macOS | Linux | iOS or iPadOS | Android |
|---|---|---|---|---|---|---|
| Guideline anchor | Own system plus WCAG 2.2 | Fluent | Human Interface Guidelines | Target desktop environment's guidelines | Human Interface Guidelines | Material |
| Navigation pattern | | | | | | |
| Window or size classes | | | | | | |
| Controls: native or custom | | | | | | |
| Type and text scaling | | | | | | |
| Materials, translucency, shadows | | | | | | |
| Input and gestures | | | | | | |
| Icons and app icon form | | | | | | |
| What deliberately differs | | | | | | |

Include only the columns for platforms the app targets. A cell may say "inherit from the shared language"; it may not be empty. Read `references/platform-adaptation.md` for the checklist behind each cell.

## Phase 6: Verification and gate (parallel)

Issue together:

- `accessibility-specialist`: compute (with Bash, a short script run from the scratchpad, or by hand with the stated formula) the WCAG contrast ratio of every foreground and background token pair in every theme, check minimum target sizes and the focus indicator, and write the measured table to `~/AgentScratch/app-design-language/contrast.md`. The design language embeds the table. A ratio that was not computed is written `NOT ASSESSED`, never estimated. Failures at the AA thresholds (4.5 to 1 for body text, 3 to 1 for large text and UI components) are listed with a proposed fix.
- `ui-engineer` (or the platform UI builder): feasibility of the token delivery and component list in this stack, including theming support and the cost of the custom components. Output `~/AgentScratch/app-design-language/feasibility.md`.
- `design-director`: gate `DD-DESIGN-LANGUAGE` (full review mode only, see the table below). Pass the document path, the contrast table, the feasibility file and the platform strategy. Because the gate needs both other results, spawn it last, after the first two return.

The main session fixes failing pairs with the user (adjust the token, record an exception with a reason, or accept a documented risk), re-runs the contrast computation for changed pairs, and records the gate result directly under the title as `> **Design Director review (DD-DESIGN-LANGUAGE)**: <APPROVE | CONCERNS | NOT ASSESSED> <date>` when the gate ran (no line when skipped). The gate runs in `full` review mode only; `solo` and `lean` print `DD-DESIGN-LANGUAGE skipped: solo mode` or `skipped: lean mode`. CONCERNS: ask to revise, accept (recorded in the change log) or discuss. REJECT: revise and re-run. NOT ASSESSED: name the missing input (the document, or the UX specs and brief it is judged against); never treat it as approval.

Check: the contrast table exists inside the document with a computed ratio per pair per theme; the feasibility file exists.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Document | Optional short form (only if the app has a UI): 3 principles, color roles with measured contrast pairs, type scale, spacing scale, the components in use | Template sections 1 to 11: every component in the UX specs, light and dark with measured contrast, per-platform adaptation for each platform | All 12 sections, plus a token naming and export contract with the code, a documented exception log and a visual regression baseline |
| Themes | One | Light and dark | Light, dark, high contrast |
| Contrast table | Text pairs only | All pairs, all themes | All pairs, all themes, re-run after any token change |
| Gate DD-DESIGN-LANGUAGE (set by review mode, not rigor) | solo and lean: skipped | solo and lean: skipped | full mode: runs |

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

- BLOCKED: no platform strategy decided, a required specialist artifact missing after one re-brief, the contrast table could not be produced and the user will not accept it as NOT ASSESSED, or the gate returned REJECT.
- NOT ASSESSED: the document is written, but some contrast pairs or the gate could not be assessed (for example `contrast for dark theme NOT ASSESSED (palette not final)`, or `DD-DESIGN-LANGUAGE` returned NOT ASSESSED and the input was not supplied). The verdict line lists each item; downstream gates must not treat them as passed.
- COMPLETE: all sections required at this rigor are written and approved, every contrast pair is computed, and no gate result is NOT ASSESSED.

## Report

```
Design language: <path>   Mode: <create | update | from-code>   Strategy: <chosen>
Themes: <list>   Components: <N>   Platforms adapted: <list>
Contrast: <N pairs computed of N>, <N failing, N excepted>
Custom components duplicating native controls: <N, reasons recorded>
From code: <inventory summary or n/a>
Downstream specs/components now inconsistent (update mode): <list or none>

Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: <DD-DESIGN-LANGUAGE: VERDICT> | none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Values, not adjectives: every token has a concrete value or an explicit "to be chosen" in Open Questions.
- Never state a contrast ratio, target size or font license that was not computed or checked.
- Never propose fonts, icons or images without a license the app can ship, and record the license.
- In update mode never rewrite sections that were not named; never edit UX specs, name the ones that now disagree.
- Never invent brand assets or claim a platform guideline says something that was not read from the guideline.
- Decisions on strategy, direction and custom components belong to the user.
