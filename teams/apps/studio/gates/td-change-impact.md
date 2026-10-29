> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# TD-CHANGE-IMPACT: Change Impact Assessment

Agent: `technical-director`

**Trigger**: When an already-approved spec, ADR, API contract or architecture element changes and downstream work (stories, code, other specs) exists. No catalog skill owns it alone: the skill making the change runs it in full mode, and program-director may request it for any cross-team change.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- The change: what was approved, what it becomes, and why
- The impact assessment: affected specs, ADRs, stories (by ID and status), code areas, tests, platforms and store or release artifacts
- Stories already in progress or closed that the change touches
- Data, API or file-format compatibility notes

**Prompt**:
> "Review this change impact assessment. Check:
> (1) Is the list of affected artifacts complete? Search for references to the changed requirement IDs, interfaces and files and name any the assessment missed.
> (2) Which closed or in-progress stories become invalid or need rework, and is that cost stated in the assessment?
> (3) Does the change break compatibility: stored data, saved files, public or IPC APIs, settings, or behavior of already-released versions? Is there a migration or deprecation path?
> (4) Does it affect each platform equally? Name platforms where the cost or risk differs (store review, OS version limits, packaging, build config).
> (5) Is the blast radius proportionate: could a narrower change deliver the same outcome?
> (6) Does it change a budget, a trust boundary or a threat-model assumption, requiring SL-THREAT-MODEL or SL-PRIVACY to run again?
> Return CONTAINED, CONCERNS [list], or WIDE IMPACT [blockers]."

**Verdicts**: CONTAINED / CONCERNS / WIDE IMPACT

CONTAINED means no issues, proceed. CONCERNS means issues that do not block, listed. WIDE IMPACT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `TD-CHANGE-IMPACT: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the impact assessment, or the artifacts it must be checked against.
