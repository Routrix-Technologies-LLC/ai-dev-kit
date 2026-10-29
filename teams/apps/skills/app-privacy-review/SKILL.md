---
name: app-privacy-review
description: "Inventory the personal data an app collects, stores, shares and infers, map its flows, retention and consent, reconcile that against what is declared, and draft the store privacy declarations. Use when the user asks for a privacy review, data inventory, GDPR or CCPA readiness, privacy labels, a Play data safety form, a privacy manifest, or before adding analytics, an SDK, accounts or a new data type."
argument-hint: "[app] [full | delta | <feature or SDK>] [--review solo|lean|full]"
user-invocable: true
---

# App privacy review

Builds the app's data inventory from what the code, configuration and running app actually do, not from what anyone remembers, then compares it to what the product and its store listings say. The output is a privacy record and draft declarations. It is engineering input for a human sign-off, not legal advice, and it never declares compliance with a law.

Writes: `docs/security/privacy.md` from template `privacy-review.md` (updated in place; a dated change entry is appended, earlier entries are kept). Store declaration drafts are sections inside it; `/app-store-prep` consumes them. Evidence in `docs/qa/evidence/privacy-<date>/`.
Next: `/app-threat-model` if data flows reveal untreated trust boundaries; `/app-store-prep` for submissions; `/app-observability` when telemetry needs redesign; `/app-gate` or `/app-release` consume the result.

## When to use and when not to

Use at the start of data-handling work, before release, when adding an SDK, analytics, accounts, sync, an AI feature or a new permission, and when preparing store forms. Not for: a vulnerability audit (`/app-security-audit`), the design of telemetry events (`/app-observability` with `analytics-specialist`), or drafting terms and the privacy policy text as a legal document (the privacy-specialist drafts product-facing notices here; a human with authority signs off).

## Inputs

- `studio.yaml` (required): `platforms`, `stack`, `hosting`, `commands`, `infra_record`. Stop and offer `/app-adopt` or `/app-start` if absent.
- Optional and read when present: `docs/security/threat-model.md`, `docs/architecture/architecture.md`, specs under `docs/product/specs/`, an existing `docs/security/privacy.md`, store listing drafts in `docs/release/store/`, the app's published privacy policy text.
- The app's audience and markets. If the user has not said whether children can use it, which regions it ships to, or whether it processes sensitive categories (health, finance, precise location, biometrics, political or religious data), ask. Unknown stays UNKNOWN in the record and makes the related checks NOT ASSESSED; it is never assumed to be "no".

## Phase 1: Scope and plan

Main session. Determine scope: `full` rebuilds the inventory; `delta` or a named feature or SDK reviews only that change against the existing record (if no record exists, run `full`). Announce the plan per `orchestration.md` section 2.

Agents: `privacy-specialist` (inventory, flows, retention, rights, declarations), `security-lead` (consulted on storage and transfer safeguards and the gate), `app-store-specialist` (declaration formats and store policy) when any of `ios`, `android`, a store-distributed `macos` or `windows`, or a browser extension store is in `platforms` or the release plan. `analytics-specialist` is consulted when product analytics exist. Not spawned lists must say why.

Gates: `SL-PRIVACY` runs at `lean` (always-on for this skill) and `full`; `solo` prints `SL-PRIVACY skipped: solo mode`.

Check: scope, markets, audience and sensitive-category answers are written into the working notes, with UNKNOWN where unanswered.

## Phase 2: Discover what the app really does

Spawn `privacy-specialist` (and `analytics-specialist` if relevant) in parallel per orchestration sections 3 and 4. Output: `docs/qa/evidence/privacy-<date>/inventory-notes.md`. The brief names the platform routing rows below and these method rules: every data element is traced to a code location, config, SDK manifest or captured request; record the source for each row; an element found in only one place is flagged for the other checks.

| Source | What to look for |
|---|---|
| Code and schemas | fields that hold identifiers, contact data, content, location, device data; database tables and local storage; log statements; analytics and crash calls; AI or ML calls that send user content |
| Dependencies and SDKs | every third-party SDK or API client and what it collects by default (analytics, ads, crash, attribution, auth, payments, maps, push); its own privacy disclosures and manifest |
| Platform declarations | permissions and entitlements requested (and whether each is used), privacy manifests and required-reason API usage on Apple platforms, data safety fields on Play, Microsoft Store and browser extension permission justifications |
| Network behavior | the hosts the running app contacts and what each request carries; captured per section 10 (request capture, headless browser network log, proxy on a simulator), without stealing focus; cookies and local storage for web |
| Backend and hosting | stored data by system, backups, logs and their retention, who has admin access, regions, subprocessors in use, the infra record's facts |
| Lifecycle | account creation and deletion paths, export, consent prompts, age gates, retention jobs |

Capture the app's behavior from a real run when it can be launched. When it cannot, the network behavior row is NOT ASSESSED and the record says the inventory is from static sources only.

Check: the notes file exists and every row of the inventory has a source; a data element without a source is not allowed.

## Phase 3: Build the inventory and flows

Main session with `privacy-specialist`'s notes. Write the inventory into `docs/security/privacy.md` section by section as each is approved (a compaction must lose nothing). For each data element:

| Field | Content |
|---|---|
| Element | e.g. email, device id, precise location, user-generated content |
| Category | identifiers, contact, financial, health, location, content, usage, diagnostics, sensitive, children's data |
| Purpose | why it is collected; functional, analytics, advertising, security, other |
| Source and storage | where it originates, where it is stored on device and server, encryption at rest, region |
| Recipients | internal systems and each third party or subprocessor |
| Linked to identity | yes, no, or pseudonymous; used for tracking across other companies' apps or sites |
| Retention and deletion | how long, what deletes it, whether user deletion reaches backups and processors |
| Basis and consent | consent obtained where, how, revocable how; or the necessity argument, marked for human confirmation |

Then flows: a data-flow diagram in text or Mermaid showing client, services, stores and third parties with trust boundaries. Then rights and lifecycle: access, export, correction, deletion, objection and how each is served. Regulatory flags are listed as QUESTIONS for a human, for example "children may use this: age gate and parental consent rules apply, needs a decision", "data leaves the user's region", "sensitive category present". Name the regime only as a pointer, with no conclusion about compliance.

Check: `docs/security/privacy.md` exists with inventory, flows, retention and rights sections, each populated or marked UNKNOWN with the question that closes it.

## Phase 4: Reconcile declared versus observed

Main session. Compare the inventory against: the app's privacy policy text, the in-app consent and permission copy, current store declarations, SDK vendor disclosures, and the permissions requested. Findings are rated with the review severities:

| Severity | Examples |
|---|---|
| CRITICAL | sensitive or children's data collected or sent to a third party that no document mentions and no consent covers; no way to delete data where deletion is promised or required |
| HIGH | personal data sent to an undeclared third party; a declared "no tracking" or "no data collected" that the app contradicts; a permission requested but not justified or used; retention longer than stated |
| MEDIUM | declaration wording out of date with an SDK; missing consent record; unclear purpose; data kept without a delete path |
| LOW | minimization opportunities, clearer wording, unused fields |

Each finding cites the inventory row, the code or capture that proves it, and the document it contradicts. Spawn `security-lead` for the safeguard questions (encryption at rest and in transit, access, key handling) as a consult; they answer in `docs/qa/evidence/privacy-<date>/security-lead.md`, which the main session reads and attributes.

Check: every declared statement checked has a result (consistent, contradicted, unverifiable). A statement that cannot be verified is listed UNVERIFIABLE, never consistent.

## Phase 5: Draft store declarations

Only for stores the app ships to or will ship to; skip the rest and say which. Spawn `app-store-specialist` and `privacy-specialist` per section 4, one output file each under the evidence folder, then the main session merges into the `Store declarations` section of `docs/security/privacy.md`.

| Target | Draft |
|---|---|
| Apple App Store and Mac App Store | privacy nutrition label answers per data type (collected, linked, tracking), the privacy manifest entries including required-reason API declarations for the app and each SDK, and whether the app tracks (which brings the App Tracking Transparency prompt); verify against the current Apple documentation |
| Google Play | data safety form: collected and shared data types, purposes, optional or required, encryption in transit, deletion request path |
| Microsoft Store | privacy policy URL and capability declarations with justifications |
| Browser extension stores | single-purpose statement, permission justifications, data use disclosures |
| Web and backend | cookie and storage inventory with categories, consent banner needs, policy sections that must exist, subprocessor list |

Each draft answer cites its inventory row. Answers that depend on an UNKNOWN stay `NEEDS INPUT: <question>`. These are drafts; the user submits.

Check: for each in-scope store a draft section exists and every field is filled from the inventory or marked NEEDS INPUT.

## Phase 6: Gate, verify and write

Main session. Verify the claims the verdict turns on: re-read the code or capture behind every CRITICAL and HIGH finding yourself, and confirm one third-party recipient from the captured traffic. Label unchecked claims UNVERIFIED. Run `SL-PRIVACY` when the review mode includes it: spawn `security-lead` with the gate ID, the finding counts, UNKNOWN list and draft status; the agent reads `gates/sl-privacy.md` itself.

Show the user the findings and the questions that need their answers (audience, markets, retention, consent), ask once, update the record, and note unresolved ones as open questions. Never write secrets or real personal data samples into the record; use field names and placeholders.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Inventory | what the app collects and where it goes | plus retention, rights, consent and flows | plus subprocessor list, regional questions and a re-check of every SDK's disclosures |
| Declarations | for stores in the next release | all target stores | all target stores plus policy text diff |

`SL-PRIVACY` runs at lean and full. Rigor sets depth, never whether a contradiction counts.

## Verdicts

First match wins:

1. **BLOCK**: any open CRITICAL or HIGH finding (`standards/severity.md`: HIGH is fixed before release; accepting one needs the user's written reason), or a gate result of BLOCK.
2. **CONCERNS**: any open MEDIUM finding, or a gate result of CONCERNS.
3. **NOT ASSESSED**: no failures, but the inventory is from static sources only, any decisive question stayed UNKNOWN (audience, markets, sensitive categories), network behavior could not be observed, a declared statement was UNVERIFIABLE, or a draft contains NEEDS INPUT. Name each and what closes it.
4. **CLEAR**: inventory complete with sources, runtime behavior observed, every declaration consistent, drafts complete, no open HIGH or above.

CLEAR means "no engineering contradiction found in what was checked", never "compliant".

## Report

```
Privacy: <app>   Date: <date>   Scope: <full|delta|feature>   Evidence: static + runtime | static only
Data elements: <n> (sensitive <n>, children's <yes|no|unknown>)   Third parties: <n>   Regions: <list|unknown>
Findings: CRITICAL <n>  HIGH <n>  MEDIUM <n>  LOW <n>
Declarations: <store: complete | NEEDS INPUT (n)> ...
Unknown / needs a human: <list>
Decisions for you: <questions> | none
Reminder: drafts only; a person with authority signs off, and this is not legal advice.
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Never state that the app complies with any law, or give legal conclusions; raise questions for a human.
- Never fill a store declaration answer that the inventory cannot support; write NEEDS INPUT.
- Never assume an unknown (audience, region, sensitive data) is benign.
- Never describe a data flow without a source in code, configuration, a vendor document or a capture.
- Never submit forms, change store consoles or edit the live privacy policy; the user does.
- Never put real personal data or secrets in the record or evidence.
- Do not change source to "fix" a finding here; route to `/app-bugfix` or `/app-plan`.
