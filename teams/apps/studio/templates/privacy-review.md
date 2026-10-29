# Privacy Review: [Product name]

<!--
WRITTEN BY: privacy-specialist with security-lead and app-store-specialist; analytics-specialist consulted on telemetry. Skill: /app-privacy-review.
LIVES AT: docs/security/privacy.md (override: paths.privacy). It is the app's privacy record: update it whenever data handling changes.
RIGOR: minimal = a short inventory (what personal data, where it is stored, whether it leaves the device, how to delete it) and a statement of "no telemetry" or what telemetry exists.
       standard = every section; inventory reconciled against the code and SDK list; store declarations drafted; consent and deletion paths verified.
       full = standard plus data protection impact assessment style analysis for sensitive data, processor/vendor register with agreements, regional law mapping, and a re-review at each release that changes data.
GATE: SL-PRIVACY. Declarations are DRAFTS: the user submits them. This document is engineering and product analysis, not legal advice; mark where counsel is needed.
Reconcile what the code actually collects (grep the code, SDKs, network calls, manifests, permissions) with what is declared. Where they differ, the finding is the gap. Personal data means anything that relates to an identifiable person, including device and advertising identifiers, IP addresses, precise location, contacts, content, and inferences.
-->

**Status:** [Draft | Reviewed | Approved]   **Last reviewed:** [YYYY-MM-DD]   **App version reviewed:** [version/commit]   **Owner:** privacy-specialist

## 1. Summary
<!-- Three to five lines in plain words: what personal data the app handles, whether anything leaves the device, who receives it, whether there are accounts, analytics or ads, and the headline findings. "Collects no personal data and sends nothing off-device" is a valid and verifiable summary; verify it. -->

## 2. Data inventory
<!-- One row per data element or category, found by reading the code, schemas, SDK manifests, network traces and permission lists. Include data created by the user, data observed from the device, data received from third parties, and data inferred. Sensitive categories (health, financial, children's data, precise location, biometrics, contacts, communications content, credentials, government IDs, data revealing protected characteristics) are flagged because they raise obligations. -->
| ID | Data element | Source (user / device / third party / inferred) | Sensitive? | Where collected in the app | Stored where | Evidence (code path, SDK) |
|---|---|---|---|---|---|---|

## 3. Data flows
<!-- Where each element goes: processes, stores, networks, third parties, regions. Name every recipient, including crash reporters, analytics, push services, email, payment, auth providers, CDNs and cloud hosts. Cross-border transfers noted. Link the architecture's trust boundaries and the threat model's data-flow diagram. -->
| Data ID | From | To (system or third party) | Transport and protection | Region | Purpose ref |
|---|---|---|---|---|---|

## 4. Purpose and minimization
<!-- For each element: the specific purpose, the lawful basis or permission where a law requires one (consent, contract, legitimate interest; mark "to confirm with counsel" if unsure), and whether it is truly needed. Ask of each: could we skip it, coarsen it (region not coordinates), process it on the device, or discard it sooner? Secondary uses (for example analytics from support data) need their own purpose. -->
| Data ID | Purpose | Basis / permission | Necessary? | Minimization option considered |
|---|---|---|---|---|

## 5. Retention and deletion
<!-- How long each element is kept, why, how it is deleted (including backups, logs, caches, analytics, third-party copies), and what triggers deletion (user request, account closure, expiry). A stated retention that no code enforces is a finding. -->
| Data ID | Retention | Enforced by | Deletion path | Third-party copies |
|---|---|---|---|---|

## 6. Sharing and processors
<!-- Every third party that receives personal data: its role (processor or independent controller), what it gets, contract or terms in place, its own retention, whether data is used for its purposes (advertising, model training), and whether it appears in store declarations. Include SDKs that collect on their own. -->
| Vendor / SDK | Role | Data received | Agreement / terms | Their retention and use | Declared in stores? |
|---|---|---|---|---|---|

## 7. Consent and transparency
<!-- Where and how the user is informed and asked: first-run notices, permission prompts (with the moment and wording), analytics opt-in or opt-out, marketing consent, consent for children where applicable, the privacy policy link and its accuracy, and how consent is withdrawn and honored. Default is off for optional collection. No dark patterns: refuse is as easy as accept. Consent records, if kept. -->
| Data / feature | Consent mechanism | Default | Withdrawal path | Verified in build? |
|---|---|---|---|---|

## 8. User rights
<!-- Access, export, correction, deletion, objection and restriction where the app's audience or law requires them: how a user exercises each in the app or by contact, the response time, identity checks, and whether the process actually exists and has been tested end to end. Local-only apps: where the data is and how the user removes it. -->
| Right | How exercised | Implemented? | Tested (date) |
|---|---|---|---|

## 9. Security of the data
<!-- Short cross-reference, not a repeat: encryption in transit and at rest, access control, key handling, logging hygiene (no personal data or secrets in logs or crash reports), backups. Link the threat model mitigations. -->

## 10. Store declarations (DRAFT, the user submits)
<!-- Draft answers per store from the inventory in sections 2 to 6. Use each store's current terminology and forms; read the store's current documentation and record the date you checked, because the forms change. Mark any answer you could not derive as UNKNOWN. -->
| Store / form | Question or category | Draft answer | Derived from (data IDs) | Docs checked on |
|---|---|---|---|---|
| Apple App Privacy details and privacy manifest | | | | |
| Google Play Data safety | | | | |
| Microsoft Store privacy policy and capability declarations | | | | |
| Web, extension store or other | | | | |

## 11. Findings and open issues
<!-- Severity words CRITICAL, HIGH, MEDIUM, LOW. Each finding: what, evidence, why it matters, fix, owner. Include declared-versus-actual mismatches, missing deletion paths, consent gaps and undeclared SDK collection. Items needing counsel are marked LEGAL REVIEW. -->
| ID | Severity | Finding | Evidence | Recommended fix | Owner | Status |
|---|---|---|---|---|---|---|

## Change log
| Date | Change in data handling | Sections updated |
|---|---|---|
