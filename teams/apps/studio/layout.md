# App layout and `studio.yaml`

Every app the studio works on is its own git repository. The studio keeps its artifacts inside that repo, so they travel with the code. This file says where they go by default, and how an app overrides that.

## `studio.yaml`

One small file at the app's repo root is the app's studio config. Agents and skills read it with the Read tool; nothing parses it with scripts. `/app-start` writes it for a new app; `/app-adopt` writes it for an existing one. Template: `templates/studio.yaml`.

```yaml
studio: 1                      # format version of this file
app:
  name: Example                # display name
  summary: One line on what it is and who it is for.
stage: build                   # discovery | definition | architecture | foundation | build | hardening | release | operate
platforms: [windows, web]      # any of: web, windows, macos, linux, ios, android, backend, cli, extension, library
stack:
  languages: [rust, typescript]
  frameworks: [tauri, react]
  data: [sqlite]
  hosting: [self-hosted docker]
  min_targets: "Windows 10 22H2+, evergreen browsers"   # oldest OS, browser or device supported
commands:                      # the exact commands, run from the repo root
  build: cargo build
  build_release: cargo build --release
  test: cargo test
  lint: cargo clippy -- -D warnings
  format: cargo fmt
  run: cargo run
  e2e: ""
  screenshot: ""               # how to capture the app without taking focus, if known
modes:
  rigor: minimal               # minimal | standard | full   (standards/rigor.md)
  review: lean                 # solo | lean | full; omit to follow rigor
specialists: [rust-specialist, hybrid-desktop-engineer]   # the agents this app usually needs
channels: []                   # how releases reach users, e.g. [web-deploy, github-releases, winget, app-store, play-store, ms-store, npm]
infra_record: ""               # repo or doc that holds hosting facts, if the app is deployed
rules:                         # standing rules for this app; every agent obeys them
  - "Example: after any UI change, build the release binary, because the user tests from it."
paths: {}                      # overrides of the default layout below, e.g. adr: docs/decisions
```

Keep it short. A key nobody uses is noise. An unknown value is left empty, never guessed.

## Default layout inside an app repo

| What | Default path | Notes |
|---|---|---|
| Studio config | `studio.yaml` | Required for studio skills. |
| One-page brief | `docs/product/brief.md` | The whole design record at minimal rigor. |
| Vision and pillars | `docs/product/vision.md` | Standard and full rigor. |
| Feature specs | `docs/product/specs/<feature>.md` | One per feature; requirement IDs `REQ-<feature>-NNN`. |
| Design language | `docs/design/design-language.md` | Tokens, type, color, components, platform adaptations. |
| UX specs | `docs/design/ux/<flow>.md` | One per flow or screen group. |
| Architecture | `docs/architecture/architecture.md` | The system overview. |
| ADRs | `docs/architecture/adr/ADR-NNNN-<slug>.md` | Numbered, never renumbered. |
| API contracts | `docs/architecture/api/` | OpenAPI, GraphQL SDL, proto, IPC command lists. |
| Threat model | `docs/security/threat-model.md` | Plus `docs/security/audits/` for audit reports. |
| Privacy record | `docs/security/privacy.md` | Data inventory, flows, retention. |
| Stack reference | `docs/stack-reference.md` | Pinned versions of runtimes, SDKs and key libraries, and known API changes since then. |
| Decision log | `docs/decisions.md` | Short dated entries; at minimal rigor this replaces ADRs. |
| Epics and stories | `planning/epics/<epic>/epic.md`, `planning/epics/<epic>/story-NNN-<slug>.md` | |
| Sprint or batch plans | `planning/sprints/<id>.md` | |
| Risk register | `planning/risks.md` | |
| Tech debt register | `planning/tech-debt.md` | |
| Test plans | `docs/qa/test-plans/<scope>.md` | |
| Test evidence | `docs/qa/evidence/<story-or-change>/` | Screenshots and evidence notes. Keep images small (PNG, a few hundred KB). |
| Bugs | `docs/qa/bugs/BUG-NNNN-<slug>.md` | Or the app's issue tracker if it has one. |
| Release checklists | `docs/release/<version>.md` | |
| Changelog | `CHANGELOG.md` | Keep a Changelog format, semantic versions. |
| Store listings | `docs/release/store/<store>.md` | Drafts; the user submits. |
| Runbooks | `docs/ops/runbooks/<topic>.md` | |
| Incidents | `docs/ops/incidents/<date>-<slug>.md` | |
| Prototypes | `prototypes/<name>/` | Throwaway, never imported by production code. |
| Session checkpoint | `.studio/state.md` | Local and gitignored. See below. |
| Local scratch | `~/AgentScratch/<task>/` | Never in the repo. |

Secondary artifacts, written by the skill or agent named in brackets:

| What | Default path |
|---|---|
| Research notes (domain and user) [domain-researcher, ux-researcher] | `docs/research/<topic>.md` (template `research-note.md`) |
| Usability test plans and results [ux-researcher] | `docs/research/<study>.md` (template `usability-test-plan.md`) |
| Tracking plan [analytics-specialist] | `docs/product/tracking-plan.md` |
| Spec and design reviews [`app-spec-review`, `app-ux-review`] | `docs/product/reviews/<date>-<scope>.md`, `docs/design/reviews/<date>-<scope>.md` |
| Supported platform matrix [platform leads] | a section of `docs/architecture/architecture.md` |
| Data and migration plans [`app-data-migration`] | `planning/migrations/<id>.md` |
| Upgrade plans [`app-upgrade`] | `planning/upgrades/<id>.md` |
| Retrospectives [`app-retro`] | `planning/retros/<date>.md` |
| Gate reports [`app-gate`] | `docs/gates/<date>-<from>-to-<to>.md` |
| Code reviews [`app-code-review`] | `docs/qa/reviews/<date>-<scope>.md` |
| Audits [`app-team-audit`, `app-perf`, `app-a11y-audit`, `app-smoke`] | `docs/qa/audit/<date>/<agent>.md`, `docs/qa/perf-<date>.md`, `docs/qa/a11y-<date>.md`, `docs/qa/smoke-<date>.md` |
| Adoption report [`app-adopt`] | `docs/qa/adoption-report.md` |
| License inventory and notices [compliance-specialist] | `docs/security/licenses.md` (template `license-inventory.md`) |
| Store policy checklist [app-store-specialist] | `docs/release/store/policy-checklist.md` |
| Localization plan [localization-specialist] | `docs/product/localization.md` (template `localization-plan.md`) |
| Observability, SLOs, backup and recovery [site-reliability-engineer] | `docs/ops/observability.md`, `docs/ops/slo.md`, `docs/ops/backup-and-recovery.md` |
| Prototype index [prototyper] | `prototypes/index.md` |
| Scope checks [`app-scope`] | `planning/scope-checks/<date>-<scope>.md` |
| API reviews [`app-api`] | `docs/architecture/api/reviews/<name>-<date>.md` |
| Performance budget [`app-perf`] | `docs/qa/perf-budget.md` (template `perf-budget.md`) |
| Internationalization reports [`app-i18n`] | `docs/qa/i18n-<date>.md` |
| Per-agent working notes of a multi-agent review | a `<date>/` folder beside the main report, one file per agent |
| Release notes [`app-release`] | `docs/release/<version>-notes.md` (template `release-notes.md`) |
| Release run records [`app-release`, `app-team-release`] | `docs/release/<version>/<agent>.md` |
| Gate panel records [`app-gate`] | `docs/gates/panel/<date>-<gate-id>.md` (append `-<from>-to-<to>` when two transitions are gated on the same day) |
| Feature run records [`app-team-feature`] | `planning/features/<feature>/<phase>-<agent>.md` |
| UI run records [`app-team-ui`] | `docs/design/ui/<area>/` |
| Hardening run records [`app-team-harden`] | `docs/qa/harden/<date>/` (canonical security, performance, accessibility and smoke reports still go to their own paths above) |
| Smoke paths [`app-test-setup`, read by `app-smoke` and `app-qa-plan`] | `docs/qa/smoke-paths.md` |
| Agent drafts awaiting approval | `.studio/drafts/<skill>-<scope>-<agent>.md` (local) |

ID schemes (never reused, never renumbered): `REQ-<feature>-NNN` requirements, `ADR-NNNN` decisions, `MIG-NNNN` migrations, `TD-NNN` tech debt, `BUG-NNNN` bugs, `SEC-NNN` security findings, `RISK-NNNN` risks.

**An existing app keeps its own layout.** If it already has `docs/adr/`, a `DECISIONS.md` or an issue tracker, map them in `paths:` instead of moving files. `/app-adopt` proposes the mapping; nothing is moved without the user's yes.

`paths:` keys: `brief`, `vision`, `specs`, `design_language`, `ux`, `architecture`, `adr`, `api`, `threat_model`, `privacy`, `stack_reference`, `decisions`, `epics`, `sprints`, `risks`, `tech_debt`, `test_plans`, `evidence`, `bugs`, `release`, `changelog`, `store`, `runbooks`, `incidents`, `prototypes`, `research`, `migrations`, `upgrades`, `reviews`, `audits`, `gates`, `licenses`, `ops`.

## The session checkpoint: `.studio/state.md`

The file is the memory, not the conversation. After a compaction, a crash, a new session or `/clear`, the first thing to read is `.studio/state.md`. Template: `templates/session-state.md`.

- The `CHECKPOINT` block is overwritten, never appended to, and stays under about 25 lines: current task, next step (concrete enough to resume cold), blocked on, files in progress, last run result, open questions.
- Below it is free narrative. When it passes about 200 lines, move it to `.studio/log/<date>.md` and start fresh.
- Studio skills update the checkpoint at each phase boundary. Add `.studio/` to the app's `.gitignore`.

## Stages

An app moves through these stages. `stage:` in `studio.yaml` records where it is; only `/app-gate` advances it, and only after the user says yes. Existing apps usually enter at `build` or `operate` through `/app-adopt`.

| Stage | The question it answers | Typical exit artifacts |
|---|---|---|
| `discovery` | What problem, for whom, and is it worth solving? | Brief (or vision), first risks |
| `definition` | What exactly will the first version do and how will it feel? | Feature specs for the MVP, UX specs for key flows, design language (standard and full) |
| `architecture` | How will it be built, on what, within which budgets? | Architecture doc, ADRs for foundation decisions, threat model (standard and full), stack reference |
| `foundation` | Does a walking skeleton build, test and run on every target? | Repo scaffold, CI green, test harness, one end-to-end path running, `commands:` filled in |
| `build` | Feature work, story by story | Epics and stories, evidence per story, reviews |
| `hardening` | Is it secure, fast, accessible, localizable and stable enough? | Security audit, performance against budgets, accessibility audit, bug bar met |
| `release` | Is this version ready to reach users? | Release checklist, release notes, signed packages or store submissions (drafted), rollback plan |
| `operate` | Is it healthy in users' hands, and what is next? | Runbooks, monitoring, incident records, the next cycle's backlog |
