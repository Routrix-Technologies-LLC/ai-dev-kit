# Architecture: [Product name]

<!--
WRITTEN BY: technical-director owns it; principal-engineer, the platform leads for the app's platforms and security-lead contribute. Skill: /app-architecture (new design) or /app-adopt (documented from code).
LIVES AT: docs/architecture/architecture.md (override: paths.architecture in studio.yaml).
RIGOR: minimal = not required; a half page in the brief or the decision log (context, main parts, where data lives, one risk) is enough.
       standard = sections 1 to 10; diagrams in text (C4 levels 1 to 3 as lists or Mermaid), budgets with numbers, every key decision links an ADR.
       full = standard plus failure-mode table, capacity assumptions, per-environment topology, an ADR for every foundation decision, and TD-ARCHITECTURE plus PE-FEASIBILITY passed.
GATES: TD-ARCHITECTURE, PE-FEASIBILITY.
Use the C4 model (context, containers, components; code level only where it earns its place). Name each box once and keep names identical to the code, repo folders and ADRs.
Describe what is decided and why; mark undecided parts OPEN with an owner. Facts about specific hosts live in the infra record, not here. Never include credentials.

PROVENANCE VARIANT: when this document is reverse-engineered from an existing codebase (/app-adopt), keep the banner below at the top and keep the INTENT UNKNOWN markers until the user confirms or corrects them. Delete the banner only when every marker is resolved. Otherwise delete the banner now.
-->

> **DOCUMENTED FROM CODE, NOT DESIGNED.** Written on [YYYY-MM-DD] by [agent] from the repository at commit [hash]. Structure and behavior below were observed in the code; the reasons were not recorded. Items marked **INTENT UNKNOWN** are inferences the user has not confirmed: they describe what the code does, not what was meant. Do not treat them as decisions. Each confirmed item should become an ADR (retrofit via /app-adr).

> **Technical Director review (TD-ARCHITECTURE)**: [VERDICT date, recorded by /app-architecture]

**Status:** [Draft | Reviewed | Approved]   **Last verified against code:** [YYYY-MM-DD, commit]   **Owner:** technical-director

## 1. Context and goals
<!-- What the system is for (link the brief or vision), the quality attributes that matter most and their rank (for example security, offline use, startup time, cost, maintainability), constraints that are fixed (platform, team size, budget, licensing, regulations), and non-goals. These ranked qualities decide every later trade-off. -->
- **Top qualities, ranked:** [1, 2, 3]
- **Constraints:** [list]
- **Non-goals:** [list]

## 2. System context (C4 level 1)
<!-- The system as one box, the people who use it (personas, roles) and the external systems it talks to (identity providers, payment, stores, APIs, OS services). One line per relationship with protocol and direction. -->
```
[Person: persona] --uses--> [System] --calls (protocol)--> [External system]
```
| Actor or external system | Relationship | Protocol and data | Owner and trust level |
|---|---|---|---|

## 3. Containers (C4 level 2)
<!-- Separately runnable or deployable units: client apps, services, workers, databases, caches, queues, file stores, extensions. For each: responsibility, technology (language, framework, runtime, from the stack reference), and how it talks to the others. -->
| Container | Responsibility | Technology | Talks to (how) | Runs where |
|---|---|---|---|---|

## 3b. Supported platform matrix
<!-- Owned by the platform leads. One row per platform in studio.yaml: minimum and newest supported OS or browser, devices or form factors, what is shared versus platform-specific, and the policy for raising the floor. Other docs link here instead of repeating it. -->
| Platform | Minimum | Newest tested | Form factors | Shared vs platform-specific |
|---|---|---|---|---|

## 4. Components (C4 level 3)
<!-- Only for containers whose internals matter. The main modules, their single responsibility, allowed dependency direction (layers; no cycles), public interfaces and where the seams for testing are. State the rule that enforces layering and how it is checked (lint rule, module boundary, review). -->
### [Container name]
| Component | Responsibility | Depends on | Exposes | Notes |
|---|---|---|---|---|

**Dependency rules:** [text, and how enforced]

## 5. Data
<!-- Entities and ownership (which container is the source of truth), storage technology per kind of data, schema and format versioning, migration approach (link data-migration plans), consistency model, caching and invalidation, backup, retention and deletion, sync and conflict resolution if multiple writers or devices. Link the privacy record for personal data. -->
| Data | Source of truth | Store | Format and version | Retention | Sensitivity |
|---|---|---|---|---|---|

## 6. Deployment topology
<!-- Where each container runs per environment (local, test, staging, production) and per platform (installers, stores, hosts). Build and release flow in one paragraph, configuration and secret handling (where secrets live, never their values), update mechanism for client apps, scaling and redundancy for services, and the rollback path. -->
| Environment or channel | Containers | Hosted or distributed via | Config and secrets | Update path |
|---|---|---|---|---|

## 7. Trust boundaries and security posture
<!-- Where the trust level changes: network edges, process and sandbox boundaries, IPC, extensions, user-supplied files, third-party code. For each boundary: who is on each side, how identity is established, what is validated, what is encrypted. This section seeds the threat model (docs/security/threat-model.md); keep them consistent. -->
| Boundary | Between | Authentication and authorization | Validation and encryption | Threat model ref |
|---|---|---|---|---|

## 8. Cross-cutting concerns
<!-- One decision each, with the ADR link: error handling and result types; logging; configuration; authentication and sessions; authorization; localization and time zones; accessibility hooks; feature flags; dependency injection or composition; concurrency and cancellation; offline and retry behavior; updates; telemetry (privacy-first). -->
| Concern | Approach | ADR |
|---|---|---|

## 9. Budgets and observability
<!-- Budgets are numbers with a measurement method and a target device or load: startup time, interaction latency, frame time or jank, memory, binary or bundle size, battery or CPU, request latency percentiles, throughput, cost per month. Observability: logs, metrics, traces, crash reporting, SLOs and alerts, and what is deliberately not collected (privacy). Link perf-budget.md if it exists. -->
| Budget or SLO | Target | Measured how, on what | Owner |
|---|---|---|---|

| Signal | Where it goes | Retention | What it answers |
|---|---|---|---|

## 10. Key decisions
<!-- The architecture-shaping decisions, each a one-line summary linked to its ADR. A decision without an ADR is marked UNRECORDED. Proposed ADRs are listed as Proposed; only Accepted ones are binding. -->
| Decision | ADR | Status |
|---|---|---|

## 11. Risks, open questions and evolution
<!-- Top technical risks with mitigation and the ADR or prototype that will retire them; OPEN questions with owner and date; known debt (link tech-debt register); how the design is expected to change at 10 times the load or data or with a second platform. -->
| Risk or question | Likelihood and impact | Mitigation or next step | Owner |
|---|---|---|---|

## Provenance table (documented-from-code variant only)
<!-- Delete this section if the banner at the top was deleted. One row per claim that came from the code. Observed means seen in code or config at the cited place. INTENT UNKNOWN means the reason is a guess. -->
| Statement | Evidence (file and symbol or commit) | Status (Observed / INTENT UNKNOWN / Confirmed by user) |
|---|---|---|
