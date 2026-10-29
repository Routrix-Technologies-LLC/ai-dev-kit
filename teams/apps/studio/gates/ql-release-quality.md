> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# QL-RELEASE-QUALITY: Release Quality Bar

Agent: `qa-lead`

**Trigger**: At `/app-release` after the candidate build exists and `/app-smoke` has run. Always on in lean and full modes.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Version and release channel(s)
- Release checklist path; smoke report; test runs on the candidate; the open bug list by severity (S1 to S4) with the bug bar
- Accessibility, performance and i18n reports for this version, if any
- Platform matrix: candidate build identifier per target and what was tested on it
- Known issues list and previous release's escaped defects

**Prompt**:
> "Review the release candidate's quality. Check:
> (1) Are there any open S1 or S2 bugs, or S3 bugs above the bug bar? List each with its record.
> (2) Did the full test suite and the smoke test pass on the exact candidate build for every platform being shipped, not an earlier build?
> (3) Were the critical user paths observed running on each target (clean install, upgrade from the previous version with real data, first run, offline or failure behavior)?
> (4) Do the performance, accessibility and localization results meet their budgets or targets, with any shortfall explicitly accepted by the user?
> (5) Are known issues documented in the release notes, and is every regression since the last release explained?
> (6) Is there evidence the rollback path works for this version (data compatibility, downgrade or rollout halt)?
> Return READY, CONCERNS [list], or NOT READY [blockers]."

**Verdicts**: READY / CONCERNS / NOT READY

READY means no issues, proceed. CONCERNS means issues that do not block, listed. NOT READY means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `QL-RELEASE-QUALITY: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no smoke or test results on the candidate, or no bug list.
