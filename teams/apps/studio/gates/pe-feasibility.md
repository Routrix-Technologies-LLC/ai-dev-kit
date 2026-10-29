> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PE-FEASIBILITY: Implementation Feasibility

Agent: `principal-engineer`

**Trigger**: After the architecture document is drafted and before TD-ARCHITECTURE, and before an epic is broken into stories when the design is new.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Architecture document and ADR paths
- Stack reference and the existing code layout (module map), if code exists
- Prototype reports, if any
- Team skills and specialists available (`specialists:`)

**Prompt**:
> "Review the architecture for implementability. Check:
> (1) Can each component and boundary be built as drawn with the pinned stack, on each platform target? Name any that need a capability, API or library behavior you could not confirm.
> (2) Are module boundaries and internal APIs clear enough that two engineers could build against them without meeting?
> (3) Where code exists, how large is the gap between the design and the current code, and is the migration path incremental and safe?
> (4) Which parts are the riskiest to implement (concurrency, native bridges, sync, packaging), and what is the smallest early slice that proves them?
> (5) Is the design testable: seams for fakes, deterministic time and IO, a way to run each platform target in CI or headless?
> (6) Does the effort distribution match the skills available, and are there single-person dependencies?
> Return VIABLE, CONCERNS [list], or HIGH RISK [blockers]."

**Verdicts**: VIABLE / CONCERNS / HIGH RISK

VIABLE means no issues, proceed. CONCERNS means issues that do not block, listed. HIGH RISK means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PE-FEASIBILITY: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the architecture document, or the stack reference.
