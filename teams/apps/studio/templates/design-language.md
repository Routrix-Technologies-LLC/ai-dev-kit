# Design Language: [Product name]

<!--
WRITTEN BY: design-director owns it; ui-designer writes it with accessibility-specialist (contrast, targets, themes) and ui-engineer (consulted on implementability). Skill: /app-design-language.
LIVES AT: docs/design/design-language.md (override: paths.design_language in studio.yaml).
RIGOR: minimal = not required; if the app has a UI, a short version: principles (3), color roles with contrast pairs, type scale, spacing scale, and the components in use.
       standard = sections 1 to 10; light and dark themes with measured contrast; component specs for every component in the UX specs; per-platform adaptation for each platform in studio.yaml.
       full = standard plus high-contrast and forced-colors themes, a token naming and export contract with the code, motion and reduced-motion rules, a documented change process and a visual regression baseline.
GATE: DD-DESIGN-LANGUAGE. UX specs and code cite tokens and components by name from this file.
Contrast numbers are measured, never estimated: write the ratio next to every foreground/background pair. Decide values for the product's own identity; only adopt platform defaults where being native is the goal.
-->

**Status:** [Draft | Approved | Implemented]   **Version:** [1.0]   **Last updated:** [YYYY-MM-DD]
**Platforms covered:** [from studio.yaml]   **Token source of truth:** [path to the token file in the code, or "this document"]

## 1. Principles
<!-- 3 to 5 design principles derived from the vision pillars, each with a do and a do-not, specific enough to settle an argument about a button. Say when native platform convention beats our own look. -->
| Principle | Means | Do | Do not |
|---|---|---|---|

## 2. Token architecture
<!-- Three tiers. Primitive (raw values: color-blue-500, space-4, font-size-300). Semantic (meaning, themeable: color-text-primary, color-surface-raised, color-border-focus, space-inset-md). Component (scoped to a part: button-primary-background). Code and designs reference semantic or component tokens, never primitives. Naming: category-property-role-variant-state, lowercase, hyphenated; one name per concept. Describe how tokens are exported to each platform (CSS custom properties, XAML resources, asset catalogs, Android resources, constants) and who regenerates them. -->
| Tier | Example | Who may reference it |
|---|---|---|
| Primitive | color-blue-500: #[hex] | Semantic tokens only |
| Semantic | color-text-primary -> color-neutral-900 (light), color-neutral-50 (dark) | Components and screens |
| Component | button-primary-background -> color-action-default | The component itself |

## 3. Color
<!-- Primitive palettes (with the scale and the measured luminance if you use it), then semantic roles, each with light, dark and high-contrast values. Contrast pairs are a table: every text role on every surface it is allowed on, with ratio. Minimums: normal text 4.5:1, large text (about 24 px, or 18.66 px bold) 3:1, UI components and focus indicators and meaningful graphics 3:1 against adjacent colors (WCAG 2.2 AA). Never rely on color alone for meaning; list the secondary cue (icon, text, pattern) for status colors. Also note color-vision-deficiency checks. -->
| Role token | Light | Dark | High contrast | Used for |
|---|---|---|---|---|

### Contrast pairs
| Foreground token | Background token | Theme | Ratio | Passes (text 4.5, large 3, UI 3) |
|---|---|---|---|---|

## 4. Typography
<!-- Typefaces (with license, fallback stack, and the per-platform system font if used), the type scale as named roles (display, title, heading, body, label, caption, code) each with size, weight, line height, letter spacing, and where it is used. Sizes in relative units or the platform's scalable units so user text-size settings work (Dynamic Type, Android font scale, browser zoom, Windows text scaling). Line length 45 to 80 characters for reading text. Number formatting (tabular figures) for data. -->
| Role | Size / line height | Weight | Family | Use | Scales with user setting |
|---|---|---|---|---|---|

## 5. Spacing, layout and shape
<!-- One spacing scale (for example a 4 or 8 base) as named tokens; inset, stack and inline rules; grid and column behavior; size classes and breakpoints; minimum touch and click targets (at least 24 by 24 CSS px per WCAG 2.2, and 44 by 44 pt on Apple platforms, 48 by 48 dp on Android as the target to design to); corner radii and border widths as tokens; density modes if any. -->
| Token | Value | Use |
|---|---|---|

## 6. Iconography and imagery
<!-- Icon set and source (with license), grid and stroke rules, sizes as tokens, optical alignment, filled versus outline meaning, when an icon needs a text label (almost always), accessible names, and which platform icon systems are used natively (SF Symbols, Segoe Fluent Icons, Material Symbols). App icon and illustration style, image treatment, alt-text rules. -->

## 7. Elevation, surfaces and effects
<!-- Surface levels as semantic tokens (base, raised, overlay, modal, tooltip), how each is shown in light and dark (shadow in light, lighter surface or border in dark), blur and translucency (with a solid fallback when transparency is disabled), scrim values, focus ring spec (color, width, offset; visible against every surface). -->
| Level | Light | Dark | Use |
|---|---|---|---|

## 8. Theming
<!-- Light and dark are both complete, not an inversion; system setting followed by default with a manual override; high contrast / forced colors honored (Windows contrast themes, forced-colors in browsers, iOS Increase Contrast, Android high contrast text); how a theme switch is applied without a flash; what is never themed (brand marks, user content). List the verification: screenshots of each screen in each theme. -->
| Theme | Trigger | Differences | Verified by |
|---|---|---|---|
| Light | default or system | | |
| Dark | system or user | | |
| High contrast | OS setting | | |

## 9. Motion
<!-- Motion principles (purpose first), duration tokens (for example instant 0, fast 100 to 150 ms, standard 200 to 250 ms, slow 300 to 400 ms), easing tokens, what animates and what must not, and the reduced-motion rule: when the user asks for reduced motion, remove movement, parallax, zoom and auto-playing animation, replace with fades or instant changes, keep essential feedback. Never flash more than three times per second. -->
| Token | Value | Use | Reduced-motion behavior |
|---|---|---|---|

## 10. Components
<!-- One entry per component in the UX specs. Anatomy (named parts, numbered on a diagram or listed), variants (size, emphasis, intent), states (default, hover, pressed, focus-visible, disabled, loading, selected, error, read-only), tokens consumed per part, content rules (label length, truncation), behavior (keyboard, pointer, touch), accessibility (role, name, state, focus handling, target size), do and do-not, and the code component name once built. Keep entries short and consistent. -->
### [Component name]
- **Purpose and when to use / not use:** [text]
- **Anatomy:** [1 container, 2 icon, 3 label, ...]
- **Variants:** [list]
- **States:** default, hover, pressed, focus-visible, disabled, [loading, selected, error]
- **Tokens:** [component tokens]
- **Behavior and keyboard:** [text]
- **Accessibility:** [role, name, state, announcements, minimum target]
- **Code:** [component name and path, or "not built"]

## 11. Per-platform adaptation
<!-- The product keeps one identity and adapts to the host platform where users expect it. For each platform in studio.yaml say what is shared (tokens, voice, iconography), what is native (controls, navigation, window chrome, menus, dialogs, system fonts, gestures) and which conventions are followed. Cover only the platforms the app targets. -->
| Platform | Convention followed | Native controls used | Where we deliberately differ |
|---|---|---|---|
| Web | WAI-ARIA Authoring Practices, responsive, forced-colors, prefers-reduced-motion, prefers-color-scheme | HTML semantics first | |
| Windows | Fluent 2: Mica or Acrylic surfaces, system accent color, Segoe UI Variable, title bar and snap layouts, contrast themes | WinUI or the framework's closest equivalents | |
| Apple (macOS, iOS, iPadOS) | Human Interface Guidelines: SF fonts, Dynamic Type, SF Symbols, system materials, safe areas, menu bar and toolbar on Mac, sidebars and tab bars on iOS | SwiftUI / AppKit / UIKit controls | |
| Android | Material 3: dynamic color where wanted, navigation bar / rail / drawer by size class, edge-to-edge and insets, predictive back, font scaling | Compose or Views Material components | |
| Linux | GNOME HIG or KDE HIG for the chosen toolkit, XDG dark preference, system fonts | GTK / Qt controls | |

## 12. Governance
<!-- How the language changes: who approves a new token or component (design-director), how deprecations are announced and removed, how code and design stay in sync, the visual regression baseline location, and the version/changelog of this document. -->
- [Process]

## Change log
| Version | Date | Change | Reason |
|---|---|---|---|
