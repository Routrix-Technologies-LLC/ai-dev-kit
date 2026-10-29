### Building something

1. **Read the spec, story or bug first.** Note what is specified, what is ambiguous, and what the acceptance criteria are. No spec at all for non-trivial work is itself a finding: say so.
2. **Ask the architecture questions a senior engineer would.** Where does this live? What does it depend on, and what will depend on it? What happens on failure, on empty input, offline, under load, on the oldest supported OS or browser? Does this touch saved data, a public API, or security?
3. **Propose the structure before writing it** when the change is more than small: files, types, data flow, and why this shape fits the app's existing patterns.
4. **Implement in small, verifiable steps.** Keep the build green between steps. Write or update tests with the change, not after. If you hit a spec ambiguity mid-way, stop and report it rather than guessing. If a constraint forces you to deviate from the spec or the ADR, say so explicitly.
5. **Prove it works.** Run the app's build, lint and tests (the commands in `studio.yaml` or the README), and produce the evidence its change type requires (`standards/testing.md`). A compile check is not a run.
6. **Leave it reviewable.** A focused diff, no drive-by reformatting, no stray debug output, comments only where the why is not obvious. Name the next useful step (tests to add, a review to run, a follow-up to file).
