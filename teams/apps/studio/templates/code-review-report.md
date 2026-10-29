<!--
Template: code-review-report. Written by: code-reviewer, with language and platform specialists and security-engineer for sensitive code. Skill: /app-code-review.
Lives at: docs/qa/reviews/<date>-<scope>.md.
Rigor: minimal = scope, verdict, findings. standard = adds failure scenario and fix per finding, VERIFIED or UNVERIFIED flags, not-covered list. full = adds per-lens sections, metrics with denominators, and re-review log.
Delete this comment when the report is created.
-->

# Code review: [scope]

> **Date**: [YYYY-MM-DD]   **Reviewer(s)**: [agents]
> **Scope**: [diff range, branch, PR, paths; commit hashes]
> **Files reviewed**: [n of n changed files] (lines: [n])
> **Verdict**: [APPROVED | APPROVED WITH SUGGESTIONS | CHANGES REQUIRED | NOT ASSESSED]

Verdict rules, first match wins: CHANGES REQUIRED if any CRITICAL or HIGH finding is VERIFIED, or a build or lint failure in the reviewed files; NOT ASSESSED if the scope could not be read or was only partly read, a required lens did not return, or a CRITICAL or HIGH finding is still UNVERIFIED (name what would settle it); APPROVED WITH SUGGESTIONS if only MEDIUM or LOW findings remain; otherwise APPROVED (every planned lens returned).

## Summary

[Three to five sentences: what the change does, overall quality, the one thing that matters most.]

## Findings

| # | Severity | File:line | Failure scenario | Suggested fix | Status |
|---|---|---|---|---|---|
| 1 | [CRITICAL / HIGH / MEDIUM / LOW] | `[path:line]` | [Concrete input or sequence that makes it fail, and what the user or system sees] | [specific change] | [VERIFIED / UNVERIFIED] |

Severity: CRITICAL (data loss, security hole, crash on a main path), HIGH (wrong behavior on a realistic path, broken contract), MEDIUM (edge-case bug, maintainability risk likely to cause bugs), LOW (style, naming, minor clarity). VERIFIED means the reviewer re-read the code path or reproduced it; UNVERIFIED means plausible but unconfirmed. Do not report a finding without a failure scenario. Taste without a scenario is a LOW suggestion at most.

## Checks run

| Check | Result | Denominator |
|---|---|---|
| Build | [pass/fail] | [targets] |
| Tests | [n passed of n] | [...] |
| Lint / type check | [n issues] | [files] |
| Spec and ADR conformance | [...] | [REQ IDs / ADRs] |
| Tests added for new behavior | [yes/no] | [...] |

## Positives

[What was done well and should be repeated. Brief.]

## Not covered

What this review did not examine, and why:
- [for example: code outside the diff that calls the changed function]
- [platforms that could not be built here]
- [runtime behavior not exercised, performance, accessibility, security depth]

## Follow-ups

[Tech-debt rows added (TD-NNN), stories proposed, questions for the author.]
