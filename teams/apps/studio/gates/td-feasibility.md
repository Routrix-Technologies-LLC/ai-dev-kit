> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# TD-FEASIBILITY: Technical Feasibility

Agent: `technical-director`

**Trigger**: At `/app-spec` in full review mode for specs with technical uncertainty, at `/app-brief` when the idea depends on a hard capability, and before `/app-prototype` picks its question.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- The brief, vision or spec path, and the specific capabilities it relies on
- Known constraints: `min_targets`, performance or battery expectations, offline needs, team and time limits
- Existing architecture or stack reference paths, if any
- Prototype reports, if any exist

**Prompt**:
> "Review this concept or spec for technical feasibility. Check:
> (1) What are the three largest technical unknowns (a capability that may not exist on a target platform, a performance ceiling, a third-party limit, a hard real-time or offline need)? For each, say what would resolve it and how cheaply.
> (2) Does every platform in the target list actually offer what the feature needs, at the oldest supported version and in the permission or sandbox model it runs under (browser, OS app sandbox, mobile background limits, server limits)?
> (3) Do any requirements imply an architecture the stack cannot deliver (real-time sync, on-device models, background work, large local data, native integrations from a web stack)?
> (4) Are there dependencies on external services, APIs, licenses or store policies that could be withdrawn, priced up or rejected, and is the fallback stated?
> (5) Is any risk large enough that a time-boxed prototype should run before this is committed to?
> (6) Is the effort order of magnitude plausible against the team's capacity (flag, do not estimate in detail)?
> Return VIABLE, CONCERNS [list], or HIGH RISK [blockers]."

**Verdicts**: VIABLE / CONCERNS / HIGH RISK

VIABLE means no issues, proceed. CONCERNS means issues that do not block, listed. HIGH RISK means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `TD-FEASIBILITY: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the document under review, or the target platform list.
