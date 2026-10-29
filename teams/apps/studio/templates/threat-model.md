# Threat Model: [Product name or scope]

<!--
WRITTEN BY: security-lead with security-engineer, privacy-specialist and the platform leads. Skill: /app-threat-model.
LIVES AT: docs/security/threat-model.md (override: paths.threat_model). Audit reports go in docs/security/audits/.
RIGOR: minimal = a half page: assets, entry points and the top 5 threats with a mitigation each; required before any auth, payment, personal data, IPC, update or network feature.
       standard = every section; STRIDE per element of the data-flow diagram; every HIGH threat has a mitigation story; reviewed at the architecture stage and on every change that moves a trust boundary.
       full = standard plus attack-tree or abuse-case detail for the top risks, platform-specific threats per target, verification evidence per mitigation, and a re-review at each release.
GATE: SL-THREAT-MODEL. Keep consistent with the architecture's trust boundaries section.
A threat model is a living map of "what could go wrong, how bad, and what we did". Rate by likelihood and impact with reasons, never by gut-feeling adjectives alone. Severity words: CRITICAL, HIGH, MEDIUM, LOW. No exploit code and no secrets in this file.
-->

**Status:** [Draft | Reviewed | Approved]   **Last reviewed:** [YYYY-MM-DD]   **Architecture version/commit:** [ref]   **Owner:** security-lead

## 1. Scope
<!-- What is modeled (containers, features, versions) and what is not, with the reason. Platforms covered. Assumptions about the environment (OS hardening, user is not an administrator, hosting provider trusted for X). Adversaries considered (curious user, malicious user, remote attacker, malicious local app or extension, compromised dependency, insider, device thief) and ones explicitly out of scope. -->
- **In scope:** [list]   **Out of scope:** [list, with reason]
- **Assumptions:** [list]
- **Adversaries:** [list with capability and motive]

## 2. Data-flow diagram (text)
<!-- Elements: external entities (E), processes (P), data stores (S), data flows (F), and trust boundaries (TB). Number everything so the STRIDE table can cite it. A text or Mermaid diagram is fine. Show every place data crosses a boundary: network, process, privilege, sandbox, device, user-controlled input, third-party code. -->
```
E1 [User] --F1 (UI input)--> P1 [Client app] ==TB1== F2 (HTTPS) ==> P2 [API service] --F3--> S1 [Database]
```
| ID | Element | Type (E / P / S / F) | Description | Data carried |
|---|---|---|---|---|

## 3. Trust boundaries
<!-- Each line where trust changes, who is on each side, and what authenticates and validates at the crossing. -->
| ID | Boundary | Inside / outside | Authentication | Validation at crossing |
|---|---|---|---|---|

## 4. Assets
<!-- What an attacker would want or what we must protect: credentials and tokens, personal data, user content, money, signing keys, update channel, availability, reputation, integrity of stored data. Classification and where each lives. -->
| ID | Asset | Where it lives | Classification | Why it matters |
|---|---|---|---|---|

## 5. Threats by STRIDE
<!-- For every element in section 2 consider each category that applies: Spoofing (identity), Tampering (data or code), Repudiation (no audit trail), Information disclosure, Denial of service, Elevation of privilege. Processes get all six; data stores mainly T, R, I, D; data flows T, I, D; external entities S, R. Write specific, realistic threats ("a malicious local app writes to the unsecured IPC pipe and triggers delete"), not generic ones. Likelihood and impact each Low / Medium / High with a reason; severity combines them. Add platform-specific threats for each target (web: XSS, CSRF, clickjacking, CSP, supply chain; desktop: DLL or binary planting, unquoted paths, insecure update channel, local IPC, protocol handlers, elevated helpers; mobile: exported components, deep links, insecure storage, screenshot leakage, intent redirection, backups; backend: injection, broken access control, SSRF, mass assignment, secrets in logs; CLI: argument and environment injection, unsafe temp files). -->
| ID | Element | STRIDE | Threat | Likelihood | Impact | Severity | Mitigation ID |
|---|---|---|---|---|---|---|---|
| T-001 | P1 | S | [specific threat] | [M: reason] | [H: reason] | HIGH | M-001 |

## 6. Mitigations
<!-- Per threat: prevent, detect, respond, or accept. Prefer removing the risk (not collecting the data, not exposing the port) over adding a control. Name the control concretely (where in the architecture, which mechanism), the owner, the story that implements it, and how it will be verified (test, scan, review). A mitigation without a verification is a hope. -->
| ID | Addresses | Control | Type (prevent / detect / respond / accept) | Story | Verification | Status |
|---|---|---|---|---|---|---|
| M-001 | T-001 | | | | | Planned |

## 7. Residual risk
<!-- What remains after mitigation, per threat that is not fully closed, with a plain statement of the risk, who accepts it (the user decides acceptance of HIGH and CRITICAL), and when it is revisited. Accepted risk is recorded, not forgotten. -->
| Threat | Residual risk | Accepted by | Date | Revisit when |
|---|---|---|---|---|

## 8. Stories raised
<!-- Mitigations that need work become stories (planning/epics/...). Link them and give priority P0 to P3. CRITICAL and HIGH threats without a story or an acceptance are open gate findings. -->
| Story | Mitigation | Priority | Status |
|---|---|---|---|

## 9. Review triggers
<!-- This model is re-opened when: a trust boundary moves, a new data type, integration, permission, auth method or update path is added, a new platform is targeted, a dependency with network or native access is added, or a security incident occurs. -->

## Change log
| Date | Change | Reviewer |
|---|---|---|
