> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PM-ACCEPTANCE: Acceptance Check

Agent: `product-manager`

**Trigger**: At `/app-story-done`, after implementation and tests, before the story can close. Lean mode skips it; full mode runs it.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Story path with its acceptance criteria and requirement IDs
- The feature spec path
- Evidence: test results, `Run result:` line, screenshots or response captures, with paths
- The story's Files list and the changed-files list from version control
- Deviations the builder reported

**Prompt**:
> "Judge whether this story is done by the product's definition. Check:
> (1) For each acceptance criterion, quote the evidence that shows it met. Any criterion without evidence is unmet.
> (2) Does the built behavior match the spec's intent, including edge cases and error states, not only the happy path?
> (3) Does the behavior hold on every platform the story targets (the platforms in its scope), with evidence from each, or is one assumed?
> (4) Do the changed files match the story's Files list? Is there extra behavior that no criterion asks for, or a criterion satisfied by a shortcut that breaks the intent?
> (5) Are deviations from the spec recorded and accepted, and does any need a spec update or a new story?
> Return ACCEPTED, CONCERNS [list], or REJECTED [blockers]."

**Verdicts**: ACCEPTED / CONCERNS / REJECTED

ACCEPTED means no issues, proceed. CONCERNS means issues that do not block, listed. REJECTED means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PM-ACCEPTANCE: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no evidence for the criteria, or no story file. Absent evidence for a criterion is a finding when other evidence exists, and NOT ASSESSED when none was provided at all.
