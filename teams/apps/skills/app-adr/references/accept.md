# app-adr: accept mode

Loaded when the argument is `accept <ADR-id>` (for example `accept ADR-0005` or `accept 5`), and by retrofit when the user says a decision is already in force. This is the only path in the studio that sets `Accepted`. Authoring always writes `Proposed`, and the planning and build skills require `Accepted`, so without this mode an ADR would enter a state it never leaves.

Acceptance authority is the user. `technical-director` may be asked for a view and recommends, but never sets the field. This skill sets `Accepted` only as the act of recording the user's explicit yes in this conversation, and never on its own. This applies in every review mode, including `solo`, and no automatic setting skips the ask.

## Steps, in order. Any refusal is final for this run; no step is skipped.

1. **Resolve the id to exactly one file.** Glob `docs/architecture/adr/ADR-NNNN-*.md` (or the app's mapped ADR path). Zero matches or more than one: stop and say which. Do not pick one. A file with no `## Status` line: stop, and say that retrofit mode adds it.

2. **Check the current status.**
   - `Accepted`: say so and stop (nothing to do).
   - `Deprecated` or `Superseded by ...`: refuse. A superseded decision is not revived by a status edit; the way back is a new ADR.
   - `Proposed`: continue.

3. **Check completeness.** `## Decision`, `### Implementation Guidelines`, `## Consequences`, `## Platform and Version Risk` and `## Validation Criteria` must exist and hold real content (not a template placeholder, not empty). Refuse naming the missing ones; an ADR with no guidelines gives builders nothing to follow.

4. **Check dependencies, strictly.** Read `## ADR Dependencies` (a table with Depends on, Enables, Blocks and Ordering note rows).
   - Section absent, empty, or its Depends on value reading `UNKNOWN`: refuse. "ADR-0005's dependency section is [absent / empty / UNKNOWN], so what this decision rests on is unknown. An empty list and an unexamined one look identical, and only one is safe to accept. Run `/app-adr retrofit <path>` to establish it."
   - Any `Depends on` ADR whose file does not exist: refuse, name it.
   - Any `Depends on` ADR whose status is not `Accepted`: refuse, name each with its status. "ADR-0005 depends on ADR-0002, which is Proposed. Accept ADR-0002 first; an accepted decision resting on an unaccepted one is a deferral with a different label." Check each dependency's own status line, not what ADR-0005 claims about it.
   - A circular dependency among the ADRs involved: refuse and show the cycle.

5. **Find the stories this will unblock, before asking.** Search the epics folder (`planning/epics/`, or the mapped path) for story files. Read `templates/story.md` to see exactly how status and the blocking reason are recorded, and match that form. Keep a story when its Status line reads `Blocked: <reason>` and the reason or its Depends on line names this ADR id. Leave out a story that names this ADR only as the successor to point at (the note left when an older ADR was superseded): it is still governed by the old ADR. For each kept story also read its other ADR references: a story that also depends on an ADR that is not Accepted stays Blocked; list it separately as "stays Blocked (also waiting on ADR-MMMM)".
   - Stories live only under the epics folder. Never match or write a path outside it.
   - If none match, say "no stories are waiting on this ADR". That is information, not an empty result to omit. Also print the denominator ("searched 23 story files").

6. **Ask the user, unconditionally.** Print the effect first: the ADR title, its decision in one sentence, its consequences' headline negative, the dependencies (all Accepted), and the list from step 5 (count and paths). Then ask (`orchestration.md` section 6): "Accept ADR-NNNN: <title>? This is what unblocks the N stories above and lets the plan rely on this decision." Options: yes, accept it (A); not yet, leave it Proposed (B); show the full ADR first (C). Recommend nothing unless the user asks; this is their decision. A skipped, dismissed or empty answer is not a yes: ask again in plain text and wait. Never batch several ADRs under one yes; each ADR gets its own ask, in dependency order.

7. **On yes, edit the status.** Change the `## Status` value to `Accepted` with Edit (include the heading in the matched text so the edit is unique). Leave `## Date` and `## Last Verified` unchanged: stories stamp themselves against them, and rewriting them would make every story drafted against the Proposed ADR look stale. If `## Date` is absent, add it with today's date and say it records acceptance. Append a short `## Acceptance Record` section after `## Related` (the one section accept mode adds beyond the template; it is additive): date, "accepted by the user in conversation", the dependency ADRs and their statuses at that time, stories unblocked. Re-read the ADR and confirm the status line says `Accepted`.

8. **If the ADR supersedes another** (its Related section names `Supersedes ADR-MMMM`), ask separately whether to mark ADR-MMMM `Superseded by ADR-NNNN` now. Then edit only that status line, and list the stories pointing at the old ADR for the user (do not re-point them).

9. **Unblock the stories.** For each kept story whose other dependencies are all Accepted, replace `Blocked: <reason>` in its Status line. The new word is `Ready` only if the story records that it already passed `QL-STORY-READY` (or the user says it did); otherwise `Draft`, and say it needs `/app-story-ready`. Never set In Progress, In Review or Complete here. Edit only the Status line and, if the story has one, a note of the ADR id and date. Re-read each edited story to confirm. A story that cannot be edited cleanly is reported by path, not skipped silently.

10. **Report** what moved: the ADR (and any date added), the stories now Ready or Draft, the stories that stay Blocked and why, and the ADRs that this one unlocks as dependencies (`Enables`) that could now be accepted. Recommend the next skill.

On "not yet" (B): change nothing, say the ADR stays Proposed and the stories remain Blocked, and finish with `COMPLETE - ADR-NNNN left Proposed at the user's choice, 0 stories unblocked`.

## Refusal wording

A refusal verdict is `BLOCKED - <exact reason>`, followed by the single action that clears it. Never partially accept; never accept and promise to fix a dependency later.
