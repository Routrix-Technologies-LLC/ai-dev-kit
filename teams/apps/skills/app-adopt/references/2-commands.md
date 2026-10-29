# app-adopt, Phase 3: find and verify the commands

Part of `/app-adopt`. The hard rules in `SKILL.md` (nothing moved, no secrets, run lock for heavy runs, no side effects on real data) apply here.

Goal: every non-empty value in `studio.yaml` `commands:` was found in the repo's own sources and then run and observed. Keys: `build`, `build_release`, `test`, `lint`, `format`, `run`, `e2e`, `screenshot`.

Steps 1 and 2 run during Phase 2, before the user's approval, because the approval lists the commands. They are read-only. Steps 3 to 5 run in Phase 3 after the yes, on the approved list only.

## Who does it

`build-engineer`, one agent, briefed per orchestration section 3. It does both discovery and verification because the order of runs matters and heavy ones must be serial. Give it: the app path, the Phase 1 detection table (quoted), the approved command list and which were approved as heavy, whether dependencies are installed, the run lock rules, and the output path `~/AgentScratch/adopt-<app>/commands.md`. It may run commands; it may not edit repo files, install anything not approved, or write outside the scratch folder. Append the return contract verbatim.

## Step 1: Find candidates (read-only)

For each key, collect every candidate and where it came from. Sources, in order of authority:

1. CI configuration (`.github/workflows`, `.gitea/workflows`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`): what CI actually runs is the best evidence of a working command, including flags and working directory.
2. Task files: `package.json` `scripts`, `Makefile`, `justfile`, `Taskfile.yml`, `tox.ini`, `noxfile.py`, `build.gradle*` tasks, Cargo aliases in `.cargo/config*`, `scripts/` or `tools/` folders, `fastlane/Fastfile`, `Taskfile`.
3. README, CONTRIBUTING, docs under `docs/` (setup and development sections).
4. Convention for the detected stack, as a last resort and always labelled `convention`, never `found`.

Record per candidate: key, command, working directory, source file and line, and whether it needs prior steps (install, codegen, environment variables, a running service). A command that needs a secret or a service the user must start is recorded with that requirement and not run unless the requirement is already met.

Conflicts (README says one thing, CI another): CI wins, and the conflict goes in the report as a finding.

## Step 2: Classify each candidate before running

| Class | Examples | Handling |
|---|---|---|
| Light | `--version`, lint, type check, format in check mode, unit tests of a small project | run directly |
| Heavy | release builds, full test suites, container builds, dependency installs, bundle analysis, emulator or simulator work | run through `~/Tools/agent_locks/run_locked.sh cpu <command>`; one at a time; exit 75 means stop |
| Windowed or GPU | `run` of a desktop or mobile app, screenshot tools, e2e that drives a browser or emulator | not run unless the user approved that specific command in Phase 2; if approved, through `run_locked.sh gpu`, never with input injection |
| Mutating | `format` that rewrites files, codegen that writes into tracked folders | run only the check variant (`--check`, `--dry-run`, `--diff`) if one exists; otherwise do not run |
| Forbidden | deploy, publish, release, migrate, db reset, anything that contacts a production service, `clean` that deletes data | never run; record as found, `not run (forbidden)` |

If the lock helper does not exist, run heavy commands one at a time and say so in the results. Never kill a process you did not start.

## Step 3: Verify by running, one at a time

Before the first run, record `git -C <app> status --short` as the baseline. For each approved command:

1. Run from the recorded working directory with a ceiling (for example 15 minutes for heavy, 3 minutes for light). A command that exceeds it is `TIMED OUT`, which counts as unverified.
2. Capture exit code, duration, and the last 20 lines of output to `~/AgentScratch/adopt-<app>/logs/<key>.txt`.
3. Judge by the kind of command, not only the exit code:
   - build: exit 0 and the expected artifact or output exists (name it).
   - test: exit 0 **and** a count of tests run greater than zero. Report "N passed, M failed, K skipped of T". Zero tests discovered is `UNVERIFIED (no tests ran)`, never a pass. A failing suite is reported as failing with the count; the command is still a working command, recorded with a note, because adoption establishes the command, not the health of the code.
   - lint and format check: exit code plus the tool's own summary. A lint failure with findings means the command works; a tool-not-found or config error means it does not.
   - run: for a CLI, run its help or version output. For a service, only when it starts with local development settings and needs no production secret or remote service: start it, observe the readiness line or first output, stop it, and confirm the process you started is gone. Otherwise `NOT RUN (needs: <requirement>)`. For a GUI app, only if approved (see class table).
   - e2e and screenshot: only if approved; evidence is a produced file of non-trivial size.
4. After each run compare `git status --short` with the baseline. New tracked-file changes are reported (the command touched the repo); do not revert them, ask the user.
5. A failure caused by the environment (dependencies missing, toolchain not installed, service unreachable) is `UNVERIFIED (environment: <what>)`, with the exact message. Do not install anything outside the approved list to make it pass.

## Step 4: Results file

Write `~/AgentScratch/adopt-<app>/commands.md` with one row per key:

```
| Key | Command | Source | Class | Status | Evidence |
```

Status values: `VERIFIED`, `VERIFIED (tests failing: N of T)`, `UNVERIFIED (<reason>)`, `NOT RUN (forbidden | windowed, not approved | mutating, no check mode)`, `ABSENT (nothing found)`. A key with nothing found is `ABSENT`; the studio never invents a command for it.

Below the table list: conflicts between sources, requirements a human must meet (secrets, services), repo changes made by runs, and the commands CI runs that the studio has no key for (for example a separate type check), so the report can recommend them.

## Step 5: What the main session checks

The main session does not trust the table's prose (orchestration section 5):

1. The results file exists with a row for every key, and every VERIFIED row has an evidence cell with real content.
2. Re-run the cheapest verified command (usually lint or a test listing) and compare. Label the other rows `UNVERIFIED by the main session` in the report if this check was skipped.
3. Report the count as "verified N of M keys found, K absent".

If the agent returns without the file, re-brief once with the gap named; a second failure makes the verification part of the run BLOCKED, and the verdict follows the rules in `SKILL.md`.
