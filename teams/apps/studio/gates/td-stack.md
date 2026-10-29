> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# TD-STACK: Stack and Dependency Decision

Agent: `technical-director`

**Trigger**: After `/app-stack` produces its stack reference and ADR draft, and before adopting any framework, runtime, SDK or major library.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- The candidates, the recommendation and the evaluation table
- Stack reference path with verified versions and the source of each
- Requirements and budgets the stack must meet, and `min_targets`
- License, security and maintenance findings from compliance-specialist and security-engineer
- Prototype evidence, if any

**Prompt**:
> "Review this stack or dependency decision. Check:
> (1) Does the choice meet the requirements and budgets on every platform the app targets, at the oldest supported version, with evidence rather than reputation?
> (2) Is the project healthy: maintained, released recently, responsive to security reports, with a bus factor above one and a stable API policy? What is the exit cost if it is abandoned?
> (3) Is the license compatible with the app's distribution (store terms, closed-source shipping, copyleft reach) and are transitive licenses checked?
> (4) Are the pinned versions verified from official sources, with known breaking changes and deprecations since the pin listed?
> (5) Does it fit the team's skills and the existing stack, or does it add a second way to do something already solved? Is the build, signing and packaging story proven on each target?
> (6) What are the supply chain and security properties: provenance, size of the dependency tree, install-time scripts, known advisories?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `TD-STACK: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the candidate list or the stack reference. ADOPT, TRIAL and REJECT in the skill map to APPROVE, CONCERNS and REJECT here.
