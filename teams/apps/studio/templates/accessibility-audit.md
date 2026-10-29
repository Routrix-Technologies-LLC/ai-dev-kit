<!--
Template: accessibility-audit. Written by: accessibility-specialist with ux-designer. Skill: /app-a11y-audit.
Lives at: docs/qa/a11y-<date>.md.
Rigor: minimal = verdict, automated results, key findings. standard = adds per-platform manual checklist, findings table, what could not be tested. full = adds assistive technology matrix, user-testing recommendation, retest log.
Delete this comment when the report is created.
-->

# Accessibility audit: [scope]

> **Date**: [YYYY-MM-DD]   **Auditor**: [agent]
> **Standard and level**: [WCAG 2.2 AA, plus the platform's accessibility API and guidelines]
> **App version / build**: [...]
> **Verdict**: [CONFORMS | PARTIAL | FAILS | NOT ASSESSED]

Verdict rules, first match wins: FAILS if any Blocker is open or a Level A criterion fails on a core flow; PARTIAL if no Blocker but a Major is open; NOT ASSESSED if no failure applies but any applicable criterion is NOT TESTED (including real screen reader use, a platform that could not be run, or a scan of zero screens); otherwise CONFORMS, which requires a recorded human screen reader pass and only Minor issues. "Conforms" never means "tested with real users with disabilities", and covers only the screens, platforms and settings listed in scope.

## Scope and environment

| Platform | Screens or flows covered | Assistive technology used | OS, browser, device and versions |
|---|---|---|---|
| [web] | [list] | [screen reader and browser pairings, zoom, keyboard only] | [...] |
| [windows] | | [Narrator, NVDA, high contrast mode, UI Automation inspector] | |
| [macos / ios] | | [VoiceOver, Accessibility Inspector, Voice Control, Dynamic Type] | |
| [android] | | [TalkBack, Accessibility Scanner, font and display size, Switch Access] | |
| [linux] | | [Orca, AT-SPI inspector] | |

## Automated results

| Tool | Scope | Issues found | Pages or screens scanned | Notes |
|---|---|---|---|---|
| [axe / Lighthouse / platform scanner / lint rule] | | [n] | [n of n] | [false positives removed, with reason] |

Automated tools catch only a fraction of problems. A clean scan is not a pass.

## Manual checklist (per platform)

Mark each Pass, Fail (finding ID) or NOT ASSESSED.

| Area | Check | [Platform 1] | [Platform 2] |
|---|---|---|---|
| Perceivable | Text alternatives for meaningful images and icons | | |
| Perceivable | Contrast: text 4.5:1, large text and UI components 3:1, in light and dark and high-contrast modes | | |
| Perceivable | Information not conveyed by color alone | | |
| Perceivable | Text scaling to 200 percent and reflow at 320 CSS px width without loss | | |
| Perceivable | Captions or transcripts for media; no auto-playing audio | | |
| Operable | Everything reachable and usable by keyboard (or switch/voice), no traps, visible focus | | |
| Operable | Logical focus order; focus moved sensibly after dialogs, navigation and errors | | |
| Operable | Touch and pointer targets large enough (WCAG 2.2 target size), no path-only gestures, drag has an alternative | | |
| Operable | Motion: respects reduce-motion; no flashing above thresholds; timeouts adjustable | | |
| Understandable | Labels and instructions on inputs; errors identified in text with a fix suggested | | |
| Understandable | Consistent navigation and help; no unexpected context change; redundant entry avoided | | |
| Understandable | Language declared; reading level reasonable | | |
| Robust | Name, role, value, state exposed correctly to the accessibility API; custom controls match platform patterns | | |
| Robust | Status messages announced without moving focus; live regions used sparingly | | |
| Robust | Works with platform settings (dark mode, large text, bold text, reduced transparency) | | |

## Findings

| ID | Platform | Location | WCAG principle and criterion | Impact (who is blocked and how) | Class | Severity | Fix | Status |
|---|---|---|---|---|---|---|---|
| A11Y-001 | [...] | [screen, component, path:line] | [Perceivable / Operable / Understandable / Robust: criterion name] | [for example: screen reader users cannot reach Submit] | [Blocker / Major / Minor] | [CRITICAL / HIGH / MEDIUM / LOW] | [...] | [Open] |

Class: Blocker (a user of assistive technology or keyboard cannot complete a core flow, or a Level A criterion fails on a core flow), Major (an AA failure, flow completable with difficulty), Minor (best practice or polish). Severity words follow standards/severity.md: Blocker is CRITICAL, Major is HIGH, Minor is MEDIUM or LOW. A finding that is also a bug takes S1 to S4 under the accessibility section of severity.md when filed.

## What an agent could not test

State plainly:
- Real screen reader speech quality and user experience across devices not available here.
- Voice control, switch access and eye tracking in practice.
- Cognitive accessibility, comprehension and real-user testing.
- Platforms, OS versions and assistive technology not on the matrix.

Recommendation: [user testing with people who use assistive technology before release, or accepted gap with owner].

## Retest

| Finding | Date | Result |
|---|---|---|
