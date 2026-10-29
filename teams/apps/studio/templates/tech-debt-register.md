<!--
Template: tech-debt-register. Written by: principal-engineer with modernization-engineer and code-reviewer. Skill: /app-tech-debt; /app-story-done adds rows for accepted shortcuts.
Lives at: planning/tech-debt.md (override: paths.tech_debt). One table, rows appended, IDs stable and never reused or renumbered.
Rigor: minimal = id, area, description, status. standard = adds impact, cost to fix, interest, owner, source. full = adds paydown plan with stories and a quarterly review log.
Delete this comment when the register is created.
-->

# Tech debt register

> **Last reviewed**: [YYYY-MM-DD]
> **Open rows**: [n of n total]   **Paydown budget**: [for example 15 percent of each sprint, or none]

## How to read this

- **Impact**: what the debt costs the product or the team today. Use High when it causes user-visible bugs, security exposure or blocks work; Medium when it slows work or raises defect rates; Low when it is untidy but harmless.
- **Cost to fix**: S (under a day), M (days), L (a week or more; split into stories).
- **Interest**: how fast it gets worse if left alone. High = every new feature on this code makes it worse; Medium = grows with time or with dependency drift; Low = static.
- **Status**: Open, Planned (has a story), In progress, Paid, Accepted (a conscious, dated decision to live with it), Dropped (no longer relevant, with reason).
- Priority is roughly impact times interest, divided by cost. Security debt is never Accepted without security-lead.

## Register

| ID | Area | Description | Impact | Cost to fix | Interest | Owner | Status | Source |
|---|---|---|---|---|---|---|---|---|
| TD-001 | [module or layer, platform] | [What is wrong and what it costs, with file:line or path] | [High/Med/Low] | [S/M/L] | [High/Med/Low] | [agent or person] | [Open] | [story-NNN review, audit date, bug ID, or ADR] |

## Paydown plan

| Row | Planned story | Target sprint or release | Notes |
|---|---|---|---|
| [TD-NNN] | [story path] | [id] | [sequencing constraints] |

## Review log

| Date | Reviewer | Rows added | Rows paid or dropped | Decisions |
|---|---|---|---|---|

Rules: a shortcut taken on purpose gets a row the same day, with the reason. Do not delete paid rows; mark them Paid with the date and story.
