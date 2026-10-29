> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# TD-PHASE-GATE: Technical Readiness at Phase Transition

Agent: `technical-director`

**Trigger**: At `/app-gate` for every stage transition (see the coverage table in `README.md`). Lean and full modes run it. Spawn in parallel with the other phase gates in the panel.

**Context to pass**:
- Current stage, target stage, `modes.rigor` and `modes.review`
- The required and recommended artifacts for this transition at this rigor, as listed by `/app-gate`
- Every artifact present, with file paths
- The `commands:` block from `studio.yaml`, and the most recent build, test and lint results with their dates
- Results of earlier gates recorded in document headers

**Prompt**:
> "Review the current state for readiness to enter [target stage], from the technical perspective, judged against what this transition requires at this rigor. Check:
> (1) Do the technical artifacts this transition requires exist with real content and agree with each other (architecture, ADRs, stack reference, API contracts)?
> (2) Does the code that exists build, test and run on every platform target, or only on the developer's machine? Cite the commands and results, not assertions.
> (3) Foundation onward: is there a walking skeleton or working path on each target, with CI green and the build reproducible?
> (4) Are technical risks and debt registered with owners, and does any open risk threaten the next stage (unproven platform capability, unpinned dependency, unreviewed foundation decision)?
> (5) Hardening onward: are the performance, reliability and size budgets measured on each target against `perf-budget.md`, and is the update and rollback path tested?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

> For a phase gate: a required artifact passed as "none" is a finding. A required artifact passed as "not expected before <stage>" or "not required at <rigor>" is not a finding. Rigor relaxes what must exist, never what must work: whatever artifacts and code do exist are judged on whether they work and agree with each other, at every rigor.

**Verdicts**: READY / CONCERNS / NOT READY

READY means no issues, proceed. CONCERNS means issues that do not block, listed. NOT READY means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `TD-PHASE-GATE: <VERDICT>` on its own line.
