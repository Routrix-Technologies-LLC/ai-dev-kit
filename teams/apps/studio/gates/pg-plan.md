> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PG-PLAN: Plan Feasibility Review

Agent: `program-director`

**Trigger**: After `/app-plan` breaks specs into epics and stories, and after `/app-sprint` drafts a sprint or batch plan.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Plan path(s): epic and story files or the sprint plan
- Capacity and the dates or batch size
- Story dependencies and statuses; risk register path
- QL-STORY-READY results for the stories, if run

**Prompt**:
> "Review this plan. Check:
> (1) Is the plan feasible at stated capacity, with must-have stories ahead of nice-to-have ones and a buffer for the unplanned?
> (2) Is the sequencing right: does anything start before its dependency (API contract, schema, design asset, decision, test harness) is done? Look for cycles and hidden dependencies.
> (3) Are stories small enough to finish and verify independently, with type, estimate, files and acceptance criteria present? Name oversized or vague ones.
> (4) Does risky work come early (new platform capability, migration, integrations, signing) rather than at the end?
> (5) Is each platform's work planned, including packaging, signing, store requirements and per-platform testing, or does the plan cover one target and assume the rest?
> (6) Does the plan leave room for review, hardening and release work, or does it schedule only features?
> Return REALISTIC, OPTIMISTIC [list], or UNREALISTIC [blockers]."

**Verdicts**: REALISTIC / OPTIMISTIC / UNREALISTIC

REALISTIC means no issues, proceed. OPTIMISTIC means issues that do not block, listed. UNREALISTIC means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PG-PLAN: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the plan files, or capacity.
