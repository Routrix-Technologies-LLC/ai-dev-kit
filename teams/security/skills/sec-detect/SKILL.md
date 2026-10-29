---
name: sec-detect
description: "Defensive / SOC review and the purple loop: would an attack be seen, logged, and acted on? Reviews telemetry and alert coverage mapped to ATT&CK, hunts for existing compromise, and checks incident and recovery readiness. Use for 'would I detect an attack', 'check my logging', 'threat hunt', 'am I already breached', 'incident readiness'."
argument-hint: "[scope] [--from-pentest]"
user-invocable: true
---

# Detection and response review

Driven by `defensive-lead`. Read-only and evidence-preserving on all logs and
hosts.

## Steps

1. `ED-SCOPE` CLEAR. Gather the exercised-technique log from any recent
   `/sec-pentest` (or exercise a safe subset to test detection).
2. Run the specialists:
   - `soc-analyst`: log coverage, alert quality, triageability; fill the
     attack-to-detection map (`detection-review.md`).
   - `detection-engineer`: telemetry pipeline and ATT&CK rule coverage; propose
     rules for the gaps (deployment is the operator's call via
     `hardening-engineer`).
   - `threat-hunter`: hunt the operator's own logs and hosts for signs of existing
     compromise. A confirmed sign is an immediate escalation.
   - `incident-response-analyst`: runbooks, log retention and integrity, backup
     and tested-restore readiness.
3. File each detection gap and readiness gap as a finding.

## Output

`detection-review.md`: telemetry inventory, attack-to-detection map, detection and
response gaps as findings, and proposed rules for the operator to approve.
