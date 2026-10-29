# Writing a studio skill

How every App Studio skill (`/app-*`) is built. Skills are the studio's workflows: they run in the main session, which orchestrates agents per `orchestration.md`.

## File and frontmatter

`.claude/skills/<name>/SKILL.md`, where `<name>` equals `name:`. Long phases may live in `.claude/skills/<name>/references/<n>-<phase>.md`, loaded only when that phase runs ("Read `references/3-review.md` now and follow it. Read it again if the conversation was compacted during this phase.").

```yaml
---
name: app-<verb>
description: "<What it does, one sentence>. Use when <the user's words or situations that should trigger it>."
argument-hint: "[app] [mode or target] [--review solo|lean|full]"
user-invocable: true
disable-model-invocation: true    # ONLY for app-dev-story, app-story-done, app-hotfix, app-release
---
```

Do not add `allowed-tools`, `model`, `context` or other keys. Skills must work with no helper scripts: they read `studio.yaml` and the studio docs with the Read tool.

## Body, in this order

1. **Title and purpose:** one paragraph. Then two lines: `Writes:` (artifact paths, with template names) and `Next:` (the skills that usually follow).
2. **When to use and when not to** (short; name the better skill for the "not" cases).
3. **Inputs:** what must exist, what is optional, and what happens when something is missing (ask, offer the producing skill, or NOT ASSESSED; never assume).
4. **Phases:** numbered `## Phase N: <name>`. Each phase says: who does it (the main session or which agents, in parallel or in sequence), what they read, what they produce (exact path), the decision point with the user if any, and the check that the phase really happened (artifact exists with content). Use the agent names from `roster.md` exactly. Select platform and language specialists from the app's `studio.yaml` instead of hardcoding one stack.
5. **Rigor and review mode:** a small table of what changes at minimal, standard and full, and which gates run at solo, lean and full. Keep it short: rigor changes what must exist, never what must work.
6. **Verdicts:** the skill's own verdict words, first match wins, always including `NOT ASSESSED` ranked below the failures and above the pass. Say exactly which conditions produce NOT ASSESSED.
7. **Report:** the fixed report shape (fenced), ending with the closing block from `orchestration.md` section 8.
8. **Rules for this skill:** the hard constraints (what it must never do), in bullets.

Do not restate `orchestration.md`; reference its sections ("Brief agents per orchestration.md section 3"). Typical length: 120 to 300 lines. Team skills are phase lists plus routing tables, not boilerplate.

## The five obligations of a gating skill

1. Its verdict list has a "could not assess" value, ranked correctly, and the report says why it applied.
2. An absent setting or input never defaults to the permissive answer. Unset means ask, or NOT ASSESSED.
3. A skipped step announces itself in the output.
4. It never asserts what it cannot source or check.
5. Before shipping a skill, apply the test: "if this step silently did not run, what would the output look like?" If the answer is "the same", the skill is not finished.

## Style

No em dashes (U+2014) or en dashes (U+2013) anywhere. Platform-, language- and framework-neutral: a skill must work for a web app, a Windows or Mac or Linux desktop app, a phone app, a backend service or a CLI, routing to the right specialists from `studio.yaml`. Never name the user's own projects or machines. Use studio vocabulary exactly (`authoring.md` "Fixed vocabulary", `layout.md` paths, template names, gate IDs).

## The catalog

Every skill in the studio. Writers implement exactly these names and scopes.

### Start and navigate
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-start` | Onboard a new app: route (fresh idea, have a spec, existing code goes to `app-adopt`), capture the idea, choose platforms and rigor, write `studio.yaml`, brief, and a foundation plan | product-director, technical-director, product-manager | `studio.yaml`, `docs/product/brief.md`, `.studio/state.md`, `.gitignore` entry | COMPLETE, BLOCKED |
| `app-adopt` | Bring an existing app under the studio: detect stack and commands, map existing docs into `paths:`, reverse-document architecture, write stack reference, detect stage, gap report; never moves files without a yes | modernization-engineer, principal-engineer, the platform lead for its platforms, build-engineer | `studio.yaml`, `docs/architecture/architecture.md` (from code, marked as such), `docs/stack-reference.md`, `docs/qa/adoption-report.md` | COMPLETE, COMPLETE WITH GAPS, NOT ASSESSED, BLOCKED |
| `app-help` | Read-only: where the app is (stage, artifacts present per `layout.md`, checkpoint, open stories) and the one or two best next skills | none (main session) | nothing | (informational) |

### Define
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-brief` | Product brief at minimal rigor, or vision with pillars, personas and positioning at standard and full | product-director, product-manager, domain-researcher, ux-researcher | `docs/product/brief.md` or `docs/product/vision.md` | COMPLETE, BLOCKED; gate PD-VISION |
| `app-spec` | Author a feature spec section by section with requirement IDs and binary acceptance criteria; retrofit mode for an existing spec | product-manager, business-analyst, ux-designer (consulted), the relevant lead (feasibility) | `docs/product/specs/<feature>.md` | COMPLETE, BLOCKED; gates PD-SPEC-ALIGN, TD-FEASIBILITY (full) |
| `app-ux` | UX spec for a flow or screen group: every state, every platform variant, copy, accessibility notes | ux-designer, content-designer, accessibility-specialist, ui-designer | `docs/design/ux/<flow>.md` | COMPLETE, BLOCKED; gate DD-UX-SPEC |
| `app-design-language` | Create or update the design language: tokens, type, color, components, theming, per-platform adaptation | design-director, ui-designer, accessibility-specialist, ui-engineer (consulted) | `docs/design/design-language.md` | COMPLETE, BLOCKED; gate DD-DESIGN-LANGUAGE |
| `app-spec-review` | Independent review of one spec or all specs (completeness, testability, contradictions across specs, scope) | product-manager, business-analyst, qa-lead (testability), relevant lead | `docs/product/reviews/<date>-<scope>.md` | APPROVED, NEEDS REVISION, MAJOR REVISION, NOT ASSESSED |

### Architect
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-architecture` | Create or update the architecture doc: context, containers, components (C4), data, deployment, trust boundaries, budgets, observability | technical-director, principal-engineer, platform leads for the app's platforms, security-lead | `docs/architecture/architecture.md` | COMPLETE, BLOCKED; gates TD-ARCHITECTURE, PE-FEASIBILITY |
| `app-adr` | New ADR, retrofit an existing decision into an ADR, or `accept` (the only route to Accepted, after the user's yes, listing what it unblocks) | technical-director, the owning lead | `docs/architecture/adr/ADR-NNNN-<slug>.md` | COMPLETE, BLOCKED; gate TD-ADR |
| `app-stack` | Choose or pin the stack, or evaluate adopting a framework or dependency; write the stack reference with versions verified from official sources | technical-director, the platform lead, language specialists, compliance-specialist, security-engineer | `docs/stack-reference.md`, an ADR draft | ADOPT, TRIAL, REJECT, NOT ASSESSED; gate TD-STACK |
| `app-api` | Design or review an API or IPC contract; breaking-change detection against the previous version | api-designer, backend-lead, consumers' leads, security-engineer | `docs/architecture/api/<name>.*`, review notes | APPROVED, CHANGES REQUIRED, BREAKING, NOT ASSESSED |
| `app-data-migration` | Plan and rehearse a schema or data-format change: expand and contract, backfill, dry run on a copy, rollback, old data still loads | database-engineer, backend-lead, qa-lead | `planning/migrations/<id>.md` from `data-migration-plan.md` | READY, CONCERNS, NOT READY, NOT ASSESSED |
| `app-threat-model` | STRIDE threat model over the data-flow diagram and trust boundaries; mitigations become stories | security-lead, security-engineer, privacy-specialist, the platform leads | `docs/security/threat-model.md` | COMPLETE, BLOCKED; gate SL-THREAT-MODEL |

### Plan
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-plan` | Turn specs into epics and stories (type, estimate, files, acceptance criteria, test cases, dependencies); never renumbers or rewrites existing stories | product-manager, principal-engineer, qa-lead, program-director | `planning/epics/<epic>/epic.md`, `story-NNN-<slug>.md` | COMPLETE, BLOCKED; gates QL-STORY-READY, PG-PLAN |
| `app-story-ready` | Readiness check of one story, an epic or a sprint; read-only except that, after a READY verdict and the user's yes, it may move those stories from Draft to Ready | qa-lead (testability), product-manager | story status (Draft to Ready only), or a report | READY, NEEDS WORK, BLOCKED, NOT ASSESSED |
| `app-sprint` | Plan a sprint or batch from ready stories (or kanban order), or report status honestly | program-director, product-manager | `planning/sprints/<id>.md` | (plan) COMPLETE; (status) ON TRACK, AT RISK, OFF TRACK, NOT ASSESSED; gate PG-PLAN |
| `app-scope` | Scope check and estimate: compare planned work to capacity and the brief, find creep, propose cuts by pillar proximity | program-director, product-director | report | REALISTIC, OPTIMISTIC, UNREALISTIC, NOT ASSESSED; gate PG-SCOPE |

### Build
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-dev-story` | Implement one story: route by layer and platform to the right builders, tests with the change, run and observe, update the story's Files list; never closes the story | the story's builders (from roster and `studio.yaml`), language specialist, test-engineer | code, tests, evidence, story file, checkpoint | IMPLEMENTED, IMPLEMENTED WITH NOTES, BLOCKED, NOT VERIFIED |
| `app-story-done` | The only way a story closes: verify each acceptance criterion against evidence, scope check (changed files vs Files list), deviations, code review, tests run | code-reviewer, qa-lead, product-manager, principal-engineer | story status, evidence notes, tech-debt rows | COMPLETE, COMPLETE WITH NOTES, NOT ASSESSED, BLOCKED; gates PE-CODE-REVIEW, QL-TEST-COVERAGE, PM-ACCEPTANCE |
| `app-code-review` | Independent multi-lens review of a diff, branch or path: code-reviewer plus the language and platform specialist plus security-engineer for sensitive code; every finding verified | code-reviewer, language and platform specialists, security-engineer | `docs/qa/reviews/<date>-<scope>.md` from `code-review-report.md` | APPROVED, APPROVED WITH SUGGESTIONS, CHANGES REQUIRED, NOT ASSESSED |
| `app-bugfix` | Fix a bug properly: reproduce, root cause, regression test seen failing, fix, test seen passing, review | escalation-engineer (hard or intermittent bugs), the owning builder, test-engineer, code-reviewer | bug record, fix, test | FIXED, FIXED WITH NOTES, CANNOT REPRODUCE, BLOCKED |
| `app-prototype` | Time-boxed spike answering one question in `prototypes/<name>/` | prototyper, the relevant lead | `prototypes/<name>/`, `prototype-report.md` | PROCEED, PIVOT, KILL, NOT ASSESSED |
| `app-upgrade` | Plan and execute a dependency, framework, runtime or SDK upgrade one major at a time, with changelog and migration-guide reading, license and security checks | modernization-engineer, the language specialist, the platform lead, compliance-specialist, security-engineer | `planning/upgrades/<id>.md` from `dependency-upgrade-plan.md`, code | UPGRADED, PARTIAL, BLOCKED, NOT ASSESSED |
| `app-tech-debt` | Find, register and prioritize tech debt; plan paydown into stories | principal-engineer, modernization-engineer, code-reviewer | `planning/tech-debt.md` | COMPLETE |

### Quality
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-test-setup` | Set up or repair the test harness and CI for the app's stack, including headless UI capture | build-engineer, test-engineer, test-automation-engineer | test config, CI config, `commands:` in `studio.yaml` | COMPLETE, PARTIAL, BLOCKED |
| `app-qa-plan` | Test plan for a sprint, feature or release: per-change-type evidence, platform matrix, manual checks | qa-lead, test-engineer | `docs/qa/test-plans/<scope>.md` | COMPLETE |
| `app-smoke` | Build, test and launch-and-observe the critical paths on each target the app supports | test-automation-engineer, test-engineer | `docs/qa/smoke-<date>.md` | PASS, PASS WITH WARNINGS, NOT ASSESSED, FAIL |
| `app-security-audit` | Security audit of the app or a scope: threat-driven, platform-aware, SEC-NNN findings | security-engineer, security-lead, identity-specialist (auth), privacy-specialist (data) | `docs/security/audits/<date>.md` | CLEAR, CONCERNS, BLOCK, NOT ASSESSED; gate SL-SECURITY-REVIEW |
| `app-perf` | Profile against budgets on each target; before and after evidence | performance-engineer, the platform specialist | `docs/qa/perf-<date>.md`, `perf-budget.md` if absent | WITHIN BUDGET, OVER BUDGET, NO BUDGET, NOT ASSESSED |
| `app-a11y-audit` | Accessibility audit against WCAG 2.2 AA and the platform's accessibility API, automated plus manual | accessibility-specialist, ux-designer | `docs/qa/a11y-<date>.md` from `accessibility-audit.md` | CONFORMS, PARTIAL, FAILS, NOT ASSESSED |
| `app-privacy-review` | Data inventory, flows, retention, consent and store privacy declarations | privacy-specialist, security-lead, app-store-specialist | `docs/security/privacy.md` | CLEAR, CONCERNS, BLOCK, NOT ASSESSED; gate SL-PRIVACY |
| `app-ux-review` | Review implemented UI against the UX spec, design language and heuristics, with evidence | ux-researcher, design-director, accessibility-specialist, content-designer | `docs/design/reviews/<date>-<scope>.md` | APPROVED, NEEDS REVISION, MAJOR REVISION, NOT ASSESSED; gate DD-VISUAL |
| `app-i18n` | Internationalization readiness or a localization pass: externalization, pseudo-localization, RTL, formats | localization-specialist, content-designer, ui-engineer | report, string resources | READY, GAPS, NOT READY, NOT ASSESSED |

### Release and operate
| Skill | Purpose | Main agents | Writes | Verdicts |
|---|---|---|---|---|
| `app-gate` | Phase gate: check required artifacts for the next stage at the app's rigor, run quality checks, run the director panel, chain of verification, then (after the user's yes) advance `stage:` | the directors per review mode, qa-lead | `docs/gates/<date>-<from>-to-<to>.md`, `studio.yaml` stage | PASS, CONCERNS, NOT ASSESSED, FAIL; gates PD/TD/DD/PG-PHASE-GATE |
| `app-release` | Prepare a release: version, changelog, release notes, checklist per channel, packaging and signing, rollout and rollback plan; deploys, tags and publishes only after an unconditional ask | release-manager, qa-lead, security-lead, desktop-packaging-engineer or app-store-specialist or infrastructure-engineer per channel | `docs/release/<version>.md`, `CHANGELOG.md` | GO, CONCERNS, NO GO, NOT ASSESSED; gates RM-RELEASE-READY, QL-RELEASE-QUALITY, SL-SECURITY-REVIEW |
| `app-store-prep` | Draft a store submission package: listing, screenshots plan, privacy forms, review notes, rejection response | app-store-specialist, privacy-specialist, content-designer, monetization-specialist | `docs/release/store/<store>.md` | READY TO SUBMIT, GAPS, NOT ASSESSED |
| `app-hotfix` | Emergency fix on the released version: branch from the release tag, minimal fix, regression test, backport check, rollback plan before deploy, unconditional asks | escalation-engineer, release-manager, code-reviewer, qa-lead | fix, `docs/release/<version>.md` | SHIPPED (after the user's action), READY, NOT ASSESSED, BLOCKED; gates RM-RELEASE-READY, SL-SECURITY-REVIEW (security-relevant fixes) |
| `app-incident` | Run an incident (severity, mitigation, comms drafts) and write the blameless postmortem with actions | site-reliability-engineer, escalation-engineer, release-manager | `docs/ops/incidents/<date>-<slug>.md` | RESOLVED, MITIGATED, ONGOING |
| `app-observability` | Design or audit logging, metrics, tracing, crash reporting, SLOs and alerts for the app's platforms | site-reliability-engineer, analytics-specialist, privacy-specialist | `docs/ops/observability.md`, runbooks | COMPLETE, GAPS, NOT ASSESSED |
| `app-retro` | Retrospective for a sprint, milestone, release or incident: what happened, why, actions with owners | program-director | `planning/retros/<date>.md` | COMPLETE |

### Teams
| Skill | Purpose | Phases and agents |
|---|---|---|
| `app-team-feature` | One feature end to end | spec (product-manager, business-analyst) then UX (ux-designer, content-designer, accessibility-specialist) then architecture (principal-engineer and the platform leads, api-designer and database-engineer if needed, security-lead if sensitive) then stories (app-plan) then build (app-dev-story per story) then review (code-reviewer, security-engineer, accessibility-specialist in parallel) then close (app-story-done) |
| `app-team-audit` | Whole-app health audit and improvement backlog for an existing app | parallel lenses: architecture (principal-engineer), code quality (code-reviewer plus language specialist), security (security-engineer), performance (performance-engineer), accessibility (accessibility-specialist), UX (ux-researcher), tests and CI (qa-lead, build-engineer), dependencies and licenses (compliance-specialist), docs (technical-writer), operations (site-reliability-engineer, if deployed); then verification of top findings; then one prioritized report and proposed stories |
| `app-team-ui` | A screen or UI area from spec to polished, accessible implementation | ux-designer then ui-designer then the platform UI builder (ui-engineer, windows-desktop-engineer, macos-engineer, ios-engineer, android-engineer, and so on) then parallel review (design-director, accessibility-specialist, content-designer) |
| `app-team-harden` | Hardening pass before a release | parallel: security-engineer, performance-engineer, accessibility-specialist, localization-specialist, test-engineer (edge and soak), site-reliability-engineer (failure modes); then fixes routed to owners; then sign-off |
| `app-team-release` | Release squad | release-manager plan, then parallel quality gate (qa-lead, security-lead, privacy-specialist if data changed, performance-engineer), then packaging or deploy prep per channel, then go/no-go, then the user's deploy or submit, then post-release watch |
