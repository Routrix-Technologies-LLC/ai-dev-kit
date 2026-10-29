---
name: kit-help
description: Explains the AI Dev Kit - what is installed, what each team and the main skills are for, example requests, how to update or remove it, and fixes for common problems. Use when the person asks what the kit can do, how to use it, "help", "what can you do", "show me the commands", "how do I...", or when agents or skills seem missing.
---

# AI Dev Kit help

Answer the question that was asked. If it was general ("help", "what can you do"), give the short tour below, adapted to what they seem to be doing, then offer one concrete next step. Keep it to one screen.

## 1. Check the install first

Run `python "$HOME/.ai-dev-kit/kit/install.py" status` (or `python3` / `py`). If it reports problems, fix them first (see Troubleshooting).

## 2. The short tour

**Three teams.**
- **App Studio** (installed everywhere): about 70 specialists for apps, websites, web panels, desktop and phone apps, APIs, bots and tools. Directors, leads and specialists for product, design, every platform, backend, data, security, testing and releases. Roster: `~/.ai-dev-kit/kit/teams/apps/studio/roster.md`.
- **Game team** (per project): 28 specialists from creative director to QA, any engine, with Godot specialists. Added to a game project by `/kit-start`.
- **Security team** (per project): 29 specialists for checking systems you own: recon, web and network testing, hardening, monitoring, compliance, reports. Only tests what its scope file lists.

**The skills to remember.**
- `/kit-start`: start anything new.
- `/app-help`: where an app stands and what to do next.
- `/app-team-feature`, `/app-team-ui`, `/app-bugfix`, `/app-code-review`, `/app-team-release`: build, polish, fix, review, ship.
- `/kit-homelab`: home lab and server work, with notes kept up to date.
- `/kit-checkpoint`: save progress in git.
- `/kit-update`: get the newest kit.
Type `/` in the chat to see every skill.

**Good ways to ask.**
- Say the goal, not the steps: "I want a web page where my family can see whose turn it is to do chores."
- Ask why: "Why did you pick that?" or "Explain that like I'm new to it."
- Ask for options: "Give me two ways to do this and which you'd pick."
- Ask for proof: "Show me it working" or "Run the tests."
- Course-correct freely: "That's more than I need, make it simpler."

## 3. Update and remove

- Update: `/kit-update`.
- Remove: `python "$HOME/.ai-dev-kit/kit/install.py" uninstall` removes only what the kit installed; files changed by hand are kept and listed. Project folders keep their own `.claude/` and `.github/` copies.

## Troubleshooting

| Problem | Fix |
|---|---|
| Skills or agents do not show up after installing | Reload VS Code: Ctrl+Shift+P (Cmd+Shift+P on a Mac), "Developer: Reload Window". Then open a new chat. |
| GitHub Copilot does not use the agents | Make sure the chat is in Agent mode (not Ask), then start a new chat. Custom agents appear in the agents dropdown. |
| A project's game or security agents are missing | Open that project's folder in VS Code (File, Open Folder); project agents only load from the open folder. |
| `python` is not found, or opens the Microsoft Store | Install Python 3 (Windows: `winget install -e --id Python.Python.3.12`, then open a new terminal), or try `py` or `python3`. |
| The status command says files were "changed by hand" | That is fine: updates keep your version. To take the kit's version, run install again with `--force` (yours is backed up in `~/.ai-dev-kit/backups/`). |
| Something else | Describe what you expected and what happened; include any error text. |
