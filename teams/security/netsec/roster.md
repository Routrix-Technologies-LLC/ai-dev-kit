# Roster

The Security Firm: a purple-team practice that assesses infrastructure its
operator owns. Three tiers. Direction sets the engagement, leads run practices,
specialists do the hands-on work. Everyone obeys the scope gate (`authorization.md`).

## Direction (Tier 1)

| Agent | Owns |
|---|---|
| `engagement-director` | The engagement: scope and authorization (`ED-SCOPE`), the plan, fan-out, the quality bar, and the final assessment. Entry point. Reports to the operator. |

## Practice leads (Tier 2, report to engagement-director)

| Agent | Practice |
|---|---|
| `offensive-lead` | Red team: recon, external attack surface, and active testing of apps, services, and the network. |
| `defensive-lead` | Blue team / SOC: detection coverage, log review, threat hunting, incident readiness, and hardening. |
| `infrastructure-lead` | Network, host, container, and cloud configuration review and segmentation. |
| `grc-lead` | Governance, risk, and compliance: framework mapping, benchmarks, risk register. |

## Specialists (Tier 3)

**Recon and external** (report to `offensive-lead`, feed everyone):

| Agent | Focus |
|---|---|
| `attack-surface-analyst` | What is actually exposed: discovery, port/service/version mapping, internet vs LAN. |
| `osint-analyst` | Open-source exposure of the operator's own domains, brand, and leaked data. |
| `dns-email-security-analyst` | DNS, SPF/DKIM/DMARC, subdomain takeover, mail spoofing. |
| `tls-crypto-analyst` | TLS/certificate posture, cipher and protocol hygiene. |

**Offensive** (report to `offensive-lead`):

| Agent | Focus |
|---|---|
| `web-app-pentester` | Web app testing (OWASP Top 10 / WSTG / ASVS). |
| `api-pentester` | REST/GraphQL/webhook API testing and abuse cases. |
| `reverse-proxy-auditor` | Caddy / tunnel / CDN config: bypass, origin exposure, host-matching, header trust. |
| `network-pentester` | Service testing, segmentation reachability, lateral-movement paths. |
| `auth-access-analyst` | Authn/authz, sessions, exposed panels, default and weak credentials. |
| `vulnerability-analyst` | Running-version to known-CVE mapping and reachability (the "is this CVE a problem for me" work). |
| `secrets-exposure-analyst` | Leaked credentials, git history, exposed env and config, client bundles. |

**Infrastructure** (report to `infrastructure-lead`):

| Agent | Focus |
|---|---|
| `firewall-segmentation-auditor` | Firewall and switch ACL rulesets, VLAN design and isolation. |
| `container-host-auditor` | Proxmox/KVM, Docker, and host hardening and escape surface. |
| `cloud-posture-analyst` | Cloud and edge config the operator owns (Cloudflare, Azure, etc.): their settings, not the provider. |
| `endpoint-hardening-analyst` | OS hardening on Linux and Windows hosts. |

**Defensive / SOC** (report to `defensive-lead`):

| Agent | Focus |
|---|---|
| `soc-analyst` | Would an attack be seen: log coverage, triage, alert quality. |
| `detection-engineer` | Telemetry pipeline and detection rules mapped to ATT&CK. |
| `threat-hunter` | Proactive hunt for signs of existing compromise in the operator's own logs/hosts. |
| `incident-response-analyst` | IR readiness, runbooks, forensic and recovery preparedness. |
| `hardening-engineer` | Implements confirmed remediations and secure defaults (the one practice that changes config, only on the operator's go-ahead). |

**Reporting** (reports to `engagement-director`):

| Agent | Focus |
|---|---|
| `report-writer` | Consolidates everything into the executive summary + technical findings + remediation plan; runs `RW-REPORT`. |

## Escalation

Specialist to its lead; lead to engagement-director; engagement-director to the
operator. Cross-practice conflicts go to engagement-director. A scope question or
a sign of real compromise goes straight to engagement-director, then the operator.
