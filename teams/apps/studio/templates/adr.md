# ADR-[NNNN]: [Title, a short decision phrase]

<!--
WRITTEN BY: technical-director with the owning lead (platform, backend, security and so on). Skill: /app-adr (new, retrofit, accept); /app-stack drafts one when it adopts a framework. The section headings below are read by /app-adr (accept and retrofit modes) and by /app-plan: keep them exactly.
LIVES AT: docs/architecture/adr/ADR-NNNN-<slug>.md (override: paths.adr). Numbered in order, never renumbered, never deleted; a changed mind is a new ADR that supersedes this one. At minimal rigor, ADRs are replaced by short entries in docs/decisions.md.
RIGOR: minimal = not used (decision log entry).
       standard = Status, Date, Summary, Context, Decision, Alternatives (at least two real ones), Consequences, Requirements addressed, Validation, Rollback.
       full = every section, including the version risk table, performance and security implications, migration plan, and a Last Verified date refreshed at each stack upgrade.
GATE: TD-ADR (before the user is asked to accept). Record the outcome directly under the title as `> **Technical Director review (TD-ADR)**: <VERDICT> <date>`. Stories that depend on a Proposed ADR are Blocked until it is Accepted. Accept mode appends an `## Acceptance Record` section at the end.
Write for someone who joins in two years and must know why, not only what. State mandates as "must" and "must never" so they can be pulled into coding rules.
-->

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

> **Only `/app-adr accept`, after the user's explicit yes in the conversation, sets `Accepted`.** `technical-director` may advise but does not accept on its own. No other agent or skill sets it, and an agent that believes the ADR is ready says so and asks; it does not edit this field. New and retrofit modes always write `Proposed`.

## Date

[YYYY-MM-DD the decision was made or proposed]

## Last Verified

[YYYY-MM-DD this ADR was last re-read against the current stack versions (docs/stack-reference.md) and requirements and found still correct. Update the date when you confirm it, even if nothing changed.]

## Decision Makers

[Who decided: the user, technical-director, and who was consulted.]

## Summary

[Two sentences: the problem and the chosen approach. Name the system area, the problem and the approach specifically, so a reader scanning twenty ADRs can decide whether to read this one.]

## Platform and Version Risk

<!-- Where the decision depends on APIs, behaviors or versions that may be newer than a model's training data or are changing fast, record it, so that the decision is re-validated at upgrade time and an agent does not guess. Take versions from docs/stack-reference.md and the lock files. -->

| Field | Value |
|-------|-------|
| **Platform / framework and pinned version** | [e.g. runtime, UI framework, OS SDK, service version] |
| **Domain** | [UI / Data / Networking / Auth / Storage / Build / Packaging / Concurrency / Other] |
| **Layer** | [Foundation / Core / Feature / Presentation: how early in the build it must exist. Not the same as Domain.] |
| **Knowledge risk** | [LOW / MEDIUM / HIGH: how likely it is that documentation or training data is out of date for this area] |
| **References consulted** | [Official docs, changelogs, migration guides, with URLs and the date read] |
| **Newer-than-training APIs used** | [List, or "None"] |
| **Verification required before relying on it** | [Specific behavior to test on each target, or "None"] |

> If knowledge risk is MEDIUM or HIGH, re-validate this ADR whenever the pinned version changes; if the decision no longer holds, mark it Superseded and write a new ADR.

## ADR Dependencies

<!-- Write None only for a list you examined. If unknown, write UNKNOWN: accept mode refuses an ADR whose dependencies are absent, empty or UNKNOWN. -->

| Field | Value |
|-------|-------|
| **Depends on** | [ADR-NNNN that must be Accepted first, or "None"] |
| **Enables** | [ADR-NNNN or capability this unlocks, or "None"] |
| **Blocks** | [Epic or story that cannot start until Accepted, or "None"] |
| **Ordering note** | [Sequencing constraint not covered above] |

## Context

### Problem statement
[What must be decided, and why now. The forces in tension, stated neutrally.]

### Current state
[How it works today, and what is wrong with it. For a new area, say so.]

### Constraints
- [Technical, platform, timeline, resource, compatibility, licensing, regulatory]

### Requirements
- [Must support X (REQ ID or pillar)]
- [Must meet budget Y]

## Decision

[The decision in enough detail to implement: what is chosen, the boundaries, the key interfaces and the data shape. Say what is NOT included.]

### Diagram
[Text or Mermaid diagram of the structure this creates, if it helps.]

### Implementation Guidelines
- **Must:** [rule]
- **Must never:** [rule]

## Options Considered

<!-- At least two real alternatives, including "do nothing" or "keep the current approach" where plausible. A straw man is not an alternative. Be fair about each one's strengths. -->

### Alternative 1: [Name]
- **Description:** [how it would work]
- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **Relative effort:** [compared with the chosen approach]
- **Why not chosen:** [specific reason tied to the constraints]

### Alternative 2: [Name]
- **Description:**
- **Pros:**
- **Cons:**
- **Relative effort:**
- **Why not chosen:**

## Consequences

### Positive
- [Outcome]

### Negative
- [Cost and trade-off accepted knowingly]

### Neutral
- [Change that is neither good nor bad]

### Risks

| Risk | Likelihood and impact | Mitigation | Early warning sign |
|---|---|---|---|

## Requirements Addressed

<!-- Mandatory. Every ADR traces to at least one requirement, pillar, budget or constraint, or states that it is foundational. -->

| Source (spec, pillar, budget) | Requirement | How this decision satisfies it |
|---|---|---|

> If foundational with no direct requirement: "Foundational. Enables: [list what it unlocks or constrains]."

## Performance implications
- **CPU / startup:** [expected impact]
- **Memory:** [expected impact]
- **Size (binary, bundle, storage):** [expected impact]
- **Network and latency:** [expected impact, if applicable]
- **Measured how:** [method and target device, or "to be measured in story X"]

## Security and privacy implications
- **New trust boundary or attack surface:** [text, or "none"]
- **Data handled and its sensitivity:** [text]
- **Dependencies and licenses added:** [text]
- **Threat model / privacy review impact:** [update needed? link]

## Migration and Rollout
[From current state to this decision: steps, ordering, data migration (link the data-migration plan), what ships when, and what stays compatible meanwhile.]

**Rollback plan:** [How to revert if the decision proves wrong, up to which point it is cheap, and what makes it irreversible.]

## Validation Criteria
[How we will know the decision was right: tests, metrics against budgets, a prototype result, a review date. Include the signal that would make us reopen it.]

## Related
- [Superseded or related ADRs, with how they relate]
- [Specs, architecture sections, prototypes, code paths once implemented]
