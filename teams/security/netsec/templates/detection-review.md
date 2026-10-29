# Detection and response review: <engagement name>

Purple-team view: for the attacks that mattered, would anyone have seen them?

## Telemetry inventory

What is actually collected, and where it lands.

| Source | What it logs | Ships to | Retention | Gaps |
|---|---|---|---|---|
| | | | | |

## Attack-to-detection map

For each notable technique the offensive side exercised (by ATT&CK ID), whether it
left a trace and whether that trace would alert.

| Technique (ATT&CK) | Where it would show | Logged? | Alerts? | Finding |
|---|---|---|---|---|
| T1190 Exploit public-facing app | reverse-proxy / app logs | | | |
| T1046 Network service scanning | firewall / IDS | | | |
| T1110 Brute force | auth logs | | | |
| T1021 Lateral movement | inter-VLAN / host logs | | | |

## Detection gaps

Each gap as a finding (`finding.md`): the technique with no coverage, why it
matters here, and the smallest telemetry or rule that would close it.

## Response readiness

- Is there a way to notice, triage, and act? Who/what gets paged?
- Are logs tamper-evident and retained long enough to investigate?
- Is there a runbook for the likely incidents? Backups tested for recovery?
