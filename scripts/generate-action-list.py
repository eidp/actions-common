#!/usr/bin/env python3
# /// script
# ///

from pathlib import Path
import re

ACTIONS_DIR = Path(".github/actions")
README_PATH = Path("README.md")
MARKER_START = "<!-- BEGIN AUTO-ACTIONS -->"
MARKER_END = "<!-- END AUTO-ACTIONS -->"

def collect_action_readmes():
    links = []
    for readme in ACTIONS_DIR.glob("*/README.md"):
        action_name = readme.parent.name
        relative_path = readme.as_posix()
        links.append(f"- [{action_name}]({relative_path})")
    return "\n".join(links)

def update_readme(content_block):
    if not README_PATH.exists():
        print("❌ README.md does not exist.")
        return

    content = README_PATH.read_text()

    marker_pattern = re.compile(
        rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
        re.DOTALL,
    )

    new_block = f"{MARKER_START}\n\n{content_block}\n\n{MARKER_END}"

    if marker_pattern.search(content):
        updated = marker_pattern.sub(new_block, content)
    else:
        updated = content.strip() + "\n\n" + new_block + "\n"

    README_PATH.write_text(updated)
    print("✅ Updated README.md with action links.")

def main():
    content_block = collect_action_readmes()
    update_readme(content_block)

if __name__ == "__main__":
    main()
