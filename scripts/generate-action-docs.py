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

ACTIONS_DIR = Path("./")
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

    header = (
        "<!-- NOTE: This file's contents are automatically generated. Do not edit manually. -->\n"
        f"# {name} (Action)\n\n{description}"
    )
    usage = f"""```yaml
- name: {name}
  uses: {repo_ref}/{action_dir.name}@{DEFAULT_VERSION}
  with:
    # your inputs here
```"""
    block = f"""{header}

## 🔧 Inputs

{inputs_md}

## 📤 Outputs

{outputs_md}

## 🚀 Usage

{usage}
"""
    return name, block.strip()

def update_readme(readme_path: Path, name: str, block: str):
    if not readme_path.exists():
        readme_path.write_text(block + "\n")
        print(f"✅ Created README.md with docs for {name}")
        return

    content = block + "\n"

    readme_path.write_text(content)
    print(f"✅ Generated: {readme_path} with action: {name}")

def find_action_dirs():
    action_dirs = []
    if ACTIONS_DIR.exists():
        for d in ACTIONS_DIR.iterdir():
            if d.is_dir() and (d / "action.yml").exists() or (d / "action.yaml").exists():
                action_dirs.append(d)
    return action_dirs

def main():
    repo_ref = get_repo_info_from_git()
    for action_dir in find_action_dirs():
        name, block = parse_action_file(action_dir, repo_ref)
        if block:
            readme = Path(action_dir / "README.md")
            update_readme(readme, name, block)

if __name__ == "__main__":
    main()
