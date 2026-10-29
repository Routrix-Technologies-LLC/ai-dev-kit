#!/usr/bin/env python3
"""AI Dev Kit installer. Standard library only, Python 3.8 or newer, Windows, macOS and Linux.

    python install.py install --for claude|copilot|both   install or refresh the kit for this user
    python install.py project <folder> --team games|security|apps [--for ...]
                                                           add a team to one project folder
    python install.py status                               what is installed, and what was changed by hand
    python install.py update                               download the latest kit and reinstall it
    python install.py uninstall                            remove what the kit installed

Options: --dry-run shows what would happen and writes nothing. --force replaces files you
changed by hand (the old copy is backed up first).

Where things go (user level):
  claude   ~/.claude/agents, ~/.claude/skills, ~/.claude/studio, and a marked block in ~/.claude/CLAUDE.md
  copilot  ~/.copilot/agents (*.agent.md), ~/.copilot/skills, ~/.copilot/studio, and a marked block
           in ~/.copilot/copilot-instructions.md
  both     all of the above
The kit keeps its own copy in ~/.ai-dev-kit/kit (the project command and updates use it) and
remembers every file it wrote in ~/.ai-dev-kit/state.json, so updates never overwrite a file
you edited and uninstall removes only what the kit put there.

The game and security teams install per project, not per user: several game agents share
names with App Studio agents, and the security team only runs where a scope.yaml says what
you own.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

REPO_URL = "https://github.com/Routrix-Technologies-LLC/ai-dev-kit"
ZIP_URL = REPO_URL + "/archive/refs/heads/main.zip"

HERE = Path(__file__).resolve().parent
HOME = Path.home()
KIT_HOME = HOME / ".ai-dev-kit"
KIT_COPY = KIT_HOME / "kit"
STATE = KIT_HOME / "state.json"
BACKUPS = KIT_HOME / "backups"

CLAUDE = HOME / ".claude"
COPILOT = HOME / ".copilot"
BLOCK_START = "<!-- ai-dev-kit:start (managed by the AI Dev Kit installer; edits inside this block are replaced on update) -->"
BLOCK_END = "<!-- ai-dev-kit:end -->"
BLOCK_RE = re.compile(r"\n*<!-- ai-dev-kit:start.*?<!-- ai-dev-kit:end -->\n*", re.S)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".txt", ".py", ".json", ".toml"}
TARGETS = {"claude": ["claude"], "copilot": ["copilot"], "both": ["claude", "copilot"]}


# ---------------------------------------------------------------- helpers

def rmtree(p: Path) -> None:
    """shutil.rmtree that clears read-only flags and retries while Windows (antivirus, indexer)
    briefly holds a folder."""
    def onerr(func, path, _exc):
        os.chmod(path, stat.S_IWRITE)
        for _ in range(10):
            try:
                func(path)
                return
            except OSError:
                time.sleep(0.3)
        func(path)
    shutil.rmtree(p, onerror=onerr)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now() -> str:
    return _dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def kit_version(root: Path) -> str:
    v = root / "VERSION"
    return v.read_text(encoding="utf-8").strip() if v.exists() else "unknown"


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    return {"version": None, "targets": [], "files": {}}


def save_state(state: dict, dry: bool) -> None:
    if dry:
        return
    KIT_HOME.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")


def rel_home(p: Path) -> str:
    try:
        return "~/" + p.relative_to(HOME).as_posix()
    except ValueError:
        return str(p)


def split_frontmatter(text: str):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def to_copilot_agent(text: str, studio_from: str, studio_to: str) -> str:
    """Claude-format agent -> VS Code / Copilot custom agent (.agent.md).

    Keeps name and description. Drops tools, model and the other Claude-only fields, so the
    agent gets the tools enabled in Copilot's picker (tool names differ between the two)."""
    fm, body = split_frontmatter(text)
    keep = []
    for line in (fm or "").splitlines():
        if line.startswith(("name:", "description:")):
            keep.append(line)
    body = body.replace(studio_from, studio_to)
    return "---\n" + "\n".join(keep) + "\n---\n" + body


class Writer:
    """Writes files, remembering what the kit owns so it never clobbers a user's edits."""

    def __init__(self, state: dict, force: bool, dry: bool):
        self.state, self.force, self.dry = state, force, dry
        self.owned = dict(state.get("files", {}))  # path -> sha of what the kit wrote
        self.touched: dict[str, str] = {}
        self.written: list[str] = []
        self.same = 0
        self.skipped: list[str] = []
        self.stamp = now()

    def backup(self, dest: Path) -> None:
        if self.dry or not dest.exists():
            return
        try:
            rel = dest.relative_to(HOME)
        except ValueError:
            rel = Path(dest.name)
        b = BACKUPS / self.stamp / rel
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, b)

    def put(self, dest: Path, data: bytes, track: bool = True) -> None:
        key = str(dest)
        new = sha(data)
        if dest.exists():
            cur_bytes = dest.read_bytes()
            cur = sha(cur_bytes)
            if cur == new:
                self.same += 1
                if track:
                    self.touched[key] = new
                return
            ours_unchanged = self.owned.get(key) == cur
            if not ours_unchanged and not self.force:
                self.skipped.append(key)
                return
            self.backup(dest)
        self.written.append(key)
        if track:
            self.touched[key] = new
        if not self.dry:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)

    def tree(self, src: Path, dest: Path, transform=None, rename=None) -> None:
        for f in sorted(src.rglob("*")):
            if f.is_dir() or "__pycache__" in f.parts:
                continue
            data = f.read_bytes()
            out = dest / f.relative_to(src)
            if rename:
                out = rename(out)
            if transform and f.suffix in TEXT_SUFFIXES:
                data = transform(f, data.decode("utf-8")).encode("utf-8")
            self.put(out, data)

    def remove_stale(self) -> list[str]:
        """Delete files the kit wrote last time but no longer ships, if the user never edited them."""
        gone = []
        for key, old in self.owned.items():
            if key in self.touched:
                continue
            p = Path(key)
            if p.exists() and sha(p.read_bytes()) == old:
                gone.append(key)
                if not self.dry:
                    p.unlink()
                    prune_empty(p.parent)
        return gone


def prune_empty(d: Path) -> None:
    stops = {HOME, CLAUDE, COPILOT, CLAUDE / "agents", CLAUDE / "skills", COPILOT / "agents", COPILOT / "skills"}
    while d not in stops and d.exists() and d.is_dir() and not any(d.iterdir()):
        d.rmdir()
        d = d.parent


def write_block(path: Path, body: str, w: Writer) -> None:
    """Insert or replace the kit's marked block, leaving the rest of the file alone."""
    block = f"{BLOCK_START}\n{body.strip()}\n{BLOCK_END}\n"
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if BLOCK_RE.search(old):
        new = BLOCK_RE.sub("\n\n" + block, old).lstrip("\n")
    else:
        new = (old.rstrip("\n") + "\n\n" if old.strip() else "") + block
    if new == old:
        w.same += 1
        return
    w.backup(path)
    w.written.append(str(path) + "  (kit block)")
    if not w.dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8", newline="\n")


def strip_block(path: Path, dry: bool) -> bool:
    if not path.exists():
        return False
    old = path.read_text(encoding="utf-8")
    if not BLOCK_RE.search(old):
        return False
    new = BLOCK_RE.sub("\n\n", old).strip("\n")
    if not dry:
        if new:
            path.write_text(new + "\n", encoding="utf-8", newline="\n")
        else:
            path.unlink()
    return True


def instructions(root: Path, host: str) -> str:
    text = (root / "kit" / "instructions.md").read_text(encoding="utf-8")
    return text.replace("{{HOST}}", "Claude Code" if host == "claude" else "GitHub Copilot")


# ---------------------------------------------------------------- install

def copy_kit_home(dry: bool) -> Path:
    """Keep a copy of the kit in ~/.ai-dev-kit/kit so projects and updates can use it later."""
    if HERE == KIT_COPY:
        return KIT_COPY
    if dry:
        return HERE
    tmp = KIT_HOME / "kit.new"
    if tmp.exists():
        rmtree(tmp)
    ignore = shutil.ignore_patterns(".git", "__pycache__", "*.pyc")
    shutil.copytree(HERE, tmp, ignore=ignore)
    if KIT_COPY.exists():
        rmtree(KIT_COPY)
    tmp.rename(KIT_COPY)
    return KIT_COPY


def install_claude(root: Path, w: Writer) -> None:
    apps = root / "teams" / "apps"
    w.tree(apps / "agents", CLAUDE / "agents")
    w.tree(apps / "skills", CLAUDE / "skills")
    w.tree(apps / "studio", CLAUDE / "studio")
    w.tree(root / "kit" / "skills", CLAUDE / "skills")
    write_block(CLAUDE / "CLAUDE.md", instructions(root, "claude"), w)


def install_copilot(root: Path, w: Writer) -> None:
    apps = root / "teams" / "apps"
    fix = lambda f, t: t.replace("~/.claude/studio/", "~/.copilot/studio/")
    w.tree(apps / "agents", COPILOT / "agents",
           transform=lambda f, t: to_copilot_agent(t, "~/.claude/studio/", "~/.copilot/studio/"),
           rename=lambda p: p.with_name(p.stem + ".agent.md") if p.suffix == ".md" else p)
    w.tree(apps / "skills", COPILOT / "skills", transform=fix)
    w.tree(apps / "studio", COPILOT / "studio", transform=fix)
    w.tree(root / "kit" / "skills", COPILOT / "skills")
    write_block(COPILOT / "copilot-instructions.md", instructions(root, "copilot"), w)


def detect_for() -> str | None:
    if os.environ.get("CLAUDECODE") == "1" or os.environ.get("CLAUDE_CODE_ENTRYPOINT"):
        return "claude"
    return None


def cmd_install(a) -> int:
    target = a.for_ or detect_for()
    if not target:
        print("Say which assistant this is for: --for claude (Claude Code), --for copilot "
              "(GitHub Copilot), or --for both.", file=sys.stderr)
        return 2
    if not (HERE / "teams" / "apps" / "agents").exists():
        print(f"This folder does not look like the AI Dev Kit (no teams/apps/agents): {HERE}", file=sys.stderr)
        return 2
    state = load_state()
    targets = sorted(set(TARGETS[target]) | (set(state.get("targets", [])) if a.keep_targets else set()))
    root = copy_kit_home(a.dry_run)
    w = Writer(state, a.force, a.dry_run)
    if "claude" in targets:
        install_claude(root, w)
    if "copilot" in targets:
        install_copilot(root, w)
    gone = w.remove_stale() if set(targets) >= set(state.get("targets", [])) else []
    # Keep ownership of skipped files the kit wrote before, so a later --force or uninstall still knows them.
    files = {k: v for k, v in w.owned.items() if k in w.skipped}
    files.update(w.touched)
    state.update(version=kit_version(root), targets=targets, files=files, installed=now())
    save_state(state, a.dry_run)

    verb = "would write" if a.dry_run else "wrote"
    print(f"AI Dev Kit {kit_version(root)} for {', '.join(targets)}: {verb} {len(w.written)}, "
          f"unchanged {w.same}, removed {len(gone)}, skipped {len(w.skipped)}")
    for k in w.skipped:
        print(f"  kept your version (you changed it; --force replaces it and backs yours up): {k}")
    if not a.dry_run:
        print("Done. Reload VS Code (Ctrl+Shift+P, then 'Developer: Reload Window') so the new agents and skills load.")
        print("Then type /kit-start to begin a project, or /kit-help for a tour.")
    return 0


# ---------------------------------------------------------------- project

def swap_paths_for_project(f: Path, t: str) -> str:
    return t.replace("~/.claude/studio/", ".claude/studio/").replace("~/.copilot/studio/", ".claude/studio/")


def gitignore_line(target: Path, line: str, w: Writer) -> None:
    gi = target / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if line in text.splitlines():
        return
    new = text + ("" if not text or text.endswith("\n") else "\n") + line + "\n"
    w.written.append(str(gi))
    if not w.dry:
        gi.parent.mkdir(parents=True, exist_ok=True)
        gi.write_text(new, encoding="utf-8", newline="\n")


def cmd_project(a) -> int:
    root = KIT_COPY if (KIT_COPY / "teams").exists() else HERE
    state = load_state()
    target_for = a.for_ or detect_for() or (state.get("targets") and ("both" if len(state["targets"]) == 2 else state["targets"][0]))
    if not target_for:
        print("Say which assistant: --for claude, --for copilot or --for both.", file=sys.stderr)
        return 2
    hosts = TARGETS[target_for]
    proj = Path(a.folder).expanduser().resolve()
    if root in (proj, *proj.parents) or KIT_HOME in (proj, *proj.parents):
        print("Pick a project folder outside the kit itself.", file=sys.stderr)
        return 2
    team = {"game": "games", "games": "games", "security": "security", "sec": "security",
            "app": "apps", "apps": "apps"}[a.team]
    src = root / "teams" / team
    claude = proj / ".claude"
    # Project files are not tracked in state.json; an existing file that differs is kept unless --force.
    w = Writer({"files": {}}, a.force, a.dry_run)

    def agents_and_skills(transform=None):
        if "claude" in hosts:
            w.tree(src / "agents", claude / "agents", transform)
            if (src / "skills").exists():
                w.tree(src / "skills", claude / "skills", transform)
        if "copilot" in hosts:
            w.tree(src / "agents", proj / ".github" / "agents",
                   transform=lambda f, t: to_copilot_agent(transform(f, t) if transform else t, "", ""),
                   rename=lambda p: p.with_name(p.stem + ".agent.md") if p.suffix == ".md" else p)
            if (src / "skills").exists():
                w.tree(src / "skills", proj / ".github" / "skills", transform)

    if team == "games":
        agents_and_skills()
        w.tree(src / "rules", claude / "rules")
        profile = claude / "game-project.md"
        if not profile.exists():
            w.put(profile, (src / "game-project.md").read_bytes(), track=False)
        w.put(claude / "ROSTER.md", (src / "ROSTER.md").read_bytes(), track=False)
        next_step = "Fill in .claude/game-project.md (the kit-start skill walks through it), then reload VS Code."
    elif team == "security":
        agents_and_skills()
        w.tree(src / "netsec", claude / "netsec")
        scope = claude / "netsec" / "scope.yaml"
        if not scope.exists():
            w.put(scope, (src / "netsec" / "scope.example.yaml").read_bytes(), track=False)
        next_step = "Fill in .claude/netsec/scope.yaml with only things you own, reload VS Code, then run /sec-engage."
    else:
        agents_and_skills(swap_paths_for_project)
        w.tree(src / "studio", claude / "studio", swap_paths_for_project)
        next_step = "Reload VS Code, then run /app-start (new app) or /app-adopt (existing code)."
    gitignore_line(proj, ".claude/agent-memory/", w)

    verb = "would write" if a.dry_run else "wrote"
    print(f"{team} team -> {proj} for {', '.join(hosts)}: {verb} {len(w.written)}, unchanged {w.same}, skipped {len(w.skipped)}")
    for k in w.skipped:
        print(f"  kept the project's version (differs; --force to replace): {k}")
    if not a.dry_run:
        print("Next: " + next_step)
    return 0


# ---------------------------------------------------------------- status, update, uninstall

def cmd_status(a) -> int:
    state = load_state()
    if not state.get("files"):
        print("The AI Dev Kit is not installed for this user.")
        return 1
    changed = [k for k, v in state["files"].items() if Path(k).exists() and sha(Path(k).read_bytes()) != v]
    missing = [k for k in state["files"] if not Path(k).exists()]
    agents = sum(1 for k in state["files"] if "/agents/" in Path(k).as_posix())
    skills = sum(1 for k in state["files"] if Path(k).name == "SKILL.md")
    print(f"AI Dev Kit {state.get('version')} for {', '.join(state.get('targets', []))}, installed {state.get('installed')}")
    print(f"  {len(state['files'])} files: {agents} agent files, {skills} skills; kit copy in {rel_home(KIT_COPY)}")
    for host, f in (("claude", CLAUDE / "CLAUDE.md"), ("copilot", COPILOT / "copilot-instructions.md")):
        if host in state.get("targets", []):
            ok = f.exists() and BLOCK_START in f.read_text(encoding="utf-8")
            print(f"  instructions block in {rel_home(f)}: {'present' if ok else 'MISSING (run install again)'}")
    for k in changed:
        print(f"  changed by hand (updates keep your version): {k}")
    for k in missing:
        print(f"  missing (run install again to restore): {k}")
    return 0


def cmd_update(a) -> int:
    state = load_state()
    targets = state.get("targets") or []
    target = a.for_ or ("both" if len(targets) == 2 else (targets[0] if targets else detect_for()))
    if not target:
        print("The kit is not installed yet. Run: python install.py install --for claude|copilot|both", file=sys.stderr)
        return 2
    print(f"Downloading the latest kit from {REPO_URL} ...")
    with tempfile.TemporaryDirectory() as td:
        zpath = Path(td) / "kit.zip"
        try:
            with urllib.request.urlopen(ZIP_URL, timeout=120) as r, open(zpath, "wb") as out:
                shutil.copyfileobj(r, out)
        except OSError as e:
            print(f"Download failed: {e}", file=sys.stderr)
            return 1
        with zipfile.ZipFile(zpath) as z:
            z.extractall(td)
        tops = [p for p in Path(td).iterdir() if p.is_dir() and (p / "install.py").exists()]
        if not tops:
            print("The download did not contain install.py; nothing changed.", file=sys.stderr)
            return 1
        new = tops[0]
        print(f"Installing {kit_version(new)} (you had {state.get('version')}).")
        cmd = [sys.executable, str(new / "install.py"), "install", "--for", target]
        if a.force:
            cmd.append("--force")
        if a.dry_run:
            cmd.append("--dry-run")
        return subprocess.call(cmd)


def cmd_uninstall(a) -> int:
    state = load_state()
    files = state.get("files", {})
    if not files:
        print("Nothing to remove: the kit has no record of installed files.")
    removed, kept = 0, []
    for k, v in files.items():
        p = Path(k)
        if not p.exists():
            continue
        if sha(p.read_bytes()) != v and not a.force:
            kept.append(k)
            continue
        removed += 1
        if not a.dry_run:
            p.unlink()
            prune_empty(p.parent)
    blocks = [str(f) for f in (CLAUDE / "CLAUDE.md", COPILOT / "copilot-instructions.md") if strip_block(f, a.dry_run)]
    if not a.dry_run:
        if KIT_COPY.exists():
            rmtree(KIT_COPY)
        if STATE.exists():
            STATE.unlink()
    verb = "would remove" if a.dry_run else "removed"
    print(f"{verb} {removed} files and the kit block from {len(blocks)} instruction file(s).")
    for k in kept:
        print(f"  kept (you changed it; --force removes it too): {k}")
    if BACKUPS.exists():
        print(f"Backups of anything the kit replaced are still in {rel_home(BACKUPS)}; delete that folder when you no longer need it.")
    print("Project folders you set up with the project command keep their .claude/ and .github/ files.")
    return 0


# ---------------------------------------------------------------- main

def main() -> int:
    if sys.version_info < (3, 8):
        print("Python 3.8 or newer is needed.", file=sys.stderr)
        return 2
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")

    def common(p):
        p.add_argument("--for", dest="for_", choices=sorted(TARGETS))
        p.add_argument("--force", action="store_true")
        p.add_argument("--dry-run", action="store_true")

    p = sub.add_parser("install", help="install or refresh the kit for this user")
    common(p)
    p.add_argument("--keep-targets", action="store_true", help=argparse.SUPPRESS)
    p = sub.add_parser("project", help="add a team to one project folder")
    p.add_argument("folder")
    p.add_argument("--team", required=True, choices=["games", "game", "security", "sec", "apps", "app"])
    common(p)
    sub.add_parser("status", help="show what is installed")
    p = sub.add_parser("update", help="download the latest kit and reinstall")
    common(p)
    p = sub.add_parser("uninstall", help="remove what the kit installed")
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")

    a = ap.parse_args()
    if a.cmd is None:
        ap.print_help()
        return 0
    return {"install": cmd_install, "project": cmd_project, "status": cmd_status,
            "update": cmd_update, "uninstall": cmd_uninstall}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
