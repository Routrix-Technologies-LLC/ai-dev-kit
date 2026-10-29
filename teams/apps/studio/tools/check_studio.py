"""Cross-check the whole App Studio: every agent, skill, template and gate that any
studio file mentions must exist, and every file must be clean text.

    python studio/tools/check_studio.py   (from the package root; see sync_shared.py)

Checks:
  - agents: frontmatter (name = file, description, tools, model), shared sections current
    (delegates to sync_shared.py --check)
  - skills (skills/app-*/SKILL.md): name = folder, description, user-invocable
  - every `app-*` skill name mentioned anywhere exists
  - every backticked agent-like name that matches a roster agent pattern exists
  - every `templates/<x>` or `<x>.md` template name from authoring.md exists in templates/
  - every gate ID (XX-WORDS) mentioned exists as gates/<id>.md
  - no em or en dashes, no CRLF, in any studio file (shared rules may quote mojibake)
Prints observations; exit 1 if any problem was found. A section that found nothing to
check says so, so a silent pass is visible.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # the package (or a project's .claude)
CLAUDE = ROOT
STUDIO = CLAUDE / "studio"
AGENTS = CLAUDE / "agents"
SKILLS = CLAUDE / "skills"

GATE_RE = re.compile(r"\b(?:PD|TD|DD|PG|PM|PE|QL|SL|RM)-(?!NNN\b)[A-Z]{3,}(?:-[A-Z]+)*\b")
SKILL_RE = re.compile(r"`/?(app-[a-z0-9-]+)`")
TICK_RE = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")
TEMPLATE_RE = re.compile(r"`(?:templates/)?([a-z0-9-]+\.(?:md|yaml))`")


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def main():
    problems = []
    studio_agents = {}
    for p in sorted(AGENTS.glob("*.md")):
        t = p.read_text(encoding="utf-8")
        if "<!-- studio-shared:" in t:
            studio_agents[p.stem] = t
    skills = {}
    for p in sorted(SKILLS.glob("app-*/SKILL.md")):
        skills[p.parent.name] = p.read_text(encoding="utf-8")
    templates = {p.name for p in (STUDIO / "templates").glob("*")} if (STUDIO / "templates").exists() else set()
    gates = {p.stem.upper() for p in (STUDIO / "gates").glob("*.md")} if (STUDIO / "gates").exists() else set()

    print(f"agents: {len(studio_agents)}  skills: {len(skills)}  templates: {len(templates)}  gates: {len(gates) - (1 if 'README' in gates else 0)}")

    # Agents: delegate structural checks to sync_shared.
    r = subprocess.run([sys.executable, str(STUDIO / "tools" / "sync_shared.py"), "--check"],
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("PROBLEM"):
            problems.append("agents: " + line[9:])

    # Skills frontmatter.
    for name, t in skills.items():
        fm = frontmatter(t)
        if fm.get("name") != name:
            problems.append(f"skill {name}: frontmatter name '{fm.get('name')}'")
        if not fm.get("description"):
            problems.append(f"skill {name}: no description")
        if fm.get("user-invocable") != "true":
            problems.append(f"skill {name}: user-invocable is not true")

    # Collect every studio text file.
    files = list(STUDIO.rglob("*.md")) + list(STUDIO.rglob("*.yaml"))
    files += [AGENTS / f"{a}.md" for a in studio_agents]
    files += list(SKILLS.glob("app-*/**/*.md"))

    # Names that look like agents but are not: skills, templates, folders, common words.
    known_non_agents = set(skills) | {t.rsplit(".", 1)[0] for t in templates}
    agent_like_roles = re.compile(r"-(director|lead|manager|engineer|specialist|designer|researcher|analyst|writer|reviewer)$|^prototyper$")

    for f in files:
        raw = f.read_bytes()
        rel = f.relative_to(ROOT).as_posix()
        if b"\r\n" in raw:
            problems.append(f"{rel}: CRLF line endings")
        text = raw.decode("utf-8", errors="replace")
        body = text.split("<!-- Everything below is generated", 1)[0]
        if "\u2014" in body or "\u2013" in body:
            problems.append(f"{rel}: em or en dash")
        for s in set(SKILL_RE.findall(text)):
            if s not in skills and s not in studio_agents:
                problems.append(f"{rel}: mentions skill `{s}` which does not exist")
        for name in set(TICK_RE.findall(body)):
            if agent_like_roles.search(name) and name not in studio_agents and name not in known_non_agents:
                problems.append(f"{rel}: mentions agent `{name}` which is not on the roster")
        for g in set(m.group(0) for m in GATE_RE.finditer(text)):
            if gates and g not in gates:
                problems.append(f"{rel}: mentions gate {g} with no gates/{g.lower()}.md")
        if templates:
            for tpl in set(re.findall(r"templates/([a-z0-9-]+\.(?:md|yaml))", body)):
                if tpl not in templates:
                    problems.append(f"{rel}: mentions templates/{tpl} which does not exist")

    auth = (STUDIO / "authoring.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Templates\*\* \(`templates/`\): (.*)", auth)
    listed = re.findall(r"`([a-z0-9-]+\.(?:md|yaml))`", m.group(1)) if m else []
    if not listed:
        problems.append("authoring.md: template list not found, template coverage NOT ASSESSED")
    for tpl in listed:
        if templates and tpl not in templates:
            problems.append(f"authoring.md lists template {tpl} but templates/{tpl} does not exist")
    for tpl in sorted(templates - set(listed)):
        problems.append(f"templates/{tpl} exists but is not in the authoring.md template list")

    if not gates:
        print("NOTE: no gates/ folder yet, gate references NOT ASSESSED")
    if not templates:
        print("NOTE: no templates/ folder yet, template references NOT ASSESSED")
    print(f"files scanned: {len(files)}")
    for p in sorted(set(problems)):
        print("PROBLEM:", p)
    print(f"problems: {len(set(problems))}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
