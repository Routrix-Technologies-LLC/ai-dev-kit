# AI Dev Kit

A complete team of AI specialists for building things: apps, websites, web panels, games, home lab setups and security checks of your own systems. Point your AI assistant at this repository and it installs everything for you.

Works with **Claude Code** and **GitHub Copilot** in Visual Studio Code, on Windows, macOS and Linux.

## Start here

New to this? Open **[START-HERE.pdf](START-HERE.pdf)**. It walks through installing VS Code, adding your AI assistant, and pointing it at this kit, one step at a time.

Already have VS Code with Claude Code or GitHub Copilot? Open a folder, open the AI chat, and paste:

> Install the AI Dev Kit from https://github.com/Routrix-Technologies-LLC/ai-dev-kit. Read AI-INSTALL.md in that repository and follow it.

Your assistant does the rest. When it finishes, reload VS Code and type `/kit-start`.

## What you get

| Team | What it is for | Size |
|---|---|---|
| **App Studio** | Apps, websites, web panels and dashboards, desktop and phone apps, APIs, bots, scripts and tools: from idea and design through building, testing, security and release. | 68 agents, 46 skills |
| **Game team** | Games in any engine, from vision and design through programming, art, audio, QA and release. Added to a game project when you start one. | 28 agents |
| **Security team** | Checking the security of systems you own: recon, web and network testing, hardening, monitoring, compliance and reports. Only tests what you list in a written scope. | 29 agents, 8 skills |
| **Kit skills** | `/kit-start` (start anything), `/kit-homelab` (home lab work with notes kept for you), `/kit-checkpoint` (save progress), `/kit-help`, `/kit-update`. | 5 skills |

It also sets up your assistant's standing instructions so it uses these teams on its own, explains what it is doing as it goes, and asks before anything risky.

**Built for the $20 plans.** Agents run on the cheaper models (Sonnet for building and reviewing, Haiku for research, writing and checklists; nothing on Opus), the assistant keeps your main chat on an affordable model, and it warns you before workflows that use a lot of your allowance. Claude Code users can have Sonnet set as their default at install.

**Stays up to date, with your say-so.** At install you choose how updates arrive: you're told about new versions and asked first (recommended), they install automatically, or never. See [CHANGELOG.md](CHANGELOG.md) for what changed.

## The commands to remember

| Type | To |
|---|---|
| `/kit-start` | Start a new project (it asks what you want and sets everything up) |
| `/app-help` | See where an app stands and what to do next |
| `/kit-homelab` | Work on servers, your network or self-hosted apps |
| `/kit-checkpoint` | Save your progress |
| `/kit-help` | Get a tour, tips, or fixes for common problems |
| `/kit-update` | Get the newest version of the kit |

Type `/` in the chat to see everything.

## Update or remove

- Update: type `/kit-update`. Change how updates arrive with `python "$HOME/.ai-dev-kit/kit/install.py" updates notify|auto|off`.
- Remove: ask your assistant to "uninstall the AI Dev Kit", or run `python "$HOME/.ai-dev-kit/kit/install.py" uninstall`. Only what the kit installed is removed.

## What is in this repository

| Path | What |
|---|---|
| `START-HERE.pdf` | Setup guide for people |
| `AI-INSTALL.md` | Install steps for the AI assistant |
| `install.py` | The installer (Python 3.8+, no extra packages) |
| `kit/` | The standing instructions and the `/kit-*` skills |
| `teams/apps/`, `teams/games/`, `teams/security/` | The three teams |

## License

MIT, see [LICENSE](LICENSE). The team structure builds on [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) (MIT); see [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

Made by Routrix Technologies LLC.
