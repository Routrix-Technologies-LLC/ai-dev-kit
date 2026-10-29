# Tracking Plan: [Product name]

<!--
WRITTEN BY: analytics-specialist with product-manager (questions), privacy-specialist (classification and consent) and the platform engineers (implementation). Skills: /app-brief (metrics), /app-spec (events per feature), /app-observability (operational telemetry), /app-privacy-review (reconciliation).
LIVES AT: docs/product/tracking-plan.md (a studio.yaml `paths:` note if kept elsewhere). Event lists in feature specs link here.
RIGOR: minimal = "No analytics" as an explicit statement, or at most 5 events, each with a question it answers, a trigger and a privacy note.
       standard = every section; each event has an owner, a privacy classification and a consent rule; events reconcile with the privacy review.
       full = standard plus a schema registry or typed event definitions in code, automated validation in CI, a sampling and retention policy, and a quarterly pruning review.
Rule: no event without a product question it answers. Collect the least that answers it. Privacy-first by default: aggregate rather than individual, on-device rather than server, opt-in where optional, and never personal content, free text typed by users, precise location, contacts or credentials in an event.
Operational telemetry (logs, traces, crash reports) is described in the architecture's observability section; list here only the product-analytics events and any crash or diagnostics events that carry user or device data.
-->

**Status:** [Draft | Approved | Implemented | Audited]   **Last updated:** [YYYY-MM-DD]   **Tool or backend:** [name, hosting, region, or "local only"]

## 1. Questions and metrics
<!-- The questions the data must answer, each tied to a metric from the vision or brief. If a question cannot lead to a decision, drop it, and its events. -->
| # | Product question | Metric (definition) | Decision it informs | Events needed |
|---|---|---|---|---|

## 2. Conventions
<!-- Event names: object_action in lowercase snake case, past tense (project_created, export_failed), unique and stable; never rename, deprecate instead. Properties: lowercase snake case, typed, with allowed values or ranges, no free text. Identity: what identifier is used (none, install-scoped random ID, account ID), how it resets, and that it is never an advertising or hardware ID. Time: UTC, client or server stamped. Versions: app version and schema version on every event. Failure events carry an error category, never raw messages. -->
- **Identity model:** [text]
- **Global properties (on every event):** [app_version, platform, os_version_major, locale, schema_version]
- **Naming rules:** [text]

## 3. Events
<!-- One row per event. Privacy classification: P0 no personal data (counters, categories, booleans), P1 pseudonymous identifiers or device data, P2 personal data, P3 sensitive personal data (should not be collected here). Consent requirement: None (strictly necessary or no personal data), Opt-out (on unless disabled, only where law and the privacy review allow), Opt-in (off until enabled). Anything above P0 needs a privacy-review reference. -->
| Event name | Trigger (exact moment) | Properties (name: type, values) | Privacy class | Consent requirement | Owner | Platforms | Question # | Since |
|---|---|---|---|---|---|---|---|---|

## 4. Property dictionary
| Property | Type | Allowed values or range | Used by events | Privacy class | Notes |
|---|---|---|---|---|---|

## 5. Consent and controls
<!-- Where the user chooses, the default, how a change takes effect immediately (queued events dropped if consent is withdrawn), the state shown in settings, regional behavior, and how the setting is stored. Link the privacy review's consent section. -->

## 6. Implementation and validation
<!-- Where events are emitted in code (a single wrapper, not scattered calls), batching and offline behavior, failure handling that never blocks the UI, how events are tested (unit tests assert the payload; a debug view in non-production builds), a payload size limit, and how the plan and code are kept in sync. -->
- [Wrapper path, test command, validation rule]

## 7. Retention, access and deletion
<!-- Retention per event class, who can access raw and aggregated data, how a deletion request is honored in the analytics backend, and export of the data. -->
| Data class | Retention | Access | Deletion path |
|---|---|---|---|

## 8. Deprecated and removed events
| Event | Deprecated on | Replaced by | Removed on |
|---|---|---|---|
