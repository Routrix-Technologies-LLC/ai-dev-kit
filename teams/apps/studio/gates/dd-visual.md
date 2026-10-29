> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# DD-VISUAL: Implemented Visual Review

Agent: `design-director`

**Trigger**: After `/app-ux-review`, and in full mode when a story of change type UI or Visual is closing. Evidence must come from a real run of the build.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Screenshots or captures, with paths, per platform and per theme (light, dark, high contrast) and size class
- The UX spec and design language paths
- The run-and-observe line (`Run result:`) for the change
- Accessibility check output, if any

**Prompt**:
> "Review the implemented UI against its specification. Check:
> (1) Does each screen in the evidence match the UX spec in layout, hierarchy, states and copy? List every deviation with the spec line it contradicts.
> (2) Do tokens, type, color, spacing and components match the design language, or are there hard-coded values and one-off components?
> (3) Is the quality consistent across every platform in `platforms` and every theme in the evidence, and does each platform feel native where the design language says it should?
> (4) Are layout, truncation, scaling and window or orientation behavior correct at the extremes (smallest and largest size class, long strings, large text settings)?
> (5) Are focus indication, contrast and target sizes visible in the captures?
> (6) Is the evidence sufficient: does it cover every changed screen and state, from the real build, not a mock? An unobserved platform or theme is a gap, not a pass.
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `DD-VISUAL: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no captures from a real run, or no spec to compare against.
