# Orchestration: how studio skills run agents

Studio skills run in the main session. The main session is the orchestrator: it talks to the user, spawns agents with the Agent tool, collects their work, and owns the decisions. Agents cannot spawn agents and cannot ask the user anything. Every studio skill follows this file; skills name only what differs.

## 1. Resolve the app first

1. Find the app: the skill argument, else the current folder if it is an app repo, else ask. Read its `studio.yaml`. If there is none, offer `/app-adopt` (existing code) or `/app-start` (new app) and stop.
2. Read `.studio/state.md` if it exists. If it shows unfinished work from an earlier run of this skill, offer to resume from the checkpoint.
3. Note `modes.rigor` and `modes.review` (`standards/rigor.md`). An unset `review` follows rigor. An argument `--review solo|lean|full` overrides it for this run only.

## 2. Announce the plan before spawning

Before the first spawn, print one block so a reduced run is never mistaken for a broken one:

```
App: <name> (<path>)   Stage: <stage>   Rigor: <rigor>   Review: <mode>
Agents this run: <agent> (<job>), <agent> (<job>), ...
Not spawned: <agent> (<why: not relevant to this app's platforms / skipped at this review mode>)
Gates: <GATE-ID> (runs) | <GATE-ID> (skipped: solo mode)
```

Pick agents from the roster by the app's `platforms`, `stack` and `specialists`. A Windows Rust app gets the Windows and Rust specialists, not the iOS engineer.

## 3. Brief each agent properly

The orchestrator reads shared inputs once and passes a distilled brief. A good brief has:

- **App and paths:** the app name, its repo path, and that `studio.yaml` must be read.
- **Goal:** one or two sentences, and the decision or artifact it serves.
- **Inputs:** the specific sections, files and lines that matter, with the key facts quoted, not "read the spec".
- **Constraints:** relevant decisions already made, what is out of scope, the rigor level.
- **Output:** the exact path to write (one file per agent, so parallel agents never share a file), the template to use, and whether it may edit existing source or only create new artifacts.
- **Return contract**, appended verbatim:

```
When done, reply with only: (1) the paths you wrote or changed, (2) at most five bullets on what you decided or found, (3) any BLOCKED or CONCERNS items, one line each, (4) decisions the user must make, as labelled options. Do not restate documents you read.
```

**Read-only reviewers** (`code-reviewer`, and any agent briefed to review without editing) cannot write files. Their return contract is the findings themselves in the shape the skill names; the main session writes the report file and checks it exists.

**Story status words** are fixed everywhere: `Draft`, `Ready`, `In Progress`, `In Review`, `Complete`, `Blocked`. `/app-plan` writes a story as Ready only when its readiness checks ran and passed, otherwise Draft. `/app-dev-story` moves a story to In Progress and then In Review; only `/app-story-done` sets Complete. Status lives only in the story file; sprint files hold commitments, not status.

**Agent drafts** that the main session will turn into a studio document after the user's approval go in the app's `.studio/drafts/<skill>-<scope>-<agent>.md` (local, gitignored with the rest of `.studio/`).

**Write permission inside a run.** Approving a phase approves the agents in it to write the artifacts the brief names. New studio documents (under `docs/`, `planning/`, `prototypes/`, tests) may be written directly at the named path. Changes to existing source code, config or build files are approved by the user for the phase as a set: list the files the phase will touch, ask once, then brief the agent. An agent never chooses its own output path for a studio document.

**User-typed skills.** `app-dev-story`, `app-story-done`, `app-hotfix` and `app-release` carry `disable-model-invocation: true`, so the model cannot start them through the Skill tool. A team skill that needs one asks once at the start: either the user types each command when the team skill reaches it, or, on the user's yes, the main session reads that skill's `SKILL.md` and follows it in place, keeping every ask it contains.

## 4. Spawn in parallel when inputs are independent

Issue every independent Agent call in one message before waiting for any. Collect all results before a dependent phase starts. Review agents for one artifact (for example a security review and an accessibility review of the same change) always run in parallel.

## 5. Trust artifacts, not prose

After each agent returns:

1. **Check the named file exists and has real content** (not just headings or placeholders). An artifact that is not on disk is a failed phase, however fluent the reply. Re-brief once with the gap named; if it fails again, report it as BLOCKED.
2. **Verify claims that a verdict turns on.** If an agent says tests pass, run them or read the run output. If it reports a finding, spot-check it (re-read the code path). Label unchecked specialist claims `UNVERIFIED`.
3. **Surface BLOCKED immediately.** Do not proceed past what it blocks. Produce a partial report when some agents finished and others did not. A skipped or failed agent's section stays a named gap; never fill it with content of your own.

## 6. Decisions belong to the user

- At each decision point, write the analysis in plain text, then ask with AskUserQuestion: 2 to 4 options, short labels, one-sentence trade-offs, `(Recommended)` on the pick. The question is the last thing in the reply.
- **A skipped, dismissed or empty answer is not an answer.** Ask again in plain text and wait. Never pick on the user's behalf.
- Ask once per artifact set, not once per file.
- **Always ask, in every mode, before:** accepting an ADR; advancing the stage; closing a story whose result is BLOCKED or NOT ASSESSED; merging, tagging, publishing, deploying or submitting anything; any destructive data operation; spending money or calling a paid external service the app does not already use.

## 7. Gates inside a skill

A skill that runs a gate spawns the gate's owner with the gate ID and the context fields its definition lists, and tells the agent to read `gates/<id>.md` first. The orchestrator does not read the gate file for the agent. Apply the review mode first: `solo` skips every gate (print `<GATE-ID> skipped: solo mode`), `lean` runs only phase gates and the always-on gates listed in `gates/README.md` (release and security gates, story code review, and the own gate of a single-purpose review skill), `full` runs them all.

When several gates run together, the result is the strictest by this rank: a blocking verdict (REJECT, NOT READY, BLOCK, NO GO, INADEQUATE, UNREALISTIC, HIGH RISK, OFF TRACK, MISALIGNED) beats CONCERNS (and its equivalents), which beats NOT ASSESSED, which beats a pass. One NOT ASSESSED keeps the result from passing.

## 8. Verdicts and the closing block

Every studio skill ends with a verdict from its own list, and every gating verdict list contains `NOT ASSESSED`, ranked below the failure values and above the pass value. A check that could not run is NOT ASSESSED, never a pass. "Zero findings" from a scan of zero files is NOT ASSESSED. A count is always given with its denominator ("0 TODOs in 214 files").

The last lines of every skill run, in this shape:

```
Verdict: <WORD> - <one line why>
Gates: <GATE-ID: VERDICT, ...> | none run (<mode>)
Wrote: <paths, or none>
Next: </app-skill ...> (<why>)
```

Recommend the next skill; never start it automatically.

## 9. Checkpoint as you go

At each phase boundary, overwrite the `CHECKPOINT` block in the app's `.studio/state.md` (template `templates/session-state.md`): current task, next step, blocked on, files in progress, last run result, open questions. A long authoring session writes each approved section to its file as it is approved, so a compaction loses nothing.

## 10. Run and observe

A change a user can see is launched and looked at before it is called done, without stealing focus: headless browser for web, offscreen window capture for desktop, simulator or emulator screenshot for mobile, request and response capture for services. The run is reported as exactly one line:

```
Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why it could not be run> | N/A - <why nothing is observable>
```

"It is a logic change" is not an acceptable N/A when the change alters what a user sees. NOT VERIFIED blocks closing a UI or Visual story. Evidence goes in `docs/qa/evidence/<story-or-change>/`.
