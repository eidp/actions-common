#!/usr/bin/env python3
# /// script
# ///

from pathlib import Path
import re

ACTIONS_HEADER = "## 🛠️ GitHub Actions"
ACTIONS_MARKER_START = "<!-- BEGIN ACTIONS -->"
ACTIONS_MARKER_END = "<!-- END ACTIONS -->"
README_PATH = Path("README.md")

def _generate_action_list() -> str:
    items = []
    for action_file in Path(".").rglob("action.y*ml"):
        action_dir = action_file.parent
        readme = action_dir / "README.md"
        if readme.exists():
            action_name = action_dir.name
            relative_path = readme.as_posix()
            items.append(f"- [{action_name}]({relative_path})")
    if not items:
        return ""
    content = f"{ACTIONS_HEADER}\n\n"
    content += "The following GitHub Actions are available in this repository:\n\n"
    content += "\n".join(items)
    return f"{ACTIONS_MARKER_START}\n\n{content}\n\n{ACTIONS_MARKER_END}"

def update_readme(content_block):
    if not README_PATH.exists():
        print("❌ README.md does not exist.")
        return
    content = README_PATH.read_text()
    marker_pattern = re.compile(
        rf"{re.escape(ACTIONS_MARKER_START)}.*?{re.escape(ACTIONS_MARKER_END)}",
        re.DOTALL,
    )
    new_block = content_block
    if marker_pattern.search(content):
        updated = marker_pattern.sub(new_block, content)
    else:
        updated = content.strip() + "\n\n" + new_block + "\n"
    README_PATH.write_text(updated)
    print("✅ Updated README.md with action links.")

def generate_action_list():
    content_block = _generate_action_list()
    update_readme(content_block)

if __name__ == "__main__":
    generate_action_list()
