<!-- NOTE: This file's contents are automatically generated. Do not edit manually. -->
# Update major version tag (Action)

This action updates or creates a major version tag based on the latest semver tag pushed to the repository. If the major version tag already exists, it updates it to point to the latest commit; otherwise, it creates a new major version tag.
Make sure that this action is only triggered for semver tags.
This action is used for managing major version tags in a GitHub repository, ensuring that the major version tag always points to the latest commit of the corresponding major version.
This is useful for repositories that contain shared workflows.
Normally, you can only refer to a shared workflow by the full tag, but this action allows you to refer to the major version tag, which is more convenient.

```yaml
on:
  push:
    tags:
    - 'v[0-9]+.[0-9]+.[0-9]+'
```

This action requires a GitHub token with the following permissions:
```yaml
  permissions:
    contents: write
```

## 🔧 Inputs

| Name|                                                                        Description                                                                       |Required|Default|
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------|
|`tag`|The source tag to create the major version tag for. This must be a semver tag like `v1.2.3`. If not provided, it will use the tag from the GitHub context.|   No   |   ``  |

## 📤 Outputs

|    Name   |                                 Description                                 |
|-----------|-----------------------------------------------------------------------------|
|`major_tag`|The created or updated major version tag, e.g., `v1` for a tag like `v1.2.3`.|

## 🚀 Usage

```yaml
- name: Update major version tag
  uses: eidp/actions-common/update-major-version-tag@v0
  with:
    # your inputs here
```
