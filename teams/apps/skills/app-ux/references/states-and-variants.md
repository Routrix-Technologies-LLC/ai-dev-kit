# app-ux: state catalog and variant checklists

Loaded by `/app-ux` in Phases 1 to 3. Each state either gets a row in the screen's state table (section 4 of the spec) or "N/A: <why>".

## State catalog

| Group | States to consider |
|---|---|
| Data | Default with typical data; empty because new (first run); empty because filtered or searched (no results); one item; very many items; very long text, very large numbers, missing optional fields; stale data; partially loaded |
| Loading | Initial load; refresh with existing content visible; incremental load (paging, infinite scroll); long-running with progress; indeterminate wait; cancelled |
| Errors | Field validation; form-level validation; network unreachable; timeout; server error; not found; permission denied or signed out; quota or rate limit; conflict (changed elsewhere); unsupported environment (old OS, missing capability); unexpected failure with a recovery path |
| Connectivity | Offline with cached content; offline without content; reconnecting; sync pending; sync conflict |
| Authorization | Signed out; session expired mid-task; role without access (hidden versus disabled versus explained); first-time permission request; permission denied by the user; permission revoked while running |
| Interaction | Hover and focus; pressed; selected; disabled (with the reason available); read-only; drag in progress; multi-select; undo available; destructive confirmation; success confirmation |
| Lifecycle | First run and onboarding; returning user; interrupted (backgrounded, window closed, device rotated, low memory, app killed and restored); update available; maintenance |
| Content | Right-to-left; longest translation; text scaled to the platform maximum; user-generated content with hostile characters or no text |

For each row record: trigger, what the user sees, what they can do next, the copy key, and how they get back to the default state. Destructive actions need an undo or a confirmation that names what will be lost.

## Variant checklists

### Web
- Layout at each named breakpoint; what collapses, reflows or hides, and how hidden things stay reachable.
- 200 percent zoom and 320 CSS pixel width reflow without two-dimensional scrolling (WCAG 2.2 reflow).
- Hover-only information has a keyboard and touch equivalent; pointer targets meet the minimum target size of WCAG 2.2.
- Back button, refresh, deep link and shared URL behaviour; browser autofill on forms.
- Reduced motion, dark scheme, forced colors.

### Desktop
- Minimum window size and what happens below it; resize behaviour of every region; restore of last size and position.
- Keyboard: every action reachable, documented shortcuts that do not collide with the OS, menu mnemonics where the platform uses them.
- Pointer: context menus, drag and drop, double-click behaviour, scroll and zoom gestures on trackpads.
- Multi-window and multi-monitor; mixed DPI when a window moves between monitors; full screen.
- Native conventions: Windows (Fluent), macOS (Human Interface Guidelines: menu bar, toolbar, sidebar, sheets), Linux (GNOME or KDE conventions as the app targets). State deliberately where the app departs from them.
- High contrast or increased contrast mode; system text size changes.

### Mobile
- Phone and tablet layouts; portrait and landscape; safe areas, notches and keyboard avoidance.
- Text scaling to the platform's largest accessibility size without truncation of essential content.
- Gestures always have a visible alternative; system back and swipe-back behave predictably; no gesture conflicts with system edges.
- Permission flow: the pre-prompt explanation, the system prompt, the denied state and the path to settings.
- Interruptions: calls, notifications, backgrounding, low power, no connectivity; state restored on return.
- Platform idioms: iOS (navigation stack, tab bar, sheets) and Android (top app bar, navigation bar or rail, predictive back), unless a cross-platform stack deliberately unifies them (record that choice).

### CLI
- Every command: synopsis, arguments, defaults, interactive prompts and their non-interactive flags.
- Output for success, failure, no results; machine-readable mode; color and unicode off; narrow terminal.
- Exit codes and their meaning; error text says what happened and what to do.
- Long-running work: progress, interruption (Ctrl-C) behaviour, resumability.

### Extension
- Each surface (popup, panel, options, injected UI); first-run permission explanation; behaviour when the host page changes or blocks the injection.
