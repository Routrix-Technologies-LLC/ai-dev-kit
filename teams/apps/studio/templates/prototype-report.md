<!--
Template: prototype-report. Written by: prototyper with the relevant lead. Skill: /app-prototype.
Lives at: prototypes/<name>/REPORT.md, beside the throwaway code (override: paths.prototypes). Prototype code is never imported by production code.
Rigor: minimal = question, verdict, what must be rebuilt. standard = adds hypothesis, timebox, what was built, shortcuts, measurements. full = adds alternatives tried, risks retired or created, and a recommended story breakdown.
Delete this comment when the report is created.
-->

# Prototype report: [name]

> **Date**: [YYYY-MM-DD]   **Author**: [agent]
> **Timebox**: [planned n hours or days / actual n]
> **Verdict**: [PROCEED | PIVOT | KILL | NOT ASSESSED]

## Question

[The single question this prototype answers, phrased so the answer is yes, no or a number. If it needs two questions, it is two prototypes.]

## Hypothesis

[What we expected and why. Success criteria stated before building: "PROCEED if <measurable>."]

## What was built

[The smallest thing that could answer the question. Platforms and versions used. Where the code is: `prototypes/[name]/`. How to run it.]

## Shortcuts taken

Be honest. Everything below is why this code must not ship:
- [hardcoded data, no error handling, no tests, no security, one platform only, mocked services, ignored edge cases]

## Measurements and observations

| Measurement | Method | Result | Compared with criterion |
|---|---|---|---|
| [latency, size, memory, frame rate, accuracy, effort, developer experience] | [how] | [number with sample count] | [met / missed] |

Observations that surprised us: [...]

## Verdict

**[PROCEED | PIVOT | KILL | NOT ASSESSED]**: [Reasoning in a few sentences, tied to the criteria. NOT ASSESSED if the question could not be answered in the timebox; say what is still unknown.]

- PROCEED: build it properly. PIVOT: the idea is sound but the approach changes (say to what). KILL: stop, and record why so it is not retried blindly.

## What must be rebuilt

The production version starts from the design, not from this code. List what carries over (learnings, test data, measurements) and what must be built fresh with real quality: [architecture, error handling, tests, security, accessibility, platforms].

## Next

[ADR to write, stories to plan, risks to log (RISK-NNNN), spec changes.]
