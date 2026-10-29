> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# DD-PHASE-GATE: Design Readiness at Phase Transition

Agent: `design-director`

**Trigger**: At `/app-gate` for every stage transition where the table in `README.md` lists it. Lean and full modes run it. Spawn in parallel with the other phase gates in the panel.

**Context to pass**:
- Current stage, target stage, `modes.rigor` and `modes.review`
- The required and recommended artifacts for this transition at this rigor, as listed by `/app-gate`
- Every artifact present, with file paths
- Design language and UX spec paths; latest UX review and accessibility audit paths, if any
- Results of earlier gates recorded in document headers

**Prompt**:
> "Review the current state for readiness to enter [target stage], from the design perspective, judged against what this transition requires at this rigor. Check:
> (1) Do the design artifacts this transition requires exist and agree with each other (design language, UX specs, copy), and do they cover the key flows of the first version?
> (2) Where UI exists, does it follow the design language and UX specs on each platform, with evidence from a real run?
> (3) Is accessibility on track for the target level: has it been designed in, audited where the transition requires it, with open failures tracked?
> (4) Is the experience consistent across the platforms the app targets, with the platform differences the design language allows and no others?
> (5) Do the words in the product (labels, errors, empty states) have an owner and a voice, and is localization readiness considered if more than one locale is planned?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

> For a phase gate: a required artifact passed as "none" is a finding. A required artifact passed as "not expected before <stage>" or "not required at <rigor>" is not a finding. Rigor relaxes what must exist, never what must work: whatever artifacts and code do exist are judged on whether they work and agree with each other, at every rigor.

**Verdicts**: READY / CONCERNS / NOT READY

READY means no issues, proceed. CONCERNS means issues that do not block, listed. NOT READY means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `DD-PHASE-GATE: <VERDICT>` on its own line.
