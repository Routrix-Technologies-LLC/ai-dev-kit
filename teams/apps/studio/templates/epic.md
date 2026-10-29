<!--
Template: epic. Written by: product-manager (stories listed by principal-engineer and qa-lead). Skill: /app-plan.
Lives at: planning/epics/<epic>/epic.md (override: paths.epics). Stories sit beside it as story-NNN-<slug>.md.
Rigor: minimal = title, goal, story list. standard = adds scope, specs, ADRs, done definition, risks. full = adds milestone link, capacity, cross-epic dependencies, rollout plan.
Delete this comment when the epic is created. Never renumber existing stories.
-->

# Epic: [epic name]

> **Status**: [Planned | In Progress | Complete | Blocked: reason]
> **Stage**: [build | hardening | ...]
> **Owner**: [agent or person]
> **Milestone / release**: [version or milestone, or none]
> **Last updated**: [YYYY-MM-DD]

## Goal

[One paragraph: the user-visible outcome this epic delivers and why it matters now. State it so a stranger can tell whether it is finished.]

## Specs and decisions

| Source | Path | Requirement IDs covered |
|---|---|---|
| Feature spec | `docs/product/specs/[feature].md` | [REQ-feature-001 to REQ-feature-009] |
| UX spec | `docs/design/ux/[flow].md` | [screens or states] |
| ADR | `docs/architecture/adr/ADR-[NNNN]-[slug].md` | [Accepted ADRs only; note version stamp] |

Every requirement in the spec is covered by at least one story below, or listed under "Deferred".

## Platforms affected

[web | windows | macos | linux | ios | android | backend | cli | extension | library]. Note any platform that gets the feature later and why.

## Scope

**In scope**
- [item]

**Out of scope**
- [item, and which epic or backlog entry owns it]

## Stories

| # | Story | Layer or area | Change type | Estimate (S/M/L) | Depends on | Status |
|---|---|---|---|---|---|---|
| 001 | [`story-001-[slug].md`](story-001-[slug].md) | [area] | [Logic/Integration/UI/Visual/Data/Config/Infra/Security/Performance/Docs] | [S/M/L] | [none or story IDs] | [Ready] |

Order stories so each one leaves the app working. Foundations and risky unknowns first.

## Definition of done for the epic

- [ ] All stories Complete (closed through /app-story-done, not by hand)
- [ ] Every REQ ID above has passing evidence
- [ ] Docs updated (specs, user docs, CHANGELOG entry drafted)
- [ ] No open S1 or S2 bugs against this epic
- [ ] [epic-specific check: for example performance budget met on each platform]

## Risks

| Risk | Likelihood | Impact | Mitigation | Register ID |
|---|---|---|---|---|
| [risk] | [L/M/H] | [L/M/H] | [action] | [RISK-NNNN or none] |

## Deferred

[Requirements or ideas consciously left out, with the reason. An empty list is fine; a missing section is not.]
