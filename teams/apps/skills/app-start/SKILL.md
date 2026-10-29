---
name: app-start
description: "Onboard a new app into the studio: capture the idea, choose platforms and rigor, write studio.yaml and the one-page brief, and name the first steps. Use when the user starts a new app or idea (web, desktop, phone, backend, CLI), asks where to begin, or has a spec but no studio setup. Existing code goes to app-adopt."
argument-hint: "[app name or folder] [--review solo|lean|full]"
user-invocable: true
---

# App Start

The front door for a new app. It routes the user (fresh idea, a spec already written, or existing code), captures the idea in plain language, asks the questions that shape the project (platforms, rigor, who it is for), and then writes the app's studio files so every other skill has something to read. It decides nothing technical on the user's behalf: an unknown stack stays empty in `studio.yaml` until `/app-stack` or the user fills it.

Writes: `studio.yaml` (template `studio.yaml`), `docs/product/brief.md` (template `product-brief.md`), `.studio/state.md` (template `session-state.md`), a `.gitignore` line for `.studio/` (only after asking). The studio's own docs and templates live under `.claude/studio/` (workspace or `~/.claude/`).
Next: `/app-brief` (standard and full rigor), `/app-stack` (stack undecided), `/app-spec` (first feature), `/app-adopt` (if existing code turns up).

## When to use and when not to

- Use for an app that does not exist yet, or exists only as an idea, notes or a spec document.
- Existing code, a repo with commits, or a live app: stop and hand off to `/app-adopt`. It maps what is there instead of starting over.
- The app already has a `studio.yaml` with a `stage:`: this is a returning user. Say what is recorded and send them to `/app-help`.

## Inputs

- The skill argument (an app name or folder), else the current folder, else ask. Each app is its own git repository, so one folder per app.
- Optional: a spec, notes, sketches or an existing README the user points at. Read them; they shorten the questions.
- Nothing else is required. A missing answer is asked for, never assumed. An answer the user cannot give yet (for example the stack) is left empty and named in the report.

## Phase 1: Read the situation

Main session, read-only, no agents. Orchestration section 1 does not apply yet (there may be no `studio.yaml`).

1. Resolve the target folder. If it does not exist, note that it will be created after the write approval in Phase 5. If it exists, list its top level (Glob `*` there, not a recursive walk).
2. Look for: `studio.yaml`, `.studio/state.md`, `docs/product/`, a `.git` folder, and source or manifest files at the top level and one level down (`package.json`, `Cargo.toml`, `pyproject.toml`, `requirements.txt`, `go.mod`, `*.csproj`, `*.sln`, `pom.xml`, `build.gradle*`, `Gemfile`, `composer.json`, `pubspec.yaml`, `Package.swift`, `*.xcodeproj`, `CMakeLists.txt`, `Makefile`). For a git repo, `git -C <folder> log --oneline -n 5` and the count from `git -C <folder> ls-files` give a safe size read. Never run `find`, `du` or a recursive grep over the folder.
3. Decide the situation:

| Found | Situation |
|---|---|
| `studio.yaml` with a `stage:` value | Returning user: report the recorded stage and rigor, recommend `/app-help`, stop |
| `studio.yaml` without a stage, or only `.studio/` | Interrupted start: read `.studio/state.md`, offer to resume at the recorded step |
| Source files, manifests or more than a handful of commits | Existing code: recommend `/app-adopt` and ask (Phase 2) before going on |
| Only docs, notes or a spec | Have a spec: continue, with the documents as input |
| Empty folder or no folder | Fresh idea: continue |

Keep what you found for Phase 2. Do not show it as a list; use it to check the user's answer.

## Phase 2: Ask where the user is

Ask with AskUserQuestion: "Where are you starting from with this app?"

- `Fresh idea` (a problem or a rough thought, nothing written yet)
- `Have a spec or notes` (documents exist, no code)
- `Existing code` (go to `/app-adopt`)
- `Not sure`

If the answer contradicts Phase 1 (existing code chosen on an empty folder, or fresh idea with a populated repo), say what was found once and ask again. For `Existing code`, say "Type `/app-adopt <folder>` to continue" and stop with Verdict COMPLETE (routed, nothing written). For `Not sure`, ask the user to describe the situation in plain text and route from that.

## Phase 3: Capture the idea

Plain-text questions, a few at a time, then restate the idea in four lines and ask whether that is right. Ask only what the documents do not already answer.

1. What is it, in one sentence, and who is it for? (If the user has no idea yet: offer two or three directions as one-line concepts with a different user and problem each, and let them pick, combine or discard. Do not invent a market.)
2. What problem does it solve, and what do those people do today instead?
3. What are the three to seven things the first version must do? (More than seven: push back, propose cuts, move them to out of scope.)
4. What is deliberately not in the first version?
5. Any hard constraints: deadline, budget, a service it must use, data it must protect, a person or team that will use it first.

Spawn nothing here. The questions are the product work; agents come in only when the user asks for a recommendation.

## Phase 4: Platforms, rigor and stack

All decisions in this phase use AskUserQuestion, asked in every mode, one grouped call where the questions are independent.

**Platforms** (multi-select): web, desktop (then which of Windows, macOS, Linux), phone or tablet (then iOS, Android, or both), backend or API, command line, browser extension, library. The platforms drive which specialists and leads the studio uses, so ask follow-ups until each chosen platform is concrete. Record them in `studio.yaml` using only the allowed values (web, windows, macos, linux, ios, android, backend, cli, extension, library).

| Platform chosen | Also ask | Add to `specialists:` (examples; fit to the stack) |
|---|---|---|
| web | Single-page app, server-rendered, or content site? Needs offline or install? | `frontend-engineer`, `ui-engineer`, `web-framework-specialist` |
| windows, macos, linux | Native, or a web-tech or cross-platform shell? Installer and auto-update wanted? | `windows-desktop-engineer`, `macos-engineer`, `linux-desktop-engineer`, `hybrid-desktop-engineer`, `desktop-packaging-engineer` |
| ios, android | Native per platform, or one shared codebase? Oldest OS or device to support? Store release planned? | `ios-engineer`, `android-engineer`, `cross-platform-mobile-engineer`, `app-store-specialist` |
| backend | Who calls it (own clients or third parties)? Where does data live? Where will it run? | `backend-engineer`, `api-designer`, `database-engineer`, `infrastructure-engineer` |
| cli, library | Who installs it, and how is it distributed? | the language specialist, `tools-engineer` |
| extension | Which browsers? | `web-platform-engineer` |

**Rigor** (`standards/rigor.md`): infer a recommendation from what the user said, then ask. Mark the inferred option `(Recommended)` and give a one-sentence trade-off each.

| Signals in the user's words | Recommend |
|---|---|
| personal tool, weekend, prototype, "just trying", single user | `minimal`: one-page brief, coarse stories, light gates |
| other people will use it, it will be released, one clear core flow | `standard`: vision, specs, architecture, stack reference before code |
| money, personal data, regulated domain, several platforms or teams, "must not break" | `full`: everything in standard plus security, privacy, accessibility and performance evidence |

An unclear signal is never defaulted to the cheaper answer: ask. Review mode follows rigor unless the user wants otherwise or passed `--review`; state which mode results (`minimal` gives `solo`, `standard` gives `lean`, `full` gives `full`) and that `/app-help` shows how to change it.

**Stack.** Ask: "Do you already have a language, framework or hosting in mind?" Options: `Yes, I will tell you` / `Help me choose (Recommended when unsure)` / `Decide later`. If the user names a stack, record it exactly as said. If they want help, spawn `technical-director` per orchestration section 3 with the idea, platforms, constraints and rigor, asking for two or three viable stacks with the deciding trade-offs and which `/app-stack` checks to run, returned in the reply (it writes nothing). Present the options and let the user choose or defer. A deferred stack stays empty and `/app-stack` is the next recommended skill.

**Minimum targets.** Ask for the oldest OS, browser or device to support. If unknown, leave `min_targets` empty and say so.

## Phase 5: Show the card, then write

Print the card, then ask once for the whole file set.

```
App: <name> (<folder>)
Summary: <one line>
Platforms: <list>     Stack: <list or "not decided">     Min targets: <value or "not set">
Rigor: <value>        Review: <mode>        Stage: discovery
Specialists: <list>
Will write: studio.yaml, docs/product/brief.md, .studio/state.md   (and create <folder> / git init if absent)
Gitignore: add ".studio/" to <folder>/.gitignore   (asked separately)
Not written: anything outside <folder>
```

Ask (one call, two questions): (1) "Write these files?" `Write them` / `Change something first` / `Do not write`; (2) "Add `.studio/` to `.gitignore`?" `Yes (Recommended)` / `No, I will handle it`. A skipped answer is not a yes. Run `git init` only if the folder is not a repository, and only because the card said so and the user answered `Write them` to question (1); never add a remote and never commit.

On yes:
1. Create the folder if needed. Write `studio.yaml` from `.claude/studio/templates/studio.yaml`: fill `app`, `platforms`, `stack` (empty values stay empty), `modes`, `specialists`, and set `stage: discovery`. `commands:` stays empty (no code exists yet); `paths: {}`; `rules:` empty unless the user stated a standing rule. Add nothing the user did not say.
2. Write `docs/product/brief.md` from `.claude/studio/templates/product-brief.md` using the Phase 3 answers verbatim where possible. Add a closing section `## Foundation plan` (below).
3. Write `.studio/state.md` from `templates/session-state.md` with the CHECKPOINT block filled (task: app start, last result, next step).
4. Apply the `.gitignore` answer. Append the line to an existing file with the Edit tool; create the file if absent; never rewrite existing lines.

**Foundation plan** (`product-manager`, spawned per orchestration section 3 at `standard` and `full`; the main session writes it at `minimal`): the ordered steps from here to a walking skeleton on every chosen platform, in the studio's own skills, for example choose the stack, spec the first feature, write the architecture (standard and up), set up tests and CI, build the thinnest end-to-end path. Five to eight lines, each naming the skill. Include the platform-specific foundation items: store developer accounts and signing for phone and desktop distribution, a hosting target for services, browser support list for web. The agent returns the text; the main session appends it to the brief.

Check that the phase really happened: Read back `studio.yaml` and the brief; both exist, no placeholder text from the template remains in a filled field, and `stage` is `discovery`. A field that was left empty on purpose stays empty (not a placeholder).

## Phase 6: Hand off

Show the path for the chosen rigor, then recommend exactly one next skill. Never start it.

| Rigor | Path to running code |
|---|---|
| `minimal` | `/app-stack` (if undecided), `/app-spec` for the first feature (or go straight to `/app-plan`), `/app-test-setup`, `/app-dev-story` |
| `standard` | `/app-brief` (grow the brief into a vision), `/app-spec` per MVP feature, `/app-architecture`, `/app-stack`, `/app-test-setup`, `/app-plan`, `/app-dev-story`, with `/app-gate` between stages |
| `full` | Standard, plus `/app-ux`, `/app-design-language`, `/app-threat-model`, `/app-privacy-review` before build |

Say once: rigor changes what must exist before the next stage, never what must work; the user can change `modes.rigor` in `studio.yaml` at any time. Finish with the one-line hand-off: "Type `<skill>` to begin."

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Questions in Phase 3 | the five, briefly | the five, plus success measure and riskiest assumption | plus compliance and data questions (what personal data, which regions) |
| Brief | one page | one page now, `/app-brief` extends it | same as standard |
| Agents | none unless the user wants a stack recommendation | `technical-director` (if help requested), `product-manager` | adds `product-director` to sanity-check scope against the stated problem |
| Gates | none | none | none (this skill runs no gate; `/app-gate` advances the stage) |

## Verdicts

First match wins.

- **BLOCKED:** the user will not or cannot name the app's purpose and target user after being asked twice; the folder cannot be created or written; `studio.yaml` exists with a stage and the user insists on overwriting it (offer `/app-help` or editing by hand instead); an agent artifact the run depends on is missing after one re-brief.
- **COMPLETE:** all files in the card were written and read back. The report lists every field left empty on purpose. Routing to `/app-adopt` with nothing written is also COMPLETE, and the report says "routed, nothing written".

This skill has no NOT ASSESSED state because it asserts nothing about an existing app; the report still names what was not decided.

## Report

```
App: <name> (<folder>)   Stage: discovery   Rigor: <rigor>   Review: <mode>
Idea: <one line>
Platforms: <list>   Stack: <list or "not decided">   Specialists: <list>
Written: <paths>   Gitignore: <added | declined | already present>
Left empty on purpose: <fields, or none>
Decisions still open: <e.g. stack, min targets, store accounts>
```

Then the closing block from orchestration section 8:

```
Verdict: <WORD> - <one line why>
Gates: none run (this skill runs no gates)
Wrote: <paths, or none>
Next: </app-skill ...> (<why>)
```

## Rules for this skill

- Never touch a folder that has code: route to `/app-adopt`.
- Never choose the stack, platforms, rigor or review mode for the user. Recommend and ask.
- Never write outside the app's folder, never add a git remote, never commit, never push.
- Never advance the stage past `discovery`; `/app-gate` owns that.
- Never write credentials, account names or machine paths into `studio.yaml` or the brief.
- Never start the next skill; print its name.
- Scan every file written for U+2014 and U+2013 before finishing; the user's workspace rule forbids em dashes.
