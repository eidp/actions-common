# Common shared workflows

## Common workflow (Workflow)

This workflow runs a number of very common tasks that are useful in many repositories.

The tasks include:
- labelling pull requests based on commit messages using the conventional commits standard.

<!-- BEGIN WORKFLOW INPUT DOCS: Common workflow -->

### 🔧 Inputs

_None_

### 🔐 Secrets

|Name           |Description                                                                                                                                     |Required|
|---------------|------------------------------------------------------------------------------------------------------------------------------------------------|--------|
|`GITHUB_TOKEN` |GitHub token used for authentication in various actions. This is automatically provided by GitHub Actions and does not need to be set manually. |Yes     |

### 📤 Outputs

_None_

<!-- END WORKFLOW INPUT DOCS -->

### Example Usage

```yaml
name: 'Common PR workflow'

on:
  pull_request:
    branches:
      - main

jobs:
  common:
    uses: eidp/actions-common/.github/workflows/common.yml@v0
    secrets:
      GITHUB_SECRET: ${{ secrets.GITHUB_SECRET }}
```