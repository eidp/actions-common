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
```

## 🔧 Inputs

|          Name         |                                               Description                                               |Required|Default|
|-----------------------|---------------------------------------------------------------------------------------------------------|--------|-------|
|     `github-token`    |                                GitHub token to authenticate API requests.                               |   Yes  |       |
|   `timeout-minutes`   |             Maximum time to wait for all jobs to complete (in minutes). Default: 30 minutes.            |   No   |  `30` |
| `initial-wait-seconds`|       Time to wait for the first job to appear in the workflow (in seconds). Default: 10 seconds.       |   No   |  `10` |
| `skipped-jobs-succeed`|Whether to treat skipped jobs as successful. Set to 'false' to fail if any job is skipped. Default: true.|   No   | `true`|
|`poll-interval-seconds`|            Time between polling API for job status updates (in seconds). Default: 5 seconds.            |   No   |  `5`  |

## 📤 Outputs

_None_

## 🚀 Usage

```yaml
- name: Check Workflow Status
  uses: eidp/actions-common/check-workflow-status@v0
  with:
    # your inputs here
```
