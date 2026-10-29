---
name: sec-report
description: "Consolidate an engagement's findings into one assessment: executive summary, ranked and deduplicated technical findings, NIST CSF posture, and a costed remediation plan, gated by RW-REPORT. Use for 'write up the assessment', 'consolidate the findings', 'give me the report', or after the testing practices have run."
argument-hint: "[engagement]"
user-invocable: true
---

# Assessment report

Driven by `report-writer`, gated by `RW-REPORT`.

## Steps

1. Gather every practice's findings and coverage notes, the GRC posture, and the
   risk register from the engagement's docs and `~/AgentScratch/<engagement>/`.
2. Consolidate and dedupe (same root cause = one finding, cross-referenced). Rank
   by real risk to the operator with `risk-analyst`, not by raw severity.
3. Build the report from `templates/engagement-report.md`:
   executive summary (plain language, stands alone), severity counts, top risks,
   NIST CSF posture, technical findings in `finding.md` format, coverage and
   limitations, and the `remediation-plan.md`.
4. Run `RW-REPORT`. Send anything unevidenced, unverified-but-rated-high, or
   missing its coverage note back before delivery. Keep secrets and the WAN IP
   out; point to raw artifacts rather than pasting them.

## Output

`engagement-report.md` and `remediation-plan.md`, ready for the operator, plus a
short spoken summary of the top risks and the first fixes.
