> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PG-SCOPE: Scope and Capacity Check

Agent: `program-director`

**Trigger**: At `/app-scope`, and when `/app-plan` or `/app-sprint` finds the plan is larger than the last estimate.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Planned scope: epics, stories or specs with estimates
- Capacity: people or agents available, time window, and velocity from recent sprints if known
- Brief or vision with the first-version boundary
- The risk register path

**Prompt**:
> "Review the scope against capacity and the brief. Check:
> (1) Does the planned work fit the capacity in the window, with a buffer for integration, bug fixing and review? Show the arithmetic from the inputs given.
> (2) Is everything in scope traceable to the brief's first version, and what has crept in since (list items with no trace)?
> (3) Are estimates grounded in evidence (past velocity, prototype results) or guessed, and which items carry the widest uncertainty?
> (4) Do the platforms multiply the work: is the cost of each additional target (build, signing, store review, testing, native behavior) in the estimate?
> (5) If it does not fit, are the proposed cuts ordered by distance from the pillars, with what each cut saves?
> (6) Which dependencies outside the team's control (store review, certificates, third parties, user decisions) sit on the critical path?
> Return REALISTIC, OPTIMISTIC [list], or UNREALISTIC [blockers]."

**Verdicts**: REALISTIC / OPTIMISTIC / UNREALISTIC

REALISTIC means no issues, proceed. OPTIMISTIC means issues that do not block, listed. UNREALISTIC means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PG-SCOPE: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no estimates, or no stated capacity.
