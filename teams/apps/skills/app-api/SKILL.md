---
name: app-api
description: "Design or review an interface contract (REST, GraphQL, gRPC, WebSocket or event messages, desktop or extension IPC, library public API) and detect breaking changes against the previous version by diffing the schema and listing every consumer. Use when the user designs a new API, changes an existing endpoint, message or command, asks whether a change breaks clients, or before releasing a contract change."
argument-hint: "[app] [design <name> | review <name>] [--review solo|lean|full]"
user-invocable: true
---

# App API

Produces or reviews the contract between two programs: a service and its clients, a UI and its native host, an extension and its page, a library and its callers. The contract is a file (schema, SDL, proto, command list), not prose, and every change to it is compared against the last released version before anyone is told it is safe.

Writes: `docs/architecture/api/<name>.<ext>` (template `api-contract.md` for the human-readable part; the machine-readable schema beside it), and review notes at `docs/architecture/api/reviews/<name>-<date>.md`.
Next: `/app-plan` (stories for the change), `/app-threat-model` (new trust boundary), `/app-data-migration` (if storage changes with it), `/app-code-review`.

## When to use and when not to

- Use for any interface another program depends on, new or changed.
- A decision about which protocol or framework to use is `/app-stack` or `/app-adr`. Database schema changes are `/app-data-migration`. A whole-system design is `/app-architecture`.

## Inputs

- Required: `studio.yaml`; for `review`, the contract file (or code that defines it) and the previous version. If the previous version cannot be found (no git history, no tag, no released copy), the breaking-change check is NOT ASSESSED; say so and offer to establish a baseline from the last release or the deployed service.
- For `design`: the spec or story that needs the interface (`docs/product/specs/`), the architecture doc, and the consumer list if known. Missing spec: ask what each consumer needs; do not design in a vacuum.
- Optional: existing contract tests, API gateway or generated clients, a deprecation policy in the architecture doc.

## Contract styles and routing

| Style | Contract artifact | Lead and specialists | Breaking-change diff tool (use what the stack has; install nothing without asking) |
|---|---|---|---|
| REST | OpenAPI document | `backend-lead`, `api-designer`, `backend-engineer` | An OpenAPI diff tool, else a structured manual diff of paths, parameters, schemas, status codes |
| GraphQL | SDL | `backend-lead`, `api-designer` | A GraphQL schema diff or inspector, else SDL text diff |
| gRPC and protobuf | `.proto` files | `backend-lead`, `api-designer`, language specialist | A protobuf breaking-change checker, else field-number and type diff |
| WebSocket, SSE, queues | message catalog (AsyncAPI or table of message types, payloads, ordering, delivery guarantees) | `distributed-systems-engineer`, `api-designer` | Manual diff of the catalog |
| Desktop IPC (named pipes, XPC, D-Bus, Tauri or Electron commands, native bridge) | command list with argument and result types, caller identity, capability required | `desktop-lead`, `hybrid-desktop-engineer` or the OS engineer | Diff of the command list and its type definitions |
| Mobile platform channels, extensions, app extensions | channel or message list | `mobile-lead`, `cross-platform-mobile-engineer` or the platform engineer | Manual diff |
| Browser extension messaging | message types and permission map | `web-platform-engineer` | Manual diff |
| Library public API | exported symbols and signatures | `principal-engineer`, language specialist | The language's public-API diff or semver-check tool, else a diff of exported declarations |

Always also: `security-engineer` (authentication, authorization, input handling, rate limits, data exposure). Consumers' leads are added in Phase 3 from the consumer list: a mobile client brings `mobile-lead`, a web client `web-lead`, a desktop client `desktop-lead`.

## Phase 1: Resolve and announce

Per `orchestration.md` sections 1 and 2. Decide the style from the argument and the files. Mixed (a REST API plus a WebSocket channel) means one contract per interface, reviewed in the same run.

Check: announce block printed, contract style(s) named, previous-version source named or marked missing.

## Phase 2: Inventory consumers

Before judging any change, find who depends on the contract. Main session, by search, not by asking first.

1. Search the app repo for generated clients, SDK wrappers, route calls, schema imports, message names, command names and permission lists.
2. Read `studio.yaml` and the architecture doc for external consumers (other apps, partners, older released clients still in the field, third-party integrations, webhooks sent to others).
3. Build a table: consumer, how it depends (generated client, hand-written call, raw message), version range in the field, who owns it, how it is updated (deploy together, app store release lag, user-controlled update, out of the team's control).
4. A consumer that cannot be updated in lock step (mobile app versions in the wild, third parties, installed desktop clients, stored webhook URLs) makes any breaking change a multi-release migration.

Decision point: show the table and ask the user to confirm and add missing consumers. An unlisted consumer is the most common cause of a "safe" break.

Check: the consumer table exists with at least the app's own clients, or the statement "no consumers found in N files searched; external consumers unconfirmed" (which caps the verdict at NOT ASSESSED for breaking-change safety).

## Phase 3: Design (design mode) or read (review mode)

### Design

Spawn `api-designer` with the spec, the consumer table and the style. Brief per `orchestration.md` section 3; output: the schema file and the contract document (from `templates/api-contract.md`, keeping its numbered headings: 1 Purpose and scope, 2 Conventions, 3 Operations, 4 Errors, 5 Authentication, authorization and security, 6 Versioning and compatibility, 7 Behavior guarantees, 8 Consumers and change impact, 9 Examples, 10 Testing and tooling, Change log; section 8 is the Phase 2 consumer table) at the exact paths. The brief requires, for every interface:

- Resource and operation naming, one convention throughout; every operation tied to a requirement ID from the spec.
- Error model (a standard such as RFC 9457 problem details for HTTP APIs, typed errors for IPC), with stable machine-readable codes and which errors are retryable.
- Idempotency for every unsafe operation that can be retried; pagination, filtering and sort for every list; limits on payload size and rate.
- Authentication, authorization (who may call, with which scope or capability), and what data each response exposes. For IPC: the caller identity check and the capability each command needs, default deny.
- Versioning and deprecation policy: how a version is named, how long old versions are supported, how clients learn of a deprecation.
- Evolution rules: additive changes only within a version; unknown fields ignored by consumers; enums treated as open; new required fields never added to existing requests.
- Timeouts, ordering and delivery guarantees for realtime and queue messages (at most once, at least once, exactly once, and what the consumer must do about duplicates).
- Examples for every operation, including one error.
- Contract tests the consumers can run, named per consumer.

Spawn in parallel with it: `security-engineer` (threat check of the draft's trust boundaries, run after the draft exists, so sequence it second), and for realtime or queue interfaces `distributed-systems-engineer` (ordering, retries, backpressure).

### Review

Spawn the style's specialists and `security-engineer` in parallel, each reading the contract and the diff against the previous version (Phase 4 results go to them if already run; otherwise run Phase 4 first). Each writes one findings file under `~/AgentScratch/app-api/<run>/`. Findings carry severity per `standards/severity.md` (CRITICAL, HIGH, MEDIUM, LOW).

Check: contract file(s) exist on disk with real content; every operation has an error case, an auth statement and an example; or the review findings files exist.

## Phase 4: Breaking-change detection

Mandatory for `review` and for `design` when a previous version exists.

1. Obtain the previous version: the file at the last release tag or last deployed commit (`git show <tag>:<path>`), or the deployed service's published schema. Record which one and its identifier. Never compare against the working tree's own earlier edit.
2. Diff the schema files with the style's tool, or by hand where none exists. Record the tool and its version, or "manual diff".
3. Classify each difference:

| Change | Class |
|---|---|
| Remove or rename an operation, field, enum value, command, message, exported symbol | BREAKING |
| Change a type, format, nullability, unit or meaning of a field | BREAKING |
| Add a required request field, parameter or capability; tighten validation | BREAKING for requests |
| Add a new response field, optional request field, operation or message type | compatible (consumers must ignore unknown fields: verify they do) |
| Add an enum value | compatible only if consumers treat enums as open; otherwise BREAKING |
| Change a status code, error code, ordering, delivery or default behavior | BREAKING (behavioral; the schema diff will not show it) |
| Change auth or permission requirements | BREAKING for existing callers |
| Protobuf field number reuse or type change; GraphQL output field changing from non-null to nullable, or an input field or argument becoming non-null or required; JSON Schema or OpenAPI response field becoming optional or nullable | BREAKING |

4. For each BREAKING item, list the affected consumers from Phase 2 (name each; "all" is not a list) and whether each can update in step with the change.
5. A diff that shows nothing is verified by one deliberate probe: confirm the tool saw both files (counts of operations or types on each side are stated). Zero differences from zero parsed operations is NOT ASSESSED.
6. Behavioral changes the diff cannot see (semantics, timing, defaults) are found by reading the code diff for handlers and the contract tests; list them as UNVERIFIED if no test covers them.

Check: a diff section exists naming both versions, the tool, the operation counts on each side, and every difference classified.

## Phase 5: Resolve breaking changes

If any BREAKING item exists, the main session presents it with the consumers and asks the user how to proceed (AskUserQuestion, 2 to 4 options):

- Make it compatible (keep the old field or operation, add the new beside it, deprecate with a date).
- Version it (new version path, media type or package; both served for the stated support window).
- Break it on purpose (in `full` review mode, `technical-director` first reviews the change with `TD-CHANGE-IMPACT` when stories or code already depend on the contract; needs: major version bump, a consumer migration plan with dates, a deprecation notice drafted, and `release-manager` informed; recorded as an ADR via `/app-adr` at standard and full rigor).

Never choose for the user. Record the answer in the review notes.

## Phase 6: Write and gate

Ask once for the file set, then write the contract document, the schema file and the review notes. The review notes carry: versions compared, tool, consumers, differences with classes, findings by severity, the user's decision on each break, UNVERIFIED items, and follow-up stories to propose to `/app-plan`. Update the checkpoint.

No gate is attached to this skill; the only gate it may invoke is `TD-CHANGE-IMPACT` in full mode, for a deliberate break. Technical risk that spans systems may be sent to `/app-architecture` (TD-ARCHITECTURE).

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Contract detail | operations, types, errors, auth (a private interface with one producer and one consumer in one repo may skip the document: the types are the contract) | plus pagination, idempotency, limits, versioning policy | plus consumer contract tests per consumer and a deprecation calendar |
| Breaking-change check | always | always | always, plus behavioral review of handlers |
| Security review | `security-engineer` on auth and data exposure | plus abuse cases and rate limits | plus `identity-specialist` when auth design changes |

Review mode: no gates run in this skill at any mode; the closing block's Gates line reads `none run (no gate attached to app-api)`, or the `TD-CHANGE-IMPACT` verdict (CONTAINED, CONCERNS, WIDE IMPACT, NOT ASSESSED) when it ran.

## Verdicts

First match wins.

1. `BREAKING`: at least one breaking difference exists, whatever the user decided in Phase 5. The report states whether each was resolved as compatible, versioned or accepted.
2. `CHANGES REQUIRED`: no breaking difference, but a finding of CRITICAL or HIGH severity is open, a required contract element is missing (error model, auth statement, version policy), or a compatible change relies on consumers ignoring unknown fields and that is unverified.
3. `NOT ASSESSED`: the previous version was unavailable, the diff tool could not parse a side, the consumer list is unconfirmed, or a spawned reviewer returned nothing. State which.
4. `APPROVED`: contract complete, a real diff against a named previous version shows only compatible changes (or this is a first version, stated as such), consumers confirmed, no open CRITICAL or HIGH finding.

A first version of a brand-new interface has no previous version; that is stated and is not NOT ASSESSED, but the consumer list must still be confirmed.

## Report

```
API: <name> (<style>)   Mode: <design|review>
Compared: <previous identifier> vs <current>   Tool: <name or manual>   Counts: <ops/types old> vs <new>
Differences: <N> (BREAKING <N>, compatible <N>, behavioral UNVERIFIED <N>)
Consumers: <name: affected or not, can update in step: yes/no> ...
Findings: CRITICAL <N>, HIGH <N>, MEDIUM <N>, LOW <N>
User decisions: <break handling per item>
Skipped: <step or agent and why>
Proposed stories: <list>
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- The contract file is the source of truth; prose never contradicts it.
- A breaking-change claim or a no-break claim always names both versions compared and the consumers checked.
- Never compare a file to itself or to the working tree's own earlier edit.
- Never edit service or client code here; stories carry the implementation.
- Never add a required field to an existing request, remove a field, or reuse a protobuf field number in a "compatible" proposal.
- Never decide how to handle a break for the user.
- Never claim consumers are unaffected without having searched for them; say how many files were searched.
