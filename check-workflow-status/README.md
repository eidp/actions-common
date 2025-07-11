<!-- NOTE: This file's contents are automatically generated. Do not edit manually. -->
# Check Workflow Status (Action)

Checks the status of specified jobs using the needs context.
This is useful for configuring required status checks in GitHub branch protection rules.
Using this action, you only need to configure a single job that checks the status of multiple jobs, rather than configuring each job individually in the branch protection rules.

## 🔧 Inputs

| Name |                      Description                     |Required|Default|
|------|------------------------------------------------------|--------|-------|
|`jobs`|Comma-separated list of job names to check status for.|   Yes  |   ``  |

## 📤 Outputs

_None_

## 🚀 Usage

```yaml
- name: Check Workflow Status
  uses: eidp/actions-common/.github/actions/check-workflow-status@v0
  with:
    # your inputs here
```
