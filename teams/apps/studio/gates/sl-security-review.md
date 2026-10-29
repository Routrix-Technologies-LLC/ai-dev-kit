> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# SL-SECURITY-REVIEW: Security Review

Agent: `security-lead`

**Trigger**: After `/app-security-audit`, and at `/app-release` before a release. Always on in lean and full modes whenever `/app-release` runs and whenever the user runs `/app-security-audit`; a hotfix runs it when it touches security-relevant code.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Audit report path (`docs/security/audits/<date>.md`) with SEC-NNN findings and their severities
- Threat model path and the mitigations that should exist
- Diff or change list since the last audit; dependency audit output (advisories, licenses)
- Release version and channels, and the platform list

**Prompt**:
> "Review the security posture for release. Check:
> (1) Are there open CRITICAL or HIGH findings? List them. Any unresolved CRITICAL or HIGH means BLOCK unless the user has recorded an explicit risk acceptance.
> (2) Is each threat-model mitigation implemented and verified, not just planned?
> (3) Were the high-risk areas audited on every shipped platform: authentication and session handling, authorization, input validation, injection, local storage and secrets, transport security, IPC and deep links, update and signing, permissions?
> (4) Do the dependency and build-chain checks show no known exploited vulnerabilities, unreviewed new dependencies or unsigned artifacts?
> (5) Is the audit current, covering the code that is shipping rather than an older version?
> (6) Are logging and telemetry free of secrets and personal data, and is there an incident contact and a way to ship a fix quickly?
> Return CLEAR, CONCERNS [list], or BLOCK [blockers]."

**Verdicts**: CLEAR / CONCERNS / BLOCK

CLEAR means no issues, proceed. CONCERNS means issues that do not block, listed. BLOCK means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `SL-SECURITY-REVIEW: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no audit report for the version being released, or no finding severities. Severity words are CRITICAL, HIGH, MEDIUM, LOW.
