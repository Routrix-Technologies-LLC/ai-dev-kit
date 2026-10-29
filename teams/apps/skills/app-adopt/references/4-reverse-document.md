# app-adopt, Phase 4: reverse-document the architecture and write the stack reference

Part of `/app-adopt`. Runs in parallel with Phase 3. The hard rules in `SKILL.md` apply: nothing existing is edited, new files only, no secrets, scratch output outside the repo.

## Agents and outputs

| Agent | Job | Output (named path) |
|---|---|---|
| `modernization-engineer` (instance 1) | Architecture from code | `docs/architecture/architecture.md`, or the drift list at `~/AgentScratch/adopt-<app>/architecture-drift.md` when an architecture document already exists |
| `modernization-engineer` (instance 2) | Stack reference from manifests and lock files | `docs/stack-reference.md` |
| `principal-engineer` | Reviews both against the code (after the writers finish) | `~/AgentScratch/adopt-<app>/review-principal.md` |
| the platform lead(s) from `studio.yaml` platforms | Review the platform sections (full review mode only) | `~/AgentScratch/adopt-<app>/review-<lead>.md` |

Brief per orchestration section 3. Each brief carries the Phase 1 detection table, the approved `paths:` mapping, the rigor, the template path (`.claude/studio/templates/architecture.md` or `stack-reference.md`), the rule that the document is written from code only, and the return contract. The writers may create the named file; they may not edit any other file in the repo.

Platform lead routing:

| Platform in `studio.yaml` | Lead |
|---|---|
| web, extension | `web-lead` |
| windows, macos, linux | `desktop-lead` |
| ios, android | `mobile-lead` |
| backend | `backend-lead` |
| hosting, CI or infrastructure found | `platform-lead` |
| cli, library | `principal-engineer` (no separate lead) |

## Architecture document rules (instance 1)

Use the template's headings. Fill a section only with what the code, configuration or repo files show.

1. **Banner first:** the template's own banner (`DOCUMENTED FROM CODE, NOT DESIGNED.`) filled in with the date, the agent and the commit hash, followed by the template's Provenance table. Both stay until every INTENT UNKNOWN marker is resolved by the user.
2. **Every claim cites its source**: a file path, plus a line or symbol where practical. A claim with no citation is deleted, not softened.
3. **Separate three kinds of statements** and label them: `OBSERVED` (read directly from code or config), `INFERRED` (concluded from several observations, say from what), `INTENT UNKNOWN` (the code shows what exists but not why). Reasons for a design are never invented. If a comment, commit message or existing document states a reason, quote and cite it.
4. **Coverage by section** (adapt to the template and rigor):
   - Context: what the app talks to (network calls, SDKs, file formats, OS services), found from dependencies, config and clients.
   - Containers or modules: top-level folders and packages with one line each on what they own, and the dependency direction between them (from imports). Cycles or layering violations found are listed as findings, not fixed.
   - Components: the five to ten that matter, found from entry points, routing tables, DI registrations, command handlers, IPC command lists, screens.
   - Data: stores, schemas or models, migrations folder (how many, latest), serialization formats, where user data lives on disk or in a database.
   - Runtime and deployment: build output, how it is packaged and launched, hosting from IaC or compose files, environments found.
   - Cross-cutting: authentication and authorization mechanism, configuration and secrets handling (where read from, never the values), logging and error reporting libraries, feature flags.
   - Trust boundaries and observability, and budgets: at `full` rigor include what the code shows; otherwise `NOT DOCUMENTED (not in code)`.
5. **Absent facts are named.** A section the code cannot support says `NOT DOCUMENTED: <why>`. Never pad.
6. **Platform-specific parts follow the app's platforms**: for example a desktop app lists its process model, IPC surface and installer; a phone app lists its targets, entitlements or permissions, background work and push setup; a web app lists rendering strategy, routes and API client layer; a service lists endpoints, jobs and queues.
7. **Existing architecture document present:** write no new `architecture.md`. Produce a drift list: each statement in the existing document checked against the code as `CONFIRMED`, `OUTDATED (<what the code shows>)` or `UNVERIFIABLE`. The existing document is not edited.

## Stack reference rules (instance 2)

Use the template `stack-reference.md`.

1. Versions come only from lock files and manifests (resolved versions from the lock file, declared ranges from the manifest). Every row cites its file. A version from memory is forbidden; a dependency without a lock entry says `declared range only`.
2. Rows: runtimes and toolchains (language version, SDKs, compilers), frameworks, build tools, UI toolkit, data layer, test frameworks, linters. At `minimal`: those that shape the code. At `standard` and `full`: every direct dependency; transitive ones only when a finding needs them.
3. "Latest version" and "support status" columns are filled only from an official source fetched during this run (release page, vendor lifecycle page, registry), with the source and date. Otherwise the cell is `NOT CHECKED`. At `full` rigor the check is expected for runtimes, SDKs and frameworks; the rest may stay `NOT CHECKED`.
4. Add a short "Known API changes since the pinned versions" section only from official changelogs or migration guides actually read; otherwise write `NOT RESEARCHED` and recommend `/app-stack` or `/app-upgrade`.
5. Licenses: list the license where the manifest declares it; do not judge compatibility here (`compliance-specialist` via `/app-upgrade` or `/app-team-audit`).
6. Flag, as findings only: end-of-life runtimes found in the lock or toolchain files, lock files missing or out of sync with the manifest, duplicated major versions of one library, dependencies pinned to git branches or local paths.

## Review (per review mode, SKILL.md table)

Reviewers read both documents and verify against the code: pick claims at random, at least ten per document (all of them if fewer), re-read the cited file, and mark each `CONFIRMED` or `WRONG`. They correct factual errors directly in the two new documents, listing each correction, and mark anything they cannot settle `UNVERIFIED`. They do not add opinions about the design; that is `/app-team-audit`.

In `solo` mode the main session performs the same spot check on five claims per document and says in the report that agent review was skipped.

## Checks the main session makes

1. Both documents exist with real content: the banner and provenance table are present, every section is either filled with cited claims or says `NOT DOCUMENTED`, no template placeholder remains.
2. Re-check three claims per document yourself (open the cited file). If any fails, the document's verdict is not clean: report the failure, send it back once, then label the remainder `UNVERIFIED`.
3. Count and report: claims by label (`OBSERVED`, `INFERRED`, `INTENT UNKNOWN`), spot-check results as "N of M confirmed", and dependencies listed against dependencies declared ("48 of 51 direct dependencies listed" is a gap, not a pass).
4. Update the checkpoint in `.studio/state.md`.
