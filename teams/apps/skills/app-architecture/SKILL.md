---
name: app-architecture
description: "Create or update the architecture document: system context, containers, components, data, key flows, deployment topology, trust boundaries, budgets and observability, with a required-ADR list; or reconstruct it from existing code. Use when the user asks how the app should be built, wants an architecture doc or diagram, says 'C4', 'system design', 'architecture overview', or an adopted app has no architecture record."
argument-hint: "[app] [full | update <section> | from-code | adr-audit] [--review solo|lean|full]"
user-invocable: true
---

# App Architecture

Produces `docs/architecture/architecture.md`: the whole-system blueprint that gives individual ADRs their context. It follows the C4 levels (context, containers, components), then data, key flows, deployment topology, trust boundaries, budgets, observability and failure modes, and ends with the list of decisions that still need an ADR. It is written section by section with the user; agents propose, the user decides.

Writes: `docs/architecture/architecture.md` (template `templates/architecture.md`), `.studio/state.md` checkpoint.
Next: `/app-adr` for each required ADR (foundation first), `/app-threat-model`, `/app-stack` if the stack is unpinned, `/app-api` and `/app-data-migration` where the doc names contracts or stores, `/app-gate` at the architecture exit.

## When to use and when not to

- Use at the architecture stage, when a feature changes the shape of the system (new container, new store, new trust boundary), and to give an adopted app an honest architecture record (`from-code`).
- A single point decision is `/app-adr`. Choosing or pinning the stack is `/app-stack`. Code-level structure of one change is `principal-engineer` inside `/app-plan`. A security analysis is `/app-threat-model`.

## Modes

| Argument | Mode |
|---|---|
| none or `full` | Walk every section |
| `update <section>` | Change only the named section(s); raise the Version; note what changed and which ADRs it touches |
| `from-code` | Reconstruct from the repository. Read `references/from-code.md` now and follow its rules for provenance and verification in every phase. Read it again if the conversation was compacted |
| `adr-audit` | Phase 5 only, against the existing document |

If the file exists and mode is `full`, ask: update (which sections) or rewrite one section. Never overwrite silently. `/app-adopt` may have written a first from-code version; `from-code` here refines it and keeps its provenance markers until each claim is confirmed.

## Inputs

| Input | If missing |
|---|---|
| `studio.yaml` | Stop; offer `/app-adopt` or `/app-start`. |
| Brief or vision | Ask for the product's purpose and users in the user's words; record as an assumption. |
| Specs (`docs/product/specs/`) | Without specs, the requirements baseline is `NOT ASSESSED - no specs`; the user states the architecturally significant requirements and they are marked as stated, not sourced. |
| UX specs, design language | Optional. Read data needs and events from the UX specs. |
| Stack reference | If the key frameworks and runtimes are not pinned, decisions about them are marked `UNVERIFIED version` and `/app-stack` is recommended. Never assert an API or version from memory. |
| Existing ADRs, threat model, privacy record | Read statuses and decisions. |

## Phase 1: Resolve, announce, load

Print the plan block (`orchestration.md` sections 1 and 2). Agents by `studio.yaml` platforms:

| Platform in `studio.yaml` | Lead consulted | Why |
|---|---|---|
| web | `web-lead` | Rendering strategy, state, routing, client budgets |
| windows, macos, linux | `desktop-lead` | Native versus hybrid, OS integration, distribution and update |
| ios, android | `mobile-lead` | Native versus cross-platform, lifecycle, offline, permissions, store path |
| backend, or any app with a server | `backend-lead` | Services, APIs, data, integrations, scaling |
| any deployed app (`hosting`, `infra_record` set) | `platform-lead` | Environments, hosting, CI/CD, observability strategy, cost |
| cli, library, extension | `principal-engineer` covers it | Command or API surface, packaging, compatibility |
| always | `principal-engineer`, `security-lead`, `technical-director` (gate and decisions) | Modules and boundaries, trust, sign-off |
| `from-code` | `modernization-engineer` | Reverse-documents the structure |

Main session reads the shared inputs once and builds the **requirements baseline**: a table of architecturally significant requirements, each as `REQ-id` (from the specs) or `stated`, the quality attribute it drives (performance, availability, offline, security, privacy, scale, platform reach, accessibility, cost, operability) and a measurable target or `target unknown`. It also builds the **knowledge gap list**: frameworks and runtimes whose pinned version is newer than what the agents reliably know, or unpinned.

Check: the baseline table has a row count and the gap list is printed, even if empty ("0 gaps in 6 dependencies").

## Phase 2: Proposals (parallel)

Issue every spawn in one message (`orchestration.md` section 4). Each agent writes one file in `~/AgentScratch/app-architecture/<agent>.md` with 2 to 3 options per decision area it owns and the trade-offs, based on the baseline and the pinned stack; they cite requirement rows; they do not write the architecture doc.

- `principal-engineer`: containers and component boundaries, dependency rules, module ownership, shared code, build and test seams.
- Platform lead(s) from the table: client or service architecture for their platform, state and data flow, offline and sync, update and distribution path, platform constraints and cost.
- `security-lead`: trust boundaries, sensitive data, authentication and authorization shape, secrets, IPC and update integrity, what must go to `/app-threat-model`.
- `platform-lead` (if deployed): environments, hosting options with cost, deployment pipeline shape, observability stack options.

For `from-code`, spawn `modernization-engineer` first alone (per `references/from-code.md`), then the others review its reconstruction instead of proposing from scratch.

Check: every spawned agent's file exists with content; missing ones are re-briefed once, then recorded as `<agent> NOT ASSESSED` and the dependent section marked as a gap.

## Phase 3: Sections, one at a time

Main session with the user. For each section: show the evidence, present the options with a recommendation, record the decision, draft, get approval, write the section to the file immediately (create the file with all headings at the first section, after one ask naming the path), update the checkpoint. Diagrams are Mermaid in fenced blocks, each followed by a table of the same content so the section survives a renderer that cannot draw it.

Write into the numbered headings of `templates/architecture.md` exactly as they are (add subsections under them where noted; never rename, renumber or drop a heading). The document header carries the template's Status line (`Draft` here; `Reviewed` and `Approved` are set by the gate and the user), Last verified against code, Owner, and the `TD-ARCHITECTURE` review line.

| Template section | Contents | Rigor |
|---|---|---|
| 1 Context and goals | Purpose (link the brief or vision), the ranked top qualities, fixed constraints, non-goals; three to five architecture principles derived from the baseline (for example "the server is never trusted with the user's plaintext"), each with the requirement it serves; the requirements baseline summary | all (principles: standard, full) |
| 2 System context (C4 level 1) | The system as one box; users and roles; external systems (identity provider, payments, stores, email, AI providers, OS services); what crosses each line | all |
| 3 Containers (C4 level 2) | Each separately deployable or runnable unit: web client, desktop process, mobile app, extension, background service, API, worker, database, queue, cache, CLI binary. For each: responsibility, technology (pinned from the stack reference), where it runs, how it talks to its neighbours (protocol, sync or async, auth) | all |
| 3b Supported platform matrix | One row per platform in `studio.yaml`: minimum and newest tested OS or browser (from `min_targets`), form factors, shared versus platform-specific, the policy for raising the floor; plus constraints that shape the design (background limits, sandboxing and entitlements, store rules). The platform leads own it | standard, full |
| 4 Components (C4 level 3) | For each container that warrants it: modules, what each owns, allowed dependency direction and how it is enforced, public surface, test seams. Not every container; say which were skipped and why. Add a `### Key flows` subsection: sequences of two to four critical paths (sign in, the core job, sync, update) across containers, with failure at each hop | standard, full |
| 5 Data | Entities and who owns each, source of truth versus cache, store per kind of data, format and version, lifecycle and retention, schema evolution and migration approach (`/app-data-migration`), sync and conflict policy, backup and restore, on-device storage and its encryption | all |
| 6 Deployment topology | Environments (local, test, staging, production or the app's equivalent), hosting, how each container is built, signed, released, updated and rolled back; per-platform distribution (store, installer, package manager, self-hosted container); config and where secrets live (never values) | all |
| 7 Trust boundaries and security posture | Boundaries on the container diagram, who is on each side, authentication and authorization model, validation and encryption, secrets, IPC and update integrity, and what goes to `/app-threat-model` | standard, full |
| 8 Cross-cutting concerns | One decision each with its ADR link: error handling, logging, configuration, authentication and sessions, authorization, localization, accessibility hooks, feature flags, concurrency and cancellation, offline and retry, updates, telemetry | standard, full |
| 9 Budgets and observability | Performance (startup, interaction latency, p95 API, frame time, memory, bundle or binary size, battery), availability target, cost ceiling, data limits, each with a target, how and where it is measured, and an owner (`target unknown` is allowed and listed, never invented); logs, metrics, traces, crash reporting, analytics, alerts and SLOs, and what is deliberately not collected | all (fewer at minimal) |
| 10 Key decisions | Each architecture-shaping decision with its ADR and status (a decision without an ADR is `UNRECORDED`; Proposed ADRs are listed as Proposed). Add a `### Requirements traceability` subsection: each baseline row mapped to the container or ADR that satisfies it, or `UNCOVERED` | all (traceability: full; standard lists uncovered rows only) |
| 11 Risks, open questions and evolution | Top technical risks with mitigation, open questions each with an owner and the layer it must be resolved before, known debt, expected change at 10 times load or with a second platform. At full add a `### Failure modes` table: what happens when each dependency is down, slow or wrong; timeouts, retries and backoff, idempotency, degraded modes, data-loss windows; and capacity assumptions | all (failure modes: full) |
| Provenance table | Only in `from-code` mode, with the banner | from-code |

At minimal rigor the template says the document is not required: a half page in the brief or `docs/decisions.md` (context, main parts, where data lives, one risk) is enough. If the user wants a file anyway, write sections 2, 3, 5 and 11 briefly and decisions go to `docs/decisions.md` instead of ADRs. Standard is sections 1 to 10. Full adds the failure-mode table, capacity assumptions, per-environment topology and an ADR for every foundation decision.

Decision rules: never make a binding choice without the user. If the user is unsure, present two to four options with costs. A conflict between an existing Accepted ADR and a new decision is surfaced; the document does not silently contradict an ADR (supersede it via `/app-adr`, or revise the proposal).

Check after each section: written with real content, not a placeholder; cited requirement rows exist in the baseline.

## Phase 4: Platform routing for container content

| App kind | Containers section must include | Deployment section must include |
|---|---|---|
| Web client plus API | Rendering strategy and where state lives; API; database; CDN or static host; auth provider | Build and deploy pipeline, environments, cache and invalidation, rollback |
| Desktop | Main process and renderer or UI process split if any, native module boundaries, local store, background helper or service, update client | Installer format, signing and notarization, update channel and rollback, per-OS differences |
| Mobile | App, extensions and widgets, push, local store, sync client, backend | Store tracks, staged rollout, minimum OS policy, forced-update strategy |
| Backend service | Services or modules, API surface, queue and workers, stores, scheduled jobs | Container or host layout, scaling, migrations in deploy, secrets, health checks |
| CLI or library | Command surface or public API, plugin points, config and state files | Distribution channels, version and compatibility policy |
| Extension | Background, content and UI surfaces, message passing, permissions | Store review path, update behavior |

## Phase 5: ADR audit and required-ADR list

Main session, using what is already loaded.

1. List every existing ADR with its status. A table of: ADR, status, conflicts with this document (none or what), platform/version risk recorded (yes/no), requirements addressed (yes/no). Status words are read from each ADR's `## Status`; an ADR without one is `NOT ASSESSED - no status`.
2. Coverage: each baseline row against ADRs. A requirement covered only by a `Proposed` ADR is "covered (Proposed)", not covered; say so and name the route (`/app-adr accept`).
3. Required new ADRs: every decision made in Phase 3 without an ADR, plus uncovered baseline rows, grouped Foundation (before any code), Core, Feature, with the requirement rows each covers. At minimal rigor this becomes the list of entries to add to `docs/decisions.md`.

Write the audit and the list into the document: statuses and the `UNRECORDED` decisions in section 10 (Key decisions), the open items in section 11.

## Phase 6: Gates

Apply the review mode (`orchestration.md` section 7). Both gates run in `full` review mode only (`gates/README.md`: neither is a phase gate or always-on); `lean` prints `TD-ARCHITECTURE skipped: lean mode` and `PE-FEASIBILITY skipped: lean mode`, and `solo` prints the same with `solo mode`.

In `full`, run them in order, because `PE-FEASIBILITY` is defined to run before `TD-ARCHITECTURE`: first spawn `principal-engineer` for `PE-FEASIBILITY` with the document path, the ADR paths, the stack reference, the module map if code exists, any prototype reports and the app's `specialists:`; then spawn `technical-director` for `TD-ARCHITECTURE` with the document path, the requirements baseline, the ADR list with statuses, the stack reference path, the knowledge gap list, the budgets, and the `PE-FEASIBILITY` result (and the `SL-THREAT-MODEL` result if that gate has run). Each reads its own gate file. Verdict words: `PE-FEASIBILITY` VIABLE, CONCERNS, HIGH RISK; `TD-ARCHITECTURE` APPROVE, CONCERNS, REJECT; either may be NOT ASSESSED (the document or the stack reference missing).

Present both verdicts together; CONCERNS: revise, accept (recorded in section 11) or discuss, as an ask. REJECT or HIGH RISK: no accept option; revise first and re-run that gate. Record each directly under the title (the template's review line) as `> **Technical Director review (TD-ARCHITECTURE)**: <APPROVE | CONCERNS | NOT ASSESSED> <date>` and `> **Principal Engineer review (PE-FEASIBILITY)**: <VIABLE | CONCERNS | NOT ASSESSED> <date>`; no line for a skipped gate. NOT ASSESSED is never recorded as an approval.

## Phase 7: Handoff

Update the checkpoint. Print the required-ADR list in priority order (top three with one sentence each), the open questions, and readiness for the architecture exit gate: required ADRs written and Accepted, threat model done where rigor needs it, stack reference pinned, budgets set. Recommend the next skill; do not start it.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Sections | Not required; a half page, or short 2, 3, 5 and 11 | 1 to 10 (with 3b for each platform) | All, with failure modes, capacity assumptions and traceability |
| Decisions recorded in | `docs/decisions.md` | ADRs for foundation decisions | ADRs for every significant decision |
| Diagrams | Context and containers | Plus components of key containers and key flows | Plus trust boundaries on the diagrams |
| Gates (set by review mode, not rigor) | solo and lean: skipped | solo and lean: skipped | full mode: PE-FEASIBILITY, then TD-ARCHITECTURE |

## Verdicts

First match wins: BLOCKED, then NOT ASSESSED, then COMPLETE.

- BLOCKED: no purpose or requirements can be established, a required platform lead or `principal-engineer` artifact is missing after one re-brief, an unresolved conflict with an Accepted ADR, or a gate returned REJECT or HIGH RISK.
- NOT ASSESSED: the document is written, but a gate that ran returned NOT ASSESSED (for example `PE-FEASIBILITY` with no stack pins) and the input was not supplied, or the requirements baseline is `NOT ASSESSED - no specs` and the user did not state the significant requirements. The verdict line names each item. Smaller gaps, such as `budgets for 3 of 7 attributes target unknown`, are listed on the line without changing the verdict.
- COMPLETE: every section required at this rigor is written and approved and nothing above applied.

## Report

```
Architecture: <path>  Version <n>  Mode: <full | update | from-code>
Containers: <n>  Components detailed for: <n of n>  Data stores: <n>  Environments: <n>
Requirements baseline: <n rows, n covered, n uncovered, n target unknown>
ADRs: <n existing (n Accepted, n Proposed)>, <n required new>
Knowledge gaps: <list or "0 in N dependencies">
Provenance (from-code): <n claims sourced, n INTENT UNKNOWN, n NOT SOURCEABLE>

Verdict: <COMPLETE | BLOCKED | NOT ASSESSED> - <one line why>
Gates: <TD-ARCHITECTURE: V, PE-FEASIBILITY: V> | none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never decide an architectural choice for the user; propose and ask.
- Never assert a version, API or platform capability that is not in the stack reference or verified from an official source; mark it `UNVERIFIED`.
- Never silently contradict an Accepted ADR. Never create or accept an ADR here (`/app-adr`).
- Every diagram has a table equivalent. Every budget has a target, a measurement method and an owner, or is listed as unknown.
- In `from-code` mode never present reconstruction as intent; unconfirmed intent stays marked.
- Write each approved section as it is approved; never hold the whole document in conversation until the end.
