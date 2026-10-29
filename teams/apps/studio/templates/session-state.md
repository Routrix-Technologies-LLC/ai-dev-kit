# Session state: [app name]

<!--
Template: session-state. Written by: the main session, via every studio skill at each phase boundary. Skill: all /app-* skills; /app-start creates it; /app-help reads it.
Lives at: .studio/state.md in the app repo. Local and gitignored (add `.studio/` to .gitignore). Old narrative rotates to .studio/log/<date>.md.
Rigor: the same at every level. The checkpoint is cheap and always kept.

HOW THIS FILE WORKS
  Two regions, not interchangeable.
  1. STATUS and CHECKPOINT blocks: what a returning session reads first. OVERWRITTEN on every update, never appended to. Keep CHECKPOINT under about 25 lines.
  2. Everything after `<!-- /CHECKPOINT -->` is free narrative. It may grow, but see Rotation.
  The file is the memory, not the conversation. After a compaction, a crash, a new session or /clear, read this file first.

ROTATION
  When the narrative passes about 200 lines, move it to `.studio/log/<date>.md` and start the Notes section fresh. Keep the STATUS and CHECKPOINT blocks in place. Nothing is lost: git history and the log hold the rest.

Do not delete the markers. Do not put secrets or credentials here.
-->

<!-- STATUS -->
Epic:
Story:
Task:
<!-- /STATUS -->

<!-- CHECKPOINT -->
**Updated:** [YYYY-MM-DD HH:MM]
**Skill / phase:** [for example /app-plan, phase 3 of 5]
**Branch:** `[branch]`
**Current task:** [one line: what is actively being worked on, specific enough to be wrong]
**Next step:** [one line: the very next action, concrete enough to resume cold]
**Blocked on:** [one line, or `nothing`]
**Files in progress:** [paths, comma-separated, or `none`]
**Run result:** [verbatim `Run result:` line from /app-dev-story for /app-story-done to read: OBSERVED - ... | NOT VERIFIED - ... | N/A - ... ; omit otherwise]
**Last verified:** [what was last actually run or checked, and its outcome, with counts and denominators]
**Open questions:** [one line each, or `none`]
<!-- /CHECKPOINT -->

---

## Notes

[Free-form. Decisions and their reasons, what was tried and rejected, context that would be expensive to reconstruct, user answers worth keeping. Date each entry. Write for the person or agent picking this up cold.]

<!--
FIELD NOTES
  "Current task: fixing the thing" is useless. "Current task: adding retry with backoff to the sync client in src/sync/client" is not.
  Keep Branch current: this file is not committed, so it stays put when you switch branches.
  Write each approved section of a long authoring session to its file as it is approved, then update the checkpoint, so a compaction loses nothing.
-->
