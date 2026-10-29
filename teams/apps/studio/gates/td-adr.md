> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# TD-ADR: ADR Review

Agent: `technical-director`

**Trigger**: After `/app-adr` drafts or retrofits an ADR and before the user is asked to accept it (the only route to Accepted).

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- ADR path and its current status
- The architecture document path and the ADRs it relates to or supersedes
- The stack reference path
- Constraints the decision must satisfy (budgets, platforms, licenses, team skills)

**Prompt**:
> "Review this ADR as the person who must live with it for years. Check:
> (1) Is the decision stated as one clear choice, in the present tense, with the context and forces that made it necessary?
> (2) Were real alternatives considered (at least two beyond the pick, including 'do nothing' where it applies) and rejected for stated reasons, not strawmen?
> (3) Are the consequences honest: what gets harder, what it costs on each target platform, what it forecloses, and how it would be reversed or migrated away from?
> (4) Does it conflict with, silently supersede or duplicate another ADR or the architecture document? Is the supersession recorded?
> (5) Is it verifiable: what test, budget or review would show the decision is working or has failed, and when it should be revisited?
> (6) Are the claims about versions, APIs and licenses sourced and current, per the stack reference?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `TD-ADR: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the ADR file, or the architecture document it must be consistent with.
