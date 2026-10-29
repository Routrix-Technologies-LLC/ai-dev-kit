---
name: sec-assess
description: "Run a full purple-team assessment of in-scope infrastructure with the whole Security Firm: recon, offensive, infrastructure, defensive/SOC, and GRC practices in parallel, verified findings, the purple detection loop, and one consolidated report. Use for a thorough or overnight assessment, 'full security assessment', 'test everything', 'firm-style discovery', or 'assess my homelab'."
argument-hint: "[scope or asset set] [--intensity passive|active|exploit]"
user-invocable: true
---

# Full security assessment

The whole firm, end to end, driven by `engagement-director` per
`netsec/orchestration.md`. Built to run broad and unattended without destabilizing
the operator's systems.

## Steps

1. **Scope and plan.** Run `/sec-engage` first (ED-SCOPE must be CLEAR). Decide the
   roster and sequence; respect `scope.yaml` quiet hours and the intensity ceiling.
2. **Recon (parallel).** `attack-surface-analyst`, `osint-analyst`,
   `dns-email-security-analyst`, `tls-crypto-analyst` build one shared map. Every
   later agent reads it instead of re-scanning.
3. **Practice fan-out (parallel across practices, serial within a host):**
   - Offensive: web, api, reverse-proxy, network, auth, vuln, secrets.
   - Infrastructure: firewall/segmentation, container/host, cloud, endpoint.
   - GRC: NIST CSF scorecard and CIS controls/benchmarks.
   Run heavy scans one at a time, one per host. Stop heavy work when the
   operator needs the machine back.
4. **Verify.** Each lead runs `FINDING-VERIFIED` on MEDIUM+ findings; unverified
   items are labelled, not dropped.
5. **Purple loop.** The defensive practice (`soc-analyst`, `detection-engineer`,
   `threat-hunter`, `incident-response-analyst`) checks whether the exercised
   techniques were logged and would alert, and whether the operator could respond.
6. **Consolidate.** The director dedupes and ranks; `report-writer` builds the
   assessment and runs `RW-REPORT`.
7. **Deliver.** One report: executive summary, ranked findings, NIST CSF posture,
   costed remediation plan, honest coverage. Remediation is proposed, not applied,
   unless the user says go (then `hardening-engineer`, one confirmed change at a
   time).

## Running unattended

Write progress and scan artifacts to `~/AgentScratch/<engagement>/`. Keep
everything non-destructive and within the intensity ceiling. If a stop condition
hits (real compromise, instability, the operator needs the machine), stop that thread, preserve state, and
record it for the morning.

## Output

`engagement-report.md`, `remediation-plan.md`, and `compliance-assessment.md` in
the engagement's docs folder, plus a short spoken summary of the top risks.
