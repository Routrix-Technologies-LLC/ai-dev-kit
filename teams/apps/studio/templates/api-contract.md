# API Contract: [Interface name] v[major.minor]

<!--
WRITTEN BY: api-designer with backend-lead and the leads of every consumer; security-engineer reviews. Skill: /app-api.
LIVES AT: docs/architecture/api/<name>.md as the human-readable contract, next to the machine-readable schema docs/architecture/api/<name>.<ext> (OpenAPI, GraphQL SDL, protobuf, JSON Schema, or a typed command list for IPC). Override: paths.api. The schema file is the source of truth for shapes; this file is the source of truth for meaning, guarantees and policy.
RIGOR: minimal = skip for a private interface with one producer and one consumer in one repo; the types are the contract.
       standard = sections 1 to 9 for any interface crossing a process, network or release boundary; schema file present; breaking-change check on every change.
       full = standard plus consumer inventory with contact, deprecation calendar, contract tests in CI and the compatibility test matrix per client version.
Applies to any interface: REST or other HTTP, GraphQL, gRPC, WebSocket and event streams, desktop IPC, browser extension messaging, library public API, CLI flags and exit codes.
Design for the consumer who is not reading this file at the moment: every error is understandable, every field has a meaning, every change has a version rule.
-->

**Status:** [Draft | Reviewed | Stable | Deprecated]   **Owner:** [role]   **Schema file:** [path]   **Last updated:** [YYYY-MM-DD]
**Producer:** [component]   **Consumers:** [component, client, third party; see section 8]

## 1. Purpose and scope
<!-- What the interface is for, who calls it, what it deliberately does not do, and the transport and style (resource-oriented HTTP, RPC, event). Name the architecture container it belongs to. -->

## 2. Conventions
<!-- State once, apply everywhere: naming (case, plurals), identifiers (opaque, type, who generates), time (UTC ISO 8601 or numeric epoch; which), money and units, nullability versus absence, enums and how unknown values must be handled by clients, pagination (cursor preferred; page size limits), filtering and sorting, idempotency (keys for unsafe retries), partial updates, content types, character limits, request size limits, and rate limits with headers or fields that report them. -->
| Topic | Rule |
|---|---|

## 3. Operations
<!-- One row per operation (HTTP method and path, RPC method, message type, command, function). Link the schema anchor for exact shapes. Say what the operation guarantees (idempotent, atomic, ordered, at-least-once) and its side effects. -->
| Operation | Purpose | Request (key fields) | Response (key fields) | Auth / permission | Idempotent | Since |
|---|---|---|---|---|---|---|

## 4. Errors
<!-- One error model for the whole interface. For HTTP use problem details (RFC 9457): type, title, status, detail, instance, plus stable machine-readable error codes. List each code once: meaning, whether retryable, what the caller should do. Errors never leak internals, stack traces or other users' data. Validation errors point at the offending field. -->
| Code / status | Meaning | Retryable | Caller action |
|---|---|---|---|

## 5. Authentication, authorization and security
<!-- Identity mechanism and token or credential lifetime, scopes or roles per operation, transport security, input validation and output encoding rules, CORS or origin checks for browser exposure, message signing or origin verification for IPC and extensions, abuse limits, audit logging of sensitive actions, and the data classification of each payload (link the privacy review). No secrets in URLs or logs. -->
| Operation or group | Required permission | Notes |
|---|---|---|

## 6. Versioning and compatibility
<!-- The policy, stated so a consumer can plan: version scheme (semantic version of the contract; major in the URL, header, package or message envelope), what counts as breaking (removing or renaming a field or operation, changing a type, tightening validation, changing meaning, adding a required request field, changing an error code, removing an enum value) versus compatible (adding optional fields, operations or enum values clients must tolerate), the deprecation process (announcement, a Deprecation or Sunset signal, minimum support window, removal), and how old clients are handled. Producers must follow the robustness rule: be conservative in what is sent, tolerant of what is received. -->
- **Current version and supported range:** [text]
- **Breaking change process:** [text]
- **Deprecation window:** [duration]

## 7. Behavior guarantees
<!-- Ordering, delivery semantics (at most once, at least once, exactly once effect via idempotency), consistency (read-your-writes? eventual?), timeouts and retry guidance with backoff and jitter, limits, caching headers and validation, pagination stability, large payload handling, and service levels (availability and latency targets, if any). -->
| Guarantee | Statement | How verified |
|---|---|---|

## 8. Consumers and change impact
<!-- Every known consumer, what it uses, who owns it and its minimum supported contract version. Used by /app-api to find who a change breaks. An unknown consumer set for a public interface is a risk: say so. -->
| Consumer | Operations used | Min version | Owner | Upgrade path |
|---|---|---|---|---|

## 9. Examples
<!-- At least one complete successful exchange and one error exchange per operation group, valid against the schema, with no real personal data. Examples are tested in CI where possible. -->

## 10. Testing and tooling
<!-- Contract tests (producer and consumer), schema linting, breaking-change diff against the previous released schema, mock server or fixtures, and the command that runs them (studio.yaml commands). -->

## Change log
| Version | Date | Change | Breaking | Consumers notified |
|---|---|---|---|---|
