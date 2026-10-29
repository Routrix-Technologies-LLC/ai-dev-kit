# Agent roster

The project's subagents live in `.claude/agents/`. Twenty-six come from the open-source
template Claude Code Game Studios (MIT, `.claude/agents/LICENSE-claude-code-game-studios.txt`),
adapted to be engine- and genre-neutral; two are written for this kit. Every agent runs on
Sonnet. Each agent reads the project profile, `.claude/game-project.md`, before it forms an
opinion or touches a file: the profile says what the game is, which engine and version, the
folder layout, where tuning data, saves, tests and tools live, and the commands that build,
test and run it. When the user talks to an agent directly it asks first; when the main
session spawns it with a written brief, the brief is the approval and it reports at the end.
All carry the same "Project rules" section (the profile's run and scratch rules, commit
rules, licensing, release-build safety, and the project's own rules).

Agents with notes enabled (`memory: project`) keep them in `.claude/agent-memory/<agent>/`
(gitignored; see `.claude/rules/agent-memory.md`).

## Direction

| Agent | Owns / use it when | Tools |
| --- | --- | --- |
| creative-director | Vision, tone, identity; breaks ties between disciplines; scope cuts that touch identity | Read, Glob, Grep, Write, Edit, WebSearch |
| technical-director | Architecture, layers, technology choices, technical risk, performance strategy | Read, Glob, Grep, Write, Edit, Bash, WebSearch |
| producer | The order of work: backlog batches, milestones, scope and risk | Read, Glob, Grep, Write, Edit, Bash, WebSearch |

## Design

| Agent | Owns / use it when | Tools |
| --- | --- | --- |
| game-designer | Core loops, rules, progression, and tuning (the numbers in the project's data and the pacing) | Read, Glob, Grep, Write, Edit, WebSearch |
| systems-designer | Formulas, curves, interaction matrices, tuning ranges for one subsystem | Read, Glob, Grep, Write, Edit |
| economy-designer | Prices, rewards, costs, margins, faucets and sinks, upgrade pacing | Read, Glob, Grep, Write, Edit |
| ux-designer | Flows, controls, screens, onboarding, in-game help | Read, Glob, Grep, Write, Edit, WebSearch |
| accessibility-specialist | Text scale, contrast, colour-blind safety, remapping, audits | Read, Glob, Grep, Write, Edit, Bash |
| domain-fidelity-researcher | A general real-world fidelity researcher: how the real thing the game depicts works (processes, rules, standards, terminology, places); sourced notes in docs/reference/; reviews the game's numbers and content against them | Read, Glob, Grep, Write, Edit, WebSearch, WebFetch |

## Programming

| Agent | Owns / use it when | Tools |
| --- | --- | --- |
| lead-programmer | Code structure, standards, review, API design, refactoring | Read, Glob, Grep, Write, Edit, Bash |
| gameplay-programmer | Implementing mechanics and systems in the game logic and the world | Read, Glob, Grep, Write, Edit, Bash |
| ui-programmer | Screens, HUD, menus, dialogs, the help topics | Read, Glob, Grep, Write, Edit, Bash |
| ai-programmer | Non-player behavior, decision logic, navigation, crowds and traffic | Read, Glob, Grep, Write, Edit, Bash |
| tools-programmer | The project's tool scripts: test and audit tools, pipeline scripts, debug utilities | Read, Glob, Grep, Write, Edit, Bash |
| persistence-engineer | Save and load of deep state, slots, versions and migration, round-trip tests | Read, Glob, Grep, Write, Edit, Bash |
| prototyper | Throwaway builds and spikes that answer one question | Read, Glob, Grep, Write, Edit, Bash |
| godot-specialist | Godot specialist (use only on a Godot project): the engine patterns of the version the profile names, scenes, nodes, resources, autoloads, export | Read, Glob, Grep, Write, Edit, Bash |
| godot-gdscript-specialist | Godot specialist (use only on a Godot project): GDScript quality, typing, signals, coroutines, idioms, performance | Read, Glob, Grep, Write, Edit, Bash |
| godot-shader-specialist | Godot specialist (use only on a Godot project): shaders, materials, particles, post-processing, pause-safe effects | Read, Glob, Grep, Write, Edit, Bash |

## Art and audio

| Agent | Owns / use it when | Tools |
| --- | --- | --- |
| art-director | Visual identity, fidelity to references, asset standards, UI look | Read, Glob, Grep, Write, Edit, WebSearch |
| technical-artist | Asset pipeline, VFX, rendering cost, any baked or generated content, art-to-engine issues | Read, Glob, Grep, Write, Edit, Bash |
| audio-director | Sonic identity, mix, audio implementation strategy | Read, Glob, Grep, Write, Edit, WebSearch |
| sound-designer | SFX specs, audio event lists, ambience layers | Read, Glob, Grep, Write, Edit |

## Quality and release

| Agent | Owns / use it when | Tools |
| --- | --- | --- |
| qa-lead | Test strategy, evidence per change, bug triage, readiness before a build | Read, Glob, Grep, Write, Edit, Bash |
| qa-tester | Automated tests, integration tests, test cases, bug reports, regression checklists | Read, Glob, Grep, Write, Edit, Bash |
| performance-analyst | Profiling against the performance budget, memory, load times | Read, Glob, Grep, Write, Edit, Bash |
| devops-engineer | Build, test and export scripts, CI, hooks, version control workflow, environment notes | Read, Glob, Grep, Write, Edit, Bash |
| release-manager | Release checks, licensing check, export, store page, versions, hotfixes | Read, Glob, Grep, Write, Edit, Bash |

## Template agents you may not need

The upstream template has more agents than this kit installs. A project can leave out
whichever of these its game does not need, and the kit does not ship them:

- **Narrative director, writer, world-builder:** for games with a story.
- **Network programmer, security engineer:** for games with online play.
- **Live-ops designer, analytics engineer, community manager:** for live-service games.
- **Localization lead:** for games in more than one language.
- **Level designer:** for games with authored levels or maps.
- **Engine programmer:** for projects with a custom engine.
- **Unity and Unreal specialists:** for those engines.
- **Godot C# specialist and Godot GDExtension specialist:** for Godot projects using C# or native extensions.

## Adding an agent back, or a new one

1. Copy the template file (the original text is in the Claude Code Game Studios repository, `.claude/agents/<name>.md`) or write a new one into `.claude/agents/<name>.md`. The file name must equal the `name:` in its frontmatter.
2. Keep `model: sonnet`, and drop any `Agent` tool (no nested spawning). Replace the template's folder layout, skills, hooks and gates with this project's, as `.claude/game-project.md` records them (decisions log, backlog, docs, source and test folders, tuning data).
3. Add the "How you work" and "Project rules" sections as they appear in any current agent file (the rules are the same text in all of them; agents without Bash get only the last four lines).
4. Remove references to agents that are not on the roster, or point them at one that is.
5. Add a line to the table above. Keep em dashes out.
