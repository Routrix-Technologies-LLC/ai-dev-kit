# Game project profile

Every game agent reads this file before it works. Fill in each `TODO` and delete lines that do not apply. Keep it short and factual; things that change week to week belong in the work list.

## The game

- **Name:** TODO
- **What it is:** TODO (genre, camera, single or multiplayer, setting, what the player does minute to minute)
- **Pillars and tone:** TODO (three to five, and what the game is not)
- **Platforms and input:** TODO
- **Real-world subject (for domain-fidelity-researcher):** TODO (what it simulates, where and when, sources to trust; or "none")

## Engine and code

- **Engine and exact version:** TODO (for example Godot 4.7, from `project.godot`)
- **Language:** TODO
- **Architecture and folders:** TODO (layers, what may depend on what, where rules, world, UI and player code live)
- **Global singletons or autoloads:** TODO
- **Input:** TODO (where actions are registered)
- **Tuning data:** TODO (where gameplay numbers live)
- **Saves:** TODO (format, where serialization lives, versioning)
- **Tests:** TODO (framework, folder, base class)
- **Tools and art pipeline:** TODO

## Commands

- **Import or build:** TODO
- **Run tests:** TODO
- **Smoke-run headless:** TODO
- **Export a build:** TODO

## Where things go

- **Decisions:** `DECISIONS.md` (dated entries)
- **Work list:** `BACKLOG.md`
- **Longer notes and research:** `docs/` and `docs/reference/`
- **Asset licences:** `ASSET_LICENSING.md`
- **Scratch folder:** `~/AgentScratch/<task>/`

## Project rules

- **Asset licence policy:** TODO (for example CC0, OFL or made in house only)
- **Commit rules:** TODO
- TODO

### Godot defaults (keep, adapt, or delete for another engine)

- Release-build safety: no touching freed objects, no thread work on scene objects, no compressed-attribute meshes without normals.
- Anything that moves stops on pause.
- Run `--headless --import` after adding a `class_name`.
