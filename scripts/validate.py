"""Validate the skill: SKILL.md frontmatter and internal Markdown links."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def check_frontmatter():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append("SKILL.md: missing YAML frontmatter")
        return
    fields = dict(
        line.split(":", 1) for line in match.group(1).splitlines() if ":" in line
    )
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip().strip('"')
    if name != ROOT.name and name != "decision-check":
        errors.append(f"SKILL.md: name is '{name}', expected 'decision-check'")
    if not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append("SKILL.md: name must be lowercase letters, digits and hyphens")
    if not description:
        errors.append("SKILL.md: description is empty")
    elif len(description) > 1024:
        errors.append(f"SKILL.md: description is {len(description)} chars (max 1024)")


def check_links():
    link = re.compile(r"\]\(([^)\s]+)\)")
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        # Ignore links inside fenced code blocks.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in link.findall(text):
            if re.match(r"^(https?:|mailto:|#)", target) or target.startswith("../../"):
                continue
            path = target.split("#")[0]
            if path and not (md.parent / path).exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link -> {target}")


check_frontmatter()
check_links()

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("All checks passed.")
