# Data Migration Plan: MIG-[NNNN] [short title]

<!--
WRITTEN BY: database-engineer with backend-lead (or the platform lead for on-device stores), reviewed by qa-lead. Skill: /app-data-migration.
LIVES AT: planning/migrations/MIG-NNNN-<slug>.md (override: paths.migrations). MIG-NNNN is never reused or renumbered.
RIGOR: minimal = sections 1, 3, 5, 6 and 8 as a short checklist: what changes, the steps, a backup/copy rehearsal, rollback, and the record of the real run.
       standard = every section; a dry run on a COPY with row counts before and after; rollback tested on the copy; proof that old data still loads.
       full = standard plus timing and lock/size measurements on production-scale data, a staged rollout, monitoring thresholds, and a second reviewer sign-off.
Covers any persistent format: server database schema, on-device database, file or save format, settings and config format, search index, cache layout.
HARD RULE: an agent rehearses on a copy and never runs this plan against real data. The real-data run happens only by the user's own action, after the user's explicit yes. Step 8 is written for the user to run or to authorize, never for an agent to run on its own.
-->

**Status:** [Draft | Rehearsed | Approved by the user | Run | Verified | Closed]   **Owner:** [role]   **Date:** [YYYY-MM-DD]
**Related:** [feature spec, ADR, architecture section]   **Affects:** [stores, files, versions of the app]

## 1. Change and reason
<!-- What changes in the data model or format and why. Before and after shapes, side by side. Which app versions read and write which shape. -->
| Item | Before | After |
|---|---|---|

**Data in scope:** [tables, collections, files; approximate size and row counts; who owns them]
**Data out of scope:** [what is untouched]

## 2. Compatibility strategy: expand and contract
<!-- Never change in place in one step. Phases, each independently shippable and reversible until the last:
 1 EXPAND: add the new structure alongside the old (new columns nullable or defaulted, new tables, new file fields that old readers ignore). No reader or writer breaks.
 2 DUAL-WRITE: new code writes both old and new shapes (or new code reads the new shape and falls back to old).
 3 BACKFILL: populate the new structure from the old for existing data (section 4).
 4 SWITCH READS: readers use the new structure; verify parity.
 5 CONTRACT: stop writing the old shape; later, remove it in a separate release after the rollback window.
State which release contains each phase and the minimum gap between them. For on-device data that users upgrade at different times, the app must read the old shape forever or until a documented floor version. -->
| Phase | Release or deploy | Change | Reversible until |
|---|---|---|---|
| Expand | | | |
| Dual-write | | | |
| Backfill | | | |
| Switch reads | | | |
| Contract | | | |

## 3. Preconditions and risks
<!-- Backups verified restorable; free space; locks and downtime or none; version prerequisites; owners available; maintenance window; what can go wrong (data volume, nulls and legacy oddities, encoding, duplicates, referential breaks, long locks, interrupted run, clock skew, two writers). Each risk with mitigation. -->
| Risk | Mitigation | Check |
|---|---|---|

## 4. Backfill design
<!-- How existing data is converted: idempotent (safe to re-run), resumable (progress marker), batched (size, pause, back-pressure), ordered, observable (progress and error counts), and non-destructive (the old data is kept until contract). Rules for invalid or odd source rows: quarantine into a named place with a count, never silently drop or guess. Expected duration at production scale. -->
- **Batch size and pacing:** [text]
- **Idempotency and resume mechanism:** [text]
- **Handling of invalid rows:** [text]

## 5. Dry run on a copy (required before any real run)
<!-- Use a copy or restored backup of real-shaped data, or a faithful synthetic set when real data is not available to agents; say which. Record before and after row counts per table or record counts per file, checksums of unchanged data, the number of quarantined rows, duration, and peak resource use. The counts must reconcile: after = before minus intentional removals plus intentional additions, each explained. -->
| Table or file | Rows before | Rows after | Expected difference | Reconciles |
|---|---|---|---|---|

- **Copy source and date:** [text]   **Run command(s):** [text]   **Duration:** [time]
- **Spot-check queries and results:** [text]
- **Application tests run against the migrated copy:** [command, result]

## 6. Rollback (tested)
<!-- The exact steps to return to the previous state at each phase, and how long it takes. Rollback is tested on the copy: migrate, roll back, compare to the original with counts and checksums. State the point of no return (usually the contract phase, or any step that discards old data) and what protects it (verified backup, retention window). Code rollback and data rollback are separate lines. -->
| Phase | Rollback steps | Tested on the copy (date, result) | Time to roll back |
|---|---|---|---|

- **Point of no return:** [step and protection]

## 7. Old data still loads
<!-- Prove it both ways: (a) the NEW code opens data written in the OLD shape (fixtures from every supported prior version, including the oldest) and (b) during rollout the OLD code still tolerates data written by the new code, until contract. Name the fixtures, the tests that load them, and the result. -->
| Data version or app version | Fixture | Test | Result |
|---|---|---|---|

## 8. Real-data run (user's action only)
<!-- Written as a runbook for the user. An agent never executes this section. Include: the pre-run backup command and verification, the exact run command, the expected output and counts from the dry run, the go/no-go checks, monitoring while it runs, the stop procedure, and the post-run verification queries. Record who ran it and when. -->
1. **Backup and verify restore:** [steps]
2. **Run:** [command]
3. **Expected result:** [counts]
4. **Stop or abort if:** [conditions]
5. **Verify after:** [queries and app checks]

| Run | Date | Run by | Environment | Result vs expected | Notes |
|---|---|---|---|---|---|

## 9. Monitoring and sign-off
<!-- What is watched after each phase (errors, latency, row-count drift, support signals) and for how long before the next phase starts. Who signs off each phase. -->

## 10. Cleanup
<!-- The contract step: when the old structure is removed, the condition (rollback window passed, version floor reached), and the separate change that does it. The temporary code (dual-write, fallback readers) and its removal story. -->
