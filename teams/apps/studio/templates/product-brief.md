# Product Brief: [Working title]

<!--
WRITTEN BY: product-director with product-manager, via /app-brief (rigor minimal) or /app-start.
LIVES AT: docs/product/brief.md (override: paths.brief in studio.yaml).
RIGOR: minimal = this page is the ENTIRE design record; every REQUIRED field filled, nothing else needed.
       standard = the brief stays as the one-page summary and links to vision.md and the feature specs.
       full = same as standard; kept in sync with the vision and re-read at every phase gate.
GATE: PD-VISION reads this page.
Keep it to one screen. If a field needs a second paragraph you are writing a spec, not a brief.
Fill every REQUIRED field. RECOMMENDED fields are cheap; delete one only when it truly does not apply.
Stack and platform detail beyond the one platforms line lives in studio.yaml and the architecture doc.
-->

**One-sentence pitch (REQUIRED):** [What it is, for whom, and the result they get, in one sentence. If it takes two, cut. Good: "A shared household budget that shows each person what is safe to spend today." Bad: "A powerful, intuitive platform for modern money management."]

## Problem (REQUIRED)
<!-- What is going wrong for the person today, in their terms, and what they do about it now. Name the current workaround; a problem with no workaround is usually not a problem. 2 to 4 lines. -->
- [Problem and the current workaround]

## Who it is for (REQUIRED)
<!-- One specific person or small group, not "everyone". Say what they do, what they already use, and why they would switch. If the user is also the only user, say so. -->
- [Primary user, context, and what they use today]

## Core job (REQUIRED)
<!-- The one job the user hires this product for. Every MVP item must serve it. -->
- When [situation], I want to [action], so I can [outcome].

## MVP: what must exist for this to be the product (REQUIRED, at most 7)
<!-- The ruthlessly short list. Each item becomes a feature spec or story. If an item can be removed and the core job still works, it is not MVP. More than 7 means it is not an MVP yet. Phrase each as what the user can do. -->
1. [Capability]

## Out of scope: not building this (REQUIRED)
<!-- Specific refusals, written so a future contributor cannot talk themselves into them: "no accounts or sync in v1", "no import from other tools", "no tablet layout". Each line is a decision; add a reason if it is not obvious. -->
- [Not doing X, because Y]

## Success metric (REQUIRED)
<!-- One measurable signal that the core job is being done, with a number and a time frame. For a personal app a plain test is fine: "I use it daily for two weeks without opening the old spreadsheet". State how it is measured. -->
- [Metric, target, how measured]

## Build order (REQUIRED)
<!-- The riskiest or most uncertain thing FIRST: the item that, if it fails, makes the rest pointless (a platform limit, a hard integration, a performance claim). Prove it before polishing anything. One line each, with the risk it retires or the question it answers. -->
1. [Riskiest item]: [what we learn or prove]

## Platforms (REQUIRED)
<!-- From the studio.yaml list: web, windows, macos, linux, ios, android, backend, cli, extension, library. Name the primary platform; add the oldest version supported only if already known. -->
- Primary: [platform]. Also: [platforms, or "none in v1"].

---
<!-- RECOMMENDED: one line each. -->
**Reference product:** [One shipped product this is closest to, and the roughly 10 percent of it the MVP keeps. Scoping against a real product is the fastest honest MVP check.]

**Feel and look:** [One line of intent that steers design choices, e.g. "calm, dense, keyboard-first".]

**Open questions:** [Up to three things that would change this brief if the answer surprised you, each with who or what can answer it.]
