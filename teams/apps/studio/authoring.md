# Writing a studio agent

How every App Studio agent file is built. Follow it exactly so the roster reads as one team.

## File and frontmatter

`.claude/agents/<name>.md`, where `<name>` equals the `name:` field and the roster row.

```yaml
---
name: <name>
description: "<Tier and area>. <What it owns, in one sentence>. Use when <the triggers>."
tools: <see the table below>
model: sonnet
maxTurns: <see the table below>
memory: project              # directors, leads, and the specialists listed below
disallowedTools: Bash        # only for agents whose tools exclude Bash
---
```

- **description** is how the main session chooses an agent: under about 300 characters, starts with the tier and area ("Tier 3 desktop specialist."), names the concrete things owned, ends with "Use when ...". No marketing words.
- Agents never get the `Agent` tool: the main session orchestrates.

| Class | tools | maxTurns |
|---|---|---|
| director | `Read, Glob, Grep, Write, Edit, WebSearch, WebFetch` (plus `Bash` for `technical-director` and `program-director`) | 80 |
| lead | `Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch` | 100 |
| builder | `Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch` | 150 |
| author | `Read, Glob, Grep, Write, Edit, WebSearch, WebFetch` (plus `Bash` for `technical-writer` and `compliance-specialist`) | 80 |
| reviewer | `Read, Glob, Grep, Bash` | 80 |

`memory: project` for every director and lead, and for: `security-engineer`, `privacy-specialist`, `performance-engineer`, `database-engineer`, `escalation-engineer`, `modernization-engineer`, `accessibility-specialist`, `build-engineer`, `infrastructure-engineer`, `site-reliability-engineer`, `ux-researcher`, `domain-researcher`.

Exceptions to the turn table: `technical-writer` gets 100 (it runs and verifies commands). The caps were raised on 2026-10-22 after real stories on an existing app routinely needed more than 50 steps (read, edit, build, lint, test, screenshot, fix).

Which collaboration sections each class receives: director gets "Making a strategic decision"; lead gets both "Making a strategic decision" and "Reviewing"; builder "Building something"; author "Authoring a spec, design or document"; reviewer "Reviewing". Every class also gets "Where you are working", "How you work", "Gates and verdicts" and the workspace rules.

## Body, in this order

1. **Opening paragraph.** "You are the <Title> of the App Studio, a Tier <N> <area> <role>." Then two to four sentences: the mission, the standard you hold, and why the role exists in a large product organization.
2. **`### Key responsibilities`**: 6 to 10 numbered items, each starting with a bold name, each concrete enough to check.
3. **Two to five domain sections** (`### ...`): the real expertise. This is most of the file. Write what a top practitioner at a large software company knows and does:
   - decision frameworks and the criteria that actually decide them;
   - checklists a reviewer could run line by line;
   - platform and language specifics, across every platform the role covers (do not tilt toward any one OS, framework or language unless the role is specific to it);
   - named industry standards and practices where they exist (for example WCAG 2.2, OWASP ASVS and MASVS, Apple Human Interface Guidelines, Fluent 2, Material 3, Twelve-Factor, semantic versioning, Keep a Changelog, DORA metrics, Google SRE practice, the C4 model, RFC 9457 problem details), described accurately and without invented clause numbers;
   - common failure modes and how to catch them early.
   Do not hardcode version numbers that will rot. Say "the current LTS" or "the version pinned in the app" and tell the agent to check.
4. **`### Deliverables`**: what this agent produces, naming the studio template files it uses (list below) and inline formats for anything without a template.
5. **`### Gates you run`** (only for gate owners): the gate IDs from the list below, one line each on when.
6. **`### What this agent must NOT do`**: 4 to 8 bullets, each naming who owns that instead.
7. **`### Works with`**: reports to, delegates to, consults, and is the escalation target for. Only names on the roster.
8. **The marker line, last:** `<!-- studio-shared: <class> -->`. Write nothing after it. `tools/sync_shared.py` stamps the shared sections (where you are working, how you work, gates, workspace rules) below it, so do not repeat that material in the body.

Length: directors 180 to 260 lines, leads 150 to 220, specialists 120 to 200. Do not hard-wrap paragraphs. Depth over padding: every line should change what the agent does.

## Style

- Second person ("You own ..."). Plain, precise, specific. No em dashes anywhere (use colons, commas, parentheses; a hyphen only inside compound words). Gender-neutral.
- Platform- and language-neutral unless the role is specific. The studio must serve web, Windows, macOS, Linux, iOS, Android, backend and CLI work in any mainstream language, now and as the user's work changes.
- Never name the user's current projects, machines or paths. App-specific facts belong in each app's `studio.yaml`, not in an agent.
- Use studio vocabulary exactly: the stages, gate IDs, template names, severity words and layout paths below.

## Fixed vocabulary

**Stages** (`layout.md`): discovery, definition, architecture, foundation, build, hardening, release, operate.

**Rigor** (`standards/rigor.md`): minimal, standard, full. **Review modes**: solo, lean, full.

**Change types** (`standards/testing.md`): Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance, Docs.

**Severity** (`standards/severity.md`): bugs S1 Critical, S2 High, S3 Medium, S4 Low; security and review findings CRITICAL, HIGH, MEDIUM, LOW; priority P0 to P3.

**Gates** (`gates/<id-lowercase>.md`), owner in brackets:

- `PD-VISION`, `PD-SPEC-ALIGN`, `PD-PHASE-GATE` [product-director]
- `TD-FEASIBILITY`, `TD-ARCHITECTURE`, `TD-ADR`, `TD-STACK`, `TD-CHANGE-IMPACT`, `TD-PHASE-GATE` [technical-director]
- `DD-DESIGN-LANGUAGE`, `DD-UX-SPEC`, `DD-VISUAL`, `DD-PHASE-GATE` [design-director]
- `PG-SCOPE`, `PG-PLAN`, `PG-MILESTONE`, `PG-PHASE-GATE` [program-director]
- `PM-ACCEPTANCE` [product-manager]
- `PE-FEASIBILITY`, `PE-CODE-REVIEW` [principal-engineer]
- `QL-STORY-READY`, `QL-TEST-COVERAGE`, `QL-RELEASE-QUALITY` [qa-lead]
- `SL-THREAT-MODEL`, `SL-SECURITY-REVIEW`, `SL-PRIVACY` [security-lead]
- `RM-RELEASE-READY` [release-manager]

**Templates** (`templates/`): `studio.yaml`, `product-brief.md`, `product-vision.md`, `feature-spec.md`, `ux-spec.md`, `design-language.md`, `usability-test-plan.md`, `architecture.md`, `adr.md`, `api-contract.md`, `data-migration-plan.md`, `stack-reference.md`, `threat-model.md`, `privacy-review.md`, `security-audit-report.md`, `accessibility-audit.md`, `perf-budget.md`, `epic.md`, `story.md`, `sprint-plan.md`, `risk-entry.md`, `tech-debt-register.md`, `dependency-upgrade-plan.md`, `test-plan.md`, `test-evidence.md`, `bug-report.md`, `code-review-report.md`, `prototype-report.md`, `release-checklist.md`, `release-notes.md`, `store-listing.md`, `runbook.md`, `incident-postmortem.md`, `retrospective.md`, `decision-log.md`, `session-state.md`, `research-note.md`, `tracking-plan.md`, `license-inventory.md`, `localization-plan.md`.

**Layout paths**: as in `layout.md` (for example `docs/product/specs/`, `docs/architecture/adr/`, `planning/epics/`, `docs/qa/evidence/`, `.studio/state.md`), always subject to the app's `paths:` overrides.
