---
name: app-data-migration
description: "Plan and rehearse a schema or data-format change (server database, on-device store, file or save format, config format) with expand and contract steps, backfill, a dry run on a copy, proof that old data still loads, and a tested rollback. Use when the user changes a database schema, changes a file or settings format, moves data stores, or asks if a migration is safe to ship."
argument-hint: "[app] [plan <slug> | rehearse <id>] [--review solo|lean|full]"
user-invocable: true
---

# App Data Migration

A migration is ready only when it has been run, on a copy, and both directions worked. This skill writes the plan, then rehearses it against a copy of representative data, proves the previous version of the data still loads, and proves rollback restores it. It never touches real data: not production, not the user's own installed data, not a shared development database that is not a throwaway.

Writes: `planning/migrations/<id>.md` (template `data-migration-plan.md`), rehearsal evidence in `docs/qa/evidence/<id>/`.
Next: `/app-plan` (stories for the migration and its release), `/app-release`, `/app-bugfix` (if the rehearsal found defects), `/app-observability` (migration monitoring).

## When to use and when not to

- Use for any change to how stored data is shaped or encoded, anywhere it lives.
- API contract changes alone are `/app-api`. Dependency or framework upgrades that carry a data change start at `/app-upgrade` and call this skill for the data part. Pipeline or warehouse backfills at volume bring in `data-engineer`.

## Inputs

- Required: `studio.yaml` (`stack.data`, platforms), the current schema or format definition, the intended new one, and the migration tooling the app already uses (read the repo for it; do not introduce a second tool without asking).
- Needed to rehearse: a copy of representative data. Sources, in order of preference: a sanitized export of production, a snapshot restored into a scratch environment, a generated dataset sized and shaped like production (record how it was generated and what it cannot represent), fixtures from tests. If none can be made, the rehearsal is NOT ASSESSED; do not rehearse on empty data and call it a pass.
- Missing definition of the new shape: ask, or offer `/app-spec` or `/app-architecture`.

## Where the data lives: routing

| Data location | Lead and specialists | Special concerns |
|---|---|---|
| Server relational database | `database-engineer`, `backend-lead`, `backend-engineer` | Lock duration, online change, replication lag, connection pools, rolling deploy with two app versions live |
| Server document or key-value store | `database-engineer`, `backend-lead` | No enforced schema, so old and new shapes coexist; readers must tolerate both |
| Pipelines, warehouse, search index | `data-engineer` | Backfill volume, reprocessing, index rebuild, dual write |
| On-device store (mobile, desktop embedded database) | `database-engineer`, `mobile-lead` or `desktop-lead`, the platform engineer | Runs on every user's device with no operator; app store rollout lag; user may skip versions; interrupted by app kill or low disk; no dry run on the real device |
| Files, save and document formats, settings | `database-engineer`, the platform engineer | Forward and backward compatibility, versioned headers, unknown field preservation, backup before write |
| Browser storage, extension storage | `web-platform-engineer`, `database-engineer` | Quota, eviction, multiple tabs and versions open at once |
| CLI config and caches | `principal-engineer`, language specialist | Hand-edited files, comments, partial writes |

`qa-lead` reviews the rehearsal evidence for every route.

## Phase 1: Resolve and announce

Per `orchestration.md` sections 1 and 2. Assign an id (`MIG-NNNN-<slug>`, never renumbering existing files in `planning/migrations/`).

Check: announce block printed, id chosen, data location(s) classified from the table.

## Phase 2: Understand the change (plan mode)

Spawn `database-engineer` (and the routed specialist) with: the current definition, the intended definition, the migration tooling, the app's deploy and release model (rolling server deploy, store release lag, user-controlled updates), and the min supported version of the app that may still read or write this data (`studio.yaml` `min_targets`). Output: a draft of `planning/migrations/<id>.md` at that exact path.

Write it into the numbered headings of `templates/data-migration-plan.md` (1 Change and reason, 2 Compatibility strategy: expand and contract, 3 Preconditions and risks, 4 Backfill design, 5 Dry run on a copy, 6 Rollback (tested), 7 Old data still loads, 8 Real-data run (user's action only), 9 Monitoring and sign-off, 10 Cleanup), with Status `Draft` in its header line. The ten items below map onto them: items 1 to 3 to sections 1 and 2; 4 to section 4; 5 to section 6; 6, 7 and 8 to section 3; 9 to section 7; 10 to sections 9 and 10. Section 5 is filled by Phase 4, and section 8 is written as steps for the user to run or authorize, never for an agent to run. The plan must contain, each concretely:

1. **What changes and why**, with the requirement or story that needs it.
2. **Compatibility window.** Which app versions can run against the old shape, the new shape, and both. A server rolling deploy means two code versions share one database for a while; a mobile or desktop app means old versions keep running on migrated or unmigrated data.
3. **Expand and contract sequence.** Expand (add new structure beside the old, tolerated by old code), migrate and backfill (copy and convert in batches, resumable, idempotent), switch reads then writes (behind a flag where possible), then contract (remove the old structure in a later release, after nothing reads it). No step both renames and drops in one release. A destructive step is its own step with its own backup.
4. **Backfill design.** Batch size, ordering, resumability after interruption, throttling to protect production, how progress is measured, how the result is verified (row counts, checksums, sampled field-by-field comparison).
5. **Rollback for each step.** What the undo is, what it loses (data written in the new shape after the switch), and the point after which rollback becomes a restore from backup. State that point plainly.
6. **Backups.** What is backed up before each destructive step, where, how restore was tested.
7. **Interruption safety.** What state remains if the process dies at each step; the migration re-runs safely.
8. **Failure budget.** Expected duration, locks held, user-visible impact, and the stop condition at which the operator aborts.
9. **Old data still loads.** The list of old-shape fixtures the new code must read, including the oldest supported version's output and any hand-edited or malformed samples seen in the wild.
10. **Release coupling.** Which release carries each step and the monitoring that watches it.

Check: the plan file exists with every template section required at the rigor non-empty (a section that does not apply says why in one line).

## Phase 3: Review the plan (parallel)

Spawn in one message: `backend-lead` (or `desktop-lead` or `mobile-lead` per route) for architecture fit and release coupling, and `qa-lead` for testability: can every claim in sections 4 to 9 be shown by a rehearsal? Each writes one review file under `~/AgentScratch/app-data-migration/<run>/`. Gaps go back to `database-engineer` once; a second failure is BLOCKED.

Decision point: show the plan summary, the point of no return, and ask the user to approve rehearsal (AskUserQuestion). Rehearsal runs real migration code on a copy; approval is for the copy and the commands, not for any real data.

## Phase 4: Rehearse on a copy

Spawn `database-engineer` and `test-engineer` to build the rehearsal, or run it in the main session if it is a handful of commands. Rules:

1. **Make the copy first and prove it is a copy.** State its location and how it differs from real data (sanitized, sampled, generated). Print the connection string or path with credentials removed and confirm it is the scratch target, not the live one. For server databases use a restored snapshot or a disposable instance. For on-device stores use a copied store file or an emulator or simulator profile. For files, copy to a scratch folder.
2. **Record the before state:** row or record counts per table or type, checksums or hashes on key columns, schema dump or file hash.
3. **Run the forward migration** with the app's real migration tooling, timed. Capture the output.
4. **Verify after:** counts reconcile (state each expected delta), sampled records compare field by field against the source, constraints and indexes exist, the new code reads the migrated data (run the app's tests or a read path against it).
5. **Old data still loads:** feed each old-shape fixture from plan item 9 to the new code, and where the compatibility window allows, run the previous app version against the migrated copy. Every fixture gets a pass or fail line.
6. **Interrupt it:** kill the run mid-backfill and rerun. It must resume or restart without duplicates or loss.
7. **Run rollback** per step, then re-verify counts and checksums against the before state. State exactly what, if anything, differs and whether the plan predicted it.
8. **Run forward again** after rollback to show the sequence is repeatable.
9. **Scale:** if the copy is smaller than production, extrapolate duration only with the stated ratio and label it ESTIMATED. Lock time and index build time do not extrapolate linearly; say so.

Evidence goes in `docs/qa/evidence/<id>/` (a `rehearsal.md` with commands run, durations, before and after counts, fixture results, rollback comparison; trimmed command output; no real personal data). A pass that lists no counts is not evidence.

Check: `rehearsal.md` exists and contains before and after counts, one result line per old-data fixture, the rollback comparison and the interruption result. Missing any is a failed phase.

## Phase 5: Decide readiness and write back

1. Update `planning/migrations/<id>.md`: set Status to `Rehearsed` only if the rehearsal passed (never `Approved by the user`, `Run`, `Verified` or `Closed`: those record the user's actions), and write rehearsal results, point of no return, estimated production duration (labelled), open risks, release coupling, and the go criteria.
2. Propose stories for each step (expand, backfill, switch, contract, monitoring) for `/app-plan`; do not write story files.
3. Overwrite the checkpoint.

The destructive production run itself is never done by this skill. Executing against real data is a separate, explicit act by the user or by `/app-release`, preceded by the unconditional ask in `orchestration.md` section 6 ("any destructive data operation").

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Plan | template sections 1, 3, 5, 6 and 8 as a short checklist | all ten | all ten, plus failure budget agreed with `site-reliability-engineer` for server data, a staged rollout and monitoring thresholds |
| Rehearsal | forward, old data loads, rollback on a small copy | plus interruption and counts reconciliation | plus production-shaped scale and timing |
| Reviews | `qa-lead` | plus the lead for the route | plus `security-lead` when personal data is moved or transformed |

Rigor changes what must exist, never what must work: rollback is always run, at every level.

No gate is attached; the closing block's Gates line reads `none run (no gate attached to app-data-migration)`.

## Verdicts

First match wins.

1. `NOT READY`: the rehearsal failed forward, an old-data fixture failed, rollback did not restore the before state (and the plan does not accept the difference in writing), the migration is not interruption safe, or a destructive step has no backup.
2. `CONCERNS`: the rehearsal that ran passed, but production scale, lock time or duration is only ESTIMATED, the compatibility window is narrower than `min_targets`, or the point of no return arrives earlier than the user expected.
3. `NOT ASSESSED`: no copy of representative data could be made, the rehearsal did not run, rollback was not run, the migration tooling is unknown, or an agent's evidence is missing. A rehearsal on empty or trivial data is NOT ASSESSED. State which. (It ranks below NOT READY and CONCERNS, which name a known problem, and above READY.)
4. `READY`: forward, old-data, interruption and rollback all run on a named copy with counts reconciled, the plan is complete, and the user has seen the point of no return.

## Report

```
Migration: <id> <title>   Data: <location and store>
Copy used: <what, size, how it differs from real data>
Forward: <duration, counts before to after, expected deltas matched yes/no>
Old data loads: <N of N fixtures>   Previous app version against migrated copy: <pass|fail|not applicable (why)>
Interruption: <resumed|restarted clean|failed>   Rollback: <restored|differs: what>
Point of no return: <step>   Production duration: <ESTIMATED from ratio, or measured>
Skipped: <step and why>
Proposed stories: <list>
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Never run against real data: production, installed user data, or a shared development database that is not disposable. If the target cannot be proven to be a copy, stop.
- Never run a destructive production step. Preparing is this skill's job; executing needs the user's explicit yes at that moment.
- Never combine a rename and a drop in one release, or contract before nothing reads the old structure.
- Never report READY without rollback having been run.
- Never use empty or trivial data as the rehearsal and call it a pass.
- Never put real personal data in evidence files.
- Never renumber or overwrite an existing migration plan.
