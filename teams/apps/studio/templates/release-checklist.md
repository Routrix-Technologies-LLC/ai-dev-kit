<!--
Template: release-checklist. Written by: release-manager with qa-lead, security-lead, and per channel desktop-packaging-engineer, app-store-specialist or infrastructure-engineer. Skill: /app-release (also /app-hotfix).
Lives at: docs/release/<version>.md (override: paths.release).
Rigor: minimal = codebase health, build verification, one channel section, rollback, go/no-go. standard = all quality gates, security, accessibility, localization, legal, sign-offs. full = adds staged rollout metrics and thresholds, post-release watch, and a communications plan.
Delete sections for channels the app does not use and say so in "Channels". Delete this comment when the checklist is created.
Every count is written with its denominator ("0 TODOs in 214 files"). A check that did not run is NOT ASSESSED, never a pass.
-->

# Release checklist: [app name] [version]

> **Target date**: [YYYY-MM-DD]   **Release type**: [major | minor | patch | hotfix]
> **Release manager**: [agent]   **Branch / tag**: [branch, planned tag]
> **Channels**: [web deploy | desktop installer and updater | package manager | Apple App Store | Google Play | Microsoft Store | package registry | none]
> **Go/no-go**: [GO | CONCERNS | NOT ASSESSED | NO GO], see the last section

## 1. Codebase health

| Check | Result | Denominator |
|---|---|---|
| Open S1 / S2 bugs | [n] | [of n open bugs] |
| Open TODO / FIXME / HACK in shipped code | [n] | [in n files scanned] |
| Planned stories Complete | [n] | [of n planned] |
| Tests passing | [n] | [of n, per platform] |
| Lint and type check clean | [yes / n issues] | [n files] |
| Debug code, feature flags and test endpoints off in release config | [verified how] | |
| Tech-debt rows (TD-NNN) accepted for this release | [list] | |
| Version number bumped everywhere it appears | [files] | |
| CHANGELOG.md entry written (Keep a Changelog, semantic version) | [yes/no] | |

## 2. Build verification (per platform)

| Platform | Release build from clean checkout | Reproducible command | Artifact (name, size, hash) | Launched and observed | Smoke result |
|---|---|---|---|---|---|
| [web / windows / macos / linux / ios / android / backend / cli / extension / library] | [pass/fail] | [from studio.yaml] | | [Run result line] | [PASS / PASS WITH WARNINGS / FAIL / NOT ASSESSED] |

Also: upgrade-in-place from the previous release works with real existing data; clean install works; uninstall leaves no damage.

## 3. Quality gates

| Gate | Verdict | Report |
|---|---|---|
| QL-RELEASE-QUALITY (READY / CONCERNS / NOT READY / NOT ASSESSED) | | `docs/qa/...` |
| RM-RELEASE-READY (GO / CONCERNS / NO GO / NOT ASSESSED) | | |
| Test plan exit criteria (`docs/qa/test-plans/...`) | [met / not met / NOT ASSESSED] | |
| Gates skipped by review mode | [list as `<GATE-ID> skipped: <mode> mode`] | |
| Performance against `perf-budget.md` | [WITHIN BUDGET / OVER BUDGET / NO BUDGET / NOT ASSESSED] | `docs/qa/perf-<date>.md` |
| Crash and error rate in the last build (if already in testers' hands) | | |

## 4. Security and privacy

| Check | Verdict | Report |
|---|---|---|
| SL-SECURITY-REVIEW / security audit | [CLEAR / CONCERNS / BLOCK / NOT ASSESSED] | `docs/security/audits/...` |
| SL-PRIVACY review; store privacy declarations match the data actually collected | | `docs/security/privacy.md` |
| Dependency advisories checked on the shipped lock file | [n advisories in n dependencies] | |
| Secrets scan of the repo and built artifacts | [n findings in n files] | |
| Signing keys and certificates valid, not expiring within [90] days | | |

## 5. Accessibility

| Check | Verdict | Report |
|---|---|---|
| Accessibility audit (WCAG 2.2 AA and platform APIs) | [CONFORMS / PARTIAL / FAILS / NOT ASSESSED] | `docs/qa/a11y-<date>.md` |

## 6. Localization

| Check | Verdict | Notes |
|---|---|---|
| Locales shipping: [list]; locale QA done for each | [READY / GAPS / NOT READY / NOT ASSESSED] | |

## 7. Channels

Complete only the sections for channels in use.

### 7a. Web deploy
- [ ] Build artifact deployed to staging and smoke-tested; migrations applied (rehearsed on a copy)
- [ ] Cache and CDN invalidation plan; asset hashes; service worker update behavior
- [ ] Environment config and secrets present in production (names only listed here)
- [ ] Health checks, monitoring and alerts watching the deploy
- [ ] Backward compatibility with clients that still hold the old version

### 7b. Desktop installer and updater
- [ ] Installer built and signed (code signing; macOS notarization; Linux package signatures); signature verified
- [ ] Install, upgrade, repair and uninstall tested on clean machines for each OS
- [ ] Auto-update feed published to a test channel first; update, downgrade-block and failed-update recovery tested
- [ ] SmartScreen or Gatekeeper behavior checked on a machine that has never seen the app
- [ ] Release notes and checksums published

### 7c. Package managers (system or language)
- [ ] Manifest/formula/recipe updated with the new version and hash
- [ ] Install from the package manager on a clean machine tested
- [ ] Maintainer review or PR status: [link]

### 7d. Apple App Store
- [ ] Build number incremented; archive signed with distribution profile; uploaded to App Store Connect
- [ ] TestFlight run on real devices; metadata, screenshots per device class, App Privacy details, age rating, export compliance complete (`docs/release/store/apple.md`)
- [ ] App Review notes and test account (no real credentials in this file)
- [ ] Phased release setting chosen: [on/off]

### 7e. Google Play
- [ ] Signed app bundle with the correct version code; Play App Signing configured
- [ ] Internal and closed testing track run; data safety form, content rating, target API level, permissions declarations complete (`docs/release/store/google-play.md`)
- [ ] Staged rollout percentage plan: [e.g. 5, 20, 50, 100]

### 7f. Microsoft Store
- [ ] Package built and signed; submission properties, age rating and screenshots complete (`docs/release/store/microsoft.md`)
- [ ] Certification requirements checked; flight ring used first: [yes/no]

### 7g. Package registries (library or CLI published to a registry)
- [ ] Version, license, README, changelog and metadata correct; package contents inspected (no secrets, no test fixtures)
- [ ] Dry-run publish output reviewed; provenance or signing enabled where supported
- [ ] Deprecation notes for removed APIs; semantic version reflects breaking changes
- [ ] Publish is irreversible or hard to retract: ask the user explicitly

## 8. Legal and licenses

- [ ] `license-inventory.md` current for this version; third-party notices included in the artifact
- [ ] Terms, privacy policy and EULA links valid; required attributions shown
- [ ] Export, encryption and regional regulatory declarations done where required
- [ ] Trademarks and third-party assets cleared

## 9. Rollout and rollback plan

| Item | Plan |
|---|---|
| Rollout order and percentages | [for example internal, 5 percent, 25 percent, 100 percent, with hold times] |
| Metrics watched and thresholds that pause the rollout | [crash-free rate, error rate, latency, support volume] |
| Who watches and for how long | [owner, window] |
| Rollback method per channel | [redeploy previous artifact, halt staged rollout, ship a hotfix build, update-feed pull; note what cannot be recalled such as store binaries and registry versions] |
| Data and schema rollback | [reversible? expand/contract state] |
| Communication | [release notes, status page, support notes] |

## 10. Go / no-go

Rules, first match wins (the same as /app-release):
1. NO GO if any S1 or S2 is open, an open CRITICAL or HIGH security finding, any gate returned a blocking verdict (BLOCK, NOT READY, NO GO), any OVER BUDGET or FAILS result stands unaccepted, any release build, test run or required signature check failed, or the rollback plan is missing.
2. CONCERNS if all of the above is clear but a gate returned CONCERNS, a recommended item is missing, or a known issue ships by decision. Each concern is accepted by the user in writing under "Accepted risks".
3. NOT ASSESSED if any required check above was not run or has no fresh evidence (including zero findings from zero files examined, or a gate skipped by mode: a release cannot be GO on gate evidence it did not collect).
4. GO otherwise.

**Verdict**: [GO | CONCERNS | NOT ASSESSED | NO GO]
**Why**: [one line naming the first rule that matched]

Deploying, tagging, publishing and submitting happen only after the user says yes.

## Accepted risks

| Concern | Accepted by | Date |
|---|---|---|

## 11. Sign-offs

| Role | Name | Date | Verdict |
|---|---|---|---|
| release-manager | | | |
| qa-lead | | | |
| security-lead | | | |
| product-manager (acceptance) | | | |
| User (final go) | | | |
