<!--
Template: dependency-upgrade-plan. Written by: modernization-engineer with the language specialist, platform lead, compliance-specialist and security-engineer. Skill: /app-upgrade.
Lives at: planning/upgrades/<id>.md (override: paths.upgrades; id is a date and short slug, for example 2026-10-react-major).
Rigor: minimal = versions, steps, rollback. standard = adds changelog notes per major, breaking changes, license and advisory check, per-platform verification. full = adds codemod rehearsal on a branch, staged rollout, and a compatibility matrix.
Delete this comment when the plan is created. Versions below are placeholders: verify every one from the official registry or release page.
-->

# Upgrade plan: [dependency, framework, runtime or SDK]

> **Status**: [Planned | In progress | UPGRADED | PARTIAL | BLOCKED | NOT ASSESSED]
> **Author**: [agent]   **Date**: [YYYY-MM-DD]
> **Why now**: [security advisory, end of support, needed feature, store requirement, routine]

## Versions

| Item | Current | Target | Source of truth checked |
|---|---|---|---|
| [package or SDK] | [x.y.z from the lock file] | [x.y.z from the official registry] | [URL, date read] |

## Majors crossed

Upgrade one major at a time. A skipped major is a risk, not a shortcut.

| Step | From | To | Changelog read | Migration guide read | Breaking changes found |
|---|---|---|---|---|---|
| 1 | [M] | [M+1] | [yes, link] | [yes, link, or none exists] | [count] |

### Notes per major

**[M to M+1]**
- Changelog highlights relevant to this app: [...]
- Migration guide key points: [...]
- Deprecations to remove now: [...]

## Breaking changes and impact

| Change | Where we use it (grep result with count) | Fix | Codemod available |
|---|---|---|---|
| [API removed, behavior changed, config renamed, minimum platform raised] | [N call sites in M files] | [what to do] | [tool and command, or manual] |

Also check: new minimum OS, runtime or browser version (does it break `min_targets` in studio.yaml?), peer and transitive dependency conflicts, build tool and CI image changes, changed defaults (security, TLS, serialization, time zones, text encoding), size and startup impact.

## License and advisory check

| Check | Result | Evidence |
|---|---|---|
| License of the target version (unchanged? new transitive licenses?) | [...] | [license-inventory.md row or source] |
| Known advisories on current version | [list or none found, in what database] | [...] |
| Known advisories on target version | [...] | [...] |
| Maintenance health (last release, open critical issues, bus factor) | [...] | [...] |

## Plan

1. Branch and baseline: record current build, test results and size/performance numbers.
2. [Step per major: bump, fix, run tests, commit separately so each is revertable.]
3. Run codemods on a clean tree; review the diff, never accept blindly.
4. Update lock files, stack reference (`docs/stack-reference.md`) and any ADR that named the version.
5. Re-run license inventory and security scan.

## Per-platform verification

| Platform | Build | Tests | Launched and observed | Notes |
|---|---|---|---|---|
| [web / windows / macos / linux / ios / android / backend / cli] | [pass/fail] | [n of n] | [Run result line] | [...] |

Include a clean install and an upgrade-in-place from the previous app version when the dependency touches storage, serialization or the installer.

## Rollback

- Revert path: [revert commits, restore lock file, pin previous version]
- Data or format changes that cannot be reverted: [none, or what and the plan]
- Trigger for rollback: [observable condition]

## Outcome

[Filled at the end: what shipped, what was deferred, new tech-debt rows (TD-NNN), measured size/perf change.]
