> Gate definition. The spawning skill passes this file's path to the agent, and the agent reads it first. The spawning session does not read it.

# QL-STORY-READY: Story Readiness

Agent: `qa-lead`

**Trigger**: After `/app-plan` writes stories, at `/app-story-ready`, and before a sprint or batch is committed to. It runs as a gate in full review mode only (at `/app-plan` and `/app-story-ready`); lean and solo print `QL-STORY-READY skipped: <mode> mode`. In every mode `/app-plan` and `/app-story-ready` still run their own readiness checklist without spawning the gate, and a story is written Ready only if that check passed, otherwise Draft.

**Context to pass**:
- App name, repo path, and the `studio.yaml` values that matter here (`stage`, `platforms`, `stack`, `modes`)
- Story, epic or sprint paths
- The feature spec(s) and requirement IDs the stories cite
- UX spec path, where the story has UI
- Test-plan or testing standards path, if any

**Prompt**:
> "Review these stories for readiness to start. Check:
> (1) Are acceptance criteria binary and observable (a tester could say yes or no without asking), and does each cite a requirement ID?
> (2) Does each story declare its change type (Logic, Integration, UI, Visual, Data, Config, Infra, Security, Performance, Docs) and the evidence that type requires?
> (3) Are test cases listed, including edge, error and platform-specific cases, and is it clear how each will be run on each platform the story touches (automated, headless, manual device check)?
> (4) Are dependencies and prerequisites (APIs, data, designs, decisions, accounts, test devices) available now, and is the Files list plausible?
> (5) Is the story small enough to finish and verify in one pass, and free of hidden scope ('and also')?
> (6) Where the story touches sensitive data, auth or permissions, is the security or privacy criterion present?
> Return ADEQUATE, GAPS [list], or INADEQUATE [blockers]."

**Verdicts**: ADEQUATE / GAPS / INADEQUATE

ADEQUATE means no issues, proceed. GAPS means issues that do not block, listed. INADEQUATE means blocking issues, listed. NOT ASSESSED is always available when a named input is missing or unreadable (name what was missing); it is never a pass, and a problem you found takes the gate's own word even if an input was also missing. Start the answer with `QL-STORY-READY: <VERDICT>` on its own line.

Missing inputs that make this gate NOT ASSESSED: the story files, or the spec they cite.
