> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PG-MILESTONE: Milestone Risk Assessment

Agent: `program-director`

**Trigger**: At a milestone boundary or midpoint, from `/app-sprint` status mode, before `/app-gate` when the transition is a milestone, and whenever the user asks for an honest status.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Milestone definition: scope, date, exit criteria
- Status of its stories: done, in progress, blocked, not started (counts and IDs), with evidence of closure
- Velocity or throughput for the last several sprints or batches
- Risk register entries and open bugs by severity (S1 to S4)

**Prompt**:
> "Assess this milestone. Check:
> (1) Counting only stories closed through `/app-story-done` with evidence, what percentage of the milestone's scope is complete, and what remains against the remaining capacity?
> (2) Which risks have materialized, which are about to, and which have no owner or mitigation?
> (3) Does the open bug count and severity (any S1 or S2) fit the milestone's exit criteria, and is the trend improving?
> (4) Are there platform-specific stragglers (a target that lags in build, tests or native behavior) that could set the milestone date?
> (5) Are external dependencies (store reviews, certificates, third-party deliveries, user decisions) scheduled with margin?
> (6) If the milestone slips, what is the smallest cut or date move that restores it, and who must decide?
> Return ON TRACK, AT RISK [list], or OFF TRACK [blockers]."

**Verdicts**: ON TRACK / AT RISK / OFF TRACK

ON TRACK means no issues, proceed. AT RISK means issues that do not block, listed. OFF TRACK means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PG-MILESTONE: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no story status data, or no milestone definition. Status taken from claims rather than closed stories is a finding.
