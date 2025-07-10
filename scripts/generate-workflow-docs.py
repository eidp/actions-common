#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml",
#   "py-markdown-table",
# ]
# ///

import yaml
from pathlib import Path
import re
from py_markdown_table.markdown_table import markdown_table

WORKFLOWS_DIR = Path(".github/workflows")
MARKER_TEMPLATE = "<!-- BEGIN WORKFLOW INPUT DOCS: {name} -->"
MARKER_END = "<!-- END WORKFLOW INPUT DOCS -->"

def parse_workflow_file(file_path: Path):
    with file_path.open() as f:
        data = yaml.load(f, Loader=yaml.BaseLoader)

    if not data or not isinstance(data.get("on"), dict) or "workflow_call" not in data["on"]:
        return None, None

    workflow_name = data.get("name", file_path.stem)

    inputs = data["on"]["workflow_call"].get("inputs", {})
    secrets = data["on"]["workflow_call"].get("secrets", {})

    input_rows = []
    for name, meta in inputs.items():
        input_rows.append({
            "Name": f"`{name}`",
            "Description": meta.get("description", "").strip().replace("\n", " "),
            "Required": "Yes" if meta.get("required", "false") == "true" else "No",
            "Type": f"{meta['type']}" if "type" in meta else "",
            "Default": f"`{meta['default']}`" if "default" in meta else "",
        })

    secret_rows = []
    for name, meta in secrets.items():
        secret_rows.append({
            "Name": f"`{name}`",
            "Description": meta.get("description", "").strip().replace("\n", " "),
            "Required": "Yes" if meta.get("required", "false") == "true" else "No",
        })

    inputs_md = markdown_table(input_rows).set_params(row_sep="markdown", quote=False).get_markdown()
    secrets_md = markdown_table(secret_rows).set_params(row_sep="markdown", quote=False).get_markdown()

    header = f"## {workflow_name} (Workflow)"
    block_start = MARKER_TEMPLATE.format(name=workflow_name)
    block = f"{block_start}\n\n### 🔧 Inputs\n\n{inputs_md}\n\n### 🔐 Secrets\n\n{secrets_md}\n\n{MARKER_END}"
    return workflow_name, f"{header}\n\n{block}"

def update_readme(readme_path: Path, name: str, block: str):
    if not readme_path.exists():
        readme_path.write_text(block + "\n")
        print(f"✅ Created README.md with docs for {name}")
        return

    content = readme_path.read_text()
    block_start = MARKER_TEMPLATE.format(name=name)
    header_pattern = rf"(## {re.escape(name)} \(Workflow\))"
    marker_pattern = rf"{re.escape(block_start)}.*?{re.escape(MARKER_END)}"

    header_match = re.search(header_pattern, content)
    marker_match = re.search(marker_pattern, content, re.DOTALL)

    if marker_match:
        # Replace just the inner block
        content = re.sub(marker_pattern, block.split("\n", 1)[1].strip(), content, flags=re.DOTALL)
        print(f"✅ Updated: {readme_path} (replaced existing block for {name})")
    elif header_match:
        # Header exists, but no doc block yet – insert after header
        insert_pos = header_match.end()
        content = (
            content[:insert_pos].rstrip()
            + "\n\n"
            + block.split("\n", 1)[1].strip()
            + "\n\n"
            + content[insert_pos:].lstrip()
        )
        print(f"✅ Updated: {readme_path} (inserted new block under existing header for {name})")
    else:
        # Header doesn't exist – append entire block at the end
        content = content.strip() + "\n\n" + block + "\n"
        print(f"✅ Updated: {readme_path} (appended full block for {name})")

    readme_path.write_text(content)

def main():
    for file in WORKFLOWS_DIR.glob("*.yml"):
        name, block = parse_workflow_file(file)
        if block:
            readme = file.with_name("README.md")
            update_readme(readme, name, block)

if __name__ == "__main__":
    main()

