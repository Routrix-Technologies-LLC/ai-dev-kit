# UX Spec: [Flow or screen group name]

<!--
WRITTEN BY: ux-designer, with content-designer (copy), accessibility-specialist (accessibility notes) and ui-designer (visual detail). Skill: /app-ux.
LIVES AT: docs/design/ux/<flow>.md (override: paths.ux in studio.yaml). One file per flow or tightly related screen group.
RIGOR: minimal = usually skipped; if used, sections 1, 3 and 4 for the one critical flow, with all states listed.
       standard = sections 1 to 10; every screen lists every state; keyboard and screen reader notes present; copy for all states.
       full = standard plus platform wireframes or annotated captures for each variant, completed motion and input-method tables, and a design-director review.
GATE: DD-UX-SPEC. Cites the design-language tokens and components by name; it never invents a new color, size or component silently.
Specify behavior and content. Pixels, tokens and component anatomy belong in the design language. Requirements and logic belong in the feature spec; link them.
-->

**Status:** [In design | In review | Approved | Implemented]   **Author:** [role]   **Last updated:** [YYYY-MM-DD]
**Feature specs:** [paths, REQ IDs covered]   **Pillars served:** [P#]   **Platforms:** [from studio.yaml]
**Design language:** [path]   **Accessibility target:** [e.g. WCAG 2.2 AA plus platform accessibility API]

## 1. Purpose and user context
<!-- The human need this flow serves, in one paragraph. Then who arrives, what they were just doing, what they already know, their likely state (hurried, anxious, relaxed, one-handed, on a bad connection) and what they are afraid of getting wrong. Design for the worst plausible arrival, not the best. -->
**User goal:** [one sentence specific enough to test]
**System goal:** [what the product needs from this interaction]
**Arrival context:** [text]

## 2. Information architecture and navigation
<!-- Where this flow sits in the app: entry points (every way in, including deep links, notifications, shortcuts, restore after relaunch), exits, back behavior, how the user knows where they are. A small map in text. Name each screen once; later sections use the same names. -->
```
[Entry point] -> [Screen A] -> [Screen B] -> [Exit / result]
                     \-> [Error or alternate]
```

## 3. Flows
<!-- One numbered flow per user goal: the happy path first, then each alternate and failure path as a branch with its own number. Each step: user action, system response, resulting screen/state. Include the interrupted case (app closed, call comes in, session expires) and the return path. Aim for the fewest steps and decisions that still protect the user. -->
### Flow F1: [name]
| Step | User action | System response | Screen and state |
|---|---|---|---|
| 1 | | | |

## 4. Screens
<!-- One block per screen. Layout described by regions in priority order (what the eye should meet first), content in each region, primary and secondary actions with their labels, and what is persistent. Wireframes or annotated captures are linked, never the only source. -->
### [Screen name]
- **Purpose:** [one line]
- **Layout and hierarchy:** [regions in priority order]
- **Content and data shown:** [fields, formats, truncation rules]
- **Primary action:** [label, result]   **Secondary actions:** [list]
- **Components used:** [names from the design language]

#### States (every one; mark N/A with a reason, never omit)
| State | What the user sees | What they can do | Copy ref |
|---|---|---|---|
| Ideal (populated) | | | |
| Empty (first use) | | | |
| Empty (no results) | | | |
| Loading (first, and refresh) | | | |
| Partial or degraded | | | |
| Error (recoverable) | | | |
| Error (not recoverable) | | | |
| Offline | | | |
| Permission denied or missing | | | |
| Success or confirmation | | | |
| Disabled or unavailable | | | |

## 5. Platform variants and breakpoints
<!-- What changes per platform and per size class: layout, navigation pattern (tab bar, sidebar, bottom bar, menu bar), controls, density, gestures, windowing (resize, multi-window, split view), and OS conventions followed (Fluent, Apple HIG, Material 3, web patterns). State the breakpoints or size classes and the layout at each; test narrow, wide, and large text. -->
| Platform or size class | Layout | Navigation | Notable differences |
|---|---|---|---|

## 6. Input methods
<!-- Every way a person can operate each action: pointer, touch, keyboard, voice, stylus, game controller or remote where relevant, assistive technology. Give keyboard shortcuts and their platform equivalents, tab order, focus start and return points, gestures with a visible alternative, and hover or long-press behavior with a non-hover equivalent. -->
| Action | Pointer / touch | Keyboard | Other (voice, switch, gesture alternative) |
|---|---|---|---|

## 7. Copy
<!-- Every string the user will read, with its key: titles, labels, placeholders, help text, confirmations, empty states, errors (what happened, why if known, what to do next, no blame, no codes alone), toasts, accessibility labels. Follow the product voice; plain words; sentence case unless the platform says otherwise. Mark strings with variables, plurals and length limits for localization. -->
| Key | Context (screen, state) | Text | Notes (variables, plural, max length) |
|---|---|---|---|

## 8. Accessibility notes
<!-- Per screen: reading and focus order, accessible name, role and state for each control, live-region announcements for async changes, focus management on open/close of dialogs and on navigation, target sizes, contrast pairs used (reference tokens), non-color cues, zoom and text-scaling behavior (200 percent without loss), reduced motion, time limits, error association with fields. Name the platform API mapping for non-web targets (UI Automation, NSAccessibility, UIAccessibility, Android accessibility, AT-SPI). -->
| Screen | Focus order | Names, roles and states | Announcements | Special cases |
|---|---|---|---|---|

## 9. Motion and feedback
<!-- Transitions and animations: what moves, why (orient, confirm, draw attention), duration and easing as design-language motion tokens, and the reduced-motion replacement (usually a fade or an instant change). Also haptics, sound, and progress feedback with thresholds (feedback under 100 ms, a spinner after about 1 s, determinate progress for longer waits). Nothing flashes more than three times per second. -->
| Moment | Motion or feedback | Token | Reduced-motion version |
|---|---|---|---|

## 10. Open questions and risks
| # | Question or risk | Owner | Needed by |
|---|---|---|---|

## Acceptance
<!-- Link the feature spec REQ IDs this spec satisfies and the checks a reviewer runs against the built UI (/app-ux-review): states reachable, copy matches, keyboard path complete, variants correct. -->
- [REQ-[feature]-NNN: how it is verified in the UI]
