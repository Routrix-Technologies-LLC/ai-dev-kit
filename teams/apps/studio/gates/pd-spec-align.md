> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PD-SPEC-ALIGN: Spec Alignment Check

Agent: `product-director`

**Trigger**: After `/app-spec` finishes a feature spec (`docs/product/specs/<feature>.md`), and when `/app-spec-review` reviews one.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Path of the feature spec and its requirement IDs (`REQ-<feature>-NNN`) with count
- Path of the brief or vision, with its pillars and non-goals quoted
- Paths of neighboring specs that overlap this one, if any

**Prompt**:
> "Review this feature spec for fit with the product, not for completeness of detail. Check:
> (1) Does the feature serve a named pillar and a named target user, and can you point to the sentence in the vision that justifies it?
> (2) Does any requirement contradict a pillar or a non-goal? Quote the pair.
> (3) Is the scope bounded: does the spec say what is out of this version, and is anything quietly added that no user need supports (admin screens, settings, platform extras)?
> (4) Does the feature behave coherently on every platform the app targets, or does the spec silently assume one (for example hover, right-click, a file system, background execution, a keyboard)? Are intended platform differences stated?
> (5) Does it overlap or conflict with another spec or an existing feature, creating two ways to do one thing?
> (6) Is the user-visible outcome measurable against the success measure in the vision?
> Return ALIGNED, CONCERNS [list], or MISALIGNED [blockers]."

**Verdicts**: ALIGNED / CONCERNS / MISALIGNED

ALIGNED means no issues, proceed. CONCERNS means issues that do not block, listed. MISALIGNED means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PD-SPEC-ALIGN: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the spec file, or the vision or brief it is judged against.
