# Studio gates

A gate is a named review that one owner agent runs on one artifact or one stage transition and answers with a fixed verdict word. Skills reference gate IDs; the definition (trigger, context to pass, prompt, verdicts) lives in one file per gate in this folder, named after the ID in lowercase.

**How a skill runs a gate.** The skill spawns the owner agent with the gate ID and the context fields the definition lists, and tells the agent to read this folder's `<id-lowercase>.md` first (installed as `~/.claude/studio/gates/`). The orchestrating session must not read the gate file for the agent: the agent reads it in its own context. See `orchestration.md` sections 7 and 8 and `shared/gates.md`.

## Gate index

| Gate ID | Owner agent | Purpose | Trigger skill | Definition |
|---|---|---|---|---|
| `PD-VISION` | `product-director` | Stress-test the brief or vision: problem, users, pillars, non-goals. | `app-brief` | `pd-vision.md` |
| `PD-SPEC-ALIGN` | `product-director` | Confirm a feature spec serves the pillars and target users and stays in scope. | `app-spec`, `app-spec-review` | `pd-spec-align.md` |
| `PD-PHASE-GATE` | `product-director` | Product-level readiness to leave one stage and enter the next. | `app-gate` | `pd-phase-gate.md` |
| `TD-FEASIBILITY` | `technical-director` | Judge whether a concept or spec can be built within the likely constraints and surface the biggest unknowns. | `app-spec` | `td-feasibility.md` |
| `TD-ARCHITECTURE` | `technical-director` | Sign off the architecture document as sound, complete and buildable. | `app-architecture` | `td-architecture.md` |
| `TD-ADR` | `technical-director` | Review one Architecture Decision Record before it can be Accepted. | `app-adr` | `td-adr.md` |
| `TD-STACK` | `technical-director` | Review a stack choice, framework adoption or significant dependency before it is adopted. | `app-stack` | `td-stack.md` |
| `TD-CHANGE-IMPACT` | `technical-director` | Review an impact assessment for a change to an approved spec, ADR or architecture. | `app-spec` (and any skill changing an approved spec, ADR or architecture) | `td-change-impact.md` |
| `TD-PHASE-GATE` | `technical-director` | Technical readiness to leave one stage and enter the next. | `app-gate` | `td-phase-gate.md` |
| `DD-DESIGN-LANGUAGE` | `design-director` | Sign off the design language: tokens, type, color, components, theming, platform adaptation. | `app-design-language` | `dd-design-language.md` |
| `DD-UX-SPEC` | `design-director` | Review a UX spec for a flow or screen group: states, platform variants, accessibility. | `app-ux` | `dd-ux-spec.md` |
| `DD-VISUAL` | `design-director` | Review the built UI against the UX spec and design language, from evidence. | `app-ux-review`, `app-team-ui`, `app-story-done` (full mode) | `dd-visual.md` |
| `DD-PHASE-GATE` | `design-director` | Design and experience readiness to leave one stage and enter the next. | `app-gate` | `dd-phase-gate.md` |
| `PG-SCOPE` | `program-director` | Validate that planned scope fits capacity and the brief, and find creep. | `app-scope` | `pg-scope.md` |
| `PG-PLAN` | `program-director` | Review an epic breakdown or sprint plan for feasibility, sequencing and risk. | `app-plan`, `app-sprint` | `pg-plan.md` |
| `PG-MILESTONE` | `program-director` | Assess whether a milestone is on track and what threatens it. | `app-sprint` (status mode) | `pg-milestone.md` |
| `PG-PHASE-GATE` | `program-director` | Delivery readiness to leave one stage and enter the next. | `app-gate` | `pg-phase-gate.md` |
| `PM-ACCEPTANCE` | `product-manager` | Verify a finished story meets each acceptance criterion and its spec. | `app-story-done` | `pm-acceptance.md` |
| `PE-FEASIBILITY` | `principal-engineer` | Judge whether the architecture can be implemented as designed, in the codebase and with the team's skills. | `app-architecture` | `pe-feasibility.md` |
| `PE-CODE-REVIEW` | `principal-engineer` | Review implemented code for correctness, standards and architecture fit. | `app-story-done`, `app-code-review`, `app-dev-story` | `pe-code-review.md` |
| `QL-STORY-READY` | `qa-lead` | Check a story, epic or sprint is testable and complete enough to start. | `app-plan`, `app-story-ready`, `app-qa-plan`, `app-team-feature` | `ql-story-ready.md` |
| `QL-TEST-COVERAGE` | `qa-lead` | Review the tests and evidence for one story before it closes. | `app-story-done` | `ql-test-coverage.md` |
| `QL-RELEASE-QUALITY` | `qa-lead` | Decide whether the quality of a release candidate meets the bar. | `app-release`, `app-team-release`, `app-team-harden` | `ql-release-quality.md` |
| `SL-THREAT-MODEL` | `security-lead` | Review the threat model for completeness and the quality of its mitigations. | `app-threat-model` | `sl-threat-model.md` |
| `SL-SECURITY-REVIEW` | `security-lead` | Judge the security audit or pre-release security posture; stop-ship authority. | `app-security-audit`, `app-release`, `app-team-release`, `app-team-harden` | `sl-security-review.md` |
| `SL-PRIVACY` | `security-lead` | Judge the data inventory, flows, retention, consent and store privacy declarations. | `app-privacy-review`, `app-release`, `app-store-prep`, `app-team-release`, `app-team-harden` | `sl-privacy.md` |
| `RM-RELEASE-READY` | `release-manager` | Final go/no-go on the release mechanics: package, signing, notes, rollout, rollback. | `app-release`, `app-hotfix`, `app-team-release` | `rm-release-ready.md` |

Each definition file lists the exact spawning skills in its **Trigger** line. Skills named in the catalog (`skill-authoring.md`) own the gates they run; `TD-CHANGE-IMPACT` and `PG-MILESTONE` have no dedicated skill and are run by the skills named in their definitions.

## Review modes

The mode comes from `modes.review` in `studio.yaml`, or follows `modes.rigor` when unset (minimal gives solo, standard gives lean, full gives full). A skill's `--review solo|lean|full` argument overrides it for that run only. Apply the mode before every gate spawn.

| Mode | What runs | What is printed for the rest |
|---|---|---|
| `solo` | No gate runs. | `<GATE-ID> skipped: solo mode` |
| `lean` | Only the four phase gates (`PD-PHASE-GATE`, `TD-PHASE-GATE`, `DD-PHASE-GATE`, `PG-PHASE-GATE`, run only by `/app-gate`) plus the always-on gates below. Every other gate is skipped. | `<GATE-ID> skipped: lean mode` |
| `full` | Every gate the skill names. | nothing skipped |

**Always-on in lean mode** (they are the last checks before users are affected, so they never depend on being at full):

| Gate | Condition |
|---|---|
| `SL-SECURITY-REVIEW` | Whenever `/app-release` runs, and when the user runs `/app-security-audit`. |
| `RM-RELEASE-READY` | Whenever `/app-release` or `/app-hotfix` runs. |
| `QL-RELEASE-QUALITY` | Whenever `/app-release` runs. |
| `SL-PRIVACY` | When `/app-release` or `/app-store-prep` ships a version whose personal-data handling changed, or when the user runs `/app-privacy-review`. |
| `PE-CODE-REVIEW` | At `/app-story-done` for any non-trivial change (more than a few lines, or any change an agent wrote). |
| A single-purpose review skill's own gate | When the user runs a skill whose whole job is that review: `/app-stack` (`TD-STACK`), `/app-threat-model` (`SL-THREAT-MODEL`), `/app-scope` (`PG-SCOPE`), `/app-security-audit` (`SL-SECURITY-REVIEW`), `/app-privacy-review` (`SL-PRIVACY`). |

A solo run of `/app-release` still prints the four skipped gates, and the release report's verdict cannot be GO on gate evidence it did not collect: it is CONCERNS or NOT ASSESSED unless the user explicitly accepts running a release unreviewed. The other per-story gates (`PM-ACCEPTANCE`, `QL-TEST-COVERAGE`, `QL-STORY-READY`) and the design-stage gates run in full mode only; `/app-story-done` still performs its own checks in every mode.

## Verdicts

Every gate has three judgement words of its own (listed in its definition) plus `NOT ASSESSED`, which is the same everywhere and is not listed in a Verdicts line.

| Position | Meaning | Words by gate family |
|---|---|---|
| Pass | No issues. Proceed. | APPROVE, ALIGNED, READY, VIABLE, CONTAINED, REALISTIC, ON TRACK, ACCEPTED, ADEQUATE, CLEAR, GO |
| Concerns | Issues present, not blocking. List them. | CONCERNS, OPTIMISTIC, AT RISK, GAPS |
| Blocking | Do not proceed until resolved. List the blockers. | REJECT, MISALIGNED, NOT READY, HIGH RISK, WIDE IMPACT, UNREALISTIC, OFF TRACK, REJECTED, INADEQUATE, BLOCK, NO GO |
| NOT ASSESSED | A named input was missing or unreadable, so no judgement was made. | NOT ASSESSED |

Verdict vocabularies:

| Gates | Pass / Concerns / Blocking |
|---|---|
| PD-VISION, TD-ARCHITECTURE, TD-ADR, TD-STACK, DD-DESIGN-LANGUAGE, DD-UX-SPEC, DD-VISUAL, SL-THREAT-MODEL, PE-CODE-REVIEW | APPROVE / CONCERNS / REJECT |
| PD-SPEC-ALIGN | ALIGNED / CONCERNS / MISALIGNED |
| PD-PHASE-GATE, TD-PHASE-GATE, DD-PHASE-GATE, PG-PHASE-GATE, QL-RELEASE-QUALITY | READY / CONCERNS / NOT READY |
| TD-FEASIBILITY, PE-FEASIBILITY | VIABLE / CONCERNS / HIGH RISK |
| TD-CHANGE-IMPACT | CONTAINED / CONCERNS / WIDE IMPACT |
| PG-SCOPE, PG-PLAN | REALISTIC / OPTIMISTIC / UNREALISTIC |
| PG-MILESTONE | ON TRACK / AT RISK / OFF TRACK |
| PM-ACCEPTANCE | ACCEPTED / CONCERNS / REJECTED |
| QL-STORY-READY, QL-TEST-COVERAGE | ADEQUATE / GAPS / INADEQUATE |
| SL-SECURITY-REVIEW, SL-PRIVACY | CLEAR / CONCERNS / BLOCK |
| RM-RELEASE-READY | GO / CONCERNS / NO GO |

**Ranking, strictest first**: blocking beats concerns, which beats NOT ASSESSED, which beats a pass. So NOT ASSESSED ranks below the failure words and above the pass word: a known problem is more actionable than an unknown, and a gate that could not look has approved nothing.

An agent that finds a problem and is also missing an input answers with the problem's word and names the missing input in its rationale. An artifact the brief reports as absent is a finding, not a missing input (except where a definition says otherwise). Agents never use a word from another gate's list, and the verdict is the first line of the answer.

**Default actions.** Pass: continue. Concerns: show the list to the user and ask (revise flagged items, accept and proceed, discuss); a revision is redone by the author of the section and recorded. Blocking: surface the blockers, write no downstream artifacts and advance no stage until resolved. NOT ASSESSED: name what was missing, supply it and re-run, or carry NOT ASSESSED into the skill's own verdict. Never treat it as a pass.

## Escalation for parallel gates

When several gates run together (for example the four phase gates in `/app-gate`, or the three release gates in `/app-release`), spawn all of them in one message and collect every verdict before acting. The combined result is the strictest verdict by the ranking above. One NOT ASSESSED keeps the combined result from passing, even if every other gate passes. The report lists every individual verdict, never only the combined one.

A user may accept a CONCERNS result. A blocking result from a gate is lifted only by fixing the cause and re-running that gate, or by the user's explicit, recorded risk acceptance; an agent never lifts it. `SL-SECURITY-REVIEW` BLOCK is a stop-ship call: the security-lead escalates it to the user, and `RM-RELEASE-READY` cannot return GO while it stands.

## Recording a gate outcome

After a gate runs, the skill records the outcome in the header of the reviewed document, directly under the title, one line per gate run:

```
> **<Owner> review (<GATE-ID>)**: <VERDICT> <date>
```

Example: `> **Technical Director review (TD-ARCHITECTURE)**: CONCERNS 2026-10-21`. Use the owner's display name, the verdict word exactly as the gate defines it (including NOT ASSESSED), and an ISO date. A later run of the same gate on the same document replaces its line and keeps the old verdict in the document's change history or the gate report. Phase gates record in the `app-gate` report (`docs/gates/<date>-<from>-to-<to>.md`) instead of a single document. The closing block of every skill lists the gate verdicts of the run (`orchestration.md` section 8).

## Gate coverage by stage

Table for standard rigor in full review mode. Phase gates are the `/app-gate` panel for the transition; per-artifact gates are run earlier by their skills. Lean mode runs only the phase gates (and the always-on gates at release). At minimal rigor the panel narrows to `TD-PHASE-GATE` and `PG-PHASE-GATE` (and `PD-PHASE-GATE` at the first transition); at full rigor all four phase gates run at every transition. Narrowing the panel never softens a verdict, and rigor relaxes what must exist, never what must work.

| Transition | Phase gates required | Phase gates optional | Per-artifact gates required (full mode) | Per-artifact gates optional |
|---|---|---|---|---|
| discovery to definition | `PD-PHASE-GATE`, `TD-PHASE-GATE` | `PG-PHASE-GATE` | `PD-VISION` | `TD-FEASIBILITY` |
| definition to architecture | `PD-PHASE-GATE`, `DD-PHASE-GATE`, `TD-PHASE-GATE` | `PG-PHASE-GATE` | `PD-SPEC-ALIGN` per spec, `DD-UX-SPEC` per flow, `DD-DESIGN-LANGUAGE` | `TD-FEASIBILITY`, `QL-STORY-READY` |
| architecture to foundation | `TD-PHASE-GATE`, `PG-PHASE-GATE` | `PD-PHASE-GATE`, `DD-PHASE-GATE` | `TD-ARCHITECTURE`, `PE-FEASIBILITY`, `TD-ADR` per foundation ADR, `TD-STACK`, `SL-THREAT-MODEL` (standard and full rigor) | `TD-CHANGE-IMPACT` |
| foundation to build | `TD-PHASE-GATE`, `PG-PHASE-GATE` | `DD-PHASE-GATE` | `PG-PLAN`, `QL-STORY-READY` for the first epic | `PG-SCOPE` |
| build to hardening | `PD-PHASE-GATE`, `TD-PHASE-GATE`, `DD-PHASE-GATE`, `PG-PHASE-GATE` | none | `PM-ACCEPTANCE`, `PE-CODE-REVIEW` and `QL-TEST-COVERAGE` per closed story; `DD-VISUAL` for UI work | `PG-MILESTONE`, `TD-CHANGE-IMPACT` |
| hardening to release | `PD-PHASE-GATE`, `TD-PHASE-GATE`, `DD-PHASE-GATE`, `PG-PHASE-GATE` | none | `SL-SECURITY-REVIEW`, `QL-RELEASE-QUALITY`; `SL-PRIVACY` when personal data is handled | `PG-MILESTONE` |
| release to operate | `TD-PHASE-GATE`, `PG-PHASE-GATE` | `PD-PHASE-GATE` | `RM-RELEASE-READY` (before the release ships) | none |

Between transitions, gates run when their skill runs: `PD-VISION` at `/app-brief`, `TD-ADR` at every `/app-adr`, `PG-SCOPE` and `PG-PLAN` while planning, the story gates at each `/app-story-done`, and the release gates at each `/app-release`. A hotfix runs `RM-RELEASE-READY` and `SL-SECURITY-REVIEW` when it touches security-relevant code.
