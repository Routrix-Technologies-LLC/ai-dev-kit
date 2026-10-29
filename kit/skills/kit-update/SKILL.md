---
name: kit-update
description: Updates the AI Dev Kit to the newest version from GitHub and reports what changed. Use when the person says "update the kit", "get the latest agents", "is there a new version", or kit-help suggests it.
---

# Update the kit

1. Say in one line what will happen: the newest kit is downloaded from GitHub and reinstalled; files the person changed by hand are kept.
2. Run `python "$HOME/.ai-dev-kit/kit/install.py" update` (use `python3` or `py` if `python` is not found). It downloads the kit, then runs the new installer for the same assistant(s) as before.
3. Read the output and report in plain words: the old and new version, how many files changed, and any file that was kept because it was edited by hand (say what that means: their version stays; `install --force` would take the kit's and back theirs up).
4. If the download fails, say so with the error; nothing was changed. Common causes: no internet, or a firewall or proxy blocking GitHub.
5. Tell them to reload VS Code (Ctrl+Shift+P, "Developer: Reload Window") so new agents and skills load.
6. Projects that already have the game or security team keep their copy. If they want the update there too, offer: `python "$HOME/.ai-dev-kit/kit/install.py" project <folder> --team games|security`, which updates files the project has not changed and lists the rest.
