#!/usr/bin/env python3
# /// script
# dependencies = ["pyyaml"]
# ///

import yaml
from pathlib import Path
import re

WORKFLOWS_DIR = Path(".github/workflows")
README_PATH = Path("README.md")
LIST_HEADER = "## 📚 Shared Workflows"
MARKER_START = "<!-- BEGIN SHARED WORKFLOWS -->"
MARKER_END = "<!-- END SHARED WORKFLOWS -->"

def is_shared_workflow(file_path: Path) -> bool:
    with open(file_path) as f:
        data = yaml.load(f, Loader=yaml.BaseLoader)
    return isinstance(data.get("on"), dict) and "workflow_call" in data["on"]

def create_slug(name: str) -> str:
    return re.sub(r"[^\w\- ]", "", name.lower()).replace(" ", "-") + "-workflow"

def generate_shared_workflow_list() -> str:
    items = []
    for wf_file in sorted(WORKFLOWS_DIR.glob("*.yml")):
        with wf_file.open() as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)

        if not isinstance(data.get("on"), dict) or "workflow_call" not in data["on"]:
            continue

        name = data.get("name", wf_file.stem)
        slug = create_slug(name)
        items.append(f"- [{name}](./.github/workflows/README.md#{slug})")

    if not items:
        return ""

    content = f"{LIST_HEADER}\n\n"
    content += "The following reusable workflows are available in this repository:\n\n"
    content += "\n".join(items)
    return f"{MARKER_START}\n\n{content}\n\n{MARKER_END}"

def update_readme(path: Path, new_list: str):
    if not path.exists():
        path.write_text(new_list + "\n")
        print(f"✅ Created {path} with shared workflow list.")
        return

    content = path.read_text()

    pattern = re.compile(
        rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
        re.DOTALL
    )

    if pattern.search(content):
        content = pattern.sub(new_list, content)
    else:
        # Add to the end of the file if no markers found
        content = content.strip() + "\n\n" + new_list + "\n"

    path.write_text(content)
    print(f"✅ Updated: {path} with shared workflow list.")

def main():
    new_list = generate_shared_workflow_list()
    if new_list:
        update_readme(README_PATH, new_list)
    else:
        print("⚠️ No shared workflows found.")

if __name__ == "__main__":
    main()
