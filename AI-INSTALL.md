# AI-INSTALL: instructions for the AI assistant

You are an AI coding assistant (Claude Code, GitHub Copilot, or similar) and the person asked you to install the AI Dev Kit from this repository. Do the whole install for them. They should only need to approve your commands and, at the end, reload VS Code.

Throughout: say in one line what each step does before you run it, in plain words. Do not change anything outside the locations listed in step 4. If a step fails, explain what went wrong in plain words and how you will fix it.

## 1. Tell them the plan

In two or three sentences: you will check that Python is available, download the kit, run its installer (which adds the agents, skills and instructions to their AI setup), then ask them to reload VS Code. It takes a few minutes.

## 2. Know which assistant you are

- Claude Code (in VS Code, the terminal or the desktop app): use `--for claude`.
- GitHub Copilot in VS Code: use `--for copilot`. If they might also use the Claude agent inside VS Code, `--for both` covers it.
- Another assistant that reads `~/.claude/` (agents, skills, `CLAUDE.md`): `--for claude`, and tell them which parts may not apply.

## 3. Python 3.8 or newer

Check with `python --version`, then `python3 --version`, then (Windows) `py --version`. Use whichever prints `Python 3.x` with x of 8 or more. On Windows, a `python` that opens the Microsoft Store or prints nothing does not count.

If none works, ask permission, then install it:
- Windows: `winget install -e --id Python.Python.3.12`. Afterwards a new terminal may be needed for `python` to work; `py` usually works at once, or use the full path under `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`.
- macOS: `xcode-select --install` provides `python3`; or `brew install python` if Homebrew is present.
- Linux: the package manager, for example `sudo apt install python3`.

Below, `python` means the command that worked.

## 4. Download the kit and install

Download into a temporary folder (not into their projects), then run the installer from there. It copies itself to `~/.ai-dev-kit/kit/`, so the download can be deleted afterwards.

With git available:

```
git clone --depth 1 https://github.com/Routrix-Technologies-LLC/ai-dev-kit.git <temp>/ai-dev-kit
```

Without git, Windows PowerShell:

```
$d = Join-Path $env:TEMP "ai-dev-kit-dl"; New-Item -ItemType Directory -Force $d | Out-Null
Invoke-WebRequest https://github.com/Routrix-Technologies-LLC/ai-dev-kit/archive/refs/heads/main.zip -OutFile "$d\kit.zip"
Expand-Archive "$d\kit.zip" -DestinationPath $d -Force
```

(the kit is then in `$d\ai-dev-kit-main`). Without git, macOS or Linux:

```
d=$(mktemp -d) && curl -fsSL https://github.com/Routrix-Technologies-LLC/ai-dev-kit/archive/refs/heads/main.zip -o "$d/kit.zip" && unzip -q "$d/kit.zip" -d "$d"
```

(the kit is then in `$d/ai-dev-kit-main`).

Then run, from anywhere:

```
python <kit folder>/install.py install --for <claude|copilot|both>
```

What it writes (and nothing else):
- Claude: `~/.claude/agents/`, `~/.claude/skills/`, `~/.claude/studio/`, and a marked block at the end of `~/.claude/CLAUDE.md`.
- Copilot: `~/.copilot/agents/` (`*.agent.md`), `~/.copilot/skills/`, `~/.copilot/studio/`, and a marked block in `~/.copilot/copilot-instructions.md`.
- Always: `~/.ai-dev-kit/` (its own copy, a record of installed files, and backups).

Existing files the person wrote are never overwritten: the installer skips them and lists them. Existing text in `CLAUDE.md` or `copilot-instructions.md` is kept; only the kit's marked block is added or replaced.

## 5. Check it

1. Read the installer's summary line. If it lists skipped files, tell the person which ones and that their own versions were kept (usually because they already had an agent or skill with the same name).
2. Run `python "$HOME/.ai-dev-kit/kit/install.py" status` and confirm the instructions block is present.
3. Delete the temporary download folder.

## 6. Hand over

Tell the person, in this order:

1. Reload VS Code so the new agents and skills load: press Ctrl+Shift+P (Cmd+Shift+P on a Mac), type "Reload Window", press Enter. Then open a new chat.
2. GitHub Copilot only: keep the chat in Agent mode.
3. To begin, type `/kit-start` and describe what they want to build. A few examples to offer:
   - "I want a simple website for my side business."
   - "Help me make a small 2D game."
   - "I want to set up a home server for my photos and backups."
4. `/kit-help` shows what the kit can do, any time.

Keep this hand-over short and friendly.

## Updating and removing later

- Update: `/kit-update`, or `python "$HOME/.ai-dev-kit/kit/install.py" update`.
- Remove: `python "$HOME/.ai-dev-kit/kit/install.py" uninstall` (removes only what the kit installed).
