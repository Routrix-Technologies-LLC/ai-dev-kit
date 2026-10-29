# Posture assessment: <engagement name>

A framework-mapped read of the environment. For a home or small environment this
is a tracking and prioritization tool, not an enterprise pass/fail audit. Rate by
real risk to this operator; map to the framework so it is trackable over time.

## Framework and profile

- Framework: NIST CSF 2.0 (default) | CIS Controls v8 | other.
- Why this one, and what "good" looks like for an environment this size.

## NIST CSF 2.0 scorecard

| Function | State | Notes | Linked findings |
|---|---|---|---|
| Govern (GV) | | ownership, policy, risk appetite | |
| Identify (ID) | | asset inventory, data, risk | |
| Protect (PR) | | access control, hardening, segmentation | |
| Detect (DE) | | logging, monitoring, alerting | |
| Respond (RS) | | IR plan, comms | |
| Recover (RC) | | backups, restore testing | |

State is one of: solid / partial / thin / absent / not assessed.

## CIS Controls v8 (if used)

| Control | IG1 target | State | Linked findings |
|---|---|---|---|
| 1 Inventory of enterprise assets | | | |
| 3 Data protection | | | |
| 4 Secure configuration | | | |
| 6 Access control management | | | |
| 8 Audit log management | | | |
| 12 Network infrastructure management | | | |
| 13 Network monitoring and defense | | | |

## Benchmark results

Pointer to per-platform CIS Benchmark scoring (Linux, Docker, Proxmox, network
devices) produced by the benchmark specialist, with the top deviations as findings.

## Priorities

The three to five posture gaps that would most reduce risk, cross-referenced to
the remediation plan.
