# Orchestration

How a full engagement runs end to end. The engagement-director drives this; the
`/sec-*` skills are the entry points.

## A full engagement (overnight baseline)

1. **Scope.** `ED-SCOPE`. Confirm `scope.yaml`, resolve targets, set intensity.
   BLOCK stops everything until the operator fixes scope.
2. **Recon.** Spawn the recon specialists in parallel against in-scope assets.
   Produce one shared map: what resolves where, internet vs LAN, open services and
   versions, the proxy/tunnel picture. Everything downstream reads this.
3. **Practice fan-out (parallel across practices, serial within a host):**
   - Offensive: web, api, reverse-proxy, network, auth, vuln, secrets, against the
     assets recon surfaced, at the intensity ceiling.
   - Infrastructure: firewall/segmentation, container/host, cloud, endpoint config
     review against benchmarks.
   - GRC: map the environment to NIST CSF and score CIS controls/benchmarks.
4. **Verification.** Each lead runs `FINDING-VERIFIED` on its MEDIUM+ findings.
5. **Purple loop.** Defensive side checks detection coverage for the techniques
   exercised; files gaps.
6. **Consolidate.** Director dedupes and ranks; `report-writer` builds the report
   and runs `RW-REPORT`.
7. **Deliver.** One assessment to the operator: exec summary, ranked findings,
   remediation plan, honest coverage. Remediation is proposed, not applied, unless
   the operator says go.

## Pointed engagements

The operator can aim the firm at one thing without a full run:

- "Poke at `<asset>`" -> scope-check it, recon it, run the relevant specialists.
- "Is this clean / listening on what it should?" -> attack-surface + firewall/
  segmentation + endpoint-hardening on that host.
- "Am I exposed to `<CVE>`?" -> vulnerability-analyst + the owning specialist.
- "Would I see an attack?" -> the defensive practice and the purple loop.
- "Score me against NIST/CIS" -> the GRC practice.

## Depth control

Scale fan-out to the engagement: a quick pointed check is a handful of agents; the
overnight baseline is the whole firm. The director decides the roster per run and
says so in the plan, so the operator can see what will and will not be covered.
