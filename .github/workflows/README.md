# Common shared workflows

## Common workflow (Workflow)

This workflow runs a number of very common tasks that are useful in many repositories.

The tasks include:
- labelling pull requests based on commit messages using the conventional commits standard.

This workflow requires the following GitHub permissions:
```yaml
permissions:
  pull-requests: write
```

<!-- BEGIN WORKFLOW INPUT DOCS: common -->

### 🔧 Inputs

|Name      |Description                                                                                                            |Required|Type   |Default         |
|----------|-----------------------------------------------------------------------------------------------------------------------|--------|-------|----------------|
|`runs-on` |The type of runner to use for the workflow. Defaults to 'ubuntu-latest'. You can specify a different runner if needed. |No      |string |`ubuntu-latest` |

### 🔐 Secrets

_None_

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
