---
name: app-adopt
description: "Bring an existing app under the studio without moving anything: detect the stack from manifests, find and verify the real build, test and lint commands, map existing docs into paths, reverse-document the architecture, write the stack reference, detect the stage with evidence, and produce a gap report. Use when the user has an existing codebase or live app, says 'adopt', 'take over', 'set up the studio for this repo', or runs the studio on an app that has no studio.yaml."
argument-hint: "[app folder] [--review solo|lean|full] [--refresh]"
user-invocable: true
---

# App Adopt

The studio's entry for an app that already exists. It reads what is there, writes what the studio needs to work on it (`studio.yaml`, an architecture document, a stack reference, an adoption report), and leaves everything else exactly where it is. The point is to replace guesses with evidence: every command in `commands:` was run and observed, every stack fact comes from a manifest or lock file, every stage claim cites what was found, and everything that could not be established is named as a gap.

Writes: `studio.yaml` (template `studio.yaml`), `docs/architecture/architecture.md` (template `architecture.md`, marked as documented from code), `docs/stack-reference.md` (template `stack-reference.md`), `docs/qa/adoption-report.md`, `.studio/state.md`, and a `.gitignore` line for `.studio/` only after asking. Paths follow the app's own layout wherever it already has one (see Phase 2).
Next: usually `/app-team-audit`, then the skills the adoption report ranks (`/app-test-setup`, `/app-security-audit`, `/app-upgrade`, `/app-adr` retrofits, `/app-spec` retrofits).

## When to use and when not to

- Use for any app with code, whatever the age, language or platform, including a live app with users.
- No code yet: use `/app-start`. Already adopted and only a refresh is needed: pass `--refresh` (Phase 0).
- This skill documents and verifies. It does not fix, upgrade, refactor or migrate; the report recommends the skills that do.

## Inputs

- The app folder (argument, else the current folder). It must be a folder the user owns and wants adopted; ask if unclear.
- Nothing is required to exist beyond source files. A missing README, CI file or test suite is a finding, not a blocker.
- Optional: the user's own notes on how to build and run it. Treat them as candidates to verify, not as truth.

## Hard rules for the whole run

- **Nothing is moved, renamed, deleted or reformatted.** Existing files are read only, with two exceptions that need the user's yes in Phase 2: appending `.studio/` to `.gitignore`, and filling an existing `studio.yaml` on `--refresh`.
- **Only new files are written**, at the paths in the Phase 2 approval. If a target path already exists, do not overwrite it: write beside it with `.adopted` before the extension and tell the user, or use the mapped existing path.
- **Verification must not change the app's data or the world.** No migrations, deploys, publishes, database resets, installs without a yes, or commands that send anything out. Heavy runs go through the run lock (`rules-full.md`, "Keep the machine usable"): `~/Tools/agent_locks/run_locked.sh cpu <command>` when it exists, `gpu` for anything that opens a window or uses the GPU, and exit 75 means the user is gaming: stop and report what remains. Where the helper does not exist, heavy runs go one at a time.
- **No secrets in any written file or report.** A secret found committed is reported as file and line only.
- **Scratch output goes to `~/AgentScratch/adopt-<app>/`**, never into the repo.

## Phase 0: Resolve and plan

Main session. Orchestration section 1 with these changes: a missing `studio.yaml` is the normal case here. If `studio.yaml` exists, this is a re-adoption: require `--refresh` or ask; in refresh mode every value already in the file is kept and shown beside the newly detected one, and only the user's per-field yes changes it.

1. Read `.studio/state.md` if present and offer to resume an unfinished adoption from its checkpoint.
2. Confirm the folder is a git repository (`git -C <app> rev-parse --is-inside-work-tree`). If it is not, say the git-based counts will be replaced by a bounded listing and the denominators will say so. Record `git -C <app> status --short` and the current branch; a dirty tree is allowed but is noted in the report.
3. Rigor: ask with AskUserQuestion, with a recommendation inferred from evidence (CI present, tests present, users or releases) and a one-sentence trade-off each. Adoption never defaults rigor. Review mode follows rigor unless `--review` is given.
4. Print the plan block from orchestration section 2. Agents this run: `build-engineer` (commands), `modernization-engineer` (architecture and stack reference), `principal-engineer` (review), the platform lead for each platform found (`web-lead`, `desktop-lead`, `mobile-lead`, `backend-lead`, plus `platform-lead` when hosting or CI is significant). Gates: none run (this skill defines no gate).

## Phase 1: Detect (read-only, main session)

Establish facts with the file that proves each one. An undetectable fact is `unknown`, never a guess.

Enumerate files with `git -C <app> ls-files` (respects ignore rules, fast) and filter by name and extension. Without git, Glob only named manifests at the root and in `apps/`, `packages/`, `services/`, `src/`, one level each. Never walk dependency or build folders.

| Evidence file(s) | Tells you |
|---|---|
| `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lock*`, `tsconfig.json`, `deno.json` | JS or TS, package manager, runtime; frameworks from dependencies |
| `Cargo.toml`, `Cargo.lock`, `rust-toolchain*` | Rust, workspace layout, edition, toolchain pin |
| `pyproject.toml`, `requirements*.txt`, `uv.lock`, `poetry.lock`, `Pipfile.lock` | Python, packaging tool, frameworks |
| `go.mod`, `go.sum` | Go and module path |
| `*.sln`, `*.csproj`, `Directory.Packages.props`, `global.json`, `packages.lock.json` | .NET, target frameworks, UI stack (WinUI, WPF, MAUI, ASP.NET) |
| `build.gradle*`, `settings.gradle*`, `gradle/libs.versions.toml`, `pom.xml`, `AndroidManifest.xml` | JVM or Android, Kotlin or Java, Gradle or Maven |
| `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, `Podfile.lock`, `Info.plist`, `*.entitlements` | Swift, Apple platforms, targets |
| `pubspec.yaml`, `pubspec.lock` | Flutter or Dart |
| `CMakeLists.txt`, `vcpkg.json`, `conanfile.*`, `*.pro` | C or C++, build and package manager, Qt |
| `src-tauri/tauri.conf.json`, `electron-builder*`, `forge.config.*` | Tauri or Electron desktop shell |
| `manifest.json` with `manifest_version` | Browser extension |
| `Dockerfile*`, `compose*.y*ml`, `*.tf`, `k8s/`, `helm/`, `wrangler.toml`, `vercel.json`, `fly.toml`, `Procfile` | Hosting and deployment method |
| `.github/workflows/`, `.gitea/workflows/`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`, `fastlane/` | CI and release automation |

Derive and record, each with its evidence file:

- **Languages and frameworks**, and the runtime or SDK pins (`engines`, toolchain files, `global.json`, `.nvmrc`, `.python-version`, `.tool-versions`).
- **Platforms** (`studio.yaml` values): web, windows, macos, linux, ios, android, backend, cli, extension, library. A desktop shell on a web stack is `[<os>, web]` only if it also ships as a website; otherwise just the desktop OS values. Ambiguity is asked about, not guessed.
- **Data stores and hosting**, from dependencies, migration folders, compose files and IaC.
- **Min targets**: from `minSdk`, deployment targets, `browserslist`, MSIX or installer manifests, `engines`. If none, leave empty.
- **Size**: tracked source files by extension and total, with the denominator (for example "212 source files of 1,040 tracked files").
- **Multiple deployables** (several apps in one repo): ask whether this is one app with several platforms or several apps to adopt separately.
- **Existing docs** (Phase 2 input): README, CONTRIBUTING, `docs/`, ADR folders, a `DECISIONS` file, changelog, issue templates, runbooks, an issue tracker reference.
- **Git facts for the stage**: tags and release branches (`git tag --list` limited to the latest 10), last commit date, commit count in the last 90 days, number of authors.

Check: write the detection table to `~/AgentScratch/adopt-<app>/detect.md`. If no manifest or build file is found at all, or the language cannot be determined, stop with NOT ASSESSED and ask the user to point at the source.

## Phase 2: Map docs into `paths:` and ask for approval

For each studio document type in `layout.md`, find the app's existing equivalent by name and by headings (Glob `docs/**`, root `*.md`, ADR folders; Grep headings only). Build the mapping table: studio key, existing location (or "none"), action.

- Existing doc present: set `paths.<key>` to it. Nothing is moved. If a doc type is split across many files (ADRs, specs), map the folder.
- No equivalent: the studio default path is used when that doc is first created, and the report lists it as absent.
- The architecture key is special: if an architecture document already exists, `docs/architecture/architecture.md` is not created. The reverse-documentation in Phase 4 then produces a drift list (what the existing document says versus what the code shows), written into the adoption report, and `paths.architecture` points at the existing file.

Before the card can list commands, run the read-only half of Phase 3 now: `build-engineer` performs Steps 1 and 2 of `references/2-commands.md` (find and classify candidate commands; nothing is run) and returns the candidate table. Also check by listing whether dependencies appear to be installed (for example a populated `node_modules/`, a `target/` or virtual environment folder, a restored package cache; test for existence only, never walk them).

Show the plan card, then ask once for the whole set with AskUserQuestion (one call, up to three questions):

1. "Write these files and run the verification commands below?" Show: files to write with paths; the `paths:` mapping; every command to be run, each marked light or heavy, plus whether dependencies appear to be installed. Options: `Yes (Recommended)` / `Change the list first` / `Stop`.
2. "Add `.studio/` to `.gitignore`?" `Yes (Recommended)` / `No`.
3. Only if dependencies are missing: "Dependencies are not installed. Verification needs them. May I install them with `<command>`?" `Install` / `Skip verification of commands that need them`. An install is a heavy run through the lock and is never done without this yes.

A skipped answer is not a yes. After a yes, write `studio.yaml` as a draft (app, platforms, stack, modes, paths, specialists; `commands:` and `stage:` still empty) and the `.studio/state.md` checkpoint. `specialists:` comes from platforms plus languages found, using agent names from `roster.md` only.

## Phase 3: Commands (build-engineer)

Read `references/2-commands.md` now and follow it. Read it again if the conversation was compacted during this phase.

Steps 1 and 2 already ran in Phase 2; this phase runs Steps 3 to 5 on the approved list. Purpose: fill `commands:` (`build`, `build_release`, `test`, `lint`, `format`, `run`, `e2e`, `screenshot`) only with commands that were found in the repo's own sources and then actually run and observed. Phase 3 and Phase 4 run in parallel (heavy commands inside Phase 3 still go one at a time through the lock).

## Phase 4: Reverse-document and stack reference

Read `references/4-reverse-document.md` now and follow it.

Purpose: `modernization-engineer` writes the architecture document from code and a separate instance writes the stack reference from lock files; the reviewers check both against the code. The architecture document starts with the template's `DOCUMENTED FROM CODE, NOT DESIGNED.` banner and carries its Provenance table, and every claim cites a file.

## Phase 5: Detect the stage with evidence (main session)

Existing apps enter at `foundation`, `build` or `operate`. `hardening` and `release` are never inferred; only `/app-gate` moves an app there. Evidence table:

| Observed | Points to |
|---|---|
| Source present, build passes, no tests, no CI, few features | `foundation` |
| Active feature work: commits in the last 90 days, open branches, issues or stories, tests present | `build` |
| Released: version tags or release branches, changelog entries, store or deploy config, running hosting, users known to the user | `operate` (with `build` if feature work is also active) |
| Recorded stage differs from the evidence (refresh) | report both and flag the disagreement |

Both `build` and `operate` are common (a live app under development). Show the evidence, state the pick and the runner-up, and ask the user to confirm with AskUserQuestion; the user knows whether people are using it. Only after the answer, write `stage:` to `studio.yaml`. If git history is unavailable, the stage evidence is thinner: say so and ask without a recommendation.

## Phase 6: Finalize `studio.yaml`

Fill `commands:` from the verified results in `~/AgentScratch/adopt-<app>/commands.md`. A command that was found but not verified is recorded only if the user chooses to in a single grouped question, as a line with a trailing comment `# unverified: <reason>`; the default is to leave it empty and list it in the report. Add `rules:` only for standing rules the user stated or the repo's own contributor docs state clearly (for example "run the release build after UI changes"); quote them. Read the file back and check it against the Phase 1 facts.

## Phase 7: Adoption report

Read `references/7-report.md` now and follow it. The main session writes `docs/qa/adoption-report.md`; it is the gap report and the artifact the verdict turns on.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Stack reference | runtimes, SDKs, direct dependencies that shape the code | all direct dependencies with locked versions | plus license and support status per dependency, checked against official sources |
| Architecture document | context, components, data, build and run | the full `architecture.md` template, sections the code supports | plus deployment, trust boundaries, observability, budgets (as found or `NOT DOCUMENTED`) |
| Gap report | missing artifacts and unverified commands | adds quick checks per audit lens | adds the lens-by-lens table with the audit skill to run for each |

| Review mode | Review pass in Phase 4 |
|---|---|
| solo | main session spot-checks five claims in each document against the code; the skipped agent review is announced |
| lean | `principal-engineer` reviews both documents |
| full | `principal-engineer` and each platform lead review their sections, in parallel |

Rigor changes what must exist, never what must work: commands are verified at every rigor.

## Verdicts

First match wins.

- **BLOCKED:** the folder cannot be read; the user declines the write approval and nothing can be produced; a required agent artifact is missing after one re-brief; the run lock reported exit 75 before anything was verified.
- **NOT ASSESSED:** the stack could not be determined (Phase 1); or neither `build` nor `test` was verified (no runnable command found, dependencies could not be installed, user declined the runs, or heavy runs were stopped by the lock) so the core claim of adoption, a working command set, is unproven; or the stage could not be evidenced and the user did not answer. The report states which reason applied.
- **COMPLETE WITH GAPS:** `studio.yaml` and the documents were written, but one or more of: `lint`, `run`, `format` or `e2e` unverified or absent; a doc type that could not be mapped; claims marked `INTENT UNKNOWN` or `UNVERIFIED` in the architecture document; a reviewer that did not run. The gaps are listed with counts and denominators.
- **COMPLETE:** `build` and `test` verified, `lint` verified or confirmed absent by the user, every file written and read back, reviews as the mode requires, stage confirmed, no unresolved mapping.

## Report

Print a summary of the adoption report, then the closing block from orchestration section 8.

```
App: <name> (<path>)   Stage: <stage>   Rigor: <rigor>   Review: <mode>
Stack: <languages, frameworks, platforms>   (evidence: <manifests>)
Commands verified: <n> of <n> found (build <ok|no>, test <ok|no>, lint <ok|no>, run <ok|unverified>, ...)
Docs mapped: <n> of <n> types   Left in place, nothing moved: yes
Documented from code: architecture (<n> claims, <n> INTENT UNKNOWN), stack reference (<n> dependencies)
Gaps: <n> (top three, one line each)
Not run: <step> (<why>)
```

```
Verdict: <WORD> - <one line why>
Gates: none run (adoption defines no gate)
Wrote: <paths>
Next: /app-team-audit (<why>), then <ranked skills from the report>
```

## Rules for this skill

- Never move, rename, reformat or delete a file. Never overwrite one.
- Never record a command in `commands:` that was not run and observed, and never record an exit-code-only pass for tests that ran zero tests.
- Never infer `hardening` or `release`.
- Never present the reverse-documented architecture as intent. Mark what is read from code, and mark what is unknown.
- Never run migrations, deploys, publishes or anything that could change real data; never open windows or inject input into the desktop to verify `run` or `screenshot` unless the user said yes to that specific command.
- Never commit. Suggest the exact paths to stage and a Conventional Commits subject, and leave it to the user.
- Record that every count has a denominator, and that every skipped step is announced in the report.
