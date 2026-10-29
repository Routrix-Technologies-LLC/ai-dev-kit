---
name: app-team-release
description: "Run the release squad from plan to post-release watch: release candidate and checklist, parallel quality gate, packaging or deploy prep per channel, go or no-go, the user's deploy or submit, then watching the release. Use when the user says 'ship it', 'cut a release', 'release this version', 'are we good to release', or wants a release coordinated across channels such as a web deploy, desktop installers, app stores or a package registry."
argument-hint: "[app] [version | next | watch <version>] [--review solo|lean|full]"
user-invocable: true
---

# Team: Release

Coordinates the people a release needs: a release manager who plans, a parallel quality gate (QA, security, privacy, performance, licenses), channel owners who prepare packages or deploys, a go or no-go decision recorded with evidence, the user's own deploy or submit decision, and a watch afterwards. It reuses `app-release` for the release artifacts and the publish step, `app-smoke`, `app-perf`, `app-security-audit` and `app-privacy-review` for evidence that is missing or stale, `app-store-prep` for store packages, and `app-hotfix` or `app-incident` if things go wrong. It never ships anything without an unconditional ask.

Writes: `docs/release/<version>.md` (checklist, via `app-release`, template `release-checklist.md`), `CHANGELOG.md`, release notes (template `release-notes.md`), and per-agent records `docs/release/<version>/<agent>.md`, the decision `docs/release/<version>/go-no-go.md`, the report `docs/release/<version>/release-report.md`, and watch notes `docs/release/<version>/watch-<date>.md`.
Next: `app-retro`, `app-incident` or `app-hotfix` if the release misbehaves, `app-gate` to record the stage.

## When to use and when not to

- Use for any planned release. For a single-person single-channel release with nothing to coordinate, `app-release` alone is enough.
- Not yet hardened: `app-team-harden` first. An emergency fix to the released version: `app-hotfix`. Store text only: `app-store-prep`. Checking what shipped is healthy: `watch` mode of this skill.

## Inputs

- The app per orchestration.md section 1. No `studio.yaml`: offer `/app-adopt` or `/app-start` and stop.
- **Version:** the argument, else inferred from `CHANGELOG.md`, the latest tag and the commits since it. Show the inference and confirm with the user; with nothing to infer, ask. Never default to a made-up version. `watch <version>` jumps to Phase 7.
- **Stage check, before anything is spawned:** the stage should be `release` (or `operate` for a follow-up release). Any earlier stage: stop and say `The release gate has not passed (stage: <stage>); run /app-gate first.` Ask in every mode: stop and run the gate (recommended), or proceed anyway. An override needs the user's reason, is recorded as a `Stage override:` line in the go/no-go record and the report, and never changes the stage.
- Read once and pass distilled: `studio.yaml`, the previous release record, the latest harden sign-off and audit (dates and verdicts), `perf-budget.md`, open bugs (S1/S2 count), the commits since the last tag, `planning/risks.md`, `docs/ops/runbooks/`.
- **Channels:** `studio.yaml` `channels` when filled, else inferred from `platforms` and `stack.hosting`; either way confirmed with the user. Unset means ask, never assume one channel.

| Channel | Owner of packaging or deploy prep | Notes |
|---|---|---|
| web or backend deploy | `infrastructure-engineer`, with `build-engineer` | migrations run before code needs them; `app-data-migration` evidence required if data changed |
| desktop installer or update feed | `desktop-packaging-engineer` | signing, notarization, update feed entry, package managers |
| iOS, Android, desktop store, extension store | `app-store-specialist` | submission package via `app-store-prep`; test track before production; phased rollout |
| library or CLI registry | `build-engineer` (and `desktop-packaging-engineer` for installers and package managers) | version stamp, provenance, tag |

## Phase 0: Resolve and announce

Main session: orchestration.md sections 1 and 2, the stage check, version and channel confirmation. `app-release` is user-typed (`disable-model-invocation`), so this session cannot invoke it as a skill. Ask once whether to follow `.claude/skills/app-release/SKILL.md` here by reading it: its Phases 2 to 6 are Phase 2 of this skill, and its Phase 7 asks are this skill's Phase 6, with the same one-ask-per-act rule. A "no" means the user types `/app-release` at Phases 2 and 6 and this skill supplies the squad work around it. `app-smoke`, `app-perf`, `app-security-audit`, `app-privacy-review` and `app-store-prep` are not user-typed and are run with the Skill tool. Print the announce block, with each conditional agent either listed or named under Not spawned with the reason.

## Phase 1: Plan (`release-manager`)

Writes `docs/release/<version>/release-manager.md`: scope since the last release (commits and closed stories), semantic version bump and why, channels and order, rollout strategy (all at once, staged percentage, canary, test track first), freeze rules, the rollback plan outline (what triggers it, how, how long, what data it cannot undo), and open questions. Decision point: user confirms scope, version, channels and rollout.

## Phase 2: Release candidate and checklist

Follow the preparation steps of `app-release` (including its Phase 5, the full rollback and rollout plan written into `docs/release/<version>.md` and read back; the Phase 1 outline is not enough): version stamped everywhere it lives, changelog entry under Keep a Changelog headings, release notes from the changelog (`technical-writer` drafts user-facing wording at standard and full), the checklist `docs/release/<version>.md` scoped to the chosen channels, and the candidate build from `commands.build_release` by `build-engineer`. A release branch is only for stabilizing and only if the app's process uses one.

Check: the checklist, changelog entry, release notes and the written rollback plan exist; the built artifact's embedded version equals the planned version (read it, do not assume). No rollback plan on disk, no Phase 3.

**Evidence currency (main session, before the spawn):** for each of smoke, security audit, performance and privacy, if the newest report predates the last source commit, run the studio skill (`app-smoke` on the release build, `app-security-audit quick` or full, `app-perf`, `app-privacy-review delta`) instead of asking an agent to redo it. These run one at a time in this session; heavy runs go through the run lock. The agents below then review fresh evidence.

## Phase 3: Quality gate (parallel)

Spawn in one message. Each brief names the release candidate build, the previous release, what changed (diff summary), and its output path.

| Agent | Spawn when | Job | Writes |
|---|---|---|---|
| `qa-lead` | always | read the `app-smoke` report for the release build (not debug), regression on critical paths, open S1/S2 count, check the harden sign-off covers this build; gate `QL-RELEASE-QUALITY` at `lean` and `full` | `docs/release/<version>/qa-lead.md` |
| `security-lead` | always | is there a security review covering the current code: compare the latest audit date to commits since; if code changed in sensitive areas, a delta review by `security-engineer` is required; gate `SL-SECURITY-REVIEW` at `lean` and `full` | `docs/release/<version>/security-lead.md` |
| `privacy-specialist` | data collection, storage, sharing, an SDK or permission changed since the last release; unknown means ask | privacy record current, store declarations match behavior; gate `SL-PRIVACY` (run by `security-lead`) at `lean` when data handling changed, always at `full` | `docs/release/<version>/privacy-specialist.md` |
| `performance-engineer` | always (minimal: only if the budget exists) | read the `app-perf` report on the release build against `perf-budget.md`; no budget means NO BUDGET, not a pass | `docs/release/<version>/performance-engineer.md` |
| `compliance-specialist` | dependencies, assets or store policies changed | licenses and notices, SBOM current, store policy conformance | `docs/release/<version>/compliance-specialist.md` |

Check: every spawned agent's file exists with real content and states a result in its own vocabulary. A missing one is re-briefed once, then a named BLOCKED gap. A stale harden sign-off or audit (code changed since) is reported as CONCERNS with the commit range, not ignored.

## Phase 4: Packaging and deploy prep, per channel (parallel)

One channel owner per chosen channel, spawned together. They prepare, build and verify locally; they publish nothing.

- Artifacts built from the release candidate commit; checksums recorded.
- Signing and notarization or provenance: the owner uses signing material already configured on the machine or in CI, never prints it, and lists every command before running it (one ask for the set, since these change files in the output folders).
- Verification of what was built: signature verifies, installer installs and launches on a clean target where one exists (else NOT VERIFIED), update feed entry validates, container image runs its health check, store package passes the store's local validators.
- Store channels: `app-store-prep` drafts the listing, declarations and review notes; the user submits.
- Rollback rehearsal on paper or on staging: the previous artifact is retrievable and the steps are exact.
- Output: `docs/release/<version>/<agent>.md` with the artifact list, hashes, verification results and what was NOT VERIFIED.

## Phase 5: Go or no-go

1. Gates per mode (orchestration.md section 7 and `gates/README.md`): `RM-RELEASE-READY`, `QL-RELEASE-QUALITY` and `SL-SECURITY-REVIEW` all run at `lean` and `full`, and `SL-PRIVACY` at `lean` when data handling changed and always at `full`. The last three ran in Phase 3; spawn `release-manager` now for `RM-RELEASE-READY` with the gate ID, the Phase 3 verdict lines and the Phase 3 and 4 file paths. `solo` prints each as skipped: solo mode; the quality agents of Phase 3 still ran, only the formal verdicts are skipped, and without them the decision cannot be GO (it is CONCERNS or NOT ASSESSED) unless the user explicitly accepts releasing unreviewed, recorded with the date. Record each outcome in the header of `docs/release/<version>.md`.
2. Spawn `release-manager` to draft `docs/release/<version>/go-no-go.md`. Brief it with every sign-off's result and path, open bugs, the stage override line if any, and the verdict rules below verbatim, never a verdict. The main session then checks the draft against the same rules; if they disagree, show both and ask.
3. Strictest wins across sign-offs and gates (orchestration.md section 7). One NOT ASSESSED keeps the result from being GO.

On `NO GO`: surface the blocking items, then offer: fix and re-run the affected phase, defer the release, or record a risk acceptance in writing. The verdict word stays NO GO; the acceptance is the user's call and is embedded in the decision record. A `SL-SECURITY-REVIEW` BLOCK is a stop-ship that only the user can accept, and `RM-RELEASE-READY` cannot return GO while it stands. Phase 6 then asks as usual. On `CONCERNS`: list them and ask whether to accept each, fix, or defer.

## Phase 6: Deploy or submit (unconditional ask)

This phase needs the user's explicit yes in every mode, including a run that was told to proceed automatically. List the exact outward actions in order for each channel (merge, tag, push, artifact upload, deploy, store submission, notes publication, feed update) and ask: all as listed, staged first (test track, staging, canary, or first rollout percentage), or stop. The user may choose per channel.

After a yes:

- The channel owner and `release-manager` execute only the listed actions, one channel at a time, verifying each step (tag exists, artifact reachable, health check green, submission accepted) before the next. A failed step stops the sequence; do not continue to the next channel; consult the rollback plan and ask.
- Secrets are never echoed. No force-push, no deletion of tags or releases, no change to the stage.
- Staged rollouts advance only on a fresh yes after the watch in Phase 7 looks healthy.

## Phase 7: Post-release record and watch

1. `release-manager` writes `docs/release/<version>/release-report.md`: what shipped, what was deferred, deviations, how each channel was verified live, links to the sign-offs.
2. Watch plan per channel with first checks at sensible times (a web deploy minutes and hours, a store release after review and during phased rollout, a desktop update feed after the first updates land), what signals to read (crash-free rate, error rate, latency, install and update failures, support reports, store reviews) and what threshold means rollback.
3. **Watch mode** (`/app-team-release watch <version>`): read the release record, collect the signals (from commands, dashboards the app has, or what the user pastes; unavailable signals are named), then `site-reliability-engineer` and `qa-lead` assess against the thresholds and write `docs/release/<version>/watch-<date>.md`. Watch verdicts: `ROLLBACK RECOMMENDED`, `DEGRADED`, `NOT ASSESSED` (no signals obtainable), `HEALTHY`. Rollback itself needs the user's yes; an incident goes to `app-incident`, a fix to `app-hotfix`.
4. Recommend `/app-retro` and `/app-gate` to record the stage; never start either.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Plan and checklist | short plan, one-page checklist | full plan and `release-checklist.md` | plus staged rollout design |
| Quality gate | `qa-lead` on the release build, `security-lead` delta check; `privacy-specialist`, `compliance-specialist` only if their condition holds | plus `performance-engineer` and all conditional agents | plus every formal gate |
| Packaging | build, sign if configured, verify | plus clean-target install check | plus rollback rehearsal |
| Gates (by review mode, default shown) | solo: none run | lean: `RM-RELEASE-READY`, `QL-RELEASE-QUALITY`, `SL-SECURITY-REVIEW`, plus `SL-PRIVACY` if data handling changed | full: all four |

Phases that may be skipped at minimal: `technical-writer` wording, the conditional lenses whose condition is false (printed), rollback rehearsal beyond writing the plan. Never skipped: the stage check, Phase 3 smoke on the release build, a security currency check, the rollback plan, the go or no-go record, and the Phase 6 ask.

## Verdicts

First match wins. The verdict is the release decision; whether it was deployed is a separate line in the report.

1. `NO GO` - an open CRITICAL or S1, a blocking gate or sign-off, smoke FAIL, a signing or verification failure, or no rollback plan.
2. `CONCERNS` - no blocker, but a sign-off carries CONCERNS (stale audit, accepted risk, deferred HIGH), to be accepted or fixed by the user.
3. `NOT ASSESSED` - a required sign-off is missing or NOT ASSESSED (no budget, nothing observable on the release build, an agent returned nothing, a channel verification NOT VERIFIED). Name each.
4. `GO` - every required sign-off present and passing, release build verified, rollback plan written.

## Report

```
Release: <app> <version>   Channels: <list>   Stage: <stage> (override: none | reason)   Rigor: <r>   Review: <m>
Plan: <path> | Candidate: <commit, artifact hashes>
Quality gate: qa <result> | security <result, audit age> | privacy <result or not spawned: why> | performance <result> | compliance <result or not spawned: why>
Packaging: <channel: verified / NOT VERIFIED items>
Decision: <verdict> (<path>)   Deployed: <not deployed | staged: where | released: where>   User decision: <as given>
Watch plan: <signals, thresholds, first check time>
Gaps: <named>
```

Then the closing block from orchestration.md section 8.

## Rules for this skill

- Nothing is tagged, pushed, uploaded, deployed, submitted or published without the Phase 6 ask, in any mode, and never in an earlier phase.
- Never decide GO for the user; the user may accept the risks of a NO GO only with a written reason that is recorded.
- Never declare a release healthy without signals; no signals is NOT ASSESSED.
- Never print or store secrets, signing keys or tokens in any record.
- Never write the stage; recommend `app-gate`.
- Agents write only their named file; a skipped agent's section stays a named gap.
