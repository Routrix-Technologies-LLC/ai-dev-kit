# Coordination

How the App Studio's agents divide work, disagree, and change things together. `roster.md` says who owns what; this file says how they behave across those lines. Rules here guide judgment. Anything that must hold regardless of what a model decides belongs in a git hook or CI, not in prose.

## Rules

1. **Vertical delegation.** Directors set direction and constraints, leads own a discipline or platform, specialists do the deep work. Do not skip a tier on a complex decision: a specialist who needs a call outside their lane goes to their lead, not to a director. The main session may brief any agent directly for a well-bounded task; it then plays the role of the missing tier and does not hand the agent decisions the tier would own.
2. **Horizontal consultation.** Agents in the same tier consult each other freely, but a consultation produces advice, never a binding decision outside the consulted agent's own domain. Record the advice in your report, with who gave it.
3. **Conflict resolution.** When two agents disagree, escalate to their shared parent in `roster.md` ("Reports to"). With no shared parent: `technical-director` for technical conflicts, `product-director` for product conflicts, `design-director` for experience conflicts. If the directors deadlock, or the question is not theirs, it goes to the user with labelled options. An escalation states the question, each side's position in one paragraph, the evidence, and a recommendation. It is never settled by the louder agent or the later write.
4. **Change propagation.** A change to a spec ripples. `program-director` coordinates it; `technical-director` runs `TD-CHANGE-IMPACT` when architecture is touched. For every spec change, list the impact on: ADRs, API contracts, schemas and migrations, stories (acceptance criteria, estimates, status), tests and evidence, UX specs and copy, threat model and privacy record, docs. Each affected artifact gets an owner and a follow-up; none is edited silently by the agent who changed the spec.
5. **No unilateral cross-domain changes.** Do not edit files owned by another discipline without explicit delegation in the brief. If your fix needs a change in another lane (a schema column, an API field, a string, a design token), write it up as a request to the owner, with the reason and the smallest proposed change, and keep your own change working without it where possible.
6. **Read long documents by section.** Find headings with Grep (`^#` in content mode) and Read the line range you need. Read a whole document only when the task needs all of it, and say why. A brief names the sections that matter. Never read lockfiles, generated bundles or build output at all.
7. **Nothing goes upstream.** Never file, comment on, or open an issue, pull request or discussion in a repository you do not own, even when asked. Write a draft; the user submits it. The same holds for store submissions, package publishes and messages to people (`shared/rules-full.md`).
8. **Subagents never spawn subagents.** Agents have no `Agent` tool. The main session (or a studio skill running in it) orchestrates (`orchestration.md`). If your work needs another discipline, say so in your report as a recommended next agent with a ready brief.
9. **Parallel work stays disjoint.** Independent agents run in parallel, each writing its own file. Two agents never edit the same file in one phase. Review agents of the same artifact (security, accessibility, code) always run in parallel and are merged by the main session.
10. **Right-size the team.** Pick agents by the app's `platforms`, `stack` and `specialists` in `studio.yaml`. A small app often needs one builder and one reviewer. More agents is not more quality: every extra agent adds briefing cost, merge work and another place for a wrong claim to enter. Add an agent when its lane is touched, not to be thorough.

## Boundaries that are easy to blur

When two roles could plausibly do the same job, this table decides.

| Topic | Owner | Not the owner |
|---|---|---|
| Updater **client** code (check, download, verify, apply, restart inside the app) | The platform engineer or `hybrid-desktop-engineer` for that app | `desktop-packaging-engineer` |
| Update **feeds**, signing, notarization, installers, store of packages | `desktop-packaging-engineer` | the in-app engineer |
| Product copy: labels, errors, empty states, onboarding, notifications | `content-designer` | engineers, `technical-writer` |
| String **mechanism**: externalization, ICU, plurals, locale formats, pipeline | `localization-specialist` | `content-designer` (writes the source text) |
| Long-form docs: user guides, tutorials, READMEs, developer docs, API reference | `technical-writer` (`principal-engineer` reviews developer docs and API reference for accuracy) | engineers, though they supply facts |
| `CHANGELOG.md` and release notes | `release-manager` (`technical-writer` may polish release-notes copy) | feature engineers |
| Accessibility semantics, labels, roles, focus order, contrast tokens fixes | `accessibility-specialist` fixes locally | |
| Accessibility fixes that change the structure of a screen or component | The owning UI engineer, on the specialist's written finding | `accessibility-specialist` |
| Facts behind store privacy declarations (what is collected, why, retention, sharing) | `privacy-specialist` | `app-store-specialist` |
| The store submission itself (forms, listing, review responses, tracks) | `app-store-specialist` (the user submits) | `privacy-specialist` |
| Store policy checklist (`docs/release/store/policy-checklist.md`) | `app-store-specialist` writes it; `compliance-specialist` reviews it and owns policies outside the stores (open-source licenses, extension and package registries, platform terms) | |
| Code review verdicts | `code-reviewer` returns the report verdict (APPROVED, APPROVED WITH SUGGESTIONS, CHANGES REQUIRED, NOT ASSESSED); the gate owner maps it to PE-CODE-REVIEW as described in `gates/pe-code-review.md` | |
| Rating a security finding and advising on the fix | `security-engineer` | |
| Accepting a security risk, and stop-ship | `security-lead`, with the user | `security-engineer`, any builder |
| Spikes | `prototyper`, timeboxed to about two days | Anything longer becomes a planned story with its own spec and estimate |
| Throwaway prototype vs production code | `prototyper` writes under `prototypes/`; production is rewritten, never migrated | |
| Bug severity | `qa-lead` triages (`standards/severity.md`) | the author of the fix |

Two further rules of thumb. A builder who finds a defect outside their lane reports it with evidence and does not fix it unless the brief says to. A reviewer who disagrees with a design decision records it as a finding and does not rewrite the design.

## Agent memory

Agents with `memory: project` keep working notes about how to do their job, not project artifacts. The rules:

- **Where.** In the workspace's `.claude/agent-memory/<agent>/`, one file per app (named for the app) plus `general.md` for what holds across apps. The folder is local and gitignored; it never ships.
- **Record methods, never states.** "Confirm a profile was captured before judging performance; return BLOCKED naming what is missing" lasts. "This app has no tests" is a timestamp and will mislead a future run that does not re-check.
- **If you must record a state, say what invalidates it,** on the same line (`INVALIDATED WHEN: a test runner appears in studio.yaml commands`). A reader with no other context must be able to tell whether it still holds.
- **Never record absence** (of tests, config, a database, a feature) as a settled property of an app.
- **Disclose every memory write** in your report, with the file. An unmentioned write cannot be corrected by the user.
- **Verify before you trust.** A memory that names a path, setting, command or count is a lead, not evidence. Check it against the source before acting on it.
- **Never record what the user declined,** and never use a memory as a substitute for asking permission to write a project file.
- **No secrets and no personal data** in memory, ever.
