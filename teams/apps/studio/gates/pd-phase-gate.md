> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PD-PHASE-GATE: Product Readiness at Phase Transition

Agent: `product-director`

**Trigger**: At `/app-gate` for every stage transition (see the coverage table in `README.md`). Lean and full modes run it. Spawn in parallel with the other phase gates in the panel.

**Context to pass**:
- Current stage, target stage, `modes.rigor` and `modes.review`
- The required and recommended artifacts for this transition at this rigor, as listed by `/app-gate`
- Every artifact present, with file paths
- The product pillars, target users and non-goals (quoted)
- Results of earlier gates on the artifacts (the header lines recorded in the documents)

**Prompt**:
> "Review the current state for readiness to enter [target stage], from the product perspective, judged against what this transition requires at this rigor. Check:
> (1) Do the artifacts that exist still serve the pillars and the target users, or has the product drifted since the vision was approved?
> (2) For the transition's stage: definition needs a bounded first version with specs a builder could start from; build needs accepted work that matches the specs; hardening and release need the shipped behavior to match what was promised. Does the evidence show this?
> (3) Is scope under control: what has been added, cut or deferred since the last transition, and was each change a decision someone made?
> (4) Across the platforms the app targets, is the product experience at a comparable quality bar, or is one platform an afterthought the vision does not sanction?
> (5) Are open product questions and assumptions recorded, with an owner and a date, and does none of them invalidate the next stage's work?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

> For a phase gate: a required artifact passed as "none" is a finding. A required artifact passed as "not expected before <stage>" or "not required at <rigor>" is not a finding. Rigor relaxes what must exist, never what must work: whatever artifacts and code do exist are judged on whether they work and agree with each other, at every rigor.

**Verdicts**: READY / CONCERNS / NOT READY

READY means no issues, proceed. CONCERNS means issues that do not block, listed. NOT READY means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PD-PHASE-GATE: <VERDICT>` on its own line.
