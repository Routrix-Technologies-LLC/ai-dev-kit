> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# QL-TEST-COVERAGE: Test Coverage Review

Agent: `qa-lead`

**Trigger**: At `/app-story-done` after tests have been run. Lean mode skips it; full mode runs it.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Story path with its change type and acceptance criteria
- Test files added or changed, and the test run output with its date and command
- Evidence folder (`docs/qa/evidence/<story-or-change>/`) listing
- Platform matrix: which targets the story affects and which were exercised
- Test-plan path, if any

**Prompt**:
> "Review the test coverage and evidence for this story. Check:
> (1) Does every acceptance criterion have at least one test or evidence item that would fail if the criterion broke? Map them one to one.
> (2) Does the evidence match the change type (Logic: unit tests; Integration: contract or end-to-end; UI and Visual: observed run and captures; Data: migration and reload of old data; Security, Performance: targeted checks against budgets)?
> (3) Were the tests actually run and seen passing (command and output present), and for a bug fix, seen failing before the fix?
> (4) Are edge, error and boundary cases covered, and is flakiness avoided (no sleeps on real time, no network without fakes)?
> (5) Is each affected platform exercised, or is a platform listed as not verified? An unexercised platform is a gap to name, not a pass.
> (6) Do tests assert behavior rather than implementation details, and do they leave no stale or skipped cases hiding failures?
> Return ADEQUATE, GAPS [list], or INADEQUATE [blockers]."

**Verdicts**: ADEQUATE / GAPS / INADEQUATE

ADEQUATE means no issues, proceed. GAPS means issues that do not block, listed. INADEQUATE means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `QL-TEST-COVERAGE: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: no test output and no evidence folder at all.
