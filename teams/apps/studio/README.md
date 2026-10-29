# App Studio

A standing application development team for Claude Code: 68 agents in three tiers, 46 workflow skills, 27 review gates, and the templates and standards that hold them together. It is modeled on [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) (MIT), adapted from games to apps, and staffed the way a very large software company staffs one product.

It is built to be wide. It covers web apps, desktop apps on Windows, macOS and Linux, phone and tablet apps on iOS and Android (native or cross-platform), backend services, CLIs, browser extensions and libraries, in any mainstream language. Nothing in it is tied to one app. Each app's specifics live in that app's own `studio.yaml`.

## Start here

| You want to | Run |
|---|---|
| Start a brand new app | `/app-start` |
| Bring an existing app under the studio | `/app-adopt <app>` |
| Find out where an app is and what to do next | `/app-help <app>` |
| Audit an existing app and get an improvement backlog | `/app-team-audit <app>` |
| Build one feature end to end | `/app-team-feature <app> <feature>` |
| Implement or close one story | `/app-dev-story`, `/app-story-done` |
| Fix a bug properly | `/app-bugfix <app> <bug>` |
| Review a change | `/app-code-review <app> [branch or path]` |
| Ship a release | `/app-release <app> <version>` |

You can also just describe the work. The main session picks the right agents from the roster, briefs them, and orchestrates.

## How it is organized

| Part | Where | What it is |
|---|---|---|
| Agents | `.claude/agents/<name>.md` | 4 directors, 10 leads, 54 specialists. See `roster.md`. |
| Skills | `.claude/skills/app-*/SKILL.md` | The workflows. Catalog in `skill-authoring.md`. |
| Orchestration | `orchestration.md` | How skills brief agents, check their work, ask the user, and report. |
| Coordination | `coordination.md` | Delegation, escalation, change propagation, agent memory. |
| Gates | `gates/` | Named reviews that return fixed verdicts. Index in `gates/README.md`. |
| Standards | `standards/` | Rigor levels, testing and evidence, engineering, documentation, severity, context management. |
| Templates | `templates/` | Every document the studio writes. |
| App layout | `layout.md` | Where each app keeps its studio artifacts, `studio.yaml`, stages. |
| Shared agent sections | `shared/` | Text stamped into every agent by `tools/sync_shared.py`. |

## Principles

- **The user decides.** Agents advise, propose and build what was agreed. Directors frame decisions with options and a recommendation; the user makes the call.
- **Evidence over assertion.** Every finding cites a file, a command and its output, a measurement or a source. A check that could not run is `NOT ASSESSED`, never a pass. A compile check is not a run.
- **Artifacts over prose.** An agent's work counts when its file exists with real content. The file is the memory: long work is checkpointed in the app's `.studio/state.md`.
- **Rigor scales, quality does not.** Minimal rigor (the default) needs a one-page brief; full rigor needs specs, ADRs and gates. Rigor relaxes what must exist, never what must work.
- **Safe by default.** Nothing is deployed, published, submitted, pushed or deleted without the user. No focus-stealing windows, no input injection, heavy jobs through the run lock, no secrets in files.
- **Check knowledge against the source.** Frameworks and store rules change faster than training data. Versions and APIs are verified against official docs and lock files and recorded in each app's stack reference.

## Maintaining it

- **Where it lives.** The AI Dev Kit installs the studio into `~/.claude/` (Claude Code) or `~/.copilot/` (GitHub Copilot), laid out as `agents/`, `skills/` and `studio/`. Its source is `teams/apps/` in the kit. Paths in these docs are written as they appear inside a project (`.claude/agents/...`).
- **Edit shared agent text** in `shared/`, then run `python studio/tools/sync_shared.py` from the package root (the folder holding `agents/`, `skills/` and `studio/`). It stamps every agent and checks names, frontmatter, the roster, em dashes and mojibake. `--check` validates without writing. `python studio/tools/check_studio.py` checks the whole studio.
- **Add an agent:** `authoring.md`. **Add a skill:** `skill-authoring.md`. Add the row to `roster.md` or the catalog.
- **Put it to work.** Claude Code loads project agents and skills only from the folder a session starts in, plus `~/.claude/`. The AI Dev Kit installs it user-wide so it works from any folder (`install.py install`), or into one project's `.claude/` so it travels with that repo (`install.py project <folder> --team apps`). Agents read the studio docs from `.claude/studio/` in an exported project and from `~/.claude/studio/` in the user-wide install; the export rewrites the paths.
- **Agent memory** lives in `.claude/agent-memory/<agent>/` (gitignored), one file per app. See `coordination.md`.

Upstream credit: Claude Code Game Studios, MIT License. This studio reuses its structure and ideas (tiers, gates, verdicts, collaboration protocol, story lifecycle, run-and-observe) with new content for application development.
