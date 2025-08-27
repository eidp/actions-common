<!-- NOTE: This file's contents are automatically generated. Do not edit manually. -->
# Check Workflow Status (Action)

Checks the status of specified jobs using the needs context.
This is useful for configuring required status checks in GitHub branch protection rules.
Using this action, you only need to configure a single job that checks the status of multiple jobs, rather than configuring each job individually in the branch protection rules.

This action requires a GitHub token with the following permissions:
```yaml
  permissions:
    contents: read
    actions: read
    pull-requests: read # Only needed if you use the `required-files-changed` input
```

## 🔧 Inputs

|          Name          |                                                                  Description                                                                  |Required|Default|
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|--------|-------|
|         `jobs`         |                                             Comma-separated list of job names to check status for.                                            |   Yes  |   ``  |
|     `github-token`     |                                                   GitHub token to authenticate API requests.                                                  |   Yes  |       |
|`requires-files-changed`|Comma-separated list of file paths or globs. If specified and this workflow runs on a PR with no matching files changed, it exits successfully.|   No   |   ``  |

## 📤 Outputs

_None_

## 🚀 Usage

```yaml
- name: Check Workflow Status
  uses: eidp/actions-common/check-workflow-status@v0
  with:
    # your inputs here
```
