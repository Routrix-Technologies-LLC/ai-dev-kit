# Checklist: foundation to build

Question: does a walking skeleton build, test and run on every target, with the loop of work (stories, evidence, review) ready?

Legend: **R** required (absent, placeholder-only or failing is FAIL). **rec** recommended (absent is CONCERNS). **-** not checked at this rigor (listed, never counted as passed). **R\*** required only at review mode `full`: it reads the outcome of a per-artifact gate, and `lean` and `solo` do not run those. At other modes report `not run: <mode> mode`, which is not a failure.

**Hard rule:** if a skeleton exists and any "must work" item below (2, 3, 4, 5) was run and failed, the verdict is FAIL at every rigor. A skeleton that cannot be run on a target here makes that target NOT ASSESSED, never skipped.

## Artifacts

| # | Item | Where | Proof beyond existence | minimal | standard | full |
|---|---|---|---|---|---|---|
| 1 | `commands:` filled in | `studio.yaml` | minimal: `build` and `run`. standard and full: `build`, `build_release`, `test`, `lint`, `run`. Each is the exact command, not prose | R | R | R |
| 2 | Clean build succeeds | run `commands.build` | Exit code and last lines of output; from a state with no build output where practical | R | R | R |
| 3 | Test harness runs and passes | run `commands.test` | "N of N run, M skipped, 0 failed". Zero tests run is NOT ASSESSED. Skipped tests are listed | rec | R | R |
| 4 | Walking skeleton: one thin path through the real layers, on every target | evidence in `docs/qa/evidence/walking-skeleton/` | Launch and observe per `orchestration.md` section 10 for each entry in `platforms`; the evidence file is newer than the last source commit. Report "N of N targets observed" | R | R | R |
| 5 | CI configured and green on the main branch | CI config file; latest run | Config file exists and runs build and tests. Latest run status read from the CI tool if a CLI is available, else asked of the user and labelled user-stated | rec | R | R |
| 6 | Reaches a test environment through the pipeline, and a person used it | deploy log, `docs/qa/evidence/walking-skeleton/` | Backend and web with `stack.hosting` set: a staging deploy and a health check. Desktop, mobile, cli: a package built by the pipeline that installs and launches on a clean target | - | R | R |
| 7 | Epics and stories exist for the MVP | `planning/epics/` | minimal: at least the first stories, each with acceptance criteria. standard and full: every MVP requirement maps to a story; the first epic's stories have status Ready (`/app-plan` writes Ready only after their readiness checks passed; Draft stories are not ready) | R | R | R |
| 8 | Design tokens in code | UI code | Tokens from the design language are the source of colors and type, not literals (Grep sample); UI platforms | - | rec | R |
| 9 | No secrets committed; `.studio/` ignored | repo, `.gitignore` | Run a secret scanner if installed, else a pattern Grep; label it a pattern scan, not an audit. Report files scanned | R | R | R |
| 10 | Lint and format pass | run `commands.lint` | Exit code | - | R | R |
| 11 | Environments and secrets handling in place | config, docs | Dev, staging and prod config separated; secret store named | - | rec | R |
| 12 | Observability skeleton | code, config | Structured logging and crash reporting wired in the skeleton (or a recorded reason they are not applicable) | - | rec | R |
| 13 | Per-artifact gate outcomes recorded | epic and sprint plan headers | `PG-PLAN` on the plan and `QL-STORY-READY` on the first epic, neither REJECT-class (UNREALISTIC, INADEQUATE) nor NOT ASSESSED. `PG-SCOPE` is optional | - | R* | R* |

## Quality checks

Run, do not read: build (2), tests (3), lint (10), and the launch-and-observe of item 4. Evidence is on disk. `commands.screenshot` unset means the observe step falls back to the platform table in `standards/testing.md`; if nothing works, the target is NOT VERIFIED and the item is NOT ASSESSED.

## Manual checks

- Have you personally run the skeleton on the machine or device you will test on?
- Does anything in the skeleton exist only on your machine (a local file, an installed tool, a secret)?

## Panel focus

`TD-PHASE-GATE`: does the skeleton prove the architecture. `PG-PHASE-GATE`: is the backlog real and sequenced. `PD-PHASE-GATE` and `DD-PHASE-GATE` (full): does the first path match the vision and the design language.

## On PASS

Stage becomes `build`. Next: `/app-sprint` or the next ready story with `/app-dev-story`, `/app-story-ready`.
