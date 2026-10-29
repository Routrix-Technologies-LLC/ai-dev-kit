> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# PE-CODE-REVIEW: Code Review of a Story

Agent: `principal-engineer`

**Trigger**: At `/app-story-done` for the story's diff, and at `/app-code-review` for a branch or path. Lean mode runs it at `/app-story-done` for any non-trivial change (more than a few lines, or any change an agent wrote); full mode runs it for every change; solo skips it.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Story path (if any) and the architecture/ADR paths that apply
- The diff, or the list of changed files and the base to compare against
- Test results and lint output
- Findings from code-reviewer, language and platform specialists, if already collected (path)

**Prompt**:
> "Review this change as the engineer who owns the codebase. Check:
> (1) Is it correct: does the logic do what the story asks, including error paths, cancellation, concurrency and resource cleanup? Cite file and line for each defect.
> (2) Does it follow the architecture and ADRs: module boundaries, dependency direction, data ownership, no layering shortcuts?
> (3) Does it follow the repository's conventions and the language's idioms, and is it simple enough that the next maintainer can change it?
> (4) Is platform-specific code isolated and correct for each platform it targets (paths, line endings, permissions, lifecycle, threading, locale), without breaking the others?
> (5) Are tests present and meaningful (they would fail if the behavior broke), and is the public or IPC API compatibility preserved?
> (6) Are there security-sensitive spots (input handling, secrets, auth, file or network access) that need a security-engineer look, and is there any new dependency that was not approved?
> Return APPROVE, CONCERNS [list], or REJECT [blockers]."

**Verdicts**: APPROVE / CONCERNS / REJECT

APPROVE means no issues, proceed. CONCERNS means issues that do not block, listed. REJECT means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `PE-CODE-REVIEW: <VERDICT>` on its own line.

Mapping from a `code-reviewer` report (`templates/code-review-report.md`) to this gate: APPROVED or APPROVED WITH SUGGESTIONS is APPROVE; CHANGES REQUIRED with only MEDIUM or LOW verified findings is CONCERNS; CHANGES REQUIRED with any verified CRITICAL or HIGH is REJECT; NOT ASSESSED stays NOT ASSESSED. Your own review can only make the verdict stricter, never looser.

Missing inputs that make this gate NOT ASSESSED: no diff or changed-file list, or no way to read the code. Use CRITICAL, HIGH, MEDIUM, LOW for findings (`standards/severity.md`); any CRITICAL or unresolved HIGH means REJECT.
