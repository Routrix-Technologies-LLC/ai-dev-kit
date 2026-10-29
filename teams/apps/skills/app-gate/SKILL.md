---
name: app-gate
description: "Phase gate for an app: check one stage transition against its artifact checklist at the app's rigor, run the quality checks, run the director panel for the review mode, verify the verdict, write the gate report, and advance `stage:` only after the user says yes. Use when the user asks 'are we ready to move on', 'can we start building', 'gate check', 'can we release', or wants to advance the app's stage."
argument-hint: "[app] [target stage] [--review solo|lean|full]"
user-invocable: true
---

# App Gate

Prescriptive: "are we ready to advance?" with a formal verdict. (`/app-help` is the read-only "where are we".) This skill checks exactly one transition between the stages in `layout.md`, proves what it can by running things and re-reading files, and is the only skill that changes `stage:` in `studio.yaml`. Rigor relaxes what must exist, never what must work.

Writes: `docs/gates/<date>-<from>-to-<to>.md`, panel records in `docs/gates/panel/`, and (only after the user's yes) the `stage:` line of `studio.yaml`.
Next: the skills named in the transition file's "On PASS", or the skills that close the FAIL, CONCERNS and NOT ASSESSED items.

## When to use and when not to

- Use it at a stage boundary, or when the user asks whether the app is ready for the next stage.
- Not for "what should I do next" (`/app-help`), a single story (`/app-story-ready`, `/app-story-done`), a release decision for a specific version (`/app-release`), or fixing what the gate finds (it names the skill to run; it never creates missing artifacts to manufacture a pass).
- A gate never stops the user from working. The verdict decides only whether `stage:` is written.

## Inputs

- `studio.yaml` (required; if absent, offer `/app-adopt` or `/app-start` and stop). Its `stage`, `platforms`, `commands`, `modes`, `paths`.
- The transition file in `references/` (the only one loaded). If its artifacts are missing, that is the finding, not a reason to stop.
- Optional: earlier gate reports, `.studio/state.md`, `planning/risks.md`.
- Any setting the checklist needs and `studio.yaml` leaves empty (a command, a platform, a hosting fact) is asked or reported NOT ASSESSED. It is never assumed.

## Phase 1: Resolve the transition

Follow `orchestration.md` section 1, then:

1. Target: the argument names the stage to move **to**. No argument: the next stage after `stage:`. Show "Stage is <from>. Gate for <from> to <to>. Correct?" and ask (AskUserQuestion) before going on. The transition must be adjacent. If the user wants to skip stages, run each gate in turn; this skill never jumps two stages. `operate` has no later gate: say so and stop.
2. Stage cross-check: a stored stage the evidence contradicts is a finding, not a fact. Glance at the layout (briefs, specs, ADRs, stories, a running build, a release tag) and say if the observed stage differs from `stage:`. A disagreement is recorded in the report and forces at least CONCERNS.
3. Print the plan block (`orchestration.md` section 2): agents this run, not spawned and why, gates. Panel: the phase gates that `gates/README.md` "Gate coverage by stage" lists as required for this transition, narrowed or widened by rigor (minimal: `TD-PHASE-GATE` and `PG-PHASE-GATE`, plus `PD-PHASE-GATE` at discovery to definition; standard: the table's required column; full rigor: all four). Review mode decides only whether the panel runs: `solo` runs none (print `<GATE-ID> skipped: solo mode` for each gate that would have run); `lean` and `full` run it. Rigor alone decides how wide it is. A gate the table marks optional runs only if the user asks. Per-artifact gates (`PD-VISION`, `TD-ARCHITECTURE`, `PM-ACCEPTANCE` and so on) are not run here: the checklist reads their recorded outcomes. At review mode `full` a missing record is a finding; at `lean` and `solo` it is reported `not run: <mode> mode` and is not a failure. A narrower panel never softens a verdict; the report names who was not consulted.
4. Checkpoint to `.studio/state.md` (`orchestration.md` section 9).

| Transition | Checklist file (read only the one you need) |
|---|---|
| discovery to definition | `references/discovery-to-definition.md` |
| definition to architecture | `references/definition-to-architecture.md` |
| architecture to foundation | `references/architecture-to-foundation.md` |
| foundation to build | `references/foundation-to-build.md` |
| build to hardening | `references/build-to-hardening.md` |
| hardening to release | `references/hardening-to-release.md` |
| release to operate | `references/release-to-operate.md` |

## Phase 2: Load the checklist and apply rigor

Read the one transition file now and follow it. Read it again if the conversation was compacted during this gate. Never load the others.

Apply `modes.rigor` (unset means minimal) to its tier columns: **R** required, **rec** recommended, **-** not checked at this rigor. Reductions only ever relax what must exist. Nothing a tier drops may be reported as passed; list it as "not checked at <rigor>". The `paths:` overrides in `studio.yaml` replace the default paths. For platform-specific items use `platforms`: a UI item for a cli, backend or library app is reported `N/A: no UI platform`, with the reason.

## Phase 3: Artifact check

Main session, parallel Glob/Grep/Read. For each item:

1. Does the artifact exist at the (overridden) path? Record size or count.
2. Is it real? Existence is not adequacy. Open it and read the sections the item names. Template markers (`[`, `TBD`, `<...>`), headings with no body, or boilerplate only count as **absent**.
3. Does the proof column hold? Do the spot-check it names (count against the denominator, compare a version to a lock file, check a date against `git log -1 --format=%cI`).
4. Record one of: PRESENT, ABSENT, PLACEHOLDER, STALE (older than the code it covers), FAILED CHECK, NOT CHECKABLE (say why).

Counts always carry the denominator ("5 of 6 MVP features have a spec"). A scan over zero files is NOT ASSESSED, not clean. Do not write the missing artifacts. Name the producing skill instead.

## Phase 4: Quality checks (run, do not read)

1. Run the commands the transition file lists, using the exact `commands:` from `studio.yaml`; never a command written from memory. Capture exit code and the last lines of output. Use a timeout.
2. Tests: report "N of N run, M skipped, F failed". A runner that cannot start, a command that is unset where the tier requires it, or zero tests run is **NOT ASSESSED**, never a pass. Where the tier drops the item (see the file), say "not required at minimal", and still run it if the command exists: a failure of something that ran is a FAIL at every tier.
3. Launch and observe for foundation to build and later (`orchestration.md` section 10): headless browser, offscreen capture, simulator or emulator, request capture, without stealing focus or injecting input. Each target in `platforms` is observed or reported NOT VERIFIED; a target that cannot be run here is NOT ASSESSED for that target, never skipped silently. Evidence goes in `docs/qa/evidence/`.
4. Heavy runs (release builds, full test suites, emulators) go one at a time, through `~/Tools/agent_locks/run_locked.sh cpu <command>` when that helper exists.
5. `qa-lead` (standard and full rigor, from foundation to build onward; not spawned at review mode solo, say so) re-checks the evidence the verdict turns on: opens the smoke or audit reports, compares claims to the repo, and writes `docs/gates/panel/<date>-qa-lead.md`. Brief per `orchestration.md` section 3 with the checklist results so far and the return contract. Verify what it reports (re-read one claimed file); label the rest UNVERIFIED.

## Phase 5: Manual checks

Facts no scan can settle (is it live, did a person use it, is a requirement missing) are asked in one AskUserQuestion batch. "No" or "not yet" is a **failed** item. A reply the user cannot give ("I don't know") stays MANUAL CHECK NEEDED and becomes NOT ASSESSED. Label every answer `user-stated`. Never assume a pass because the user did not object.

## Phase 6: Director panel

Skip entirely at review mode `solo` (announced in Phase 1). Otherwise spawn the panel Phase 1 chose in one message, one agent per gate: `product-director` (`PD-PHASE-GATE`), `technical-director` (`TD-PHASE-GATE`), `design-director` (`DD-PHASE-GATE`), `program-director` (`PG-PHASE-GATE`). Per `orchestration.md` section 7, tell each agent the gate ID and to read `gates/<gate-id-lowercase>.md` first; do not read it for them.

Context to pass, quoted, not "read the folder": the transition, rigor and review mode; the checklist table with each item's status; the quality-check results; the manual answers; the paths of the key artifacts. For each artifact write one of three things: its path, `none` (the transition requires it at this rigor and it does not exist: a finding), or `not expected before <stage>` / `not required at rigor <tier>` (not a finding). Each agent writes `docs/gates/panel/<date>-<GATE-ID>.md` (layout.md; if that name exists from another transition the same day, append `-<from>-to-<to>`) and returns its verdict first. The verdict word is one of READY, CONCERNS, NOT READY, or NOT ASSESSED.

Combine per `orchestration.md` section 7. A director that did not return, or returned NOT ASSESSED, keeps the gate from passing; say which.

## Phase 7: Draft the verdict and verify it (chain of verification)

Draft the verdict by the rules below, then challenge it before it is final:

1. Write five questions fitted to the draft. For PASS: what required item might be hollow, which check ran against stale output, which target was not observed, what did the user say that I accepted without proof, what would a hostile reviewer open first. For FAIL or CONCERNS: is each blocker real and sourced, is anything marked failed that is only recommended, is the severity right. For NOT ASSESSED: is the missing input really unobtainable now, does asking the user clear it.
2. Answer **at least two** by a tool action: re-open a file, re-run a command, re-count a glob, re-read a git date. Reasoning alone does not count.
3. Revise up (a worse verdict) on evidence. Revise down only on evidence found by a tool. Never turn NOT ASSESSED into PASS by reasoning about the missing input; only obtaining the input clears it.
4. Record the footer: `Chain-of-Verification: N questions, T by tool action - verdict unchanged | revised from X to Y`.

## Phase 8: Write the gate report

Write `docs/gates/<date>-<from>-to-<to>.md` directly (a new studio document; `mkdir` as needed). Shape:

```
# Gate: <from> to <to> (<date>)
App: <name>   Stage: <from>   Rigor: <r>   Review: <mode>   Panel: <who ran; who was not consulted>
Verdict: <PASS|CONCERNS|NOT ASSESSED|FAIL>

## Artifacts            (table: item, required at this rigor, status, evidence path or count with denominator)
## Not checked at <rigor>   (items the tier dropped, listed by name)
## Quality checks       (command, result, "N of N")
## Manual checks        (question, answer, user-stated)
## Panel                (gate ID, verdict, one line; skipped gates named)
## Blockers             (each: what, why it blocks, the skill that clears it)
## Concerns             (each: what, risk, owner)
## Not assessed         (each: what could not be checked, why, what would clear it)
## Accepted risks       (filled only if the user advances on CONCERNS)
Chain-of-Verification: ...
```

## Phase 9: Stage change (the only place it happens)

- **PASS:** show the one-line change (`stage: <from>` to `stage: <to>`) and ask (AskUserQuestion): advance / stay / discuss. Always ask, in every mode.
- **CONCERNS:** list every concern. Advance only if the user explicitly accepts **each** one; record them under "Accepted risks" with the date. A blanket "fine" is not acceptance.
- **FAIL or NOT ASSESSED:** do not offer to advance. Say what clears it and name the skills. No override exists.
- On yes: Edit the `stage:` line in `studio.yaml` (that line only), read the file back, and confirm the value. Update `.studio/state.md`. If the read-back does not show the new value, report BLOCKED and fix nothing else.
- Never edit `stage:` outside this skill, and never advance on a verdict that was not written to the report first.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Checklist | fewest required artifacts (the tier column) | adds specs, ADRs, audits, reviews | adds design language, privacy, budgets, gate records |
| Must work | build, run, smoke, bug bar, open CRITICAL or HIGH | the same plus tests, lint, CI | the same plus budgets, accessibility, rehearsals |
| `qa-lead` re-check | skipped | yes | yes |

| Review mode | Panel |
|---|---|
| solo | none; the checklist and the quality checks still run in full |
| lean | the panel Phase 1 chose (width set by rigor) |
| full | the same panel; in addition a missing per-artifact gate record is a finding |

## Verdicts

First match wins.

1. **FAIL:** any required item is absent, placeholder-only or failed a check; a command that ran failed; a hard rule in the transition file tripped; any panel verdict is NOT READY; the gate would otherwise pass but the stage evidence contradicts the claimed `from` stage in a way that matters.
2. **CONCERNS:** every required item holds, but a recommended item is absent, a risk was accepted in writing, a panel verdict is CONCERNS, a stage-detection disagreement exists, or the user accepted a deviation.
3. **NOT ASSESSED:** a required check could not run (command unset or runner failed, zero tests run, a target could not be observed, a report is stale and could not be refreshed, a user answer is "I don't know", a director did not return or returned NOT ASSESSED). The report says which and what would clear it.
4. **PASS:** every required item holds, every quality check ran and passed, no concern, panel clear or skipped by mode (named). A checklist that left zero checks verified may not pass.

A FAIL or CONCERNS finding takes its own word even if something else was also not assessed; name the unassessed item in the report too.

## Report (reply)

```
Gate: <from> to <to>  Rigor: <r>  Review: <mode>
Required: <n of n> hold   Recommended: <n of n>   Not checked at <rigor>: <n>
Quality checks: <n run, n passed, n not assessed>
Panel: <ids with verdicts, or skipped: solo mode>   Not consulted: <...>
Chain-of-Verification: <N> questions, <T> by tool action - <unchanged | revised from X to Y>
Stage: <unchanged | advanced to <to> on the user's yes | advanced with accepted risks>
Verdict: <WORD> - <one line why>
Gates: <PD/TD/DD/PG-PHASE-GATE: VERDICT, ...> | none run (<mode>)
Wrote: <report path, panel paths, studio.yaml if changed>
Next: </app-skill ...> (<why>)
```

The last four lines follow `orchestration.md` section 8 exactly.

## Rules for this skill

- Never change `stage:` without the user's yes in this run, and never on FAIL or NOT ASSESSED.
- Never create or fill in a missing artifact to get a pass; name the skill that does.
- Never treat a skipped check, an unset command, a test run of zero or a stale report as a pass.
- Never load more than one transition file, and never invent checklist items the file does not contain; the only additive item is a written `rules:` entry in `studio.yaml`.
- Every count carries its denominator; every user answer is labelled user-stated; every skipped gate and tier-dropped item is named in the output.
- Run, do not read, anything the verdict turns on. At least two chain-of-verification questions are answered by a tool action.
- Recommend the next skill; never start it.
