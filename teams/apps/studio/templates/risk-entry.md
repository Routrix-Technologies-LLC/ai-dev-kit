<!--
Template: risk-entry. Written by: program-director (any agent may propose one). Skill: /app-sprint, /app-scope, /app-gate and /app-retro add or update entries.
Lives at: planning/risks.md (override: paths.risks), one section per risk, newest at the bottom, IDs stable and never reused.
Rigor: minimal = ID, description, mitigation, status. standard = adds probability, impact, owner, trigger, review date. full = adds contingency, cost of impact, linked stories and ADRs, history.
Copy the block below for each new risk and delete this comment from the register.
-->

## RISK-[NNNN]: [short title]

| Field | Value |
|---|---|
| Status | [Open / Mitigating / Accepted / Occurred / Closed] |
| Category | [Technical / Schedule / Scope / Security / Privacy / Legal / Platform or store policy / Dependency / Operational / People] |
| Raised | [YYYY-MM-DD by agent or person] |
| Owner | [one named owner] |
| Probability | [Low / Medium / High] |
| Impact | [Low / Medium / High] |
| Score | [probability x impact, 1 to 9] |
| Review by | [YYYY-MM-DD] |

**Description**: [If <condition>, then <consequence for users or the project>. One or two sentences, specific enough to be wrong.]

**Trigger / early warning**: [The observable sign that this is starting to happen.]

**Mitigation** (reduce likelihood or impact now): [Action, owner, due date.]

**Contingency** (what we do if it happens): [Plan B, and the point at which we switch.]

**Linked**: [stories, ADRs, bugs, milestones]

**History**
- [YYYY-MM-DD]: [raised, re-scored, mitigated, closed, and why]

Rules: an Accepted risk names who accepted it and when. A risk that occurred becomes an issue: open a bug or incident and keep the link. Closed risks stay in the file.
