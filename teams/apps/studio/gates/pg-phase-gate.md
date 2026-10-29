> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PG-PHASE-GATE: Delivery Readiness at Phase Transition

Agent: `program-director`

**Trigger**: At `/app-gate` for every stage transition (see the coverage table in `README.md`). Lean and full modes run it. Spawn in parallel with the other phase gates in the panel.

**Context to pass**:
- Current stage, target stage, `modes.rigor` and `modes.review`
- The required and recommended artifacts for this transition at this rigor, as listed by `/app-gate`
- Every artifact present, with file paths
- Plans, sprint status, risk register and tech debt register paths
- Results of earlier gates recorded in document headers

**Prompt**:
> "Review the current state for readiness to enter [target stage], from the delivery perspective, judged against what this transition requires at this rigor. Check:
> (1) Do the planning artifacts this transition requires exist and reflect reality (stories, sprints, risks), and is the checkpoint in `.studio/state.md` current?
> (2) Is the next stage's work planned and sequenced, with capacity and dependencies known?
> (3) Are risks registered with owners and mitigations, and does any open risk or unresolved decision block the next stage?
> (4) Is the process healthy: are stories closing through the proper route with evidence, and are retros and tech debt being recorded rather than accumulating silently?
> (5) For hardening, release and operate: are the packaging, signing, store, hosting and rollback steps planned for every target platform, with owners and lead times?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

> For a phase gate: a required artifact passed as "none" is a finding. A required artifact passed as "not expected before <stage>" or "not required at <rigor>" is not a finding. Rigor relaxes what must exist, never what must work: whatever artifacts and code do exist are judged on whether they work and agree with each other, at every rigor.

**Verdicts**: READY / CONCERNS / NOT READY

READY means no issues, proceed. CONCERNS means issues that do not block, listed. NOT READY means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PG-PHASE-GATE: <VERDICT>` on its own line.
