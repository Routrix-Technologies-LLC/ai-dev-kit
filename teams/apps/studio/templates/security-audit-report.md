<!--
Template: security-audit-report. Written by: security-engineer with security-lead, identity-specialist (auth) and privacy-specialist (data). Skill: /app-security-audit.
Lives at: docs/security/audits/<date>.md.
Rigor: minimal = scope, verdict, findings, not-assessed list. standard = adds method, category table, exposure verification evidence. full = adds threat-model cross-reference, dependency and supply-chain results, retest section.
Delete this comment when the report is created.
-->

# Security audit: [scope]

> **Date**: [YYYY-MM-DD]   **Auditor(s)**: [agents]
> **App version / commit**: [...]   **Platforms**: [web, backend, windows, macos, linux, ios, android, cli, extension, library]
> **Verdict**: [CLEAR | CONCERNS | BLOCK | NOT ASSESSED]

Verdict rules, first match wins: BLOCK if any CRITICAL or HIGH finding is open (an UNVERIFIED one on an exposed surface counts); CONCERNS if any MEDIUM finding is open; NOT ASSESSED if no failure applies but any in-scope category could not be checked (zero findings from zero files examined is NOT ASSESSED); otherwise CLEAR (LOW findings and accepted risks may remain, listed).

## Scope

- In scope: [components, repos, endpoints, builds, trust boundaries]
- Out of scope: [and why]
- Threat model used: `docs/security/threat-model.md` [version/date, or "none exists"]

## Method

[What was done: code reading (files examined, n of n), dependency and secret scanning (tools and versions), configuration review, dynamic testing against which environment, platform-specific inspection (entitlements, manifest, permissions, installer, update channel). State what was run versus read only.]

## Categories checked

Reference: OWASP Top 10, OWASP ASVS, OWASP MASVS for mobile, and platform hardening guides.

| Category | Checked | Result | Notes |
|---|---|---|---|
| Authentication and session management | [Yes / NOT ASSESSED] | [pass / findings: SEC-NNN] | |
| Authorization and access control | | | |
| Input validation and injection | | | |
| Output encoding and XSS or content injection | | | |
| Cryptography and key management | | | |
| Secrets in code, config, logs and build artifacts | | | |
| Data storage and transport | | | |
| API and IPC surface | | | |
| Dependencies and supply chain | | | |
| Update, install and signing | | | |
| Platform hardening (sandbox, permissions, entitlements, CSP, headers) | | | |
| Error handling and logging (no sensitive data) | | | |
| Privacy-relevant data flows | | | |
| Denial of service and resource limits | | | |

## Findings

### SEC-[NNN]: [title]

<!-- SEC-NNN IDs are stable within the report and never reused. -->

| Field | Value |
|---|---|
| Severity | [CRITICAL / HIGH / MEDIUM / LOW] |
| Category | [from the table] |
| Location | `[path:line]` or [endpoint / component] |
| Status | [Open / Fixed / Accepted by security-lead] |
| Effort to fix | [S / M / L] |

**Attack scenario**: [Who the attacker is, what access they start with, the steps, and what they gain. Concrete enough to reproduce.]

**Remediation**: [Specific change, plus a regression test or control to add.]

## Exposure verification evidence

Before calling anything exposed, verify it. For each exposure claim:

| Claim | Check performed | Result | Evidence |
|---|---|---|---|
| [for example: admin endpoint reachable from the internet] | [public DNS lookup, port scan scope, reverse proxy rules, firewall scope, auth requirement, actual request] | [confirmed / not reachable / internal only] | [command output or log path] |

## Not assessed

[Every category or area not checked, with the reason and who could check it.]

## Retest

| Finding | Retest date | Result |
|---|---|---|
