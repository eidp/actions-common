#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml",
#   "py-markdown-table",
# ]
# ///

import yaml
import subprocess
from pathlib import Path
import re
from py_markdown_table.markdown_table import markdown_table

ACTIONS_DIR = Path(".github/actions")
MARKER_TEMPLATE = "<!-- BEGIN ACTION DOCS: {name} -->"
MARKER_END = "<!-- END ACTION DOCS -->"
DEFAULT_VERSION = "v0"

def get_repo_info_from_git():
    try:
        url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True).strip()
        # Matches:
        #   git@github.com:org/repo.git
        #   https://github.com/org/repo.git
        match = re.search(r"github\.com[:/](?P<org_repo>[^/]+/[^/]+?)(?:\.git)?$", url)
        if match:
            return match.group("org_repo")
        else:
            raise ValueError("Could not parse GitHub org/repo from URL.")
    except Exception as e:
        print(f"⚠️ Failed to detect GitHub org/repo from git: {e}")
        return "your-org/your-repo"

def parse_action_file(action_dir: Path, repo_ref: str):
    action_file = action_dir / "action.yml"
    if not action_file.exists():
        action_file = action_dir / "action.yaml"
    if not action_file.exists():
        return None, None

    with action_file.open() as f:
        data = yaml.load(f, Loader=yaml.BaseLoader)

    name = data.get("name", action_dir.name)
    description = data.get("description", "").strip()

    input_rows = []
    for input_name, meta in data.get("inputs", {}).items():
        input_rows.append({
            "Name": f"`{input_name}`",
            "Description": meta.get("description", "").strip().replace("\n", " "),
            "Required": "Yes" if meta.get("required", "false") == "true" else "No",
            "Default": f"`{meta['default']}`" if "default" in meta else "",
        })

    output_rows = []
    for output_name, meta in data.get("outputs", {}).items():
        output_rows.append({
            "Name": f"`{output_name}`",
            "Description": meta.get("description", "").strip().replace("\n", " "),
        })

    inputs_md = markdown_table(input_rows).set_params(row_sep="markdown", quote=False).get_markdown() if input_rows else "_None_"
    outputs_md = markdown_table(output_rows).set_params(row_sep="markdown", quote=False).get_markdown() if output_rows else "_None_"

    header = f"# {name} (Action)\n\n{description}"
    block_start = MARKER_TEMPLATE.format(name=name)

    usage = f"""```yaml
- name: {name}
  uses: {repo_ref}/.github/actions/{action_dir.name}@{DEFAULT_VERSION}
  with:
    # your inputs here
```"""
    block = f"""{header}
{block_start}

## 🔧 Inputs

{inputs_md}

## 📤 Outputs

{outputs_md}

## 🚀 Usage

{usage}

{MARKER_END}
"""
    return name, block.strip()

def update_readme(readme_path: Path, name: str, block: str):
    if not readme_path.exists():
        readme_path.write_text(block + "\n")
        print(f"✅ Created README.md with docs for {name}")
        return

    content = readme_path.read_text()
    pattern = re.compile(
        rf"# {re.escape(name)} \(Action\).*?{re.escape(MARKER_END)}",
        re.DOTALL,
    )

    if pattern.search(content):
        content = pattern.sub(block, content)
    else:
        content = content.strip() + block + "\n"

    readme_path.write_text(content)
    print(f"✅ Updated: {readme_path} with action: {name}")

def main():
    repo_ref = get_repo_info_from_git()
    for action_dir in ACTIONS_DIR.iterdir():
        if action_dir.is_dir():
            name, block = parse_action_file(action_dir, repo_ref)
            if block:
                readme = action_dir / "README.md"
                update_readme(readme, name, block)

if __name__ == "__main__":
    main()
