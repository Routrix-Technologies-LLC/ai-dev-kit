# Stack Reference: [Product name]

<!--
WRITTEN BY: technical-director with the platform lead and language specialists; compliance-specialist checks licenses. Skill: /app-stack (create, refresh, evaluate), /app-adopt (first version from the repo), /app-upgrade (update after a bump).
LIVES AT: docs/stack-reference.md (override: paths.stack_reference).
RIGOR: minimal = a short table of runtimes, frameworks and key libraries with versions from the lock files and the date checked.
       standard = sections 1 to 6 and 7; every pinned version traced to a lock file or an official source; known API changes and deprecations for the major dependencies.
       full = standard plus support and end-of-life dates, license and advisory status per dependency, and a refresh schedule.
Purpose: models and people both carry stale beliefs about frameworks. This file is the corrective. Agents read it BEFORE writing code against any listed dependency, and trust it over memory.
Every version is copied from a lock file, manifest or official release page, never from memory. Each row carries the date checked and the source. If you cannot verify a row, write UNVERIFIED rather than a plausible number.
-->

**Last full refresh:** [YYYY-MM-DD]   **Refreshed by:** [agent or person]   **Next refresh due:** [date or trigger, e.g. before each release or at each major upgrade]

## 1. Toolchain and runtimes
<!-- Languages, compilers, runtimes, SDKs, build tools, package managers: the exact versions the build uses (from toolchain files, CI config, lock files), and the minimum version the app supports where that differs. -->
| Component | Pinned version | Where pinned (file) | Supported until / support status | Checked on | Source |
|---|---|---|---|---|---|

## 2. Frameworks and key libraries
<!-- Every dependency that shapes the architecture or has a large API surface: UI, state, data access, networking, auth, serialization, testing, logging. Direct dependencies only unless a transitive one matters. Include license and the latest available version so drift is visible. -->
| Dependency | Pinned | Latest known (date) | License | Role | Where pinned | Checked on | Source |
|---|---|---|---|---|---|---|---|

## 3. Platform targets
<!-- Oldest and newest OS, browser, device or runtime targets (from studio.yaml min_targets), plus the platform SDK version used to build and the policy for raising the floor. Store or platform requirements with deadlines (target SDK level, notarization, signing). -->
| Platform | Minimum | Build SDK | Policy and deadlines | Checked on | Source |
|---|---|---|---|---|---|

## 4. Known API changes newer than training data
<!-- The heart of this file. For each major dependency or platform, list changes an agent is likely to get wrong: renamed or removed APIs, changed defaults, new recommended replacements, behavior changes, new required configuration. Format: "Do not write X (old). Write Y (current, since version N). Source." Fill this from official changelogs and migration guides read during /app-stack, not from memory. -->
| Area | Old pattern (do not write) | Current pattern (write this) | Since version | Source and date read |
|---|---|---|---|---|

## 5. Deprecations and things to avoid
<!-- APIs deprecated in the pinned versions with their replacement and removal version; packages abandoned or archived; patterns the project has banned (with ADR link); known vulnerable versions. -->
| Item | Status | Replacement | Removal or end-of-life | Source |
|---|---|---|---|---|

## 6. Upgrade notes
<!-- What the next upgrades involve: for each dependency behind its latest major, the breaking changes to expect, the order to upgrade in (one major at a time), blockers (a dependency that does not yet support the new version), and the link to a dependency-upgrade-plan if one exists. -->
| Dependency | Current | Next target | Breaking changes to expect | Blockers | Plan |
|---|---|---|---|---|---|

## 7. How to verify this file
<!-- The commands that regenerate or check versions (for example the package manager's list, outdated and audit commands from studio.yaml or the toolchain), and the rule: when a lock file changes, this file changes in the same commit or the same story. -->
- [Command and what it checks]
