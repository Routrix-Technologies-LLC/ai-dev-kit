---
paths:
  - ".claude/agent-memory/**"
---

# Agent Memory Rules

Adapted from the `agent-memory` rule of Claude Code Game Studios (MIT, see
`.claude/agents/LICENSE-claude-code-game-studios.txt`).

Agents with `memory: project` may keep working notes in `.claude/agent-memory/<agent>/`.
That folder is gitignored, per agent, and never ships. The notes are the agent's own
record of how to do its job here, not a project artifact: writing one needs no
approval, but it is never a substitute for asking when a brief or the user has not
approved a change to the project itself, and it must never record something the user
declined to have written.

## Record methods, never states

A note that says what is missing or absent ("X doesn't exist yet", "there are no tests
for Y", "the inventory has no Z") is true when written and wrong a week later, when it tells
a future run to skip work or give a wrong answer. This project changes every day.

- **Record a method:** "To find where saves are written, read the save function the
  profile names and search for the field" lasts. "Inventory is not saved" is a timestamp.
- **If you must record a state,** write what invalidates it on the same line:
  `INVALIDATED WHEN: <the file, key or commit that changes it>`. A reader with no other
  context must be able to tell whether the note still holds.
- **Never record the absence of a feature, asset, test or config as a settled property
  of the project.**

## Disclose the write

Say in your report that you recorded a note and where. An unmentioned write is
indistinguishable from no write, and the user cannot correct a note they do not know exists.

## Verify before you trust

A note reflects what was true when it was written. If it names a file, a path, a key, a
number or a count, check that it still holds before acting on it. Memory is a starting
point for investigation, never evidence.
