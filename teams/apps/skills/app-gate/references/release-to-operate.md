# Checklist: release to operate

Question: did this version reach users, can it be rolled back, and will the team see trouble before users report it?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (listed, never counted as passed). Facts about what is live in a store or a hosting environment cannot be read from the repo: ask the user and label the answer user-stated; an unanswered question is NOT ASSESSED. **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | Release record complete with a go/no-go | `docs/release/<version>.md` | Every checklist row is resolved or marked N/A with a reason; the recorded verdict is GO, or CONCERNS with the user's acceptance. A NO GO is FAIL. At review mode `full` the `RM-RELEASE-READY` outcome (GO, or CONCERNS accepted by the user) is recorded in the header; at `lean` it runs inside `/app-release`, so a missing line means the release did not go through that skill: report it | R | R | R |
| 2 | The release reached users | git tags where the app tags releases; the user | `git tag --list` shows the version tag (an app that does not tag records its version identifier in the release record instead). For each channel in the record, the user states it is live (or approved and rolling out). Count "N of N channels confirmed" | R | R | R |
| 3 | Changelog and release notes | `CHANGELOG.md`, `docs/release/<version>-notes.md` | A dated entry for exactly this version; entries trace to merged stories or commits | R | R | R |
| 4 | Rollback plan written and specific | the release record | Trigger criteria, who decides, mechanism per channel, data compatibility, and what cannot be undone. Not "revert the commit" | R | R | R |
| 5 | Rollback tested or rehearsed | the release record | A rehearsal, a previous successful rollback, or a staging dry run is recorded | - | rec | R |
| 6 | Post-release smoke on the shipped artifact | `docs/qa/smoke-<date>.md` | Run against the live URL, the installed package from the real channel, or the store build, and observed. Not the pre-release build | R | R | R |
| 7 | Monitoring and crash reporting live, with a signal seen | `docs/ops/observability.md`, dashboards | Deployed or distributed apps: the user or a query shows at least one real event or crash arriving, with a symbolicated stack if crash reporting is used. Local-only apps record `N/A: no telemetry by design` | rec | R | R |
| 8 | Runbooks for the top failure modes | `docs/ops/runbooks/` | One per alert or likely failure (deploy failure, data restore, rollback); each has steps and a verification | - | R | R |
| 9 | Owner and contact for incidents | runbooks or the release record | A named person or channel who is reached first | - | rec | R |
| 10 | Watch-window result recorded | the release record | Error, crash and latency numbers for the first window compared with the baseline, or "no baseline" stated | - | rec | R |
| 11 | Next cycle started | `planning/` | Known issues and deferred items from the release are stories or backlog rows | rec | rec | R |

## Quality checks

Run the post-release smoke (item 6) yourself if a command or script exists for the live target; otherwise it is a manual check and the item is NOT ASSESSED until the user supplies the observation. Read back the rollback plan once; confirm it names a mechanism for every channel in item 2.

## Manual checks

- Have you seen the live version working with your own eyes?
- If this release were bad right now, do you know the first thing you would do?

## Panel focus

`TD-PHASE-GATE` and `PG-PHASE-GATE` are required; `PD-PHASE-GATE` is optional at standard and runs at full rigor (with `DD-PHASE-GATE`). `TD-PHASE-GATE`: operability and rollback. `PG-PHASE-GATE`: delivery closed out cleanly and the next cycle is staged. `PD-PHASE-GATE` and `DD-PHASE-GATE`: the live product matches intent.

## On PASS

Stage becomes `operate`. There is no later gate. Next: `/app-retro`, `/app-observability` (to fill gaps), `/app-incident` and `/app-hotfix` as needed, `/app-plan` for the next cycle.
