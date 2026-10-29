> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# TD-ARCHITECTURE: Architecture Sign-Off

Agent: `technical-director`

**Trigger**: After `/app-architecture` drafts or revises `docs/architecture/architecture.md`, and after any major architecture revision.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Architecture document path
- The requirements baseline: spec paths and the quality attributes and budgets (performance, reliability, security, size, battery) the design must meet
- ADR list with statuses
- The stack reference path
- PE-FEASIBILITY and SL-THREAT-MODEL results, if already run

**Prompt**:
> "Review this architecture document for technical soundness. Check:
> (1) Is every spec requirement and every quality budget covered by a named component or decision? List any that no part of the design answers.
> (2) Are the containers, components and trust boundaries drawn at the right level (C4), with data ownership single and clear and each dependency pointing the right way?
> (3) Is each platform handled explicitly: what is shared, what is native or platform-specific, and how the seams (IPC, FFI, bridges, API) are typed and versioned? No platform may be covered by 'works the same'.
> (4) Are the hard parts addressed rather than deferred: data model and migration, offline and conflict handling, concurrency, auth, error and failure behavior, updates and rollback, observability?
> (5) Are foundation decisions each backed by an ADR, with alternatives, and are any foundation ADRs still Proposed or missing before implementation starts?
> (6) Are the choices proportionate to the app's size and team, or is there accidental complexity (premature services, abstraction layers with one implementation)?
> (7) Do the security and privacy boundaries match the threat model, and are the load-bearing assumptions stated?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `TD-ARCHITECTURE: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the architecture document or the requirements baseline.
