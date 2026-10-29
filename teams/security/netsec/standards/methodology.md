# Methodology

The firm works a repeatable method so an overnight run is thorough, evidenced, and
safe, not a pile of tool output. It is informed by NIST SP 800-115 (technical
assessment), the PTES phases, the OWASP testing guides, and the MITRE ATT&CK
tactics as a coverage map. Scale the depth to the engagement's rigor and the
target's value; the questions stay the same.

## The phases

1. **Authorize and scope.** Confirm `scope.yaml` exists and is authorized. Resolve
   targets. Set the intensity ceiling. Nothing active runs before this. (Gate:
   `ED-SCOPE`.)
2. **Reconnaissance and discovery.** Build the real picture of each in-scope
   asset: public DNS and records, what resolves where, certificates, exposed vs
   internal, open ports and their services and versions, the reverse-proxy and
   tunnel map, the attack surface as it actually is (not as the config implies).
3. **Enumeration and mapping.** For each service, enumerate what it exposes:
   endpoints, methods, parameters, auth surfaces, admin panels, shares, APIs,
   management interfaces. Map trust boundaries (internet to edge, edge to LAN,
   VLAN to VLAN, host to container, user to admin).
4. **Analysis and testing.** Work each boundary and service with the specialty
   method: trace untrusted input to its effect, check the control and not just
   the bug, compare the running version to known CVEs, review the config against
   the benchmark. Keep it non-destructive; prove, do not break.
5. **Verification.** Before anything is called a finding, confirm it is real and
   reachable, and scope it to the right audience (internet, LAN, local). Over-rated
   or unverified items go back, not forward.
6. **Reporting and remediation.** Consolidate into one assessment: executive
   summary, ranked technical findings with evidence, and a remediation plan with
   the shortest path to the biggest risk reduction. (Gates: `RW-REPORT`.)
7. **Detection check (purple).** For the attacks that mattered, ask the defensive
   side whether they were logged and whether they would have alerted. A finding
   that no one would have seen is itself a finding.
8. **Re-test.** After a fix, retry the original and two variants. A fix that blocks
   only the exact probe is not a fix.

## Coverage map

Use MITRE ATT&CK tactics as a checklist of what an assessment should at least
consider for this environment: reconnaissance, initial access, execution,
persistence, privilege escalation, defense evasion, credential access, discovery,
lateral movement, collection, exfiltration, impact. Not every tactic applies to
every target; name the ones you assessed and the ones you did not.

## Depth by intensity

- **passive**: records, configs, public DNS, certificates, version banners, the
  infra repo. No probing that touches the target beyond a normal client request.
- **active-nondestructive**: port and service scanning, safe probes and version
  checks, auth-surface mapping, header and TLS testing, config review against
  benchmarks. Changes no state. The default.
- **exploit-opt-in**: proof-of-concept only against `exploit_safe` targets, only
  far enough to confirm the weakness, never to disrupt or to pull real data.

Denial-of-service, stress, flood, and resource-exhaustion testing is forbidden at
every intensity.
