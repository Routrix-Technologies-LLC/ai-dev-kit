> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PD-VISION: Vision and Pillars Check

Agent: `product-director`

**Trigger**: After the brief (`docs/product/brief.md`) or vision (`docs/product/vision.md`) is drafted by `/app-brief`, and after any change to the pillars or target users.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Path of the brief or vision, and whether it is a brief (minimal rigor) or a vision (standard, full)
- The stated pillars (or, in a brief, the 'what it is' and 'what it is not' lines) and the target users
- Research or domain notes the document cites (paths)

**Prompt**:
> "Review this brief or vision as the owner of what the product is. Check:
> (1) Is the problem real and specific, stated from the user's side, with evidence or a named assumption to test, rather than a solution looking for a problem?
> (2) Are the target users concrete enough to decide with (who, in what situation, on which devices and platforms), and does the platform list follow from where those users are?
> (3) Do the pillars (or the brief's principles) actually decide trade-offs? Name one plausible feature each pillar would reject; a pillar that rejects nothing is a slogan.
> (4) Is there an explicit non-goals list, and does it cut something tempting? Is the first version's boundary clear enough that scope creep can be named when it happens?
> (5) Is there a falsifiable success measure (a behavior or outcome, not a feature list), and can it be observed on every platform the app targets?
> (6) Do positioning and the competitive or comparable context hold up against sourced facts, or is the differentiation asserted?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PD-VISION: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the brief or vision file, or the target users section.
