<!-- BEGIN ACTION DOCS: Update major version tag -->
<!-- BEGIN ACTION DOCS: Update major version tag -->
# Update major version tag (Action)

This action updates or creates a major version tag based on the latest semver tag pushed to the repository. If the major version tag already exists, it updates it to point to the latest commit; otherwise, it creates a new major version tag.
Make sure that this action is only triggered for semver tags.

```yaml
on:
  push:
    tags:
    - 'v[0-9]+.[0-9]+.[0-9]+'
```
<!-- BEGIN ACTION DOCS: Update major version tag -->

## 🔧 Inputs

| Name|                                                                        Description                                                                       |Required|Default|
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------|--------|-------|
|`tag`|The source tag to create the major version tag for. This must be a semver tag like `v1.2.3`. If not provided, it will use the tag from the GitHub context.|   No   |   ``  |

## 📤 Outputs

_None_

## 🚀 Usage

```yaml
- name: Update major version tag
  uses: eidp/actions-common/.github/actions/update-major-version-tag@v0
  with:
    # your inputs here
```

<!-- END ACTION DOCS -->
