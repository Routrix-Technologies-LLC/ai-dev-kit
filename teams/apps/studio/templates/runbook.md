<!--
Template: runbook. Written by: site-reliability-engineer with escalation-engineer and the owning lead. Skill: /app-observability (writes runbooks), /app-incident updates them.
Lives at: docs/ops/runbooks/<topic>.md (override: paths.runbooks).
Rigor: minimal = symptoms, mitigation, rollback. standard = adds impact, diagnosis steps, escalation, verification, re-run safety notes. full = adds dashboards and alert links, rehearsal log, and owner review dates.
Write for someone arriving mid-incident, stressed and searching. Put the answer first, commands copyable, no credentials (name where they live instead). Delete this comment when the runbook is created.
-->

# Runbook: [topic, phrased as the problem, for example "Sync is failing for all users"]

> **Owner**: [role]   **Last verified**: [YYYY-MM-DD, by running the steps]
> **Applies to**: [service, platform, versions]
> **Severity if true**: [S1 | S2 | S3 | S4]
> **Alert / dashboard**: [names or links]

## In one minute

[The fastest safe action, and what to check first. If you only read this section, you should still stop the bleeding.]

## Symptoms

How you know this is the problem:
- [User-visible sign, exact error text or code]
- [Metric or log signature, with query]
- Not this runbook if: [look-alike condition and where to go instead]

## Impact

[Who is affected (all users, one platform, one region, one plan), what they cannot do, whether data is at risk, and how fast it gets worse.]

## Diagnosis

Run in order. Each step says what you should see and what it means.

1. [Check X: `command`] Expect: [output]. If different: [go to step n / escalate].
2. [Check Y: `command`] Expect: [...].
3. [Decide: cause A (symptom), cause B (symptom), unknown (escalate)]

Read-only steps are marked READ-ONLY. Safe to re-run: [yes for all diagnosis steps / except step n].

## Mitigation

Pick the cause from Diagnosis.

**Cause A**
1. [Action with exact command.]
2. [Action.]
- Safe to re-run: [yes / no, and what happens on a second run]
- Expected time: [n minutes]

> WARNING (destructive): [step that deletes, overwrites, restarts or cannot be undone]. Before it: [take a backup/snapshot, confirm target environment, confirm with owner]. Undo: [how, or "cannot be undone"].

## Rollback

[How to return to the last known good state: redeploy previous build, flip the flag, restore backup, halt rollout, revert the update feed. Include the verification that rollback worked and what rollback does not undo.]

## Escalation

| When | Who | How | What to bring |
|---|---|---|---|
| [Not fixed in n minutes / data at risk / security suspected] | [role: escalation-engineer, security-lead, release-manager, the user] | [channel] | [timeline, steps tried, outputs] |

Security suspected: stop, preserve logs, do not clean up, escalate to security-lead and the user.

## Verification

You are done when all are true:
- [ ] [Metric back within normal range for n minutes]
- [ ] [A real user path works end to end: describe]
- [ ] [No error signature in logs for n minutes]
- [ ] [Alert cleared on its own]

## After

- Record what happened (`/app-incident` for S1 or S2).
- Update this runbook with anything that was wrong or missing.
- Add monitoring or a test so it is caught earlier next time.

## Rehearsal log

| Date | By | Outcome | Fixes made to this doc |
|---|---|---|---|
