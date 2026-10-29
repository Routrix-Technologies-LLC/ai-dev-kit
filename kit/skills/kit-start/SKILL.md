---
name: kit-start
description: The front door of the AI Dev Kit. Turns "I want to build X" into a set-up project with the right agent team and the right first step. Use when the person wants to start anything new (an app, website, web panel, dashboard, game, bot, script, home lab project, or a security check of their own stuff), says "start", "new project", "I have an idea", "where do I begin", or is not sure what to build.
argument-hint: "[what you want to build, in your own words]"
---

# Start a project

Goal: in a few minutes, go from an idea in plain words to a project folder that is set up, saved in git, has the right agent team, and has a clear first step. Talk like a helpful senior colleague: short, friendly, no jargon without a one-line explanation.

## 1. Understand the idea

If the person already said what they want, restate it in one sentence and confirm. Otherwise ask: "What would you like to make or do? Describe it however you like."

Then ask only what you need to route it, one question at a time, each with a suggested answer:

- Who is it for (just them, friends or family, a business, the public)?
- Where should it run (in a web browser, on a Windows or Mac computer, on a phone, on a server at home, unsure)?
- Is there existing code or a running system, or is this from scratch?

If they are unsure what to build, offer three small ideas that match what they said they care about, each buildable in an afternoon, and let them pick.

## 2. Pick the route

| The idea is | Route |
|---|---|
| An app, website, web panel or dashboard, desktop or phone app, API, bot, browser extension, script or command-line tool | **App** |
| Existing code they want to improve or finish | **Existing app** |
| A video game | **Game** |
| Servers, networking, a NAS, self-hosted services, Docker, a home lab | **Home lab**: hand off to `/kit-homelab` and stop here |
| Checking the security of systems, sites or networks they own | **Security** |

Say which route you picked and why in one sentence.

## 3. Make the project folder

1. Suggest a short folder name (lowercase, hyphens) and the location `~/Projects/<name>/`. On Windows avoid folders synced by OneDrive or Dropbox if possible (sync tools fight with build folders); say why in one line if you steer them away.
2. Create the folder. For an existing app, use the folder the code is already in instead.
3. If `git` is installed, run `git init` there (skip if it is already a repository). If git is missing, explain that git is how their work gets saved and undone, and offer to install it (Windows: `winget install --id Git.Git -e`; macOS: `xcode-select --install`; Linux: the package manager). Ask first.
4. Add a `.gitignore` suited to the stack once it is known (at minimum `.env`, `node_modules/`, build output, `.claude/agent-memory/`).

## 4. Set up the team for the route

Use `python "$HOME/.ai-dev-kit/kit/install.py"` (try `python3` or `py` if `python` is not found). `--for` is `claude` if you are Claude Code, `copilot` if you are GitHub Copilot.

**App or Existing app.** The App Studio is already installed for every folder, so nothing to copy. Next step is `/app-start` (new) or `/app-adopt` (existing code), run with the project folder as the app. If the person has no strong opinion on technology, let `/app-start` and `/app-stack` recommend a mainstream, well-documented stack and explain the choice in plain words.

**Game.**
1. Run `python "$HOME/.ai-dev-kit/kit/install.py" project <folder> --team games --for <claude|copilot>`.
2. Fill in `<folder>/.claude/game-project.md` together, one question at a time: the game's name and one-line pitch, genre and camera, single or multiplayer, platforms, three to five pillars (what it must feel like) and what it is not. If they have no engine yet, recommend one and say why (Godot is free, light and beginner-friendly for 2D and 3D; Unity and Unreal are the alternatives when they have a reason), and help them install it. Leave the engine-specific lines as `TODO` until the engine project exists, then fill them from the real files.
3. First steps after the reload: `creative-director` to sharpen the pillars, then `prototyper` for the smallest playable version of the core loop.

**Security.**
1. Explain in two sentences: the security team only ever tests what is written in a scope file, and only things the person owns or has written permission to test. Testing anything else can be illegal.
2. Run `python "$HOME/.ai-dev-kit/kit/install.py" project <folder> --team security --for <claude|copilot>`.
3. Fill in `<folder>/.claude/netsec/scope.yaml` together: only their own domains, IP ranges, devices and sites. Leave anything they are unsure they own out of scope.
4. First step after the reload: `/sec-engage`, then `/sec-assess` for a full review.

## 5. Open it and hand off

Agents and skills that live inside a project load when that folder is opened. Tell the person, step by step:

1. In VS Code: File, Open Folder, choose `<folder>`. Trust the folder when asked.
2. Open the AI chat again in the new window.
3. Type the first command you named in step 4 (for example `/app-start` or `/sec-engage`), or for a game: "Let's start: have the creative director help me sharpen the pillars."

For an App route you may continue in this window if the person prefers; say that opening the project folder is still the tidy way to work.

## 6. Save

Make the first commit in the new project: `git add` the files you created by path, commit with "Set up project with the AI Dev Kit". Mention `/kit-checkpoint` for saving progress later.

## Done when

The folder exists, git is initialized (or the person declined), the team is in place for the route, any profile or scope file is filled in or has clear `TODO`s, and the person knows exactly what to type next.
