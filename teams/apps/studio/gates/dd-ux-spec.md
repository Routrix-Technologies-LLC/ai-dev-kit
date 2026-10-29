> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# DD-UX-SPEC: UX Spec Review

Agent: `design-director`

**Trigger**: After `/app-ux` writes `docs/design/ux/<flow>.md`.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- UX spec path
- The feature spec(s) and requirement IDs the flow implements
- Design language path
- Accessibility notes and the content (copy) deck, if separate

**Prompt**:
> "Review this UX spec. Check:
> (1) Does the flow let the target user complete the spec's goal with the fewest steps and no dead ends? Trace the main path and one error path end to end.
> (2) Is every state specified for each screen: empty, loading, partial, success, error, offline, permission denied, first run, and long or localized content?
> (3) Is there a defined variant for each platform in `platforms` (input model, navigation idiom, window or screen size classes, system integrations like share sheets, menus, notifications, shortcuts), with differences justified?
> (4) Is accessibility designed in: reading and focus order, keyboard and switch operation, screen reader labels and roles, target sizes, motion alternatives, text scaling?
> (5) Does it use the design language's components and tokens, and flag any new component it needs rather than inventing one inline?
> (6) Does every requirement ID mapped to this flow have a visible place in it, and is any behavior specified here that no requirement asks for?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `DD-UX-SPEC: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the UX spec or the feature spec it implements.
