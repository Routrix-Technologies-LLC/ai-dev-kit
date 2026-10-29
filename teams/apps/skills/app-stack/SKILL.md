---
name: app-stack
description: "Choose or pin an app's technology stack, or evaluate adopting a framework or dependency, against explicit criteria, with every version verified from official sources and lock files, then write the stack reference. Use when the user asks what to build it with, whether to adopt a library or framework, to pin or refresh versions, or when agents keep suggesting APIs that do not exist in the pinned version."
argument-hint: "[app] [choose | pin | refresh | evaluate <candidate>] [--review solo|lean|full]"
user-invocable: true
---

# App Stack

Decides or records what the app is built with, and makes the record trustworthy. Three jobs: (1) choose a stack for a new app, (2) evaluate one candidate (a framework, runtime, database, SDK or dependency) before it is adopted, (3) pin and verify what the app actually uses so agents consult the reference instead of memory. Every claim about a version, a release date, an API or a license is either fetched from an official source this run, read from a lock file, or written down as a gap. Nothing is filled from training data.

Writes: `docs/stack-reference.md` (template `stack-reference.md`), an ADR draft at `docs/architecture/adr/ADR-NNNN-<slug>.md` (template `adr.md`, status Proposed), and at minimal rigor a dated entry in `docs/decisions.md` instead of the ADR.
Next: `/app-adr accept` (after the user's yes), `/app-architecture`, `/app-upgrade` (when the pinned versions lag), `/app-test-setup` (foundation).

## When to use and when not to

- Use for a stack choice, a new framework or dependency, a version pin, or a refresh after a toolchain change.
- A dependency or framework version bump on a known stack is `/app-upgrade`. A decision that is not about technology is `/app-adr`. Proving a risky technology works is `/app-prototype` (this skill may recommend it).
- Existing code with no record: `/app-adopt` calls this skill's pin mode; run it directly only to refresh.

## Inputs

- Required: `studio.yaml` (platforms, stack, `min_targets`), and for `choose` or `evaluate` the brief or vision and the architecture doc if they exist. Missing brief: ask what the app is and who it is for, then offer `/app-brief`. Never invent requirements.
- Optional: existing `docs/stack-reference.md`, lock files, team skill notes in the brief, the budgets in `perf-budget.md`.
- Unset `stack:` keys stay empty; unknown facts are asked, never guessed.

## Modes

| Mode | Use | Starts at |
|---|---|---|
| `choose` | No stack yet, or one layer undecided | Phase 2 |
| `evaluate <candidate>` | One adoption decision | Phase 2 with a single candidate plus "do nothing or build it ourselves" as the baseline |
| `pin` | Record what is in use | Phase 3 |
| `refresh` | Reference exists; versions or knowledge gap moved | Phase 3, appending, never truncating older entries |

## Phase 1: Resolve and announce

Per `orchestration.md` sections 1 and 2. Pick agents by platform:

| Platform in `studio.yaml` | Platform lead | Specialists to consult |
|---|---|---|
| web | `web-lead` | `web-framework-specialist`, `web-platform-engineer`, `typescript-specialist` |
| windows, macos, linux | `desktop-lead` | `hybrid-desktop-engineer` (webview or cross-platform shells), the OS engineer, the language specialist |
| ios, android | `mobile-lead` | `ios-engineer`, `android-engineer`, `cross-platform-mobile-engineer` |
| backend | `backend-lead` | `database-engineer`, `distributed-systems-engineer`, the language specialist |
| cli, library | `principal-engineer` | the language specialist |
| extension | `web-lead` | `web-platform-engineer` |

Always: `technical-director` (owns the decision), `compliance-specialist` (license), `security-engineer` (security record). Add `build-engineer` when the build or CI toolchain is part of the choice.

Check: the announce block is printed, naming skipped agents and the gate line for TD-STACK.

## Phase 2: Frame the decision (choose and evaluate)

Main session, with the user.

1. State the decision in one sentence ("Which UI framework for the desktop client?") and the layer it covers. One layer per run; a whole-stack choice is a sequence of layer decisions that share constraints.
2. Collect hard constraints from `studio.yaml` and the brief: platforms, `min_targets`, offline needs, team languages, budgets, hosting, regulatory, store rules, license policy. These are pass or fail filters, applied before scoring.
3. Agree 3 to 7 weighted criteria with the user from this menu, dropping what does not matter: fit to requirements, maturity and stability, ecosystem and libraries, license, security record, maintenance health, team skill, lock-in, reversibility (the cost of leaving), performance against budgets, accessibility support on target platforms, hiring and community.
4. List candidates: 2 to 4 real ones, plus the baseline. For `evaluate`, the baseline is "no new dependency".

Decision point: show the constraints, criteria and weights as a table and ask the user to confirm or change (AskUserQuestion). Write nothing until confirmed.

Check: constraints, criteria with weights, and candidates are in the working notes for the briefs.

## Phase 3: Gather facts (parallel)

Spawn per `orchestration.md` sections 3 and 4, one agent per fact area, each writing one file to `~/AgentScratch/app-stack/<run>/<agent>.md` (outside the repo; the main session copies what survives into the reference).

| Agent | Establishes | Sources it must use |
|---|---|---|
| platform lead or specialists | Fit per hard constraint and per criterion; known limits on each target; migration and escape paths | Official docs, release notes, issue trackers |
| `compliance-specialist` | License of each candidate and its transitive dependencies; obligations (attribution, copyleft reach, SBOM); store policy conflicts | License files, package metadata, official policy pages |
| `security-engineer` | Advisory history, time to patch, supply-chain posture (maintainers, signing, provenance), default-secure or not | Official advisories, the ecosystem's advisory database, release signing docs |
| `build-engineer` (if relevant) | Toolchain support, CI support, reproducible builds, cross-compilation | Official docs |

Each agent labels every finding `SOURCED <url>`, `READ <file:line>` or `UNSOURCED`. Unsourced claims are opinions and score nothing.

In `pin` and `refresh` mode, spawn only the language and platform specialists to read the app's manifests and report what is in use.

Check: every spawned agent's file exists with content (`orchestration.md` section 5). Missing one is a named gap, not filled by the main session.

## Phase 4: Verify versions and the knowledge gap

Main session. This phase is mandatory in every mode; it is what makes the reference trustworthy.

1. **Installed versions** come from lock files and toolchain probes, never from memory or the manifest's range:

| Ecosystem | Lock or resolved source | Probe (light, read-only commands only) |
|---|---|---|
| JavaScript or TypeScript | the lock file for the package manager in use | runtime and package manager `--version` |
| Python | lock or resolved requirements file | interpreter `--version` |
| .NET | `packages.lock.json` or the resolved project assets; SDK pin in `global.json` | `dotnet --version` |
| Rust | `Cargo.lock`; `rust-toolchain` file | `rustc --version` |
| Go | `go.mod` and `go.sum` | `go version` |
| JVM | Gradle or Maven resolved dependency report; wrapper properties | `java -version` |
| iOS and macOS | resolved package file; Xcode and SDK version | the Xcode command line tools version query |
| Android | Gradle version catalog and wrapper; compile and target SDK | wrapper version task |
| C and C++ | vcpkg or Conan lock and baseline; CMake minimum | compiler and CMake `--version` |
| Containers and hosting | image tags and digests in Dockerfiles or compose files | none; read the files |

   No lock file is itself a finding (unpinned builds). A probe that fails is `installed NOT DETERMINED`, never "not installed".
2. **Latest supported version** comes from the official source (project release page, official docs, the registry's own page, the vendor's support policy), fetched this run with WebFetch or WebSearch. Record the URL and the fetch date. Record the support window (LTS, security-only, end of life) from the official policy.
3. **Knowledge gap.** State your own training cutoff as the model running this skill. If you cannot state one, treat it as unknown and grade every version HIGH RISK. For each pinned item compare its release date to the cutoff:
   - released well before the cutoff: LOW RISK (reference notes optional);
   - near the cutoff or a major after it: MEDIUM RISK (reference notes recommended);
   - after the cutoff, or release date NOT SOURCEABLE: HIGH RISK (breaking changes and deprecations section required).
4. **For MEDIUM and HIGH items**, fetch the official migration guide, changelog or release notes and extract: breaking changes, deprecated APIs with the replacement, and new recommended practices. Cite the URL for each. Anything the official page does not state is written `NOT SOURCEABLE: <what>, not stated at <url>`; a gap is a successful outcome. An inference is labelled as one and names what it rests on.
5. Pinned beyond or behind what is installed: state both and ask (pin installed, pin newer and upgrade later, or pin newer on purpose). Record the answer.

Check: every pinned row has an installed value (or NOT DETERMINED), a source URL with date, a support window (or NOT SOURCEABLE), and a risk grade. A row without a URL is UNSOURCED and caps the verdict at NOT ASSESSED.

## Phase 5: Evaluate and recommend (choose and evaluate)

Main session with `technical-director` consulted (spawn once with the criteria table and the fact files; ask for a scored comparison and the single biggest risk, written to `~/AgentScratch/app-stack/<run>/technical-director.md`).

1. Apply the hard filters. A candidate that fails one is REJECT, with the reason.
2. Score the rest per criterion from SOURCED or READ facts only. A criterion with no sourced fact is marked `unknown` and counts against confidence, not as neutral.
3. Always state lock-in and reversibility in concrete terms: what it would cost to leave, and which seam (interface, adapter, data format) keeps that cost low.
4. Recommend one verdict per candidate: ADOPT, TRIAL (adopt behind a seam or inside a `/app-prototype`, with a named exit test), or REJECT.

Decision point: present the comparison, the recommendation and the biggest risk, then ask which candidate to take (2 to 4 options, `(Recommended)`). A skipped answer is not an answer.

## Phase 6: Write the artifacts

After the user's choice, list the files to be written and ask once (`orchestration.md` section 6).

1. `docs/stack-reference.md` from `stack-reference.md`, using its numbered headings (1 Toolchain and runtimes, 2 Frameworks and key libraries, 3 Platform targets, 4 Known API changes newer than training data, 5 Deprecations and things to avoid, 6 Upgrade notes, 7 How to verify this file): the pinned tables in sections 1 to 3 (item, installed, latest supported, support window, source URL and fetch date, risk grade), the Last verified date, breaking changes per version span in section 4 (appended under a heading naming the span, never truncating older spans), `NOT SOURCEABLE` lines, and a "do not suggest" list of deprecated or removed APIs in section 5. Existing reference pinning a newer version than chosen: stop and ask. Same version: refresh the date only if re-verified this run.
2. The decision: standard and full rigor, an ADR draft (status Proposed; the next number comes from scanning the ADR folder as `/app-adr` Phase N1 does, and its headings are the `adr.md` template's exactly) with the criteria table, alternatives, consequences, reversibility and validation criteria. Minimal rigor, a dated `docs/decisions.md` entry. Never set status Accepted here; that is `/app-adr accept`.
3. Update `studio.yaml` `stack:` and `specialists:` only with the user's yes, listing the keys changed.

Check: re-read each written file; the table has no empty cell that is not marked NOT DETERMINED or NOT SOURCEABLE.

## Phase 7: Gate and checkpoint

`TD-STACK` (owner `technical-director`) is this skill's own single-purpose gate, so it runs in `lean` and `full` and is skipped in `solo` (`gates/README.md`). Spawn it with the candidates, the recommendation and evaluation table, the stack reference path with the source of each version, the requirements and budgets, `min_targets`, the license and security findings, and any prototype evidence; it reads its own gate file. Its words are APPROVE, CONCERNS, REJECT or NOT ASSESSED. Record the result directly under the title of the stack reference (and the ADR draft) as `> **Technical Director review (TD-STACK)**: <VERDICT> <date>`; a skipped gate adds no line and prints `TD-STACK skipped: solo mode`. A REJECT leaves the files written but the choice not adopted, and the skill's verdict is REJECT. Overwrite the `CHECKPOINT` in `.studio/state.md`.

## Rigor and review mode

| | minimal | standard | full |
|---|---|---|---|
| Criteria | 3 to 4 | 4 to 6 | 5 to 7, each with a sourced fact |
| Decision record | `decisions.md` entry | ADR draft | ADR draft with spike evidence for any TRIAL |
| Reference depth | pinned table | plus breaking changes for MEDIUM and HIGH | plus per-module notes where changes are large |
| Security and license agents | consulted for runtime or framework picks | always | always, with transitive dependency scan |

Rigor never lowers verification: versions are checked against sources at every level.

| Review mode | Gates |
|---|---|
| solo | `TD-STACK skipped: solo mode` |
| lean | TD-STACK runs (the own gate of a single-purpose review skill, always-on in lean) |
| full | TD-STACK runs |

## Verdicts

First match wins, per candidate for `choose` and `evaluate`; for `pin` and `refresh` the verdict covers the pinned set.

1. `REJECT`: fails a hard constraint, has a license the policy forbids, or an unmitigated critical security finding. Pin mode: a pinned item is end of life with no plan. Also `TD-STACK` returned REJECT.
2. `TRIAL`: viable but a risk is unproven or lock-in is high; adopt behind a seam with an exit test. Pin mode: verified, but one or more items are MEDIUM or HIGH risk with gaps recorded. Also `TD-STACK` returned CONCERNS that the user accepted.
3. `NOT ASSESSED`: a criterion that decides the outcome has no sourced fact, official sources could not be fetched, a lock file is missing so installed versions are unknown, an agent's file is missing, or `TD-STACK` returned NOT ASSESSED. State which and what would settle it. (This ranks below REJECT and TRIAL, which name a known problem, and above ADOPT, which needs everything verified.)
4. `ADOPT`: all hard filters pass and every deciding criterion is sourced. Pin mode: every row verified, no gaps outside NOT SOURCEABLE lines.

The gate and the skill's own judgement combine by the ranking in `gates/README.md` (REJECT beats CONCERNS beats NOT ASSESSED beats a pass): a gate REJECT makes the verdict REJECT, a gate CONCERNS caps it at TRIAL, a gate NOT ASSESSED caps it at NOT ASSESSED, and the gate never raises the verdict.

## Report

```
Stack: <mode> <layer or candidate>
Constraints: <list>   Criteria: <weighted list>
Candidates: <name: verdict, one-line why> ...
Pinned: <N items> (verified from source: <N>, NOT DETERMINED: <N>, NOT SOURCEABLE gaps: <N>)
Risk grades: LOW <N>, MEDIUM <N>, HIGH <N>   Training cutoff used: <stated or unknown>
Reversibility: <what leaving costs, and the seam>
Skipped: <agent or step and why>
Decisions for the user: <labelled options, or none>
```

Then the closing block from `orchestration.md` section 8.

## Rules for this skill

- Never write a version, date, license or API fact that was not fetched or read this run. Write the gap.
- Never pin from a manifest range. The installed version comes from the lock file or a probe.
- Never set an ADR to Accepted, and never edit source, manifests or lock files; changing versions is `/app-upgrade`.
- Never score an unknown as neutral.
- Never truncate older version spans in an existing reference.
- A candidate's marketing page is not a source for its security or maturity claims.
- Never pick for the user when the answer is skipped; ask again.
