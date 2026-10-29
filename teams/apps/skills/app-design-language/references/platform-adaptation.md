# app-design-language: per-platform adaptation checklist

Loaded in Phase 5. Check the current official guideline for each platform before writing a cell; guidelines change, and a cell that cannot be sourced is written `NOT ASSESSED - guideline not consulted`.

## Web
- Own system, built to WCAG 2.2 AA. Responsive by named breakpoints; fluid type and spacing where it helps.
- Respect user preferences: color scheme, reduced motion, contrast, forced colors, zoom and text-size changes.
- Native HTML controls first; custom controls need roles, names, states and keyboard behaviour equal to the native one.
- Focus visible on every interactive element; no hover-only information; target size minimums.
- Performance is part of the design: font loading strategy, image formats and sizes, layout shift.

## Windows (Fluent)
- Fluent 2 layout, controls and materials as the app's framework supports them; system accent color and light, dark and high contrast themes honored.
- Title bar and window controls, snap layouts, per-monitor DPI, keyboard shortcuts and access keys, context menus, Narrator and UI Automation names.
- Decide whether to follow the system accent color or a brand accent.

## macOS (Human Interface Guidelines)
- Menu bar as the command surface, standard menus, toolbar, sidebar and inspector patterns, sheets and popovers, window restoration, full screen and Stage Manager behaviour.
- Vibrancy and materials, system fonts and Dynamic Type equivalents, light, dark and increased contrast, VoiceOver.
- Keyboard-first expectations: standard shortcuts must keep their meaning.

## Linux
- Follow the conventions of the desktop environment the app targets (GNOME Human Interface Guidelines, KDE Human Interface Guidelines), state which, and test under both light and dark system themes and under Wayland and X11 where relevant.
- Header bar versus menu bar, client-side versus server-side decorations, system font and scaling (fractional scaling), Orca.

## iOS and iPadOS (Human Interface Guidelines)
- Navigation stack, tab bar, sheets, system gestures and swipe back, safe areas, Dynamic Type through the largest accessibility sizes, light and dark, VoiceOver and Voice Control, haptics used sparingly and meaningfully.
- iPad: size classes, multitasking and split view, pointer and keyboard support.

## Android (Material)
- Material components and theming (color roles, dynamic color if adopted, shape, type), top app bar, navigation bar or rail by window size class, predictive back, edge-to-edge and insets, font scaling, TalkBack and Switch Access.
- Foldables and large screens: window size classes, not device checks.

## Cross-platform stacks
- A shared UI toolkit draws its own controls: audit text input, selection, scrolling physics, context menus, accessibility tree exposure and IME behaviour on every platform before declaring a custom control equivalent.
- Record the deliberate platform differences in the table; "looks the same everywhere" is a decision with a cost, not a default.

## Every cell, ask
- Does it match the platform's expectation, or is the departure recorded with a reason?
- Does it work with the platform's accessibility API, text scaling and contrast settings?
- Can it be built in this stack without a custom control that loses native behaviour?
