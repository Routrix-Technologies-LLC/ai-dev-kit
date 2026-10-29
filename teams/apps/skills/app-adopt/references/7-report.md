# app-adopt, Phase 7: the adoption report and gap analysis

Part of `/app-adopt`. Main session writes `docs/qa/adoption-report.md` (or, if that file exists, `docs/qa/adoption-report-<date>.md`; never overwrite). It is a new file in a studio folder, covered by the Phase 2 approval. Every number carries its denominator. Every step that did not run is listed under "Not run" with its reason.

## Report structure

```markdown
# Adoption report: <app name>

Date: <date>   Rigor: <rigor>   Review: <mode>   Stage: <stage> (confirmed by the user | not confirmed)
Verdict: <WORD> - <reason>

## 1. What this app is
Platforms, languages, frameworks, hosting, size ("<n> source files of <n> tracked"). Each fact with its evidence file.

## 2. Commands
Table from commands.md: key, command, status, evidence. Then: absent keys, conflicts between README and CI, commands CI runs that have no key.

## 3. Where things live (paths mapping)
Table: studio document type, where it lives now, action (mapped | absent | created by adoption). "Nothing was moved."

## 4. Stage and evidence
The evidence table from Phase 5, the pick, the runner-up, what the user confirmed. Disagreements with a recorded stage.

## 5. Documented from code
What was written, how many claims, how many INTENT UNKNOWN, spot-check results. Drift list summary if an architecture document already existed.

## 6. Gaps
Findings by area, each: ID (GAP-NN), what, evidence (file and line, never a secret's value), severity (CRITICAL, HIGH, MEDIUM, LOW per standards/severity.md), recommended skill.

## 7. Audit lens preview
One line per lens (see below): quick signal found, or NOT CHECKED, with the skill that does it properly.

## 8. Recommended next skills
Ordered list with a reason each.

## 9. Not run
Every step skipped or incomplete, and why.

## 10. Open questions for the user
Things the code cannot answer: intent, users, deadlines, planned platforms.
```

## Gap detection (quick signals only, no deep analysis)

Detect these from files and the Phase 3 results. Each is a cheap existence or consistency check. Do not read source files in bulk here.

| Area | Signal | Typical finding |
|---|---|---|
| Build and CI | no CI config; CI and README disagree; no lock file; toolchain not pinned | no reproducible build |
| Tests | no test files; tests ran zero cases; tests failing; no coverage of the main path (listing of test folders versus source folders) | untested app |
| Docs | no README, no setup steps, no architecture doc, no changelog on a released app | undocumented |
| Dependencies | EOL runtime or framework in toolchain files; very old lock file; several majors behind where visible from the lock | upgrade debt |
| Security | secrets committed (file and line only), permissive config files, no dependency audit in CI | needs `/app-security-audit` |
| Privacy | analytics or crash SDKs in dependencies, accounts or personal data models | needs `/app-privacy-review` |
| Release | no version tags on a released app, no release docs, no rollback note | release process unwritten |
| Operations | deployed app without runbooks, logging or monitoring libraries absent | needs `/app-observability` |
| Accessibility and i18n | UI code with hardcoded strings (sample a UI folder by count of obvious literals, say it is a sample), no localization resources | readiness unknown |
| Studio files | no `.gitignore` entry for `.studio/` (declined), `commands:` keys empty | state it |

Severity follows `standards/severity.md`. A signal that could not be checked is `NOT CHECKED`, never "no problem found".

## Audit lens preview (rigor full; one line each at standard; omit at minimal)

For each lens give a signal and the skill to run: architecture (module cycles, size outliers) with `/app-team-audit`; code quality; security with `/app-security-audit`; performance with `/app-perf`; accessibility with `/app-a11y-audit`; UX with `/app-ux-review`; tests and CI with `/app-test-setup`; dependencies and licenses with `/app-upgrade`; docs; operations with `/app-observability`.

## Recommended next skills (ranking rules)

1. `/app-team-audit` first for most adopted apps: it turns the gap list into a verified, prioritized backlog.
2. If `build` or `test` is unverified or absent: `/app-test-setup` before anything else, because every later skill depends on working commands.
3. If a secret was found committed: tell the user now (file and line), recommend `/app-security-audit`, and say rotating the credential is a human action.
4. If an EOL runtime or framework was found: `/app-upgrade`.
5. If the app is live and has no runbooks or monitoring: `/app-observability`.
6. Decisions visible in code with no record: `/app-adr` in retrofit mode, a few at a time.
7. Features with no spec: `/app-spec` in retrofit mode for the ones about to change.
8. If rigor is `standard` or `full` and the stage is `build`: `/app-plan` after the audit, to turn accepted findings and the user's backlog into stories.
9. Always mention `/app-help` as the way back in.

Recommend; never start. The final hand-off is exactly: "Type `<skill>` to begin."

## Suggested commit

State the paths adoption created or changed and a Conventional Commits subject, for example `docs: adopt app into studio (studio.yaml, architecture, stack reference)`. List files by path. Do not stage or commit.

## Check that the report happened

Read the file back: all ten sections present, the Verdict line matches the closing block, no section left as a template placeholder, no em or en dashes, no secret values. If the report could not be written, the verdict is BLOCKED.
