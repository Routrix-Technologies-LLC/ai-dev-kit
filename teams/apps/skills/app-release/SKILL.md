---
name: app-release
description: "Prepare a release of an app for every channel it ships through (web or service deploy, desktop installers and update feeds, package managers, app stores, package registries): version, changelog, release notes, checklist, packaging and signing checks, rollout and rollback plan, go/no-go. Tags, publishes, deploys or submits only after an unconditional ask. Use when the user says release, ship, cut a version, publish, deploy to production, submit the build, or 'are we ready to ship'."
argument-hint: "[app] [version or 'next'] [--channels <list>] [--review solo|lean|full]"
user-invocable: true
disable-model-invocation: true
---

# App Release

Prepares a version to reach users and records the decision. It writes the plan, the notes, the checklist and the rollback plan first, verifies the packages, asks the gates, and only then asks the user, one irreversible act at a time, before it tags, publishes, deploys or submits.

Writes: `docs/release/<version>.md` (template `release-checklist.md`), `docs/release/<version>-notes.md` (template `release-notes.md`), `CHANGELOG.md`.
Next: `/app-store-prep` (store channels, before this), `/app-hotfix` (if the release is bad), `/app-gate` (release to operate once it is live), `/app-retro`.

## When to use and when not to

- Use for a planned release of a version. For a store listing and review package only, `/app-store-prep` first. For an emergency fix on the live version, `/app-hotfix`. For "is the app ready for the release stage", `/app-gate hardening to release`. For the whole release squad, `/app-team-release`.
- Stage should be `release` or `operate`. If it is earlier, stop and recommend `/app-gate`. The one exception is an internal or beta-only channel (a test track, an internal feed, a staging deploy); say so in the record and keep every irreversible ask.

## Inputs

- `studio.yaml`: `platforms`, `stack` (including `stack.hosting`), `commands` (`build_release`, `test`), `channels`, `infra_record`, `rules`.
- The last release: newest tag (`git tag --list`), previous `docs/release/<version>.md`, `CHANGELOG.md`.
- Evidence from earlier skills: newest smoke, security audit, performance, accessibility, privacy records. Missing or stale evidence is reported, and the gate that depends on it is NOT ASSESSED; this skill does not produce it (it names the skill).
- **Channels:** `studio.yaml` `channels` when filled, else proposed from `platforms` and `stack.hosting`. Either way the user confirms the exact list for this release. Never assume a channel, and never add one the user did not confirm. If `channels` is empty, suggest the user record the confirmed list there.

## Phase 1: Resolve and plan

Follow `orchestration.md` sections 1 and 2. Then:

1. Version: derive the proposed version by semantic versioning from the changes since the last tag (breaking public change: major; features: minor; fixes only: patch). Show the reasoning and ask. The version string must match what the build stamps (check the manifest or version file). Mobile stores also need a build number or version code that only ever increases, separate from the user-visible version: check it against the last uploaded build.
2. Channels: confirm the list. Route each channel to its owner:

| Channel | Examples | Owner agent | What is specific |
|---|---|---|---|
| Web or service deploy | container image, static host, serverless, VM | `infrastructure-engineer` (with `build-engineer`) | immutable artifact, config per environment, migrations first, health checks, staged or blue-green, rollback is redeploying the previous artifact (and a data plan) |
| Desktop installers and update feeds | MSIX, MSI, pkg and dmg, Flatpak, AppImage, auto-update feed | `desktop-packaging-engineer` | signing and notarization, install and upgrade on a clean machine, feed entry staged and reversible, downgrade protection; what is already installed cannot be recalled |
| Package managers | winget, Homebrew, Chocolatey, distro repositories | `desktop-packaging-engineer` | manifest and checksum correct, review by the repository's maintainers, hash matches the published file |
| Mobile and desktop stores | App Store, Google Play, Microsoft Store, Mac App Store, extension stores, Flathub or the Snap Store | `app-store-specialist` | review time and rejection risk, phased rollout where the store offers it, store signing and upload-key handling, an increasing build number, a published store version cannot be unpublished (you ship a newer one) |
| Package registries | npm, PyPI, crates.io, NuGet, Maven | `build-engineer` with the language specialist from `studio.yaml` | publish is effectively permanent (yank, not delete), dry run first, provenance and 2FA, files in the package are exactly intended |
| Binary downloads (CLI, release pages) | tarballs, zip, GitHub-style releases | `desktop-packaging-engineer` or `build-engineer` | checksums, signatures, install script safety |

3. Print the plan block. Gates (`gates/README.md`): `RM-RELEASE-READY`, `SL-SECURITY-REVIEW` and `QL-RELEASE-QUALITY` run at `lean` and `full`; `SL-PRIVACY` runs at `lean` when personal-data handling changed since the last release (unknown means ask) and always at `full`. `solo` runs none: print `<GATE-ID> skipped: solo mode` for each, and the verdict cannot be GO on gate evidence it did not collect (see Verdicts). `solo` never skips the checks in Phases 3 to 5.
4. Checkpoint.

## Phase 2: Changelog and notes (release-manager)

1. Gather changes since the last tag from `git log` and the Complete stories. Every entry must trace to a commit or story; a claim with no source is dropped, not rewritten. Provenance check: if the last tag, `CHANGELOG.md` and the commit history disagree about what shipped last time, report the discrepancy.
2. `release-manager` drafts the `CHANGELOG.md` entry in Keep a Changelog form (Added, Changed, Deprecated, Removed, Fixed, Security), with the date and version, and `docs/release/<version>-notes.md` from `release-notes.md` (user-facing: what changed for people, known issues, upgrade notes, data or setting changes). At standard and full, `technical-writer` may polish the notes copy.
3. The main session edits `CHANGELOG.md` (it is an existing file: list it in the files-to-touch ask) and writes the notes. Verify by reading both back.

## Phase 3: Quality and security gates (parallel)

Spawn in one message, at the review modes that run them: `qa-lead` (`QL-RELEASE-QUALITY`), `security-lead` (`SL-SECURITY-REVIEW`), a second `security-lead` for `SL-PRIVACY` when data handling changed (over the current `docs/security/privacy.md`; if that record is older than the change, run `/app-privacy-review delta` first and say so), and `compliance-specialist` when dependencies or assets changed (licenses and notices). Per `orchestration.md` section 7: pass the gate ID and context (version, channels, evidence paths and dates, open S1/S2 and CRITICAL/HIGH counts), tell the agent to read its gate file. Each writes `docs/release/<version>/<agent>.md` (layout.md run records; a second `security-lead` run writes `security-lead-privacy.md`).

Also run, yourself, what the verdict turns on: `commands.build_release` from a clean state, `commands.test`, and read the newest smoke report (is it newer than the last source commit; does it cover every platform). A check that cannot run is NOT ASSESSED.

## Phase 4: Package and channel checks (per channel, in parallel)

Brief each channel owner (Phase 1 table) to prepare and verify, writing findings to `docs/release/<version>/<agent>.md` (one section per channel when one agent owns several), **without publishing**:

- Build the shipping artifact from the release commit, not a dev build; version stamp matches.
- Integrity: checksums recorded; signature verified with the platform's own verify tool (for example the code-signing verify command, a notarization status check, a package signature check); the report quotes the tool output.
- Clean-machine or clean-environment install, launch, upgrade from the previous version, and uninstall or rollback of the package. Evidence or NOT VERIFIED with the reason (no clean target available is NOT VERIFIED, not "fine").
- Dry run of the publish command where the channel has one (registry dry run, store validation upload to a test track, deploy to staging).
- Update path: the feed or store entry for the new version, staged percentage, and what existing users see.
- Secrets: credentials and signing keys are used from the secret store; none are written to the repo or the record.

If a channel needs a store package, route to `/app-store-prep`; a missing store package makes that channel NOT ASSESSED.

## Phase 5: Rollback and rollout plan (before anything irreversible)

Write the plan into `docs/release/<version>.md` **before** the first ask in Phase 7, and read it back to confirm. It names, per channel: the rollout shape (all at once, staged percentages, phased, canary) and the pause point; the signals watched and thresholds that trigger a rollback; who decides; the mechanism and the time it takes; data compatibility (is the previous version safe with data the new one wrote; migration reversibility); what cannot be undone (installed desktop builds, store versions, registry publishes) and the fix-forward path (`/app-hotfix`); and who is told. A plan that says "revert the commit" is not a plan. No plan on disk, no Phase 7.

## Phase 6: Checklist and go/no-go

1. Write `docs/release/<version>.md` from `release-checklist.md`: one row per applicable item, grouped by channel, each row PASS, FAIL, N/A with reason, or NOT ASSESSED with reason, with its evidence path.
2. At the review modes that run it, spawn `release-manager` with `RM-RELEASE-READY`, the whole record and the Phase 3 verdict lines (it cannot return GO while one of them is blocking or NOT ASSESSED). Record each gate outcome in the header of `docs/release/<version>.md`, one line per gate, as `gates/README.md` "Recording a gate outcome" shows. Combine with the Phase 3 gates per `orchestration.md` section 7.
3. Verdict by the rules below. Present the analysis in plain text and the open items, then the decision (Phase 7).

## Phase 7: The unconditional asks

Every irreversible act has its own ask, in every mode and every review mode: merging to the release branch, creating the tag, pushing the tag or any branch, publishing a package, deploying to production, uploading or submitting a store build, promoting a staged rollout. One yes covers one act and one channel.

- **GO:** ask per act. Options: do it now / do only the earlier acts and stop / stop.
- **CONCERNS:** list each concern; the user must accept each one in writing (recorded in the record's "Accepted risks"); then ask as for GO.
- **NOT ASSESSED:** do not offer to proceed by default. The user may choose to ship unverified; that is a separate explicit decision naming each unassessed item, recorded with the date, and the verdict stays NOT ASSESSED.
- **NO GO:** no asks to act. Name the blockers and the skills that clear them.

After a yes, perform the act only if it is non-interactive and credentials are already in place; otherwise print the exact command (or steps) for the user to run, and wait for the user to confirm it happened. A confirmation is recorded as user-stated with the time. Never run an act on the strength of an earlier answer, never batch two acts into one ask, and never publish to a channel the user did not confirm in Phase 1.

## Phase 8: After the act

Update the record with what happened, when and by whom. Watch the signals named in Phase 5 for the first window with the user (query, dashboard, store console: the user supplies what the repo cannot show). Report the first-window result honestly; "no data yet" is not "healthy". Recommend `/app-gate release to operate` when the release is live.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Record | checklist, tests green, run and observe, CHANGELOG entry, rollback plan | plus security review for sensitive areas, release-quality review, release notes | plus privacy, accessibility, performance evidence, rehearsed rollback |
| Gates (set by review mode, shown here at its default) | solo: none run | lean: `RM-RELEASE-READY`, `QL-RELEASE-QUALITY`, `SL-SECURITY-REVIEW`, plus `SL-PRIVACY` if data handling changed | full: all four |

Review mode follows `orchestration.md` section 7 with the always-on gates named in Phase 1. Rigor changes which documents must exist, never whether a clean build, passing tests, a verified signature and a written rollback plan are required.

## Verdicts

First match wins.

1. **NO GO:** a blocking gate verdict (`NO GO`, `NOT READY`, `BLOCK`), an open S1 or S2 bug, an open CRITICAL or HIGH security finding, a failing release build or test run, an unverified signature on a channel that requires one, or no rollback plan.
2. **CONCERNS:** all of the above clear, but a gate returned CONCERNS, a recommended item is missing, or a known issue is shipping by decision.
3. **NOT ASSESSED:** a required check could not run or has no fresh evidence (stale smoke, unrunnable tests, a channel with no package, a gate agent that did not return, a clean-machine install that could not be done). The record says which.
4. **GO:** every applicable row passes, every gate required at this review mode returned its pass word, the plan is on disk. At `solo`, or whenever a required gate was skipped, GO is not available: the verdict is CONCERNS or NOT ASSESSED, naming the skipped gates, unless the user explicitly accepts running the release unreviewed (recorded with the date, and the report says so).

## Report

```
Release: <app> <version>  Channels: <list>  Rigor: <r>  Review: <mode>
Checklist: <n of n> rows pass, <n> concerns, <n> not assessed
Build and tests: <result with N of N>   Signatures verified: <n of n>   Rollback plan: <written, read back>
Acts asked and answered: <act: yes/no/not asked>
Verdict: <WORD> - <one line why>
Gates: <RM-RELEASE-READY, QL-RELEASE-QUALITY, SL-SECURITY-REVIEW: verdicts> | none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never merge, tag, push, publish, deploy or submit without an unconditional yes for that act in this run, in every mode. `disable-model-invocation: true`: only the user starts it.
- The rollback plan is written and read back before the first ask.
- Never write signing keys, tokens or credentials to the repo or the record.
- A step that did not run is named as such in the record; a stale or missing check is NOT ASSESSED, never a pass.
- Verify specialist claims that the verdict turns on (re-read the signature output, re-run the build); label the rest UNVERIFIED.
- Do not invent changelog entries or channels. Recommend the next skill; never start it.
