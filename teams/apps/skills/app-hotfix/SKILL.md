---
name: app-hotfix
description: "Emergency fix on the released version of an app: confirm severity, branch from the release tag, make the minimal fix with a regression test seen failing then passing, get independent review and QA, check the backport to the main branch, write the rollback plan before any deploy, and ask unconditionally before merge, tag, deploy or submit. Use when the user says hotfix, production is broken, users are losing data, urgent patch to the live version, or a crash in the released build."
argument-hint: "[app] [bug id or description] [--review solo|lean|full]"
user-invocable: true
disable-model-invocation: true
---

# App Hotfix

The fastest safe path from "the live version is hurting users" to a fix in their hands: smallest possible change, proven by a test that failed first, reviewed by someone else, with a way back written down before anything ships. Speed comes from cutting scope, never from skipping the checks or the asks.

Writes: the fix and its regression test, `docs/release/<patch-version>.md` (template `release-checklist.md`, hotfix record), a `CHANGELOG.md` entry, evidence in `docs/qa/evidence/hotfix-<slug>/`.
Next: `/app-incident` (the postmortem, within days), `/app-smoke`, `/app-release` for follow-on channels, `/app-retro`.

## When to use and when not to

- Use for S1 (Critical) and S2 (High) defects in a version users already have, as defined in `standards/severity.md`. Rate a security issue by its impact.
- Not for S3 and S4: use `/app-bugfix` and ship in the next release. Not for a regression found before release: `/app-bugfix` on the branch. Not for running the outage itself (comms, status, mitigation choices): `/app-incident`, which can run alongside this.
- If mitigation without code is faster (flag off, config revert, rollback to the previous release), say so in Phase 2 and offer it first. A hotfix is not the only remedy.

## Inputs

- A bug id or description, and the version where it was seen. `studio.yaml` (`commands`, `platforms`, `rules`, `specialists`). The release tags (`git tag --list`) and the newest release record in `docs/release/`.
- Which tag users are actually on is asked, never assumed from the newest tag. A mobile or desktop app may have several live versions; the fix targets the user's choice and the report says which.

## Phase 1: Severity

Read the report. Rate on `standards/severity.md` (S1: crash, data loss, security impact, complete feature failure; S2: major feature broken with the app usable). Show the rating and the reason; ask (AskUserQuestion) to confirm S1, S2, or S3 or lower. On S3 or lower stop with verdict BLOCKED ("redirected to /app-bugfix"). Follow `orchestration.md` sections 1 and 2; print the plan block. Gates (`gates/README.md`): `RM-RELEASE-READY` runs at `lean` and `full` before any deploy; `SL-SECURITY-REVIEW` runs at `lean` and `full` when the fix touches security-relevant code (auth, money, personal data, IPC, updates, crypto, parsing of untrusted input; decide in Phase 4 and ask if unsure). At `solo` print `RM-RELEASE-READY skipped: solo mode` (and the security gate if it would have run). The reviews in Phase 6 are the skill's own steps and run in every mode.

## Phase 2: Record, mitigation, rollback plan

1. Identify the affected release: tag, channel(s), how many users on it if known (user-stated). Compute the next patch version by semantic versioning and confirm it.
2. Offer immediate mitigations that need no new build (feature flag off, config or server-side change, halting a staged rollout, rolling back to the previous version where the channel allows, a status notice). The user chooses; do not execute production changes yourself.
3. Write `docs/release/<patch-version>.md` now, from `release-checklist.md` with these sections: Problem and user impact, Severity, Affected versions and channels, Root cause (empty until Phase 4), Fix, Tests and evidence, Approvals, Backport, **Rollback plan**, Timeline (UTC, user-stated times marked).
4. Draft the rollback plan now and complete it before Phase 7: how to undo this patch on each channel (redeploy the previous artifact, re-point the update feed, halt the rollout, submit the previous build as a newer version), what data written by the patched version the previous one can still read, what cannot be undone, and who decides. Channels that cannot recall installed builds say so and name the fix-forward path.

## Phase 3: Branch from the release

1. Check the working tree (`git status`). If it has uncommitted work, do not touch it: offer a separate worktree for the hotfix (`git worktree add`), or let the user commit or stash first.
2. Branch from the **release tag** (or its release branch if one was cut), never the head of the main branch, which may hold unshipped work. Ask before creating it: `hotfix/<slug>` from `<tag>`; options: create it / use another base / I will do it myself.
3. Confirm the tag builds: run `commands.build` on the branch before changing anything. A tag that does not build is itself the first finding.

## Phase 4: Reproduce, root cause, propose

1. Owner: `escalation-engineer` for a crash, an intermittent defect or an unclear cause; otherwise the builder for the layer and platform from `studio.yaml` (`specialists`) with the language specialist. Brief per `orchestration.md` section 3, with the failing behavior, the tag, the severity and the time pressure; it writes `docs/qa/evidence/hotfix-<slug>/diagnosis.md`.
2. Reproduce on the tagged build and keep the evidence. A defect that cannot be reproduced is BLOCKED unless logs or crash data identify the cause; say what evidence supports the diagnosis.
3. Root cause in one paragraph, from the evidence, not from the fix.
4. Propose the **minimal** change: the files, what changes, what is deliberately left alone, and whether it touches security-relevant code. No refactor, no cleanup, no features, no dependency upgrades. List every file the phase will touch (including `CHANGELOG.md` and the version stamp), say that the fix will be committed locally on the hotfix branch (no push), and ask once for approval before any code changes. The change is approved before it exists.

## Phase 5: Implement and prove

1. Write the regression test first and run it against the **unfixed** tagged code: it must fail, for the reason in the diagnosis. A test never seen failing is not accepted (`standards/testing.md`).
2. Apply the fix. Run the new test (must pass), then `commands.test` (the exact configured command, narrowed to the affected suite only where the runner supports it, then the full suite once). If `commands.test` is unset or no test can cover it, record `Tests: NOT RUN - <reason>`; the QA step below then carries the burden and the verdict cannot be READY without it.
3. For anything a user can see: run and observe the patched build (`orchestration.md` section 10) and keep the one-line `Run result`.
4. Bump the version stamp and add the `CHANGELOG.md` entry (Fixed or Security), read back.

## Phase 6: Independent review and QA (parallel)

Spawn in one message, after the fix is on the branch:

- `code-reviewer`: review the diff for correctness, side effects, data safety, scope creep. Output `docs/qa/evidence/hotfix-<slug>/review.md`. Read-only.
- `qa-lead`: decide the verification scope (smoke on the patched build is the floor; targeted regression of the neighboring areas; a full pass for core-path fixes) and read the evidence. Output `docs/qa/evidence/hotfix-<slug>/qa.md`.
- `release-manager`: timing, rollout shape, channel plan, the rollback plan's completeness and communication needs. Output `docs/qa/evidence/hotfix-<slug>/release.md`.

All three must approve. Then, at `lean` and `full`, spawn in one message `release-manager` for `RM-RELEASE-READY` (context: patch version, channels, the hotfix record, the review and QA verdicts, the rollback plan, the smoke result) and, if the fix touches security-relevant code, `security-lead` for `SL-SECURITY-REVIEW` (context: the diff, the threat model if present, the dependency state); each is told to read its gate file. Record each outcome in the header of `docs/release/<patch-version>.md`. `RM-RELEASE-READY` cannot return GO while the security gate blocks. CONCERNS or a rejection stops the deploy: fix and repeat Phase 5 and 6. Then run `/app-smoke` (or its steps) on the patched build for every platform affected. A smoke FAIL returns to Phase 4. A smoke result of NOT ASSESSED is not a pass: obtain it, or the user makes an explicit, recorded decision to ship unverified, and the verdict stays READY, never SHIPPED-clean (the record says "shipped with unverified QA by the user's decision"). Verify one reviewer claim yourself (re-run the failing test on the unfixed tag).

## Phase 7: Backport and the asks

Order matters; each act has its own unconditional ask in every mode. The words "merge", "tag", "deploy" and "submit" never run on an earlier answer.

1. Complete the rollback plan and read it back. No plan, no asks.
2. **Ask: merge the hotfix to the main branch (and to the release branch if one exists)?** Options: merge / merge only after more review / stop. On yes, merge.
3. **Backport check (never assumed).** Confirm the fix is in the main branch: `git branch --contains <fix commit>` on the main branch, or the same patch present by `git cherry`. If the main branch has diverged and the change does not apply, create the backport as a branch or story and say so. State the result: `Backport: VERIFIED on <branch> at <commit>` or `NOT VERIFIED - <what was not checked>`. An unbackported hotfix returns as a regression in the next release.
4. **Ask: tag `<patch tag>` on the fixed commit?** On yes, tag the fixed build (not the head of the main branch).
5. **Ask per channel: push, then deploy, publish or submit?** One ask per channel; staged or phased rollout recommended where the channel supports it. After a yes, perform the act only if it is non-interactive and credentials are already configured; otherwise print the exact command or steps and wait for the user to confirm it was done. Record the confirmation as user-stated with the time.

## Phase 8: Verify in the field

After the user confirms a deploy: re-run the reproduction against the deployed build (or ask the user to, and record user-stated), and watch the signals named in the rollback plan for the agreed window. If the defect is still present or new errors appear, the hotfix failed: say so, evaluate rollback against the plan, and escalate. Update the bug record. Recommend `/app-incident` for the postmortem and `/app-retro`; recommend `/app-release` or `/app-gate` follow-ups for channels still pending.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Must hold | branch from the tag, minimal fix, regression test seen failing and passing, rollback plan written, all asks | plus independent review and QA scope decision | plus rehearsed or previously proven rollback, postmortem scheduled |
| Gates | solo: none run | lean: `RM-RELEASE-READY`, plus `SL-SECURITY-REVIEW` for security-relevant fixes | full: the same |

Review mode does not remove the Phase 6 approvals: an emergency is where an unreviewed change is most likely to hurt. At review mode `solo` the three approvals run as agents anyway; they are the skill's own steps, not gates. The gates themselves are skipped only at `solo`, with the skip printed; the verdict then cannot be READY for deploy unless the user explicitly accepts shipping without them, recorded in the record with the date.

## Verdicts

First match wins.

1. **BLOCKED:** severity is S3 or lower; a gate returned a blocking word (`NO GO`, `BLOCK`); cannot reproduce and no evidence for the cause; the tag does not build; the regression test was never seen failing; a reviewer, QA or release-manager rejected; a QA step is NOT ASSESSED and unresolved; no rollback plan; the user declined the asks.
2. **NOT ASSESSED:** a required check could not run or has no fresh evidence (smoke NOT ASSESSED and not accepted by the user, a gate agent that did not return, a required gate skipped at `solo` and not accepted by the user, tests unrunnable). The report names each and what clears it.
3. **READY:** the fix is committed on the hotfix branch, tests and review and QA are done, the required gates returned GO or accepted CONCERNS, the backport check has run or is the next ask, the rollback plan is on disk, and nothing has been tagged or deployed yet (or only some acts are done).
4. **SHIPPED:** the user confirmed that the patch is deployed, published or submitted on the channels named in the record, after the Phase 7 asks, backport is VERIFIED, and Phase 8 verification was done or its result is recorded as pending.

A CONCERNS gate result must be accepted by the user, in writing in the record, before READY.

## Report

```
Hotfix: <app> <patch version> (from <tag>)  Severity: <S1|S2>  Rigor: <r>  Review: <mode>
Root cause: <one line>   Fix: <files changed>
Tests: <regression test seen failing: yes/no; N of N pass>   Run result: <line>
Approvals: code-reviewer <v>, qa-lead <v>, release-manager <v>   Smoke: <result>
Backport: <VERIFIED ... | NOT VERIFIED ...>   Rollback plan: <written, read back>
Acts: <merge: asked/answered, tag: ..., channels: ...>
Verdict: <WORD> - <one line why>
Gates: <RM-RELEASE-READY, SL-SECURITY-REVIEW: verdicts> | none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Merging, tagging, deploying, publishing and submitting each need their own unconditional yes in this run, in every mode. Only the user starts the skill.
- Branch from the release tag, never from the head of the main branch. Never push; pushing a branch or tag is part of the ask for the act that needs it. Never disturb the user's uncommitted work.
- Minimal change only. No refactoring, cleanup or dependency changes in a hotfix.
- The regression test must be seen failing on the unfixed code. Do not disable or loosen any test to go green.
- The rollback plan is written and read back before the first ask. Backport is verified or reported NOT VERIFIED, never assumed.
- Never write secrets or credentials into the record. Production changes are the user's actions or ones they explicitly approve act by act.
- Escalate to `technical-director` if the fix will take longer than the user's stated time box or touches architecture.
- Recommend the next skill; never start it.
