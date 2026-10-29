---
name: app-prototype
description: "Run a time-boxed spike that answers one question in an isolated prototypes/<name>/ folder, then decide PROCEED, PIVOT or KILL and list what must be rebuilt properly. Use when the user says prototype, spike, proof of concept, 'will this work', 'can we use X', or a risky idea or unknown technology needs proving before committing."
argument-hint: "[question or idea] [--name <slug>] [--timebox 4h|1d] [--review solo|lean|full]"
user-invocable: true
---

# App Prototype

A prototype is a throwaway build that answers exactly one question fast, with evidence, before the app commits to it. It lives in `prototypes/<name>/`, is never imported by production code, and ends in a decision: PROCEED, PIVOT or KILL. The code is never promoted. The report says what must be rebuilt properly if the answer is PROCEED.

Writes: `prototypes/<name>/` (the spike), `prototypes/<name>/REPORT.md` (template `prototype-report.md`), and one row in `prototypes/index.md`. The folder is `paths.prototypes` from `studio.yaml` when set.
Next: `/app-adr` or `/app-stack` (PROCEED on a technology or approach), `/app-spec` or `/app-plan` (PROCEED on a feature), `/app-prototype` again (PIVOT), `/app-brief` (KILL on the idea).

## When to use and when not to

Use it when one specific, risky unknown blocks a decision: a technical approach, a framework or library, a third-party API, a performance claim, a platform capability, an interaction that might not work. Not for these:

- Building the real thing the real way: `/app-dev-story`.
- Choosing or evaluating a stack or dependency on paper: `/app-stack` (it may ask for a prototype and come back).
- Proving the whole path through the finished foundation (a walking skeleton): that is foundation-stage work planned with `/app-plan`, not a spike.
- Hunting a bug: `/app-bugfix`.

## Inputs

- Required: `studio.yaml` (orchestration.md section 1). Without it, offer `/app-adopt` or `/app-start` and stop.
- Required: a question. If none is given, ask for it in plain text (Phase 1). Never pick one for the user.
- Optional, read when present: the brief or vision, the relevant spec, `docs/architecture/architecture.md`, `docs/stack-reference.md`, existing ADRs, and any `prototypes/*/` carry-forward note from an earlier PIVOT.

## Phase 1: Define the question and the signal

Who: the main session with the user. Write nothing yet.

1. If `prototypes/index.md` or a `PIVOT-NOTE.md` exists for this idea, read it and start from its revised hypothesis. Say which note you used. Count earlier PIVOT verdicts for the same idea; at three, do not plan a fourth build: ask whether to KILL (Rules).
2. Settle, in the user's words, three things:
   - **The question**, as "Can we <do X> using <approach Y> within <limit Z>?" or "If the user <does X>, will <outcome Y> hold?" A question that cannot be answered yes or no is too vague; narrow it.
   - **The signal**: the measurable result that answers it, stated before building. Examples: p95 latency under a number over N requests, the sync completes after 10 minutes offline, the import handles a 100 MB file without exceeding a memory ceiling, 5 of 5 testers finish the task unaided, the vendor API returns the field we need. "It feels good" is not a signal unless a human will judge it and the report says so.
   - **The riskiest assumption**: build the part that could kill the idea first, not the easy part.
3. Ask for the timebox with AskUserQuestion: `4 hours (Recommended for a technical question)`, `1 day (a UX or multi-part question)`, `Other`. Anything over one day means the question is too big; split it.
4. Choose the kind, which sets how the answer is observed:

| Kind | Typical question | How it is observed |
|---|---|---|
| Technical feasibility | Does this approach, library or API work for us | Running the minimal code, measured output |
| Performance or scale | Can it meet a budget on the target | Numbers from a repeatable run on the target class of hardware |
| Integration | Does the third-party service give us what we need | Real calls against a sandbox account (never production data), captured responses; a paid or metered service the app does not already use needs the user's yes first |
| Interaction or UX | Will users get through this flow | A clickable build in front of a person, observed |
| Platform capability | Does the OS or store allow it | Run on the real OS or simulator, captured screenshot or log |

Check: the question, signal, riskiest assumption and timebox are stated back to the user in four lines and the user agreed.

## Phase 2: Plan and announce

Print the announce block (orchestration.md section 2). Agents: `prototyper` builds; the lead who owns the question reviews feasibility: `web-lead`, `desktop-lead`, `mobile-lead`, `backend-lead` or `platform-lead`, chosen from the app's `platforms` and the kind of question. Language or platform specialists from `studio.yaml` `specialists:` only if the question is inside their area. Gates: none (prototypes are not gated).

Write the plan to `prototypes/<name>/PLAN.md` (new file, so no ask is needed beyond the user's approval of the plan itself): question, signal, riskiest assumption, minimum build, what is explicitly cut (error handling, auth, styling, tests beyond the one that measures the signal, packaging), timebox, and where evidence will be saved. List what outside the folder the spike will touch. The default is nothing. If it must touch the app's existing source, config or build files, list those files and ask once (orchestration.md section 3); the preferred answer is to copy what is needed into the prototype folder.

Ask the user to approve the plan. Checkpoint to `.studio/state.md` (section 9).

Check: `prototypes/<name>/PLAN.md` exists with all six parts filled.

## Phase 3: Build

Who: `prototyper`, briefed per orchestration.md section 3. The brief states: work only inside `prototypes/<name>/`; no imports from production source and none into it; no real credentials, production data or personal data (use fixtures and sandbox accounts); disposable dependencies are fine but each is listed with its license in the plan so a later PROCEED can be checked; stop at the timebox and report what was learned rather than overrunning; log every shortcut taken as a line in `prototypes/<name>/SHORTCUTS.md`, because that list becomes the "rebuild properly" section.

If the prototyper reports BLOCKED, or stuck for half the timebox, ask the user: reframe the question, switch approach, or stop with NOT ASSESSED.

Check, by the main session, not the agent's word:

1. The folder exists and has runnable content, not only notes.
2. Isolation: Grep the app's source and build config for the prototype folder name and for imports reaching into `prototypes/`; and Grep the prototype for relative imports escaping its folder. Any hit is a failed check; have it fixed.
3. `SHORTCUTS.md` exists and is not empty.

## Phase 4: Run and observe

Who: `prototyper` runs it; the main session verifies. Run it the way it will be used and capture the signal, following orchestration.md section 10 (without stealing focus; headless browser for web, offscreen window capture for desktop, simulator or emulator for mobile, request and response capture for services and APIs). Save raw evidence to `prototypes/<name>/evidence/`: numbers with the command that produced them and the machine class, screenshots, response captures, logs. Repeat a measurement at least three times (at minimal rigor one run is acceptable if the report calls it an anecdote). Heavy runs (load tests, large builds, emulators) go through `~/Tools/agent_locks/run_locked.sh cpu <command>` (`gpu` for windowed or GPU work) when that helper exists, otherwise one at a time; exit code 75 means the user is gaming, so stop and report NOT VERIFIED for what did not run. Never take focus or inject input on the user's desktop.

For a UX or interaction question, the build is handed to a person: give the user the exact command or URL and wait. If nobody can try it this session, do not infer an answer from how it looks. The recommendation is NOT ASSESSED (built, not tried).

Report the run as one line: `Run result: OBSERVED - <what was seen, evidence path> | NOT VERIFIED - <why> | N/A - <why nothing is observable>`. A technical or UX question is never N/A.

Check: `prototypes/<name>/evidence/` has files that the report can cite.

## Phase 5: Debrief and decide

Who: the main session with the user.

1. Compare the evidence with the signal from Phase 1, in plain text: signal met, partly met, not met, or not measured. Quote the numbers.
2. Name what surprised you and what the prototype did not test (a local run says nothing about production load, real network conditions or real device fleets; say so when it applies).
3. Recommend one of PROCEED, PIVOT or KILL with reasons. Then ask the user with AskUserQuestion, recommended option marked. A skipped answer is not an answer; ask again.

| Verdict | Meaning | Required content |
|---|---|---|
| PROCEED | The question is answered yes within the limits | What must be rebuilt properly (from `SHORTCUTS.md`), the decision it supports (ADR, stack choice, spec), residual risks |
| PIVOT | The core is sound but the approach or question must change | The revised question and hypothesis; written to `prototypes/<name>/PIVOT-NOTE.md` for the next run |
| KILL | The answer is no, or the cost is out of proportion | Why, what was learned, and what to do instead (another approach, cut the feature, change the brief) |
| NOT ASSESSED | The prototype was built but the question was not answered | What is missing (not tried by a person, not measured on the target, blocked) and who can supply it |

## Phase 6: Report and index

Who: the main session writes; `prototyper` may draft. Use `templates/prototype-report.md`. Write `prototypes/<name>/REPORT.md` using the template's sections (Question, Hypothesis, What was built, Shortcuts taken, Measurements and observations, Verdict, What must be rebuilt, Next), and include the signal, kind, timebox and time spent, evidence paths, licenses of any dependencies tried, and the Run result line. Append one row to `prototypes/index.md` (create it if missing): name, date, question, verdict, link. If earlier PIVOTs exist for the idea, note the chain.

Check: the report file exists with every section filled (no placeholders); the index row exists.

Ask before cleanup: the prototype folder is kept by default as a record. Delete it only on the user's yes. Never move prototype code into production folders.

## Rigor and review mode

Rigor never changes whether the question gets answered.

| | minimal | standard | full |
|---|---|---|---|
| Plan file | 4 lines inside the report | `PLAN.md` | `PLAN.md` with lead review before the build |
| Evidence | one captured result | three repeated measurements or a recorded session | plus the conditions that were not tested, listed |
| Lead review of feasibility | skipped | on PROCEED | before building and on PROCEED |

Review modes: no gates run at any mode (`Gates: none run`). At `full`, a PROCEED that adopts a framework or dependency should be followed by `/app-stack` with `TD-STACK`.

## Verdicts

First match wins. Rank: NOT ASSESSED sits below KILL and PIVOT and above PROCEED, so a decision never reads as a pass without evidence.

1. KILL: the user chose KILL, or the signal was measured and not met and no revised approach is worth trying.
2. PIVOT: the user chose PIVOT and `PIVOT-NOTE.md` exists.
3. NOT ASSESSED: no Run result of OBSERVED for the signal, a UX question nobody tried, a measurement taken on something other than the target class, the plan changed the question mid-build, or the isolation check failed and was not fixed. Say which.
4. PROCEED: the signal was met on observed evidence and the rebuild list exists.

## Report

```
Prototype: <name>   Question: <one line>
Timebox: <planned> / <spent>   Kind: <kind>
Signal: <stated signal> -> <result with numbers>
Run result: <one line>
Isolation check: <passed / failed + hits>
Rebuild properly: <n items, or none>
Verdict: <WORD> - <one line why>
Gates: none run (<mode>)
Wrote: <paths>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- One question per prototype. If a second question appears, record it and start another run.
- Prototype code is never imported by production code and never promoted into it; PROCEED means rebuild.
- No real credentials, production data or personal data in a prototype. Sandbox accounts and fixtures only; a sandbox key is read from the environment by name and never written into the prototype folder, the report or the evidence.
- No polish: no styling, packaging, full error handling or broad tests beyond what measures the signal.
- The signal is written before the build. Changing it afterward is recorded as a change in the report, never done silently.
- Three PIVOTs on the same idea force an explicit KILL decision: ask whether continuing is sunk cost.
- A prototype nobody ran or tried is NOT ASSESSED, whatever it looks like.
- Never decide the verdict for the user, and never skip a dismissed question.
- Never start the next skill automatically.
