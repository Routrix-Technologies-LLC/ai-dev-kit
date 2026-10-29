> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# DD-DESIGN-LANGUAGE: Design Language Sign-Off

Agent: `design-director`

**Trigger**: After `/app-design-language` drafts or revises `docs/design/design-language.md`.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Design language path
- Vision pillars and target users (quoted)
- Accessibility requirements (target WCAG level) and the platforms' native conventions the app intends to follow or deliberately depart from
- UX specs that already use the language, if any

**Prompt**:
> "Review this design language. Check:
> (1) Does it express the product's pillars and audience, with a clear point of view, rather than a generic kit? Say what makes it recognizably this product.
> (2) Are tokens complete and systematic (color roles, type scale, spacing, radius, elevation, motion) with names that describe purpose, not appearance, and values defined for light, dark and high contrast?
> (3) Do the color pairs meet contrast requirements (WCAG 2.2 AA at minimum) for text and for non-text UI, in every theme, with focus indication that is visible?
> (4) For each platform in `platforms`, is it stated what adapts (navigation patterns, controls, density, input method, window or safe-area behavior, system fonts) and what stays consistent? Is there a rule for when to follow the platform guideline (Apple HIG, Fluent, Material, web conventions) and when to depart?
> (5) Is each component specified with its states (default, hover, focus, pressed, disabled, loading, error, empty) and sizing for touch and pointer targets?
> (6) Is it implementable: can engineers map tokens to the stack's theming mechanism, and does it avoid values that cannot be produced consistently across targets?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `DD-DESIGN-LANGUAGE: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the design language document or the vision it must express.
