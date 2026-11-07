# Changelog

What changed in each version of the AI Dev Kit, newest first. When updates are on, your assistant shows you the entries that are new since your installed version.

## 2026-11-07

- Live verification: the App Studio team no longer calls something done because tests passed against fakes. A feature with behaviour has to be put on a real test machine (a test server, container, emulator or device) and used the way a person would: real requests, a real browser taking screenshots in the background, a real install. Mock-ups are fine for showing a look, but they are labelled as mock-ups and never count as proof.
- Security testing now attacks the running test copy with real tools (scanners and fuzzers), on top of the agents reading the code, so the check does not come only from the assistant reviewing its own work. The attack tools run only on throwaway test machines, never on your own computer.
- Each app's `studio.yaml` has a new `test_environment:` section that says where the test copy lives. `/app-start` and `/app-adopt` ask about it, and if there is no test environment yet, making one becomes the first job.
- Stories, the planner, the done-check, smoke tests, QA plans, security audits, hardening, releases and the stage gates all check for this live proof. Without it, the answer is "not assessed", never "pass".

## 2026-10-29

- Usage-friendly by default: agents for research, writing and checklists now run on the cheaper Haiku model; everything else stays on Sonnet, and nothing uses Opus. The standing instructions keep the main conversation on Sonnet and warn before the big team workflows.
- Updates: choose at install to be told about new versions (and approve each one), have them installed automatically, or turn checks off. Change it any time with `install.py updates notify|auto|off`.
- Claude Code: the installer can set Sonnet as the default model for new sessions.
- First release: App Studio, game team, security team, `/kit-*` skills, installer for Claude Code and GitHub Copilot, and the START-HERE guide.
