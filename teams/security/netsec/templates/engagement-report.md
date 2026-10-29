# Security assessment: <engagement name>

- **Operator:** <name>
- **Dates:** <start> to <end>
- **Scope:** <one line; full detail in scope.yaml>
- **Intensity:** passive | active-nondestructive | exploit-opt-in
- **Prepared by:** Security Firm agent team

## Executive summary

Three short paragraphs, for someone who will read only this:

1. What was assessed and how far it went (and what was deliberately out of scope).
2. The posture in plain words: what is solid, what is the biggest risk right now.
3. The headline numbers and the one or two things to do first.

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Info | 0 |

## Top risks

The handful that matter most, each in one line: the risk, the asset, and the fix.
Ordered by risk to this operator, not by raw severity.

## Posture by NIST CSF function

A one-line read on each: Govern, Identify, Protect, Detect, Respond, Recover.
What is working, what is thin.

## Technical findings

All findings, most-severe first, each in the `finding.md` format. Grouped by
practice or by asset, whichever reads better for this engagement.

## Coverage and limitations

- What was assessed (assets, techniques, frameworks).
- What was **not** assessed, and why (out of scope, not reachable, needs go-ahead).
- What is `UNVERIFIED` and what would confirm it.
- Tools used, with versions and dates.

## Remediation plan

Pointer to `remediation-plan.md`: the ordered, costed fix list.

## Appendix

Raw scan locations (in `~/AgentScratch/<engagement>/`, not in this repo),
command log, and the scope of record (`scope.yaml` at the assessed commit).
