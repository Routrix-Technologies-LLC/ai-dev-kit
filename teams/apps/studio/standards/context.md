# Context management

Context is the scarcest resource in a long session. The conversation will be compacted or lost; files persist. **The file is the memory, not the conversation.**

## The checkpoint: `.studio/state.md`

Template: `templates/session-state.md`. Location and rules: `layout.md`.

- Overwrite the `CHECKPOINT` block (never append to it) at each phase boundary and after each significant milestone: a section approved and written, a decision made, a test result obtained, a story closed. Keep it under about 25 lines: current task, next step (concrete enough to resume cold), blocked on, files in progress, last run result, open questions.
- Below it is free narrative. Past about 200 lines, move it to `.studio/log/<date>.md` and start fresh. Add `.studio/` to the app's `.gitignore`.
- Volatile state (checkpoint, logs, captures, scratch) stays out of cloud-synced folders where it can; scratch goes to `~/AgentScratch/<task>/`. Do not rewrite the checkpoint on every turn: write it on milestones.

## Write incrementally

For any multi-section document (spec, architecture, audit, plan):

1. Create the file with every section heading and an empty body, after the user agrees to the path.
2. Settle one section at a time, then write it to the file at once.
3. Update the checkpoint after each section.
4. Once written, earlier discussion of that section can be safely dropped. The context then holds only the current section, not the whole conversation.

A skill that writes once at the end records approved sections in the checkpoint instead.

## Keep reads small

- Read documents by section: Grep for headings (`^#`), Read the range. Read a whole long document only when the task needs all of it, and say why.
- Do not read lockfiles, generated bundles, build output, `node_modules`, or minified files. Search the folders that matter, by path.
- Use a subagent for research that would take more than a few thousand tokens of reading across many files; use direct reads when you know the one or two files. A subagent starts with no history, so brief it fully.
- Compact at natural points (after writing a section, after a commit, after a story closes), and before the window is nearly full, not at the limit. Use `/clear` between unrelated tasks or after two failed corrections.

## Recovering after compaction, a crash or `/clear`

1. Read `.studio/state.md` first.
2. Read the files it lists as in progress, by section.
3. Read `studio.yaml` and re-apply the app's `rules:`.
4. Check git status for the app (`git -C <app> status`, `git -C <app> log -5`) to see what is already changed or committed.
5. Re-run the last check named in the checkpoint rather than trusting a remembered result.
6. State what you recovered and where you are resuming, then continue from the next incomplete step. Do not redo approved work, and do not assume anything the files do not show.

When asked to compact, preserve: the checkpoint path, files changed and why, decisions with their reasons, the status of each agent invocation (done, failed, blocked), test results with counts, open questions for the user, and which sections of the current document are written versus pending.

## Error recovery: agents that fail

**Verify the artifact before reading the reply.** If the brief named a file, check that it exists and has real content (not only headings or placeholders). A fluent reply with no file is a failed phase. An agent can do a lot of work and return a single plausible sentence with nothing written, and nothing in its prose will say so.

When an agent returns BLOCKED, errors, or writes nothing:

1. **Surface it at once,** naming the agent, the reason, and what is missing and where it was expected. Do not advance past what it blocks.
2. **Re-brief once.** Name the unmet contract plainly ("you did not write `<path>`; writing it, or saying exactly why you cannot, is the required output") and add what was missing. Prefer continuing the same agent (its context is still there) over a fresh one when that is possible; a fresh agent needs a complete brief.
3. **If it fails again, it is BLOCKED.** Offer the user options: skip it and record the gap, retry with narrower scope, or stop and resolve the blocker.
4. **Always produce a partial report** of what did finish. One blocked agent never discards the others' work.
5. **A skip does not clear the block.** The final verdict names the skipped agent and its gap; it is not a pass.
6. **Never fill a failed agent's gap with your own content.** Its section stays a named gap, so the reader can see what was not done. Writing a plausible substitute turns a visible hole into an invisible one.
7. **Verify claims that a verdict turns on.** If an agent says tests pass, run them or read their output. Label unchecked claims `UNVERIFIED`. A check that could not run is NOT ASSESSED, never a pass.
