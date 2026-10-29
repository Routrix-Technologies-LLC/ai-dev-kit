"""Stamp the App Studio's shared sections into every studio agent, and check the roster.

The studio is a package laid out like a .claude folder: agents/, skills/ and studio/
side by side. In the AI Dev Kit that folder is teams/apps/; in a project
it was exported into, it is the project's .claude/. Paths below are relative to it.

Each studio agent file in agents/ ends its own text with a marker line:

    <!-- studio-shared: <class> -->

where <class> is director, lead, builder, author or reviewer. Everything after the
marker is replaced by the shared sections from studio/shared/, so edit those
files (never the stamped copies) and re-run this script:

    python studio/tools/sync_shared.py          # stamp and check
    python studio/tools/sync_shared.py --check  # check only, exit 1 on problems

Agents whose tools include Bash get rules-full.md; the rest get rules-short.md.
Files without the marker (for example the doc-* council agents) are left alone.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # the package (or a project's .claude)
AGENTS = ROOT / "agents"
STUDIO = ROOT / "studio"
SHARED = STUDIO / "shared"

MARKER = re.compile(r"^<!-- studio-shared: (\w+) -->\s*$", re.M)
CLASS_PARTS = {
    "director": ["collab-director.md"],
    "lead": ["collab-director.md", "collab-reviewer.md"],
    "builder": ["collab-builder.md"],
    "author": ["collab-author.md"],
    "reviewer": ["collab-reviewer.md"],
}
EM_DASH = "\u2014"
EN_DASH = "\u2013"
MOJIBAKE = ("Ã", "Â", "â€")


def read(name: str) -> str:
    return (SHARED / name).read_text(encoding="utf-8").strip() + "\n"


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def shared_block(cls: str, has_bash: bool) -> str:
    parts = ["workspace.md", "collab-common.md", *CLASS_PARTS[cls], "gates.md",
             "rules-full.md" if has_bash else "rules-short.md"]
    body = "\n".join(read(p) for p in parts)
    return ("<!-- Everything below is generated from .claude/studio/shared/ by "
            "sync_shared.py. Edit those files, not this copy. -->\n\n" + body)


def main() -> int:
    check_only = "--check" in sys.argv
    problems, stamped, names = [], 0, set()
    roster = (STUDIO / "roster.md").read_text(encoding="utf-8") if (STUDIO / "roster.md").exists() else ""

    for path in sorted(AGENTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = MARKER.search(text)
        if not m:
            continue
        cls = m.group(1)
        fm = frontmatter(text)
        name = fm.get("name", "")
        names.add(name)
        if cls not in CLASS_PARTS:
            problems.append(f"{path.name}: unknown class '{cls}'")
            continue
        if name != path.stem:
            problems.append(f"{path.name}: frontmatter name '{name}' does not match the file name")
        for key in ("description", "tools", "model"):
            if not fm.get(key):
                problems.append(f"{path.name}: frontmatter has no {key}")
        if "Agent" in [t.strip() for t in fm.get("tools", "").split(",")]:
            problems.append(f"{path.name}: studio agents must not have the Agent tool")
        if roster and f"`{name}`" not in roster:
            problems.append(f"{path.name}: not listed in roster.md")

        has_bash = "Bash" in [t.strip() for t in fm.get("tools", "").split(",")]
        new = text[: m.end()].rstrip("\n") + "\n\n" + shared_block(cls, has_bash)
        if new != text:
            if check_only:
                problems.append(f"{path.name}: shared sections are out of date")
            else:
                path.write_text(new, encoding="utf-8", newline="\n")
                stamped += 1
        if EM_DASH in new or EN_DASH in new:
            problems.append(f"{path.name}: contains an em or en dash")
        # The shared rules quote the mojibake characters on purpose, so only the
        # agent's own body is checked for them.
        if any(s in text[: m.start()] for s in MOJIBAKE):
            problems.append(f"{path.name}: contains mojibake")

    # Every backticked agent name the roster mentions in a table row must exist.
    for row in re.findall(r"^\|\s*`([a-z0-9-]+)`\s*\|", roster, re.M):
        if row not in names:
            problems.append(f"roster.md lists `{row}` but no studio agent file has that name")

    print(f"studio agents: {len(names)}, stamped: {stamped}")
    for p in problems:
        print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
