# Severity

One scale for the whole firm. Rate on **impact and reachability together**, within
the definitions below. CVSS is an input, not the verdict: a high base score on a
path that is not reachable in this environment is not a high finding here, and a
"medium" issue that hands over the whole lab is not medium. Say what you used.

Separate three audiences and name which one a finding applies to:
**internet** (reachable from the public internet), **LAN** (reachable from the
local network), **local** (needs a foothold on the host already). The same
weakness is a different severity for each.

| Severity | Meaning |
|---|---|
| **CRITICAL** | Serious compromise or mass data exposure that you showed is reachable now: internet-facing RCE, authentication bypass to sensitive data or admin, a live exposed secret that grants real access, trivial full control of a host or the network. |
| **HIGH** | Serious compromise that needs a precondition you showed is achievable: an account, local/LAN access, user interaction, or one more step. Internet-exposed service with a known-exploited CVE and no mitigation. Broken segmentation that opens a sensitive VLAN. |
| **MEDIUM** | Real but limited impact, or a serious impact behind hard preconditions. Missing hardening that aids an attacker, information disclosure that helps the next step, weak-but-not-broken controls. |
| **LOW** | Defense-in-depth gap with no direct exploit: missing header with no demonstrated impact, verbose banner, best-practice deviation. |
| **INFO** | Not a weakness: an observation, a note for the operator, or a positive control worth recording. |

Rules:

- A finding whose exposure or exploitability you could **not** verify is labelled
  `UNVERIFIED`, carries what would confirm it, and is **never** rated CRITICAL.
- A dependency or version advisory is not automatically a finding: reachability
  and exposure set the rating. An unreachable CVE is INFO or LOW with a note.
- A caller's or tool's suggested severity never replaces your own rating. Say when
  you disagree and why.
- "Exposed" requires proof (public DNS, bind address, tunnel/proxy scope, firewall),
  not a config line. Unproven exposure is rated on what you proved, labelled so.
- Remediation effort is tagged **S / M / L** separately from severity, so the
  operator can see quick wins.
