---
name: sec-compliance
description: "Framework-mapped posture assessment: score the environment against NIST CSF 2.0 (and 800-53/800-171 for depth) and CIS Controls v8 + CIS Benchmarks, with a ranked risk register. Produces a trackable scorecard, not a compliance declaration. Use for 'score me against NIST', 'CIS benchmark', 'where do I stand', 'risk assessment', 'posture review'."
argument-hint: "[scope] [--framework csf|cis]"
user-invocable: true
---

# Posture and compliance assessment

Driven by `grc-lead`. Maps the environment and the other practices' findings to a
recognized framework so posture is trackable over time. Right-sized: a homelab is
scored to prioritize, not to pass an enterprise audit.

## Steps

1. `ED-SCOPE` CLEAR. Gather the technical findings and coverage notes from the
   other practices (run a `/sec-assess` first for a full picture, or score what
   exists).
2. Run the specialists:
   - `nist-compliance-specialist`: CSF 2.0 scorecard (Govern, Identify, Protect,
     Detect, Respond, Recover), with 800-53/800-171 control mapping if depth is
     wanted.
   - `cis-benchmark-specialist`: CIS Controls v8 (at IG1 for a small environment)
     and per-platform CIS Benchmarks, top deviations as findings.
   - `risk-analyst`: ranked risk register (likelihood x impact here), with a
     proposed decision per risk and an overall posture statement.
3. Confirm every framework edition against its official source before citing.

## Output

`compliance-assessment.md`: the CSF scorecard, CIS scoring, and the ranked risk
register, cross-linked to findings and feeding the remediation plan.
