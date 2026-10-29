# Product Vision: [Product name]

<!--
WRITTEN BY: product-director, with domain-researcher (sources), ux-researcher (personas) and product-manager, via /app-brief.
LIVES AT: docs/product/vision.md (override: paths.vision in studio.yaml).
RIGOR: minimal = not used; the one-page product-brief.md replaces it.
       standard = sections 1 to 8 filled; two personas are enough; pillars, anti-pillars and metrics required; sources listed.
       full = every section; each persona backed by named evidence; positioning checked against real alternatives with dates; pillars tested against the three hardest decisions so far; re-read at every phase gate.
GATE: PD-VISION. Downstream docs (feature specs, UX specs, design language) cite pillars by ID (P1, P2 ...).
Every claim about users or the market carries a source and a date checked, or is marked ASSUMPTION. Do not invent personas or numbers.
-->

**Status:** [Draft | In review | Approved by the user]   **Last reviewed:** [YYYY-MM-DD]   **Owner:** product-director

## 1. Problem and jobs to be done
<!-- State the problem as observable behavior and cost: what people do now, what it costs them (time, money, errors, stress), how often. Then list 3 to 6 jobs as "When [situation], I want to [motivation], so I can [outcome]". Separate functional jobs from emotional or social ones. Good: names the trigger situation. Bad: a feature list in disguise. -->
**Problem:** [Observable problem, frequency, cost.]

| ID | Job (When ... I want ... so I can ...) | Frequency | Importance | Current alternative |
|---|---|---|---|---|
| J1 | [job] | [daily / weekly / rare] | [high / medium / low] | [what they do today] |

## 2. People it is for
<!-- Personas built from evidence, not imagination: interviews, support requests, reviews, analytics, the user's own experience (mark it as such). A persona is a pattern of behavior and context, not a stock photo and an age. Two to four personas; one is primary, and the primary one wins design conflicts. For a personal tool with one user, one persona is correct. -->
### Primary persona: [Label]
- **Context:** [Where, when, on what device, under what time pressure.]
- **Jobs (from section 1):** [J1, J2]
- **Pain today:** [Specific incidents, in their words if quoted.]
- **Skill and tools:** [Technical comfort, current tools, accessibility needs if known.]
- **Evidence:** [Source, date, sample size or "single observation"; confidence high / medium / low.]
- **Would not use us if:** [The deal breaker.]

### Secondary persona(s)
- [Same fields, shorter.]

### Not for
- [Who we are deliberately not serving, and why.]

## 3. Value proposition
<!-- One paragraph: For [persona] who [job and situation], [product] is a [category] that [key benefit]. Unlike [alternative], it [differentiator that is true and checkable]. Then up to 3 benefits, each tied to a job ID and each with proof or a plan to prove it. -->
[Statement.]

| Benefit | Job | Proof it is real (feature, measurement, or "to be proven in prototype") |
|---|---|---|

## 4. Positioning and alternatives
<!-- Compare against what users really use, including doing nothing, spreadsheets and paper. Facts only, each with a source and the date checked. Say where we are worse and why that is acceptable. -->
| Alternative | Strong at | Weak at | Price / terms | Source, date checked |
|---|---|---|---|---|

**Where we win:** [One or two specific situations.]  **Where we lose, on purpose:** [One or two.]

## 5. Design pillars
<!-- 3 to 5 pillars. A pillar is FALSIFIABLE: a team could build something that violates it, and the design test says so. "Intuitive" and "high quality" are not pillars. Each pillar has a design test: a concrete question or measurable check a reviewer applies to a feature or screen, and a cost: what we give up to honor it. Pillars rank; when two conflict, the lower number wins, and that is written down. -->
| ID | Pillar (a commitment, one sentence) | Design test | What it costs us |
|---|---|---|---|
| P1 | [e.g. "Every common action works without a network."] | [e.g. "Can the task be completed offline? If not, it violates P1."] | [e.g. "No server-only features."] |

**Conflict rule:** [P1 beats P2 beats P3. One real or likely conflict and how it resolves.]

## 6. Anti-pillars
<!-- 2 to 4 things this product refuses to be, even though users or stakeholders may ask. Each is a decision with a reason, and each should be something a competitor does and gains from. -->
- **Not [X]:** [Why. What we do instead.]

## 7. Success metrics
<!-- One north-star metric that tracks the core job being done (not vanity: not downloads, not page views). Counter-metrics guard against gaming it (quality, trust, accessibility, performance, opt-outs). Targets have numbers and dates; for a personal app a plain test is fine. Each metric names its source and links a tracking-plan.md event if instrumented. -->
| Type | Metric | Definition | Target and timeframe | Source |
|---|---|---|---|---|
| North star | [metric] | [exact formula] | [target] | [event / survey / manual] |
| Counter | [e.g. crash-free sessions, task error rate, opt-out rate] | | [floor or ceiling] | |

## 8. Scope tiers
<!-- Tier 1 is the product: without it there is no product. Tier 2 makes it good. Tier 3 is wanted but cuttable. Tier 4 is explicitly later. Every item names the pillar or job it serves; an item that serves none is a cut candidate. Cut from the bottom when scope or time slips (PG-SCOPE uses this table). -->
| Tier | Meaning | Capability | Serves (P#, J#) | Spec |
|---|---|---|---|---|
| 1 | Must ship | [capability] | [P1, J1] | docs/product/specs/[feature].md |
| 2 | Should ship | | | |
| 3 | Could ship | | | |
| 4 | Later, not now | | | |

## 9. Risks and assumptions
<!-- The assumptions that would sink the product if false, each with how and when we will test it. Riskiest first; this ordering feeds the build order. -->
| # | Assumption | If wrong | How we test it | By when |
|---|---|---|---|---|

## 10. Sources and open questions
- [Source, date checked, what it supports]
- Open: [question, who can answer]
