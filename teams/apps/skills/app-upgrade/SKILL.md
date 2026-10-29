---
name: app-upgrade
description: "Plan and execute a dependency, framework, runtime or SDK upgrade one major version at a time, reading the changelog and migration guide for every major crossed, checking licenses and advisories, keeping the build green between hops, and verifying on every target platform. Use when the user says upgrade, bump, update to the latest, migrate to a new major version, a runtime or SDK is going out of support, or a security advisory requires a newer version."
argument-hint: "[package, framework, runtime or SDK] [--to <version>] [--review solo|lean|full]"
user-invocable: true
---

# App Upgrade

An upgrade is a sequence of small, reversible hops, each one major version, each ending with a green build and passing tests. The skill reads what changed (changelog and migration guide for every major crossed), checks what the new version brings in (licenses, advisories), plans the hops, executes them, and verifies the result on every target the app supports. It does not guess API changes from memory: the guides are read, and anything it cannot read is named.

Writes: `planning/upgrades/<id>.md` (template `dependency-upgrade-plan.md`), code and lockfile changes, evidence in `docs/qa/evidence/upgrade-<id>/`, updated `docs/stack-reference.md`, tech-debt rows for deferred work.
Next: `/app-smoke` (final confirmation), `/app-code-review` (the diff), `/app-adr` (if the upgrade changes an architectural decision), `/app-release`.

## When to use and when not to

Use it for any change of a version that crosses a major boundary, any runtime or SDK or toolchain move, and any batch of minor and patch bumps large enough to need a plan. A single patch bump with a green build and no advisory does not need this skill; do it as an ordinary change. Not for these:

- Choosing between libraries or adopting a new one: `/app-stack`.
- A security finding in your own code: `/app-bugfix` or `/app-security-audit`.
- Replacing a framework wholesale (a rewrite, a strangler migration): plan with `/app-stack` and `/app-adr`, then use this skill per stage.
- Changing stored data formats: `/app-data-migration`.

## Inputs

- Required: `studio.yaml` with `commands.build` and `commands.test`. If either is empty, offer `/app-test-setup` and stop; an upgrade without a way to prove the build is not attempted.
- Required: the current version of the target, read from the manifest and lockfile, never from memory.
- Optional: `docs/stack-reference.md` (pinned versions and known API changes), existing upgrade plans in `planning/upgrades/`, CI configuration.
- Network access to the official changelog, migration guide and advisory sources. Reading these is mandatory (Phase 2). If an official source cannot be reached for a hop, that hop is NOT ASSESSED on its research, and the plan says so.

## Phase 1: Scope and baseline

Who: the main session, plus `modernization-engineer` for an unfamiliar codebase.

1. Resolve the target: package, framework, runtime, SDK, toolchain or platform target (for example a minimum OS or API level). Read the current version from the manifest and lockfile. Determine the requested version: `--to`, or the latest stable the official source lists (never a pre-release unless the user asks).
2. Build the inventory: what else moves with it (peer dependencies, build plugins, the language version, the test runner, type definitions, native toolchains, store minimum-SDK rules). List each with current and required version.
3. Compute the hops: every major version between current and target is one hop, unless the maintainers' own guide documents a supported direct path (cite it in the plan); runtimes and platform targets with long-term-support lines follow the vendor's supported upgrade path. Example shape: 3.x to 4, 4 to 5, 5 to 6. Minor and patch bumps inside the current major are folded into the first hop, as a separate preliminary hop when risky.
4. Baseline: run `commands.build` and `commands.test` before touching anything (heavy runs one at a time; if the user needs the machine back, stop and report what is still to run), and `commands.lint` if set. Record the result and counts (tests run, passed, skipped). If the baseline is red, stop: the verdict is BLOCKED, naming what failed. An upgrade never starts from red, because failures cannot then be attributed. Offer `/app-bugfix` or `/app-test-setup`.
5. Create a working branch only if the user asked for one; otherwise ask once how the hops should be committed (one commit per green hop, one branch, or leave the tree uncommitted). Do not commit, push or merge without that answer.

Check: the inventory and hop list are written into the draft plan header; the baseline result line exists with counts.

## Phase 2: Research every major crossed

Who: the platform and language specialists from `studio.yaml` `specialists:` (for example `typescript-specialist`, `rust-specialist`, `dotnet-specialist`, `jvm-specialist`, `python-specialist`, `go-specialist`, `cpp-specialist`) plus the platform engineer for the surface touched (`web-framework-specialist`, `windows-desktop-engineer`, `macos-engineer`, `ios-engineer`, `android-engineer`, `cross-platform-mobile-engineer`, `hybrid-desktop-engineer`, `backend-engineer`, and so on), in parallel, one brief per hop group, each writing its own file `planning/upgrades/<id>-research-<n>.md`.

Each agent reads, from the official source (project documentation, release notes, migration guide, repository changelog), for every major version in its hop:

- the changelog and release notes between the two versions;
- the official migration or upgrade guide, if one exists (say "none published" if not);
- removed and renamed APIs, changed defaults, changed minimum requirements (language version, OS, browser, API level), changed build or config format, codemods or automated migration tools the maintainers provide;
- the support status of the version being left (end of life dates) and of the version being reached.

Each finding carries the source URL and the version it applies to. A claim without a source is marked UNVERIFIED. Training-data memory of an API is not a source; the agent must search or fetch. When the pinned version is newer than what the agent knows, trust the fetched text over memory.

Check: every hop has a research file with at least one source URL per breaking change, or an explicit "no breaking changes listed in <URL>". A hop whose sources could not be fetched is recorded as `RESEARCH NOT ASSESSED` and carried to the verdict.

## Phase 3: Licenses and advisories

Who: `compliance-specialist` and `security-engineer` in parallel, each writing `planning/upgrades/<id>-license.md` and `planning/upgrades/<id>-security.md`.

- `compliance-specialist`: the license of the target version and of every new or changed transitive dependency it pulls in, compared with the app's license policy and distribution model (a change from a permissive to a copyleft or source-available license, a new notice obligation, a license that forbids the app's use). Output: a table of package, old license, new license, verdict (OK, NEEDS NOTICE, CONFLICT). SBOM or notices file updated if the app keeps one.
- `security-engineer`: known advisories for the current and target versions, using the ecosystem's read-only audit tooling (the package manager's audit command, never an `audit fix` or anything that rewrites a manifest, an advisory database query, or a scanner such as an OSV-based one) and the official advisory pages. Output: advisories fixed by the upgrade, advisories that remain or are introduced, whether the upgrade is urgent because of them. If no audit tool is available for the ecosystem, say `NOT ASSESSED - no advisory source for <ecosystem>` rather than reporting zero advisories. A count is always given with its denominator ("0 advisories across 214 packages").

A CONFLICT license or an introduced CRITICAL or HIGH advisory pauses the plan: present options to the user (choose another version, replace the package, accept with a recorded reason).

## Phase 4: Plan and approval

Who: the main session writes `planning/upgrades/<id>.md` from `templates/dependency-upgrade-plan.md` (the id is the date plus a short slug). It contains: scope and reason, inventory, the hop table, per hop the breaking changes with sources, the code areas affected (use Grep to find actual usages of every removed or changed API; count them), the verification matrix, the rollback for each hop, risks, license and advisory results, and the effort estimate.

The verification matrix (used in Phase 6) is derived from `studio.yaml`:

| Target | What proves it |
|---|---|
| web | build, tests, headless browser load of the critical routes in each supported browser family, bundle size compared with before |
| windows, macos, linux | build and test on that OS, launch and window capture, installer or package builds if the app ships one |
| ios, android | simulator and emulator launch at the minimum and the newest supported OS version, store minimum-SDK rules met |
| backend | build, tests, start against a throwaway database with migrations applied, health check and critical requests |
| cli | build, tests, run `--help` and one real command on a fixture on each OS |
| library | build, tests, public API diff against the previous release |
| extension | build, tests, load the unpacked extension in each target browser, manifest and permission diff against the previous version |

Ask once with AskUserQuestion: approve the plan, the hop order, the commit policy, and the list of source and config files the hops will touch (orchestration.md section 3). `(Recommended)` goes on the smallest-hop order. Checkpoint to `.studio/state.md`.

Check: the plan file exists, every hop has sources, a rollback and an affected-code count.

## Phase 5: Execute, one hop at a time

Who: `modernization-engineer` leads, with the language specialist and platform engineer for the code they own, in sequence per hop (parallel agents would conflict in the same files). `test-engineer` fixes or updates tests broken by the change, never by deleting coverage.

For each hop, in order:

1. Apply the version change in the manifest and lockfile only for this hop's packages. Run the maintainers' codemod or migration tool if the guide provides one.
2. Apply the code changes the guide requires. Fix deprecations that this hop removes. Do not refactor beyond what the hop needs; list wanted cleanups as tech debt.
3. Run `commands.build`, then `commands.test`, then `commands.lint` when set. The main session reads the output itself. Compare with the baseline: same or higher test count, no new skips, no new warnings of the kind that become errors in the next hop.
4. Green: record the hop (commands, counts, files changed) in the plan, commit if the commit policy says so, then start the next hop.
5. Red: the engineer gets two focused attempts, consulting the migration guide and the maintainers' issue tracker. Still red: stop. Do not skip ahead to the next hop, do not disable tests, do not pin around the failure silently. Present options (investigate further, roll this hop back and stay on the previous major, defer the hop). Verdict inputs: PARTIAL if earlier hops are green and kept, BLOCKED if the first hop failed.

Never mix a hop with unrelated changes. Never edit a lockfile by hand when the package manager can regenerate it.

Check: after each hop, the plan has a result row with the exact commands and counts. A hop without a row did not happen.

## Phase 6: Verify on every target

Who: `test-automation-engineer` and `test-engineer`, with the platform lead's specialists for target-specific problems.

Run the verification matrix from Phase 4 for every platform in `studio.yaml` `platforms` and every oldest and newest target in `stack.min_targets`. Capture evidence without stealing focus or injecting input (orchestration.md section 10) into `docs/qa/evidence/upgrade-<id>/`; emulators, simulators and full suites run through the lock helper as in Phase 1. Compare with the baseline: startup time, bundle or binary size, memory at idle, and any budget in `perf-budget.md`; a regression beyond budget is a finding.

A target that cannot be run on this machine (an iOS simulator on a non-Apple host, a Linux desktop on a Windows host, a device the app supports but is not available) is recorded as `NOT VERIFIED - <why>` and makes the verdict NOT ASSESSED for that target. It is never counted as passed. Offer the CI route (`/app-test-setup`) or the user's manual check.

Also check: every API listed as removed in the guides no longer appears (Grep, with counts), deprecation warnings did not increase, and the lockfile has no duplicate majors of the upgraded package unless the plan accepts them.

## Phase 7: Close out

Who: the main session.

1. Update `docs/stack-reference.md` with the new pinned versions and the API changes learned (this is what stops agents using the old API later). Update the SBOM or notices file if the app keeps one.
2. Register deferred work (cleanups, remaining deprecations, a hop postponed) in `planning/tech-debt.md` as rows in the register's nine columns with Source `upgrade <id>` (see `/app-tech-debt`).
3. Fill the plan's outcome section: hops done, hops deferred, the evidence paths, the rollback note for what was shipped.
4. Recommend `/app-code-review` on the whole diff and `/app-smoke`. If the upgrade changed an architectural decision, recommend `/app-adr`.

## Rigor and review mode

Rigor changes how much is written, never what must work.

| | minimal | standard | full |
|---|---|---|---|
| Plan | short (hops, sources, rollback) | full template | full template plus estimate and risk notes |
| Research files | one combined file | one per hop group | one per hop, second-source check for each breaking change |
| Verification | build, tests, launch on this machine's target | every target in `platforms` | every target at the oldest and newest supported version |
| Licenses and advisories | always run | always run | always run, with SBOM update |

Gates: none are defined for this skill. At `full`, when the upgrade replaces the app's framework or runtime major, recommend `TD-STACK` through `/app-stack` before executing. Print `Gates: none run (<mode>)` otherwise.

## Verdicts

First match wins. NOT ASSESSED ranks below the failures and above the pass.

1. BLOCKED: the baseline was red, a license CONFLICT or introduced CRITICAL advisory was not resolved, or the first hop could not be made green.
2. PARTIAL: at least one hop is done and kept, and the target version was not reached (a hop failed, was deferred or was declined).
3. NOT ASSESSED: the target version was reached, but a hop's research could not be sourced, an advisory source or license check was unavailable, a platform target could not be verified, or the test count dropped without an explanation. Name each.
4. UPGRADED: every hop is green, every target in the matrix was verified with evidence, licenses and advisories were checked with denominators, and `docs/stack-reference.md` is updated.

## Report

```
Upgrade: <package or platform>  <from> -> <to>  (<n> hops: <list>)
Baseline: build <ok/fail>, tests <passed>/<run> (<skipped> skipped)
Per hop: <hop> - build/tests/lint <results>, files changed <n>
Licenses: <n> changed, <n> conflicts   Advisories: <fixed>/<remaining>/<introduced> across <n> packages
Targets: <target>: VERIFIED <evidence path> | NOT VERIFIED <why>
Deferred: <items and where recorded>
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never start from a red build. Never jump two majors at once. Never leave a hop red and move on.
- Never rely on memory for an API change: read and cite the changelog and migration guide for every major crossed.
- Never delete, skip or loosen a test to get green. A lower test count needs a named reason.
- Never report zero advisories or zero license issues without the source and the denominator.
- A target the skill could not run is NOT VERIFIED and keeps the verdict from UPGRADED.
- Never commit, push, tag or merge without the commit policy the user approved in Phase 4. Never hand-edit lockfiles.
- Never bundle unrelated refactors into a hop.
- Never start the next skill automatically.
