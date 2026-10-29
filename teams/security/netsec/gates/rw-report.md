# RW-REPORT

**Trigger:** before the assessment is delivered to the operator.

**Owner:** report-writer.

**Inputs:** the draft report (`engagement-report.md`), all findings, the coverage
notes from each practice, `scope.yaml`.

**Checks:**

1. **Every finding is evidenced.** No claim without a command/output, file+lines,
   measurement, or source. No secret values; no WAN IP.
2. **Every MEDIUM+ finding is verified** (`FINDING-VERIFIED` CONFIRMED), or is
   clearly labelled `UNVERIFIED`.
3. **Exposure is scoped.** Each finding names its audience (internet/LAN/local)
   and proved it.
4. **Coverage is honest.** What was not assessed is stated. Nothing is reported as
   clean that was merely unchecked. Tool versions and dates are recorded.
5. **Deduplicated and ranked.** Same root causes merged; ordered by risk to this
   operator; remediation plan present and costed.
6. **Readable at the top.** The executive summary stands alone and the top risks
   are in plain language.

**Verdicts:** `READY`, `CONCERNS`, `NOT ASSESSED`.

- `READY`: deliver it.
- `CONCERNS`: list what must be fixed first (an unevidenced claim, an unverified
  CRITICAL, a missing coverage note). It does not go to the operator until fixed.
- `NOT ASSESSED`: the draft or its inputs could not be read.
