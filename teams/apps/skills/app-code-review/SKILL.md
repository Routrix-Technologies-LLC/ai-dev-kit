---
name: app-code-review
description: "Independent multi-lens review of a diff, branch, pull request or path: code-reviewer plus the language and platform specialists, plus security-engineer for sensitive code, in parallel, with every finding verified before it is reported. Use when the user asks for a code review, a review before merge, a second look at a change, or after /app-dev-story and before /app-story-done."
argument-hint: "[app] [target: diff | branch | PR number | path] [story-path] [--review solo|lean|full]"
user-invocable: true
---

# App Code Review

Reviews a change the way an independent senior engineer would: several lenses read the same code at the same time, and then the main session checks every claim against the code before putting it in the report. Specialist output is a lead, not a verdict: a fluent finding that falls apart when the inputs are enumerated is dropped, and one that cannot be checked is labeled so.

Writes: `docs/qa/reviews/<date>-<scope>.md` from `templates/code-review-report.md`. Edits no source.
Next: fix the required changes with `/app-dev-story` or `/app-bugfix`, then `/app-story-done`.

## When to use and when not to

- Use for a diff, branch, PR or set of files before it merges or before its story closes.
- Not for a whole-app health check (`/app-team-audit`), a security-only audit (`/app-security-audit`), a UI-against-spec review (`/app-ux-review`), or a spec (`/app-spec-review`).
- This skill runs no gate (the catalog lists none). `PE-CODE-REVIEW` runs inside `/app-story-done` (always at lean for a non-trivial change) and uses this skill's report as input when it is fresh.

## Inputs

- `studio.yaml` (platforms, stack, `specialists:`, `commands:`, `modes`). None: offer `/app-adopt` or `/app-start` and stop.
- A target. No argument: the working tree diff against the branch base (uncommitted plus commits not on the base branch). A PR number or branch: fetch it read-only with the tools the repo uses (`gh pr diff`, `git fetch`, `git diff <base>...<head>`) and diff against its base. Never check the branch out over the user's working tree, and never post comments, reviews or approvals to the PR or the tracker: the user posts the report if they want it there. A path: all files under it. Optional story path: pulls in its criteria, QA test cases and cited spec and ADR sections.
- Nothing to review (empty diff, path matches no files): the verdict is NOT ASSESSED with that reason. Do not write a report that says "no issues".

## Phase 1: Fix the scope

Resolve the target to an explicit file list and diff, and count: files, added and removed lines, and which are source, test, config, build, docs, generated or vendored. Exclude generated and vendored files by name and say so ("12 of 87 files excluded: generated"). Read the story, if given, and the spec and ADR text it cites, by section. Record `git rev-parse HEAD` and the base so the report names exactly what was reviewed.

If the diff is very large (more than about 1500 changed lines), say so and ask once: review all of it in slices / review the files the user names first / continue as one pass. Do not silently sample.

## Phase 2: Choose the lenses and announce

Print the plan block (`orchestration.md` section 2). Always spawn `code-reviewer`. Add lenses from the files and the app:

| Lens | Spawn when |
|---|---|
| `code-reviewer` | Always: correctness, data loss, error handling, edge cases, tests that cannot fail, maintainability, spec and ADR conformance |
| The language specialist for each language in the diff | Rigor standard and full: `typescript-specialist` (TS and JS), `python-specialist`, `dotnet-specialist` (C#), `rust-specialist`, `go-specialist`, `jvm-specialist` (Java, Kotlin), `cpp-specialist` (C, C++). Prefer the ones in `studio.yaml` `specialists:` |
| The platform specialist for each platform the diff touches | Rigor standard and full: `frontend-engineer`, `ui-engineer`, `web-framework-specialist`, `web-platform-engineer` (web), `windows-desktop-engineer`, `win32-systems-specialist`, `macos-engineer`, `linux-desktop-engineer`, `hybrid-desktop-engineer` (desktop), `ios-engineer`, `android-engineer`, `cross-platform-mobile-engineer` (mobile), `backend-engineer`, `database-engineer`, `distributed-systems-engineer`, `api-designer`, `identity-specialist` (backend), `infrastructure-engineer`, `build-engineer` (infra and build). Only those whose area the changed files are in, and only for platforms in `studio.yaml` |
| `security-engineer` | The diff touches a sensitive path, at every rigor (see list). Not spawned otherwise: say `security-engineer not spawned: no sensitive paths in the diff` |
| `accessibility-specialist` | Rigor standard and full, when UI files changed |
| `test-engineer` | Rigor full, or a Logic, Integration or API story: testability lens (are the hooks exposed, do tests assert the criteria, edge cases uncovered) |

**Sensitive paths:** authentication and sessions, authorization and permissions, cryptography and key handling, payment or purchase code, personal or health data, IPC and native bridges, auto-update and installers, network listeners and outbound calls to new hosts, deserialization and file parsing, anything that builds a query, command, path or HTML from input, secrets and configuration of them, CI and deploy definitions. When in doubt about a path, treat it as sensitive.

At rigor minimal only `code-reviewer` and (if sensitive) `security-engineer` run; the plan block says the others were not spawned because of the rigor. Review modes do not change the lenses (this skill runs no gate).

## Phase 3: Brief and spawn, all lenses in one message

Issue every Agent call in one message (`orchestration.md` section 4). Each brief (section 3) carries: app, repo path and that `studio.yaml` must be read; the file list and how to see the diff (the exact git command); the story criteria and cited spec or ADR text, quoted; the lens and what it must not duplicate; the severity words (CRITICAL, HIGH, MEDIUM, LOW per `standards/severity.md`); and that the agent edits nothing.

**Return contract for this skill** (replaces the default one, because reviewers have no write access): the reply is the findings, nothing else, each in this shape:

```
F<n> | <CRITICAL|HIGH|MEDIUM|LOW> | <file>:<line> | <one-line claim>
Code: <the quoted lines>
Trigger: <the concrete input, state or sequence that makes it fail>
Why it matters: <consequence for users or data>
Fix: <the smallest correction>
```

plus a final line `Checked and clean: <areas the lens looked at and found fine>`. Tell them: findings without a file, line and trigger are not findings; style preferences go under LOW; do not report what a linter or the compiler already catches unless the build is configured to ignore it.

Lens focus to include in the brief: `code-reviewer` (correctness, error handling and the unhappy paths, concurrency and ordering, resource cleanup, data loss and migrations, input validation at boundaries, tests that pass for the wrong reason, dead or duplicated code, conformance to the cited requirement and ADR); language specialists (idiom, typing, error model, async and ownership, tooling configuration); platform specialists (lifecycle, threading and main-thread rules, permissions, OS integration, framework misuse, deprecated or version-wrong APIs against `docs/stack-reference.md`); `security-engineer` (authn and authz, injection, secrets, crypto use, unsafe deserialization, SSRF and path traversal, IPC and capability scope, supply chain of added dependencies, logging of sensitive data, against OWASP ASVS or MASVS as the platform fits); `accessibility-specialist` (names, roles, focus order, keyboard and screen-reader paths, contrast, text scaling, motion).

## Phase 4: Collect and verify every finding

Wait for all lenses. A lens that returned nothing, or an error, is a named gap and BLOCKED for that lens (re-brief once; if it fails again, the section reads `NOT ASSESSED: <lens> did not return`). Never fill a gap with your own review pretending to be the lens.

Then verify each finding yourself. Do not pass findings through unchecked:

1. Merge duplicates across lenses (same file and cause); keep the strongest evidence and note which lenses agreed.
2. Re-read the code at `file:line` in the working tree (not the quote). Is the quoted code really there? Does the trigger actually reach it (enumerate the inputs and the callers)? Is the claimed consequence real?
3. Where cheap, prove it: grep for callers, read the test, run a one-off command, or run the project's tests for that area. A security finding rated CRITICAL or HIGH gets a concrete exploit path or an honest "not demonstrated".
4. Label each: **VERIFIED** (you confirmed it), **REFUTED** (you showed it false: drop it, count it), **UNVERIFIED** (plausible, you could not confirm: report separately with the specialist's evidence). Re-rate severity from what you confirmed, not from the agent's tone.
5. Keep the denominators: "31 raw findings from 5 lenses: 19 verified, 6 refuted, 4 unverified, 2 merged".

**Mechanical checks, run by you:** `commands.build` and `commands.lint` (and `commands.format` as a check where it supports one) on the reviewed tree, one heavy run at a time. A failure in the reviewed files is a VERIFIED finding with the exit code. An empty command is `NOT ASSESSED: commands.<key> is not set`. Tests are not run by this skill unless the user asks; the report says `Tests: not run by this review`.

**Conformance:** when a story or ADR was given, classify each deviation: ARCHITECTURAL VIOLATION (uses a pattern the ADR rejects: HIGH), ADR DRIFT (diverges without a forbidden pattern: MEDIUM), MINOR DEVIATION (LOW). A cited ADR or spec that could not be read is `NOT ASSESSED: <doc> could not be read`; none cited is `NO ADRS CITED`, which is not NOT ASSESSED.

## Phase 5: Write the report

Write `docs/qa/reviews/<date>-<scope>.md` from `templates/code-review-report.md` (`paths` overrides apply; scope slug from the target, `-2` suffix if the name exists). New studio documents may be written directly. Contents: what was reviewed (target, base and head commits, file counts, exclusions), lenses run and not run with reasons, mechanical check results, findings by severity with their VERIFIED or UNVERIFIED label and evidence, refuted count, positive observations (always; what is done well), required changes, suggestions, and the verdict. Check the file exists with real content before reporting.

## Verdicts

First match wins. NOT ASSESSED ranks below CHANGES REQUIRED and above both approvals.

1. **CHANGES REQUIRED**: any VERIFIED CRITICAL or HIGH finding, an ARCHITECTURAL VIOLATION, or a build or lint failure in the reviewed files. These are the Required Changes.
2. **NOT ASSESSED**: nothing to review; a lens that was required did not return; any UNVERIFIED CRITICAL or HIGH finding remains; a required section could not be assessed (unreadable ADR, empty build command and no other mechanical check). Name each and what would settle it. A review that skipped a lens has not approved the code.
3. **APPROVED WITH SUGGESTIONS**: only VERIFIED MEDIUM and LOW findings, or UNVERIFIED MEDIUM and LOW claims worth a look.
4. **APPROVED**: no required changes, no suggestions, every lens that was planned returned.

MEDIUM findings are suggestions by default; the user or `principal-engineer` may promote one. Do not invent required changes to look thorough, and do not hide a finding to look agreeable.

## Rigor and review mode

| Setting | Effect |
|---|---|
| minimal | `code-reviewer` (+ `security-engineer` if sensitive); no language, platform, accessibility or test lens |
| standard | Adds language, platform and (UI files) accessibility lenses |
| full | Adds `test-engineer` testability; ADR conformance is mandatory when a story is given |
| solo, lean, full | No effect: this skill runs no gate. `Gates: none run (<mode>)` |

## Report to the user

Print the summary (not the whole report): verdict, counts with denominators, each Required Change as `file:line - claim - fix`, the UNVERIFIED items, lenses not spawned and why, report path. Then the user decision, asked with the question last: after CHANGES REQUIRED: fix now with `/app-dev-story` or `/app-bugfix` (Recommended) / discuss a finding / stop. After APPROVED WITH SUGGESTIONS: apply suggestions first / close with `/app-story-done` and log them as tech debt / stop. After NOT ASSESSED: supply what is missing and rerun / stop.

End with the closing block (`orchestration.md` section 8):

```
Verdict: <APPROVED | APPROVED WITH SUGGESTIONS | CHANGES REQUIRED | NOT ASSESSED> - <one line why>
Gates: none run (<mode>)
Wrote: docs/qa/reviews/<date>-<scope>.md
Next: </app-dev-story <story> | /app-bugfix <bug> | /app-story-done <story>> (<why>)
```

## Rules for this skill

- Never edit source, tests or config. Review only.
- Never post to a pull request, issue or tracker, and never check out the reviewed branch over the user's working tree.
- Never report a specialist finding as a defect before checking it against the code. Unchecked means UNVERIFIED, and it says so.
- Never write "no issues" for a scope of zero files or a lens that did not run.
- Never spawn a specialist for a platform or language the app does not have.
- Never rate a finding by how confident it sounds.
- Do not start the next skill.
