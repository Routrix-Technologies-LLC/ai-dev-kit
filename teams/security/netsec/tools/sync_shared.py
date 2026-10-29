"""Stitch the shared blocks into every agent file.

Each agent in ../agents/<name>.md ends its hand-written part with a marker line:

    <!-- netsec-shared: director | lead | specialist -->

Everything from that marker to end of file is generated: a notice, then
shared/common.md, then shared/<role>.md. Edit the shared/ files, never the
generated tail of an agent. Run from network-security-agents/:

    python netsec/tools/sync_shared.py          # write
    python netsec/tools/sync_shared.py --check   # fail if any agent is stale
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]      # network-security-agents/
AGENTS = ROOT / "netsec" / "agents" if (ROOT / "netsec" / "agents").exists() else ROOT / "agents"
SHARED = ROOT / "netsec" / "shared"
MARKER = "<!-- netsec-shared:"
NOTICE = ("<!-- Everything below is generated from netsec/shared/ by sync_shared.py. "
          "Edit those files, not this copy. -->")
ROLES = {"director", "lead", "specialist"}


def block(role: str) -> str:
    common = (SHARED / "common.md").read_text(encoding="utf-8").strip()
    rolemd = (SHARED / f"{role}.md").read_text(encoding="utf-8").strip()
    return f"{NOTICE}\n\n{common}\n\n{rolemd}\n"


def rebuild(text: str, path: Path) -> str:
    lines = text.splitlines()
    marker_idx = next((i for i, l in enumerate(lines) if l.strip().startswith(MARKER)), None)
    if marker_idx is None:
        raise SystemExit(f"{path.name}: no '{MARKER} ... -->' marker found")
    marker_line = lines[marker_idx].strip()
    role = marker_line[len(MARKER):].rstrip("->").strip()
    if role not in ROLES:
        raise SystemExit(f"{path.name}: marker role '{role}' not one of {sorted(ROLES)}")
    head = "\n".join(lines[:marker_idx]).rstrip("\n")
    return f"{head}\n\n{marker_line}\n\n{block(role)}"


def main() -> int:
    check = "--check" in sys.argv
    agents = sorted(AGENTS.glob("*.md"))
    if not agents:
        raise SystemExit(f"no agents found in {AGENTS}")
    stale = []
    for path in agents:
        current = path.read_text(encoding="utf-8")
        wanted = rebuild(current, path)
        if current == wanted:
            continue
        if check:
            stale.append(path.name)
        else:
            path.write_text(wanted, encoding="utf-8", newline="\n")
            print(f"synced {path.name}")
    if check and stale:
        print("stale (run sync_shared.py): " + ", ".join(stale))
        return 1
    if not check:
        print(f"done: {len(agents)} agents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
