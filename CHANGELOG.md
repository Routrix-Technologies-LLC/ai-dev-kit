# Changelog

What changed in each version of the AI Dev Kit, newest first. When updates are on, your assistant shows you the entries that are new since your installed version.

## 2026-10-29

- Usage-friendly by default: agents for research, writing and checklists now run on the cheaper Haiku model; everything else stays on Sonnet, and nothing uses Opus. The standing instructions keep the main conversation on Sonnet and warn before the big team workflows.
- Updates: choose at install to be told about new versions (and approve each one), have them installed automatically, or turn checks off. Change it any time with `install.py updates notify|auto|off`.
- Claude Code: the installer can set Sonnet as the default model for new sessions.
- First release: App Studio, game team, security team, `/kit-*` skills, installer for Claude Code and GitHub Copilot, and the START-HERE guide.
